#!/usr/bin/env python3
"""Gera o CSS do tema claro (html.light) a partir do <style> do index.html.
- Variáveis de cor redefinidas à mão (paleta pergaminho + ouro + ciano escuro).
- Cores fixas (#hex) em background/border/color/box-shadow/outline/fill: luminosidade invertida, matiz mantido.
- Saída: bloco entre /*LIGHT-START*/ e /*LIGHT-END*/ (substituído a cada execução).
Uso: python3 tools/theme/build_light.py index.html"""
import re, sys, colorsys

VARS = ("html.light{--bg:#f4efe2;--bg2:#fffcf4;--panel:#ffffff;--line:#d9cfb6;--txt:#1d1a14;--mut:#5b6270;"
        "--gold:#a47b12;--gold2:#7c5a08;--cy:#0a6f93;--red:#b8322a;--grn:#17783f;--amb:#9a6200;color-scheme:light}")
MANUAL = """
html.light,html.light body{background:radial-gradient(1200px 600px at 50% -200px,#fff6dc 0%,var(--bg) 60%) fixed}
html.light .btn.gold{background:linear-gradient(90deg,#e6bf55,#f5da8a);color:#2b1f00}
html.light .brand h1{background:linear-gradient(90deg,#8a6208,#b8891c);-webkit-background-clip:text;background-clip:text}
html.light img.logo{filter:drop-shadow(0 1px 2px #0002)}
html.light .hoOrb span{color:#fff}html.light .hoOrb small{color:#eaf7ff}
html.light .hoOrb{background:radial-gradient(circle at 35% 35%,#9fe0ff,#4b3fae 60%,#2a2f5a);box-shadow:0 0 40px #0a6f9340}
html.light .hoBrasao{background:radial-gradient(#fff7df,#efe3c2)}
html.light .hoCenter{background:radial-gradient(#fffaf0,#f1e7cf)}
html.light .hoHero{background:linear-gradient(135deg,#fbf3df,#eef6fb)}
html.light ::selection{background:#f5da8a}
html.light header{background:rgba(255,251,240,.94)}
html.light .bar{background:rgba(255,251,240,.97)}
html.light #hlBar{background:rgba(255,251,240,.98)}
"""
SKIP_COLOR = {"#14100a", "#fff", "#ffffff"}   # textos escuros sobre ouro e brancos sobre fundos fortes

def hex2rgb(h):
    h = h.lstrip("#"); a = ""
    if len(h) in (3, 4): h = "".join(c * 2 for c in h)
    if len(h) == 8: h, a = h[:6], h[6:]
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)), a

def flip(hx):
    (r, g, b), a = hex2rgb(hx)
    hh, l, s = colorsys.rgb_to_hls(r, g, b)
    l2 = 1 - l
    if l < 0.5: l2 = min(0.985, 0.90 + (0.5 - l) * 0.18)   # fundos escuros → claros quentes
    else: l2 = max(0.16, 1 - l - 0.08)                      # textos/claros → escuros
    if s > 0.35 and l >= 0.5: l2 = max(l2, 0.30)            # acentos vivos não viram quase-preto
    r2, g2, b2 = colorsys.hls_to_rgb(hh, l2, min(1, s * (0.9 if l < 0.5 else 1)))
    return "#%02x%02x%02x%s" % (round(r2 * 255), round(g2 * 255), round(b2 * 255), a)

PROPS = re.compile(r"^(background(-color)?|border(-[a-z]+)*|color|box-shadow|outline(-color)?|fill|stroke|text-shadow|accent-color)$")

def css_rules(css):
    """Regras de nível superior e dentro de @media (preserva o @media)."""
    out, i = [], 0
    while i < len(css):
        m = re.compile(r"([^{}]+)\{").search(css, i)
        if not m: break
        sel = m.group(1).strip(); j = m.end()
        if sel.startswith("@media"):
            depth, k = 1, j
            while depth and k < len(css):
                depth += {"{": 1, "}": -1}.get(css[k], 0); k += 1
            for s2, d2 in css_rules(css[j:k - 1]): out.append((sel + "||" + s2, d2))
            i = k; continue
        if sel.startswith("@"):
            k = css.find("}", j); i = k + 1; continue
        k = css.find("}", j); out.append((sel, css[j:k])); i = k + 1
    return out

def build(css):
    lines = []
    for sel, decls in css_rules(css):
        if "html.light" in sel or ":root" in sel: continue
        media = None
        if "||" in sel: media, sel = sel.split("||", 1)
        new = []
        for d in decls.split(";"):
            if ":" not in d: continue
            p, v = d.split(":", 1); p = p.strip()
            if not PROPS.match(p) or "#" not in v or "var(" in v and not re.search(r"#[0-9a-fA-F]{3,8}", v): continue
            if p == "color" and v.strip().lower() in SKIP_COLOR: continue
            v2 = re.sub(r"#[0-9a-fA-F]{8}\b|#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3,4}\b", lambda m: m.group(0) if m.group(0).lower() in SKIP_COLOR and p != "color" else flip(m.group(0)), v)
            if v2 != v: new.append(f"{p}:{v2.strip()}")
        if not new: continue
        sels = ",".join("html.light " + s.strip() if not s.strip().startswith("html") else s.strip().replace("html.", "html.light.", 1) for s in sel.split(","))
        rule = f"{sels}{{{';'.join(new)}}}"
        lines.append(f"{media}{{{rule}}}" if media else rule)
    return VARS + "\n" + MANUAL.strip() + "\n" + "\n".join(lines)

if __name__ == "__main__":
    p = sys.argv[1]; s = open(p, encoding="utf-8").read()
    s = re.sub(r"\n?/\*LIGHT-START\*/.*?/\*LIGHT-END\*/", "", s, flags=re.S)
    a, b = s.index("<style>") + 7, s.index("</style>")
    light = build(s[a:b])
    s = s[:b] + "\n/*LIGHT-START*/\n" + light + "\n/*LIGHT-END*/\n" + s[b:]
    open(p, "w", encoding="utf-8").write(s)
    print("regras do tema claro:", light.count("{"))
