"""Biblioteca de ilustración vectorial (Pillow) para las cartas: estilo Rider-Waite con contornos de tinta.
Todo se dibuja con supersampling (S) y se reduce con LANCZOS, así los bordes quedan suaves."""
import math
from PIL import Image, ImageDraw, ImageFont, ImageChops

S = 6                      # supersampling del área de arte
AW, AH = 66, 92            # tamaño del área de arte en píxeles finales

INK = (30, 20, 26)
SKIN = (240, 200, 160); SKIN_D = (214, 164, 124)
YEL = (250, 214, 84); YEL_L = (255, 240, 160); YEL_D = (222, 170, 40)
RED = (200, 44, 44); RED_D = (140, 26, 34)
BLU = (52, 92, 176); BLU_D = (30, 52, 120); BLU_L = (130, 180, 235); SKY = (150, 205, 235)
GRN = (70, 150, 76); GRN_D = (38, 100, 52); GRN_L = (150, 200, 100)
PUR = (124, 64, 156); PUR_D = (80, 36, 108)
ORA = (236, 142, 52); WHT = (250, 246, 236); GRY = (150, 150, 160); GRY_D = (90, 90, 102); GRY_L = (200, 200, 208)
BRN = (130, 86, 50); BRN_D = (84, 54, 32); BLK = (26, 22, 34); GOLD = (232, 180, 50); GOLD_D = (168, 118, 26)
PINK = (236, 140, 170)


def mix(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

def shade(c, f):
    return tuple(max(0, min(255, int(v * f))) for v in c[:3])


class Art:
    def __init__(self, w=AW, h=AH):
        self.w, self.h = w, h
        self.im = Image.new("RGBA", (w * S, h * S), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.im)

    def P(self, pts):
        return [(x * S, y * S) for x, y in pts]

    # ---- primitivas -------------------------------------------------
    def poly(self, pts, fill, ol=INK, w=.7):
        if fill is not None:
            self.d.polygon(self.P(pts), fill=fill)
        if ol:
            self.d.line(self.P(list(pts) + [pts[0]]), fill=ol, width=max(1, int(w * S)), joint="curve")

    def ell(self, cx, cy, rx, ry=None, fill=WHT, ol=INK, w=.7):
        ry = rx if ry is None else ry
        box = [(cx - rx) * S, (cy - ry) * S, (cx + rx) * S, (cy + ry) * S]
        self.d.ellipse(box, fill=fill, outline=ol if ol else None, width=max(1, int(w * S)))

    def rect(self, x0, y0, x1, y1, fill, ol=INK, w=.7):
        self.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], fill, ol, w)

    def line(self, pts, col=INK, w=.8, round_=True):
        pts = list(pts)
        self.d.line(self.P(pts), fill=col, width=max(1, int(w * S)), joint="curve")
        if round_:
            r = w * S / 2
            for (x, y) in (pts[0], pts[-1]):
                self.d.ellipse([x * S - r, y * S - r, x * S + r, y * S + r], fill=col)

    def limb(self, p0, p1, w, col, ol=INK):
        """Brazo/pierna gruesa con contorno."""
        if ol:
            self.line([p0, p1], ol, w + 1.2)
        self.line([p0, p1], col, w)

    def arc(self, cx, cy, r, a0, a1, col=INK, w=.8):
        self.d.arc([(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S], a0, a1, fill=col, width=max(1, int(w * S)))

    def curve(self, pts, col=INK, w=.8, n=24):
        """Spline de Catmull-Rom sencilla."""
        pts = [pts[0]] + list(pts) + [pts[-1]]
        out = []
        for i in range(1, len(pts) - 2):
            p0, p1, p2, p3 = pts[i - 1], pts[i], pts[i + 1], pts[i + 2]
            for k in range(n):
                t = k / n
                out.append(tuple(.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t * t
                                       + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t ** 3) for j in (0, 1)))
        out.append(pts[-2])
        self.line(out, col, w)
        return out

    def blob(self, pts, fill, ol=INK, w=.7, n=10):
        """Polígono suavizado (curva cerrada)."""
        pts = list(pts)
        ext = pts[-1:] + pts + pts[:2]
        out = []
        for i in range(1, len(ext) - 2):
            p0, p1, p2, p3 = ext[i - 1], ext[i], ext[i + 1], ext[i + 2]
            for k in range(n):
                t = k / n
                out.append(tuple(.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t * t
                                       + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t ** 3) for j in (0, 1)))
        self.poly(out, fill, ol, w)

    def grad(self, y0, y1, c0, c1, x0=0, x1=None):
        x1 = self.w if x1 is None else x1
        for y in range(int(y0 * S), int(y1 * S)):
            t = (y - y0 * S) / max(1, (y1 - y0) * S)
            self.d.line([(x0 * S, y), (x1 * S, y)], fill=mix(c0, c1, t))

    def glow(self, cx, cy, r, col, alpha=200, power=1.6):
        n = int(r * 2 * S)
        g = Image.radial_gradient("L").resize((n, n))
        g = g.point(lambda v: int(alpha * max(0, (1 - v / 255)) ** power))
        layer = Image.new("RGBA", (n, n), col + (255,))
        layer.putalpha(g)
        self.im.alpha_composite(layer, (int(cx * S - n / 2), int(cy * S - n / 2)))
        self.d = ImageDraw.Draw(self.im)

    def star(self, cx, cy, r, fill=GOLD, pts=5, inner=.45, rot=-90, ol=INK, w=.5):
        P = []
        for i in range(pts * 2):
            rr = r if i % 2 == 0 else r * inner
            a = math.radians(rot + i * 180 / pts)
            P.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
        self.poly(P, fill, ol, w)

    def dots(self, pts, r, col):
        for (x, y) in pts:
            self.ell(x, y, r, r, col, None)

    def cross_hatch(self, poly_pts, col, step=1.6, w=.3):
        """Sombreado con rayas diagonales dentro de un polígono (recortado con máscara)."""
        m = Image.new("L", self.im.size, 0)
        ImageDraw.Draw(m).polygon(self.P(poly_pts), fill=255)
        h = Image.new("RGBA", self.im.size, (0, 0, 0, 0))
        hd = ImageDraw.Draw(h)
        k = -self.h
        while k < self.w + self.h:
            hd.line([(k * S, self.h * S), ((k + self.h) * S, 0)], fill=col + (255,), width=max(1, int(w * S)))
            k += step
        h.putalpha(ImageChops.multiply(h.getchannel("A"), m))
        self.im.alpha_composite(h)
        self.d = ImageDraw.Draw(self.im)

    def shadow_poly(self, pts, col, alpha=90):
        """Sombra translúcida sobre una forma (mismo polígono ya dibujado)."""
        layer = Image.new("RGBA", self.im.size, (0, 0, 0, 0))
        ImageDraw.Draw(layer).polygon(self.P(pts), fill=col + (alpha,))
        self.im.alpha_composite(layer)
        self.d = ImageDraw.Draw(self.im)

    # ---- elementos comunes -----------------------------------------
    def head(self, cx, cy, r=3.6, skin=SKIN, hair=None, face="r", hair_style="short"):
        """Cabeza con pelo. face: 'r' mira a la derecha, 'l' izquierda, 'f' de frente."""
        if hair and hair_style == "long":
            self.poly([(cx - r - .6, cy - r * .2), (cx - r * .9, cy + r * 2.4), (cx + r * .9, cy + r * 2.4), (cx + r + .6, cy - r * .2)], hair, INK, .6)
        self.ell(cx, cy, r, r * 1.12, skin, INK, .6)
        if hair:
            self.d.pieslice([(cx - r - .4) * S, (cy - r * 1.18) * S, (cx + r + .4) * S, (cy + r * .9) * S], 180, 360, fill=hair)
            self.d.arc([(cx - r - .4) * S, (cy - r * 1.18) * S, (cx + r + .4) * S, (cy + r * .9) * S], 180, 360, fill=INK, width=int(.6 * S))
        dx = {"r": r * .35, "l": -r * .35, "f": 0}[face]
        if face == "f":
            self.dots([(cx - r * .38, cy + r * .1), (cx + r * .38, cy + r * .1)], .33, INK)
        else:
            self.dots([(cx + dx + (r * .2 if face == "r" else -r * .2), cy + r * .1)], .33, INK)
        self.line([(cx + dx - r * .25, cy + r * .62), (cx + dx + r * .25, cy + r * .62)], (170, 80, 80), .35, False)

    def halo(self, cx, cy, r, col=YEL_L):
        self.glow(cx, cy, r * 1.7, col, 180)
        self.ell(cx, cy, r, r, None, GOLD_D, .5)

    def hand(self, x, y, r=1.2, skin=SKIN):
        self.ell(x, y, r, r, skin, INK, .45)

    def cloud(self, cx, cy, w=14, col=WHT, ol=GRY):
        for dx, dy, r in ((-.3, .1, .28), (0, -.1, .34), (.3, .05, .3), (.05, .12, .3)):
            self.ell(cx + dx * w, cy + dy * w * .5, r * w * .5, r * w * .38, col, None)
        self.line([(cx - w * .45, cy + w * .09), (cx + w * .45, cy + w * .09)], ol, .4, False)

    def mountain(self, pts, col, snow=None, ol=INK):
        self.poly(pts, col, ol, .6)

    def sun(self, cx, cy, r, rays=16, col=YEL, face=True):
        self.glow(cx, cy, r * 2.2, YEL_L, 170)
        for k in range(rays):
            a = k * 2 * math.pi / rays
            a2, a3 = a - math.pi / rays * .6, a + math.pi / rays * .6
            L = r * (1.75 if k % 2 == 0 else 1.45)
            self.poly([(cx + math.cos(a2) * r, cy + math.sin(a2) * r), (cx + math.cos(a) * L, cy + math.sin(a) * L),
                       (cx + math.cos(a3) * r, cy + math.sin(a3) * r)], ORA if k % 2 else YEL_D, INK, .4)
        self.ell(cx, cy, r, r, col, INK, .6)
        if face:
            self.dots([(cx - r * .32, cy - r * .08), (cx + r * .32, cy - r * .08)], r * .09, INK)
            self.line([(cx - r * .25, cy + r * .38), (cx + r * .25, cy + r * .38)], ORA, .4, False)

    def crescent(self, cx, cy, r, col=WHT, ol=INK, off=.45):
        self.ell(cx, cy, r, r, col, ol, .6)
        self.ell(cx + r * off, cy - r * .08, r * .86, r * .9, None, None)
        # recorte: pintamos el "mordisco" con transparencia
        m = Image.new("L", self.im.size, 255)
        ImageDraw.Draw(m).ellipse([(cx + r * off - r * .86) * S, (cy - r * .08 - r * .9) * S, (cx + r * off + r * .86) * S, (cy - r * .08 + r * .9) * S], fill=0)
        # el recorte solo debe afectar la zona del disco; se restringe con caja
        box = Image.new("L", self.im.size, 255)
        ImageDraw.Draw(box).rectangle([(cx - r - 1) * S, (cy - r - 1) * S, (cx + r + 1) * S, (cy + r + 1) * S], fill=0)
        keep = ImageChops.lighter(m, box)
        a = self.im.getchannel("A")
        self.im.putalpha(ImageChops.multiply(a, keep))
        self.d = ImageDraw.Draw(self.im)
        self.arc(cx, cy, r, 100, 260, ol, .6)
        self.arc(cx + r * off, cy - r * .08, r * .86, -80, 80, ol, .6)

    def pillar(self, x0, x1, y0, y1, col, cap=None):
        cap = cap or shade(col, 1.15)
        self.rect(x0, y0, x1, y1, col, INK, .6)
        self.rect(x0 - .8, y0, x1 + .8, y0 + 2.4, cap, INK, .5)
        self.rect(x0 - .8, y1 - 2, x1 + .8, y1, cap, INK, .5)
        self.line([((x0 + x1) / 2, y0 + 2.4), ((x0 + x1) / 2, y1 - 2)], shade(col, .75), .35, False)

    def tree(self, x, y, h, crown_r, trunk=BRN, leaf=GRN):
        self.poly([(x - 1.2, y), (x - .7, y - h), (x + .7, y - h), (x + 1.2, y)], trunk, INK, .5)
        for dx, dy, r in ((-crown_r * .5, 0, .62), (crown_r * .5, 0, .62), (0, -crown_r * .4, .7)):
            self.ell(x + dx, y - h + dy, crown_r * r, crown_r * r * .85, leaf, INK, .5)

    def finish(self):
        return self.im.resize((self.w, self.h), Image.LANCZOS)
