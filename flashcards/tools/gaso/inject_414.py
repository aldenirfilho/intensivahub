"""Atualiza um app 4.13.0 para 4.14.0: motor (VM/venosa), aba 🧪 Gaso (analisador ampliado), Jornada com 📆 desafios semanais e CSS.
Uso: python3 inject_414.py <APP_DIR>   (aborta se já estiver em 4.14.0)"""
import sys, os, re
APP = sys.argv[1]; HERE = os.path.dirname(os.path.abspath(__file__))
js = open(os.path.join(APP, "app.js"), encoding="utf-8").read()
assert 'APP_VERSION = "4.13.0"' in js, "esperado app 4.13.0"
def rep(old, new, cnt=1):
    global js
    assert js.count(old) == cnt, (old[:80], js.count(old)); js = js.replace(old, new)
eng = open(os.path.join(HERE, "gaso_engine.js"), encoding="utf-8").read().replace('if (typeof module !== "undefined") module.exports = GASO_ENG;\n', "").rstrip() + "\n"
gz = open(os.path.join(HERE, "gz_module.js"), encoding="utf-8").read().rstrip() + "\n\n"
jb = open(os.path.join(HERE, "jornada_block.js"), encoding="utf-8").read().rstrip() + "\n"
a = js.index("/* ---------------- 🧪 Motor ácido-base"); b = js.index("/* ---------------- Micropartículas (TEMI / R3)")
js = js[:a] + "/* ---------------- 🧪 Motor ácido-base (espelho do gaso_engine.py; paridade testada: 4.000 casos + 3.000 extras de VM/venosa) ---------------- */\n" + eng + gz + js[b:]
a = js.index("function jStats() {"); b = js.index("\n\n/* ---------------- Mapa de domínio")
js = js[:a] + jb + js[b:]
rep('h: ["🕊️ Honra", "#c9b6ff"], g: ["🧪 Gasometria", "#ff9d5c"], a: ["🏆 Conquistas", "#e8c56a"] };', 'h: ["🕊️ Honra", "#c9b6ff"], g: ["🧪 Gasometria", "#ff9d5c"], d: ["📆 Desafios", "#7fe0ff"], a: ["🏆 Conquistas", "#e8c56a"] };')
rep('} else if (k === "_tt") { const c = out._tt; out._tt = rv && (!c || (rv.t || 0) > (c.t || 0)) ? rv : c;', '} else if (k === "_tt" || k === "_wl") { const c = out[k]; out[k] = rv && (!c || (rv.t || 0) > (c.t || 0)) ? rv : c;')
rep('$("#metaHome").innerHTML = metaBarHTML(false);', '$("#metaHome").innerHTML = metaBarHTML(false) + WC.mini();')
rep('const APP_VERSION = "4.13.0";', 'const APP_VERSION = "4.14.0";')
open(os.path.join(APP, "app.js"), "w", encoding="utf-8").write(js)
h = open(os.path.join(APP, "index.html"), encoding="utf-8").read()
a = h.index("/* 4.13.0 · 🧪 Gasometria + Jornada expandida */")
END = "@media(max-width:700px){.catGrid,.gzForms{grid-template-columns:1fr}.gzForm{grid-template-columns:repeat(2,minmax(0,1fr))}}\n"
b = h.index(END, a) + len(END)   # substitui só o bloco da 4.13 (o CSS do zoom e o resto ficam intactos)
css = open(os.path.join(HERE, "gaso_413.css"), encoding="utf-8").read()
h = h[:a] + (css if css.endswith("\n") else css + "\n") + h[b:]
open(os.path.join(APP, "index.html"), "w", encoding="utf-8").write(h)
print("ok", len(js))
