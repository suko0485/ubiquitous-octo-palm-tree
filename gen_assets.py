#!/usr/bin/env python3
"""Genera TODAS las texturas (32x32), modelos, lang, recetas y logros del mod.  Uso:  python3 gen_assets.py"""
import os, random, math
from pixlib import Img, mix, shade
from icons import ICONS, W, CR, GO, GD, DK, heart, star, crescent
import card_data as D
import gen_data

R = "src/main/resources"; A = f"{R}/assets/tarot"
for d in ("textures/item", "textures/block", "models/item", "models/block", "items", "blockstates", "lang"):
    os.makedirs(f"{A}/{d}", exist_ok=True)

FONT = {"0": ["111", "101", "101", "101", "111"], "I": ["111", "010", "010", "010", "111"],
        "V": ["101", "101", "101", "010", "010"], "X": ["101", "101", "010", "101", "101"]}
def text(im, s, cx, y, c):
    wdt = len(s) * 4 - 1; x0 = int(cx - wdt / 2)
    for i, ch in enumerate(s):
        for r, row in enumerate(FONT[ch]):
            for k, b in enumerate(row):
                if b == "1": im.px(x0 + i * 4 + k, y + r, c)

RARITY = {"common": (0.0, 0), "uncommon": (0.15, 14), "rare": (0.3, 26), "epic": (0.5, 42)}

def card(cid, numeral, base, rarity):
    im = Img(); rnd = random.Random(cid)
    glow, stars = RARITY[rarity]
    top = shade(base, .35); bot = shade(base, .95)
    X0, X1, Y0, Y1 = 3, 28, 1, 30
    # fondo cósmico con degradado
    for y in range(Y0, Y1 + 1):
        for x in range(X0, X1 + 1):
            t = (y - Y0) / (Y1 - Y0)
            c = mix(top, bot, t)
            if rnd.random() < .04: c = shade(c, 1.25)
            im.px(x, y, c)
    for _ in range(stars + 6):
        x, y = rnd.randint(X0 + 2, X1 - 2), rnd.randint(Y0 + 2, Y1 - 2)
        im.px(x, y, mix(W, base, .3))
    # marcos: oscuro externo, dorado, interior sombreado
    outline = (60, 38, 8)
    im.frame(X0, Y0, X1, Y1, outline)
    im.frame(X0 + 1, Y0 + 1, X1 - 1, Y1 - 1, GO)
    im.frame(X0 + 2, Y0 + 2, X1 - 2, Y1 - 2, GD)
    for x in range(X0 + 1, X1): im.px(x, Y0 + 1, (255, 236, 150))      # luz arriba
    for y in range(Y0 + 1, Y1): im.px(X0 + 1, y, (255, 226, 130))
    for x in range(X0 + 1, X1): im.px(x, Y1 - 1, (150, 104, 24))        # sombra abajo
    for y in range(Y0 + 1, Y1): im.px(X1 - 1, y, (150, 104, 24))
    # esquinas ornamentadas
    for (cx, cy) in ((X0 + 1, Y0 + 1), (X1 - 1, Y0 + 1), (X0 + 1, Y1 - 1), (X1 - 1, Y1 - 1)):
        im.px(cx, cy, (255, 250, 200))
    # panel del ícono con halo
    px0, py0, px1, py1 = 6, 4, 25, 23
    for y in range(py0, py1 + 1):
        for x in range(px0, px1 + 1):
            d = math.hypot(x - 15.5, y - 13.5) / 12
            c = mix(shade(base, 1.35 + glow), shade(base, .22), min(1, d))
            im.px(x, y, c)
    im.frame(px0 - 1, py0 - 1, px1 + 1, py1 + 1, shade(GD, .8)); 
    im.px(px0 - 1, py0 - 1, GO); im.px(px1 + 1, py0 - 1, GO); im.px(px0 - 1, py1 + 1, GO); im.px(px1 + 1, py1 + 1, GO)
    ICONS[cid](im, base)
    # placa del numeral
    im.rect(6, 25, 25, 28, (30, 18, 44)); im.frame(5, 24, 26, 29, GD)
    text(im, numeral, 15.5, 25 if len(numeral) < 6 else 25, GO)
    # gema de rareza
    gem = {"common": (170, 170, 170), "uncommon": (90, 220, 120), "rare": (90, 160, 255), "epic": (255, 90, 200)}[rarity]
    im.px(15, 3, gem); im.px(16, 3, gem)
    return im

def sparkle(im, cx, cy, c, r=2):
    im.px(cx, cy, W)
    for k in range(1, r + 1):
        for d in ((k, 0), (-k, 0), (0, k), (0, -k)): im.px(cx + d[0], cy + d[1], c if k == 1 else shade(c, .7))

def item_stardust():
    im = Img(); sparkle(im, 16, 14, (190, 160, 255), 5); sparkle(im, 8, 8, GO, 2); sparkle(im, 24, 21, GO, 3); sparkle(im, 22, 7, (255, 255, 255), 1)
    sparkle(im, 10, 23, (200, 180, 255), 2); im.disc(16, 14, 2, W); return im
def item_shard():
    im = Img(); c = (120, 190, 255)
    im.poly([(16, 3), (22, 12), (19, 28), (13, 28), (10, 12)], c); im.poly([(16, 3), (22, 12), (16, 14)], (200, 235, 255)); im.poly([(16, 14), (22, 12), (19, 28)], shade(c, .7))
    im.poly([(10, 12), (16, 14), (13, 28)], shade(c, .85)); im.line(16, 3, 16, 14, W); im.frame(0, 0, 0, 0, c); im.px(14, 9, W); sparkle(im, 25, 7, GO, 2); return im
def item_tear():
    im = Img()
    for y in range(4, 27):
        w = 0 if y < 4 else (y - 4) * 0.45 if y < 15 else math.sqrt(max(0, 8.3 ** 2 - (y - 19) ** 2))
        for x in range(int(16 - w), int(16 + w) + 1): im.px(x, y, mix((60, 120, 255), (170, 220, 255), (y - 4) / 23))
    im.px(13, 20, W); im.px(12, 21, W); im.px(13, 21, W); sparkle(im, 24, 8, W, 2); return im
def item_crown():
    im = Img(); im.rect(7, 18, 25, 24, GD); im.rect(7, 18, 25, 19, GO); im.frame(7, 18, 25, 24, (90, 60, 10))
    for x in (7, 16, 25): im.poly([(x - 3, 18), (x, 8), (x + 3, 18)], GO)
    for x in (7, 16, 25): im.px(x, 8, (230, 60, 90)); im.px(x, 7, W)
    im.disc(16, 21, 1.5, (110, 60, 190)); im.line(14, 10, 17, 24, DK); im.line(17, 24, 15, 27, DK); im.line(10, 20, 8, 25, (90, 60, 10)); return im
def item_heart():
    im = Img(); im.disc(16, 16, 13, (80, 40, 140, 70)); heart(im, 16, 15, 9, (225, 60, 110)); heart(im, 15, 14, 6, (255, 130, 170)); heart(im, 14, 12, 3, W)
    for (x, y) in ((6, 6), (26, 8), (25, 25), (7, 24)): sparkle(im, x, y, (255, 160, 220), 2)
    return im
def item_page():
    im = Img(); im.rect(7, 4, 24, 28, (236, 220, 178)); im.frame(7, 4, 24, 28, (120, 90, 50)); im.rect(8, 5, 23, 5, W)
    for y in (9, 12, 15): im.line(10, y, 21, y, (150, 120, 80))
    star(im, 16, 21, 4, (150, 70, 200)); im.disc(16, 21, 1, GO); im.line(8, 28, 23, 28, (170, 140, 90)); return im
def item_booster():
    im = Img(); base = (70, 70, 190)
    for y in range(2, 30):
        for x in range(7, 25): im.px(x, y, mix(shade(base, 1.3), shade(base, .6), (y - 2) / 28))
    im.frame(7, 2, 24, 29, (20, 20, 70)); 
    for x in range(7, 25, 2): im.px(x, 2, GO); im.px(x, 3, GD); im.px(x, 28, GO); im.px(x, 29 - 1, GD)
    im.rect(8, 6, 23, 6, GO); im.rect(8, 25, 23, 25, GO); star(im, 16, 15, 6, GO, 8, .4); star(im, 16, 15, 3, W, 8, .45)
    sparkle(im, 10, 10, W, 1); sparkle(im, 22, 21, W, 1); return im
def item_grimoire():
    im = Img(); c = (110, 30, 120); im.rect(6, 4, 25, 28, c); im.frame(6, 4, 25, 28, (40, 10, 50)); im.rect(6, 4, 9, 28, shade(c, .6))
    for y in (7, 12, 17, 22, 26): im.rect(6, y, 9, y, GD)
    im.frame(12, 8, 22, 24, GO); im.frame(13, 9, 21, 23, GD); star(im, 17, 16, 4, GO, 6, .5); im.disc(17, 16, 1.4, (120, 220, 255))
    im.rect(23, 4, 25, 28, (230, 215, 180)); im.px(24, 4, W); return im
def item_deck():
    im = Img(); base = (110, 50, 170)
    for k, off in enumerate((4, 2, 0)):
        x0, y0 = 7 + off, 6 + off - 1
        for y in range(y0, y0 + 22):
            for x in range(x0, x0 + 15): im.px(x, y, mix(shade(base, 1.2), shade(base, .55), (y - y0) / 22))
        im.frame(x0, y0, x0 + 14, y0 + 21, GO if k == 2 else GD)
    star(im, 14, 16, 5, GO, 8, .4); im.disc(14, 16, 1.3, W); im.frame(9, 7, 21, 26, GD); return im

def wood_noise(im, x0, y0, x1, y1, base, rnd, vertical=False):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            k = (x if vertical else y)
            c = shade(base, 1.0 + (0.12 if k % 5 == 0 else (-0.1 if k % 5 == 3 else 0)) + rnd.uniform(-.06, .06)); im.px(x, y, c)

def table_top():
    im = Img(); rnd = random.Random(11); wood = (58, 34, 22)
    wood_noise(im, 0, 0, 31, 31, wood, rnd); im.frame(0, 0, 31, 31, (30, 16, 10)); im.frame(1, 1, 30, 30, GD)
    for y in range(3, 29):  # tapete de terciopelo
        for x in range(3, 29): im.px(x, y, mix((86, 28, 120), (60, 18, 92), rnd.random() * .5 + (y - 3) / 60))
    im.frame(3, 3, 28, 28, GO); im.frame(4, 4, 27, 27, (140, 100, 30))
    for (x, y) in ((3, 3), (28, 3), (3, 28), (28, 28)): im.px(x, y, W)
    for k in range(4, 28, 3): im.px(k, 5, GD); im.px(k, 26, GD); im.px(5, k, GD); im.px(26, k, GD)
    # cartas en abanico
    for (cx, cy, c, dx) in ((9, 21, (190, 60, 70), -2), (12, 20, (70, 110, 200), -1), (15, 20, (230, 180, 50), 0)):
        im.rect(cx - 2, cy - 3, cx + 2, cy + 3, c); im.frame(cx - 2, cy - 3, cx + 2, cy + 3, GO); im.px(cx, cy, W)
    # esfera de cristal
    im.disc(20, 15, 5.2, (30, 20, 70)); im.disc(20, 15, 4.5, (110, 70, 200)); im.disc(19, 14, 3, (170, 140, 255)); im.disc(18, 13, 1.3, W)
    im.ring(20, 15, 5.2, (60, 40, 120)); im.rect(17, 20, 23, 21, GD); im.rect(18, 20, 22, 20, GO)
    # velas en esquinas
    for (cx, cy) in ((7, 7), (24, 24)):
        im.rect(cx - 1, cy, cx + 1, cy + 3, CR); im.px(cx, cy - 1, (255, 200, 60)); im.px(cx, cy - 2, (255, 120, 30)); im.px(cx - 1, cy - 1, (255, 150, 40, 140)); im.px(cx + 1, cy - 1, (255, 150, 40, 140))
    star(im, 10, 11, 2.5, GO, 4, .35); star(im, 24, 8, 1.8, GO, 4, .35)
    return im
def table_side():
    im = Img(); rnd = random.Random(12); wood = (52, 30, 20)
    wood_noise(im, 0, 0, 31, 31, wood, rnd, True)
    im.rect(0, 0, 31, 3, (86, 28, 120)); im.rect(0, 4, 31, 4, GO); im.rect(0, 5, 31, 5, GD)   # faldón de terciopelo
    for x in range(0, 32, 4): im.rect(x, 4, x, 7, GO if x % 8 == 0 else GD)
    im.frame(0, 0, 31, 31, (28, 15, 9))
    for (x0, x1) in ((2, 8), (23, 29)):          # patas talladas
        im.rect(x0, 9, x1, 30, (70, 42, 28)); im.frame(x0, 9, x1, 30, (34, 18, 12))
        for y in (12, 17, 22, 27): im.line(x0 + 1, y, x1 - 1, y + 1, (34, 18, 12))
    # panel central con runa tallada
    im.frame(11, 11, 20, 28, GD); im.rect(12, 12, 19, 27, (40, 22, 16))
    star(im, 15.5, 19.5, 4, GO, 6, .5); im.disc(15.5, 19.5, 1.3, (140, 210, 255)); im.line(15, 13, 15, 15, GD); im.line(15, 24, 15, 26, GD)
    return im
def table_bottom():
    im = Img(); rnd = random.Random(13); wood_noise(im, 0, 0, 31, 31, (34, 20, 14), rnd); im.frame(0, 0, 31, 31, (20, 10, 6)); return im

def altar_stone(top):
    im = Img(); rnd = random.Random(21 if top else 22); base = (38, 38, 52)
    for y in range(32):
        for x in range(32):
            br = 1.0 + rnd.uniform(-.14, .14); im.px(x, y, shade(base, br))
    for y in range(0, 32, 8):                      # ladrillos
        im.line(0, y, 31, y, (18, 18, 28))
        for x in range((4 if (y // 8) % 2 else 0), 32, 16): im.line(x, y, x, y + 7, (18, 18, 28))
    im.frame(0, 0, 31, 31, (14, 14, 22))
    glow = (150, 90, 255)
    def rune(cx, cy, k):
        pat = [[(0, -3), (0, 3)], [(-2, -3), (2, 3)], [(-2, 0), (2, 0), (0, -3)], [(-2, 3), (0, -3), (2, 3)], [(-2, -2), (2, -2), (0, 3)]][k % 5]
        for i in range(len(pat) - 1): im.line(cx + pat[i][0], cy + pat[i][1], cx + pat[i + 1][0], cy + pat[i + 1][1], glow)
        im.px(cx, cy, W)
    if top:
        im.frame(2, 2, 29, 29, (70, 70, 96)); im.ring(15.5, 15.5, 9, (90, 60, 160), 1); im.ring(15.5, 15.5, 6, glow, 1)
        star(im, 15.5, 15.5, 4.5, (200, 160, 255), 8, .45); im.disc(15.5, 15.5, 1.6, W)
        for k in range(8):
            t = k * math.pi / 4; rune(int(15.5 + math.cos(t) * 12), int(15.5 + math.sin(t) * 12), k)
        for (x, y) in ((4, 4), (27, 4), (4, 27), (27, 27)): im.disc(x, y, 1.5, (120, 220, 255)); im.px(x, y, W)
    else:
        for k, (cx, cy) in enumerate(((8, 4), (24, 4), (8, 12), (24, 12), (8, 20), (24, 20), (8, 28), (24, 28))): rune(cx, cy, k)
        im.disc(16, 8, 1.4, (120, 220, 255)); im.disc(16, 24, 1.4, (120, 220, 255)); im.px(16, 8, W); im.px(16, 24, W)
        im.line(16, 10, 16, 22, (80, 50, 150))
    return im

if __name__ == "__main__":
    try:
        import gen_cards   # cartas ilustradas 128x128 (requiere Pillow + numpy)
        gen_cards.run(f"{A}/textures/item")
    except ImportError:
        for (cid, num, *_rest) in D.CARDS:
            base, rar = _rest[-2], _rest[-1]
            card(cid, num, base, rar).save(f"{A}/textures/item/card_{cid}.png")
    for name, fn in (("stardust", item_stardust), ("destiny_shard", item_shard), ("astral_tear", item_tear), ("broken_crown", item_crown),
                     ("destiny_heart", item_heart), ("expansion_page", item_page), ("booster_pack", item_booster),
                     ("grimoire", item_grimoire), ("destiny_deck", item_deck)):
        fn().save(f"{A}/textures/item/{name}.png")
    table_top().save(f"{A}/textures/block/tarot_table_top.png"); table_side().save(f"{A}/textures/block/tarot_table_side.png")
    table_bottom().save(f"{A}/textures/block/tarot_table_bottom.png")
    altar_stone(True).save(f"{A}/textures/block/arcane_altar_top.png"); altar_stone(False).save(f"{A}/textures/block/arcane_altar_side.png")
    gen_data.run(R, A)
    print("assets ok: 22 cartas + 9 ítems + 2 bloques en 32x32")
