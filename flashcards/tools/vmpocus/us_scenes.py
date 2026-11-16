"""Fábricas de cenas anatômicas sintéticas para o POCUS 360X (pulmão, coração, VCI, abdome, vasos, olho, diafragma...)."""
import math, random
from us_core import Scene

TIS, MUS, FAT, FLU, BRI = 0.32, 0.26, 0.18, 0.012, 0.95


def wall(sc, rng, z0=0.0, z1=1.4, lines=5):
    sc.band(z0, z0 + 0.25, 0.4); sc.band(z0 + 0.25, z0 + 0.6, 0.14)
    sc.band(z0 + 0.6, z1, 0.2)
    for i in range(lines):
        z = z0 + 0.7 + (z1 - z0 - 0.75) * (i + rng.random() * 0.5) / lines; sc.line([(sc.x0, z), (sc.x1, z + rng.uniform(-0.1, 0.1))], 0.04, 0.42)


# ------------------------------------------------------------------------------------------------ PULMÃO
def lung(probe="convex", depth=12, pat="A", bl=(), cons=None, ribs=True, pleura_irreg=False, zp=None, seed=0, subpl=(), linear_w=4.5):
    """pat: A (linhas A), B (linhas B: bl=[(x,w,amp)]), C (consolidação cons=dict(x0,x1,z1,bron=True, shred=True)), N (pleura sem ar = derrame/consolidação total)"""
    rng = random.Random(seed)
    sc = Scene(probe, depth, width=linear_w, angle=60 if probe == "convex" else 80)
    zp = zp or (1.9 if probe == "convex" else 1.3)
    wall(sc, rng, 0, zp - 0.15)
    xr = 2.7 if probe == "convex" else 2.0
    if ribs:
        cx_, rx_ = (xr * 1.6, 2.25) if probe == "convex" else (linear_w / 2 + 0.25, 0.75)
        for x in (-cx_, cx_): sc.ell(x, zp - 0.25, rx_, 0.42, BRI, a=12.0); sc.ell(x, zp + 0.1, rx_ * 0.95, 0.3, 0.0, a=12.0)
    pl = [(sc.x0 + i * (sc.x1 - sc.x0) / 30, zp + (0.04 * math.sin(i * 1.7) if pleura_irreg else 0) + (rng.uniform(-0.06, 0.06) if pleura_irreg else 0)) for i in range(31)]
    if pat == "C" and cons:
        x0, x1, z1 = cons["x0"], cons["x1"], cons["z1"]
        left = [p for p in pl if p[0] <= x0]; right = [p for p in pl if p[0] >= x1]
        if left: sc.air_below(left + [(x0, zp)])
        if right: sc.air_below([(x1, zp)] + right)
        # tecido hepatizado
        pts = [(x0, zp)] + [(x0 + (x1 - x0) * i / 12, zp + 0.05) for i in range(13)] + [(x1, zp)]
        deep = [(x1 - (x1 - x0) * i / 16, z1 + (rng.uniform(-0.7, 0.7) if cons.get("shred", True) else 0)) for i in range(17)]
        sc.poly(pts + deep, 0.42, a=0.12)
        for i in range(12): sc.line([(x0 + (x1 - x0) * rng.random(), zp + 0.3 + (z1 - zp) * rng.random()) for _ in range(2)], 0.04, 0.5)
        if cons.get("bron", True):
            for _ in range(cons.get("nb", 14)):
                x = rng.uniform(x0 + 0.3, x1 - 0.3); z = rng.uniform(zp + 0.6, z1 - 0.5)
                sc.line([(x, z), (x + rng.uniform(-0.5, 0.5), z + rng.uniform(0.3, 0.9))], 0.13, BRI, a=0.6 if cons.get("dyn") else 1.5)
        if cons.get("fluid_bron"):
            for _ in range(5):
                x = rng.uniform(x0 + 0.5, x1 - 0.5); z = rng.uniform(zp + 0.8, z1 - 0.8)
                sc.line([(x, z), (x + 0.6, z + 0.9)], 0.18, FLU); sc.line([(x - 0.08, z), (x + 0.52, z + 0.9)], 0.04, 0.7)
        if cons.get("shred", True): sc.air_below(deep[::-1])
        sc.line(pl, 0.09, 0.85)
    elif pat == "N":
        sc.line(pl, 0.08, 0.7)
    else:
        sc.air_below(pl); sc.line(pl, 0.1 if not pleura_irreg else 0.16, BRI)
        if pat == "B":
            sc.alines = False if len(bl) > 3 else True
            sc.blines = list(bl)
        if pleura_irreg and subpl:
            for (x, w, d) in subpl: sc.poly([(x - w / 2, zp), (x, zp + d), (x + w / 2, zp)], 0.4, a=0.2)
    return sc


def effusion(depth=16, size="grande", septa=0, echo=0.0, lung_tongue=True, spine=True, seed=0, side="dir", cal=None, lung="ar"):
    """Corte coronal posterolateral (marcador cefálico à esquerda): tórax à esquerda, fígado/baço à direita."""
    rng = random.Random(seed); sc = Scene("convex", depth, angle=70); sc.alines = True
    wall(sc, rng, 0, 1.6)
    dia = [(2.6, 1.6), (1.6, 4.5), (0.7, 8.0), (0.1, 12.0), (-0.3, depth + 1)]
    sc.poly([(sc.x1, 1.6)] + dia + [(sc.x1, depth + 1)], 0.34)  # víscera
    for _ in range(30): sc.ell(rng.uniform(1.5, 10), rng.uniform(3, depth), rng.uniform(0.2, 0.5), rng.uniform(0.1, 0.25), 0.44)
    zs = 12.6  # coluna
    if size == "grande": edge = None; fl = [(sc.x0, 1.6), (2.6, 1.6)] + dia[1:4] + [(sc.x0, zs)]
    elif size == "moderado": edge = [(-1.6, 1.6), (-5.8, zs), (-5.8, depth + 1)]; fl = [(-1.6, 1.6), (2.6, 1.6)] + dia[1:4] + [(-5.8, zs)]
    elif size == "pequeno": edge = [(0.9, 1.6), (1.1, 6.6)] + dia[2:]; fl = [(0.9, 1.6), (2.6, 1.6), (1.6, 4.5), (1.1, 6.6)]
    else: edge = [(2.6, 1.6)] + dia[1:]; fl = None
    if edge:
        lp = [(sc.x0, 1.6)] + edge + [(sc.x0, depth + 1)]
        if lung == "cons":
            sc.poly(lp, 0.5, a=0.12)
            for _ in range(14):
                x = rng.uniform(-9, edge[0][0] - 1.5); z = rng.uniform(2.5, 10)
                sc.line([(x, z), (x + rng.uniform(-0.5, 0.5), z + rng.uniform(0.3, 0.8))], 0.12, BRI, a=1.5)
        else:
            sc.poly(lp, 0.0, a=9.0); sc.dAir.polygon([sc.p(x, z) for x, z in lp], fill=1.0)
    if fl is None:
        sc.line(dia, 0.2, BRI); sc.label(6.5, depth - 2, "fígado" if side == "dir" else "baço"); return sc
    sc.poly(fl, FLU + echo, a=0.0)
    if echo: sc.dots(int(220 * echo / 0.1), (-6, 1), (2, 11), 0.05, 0.45, rng)
    for k in range(septa):
        x = rng.uniform(-6, -1); sc.line([(x, 2.4), (x + rng.uniform(-1.5, 1.5), 5), (x + rng.uniform(-1, 2), 10)], 0.07, 0.85)
    sc.line(dia, 0.2, BRI)
    if lung_tongue and size == "grande":
        sc.poly([(sc.x0, 3.0), (-2.2, 5.6), (sc.x0, 8.8)], 0.46, a=0.15)
        for _ in range(5): sc.line([(rng.uniform(-8, -4), rng.uniform(4.5, 7)), (rng.uniform(-5, -3), rng.uniform(5, 6.5))], 0.07, 0.9)
    if spine:
        sc.line([(-0.6, zs + 0.2), (-10, zs + 0.5)], 0.35, BRI, a=12)
        if size in ("grande", "moderado"): sc.label(-3.2 if size == "moderado" else -5.5, zs - 0.9, "coluna")
    if lung == "cons" and size != "grande": sc.label(-7.5, 6.0, "pulmão consolidado")
    sc.label(6.5, depth - 2, "fígado" if side == "dir" else "baço")
    if cal: sc.mark("cal", (-2.6, 10.5 - cal), (-2.6, 10.5), f"{cal * 10:.0f} mm")
    return sc


# ------------------------------------------------------------------------------------------------ CORAÇÃO
def _chamber(sc, cx, cz, rx, rz, th, rot=0.0, myo=0.4):
    sc.ell(cx, cz, rx + th, rz + th, myo, a=0.12, rot=rot); sc.ell(cx, cz, rx, rz, FLU, a=0.0, rot=rot)


def plax(depth=16, lv=(2.4, 1.8), ef="normal", peff=0.0, rv=1.0, seed=0, ao=1.3, la=1.9, fat=False, pleff=0.0):
    rng = random.Random(seed); sc = Scene("sector", depth, angle=80); sc.alines = False
    sc.band(0, 1.0, 0.25)
    # VD anterior
    _chamber(sc, -0.5, 3.0, 2.9, 0.75 * rv, 0.45, rot=0.12)
    # septo e VE (elipse inclinada)
    th = 1.0 if ef != "hipertrofia" else 1.6
    _chamber(sc, -1.2, 5.6 + 0.6 * rv, 3.6, lv[1], th, rot=0.18)
    # raiz aórtica e AE
    sc.ell(3.6, 5.0 + 0.3 * rv, 1.9, ao * 0.5, FLU, a=0.0, rot=-0.05); sc.line([(1.9, 4.4 + 0.3 * rv), (5.4, 4.3 + 0.3 * rv)], 0.12, 0.8); sc.line([(1.9, 5.7 + 0.3 * rv), (5.4, 5.8 + 0.3 * rv)], 0.12, 0.8)
    sc.ell(3.9, 8.0 + 0.3 * rv, la * 0.9, la * 0.7, FLU, a=0.0)
    sc.line([(1.8, 6.2 + 0.4 * rv), (0.6, 7.0 + 0.4 * rv)], 0.1, 0.85); sc.line([(2.2, 7.4 + 0.4 * rv), (1.2, 7.9 + 0.4 * rv)], 0.08, 0.8)
    # pericárdio posterior + aorta descendente
    zp = 8.4 + 0.6 * rv
    if peff:
        sc.poly([(-6, zp - 0.3), (-1, zp + 0.1), (2.0, zp + 0.35), (3.3, zp + 0.55), (3.6, zp + 0.5 + peff * 0.35), (2.0, zp + 0.35 + peff * 0.75), (-1, zp + 0.1 + peff), (-6, zp - 0.3 + peff)], FLU, a=0.0); zp += peff
    sc.line([(-5.5, zp), (0, zp + 0.3), (3, zp + 0.6)], 0.22, BRI, a=1.0)
    sc.ell(3.6, zp + 1.3, 0.75, 0.75, FLU, a=0.0); sc.ring(3.6, zp + 1.3, 0.75, 0.75, 0.08, 0.8)
    if pleff: sc.poly([(-7, zp + 2.7), (-2, zp + 2.45), (2, zp + 2.25), (4.5, zp + 2.2), (6.5, zp + 2.6), (6.5, zp + 3.0), (2, zp + 2.25 + pleff * 1.5), (-7, zp + 2.7 + pleff * 2.3)], FLU, a=0.0)
    if fat: sc.poly([(-3.2, 1.35), (3, 1.25), (3.3, 2.15), (-3.4, 2.35)], 0.1, a=0.1); sc.dots(60, (-3, 3), (1.4, 2.2), 0.05, 0.3, rng)
    sc.label(3.6, zp + 2.6, "Ao desc.")
    return sc


def psax(depth=16, rv_ratio=0.6, dsign=False, peff=0.0, ef="normal", seed=0, hyper=False):
    rng = random.Random(seed); sc = Scene("sector", depth, angle=80); sc.alines = False
    sc.band(0, 1.0, 0.25)
    cz = 7.2; R = 2.0 if not hyper else 1.3; th = 1.0 if not hyper else 1.8
    if peff: sc.ell(0.2, cz, R + th + peff + 0.3, R + th + peff + 0.3, FLU, a=0.0); sc.ring(0.2, cz, R + th + peff + 0.4, R + th + peff + 0.4, 0.2, BRI)
    else: sc.ring(0.2, cz, R + th + 0.35, R + th + 0.35, 0.2, BRI, a=0.6)
    # VD em crescente (anterior-esquerda da tela)
    rv = R * (0.9 + 1.6 * rv_ratio)
    sc.ell(-1.6 * (0.6 + rv_ratio), cz - R * 0.9, rv, R * (0.55 + 0.6 * rv_ratio), 0.4, a=0.12, rot=-0.5)
    sc.ell(-1.6 * (0.6 + rv_ratio), cz - R * 0.9, rv - 0.4, R * (0.55 + 0.6 * rv_ratio) - 0.4, FLU, a=0.0, rot=-0.5)
    sc.ell(0.2, cz, R + th, R + th, 0.42, a=0.12)
    if dsign:  # septo retificado: VE em "D"
        pts = [(0.2 + R * math.cos(t), cz + R * math.sin(t)) for t in [math.radians(a) for a in range(-40, 230, 6)]]
        sc.poly(pts + [(0.2 + R * math.cos(math.radians(-40)), cz + R * math.sin(math.radians(-40)))], FLU, a=0.0)
        sc.line([(0.2 + R * math.cos(math.radians(230)) + 0.2, cz + R * math.sin(math.radians(230))), (0.2 + R * math.cos(math.radians(-40)), cz + R * math.sin(math.radians(-40)))], 0.25, 0.42)
    else:
        sc.ell(0.2, cz, R, R, FLU, a=0.0)
    # músculos papilares
    for a in (110, 60): sc.ell(0.2 + 0.75 * R * math.cos(math.radians(a)), cz + 0.75 * R * math.sin(math.radians(a)), 0.35, 0.28, 0.42)
    return sc


def a4c(depth=17, rv_ratio=0.7, peff=0.0, la=1.0, ra=1.0, seed=0, thrombus=False, rv_dil_apex=False, lvw=1.6):
    rng = random.Random(seed); sc = Scene("sector", depth, angle=80); sc.alines = False
    sc.band(0, 0.8, 0.25)
    # ápice no topo; VE à direita da tela, VD à esquerda (convenção cardiológica)
    if peff: sc.ell(0.2, 7.2, 4.2 + rv_ratio + peff, 6.4 + peff, FLU, a=0.0)
    sc.ell(0.2, 7.2, 4.2 + rv_ratio, 6.4, BRI * 0.8, a=0.3); sc.ell(0.2, 7.2, 4.0 + rv_ratio, 6.2, 0.36)
    sc.ell(1.75, 6.4, lvw + 0.7, 4.3, 0.42, a=0.12, rot=-0.12); sc.ell(1.75, 6.6, lvw, 3.6, FLU, a=0.0, rot=-0.12)
    rx = 0.4 + 1.3 * rv_ratio; rz = 3.0 + (1.2 if rv_dil_apex else 0.0) * rv_ratio
    sc.ell(-0.35 - rx, 7.4 - (0.6 if rv_dil_apex else 0), rx + 0.35, rz + 0.4, 0.42, a=0.12, rot=0.25); sc.ell(-0.35 - rx, 7.6 - (0.6 if rv_dil_apex else 0), rx, rz, FLU, a=0.0, rot=0.25)
    sc.line([(2.2, 10.3), (1.4, 10.0)], 0.1, 0.9); sc.line([(2.9, 10.1), (3.4, 9.8)], 0.1, 0.9); sc.line([(-1.0, 10.2), (-1.8, 10.4)], 0.1, 0.9)
    sc.ell(2.0, 12.4, 1.7 * la, 1.5 * la, 0.42, a=0.12); sc.ell(2.0, 12.4, 1.4 * la, 1.25 * la, FLU, a=0.0)
    sc.ell(-1.7, 12.3, 1.6 * ra, 1.5 * ra, 0.42, a=0.12); sc.ell(-1.7, 12.3, 1.3 * ra, 1.25 * ra, FLU, a=0.0)
    if thrombus: sc.ell(-1.4, 11.9, 0.75, 0.3, 0.6, rot=0.4)
    return sc


def subcostal(depth=18, peff=0.0, rv_collapse=False, rv_ratio=0.7, seed=0, lvw=1.4, echo=False, bubbles=False):
    rng = random.Random(seed); sc = Scene("sector", depth, angle=80); sc.alines = False
    sc.band(0, 1.0, 0.3)
    sc.poly([(-9, 1.0), (9, 1.0), (9, 4.5), (-1, 7.0), (-9, 6.0)], 0.36)  # fígado
    for _ in range(18): sc.ell(rng.uniform(-6, 6), rng.uniform(2, 5.5), rng.uniform(0.2, 0.4), 0.15, 0.44)
    cz = 11.0
    if peff: sc.ell(0.6, cz, 5.4 + peff, 3.6 + peff, FLU, a=0.0, rot=-0.25)
    sc.ring(0.6, cz, 5.5 + peff, 3.7 + peff, 0.22, BRI, rot=-0.25, a=0.8)
    sc.ell(0.6, cz, 5.3, 3.5, 0.36, rot=-0.25)
    # VD anterior (em cima), septo, VE posterior
    rvh = 0.7 + 1.0 * rv_ratio
    sc.ell(-0.3, cz - 2.0, 4.0, rvh + 0.35, 0.42, a=0.12, rot=-0.25)
    if rv_collapse: sc.poly([(-3.8, cz - 1.0), (-1.5, cz - 1.6), (0.2, cz - 2.3 + rvh * 0.9), (2.6, cz - 3.0), (3.4, cz - 2.8), (1.0, cz - 1.7), (-3.4, cz - 0.6)], FLU, a=0.0)
    else: sc.ell(-0.3, cz - 2.0, 3.6, rvh, FLU, a=0.0, rot=-0.25)
    sc.ell(1.6, cz + 0.9, 3.4, lvw + 0.6, 0.42, a=0.12, rot=-0.25); sc.ell(1.6, cz + 0.9, 3.0, lvw, FLU, a=0.0, rot=-0.25)
    sc.ell(-3.6, cz + 1.2, 1.4, 1.2, FLU, a=0.0)
    if echo and peff: sc.dots(90, (-4, 5), (cz - 4.2 - peff, cz - 3.6), 0.12, 0.42, rng); sc.ell(3.0, cz - 3.4 - peff * 0.6, 1.2, peff * 0.35, 0.38)
    if bubbles: sc.dots(70, (-4.6, -2.6), (cz + 0.4, cz + 2.1), 0.06, BRI, rng); sc.dots(40, (-3.0, 2.0), (cz - 2.6, cz - 1.4), 0.06, BRI, rng)
    return sc


def ivc_long(diam=1.8, depth=14, hv=True, seed=0, plet=False):
    rng = random.Random(seed); sc = Scene("convex", depth, angle=60); sc.alines = False
    wall(sc, rng, 0, 1.5)
    sc.poly([(-8, 1.5), (8, 1.5), (8, 9), (-8, 8)], 0.36)
    for _ in range(25): sc.ell(rng.uniform(-6, 6), rng.uniform(2, 8.5), rng.uniform(0.2, 0.4), 0.15, 0.44)
    zc = 6.2
    sc.poly([(-7, zc - diam / 2), (1.0, zc - diam / 2 - 0.1), (2.4, zc - diam / 2 - 0.9), (3.0, zc - 2.2), (3.8, zc - 2.0), (3.2, zc + diam / 2 - 0.9), (1.6, zc + diam / 2 - 0.2), (-7, zc + diam / 2)], FLU, a=0.0)
    sc.line([(-7, zc - diam / 2), (1.0, zc - diam / 2 - 0.1), (2.4, zc - diam / 2 - 0.9)], 0.1, 0.75); sc.line([(-7, zc + diam / 2), (1.6, zc + diam / 2 - 0.2), (3.2, zc + diam / 2 - 0.9)], 0.1, 0.75)
    if hv: sc.poly([(-1.2, zc - diam / 2), (-0.2, 2.6), (0.5, 2.8), (-0.2, zc - diam / 2)], FLU, a=0.0)
    sc.ell(3.4, zc - 2.5, 1.3, 1.1, FLU, a=0.0); sc.label(3.4, zc - 2.5, "AD")
    sc.mark("cal", (-2.5, zc - diam / 2), (-2.5, zc + diam / 2), f"{diam:.1f} cm".replace(".", ","))
    return sc


# ------------------------------------------------------------------------------------------------ ABDOME / eFAST
def ruq(fluid=0.0, depth=16, seed=0, pleural=0.0, kidney=True, hydro=0, side="dir"):
    """Hepatorrenal (Morison), coronal, cefálico à esquerda."""
    rng = random.Random(seed); sc = Scene("convex", depth, angle=70); sc.alines = False
    wall(sc, rng, 0, 1.5)
    sc.poly([(sc.x0, 1.5), (sc.x1, 1.5), (sc.x1, 6.5), (2.0, 9.0), (-3, 9.8), (sc.x0, 9)], 0.36)
    for _ in range(30): sc.ell(rng.uniform(-8, 8), rng.uniform(2.5, 8.5), rng.uniform(0.2, 0.45), 0.15, 0.45)
    dia = [(-1.4, 1.5), (-3.0, 3.5), (-4.6, 6.0), (-6.3, 8.8), (sc.x0, 9.6)]
    lp = [(sc.x0, 1.5)] + dia
    if pleural:
        sc.poly(lp, FLU + (0.06 if pleural > 0.5 else 0), a=0.0)
        if pleural > 0.5: sc.dots(120, (-9, -2), (2, 9), 0.05, 0.4, rng)
        sc.line([(-4.0, 9.2), (-9, 10.2)], 0.3, BRI, a=12); sc.label(-6.5, 8.4, "coluna")
    else: sc.poly(lp, 0.0, a=9.0); sc.dAir.polygon([sc.p(x, z) for x, z in lp], fill=1.0)
    sc.line(dia, 0.2, BRI)  # diafragma
    if fluid: sc.poly([(-6, 9.0 - 0.1), (-1, 9.85), (3.5, 8.6), (3.5, 8.6 + fluid), (-1, 9.85 + fluid * 1.3), (-6, 9.0 + fluid)], FLU, a=0.0)
    if kidney:
        kz = 11.2 + fluid * 1.1
        sc.ell(0.0, kz, 4.6, 2.0, 0.28, a=0.12, rot=-0.18); sc.ring(0.0, kz, 4.6, 2.0, 0.12, 0.75, rot=-0.18)
        sc.ell(0.0, kz, 2.6, 0.9, 0.6, rot=-0.18)
        if hydro:
            for j in range(3 + hydro): sc.ell(-1.8 + j * 1.1, kz + (0.1 if j % 2 else -0.15), 0.5 + 0.25 * hydro, 0.35 + 0.15 * hydro, FLU, a=0.0)
            sc.ell(0.4, kz + 0.2, 0.9 + 0.4 * hydro, 0.6 + 0.2 * hydro, FLU, a=0.0)
    sc.label(2.0, 5.0, "fígado" if side == "dir" else "baço"); sc.label(2.0, 11.2 + fluid * 1.1, "rim")
    return sc


def pelvis(fluid=0.0, depth=16, seed=0, vol=1.0):
    rng = random.Random(seed); sc = Scene("convex", depth, angle=70); sc.alines = False
    wall(sc, rng, 0, 1.8)
    sc.band(1.8, depth + 1, 0.3)
    w, h = 4.0 * vol, 3.0 * vol
    sc.ell(0, 2.2 + h, w, h, FLU, a=0.0); sc.ring(0, 2.2 + h, w, h, 0.15, 0.7)
    if fluid: sc.poly([(-3.0, 2.2 + 2 * h + 0.1), (3.0, 2.2 + 2 * h + 0.1), (4.5, 2.2 + 2 * h + fluid), (0, 2.2 + 2 * h + fluid * 1.6), (-4.5, 2.2 + 2 * h + fluid)], FLU, a=0.0)
    for _ in range(12): sc.ell(rng.uniform(-6, 6), rng.uniform(2.5 + 2 * h + fluid * 1.6, depth), rng.uniform(0.4, 1.0), 0.3, 0.4)
    sc.label(0, 2.2 + 0.55 * h, "bexiga")
    if vol: sc.mark("cal", (-w * 0.94, 2.2 + 1.35 * h), (w * 0.94, 2.2 + 1.35 * h), f"{2 * w:.1f} cm".replace(".", ","))
    return sc


# ------------------------------------------------------------------------------------------------ VASOS
def vessels(compress=False, dvt=False, depth=4.5, seed=0, art_r=0.42, vein_r=0.6, color=None, needle=False, needle_art=False):
    """Femoral comum transversal (linear): artéria (lateral, redonda) e veia (medial, oval)."""
    rng = random.Random(seed); sc = Scene("linear", depth, width=4.5); sc.alines = False; sc.blur = 1.6
    sc.band(0, 0.25, 0.4); sc.band(0.25, 1.0, 0.16); sc.band(1.0, depth + 1, 0.3)
    for _ in range(14): sc.line([(rng.uniform(-2.5, 2.5), rng.uniform(1.1, 4)), (rng.uniform(-2.5, 2.5), rng.uniform(1.1, 4))], 0.03, 0.42)
    ax, az = 0.9, 1.9; vx, vz = -0.6, 2.0
    sc.ell(ax, az, art_r + 0.06, art_r + 0.06, 0.75); sc.ell(ax, az, art_r, art_r, FLU, a=0.0)
    vr_x, vr_z = vein_r * 1.15, vein_r * (0.12 if compress and not dvt else 0.95)
    if compress: az2 = vz + 0.25
    else: az2 = vz
    sc.ell(vx, az2, vr_x + 0.07, vr_z + 0.07, 0.7); sc.ell(vx, az2, vr_x, max(vr_z, 0.03), FLU if not dvt else 0.09, a=0.0)
    if dvt: sc.dots(22, (vx - vr_x * 0.7, vx + vr_x * 0.7), (az2 - vr_z * 0.6, az2 + vr_z * 0.6), 0.05, 0.22, rng)
    if color: sc.color.append((ax, az, art_r * 0.9, art_r * 0.9, "red"))
    if color == "both": sc.color.append((vx, az2, vr_x * 0.9, vr_z * 0.9, "blue"))
    if needle: sc.line([(-2.3, 0.2), (vx - 0.05, az2 - 0.1)], 0.05, BRI); sc.line([(vx - 0.05, az2 - 0.1), (vx + 0.2, az2)], 0.05, BRI)
    if needle_art: sc.line([(-2.3, 0.2), (ax - 0.1, az - 0.05)], 0.05, BRI)
    sc.label(ax, az - art_r - 0.35, "A"); sc.label(vx, az2 - max(vr_z, 0.2) - 0.35, "V")
    return sc


def aorta(diam=2.0, depth=16, seed=0, thrombus=0.0, flap=False):
    rng = random.Random(seed); sc = Scene("convex", depth, angle=70); sc.alines = False
    wall(sc, rng, 0, 2.0); sc.band(2.0, depth + 1, 0.3)
    for _ in range(10): sc.ell(rng.uniform(-6, 6), rng.uniform(3, 6), rng.uniform(0.5, 1.2), rng.uniform(0.3, 0.6), 0.45)
    zc = 9.0 - diam * 0.2
    sc.ell(-0.4, zc + diam / 2 + 1.6, 2.6, 0.9, BRI, a=10)  # vértebra
    sc.ell(-0.2, zc, diam / 2 + 0.1, diam / 2 + 0.1, 0.7); sc.ell(-0.2, zc, diam / 2, diam / 2, FLU, a=0.0)
    if thrombus: sc.poly([(-0.2 + diam / 2 * math.cos(a_), zc + diam / 2 * math.sin(a_)) for a_ in [x / 20 * math.pi for x in range(-2, 23)]] + [(-0.2 + (diam / 2 - thrombus) * math.cos(a_), zc + (diam / 2 - thrombus) * math.sin(a_)) for a_ in [x / 20 * math.pi for x in range(22, -3, -1)]], 0.3)
    if flap:
        r_ = diam / 2; a1, a2 = math.radians(205), math.radians(-15)
        sc.line([(-0.2 + r_ * math.cos(a1), zc + r_ * math.sin(a1)), (-0.1, zc - 0.12), (-0.2 + r_ * math.cos(a2), zc + r_ * math.sin(a2))], 0.1, BRI, a=0.4)
    sc.ell(2.6, zc + 0.3, 0.8, 0.55, FLU, a=0.0)  # VCI
    sc.mark("cal", (-0.2, zc - diam / 2 - 0.1), (-0.2, zc + diam / 2 + 0.1), f"{diam:.1f} cm".replace(".", ","))
    return sc


# ------------------------------------------------------------------------------------------------ OLHO / DIAFRAGMA / ESTÔMAGO / VIA AÉREA
def onsd(d=5.0, depth=5.0, seed=0, papil=False):
    rng = random.Random(seed); sc = Scene("linear", depth, width=4.0); sc.alines = False; sc.blur = 1.8
    sc.band(0, 0.25, 0.35); sc.band(0.25, depth + 1, 0.3)
    sc.ell(0, 1.4, 1.2, 1.2, FLU, a=0.0); sc.ring(0, 1.4, 1.2, 1.2, 0.08, 0.6)
    sc.ell(0, 0.55, 0.55, 0.22, 0.45); sc.line([(-0.8, 0.45), (0.8, 0.45)], 0.04, 0.7)
    if papil: sc.ell(0, 2.55, 0.35, 0.12, 0.6)
    w = d / 10 / 2; sc.poly([(-w, 2.6), (w, 2.6), (w * 1.05, depth + 1), (-w * 1.05, depth + 1)], 0.08, a=0.05)
    sc.mark("cal", (-w, 2.9), (w, 2.9), f"DBNO {d:.1f} mm".replace(".", ","))
    return sc


def diaphragm_zoa(te=0.18, depth=3.5, seed=0):
    rng = random.Random(seed); sc = Scene("linear", depth, width=4.0); sc.alines = False; sc.blur = 1.4
    sc.band(0, 0.25, 0.4); sc.band(0.25, 0.7, 0.16); sc.band(0.7, 1.2, 0.22)
    z0 = 1.35; sc.ell(-1.9, z0 - 0.3, 0.7, 0.35, BRI, a=12); sc.ell(1.9, z0 - 0.3, 0.7, 0.35, BRI, a=12)
    sc.line([(sc.x0, z0), (sc.x1, z0)], 0.06, BRI); sc.band(z0 + 0.03, z0 + te - 0.03, 0.06)
    sc.line([(sc.x0, z0 + te), (sc.x1, z0 + te)], 0.06, BRI); sc.band(z0 + te + 0.03, depth + 1, 0.34)
    sc.mark("cal", (0.3, z0), (0.3, z0 + te), f"{te * 10:.1f} mm".replace(".", ","))
    return sc


def gastric(cont="vazio", area=4.0, depth=14, seed=0, tube=False):
    rng = random.Random(seed); sc = Scene("convex", depth, angle=70); sc.alines = False
    wall(sc, rng, 0, 1.5); sc.poly([(sc.x0, 1.5), (sc.x1, 1.5), (sc.x1, 4.5), (sc.x0, 5.5)], 0.36)
    r = math.sqrt(area / math.pi); cz = 6.0 + r
    ry = r * 0.85 if cont != "vazio" else r * 0.6
    sc.ell(0, cz, r + 0.62, ry + 0.62, 0.85)   # serosa
    sc.ell(0, cz, r + 0.52, ry + 0.52, 0.06)   # muscular própria (hipoecoica)
    sc.ell(0, cz, r + 0.2, ry + 0.2, 0.75)     # submucosa
    sc.ell(0, cz, r + 0.06, ry + 0.06, 0.15)   # mucosa
    if cont == "vazio": sc.ell(0, cz, r, ry, 0.15); sc.ell(0, cz, r * 0.35, ry * 0.3, 0.6)
    elif cont == "liquido": sc.ell(0, cz, r, ry, FLU, a=0.0)
    else:
        sc.ell(0, cz, r, ry, 0.5); sc.dots(40, (-r * 0.8, r * 0.8), (cz - ry * 0.75, cz - ry * 0.4), 0.1, 0.9, rng)
        band = [(-r * 0.85, cz - ry * 0.55), (r * 0.85, cz - ry * 0.55), (r * 0.8, cz - ry * 0.35), (-r * 0.8, cz - ry * 0.35)]
        sc.poly(band, 0.7, a=3.5)
    if tube: sc.ring(0.2, cz + 0.1, 0.35, 0.3, 0.07, BRI, a=4.0)
    sc.ell(3.5, cz + r + 2.5, 1.1, 1.1, FLU, a=0.0); sc.label(3.5, cz + r + 2.5, "Ao")
    sc.label(0, cz - r - 1.0, "antro")
    return sc


def trachea(esoph=False, depth=4.0, seed=0):
    rng = random.Random(seed); sc = Scene("linear", depth, width=4.5); sc.alines = True; sc.blur = 1.5
    sc.band(0, 0.25, 0.35); sc.band(0.25, depth + 1, 0.28)
    sc.ell(-1.8, 1.1, 0.7, 0.55, 0.36); sc.ell(1.8, 1.1, 0.7, 0.55, 0.36)  # tireoide
    sc.ring(0, 1.9, 1.15, 1.0, 0.18, 0.6)
    arc = [(1.1 * math.cos(a), 1.9 - 1.0 * math.sin(a)) for a in [math.pi * x / 20 for x in range(2, 19)]]
    sc.line(arc, 0.07, BRI); sc.air_below(arc[::-1][::-1])
    if esoph:
        ex, ez = 1.45, 2.4
        sc.ell(ex, ez, 0.55, 0.45, 0.25); sc.line([(ex - 0.45, ez - 0.05), (ex + 0.45, ez - 0.1)], 0.06, BRI)
        sc.dAir.polygon([sc.p(x, z) for x, z in [(ex - 0.42, ez), (ex + 0.42, ez - 0.05), (ex + 0.42, depth + 1), (ex - 0.42, depth + 1)]], fill=1.0)
        sc.poly([(ex - 0.42, ez + 0.02), (ex + 0.42, ez - 0.03), (ex + 0.42, depth + 1), (ex - 0.42, depth + 1)], 0.0, a=9.0)
    sc.label(0, 0.55, "traqueia")
    return sc


def bladder(w=8.0, h=6.0, d=7.0, depth=14, seed=0, catheter=False, clots=False):
    rng = random.Random(seed); sc = Scene("convex", depth, angle=70); sc.alines = False
    wall(sc, rng, 0, 1.6); sc.band(1.6, depth + 1, 0.3)
    sc.ell(0, 2.0 + h / 2, w / 2, h / 2, FLU, a=0.0); sc.ring(0, 2.0 + h / 2, w / 2, h / 2, 0.12, 0.7)
    if catheter: sc.ell(0, 2.0 + h - 0.8, 0.5, 0.4, BRI, a=6)
    if clots: sc.ell(-0.8, 2.0 + h - 1.0, 1.4, 0.8, 0.45, rot=0.2); sc.ell(1.4, 2.0 + h - 0.6, 0.8, 0.45, 0.4)
    yy = 2.0 + 0.78 * h; xx = w / 2 * math.sqrt(1 - ((yy - 2.0 - h / 2) / (h / 2)) ** 2)
    sc.mark("cal", (-xx, yy), (xx, yy), f"{w:.1f} cm".replace(".", ","))
    sc.mark("cal", (0, 2.0), (0, 2.0 + h), f"{h:.1f} cm".replace(".", ","))
    return sc
