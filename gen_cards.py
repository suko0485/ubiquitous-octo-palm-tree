#!/usr/bin/env python3
"""Genera las 22 cartas del Tarot (128x128, ilustración estilo Rider-Waite) con marco por rareza.
Requiere Pillow + numpy.  Uso:  python3 gen_cards.py [--sheet hoja.png]
(gen_assets.py lo llama automáticamente si Pillow está instalado)."""
import sys, os
from PIL import Image, ImageDraw, ImageFont, ImageChops
import numpy as np
import card_data as D
from rw_lib import Art, AW, AH, mix, shade, INK
import rw_scenes1, rw_scenes2, rw_scenes3

SCENES = {}
for m in (rw_scenes1, rw_scenes2, rw_scenes3):
    for k, v in vars(m).items():
        if callable(v) and not k.startswith("_") and k in {c[0] for c in D.CARDS} | {"star_"}:
            SCENES[k] = v
if "star_" in SCENES: SCENES["star"] = SCENES.pop("star_")

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
def font(name, px):
    for p in (FONT_DIR + name, name):
        try: return ImageFont.truetype(p, px)
        except OSError: pass
    return ImageFont.load_default()

SZ = 128; Q = 4                     # lienzo final y supersampling del marco
CX0, CY0, CX1, CY1 = 26, 2, 101, 125   # carta (inclusivo): 76 x 124
WX, WY = 31, 16                     # esquina del área de arte (66 x 92)

METAL = {  # (claro, medio, oscuro, gema)
    "common":   ((196, 196, 204), (150, 150, 160), (92, 92, 104), (176, 180, 190)),
    "uncommon": ((226, 168, 108), (176, 120, 66), (108, 66, 34), (96, 220, 130)),
    "rare":     ((226, 236, 250), (170, 190, 224), (86, 106, 150), (90, 160, 255)),
    "epic":     ((255, 232, 130), (232, 184, 56), (140, 92, 20), (255, 90, 210)),
}
CREAM = (246, 236, 208)

def frame_layer(cid, numeral, name, base, rarity):
    L = Image.new("RGBA", (SZ * Q, SZ * Q), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    lt, md, dk, gem = METAL[rarity]
    def R(x0, y0, x1, y1, r, fill=None, ol=None, w=1):
        d.rounded_rectangle([x0 * Q, y0 * Q, (x1 + 1) * Q - 1, (y1 + 1) * Q - 1], r * Q, fill=fill, outline=ol, width=int(w * Q))
    R(CX0, CY0, CX1, CY1, 4, INK)                                   # silueta
    # marco metálico con degradado vertical + biselado
    mtl = Image.new("RGBA", L.size, (0, 0, 0, 0)); md_ = ImageDraw.Draw(mtl)
    for y in range((CY0 + 1) * Q, (CY1) * Q):
        t = (y - (CY0 + 1) * Q) / ((CY1 - CY0 - 1) * Q)
        md_.line([((CX0 + 1) * Q, y), ((CX1) * Q, y)], fill=mix(lt, dk, t) + (255,))
    msk = Image.new("L", L.size, 0)
    ImageDraw.Draw(msk).rounded_rectangle([(CX0 + 1) * Q, (CY0 + 1) * Q, (CX1) * Q + Q - 1, (CY1) * Q + Q - 1], 3 * Q, fill=255)
    L.paste(mtl, (0, 0), msk); d = ImageDraw.Draw(L)
    R(CX0 + 1, CY0 + 1, CX1 - 1, CY1 - 1, 3, None, shade(dk, .6), .5)
    # pergamino interior con leve tinte del color de la carta
    paper = mix(CREAM, base, .10)
    R(CX0 + 3, CY0 + 3, CX1 - 3, CY1 - 3, 2, paper, INK, .6)
    # banda superior (numeral) y banda inferior (nombre): línea de tinta + filete dorado
    ty0, ty1 = CY0 + 4, WY - 2
    by0, by1 = WY + AH + 1, CY1 - 4
    d.rectangle([(WX - 1) * Q, (WY - 1) * Q, (WX + AW) * Q - 1, (WY + AH) * Q - 1], outline=INK, width=int(.9 * Q))
    d.rectangle([(WX - 2) * Q, (WY - 2) * Q, (WX + AW + 1) * Q - 1, (WY + AH + 1) * Q - 1], outline=mix(md, dk, .3), width=int(.5 * Q))
    # numeral romano
    f = font("DejaVuSerif-Bold.ttf", 7 * Q)
    tw = d.textlength(numeral, font=f)
    d.text((64 * Q - tw / 2, (ty0 + 5.4) * Q), numeral, font=f, fill=INK, anchor="ls")
    # gemas de rareza flanqueando el numeral + rombos decorativos
    for gx in (CX0 + 9, CX1 - 9):
        gy = ty0 + 3.6
        d.polygon([(gx * Q, (gy - 2.2) * Q), ((gx + 1.8) * Q, gy * Q), (gx * Q, (gy + 2.2) * Q), ((gx - 1.8) * Q, gy * Q)], fill=gem, outline=INK)
        d.point((int(gx * Q - Q * .5), int((gy - .7) * Q)), fill=(255, 255, 255))
    # nombre (se achica para caber)
    txt = name.upper(); size = 6.4 * Q
    while True:
        f = font("DejaVuSerifCondensed-Bold.ttf", int(size))
        w = d.textlength(txt, font=f)
        if w <= (AW - 2) * Q or size < 3.6 * Q: break
        size -= .25 * Q
    d.text((64 * Q - w / 2, (by1 - 1.6) * Q), txt, font=f, fill=INK, anchor="ls")
    # adornos del marco por rareza
    if rarity in ("rare", "epic"):
        for (x, y) in ((CX0 + 1, CY0 + 1), (CX1 - 1, CY0 + 1), (CX0 + 1, CY1 - 1), (CX1 - 1, CY1 - 1)):
            d.ellipse([(x - 1.3) * Q, (y - 1.3) * Q, (x + 1.3) * Q, (y + 1.3) * Q], fill=gem if rarity == "rare" else (255, 250, 210), outline=INK)
    if rarity == "epic":
        for y in range(CY0 + 14, CY1 - 12, 6):
            for x in (CX0 + 1.6, CX1 - 1.6): d.ellipse([(x - .55) * Q, (y - .55) * Q, (x + .55) * Q, (y + .55) * Q], fill=(255, 250, 210))
        d.rectangle([(CX0 + 2) * Q, (CY0 + 2) * Q, (CX1 - 1) * Q - 1, (CY1 - 1) * Q - 1], outline=(150, 70, 190), width=int(.5 * Q))
    return L.resize((SZ, SZ), Image.LANCZOS)

def shine(art, rarity):
    """Brillo holográfico suave en cartas raras/épicas."""
    if rarity not in ("rare", "epic"): return art
    w, h = art.size
    ys, xs = np.mgrid[0:h, 0:w]
    band = np.clip(1 - np.abs((xs + ys * .6) - (w * 1.0)) / 9, 0, 1)
    a = (band * (50 if rarity == "rare" else 70)).astype(np.uint8)
    lay = Image.new("RGBA", art.size, (255, 255, 255, 0)); lay.putalpha(Image.fromarray(a))
    out = art.copy(); out.alpha_composite(lay)
    return out

def vignette(art):
    w, h = art.size
    ys, xs = np.mgrid[0:h, 0:w]
    r = np.hypot((xs - w / 2) / (w / 2), (ys - h / 2) / (h / 2))
    a = (np.clip(r - .75, 0, 1) * 110).astype(np.uint8)
    lay = Image.new("RGBA", art.size, (20, 10, 30, 0)); lay.putalpha(Image.fromarray(a))
    out = art.copy(); out.alpha_composite(lay)
    return out

def card_image(cid, numeral, name, base, rarity):
    art = Art()
    if cid in SCENES: SCENES[cid](art)
    img = vignette(shine(art.finish(), rarity))
    canvas = Image.new("RGBA", (SZ, SZ), (0, 0, 0, 0))
    canvas.alpha_composite(frame_layer(cid, numeral, name, base, rarity))
    # fondo opaco bajo el arte (por si la escena deja huecos) y arte encima
    canvas.alpha_composite(Image.new("RGBA", (AW, AH), (30, 24, 40, 255)), (WX, WY))
    canvas.alpha_composite(img, (WX, WY))
    return canvas

def run(outdir, sheet=None):
    os.makedirs(outdir, exist_ok=True)
    ims = []
    for (cid, num, es, en, *_r) in D.CARDS:
        base, rar = _r[-2], _r[-1]
        im = card_image(cid, num, es, base, rar)
        im.save(f"{outdir}/card_{cid}.png"); ims.append(im)
    if sheet:
        k = 3; cols = 6; rows = 4
        sh = Image.new("RGBA", (cols * SZ * k // 1 * 1, rows * SZ * k), (46, 40, 58, 255))
        for i, im in enumerate(ims):
            big = im.crop((CX0 - 2, CY0 - 1, CX1 + 3, CY1 + 2)).resize(((CX1 - CX0 + 5) * k, (CY1 - CY0 + 3) * k), Image.NEAREST)
            sh.alpha_composite(big, ((i % cols) * SZ * k + 10, (i // cols) * SZ * k + 4))
        sh.convert("RGB").save(sheet)
    return len(ims)

if __name__ == "__main__":
    out = "src/main/resources/assets/tarot/textures/item"
    sheet = sys.argv[sys.argv.index("--sheet") + 1] if "--sheet" in sys.argv else None
    if "--preview" in sys.argv:
        out = os.path.join(os.environ.get("TMPDIR", "/tmp"), "cards_preview")
    print("cartas generadas:", run(out, sheet))
