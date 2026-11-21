"""Escenas VIII-XIV (Fuerza ... Templanza)."""
import math
from rw_lib import *


def strength(a):
    a.grad(0, 92, YEL_L, YEL)
    a.blob([(-4, 62), (14, 50), (34, 58), (54, 46), (70, 56), (70, 92), (-4, 92)], mix(GRN, BLU, .35), INK, .6)
    a.blob([(-4, 72), (20, 66), (46, 74), (70, 68), (70, 92), (-4, 92)], GRN, INK, .6)
    # leona/león
    a.poly([(40, 84), (44, 66), (60, 64), (64, 84), (58, 88), (46, 88)], ORA, INK, .6)
    a.curve([(62, 70), (66, 76), (62, 82)], ORA, 1.4)
    a.ell(40, 62, 7.5, 7, YEL_D, INK, .6); a.ell(40, 63, 4.6, 4.4, ORA, INK, .5)
    a.dots([(38, 61), (42.5, 61)], .5, INK); a.poly([(38.5, 64), (42, 64), (40.3, 66)], RED_D, INK, .3)
    # mujer de blanco
    a.poly([(14, 40), (28, 40), (34, 86), (8, 86)], WHT, INK, .7)
    a.line([(18, 46), (16, 84)], GRY_L, .4, False); a.line([(24, 46), (26, 84)], GRY_L, .4, False)
    a.rect(14, 56, 28, 58, GRN, INK, .4)
    for x in range(15, 28, 3): a.ell(x, 57, 1.1, 1.1, RED, INK, .25)
    a.limb((24, 44), (34, 58), 3, WHT); a.limb((17, 44), (24, 56), 3, WHT)
    a.hand(35, 59.5, 1.3); a.hand(25, 57.5, 1.2)
    a.head(21, 33, 3.7, hair=BRN, face="r", hair_style="long")
    a.ell(21, 27.4, 3.6, 1.4, None, GRN_D, .8)
    for x in (18.4, 21, 23.6): a.ell(x, 26.6, 1.1, 1.1, RED, INK, .25)
    pts = [(21 + 6 * math.cos(t) / (1 + math.sin(t) ** 2), 15 + 3.4 * math.sin(t) * math.cos(t) / (1 + math.sin(t) ** 2) * 1.6) for t in [i * math.pi / 40 for i in range(81)]]
    a.line(pts, INK, 1.8); a.line(pts, WHT, .8)


def hermit(a):
    a.grad(0, 92, (176, 186, 204), (112, 122, 146))
    a.poly([(-2, 56), (14, 38), (26, 50), (40, 30), (56, 52), (70, 44), (70, 64), (-2, 64)], (210, 216, 230), INK, .6)
    a.poly([(40, 30), (46, 40), (40, 42), (35, 40)], WHT, None)
    a.cross_hatch([(40, 30), (56, 52), (42, 54)], GRY, 2.2, .3)
    a.blob([(-4, 70), (20, 64), (46, 70), (70, 62), (70, 92), (-4, 92)], (232, 238, 248), INK, .6)
    for (x, y) in ((8, 84), (50, 82), (30, 88)): a.line([(x, y), (x + 8, y - 1)], GRY_L, .5, False)
    # capa gris
    a.poly([(26, 28), (44, 28), (52, 84), (18, 84)], GRY, INK, .7)
    a.poly([(30, 26), (40, 26), (44, 34), (26, 34)], GRY_D, INK, .6)
    a.cross_hatch([(18, 84), (30, 40), (34, 84)], GRY_D, 2, .3)
    a.line([(36, 34), (38, 82)], GRY_D, .4, False)
    # barba y rostro
    a.ell(34, 29, 3.2, 3.6, SKIN, INK, .6)
    a.poly([(31, 31), (37, 31), (38, 41), (34, 46), (30, 41)], WHT, INK, .5)
    # linterna y báculo
    a.limb((29, 40), (22, 50), 3, GRY); a.hand(21.4, 51, 1.3)
    a.line([(21.4, 50), (21.4, 44)], INK, .5)
    a.rect(18.4, 36, 24.4, 44, GRY_D, INK, .5)
    a.glow(21.4, 40, 7, YEL_L, 230)
    a.star(21.4, 40, 3, YEL_L, 6, .5, ol=GOLD_D, w=.3)
    a.poly([(18.4, 36), (21.4, 33), (24.4, 36)], GRY_D, INK, .5)
    a.limb((40, 44), (46, 56), 3, GRY); a.hand(46.6, 57, 1.3)
    a.line([(46.6, 58), (47.6, 88)], BRN_D, 1.2); a.line([(46.6, 58), (46.6, 22)], BRN_D, 1.2)
    a.ell(46.6, 21, 1.1, 1.1, BRN, INK, .4)


def _creatures(a, spots):
    # ángel, águila, león, toro (símbolos de los evangelistas) con alas y nube
    kinds = ["angel", "eagle", "bull", "lion"]
    for (x, y), k in zip(spots, kinds):
        a.cloud(x, y + 4, 15, WHT, GRY_L)
        a.poly([(x - 8, y - 2), (x - 3, y - 4), (x - 3, y + 3), (x - 9, y + 2)], WHT, INK, .4)
        a.poly([(x + 8, y - 2), (x + 3, y - 4), (x + 3, y + 3), (x + 9, y + 2)], WHT, INK, .4)
        if k == "angel":
            a.poly([(x - 3, y + 6), (x - 2, y), (x + 2, y), (x + 3, y + 6)], BLU, INK, .4); a.head(x, y - 2, 2.4, hair=YEL_D, face="f")
        elif k == "eagle":
            a.ell(x, y + 1, 3, 3.6, BRN, INK, .5); a.ell(x, y - 2.4, 2, 2, WHT, INK, .4); a.poly([(x, y - 2), (x + 3, y - 1.4), (x, y - .6)], GOLD, INK, .3)
        elif k == "bull":
            a.ell(x, y, 3.4, 3.4, ORA, INK, .5); a.poly([(x - 4, y - 3), (x - 2, y - 2), (x - 4, y - 1)], WHT, INK, .3); a.poly([(x + 4, y - 3), (x + 2, y - 2), (x + 4, y - 1)], WHT, INK, .3)
            a.dots([(x - 1, y - .4), (x + 1, y - .4)], .4, INK)
        else:
            a.ell(x, y, 3.8, 3.8, YEL_D, INK, .5); a.ell(x, y + .4, 2.3, 2.3, ORA, INK, .4); a.dots([(x - 1, y), (x + 1, y)], .4, INK)


def wheel(a):
    a.grad(0, 92, SKY, mix(SKY, WHT, .6))
    _creatures(a, [(10, 12), (56, 12), (10, 80), (56, 80)])
    cx, cy = 33, 46
    a.ell(cx, cy, 22, 22, BLU, INK, .8)
    a.ell(cx, cy, 20, 20, YEL, INK, .5); a.ell(cx, cy, 15, 15, mix(BLU, WHT, .5), INK, .5)
    a.ell(cx, cy, 6, 6, GOLD, INK, .6)
    for k in range(8):
        t = k * math.pi / 4 + .39
        a.line([(cx + math.cos(t) * 6, cy + math.sin(t) * 6), (cx + math.cos(t) * 20, cy + math.sin(t) * 20)], GOLD_D, 1.1)
        a.ell(cx + math.cos(t) * 17.4, cy + math.sin(t) * 17.4, 1.5, 1.5, RED, INK, .3)
    for (ang, ch) in ((-90, "T"), (0, "R"), (90, "O"), (180, "A")):
        pass
    a.star(cx, cy, 4, YEL_L, 8, .4, ol=GOLD_D, w=.3)
    # esfinge arriba, serpiente izq, Anubis der
    a.poly([(cx - 5, 22), (cx - 4, 16), (cx + 4, 16), (cx + 5, 22)], ORA, INK, .5); a.head(cx, 14, 2.2, hair=BLU_D, face="f"); a.line([(cx + 2, 18), (cx + 8, 12)], GRY_L, .6)
    a.curve([(12, 36), (8, 46), (14, 56), (10, 66), (16, 70)], GRN_D, 2.2); a.ell(16, 70.6, 1.6, 1.3, GRN, INK, .4)
    a.poly([(50, 56), (56, 56), (56, 72), (50, 72)], ORA, INK, .5); a.poly([(51, 52), (56, 52), (59, 57), (52, 57)], BLK, INK, .5)


def justice(a):
    a.grad(0, 92, YEL_L, YEL)
    a.rect(6, 0, 60, 92, PUR, None)
    a.cross_hatch([(6, 0), (60, 0), (60, 92), (6, 92)], PUR_D, 3, .4)
    a.pillar(2, 11, 0, 90, GRY_L, GRY); a.pillar(55, 64, 0, 90, GRY_L, GRY)
    a.poly([(16, 90), (18, 40), (48, 40), (50, 90)], mix(GOLD, BRN, .3), INK, .7)  # asiento
    a.poly([(20, 46), (46, 46), (50, 86), (16, 86)], RED, INK, .7)
    a.poly([(24, 40), (42, 40), (40, 56), (26, 56)], GRN, INK, .6)
    a.line([(33, 46), (33, 84)], RED_D, .4, False)
    a.limb((24, 50), (14, 54), 3.2, RED); a.limb((42, 50), (52, 56), 3.2, RED)
    a.hand(13.4, 54.2, 1.3); a.hand(52.4, 56.4, 1.3)
    a.poly([(12.6, 54), (14.4, 54), (14.4, 20), (13.5, 16), (12.6, 20)], GRY_L, INK, .5); a.rect(10, 52.6, 17, 54, GOLD, INK, .4)
    a.line([(52.4, 56), (52.4, 46)], GOLD_D, .6); a.line([(44, 46), (61, 46)], GOLD_D, .8)
    for x in (44, 61):
        a.line([(x, 46), (x - 2.6, 54)], GOLD_D, .4); a.line([(x, 46), (x + 2.6, 54)], GOLD_D, .4)
        a.poly([(x - 3.6, 54), (x + 3.6, 54), (x, 57)], GOLD, INK, .4)
    a.head(33, 33, 3.7, hair=BRN, face="f", hair_style="long")
    a.poly([(28.6, 30.4), (37.4, 30.4), (38, 26), (35, 28), (33, 24), (31, 28), (28, 26)], GOLD, INK, .5)
    a.rect(31.8, 28.4, 34.2, 30.4, BLU, INK, .3)


def hanged(a):
    a.grad(0, 92, (200, 226, 232), (226, 236, 210))
    a.blob([(-4, 82), (20, 78), (46, 84), (70, 78), (70, 92), (-4, 92)], GRN_L, INK, .6)
    # árbol en T
    a.poly([(6, 12), (60, 12), (60, 19), (6, 19)], BRN, INK, .7)
    a.poly([(6, 12), (60, 12), (60, 14), (6, 14)], GRN, None)
    for x in (10, 20, 46, 56): a.ell(x, 15, 2.6, 2.2, GRN, INK, .4)
    a.poly([(1, 10), (6, 10), (6, 90), (1, 90)], BRN, INK, .6); a.poly([(60, 10), (65, 10), (65, 90), (60, 90)], BRN, INK, .6)
    a.rect(6, 16, 60, 20, BRN, INK, .6)
    a.line([(33, 20), (33, 28)], BRN_D, .8)
    # cuerpo invertido
    a.limb((33, 28), (33, 38), 3.2, YEL_D); a.poly([(30, 26), (36, 26), (36, 30), (30, 30)], YEL_D, INK, .5)
    a.limb((31, 38), (33, 28), 3.2, RED)
    a.limb((33, 38), (40, 46), 3, RED); a.limb((40, 46), (28, 52), 3, RED)   # pierna doblada (4)
    a.poly([(25, 36), (41, 36), (39, 62), (27, 62)], BLU, INK, .7)
    a.poly([(25, 36), (41, 36), (41, 40), (25, 40)], WHT, INK, .4)
    a.limb((27, 40), (33, 52), 3, BLU); a.limb((39, 40), (33, 52), 3, BLU)  # brazos atrás
    a.hand(33, 53, 1.2)
    a.limb((33, 62), (33, 38), 3, RED)
    a.head(33, 70, 3.8, hair=YEL_D, face="f")
    a.halo(33, 70, 6.6); a.glow(33, 70, 10, YEL_L, 220)
    a.head(33, 70, 3.8, hair=None, face="f")
    a.poly([(28, 70), (38, 70), (37, 66), (29, 66)], YEL_D, INK, .3)


def death(a):
    a.grad(0, 92, (230, 214, 160), (250, 236, 190))
    a.sun(33, 44, 6.4, rays=18, col=WHT, face=False)
    for x in (12, 52):
        a.rect(x - 4, 36, x + 4, 66, GRY_L, INK, .6)
        a.poly([(x - 5, 36), (x, 28), (x + 5, 36)], GRY, INK, .6)
    a.poly([(0, 62), (66, 62), (66, 70), (0, 70)], BLU_L, INK, .5)
    a.blob([(-4, 74), (20, 70), (46, 76), (70, 70), (70, 92), (-4, 92)], mix(GRN, GOLD, .5), INK, .6)
    # personajes a los pies
    a.poly([(2, 92), (4, 78), (24, 78), (26, 92)], RED, INK, .6); a.head(8, 76, 3, hair=WHT, face="f")  # rey caído
    a.poly([(8, 80), (20, 80), (20, 84), (8, 84)], GOLD, INK, .4)
    a.poly([(46, 90), (48, 74), (56, 74), (58, 90)], WHT, INK, .6); a.poly([(48, 74), (52, 66), (56, 74)], WHT, INK, .5); a.head(52, 72, 2.4, face="f")
    a.poly([(60, 90), (61, 80), (65, 80), (66, 90)], BLU, INK, .5); a.head(63, 78, 2, hair=YEL, face="f")
    # caballo blanco
    a.poly([(20, 56), (34, 52), (50, 54), (52, 62), (50, 80), (46, 80), (44, 64), (28, 64), (26, 80), (22, 80), (22, 64)], WHT, INK, .7)
    a.poly([(46, 54), (52, 40), (58, 42), (56, 50), (50, 58)], WHT, INK, .7)
    a.poly([(50, 42), (47, 46), (50, 55)], GRY_D, INK, .4)
    a.dots([(55.6, 43)], .5, INK); a.line([(52, 41), (50, 36)], RED, 1.3)
    a.curve([(22, 56), (16, 62), (18, 70)], WHT, 1.6)
    a.poly([(30, 52), (48, 52), (48, 57), (30, 57)], RED, INK, .5)
    # esqueleto con armadura negra
    a.poly([(30, 30), (42, 30), (43, 54), (29, 54)], BLK, INK, .6)
    a.rect(30, 38, 42, 40, GRY_D, None)
    a.limb((42, 34), (50, 30), 3, BLK); a.hand(50, 29.5, 1.2, WHT)
    a.line([(50, 29), (50, 6)], BRN_D, .9)
    a.poly([(50, 6), (50, 24), (64, 22), (64, 8)], BLK, INK, .6); a.star(57, 15, 3.2, WHT, 5, .5, ol=None)
    a.ell(36, 24, 3.8, 4.2, WHT, INK, .6)
    a.dots([(34.4, 23.4), (37.6, 23.4)], .8, INK); a.line([(34.6, 27), (37.4, 27)], INK, .4, False)
    a.poly([(31, 26), (34, 18), (38, 18), (41, 26)], BLK, INK, .5)
    a.line([(36, 18), (36, 12)], RED, 1.3)
    a.limb((31, 56), (31, 68), 2.8, BLK)


def temperance(a):
    a.grad(0, 92, (200, 224, 240), (240, 244, 250))
    a.mountain([(14, 52), (30, 34), (46, 52)], GRY_L)
    a.mountain([(30, 52), (46, 36), (66, 52)], mix(GRY_L, BLU, .3))
    a.glow(33, 30, 11, YEL_L, 220); a.poly([(30, 30), (33, 24), (36, 30)], GOLD, INK, .4)
    a.curve([(26, 90), (30, 80), (36, 72), (34, 62), (33, 54)], BRN, 3)
    a.blob([(-4, 66), (14, 62), (30, 66), (50, 62), (70, 66), (70, 92), (-4, 92)], GRN_L, INK, .6)
    a.blob([(34, 72), (56, 68), (62, 76), (50, 84), (30, 82)], BLU_L, INK, .6)
    for (x, y) in ((8, 80), (14, 72), (58, 86), (52, 76)):
        a.line([(x, y + 6), (x, y)], GRN_D, .6); a.poly([(x - 1.6, y + 1), (x, y - 2.6), (x + 1.6, y + 1)], PUR, INK, .35)
    # alas rojas
    a.poly([(24, 30), (4, 18), (6, 36), (14, 46), (22, 52)], RED, INK, .6); a.poly([(42, 30), (62, 18), (60, 36), (52, 46), (44, 52)], RED, INK, .6)
    for k in range(4): a.line([(22 - k * 4, 34 + k * 3), (8 + k * 2, 24 + k * 3)], RED_D, .4, False); a.line([(44 + k * 4, 34 + k * 3), (58 - k * 2, 24 + k * 3)], RED_D, .4, False)
    # túnica blanca
    a.poly([(24, 34), (42, 34), (46, 72), (20, 72)], WHT, INK, .7)
    a.poly([(30, 42), (36, 42), (33, 49)], None, INK, .4); a.rect(29.6, 42, 36.4, 49, None, INK, .4)
    a.line([(26, 52), (24, 70)], GRY_L, .4, False); a.line([(40, 52), (42, 70)], GRY_L, .4, False)
    # pies: uno en el agua, uno en tierra
    a.poly([(24, 72), (30, 72), (29, 77), (24, 77)], SKIN, INK, .4); a.poly([(36, 72), (42, 72), (42, 76), (36, 77)], SKIN, INK, .4)
    # copas y chorro
    a.limb((26, 42), (18, 54), 3, WHT); a.limb((40, 42), (46, 56), 3, WHT)
    a.poly([(14, 52), (21, 52), (19.5, 58), (15.5, 58)], GOLD, INK, .4); a.poly([(43, 56), (50, 56), (48.5, 62), (44.5, 62)], GOLD, INK, .4)
    a.curve([(20, 53), (28, 52), (38, 56), (45, 58)], BLU_L, 1.4)
    a.head(33, 25, 3.7, hair=YEL, face="f", hair_style="long")
    a.halo(33, 25, 6.6)
    a.ell(33, 21, 1, 1, RED, None)
