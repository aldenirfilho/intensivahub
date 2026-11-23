#!/usr/bin/env python3
"""Injeta os 📕🗒️💉 Cadernos 360X (4.25.0) sobre o app 4.24.0.
Uso: python3 tools/cad/inject_425.py <APP_DIR>   (depois: python3 tools/theme/build_light.py index.html)
ALDENIR ROCHA DE OLIVEIRA FILHO · PROJETO 360X"""
import sys, os
D = sys.argv[1] if len(sys.argv) > 1 else "."
here = os.path.dirname(os.path.abspath(__file__))
app, idx = os.path.join(D, "app.js"), os.path.join(D, "index.html")
s = open(app, encoding="utf-8").read()
if "const CAD = {" in s:
    sys.exit("já injetado")

def R(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (a[:80], c)
    s = s.replace(a, b)

R('const APP_VERSION = "4.24.0";', 'const APP_VERSION = "4.25.0";')
R('gf: "📐 Fórmulas" },', 'gf: "📐 Fórmulas", p: "💉 Prescrições" },')
R(': "marque de 1 a 5 · +1 a +5 XP"}</span></div>`;', ': "marque de 1 a 5 · +1 a +5 XP"}</span>${CE.btn(k, short)}</div>`;')
R('''    } else if (k === "_hu") {   // itens próprios da aba Honra: vence o mod mais recente (inclui exclusões)
      const o = Object.assign({}, out._hu || {});
      for (const [id, e] of Object.entries(rv || {})) { if (!e || typeof e !== "object") continue; const c = o[id]; if (!c || (e.mod || 0) > (c.mod || 0)) o[id] = e; }
      out._hu = o;''', '''    } else if (k === "_hu" || k === "_ce" || k === "_nb" || k === "_px") {   // Honra (meus) e 📕🗒️💉 cadernos (4.25.0): vence o mod mais recente de cada item (inclui exclusões)
      const o = Object.assign({}, out[k] || {});
      for (const [id, e] of Object.entries(rv || {})) { if (!e || typeof e !== "object") continue; const c = o[id]; if (!c || (e.mod || 0) > (c.mod || 0)) o[id] = e; }
      out[k] = o;''')
R('    if (ok) this.ok++;\n', '    if (ok) this.ok++; else CE.auto("q:" + q.id);   // 📕 4.25.0: questão errada entra no caderno (desligável)\n')
R('  c.srs = schedule(c.srs, g);\n', '  c.srs = schedule(c.srs, g); if (g === 1 && !Study.sim) CE.auto("c:" + c.id);   // 📕 4.25.0: "De novo" → caderno (se ligado)\n')
R('a: ["🏆 Conquistas", "#e8c56a"] };', 'a: ["🏆 Conquistas", "#e8c56a"], e: ["📕 Cadernos", "#e8a87c"] };')
R('"gaso", "foco", "jornada", "buscar", "importar", "prompt", "ajustes"], view = valid.includes(v) ? v : "inicio";',
  '"gaso", "foco", "jornada", "buscar", "importar", "prompt", "ajustes", "erros", "notas", "prescricoes"], view = valid.includes(v) ? v : "inicio";')
R('  if (view === "foco") FO.open();\n', '  if (view === "foco") FO.open();\n  if (view === "erros") CE.open();\n  if (view === "notas") NB.open();\n  if (view === "prescricoes") PX.open();\n')
R('$("#metaHome").innerHTML = metaBarHTML(false) + WC.mini();', '$("#metaHome").innerHTML = metaBarHTML(false) + WC.mini() + CAD.homeStrip(); CAD.bindHome();')
R('''    A("qi80", "titulo", "🩻", "Leitor de Imagens",''', '''    /* ---------- 4.25.0: 📕🗒️💉 cadernos ---------- */
    [[10, "medalha", "📕", "Escriba dos Erros I"], [50, "trofeu", "📕", "Escriba dos Erros II"], [200, "brasao", "📚", "Arquivista dos Erros"]].forEach(([n, t, ic, nm]) => A("ce" + n, t, ic, nm, `Ter ${n} itens no 📕 Caderno de Erros (ativos + dominados)`, () => CAD.st().ceA, n, "cat"));
    [[10, "medalha", "✅", "Erro Vencido I"], [50, "trofeu", "🗡️", "Erro Vencido II"], [150, "brasao", "🐉", "Matador de Erros"]].forEach(([n, t, ic, nm]) => A("ced" + n, t, ic, nm, `Dominar ${n} itens do 📕 Caderno de Erros`, () => CAD.st().ceD, n, "des"));
    [[10, "medalha", "🗒️", "Memória Externa I"], [50, "trofeu", "🗒️", "Memória Externa II"]].forEach(([n, t, ic, nm]) => A("nb" + n, t, ic, nm, `Escrever ${n} notas no 🗒️ Caderno de Notas`, () => CAD.st().nbN, n, "est"));
    [[30, "medalha", "🔔", "Lembrei!"], [200, "trofeu", "🔔", "Guardião dos Detalhes"]].forEach(([n, t, ic, nm]) => A("nbr" + n, t, ic, nm, `Relembrar ${n} vezes as notas com 🔔`, () => CAD.st().nbR, n, "ass"));
    [[25, "medalha", "💉", "Prescritor Aprendiz"], [100, "trofeu", "💉", "Prescritor Cavaleiro"], [250, "brasao", "⚕️", "Prescritor Mestre"]].forEach(([n, t, ic, nm]) => A("px" + n, t, ic, nm, `Estudar ${n} modelos do 💉 Caderno de Prescrições`, () => CAD.st().pxV, n, "cat"));
    A("px500", "titulo", "℞", "Senhor das Prescrições", "Estudar os 500 modelos do 💉 Caderno de Prescrições", () => CAD.st().pxV, 500, "tit");
    A("qi80", "titulo", "🩻", "Leitor de Imagens",''')
mod = open(os.path.join(here, "cad_module.js"), encoding="utf-8").read()
R('/* ---------------- Roteamento ---------------- */', mod.rstrip() + '\n$("#ceHdr").addEventListener("mousedown", e => e.preventDefault()); $("#ceHdr").addEventListener("click", () => CE.capture());\n\n/* ---------------- Roteamento ---------------- */')
open(app, "w", encoding="utf-8").write(s)

h = open(idx, encoding="utf-8").read()
def H(a, b):
    global h
    assert h.count(a) == 1, (a[:60], h.count(a))
    h = h.replace(a, b)
H('  <button class="btn sm vozHdr" id="vozBtn"', '  <button class="btn sm" id="ceHdr" title="📕 Salvar o trecho ou a tabela selecionada no Caderno de Erros (sem seleção: abre o caderno)" aria-label="Salvar trecho no caderno de erros">📕</button>\n  <button class="btn sm vozHdr" id="vozBtn"')
H('  <a href="#gaso" data-v="gaso">🧪 Gaso</a>\n', '  <a href="#prescricoes" data-v="prescricoes">💉 Prescrições</a>\n  <a href="#gaso" data-v="gaso">🧪 Gaso</a>\n')
H('  <a href="#honra" data-v="honra">🕊️ Honra</a>\n', '  <a href="#erros" data-v="erros">📕 Erros</a>\n  <a href="#notas" data-v="notas">🗒️ Notas</a>\n  <a href="#honra" data-v="honra">🕊️ Honra</a>\n')
H('<section class="view" id="v-foco"><div id="foHost"></div></section>', '<section class="view" id="v-foco"><div id="foHost"></div></section>\n<!-- 📕🗒️💉 CADERNOS 360X (4.25.0) · ALDENIR ROCHA DE OLIVEIRA FILHO · PROJETO 360X -->\n<section class="view" id="v-erros"><div id="ceHost"></div></section>\n<section class="view" id="v-notas"><div id="nbHost"></div></section>\n<section class="view" id="v-prescricoes"><div id="pxHost"></div></section>')
css = open(os.path.join(here, "cad_425.css"), encoding="utf-8").read().strip()
H('/*LIGHT-START*/', css + '\n/*LIGHT-START*/') if '/*LIGHT-START*/' in h else None
open(idx, "w", encoding="utf-8").write(h)
print("ok: app.js 4.25.0 + index.html (abas, botão 📕, CSS)")
