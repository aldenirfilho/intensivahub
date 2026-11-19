"""🩻 Imagens sintéticas didáticas: radiografia de tórax, TC de crânio, microscopia (esfregaço, Gram, sedimento, cristais, FAN),
cintilografia de tireoide e mapa corporal (queimaduras/distribuição de lesões). Questões ilustradas 4.24.0."""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from figs_core import fnt, save_pil, TAG

SS = 2


def _blur(a, r): return np.asarray(Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r)), float) / 255


def _mask(W, H, draw_fn, blur=0):
    im = Image.new("L", (W, H), 0); d = ImageDraw.Draw(im); draw_fn(d)
    if blur: im = im.filter(ImageFilter.GaussianBlur(blur))
    return np.asarray(im, float) / 255


def _frame(img_arr, path, title, sub="", dark=True, label=None):
    """Coloca a imagem (array 0–1 ou PIL RGB) num quadro com título e selo."""
    im = img_arr if isinstance(img_arr, Image.Image) else Image.fromarray((np.clip(img_arr, 0, 1) * 255).astype(np.uint8)).convert("RGB")
    W = im.width + 40; top = 58 + (32 if sub else 0); H = im.height + top + 20
    out = Image.new("RGB", (W, H), "#0b0f14" if dark else "#fbfaf7"); d = ImageDraw.Draw(out)
    d.text((16, 14), title, font=fnt(24, True), fill="#e8c66a" if dark else "#6e1e1e")
    d.text((W - 16 - d.textlength(TAG, font=fnt(17)), 18), TAG, font=fnt(17), fill="#8a93a3")
    if sub: d.text((18, 50), sub, font=fnt(20), fill="#c8ccd4" if dark else "#333")
    out.paste(im, (20, top))
    if label:
        for x, y, txt in label: d.text((20 + x, top + y), txt, font=fnt(26, True), fill="#ffe08a")
    save_pil(out, path, colors=0)


# ============================================================ radiografia de tórax (PA/AP)
def cxr(sp, path, title):
    """sp: mods=[(nome, {...})], ap (bool), sub. mods: pnx{side,size,tension}, effusion{side,level}, consol{side,zone}, ards, edema, cardio{ctr},
    mediast{w}, ett{tip|pos:rmb/eso}, cvc{tip|pos:ij_up/ra}, ngt{pos:est/rbronch/eso}, pneumoperit, collapse{side}, cavity{side}, miliary, hilar, emphysema, kerley, elevated{side}"""
    W = H = 760; rng = np.random.default_rng(sp.get("seed", 7)); M = dict(sp.get("mods", []))
    Y, X = np.mgrid[0:H, 0:W].astype(float)
    emph = "emphysema" in M; diaR, diaL = (560, 578) if not emph else (640, 650)
    if "elevated" in M:
        if M["elevated"].get("side", "d") == "d": diaR -= 85
        else: diaL -= 85
    shift = 0
    if "pnx" in M and M["pnx"].get("tension"): shift = 70 if M["pnx"].get("side", "d") == "d" else -70
    if "collapse" in M: shift = -50 if M["collapse"].get("side", "e") == "e" else 50
    dome = lambda x, x0, x1, base, rise: base - rise * np.sin(np.pi * np.clip((x - x0) / (x1 - x0), 0, 1))
    domeR = dome(X, 125, 372, diaR + 15, 72 if not emph else 25); domeL = dome(X, 388, 635, diaL + 15, 72 if not emph else 25)
    mwx = max(0, M.get("mediast", {}).get("w", 62) - 62)
    def lungmask(side):
        if side == "d":
            u = np.clip((Y - 150) / (diaR - 150), 0, 1); xl = 135 + 95 * (1 - u) ** 1.9 + 30 * np.clip((175 - Y) / 30, 0, 1); xm = 352 + min(shift, 0) * .3 - 52 * (1 - np.clip((Y - 150) / 180, 0, 1)) ** 2 - mwx * (1 - np.clip((Y - 160) / 240, 0, 1))
            m = (X > xl) & (X < xm) & (Y < domeR) & (Y > 142)
        else:
            u = np.clip((Y - 150) / (diaL - 150), 0, 1); xl = 625 - 95 * (1 - u) ** 1.9 - 30 * np.clip((175 - Y) / 30, 0, 1); xm = 408 + max(shift, 0) * .3 + 52 * (1 - np.clip((Y - 150) / 180, 0, 1)) ** 2 + mwx * (1 - np.clip((Y - 160) / 240, 0, 1))
            m = (X < xl) & (X > xm) & (Y < domeL) & (Y > 142)
        return _blur(m.astype(float), 5)
    LR, LL = lungmask("d"), lungmask("e")
    if "collapse" in M:
        if M["collapse"].get("side", "e") == "e": LL = LL * 0.15
        else: LR = LR * 0.15
    lung = np.clip(LR + LL, 0, 1)
    body = _mask(W, H, lambda d: d.polygon([(70, 760), (60, 300), (120, 150), (250, 95), (510, 95), (640, 150), (700, 300), (690, 760)], fill=255), 18)
    img = 0.04 + 0.42 * body
    img -= 0.31 * lung * (1.12 if emph else 1)
    tex = _blur(rng.random((H, W)), 3.5) - 0.5; ves = _blur(np.clip(rng.random((H, W)) - 0.985, 0, 1) * 30, 2.5)
    hil = np.exp(-(((X - 320) ** 2 + (Y - 340) ** 2) / 4200.)) + np.exp(-(((X - 440) ** 2 + (Y - 340) ** 2) / 4200.))
    texture = lung * (0.10 * tex + 0.05 * ves + 0.10 * hil * (0.4 if emph else 1))
    abd = ((((X < 380) & (Y > domeR)) | ((X >= 380) & (Y > domeL))) & (Y > 400)).astype(float)
    abd = _blur(abd, 4) * body
    cw = M.get("cardio", {}).get("ctr", 0.46); hw = cw * 500; mw = M.get("mediast", {}).get("w", 62)
    med = _mask(W, H, lambda d: (d.rectangle([380 - mw + shift, 130, 380 + mw + shift, 400], fill=255),
                                  d.ellipse([380 - hw * 0.36 + shift, 360, 380 + hw * 0.64 + shift, diaL + 30], fill=255),
                                  d.ellipse([395 + shift - 35, 235, 465 + shift, 300], fill=255)), 12)
    spine = _mask(W, H, lambda d: d.rectangle([363 + shift * .25, 60, 397 + shift * .25, 760], fill=255), 5)
    trach = _mask(W, H, lambda d: (d.line([(380 + shift * .6, 60), (380 + shift * .6, 300)], fill=255, width=26),
                                    d.line([(380 + shift * .6, 300), (330 + shift * .5, 362)], fill=255, width=18), d.line([(380 + shift * .6, 300), (440 + shift * .5, 366)], fill=255, width=16)), 5)
    gas = _mask(W, H, lambda d: d.ellipse([470, diaL + 5, 575, diaL + 50], fill=255), 6)
    rib = np.zeros((H, W))
    for k in range(10 if not emph else 11):
        y0 = 168 + k * 40
        rib += _mask(W, H, lambda d, y0=y0: (d.arc([80, y0 - 60, 380, y0 + 70], 200, 340, fill=255, width=9), d.arc([380, y0 - 60, 680, y0 + 70], 200, 340, fill=255, width=9)), 2)
    clav = _mask(W, H, lambda d: (d.line([(160, 165), (350, 190)], fill=255, width=16), d.line([(600, 165), (410, 190)], fill=255, width=16)), 3)
    opac = np.zeros((H, W))   # opacidades pulmonares (somam e removem textura)
    if "effusion" in M:
        e = M["effusion"]; side = e.get("side", "d"); lv = e.get("level", 0.35); Lm = LR if side == "d" else LL
        dia = diaR if side == "d" else diaL; top = dia - lv * 400
        ylev = top + (130 * (np.clip(X - 135, 0, None) / 217) ** 0.5 if side == "d" else 130 * (np.clip(625 - X, 0, None) / 217) ** 0.5)
        opac += 0.34 * Lm * _blur((Y > ylev).astype(float), 6)
        abd = abd + 0.0
    if "consol" in M:
        c = M["consol"]; side = c.get("side", "d"); zone = c.get("zone", "inf")
        cy = {"sup": 235, "med": 370, "inf": 470}[zone]; cx = 250 if side == "d" else 510
        m = _mask(W, H, lambda d: d.ellipse([cx - 100, cy - 75, cx + 100, cy + 85], fill=255), 16) * (LR if side == "d" else LL)
        br = _mask(W, H, lambda d: [d.line([(cx + (45 if side == "d" else -45), cy - 45), (cx + i * 24 - 40, cy + 50)], fill=255, width=3) for i in range(4)], 1.2)
        opac += 0.34 * m - 0.08 * br * m
    if "ards" in M or "edema" in M:
        ed = "edema" in M; bat = _blur(rng.random((H, W)), 9); bat = (bat - bat.min()) / (bat.max() - bat.min())
        dist = hil * (1.4 if ed else 0.5) + (0.95 if not ed else 0.35) * bat
        opac += lung * np.clip(0.30 * dist + (0.09 if not ed else 0.04), 0, 0.36)
    if "collapse" in M:
        opac += 0.30 * _blur(lungmask(M["collapse"].get("side", "e")), 2)
    if "cavity" in M:
        cx, cy = (250, 235) if M["cavity"].get("side", "d") == "d" else (510, 235)
        opac += 0.24 * _mask(W, H, lambda d: d.ellipse([cx - 80, cy - 62, cx + 80, cy + 72], fill=255), 14) * lung
        opac -= 0.30 * _mask(W, H, lambda d: d.ellipse([cx - 30, cy - 26, cx + 30, cy + 28], fill=255), 2)
        opac += 0.10 * _mask(W, H, lambda d: d.ellipse([cx - 34, cy - 30, cx + 34, cy + 32], outline=255, width=6), 1.5)
    if "miliary" in M:
        opac += 0.14 * lung * _mask(W, H, lambda d: [d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=255) for x, y in zip(rng.integers(120, 650, 950), rng.integers(160, 600, 950))], 1.1)
    img += texture * (1 - np.clip(opac / 0.3, 0, 1)) + opac
    img += 0.36 * med * (1 - 0.3 * lung) + 0.10 * spine - 0.16 * trach + 0.13 * abd * (1 - lung) - 0.22 * gas * abd + 0.07 * np.clip(rib, 0, 1) + 0.13 * clav
    if "kerley" in M:
        for k in range(8):
            for x0, x1 in ((142, 176), (586, 620)):
                y0 = 455 + k * 9; img += 0.12 * _mask(W, H, lambda d: d.line([(x0, y0), (x1, y0)], fill=255, width=2), 0.8)
    if "hilar" in M:
        img += 0.22 * _mask(W, H, lambda d: [d.ellipse([x - 38, 295 + k * 38, x + 38, 345 + k * 38], fill=255) for x in (318, 444) for k in range(3)], 6)
    if "pnx" in M:
        p = M["pnx"]; side = p.get("side", "d"); sz = p.get("size", 0.35); Lm = LR if side == "d" else LL
        cxl = 352 if side == "d" else 408
        edge = _mask(W, H, (lambda d: d.ellipse([150 + sz * 190, 170 + sz * 140, cxl + 30, (diaR if side == "d" else diaL) - 55 - sz * 60], fill=255)) if side == "d"
                     else (lambda d: d.ellipse([cxl - 30, 170 + sz * 140, 610 - sz * 190, diaL - 55 - sz * 60], fill=255)), 1.5)
        air = np.clip(Lm - edge, 0, 1)
        img -= air * (texture + 0.09)
        img += 0.18 * np.clip(_blur(edge, 1.0) - _blur(edge, 3.0), 0, 1) * 3 * Lm
    if "pneumoperit" in M:
        img -= 0.30 * _mask(W, H, lambda d: d.chord([150, diaR - 70, 360, diaR + 40], 180, 360, fill=255), 2) * (Y > domeR - 2) * (X < 372)
    if "ett" in M:
        e = M["ett"]; tip = e.get("tip", 245); x = 380 + shift * .6
        def tube(d):
            if e.get("pos") == "rmb": d.line([(x, 40), (x, 300), (335, 352)], fill=255, width=10)
            elif e.get("pos") == "eso": d.line([(x + 24, 40), (x + 24, 520)], fill=255, width=10)
            else: d.line([(x, 40), (x, tip)], fill=255, width=10)
        img += 0.5 * _mask(W, H, tube, 1)
    if "cvc" in M:
        c = M["cvc"]; tip = c.get("tip", 330)
        def line(d):
            if c.get("pos") == "ij_up": d.line([(240, 120), (330, 205), (355, 228), (350, 170), (345, 60)], fill=255, width=6)
            elif c.get("pos") == "ra": d.line([(240, 120), (330, 205), (352, 250), (356, 470)], fill=255, width=6)
            else: d.line([(240, 120), (330, 205), (352, 250), (352, tip)], fill=255, width=6)
        img += 0.5 * _mask(W, H, line, 1)
    if "ngt" in M:
        n = M["ngt"]
        def ng(d):
            if n.get("pos") == "rbronch": d.line([(372, 40), (372, 300), (330, 360), (265, 520)], fill=255, width=7)
            elif n.get("pos") == "eso": d.line([(392, 40), (395, 400)], fill=255, width=7)
            else: d.line([(392, 40), (398, diaL - 10), (450, diaL + 25), (520, diaL + 38)], fill=255, width=7)
        img += 0.45 * _mask(W, H, ng, 1)
    img = _blur(np.clip(img + rng.normal(0, 0.012, img.shape), 0, 1), 0.6)
    _frame(img, path, title, sp.get("sub", "Radiografia de tórax " + ("AP no leito" if sp.get("ap") else "PA")), label=[(14, 10, "D")])


# ============================================================ TC de crânio (corte axial)
def ct(sp, path, title):
    """sp: mods=[(nome, {...})]: epidural, subdural, hsa, hip, avc, desvio, hidro, edema, sdc (subdural crônico), hiv; sub"""
    W = H = 640; rng = np.random.default_rng(sp.get("seed", 9)); M = dict(sp.get("mods", [])); c = W / 2
    yy, xx = np.mgrid[0:H, 0:W]
    img = np.zeros((H, W))
    skull = _mask(W, H, lambda d: d.ellipse([90, 50, 550, 600], fill=255), 1.5) - _mask(W, H, lambda d: d.ellipse([110, 70, 530, 580], fill=255), 1.5)
    brain = _mask(W, H, lambda d: d.ellipse([112, 72, 528, 578], fill=255), 1.5)
    img += 0.95 * np.clip(skull, 0, 1)
    sh = M.get("desvio", {}).get("mm", 0) * 4 * (1 if M.get("desvio", {}).get("side", "e") == "e" else -1)
    ed = "edema" in M; hyd = "hidro" in M
    gm = brain * 0.47; wm = _mask(W, H, lambda d: d.ellipse([150, 112, 490, 538], fill=255), 18) * (0.0 if ed else -0.06)
    img += gm + wm * brain
    # sulcos
    if not ed:
        for k in range(26):
            a = rng.uniform(0, 2 * np.pi); r0 = 0.88
            x0 = c + 200 * r0 * math.cos(a); y0 = 325 + 240 * r0 * math.sin(a)
            x1 = c + 175 * math.cos(a + .05); y1 = 325 + 210 * math.sin(a + .05)
            img -= 0.14 * _mask(W, H, lambda d: d.line([(x0, y0), (x1, y1)], fill=255, width=4), 1.2) * brain
    # foice e ventrículos
    img += 0.25 * _mask(W, H, lambda d: d.line([(c + sh * 0.4, 80), (c + sh, 320), (c + sh * 0.4, 570)], fill=255, width=4), 1)
    vs = 1.8 if hyd else (0.55 if ed else 1.0)
    def vent(d):
        for s in (-1, 1):
            comp = 0.6 if (sh and s == (1 if sh < 0 else -1)) else 1.0
            d.ellipse([c + sh + s * 14 - (60 * vs * comp if s < 0 else 0), 230 - 40 * vs, c + sh + s * 14 + (60 * vs * comp if s > 0 else 0), 330 + 30 * vs], fill=255)
            d.ellipse([c + sh + s * 50 - 22 * vs, 360, c + sh + s * 50 + 22 * vs, 440 + 25 * vs], fill=255)
    V = _mask(W, H, vent, 3); img -= 0.30 * V * brain
    img += 0.03 * (_blur(rng.random((H, W)), 1.2) - .5) * brain
    hd = 0.82
    if "epidural" in M:
        side = M["epidural"].get("side", "d"); x0 = 110 if side == "d" else 470
        m = _mask(W, H, lambda d: d.ellipse([x0 - 10, 170, x0 + 70, 420], fill=255), 1.5) * brain
        img = img * (1 - m) + hd * m
    if "subdural" in M or "sdc" in M:
        key = "subdural" if "subdural" in M else "sdc"; side = M[key].get("side", "d")
        th = M[key].get("th", 34); outer = _mask(W, H, lambda d: d.ellipse([112, 72, 528, 578], fill=255), 1)
        inner = _mask(W, H, lambda d: d.ellipse([112 + (th if side == "d" else 0), 72 + th * .5, 528 - (th if side == "e" else 0), 578 - th * .5], fill=255), 1.5)
        half = (xx < c) if side == "d" else (xx > c)
        m = np.clip(outer - inner, 0, 1) * half
        img = img * (1 - m) + (hd if key == "subdural" else 0.24) * m
    if "hsa" in M:
        for k in range(30):
            a = rng.uniform(0, 2 * np.pi)
            x0 = c + 200 * .88 * math.cos(a); y0 = 325 + 240 * .88 * math.sin(a); x1 = c + 175 * math.cos(a + .05); y1 = 325 + 210 * math.sin(a + .05)
            img += 0.38 * _mask(W, H, lambda d: d.line([(x0, y0), (x1, y1)], fill=255, width=4), 1.2) * brain
        img += 0.40 * _mask(W, H, lambda d: (d.line([(c, 80), (c, 215)], fill=255, width=9), d.line([(c, 445), (c, 570)], fill=255, width=7),
                                              d.line([(c - 25, 300), (c - 150, 250)], fill=255, width=8), d.line([(c + 25, 300), (c + 150, 250)], fill=255, width=8)), 1.5) * brain
    if "hip" in M:
        side = M["hip"].get("side", "e"); x = c + (-80 if side == "d" else 80); r = M["hip"].get("r", 45)
        img -= 0.12 * _mask(W, H, lambda d: d.ellipse([x - r - 18, 330 - r - 18, x + r + 18, 330 + r + 18], fill=255), 6)
        m = _mask(W, H, lambda d: d.ellipse([x - r, 330 - r, x + r, 330 + r * .9], fill=255), 2); img = img * (1 - m) + hd * m
    if "avc" in M:
        side = M["avc"].get("side", "e"); s = 1 if side == "e" else -1
        img -= 0.13 * _mask(W, H, lambda d: d.polygon([(c + s * 60, 300), (c + s * 210, 170), (c + s * 215, 470)], fill=255), 10) * brain
    if "hiv" in M:
        img += 0.40 * _mask(W, H, lambda d: [d.rectangle([c + s * 50 - 20, 410, c + s * 50 + 20, 455], fill=255) for s in (-1, 1)], 2) * V
    img = np.clip(img + rng.normal(0, 0.018, img.shape), 0, 1)
    _frame(img, path, title, sp.get("sub", "TC de crânio sem contraste · corte axial · janela de parênquima"), label=[(10, 10, "D")])


# ============================================================ microscopia
def _scope(W=720):
    im = Image.new("RGB", (W * SS, W * SS), (0, 0, 0)); return im, ImageDraw.Draw(im)


def _vignette(im, bg):
    W = im.width; m = Image.new("L", im.size, 0); ImageDraw.Draw(m).ellipse([12, 12, W - 12, W - 12], fill=255)
    out = Image.new("RGB", im.size, (8, 10, 14)); out.paste(im, (0, 0), m.filter(ImageFilter.GaussianBlur(10)))
    return out.resize((W // SS, W // SS), Image.LANCZOS)


def micro(sp, path, title):
    """sp: modo: smear|gram|sed|cryst|ana ; tipo (conforme o modo); sub"""
    mode, tp = sp["modo"], sp["tipo"]; rng = np.random.default_rng(sp.get("seed", 11)); W = 720 * SS
    bgc = {"smear": (238, 222, 226), "gram": (240, 225, 232), "sed": (205, 208, 204), "cryst": (22, 18, 30), "ana": (6, 10, 8)}[mode]
    im = Image.new("RGB", (W, W), bgc); d = ImageDraw.Draw(im)
    R = lambda a, b: rng.uniform(a, b)
    def rbc(x, y, r=34, kind="n"):
        col = (214, 120, 132)
        if kind == "sphero": d.ellipse([x - r * .8, y - r * .8, x + r * .8, y + r * .8], fill=(196, 92, 108)); return
        if kind == "sickle": d.chord([x - r * 1.5, y - r * .7, x + r * 1.5, y + r * .9], 200, 340, fill=col); return
        if kind == "tear": d.polygon([(x - r, y), (x - r * .4, y - r * .9), (x + r * .6, y - r * .6), (x + r * 1.8, y + r * .1), (x + r * .6, y + r * .7), (x - r * .4, y + r * .9)], fill=col); return
        if kind == "schisto":
            a = R(0, 6.28); pts = [(x + r * math.cos(a + t) * (1 if i % 2 else .45), y + r * math.sin(a + t) * (1 if i % 2 else .45)) for i, t in enumerate(np.linspace(0, 3.6, 6))]
            d.polygon(pts, fill=(196, 92, 108)); return
        d.ellipse([x - r, y - r, x + r, y + r], fill=col)
        if kind == "target": d.ellipse([x - r * .62, y - r * .62, x + r * .62, y + r * .62], fill=(240, 205, 210)); d.ellipse([x - r * .28, y - r * .28, x + r * .28, y + r * .28], fill=col)
        elif kind == "acanto":
            for k in range(7): a = k * .9 + R(0, .4); d.ellipse([x + r * math.cos(a) - 6, y + r * math.sin(a) - 6, x + r * math.cos(a) + 6, y + r * math.sin(a) + 6], fill=col)
        else: d.ellipse([x - r * .4, y - r * .4, x + r * .4, y + r * .4], fill=(232, 178, 186))
    def nucleus_lobes(x, y, n, col=(98, 54, 140), r=18):
        for k in range(n): a = k * (6.28 / n) + R(0, .3); d.ellipse([x + 22 * math.cos(a) - r, y + 22 * math.sin(a) - r, x + 22 * math.cos(a) + r, y + 22 * math.sin(a) + r], fill=col)
    if mode == "smear":
        pts = [(R(60, W - 60), R(60, W - 60)) for _ in range(150)]
        if tp == "rouleaux":
            for k in range(14):
                x0, y0, a = R(100, W - 300), R(100, W - 100), R(-.5, .5)
                for j in range(7): rbc(x0 + j * 30 * math.cos(a), y0 + j * 30 * math.sin(a), 34)
        else:
            for i, (x, y) in enumerate(pts):
                kind = "n"
                if tp == "schisto" and i % 4 == 0: kind = "schisto"
                if tp == "sphero" and i % 2 == 0: kind = "sphero"
                if tp == "target" and i % 2 == 0: kind = "target"
                if tp == "sickle" and i % 3 == 0: kind = "sickle"
                if tp == "tear" and i % 3 == 0: kind = "tear"
                if tp == "acanto" and i % 2 == 0: kind = "acanto"
                rbc(x, y, R(30, 36), kind)
            if tp == "malaria":
                for x, y in pts[:30:3]: d.ellipse([x - 11, y - 11, x + 11, y + 11], outline=(90, 40, 140), width=5); d.ellipse([x + 6, y - 14, x + 14, y - 6], fill=(120, 30, 120))
                x, y = W * .5, W * .5; d.chord([x - 70, y - 30, x + 70, y + 40], 190, 350, fill=(150, 90, 170), outline=(90, 40, 140), width=4)
            if tp == "plaquetas_baixas": pass
            else:
                for _ in range(12 if tp != "plaquetas_baixas" else 1): x, y = R(60, W - 60), R(60, W - 60); d.ellipse([x - 6, y - 6, x + 6, y + 6], fill=(150, 90, 170))
        if tp == "blast":
            for _ in range(3):
                x, y = R(150, W - 150), R(150, W - 150); d.ellipse([x - 70, y - 70, x + 70, y + 70], fill=(170, 160, 210)); d.ellipse([x - 58, y - 58, x + 54, y + 56], fill=(110, 70, 165))
                for k in range(2): d.ellipse([x - 20 + k * 22, y - 18, x - 8 + k * 22, y - 6], fill=(150, 120, 200))
                d.line([(x - 30, y + 30), (x + 25, y - 20)], fill=(160, 40, 60), width=6)
        if tp == "hiperseg":
            x, y = W * .5, W * .5; d.ellipse([x - 60, y - 60, x + 60, y + 60], fill=(235, 205, 220)); nucleus_lobes(x, y, 6, r=15)
    elif mode == "gram":
        purple, pink = (78, 40, 120), (205, 80, 120)
        for _ in range(9):
            x, y = R(120, W - 120), R(120, W - 120); d.ellipse([x - 70, y - 70, x + 70, y + 70], fill=(236, 200, 214)); nucleus_lobes(x, y, 3, col=(150, 60, 120), r=17)
            if tp == "dgn":
                for k in range(7): a = R(0, 6.3); rr_ = R(10, 40); xx_, yy_ = x + rr_ * math.cos(a), y + rr_ * math.sin(a); d.ellipse([xx_ - 13, yy_ - 10, xx_ - 1, yy_ + 10], fill=pink); d.ellipse([xx_ + 1, yy_ - 10, xx_ + 13, yy_ + 10], fill=pink)
        for _ in range(28 if tp != "dgn" else 0):
            x, y = R(60, W - 60), R(60, W - 60)
            if tp == "cgp_cachos":
                for k in range(9): dx_, dy_ = R(-24, 24), R(-24, 24); d.ellipse([x + dx_ - 9, y + dy_ - 9, x + dx_ + 9, y + dy_ + 9], fill=purple)
            elif tp == "cgp_cadeia":
                a = R(0, 6.3)
                for k in range(7): d.ellipse([x + k * 17 * math.cos(a) - 8, y + k * 17 * math.sin(a) + 6 * math.sin(k) - 8, x + k * 17 * math.cos(a) + 8, y + k * 17 * math.sin(a) + 6 * math.sin(k) + 8], fill=purple)
            elif tp == "diplo_lanceta":
                a = R(0, 6.3)
                for k in (-1, 1): cx_, cy_ = x + k * 11 * math.cos(a), y + k * 11 * math.sin(a); d.polygon([(cx_ + 12 * k * math.cos(a), cy_ + 12 * k * math.sin(a)), (cx_ - 9 * math.sin(a), cy_ + 9 * math.cos(a)), (cx_ - 6 * k * math.cos(a), cy_ - 6 * k * math.sin(a)), (cx_ + 9 * math.sin(a), cy_ - 9 * math.cos(a))], fill=purple)
            elif tp == "bgn":
                a = R(0, 3.14); d.line([(x, y), (x + 30 * math.cos(a), y + 30 * math.sin(a))], fill=pink, width=12)
            elif tp == "bgp":
                a = R(0, 3.14); d.line([(x, y), (x + 40 * math.cos(a), y + 40 * math.sin(a))], fill=purple, width=14)
            elif tp == "levedura":
                d.ellipse([x - 16, y - 12, x + 16, y + 12], fill=purple); d.ellipse([x + 12, y - 8, x + 26, y + 6], fill=purple)
                if _ % 4 == 0: d.line([(x, y), (x + 120, y + 40)], fill=purple, width=10)
    elif mode == "sed":
        for _ in range(26): x, y = R(40, W - 40), R(40, W - 40); d.ellipse([x - 7, y - 7, x + 7, y + 7], outline=(150, 150, 150), width=2)
        def cast(x, y, a, fillc, inner=None, L=440, w=84):
            dx, dy = L / 2 * math.cos(a), L / 2 * math.sin(a); px, py = -w / 2 * math.sin(a), w / 2 * math.cos(a)
            d.polygon([(x - dx + px, y - dy + py), (x + dx + px, y + dy + py), (x + dx - px, y + dy - py), (x - dx - px, y - dy - py)], fill=fillc, outline=(110, 110, 110))
            if inner:
                for k in range(14): t = R(-.45, .45); s = R(-.3, .3); cx_, cy_ = x + 2 * dx * t + 2 * px * s, y + 2 * dy * t + 2 * py * s; inner(cx_, cy_)
        for k in range(3):
            x, y, a = R(200, W - 200), R(200, W - 200), R(0, 3.1)
            if tp == "hem_cil": cast(x, y, a, (200, 175, 160), lambda cx_, cy_: d.ellipse([cx_ - 10, cy_ - 10, cx_ + 10, cy_ + 14], fill=(200, 80, 70)))
            elif tp == "leuco_cil": cast(x, y, a, (205, 200, 190), lambda cx_, cy_: d.ellipse([cx_ - 12, cy_ - 12, cx_ + 12, cy_ + 12], fill=(160, 160, 175), outline=(90, 90, 110)))
            elif tp == "granuloso": cast(x, y, a, (120, 95, 70), lambda cx_, cy_: d.ellipse([cx_ - 5, cy_ - 5, cx_ + 5, cy_ + 5], fill=(70, 50, 35)))
            elif tp == "hialino": cast(x, y, a, (222, 226, 222))
            elif tp == "ceroso": cast(x, y, a, (225, 215, 170)); d.line([(x, y - 20), (x + 15, y + 20)], fill=(150, 140, 110), width=3)
        if tp == "dismorficas":
            for _ in range(40): x, y = R(60, W - 60), R(60, W - 60); d.ellipse([x - 20, y - 20, x + 20, y + 20], outline=(190, 90, 90), width=5); d.ellipse([x + 14, y - 10, x + 26, y + 2], outline=(190, 90, 90), width=4)
        for _ in range(18 if tp in ("oxalato", "urico", "estruvita", "cistina") else 0):
            x, y = R(80, W - 80), R(80, W - 80); s = R(22, 40)
            if tp == "oxalato": d.rectangle([x - s, y - s, x + s, y + s], outline=(70, 70, 70), width=4); d.line([(x - s, y - s), (x + s, y + s)], fill=(70, 70, 70), width=3); d.line([(x - s, y + s), (x + s, y - s)], fill=(70, 70, 70), width=3)
            elif tp == "urico": d.polygon([(x - s * 1.4, y), (x, y - s * .8), (x + s * 1.4, y), (x, y + s * .8)], fill=(220, 180, 60), outline=(150, 110, 20))
            elif tp == "estruvita": d.polygon([(x - s * 1.6, y - s * .5), (x - s * 1.2, y - s * .9), (x + s * 1.2, y - s * .9), (x + s * 1.6, y - s * .5), (x + s * 1.2, y + s * .7), (x - s * 1.2, y + s * .7)], fill=(225, 230, 228), outline=(80, 80, 80))
            elif tp == "cistina": d.regular_polygon((x, y, s * 1.2), 6, outline=(70, 70, 70), fill=(225, 228, 222))
    elif mode == "cryst":
        d.line([(W * .3, W * .86), (W * .45, W * .71)], fill=(240, 240, 240), width=6); d.polygon([(W * .45, W * .71), (W * .418, W * .725), (W * .435, W * .742)], fill=(240, 240, 240))
        d.text((W * .27, W * .875), "γ · eixo do compensador", font=fnt(34), fill=(235, 235, 235))
        axis = math.atan2(-1, 1)
        for k in range(16):
            x, y = R(150, W - 150), R(120, W - 220); par = k % 2 == 0; a = axis + (0 if par else math.pi / 2) + R(-.15, .15)
            if tp == "urato":
                col = (240, 210, 40) if par else (60, 140, 255); L = R(70, 120)
                d.line([(x - L * math.cos(a), y - L * math.sin(a)), (x + L * math.cos(a), y + L * math.sin(a))], fill=col, width=9)
            else:
                col = (70, 150, 255) if par else (230, 205, 70); L = R(28, 46)
                pts = [(x + L * math.cos(a), y + L * math.sin(a)), (x + L * .45 * math.cos(a + 1.9), y + L * .45 * math.sin(a + 1.9)), (x - L * math.cos(a), y - L * math.sin(a)), (x - L * .45 * math.cos(a + 1.9), y - L * .45 * math.sin(a + 1.9))]
                d.polygon(pts, fill=col)
        for _ in range(10): x, y = R(80, W - 80), R(80, W - 80); d.ellipse([x - 36, y - 36, x + 36, y + 36], outline=(60, 55, 80), width=3)
    elif mode == "ana":
        g = lambda v: (int(20 + 40 * v), int(60 + 195 * v), int(30 + 60 * v))
        for k in range(16):
            x, y = R(110, W - 110), R(110, W - 110); r = R(60, 78)
            d.ellipse([x - r * 1.35, y - r * 1.25, x + r * 1.35, y + r * 1.25], fill=g(0.45 if tp == "cito" else 0.08))
            if tp == "homog": d.ellipse([x - r, y - r, x + r, y + r], fill=g(0.85))
            elif tp in ("pontilhado", "centromero", "nucleolar"):
                d.ellipse([x - r, y - r, x + r, y + r], fill=g(0.18))
                n, s = {"pontilhado": (140, 4), "centromero": (46, 7), "nucleolar": (4, 16)}[tp]
                for _ in range(n): a, rr = R(0, 6.3), r * math.sqrt(R(0, .85)); d.ellipse([x + rr * math.cos(a) - s, y + rr * math.sin(a) - s, x + rr * math.cos(a) + s, y + rr * math.sin(a) + s], fill=g(0.95))
            elif tp == "cito": d.ellipse([x - r, y - r, x + r, y + r], fill=g(0.08))
            if tp == "homog" and k == 3: d.rectangle([x - r * .9, y - 12, x + r * .9, y + 12], fill=g(1.0))
    im = im.filter(ImageFilter.GaussianBlur(1.6 if mode in ("smear", "gram", "sed") else 1.2))
    out = _vignette(im, bgc)
    _frame(out, path, title, sp.get("sub", ""))


# ============================================================ cintilografia de tireoide
def scint(sp, path, title):
    """sp: tipo: graves|quente|frio|bmn|baixa ; capt (texto de captação)"""
    W, H = 560, 560; tp = sp["tipo"]; rng = np.random.default_rng(3)
    lob = _mask(W, H, lambda d: (d.ellipse([150, 120, 265, 430], fill=255), d.ellipse([295, 120, 410, 430], fill=255), d.rectangle([240, 300, 320, 360], fill=255)), 10)
    act = lob * {"graves": 1.0, "quente": 0.12, "frio": 0.7, "bmn": 0.6, "baixa": 0.06}[tp]
    if tp == "quente": act += 1.0 * _mask(W, H, lambda d: d.ellipse([300, 230, 400, 340], fill=255), 8)
    if tp == "frio": act *= 1 - 0.85 * _mask(W, H, lambda d: d.ellipse([170, 240, 250, 330], fill=255), 6)
    if tp == "bmn": act *= 0.5 + 1.0 * _blur(rng.random((H, W)), 18) ** 1.5 * 3
    if tp == "baixa": act += 0.12 * _mask(W, H, lambda d: (d.ellipse([255, 470, 305, 520], fill=255)), 8)
    act = np.clip(act, 0, 1) + rng.normal(0, 0.02, (H, W))
    a = np.clip(act, 0, 1); rgb = np.stack([np.clip(a * 2.2, 0, 1), np.clip(a * 2.2 - 0.9, 0, 1), np.clip(a * 3 - 2.2, 0, 1)], -1)
    im = Image.fromarray((rgb * 255).astype(np.uint8))
    d = ImageDraw.Draw(im); d.text((20, 18), "Tc-99m · anterior", font=fnt(22), fill=(200, 200, 200)); d.text((20, 520), sp.get("capt", ""), font=fnt(22, True), fill=(255, 220, 120))
    d.text((28, 270), "D", font=fnt(28, True), fill=(255, 224, 138))
    _frame(im, path, title, sp.get("sub", "Cintilografia de tireoide"))


# ============================================================ mapa corporal (frente e costas)
REG = {}  # nome: (lado 'f'/'c', polígono/elipse)
def _body_regions(ox):
    """Regiões simplificadas no estilo Lund-Browder; ox = deslocamento horizontal do boneco."""
    r = {}
    r["cabeca"] = ("e", (ox + 70, 20, ox + 150, 110)); r["pescoco"] = ("r", (ox + 95, 108, ox + 125, 135))
    r["tronco_sup"] = ("r", (ox + 55, 135, ox + 165, 245)); r["tronco_inf"] = ("r", (ox + 60, 245, ox + 160, 345))
    r["genital"] = ("r", (ox + 98, 345, ox + 122, 368))
    r["braco_d"] = ("p", [(ox + 55, 140), (ox + 30, 150), (ox + 18, 255), (ox + 40, 258), (ox + 55, 175)]); r["antebraco_d"] = ("p", [(ox + 18, 258), (ox + 40, 258), (ox + 32, 345), (ox + 10, 345)])
    r["mao_d"] = ("e", (ox + 4, 345, ox + 36, 390))
    r["braco_e"] = ("p", [(ox + 165, 140), (ox + 190, 150), (ox + 202, 255), (ox + 180, 258), (ox + 165, 175)]); r["antebraco_e"] = ("p", [(ox + 202, 258), (ox + 180, 258), (ox + 188, 345), (ox + 210, 345)])
    r["mao_e"] = ("e", (ox + 184, 345, ox + 216, 390))
    r["coxa_d"] = ("r", (ox + 60, 368, ox + 108, 480)); r["perna_d"] = ("r", (ox + 64, 480, ox + 104, 590)); r["pe_d"] = ("r", (ox + 58, 590, ox + 104, 612))
    r["coxa_e"] = ("r", (ox + 112, 368, ox + 160, 480)); r["perna_e"] = ("r", (ox + 116, 480, ox + 156, 590)); r["pe_e"] = ("r", (ox + 116, 590, ox + 162, 612))
    return r


def body(sp, path, title):
    """sp: frente=[(região, grau)], costas=[(região, grau)], grau: s (superficial), p (parcial), f (total), x (lesão), leg=True, sub, nota"""
    W, H = 760, 760; im = Image.new("RGB", (W, H), "#fbfaf7"); d = ImageDraw.Draw(im)
    COLG = {"s": (247, 196, 196), "p": (214, 64, 52), "f": (90, 40, 30), "x": (150, 70, 160)}
    for ox, side, lab in ((90, "frente", "Frente"), (430, "costas", "Costas")):
        R = _body_regions(ox); marks = dict(sp.get(side, []))
        for nm, (kind, geo) in R.items():
            key = nm if side == "frente" else (nm[:-2] + ("_e" if nm.endswith("_d") else "_d") if nm[-2:] in ("_d", "_e") else nm)
            fill = COLG[marks[key]] if key in marks else (232, 226, 214)
            if nm == "genital" and side == "costas": continue
            (d.ellipse if kind == "e" else d.rectangle if kind == "r" else d.polygon)(geo, fill=fill, outline=(120, 110, 100))
        d.text((ox + 82, 640), lab, font=fnt(24, True), fill="#1d2433")
    if sp.get("leg", True):
        x = 20
        for g, txt in (("s", "1º grau (não entra na SCQ)"), ("p", "2º grau"), ("f", "3º grau"), ("x", "lesão")):
            if any(gg == g for _, gg in sp.get("frente", []) + sp.get("costas", [])) or (g == "s" and sp.get("burn", True)):
                d.rectangle([x, 690, x + 24, 712], fill=COLG[g], outline=(100, 100, 100)); d.text((x + 30, 690), txt, font=fnt(17), fill="#333"); x += 50 + d.textlength(txt, font=fnt(17))
    if sp.get("nota"): d.text((20, 725), sp["nota"], font=fnt(17), fill="#333")
    _frame(im, path, title, sp.get("sub", ""), dark=False)
