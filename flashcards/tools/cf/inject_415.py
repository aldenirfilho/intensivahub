#!/usr/bin/env python3
"""4.15.0 · 🎯 Confiança no domínio 1–5 em todas as abas (soma XP).
Aplica sobre a 4.14.0: módulo CF (tools/cf/cf_module.js), caixinha nos itens de cada aba, sincronização
(c.cf no progresso do card; S.logs._cf nos demais), fonte de XP 🎯, painel e conquistas na Jornada, filtros e CSS.
Uso: python3 tools/cf/inject_415.py   (rodar de dentro de flashcards/; depois: python3 tools/theme/build_light.py index.html)"""
import pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
APP, HTML = ROOT / "app.js", ROOT / "index.html"
MOD = (pathlib.Path(__file__).parent / "cf_module.js").read_text(encoding="utf-8")


def rep(src, old, new, label):
    n = src.count(old)
    if n != 1:
        sys.exit(f"❌ {label}: esperado 1 trecho, achei {n}")
    print(f"✅ {label}")
    return src.replace(old, new)


a = APP.read_text(encoding="utf-8")
if 'const APP_VERSION = "4.15.0"' in a:
    sys.exit("⚠️ app.js já está na 4.15.0 — nada a fazer")

a = rep(a, 'const APP_VERSION = "4.14.0";', 'const APP_VERSION = "4.15.0";', "versão 4.15.0")
# ---------- progresso do card leva a confiança (índice 11) ----------
a = rep(a, "p.mod, p.hl && p.hl.length ? p.hl : 0];", "p.mod, p.hl && p.hl.length ? p.hl : 0, Array.isArray(p.cf) ? p.cf : 0];", "encP com cf")
a = rep(a, "hl: Array.isArray(a[10]) ? a[10] : [] });", "hl: Array.isArray(a[10]) ? a[10] : [], cf: Array.isArray(a[11]) ? a[11] : null });", "decP com cf")
a = rep(a, "hl: p && p.hl ? p.hl : [] });", "hl: p && p.hl ? p.hl : [], cf: p && Array.isArray(p.cf) ? p.cf : null });", "card montado com cf")
a = rep(a, "hl: c.hl || [], mod: Date.now() };", "hl: c.hl || [], cf: Array.isArray(c.cf) ? c.cf : null, mod: Date.now() };", "saveProg grava cf")
# ---------- mescla dos logs: _cf pela marcação mais recente ----------
a = rep(a, '    } else if (k === "_tt" || k === "_wl") {',
        '    } else if (k === "_cf") {   // 🎯 confiança (4.15.0): por item, vence a marcação mais recente\n'
        '      const o = Object.assign({}, out._cf || {});\n'
        '      for (const [id, e] of Object.entries(rv || {})) { if (!Array.isArray(e)) continue; const c = o[id]; if (!Array.isArray(c) || (e[1] || 0) > (c[1] || 0)) o[id] = e; }\n'
        '      out._cf = o;\n'
        '    } else if (k === "_tt" || k === "_wl") {', "mergeLogs _cf")
# ---------- módulo ----------
a = rep(a, "/* ---------------- Questões (TEMI / R3) ---------------- */", MOD + "/* ---------------- Questões (TEMI / R3) ---------------- */", "módulo CF")
# ---------- ❓ Questões ----------
a = rep(a, "err = lst.filter(q => R[q.id] && !R[q.id][0]).length;", 'err = lst.filter(q => R[q.id] && !R[q.id][0]).length, low = lst.filter(q => CF.low("q:" + q.id)).length;', "questões: conta confiança baixa")
a = rep(a, '<button class="btn" data-st="err" ${err ? "" : "disabled"}>🔁 Só as erradas (${err})</button>',
        '<button class="btn" data-st="err" ${err ? "" : "disabled"}>🔁 Só as erradas (${err})</button><button class="btn" data-st="cf" ${low ? "" : "disabled"}>🔴 Confiança baixa (${low})</button>', "questões: botão confiança baixa")
a = rep(a, ': k === "err" ? sh(l.filter(q => R[q.id] && !R[q.id][0])) : fresh.concat(old)',
        ': k === "err" ? sh(l.filter(q => R[q.id] && !R[q.id][0])) : k === "cf" ? sh(l.filter(q => CF.low("q:" + q.id))) : fresh.concat(old)', "questões: bloco de confiança baixa")
a = rep(a, "✨ +15 XP por acerto, +5 por tentativa.</p>", "✨ +15 XP por acerto, +5 por tentativa · 🎯 confiança 1–5 depois de responder: +1 a +5 XP (<span class=\"kbd\">Shift</span>+<span class=\"kbd\">1</span>–<span class=\"kbd\">5</span>).</p>", "questões: legenda")
a = rep(a, '${q.ref ? `<div class="qzRef">📚 ${esc(q.ref)}</div>` : ""}', '${q.ref ? `<div class="qzRef">📚 ${esc(q.ref)}</div>` : ""}${CF.box("q:" + q.id, { pri: 1 })}', "questões: caixinha no comentário")
# ---------- 🧪 Gaso ----------
a = rep(a, "${c.peg}</div></div>", '${c.peg}</div></div>${CF.box("g:" + c.n, { pri: 1 })}', "gaso: caixinha no fim do caso")
a = rep(a, '<div class="gzF"><b>${t}</b><span>${d}</span></div>', '<div class="gzF"><b>${t}</b><span>${d}</span>${CF.box("gf:" + CF.slug(t), { sm: 1 })}</div>', "gaso: caixinha nas fórmulas")
# ---------- 💊 Micro ----------
a = rep(a, '(+${m.comentario ? 3 : 2} XP)</button>`}</div></div>', '(+${m.comentario ? 3 : 2} XP)</button>`}</div>${CF.box("m:" + m.id, { pri: 1 })}</div>', "micro: caixinha")
# ---------- 🧠 Mnemônicos ----------
a = rep(a, '<div class="mnTit">${esc(m.t)}</div>${this.sig(m)}${this.body(m)}${this.foot(m)}</div>', '<div class="mnTit">${esc(m.t)}</div>${this.sig(m)}${this.body(m)}${this.foot(m)}${CF.box("n:" + m.id, { sm: 1 })}</div>', "mnemônicos: caixinha na consulta")
a = rep(a, '${this.sig(m)}${this.body(m)}\n      <div class="mnAns">', '${this.sig(m)}${this.body(m)}${CF.box("n:" + m.id, { pri: 1 })}\n      <div class="mnAns">', "mnemônicos: caixinha no treino")
a = rep(a, '["o", "⚒️ Criados no 360X"]];', '["o", "⚒️ Criados no 360X"], ["cf", "🔴 Confiança baixa (1–2)"], ["cf0", "⬜ Confiança não marcada"]];', "mnemônicos: filtros de confiança")
a = rep(a, '(f === "c" && m.o === "c") || (f === "o" && m.o === "o"))', '(f === "c" && m.o === "c") || (f === "o" && m.o === "o") || (f === "cf" && CF.low("n:" + m.id)) || (f === "cf0" && !CF.val("n:" + m.id)))', "mnemônicos: filtro aplicado")
# ---------- 🕊️ Honra ----------
a = rep(a, '["fav", "⭐ Favoritos"]].concat(mnK ?', '["fav", "⭐ Favoritos"], ["cf", "🔴 Confiança baixa (1–2)"], ["cf0", "⬜ Confiança não marcada"]].concat(mnK ?', "honra: filtros de confiança")
a = rep(a, '(f === "u" && x.o === "u"))', '(f === "u" && x.o === "u") || (f === "cf" && CF.low("h:" + x.id)) || (f === "cf0" && !CF.val("h:" + x.id)))', "honra: filtro aplicado")
a = rep(a, '<div class="mnTit">${esc(c.q)}</div>${this.back(c)}${this.foot(c.id)}</div>', '<div class="mnTit">${esc(c.q)}</div>${this.back(c)}${this.foot(c.id)}${CF.box("h:" + c.id, { sm: 1 })}</div>', "honra: caixinha nos cards")
a = rep(a, '<div class="mnTit">${esc(m.t)}</div>${MN.sig(m)}${MN.body(m)}${this.foot(m.id)}</div>', '<div class="mnTit">${esc(m.t)}</div>${MN.sig(m)}${MN.body(m)}${this.foot(m.id)}${CF.box("h:" + m.id, { sm: 1 })}</div>', "honra: caixinha nos mnemônicos")
a = rep(a, '${q}${mnK ? MN.sig(x) + MN.body(x) : this.back(x)}\n', '${q}${mnK ? MN.sig(x) + MN.body(x) : this.back(x)}${CF.box("h:" + x.id, { pri: 1 })}\n', "honra: caixinha no treino")
a = rep(a, '${this.back(c)}</div>\n', '${this.back(c)}${CF.box("h:" + c.id, { sm: 1 })}</div>\n', "honra: caixinha na mensagem de hoje")
a = rep(a, '☑️ Usei esta bússola (+2 XP)</button>`}</div></div>', '☑️ Usei esta bússola (+2 XP)</button>`}</div>${CF.box("hb:" + b.id, { pri: 1 })}</div>', "honra: caixinha na bússola")
# ---------- 🏆 Jornada ----------
a = rep(a, 'a: ["🏆 Conquistas", "#e8c56a"] };', 'f: ["🎯 Confiança", "#ffd166"], a: ["🏆 Conquistas", "#e8c56a"] };', "fonte de XP 🎯")
a = rep(a, "wcd = WC.done();", "wcd = WC.done(), cfs = CF.stats();", "jStats: estatística de confiança")
a = rep(a, "wcN: wcd.n, wcAll: wcd.all };", "wcN: wcd.n, wcAll: wcd.all, cfN: cfs.n, cf5: cfs.top, cfLow: cfs.low };", "jStats: campos cfN/cf5/cfLow")
a = rep(a, "    /* ---------- 4.13.0: 🎭 estilo de comportamento ---------- */",
        '    /* ---------- 4.15.0: 🎯 confiança no domínio ---------- */\n'
        '    [[10, "medalha", "🎯", "Primeira Autoavaliação"], [100, "medalha", "🪞", "Espelho Honesto"], [500, "trofeu", "🧭", "Bússola Interior"], [2000, "brasao", "🔭", "Autoconhecimento"], [5000, "honra", "🌌", "Oráculo de Si Mesmo"]]\n'
        '      .forEach(([n, t, ic, nm]) => A("cf" + n, t, ic, nm, `Marcar a confiança 🎯 (1–5) em ${n.toLocaleString("pt-BR")} itens diferentes`, s => s.cfN, n, "est"));\n'
        '    [[50, "medalha"], [250, "trofeu"], [1000, "brasao"], [3000, "honra"]].forEach(([n, t]) => A("cf5_" + n, t, "💎", `Domínio Pleno ${n.toLocaleString("pt-BR")}`, `Ter ${n.toLocaleString("pt-BR")} itens com confiança 💎 5 (domino)`, s => s.cf5, n, "des"));\n'
        '    [[25, "medalha"], [100, "trofeu"]].forEach(([n, t]) => A("cfh" + n, t, "🦁", `Coragem de Admitir ${n}`, `Marcar com honestidade ${n} itens como 🔴 1 ou 🟠 2 — saber o que ainda não sabe é o 1º passo`, s => s.cfLow, n, "est"));\n'
        "    /* ---------- 4.13.0: 🎭 estilo de comportamento ---------- */", "conquistas de confiança")
a = rep(a, '     <div class="panel"><h2 style="margin-top:0">📊 Painel de produtividade (XP)</h2>', '     ${CF.html()}\n     <div class="panel"><h2 style="margin-top:0">📊 Painel de produtividade (XP)</h2>', "jornada: painel de confiança")
a = rep(a, '    WC.bind($("#jrHost"));', '    WC.bind($("#jrHost")); CF.bind($("#jrHost"));', "jornada: bind")
# ---------- 🎴 Estudo: caixinha na barra de resposta e na de revisão ----------
a = rep(a, '  $("#barHist").classList.toggle("on", which === "hist" && st);\n',
        '  $("#barHist").classList.toggle("on", which === "hist" && st);\n'
        '  const ca = $("#cfStudy"), ch = $("#cfHist"), hv = which === "hist" && st && Study.view != null && Study.undo[Study.view];\n'
        '  if (ca) ca.innerHTML = which === "ans" && st && Study.cur ? CF.box("c:" + Study.cur.id, { pri: 1, bar: 1 }) : "";\n'
        '  if (ch) ch.innerHTML = hv ? CF.box("c:" + hv.id, { pri: 1, bar: 1 }) : "";\n', "estudo: caixinha nas barras")
# ---------- correção: novo estudo filtrado não reabre o card revelado da sessão anterior ----------
a = rep(a, "Study.prefix = prefix; Study.ids = ids ? new Set(ids) : null;", "Study.cur = null; Study.shown = false; Study.view = null; Study.prefix = prefix; Study.ids = ids ? new Set(ids) : null;", "estudo: novo início zera o card corrente")
# ---------- 🔎 Buscar ----------
a = rep(a, '      if (i === "destaque" && !(c.hl && c.hl.length)) return false;\n',
        '      if (i === "destaque" && !(c.hl && c.hl.length)) return false;\n'
        '      const cv = Array.isArray(c.cf) ? c.cf[0] || 0 : 0;\n'
        '      if (/^conf[1-5]$/.test(i) && cv !== +i.slice(4)) return false;\n'
        '      if (i === "confbaixa" && !(cv > 0 && cv <= 2)) return false;\n'
        '      if (i === "semconf" && cv) return false;\n', "buscar: filtros is:conf")
a = rep(a, '${c.marked ? "🚩" : ""}${c.susp ? "⏸️" : ""}</div>', '${c.marked ? "🚩" : ""}${c.susp ? "⏸️" : ""}${Array.isArray(c.cf) && c.cf[0] ? `<span class="pill cfPill">${CF.LV[c.cf[0]][0]} ${c.cf[0]}</span>` : ""}</div>', "buscar: selo de confiança")
a = rep(a, '<div class="host"></div>\n', '<div class="host"></div>${CF.box("c:" + c.id, { sm: 1 })}\n', "buscar: caixinha no resultado")
APP.write_text(a, encoding="utf-8")

# ================= index.html =================
h = HTML.read_text(encoding="utf-8")
h = rep(h, '<div class="bar" id="barAns"><div class="in ans">', '<div class="bar" id="barAns"><div class="in cfIn" id="cfStudy"></div><div class="in ans">', "html: caixinha na barra de resposta")
h = rep(h, '<div class="bar" id="barHist"><div class="in" style="grid-template-columns:1fr 1fr 1.3fr">', '<div class="bar" id="barHist"><div class="in cfIn" id="cfHist"></div><div class="in" style="grid-template-columns:1fr 1fr 1.3fr">', "html: caixinha na barra de revisão")
h = rep(h, '<span class="kbd">L</span> ouvir', '<span class="kbd">Shift</span>+<span class="kbd">1</span>–<span class="kbd">5</span> 🎯 confiança · <span class="kbd">L</span> ouvir', "html: atalho no rodapé do estudo")
CSS = """/* 4.15.0 · 🎯 confiança no domínio 1–5 */
.cfBox{display:flex;flex-wrap:wrap;align-items:center;gap:6px 8px;margin:10px 0 2px;padding:8px 10px;border:1px dashed var(--line);border-radius:12px;background:#0f151d}
.cfBox.v1,.cfBox.v2{border-style:solid;border-color:color-mix(in srgb,var(--red) 55%,transparent)}.cfBox.v3{border-style:solid;border-color:color-mix(in srgb,var(--amb) 55%,transparent)}.cfBox.v4,.cfBox.v5{border-style:solid;border-color:color-mix(in srgb,var(--grn) 55%,transparent)}
.cfLbl{font-size:13px;font-weight:700;color:var(--gold2);white-space:nowrap}
.cfBtns{display:inline-flex;gap:5px;flex-wrap:nowrap}
.cfB{min-width:44px;height:36px;padding:0 7px;border-radius:9px;border:1.5px solid var(--cfc);background:transparent;color:var(--txt);font:700 15px Inter,system-ui,sans-serif;cursor:pointer;display:inline-flex;align-items:center;justify-content:center;gap:3px;touch-action:manipulation}
.cfB i{font-style:normal;font-size:14px;opacity:.8}
.cfB:hover{background:color-mix(in srgb,var(--cfc) 18%,transparent)}
.cfB.lit{background:color-mix(in srgb,var(--cfc) 22%,transparent)}
.cfB.on{background:var(--cfc);color:#14100a;box-shadow:0 0 0 2px color-mix(in srgb,var(--cfc) 40%,transparent)}.cfB.on i{opacity:1}
.cfB.pop{animation:cfpop .35s ease-out}@keyframes cfpop{0%{transform:scale(1)}40%{transform:scale(1.18)}100%{transform:scale(1)}}
.cfSt{font-size:12.5px;color:var(--mut)}
.cfBox.sm{padding:6px 8px;margin-top:8px;gap:5px 6px}.cfBox.sm .cfB{min-width:36px;height:30px;font-size:13px;padding:0 4px}.cfBox.sm .cfLbl{font-size:12px}
.bar .cfIn{display:block}.bar .cfIn:empty{display:none}
.bar .cfBox{margin:0 0 8px;padding:6px 8px;justify-content:center}
#v-estudar{padding-bottom:48px}
.cfDist{display:grid;gap:6px;margin:10px 0}.cfRowS{display:grid;grid-template-columns:150px 1fr 110px;gap:8px;align-items:center;font-size:13px}
.cfSec td,.cfSec th{text-align:center;padding:6px 6px}.cfSec td:first-child,.cfSec th:first-child{text-align:left}.cfSec td:not(:first-child),.cfSec th:not(:first-child){white-space:nowrap}
.pill.cfPill{color:#ffd166}
@media(max-width:440px){.bar .cfBox .cfSt{display:none}.bar .cfBox .cfB{min-width:40px}.cfRowS{grid-template-columns:118px 1fr 84px}}
html.lay-mobile .bar .cfBox .cfSt{display:none}
"""
h = rep(h, "/*LIGHT-START*/", CSS + "/*LIGHT-START*/", "html: CSS da caixinha")
HTML.write_text(h, encoding="utf-8")
print("🎯 4.15.0 aplicada. Agora rode: python3 tools/theme/build_light.py index.html")
