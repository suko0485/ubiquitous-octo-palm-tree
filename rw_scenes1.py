"""Escenas 0-VII (Loco ... Carro). Coordenadas locales en un área de 66x92."""
import math
from rw_lib import *


def _ground_hills(a, y, col, col2=None):
    a.blob([(-4, y + 6), (0, y), (14, y - 3), (30, y + 1), (48, y - 4), (70, y), (70, 92), (-4, 92)], col, INK, .6)


def fool(a):
    a.grad(0, 92, YEL_L, YEL)
    a.sun(50, 15, 5.2, rays=16, col=WHT, face=False)
    # montañas nevadas
    a.poly([(-2, 58), (10, 40), (16, 48), (26, 34), (40, 56), (50, 46), (70, 60), (70, 64), (-2, 64)], (236, 238, 248), INK, .6)
    a.poly([(26, 34), (30, 40), (27, 42), (24, 40)], WHT, None)
    a.poly([(-2, 58), (6, 48), (14, 58)], GRY_L, None)
    a.poly([(26, 34), (40, 56), (28, 56)], (190, 196, 214), None)
    # acantilado
    a.poly([(-4, 66), (44, 66), (47, 70), (42, 76), (46, 84), (40, 92), (-4, 92)], (222, 214, 196), INK, .7)
    a.poly([(-4, 66), (44, 66), (44, 68), (-4, 69)], GRN_L, INK, .5)
    a.line([(14, 76), (20, 80)], GRY, .4); a.line([(26, 84), (34, 82)], GRY, .4)
    a.line([(0, 80), (8, 78)], GRY, .4)
    # perro blanco
    a.poly([(10, 66), (10, 58), (15, 56), (21, 58), (21, 66), (18, 66), (18, 62), (13, 62), (13, 66)], WHT, INK, .5)
    a.poly([(21, 58), (25, 54), (26, 57), (23, 60)], WHT, INK, .5)
    a.poly([(10, 59), (6, 52), (8, 51), (12, 57)], WHT, INK, .5)
    a.dots([(24.5, 56)], .4, INK)
    # piernas
    a.limb((28, 52), (24, 65), 2.6, (240, 230, 190)); a.limb((31, 52), (36, 63), 2.6, (240, 230, 190))
    a.poly([(22, 66), (27, 66), (27, 64), (23, 63)], RED_D, INK, .5)
    a.poly([(34, 64), (39, 62), (38, 60), (34, 61)], RED_D, INK, .5)
    # túnica con adornos
    a.poly([(22, 37), (34, 37), (36, 54), (20, 54)], WHT, INK, .7)
    a.poly([(20, 54), (36, 54), (35, 51), (21, 51)], YEL_D, INK, .4)
    for (x, y) in ((25, 42), (30, 44), (26, 48), (31, 49), (28, 40)):
        a.star(x, y, 1.5, ORA, 6, .5, ol=None)
    a.poly([(22, 37), (14, 44), (17, 56), (21, 48)], RED, INK, .6)  # capa
    # brazos
    a.limb((23, 40), (19, 31), 2.4, WHT); a.hand(18.8, 30, 1.2)
    a.limb((33, 40), (39, 36), 2.4, WHT); a.hand(40, 35.6, 1.2)
    # rosa blanca
    a.line([(18.8, 29), (18, 24)], GRN_D, .5)
    for dx, dy in ((0, 0), (-.9, .5), (.9, .5), (0, .9)):
        a.ell(18 + dx, 23.2 + dy, 1.1, 1.1, WHT, INK, .35)
    # bastón + hatillo
    a.line([(40, 35.6), (46, 24)], BRN_D, .9)
    a.ell(47.5, 23, 3.4, 3, (236, 210, 150), INK, .5)
    a.line([(45, 21.5), (50, 24.6)], BRN, .4, False)
    # cabeza, cabello, gorro y pluma
    a.head(28, 30, 3.6, hair=BRN, face="r")
    a.poly([(24.6, 28), (28, 24), (31.6, 28)], RED, INK, .5)
    a.line([(28, 25), (32, 18), (34, 19)], RED, .9)
    a.line([(33, 18.4), (33.4, 21)], RED_D, .4, False)


def magician(a):
    a.grad(0, 92, YEL_L, YEL)
    a.glow(33, 24, 26, WHT, 120)
    # infinito
    pts = [(33 + 7.5 * math.cos(t) / (1 + math.sin(t) ** 2), 11 + 4.5 * math.sin(t) * math.cos(t) / (1 + math.sin(t) ** 2) * 1.6) for t in [i * math.pi / 40 for i in range(81)]]
    a.line(pts, INK, 2.1); a.line(pts, WHT, .9)
    # rosas y lirios al fondo
    a.rect(0, 74, 66, 92, GRN, None)
    a.grad(74, 92, GRN, GRN_D)
    for x in (6, 12, 52, 59, 63):
        a.line([(x, 90), (x, 78)], GRN_D, .6)
        a.ell(x, 77, 2.1, 2.1, RED, INK, .4); a.ell(x, 77, .8, .8, RED_D, None)
    for x in (18, 46):
        a.line([(x, 90), (x, 80)], GRN_D, .6)
        a.poly([(x - 2.4, 79), (x, 82), (x + 2.4, 79), (x, 75)], WHT, INK, .4)
    # túnica blanca y capa roja
    a.poly([(24, 31), (42, 31), (47, 70), (19, 70)], RED, INK, .7)
    a.poly([(27, 31), (39, 31), (41, 70), (25, 70)], WHT, INK, .6)
    a.line([(26, 41), (40, 41)], GOLD_D, .5, False)
    a.poly([(25.5, 48), (40.5, 48), (41, 50), (25, 50)], GOLD, INK, .35)
    # brazos: vara arriba y dedo abajo
    a.limb((27, 34), (18, 42), 3.1, WHT); a.hand(17.2, 43.2, 1.3)
    a.limb((39, 34), (47, 26), 3.1, WHT); a.hand(47.6, 25, 1.3)
    a.poly([(47.4, 25), (47.4, 3), (49.2, 3), (49.2, 25)], WHT, INK, .4)
    a.rect(47.4, 3, 49.2, 6, GOLD, INK, .35); a.rect(47.4, 22, 49.2, 25, GOLD, INK, .35)
    a.glow(48.3, 3, 5, YEL_L, 220)
    # cabeza + diadema
    a.head(33, 23, 3.8, hair=BRN, face="f")
    a.rect(29.4, 20.8, 36.6, 21.8, WHT, INK, .35)
    a.line([(26, 22.5), (24, 28)], BRN, .6)
    # mesa con los 4 palos
    a.rect(9, 58, 57, 62, BRN, INK, .7)
    a.poly([(11, 62), (55, 62), (53, 78), (13, 78)], BRN_D, INK, .6)
    a.line([(14, 66), (52, 66)], BRN, .4, False)
    a.rect(9, 58, 57, 59.4, mix(BRN, WHT, .35), INK, .4)
    # copa
    a.poly([(14, 52), (20, 52), (18.5, 56), (15.5, 56)], GOLD, INK, .5); a.line([(17, 56), (17, 58)], GOLD_D, .8); a.rect(14.5, 57, 19.5, 58, GOLD, INK, .4)
    a.ell(17, 52, 3, .8, GOLD_D, INK, .4)
    # espada
    a.poly([(25.4, 40), (26.6, 40), (26.6, 56), (25.4, 56)], GRY_L, INK, .4)
    a.rect(23.5, 56, 28.5, 57.2, GOLD, INK, .4)
    # pentáculo
    a.ell(41, 55, 3.5, 3.5, GOLD, INK, .5); a.star(41, 55, 2.5, YEL_L, 5, .4, ol=GOLD_D, w=.3)
    # bastón corto
    a.poly([(48.4, 52), (49.6, 52), (49.6, 58), (48.4, 58)], WHT, INK, .4)
    a.rect(48.4, 52, 49.6, 53.5, GOLD, INK, .3)


def priestess(a):
    a.grad(0, 92, mix(BLU, WHT, .55), mix(BLU, BLU_D, .3))
    # cortina con granadas
    a.rect(10, 0, 56, 80, (120, 160, 215), None)
    for (x, y) in [(15, 12), (27, 8), (39, 10), (51, 14), (15, 30), (51, 32), (15, 52), (51, 56), (33, 6)]:
        a.ell(x, y, 2.4, 2.4, RED, INK, .4); a.ell(x, y, .7, .7, GOLD, None)
        a.line([(x - 3, y - 3), (x, y - 2.5), (x + 3, y - 3)], GRN_D, .4, False)
    a.poly([(10, 0), (56, 0), (56, 6), (10, 6)], BLU_D, INK, .5)
    # pilares B y J
    a.pillar(2, 11, 4, 84, BLK, GRY_D); a.pillar(55, 64, 4, 84, WHT, GRY_L)
    a.rect(4, 28, 9, 36, WHT, None); a.line([(5.2, 29), (5.2, 35)], BLK, .6); a.arc(6.2, 30.8, 1.5, -90, 90, BLK, .5); a.arc(6.2, 33.4, 1.7, -90, 90, BLK, .5)
    a.rect(57, 28, 62, 36, BLK, None); a.line([(60, 29), (60, 34)], WHT, .6); a.arc(58.8, 34.2, 1.2, 90, 270, WHT, .5)
    # trono / manto
    a.poly([(20, 82), (23, 36), (43, 36), (46, 82)], BLU, INK, .7)
    a.poly([(14, 84), (20, 44), (24, 36), (22, 84)], mix(BLU, WHT, .7), INK, .6)   # velo
    a.poly([(52, 84), (46, 44), (42, 36), (44, 84)], mix(BLU, WHT, .7), INK, .6)
    a.poly([(24, 40), (42, 40), (43, 80), (23, 80)], BLU_L, INK, .5)
    # pliegues y agua
    for x in (27, 31, 36, 40): a.line([(x, 52), (x + (x - 33) * .15, 80)], BLU_D, .4, False)
    a.cross_hatch([(14, 84), (20, 44), (22, 84)], BLU_D, 2.6, .3)
    # cruz solar en el pecho
    a.line([(33, 41), (33, 49)], WHT, .8); a.line([(29.5, 45), (36.5, 45)], WHT, .8)
    # rollo TORA
    a.poly([(28, 55), (41, 53), (42, 60), (29, 62)], WHT, INK, .5)
    a.line([(31, 57), (39, 56)], GRY_D, .5, False); a.line([(31, 59.5), (38, 58.4)], GRY_D, .5, False)
    a.limb((26, 42), (30, 56), 3, BLU); a.limb((40, 42), (37, 56), 3, BLU)
    # cabeza y corona lunar
    a.head(33, 28, 3.6, hair=BRN_D, face="f", hair_style="long")
    a.poly([(28, 27), (38, 27), (38, 24), (28, 24)], mix(BLU, WHT, .7), INK, .4)
    a.crescent(27.4, 24, 3.1, WHT, INK, -.55); a.crescent(38.6, 24, 3.1, WHT, INK, .55)
    a.ell(33, 21.5, 3.2, 3.2, GRY_L, INK, .5); a.ell(33, 21.5, 1.6, 1.6, WHT, None)
    # luna creciente a los pies
    a.crescent(33, 80, 5.2, WHT, INK, .5)
    a.glow(33, 80, 8, WHT, 120)


def empress(a):
    a.grad(0, 70, mix(GRN, WHT, .45), mix(GRN, GRN_D, .2))
    for (x, h, r) in ((6, 36, 9), (16, 40, 8), (50, 38, 9), (60, 34, 10), (36, 34, 7)):
        a.tree(x, 66, h * .55, r, leaf=mix(GRN_D, GRN, .35 + (x % 7) / 20))
    # arroyo y trigo
    a.poly([(-2, 70), (22, 66), (30, 92), (-2, 92)], BLU_L, INK, .5)
    for k in range(7): a.line([(2 + k * 3, 74 + (k % 3) * 4), (6 + k * 3, 73 + (k % 3) * 4)], WHT, .4, False)
    a.poly([(24, 68), (70, 68), (70, 92), (30, 92)], GOLD, INK, .5)
    for x in range(30, 68, 3):
        for y in (70, 76, 82, 88): a.line([(x + (y % 5) - 2, y + 4), (x + (y % 5) - 2, y)], GOLD_D, .5, False); a.ell(x + (y % 5) - 2, y - .6, .7, 1.2, YEL, None)
    # trono / almohadón
    a.poly([(16, 70), (50, 70), (52, 56), (14, 56)], RED, INK, .7)
    a.poly([(12, 40), (54, 40), (52, 58), (14, 58)], mix(RED, WHT, .35), INK, .6)
    a.dots([(20, 46), (26, 50), (40, 46), (46, 50), (33, 44)], .8, GOLD)
    # vestido blanco con granadas
    a.poly([(24, 36), (42, 36), (48, 72), (18, 72)], WHT, INK, .7)
    for (x, y) in ((24, 54), (31, 60), (38, 54), (28, 67), (36, 66), (42, 62), (21, 66), (33, 50)):
        a.ell(x, y, 1.5, 1.5, RED, INK, .3)
    a.line([(31, 40), (31, 72)], GRY_L, .4, False); a.line([(37, 40), (37, 72)], GRY_L, .4, False)
    a.limb((25, 40), (18, 52), 3, WHT); a.limb((41, 40), (46, 50), 3, WHT)
    a.hand(17.6, 53, 1.2); a.hand(46.4, 50.6, 1.2)
    # cetro
    a.line([(46.4, 50), (50, 20)], GOLD_D, 1.1)
    a.ell(50.5, 17.8, 2.6, 2.6, GOLD, INK, .5); a.ell(50.5, 17.8, .9, .9, WHT, None); a.line([(50.5, 15), (50.5, 13)], GOLD, .6)
    # escudo de Venus
    a.poly([(10, 66), (22, 66), (22, 74), (16, 82), (10, 74)], PINK, INK, .6)
    a.ell(16, 70, 2.4, 2.4, None, WHT, .6); a.line([(16, 72.4), (16, 77)], WHT, .6); a.line([(14, 75), (18, 75)], WHT, .6)
    # cabeza, melena y corona de 12 estrellas
    a.head(33, 29, 3.8, hair=YEL, face="f", hair_style="long")
    a.poly([(28, 27), (38, 27), (38, 25), (28, 25)], GOLD, INK, .4)
    for k in range(7):
        a.star(27.5 + k * 1.8, 23.2 + abs(k - 3) * .9, 1.4, WHT, 5, .45, ol=GOLD_D, w=.25)
    a.star(33, 20.6, 1.5, YEL_L, 5, .45, ol=GOLD_D, w=.25)


def emperor(a):
    a.grad(0, 92, (232, 120, 60), (200, 70, 40))
    a.poly([(-2, 52), (10, 34), (18, 44), (30, 28), (44, 46), (54, 36), (70, 54), (70, 64), (-2, 64)], (150, 80, 60), INK, .6)
    a.poly([(30, 28), (36, 36), (33, 38), (28, 34)], (230, 210, 200), None)
    a.cross_hatch([(30, 28), (44, 46), (34, 48)], (110, 50, 40), 2.2, .35)
    # trono de piedra con cabezas de carnero
    a.poly([(10, 92), (10, 24), (56, 24), (56, 92)], GRY, INK, .7)
    a.poly([(14, 92), (14, 28), (52, 28), (52, 92)], GRY_L, INK, .5)
    for k in range(6): a.line([(14, 40 + k * 9), (52, 40 + k * 9)], GRY, .3, False)
    for sx in (1, -1):
        cx = 33 + sx * 22
        a.ell(cx, 30, 4.2, 3.6, GRY_L, INK, .5)
        a.arc(cx + sx * 1, 30, 4, 90 if sx < 0 else -90, 270 if sx < 0 else 90, INK, .7)
    # túnica roja, armadura, botas
    a.poly([(19, 40), (47, 40), (50, 80), (16, 80)], RED, INK, .7)
    a.poly([(22, 46), (44, 46), (46, 74), (20, 74)], mix(RED, WHT, .1), INK, .4)
    a.poly([(24, 38), (42, 38), (44, 50), (22, 50)], (200, 210, 224), INK, .6)
    a.line([(33, 40), (33, 50)], GRY, .4, False)
    a.rect(21, 52, 45, 55, GOLD, INK, .5)
    a.limb((28, 80), (26, 88), 3.6, GRY_D); a.limb((38, 80), (40, 88), 3.6, GRY_D)
    # barba, rostro, corona
    a.poly([(28, 29), (38, 29), (39, 40), (33, 45), (27, 40)], WHT, INK, .6)
    a.ell(33, 28, 3.6, 4, SKIN, INK, .6)
    a.poly([(28.6, 31), (37.4, 31), (36, 40), (33, 43), (30, 40)], WHT, INK, .4)
    a.dots([(31.4, 27.5), (34.6, 27.5)], .35, INK)
    a.poly([(28, 25), (29.5, 20), (31.2, 24), (33, 18), (34.8, 24), (36.5, 20), (38, 25)], GOLD, INK, .5)
    # brazos y atributos: cetro ankh y orbe
    a.limb((24, 44), (17, 58), 3.4, mix(GRY_L, RED, .1)); a.hand(16.5, 59, 1.3)
    a.limb((42, 44), (50, 54), 3.4, mix(GRY_L, RED, .1)); a.hand(50.6, 55, 1.3)
    a.line([(16.5, 60), (16.5, 40)], GOLD_D, 1)
    a.ell(16.5, 36.8, 2.2, 2.8, None, GOLD_D, 1); a.line([(13.5, 42), (19.5, 42)], GOLD_D, 1)
    a.ell(50.6, 51.6, 3.1, 3.1, GOLD, INK, .5); a.line([(50.6, 48.5), (50.6, 54.7)], GOLD_D, .5); a.line([(47.5, 51.6), (53.7, 51.6)], GOLD_D, .5)
    a.line([(50.6, 48.6), (50.6, 46.8)], GOLD_D, .6); a.line([(49.6, 47.6), (51.6, 47.6)], GOLD_D, .6)


def hierophant(a):
    a.grad(0, 92, (166, 150, 190), (112, 96, 146))
    a.pillar(2, 12, 0, 86, GRY_L, GRY); a.pillar(54, 64, 0, 86, GRY_L, GRY)
    a.rect(12, 0, 54, 6, PUR_D, INK, .5)
    a.rect(12, 6, 54, 8, GOLD, INK, .4)
    # trono
    a.poly([(18, 86), (18, 18), (48, 18), (48, 86)], mix(PUR, GRY_D, .4), INK, .7)
    a.poly([(21, 86), (21, 22), (45, 22), (45, 86)], mix(PUR_D, BLK, .2), INK, .5)
    # capa roja y túnica
    a.poly([(22, 34), (44, 34), (50, 74), (16, 74)], RED, INK, .7)
    a.poly([(27, 34), (39, 34), (41, 74), (25, 74)], WHT, INK, .5)
    a.rect(30, 34, 36, 74, GOLD, INK, .4)
    a.line([(33, 38), (33, 72)], GOLD_D, .4, False)
    a.poly([(22, 34), (44, 34), (42, 40), (24, 40)], BLU, INK, .5)
    # triple corona
    a.head(33, 27, 3.6, hair=WHT, face="f", hair_style="long")
    for (w, y, c) in ((5.2, 21, GOLD), (4.2, 17.5, GOLD), (3.2, 14.4, GOLD)):
        a.poly([(33 - w, y + 3.4), (33 - w * .7, y), (33 + w * .7, y), (33 + w, y + 3.4)], c, INK, .5)
    a.line([(33, 14.4), (33, 11)], GOLD_D, .8); a.line([(31.8, 12.4), (34.2, 12.4)], GOLD_D, .8)
    a.line([(29, 21.5), (37, 21.5)], RED, .5, False)
    # brazos: bendición y báculo
    a.limb((24, 40), (17, 52), 3.2, RED); a.hand(16.8, 53, 1.3)
    a.limb((42, 40), (48, 45), 3.2, RED); a.hand(48.5, 45.6, 1.3)
    a.line([(48.5, 66), (48.5, 14)], GOLD_D, 1)
    for y, w in ((15, 3.4), (19, 2.6), (23, 1.8)): a.line([(48.5 - w, y), (48.5 + w, y)], GOLD_D, .9)
    a.dots([(48.5, 63)], 1, GOLD)
    a.line([(15.2, 53), (14.6, 48)], SKIN_D, .5, False)
    # monjes a los pies
    for (x, c) in ((22, WHT), (44, RED)):
        a.poly([(x - 5, 88), (x - 3.5, 77), (x + 3.5, 77), (x + 5, 88)], c, INK, .6)
        a.head(x, 74, 2.9, hair=None, face="f")
        a.poly([(x - 2.8, 72.6), (x + 2.8, 72.6), (x + 2.6, 70), (x - 2.6, 70)], BRN, None)
        a.rect(x - 3.4, 77.5, x + 3.4, 79.4, c if c == WHT else RED_D, INK, .4)
    # llaves cruzadas
    for (x0, x1) in ((28, 38), (38, 28)):
        a.line([(x0, 82), (x1, 90)], GOLD, 1.2)
        a.ell(x0, 82, 1.4, 1.4, None, GOLD_D, .7)
    a.line([(30, 86), (30, 89)], GOLD_D, .5)


def lovers(a):
    a.grad(0, 92, SKY, mix(SKY, WHT, .5))
    a.sun(33, 12, 4.2, rays=12, col=YEL, face=False)
    # montaña central
    a.poly([(24, 76), (33, 36), (42, 76)], GRY, INK, .7)
    a.poly([(33, 36), (37, 52), (30, 52)], mix(GRY, WHT, .5), None)
    a.cross_hatch([(33, 36), (42, 76), (34, 76)], GRY_D, 1.8, .3)
    a.line([(33, 36), (33, 31)], ORA, 1.2); a.line([(31, 33), (35, 32)], ORA, .8)
    # arcángel
    a.poly([(14, 22), (3, 10), (8, 26), (4, 32), (16, 28)], RED, INK, .6); a.poly([(52, 22), (63, 10), (58, 26), (62, 32), (50, 28)], RED, INK, .6)
    a.line([(8, 14), (14, 22)], RED_D, .4, False); a.line([(58, 14), (52, 22)], RED_D, .4, False)
    a.poly([(24, 24), (42, 24), (45, 40), (21, 40)], PUR, INK, .7)
    a.limb((25, 28), (14, 36), 3.2, PUR); a.limb((41, 28), (52, 36), 3.2, PUR)
    a.hand(13, 36.6, 1.2); a.hand(53, 36.6, 1.2)
    a.head(33, 18, 3.6, hair=ORA, face="f", hair_style="long")
    a.ell(33, 18, 7, 7, None, YEL_D, .4)
    # árbol con serpiente (derecha) y árbol con llamas (izquierda)
    a.poly([(47, 78), (49, 56), (53, 56), (55, 78)], BRN, INK, .5)
    a.ell(51, 52, 9, 8, GRN, INK, .6); a.dots([(46, 50), (53, 47), (56, 53), (49, 56)], 1.1, RED)
    a.curve([(51, 78), (47, 72), (54, 66), (48, 60), (53, 55)], GRN_D, 1.6)
    a.poly([(8, 78), (10, 56), (14, 56), (16, 78)], BRN, INK, .5)
    a.ell(12, 52, 8, 8, GRN_D, INK, .6)
    for (x, y) in ((8, 47), (12, 44), (16, 47), (9, 54), (15, 54)):
        a.poly([(x - 1.4, y + 2), (x, y - 2.4), (x + 1.4, y + 2)], ORA, INK, .3)
    # prado
    a.blob([(-4, 80), (12, 76), (33, 80), (54, 76), (70, 80), (70, 92), (-4, 92)], GRN, INK, .6)
    # figuras: hombre (izq) y mujer (der)
    a.poly([(17, 66), (23, 66), (24, 82), (16, 82)], SKIN, INK, .6)
    a.limb((19, 82), (19, 90), 2.4, SKIN); a.limb((22, 82), (22, 90), 2.4, SKIN)
    a.head(20, 60, 3.2, hair=BRN, face="r"); a.limb((21, 68), (28, 62), 2, SKIN); a.hand(28.6, 61.4, 1)
    a.poly([(42, 66), (48, 66), (49, 82), (41, 82)], SKIN, INK, .6)
    a.limb((43, 82), (43, 90), 2.4, SKIN); a.limb((47, 82), (47, 90), 2.4, SKIN)
    a.head(45, 60, 3.2, hair=YEL_D, face="l", hair_style="long"); a.limb((44, 68), (37, 62), 2, SKIN); a.hand(36.4, 61.4, 1)
    a.line([(42, 74), (48, 74)], GRN_D, .5, False); a.line([(17, 74), (23, 74)], GRN_D, .5, False)


def chariot(a):
    a.grad(0, 92, (24, 36, 86), (80, 110, 176))
    for (x, y) in ((6, 8), (58, 12), (12, 22), (54, 26), (30, 4)):
        a.star(x, y, 1.1, YEL_L, 4, .35, ol=None)
    # ciudad
    for (x, w, h) in ((2, 8, 20), (11, 7, 26), (50, 9, 24), (59, 8, 18)):
        a.rect(x, 62 - h, x + w, 62, GRY, INK, .5)
        for yy in range(int(62 - h) + 4, 60, 6): a.rect(x + 2.4, yy, x + 4, yy + 2.4, YEL_D, None)
        for xx in range(int(x), int(x + w), 3): a.rect(xx, 62 - h - 2, xx + 1.6, 62 - h, GRY, INK, .3)
    a.poly([(0, 62), (66, 62), (66, 68), (0, 68)], BLU_L, INK, .5)
    for k in range(8): a.line([(k * 9, 65), (k * 9 + 4, 65)], WHT, .4, False)
    # carro: cubo de piedra con disco alado
    a.poly([(12, 64), (54, 64), (54, 82), (12, 82)], GRY_L, INK, .7)
    a.rect(12, 64, 54, 67, GRY, INK, .5)
    a.poly([(18, 72), (26, 70), (28, 74), (20, 76)], GOLD, INK, .4); a.poly([(48, 72), (40, 70), (38, 74), (46, 76)], GOLD, INK, .4)
    a.ell(33, 73, 3.4, 3.4, RED, INK, .5); a.ell(33, 73, 1.2, 1.2, GOLD, None)
    a.ell(14, 86, 4.2, 4.2, GOLD_D, INK, .6); a.ell(52, 86, 4.2, 4.2, GOLD_D, INK, .6)
    # esfinges negra y blanca
    for (cx, col, sx) in ((11, BLK, 1), (55, WHT, -1)):
        a.poly([(cx - sx * 8, 90), (cx - sx * 6, 78), (cx + sx * 4, 78), (cx + sx * 8, 90)], col, INK, .6)
        a.ell(cx + sx * 1, 74, 3.4, 3.6, col, INK, .6)
        a.poly([(cx - sx * 3, 71), (cx + sx * 3, 71), (cx + sx * 4.4, 77), (cx - sx * 4.4, 77)], GOLD, INK, .4)
    # auriga con armadura
    a.poly([(26, 40), (40, 40), (42, 64), (24, 64)], (200, 210, 224), INK, .7)
    a.poly([(26, 52), (40, 52), (42, 64), (24, 64)], RED, INK, .5)
    a.rect(25, 51, 41, 53.4, GOLD, INK, .4)
    a.limb((28, 44), (22, 52), 3.2, (200, 210, 224)); a.limb((38, 44), (45, 38), 3.2, (200, 210, 224))
    a.hand(21.4, 52.6, 1.3); a.hand(45.6, 37, 1.3)
    a.line([(45.6, 36), (45.8, 24)], GOLD_D, .9); a.star(45.8, 22.4, 1.6, YEL_L, 4, .35, ol=GOLD_D, w=.3)
    a.head(33, 34, 3.6, hair=BRN, face="f")
    a.poly([(28.5, 31.6), (37.5, 31.6), (36, 29), (34.4, 31), (33, 27.6), (31.6, 31), (30, 29)], GOLD, INK, .4)
    a.star(33, 27.5, 1.5, YEL_L, 8, .4, ol=GOLD_D, w=.3)
    # palio azul con estrellas y cuatro columnas
    for x in (14, 52): a.line([(x, 28), (x, 64)], GOLD_D, 1.4)
    a.poly([(10, 28), (56, 28), (58, 18), (8, 18)], BLU_D, INK, .7)
    a.rect(8, 18, 58, 20.4, GOLD, INK, .4)
    for x in (14, 22, 30, 38, 46, 52): a.star(x, 24, 1.3, YEL_L, 5, .4, ol=None)
    for x in range(8, 58, 5): a.poly([(x, 28), (x + 2.5, 31), (x + 5, 28)], BLU, INK, .3)
