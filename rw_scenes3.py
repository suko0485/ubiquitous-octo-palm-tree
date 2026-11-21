"""Escenas XV-XXI (Diablo ... Mundo)."""
import math
from rw_lib import *
from rw_scenes2 import _creatures


def devil(a):
    a.grad(0, 92, (14, 12, 22), (40, 22, 40))
    a.glow(33, 30, 22, RED_D, 120)
    a.rect(14, 42, 52, 60, GRY_D, INK, .7); a.rect(10, 38, 56, 43, GRY, INK, .6)
    a.cross_hatch([(14, 42), (52, 42), (52, 60), (14, 60)], BLK, 2.2, .35)
    # alas de murciélago
    a.poly([(26, 20), (4, 6), (8, 24), (3, 34), (14, 32), (22, 38)], BLK, INK, .6); a.poly([(40, 20), (62, 6), (58, 24), (63, 34), (52, 32), (44, 38)], BLK, INK, .6)
    # cuerpo
    a.poly([(25, 20), (41, 20), (43, 38), (23, 38)], GRY_D, INK, .6)
    a.ell(33, 12, 4.8, 5.4, GRY, INK, .6)
    a.poly([(28.4, 8), (24, -1), (31, 6)], WHT, INK, .5); a.poly([(37.6, 8), (42, -1), (35, 6)], WHT, INK, .5)
    a.poly([(29, 15), (37, 15), (33, 22)], GRY_L, INK, .4)
    a.dots([(31, 11.4), (35, 11.4)], .6, YEL)
    a.star(33, 7.6, 1.8, RED, 5, .4, rot=90, ol=None)
    a.limb((26, 26), (16, 32), 3.4, GRY_D); a.limb((40, 26), (50, 34), 3.4, GRY_D)
    a.hand(15.6, 32, 1.4, GRY_L); a.hand(50.4, 34.4, 1.4, GRY_L)
    a.line([(15, 32), (15, 26)], BRN, .8); a.poly([(13.6, 26), (15, 21), (16.4, 26)], ORA, INK, .4)   # antorcha
    a.glow(15, 24, 4, ORA, 220)
    a.ell(33, 36, 5, 2.4, GRY, INK, .4)
    # personajes encadenados
    a.limb((30, 60), (26, 64), 1, GRY_L); a.limb((36, 60), (40, 64), 1, GRY_L)
    for (x, sx, hair) in ((22, -1, BRN), (44, 1, YEL_D)):
        a.curve([(33, 56), (x, 58), (x, 62)], GRY_L, .9)
        a.poly([(x - 4, 66), (x + 4, 66), (x + 5, 84), (x - 5, 84)], SKIN, INK, .6)
        a.limb((x - 2, 84), (x - 2, 91), 2.6, SKIN); a.limb((x + 2, 84), (x + 2, 91), 2.6, SKIN)
        a.head(x, 62, 3.2, hair=hair, face="f")
        a.poly([(x - 3, 59), (x - 4.4, 55), (x - 1.8, 58)], ORA, INK, .3); a.poly([(x + 3, 59), (x + 4.4, 55), (x + 1.8, 58)], ORA, INK, .3)
        a.curve([(x + sx * 4, 82), (x + sx * 9, 84), (x + sx * 9, 90)], RED if sx < 0 else PUR, 1.6)
    a.poly([(16, 82), (22, 74), (20, 84)], ORA, INK, .3)


def tower(a):
    a.grad(0, 92, (8, 10, 26), (40, 36, 66))
    a.glow(52, 12, 16, YEL, 150)
    a.poly([(-2, 92), (-2, 74), (14, 66), (26, 74), (40, 68), (70, 76), (70, 92)], GRY_D, INK, .7)
    a.cross_hatch([(-2, 92), (-2, 74), (30, 76), (30, 92)], BLK, 2, .35)
    # torre
    a.poly([(22, 72), (25, 22), (43, 22), (46, 72)], GRY, INK, .8)
    for y in range(28, 70, 8): a.line([(24.5, y), (44.5, y)], GRY_D, .35, False)
    for (x, y) in ((30, 34), (30, 52)): a.rect(x, y, x + 5, y + 8, YEL, INK, .5); a.poly([(x, y + 8), (x + 2.5, y + 2), (x + 5, y + 8)], ORA, INK, .3)
    a.rect(36, 44, 41, 52, YEL, INK, .5)
    a.poly([(20, 22), (46, 22), (47, 17), (19, 17)], GRY_L, INK, .6)
    a.glow(33, 40, 17, ORA, 120)
    # corona
    a.poly([(38, 15), (52, 5), (54, 12), (46, 18), (40, 17)], GOLD, INK, .5)
    for x in (42, 46, 50): a.poly([(x, 8 + (x - 42) * -.4), (x + 1, 4 + (x - 42) * -.4), (x + 2, 8)], GOLD, INK, .3)
    # rayo
    a.poly([(66, 0), (46, 22), (53, 22), (36, 46), (50, 28), (43, 28), (60, 0)], YEL, INK, .5)
    a.glow(44, 24, 6, WHT, 230)
    # personas cayendo
    for (x, y, c) in ((12, 38, RED), (54, 56, BLU)):
        a.limb((x, y), (x + 5, y + 8), 2.4, c); a.limb((x, y), (x - 4, y + 7), 2.2, c); a.limb((x, y), (x + 4, y - 7), 2, c); a.limb((x, y), (x - 5, y - 5), 2, c)
        a.poly([(x - 2.5, y - 1), (x + 2.5, y - 1), (x + 2, y + 6), (x - 2, y + 6)], c, INK, .5)
        a.head(x, y - 4.4, 2.6, hair=YEL_D if c == BLU else BLK, face="f")
    for k in range(22):
        x = (k * 17) % 60 + 3; y = (k * 29) % 80 + 4
        a.poly([(x, y), (x + .7, y - 1.6), (x + 1.4, y)], YEL, None)


def star_(a):
    a.grad(0, 92, (14, 24, 80), (70, 110, 190))
    for (x, y, r) in ((10, 12, 2.6), (22, 6, 2.2), (46, 7, 2.2), (57, 14, 2.6), (8, 28, 2.2), (58, 32, 2.2), (28, 22, 2)):
        a.star(x, y, r, YEL, 8, .42, ol=GOLD_D, w=.3)
    a.glow(33, 16, 16, YEL_L, 160)
    a.star(33, 16, 9, YEL, 8, .42, ol=GOLD_D, w=.6); a.star(33, 16, 4.4, WHT, 8, .42, ol=None)
    a.blob([(-4, 62), (20, 58), (46, 64), (70, 58), (70, 92), (-4, 92)], GRN, INK, .6)
    a.blob([(10, 80), (36, 72), (62, 80), (52, 90), (22, 90)], BLU_L, INK, .6)
    for k in range(5): a.line([(18 + k * 8, 82 + (k % 2) * 3), (22 + k * 8, 82 + (k % 2) * 3)], WHT, .4, False)
    a.tree(56, 66, 20, 8, leaf=GRN_D)
    a.poly([(52, 44), (58, 44), (57, 50), (53, 50)], WHT, INK, .4); a.poly([(58, 45), (62, 47), (58, 48)], BRN_D, INK, .3)
    # mujer arrodillada
    a.limb((30, 70), (22, 82), 3.4, SKIN); a.limb((36, 70), (42, 80), 3.4, SKIN)
    a.poly([(26, 46), (38, 46), (40, 72), (26, 72)], SKIN, INK, .6)
    a.curve([(26, 34), (22, 50), (24, 68)], YEL_D, 3.2)
    a.head(31, 40, 3.6, hair=YEL_D, face="l", hair_style="long")
    a.limb((27, 52), (20, 64), 3, SKIN); a.limb((36, 52), (44, 64), 3, SKIN)
    a.poly([(16, 62), (24, 62), (22, 70), (18, 70)], GOLD_D, INK, .5); a.poly([(41, 62), (49, 62), (47, 70), (43, 70)], GOLD_D, INK, .5)
    a.curve([(19, 70), (18, 78), (24, 82)], BLU_L, 1.6); a.curve([(45, 70), (47, 76), (50, 78)], BLU_L, 1.6)


def moon(a):
    a.grad(0, 92, (20, 22, 70), (86, 100, 170))
    a.glow(33, 22, 22, YEL_L, 160)
    a.ell(33, 22, 11, 11, YEL_L, INK, .7); a.ell(37.4, 20.6, 8.6, 9.2, (30, 40, 100), None)
    a.arc(33, 22, 11, 100, 260, INK, .7)
    a.ell(29, 22, 5.4, 6.6, YEL_L, INK, .5); a.dots([(28, 21), (31, 21)], .5, INK); a.line([(28.4, 25), (30.8, 25)], ORA, .4, False)
    for k in range(16):
        a.poly([(8 + k * 3.4, 40 - (k % 3)), (9 + k * 3.4, 36), (10 + k * 3.4, 40)], YEL, None)
    a.poly([(0, 62), (14, 38), (28, 56), (40, 40), (52, 56), (66, 42), (66, 64), (0, 64)], mix(GRY_D, BLU, .35), INK, .6)
    # torres
    for x in (8, 54):
        a.rect(x - 5, 40, x + 5, 76, GRY, INK, .7); a.poly([(x - 6, 40), (x, 32), (x + 6, 40)], GRY_D, INK, .6)
        a.rect(x - 1.4, 46, x + 1.4, 52, YEL_D, None)
    # camino y estanque
    a.poly([(20, 92), (33, 66), (46, 92)], (218, 196, 140), INK, .5); a.curve([(33, 64), (30, 70), (36, 76), (30, 84), (33, 90)], (196, 168, 110), 2)
    a.blob([(4, 80), (33, 74), (62, 80), (62, 92), (4, 92)], BLU, INK, .6)
    a.ell(33, 88, 5, 1.6, BLU_L, None)
    # cangrejo
    a.ell(33, 85, 3.4, 2.4, RED, INK, .5); a.line([(29.6, 84), (26.6, 80)], RED, 1.2); a.line([(36.4, 84), (39.4, 80)], RED, 1.2)
    # perro y lobo
    a.poly([(10, 78), (12, 68), (20, 66), (22, 78), (18, 78), (18, 72), (14, 72), (14, 78)], GRY_L, INK, .5); a.poly([(20, 66), (24, 60), (25, 63), (22, 68)], GRY_L, INK, .5)
    a.poly([(44, 78), (46, 68), (54, 66), (56, 78), (52, 78), (52, 72), (48, 72), (48, 78)], GRY, INK, .5); a.poly([(46, 68), (42, 62), (41, 65), (44, 70)], GRY, INK, .5)


def sun(a):
    a.grad(0, 92, BLU_L, (210, 232, 250))
    a.sun(33, 20, 10, rays=20, col=YEL, face=True)
    a.rect(0, 52, 66, 76, ORA, INK, .6)
    for y in range(52, 76, 6):
        a.line([(0, y), (66, y)], RED_D, .35, False)
        for x in range(0, 70, 10): a.line([(x + (y % 12) // 2, y), (x + (y % 12) // 2, y + 6)], RED_D, .35, False)
    a.rect(0, 76, 66, 92, GRN, None); a.grad(76, 92, GRN_L, GRN)
    for x in (6, 22, 44, 60):
        a.line([(x, 88), (x, 52)], GRN_D, .8)
        for k in range(10):
            t = k * math.pi / 5; a.poly([(x + math.cos(t) * 2.6, 46 + math.sin(t) * 2.6), (x + math.cos(t) * 5, 46 + math.sin(t) * 5), (x + math.cos(t + .4) * 2.6, 46 + math.sin(t + .4) * 2.6)], YEL, INK, .3)
        a.ell(x, 46, 2.6, 2.6, BRN_D, INK, .4)
    # caballo blanco y niño
    a.poly([(24, 74), (42, 70), (52, 74), (50, 88), (46, 88), (45, 80), (30, 80), (28, 88), (24, 88)], WHT, INK, .7)
    a.poly([(42, 72), (50, 62), (56, 64), (52, 74)], WHT, INK, .7); a.dots([(54.4, 64.4)], .5, INK)
    a.curve([(44, 64), (40, 70), (44, 74)], YEL_D, 1.6)
    a.poly([(30, 72), (50, 68), (50, 72), (30, 76)], RED, INK, .5)
    a.poly([(33, 60), (41, 60), (42, 72), (32, 72)], SKIN, INK, .5)
    a.limb((33, 62), (26, 58), 2.6, SKIN); a.limb((41, 62), (46, 56), 2.4, SKIN)
    a.line([(46, 56), (48, 42)], BRN_D, .7); a.poly([(48, 42), (48, 50), (59, 47)], RED, INK, .5)
    a.head(37, 54, 3.4, hair=YEL_D, face="f")
    a.line([(34, 51), (40, 51)], RED, 1.1); a.line([(37, 51), (38.4, 46)], RED, 1.1)


def judgement(a):
    a.grad(0, 92, (170, 190, 215), (230, 236, 246))
    a.cloud(10, 14, 28, WHT, GRY_L); a.cloud(54, 12, 28, WHT, GRY_L); a.cloud(33, 24, 40, WHT, GRY_L)
    a.poly([(0, 62), (12, 46), (24, 60), (38, 42), (52, 58), (66, 46), (66, 66), (0, 66)], GRY_L, INK, .6)
    a.poly([(12, 46), (16, 52), (8, 52)], WHT, None); a.poly([(38, 42), (44, 50), (33, 50)], WHT, None)
    a.rect(0, 64, 66, 92, BLU, None); a.grad(64, 92, BLU_L, BLU)
    for k in range(10): a.line([(k * 8, 70 + (k % 3) * 6), (k * 8 + 4, 70 + (k % 3) * 6)], WHT, .4, False)
    # ángel Gabriel con trompeta y estandarte
    a.glow(33, 16, 20, YEL_L, 180)
    a.poly([(26, 16), (4, 8), (8, 22), (3, 30), (14, 28), (24, 32)], mix(RED, WHT, .2), INK, .6); a.poly([(40, 16), (62, 8), (58, 22), (63, 30), (52, 28), (42, 32)], mix(RED, WHT, .2), INK, .6)
    a.poly([(25, 18), (41, 18), (43, 34), (23, 34)], BLU_L, INK, .6)
    a.head(33, 13, 3.4, hair=YEL_D, face="f", hair_style="long"); a.halo(33, 13, 6)
    a.limb((26, 22), (16, 28), 2.8, BLU_L); a.limb((40, 22), (50, 16), 2.8, BLU_L)
    a.poly([(50, 16), (62, 8), (62, 14), (52, 19)], GOLD, INK, .4); a.ell(62.4, 11, 2, 3, GOLD, INK, .4)
    a.poly([(52, 20), (52, 30), (44, 30), (44, 22)], WHT, INK, .4); a.line([(48, 22), (48, 29)], RED, .8); a.line([(45, 25.6), (51, 25.6)], RED, .8)
    # ataúdes y resucitados
    for (x, y, col) in ((14, 78, GRY_L), (33, 82, GRY), (52, 78, GRY_L)):
        a.poly([(x - 8, y), (x + 8, y), (x + 6, y + 8), (x - 6, y + 8)], col, INK, .6)
        a.poly([(x - 4, y - 14), (x + 4, y - 14), (x + 5, y), (x - 5, y)], (190, 196, 204), INK, .6)
        a.limb((x - 3, y - 8), (x - 7, y - 18), 2.2, (190, 196, 204)); a.limb((x + 3, y - 8), (x + 7, y - 18), 2.2, (190, 196, 204))
        a.head(x, y - 17, 3, hair=BRN if x != 33 else YEL_D, face="f")
        a.hand(x - 7.4, y - 19, 1.1, (190, 196, 204)); a.hand(x + 7.4, y - 19, 1.1, (190, 196, 204))


def world(a):
    a.grad(0, 92, SKY, mix(SKY, WHT, .5))
    a.cloud(33, 46, 62, WHT, GRY_L)
    _creatures(a, [(10, 12), (56, 12), (10, 80), (56, 80)])
    # corona de laurel
    for t in [i * math.pi / 22 for i in range(44)]:
        x, y = 33 + 19 * math.cos(t), 46 + 28 * math.sin(t)
        a.ell(x, y, 2.9, 2.2, GRN if int(t * 10) % 2 else GRN_L, INK, .35)
    a.ell(33, 46, 19, 28, None, GRN_D, .5); a.ell(33, 46, 15.6, 25, None, GRN_D, .4)
    a.poly([(28, 16), (38, 16), (36, 22), (30, 22)], RED, INK, .5); a.poly([(28, 76), (38, 76), (36, 70), (30, 70)], RED, INK, .5)
    # bailarina con bastones
    a.limb((33, 44), (38, 60), 2.8, SKIN); a.limb((33, 62), (28, 70), 2.8, SKIN); a.limb((33, 62), (38, 54), 2.8, SKIN)
    a.poly([(28, 38), (38, 38), (37, 56), (29, 56)], SKIN, INK, .5)
    a.curve([(40, 38), (26, 46), (38, 54), (26, 64)], PUR, 3.4)
    a.line([(40, 38), (26, 46), (38, 54), (26, 64)], PUR_D, .4, False)
    a.limb((29, 42), (20, 32), 2.4, SKIN); a.limb((37, 54), (45, 62), 2.4, SKIN)
    a.line([(20, 32), (17, 22)], WHT, 1.2); a.line([(45, 62), (49, 72)], WHT, 1.2)
    a.line([(19, 24), (18, 21)], GOLD, 1.4); a.line([(48, 70), (49, 74)], GOLD, 1.4)
    a.head(33, 32, 3.6, hair=BRN, face="f", hair_style="long")
