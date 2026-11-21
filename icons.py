import math
from pixlib import Img, mix, shade

W = (255, 247, 222); CR = (236, 220, 180); GO = (255, 214, 84); GD = (190, 140, 36); DK = (28, 18, 44)

def heart(im, cx, cy, s, c):
    for y in range(-s, s + 2):
        for x in range(-s - 1, s + 2):
            u, v = x / (s + .5), -y / (s + .5) + .15
            if (u * u + v * v - 1) ** 3 - u * u * v ** 3 <= 0: im.px(cx + x, cy + y, c)

def star(im, cx, cy, r, c, pts=5, inner=.45, rot=-90):
    P = []
    for i in range(pts * 2):
        rr = r if i % 2 == 0 else r * inner
        a = math.radians(rot + i * 180 / pts); P.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    im.poly(P, c)

def crescent(im, cx, cy, r, c, off=3):
    for y in range(int(cy - r - 1), int(cy + r + 2)):
        for x in range(int(cx - r - 1), int(cx + r + 2)):
            if math.hypot(x - cx, y - cy) <= r and math.hypot(x - cx - off, y - cy + 1) > r - 0.5: im.px(x, y, c)

# Todos dibujan en el área central ~ x 7..24, y 5..22 (centro 15.5, 13.5)
def fool(im, a):
    im.disc(21, 8, 2.6, GO); im.rect(7, 18, 14, 22, GD); im.rect(7, 17, 14, 17, CR)
    im.disc(14, 10, 1.7, W); im.line(14, 12, 14, 16, W); im.line(14, 13, 18, 11, W); im.line(14, 16, 17, 20, W); im.line(14, 16, 12, 18, W)
    im.line(15, 9, 19, 6, a); im.px(19, 5, GO); im.line(12, 21, 20, 21, mix(a, W, .4))
def magician(im, a):
    im.line(8, 10, 12, 7, W); im.line(12, 7, 15, 10, W); im.line(15, 10, 18, 13, W); im.line(18, 13, 21, 10, W); im.line(21, 10, 24, 7, W)
    im.ring(11, 8, 3, GO); im.ring(20, 8, 3, GO)
    im.line(10, 21, 20, 12, CR); im.line(11, 21, 21, 12, shade(CR, .7)); im.px(21, 11, GO); im.px(22, 10, W); im.px(20, 10, GO)
def priestess(im, a):
    im.rect(8, 8, 10, 21, W); im.rect(21, 8, 23, 21, DK); im.frame(21, 8, 23, 21, CR); im.rect(8, 7, 10, 7, GO); im.rect(21, 7, 23, 7, GO)
    crescent(im, 15.5, 11, 4, GO, 2); im.rect(13, 16, 18, 21, mix(a, W, .5)); im.line(15.5, 16, 15.5, 21, DK)
def empress(im, a):
    im.ring(15.5, 10, 5, W, 2); im.line(15.5, 15, 15.5, 22, W); im.line(15, 15, 15, 22, W); im.line(12, 19, 19, 19, W)
    im.poly([(6, 14), (10, 11), (9, 16)], mix(a, GO, .5)); im.poly([(25, 14), (21, 11), (22, 16)], mix(a, GO, .5)); im.px(15, 10, GO); im.px(16, 9, GO)
def emperor(im, a):
    im.rect(9, 11, 22, 22, shade(a, 1.3)); im.frame(9, 11, 22, 22, W); im.rect(9, 6, 11, 11, W); im.rect(20, 6, 22, 11, W); im.rect(13, 14, 18, 22, DK)
    im.poly([(11, 11), (15.5, 5), (20, 11)], GO); im.px(15, 8, W); im.line(7, 22, 24, 22, GD)
def hierophant(im, a):
    im.rect(15, 5, 16, 22, W); im.rect(11, 8, 20, 9, GO); im.rect(9, 12, 22, 13, GO); im.rect(12, 16, 19, 17, GO)
    im.px(15, 4, GO); im.px(16, 4, GO); im.disc(15.5, 21, 1.4, mix(a, W, .4))
def lovers(im, a):
    heart(im, 12, 11, 4, (240, 90, 120)); heart(im, 19, 14, 4, (255, 130, 160))
    im.px(10, 9, W); im.px(17, 12, W); star(im, 22, 6, 2.3, GO); im.line(8, 21, 23, 21, mix(a, W, .5))
def chariot(im, a):
    im.rect(9, 12, 22, 17, CR); im.frame(9, 12, 22, 17, GD); im.poly([(8, 11), (15.5, 5), (23, 11)], mix(a, W, .35)); im.disc(15.5, 14, 1.5, GO)
    for cx in (11, 20):
        im.ring(cx, 19, 3, W, 1); im.px(cx, 19, GO); im.line(cx - 3, 19, cx + 3, 19, GD); im.line(cx, 16, cx, 22, GD)
def strength(im, a):
    for k in range(12):
        t = k * math.pi / 6; im.line(15.5 + math.cos(t) * 5, 13.5 + math.sin(t) * 5, 15.5 + math.cos(t) * 8.5, 13.5 + math.sin(t) * 8.5, GD)
    im.disc(15.5, 13.5, 6, GO); im.px(13, 12, DK); im.px(18, 12, DK); im.px(14, 12, DK); im.px(17, 12, DK)
    im.poly([(14, 15), (17, 15), (15.5, 17)], DK); im.line(15.5, 17, 15.5, 19, DK); im.line(13, 19, 18, 19, DK)
def hermit(im, a):
    im.rect(12, 8, 19, 18, (50, 50, 60)); im.frame(12, 8, 19, 18, W); im.rect(13, 9, 18, 17, mix(a, GO, .6)); star(im, 15.5, 13, 3, W)
    im.rect(14, 5, 17, 7, W); im.px(15, 4, W); im.line(22, 6, 22, 22, CR); im.line(8, 22, 24, 22, GD); im.line(11, 8, 13, 8, W)
def wheel(im, a):
    im.ring(15.5, 13.5, 8, W, 2); im.ring(15.5, 13.5, 3, GO, 1)
    for k in range(8):
        t = k * math.pi / 4; im.line(15.5, 13.5, 15.5 + math.cos(t) * 8, 13.5 + math.sin(t) * 8, GO)
    for k in range(8):
        t = k * math.pi / 4 + .39; im.disc(15.5 + math.cos(t) * 9, 13.5 + math.sin(t) * 9, 1, mix(a, W, .5))
def justice(im, a):
    im.line(15.5, 5, 15.5, 22, W); im.line(15, 5, 15, 22, W); im.rect(13, 21, 18, 22, GD); im.line(8, 9, 23, 9, GO)
    for cx in (8, 23):
        im.line(cx, 9, cx - 3, 15, CR); im.line(cx, 9, cx + 3, 15, CR); im.poly([(cx - 4, 15), (cx + 4, 15), (cx, 18)], GO)
    im.disc(15.5, 6, 1.6, GO)
def hanged(im, a):
    im.line(8, 5, 23, 5, GD); im.line(15.5, 5, 15.5, 11, CR); im.disc(15.5, 17, 2.4, W)
    im.line(15.5, 11, 15.5, 14, W); im.poly([(13, 11), (18, 11), (15.5, 15)], mix(a, W, .4)); im.line(13, 9, 10, 7, W); im.line(18, 9, 21, 7, W)
    im.px(14, 17, DK); im.px(17, 17, DK); im.ring(15.5, 17, 4.5, mix(GO, a, .3))
def death(im, a):
    im.disc(15.5, 11.5, 6.5, W); im.rect(12, 16, 19, 20, W)
    im.disc(12.5, 11.5, 2, DK); im.disc(18.5, 11.5, 2, DK); im.poly([(15.5, 13.5), (14, 16), (17, 16)], DK)
    for x in (13, 15, 17, 19): pass
    for x in (13, 15, 16, 18): im.line(x, 18, x, 20, DK)
    im.px(12, 11, (200, 60, 80)); im.px(18, 11, (200, 60, 80))
def temperance(im, a):
    im.poly([(7, 6), (14, 6), (13, 11), (8, 11)], mix(a, W, .55)); im.poly([(18, 15), (25, 15), (24, 20), (19, 20)], mix(a, GO, .55))
    im.rect(10, 11, 11, 13, CR); im.rect(21, 20, 22, 22, CR)
    im.line(12, 7, 20, 13, (120, 210, 255)); im.line(20, 13, 21, 15, (120, 210, 255)); im.px(16, 10, W); im.px(18, 12, W); im.px(14, 8, W)
    im.line(13, 6, 13, 6, W); im.px(24, 6, GO); im.px(7, 17, GO)
def devil(im, a):
    im.disc(15.5, 14, 6, (190, 40, 40)); im.poly([(9, 11), (6, 4), (13, 8)], W); im.poly([(22, 11), (25, 4), (18, 8)], W)
    im.px(13, 13, GO); im.px(14, 13, GO); im.px(17, 13, GO); im.px(18, 13, GO); im.line(13, 18, 18, 18, DK); im.px(14, 19, W); im.px(17, 19, W)
    im.poly([(13, 21), (18, 21), (15.5, 23)], (150, 30, 30))
def tower(im, a):
    im.rect(11, 9, 20, 22, mix(a, W, .35)); im.frame(11, 9, 20, 22, DK)
    for y in range(11, 22, 3):
        im.line(11, y, 20, y, shade(a, .7))
    im.rect(10, 6, 21, 8, mix(a, W, .5)); 
    for x in (10, 13, 16, 19): im.rect(x, 4, x + 1, 5, mix(a, W, .5))
    im.poly([(23, 4), (18, 12), (21, 12), (16, 20), (25, 10), (21, 10)], (255, 235, 90)); im.rect(14, 15, 15, 17, DK)
def star_(im, a):
    star(im, 15.5, 13.5, 8, W, 8, .4); star(im, 15.5, 13.5, 4, GO, 8, .45)
    star(im, 8, 7, 2, GO, 4, .3); star(im, 24, 20, 2, GO, 4, .3); im.px(23, 6, W); im.px(8, 20, W)
def moon(im, a):
    crescent(im, 14, 13.5, 8, W, 4); crescent(im, 14, 13.5, 6, GO, 3)
    im.px(22, 7, W); im.px(24, 12, GO); im.px(21, 19, W)
    for (x, y) in ((8, 21), (23, 21)): im.line(x, y, x, y + 1, (140, 190, 255))
def sun(im, a):
    for k in range(16):
        t = k * math.pi / 8; r2 = 9.5 if k % 2 == 0 else 7.5
        im.line(15.5 + math.cos(t) * 6, 13.5 + math.sin(t) * 6, 15.5 + math.cos(t) * r2, 13.5 + math.sin(t) * r2, GO if k % 2 == 0 else (255, 160, 50))
    im.disc(15.5, 13.5, 5.2, (255, 190, 50)); im.disc(15.5, 13.5, 3.7, (255, 235, 130))
    im.px(14, 12, (200, 110, 20)); im.px(17, 12, (200, 110, 20)); im.line(14, 15, 17, 15, (200, 110, 20))
def judgement(im, a):
    im.poly([(8, 17), (17, 12), (17, 17)], GO); im.poly([(17, 9), (23, 6), (23, 22), (17, 19)], GD); im.disc(8, 17, 2, GO)
    im.rect(22, 7, 23, 21, GO)
    for k in range(5): im.line(10, 8 + k * 2, 14, 10 + k, W)
    im.line(6, 19, 4, 22, W); im.px(14, 22, W)
def world(im, a):
    im.ring(15.5, 13.5, 9, (90, 190, 110), 2)
    for k in range(10):
        t = k * math.pi / 5; im.disc(15.5 + math.cos(t) * 9, 13.5 + math.sin(t) * 9, 1.2, (70, 170, 90))
    im.disc(15.5, 13.5, 4.5, (90, 160, 230)); im.poly([(12, 11), (15, 10), (16, 13), (13, 15)], (90, 190, 110)); im.poly([(17, 14), (20, 14), (19, 17)], (90, 190, 110))
    im.ring(15.5, 13.5, 4.5, W); im.px(15, 22, GO); im.px(16, 22, GO)

ICONS = dict(fool=fool, magician=magician, priestess=priestess, empress=empress, emperor=emperor, hierophant=hierophant,
             lovers=lovers, chariot=chariot, strength=strength, hermit=hermit, wheel=wheel, justice=justice, hanged=hanged,
             death=death, temperance=temperance, devil=devil, tower=tower, star=star_, moon=moon, sun=sun,
             judgement=judgement, world=world)
