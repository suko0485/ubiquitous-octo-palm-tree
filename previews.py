"""Previsualizaciones de los jefes: turnaround PNG y GIF con todas las animaciones (usa el rasterizador de bosslib)."""
import os, sys
from PIL import Image, ImageDraw
import bosslib as L

OUT = "previews"
SCALE = {"hierophant": 4.3, "moon_shadow": 4.6, "last_judgement": 3.5}
CENTER = {"hierophant": 26, "moon_shadow": 26, "last_judgement": 34}


def tex_of(m):
    return Image.open(f"src/main/resources/assets/tarot/textures/entity/{m.id}.png")


def state(**kw):
    s = dict(time=0, anim=None, anim_t=0, phase=1, walk_pos=0, walk_amp=0, look_yaw=0, look_pitch=0, death=None)
    s.update(kw)
    return s


def turnaround(m, size=(280, 340)):
    tex = tex_of(m)
    views = [("frente", 0), ("3/4", 38), ("perfil", 90), ("espalda", 180)]
    sheet = Image.new("RGB", (size[0] * 4, size[1] * 2), (26, 22, 40))
    for row, ph in enumerate((1, 2)):
        for i, (lab, yaw) in enumerate(views):
            im = L.render(m, tex, state(time=20, phase=ph), yaw=yaw, pitch=10, scale=SCALE[m.id], size=size,
                          center_y=CENTER[m.id], label=f"{m.title} · fase {ph} · {lab}")
            sheet.paste(im, (i * size[0], row * size[1]))
    sheet.save(f"{OUT}/{m.id}_turnaround.png")


def timeline(m):
    seq = []
    seq += [("idle", dict(time=t), 1) for t in range(0, 80, 2)]
    seq += [("caminar", dict(time=t, walk_pos=t * .9, walk_amp=1), 1) for t in range(0, 56, 2)]
    for name, ln in (("slam", 40), ("cast", 34), ("summon", 36)):
        seq += [(f"{name} (golpe/hechizo)", dict(time=t, anim=name, anim_t=t), 1) for t in range(0, ln + 2, 2)]
    seq += [("enrage · fase 2", dict(time=t, anim="enrage", anim_t=t), 2) for t in range(0, 46, 2)]
    seq += [("special · fase 2", dict(time=t, anim="special", anim_t=t), 2) for t in range(0, 48, 2)]
    seq += [("muerte", dict(time=t, death=t), 2) for t in range(0, 22, 2)]
    return seq


def gif(m, size=(300, 350), yaw=28):
    tex = tex_of(m)
    frames = []
    for label, kw, ph in timeline(m):
        st = state(phase=ph, **kw)
        im = L.render(m, tex, st, yaw=yaw, pitch=9, scale=SCALE[m.id], size=size, center_y=CENTER[m.id], label=f"{m.title} · {label}")
        frames.append(im.convert("P", palette=Image.ADAPTIVE, colors=128))
    frames[0].save(f"{OUT}/{m.id}_animaciones.gif", save_all=True, append_images=frames[1:], duration=100, loop=0, optimize=True)


def run(models, only=None, gifs=True):
    os.makedirs(OUT, exist_ok=True)
    for m in models:
        if only and m.id != only:
            continue
        turnaround(m); action_sheet(m)
        if gifs:
            gif(m)
        print("preview", m.id)


def action_sheet(m, size=(240, 300)):
    """Fotogramas clave de cada animación en una sola hoja."""
    tex = tex_of(m)
    shots = [("idle", dict(time=40), 1), ("caminar", dict(time=20, walk_pos=7, walk_amp=1), 1),
             ("slam: alza", dict(anim="slam", anim_t=26), 1), ("slam: golpe", dict(anim="slam", anim_t=32), 1),
             ("cast", dict(anim="cast", anim_t=24), 1), ("summon", dict(anim="summon", anim_t=20), 1),
             ("special", dict(anim="special", anim_t=30), 2), ("special: golpe", dict(anim="special", anim_t=37), 2),
             ("enrage", dict(anim="enrage", anim_t=20), 2), ("muerte", dict(death=18), 2)]
    cols = 5
    sheet = Image.new("RGB", (size[0] * cols, size[1] * 2), (26, 22, 40))
    for i, (lab, kw, ph) in enumerate(shots):
        kw = dict(kw); kw.setdefault("time", kw.get("anim_t", 0))
        im = L.render(m, tex, state(phase=ph, **kw), yaw=24, pitch=9, scale=SCALE[m.id] * .8, size=size, center_y=CENTER[m.id], label=f"{m.title} · {lab}")
        sheet.paste(im, ((i % cols) * size[0], (i // cols) * size[1]))
    sheet.save(f"{OUT}/{m.id}_acciones.png")


if __name__ == "__main__":
    import gen_bosses
    models = gen_bosses.main()
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    run(models, only=args[0] if args else None, gifs="--nogif" not in sys.argv)
