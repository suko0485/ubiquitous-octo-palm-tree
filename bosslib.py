"""Librería para definir jefes con modelo 3D por cajas + animaciones por keyframes.

Un mismo `Model` produce:
  * el JSON que lee el mod (src/main/resources/tarot_boss/<id>.json)
  * la textura PNG (UV empaquetados + pintura procedural)
  * previsualizaciones (turnaround PNG y GIF animado) con un rasterizador propio

Convenciones de AUTORÍA (para escribir cómodo):
  - posiciones y cajas en "y hacia ARRIBA"; x+ = izquierda de la criatura, z- = frente
  - un `Part` de primer nivel se ubica respecto al suelo; los hijos respecto al pivote de su padre
  - rotaciones en grados con la convención de Minecraft (rx<0 levanta algo hacia el frente,
    rz>0 abre el brazo derecho -x hacia afuera / rz<0 el izquierdo, ry>0 gira hacia la derecha)
El exportador convierte todo a la convención interna de Minecraft (y hacia abajo, origen a 24 px del suelo).
"""
import json, math, os, random
from pixlib import Img, mix, shade

FACE_KEYS = ("top", "bottom", "right", "front", "left", "back")
CHANNELS = ("x", "y", "z", "rx", "ry", "rz")


# ------------------------------------------------------------------ definición
class Box:
    def __init__(self, x, y, z, dx, dy, dz, mat, decor):
        for d in (dx, dy, dz):
            assert int(d) == d and d > 0, "las dimensiones de caja deben ser enteros > 0"
        self.x, self.y, self.z = x, y, z
        self.dx, self.dy, self.dz = int(dx), int(dy), int(dz)
        self.mat, self.decor = mat, decor
        self.u = self.v = 0


class Part:
    def __init__(self, name, parent, at, rot, p2, spin, look, walk):
        self.name, self.parent, self.at, self.rot = name, parent, at, rot
        self.p2, self.spin, self.look, self.walk = p2, spin, look, walk or []
        self.boxes = []

    def box(self, x, y, z, dx, dy, dz, mat, **decor):
        for k in decor:
            assert k in FACE_KEYS, k
        self.boxes.append(Box(x, y, z, dx, dy, dz, mat, decor))
        return self


class Clip:
    def __init__(self, length, loop=False):
        self.length, self.loop, self.tracks = length, loop, {}

    def k(self, part, ch, keys):
        """keys: [(t, valor[, ease])]; ease: 's' suave (por defecto), 'l' lineal, 'in' acelera, 'out' frena."""
        assert ch in CHANNELS, ch
        self.tracks.setdefault(part, {})[ch] = [(k[0], k[1], k[2] if len(k) > 2 else "s") for k in keys]
        return self


class Model:
    def __init__(self, mid, texture, mats, title=""):
        self.id, self.texture, self.mats, self.title = mid, texture, mats, title
        self.parts, self.by_name, self.clips = [], {}, {}
        self.tex_w = self.tex_h = 128

    def add(self, name, parent, at, rot=(0, 0, 0), p2=False, spin=(0, 0), look=False, walk=None):
        assert name not in self.by_name, name
        assert parent is None or parent in self.by_name, parent
        p = Part(name, parent, at, rot, p2, spin, look, walk)
        self.parts.append(p)
        self.by_name[name] = p
        return p

    def clip(self, name, length, loop=False):
        c = Clip(length, loop)
        self.clips[name] = c
        return c

    # ---- arcos de teselas (medias lunas, anillos, aros) ----
    def arc(self, prefix, parent, center, radius, a0, a1, n, widths, thick, mat, plane="xy", p2=False):
        """Coloca n teselas sobre un arco. plane 'xy' (de frente) o 'yz' (de perfil). Ángulos en grados, antihorario
        visto desde el frente (xy) / desde la derecha de la criatura (yz). widths: grosor radial por tesela."""
        cx, cy, cz = center
        step = (a1 - a0) / n
        chord = max(2, int(round(abs(math.radians(step)) * radius)) + 1)
        for i in range(n):
            ang = a0 + step * (i + .5)
            w = widths[min(len(widths) - 1, int(i * len(widths) / n))] if isinstance(widths, (list, tuple)) else widths
            c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))
            if plane == "xy":
                at = (cx + radius * c, cy + radius * s, cz)
                rot = (0, 0, -(ang + 90))
                p = self.add(f"{prefix}{i}", parent, at, rot, p2=p2)
                p.box(-chord / 2.0, -w / 2.0, -thick / 2.0, chord, w, thick, mat)
            else:
                at = (cx, cy + radius * s, cz + radius * c)
                rot = (ang + 90, 0, 0)
                p = self.add(f"{prefix}{i}", parent, at, rot, p2=p2)
                p.box(-thick / 2.0, -w / 2.0, -chord / 2.0, thick, w, chord, mat)
        return self


# ------------------------------------------------------------------ interpolación (misma lógica que BossModel.java)
def ease(kind, u):
    if kind == "l":
        return u
    if kind == "in":
        return u * u * u
    if kind == "out":
        return 1 - (1 - u) ** 3
    return u * u * (3 - 2 * u)


def sample(keys, t):
    if not keys:
        return 0.0
    if t <= keys[0][0]:
        return keys[0][1]
    if t >= keys[-1][0]:
        return keys[-1][1]
    for i in range(len(keys) - 1):
        a, b = keys[i], keys[i + 1]
        if a[0] <= t <= b[0]:
            u = (t - a[0]) / max(1e-6, b[0] - a[0])
            return a[1] + (b[1] - a[1]) * ease(b[2], u)
    return keys[-1][1]


# ------------------------------------------------------------------ exportación a convención Minecraft
def to_mc_part(m, p):
    if p.parent is None:
        o = (p.at[0], 24 - p.at[1], p.at[2])
    else:
        o = (p.at[0], -p.at[1], p.at[2])
    return o


def export(m):
    parts = []
    for p in m.parts:
        o = to_mc_part(m, p)
        parts.append({
            "name": p.name, "parent": p.parent,
            "o": [round(v, 3) for v in o], "r": [float(v) for v in p.rot],
            "boxes": [{"uv": [b.u, b.v], "p": [round(b.x, 3), round(-(b.y + b.dy), 3), round(b.z, 3)], "s": [b.dx, b.dy, b.dz]} for b in p.boxes],
            "p2": p.p2, "spin": list(p.spin), "look": p.look,
            "walk": [[ch, a, ph, bias] for (ch, a, ph, bias) in p.walk],
        })
    clips = {}
    for name, c in m.clips.items():
        tr = {}
        for part, chans in c.tracks.items():
            assert part in m.by_name, f"clip {name}: parte desconocida {part}"
            tr[part] = {}
            for ch, keys in chans.items():
                sign = -1 if ch == "y" else 1
                tr[part][ch] = [[k[0], round(k[1] * sign, 4), k[2]] for k in keys]
        clips[name] = {"len": c.length, "loop": c.loop, "tracks": tr}
    return {"id": m.id, "texture": m.texture, "tex_w": m.tex_w, "tex_h": m.tex_h, "parts": parts, "clips": clips}


# ------------------------------------------------------------------ UV + textura
def pack_uv(m, sizes=(64, 128, 256, 512)):
    rects = []
    for p in m.parts:
        for b in p.boxes:
            rects.append((b, 2 * (b.dx + b.dz), b.dy + b.dz))
    rects.sort(key=lambda r: (-r[2], -r[1]))
    for S in sizes:
        x = y = rowh = 0
        ok = True
        for b, w, h in rects:
            if x + w > S:
                x, y, rowh = 0, y + rowh, 0
            if rowh == 0:
                rowh = h
            if y + h > S or w > S:
                ok = False
                break
            b.u, b.v = x, y
            x += w
        if ok:
            m.tex_w = m.tex_h = S
            return S
    raise RuntimeError("no entra en la textura")


def face_rects(b):
    u, v, dx, dy, dz = b.u, b.v, b.dx, b.dy, b.dz
    return {"top": (u + dz, v, dx, dz), "bottom": (u + dz + dx, v, dx, dz), "right": (u, v + dz, dz, dy),
            "front": (u + dz, v + dz, dx, dy), "left": (u + dz + dx, v + dz, dz, dy), "back": (u + 2 * dz + dx, v + dz, dx, dy)}


FACE_LIGHT = {"top": 1.14, "front": 1.0, "left": .93, "right": .93, "back": .84, "bottom": .68}


def _noise(rnd, amt):
    return 1.0 + rnd.uniform(-amt, amt)


def paint_face(im, rect, face, mat, rnd, seed):
    x0, y0, w, h = rect
    kind = mat.get("kind", "flat")
    base, hi, lo = mat["c"], mat.get("hi", shade(mat["c"], 1.25)), mat.get("lo", shade(mat["c"], .6))
    nz = mat.get("noise", .05)
    fl = FACE_LIGHT[face]
    for j in range(h):
        for i in range(w):
            t = j / max(1, h - 1)
            if kind == "cloth":
                fold = math.sin((i + seed % 5) * 1.55) * .08 + (0.06 if (i + seed) % 4 == 0 else 0)
                c = mix(hi, lo, t * .75)
                f = 1 + fold
            elif kind == "metal":
                c = mix(hi, base, min(1, t * 1.6)) if t < .5 else mix(base, lo, (t - .5) * 1.3)
                f = 1.0
                if i == 0 or j == 0:
                    f = 1.18
                if i == w - 1 or j == h - 1:
                    f = .78
            elif kind == "stone":
                blk = ((i // 3) * 7 + (j // 3) * 13 + seed) % 5
                c = mix(base, hi, blk / 9.0) if blk % 2 else mix(base, lo, blk / 9.0)
                f = 1.0
            elif kind == "crystal":
                d = abs(i - w / 2.0) / max(1, w / 2.0) * .6 + abs(j - h / 2.0) / max(1, h / 2.0) * .4
                c = mix(hi, lo, min(1, d * 1.2))
                f = 1.0 + (0.12 if (i + j) % 5 == 0 else 0)
            elif kind == "glow":
                c = mix(hi, base, min(1, abs(i - w / 2.0) / max(1, w / 2.0)))
                f = 1.0
            elif kind == "feather":
                c = mix(hi, lo, t ** 1.3)
                f = 1.0 + (0.1 if i % 2 == 0 else -0.04)
            elif kind == "wisp":
                c = mix(hi, lo, t)
                f = 1.0 + (0.1 if (i + j * 2) % 7 == 0 else 0)
            else:
                c = mix(hi, base, t) if kind == "grad" else base
                f = 1.0
            f *= fl * _noise(rnd, nz)
            # borde: separa las piezas visualmente
            if w > 3 and h > 3 and (i == 0 or j == 0 or i == w - 1 or j == h - 1) and kind != "glow":
                f *= .86
            im.px(x0 + i, y0 + j, shade(c, f))


def paint_model(m, seed=1):
    im = Img(m.tex_w, m.tex_h)
    rnd = random.Random(seed)
    n = 0
    for p in m.parts:
        for b in p.boxes:
            mat = m.mats[b.mat]
            rects = face_rects(b)
            for f in FACE_KEYS:
                n += 1
                paint_face(im, rects[f], f, mat, rnd, n)
            for f, fn in b.decor.items():
                x0, y0, w, h = rects[f]
                fn(im, x0, y0, w, h)
    return im


# ------------------------------------------------------------------ utilidades de decoración
def dots(im, x0, y0, pts, col):
    for (i, j) in pts:
        im.px(x0 + i, y0 + j, col)


def hline(im, x0, y0, i0, i1, j, col):
    for i in range(i0, i1 + 1):
        im.px(x0 + i, y0 + j, col)


def vline(im, x0, y0, i, j0, j1, col):
    for j in range(j0, j1 + 1):
        im.px(x0 + i, y0 + j, col)


def cracks(im, x0, y0, w, h, seed, col, n=2, length=None):
    r = random.Random(seed)
    for _ in range(n):
        x, y = r.randint(0, max(0, w - 1)), r.randint(0, max(0, h // 3))
        for _s in range(length or h):
            im.px(x0 + x, y0 + y, col)
            y += 1
            x += r.choice((-1, 0, 0, 1))
            if x < 0 or x >= w or y >= h:
                break


# ------------------------------------------------------------------ poses (misma lógica que BossModel.java)
def pose(m, st):
    """st: dict(time, anim(str|None), anim_t, phase, walk_pos, walk_amp, look_yaw, look_pitch, death(float|None))
    devuelve {parte: (ox,oy,oz,rx,ry,rz, visible)} con rotaciones en grados."""
    out = {}
    for p in m.parts:
        o = to_mc_part(m, p)
        out[p.name] = [o[0], o[1], o[2], p.rot[0], p.rot[1], p.rot[2], True]

    def apply(clip, t):
        for part, chans in clip.tracks.items():
            e = out[part]
            for ch, keys in chans.items():
                v = sample(keys, t)
                if ch == "y":
                    v = -v
                e[CHANNELS.index(ch)] += v

    idle = m.clips.get("idle")
    if idle:
        apply(idle, st["time"] % idle.length)
    if st.get("anim") and st["anim"] in m.clips and 0 <= st["anim_t"] < m.clips[st["anim"]].length:
        apply(m.clips[st["anim"]], st["anim_t"])
    f = st.get("walk_pos", 0) * 0.6662
    amp = st.get("walk_amp", 0)
    for p in m.parts:
        e = out[p.name]
        for ch, a, ph, bias in p.walk:
            v = (a * math.sin(f + ph) + bias) * amp
            if ch == "y":
                v = -v
            e[CHANNELS.index(ch)] += v
        if p.spin[0] or p.spin[1]:
            e[4] += p.spin[0] * st["time"]
            e[5] += p.spin[1] * st["time"]
        if p.look:
            e[4] += st.get("look_yaw", 0)
            e[3] += st.get("look_pitch", 0)
        if p.p2 and st.get("phase", 1) < 2:
            e[6] = False
    if st.get("death") is not None and "death" in m.clips:
        apply(m.clips["death"], min(st["death"], m.clips["death"].length))
    return out


# ------------------------------------------------------------------ rasterizador de previsualización
def _rot(rx, ry, rz):
    cx, sx = math.cos(rx), math.sin(rx)
    cy, sy = math.cos(ry), math.sin(ry)
    cz, sz = math.cos(rz), math.sin(rz)
    RX = [[1, 0, 0], [0, cx, -sx], [0, sx, cx]]
    RY = [[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]]
    RZ = [[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]]

    def mm(a, b):
        return [[sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    return mm(RZ, mm(RY, RX))  # Rz * Ry * Rx (JOML rotationZYX)


def render(m, tex, st, yaw=0, pitch=12, scale=5.0, size=(320, 360), ss=2, bg=(26, 22, 40), center_y=26, label=None):
    import numpy as np
    from PIL import Image, ImageDraw
    W, H = size[0] * ss, size[1] * ss
    S = scale * ss
    buf = np.zeros((H, W, 3), np.float32)
    buf[:] = bg
    zbuf = np.full((H, W), -1e9, np.float32)
    texa = np.asarray(tex.convert("RGBA"), np.uint8)
    pz = pose(m, st)
    wm = {}  # mundo (modelo MC): (R, t)
    cy_, sy_ = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
    cp, sp = math.cos(math.radians(pitch)), math.sin(math.radians(pitch))
    light = np.array([-.35, .8, .5]); light /= np.linalg.norm(light)

    def view(pt):  # punto en espacio de modelo MC -> coordenadas de cámara (x der, y arriba, z hacia el espectador)
        mx, my, mz = pt
        X, Y, Z = mx, 24 - my - 0, -mz        # el modelo se dibuja con el pie en y=24
        Y = Y - center_y
        x1 = X * cy_ + Z * sy_
        z1 = -X * sy_ + Z * cy_
        y2 = Y * cp - z1 * sp
        z2 = Y * sp + z1 * cp
        return (x1, y2, z2)

    for p in m.parts:
        o = pz[p.name]
        if not o[6]:
            continue
        R = _rot(math.radians(o[3]), math.radians(o[4]), math.radians(o[5]))
        t = (o[0], o[1], o[2])
        if p.parent is not None:
            pR, pt = wm.get(p.parent, (None, None))
            if pR is None:      # padre oculto -> hijos ocultos
                continue
            R = [[sum(pR[i][k] * R[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
            t = tuple(sum(pR[i][k] * t[k] for k in range(3)) + pt[i] for i in range(3))
        wm[p.name] = (R, t)
        for b in p.boxes:
            x, y, z = b.x, -(b.y + b.dy), b.z
            f_, g, h = x + b.dx, y + b.dy, z + b.dz
            V = [(x, y, z), (f_, y, z), (f_, g, z), (x, g, z), (x, y, h), (f_, y, h), (f_, g, h), (x, g, h)]
            Wv = []
            for v in V:
                lx = sum(R[0][k] * v[k] for k in range(3)) + t[0]
                ly = sum(R[1][k] * v[k] for k in range(3)) + t[1]
                lz = sum(R[2][k] * v[k] for k in range(3)) + t[2]
                Wv.append(view((lx, ly, lz)))
            Wv = np.array(Wv)
            ctr = Wv.mean(axis=0)
            u, v0, dx, dy, dz = b.u, b.v, b.dx, b.dy, b.dz
            j, k, l, m_, n, o_ = u, u + dz, u + dz + dx, u + dz + dx + dx, u + dz + dx + dz, u + dz + dx + dz + dx
            pp, q, r = v0, v0 + dz, v0 + dz + dy
            faces = [([5, 4, 0, 1], (k, pp, l, q)), ([2, 3, 7, 6], (l, q, m_, pp)), ([0, 4, 7, 3], (j, q, k, r)),
                     ([1, 0, 3, 2], (k, q, l, r)), ([5, 1, 2, 6], (l, q, n, r)), ([4, 5, 6, 7], (n, q, o_, r))]
            for idx, (u1, v1, u2, v2) in faces:
                P = Wv[idx]
                uv = np.array([(u2, v1), (u1, v1), (u1, v2), (u2, v2)], np.float32)
                nrm = np.cross(P[1] - P[0], P[3] - P[0])
                nl = np.linalg.norm(nrm)
                if nl < 1e-6:
                    continue
                nrm /= nl
                if np.dot(nrm, P.mean(axis=0) - ctr) < 0:
                    nrm = -nrm
                shade_f = .55 + .55 * max(0.0, float(np.dot(nrm, light))) + .12 * max(0.0, float(nrm[2]))
                px = np.stack([W / 2 + P[:, 0] * S, H / 2 - P[:, 1] * S], axis=1)
                e1, e2 = px[1] - px[0], px[3] - px[0]
                det = e1[0] * e2[1] - e1[1] * e2[0]
                if abs(det) < 1e-4:
                    continue
                x0i, x1i = int(max(0, math.floor(px[:, 0].min()))), int(min(W - 1, math.ceil(px[:, 0].max())))
                y0i, y1i = int(max(0, math.floor(px[:, 1].min()))), int(min(H - 1, math.ceil(px[:, 1].max())))
                if x1i < x0i or y1i < y0i:
                    continue
                gx, gy = np.meshgrid(np.arange(x0i, x1i + 1) + .5, np.arange(y0i, y1i + 1) + .5)
                dxg, dyg = gx - px[0, 0], gy - px[0, 1]
                a = (dxg * e2[1] - dyg * e2[0]) / det
                bb = (e1[0] * dyg - e1[1] * dxg) / det
                mask = (a >= 0) & (a <= 1) & (bb >= 0) & (bb <= 1)
                if not mask.any():
                    continue
                z = P[0, 2] + a * (P[1, 2] - P[0, 2]) + bb * (P[3, 2] - P[0, 2])
                tu = uv[0, 0] + a * (uv[1, 0] - uv[0, 0]) + bb * (uv[3, 0] - uv[0, 0])
                tv = uv[0, 1] + a * (uv[1, 1] - uv[0, 1]) + bb * (uv[3, 1] - uv[0, 1])
                tx = np.clip(np.floor(tu), min(u1, u2), max(u1, u2) - 1).astype(int)
                ty = np.clip(np.floor(tv), min(v1, v2), max(v1, v2) - 1).astype(int)
                col = texa[ty, tx]
                zb = zbuf[y0i:y1i + 1, x0i:x1i + 1]
                upd = mask & (z > zb) & (col[..., 3] > 8)
                if not upd.any():
                    continue
                sub = buf[y0i:y1i + 1, x0i:x1i + 1]
                sub[upd] = np.clip(col[..., :3][upd].astype(np.float32) * shade_f, 0, 255)
                zb[upd] = z[upd]
    img = Image.fromarray(buf.astype(np.uint8)).resize(size, Image.LANCZOS)
    if label:
        d = ImageDraw.Draw(img)
        d.text((8, 6), label, fill=(235, 225, 255))
    return img
