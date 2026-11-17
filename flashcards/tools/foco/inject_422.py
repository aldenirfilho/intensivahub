#!/usr/bin/env python3
"""Injeta o módulo ⏳ Foco 360X (4.22.0) no app.js e no index.html.
Uso: python3 tools/foco/inject_422.py <APP_DIR>   (depois: python3 tools/theme/build_light.py index.html)
Idempotente: recusa rodar duas vezes (procura o marcador FO)."""
import sys, pathlib

APP = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
HERE = pathlib.Path(__file__).parent
js, html = (APP / "app.js").read_text(), (APP / "index.html").read_text()
assert "const FO = {" not in js, "já injetado"


def rep(s, old, new, n=1):
    c = s.count(old)
    assert c == n, (old[:80], c)
    return s.replace(old, new)


mod = (HERE / "fo_module.js").read_text()
css = (HERE / "fo_422.css").read_text()

# 1) versão
js = rep(js, 'const APP_VERSION = "4.21.0";', 'const APP_VERSION = "4.22.0";')
# 2) módulo antes do roteamento
js = rep(js, "/* ---------------- Roteamento ---------------- */", mod.rstrip() + "\n\n/* ---------------- Roteamento ---------------- */")
# 3) rota, abertura e âncora de tema
js = rep(js, '"auditoria", "inexoravel", "gaso", "jornada"', '"auditoria", "inexoravel", "gaso", "foco", "jornada"')
js = rep(js, '  if (view === "gaso") GZ.open();\n', '  if (view === "gaso") GZ.open();\n  if (view === "foco") FO.open();\n  FO.route(view);\n')
# 4) fonte de XP
js = rep(js, 'f: ["🎯 Confiança", "#ffd166"], a: ["🏆 Conquistas", "#e8c56a"] };', 'f: ["🎯 Confiança", "#ffd166"], o: ["⏳ Foco", "#9be7c4"], a: ["🏆 Conquistas", "#e8c56a"] };')
# 5) mescla dos logs entre aparelhos
js = rep(js, '    } else if (k === "_tt" || k === "_wl") {', '''    } else if (k === "_fo") {   // ⏳ foco (4.22.0): sessões e estacionamento por id (união); ponto de partida pelo mais recente
      const c = out._fo || {}, r = rv || {}, o = Object.assign({}, c);
      o.s = Object.assign({}, c.s || {}, r.s || {}); o.p = mergeDay(c.p || null, r.p || null) || {};
      const b1 = c.b, b2 = r.b; o.b = b2 && (!b1 || (b2.t || 0) > (b1.t || 0)) ? b2 : b1; if (!o.b) delete o.b;
      out._fo = o;
    } else if (k === "_tt" || k === "_wl") {''')
# 6) estatísticas da Jornada
js = rep(js, "(l.hn || 0) + (l.gS || 0) + (l.gA || 0) + (l.sims || []).length > 0;", "(l.hn || 0) + (l.gS || 0) + (l.gA || 0) + (l.foN || 0) + (l.sims || []).length > 0;")
js = rep(js, "wcN: wcd.n, wcAll: wcd.all, cfN: cfs.n, cf5: cfs.top, cfLow: cfs.low };",
         "wcN: wcd.n, wcAll: wcd.all, cfN: cfs.n, cf5: cfs.top, cfLow: cfs.low,\n    foN: fos.n, foM: fos.min, foZ: fos.z25, foAvg: fos.l7 >= 7 ? Math.floor(fos.avg7) : 0, foDeg: fos.top, foRt: fos.rt, foRun: fos.maxRun };")
js = rep(js, "wcd = WC.done(), cfs = CF.stats();", "wcd = WC.done(), cfs = CF.stats(), fos = FO.stats();")
# 7) conquistas
js = rep(js, "    /* ---------- 4.13.0: 🎭 estilo de comportamento ---------- */", '''    /* ---------- 4.22.0: ⏳ Foco 360X ---------- */
    A("fo1", "medalha", "⏳", "Primeira Âncora", "Concluir 1 bloco na aba ⏳ Foco", s => s.foN, 1, "est");
    [[60, "medalha", "🕐", "Hora Focada"], [300, "trofeu", "🗡️", "Cinco Horas de Lâmina"], [1500, "brasao", "🧘", "Monge do Foco"], [6000, "honra", "🦉", "Mestre da Atenção"]]
      .forEach(([n, t, ic, nm]) => A("fom" + n, t, ic, nm, `Somar ${n.toLocaleString("pt-BR")} minutos no tema em blocos de foco`, s => s.foM, n, "est"));
    [[1, "trofeu", "🎯", "Zona 25"], [10, "brasao", "🛡️", "Guardião dos 25"], [50, "honra", "👑", "Senhor dos 25"]]
      .forEach(([n, t, ic, nm]) => A("foz" + n, t, ic, nm, `Fechar ${n} sessão(ões) limpa(s) de 25 min ou mais`, s => s.foZ, n, "des"));
    A("foavg25", "titulo", "🏹", "Foco Pleno 25", "Média de 25 min no tema nas últimas 7 sessões de foco", s => s.foAvg, 25, "tit");
    A("fodeg25", "titulo", "🪜", "Escalador da Atenção", "Chegar ao último degrau da escada do foco (25 min)", s => s.foDeg, 25, "tit");
    [[25, "medalha"], [100, "trofeu"], [400, "brasao"]].forEach(([n, t]) => A("fort" + n, t, "🔁", `Arte de Voltar ${n}`, `Perceber a divagação e voltar ao tema ${n} vezes (😵 voltei ou 🧭 checagem)`, s => s.foRt, n, "est"));
    [[3, "medalha", "🔥", "Três Dias de Foco"], [7, "trofeu", "📿", "Semana Focada"], [30, "brasao", "🏯", "Mês de Atenção"]]
      .forEach(([n, t, ic, nm]) => A("fod" + n, t, ic, nm, `Fazer ao menos 1 bloco de foco em ${n} dias seguidos`, s => s.foRun, n, "ass"));
    /* ---------- 4.13.0: 🎭 estilo de comportamento ---------- */''')
# 8) inicialização
js = rep(js, "  HL.init();\n  Cloud.init();", "  HL.init();\n  FO.init();\n  Cloud.init();")

# index.html: aba, seção e CSS
html = rep(html, '  <a href="#estudar" data-v="estudar">🎴 Estudar</a>\n', '  <a href="#estudar" data-v="estudar">🎴 Estudar</a>\n  <a href="#foco" data-v="foco">⏳ Foco</a>\n')
html = rep(html, '<section class="view" id="v-gaso"><div id="gzHost"></div></section>', '<section class="view" id="v-gaso"><div id="gzHost"></div></section>\n<section class="view" id="v-foco"><div id="foHost"></div></section>')
html = rep(html, "</style>\n</head>", css.rstrip() + "\n</style>\n</head>")

(APP / "app.js").write_text(js)
(APP / "index.html").write_text(html)
print("4.22.0 injetado:", len(js), len(html))
