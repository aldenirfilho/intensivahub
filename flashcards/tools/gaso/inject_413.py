"""Injeta a aba 🧪 Gasometria + Jornada 4.13.0 no app.js e index.html de uma cópia do app.
Uso: python3 inject_413.py <APP_DIR>   (idempotente: aborta se já injetado)"""
import sys, os, re

APP = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
js = open(os.path.join(APP, "app.js"), encoding="utf-8").read()
if "const GZ = {" in js:
    sys.exit("já injetado")


def rep(old, new, cnt=1):
    global js
    n = js.count(old)
    assert n == cnt, (old[:80], n)
    js = js.replace(old, new)


eng = open(os.path.join(HERE, "gaso_engine.js"), encoding="utf-8").read().replace("if (typeof module !== \"undefined\") module.exports = GASO_ENG;\n", "").rstrip() + "\n"
gz = open(os.path.join(HERE, "gz_module.js"), encoding="utf-8").read().rstrip() + "\n\n"
jb = open(os.path.join(HERE, "jornada_block.js"), encoding="utf-8").read().rstrip() + "\n"

# 1) motor + módulo GZ antes das micropartículas
rep("/* ---------------- Micropartículas (TEMI / R3) ---------------- */",
    "/* ---------------- 🧪 Motor ácido-base (espelho do gaso_engine.py; paridade testada em 4.000 casos) ---------------- */\n" + eng + gz +
    "/* ---------------- Micropartículas (TEMI / R3) ---------------- */")

# 2) Jornada: substitui jStats/ACH/JR
a = js.index("function jStats() {")
b = js.index("\n\n/* ---------------- Mapa de domínio")
js = js[:a] + jb + js[b:]

# 3) fontes de XP, divisões de questões, rótulo do bloco
rep('h: ["🕊️ Honra", "#c9b6ff"], a: ["🏆 Conquistas", "#e8c56a"] };',
    'h: ["🕊️ Honra", "#c9b6ff"], g: ["🧪 Gasometria", "#ff9d5c"], a: ["🏆 Conquistas", "#e8c56a"] };')
rep('const DIVS = { temi: "🏛️ TEMI 2028", r3: "🩺 R3 Clínica Médica" };',
    'const DIVS = { temi: "🏛️ TEMI 2028", r3: "🩺 R3 Clínica Médica", gaso: "🧪 Gasometria" };\nconst DIVS_CURTO = { temi: "TEMI", r3: "R3", gaso: "Gasometria" };')
rep('.catch(() => ({ temi: [], r3: [] })); },', '.catch(() => ({ temi: [], r3: [], gaso: [] })); },')
rep('deck: `Questões ${this.div === "temi" ? "TEMI" : "R3"}${this.tema', 'deck: `Questões ${DIVS_CURTO[this.div] || this.div}${this.tema')
rep('async open() { await this.load(); this.block ? this.show() : this.home(); },',
    'async open() { await this.load(); if (!DIVS[this.div]) this.div = "temi"; this.block ? this.show() : this.home(); },')

# 4) mapa de domínio: todas as divisões
rep('data = QZ.data || { temi: [], r3: [] };', 'data = QZ.data || { temi: [], r3: [], gaso: [] };')
rep('for (const div of ["temi", "r3"]) {', 'for (const div of Object.keys(DIVS)) {')
rep('fonte: div === "temi" ? "❓ TEMI" : "❓ R3", div,', 'fonte: "❓ " + (DIVS_CURTO[div] || div), div,')

# 5) histograma de horário (estilo de estudo)
rep('L.qN = (L.qN || 0) + 1;\n', 'L.qN = (L.qN || 0) + 1; GZ.hr(L);\n')
rep('L.nAns++; if (g > 1) L.nOk++;', 'L.nAns++; if (g > 1) L.nOk++; GZ.hr(L);')

# 6) título ativo: vence a escolha mais recente
rep('    } else out[k] = mergeDay(out[k], rv);\n  }\n  return out;\n}',
    '    } else if (k === "_tt") { const c = out._tt; out._tt = rv && (!c || (rv.t || 0) > (c.t || 0)) ? rv : c;\n    } else out[k] = mergeDay(out[k], rv);\n  }\n  return out;\n}')

# 7) rota
rep('"honra", "jornada", "buscar"', '"honra", "gaso", "jornada", "buscar"')
rep('  if (view === "honra") HO.open();\n', '  if (view === "honra") HO.open();\n  if (view === "gaso") GZ.open();\n')

# 8) versão
rep('const APP_VERSION = "4.12.0";', 'const APP_VERSION = "4.13.0";')
open(os.path.join(APP, "app.js"), "w", encoding="utf-8").write(js)

# ---------------- index.html ----------------
h = open(os.path.join(APP, "index.html"), encoding="utf-8").read()
m = re.search(r'(\s*)<a href="#questoes" data-v="questoes">[^<]*</a>', h)
assert m, "nav questoes"
h = h[:m.end()] + m.group(1) + '<a href="#gaso" data-v="gaso">🧪 Gaso</a>' + h[m.end():]
m = re.search(r'(\s*)<section class="view" id="v-jornada">', h)
assert m, "sec jornada"
h = h[:m.start()] + m.group(1) + '<section class="view" id="v-gaso"><div id="gzHost"></div></section>' + h[m.start():]
CSS = open(os.path.join(HERE, "gaso_413.css"), encoding="utf-8").read()
assert "/*LIGHT-START*/" in h
i = h.index("/*LIGHT-START*/")
h = h[:i] + CSS + h[i:]
open(os.path.join(APP, "index.html"), "w", encoding="utf-8").write(h)
print("ok", len(js))
