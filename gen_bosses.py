#!/usr/bin/env python3
"""Genera los 3 jefes con modelo 3D propio: datos del modelo (JSON), texturas, BossAnim.java y previsualizaciones.

Uso:
    python3 gen_bosses.py            # modelos + texturas + BossAnim.java
    python3 gen_bosses.py --preview  # además renderiza previews/ (turnaround PNG + GIF animado; requiere Pillow + numpy)
"""
import json, math, os, sys, zlib
from pixlib import Img, shade
import bosslib as L
from bosslib import dots, hline, vline, cracks

R = "src/main/resources"
OUT_JSON = f"{R}/tarot_boss"
OUT_TEX = f"{R}/assets/tarot/textures/entity"
OUT_JAVA = "src/main/java/com/tarotmod/boss/entity/BossAnim.java"

# Animaciones de acción (mismo orden/IDs en BossAnim.java). El golpe de 'slam' cae en el tick 30 (= telegrafiado del BossManager).
ANIMS = [("slam", 40), ("cast", 34), ("summon", 36), ("special", 46), ("enrage", 44)]
IDLE_LEN, DEATH_LEN = 80, 20


def mats(**kw):
    return kw


# ====================================================================================================
# 0 · EL HIEROFANTE CORROMPIDO
# ====================================================================================================
def hierophant():
    M = dict(
        robe=dict(kind="cloth", c=(78, 34, 98), hi=(104, 52, 130), lo=(44, 18, 62)),
        robe2=dict(kind="cloth", c=(96, 44, 118), hi=(126, 66, 152), lo=(58, 26, 80)),
        gold=dict(kind="metal", c=(214, 168, 58), hi=(255, 232, 130), lo=(122, 82, 22)),
        bone=dict(kind="grad", c=(184, 184, 168), hi=(204, 204, 188), lo=(150, 150, 140)),
        beard=dict(kind="cloth", c=(204, 202, 214), hi=(232, 230, 242), lo=(150, 146, 170)),
        mitre=dict(kind="cloth", c=(228, 222, 236), hi=(250, 246, 255), lo=(168, 156, 190)),
        mitre2=dict(kind="cloth", c=(118, 56, 150), hi=(150, 84, 186), lo=(70, 30, 98)),
        crys=dict(kind="crystal", c=(170, 92, 255), hi=(240, 205, 255), lo=(84, 30, 160), noise=.02),
        wood=dict(kind="grad", c=(86, 56, 36), hi=(116, 80, 52), lo=(50, 30, 20)),
        dark=dict(kind="flat", c=(30, 18, 44)),
    )
    m = L.Model("hierophant", "textures/entity/hierophant.png", M, "El Hierofante Corrompido")

    def face(im, x0, y0, w, h):  # cara cadavérica con ojos violetas
        dots(im, x0, y0, [(1, 3), (2, 3), (5, 3), (6, 3)], (236, 150, 255))
        dots(im, x0, y0, [(1, 2), (2, 2), (5, 2), (6, 2)], (60, 30, 80))
        dots(im, x0, y0, [(3, 4), (4, 4), (3, 5), (4, 5)], (120, 120, 112))
        hline(im, x0, y0, 2, 5, 7, (70, 36, 90))
        cracks(im, x0, y0, w, h, 5, (176, 96, 255), 1, 4)

    def stole_cross(im, x0, y0, w, h):
        vline(im, x0, y0, 2, 1, h - 2, (255, 226, 120)); vline(im, x0, y0, 3, 1, h - 2, (255, 226, 120))
        hline(im, x0, y0, 0, 5, 3, (255, 226, 120)); hline(im, x0, y0, 0, 5, 4, (214, 168, 58))
        dots(im, x0, y0, [(2, 3), (3, 3)], (180, 110, 255))

    def mitre_cross(im, x0, y0, w, h):
        vline(im, x0, y0, w // 2, 0, h - 1, (160, 80, 220)); vline(im, x0, y0, w // 2 - 1, 0, h - 1, (160, 80, 220))
        hline(im, x0, y0, 1, w - 2, h // 2, (214, 168, 58))

    def chest_cracks(im, x0, y0, w, h):
        cracks(im, x0, y0, w, h, 9, (196, 120, 255), 2, 9)

    # ---- falda (suelo) ----
    robe = m.add("robe", None, (0, 0, 0), walk=[("rx", 4, 0, 0)])
    robe.box(-8, 0, -7, 16, 1, 14, "gold")
    robe.box(-8, 1, -7, 16, 4, 14, "robe", front=chest_cracks)
    robe.box(-7, 5, -6, 14, 6, 12, "robe2")
    robe.box(-5, 11, -3, 10, 5, 6, "robe")

    # ---- torso ----
    torso = m.add("torso", None, (0, 16, 0), walk=[("rx", 0, 0, 7)])
    torso.box(-6, -1, -4, 12, 14, 8, "robe2", front=chest_cracks)
    torso.box(-7, -1, -5, 14, 3, 10, "gold")
    torso.box(-3, 2, -5, 6, 8, 1, "mitre", front=stole_cross)
    torso.box(-8, 10, -5, 16, 3, 10, "gold")
    torso.box(-5, 2, 4, 10, 8, 1, "mitre2")

    head = m.add("head", "torso", (0, 13, 0), look=True)
    head.box(-4, 0, -4, 8, 8, 8, "bone", front=face)
    head.box(-3, -5, -5, 6, 6, 1, "beard")
    mit = m.add("mitre", "head", (0, 8, 0))
    mit.box(-5, 0, -5, 10, 2, 10, "gold")
    mit.box(-4, 2, -4, 8, 5, 8, "mitre", front=mitre_cross)
    mit.box(-3, 7, -3, 6, 4, 6, "mitre2")
    mit.box(-2, 11, -2, 4, 2, 4, "gold")
    mit.box(-1, 13, -1, 2, 3, 2, "crys")
    for s, name in ((-1, "ribbon_r"), (1, "ribbon_l")):
        rb = m.add(name, "head", (3 * s, 8, 5))
        rb.box(-1, -12, 0, 2, 12, 1, "mitre2")

    # ---- brazo derecho + báculo ----
    def arm(side, sname):
        x = 8 * side
        a = m.add(f"arm_{sname}", "torso", (x, 11, 0), rot=(-10 if side < 0 else -34, 0, 6 if side < 0 else -14),
                  walk=[("rx", 7 if side < 0 else 12, 0 if side < 0 else math.pi, 0)])
        a.box(-4, -1, -4, 8, 3, 8, "gold")
        a.box(-3, -10, -3, 6, 9, 6, "robe2")
        f = m.add(f"forearm_{sname}", f"arm_{sname}", (0, -10, 0), rot=(-25 if side < 0 else -58, 0, 0))
        f.box(-3, -8, -3, 6, 8, 6, "robe")
        f.box(-3, -10, -3, 6, 2, 6, "gold")
        f.box(-2, -13, -2, 4, 3, 4, "bone")
        return a, f

    arm(-1, "r")
    arm(1, "l")
    st = m.add("staff", "forearm_r", (0, -11, 0), rot=(35, 0, -6))
    st.box(-1, -14, -1, 2, 34, 2, "wood")
    st.box(-6, 12, -1.5, 12, 2, 3, "gold")
    st.box(-5, 15, -1.5, 10, 2, 3, "gold")
    st.box(-4, 18, -1.5, 8, 2, 3, "gold")
    st.box(-1.5, 20, -1.5, 3, 5, 3, "crys")
    orb = m.add("orb", "forearm_l", (0, -15, 0), spin=(6, 4))
    orb.box(-2, -2, -2, 4, 4, 4, "crys")

    # ---- órbitas ----
    keys = m.add("keys", "torso", (0, 2, 0), spin=(3, 0))
    for s in (-1, 1):
        x = 15 if s > 0 else -17
        keys.box(x, -4, -1, 2, 8, 2, "gold")
        keys.box(x - 1, 4, -1, 4, 3, 2, "gold")
        keys.box(x + (2 if s > 0 else -2), -4, -1, 2, 2, 2, "gold")
    halo = m.add("halo", "torso", (0, 30, 0), spin=(2.2, 0))
    for i in range(6):
        a = i * math.pi / 3
        halo.box(11 * math.cos(a) - 1, (-3 if i % 2 else 0), 11 * math.sin(a) - 1, 2, 6, 2, "crys")

    # ---- fase 2: cristales corruptos ----
    halo2 = m.add("halo2", "torso", (0, 35, 0), p2=True, spin=(-3.2, 0))
    for i in range(8):
        a = i * math.pi / 4 + .3
        halo2.box(16 * math.cos(a) - 1, (i % 3) * 2 - 2, 16 * math.sin(a) - 1, 2, 7, 2, "crys")
    for i, (x, rx, rz, hgt) in enumerate(((-4, 25, 14, 14), (4, 25, -14, 14), (0, 38, 0, 19))):
        sp = m.add(f"spike{i}", "torso", (x, 11, 5), rot=(rx, 0, rz), p2=True)
        sp.box(-2, 0, 0, 4, hgt, 4, "crys")
    for s, n in ((-1, "r"), (1, "l")):
        sc = m.add(f"shcr_{n}", f"arm_{n}", (3 * s, 3, 0), rot=(0, 0, -22 * s), p2=True)
        sc.box(-2, 0, -2, 4, 8, 4, "crys")

    # ================= animaciones =================
    c = m.clip("idle", IDLE_LEN, loop=True)
    c.k("torso", "y", [(0, 0), (40, .8), (80, 0)]).k("torso", "rx", [(0, 0), (40, -1.5), (80, 0)])
    c.k("head", "rx", [(0, 0), (40, 2.5), (80, 0)]).k("head", "ry", [(0, -4), (40, 4), (80, -4)])
    c.k("arm_l", "rx", [(0, 0), (40, -7), (80, 0)]).k("arm_l", "rz", [(0, 0), (40, -4), (80, 0)])
    c.k("forearm_l", "rx", [(0, 0), (40, -8), (80, 0)])
    c.k("arm_r", "rx", [(0, 0), (40, 2), (80, 0)])
    c.k("robe", "rz", [(0, -1.2), (40, 1.2), (80, -1.2)])
    c.k("ribbon_r", "rx", [(0, 5), (40, -4), (80, 5)]).k("ribbon_l", "rx", [(0, -4), (40, 5), (80, -4)])
    c.k("orb", "y", [(0, 0), (40, 1.6), (80, 0)])
    c.k("halo", "y", [(0, 0), (40, 1.2), (80, 0)])
    c.k("halo2", "y", [(0, 0), (40, -1.2), (80, 0)])

    # GOLPE: el báculo se alza y se clava en el tick 30
    c = m.clip("slam", 40)
    c.k("arm_r", "rx", [(0, 0), (26, -108), (31, -4, "in"), (35, -4), (40, 0)])
    c.k("forearm_r", "rx", [(0, 0), (26, -14), (31, 10, "in"), (35, 10), (40, 0)])
    c.k("staff", "rx", [(0, 0), (26, -12), (31, 6, "in"), (35, 6), (40, 0)])
    c.k("arm_l", "rx", [(0, 0), (26, -30), (31, 8, "in"), (40, 0)]).k("arm_l", "rz", [(0, 0), (26, -22), (31, 0), (40, 0)])
    c.k("torso", "rx", [(0, 0), (26, -10), (31, 15, "in"), (35, 12), (40, 0)])
    c.k("head", "rx", [(0, 0), (26, -14), (31, 12, "in"), (40, 0)])
    c.k("torso", "y", [(0, 0), (26, 1.5), (31, -2.5, "in"), (36, -1.5), (40, 0)])
    c.k("robe", "rx", [(0, 0), (26, -4), (31, 6, "in"), (40, 0)])
    c.k("halo", "y", [(0, 0), (26, 3), (31, -1), (40, 0)])

    # BOMBARDEO: levanta la mano izquierda con el orbe y señala
    c = m.clip("cast", 34)
    c.k("arm_l", "rx", [(0, 0), (24, -128), (29, -92, "in"), (34, 0)]).k("arm_l", "rz", [(0, 0), (24, -10), (34, 0)])
    c.k("forearm_l", "rx", [(0, 0), (24, 30), (29, 38), (34, 0)])
    c.k("arm_r", "rx", [(0, 0), (24, -22), (34, 0)])
    c.k("torso", "rx", [(0, 0), (24, -8), (29, 8, "in"), (34, 0)])
    c.k("head", "rx", [(0, 0), (24, -16), (29, 10), (34, 0)])
    c.k("halo", "y", [(0, 0), (24, 4), (34, 0)])
    c.k("orb", "y", [(0, 0), (24, 3), (29, 0), (34, 0)])

    # ESBIRROS: alza ambos brazos y convoca (el BossManager invoca a los 14 ticks)
    c = m.clip("summon", 36)
    c.k("arm_r", "rx", [(0, 0), (12, -30), (28, -30), (36, 0)]).k("arm_r", "rz", [(0, 0), (12, 55), (28, 55), (36, 0)])
    c.k("arm_l", "rx", [(0, 0), (12, -34), (28, -34), (36, 0)]).k("arm_l", "rz", [(0, 0), (12, -62), (28, -62), (36, 0)])
    c.k("forearm_r", "rx", [(0, 0), (12, 12), (28, 12), (36, 0)]).k("forearm_l", "rx", [(0, 0), (12, 30), (28, 30), (36, 0)])
    c.k("head", "rx", [(0, 0), (12, -28), (28, -28), (36, 0)])
    c.k("torso", "rx", [(0, 0), (12, -9), (28, -9), (36, 0)]).k("torso", "y", [(0, 0), (12, 3), (28, 3), (36, 0)])
    c.k("robe", "y", [(0, 0), (12, 2), (28, 2), (36, 0)])
    c.k("halo", "y", [(0, 0), (12, 6), (28, 6), (36, 0)]).k("halo2", "y", [(0, 0), (12, 8), (28, 8), (36, 0)])
    c.k("keys", "y", [(0, 0), (12, 5), (28, 5), (36, 0)])

    # ESPECIAL (pilares): golpe a dos manos con el báculo, golpea ~tick 36
    c = m.clip("special", 46)
    c.k("arm_r", "rx", [(0, 0), (30, -120), (36, -6, "in"), (41, -6), (46, 0)])
    c.k("forearm_r", "rx", [(0, 0), (30, -10), (36, 14, "in"), (46, 0)])
    c.k("staff", "rx", [(0, 0), (30, -16), (36, 8, "in"), (46, 0)])
    c.k("arm_l", "rx", [(0, 0), (30, -118), (36, -8, "in"), (41, -8), (46, 0)]).k("arm_l", "rz", [(0, 0), (30, -8), (36, 0), (46, 0)])
    c.k("forearm_l", "rx", [(0, 0), (30, -16), (36, 10), (46, 0)])
    c.k("torso", "rx", [(0, 0), (30, -14), (36, 18, "in"), (41, 14), (46, 0)])
    c.k("torso", "y", [(0, 0), (30, 3), (36, -3, "in"), (46, 0)])
    c.k("head", "rx", [(0, 0), (30, -20), (36, 14, "in"), (46, 0)])
    c.k("halo", "y", [(0, 0), (30, 6), (36, -1), (46, 0)]).k("halo2", "y", [(0, 0), (30, 6), (36, -1), (46, 0)])

    # FASE 2: rugido con los brazos abiertos y temblor
    c = m.clip("enrage", 44)
    c.k("head", "rx", [(0, 0), (10, -34), (34, -34), (44, 0)])
    c.k("arm_r", "rz", [(0, 0), (10, 62), (34, 62), (44, 0)]).k("arm_r", "rx", [(0, 0), (10, -22), (34, -22), (44, 0)])
    c.k("arm_l", "rz", [(0, 0), (10, -70), (34, -70), (44, 0)]).k("arm_l", "rx", [(0, 0), (10, -22), (34, -22), (44, 0)])
    c.k("torso", "rx", [(0, 0), (10, -12), (34, -12), (44, 0)])
    c.k("torso", "rz", [(0, 0), (12, 3), (16, -3), (20, 3), (24, -3), (28, 3), (32, -3), (36, 0), (44, 0)])
    c.k("robe", "rz", [(0, 0), (12, -4), (16, 4), (20, -4), (24, 4), (28, -4), (32, 4), (36, 0)])
    c.k("halo", "y", [(0, 0), (10, 8), (34, 8), (44, 0)]).k("halo2", "y", [(0, 0), (10, 10), (34, 10), (44, 0)])
    c.k("keys", "y", [(0, 0), (10, 6), (34, 6), (44, 0)])

    # MUERTE (20 ticks, sobre la caída vanilla): los brazos caen, la mitra se desprende y las órbitas se disipan
    c = m.clip("death", DEATH_LEN)
    c.k("arm_r", "rz", [(0, 0), (14, 38)]).k("arm_l", "rz", [(0, 0), (14, -44)])
    c.k("arm_r", "rx", [(0, 0), (14, 20)]).k("arm_l", "rx", [(0, 0), (14, 24)])
    c.k("head", "rx", [(0, 0), (6, -26), (18, 36)])
    c.k("mitre", "y", [(0, 0), (6, 1), (20, 12, "in")]).k("mitre", "rz", [(0, 0), (20, 40)])
    c.k("halo", "y", [(0, 0), (20, 22, "in")]).k("halo2", "y", [(0, 0), (20, 26, "in")]).k("keys", "y", [(0, 0), (20, 16, "in")])
    c.k("staff", "rx", [(0, 0), (20, -50)])
    return m


# ====================================================================================================
# 1 · LA SOMBRA DE LA LUNA
# ====================================================================================================
def moon_shadow():
    M = dict(
        cloak=dict(kind="wisp", c=(34, 38, 94), hi=(66, 74, 150), lo=(18, 20, 56)),
        cloak2=dict(kind="wisp", c=(26, 28, 72), hi=(48, 54, 118), lo=(12, 14, 40)),
        trim=dict(kind="metal", c=(150, 170, 220), hi=(226, 238, 255), lo=(80, 96, 150)),
        void=dict(kind="flat", c=(4, 4, 16)),
        ghost=dict(kind="grad", c=(150, 172, 214), hi=(188, 206, 238), lo=(110, 130, 176)),
        silver=dict(kind="glow", c=(206, 224, 255), hi=(255, 255, 255), lo=(140, 164, 220), noise=.02),
        pole=dict(kind="grad", c=(54, 44, 72), hi=(86, 74, 112), lo=(30, 24, 44)),
        m_dark=dict(kind="crystal", c=(48, 52, 92), hi=(86, 94, 150), lo=(22, 24, 50)),
        m_half=dict(kind="crystal", c=(150, 170, 220), hi=(230, 240, 255), lo=(60, 70, 120)),
        m_full=dict(kind="glow", c=(236, 244, 255), hi=(255, 255, 255), lo=(190, 210, 250)),
    )
    m = L.Model("moon_shadow", "textures/entity/moon_shadow.png", M, "La Sombra de la Luna")

    def hood_face(im, x0, y0, w, h):
        im.rect(x0 + 1, y0 + 1, x0 + w - 2, y0 + h - 2, (4, 4, 16))
        hline(im, x0, y0, 1, w - 2, 1, (24, 28, 70)); vline(im, x0, y0, 1, 1, h - 2, (24, 28, 70)); vline(im, x0, y0, w - 2, 1, h - 2, (24, 28, 70))
        for ex in (2, w - 4):
            dots(im, x0, y0, [(ex, 4), (ex + 1, 4), (ex, 5), (ex + 1, 5)], (200, 255, 255))
            dots(im, x0, y0, [(ex - 1, 5), (ex + 2, 5)], (90, 200, 230))
        hline(im, x0, y0, 3, w - 4, h - 3, (60, 90, 140))

    def moon_phase(frac):
        def fn(im, x0, y0, w, h):
            for j in range(h):
                for i in range(w):
                    if i / max(1, w - 1) <= frac:
                        im.px(x0 + i, y0 + j, (236, 244, 255))
        return fn

    body = m.add("body", None, (0, 28, 0), walk=[("rx", 0, 0, 14)])
    # cola de capa en cadena (se mece con retraso)
    segs = [("tail1", None, (0, 0, 0), (-5, -6, -3, 10, 6, 6)), ("tail2", "tail1", (0, -6, 0), (-4, -5, -2.5, 8, 5, 5)),
            ("tail3", "tail2", (0, -5, 0), (-3, -5, -2, 6, 5, 4)), ("tail4", "tail3", (0, -5, 0), (-2, -4, -1.5, 4, 4, 3)),
            ("tail5", "tail4", (0, -4, 0), (-1, -4, -1, 2, 4, 2))]
    for name, par, at, bx in segs:
        p = m.add(name, par or "body", at, walk=[("rx", 7, -.55 * int(name[-1]), 11)])
        p.box(*bx, "cloak" if name in ("tail1", "tail3", "tail5") else "cloak2")
    torso = m.add("torso", "body", (0, 0, 0))
    torso.box(-6, 0, -3, 12, 13, 6, "cloak")
    torso.box(-6, 5, -4, 12, 2, 1, "trim")
    torso.box(-8, 10, -4, 16, 4, 8, "cloak2")
    head = m.add("head", "torso", (0, 14, 0), look=True)
    head.box(-5, 0, -5, 10, 10, 10, "cloak2", front=hood_face)
    tip = m.add("hood_tip", "head", (0, 9, 4), rot=(32, 0, 0))
    tip.box(-2, -2, 0, 4, 4, 7, "cloak2")

    # luna creciente a la espalda
    moon = m.add("moon", "torso", (0, 12, 8), spin=(0, 0.5))
    m.arc("mc", "moon", (0, 0, 0), 15, 40, 330, 12, [2, 3, 4, 5, 5, 5, 5, 5, 4, 3, 2, 2], 2, "silver")
    moonf = m.add("moon_full", "torso", (0, 14, 12), p2=True, spin=(0, -0.3))
    moonf.box(-7, -3, 0, 14, 6, 2, "m_full"); moonf.box(-5, -5, 0, 10, 10, 2, "m_full"); moonf.box(-3, -7, 0, 6, 14, 2, "m_full")

    # lunas orbitales: nueva, cuarto, llena
    orbit = m.add("moonlets", "body", (0, 8, 0), spin=(4, 0))
    orbit.box(14, -1, -1.5, 3, 3, 3, "m_dark")
    orbit.box(-6.5, 3, -15, 3, 3, 3, "m_half", front=moon_phase(.5))
    orbit.box(-8, 0, 13, 3, 3, 3, "m_full")

    # brazos flotantes
    def sleeve(side, n):
        x = 8 * side
        a = m.add(f"arm_{n}", "torso", (x, 11, 0), rot=(-18, 0, 8 if side < 0 else -8), walk=[("rx", 6, 0 if side < 0 else math.pi, 0)])
        a.box(-3, -8, -3, 6, 8, 6, "cloak")
        f = m.add(f"forearm_{n}", f"arm_{n}", (0, -8, 0), rot=(-40, 0, 0))
        f.box(-3, -8, -3, 6, 6, 6, "cloak2")
        f.box(-3.5, -9, -3.5, 7, 2, 7, "trim")
        f.box(-1.5, -12, -1.5, 3, 3, 3, "ghost")
    sleeve(-1, "r")
    sleeve(1, "l")
    sc = m.add("scythe", "forearm_r", (0, -11, 0), rot=(40, 0, 0))
    sc.box(-1, -16, -1, 2, 46, 2, "pole")
    sc.box(-1.5, 28, -1.5, 3, 3, 3, "trim")
    m.arc("blade", "scythe", (0, 16, 0), 14, 80, 205, 9, [4, 5, 5, 4, 4, 3, 3, 2, 2], 2, "silver", plane="yz")

    # fase 2: alas de sombra
    for s, n in ((-1, "r"), (1, "l")):
        w = m.add(f"wisp_{n}", "torso", (6 * s, 10, 4), rot=(10, 0, -28 if s < 0 else 28), p2=True)
        w.box(-2, -22, 0, 4, 22, 1, "cloak")
        w2 = m.add(f"wisp2_{n}", f"wisp_{n}", (0, -22, 0), rot=(0, 0, 0), p2=True)
        w2.box(-1.5, -14, 0, 3, 14, 1, "cloak2")

    # ================= animaciones =================
    c = m.clip("idle", IDLE_LEN, loop=True)
    c.k("body", "y", [(0, -1.4), (40, 1.4), (80, -1.4)])
    c.k("torso", "rx", [(0, 1.5), (40, -1.5), (80, 1.5)])
    c.k("head", "rx", [(0, 2), (40, -2), (80, 2)]).k("head", "ry", [(0, 5), (40, -5), (80, 5)])
    c.k("arm_r", "rz", [(0, 3), (40, -5), (80, 3)]).k("arm_l", "rz", [(0, -3), (40, 5), (80, -3)])
    c.k("arm_r", "rx", [(0, -2), (40, 4), (80, -2)]).k("arm_l", "rx", [(0, 4), (40, -2), (80, 4)])
    c.k("tail1", "rx", [(0, -3), (40, 4), (80, -3)]).k("tail2", "rx", [(0, -5), (40, 6), (80, -5)])
    c.k("tail3", "rx", [(0, -7), (40, 8), (80, -7)]).k("tail4", "rx", [(0, -9), (40, 10), (80, -9)]).k("tail5", "rx", [(0, -12), (40, 12), (80, -12)])
    c.k("tail1", "rz", [(0, 3), (40, -3), (80, 3)]).k("tail3", "rz", [(0, 5), (40, -5), (80, 5)]).k("tail5", "rz", [(0, 8), (40, -8), (80, 8)])

    # GOLPE: guadañazo lunar (tick 30)
    c = m.clip("slam", 40)
    c.k("torso", "ry", [(0, 0), (26, -58), (31, 66, "in"), (35, 66), (40, 0)])
    c.k("torso", "rx", [(0, 0), (26, -8), (31, 14, "in"), (40, 0)])
    c.k("arm_r", "rx", [(0, 0), (26, -64), (31, -52), (40, 0)]).k("arm_r", "rz", [(0, 0), (26, 46), (31, -14, "in"), (40, 0)])
    c.k("forearm_r", "rx", [(0, 0), (26, -18), (31, 6), (40, 0)])
    c.k("scythe", "rx", [(0, 0), (26, -24), (31, 24, "in"), (40, 0)])
    c.k("arm_l", "rz", [(0, 0), (26, -34), (31, -8), (40, 0)])
    c.k("body", "y", [(0, 0), (26, 2), (31, -1.5), (40, 0)])
    c.k("moon", "rz", [(0, 0), (31, 80, "in"), (40, 90)])

    # BOMBARDEO: dos manos al frente y rayo lunar
    c = m.clip("cast", 34)
    c.k("arm_r", "rx", [(0, 0), (24, -62), (29, -70), (34, 0)]).k("arm_l", "rx", [(0, 0), (24, -62), (29, -70), (34, 0)])
    c.k("arm_r", "rz", [(0, 0), (24, 14), (34, 0)]).k("arm_l", "rz", [(0, 0), (24, -14), (34, 0)])
    c.k("forearm_r", "rx", [(0, 0), (24, -30), (34, 0)]).k("forearm_l", "rx", [(0, 0), (24, -30), (34, 0)])
    c.k("torso", "rx", [(0, 0), (24, -10), (29, 12, "in"), (34, 0)])
    c.k("head", "rx", [(0, 0), (24, -14), (29, 8), (34, 0)])
    c.k("body", "y", [(0, 0), (24, 3), (34, 0)])
    c.k("moon", "rz", [(0, 0), (29, 140, "in"), (34, 160)])

    # ESBIRROS: aullido a la luna
    c = m.clip("summon", 36)
    c.k("head", "rx", [(0, 0), (12, -38), (28, -38), (36, 0)])
    c.k("arm_r", "rx", [(0, 0), (12, -150), (28, -150), (36, 0)]).k("arm_l", "rx", [(0, 0), (12, -150), (28, -150), (36, 0)])
    c.k("arm_r", "rz", [(0, 0), (12, 22), (28, 22), (36, 0)]).k("arm_l", "rz", [(0, 0), (12, -22), (28, -22), (36, 0)])
    c.k("forearm_r", "rx", [(0, 0), (12, 28), (28, 28), (36, 0)]).k("forearm_l", "rx", [(0, 0), (12, 28), (28, 28), (36, 0)])
    c.k("torso", "rx", [(0, 0), (12, -12), (28, -12), (36, 0)])
    c.k("body", "y", [(0, 0), (12, 7), (28, 7), (36, 0)])
    c.k("moon", "rz", [(0, 0), (12, 60), (28, 120), (36, 180)])
    c.k("moon_full", "y", [(0, 0), (12, 3), (28, 3), (36, 0)])
    for t, a in (("tail1", 12), ("tail2", 20), ("tail3", 28), ("tail4", 36), ("tail5", 44)):
        c.k(t, "rx", [(0, 0), (12, a), (28, a), (36, 0)])

    # ESPECIAL: eclipse (gira dos veces y estalla ~tick 40)
    c = m.clip("special", 46)
    c.k("body", "y", [(0, 0), (14, 9), (38, 9), (42, -2, "in"), (46, 0)])
    c.k("torso", "ry", [(0, 0), (6, 0), (38, 720, "in"), (46, 720)])
    c.k("arm_r", "rz", [(0, 0), (14, 80), (38, 80), (46, 0)]).k("arm_l", "rz", [(0, 0), (14, -80), (38, -80), (46, 0)])
    c.k("arm_r", "rx", [(0, 0), (14, -10), (46, 0)]).k("arm_l", "rx", [(0, 0), (14, -10), (46, 0)])
    c.k("head", "rx", [(0, 0), (14, -22), (38, -22), (44, 8), (46, 0)])
    c.k("moon", "rz", [(0, 0), (38, 360), (46, 400)])
    for t, a in (("tail1", 8), ("tail2", 16), ("tail3", 24), ("tail4", 32), ("tail5", 40)):
        c.k(t, "rx", [(0, 0), (14, -a), (38, -a), (46, 0)])

    # FASE 2: se eleva y tiembla
    c = m.clip("enrage", 44)
    c.k("body", "y", [(0, 0), (10, 8), (34, 8), (44, 0)])
    c.k("head", "rx", [(0, 0), (10, -34), (34, -34), (44, 0)])
    c.k("arm_r", "rz", [(0, 0), (10, 75), (34, 75), (44, 0)]).k("arm_l", "rz", [(0, 0), (10, -75), (34, -75), (44, 0)])
    c.k("torso", "rz", [(0, 0), (12, 4), (16, -4), (20, 4), (24, -4), (28, 4), (32, -4), (36, 0)])
    c.k("moon", "rz", [(0, 0), (34, 300, "in"), (44, 360)])
    for t, a in (("tail1", 10), ("tail2", 18), ("tail3", 26), ("tail4", 34), ("tail5", 42)):
        c.k(t, "rx", [(0, 0), (10, -a), (34, -a), (44, 0)])

    # MUERTE: la sombra se desvanece cayendo
    c = m.clip("death", DEATH_LEN)
    c.k("body", "y", [(0, 0), (20, -9, "in")])
    c.k("arm_r", "rz", [(0, 0), (14, 36)]).k("arm_l", "rz", [(0, 0), (14, -36)])
    c.k("head", "rx", [(0, 0), (16, 40)])
    c.k("moon", "y", [(0, 0), (20, 14, "in")]).k("moon", "rz", [(0, 0), (20, 180)])
    c.k("moonlets", "y", [(0, 0), (20, 18, "in")])
    for t, a in (("tail1", 8), ("tail2", 16), ("tail3", 24), ("tail4", 32), ("tail5", 40)):
        c.k(t, "rx", [(0, 0), (20, a)])
    return m


# ====================================================================================================
# 2 · EL JUICIO FINAL
# ====================================================================================================
def judgement():
    M = dict(
        plate=dict(kind="metal", c=(208, 170, 74), hi=(255, 230, 138), lo=(120, 82, 24)),
        ivory=dict(kind="metal", c=(226, 220, 204), hi=(252, 250, 240), lo=(150, 140, 126)),
        dark=dict(kind="stone", c=(40, 32, 40), hi=(62, 52, 62), lo=(20, 16, 22), noise=.03),
        cloth=dict(kind="cloth", c=(150, 34, 44), hi=(190, 54, 62), lo=(84, 16, 26)),
        glow=dict(kind="glow", c=(255, 190, 80), hi=(255, 250, 200), lo=(255, 150, 40), noise=.02),
        feather=dict(kind="feather", c=(236, 222, 190), hi=(255, 252, 240), lo=(244, 150, 60)),
        feather2=dict(kind="feather", c=(250, 190, 90), hi=(255, 240, 170), lo=(220, 60, 30)),
        ember=dict(kind="crystal", c=(255, 150, 60), hi=(255, 240, 160), lo=(200, 60, 20), noise=.02),
    )
    m = L.Model("last_judgement", "textures/entity/last_judgement.png", M, "El Juicio Final")

    def visor(im, x0, y0, w, h):
        im.rect(x0 + 1, y0 + 4, x0 + w - 2, y0 + 5, (255, 244, 190))
        hline(im, x0, y0, 1, w - 2, 3, (60, 40, 10)); hline(im, x0, y0, 1, w - 2, 6, (60, 40, 10))
        vline(im, x0, y0, w // 2, 6, h - 2, (60, 40, 10))
        hline(im, x0, y0, 2, w - 3, h - 2, (60, 40, 10))

    def chest(im, x0, y0, w, h):  # balanza del juicio
        cx = w // 2
        vline(im, x0, y0, cx, 3, 12, (70, 40, 10)); vline(im, x0, y0, cx - 1, 3, 12, (255, 230, 138))
        hline(im, x0, y0, cx - 6, cx + 5, 4, (255, 230, 138)); hline(im, x0, y0, cx - 6, cx + 5, 5, (120, 82, 24))
        for sx in (cx - 6, cx + 5):
            vline(im, x0, y0, sx, 5, 8, (70, 40, 10)); hline(im, x0, y0, sx - 2, sx + 2, 9, (255, 150, 40))
        dots(im, x0, y0, [(cx, 2), (cx - 1, 2)], (255, 250, 200))

    # ---- piernas ----
    for s, n in ((-1, "r"), (1, "l")):
        up = m.add(f"leg_{n}", None, (6 * s, 28, 0), walk=[("rx", 32, 0 if s < 0 else math.pi, 0)])
        up.box(-4, -14, -4, 8, 14, 8, "plate")
        up.box(-5, -4, -5, 10, 5, 2, "ivory")
        lo = m.add(f"shin_{n}", f"leg_{n}", (0, -14, 0), walk=[("rx", 14, (0 if s < 0 else math.pi) + .9, 12)])
        lo.box(-4, -14, -4, 8, 14, 8, "dark")
        lo.box(-5, -11, -5, 10, 7, 1, "plate")
        lo.box(-4, -14, -8, 8, 4, 12, "plate")
    sk = m.add("skirt", None, (0, 28, 0))
    sk.box(-9, -9, -6, 18, 9, 12, "plate")
    sk.box(-7, -12, -7, 5, 12, 1, "ivory"); sk.box(2, -12, -7, 5, 12, 1, "ivory")
    tab = m.add("tabard", "skirt", (0, 0, -7), walk=[("rx", -5, 0, 0)])
    tab.box(-3, -18, -1, 6, 18, 1, "cloth")
    tab.box(-3, -19, -1, 6, 1, 1, "plate")

    # ---- torso ----
    torso = m.add("torso", None, (0, 28, 0), walk=[("rx", 0, 0, 5)])
    torso.box(-9, 0, -5, 18, 18, 10, "plate", front=chest)
    torso.box(-6, -4, -4, 12, 4, 8, "dark")
    torso.box(-10, 16, -6, 20, 3, 12, "ivory")
    torso.box(-6, 4, 5, 12, 12, 2, "ivory")

    head = m.add("head", "torso", (0, 19, 0), look=True)
    head.box(-5, 0, -5, 10, 10, 10, "plate", front=visor)
    head.box(-1, 10, -5, 2, 6, 10, "ivory")
    for s, n in ((-1, "r"), (1, "l")):
        hn = m.add(f"horn_{n}", "head", (6 * s, 8, 0), rot=(0, 0, 30 if s < 0 else -30))
        hn.box(-1.5, 0, -1.5, 3, 9, 3, "ivory")

    # ---- aureola (anillo que gira) ----
    halo = m.add("halo", "torso", (0, 26, 9), spin=(0, 1.0))
    m.arc("hr", "halo", (0, 0, 0), 15, 0, 360, 14, 3, 2, "glow")
    halo2 = m.add("halo2", "torso", (0, 26, 11), spin=(0, -1.6), p2=True)
    m.arc("hs", "halo2", (0, 0, 0), 9, 0, 360, 10, 3, 2, "ember", p2=True)

    # ---- alas ----
    for s, n in ((-1, "r"), (1, "l")):
        wing = m.add(f"wing_{n}", "torso", (5 * s, 14, 6), rot=(12, 0, 0))
        wing.box(-6 if s < 0 else 0, -2, -1, 6, 4, 3, "ivory")
        lens = (22, 27, 31, 30, 26, 20)
        for i, ln in enumerate(lens):
            ang = 58 + i * 17
            fa = m.add(f"fea_{n}{i}", f"wing_{n}", (s * (1 + i * .6), 0, 1 + (i % 3) * 1.3), rot=(0, 0, ang if s < 0 else -ang))
            fa.box(-2, -ln, 0, 4, ln, 1, "feather")
        for i, ln in enumerate((38, 42, 38)):
            ang = 80 + i * 26
            fb = m.add(f"feb_{n}{i}", f"wing_{n}", (s * (2 + i), 0, 5 + i * 1.3), rot=(0, 0, ang if s < 0 else -ang), p2=True)
            fb.box(-2, -ln, 0, 4, ln, 1, "feather2")

    # ---- brazo derecho + martillo ----
    def arm(side, n, rest, frest):
        x = 13 * side
        a = m.add(f"arm_{n}", "torso", (x, 15, 0), rot=rest, walk=[("rx", 10, math.pi if side < 0 else 0, 0)])
        a.box(-5, 0, -5, 10, 6, 10, "plate")
        a.box(-1.5, 6, -1.5, 3, 6, 3, "ivory")
        a.box(-4, -12, -4, 8, 12, 8, "dark")
        f = m.add(f"forearm_{n}", f"arm_{n}", (0, -12, 0), rot=frest)
        f.box(-4, -12, -4, 8, 12, 8, "plate")
        f.box(-5, -4, -5, 10, 3, 10, "ivory")
        f.box(-3, -15, -3, 6, 3, 6, "dark")
        return a, f
    arm(-1, "r", (-8, 0, 6), (-22, 0, 0))
    arm(1, "l", (-10, 0, -6), (-52, 0, 0))
    ham = m.add("hammer", "forearm_r", (0, -14, 0), rot=(30, 0, 0))
    ham.box(-2, -12, -2, 4, 50, 4, "dark")
    ham.box(-7, 36, -4.5, 14, 11, 9, "plate")
    ham.box(-8, 38, -3, 1, 7, 6, "ivory"); ham.box(7, 38, -3, 1, 7, 6, "ivory")
    ham.box(-3, 38, -5.5, 6, 7, 1, "glow")
    ham.box(-1, 39, 4.5, 2, 5, 4, "ivory")
    ham.box(-3, -14, -3, 6, 2, 6, "plate")
    tr = m.add("trumpet", "forearm_l", (0, -14, 0), rot=(20, 0, 0))
    tr.box(-1, -1, 0, 2, 2, 2, "ivory")
    tr.box(-1, -1, -18, 2, 2, 18, "plate")
    tr.box(-2, -2, -22, 4, 4, 4, "plate")
    tr.box(-3, -3, -25, 6, 6, 3, "plate")
    tr.box(-4, -4, -27, 8, 8, 2, "glow")

    # ================= animaciones =================
    c = m.clip("idle", IDLE_LEN, loop=True)
    c.k("torso", "y", [(0, 0), (40, 1.0), (80, 0)]).k("torso", "rx", [(0, 0), (40, -2), (80, 0)])
    c.k("head", "rx", [(0, 1), (40, -2), (80, 1)]).k("head", "ry", [(0, -3), (40, 3), (80, -3)])
    c.k("arm_r", "rx", [(0, 0), (40, -3), (80, 0)]).k("arm_l", "rx", [(0, -3), (40, 0), (80, -3)])
    c.k("tabard", "rx", [(0, 3), (40, -3), (80, 3)])
    for n, s in (("r", 1), ("l", -1)):
        c.k(f"wing_{n}", "rz", [(0, -4 * s), (40, 6 * s), (80, -4 * s)])
        for i in range(6):
            c.k(f"fea_{n}{i}", "rz", [(0, -2 * s * (1 + i * .25)), (40, 3 * s * (1 + i * .25)), (80, -2 * s * (1 + i * .25))])
    c.k("halo", "y", [(0, 0), (40, 1.5), (80, 0)])

    # GOLPE: martillazo (tick 30)
    c = m.clip("slam", 40)
    c.k("arm_r", "rx", [(0, 0), (26, -122), (31, -34, "in"), (36, -34), (40, 0)])
    c.k("forearm_r", "rx", [(0, 0), (26, -20), (31, 12, "in"), (40, 0)])
    c.k("hammer", "rx", [(0, 0), (26, -10), (31, 40, "in"), (36, 40), (40, 0)])
    c.k("arm_l", "rx", [(0, 0), (26, -34), (31, 10), (40, 0)]).k("arm_l", "rz", [(0, 0), (26, -22), (31, 0), (40, 0)])
    c.k("torso", "rx", [(0, 0), (26, -13), (31, 20, "in"), (36, 16), (40, 0)])
    c.k("torso", "y", [(0, 0), (26, 3), (31, -4, "in"), (36, -2), (40, 0)])
    c.k("head", "rx", [(0, 0), (26, -16), (31, 14), (40, 0)])
    for n, s in (("r", 1), ("l", -1)):
        c.k(f"wing_{n}", "rz", [(0, 0), (26, 22 * s), (31, -12 * s, "in"), (40, 0)])
    c.k("leg_r", "rx", [(0, 0), (26, -12), (31, 12), (40, 0)]).k("leg_l", "rx", [(0, 0), (26, 10), (31, -4), (40, 0)])

    # BOMBARDEO: señala con el martillo / alas abiertas
    c = m.clip("cast", 34)
    c.k("arm_r", "rx", [(0, 0), (24, -92), (29, -104), (34, 0)])
    c.k("forearm_r", "rx", [(0, 0), (24, -10), (34, 0)])
    c.k("hammer", "rx", [(0, 0), (24, -20), (29, 10), (34, 0)])
    c.k("arm_l", "rx", [(0, 0), (24, -24), (34, 0)])
    c.k("torso", "rx", [(0, 0), (24, -9), (29, 11, "in"), (34, 0)])
    c.k("head", "rx", [(0, 0), (24, -10), (29, 8), (34, 0)])
    for n, s in (("r", 1), ("l", -1)):
        c.k(f"wing_{n}", "rz", [(0, 0), (24, 26 * s), (34, 0)])
    c.k("halo", "y", [(0, 0), (24, 4), (34, 0)])

    # ESBIRROS: toca la trompeta del juicio
    c = m.clip("summon", 36)
    c.k("arm_l", "rx", [(0, 0), (12, -82), (28, -82), (36, 0)]).k("arm_l", "rz", [(0, 0), (12, 4), (36, 0)])
    c.k("forearm_l", "rx", [(0, 0), (12, -66), (28, -66), (36, 0)])
    c.k("trumpet", "rx", [(0, 0), (12, 14), (28, 14), (36, 0)])
    c.k("head", "rx", [(0, 0), (12, -26), (28, -26), (36, 0)])
    c.k("torso", "rx", [(0, 0), (12, -14), (28, -14), (36, 0)]).k("torso", "y", [(0, 0), (12, 1.5), (28, 1.5), (36, 0)])
    c.k("arm_r", "rx", [(0, 0), (12, -8), (28, -8), (36, 0)])
    for n, s in (("r", 1), ("l", -1)):
        c.k(f"wing_{n}", "rz", [(0, 0), (12, 34 * s), (28, 34 * s), (36, 0)]).k(f"wing_{n}", "rx", [(0, 0), (12, -12), (28, -12), (36, 0)])
    c.k("halo", "y", [(0, 0), (12, 5), (28, 5), (36, 0)])

    # ESPECIAL (corona de fuego): agacharse, saltar y estrellar el martillo ~tick 36
    c = m.clip("special", 46)
    c.k("torso", "y", [(0, 0), (10, -5), (22, 16), (30, 16), (36, -4, "in"), (46, 0)])
    c.k("leg_r", "y", [(0, 0), (10, 0), (22, 16), (30, 16), (36, 0, "in"), (46, 0)]).k("leg_l", "y", [(0, 0), (10, 0), (22, 16), (30, 16), (36, 0, "in"), (46, 0)])
    c.k("skirt", "y", [(0, 0), (10, -3), (22, 16), (30, 16), (36, 0, "in"), (46, 0)])
    c.k("leg_r", "rx", [(0, 0), (10, -38), (22, 18), (36, -10), (46, 0)]).k("leg_l", "rx", [(0, 0), (10, -38), (22, 18), (36, -10), (46, 0)])
    c.k("shin_r", "rx", [(0, 0), (10, 52), (22, 30), (36, 6), (46, 0)]).k("shin_l", "rx", [(0, 0), (10, 52), (22, 30), (36, 6), (46, 0)])
    c.k("arm_r", "rx", [(0, 0), (22, -150), (30, -150), (36, -30, "in"), (41, -30), (46, 0)])
    c.k("arm_l", "rx", [(0, 0), (22, -130), (30, -130), (36, -20, "in"), (46, 0)])
    c.k("hammer", "rx", [(0, 0), (22, 0), (36, 44, "in"), (46, 0)])
    c.k("torso", "rx", [(0, 0), (10, 14), (22, -14), (36, 22, "in"), (42, 16), (46, 0)])
    c.k("head", "rx", [(0, 0), (22, -22), (36, 16), (46, 0)])
    for n, s in (("r", 1), ("l", -1)):
        c.k(f"wing_{n}", "rz", [(0, 0), (10, -10 * s), (22, 40 * s), (30, 40 * s), (36, -14 * s, "in"), (46, 0)])
    c.k("halo", "y", [(0, 0), (22, 4), (36, -1), (46, 0)])

    # FASE 2: rugido, alas completamente abiertas
    c = m.clip("enrage", 44)
    c.k("head", "rx", [(0, 0), (10, -36), (34, -36), (44, 0)])
    c.k("torso", "rx", [(0, 0), (10, -16), (34, -16), (44, 0)])
    c.k("torso", "rz", [(0, 0), (12, 2), (16, -2), (20, 2), (24, -2), (28, 2), (32, -2), (36, 0)])
    c.k("arm_r", "rz", [(0, 0), (10, 52), (34, 52), (44, 0)]).k("arm_l", "rz", [(0, 0), (10, -52), (34, -52), (44, 0)])
    c.k("arm_r", "rx", [(0, 0), (10, -20), (34, -20), (44, 0)]).k("arm_l", "rx", [(0, 0), (10, -20), (34, -20), (44, 0)])
    for n, s in (("r", 1), ("l", -1)):
        c.k(f"wing_{n}", "rz", [(0, 0), (10, 46 * s), (34, 46 * s), (44, 0)]).k(f"wing_{n}", "rx", [(0, 0), (10, -14), (34, -14), (44, 0)])
    c.k("halo", "y", [(0, 0), (10, 8), (34, 8), (44, 0)])

    # MUERTE: cae de rodillas, las alas se pliegan, el martillo se suelta
    c = m.clip("death", DEATH_LEN)
    c.k("torso", "y", [(0, 0), (20, -8, "in")]).k("torso", "rx", [(0, 0), (20, 24)])
    c.k("head", "rx", [(0, 0), (20, 40)])
    c.k("leg_r", "rx", [(0, 0), (20, -40)]).k("leg_l", "rx", [(0, 0), (20, -40)])
    c.k("shin_r", "rx", [(0, 0), (20, 70)]).k("shin_l", "rx", [(0, 0), (20, 70)])
    c.k("arm_r", "rz", [(0, 0), (16, 30)]).k("arm_l", "rz", [(0, 0), (16, -30)])
    for n, s in (("r", 1), ("l", -1)):
        c.k(f"wing_{n}", "rz", [(0, 0), (20, -30 * s)])
    c.k("halo", "y", [(0, 0), (20, 18, "in")])
    c.k("hammer", "rx", [(0, 0), (20, 60)])
    return m


BOSSES = [("hierophant", hierophant), ("moon_shadow", moon_shadow), ("last_judgement", judgement)]


# ====================================================================================================
def write_java_anim():
    lines = ["package com.tarotmod.boss.entity;", "",
             "/** GENERADO por gen_bosses.py: IDs y duraciones (ticks) de las animaciones de acción de los jefes. */",
             "public final class BossAnim {", "    private BossAnim() {}", "", "    public static final int IDLE = 0;"]
    for i, (n, _l) in enumerate(ANIMS, 1):
        lines.append(f"    public static final int {n.upper()} = {i};")
    lines += ["", "    /** Nombre de clip por ID (el índice 0 es 'sin animación'). */",
              "    public static final String[] NAMES = {\"idle\", " + ", ".join(f'"{n}"' for n, _ in ANIMS) + "};",
              "    /** Duración en ticks por ID. */",
              "    public static final int[] LENGTH = {0, " + ", ".join(str(l) for _, l in ANIMS) + "};", "",
              f"    public static final int DEATH_LENGTH = {DEATH_LEN};", "}", ""]
    os.makedirs(os.path.dirname(OUT_JAVA), exist_ok=True)
    open(OUT_JAVA, "w").write("\n".join(lines))


def build(mdl):
    for name, length in ANIMS:
        assert name in mdl.clips and mdl.clips[name].length == length, f"{mdl.id}: falta clip {name}"
    assert "idle" in mdl.clips and "death" in mdl.clips
    S = L.pack_uv(mdl)
    im = L.paint_model(mdl, seed=zlib.crc32(mdl.id.encode()) % 997)
    return S, im


def main():
    os.makedirs(OUT_JSON, exist_ok=True); os.makedirs(OUT_TEX, exist_ok=True)
    write_java_anim()
    built = []
    for bid, fn in BOSSES:
        mdl = fn()
        S, im = build(mdl)
        im.save(f"{OUT_TEX}/{bid}.png")
        json.dump(L.export(mdl), open(f"{OUT_JSON}/{bid}.json", "w"), separators=(",", ":"))
        nb = sum(len(p.boxes) for p in mdl.parts)
        print(f"{bid}: {len(mdl.parts)} partes, {nb} cajas, textura {S}x{S}, {len(mdl.clips)} clips")
        built.append(mdl)
    return built


if __name__ == "__main__":
    models = main()
    if "--preview" in sys.argv:
        import previews
        previews.run(models)
