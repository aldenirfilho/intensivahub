"""🖼️ Figuras das questões ilustradas (4.24.0) — gráficos e esquemas em matplotlib/PIL.
Toda figura é sintética e didática. Cada função recebe (spec, path, title) e grava PNG (ou JPG, pela extensão)."""
import io, math, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import patches
from PIL import Image, ImageDraw, ImageFont

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11.5, "axes.titlesize": 12.5, "axes.labelsize": 11.5,
                     "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.alpha": .25,
                     "legend.fontsize": 10, "legend.frameon": False, "axes.titleweight": "bold"})
PAL = ["#1f5fa8", "#c0392b", "#1e8449", "#b9770e", "#7d3c98", "#117a8b", "#555555", "#d35400"]
INK, MUTE, GOLD = "#1d2433", "#7a8090", "#9a6b00"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"; FONTB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
TAG = "CÓDICE 360X · figura sintética didática"


def fnt(s, b=False): return ImageFont.truetype(FONTB if b else FONT, s)


def save_pil(im, path, colors=96):
    if path.lower().endswith(".jpg"):
        im.convert("RGB").save(path, quality=80, optimize=True, progressive=True)
    else:
        im = im.convert("RGB").quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE) if colors else im
        im.save(path, optimize=True)


def mfig(h=5.4, w=10.0, title="", dark=False):
    bg = "#0b0f14" if dark else "#fbfaf7"
    fig = plt.figure(figsize=(w, h), dpi=100, facecolor=bg)
    fig.text(0.012, 0.985, title, ha="left", va="top", fontsize=12.5, fontweight="bold", color="#e8c66a" if dark else "#6e1e1e")
    fig.text(0.988, 0.985, TAG, ha="right", va="top", fontsize=8.5, color="#8a93a3" if dark else MUTE)
    return fig


def save_fig(fig, path, colors=96):
    b = io.BytesIO(); fig.savefig(b, format="png", facecolor=fig.get_facecolor(), dpi=100); plt.close(fig); b.seek(0)
    save_pil(Image.open(b), path, colors)


def _axes(fig, rect=(0.08, 0.12, 0.88, 0.76)):
    ax = fig.add_axes(rect); ax.set_facecolor("#ffffff"); return ax


# ---------------------------------------------------------------- linhas (tendências, curvas)
def lines(sp, path, title):
    """sp: x, series=[{y, lab, c, ax(0/1), ls, mk, step, lw, x}], xl, yl, yl2, ylim, ylim2, xlim, logy, bands=[(y0,y1,cor,txt)],
    vb=[(x0,x1,cor,txt)], hl=[(y,txt,cor)], vl=[(x,txt,cor)], ann=[(x,y,txt)], sub, xt (rótulos), h, leg (loc)"""
    fig = mfig(sp.get("h", 5.4), title=title); ax = _axes(fig, sp.get("rect", (0.085, 0.13, 0.83 if any(s.get("ax") for s in sp["series"]) else 0.885, 0.74)))
    ax2 = ax.twinx() if any(s.get("ax") for s in sp["series"]) else None
    if ax2 is not None: ax2.spines["right"].set_visible(True); ax2.grid(False)
    for y0, y1, c, t in sp.get("bands", []):
        ax.axhspan(y0, y1, color=c, alpha=.13, lw=0)
        if t: ax.text(0.995, (y0 + y1) / 2, t, transform=ax.get_yaxis_transform(), ha="right", va="center", fontsize=9, color=c, alpha=.95)
    for x0, x1, c, t in sp.get("vb", []):
        ax.axvspan(x0, x1, color=c, alpha=.12, lw=0)
        if t: ax.text((x0 + x1) / 2, 0.985, t, transform=ax.get_xaxis_transform(), ha="center", va="top", fontsize=9, color=c)
    for i, s in enumerate(sp["series"]):
        a = ax2 if s.get("ax") else ax; c = s.get("c", PAL[i % len(PAL)]); x = s.get("x", sp.get("x"))
        kw = dict(color=c, lw=s.get("lw", 2.4), ls=s.get("ls", "-"), label=s.get("lab"), marker=s.get("mk", "o" if len(s["y"]) <= 16 else None), ms=s.get("ms", 6))
        if s.get("step"): a.step(x, s["y"], where="post", **{k: v for k, v in kw.items() if k not in ("marker", "ms")})
        else: a.plot(x, s["y"], **kw)
        if s.get("lbl"):
            for xx, yy in zip(x, s["y"]): a.annotate(f"{yy:g}".replace(".", ","), (xx, yy), textcoords="offset points", xytext=(0, 8), ha="center", fontsize=9, color=c)
    for y, t, *c in sp.get("hl", []):
        cc = c[0] if c else "#888"; ax.axhline(y, color=cc, ls="--", lw=1.3)
        if t: ax.text(0.005, y, " " + t, transform=ax.get_yaxis_transform(), va="bottom", fontsize=9, color=cc)
    for x, t, *c in sp.get("vl", []):
        cc = c[0] if c else "#888"; ax.axvline(x, color=cc, ls=":", lw=1.4)
        if t: ax.text(x, 0.02, " " + t, transform=ax.get_xaxis_transform(), rotation=90, va="bottom", fontsize=9, color=cc)
    for x, y, t in sp.get("ann", []): ax.annotate(t, (x, y), textcoords="offset points", xytext=(6, 10), fontsize=9.5, color=INK, arrowprops=dict(arrowstyle="-", color="#999", lw=.8))
    if sp.get("logy"): ax.set_yscale("log")
    if sp.get("logy2") and ax2 is not None: ax2.set_yscale("log")
    if "ylim" in sp: ax.set_ylim(*sp["ylim"])
    if "xlim" in sp: ax.set_xlim(*sp["xlim"])
    if ax2 is not None and "ylim2" in sp: ax2.set_ylim(*sp["ylim2"])
    if "xt" in sp: ax.set_xticks(sp["x"] if "xtp" not in sp else sp["xtp"]); ax.set_xticklabels(sp["xt"], fontsize=10)
    ax.set_xlabel(sp.get("xl", "")); ax.set_ylabel(sp.get("yl", ""))
    if ax2 is not None: ax2.set_ylabel(sp.get("yl2", ""))
    if sp.get("sub"): ax.set_title(sp["sub"], loc="left", fontsize=11.5, color=INK)
    hs, ls_ = ax.get_legend_handles_labels()
    if ax2 is not None: h2, l2 = ax2.get_legend_handles_labels(); hs += h2; ls_ += l2
    if any(ls_): ax.legend(hs, ls_, loc=sp.get("leg", "best"))
    save_fig(fig, path)


# ---------------------------------------------------------------- barras
def bars(sp, path, title):
    """sp: cats, groups=[{v, lab, c}], yl, hl=[(y,txt)], horiz, sub, ylim, vals (mostrar valores), stacked"""
    fig = mfig(sp.get("h", 5.2), title=title); ax = _axes(fig, sp.get("rect", (0.09 if not sp.get("horiz") else 0.25, 0.13, 0.86 if not sp.get("horiz") else 0.71, 0.74)))
    n = len(sp["groups"]); idx = np.arange(len(sp["cats"])); w = 0.8 / (1 if sp.get("stacked") else n); base = np.zeros(len(idx))
    for i, g in enumerate(sp["groups"]):
        c = g.get("c", PAL[i % len(PAL)]); v = np.array(g["v"], float)
        pos = idx if sp.get("stacked") else idx - 0.4 + w * (i + .5)
        if sp.get("horiz"): r = ax.barh(pos, v, w * .92, left=base if sp.get("stacked") else None, color=c, label=g.get("lab"))
        else: r = ax.bar(pos, v, w * .92, bottom=base if sp.get("stacked") else None, color=c, label=g.get("lab"))
        if sp.get("vals", True) and not sp.get("stacked"):
            for rr, vv in zip(r, v):
                t = (f"{vv:g}").replace(".", ",")
                if sp.get("horiz"): ax.text(rr.get_width(), rr.get_y() + rr.get_height() / 2, " " + t, va="center", fontsize=9.5)
                else: ax.text(rr.get_x() + rr.get_width() / 2, rr.get_height(), t, ha="center", va="bottom", fontsize=9.5)
        if sp.get("stacked"): base = base + v
    if sp.get("horiz"): ax.set_yticks(idx); ax.set_yticklabels(sp["cats"]); ax.invert_yaxis(); ax.set_xlabel(sp.get("yl", ""))
    else: ax.set_xticks(idx); ax.set_xticklabels(sp["cats"], fontsize=10); ax.set_ylabel(sp.get("yl", ""))
    for y, t in sp.get("hl", []):
        (ax.axvline if sp.get("horiz") else ax.axhline)(y, color="#888", ls="--", lw=1.2)
    if "ylim" in sp: (ax.set_xlim if sp.get("horiz") else ax.set_ylim)(*sp["ylim"])
    if sp.get("sub"): ax.set_title(sp["sub"], loc="left", color=INK)
    if any(g.get("lab") for g in sp["groups"]): ax.legend(loc=sp.get("leg", "best"))
    save_fig(fig, path)


# ---------------------------------------------------------------- tabela de exames (PIL)
def tab(sp, path, title):
    """sp: cols=[...], rows=[[...]], sub, w (colunas), note, flags: célula iniciando com '↑' vermelho, '↓' azul, '!' âmbar"""
    cols, rows = sp["cols"], sp["rows"]; fb, fr, fs = fnt(25, True), fnt(24), fnt(19)
    d0 = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    tw = lambda s, f: d0.textlength(str(s), font=f)
    cw = [max([tw(c, fb)] + [tw(r[i], fr) for r in rows]) + 36 for i, c in enumerate(cols)]
    W = max(int(sum(cw)) + 40, 760); sc = 1.0
    if sum(cw) + 40 < W: extra = (W - 40 - sum(cw)) / len(cw); cw = [c + extra for c in cw]
    rh = 46; top = 62 + (34 if sp.get("sub") else 0); H = top + rh * (len(rows) + 1) + 30 + (34 if sp.get("note") else 0)
    im = Image.new("RGB", (W, H), "#fbfaf7"); d = ImageDraw.Draw(im)
    d.text((14, 12), title, font=fnt(24, True), fill="#6e1e1e"); d.text((W - 14 - d.textlength(TAG, font=fs), 16), TAG, font=fs, fill="#8a8a8a")
    if sp.get("sub"): d.text((20, 54), sp["sub"], font=fnt(23, True), fill="#1d2433")
    x0, y = 20, top
    d.rectangle([x0, y, W - 20, y + rh], fill="#1d2b45")
    x = x0
    for i, c in enumerate(cols): d.text((x + 16, y + 11), str(c), font=fb, fill="#f5e7b8"); x += cw[i]
    for ri, r in enumerate(rows):
        y += rh; d.rectangle([x0, y, W - 20, y + rh], fill="#ffffff" if ri % 2 == 0 else "#f1f3f7")
        x = x0
        for i, c in enumerate(r):
            s = str(c); col = "#1d2433"; f = fr
            if s.startswith("↑"): col = "#b3261e"; f = fnt(24, True)
            elif s.startswith("↓"): col = "#1f5fa8"; f = fnt(24, True)
            elif s.startswith("!"): col = "#9a6b00"; f = fnt(24, True); s = s[1:]
            d.text((x + 16, y + 11), s, font=f, fill=col); x += cw[i]
    d.rectangle([x0, top, W - 20, y + rh], outline="#9aa3b5", width=2)
    if sp.get("note"): d.text((22, y + rh + 12), sp["note"], font=fs, fill="#555")
    save_pil(im, path, colors=64)


# ---------------------------------------------------------------- Kaplan-Meier
def km(sp, path, title):
    """sp: arms=[{lab, hz (taxa constante/mês) ou pts=[(t,S)], c}], tmax, xl, sub, hr (texto), risk (nº em risco por braço)"""
    fig = mfig(5.6, title=title); ax = _axes(fig, (0.09, 0.14, 0.87, 0.72))
    for i, a in enumerate(sp["arms"]):
        c = a.get("c", PAL[i])
        if "pts" in a: t, s = zip(*a["pts"])
        else:
            t = np.linspace(0, sp["tmax"], 25); s = np.exp(-a["hz"] * t)
            if a.get("plateau") is not None: s = a["plateau"] + (1 - a["plateau"]) * np.exp(-a["hz"] * t)
        ax.step(t, np.array(s) * 100, where="post", color=c, lw=2.6, label=a["lab"])
    ax.set_ylim(0, 102); ax.set_xlim(0, sp["tmax"]); ax.set_ylabel(sp.get("yl", "Sobrevida (%)")); ax.set_xlabel(sp.get("xl", "Meses"))
    if sp.get("hr"): ax.text(0.02, 0.06, sp["hr"], transform=ax.transAxes, fontsize=11, color=INK, bbox=dict(fc="#fff8e6", ec="#d9b45a"))
    if sp.get("sub"): ax.set_title(sp["sub"], loc="left", color=INK)
    if sp.get("hl"): ax.axhline(sp["hl"], color="#999", ls=":", lw=1.2)
    ax.legend(loc="upper right"); save_fig(fig, path)


# ---------------------------------------------------------------- forest plot
def forest(sp, path, title):
    """sp: rows=[(rótulo, est, lo, hi, peso?)], total=(est,lo,hi) opcional, null=1, xl, log, ticks, sub, left/right (rótulos de favorecimento)"""
    from matplotlib.ticker import NullFormatter, FixedLocator
    rows = sp["rows"]; n = len(rows) + (2 if sp.get("total") else 0)
    fig = mfig(max(3.4, 1.9 + 0.5 * n), title=title); ax = _axes(fig, (0.36, 0.22, 0.40, 0.6))
    ax.set_ylim(0.3, n + 0.7); ys = []
    for i, (lab, e, lo, hi, *w) in enumerate(rows):
        y = n - i; ax.plot([lo, hi], [y, y], color=INK, lw=1.6); s_ = 50 + (w[0] * 4 if w else 40)
        ax.scatter([e], [y], s=s_, marker="s", color="#1f5fa8", zorder=3); ys.append((y, lab, f"{e:.2f} ({lo:.2f}–{hi:.2f})".replace(".", ","), False))
    if sp.get("total"):
        e, lo, hi = sp["total"]; y = 1
        ax.fill([lo, e, hi, e], [y, y + .32, y, y - .32], color="#c0392b"); ys.append((y, sp.get("totlab", "Global"), f"{e:.2f} ({lo:.2f}–{hi:.2f})".replace(".", ","), True))
    nl = sp.get("null", 1); ax.axvline(nl, color="#666", lw=1.2)
    if sp.get("margin") is not None:
        ax.axvline(sp["margin"], color="#c0392b", ls="--", lw=1.6); ax.text(sp["margin"], n + 0.55, " margem", color="#c0392b", fontsize=9.5, va="top")
    tk = sp.get("ticks", [0.25, 0.5, 1, 2, 4])
    if sp.get("log", True): ax.set_xscale("log")
    ax.set_xlim(sp.get("xlim", (tk[0], tk[-1])))
    ax.xaxis.set_major_locator(FixedLocator(tk)); ax.xaxis.set_minor_formatter(NullFormatter()); ax.set_xticklabels([f"{t:g}".replace(".", ",") for t in tk])
    ax.set_yticks([]); ax.spines["left"].set_visible(False); ax.grid(axis="y", visible=False)
    fig.canvas.draw()
    for y, lab, txt, bold in ys:
        yf = fig.transFigure.inverted().transform(ax.transData.transform((tk[0], y)))[1]
        fig.text(0.015, yf, lab, va="center", fontsize=10.5, color=INK, fontweight="bold" if bold else "normal")
        fig.text(0.78, yf, txt, va="center", fontsize=10.5, color=INK, fontweight="bold" if bold else "normal")
    fig.text(0.78, 0.89, sp.get("cab", "Efeito (IC 95%)"), fontsize=10, color=MUTE)
    ax.set_xlabel(sp.get("xl", "Risco relativo (IC 95%)"))
    if sp.get("left"): fig.text(0.37, 0.025, "← " + sp["left"], fontsize=9.5, color="#1e8449")
    if sp.get("right"): fig.text(0.75, 0.025, sp["right"] + " →", ha="right", fontsize=9.5, color="#c0392b")
    if sp.get("sub"): fig.text(0.015, 0.9, sp["sub"], fontsize=11.5, fontweight="bold", color=INK)
    save_fig(fig, path)


# ---------------------------------------------------------------- ROC
def roc(sp, path, title):
    """sp: curves=[{lab, auc, c}] (curva binormal), pts=[(1-esp, sens, txt)], sub"""
    from math import sqrt
    fig = mfig(6.2, w=8.4, title=title); ax = _axes(fig, (0.11, 0.11, 0.84, 0.76))
    from scipy.stats import norm
    for i, c in enumerate(sp["curves"]):
        auc = c["auc"]; dprime = sqrt(2) * norm.ppf(auc); fpr = np.linspace(0, 1, 200); tpr = norm.cdf(dprime + norm.ppf(np.clip(fpr, 1e-6, 1 - 1e-6)))
        ax.plot(fpr, tpr, color=c.get("c", PAL[i]), lw=2.6, label=f"{c['lab']} (AUC {auc:.2f})".replace(".", ","))
    ax.plot([0, 1], [0, 1], ls="--", color="#999", lw=1.2, label="Acaso (AUC 0,50)")
    for x, y, t in sp.get("pts", []): ax.scatter([x], [y], s=70, color="#b9770e", zorder=4); ax.annotate(t, (x, y), textcoords="offset points", xytext=(8, -14), fontsize=10)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1.01); ax.set_xlabel("1 − especificidade"); ax.set_ylabel("Sensibilidade"); ax.legend(loc="lower right")
    if sp.get("sub"): ax.set_title(sp["sub"], loc="left", color=INK)
    save_fig(fig, path)


# ---------------------------------------------------------------- fluxograma com lacuna
def flow(sp, path, title):
    """sp: nodes=[(id, texto, x, y, estilo)] em unidades (0–10 × 0–N), edges=[(a, b, rótulo)], h, sub. estilo: 'q' (lacuna ?), 'd' (decisão), 'g' (verde), 'r' (vermelho)"""
    H = sp.get("h", 6.4); fig = mfig(H, title=title); ax = fig.add_axes((0.02, 0.02, 0.96, 0.88)); ax.axis("off")
    ys = [n[3] for n in sp["nodes"]]; ax.set_xlim(0, 10); ax.set_ylim(min(ys) - .8, max(ys) + .8); P = {}
    for nid, txt, x, y, *st in sp["nodes"]:
        st = st[0] if st else ""; w = sp.get("bw", 2.9); h = 0.62 + 0.27 * txt.count("\n")
        fc = {"q": "#fff2cc", "d": "#e8f0fb", "g": "#e3f4e6", "r": "#fbe5e3", "": "#ffffff"}[st]; ec = {"q": "#d4a017", "d": "#1f5fa8", "g": "#1e8449", "r": "#c0392b", "": "#465066"}[st]
        box = patches.FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.06,rounding_size=0.12", fc=fc, ec=ec, lw=2.2 if st == "q" else 1.5, ls="--" if st == "q" else "-")
        ax.add_patch(box); ax.text(x, y, txt, ha="center", va="center", fontsize=12 if st == "q" else 10.2, fontweight="bold" if st in ("q", "d") else "normal", color=INK, wrap=True)
        P[nid] = (x, y, w, h)
    for a, b, *lab in sp["edges"]:
        xa, ya, wa, ha = P[a]; xb, yb, wb, hb = P[b]
        if abs(ya - yb) < 0.05: s, e = (xa + (wa / 2 if xb > xa else -wa / 2), ya), (xb - (wb / 2 if xb > xa else -wb / 2), yb)
        else: s, e = (xa, ya - ha / 2 if yb < ya else ya + ha / 2), (xb, yb + hb / 2 if yb < ya else yb - hb / 2)
        ax.annotate("", xy=e, xytext=s, arrowprops=dict(arrowstyle="-|>", color="#465066", lw=1.5, connectionstyle="arc3,rad=0" if abs(xa - xb) < .05 or abs(ya - yb) < .05 else "angle,angleA=0,angleB=90"))
        if lab and lab[0]: ax.text((s[0] + e[0]) / 2 + .08, (s[1] + e[1]) / 2, lab[0], fontsize=9.5, color="#1f5fa8", fontweight="bold")
    if sp.get("sub"): fig.text(0.015, 0.93, sp["sub"], fontsize=11.5, fontweight="bold", color=INK)
    save_fig(fig, path)


# ---------------------------------------------------------------- Gamblegram
def gamble(sp, path, title):
    """sp: cols=[{lab, cat:[(nome, val, cor)], an:[(nome, val, cor)]}] — cada coluna mostra cátions × ânions (mEq/L)"""
    fig = mfig(5.8, title=title); ax = _axes(fig, (0.08, 0.08, 0.9, 0.8)); ax.grid(False)
    x = 0
    for col in sp["cols"]:
        for side, items in ((0, col["cat"]), (1, col["an"])):
            b = 0
            for nm, v, c in items:
                ax.bar(x + side * 0.95, v, 0.9, bottom=b, color=c, ec="white", lw=1.2)
                if v >= 6: ax.text(x + side * 0.95, b + v / 2, f"{nm}\n{v:g}".replace(".", ","), ha="center", va="center", fontsize=9.5, color="white", fontweight="bold")
                b += v
        ax.text(x + .47, -9, col["lab"], ha="center", va="top", fontsize=11, fontweight="bold", color=INK)
        x += 2.6
    ax.set_xticks([]); ax.set_ylabel("mEq/L"); ax.set_ylim(-20, max(sum(v for _, v, _ in c["cat"]) for c in sp["cols"]) + 8); ax.axhline(0, color="#444", lw=1)
    save_fig(fig, path)


# ---------------------------------------------------------------- Rumack-Matthew
def nomo(sp, path, title):
    """sp: pts=[(h, µg/mL, rótulo)]"""
    fig = mfig(5.8, title=title); ax = _axes(fig, (0.1, 0.12, 0.86, 0.74))
    t = np.linspace(4, 24, 100); L = 150 * 2 ** (-(t - 4) / 4)
    ax.plot(t, L, color="#c0392b", lw=2.6, label="Linha de tratamento (150 µg/mL na 4ª h)")
    ax.plot(t, 2 * L, color="#7d3c98", lw=1.6, ls="--", label="Linha 'provável hepatotoxicidade' (200 µg/mL na 4ª h)")
    ax.fill_between(t, L, 1000, color="#c0392b", alpha=.07)
    for h, v, lab in sp["pts"]: ax.scatter([h], [v], s=110, color="#1f5fa8", zorder=4, marker="D"); ax.annotate(lab, (h, v), textcoords="offset points", xytext=(10, 6), fontsize=10.5, fontweight="bold", color="#1f5fa8")
    ax.set_yscale("log"); ax.set_ylim(3, 600); ax.set_xlim(0, 24); ax.set_xlabel("Horas após ingestão aguda única"); ax.set_ylabel("Paracetamol sérico (µg/mL)")
    ax.legend(loc="upper right"); save_fig(fig, path)


# ---------------------------------------------------------------- eletroforese de proteínas
def ep(sp, path, title):
    """sp: tipo: normal|mono|poli|nefro|hipo|a1|cirrose ; sub"""
    x = np.linspace(0, 10, 900); g = lambda c, s, a: a * np.exp(-0.5 * ((x - c) / s) ** 2)
    alb, a1, a2, be, ga = 1.0, .09, .17, .16, .22; gw = .55; extra = 0 * x
    tp = sp["tipo"]
    if tp == "mono": extra = g(8.0, .14, .95)
    if tp == "poli": ga, gw = .5, .75
    if tp == "nefro": alb, a2, ga = .45, .42, .12
    if tp == "hipo": ga = .05
    if tp == "a1": a1 = .015
    if tp == "cirrose": alb, ga, gw = .55, .45, .9; extra = g(6.7, .45, .2)
    y = g(2.0, .28, alb) + g(3.5, .22, a1) + g(4.6, .26, a2) + g(6.1, .3, be) + g(8.0, gw, ga) + extra
    fig = mfig(4.8, title=title); ax = _axes(fig, (0.06, 0.18, 0.9, 0.66)); ax.grid(False)
    ax.fill_between(x, y, color="#1f5fa8", alpha=.18); ax.plot(x, y, color="#1f5fa8", lw=2.4)
    for c, lab in ((2.0, "Albumina"), (3.5, "α1"), (4.6, "α2"), (6.1, "β"), (8.0, "γ")): ax.text(c, -0.12, lab, ha="center", fontsize=11, fontweight="bold", color=INK)
    ax.set_yticks([]); ax.set_xticks([]); ax.set_ylim(-0.18, max(1.08, y.max() + .08)); ax.spines["left"].set_visible(False)
    ax.set_title(sp.get("sub", "Eletroforese de proteínas séricas (densitometria)"), loc="left", color=INK)
    save_fig(fig, path)


# ---------------------------------------------------------------- ROTEM
def rotem(sp, path, title):
    """sp: ch=[{lab, ct (s), a10, mcf (mm), li60 (%), sem: True se plano}], sub"""
    chs = sp["ch"]; fig = mfig(1.4 + 1.55 * len(chs), title=title)
    for i, c in enumerate(chs):
        ax = fig.add_axes((0.06, 0.88 - (i + 1) * (0.8 / len(chs)) + 0.02, 0.6, 0.8 / len(chs) - 0.05)); ax.set_facecolor("#0d1b12"); ax.grid(False)
        t = np.linspace(0, 3600, 900); ct = c["ct"]; mcf = c["mcf"]; k = c.get("k", 0.006)
        a = np.where(t < ct, 0, mcf * (1 - np.exp(-k * (t - ct))))
        if c.get("li60") is not None:
            lys = 1 - (1 - c["li60"] / 100) * np.clip((t - ct - 600) / 2400, 0, 1) ** 1.6
            a = a * np.where(t > ct + 600, 1 - (1 - lys), 1) if c["li60"] >= 85 else a * np.where(t > ct + 600, lys, 1)
        ax.fill_between(t / 60, a / 2, -a / 2, color="#3ddc84", alpha=.85); ax.axhline(0, color="#3ddc84", lw=1)
        ax.set_xlim(0, 60); ax.set_ylim(-36, 36); ax.set_yticks([]); ax.tick_params(colors="#666", labelsize=8)
        ax.text(0.01, 0.82, c["lab"], transform=ax.transAxes, color="#e8c66a", fontsize=11, fontweight="bold")
        info = f"CT {c['ct']} s   A10 {c.get('a10', int(mcf * .8))} mm   MCF {mcf} mm" + (f"   LI60 {c['li60']}%" if c.get("li60") is not None else "")
        fig.text(0.68, ax.get_position().y0 + ax.get_position().height / 2, info, va="center", fontsize=11, color=INK, family="DejaVu Sans Mono")
    fig.text(0.06, 0.035, "tempo (min) →", fontsize=9, color=MUTE)
    if sp.get("ref"): fig.text(0.68, 0.035, sp["ref"], fontsize=9, color=MUTE)
    save_fig(fig, path)


# ---------------------------------------------------------------- espirometria: alça fluxo-volume
def spiro(sp, path, title):
    """sp: tipo: normal|obst|obst_grave|rest|fixa|extra|intra ; pred (mostrar prevista tracejada); tab (lista de linhas de texto)"""
    def loop(tp):
        fvc, pef = 4.6, 9.0
        if tp in ("obst", "obst_grave"): fvc = 3.9 if tp == "obst" else 3.0; pef = 5.5 if tp == "obst" else 3.0
        if tp == "rest": fvc, pef = 2.6, 7.8
        v = np.linspace(0, fvc, 300); u = v / fvc
        if tp in ("obst", "obst_grave"): ex = pef * (np.minimum(u / 0.08, 1) ** .7) * (1 - u) ** (2.6 if tp == "obst" else 3.4) / ((1 - .08) ** (2.6 if tp == "obst" else 3.4)) * np.where(u < .08, 1, 1)
        else: ex = pef * np.where(u < .12, (u / .12) ** .6, (1 - u) / (1 - .12))
        insp = -0.85 * pef * np.sin(np.pi * u) ** .9
        if tp in ("fixa", "extra"): ex = np.minimum(ex, 3.2) if tp == "fixa" else ex
        if tp in ("fixa", "extra"): insp = np.maximum(insp, -3.0)
        if tp == "intra": ex = np.minimum(ex, 3.2)
        return v, ex, insp
    fig = mfig(6.0, w=9.2, title=title); ax = _axes(fig, (0.1, 0.11, 0.62 if sp.get("tab") else 0.86, 0.76))
    if sp.get("pred", True):
        v, e, i = loop("normal"); ax.plot(v, e, color="#999", ls="--", lw=1.4, label="Prevista"); ax.plot(v, i, color="#999", ls="--", lw=1.4)
    v, e, i = loop(sp["tipo"]); ax.plot(v, e, color="#1f5fa8", lw=2.8, label="Paciente"); ax.plot(v, i, color="#1f5fa8", lw=2.8)
    ax.axhline(0, color="#444", lw=1); ax.set_xlabel("Volume (L)"); ax.set_ylabel("Fluxo (L/s)   expiração ↑ · inspiração ↓"); ax.legend(loc="upper right"); ax.set_xlim(-0.1, 5.2)
    if sp.get("tab"):
        y = 0.82
        for ln in sp["tab"]: fig.text(0.75, y, ln, fontsize=11.5, color=INK, family="DejaVu Sans Mono"); y -= 0.065
    save_fig(fig, path)


# ---------------------------------------------------------------- alça pressão-volume do VE
def pvloop(sp, path, title):
    """sp: loops=[{tipo, lab}] ; tipo: normal|ea|im|ia|em|inotropo+|inotropo-|precarga+|poscarga+ ; sub"""
    from scipy.interpolate import PchipInterpolator
    def L(tp):
        edv, esv, edp, dbp, sbp, esp = 120, 50, 8, 80, 120, 100
        if tp == "ea": sbp, esp, edp, esv = 195, 160, 20, 55
        if tp == "im": edv, esv, dbp, sbp, esp = 175, 60, 70, 112, 90
        if tp == "ia": edv, esv, dbp, sbp, esp, edp = 215, 85, 45, 150, 120, 16
        if tp == "em": edv, esv, edp, sbp, esp = 85, 40, 6, 105, 88
        if tp == "inotropo+": esv, sbp, esp = 30, 130, 108
        if tp == "inotropo-": esv, edv, edp, sbp, esp = 95, 150, 18, 98, 85
        if tp == "precarga+": edv, edp = 155, 14
        if tp == "poscarga+": sbp, esp, esv, dbp = 160, 140, 75, 105
        p0 = 4
        v1 = np.linspace(esv + (25 if tp == "ia" else 0), edv, 60); p1 = p0 + (edp - p0) * ((v1 - v1[0]) / (edv - v1[0])) ** 2.4
        ve = edv - (22 if tp == "im" else 0)
        v2 = np.linspace(edv, ve, 15); p2 = np.linspace(edp, dbp, 15)
        sx = [0, .12, .4, .8, 1]; sy = [dbp, dbp + .72 * (sbp - dbp), sbp, sbp * .97, esp]
        s_ = np.linspace(0, 1, 70); v3 = ve - (ve - esv) * s_; p3 = PchipInterpolator(sx, sy)(s_)
        v4 = np.linspace(esv, esv + (25 if tp == "ia" else 0), 15); p4 = np.linspace(esp, p0, 15)
        return np.r_[v1, v2, v3, v4], np.r_[p1, p2, p3, p4]
    fig = mfig(5.8, w=9.0, title=title); ax = _axes(fig, (0.1, 0.11, 0.86, 0.76))
    for i, lp in enumerate(sp["loops"]):
        v, p = L(lp["tipo"]); ref = i == 0 and len(sp["loops"]) > 1
        ax.plot(v, p, lw=2.0 if ref else 2.8, ls="--" if ref else "-", color=lp.get("c", "#9a9a9a" if ref else PAL[i % len(PAL)]), label=lp["lab"])
    ax.set_xlabel("Volume do VE (mL)"); ax.set_ylabel("Pressão do VE (mmHg)"); ax.set_xlim(0, 240); ax.set_ylim(0, 220); ax.legend(loc="upper right")
    if sp.get("sub"): ax.set_title(sp["sub"], loc="left", color=INK)
    save_fig(fig, path)


# ---------------------------------------------------------------- curva de dissociação da Hb
def o2hb(sp, path, title):
    """sp: curves=[{p50, lab, c}], pts=[(PaO2, sat, txt)]"""
    fig = mfig(5.6, w=9.0, title=title); ax = _axes(fig, (0.1, 0.12, 0.86, 0.74)); p = np.linspace(0.5, 110, 400)
    for i, c in enumerate(sp["curves"]):
        s = 100 * p ** 2.7 / (p ** 2.7 + c["p50"] ** 2.7); ax.plot(p, s, lw=2.6, color=c.get("c", PAL[i]), label=c["lab"])
    for x, y, t in sp.get("pts", []): ax.scatter([x], [y], s=60, color="#b9770e", zorder=4); ax.annotate(t, (x, y), textcoords="offset points", xytext=(8, -14), fontsize=10)
    ax.axhline(50, color="#aaa", ls=":", lw=1); ax.set_xlabel("PaO₂ (mmHg)"); ax.set_ylabel("SatO₂ (%)"); ax.set_ylim(0, 102); ax.set_xlim(0, 110); ax.legend(loc="lower right")
    save_fig(fig, path)
