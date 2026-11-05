"""Lê os módulos em texto (mod/*.txt) → temas no formato do dataset.
Formato:
  # NUM | EMOJI | Nome do tema | slug
  ## A | Nome do subtema | fonte padrão
  Q: pergunta
  A: resposta (várias linhas; '| a | b |' = tabela, 1ª linha cabeçalho; '- x' = lista)
  X: pegadinha / nerd     S: fonte     I: imagem.png
  (linha em branco separa cards)"""
import glob, re, html

def fmt(lines):
    out, tab, lst = [], [], []
    def flush():
        nonlocal tab, lst
        if tab:
            h = "<table class=t><tr>" + "".join(f"<th>{c}</th>" for c in tab[0]) + "</tr>" + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in tab[1:]) + "</table>"
            out.append(h); tab = []
        if lst: out.append("<ul>" + "".join(f"<li>{i}</li>" for i in lst) + "</ul>"); lst = []
    for ln in lines:
        s = ln.strip()
        if s.startswith("|") and s.endswith("|"):
            if lst: flush()
            tab.append([c.strip() for c in s[1:-1].split("|")])
        elif s.startswith("- "):
            if tab: flush()
            lst.append(s[2:])
        else:
            flush()
            if s: out.append(s)
    flush()
    res = ""
    for i, p in enumerate(out):
        if i and not p.startswith(("<table", "<ul")) and not out[i - 1].startswith(("<table", "<ul")): res += "<br>"
        res += p
    return res

def esc(s):  # protege < e > soltos (ex.: "< 30") sem quebrar tags que eu escrevo
    return re.sub(r"<(?!/?(b|i|u|br|sub|sup|span|small)\b)", "&lt;", s).replace(" > ", " &gt; ")

def load(path):
    themes = []
    for fn in sorted(glob.glob(path)):
        th = None; sub = None; cur = None; key = None
        def close():
            nonlocal cur
            if cur and cur.get("f"):
                c = dict(t=sub[0], f=fmt([esc(z) for z in cur["Q"]]), b=fmt([esc(z) for z in cur["A"]]), x=fmt([esc(z) for z in cur.get("X", [])]), s=" ".join(cur.get("S", [])).strip() or sub[2], i=" ".join(cur.get("I", [])).strip(), orig="v4")
                th["cards"].append(c)
            cur = None
        for raw in open(fn, encoding="utf-8").read().split("\n"):
            ln = raw.rstrip()
            if ln.startswith("# "):
                close(); p = [x.strip() for x in ln[2:].split("|")]
                if th is None or th["num"] != p[0]:
                    th = dict(num=p[0], emo=p[1], nome=p[2], slug=p[3], subs={}, cards=[]); themes.append(th)
                continue
            if ln.startswith("## "):
                close(); p = [x.strip() for x in ln[3:].split("|")]; sub = (p[0], p[1], p[2] if len(p) > 2 else ""); th["subs"][p[0]] = p[1]; continue
            m = re.match(r"^([QAXSI]):\s?(.*)$", ln)
            if m:
                if m.group(1) == "Q": close(); cur = {"f": True, "Q": [], "A": []}
                key = m.group(1); cur.setdefault(key, []).append(m.group(2)); continue
            if not ln.strip():
                if cur and key in ("A", "X"): cur[key].append("")
                continue
            if cur is not None and key: cur[key].append(ln)
        close()
    # mescla temas com mesmo número vindos de arquivos diferentes
    merged = {}
    for t in themes:
        if t["num"] in merged: merged[t["num"]]["subs"].update(t["subs"]); merged[t["num"]]["cards"] += t["cards"]
        else: merged[t["num"]] = t
    out = list(merged.values())
    for t in out:
        order = list(t["subs"]); t["cards"].sort(key=lambda c: order.index(c["t"]))
        for c in t["cards"]: c["sub"] = t["subs"][c["t"]]
    return out
