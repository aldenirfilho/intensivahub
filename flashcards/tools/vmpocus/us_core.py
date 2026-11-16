"""Núcleo do gerador sintético de ultrassom (POCUS) — CÓDICE 360X.

B-mode: cena física (cm) desenhada em mapas de ecogenicidade (E) e atenuação (A) → amostragem por feixes (linear, convexo,
setorial) → sombra acústica (transmissão acumulada), reverberações (linhas A), linhas B, speckle correlacionado,
compressão logarítmica → conversão de varredura → moldura de aparelho (régua de profundidade, marcador, calipers, rótulos).
"""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from scipy.ndimage import gaussian_filter, map_coordinates

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"; FONTB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
PX = 40  # px/cm nos mapas de cena
def fnt(s, b=False): return ImageFont.truetype(FONTB if b else FONT, s)


class Scene:
    def __init__(s, probe="convex", depth=14.0, width=4.0, angle=70.0, base=0.32, att=0.10):
        s.probe, s.depth, s.width, s.angle = probe, depth, width, angle
        s.R0 = {"linear": 0.0, "convex": 4.5, "sector": 0.15}[probe]
        half = width / 2 if probe == "linear" else math.sin(math.radians(angle / 2)) * (s.R0 + depth)
        s.x0, s.x1, s.z0, s.z1 = -half - 0.5, half + 0.5, -1.6, depth + 0.6
        W = int((s.x1 - s.x0) * PX); H = int((s.z1 - s.z0) * PX)
        s.E = Image.new("F", (W, H), base); s.A = Image.new("F", (W, H), att)
        s.dE, s.dA = ImageDraw.Draw(s.E), ImageDraw.Draw(s.A)
        s.blines = []; s.air = Image.new("F", (W, H), 0.0); s.dAir = ImageDraw.Draw(s.air)
        s.haze = 0.055; s.alines = True; s.marks = []; s.labels = []; s.color = []; s.alevel = 0.6; s.blur = 2.6
    def p(s, x, z): return ((x - s.x0) * PX, (z - s.z0) * PX)
    # primitivas ---------------------------------------------------------------------------------------------
    def ell(s, cx, cz, rx, rz, e, a=None, rot=0.0):
        pts = [s.p(cx + rx * math.cos(t) * math.cos(rot) - rz * math.sin(t) * math.sin(rot), cz + rx * math.cos(t) * math.sin(rot) + rz * math.sin(t) * math.cos(rot)) for t in np.linspace(0, 2 * math.pi, 90)]
        s.dE.polygon(pts, fill=e)
        if a is not None: s.dA.polygon(pts, fill=a)
    def poly(s, pts, e, a=None):
        q = [s.p(x, z) for x, z in pts]; s.dE.polygon(q, fill=e)
        if a is not None: s.dA.polygon(q, fill=a)
    def line(s, pts, w, e, a=None):
        q = [s.p(x, z) for x, z in pts]; s.dE.line(q, fill=e, width=max(1, int(w * PX)), joint="curve")
        if a is not None: s.dA.line(q, fill=a, width=max(1, int(w * PX)), joint="curve")
    def ring(s, cx, cz, rx, rz, th, e, rot=0.0, a=None):
        pts = [(cx + rx * math.cos(t) * math.cos(rot) - rz * math.sin(t) * math.sin(rot), cz + rx * math.cos(t) * math.sin(rot) + rz * math.sin(t) * math.cos(rot)) for t in np.linspace(0, 2 * math.pi, 120)]
        s.line(pts, th, e, a)
    def band(s, z0, z1, e, a=None): s.poly([(s.x0, z0), (s.x1, z0), (s.x1, z1), (s.x0, z1)], e, a)
    def dots(s, n, xr, zr, r, e, rng, a=None):
        for _ in range(n):
            x, z = rng.uniform(*xr), rng.uniform(*zr); s.ell(x, z, r * rng.uniform(0.6, 1.4), r * rng.uniform(0.5, 1.0), e, a)
    def air_below(s, pts):  # superfície de ar (pleura/alça): abaixo dela, sombra suja + reverberação
        q = [s.p(x, z) for x, z in pts] + [s.p(pts[-1][0], s.z1 + 1), s.p(pts[0][0], s.z1 + 1)]
        s.dA.polygon(q, fill=9.0); s.dE.polygon(q, fill=0.0); s.dAir.polygon(q, fill=1.0)
    def mark(s, kind, *a): s.marks.append((kind,) + a)
    def label(s, x, z, txt): s.labels.append((x, z, txt))


def _beams(sc, nb=300, ns=560):
    if sc.probe == "linear":
        xb = np.linspace(-sc.width / 2, sc.width / 2, nb); r = np.linspace(0, sc.depth, ns)
        X = np.tile(xb, (ns, 1)); Z = np.tile(r[:, None], (1, nb))
    else:
        th = np.radians(np.linspace(-sc.angle / 2, sc.angle / 2, nb)); r = np.linspace(0, sc.depth, ns)
        X = np.sin(th)[None, :] * (sc.R0 + r[:, None]); Z = np.cos(th)[None, :] * (sc.R0 + r[:, None]) - sc.R0
    return X, Z, r


def _sample(img, sc, X, Z):
    a = np.asarray(img, dtype=np.float32)
    return map_coordinates(a, [(Z - sc.z0) * PX, (X - sc.x0) * PX], order=1, mode="nearest")


def bmode(sc, seed=0, nb=300, ns=560, gain=1.0, speck=(1.1, 1.6), dr=34.0):
    rng = np.random.default_rng(seed)
    X, Z, r = _beams(sc, nb, ns); dr_cm = r[1] - r[0]
    Eb = gaussian_filter(np.asarray(sc.E, dtype=np.float32), sc.blur)
    E = map_coordinates(Eb, [(Z - sc.z0) * PX, (X - sc.x0) * PX], order=1, mode="nearest"); A = _sample(sc.A, sc, X, Z); AIR = _sample(sc.air, sc, X, Z)
    T = np.exp(-np.cumsum(A, axis=0) * dr_cm); T = np.vstack([np.ones((1, nb)), T[:-1]])
    I = E * T
    # reverberação: linhas A a múltiplos da profundidade da superfície de ar + névoa sob o ar
    hz = np.zeros_like(I)
    for b in range(nb):
        idx = np.nonzero(AIR[:, b] > 0.5)[0]
        if not len(idx): continue
        k0 = idx[0]; tk = T[max(k0 - 1, 0), b]; I[k0:k0 + 3, b] = np.maximum(I[k0:k0 + 3, b], 0.95 * tk)
        hz[k0 + 3:, b] = sc.haze * tk * np.exp(-(np.arange(ns - k0 - 3)) / (ns * 0.7))
        if sc.alines:
            rp = r[k0] + sc.R0 * 0  # profundidade da pleura ao longo do feixe
            for kk in range(2, 9):
                d = rp * kk
                if d >= sc.depth: break
                j = int(d / dr_cm); amp = sc.alevel * tk * (0.72 ** (kk - 2))
                lo, hi = max(0, j - 3), min(ns, j + 4)
                I[lo:hi, b] += amp * np.exp(-((np.arange(lo, hi) - j) / 1.6) ** 2)
    I += hz
    # linhas B (seguem o feixe a partir da pleura, sem esmaecer)
    for (xb, w, amp) in sc.blines:
        if sc.probe == "linear": bc = (xb + sc.width / 2) / sc.width * (nb - 1)
        else: bc = (math.degrees(math.atan2(xb, 1.2 + sc.R0)) + sc.angle / 2) / sc.angle * (nb - 1)
        wb = max(1.5, w / (sc.width if sc.probe == "linear" else (sc.R0 + 3) * math.radians(sc.angle)) * nb)
        for b in range(max(0, int(bc - 3 * wb)), min(nb, int(bc + 3 * wb) + 1)):
            g = math.exp(-((b - bc) / wb) ** 2)
            idx = np.nonzero(AIR[:, b] > 0.5)[0]
            if not len(idx): continue
            k0 = idx[0]; prof = amp * g * T[max(k0 - 1, 0), b] * (0.85 + 0.15 * np.exp(-np.arange(ns - k0) / ns))
            I[k0:, b] = I[k0:, b] * (1 - 0.8 * g) + prof
    # speckle
    n = rng.standard_normal((ns, nb)) + 1j * rng.standard_normal((ns, nb))
    n = gaussian_filter(n.real, speck) + 1j * gaussian_filter(n.imag, speck); sp = np.abs(n); sp /= sp.mean()
    I = I * sp * gain * np.exp(-0.015 * r)[:, None]
    D = np.clip((20 * np.log10(I + 1e-4) + dr) / dr, 0, 1) ** 1.25
    return D, X, Z


def scan_convert(sc, D, W, H, nb=300, ns=560):
    """Devolve imagem (H×W) 0..1 + função de mapeamento físico→pixel."""
    if sc.probe == "linear": xr = sc.width / 2; zr0, zr1 = 0.0, sc.depth
    else:
        xr = math.sin(math.radians(sc.angle / 2)) * (sc.R0 + sc.depth); zr0 = (math.cos(math.radians(sc.angle / 2)) * sc.R0 - sc.R0); zr1 = sc.depth
    scale = min(W / (2 * xr), H / (zr1 - zr0)); offx = W / 2; offz = (H - (zr1 - zr0) * scale) / 2 - zr0 * scale
    yy, xx = np.mgrid[0:H, 0:W]; x = (xx - offx) / scale; z = (yy - offz) / scale
    if sc.probe == "linear":
        b = (x + sc.width / 2) / sc.width * (nb - 1); s = z / sc.depth * (ns - 1)
    else:
        rr = np.hypot(x, z + sc.R0) - sc.R0; th = np.degrees(np.arctan2(x, z + sc.R0))
        b = (th + sc.angle / 2) / sc.angle * (nb - 1); s = rr / sc.depth * (ns - 1)
    ok = (b >= 0) & (b <= nb - 1) & (s >= 0) & (s <= ns - 1)
    img = map_coordinates(D, [np.clip(s, 0, ns - 1), np.clip(b, 0, nb - 1)], order=1) * ok
    to_px = lambda X, Z: (offx + X * scale, offz + Z * scale)
    return img, to_px, scale, ok


def frame(W=1200, H=900, title="", sub="", k=2):
    im = Image.new("RGB", (W * k, H * k), (0, 0, 0)); d = ImageDraw.Draw(im)
    d.text((22 * k, 18 * k), title, fill=(235, 235, 235), font=fnt(22 * k, True))
    if sub: d.text((22 * k, 50 * k), sub, fill=(170, 175, 180), font=fnt(15 * k))
    d.text((W * k - 22 * k, 22 * k), "imagem sintética didática · CÓDICE 360X", fill=(140, 145, 150), font=fnt(14 * k), anchor="ra")
    return im, d


def paste_bmode(im, d, sc, D, box, k=2, seed=0, ruler=True, label=None):
    x0, y0, x1, y1 = [v * k for v in box]
    img, to_px, scale, ok = scan_convert(sc, D, x1 - x0, y1 - y0)
    g = (img * 255).astype(np.uint8); rgb = np.stack([g, g, (g * 0.98).astype(np.uint8)], -1)
    # Doppler colorido
    if sc.color:
        yy, xx = np.mgrid[0:y1 - y0, 0:x1 - x0]
        for (cx, cz, rx, rz, kind) in sc.color:
            px, pz = to_px(cx, cz); m = (((xx - px) / (rx * scale)) ** 2 + ((yy - pz) / (rz * scale)) ** 2 <= 1) & ok
            rnd = np.random.default_rng(seed).random(m.shape)
            if kind == "red": col = np.stack([180 + 60 * rnd, 30 * rnd, 20 * rnd], -1)
            elif kind == "blue": col = np.stack([20 * rnd, 60 + 60 * rnd, 190 + 50 * rnd], -1)
            else: col = np.stack([200 * rnd, 160 * (1 - rnd), 220 * rnd], -1)
            rgb[m] = col[m].astype(np.uint8)
    im.paste(Image.fromarray(rgb), (x0, y0))
    tp = lambda X, Z: (x0 + to_px(X, Z)[0], y0 + to_px(X, Z)[1])
    # marcador de orientação
    if sc.probe == "linear": mx, mz = -sc.width / 2, 0
    else: a = math.radians(sc.angle / 2); mx, mz = -math.sin(a) * sc.R0, math.cos(a) * sc.R0 - sc.R0
    px, pz = tp(mx, mz); d.ellipse([px - 7 * k, pz - 20 * k, px + 7 * k, pz - 6 * k], fill=(90, 200, 255))
    # régua de profundidade
    if ruler:
        rx = x1 + 10 * k
        for cm in range(0, int(sc.depth) + 1):
            _, pzz = tp(0, cm); big = cm % 5 == 0
            d.line([rx, pzz, rx + (14 if big else 8) * k, pzz], fill=(200, 200, 200), width=k)
            if big or sc.depth <= 6: d.text((rx + 18 * k, pzz), f"{cm}", fill=(200, 200, 200), font=fnt(12 * k), anchor="lm")
        d.text((rx, y1 - 4 * k), "cm", fill=(160, 160, 160), font=fnt(12 * k), anchor="ls")
    for (kind, *a) in sc.marks:
        if kind == "cal":
            (ax, az), (bx, bz), txt = a[0], a[1], a[2]; pa, pb = tp(ax, az), tp(bx, bz)
            n = 18
            for i in range(n):
                if i % 2: continue
                q0 = (pa[0] + (pb[0] - pa[0]) * i / n, pa[1] + (pb[1] - pa[1]) * i / n); q1 = (pa[0] + (pb[0] - pa[0]) * (i + 1) / n, pa[1] + (pb[1] - pa[1]) * (i + 1) / n)
                d.line([q0, q1], fill=(255, 230, 90), width=2 * k)
            for q in (pa, pb): d.line([q[0] - 8 * k, q[1], q[0] + 8 * k, q[1]], fill=(255, 230, 90), width=2 * k); d.line([q[0], q[1] - 8 * k, q[0], q[1] + 8 * k], fill=(255, 230, 90), width=2 * k)
            if abs(pb[0] - pa[0]) > abs(pb[1] - pa[1]):
                d.text(((pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2 - 12 * k), txt, fill=(255, 230, 90), font=fnt(16 * k, True), anchor="ms")
            else:
                d.text(((pa[0] + pb[0]) / 2 + 14 * k, (pa[1] + pb[1]) / 2), txt, fill=(255, 230, 90), font=fnt(16 * k, True), anchor="lm")
        elif kind == "gate":
            px, pz = tp(a[0], a[1]); d.line([px - 10 * k, pz, px + 10 * k, pz], fill=(120, 255, 140), width=2 * k); d.line([px - 10 * k, pz + 12 * k, px + 10 * k, pz + 12 * k], fill=(120, 255, 140), width=2 * k)
        elif kind == "mline":
            pa, pb = tp(a[0], 0), tp(a[0], sc.depth); d.line([pa, pb], fill=(120, 255, 140), width=k)
    for (x, z, txt) in sc.labels:
        px, pz = tp(x, z); d.text((px, pz), txt, fill=(240, 240, 120), font=fnt(17 * k, True), anchor="mm")
    if label: d.text(((x0 + x1) / 2, y0 - 10 * k), label, fill=(220, 220, 220), font=fnt(16 * k, True), anchor="ms")
    return tp


def save(im, path, k=2):
    im = im.resize((im.width // k, im.height // k), Image.LANCZOS)
    im.convert("RGB").quantize(colors=128, method=Image.Quantize.FASTOCTREE).save(path, optimize=True)
