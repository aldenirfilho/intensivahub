#!/usr/bin/env python3
"""☑️ Códice 360X 4.26.0 — encaixa a checagem dos itens dos mnemônicos (MNCK) em app.js e index.html.
Uso: python3 tools/mn/inject_426.py <APP_DIR>   e depois   python3 tools/theme/build_light.py index.html
Recusa rodar duas vezes (procura "const MNCK = {").
ALDENIR ROCHA DE OLIVEIRA FILHO · PROJETO 360X"""
import sys, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
D = sys.argv[1] if len(sys.argv) > 1 else "."
AJ, IH = os.path.join(D, "app.js"), os.path.join(D, "index.html")
js, html = open(AJ, encoding="utf-8").read(), open(IH, encoding="utf-8").read()
if "const MNCK = {" in js: sys.exit("já injetado (const MNCK = { encontrado)")

def rep(s, a, b, n=1, what=""):
    c = s.count(a)
    if c != n: sys.exit(f"✗ {what or a[:70]!r}: esperado {n}, achei {c}")
    return s.replace(a, b)

js, k = re.subn(r'const APP_VERSION = "[^"]+";', 'const APP_VERSION = "4.26.0";', js, count=1); assert k == 1
js = rep(js, 'k === "_hu" || k === "_ce" || k === "_nb" || k === "_px") {', 'k === "_hu" || k === "_ce" || k === "_nb" || k === "_px" || k === "_nc") {   /* ☑️ _nc: checagem dos mnemônicos (4.26.0) */', what="mergeLogs")
# filtros da lista
js = rep(js, '(f === "cf0" && !CF.val("n:" + m.id)))', '(f === "cf0" && !CF.val("n:" + m.id)) || (f === "ck" && MNCK.st(m) === 2) || (f === "ckp" && MNCK.st(m) === 1) || (f === "ck0" && !MNCK.st(m)))', what="MN.list filtros")
# corpo: caixinha em cada item quando ck
a = '''  body(m) {
    const wide = m.tp !== "a" && m.k.some(k => k[0].length > 6);
    return `<table class="mnTab${wide ? " wide" : ""}">${m.k.map(k => `<tr><td class="l">${esc(k[0])}</td><td>${esc(k[1])}</td></tr>`).join("")}</table>'''
b = '''  body(m, ck) {
    const wide = m.tp !== "a" && m.k.some(k => k[0].length > 6), a = ck ? MNCK.bits(m) : null;   /* ☑️ 4.26.0: ck = caixinha em cada item */
    return `<table class="mnTab${wide ? " wide" : ""}${ck ? " ck" : ""}">${m.k.map((k, i) => `<tr${ck && a[i] ? ' class="on"' : ""}>${ck ? MNCK.cell(m, i, a[i]) : ""}<td class="l">${esc(k[0])}</td><td>${esc(k[1])}</td></tr>`).join("")}</table>${ck ? MNCK.bar(m) : ""}'''
js = rep(js, a, b, what="MN.body")
js = rep(js, '<span class="mnTools">${this.orig(m)}<button class="mnImg" data-img="${m.id}" title="Gerar cartão-imagem" aria-label="Gerar cartão-imagem">🖼️</button><button class="mnFav"', '<span class="mnTools">${MNCK.chip(m)}${this.orig(m)}<button class="mnImg" data-img="${m.id}" title="Gerar cartão-imagem" aria-label="Gerar cartão-imagem">🖼️</button><button class="mnFav"', what="MN.card chip")
js = rep(js, '<div class="mnTit">${esc(m.t)}</div>${this.sig(m)}${this.body(m)}${this.foot(m)}', '<div class="mnTit">${esc(m.t)}</div>${this.sig(m)}${this.body(m, 1)}${this.foot(m)}', what="MN.card body")
# cabeçalho: modo Checklist, contador, filtros e busca
js = rep(js, '["cf", "🔴 Confiança baixa (1–2)"], ["cf0", "⬜ Confiança não marcada"]];', '["cf", "🔴 Confiança baixa (1–2)"], ["cf0", "⬜ Confiança não marcada"], ["ck", "☑️ Checados por inteiro"], ["ckp", "◐ Checagem em andamento"], ["ck0", "☐ Ainda não checados"]];', what="MN.head filtros")
js = rep(js, 'data-mode="treino">🎲 Treinar</button>\n      <span class="metaNow">🧠 Dominados: <b>${nDom}</b>/${all.length} · ⭐ ${nFav}',
         'data-mode="treino">🎲 Treinar</button><button class="btn ${this.mode === "check" ? "cy" : ""}" data-mode="check">☑️ Checklist</button>\n      <span class="metaNow">🧠 Dominados: <b>${nDom}</b>/${all.length} · ☑️ <b id="mnCkN">${MNCK.tot(all).full}</b> checados · ⭐ ${nFav}', what="MN.head modo")
js = rep(js, '${this.mode === "lista" ? `<input type="search" id="mnQ"', '${this.mode !== "treino" ? `<input type="search" id="mnQ"', what="MN.head busca")
js = rep(js, '    if (this.mode === "treino") { if (!this.cur || !this.list().some(m => m.id === this.cur.id)) this.pick(); host.innerHTML = this.head() + this.train(); }\n',
         '    if (this.mode === "treino") { if (!this.cur || !this.list().some(m => m.id === this.cur.id)) this.pick(); host.innerHTML = this.head() + this.train(); }\n    else if (this.mode === "check") host.innerHTML = this.head() + MNCK.view(this.list());   /* ☑️ 4.26.0 */\n', what="MN.render")
js = rep(js, '    const fi = $("#mnFavImg", host); if (fi) fi.onclick = () => CARDIMG.show(this.all().filter(m => this.fav(m.id)), "Favoritos " + DIVS[this.div]);\n',
         '    const fi = $("#mnFavImg", host); if (fi) fi.onclick = () => CARDIMG.show(this.all().filter(m => this.fav(m.id)), "Favoritos " + DIVS[this.div]);\n    MNCK.bind(host);   /* ☑️ 4.26.0 */\n', what="MN.bind")
# estatística e conquistas
js = rep(js, 'mn: Object.values(S.logs._n || {}).filter(e => e && (e.s || 0) >= 2).length,', 'mn: Object.values(S.logs._n || {}).filter(e => e && (e.s || 0) >= 2).length, nck: Object.values(S.logs._nc || {}).filter(e => e && e.c).length,', what="jStats")
a = '[[10, "medalha"], [50, "trofeu"], [150, "brasao"], [300, "honra"], [500, "honra"], [800, "honra"]].forEach(([n, t]) => A("mn" + n, t, "🧠", `Mnemonista ${n}`, `Dominar ${n} mnemônicos (2 acertos seguidos no treino)`, s => s.mn, n, "cat"));'
b = ('[[10, "medalha"], [50, "trofeu"], [150, "brasao"], [300, "honra"], [500, "honra"], [800, "honra"], [1000, "honra"]].forEach(([n, t]) => A("mn" + n, t, "🧠", `Mnemonista ${n}`, `Dominar ${n} mnemônicos (2 acertos seguidos no treino)`, s => s.mn, n, "cat"));\n'
     '    [[25, "medalha"], [100, "trofeu"], [300, "brasao"], [700, "honra"], [1100, "honra"]].forEach(([n, t]) => A("nck" + n, t, "☑️", `Checklista ${n}`, `Checar todos os itens de ${n} mnemônicos (modo ☑️ Checklist)`, s => s.nck, n, "cat"));   /* ☑️ 4.26.0 */')
js = rep(js, a, b, what="conquistas")
# módulo depois do MN (antes da Honra)
mod = open(os.path.join(HERE, "ck_426.js"), encoding="utf-8").read().rstrip() + "\n\n"
js = rep(js, "/* ---------------- 🕊️ Honra: guia espiritual, bússolas de decisão e fluxo ----------------", mod + "/* ---------------- 🕊️ Honra: guia espiritual, bússolas de decisão e fluxo ----------------", what="posição do módulo")
# CSS antes do tema claro
css = open(os.path.join(HERE, "ck_426.css"), encoding="utf-8").read().strip() + "\n"
html = rep(html, "/*LIGHT-START*/", css + "/*LIGHT-START*/", what="CSS")
open(AJ, "w", encoding="utf-8").write(js); open(IH, "w", encoding="utf-8").write(html)
print("✅ 4.26.0: checagem dos mnemônicos injetada (app.js + index.html)")
