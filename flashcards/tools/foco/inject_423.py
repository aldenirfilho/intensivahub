#!/usr/bin/env python3
"""Injeta a 4.23.0 no app.js e no index.html:
  🎧 AMB — som de estudo (ruído rosa/branco/marrom, chuva, mar) ligado ao ⏳ Foco, com comparação N-de-1;
  ❓ filtro 🆕 Lote nov/2026 nas Questões (QT601–QT900 e QR601–QR900, campo "lote").
Uso: python3 tools/foco/inject_423.py <APP_DIR>   (depois: python3 tools/theme/build_light.py index.html)
Idempotente: recusa rodar duas vezes (procura o marcador AMB)."""
import sys, pathlib

APP = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
HERE = pathlib.Path(__file__).parent
js, html = (APP / "app.js").read_text(), (APP / "index.html").read_text()
assert "const AMB = {" not in js, "já injetado"


def rep(s, old, new, n=1):
    c = s.count(old)
    assert c == n, (old[:90], c)
    return s.replace(old, new)


mod = (HERE / "amb_module.js").read_text()
css = (HERE / "amb_423.css").read_text()

# 1) versão
js = rep(js, 'const APP_VERSION = "4.22.0";', 'const APP_VERSION = "4.23.0";')
# 2) módulo AMB logo antes do roteamento (depois do FO)
js = rep(js, "/* ---------------- Roteamento ---------------- */", mod.rstrip() + "\n\n/* ---------------- Roteamento ---------------- */")
# 3) FO: subaba 🎧 Sons
js = rep(js, '["nota", "🗒️ Estacionamento"], ["met", "📘 Método"]]', '["nota", "🗒️ Estacionamento"], ["som", "🎧 Sons"], ["met", "📘 Método"]]')
js = rep(js, 'else if (this.sub === "met") body = this.vMet();', 'else if (this.sub === "met") body = this.vMet(); else if (this.sub === "som") body = AMB.vSom();')
# 4) FO: painel de som no preparo do bloco e controle compacto durante o bloco
js = rep(js, '     <div class="panel foCard"><h3>⚙️ Durante o bloco</h3>', '     ${AMB.panel()}\n     <div class="panel foCard"><h3>⚙️ Durante o bloco</h3>')
js = rep(js, '''<button class="btn sm ${this.conf ? "red" : ""}" data-fo="parar">${this.conf ? "⚠️ Toque de novo para encerrar" : "🛑 Encerrar"}</button></div></div></div>\n     <p class="metaNow">🔁''',
         '''<button class="btn sm ${this.conf ? "red" : ""}" data-fo="parar">${this.conf ? "⚠️ Toque de novo para encerrar" : "🛑 Encerrar"}</button></div>${AMB.mini()}</div></div>\n     <p class="metaNow">🔁''')
# 5) FO: som automático no início/fim do bloco e registro do som usado (para a comparação N-de-1)
js = rep(js, '    this.beep("ini"); this.lock(); this.save();', '    this.beep("ini"); this.lock(); AMB.blockStart(); this.save();')
js = rep(js, "el: this.m1(T.el), min: this.m1(T.no), dv: r.dv, rt: r.rt, ck: r.ck, pzN: r.pzN, q: 0, cs: [] };",
         'el: this.m1(T.el), min: this.m1(T.no), dv: r.dv, rt: r.rt, ck: r.ck, pzN: r.pzN, q: 0, cs: [], amb: r.amb || "" };')
js = rep(js, 'lsSet("foEnd", JSON.stringify(this.end)); this.unlock();', 'lsSet("foEnd", JSON.stringify(this.end)); this.unlock(); AMB.blockEnd();')
js = rep(js, "done: e.done, cl, tr, rit: e.rit };", 'done: e.done, cl, tr, rit: e.rit, amb: e.amb || "" };')
# 6) FO: botão 🎧 na barra do topo durante o bloco
js = rep(js, 'aria-label="Estacionar um pensamento">🗒️</button>`);',
         'aria-label="Estacionar um pensamento">🗒️</button>`) + `<button class="btn sm ambBarB" data-amb="bar" title="Som de fundo" aria-label="Ligar ou desligar o som de fundo">${AMB.on ? "🎧" : "🔇"}</button>`;')
js = rep(js, '    if (a === "tog") return this.toggle();', '    if (a === "tog" || a === "bar") return this.toggle();')
# 7) Jornada: estatísticas e conquistas do som
js = rep(js, "foRt: fos.rt, foRun: fos.maxRun };",
         "foRt: fos.rt, foRun: fos.maxRun,\n    foAmb: fos.ss.filter(x => x.amb && x.cl).length, foN1: (n => Math.min(n.com ? n.com.n : 0, n.sem ? n.sem.n : 0))(AMB.n1()) };")
js = rep(js, "    /* ---------- 4.13.0: 🎭 estilo de comportamento ---------- */", '''    /* ---------- 4.23.0: 🎧 som de estudo ---------- */
    A("foamb5", "medalha", "🎧", "Trilha do Foco", "Fechar 5 blocos limpos com som de fundo", s => s.foAmb, 5, "est");
    A("fon1", "trofeu", "🔬", "Cientista de Si", "Fazer 3 blocos com som e 3 sem som (libera a comparação N-de-1 na aba 🎧 Sons)", s => s.foN1, 3, "des");
    /* ---------- 4.13.0: 🎭 estilo de comportamento ---------- */''')
# 8) inicialização
js = rep(js, "  FO.init();\n", "  FO.init();\n  AMB.init();\n")
# 9) Questões: filtro 🆕 Lote nov/2026
js = rep(js, "const lst = this.list(), pend = lst.filter(q => !R[q.id]).length,",
         "const lst = this.list(), lote = lst.filter(q => q.lote), lotN = lote.filter(q => !R[q.id]).length, pend = lst.filter(q => !R[q.id]).length,")
js = rep(js, '<button class="btn" data-st="all">📚 Todas em ordem (${lst.length})</button></div>',
         '<button class="btn" data-st="all">📚 Todas em ordem (${lst.length})</button>${lote.length ? `<button class="btn" data-st="lote" title="Questões ${lote[0].id.slice(0, 2)}601–${lote[0].id.slice(0, 2)}900, novas na 4.23.0">🆕 Lote nov/2026 · ${lotN} inéditas de ${lote.length}</button>` : ""}</div>')
js = rep(js, ': k === "cf" ? sh(l.filter(q => CF.low("q:" + q.id))) :',
         ': k === "cf" ? sh(l.filter(q => CF.low("q:" + q.id))) : k === "lote" ? fresh.filter(q => q.lote).concat(old.filter(q => q.lote)).slice(0, 20) :')

html = rep(html, "</style>\n</head>", css.rstrip() + "\n</style>\n</head>")
(APP / "app.js").write_text(js)
(APP / "index.html").write_text(html)
print("4.23.0 injetado:", len(js), len(html))
