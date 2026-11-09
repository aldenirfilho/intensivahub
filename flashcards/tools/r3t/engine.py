"""R3 Turbo 360X — parser de cards compactos + ilustrações didáticas (matplotlib)."""
import re, textwrap, os, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon
BG, FG, GOLD, CY, RD, GR, AM, PU, MU = "#0b0e13", "#ece8dc", "#d4af37", "#4dd4ff", "#ff6b6b", "#5be38a", "#ffc14d", "#b48cff", "#9aa4b2"
PAL = [CY, GOLD, GR, PU, AM, RD, "#7fd1b9", "#f49ac2"]
SEV = {2: [GR, RD], 3: [GR, AM, RD], 4: [GR, AM, "#ff9446", RD], 5: [GR, "#b8e35b", AM, "#ff9446", RD], 6: [GR, "#b8e35b", AM, "#ff9446", RD, "#c43c5a"]}
EMO = re.compile("[\U0001F000-\U0001FAFF☀-➿️‍]")
def plain(s): return EMO.sub("", re.sub(r"\*\*|!!|\+\+", "", s)).replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").strip()
def fmt(s):
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s); s = re.sub(r"!!(.+?)!!", r"<b class=r>\1</b>", s)
    return re.sub(r"\+\+(.+?)\+\+", r"<b class=c>\1</b>", s)

def parse(txt):
    cards, cur = [], None
    for ln in txt.strip().splitlines():
        ln = ln.strip()
        if not ln: continue
        k, v = ln[0], ln[1:].strip()
        if k == "@": cur = dict(t=v[0], f=fmt(v[1:].strip()), body=[], x="", s="", spec=None); cards.append(cur)
        elif k == "|": cur["body"].append(("row", [fmt(c.strip()) for c in ln.strip("|").split("|")]))
        elif k == "-": cur["body"].append(("li", fmt(v)))
        elif k == "=": cur["body"].append(("p", fmt(v)))
        elif k == "!": cur["x"] = fmt(v)
        elif k == "^": cur["s"] = v
        elif k == "%": cur["spec"] = v
        else: raise ValueError(f"linha inválida: {ln}")
    for c in cards:
        out, i, B = "", 0, c.pop("body")
        while i < len(B):
            kind = B[i][0]; j = i
            while j < len(B) and B[j][0] == kind: j += 1
            grp = [b[1] for b in B[i:j]]
            if kind == "row":
                out += "<table class=t><tr>" + "".join(f"<th>{h}</th>" for h in grp[0]) + "</tr>" + "".join("<tr>" + "".join(f"<td>{x}</td>" for x in r) + "</tr>" for r in grp[1:]) + "</table>"
            elif kind == "li": out += "<ul>" + "".join(f"<li>{x}</li>" for x in grp) + "</ul>"
            else: out += "<br>".join(grp) + ("<br>" if j < len(B) else "")
            i = j
        assert out, c["f"]; c["b"] = out
    return cards

def _fig(title, h=5.2):
    fig = plt.figure(figsize=(10, h), facecolor=BG); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 10); ax.set_ylim(0, h); ax.axis("off")
    ax.add_patch(FancyBboxPatch((.12, .12), 9.76, h - .24, boxstyle="round,pad=0.02,rounding_size=.15", fc=BG, ec=GOLD, lw=1.4))
    ax.plot([.5, 9.5], [h - .78, h - .78], color=GOLD, lw=.8, alpha=.6)
    ax.text(5, h - .45, "\n".join(textwrap.wrap(plain(title), 62)), ha="center", va="center", fontsize=15, color=GOLD, family="DejaVu Serif", weight="bold")
    ax.text(9.7, .28, "CÓDICE 360X · R3 CM · Turbo TEMI 360X", ha="right", va="center", fontsize=7.5, color=MU, family="DejaVu Serif")
    ax.text(.3, .28, "◆", ha="left", va="center", fontsize=9, color=CY)
    return fig, ax
def _box(ax, x, y, w, h, t, c, fs=10.5, wrap=None, fill="#141a22"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.03,rounding_size=.1", fc=fill, ec=c, lw=2))
    wrap = wrap or max(10, int(w * 9.5 * 10.5 / fs))
    ax.text(x + w / 2, y + h / 2, "\n".join(sum((textwrap.wrap(p, wrap) or [""] for p in plain(t).split("\\n")), [])), ha="center", va="center", fontsize=fs, color=FG)

def render(spec, path):
    kind, rest = spec.split(" ", 1); title, body = [s.strip() for s in rest.split("::", 1)]
    if kind == "flow":
        st = [s.strip() for s in body.split(">>")]; n = len(st); h = max(4.2, 1.35 + n * 0.95)
        fig, ax = _fig(title, h); top = h - 1.05; bh = min(.72, (top - .55) / n - .2)
        for i, s in enumerate(st):
            y = top - (i + 1) * (bh + .22); lab, _, txt = s.partition(":") if ":" in s[:22] else ("", "", s)
            c = PAL[i % len(PAL)]
            ax.add_patch(FancyBboxPatch((.55, y), .6, bh, boxstyle="round,pad=0.02,rounding_size=.08", fc=c, ec=c))
            ax.text(.85, y + bh / 2, str(i + 1), ha="center", va="center", fontsize=13, color=BG, weight="bold")
            _box(ax, 1.35, y, 8.1, bh, (lab.strip() + " — " if lab else "") + txt.strip(), c, fs=10.5)
            if i < n - 1: ax.annotate("", (.85, y - .2), (.85, y), arrowprops=dict(arrowstyle="->", color=MU, lw=1.4))
    elif kind in ("zones", "cmp"):
        it = [s.strip() for s in body.split("|")]; n = len(it)
        cols = SEV.get(n, PAL) if kind == "zones" else PAL; per = n if n <= 4 else (3 if n in (5, 6, 9) else 4); rows = -(-n // per)
        h = 1.6 + rows * (2.0 if kind == "cmp" else 1.7); fig, ax = _fig(title, h)
        w = (9.0 - (per - 1) * .2) / per; bh = (h - 1.6) / rows - .25
        for i, s in enumerate(it):
            lab, _, txt = s.partition("="); r, k = divmod(i, per); x = .5 + k * (w + .2); y = h - 1.1 - (r + 1) * (bh + .25) + .05
            c = cols[i % len(cols)]
            ax.add_patch(FancyBboxPatch((x, y + bh - .42), w, .42, boxstyle="round,pad=0.02,rounding_size=.08", fc=c, ec=c))
            ax.text(x + w / 2, y + bh - .21, "\n".join(textwrap.wrap(plain(lab), int(w * 7.5))), ha="center", va="center", fontsize=10.5, color=BG, weight="bold")
            _box(ax, x, y, w, bh - .5, txt.strip(), c, fs=9.6 if per >= 4 else 10.2)
            if kind == "zones" and k < per - 1 and i < n - 1: ax.annotate("", (x + w + .19, y + bh - .21), (x + w + .01, y + bh - .21), arrowprops=dict(arrowstyle="->", color=MU, lw=1.2))
    elif kind == "tiers":
        it = [s.strip() for s in body.split("|")]; n = len(it); h = 1.7 + n * .85; fig, ax = _fig(title, h)
        for i, s in enumerate(it):
            y = .55 + i * .82; f1 = i / n; f2 = (i + 1) / n; cx = 5
            w1, w2 = 9 * (1 - f1 * .6), 9 * (1 - f2 * .6); c = PAL[i % len(PAL)]
            ax.add_patch(Polygon([(cx - w1 / 2, y), (cx + w1 / 2, y), (cx + w2 / 2, y + .74), (cx - w2 / 2, y + .74)], fc="#141a22", ec=c, lw=2))
            ax.text(cx, y + .37, "\n".join(textwrap.wrap(plain(s), int(w2 * 9))), ha="center", va="center", fontsize=10.2, color=FG)
    else: raise ValueError(kind)
    fig.savefig(path, dpi=100, facecolor=BG); plt.close(fig)
