/* ================= 📕🗒️💉 Cadernos 360X (4.25.0): Erros · Notas · Prescrições =================
   ALDENIR ROCHA DE OLIVEIRA FILHO · PROJETO 360X
   - 📕 Caderno de Erros (CE): salva qualquer item do app (flashcard, questão, micropartícula, mnemônico, Honra, bússola,
     caso e fórmula de gasometria, prescrição) pelo botão 📕 que fica ao lado da caixinha 🎯, e trechos/tabelas pela seleção
     (botão 📕 do cabeçalho). Revisão mesclada (itens de todas as seções sorteados), refazer questões, estudar flashcards,
     mesclar itens numa nota. Dados: S.logs._ce {chave: {t, mod, del, src, ti, sn, h?, d, no, dom, st, n, lt}}.
   - 🗒️ Caderno de Notas (NB): lembretes de detalhes que costuma esquecer, com revisão espaçada (1→3→7→15→30→60→120 dias).
     Dados: S.logs._nb {id: {t, mod, del, ti, tx, tg, cor, pin, lem, iv, due, n, src}}.
   - 💉 Caderno de Prescrições (PX): 500 modelos (data/prescricoes.json) com quando usar, ℞ detalhada, monitorização, ajustes,
     contraindicações, alertas e referência; peso → doses por kg e mL/h. Dados: S.logs._px {id: {v, f, mod}}.
   Sincronização: _ce, _nb e _px se mesclam pelo `mod` mais recente de cada item (mesma regra do _hu da Honra). */
const CAD = {
  CRED: "ALDENIR ROCHA DE OLIVEIRA FILHO · PROJETO 360X",
  foot(x) { return `<div class="cadFoot">⚜️ ${x ? x + " · " : ""}<b>${this.CRED}</b></div>`; },
  nz: s => String(s || "").normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase(),
  uid: p => p + Date.now().toString(36) + Math.random().toString(36).slice(2, 6),
  dl(name, text, type = "text/markdown") { const a = document.createElement("a"); a.href = URL.createObjectURL(new Blob([text], { type: type + ";charset=utf-8" })); a.download = name; document.body.appendChild(a); a.click(); setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 1500); },
  async copy(text, ok = "📋 Copiado!") {
    try { await navigator.clipboard.writeText(text); toast(ok); return true; }
    catch (e) { const t = document.createElement("textarea"); t.value = text; t.style.position = "fixed"; t.style.opacity = "0"; document.body.appendChild(t); t.select(); let r = false; try { r = document.execCommand("copy"); } catch (x) {} t.remove(); toast(r ? ok : "Não consegui copiar — selecione o texto e use Copiar do sistema."); return r; }
  },
  clean(html, max = 9000) {   // trecho salvo: só marcação de texto e tabela (sem scripts, eventos, imagens ou links externos)
    const t = document.createElement("template"); t.innerHTML = String(html || "");
    t.content.querySelectorAll("script,style,iframe,object,embed,link,meta,img,video,audio,svg,canvas,button,input,select,textarea,form").forEach(n => n.remove());
    t.content.querySelectorAll("*").forEach(n => { for (const a of [...n.attributes]) { const nm = a.name.toLowerCase(); if (nm.startsWith("on") || nm === "id" || nm === "class" || nm === "style" || (nm === "href" && /^\s*javascript:/i.test(a.value))) n.removeAttribute(a.name); } if (n.tagName === "A") { n.removeAttribute("href"); } });
    let h = t.innerHTML.replace(/\s+/g, " ").trim(); if (h.length > max) h = h.slice(0, max) + "…";
    return h;
  },
  view() { return (location.hash || "#inicio").slice(1); },
  VNAME: { inicio: "🏠 Início", estudar: "🎴 Estudar", questoes: "❓ Questões", micro: "💊 Micro", mnemonicos: "🧠 Mnemônicos", honra: "🕊️ Honra", gaso: "🧪 Gaso", foco: "⏳ Foco", jornada: "🏆 Jornada", buscar: "🔎 Buscar", erros: "📕 Erros", notas: "🗒️ Notas", prescricoes: "💉 Prescrições", auditoria: "🔍 Auditoria", inexoravel: "⚖️ Inexorável" },
  st() {   // números para conquistas e início
    const ce = Object.values(S.logs._ce || {}).filter(e => e && !e.del), nb = Object.values(S.logs._nb || {}).filter(e => e && !e.del), px = Object.values(S.logs._px || {});
    return { ceA: ce.length, ceD: ce.filter(e => e.dom).length, ceR: ce.reduce((a, e) => a + (e.n || 0), 0), nbN: nb.length, nbR: nb.reduce((a, e) => a + (e.n || 0), 0), pxV: px.filter(e => e && e.v).length, pxF: px.filter(e => e && e.f).length };
  },
  homeStrip() {
    const ce = CE.items(), at = ce.filter(e => !e.dom).length, due = NB.due().length, s = this.st();
    return `<div class="panel cadStrip"><a class="cadChip" href="#erros">📕 <b>${at}</b> no caderno de erros</a><a class="cadChip${due ? " hot" : ""}" href="#notas">🔔 <b>${due}</b> nota${due === 1 ? "" : "s"} para relembrar hoje</a><a class="cadChip" href="#prescricoes" id="pxDayLnk">💉 Prescrição do dia</a><span class="cadChip mut">℞ ${s.pxV}/500 estudadas</span></div>`;
  },
  bindHome() { const a = $("#pxDayLnk"); if (a) a.onclick = e => { e.preventDefault(); PX.day(); }; }
};

/* ---------------- 📕 Caderno de Erros ---------------- */
const CE = {
  T: { c: ["🎴", "Flashcard"], q: ["❓", "Questão"], m: ["💊", "Micropartícula"], n: ["🧠", "Mnemônico"], h: ["🕊️", "Honra"], hb: ["🧭", "Bússola"], g: ["🧪", "Caso de gasometria"], gf: ["📐", "Fórmula"], p: ["💉", "Prescrição"], s: ["✂️", "Trecho / tabela"] },
  mode: "lista", ft: "", fs: "ativos", q: "", lim: 30, opened: null, sel: new Set(), rv: null,
  R() { return (S.logs._ce = S.logs._ce || {}); },
  typ(k) { const i = String(k).indexOf(":"); return i > 0 ? k.slice(0, i) : "s"; },
  has(k) { const e = this.R()[k]; return !!e && !e.del; },
  items() { return Object.entries(this.R()).filter(([, e]) => e && !e.del).map(([k, e]) => Object.assign({ k }, e)).sort((a, b) => (b.t || 0) - (a.t || 0)); },
  opt(k) { return lsGet("ce_" + k) !== "0" && (k !== "c" || lsGet("ce_c") === "1"); },   // padrão: questões erradas entram sozinhas; flashcards "De novo" só se ligar
  btn(k, sm) { const on = this.has(k); return `<button type="button" class="ceB${on ? " on" : ""}${sm ? " sm" : ""}" data-cek="${esc(k)}" title="${on ? "Está no 📕 Caderno de Erros — toque para tirar" : "Salvar no 📕 Caderno de Erros"}" aria-pressed="${on}">${on ? "📕 No caderno ✓" : "📕 Caderno"}</button>`; },
  paint(k) { for (const b of $$("[data-cek]")) if (b.dataset.cek === k) { const t = document.createElement("div"); t.innerHTML = this.btn(k, b.classList.contains("sm")); b.replaceWith(t.firstElementChild); } },
  async meta(k, el) {   // título e prévia (texto) guardados junto da chave — servem de reserva se o item sair do app
    let ti = "", sn = "";
    try { const r = await this.res(k); if (r) { ti = r.ti || ""; sn = strip(r.b || r.f || ""); } } catch (e) {}
    if (!ti && el) { const box = el.closest(".gzF,.mnCard,.mcCard,.res,.pxDet,.hoPanel,.panel,.bar") || el.parentElement; const tx = box ? box.innerText || "" : ""; ti = tx.split("\n").map(s => s.trim()).find(s => s.length > 8) || ""; sn = tx; }
    return { ti: strip(ti).slice(0, 160), sn: strip(sn).slice(0, 600) };
  },
  async add(k, o = {}, el) {
    const R = this.R(), now = Date.now(), c = R[k] && !R[k].del ? R[k] : null;
    const m = c ? {} : await this.meta(k, el);
    R[k] = Object.assign({ t: now, src: "m", st: 0, n: 0, dom: 0, d: CAD.VNAME[CAD.view()] || "" }, c || {}, m, o, { mod: now, del: 0 });
    if (!c) { const L = L0(); L.ceN = (L.ceN || 0) + 1; }
    await saveLog(); this.paint(k); return R[k];
  },
  async rm(k) { const R = this.R(); R[k] = { mod: Date.now(), del: 1 }; await saveLog(); this.paint(k); },
  async toggle(k, el) { if (this.has(k)) { await this.rm(k); toast("📕 Tirado do caderno de erros"); } else { await this.add(k, {}, el); toast(`📕 Salvo no caderno de erros · <a href="#erros" style="color:var(--gold2)">abrir</a>`); } },
  async auto(k) { const t = this.typ(k); if (!this.opt(t) || this.has(k)) return; await this.add(k, { src: "a" }); },
  grab() {   // seleção atual (inclui o card do estudo, que fica num shadow DOM)
    let sel = null;
    try { const host = $("#cardHost"), r = host && host.shadowRoot; if (r && r.getSelection) { const s2 = r.getSelection(); if (s2 && !s2.isCollapsed && String(s2).trim()) sel = s2; } } catch (e) {}
    if (!sel) { const s1 = window.getSelection ? window.getSelection() : null; if (s1 && !s1.isCollapsed && String(s1).trim()) sel = s1; }
    if (!sel) return null; const a = sel.anchorNode, el = a && (a.nodeType === 1 ? a : a.parentElement);
    if (el && el.closest && el.closest("input,textarea,#ceHost,#nbHost")) return null;
    let html = ""; if (sel.rangeCount) { const d = document.createElement("div"); for (let i = 0; i < sel.rangeCount; i++) d.appendChild(sel.getRangeAt(i).cloneContents()); html = CAD.clean(d.innerHTML); }
    return { sel, txt: String(sel).trim(), html };
  },
  async capture() {   // botão 📕 do cabeçalho: salva o trecho/tabela selecionado; sem seleção, abre o caderno
    let g = this.grab(); if (!g && this.lastSel && Date.now() - this.lastSel.t < 30000) g = this.lastSel;
    if (!g || !g.txt) { location.hash = "erros"; return; }
    const k = CAD.uid("s:"), ti = g.txt.replace(/\s+/g, " ").slice(0, 90);
    await this.add(k, { src: "s", ti, sn: g.txt.slice(0, 600), h: g.html || esc(g.txt) });
    this.lastSel = null; try { g.sel.removeAllRanges(); } catch (e) {}
    toast(`✂️ Trecho salvo no 📕 caderno de erros · <a href="#erros" style="color:var(--gold2)">abrir</a>`);
  },
  /* resolve o conteúdo atual do item: título, frente (pergunta) e verso (resposta) em HTML */
  async res(k) {
    const t = this.typ(k), id = k.slice(t.length + 1), e = this.R()[k] || {};
    const find = (data, divs) => { for (const d of divs) { const x = (data[d] || []).find(i => String(i.id) === id); if (x) return x; } return null; };
    if (t === "c") { const c = S.byId.get(id); if (!c) return null; return { ti: strip(c.q).slice(0, 160), card: c, f: c.q, b: c.a, sub: c.deck }; }
    if (t === "q") { await QZ.load(); const q = find(QZ.data, ["temi", "r3", "gaso"]); if (!q) return null;
      return { ti: strip(q.enun).slice(0, 160), q, sub: q.tema, f: `<div class="qzEnun">${q.enun}</div>${q.fig ? `<figure class="qzFig img"><img alt="${esc(q.fig.alt || "Figura")}" data-qfk="${esc(q.fig.p + "#" + q.fig.k)}" data-qfn="${esc(q.fig.k)}"></figure>` : ""}<ol class="ceAlts">${q.alts.map((a, i) => `<li><b>${"ABCDE"[i]}</b> ${a}</li>`).join("")}</ol>`,
        b: `<div class="qzRes ok">✅ Gabarito ${"ABCDE"[q.gab]}: ${q.alts[q.gab]}</div><div class="qzExp">${q.com}${q.pega ? `<div class="qzPega">🎯 <b>Pegadinha:</b> ${q.pega}</div>` : ""}</div>${q.ref ? `<div class="qzRef">📚 ${esc(q.ref)}</div>` : ""}` }; }
    if (t === "m") { await MC.load(); const m = find(MC.data, ["temi", "r3"]); if (!m) return null;
      return { ti: strip(m.titulo), sub: m.tema, f: `<h3 class="ceH">${m.emoji || "💊"} ${m.titulo}</h3>`, b: `<div class="mcTxt">${m.texto}</div>${m.gancho ? `<div class="mcHook">🧠 ${m.gancho}</div>` : ""}${m.comentario ? `<div class="qzExp">${m.comentario}</div>` : ""}` }; }
    if (t === "n") { await MN.load(); const m = find(MN.data, ["temi", "r3"]); if (!m) return null; return this.mnRes(m); }
    if (t === "h" || t === "hb") { await HO.load(); const D = HO.data || {};
      if (t === "hb") { const b = (D.bu || []).find(x => String(x.id) === id); if (!b) return null; return { ti: strip(b.t), sub: "🧭 Bússola", f: `<h3 class="ceH">${b.e || "🧭"} ${b.t}</h3>${b.sin ? `<p>${b.sin}</p>` : ""}`, b: ["N", "S", "L"].filter(f => b[f]).map(f => `<p><b>${{ N: "💬 Norte", S: "⛔ Sombra", L: "🧭 Leme" }[f]}:</b> ${b[f]}</p>`).join("") }; }
      const c = (D.cards || []).find(x => String(x.id) === id); if (c) return { ti: strip(c.q), sub: c.tema, f: `<h3 class="ceH">🕊️ ${c.q}</h3>`, b: `<p>${c.a}</p>${c.r ? `<p class="qzRef">📖 ${esc(c.r)}</p>` : ""}${c.ap ? `<div class="mcHook">🌱 ${c.ap}</div>` : ""}` };
      const m = (D.mn || []).find(x => String(x.id) === id); if (m) return this.mnRes(m); return null; }
    if (t === "g") { await GZ.load(); const c = (GZ.data.casos || []).find(x => String(x.n) === id); if (!c) return null;
      const lab = c.lab && typeof c.lab === "object" ? Object.entries(c.lab).map(([a, v]) => `<span class="pill">${esc(a)} ${esc(v)}</span>`).join("") : "";
      return { ti: strip(c.ctx).slice(0, 160), sub: c.deck, f: `<p>${c.ctx}</p>${lab ? `<div class="ceGas">${lab}</div>` : ""}`, b: `<p><b>✅ ${c.dx || ""}</b></p>${c.causa ? `<p>${c.causa}</p>` : ""}${c.cond ? `<p>⚡ ${c.cond}</p>` : ""}${c.peg ? `<div class="qzPega">🎯 ${c.peg}</div>` : ""}` }; }
    if (t === "p") { await PX.load(); const p = PX.byId(id); if (!p) return null; return { ti: p.ti, sub: PX.AREA[p.area][0] + " · " + p.cat, f: `<h3 class="ceH">💉 ${esc(p.ti)}</h3><p><b>🎯 Quando usar:</b> ${PX.fmt(p.quando)}</p>`, b: PX.rxHTML(p) }; }
    if (t === "s") return { ti: e.ti || "Trecho", sub: e.d || "", f: `<h3 class="ceH">✂️ ${esc(e.ti || "Trecho salvo")}</h3>`, b: `<div class="ceSnip">${e.h || esc(e.sn || "")}</div>` };
    return null;
  },
  mnRes(m) { const k = (m.k || []).map(([a, b]) => `<li><b>${esc(a)}</b> — ${b}</li>`).join(""); return { ti: strip(m.t), sub: m.tema, f: `<h3 class="ceH">🧠 ${m.t}</h3>${m.m ? `<p class="mnSig">${esc(m.m)}</p>` : ""}`, b: `${k ? `<ul class="ceK">${k}</ul>` : ""}${m.x ? `<div class="mcHook">⚡ ${m.x}</div>` : ""}${m.c ? `<p class="metaNow">${m.c}</p>` : ""}` }; },
  async fill(host, r) {   // monta frente/verso (flashcards usam o mesmo renderizador do estudo)
    if (!r) { host.innerHTML = `<p class="metaNow">⚠️ Este item não está mais no app. Ficou a prévia salva.</p>`; return; }
    if (r.card) { host.innerHTML = `<div class="ceF host"></div><div class="ceBk host"></div>`; await renderInto($(".ceF", host), r.card.q, r.card.style, r.card.deck); await renderInto($(".ceBk", host), r.card.a, r.card.style, r.card.deck); return; }
    host.innerHTML = `<div class="ceF">${r.f || ""}</div><div class="ceBk">${r.b || ""}</div>`; this.figs(host);
  },
  figs(host) { for (const im of $$("[data-qfk]", host)) MEDIAPACK.url(im.dataset.qfk, im.dataset.qfn).then(u => { if (u && im.isConnected) { im.src = u; ZOOM.bind(im.closest(".ceF") || host); } }); },
  list() {
    const qn = CAD.nz(this.q).split(/\s+/).filter(Boolean);
    return this.items().filter(e => (!this.ft || this.typ(e.k) === this.ft) && (this.fs === "todos" || (this.fs === "dom" ? e.dom : !e.dom)) && (!qn.length || qn.every(w => CAD.nz([e.ti, e.sn, e.no, e.tg, e.d].join(" ")).includes(w))));
  },
  async open() { if (this.mode === "rev" && this.rv) return this.revShow(); this.render(); },
  render() {
    const all = this.items(), act = all.filter(e => !e.dom), dom = all.length - act.length, l = this.list(), cnt = {};
    for (const e of all) { const t = this.typ(e.k); cnt[t] = (cnt[t] || 0) + 1; }
    const qn = act.filter(e => this.typ(e.k) === "q").length, cn = act.filter(e => this.typ(e.k) === "c").length;
    $("#ceHost").innerHTML = `<div class="panel cadHero"><h2 style="margin:0 0 4px">📕 Caderno de Erros</h2><p class="metaNow" style="margin:0">Tudo que você errou, quase errou ou quer rever — de todas as seções, num lugar só.</p>
      <div class="stats" style="margin:10px 0"><div class="stat"><b class="n">${act.length}</b><span>ativos</span></div><div class="stat"><b style="color:var(--cy)">${dom}</b><span>✅ dominados</span></div><div class="stat"><b style="color:var(--gold2)">${all.reduce((a, e) => a + (e.n || 0), 0)}</b><span>revisões</span></div></div>
      <div class="metaRow"><button class="btn gold" id="ceRev" ${act.length ? "" : "disabled"}>🔀 Revisão mesclada (${Math.min(20, act.length)})</button><button class="btn" id="ceRevAll" ${act.length > 20 ? "" : "hidden"}>🔀 Todos (${act.length})</button><button class="btn" id="ceQz" ${qn ? "" : "disabled"}>❓ Refazer as questões (${qn})</button><button class="btn" id="ceCards" ${cn ? "" : "disabled"}>🎴 Estudar os flashcards (${cn})</button></div>
      <details class="ceHow"><summary>❔ Como salvar itens</summary><p class="metaNow">• Botão <b>📕 Caderno</b> ao lado da caixinha 🎯 em cada flashcard (ao revelar), questão (ao responder), micropartícula, mnemônico, card/bússola da Honra, caso e fórmula de gasometria e prescrição.<br>• <b>Trechos e tabelas:</b> selecione o texto (ou a tabela) em qualquer tela e toque no <b>📕</b> do cabeçalho.<br>• <b>Automático:</b> questões erradas entram sozinhas (desligável abaixo); flashcards marcados “De novo” também, se você ligar.</p>
       <div class="metaRow"><label class="chk2"><input type="checkbox" id="ceOptQ" ${this.opt("q") ? "checked" : ""}> ❓ Questões erradas entram sozinhas</label><label class="chk2"><input type="checkbox" id="ceOptC" ${this.opt("c") ? "checked" : ""}> 🎴 Flashcards “De novo” entram sozinhos</label></div></details></div>
     <div class="panel"><div class="metaRow ceFilt"><button class="btn sm ${!this.ft ? "gold" : ""}" data-ft="">Todos (${all.length})</button>${Object.entries(this.T).filter(([t]) => cnt[t]).map(([t, [ic, nm]]) => `<button class="btn sm ${this.ft === t ? "gold" : ""}" data-ft="${t}" title="${nm}">${ic} ${cnt[t]}</button>`).join("")}</div>
      <div class="metaRow"><select id="ceFs"><option value="ativos" ${this.fs === "ativos" ? "selected" : ""}>📕 Ativos</option><option value="dom" ${this.fs === "dom" ? "selected" : ""}>✅ Dominados</option><option value="todos" ${this.fs === "todos" ? "selected" : ""}>📚 Todos</option></select><input id="ceQ" class="grow" placeholder="🔎 Buscar no caderno (título, prévia, sua nota, tag)…" value="${esc(this.q)}"></div>
      <div class="metaRow"><button class="btn sm" id="ceSelAll">☑️ Selecionar visíveis</button><button class="btn sm" id="ceMerge" ${this.sel.size >= 1 ? "" : "disabled"}>🧩 Mesclar ${this.sel.size || ""} em uma nota</button><button class="btn sm" id="ceSelRev" ${this.sel.size >= 1 ? "" : "disabled"}>🔀 Revisar selecionados</button><button class="btn sm" id="ceSelNone" ${this.sel.size ? "" : "hidden"}>✖ Limpar seleção</button><button class="btn sm" id="ceExp" ${all.length ? "" : "disabled"}>📤 Exportar (.md)</button></div>
      <div id="ceList">${l.length ? l.slice(0, this.lim).map(e => this.row(e)).join("") : `<p class="empty">${all.length ? "Nada neste filtro." : "📕 Caderno vazio. Toque em <b>📕 Caderno</b> em qualquer item, ou erre uma questão 😉."}</p>`}</div>
      ${l.length > this.lim ? `<div class="metaRow" style="justify-content:center"><button class="btn" id="ceMore">⬇️ Mostrar mais (${l.length - this.lim})</button></div>` : ""}</div>${CAD.foot("📕 Caderno de Erros")}`;
    this.bind();
  },
  row(e) {
    const t = this.typ(e.k), [ic, nm] = this.T[t] || ["📌", "Item"], open = this.opened === e.k;
    return `<div class="ceRow${e.dom ? " dom" : ""}${open ? " open" : ""}" data-k="${esc(e.k)}"><div class="ceHd"><input type="checkbox" class="ceSel" ${this.sel.has(e.k) ? "checked" : ""} aria-label="Selecionar"><span class="pill" title="${nm}">${ic} ${nm}</span>${e.src === "a" ? `<span class="pill ceAuto" title="Entrou sozinho (resposta errada)">⚡ auto</span>` : ""}${e.dom ? `<span class="pill" style="color:#5be38a">✅ dominado</span>` : ""}${e.tg ? `<span class="pill ceTg">🏷️ ${esc(e.tg)}</span>` : ""}<span class="ceTi">${esc(e.ti || "(sem título)")}</span><span class="ceMeta">${e.n ? `🔁 ${e.n}× · ` : ""}${new Date(e.t || 0).toLocaleDateString("pt-BR")}</span></div>
      ${open ? `<div class="ceBd"><div class="ceBody"><p class="metaNow">⏳ carregando…</p></div>
        <label class="ceNoL">✍️ Minha nota sobre este erro<textarea class="ceNo" rows="2" placeholder="Por que errei? O detalhe que não posso esquecer…">${esc(e.no || "")}</textarea></label>
        <div class="metaRow"><input class="ceTgIn" placeholder="🏷️ tag (ex.: dose, prova, plantão)" value="${esc(e.tg || "")}"><button class="btn sm gold" data-a="save">💾 Salvar nota</button>${e.dom ? `<button class="btn sm" data-a="undom">↩️ Voltar para ativos</button>` : `<button class="btn sm" data-a="dom">✅ Dominei</button>`}${t === "q" ? `<button class="btn sm" data-a="redo">❓ Refazer</button>` : ""}${t === "c" ? `<button class="btn sm" data-a="study">🎴 Estudar</button>` : ""}${t === "p" ? `<button class="btn sm" data-a="px">💉 Abrir prescrição</button>` : ""}<button class="btn sm" data-a="note">🗒️ Virar nota</button><button class="btn sm danger" data-a="del">🗑️ Tirar</button></div></div>` : ""}</div>`;
  },
  bind() {
    const H = $("#ceHost");
    $$("[data-ft]", H).forEach(b => b.onclick = () => { this.ft = b.dataset.ft; this.lim = 30; this.render(); });
    $("#ceFs").onchange = e => { this.fs = e.target.value; this.render(); };
    let qT; $("#ceQ").oninput = e => { clearTimeout(qT); qT = setTimeout(() => { this.q = e.target.value; this.render(); const i = $("#ceQ"); if (i) { i.focus(); i.setSelectionRange(i.value.length, i.value.length); } }, 250); };
    const mo = $("#ceMore"); if (mo) mo.onclick = () => { this.lim += 30; this.render(); };
    $("#ceRev").onclick = () => this.revStart(this.items().filter(e => !e.dom).map(e => e.k), 20);
    $("#ceRevAll").onclick = () => this.revStart(this.items().filter(e => !e.dom).map(e => e.k), 9999);
    $("#ceQz").onclick = () => this.redoQ(this.items().filter(e => !e.dom && this.typ(e.k) === "q").map(e => e.k));
    $("#ceCards").onclick = () => { const ids = this.items().filter(e => !e.dom && this.typ(e.k) === "c").map(e => e.k.slice(2)).filter(id => S.byId.get(id)); if (!ids.length) return toast("Os flashcards salvos não estão nas coleções ativas."); startStudy(null, ids); };
    $("#ceOptQ").onchange = e => { lsSet("ce_q", e.target.checked ? "1" : "0"); toast(e.target.checked ? "❓ Questões erradas entram sozinhas" : "❓ Só entra o que você salvar"); };
    $("#ceOptC").onchange = e => { lsSet("ce_c", e.target.checked ? "1" : "0"); toast(e.target.checked ? "🎴 “De novo” entra sozinho" : "🎴 Só entra o que você salvar"); };
    $("#ceSelAll").onclick = () => { this.list().slice(0, this.lim).forEach(e => this.sel.add(e.k)); this.render(); };
    const sn = $("#ceSelNone"); if (sn) sn.onclick = () => { this.sel.clear(); this.render(); };
    $("#ceMerge").onclick = () => this.merge([...this.sel]);
    $("#ceSelRev").onclick = () => this.revStart([...this.sel], 9999);
    $("#ceExp").onclick = () => this.exportMd();
    $$(".ceRow", H).forEach(row => {
      const k = row.dataset.k;
      $(".ceSel", row).onchange = e => { e.target.checked ? this.sel.add(k) : this.sel.delete(k); this.render(); };
      $(".ceHd", row).onclick = e => { if (e.target.closest(".ceSel")) return; this.opened = this.opened === k ? null : k; this.render(); };
      if (this.opened === k) {
        this.res(k).then(r => { const b = $(".ceBody", row); if (b) this.fill(b, r || null).then(() => { if (!r) b.insertAdjacentHTML("beforeend", `<p>${esc((this.R()[k] || {}).sn || "")}</p>`); }); });
        $$("[data-a]", row).forEach(b => b.onclick = () => this.act(k, b.dataset.a, row, b));
      }
    });
  },
  async act(k, a, row, b) {
    const e = this.R()[k]; if (!e) return;
    if (a === "save") { e.no = $(".ceNo", row).value.trim().slice(0, 2000); e.tg = $(".ceTgIn", row).value.trim().slice(0, 40); e.mod = Date.now(); await saveLog(); toast("💾 Nota salva"); return this.render(); }
    if (a === "dom" || a === "undom") { e.dom = a === "dom" ? Date.now() : 0; e.mod = Date.now(); await saveLog(); if (a === "dom") { addXP(3, "erro vencido", "e"); toast("✅ Dominado! Saiu dos ativos (+3 XP)"); } return this.render(); }
    if (a === "redo") return this.redoQ([k]);
    if (a === "study") { const id = k.slice(2); if (!S.byId.get(id)) return toast("Este flashcard não está nas coleções ativas."); return startStudy(null, [id]); }
    if (a === "px") return PX.go(k.slice(2));
    if (a === "note") { const r = await this.res(k); const id = await NB.save({ ti: "📕 " + (e.ti || "Erro").slice(0, 90), tx: [e.no ? "✍️ " + e.no : "", strip(r ? r.b : e.sn || "").slice(0, 1500)].filter(Boolean).join("\n\n"), tg: e.tg || "erro", src: "ce" }); toast(`🗒️ Nota criada · <a href="#notas" style="color:var(--gold2)">abrir</a>`); return id; }
    if (a === "del") { if (b.dataset.cf !== "1") { b.dataset.cf = "1"; b.textContent = "Confirmar?"; return; } await this.rm(k); this.sel.delete(k); this.opened = null; toast("🗑️ Tirado do caderno"); return this.render(); }
  },
  async redoQ(keys) {
    await QZ.load(); const ids = new Set(keys.map(k => k.slice(2))), all = ["temi", "r3", "gaso"].flatMap(d => QZ.data[d] || []), bl = all.filter(q => ids.has(String(q.id)));
    if (!bl.length) return toast("Questões não encontradas.");
    for (let i = bl.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [bl[i], bl[j]] = [bl[j], bl[i]]; }
    QZ.block = bl.slice(0, 50); QZ.i = 0; QZ.ok = 0; QZ.pickd = null; QZ.done = false;
    if (location.hash !== "#questoes") location.hash = "questoes"; else QZ.show();
  },
  async merge(keys) {
    if (!keys.length) return; const parts = [];
    for (const k of keys) { const e = this.R()[k] || {}, r = await this.res(k).catch(() => null), [ic] = this.T[this.typ(k)] || ["📌"]; parts.push(`${ic} ${e.ti || (r && r.ti) || k}${e.no ? `\n   ✍️ ${e.no}` : ""}\n   ${strip(r ? r.b : e.sn || "").slice(0, 400)}`); }
    await NB.save({ ti: `🧩 Mesclagem de ${keys.length} ${keys.length === 1 ? "item" : "itens"} do caderno de erros`, tx: parts.join("\n\n"), tg: "mesclagem", src: "ce" });
    this.sel.clear(); this.render(); toast(`🧩 Nota de mesclagem criada · <a href="#notas" style="color:var(--gold2)">abrir</a>`);
  },
  exportMd() {
    const L = this.items(), lines = [`# 📕 Caderno de Erros 360X`, ``, `_${CAD.CRED}_ · exportado em ${new Date().toLocaleString("pt-BR")} · ${L.length} itens`, ``];
    for (const e of L) { const [ic, nm] = this.T[this.typ(e.k)] || ["📌", "Item"]; lines.push(`## ${ic} ${e.ti || nm}`, `- Tipo: ${nm}${e.dom ? " · ✅ dominado" : ""}${e.tg ? ` · 🏷️ ${e.tg}` : ""} · salvo em ${new Date(e.t || 0).toLocaleDateString("pt-BR")}${e.n ? ` · revisado ${e.n}×` : ""}`); if (e.no) lines.push(`- ✍️ Nota: ${e.no}`); if (e.sn) lines.push(``, `> ${e.sn.replace(/\n+/g, " ").slice(0, 600)}`); lines.push(``); }
    CAD.dl(`Caderno_de_Erros_360X_${today()}.md`, lines.join("\n")); toast("📤 Caderno exportado");
  },
  /* 🔀 Revisão mesclada: itens de todas as seções, sorteados; frente → mostrar → ✅ acertei / 🔁 errei de novo */
  revStart(keys, max) {
    const l = keys.filter(k => this.has(k)); if (!l.length) return toast("Nada para revisar.");
    for (let i = l.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [l[i], l[j]] = [l[j], l[i]]; }
    this.rv = { l: l.slice(0, max), i: 0, ok: 0, shown: false }; this.mode = "rev"; this.revShow();
  },
  async revShow() {
    const R = this.rv, H = $("#ceHost"); if (!R) return this.render();
    if (R.i >= R.l.length) { const n = R.l.length; this.mode = "lista"; this.rv = null;
      H.innerHTML = `<div class="empty"><div style="font-size:46px">${R.ok === n ? "🏆" : "📕"}</div><h2>Revisão mesclada concluída</h2><p>✅ ${R.ok}/${n} lembrados · 🔁 ${n - R.ok} para rever</p><div class="metaRow" style="justify-content:center"><button class="btn gold" id="ceBack">📕 Voltar ao caderno</button></div></div>${CAD.foot("📕 Caderno de Erros")}`;
      $("#ceBack").onclick = () => this.render(); return; }
    const k = R.l[R.i], e = this.R()[k] || {}, [ic, nm] = this.T[this.typ(k)] || ["📌", "Item"];
    H.innerHTML = `<div class="metaRow"><span class="pill">🔀 Revisão mesclada ${R.i + 1}/${R.l.length}</span><span class="pill">${ic} ${nm}</span>${e.tg ? `<span class="pill">🏷️ ${esc(e.tg)}</span>` : ""}<span class="grow"></span><button class="btn sm" id="ceRvQuit">⏹️ Encerrar</button></div>
      <div class="progress"><i style="width:${100 * R.i / R.l.length}%"></i></div>
      <div class="panel ceRv${R.shown ? " shown" : ""}"><div id="ceRvBody"><p class="metaNow">⏳ carregando…</p></div>${e.no && R.shown ? `<div class="mcHook">✍️ <b>Sua nota:</b> ${esc(e.no)}</div>` : ""}</div>
      <div class="metaRow" style="justify-content:center">${R.shown ? `<button class="btn" id="ceRvBad">🔁 Errei de novo</button><button class="btn gold" id="ceRvOk">✅ Acertei${(e.st || 0) >= 2 ? " (vira dominado)" : ""}</button>` : `<button class="btn gold" id="ceRvShow">👁️ Mostrar resposta</button>`}</div>
      <p class="metaNow" style="text-align:center">⌨️ <span class="kbd">Espaço</span> mostrar · <span class="kbd">1</span> errei · <span class="kbd">2</span> acertei · 3 acertos seguidos = ✅ dominado · +1 XP por item</p>`;
    const r = await this.res(k).catch(() => null), body = $("#ceRvBody"); if (!body) return;
    await this.fill(body, r); if (!r) body.insertAdjacentHTML("beforeend", `<p>${esc(e.sn || "")}</p>`);
    $("#ceRvQuit").onclick = () => { this.rv = null; this.mode = "lista"; this.render(); };
    const sh = $("#ceRvShow"); if (sh) sh.onclick = () => { R.shown = true; this.revShow(); };
    const ok = $("#ceRvOk"), bad = $("#ceRvBad"); if (ok) ok.onclick = () => this.revAns(true); if (bad) bad.onclick = () => this.revAns(false);
  },
  async revAns(ok) {
    const R = this.rv; if (!R || !R.shown) return; const k = R.l[R.i], e = this.R()[k]; if (!e) return;
    e.n = (e.n || 0) + 1; e.lt = Date.now(); e.st = ok ? (e.st || 0) + 1 : 0; if (ok) R.ok++;
    if (ok && e.st >= 3 && !e.dom) { e.dom = Date.now(); toast("✅ 3 acertos seguidos — dominado!"); addXP(3, "erro vencido", "e"); }
    e.mod = Date.now(); const L = L0(); L.ceR = (L.ceR || 0) + 1; addXP(1, ok ? "lembrei" : "revisão", "e"); await saveLog();
    R.i++; R.shown = false; this.revShow();
  }
};
document.addEventListener("click", e => {
  const b = e.target && e.target.closest ? e.target.closest("[data-cek]") : null; if (!b) return;
  e.preventDefault(); e.stopPropagation(); CE.toggle(b.dataset.cek, b);
}, true);
document.addEventListener("selectionchange", () => { clearTimeout(CE._st); CE._st = setTimeout(() => { const g = CE.grab(); if (g && g.txt) CE.lastSel = Object.assign(g, { t: Date.now() }); }, 200); });
document.addEventListener("keydown", e => {
  if (CAD.view() !== "erros" || !CE.rv || e.ctrlKey || e.metaKey || e.altKey || /input|textarea|select/i.test((e.target || {}).tagName || "")) return;
  if (e.code === "Space" && !CE.rv.shown) { e.preventDefault(); CE.rv.shown = true; CE.revShow(); }
  else if (CE.rv.shown && (e.key === "1" || e.key === "2")) { e.preventDefault(); CE.revAns(e.key === "2"); }
});

/* ---------------- 🗒️ Caderno de Notas (lembretes com revisão espaçada) ---------------- */
const NB = {
  IV: [1, 3, 7, 15, 30, 60, 120], COR: { "": "⚪", r: "🟥", o: "🟧", y: "🟨", g: "🟩", b: "🟦", p: "🟪" },
  f: "", q: "", tg: "", ed: null, lim: 40,
  R() { return (S.logs._nb = S.logs._nb || {}); },
  items() { return Object.entries(this.R()).filter(([, e]) => e && !e.del).map(([id, e]) => Object.assign({ id }, e)).sort((a, b) => (b.pin ? 1 : 0) - (a.pin ? 1 : 0) || (b.mod || 0) - (a.mod || 0)); },
  due() { const eod = endOfDay(); return this.items().filter(e => e.lem && (e.due || 0) <= eod); },
  async save(o, id) {
    const R = this.R(), now = Date.now(); id = id || CAD.uid("nb");
    const c = R[id] && !R[id].del ? R[id] : { t: now, lem: true, iv: 0, due: now + DAY, n: 0, pin: false, cor: "" };
    R[id] = Object.assign({}, c, o, { mod: now, del: 0 }); R[id].ti = String(R[id].ti || "").slice(0, 140); R[id].tx = String(R[id].tx || "").slice(0, 6000); R[id].tg = String(R[id].tg || "").slice(0, 60);
    if (!c.t || c.t === now) { const L = L0(); L.nbN = (L.nbN || 0) + 1; }
    await saveLog(); return id;
  },
  async rm(id) { this.R()[id] = { mod: Date.now(), del: 1 }; await saveLog(); },
  async open() { this.render(); },
  md(s) { return esc(s).replace(/\*\*(.+?)\*\*/g, "<b>$1</b>").replace(/(^|\s)_(.+?)_(?=\s|$)/g, "$1<i>$2</i>").replace(/\n/g, "<br>"); },
  list() {
    const qn = CAD.nz(this.q).split(/\s+/).filter(Boolean), eod = endOfDay();
    return this.items().filter(e => (!this.f || (this.f === "pin" ? e.pin : this.f === "due" ? e.lem && (e.due || 0) <= eod : this.f === "lem" ? e.lem : this.f === "ce" ? e.src === "ce" : true)) && (!this.tg || (e.tg || "").split(/[,;]\s*/).includes(this.tg)) && (!qn.length || qn.every(w => CAD.nz([e.ti, e.tx, e.tg].join(" ")).includes(w))));
  },
  render() {
    const all = this.items(), due = this.due(), l = this.list(), tags = [...new Set(all.flatMap(e => (e.tg || "").split(/[,;]\s*/).filter(Boolean)))].sort((a, b) => a.localeCompare(b, "pt")), E = this.ed ? this.R()[this.ed] || {} : {};
    $("#nbHost").innerHTML = `<div class="panel cadHero"><h2 style="margin:0 0 4px">🗒️ Caderno de Notas</h2><p class="metaNow" style="margin:0">Os detalhes que costumam escapar — doses, cortes, pegadinhas, rotinas. Notas com 🔔 voltam em 1 → 3 → 7 → 15 → 30 → 60 → 120 dias.</p>
      <div class="stats" style="margin:10px 0"><div class="stat"><b class="n">${all.length}</b><span>notas</span></div><div class="stat"><b style="color:${due.length ? "var(--amb)" : "var(--mut)"}">🔔 ${due.length}</b><span>para relembrar hoje</span></div><div class="stat"><b style="color:var(--cy)">${all.filter(e => e.pin).length}</b><span>📌 fixadas</span></div></div>
      ${due.length ? `<div class="nbDue"><h3 style="margin:0 0 6px">🔔 Relembrar hoje</h3>${due.slice(0, 12).map(e => `<div class="nbDueR" data-id="${e.id}"><b>${this.COR[e.cor || ""]} ${esc(e.ti || "(sem título)")}</b><div class="nbTx">${this.md(e.tx || "")}</div><div class="metaRow"><button class="btn sm" data-r="0">🔁 Esqueci</button><button class="btn sm gold" data-r="1">✅ Lembrei (+1 XP)</button></div></div>`).join("")}</div>` : ""}</div>
     <div class="panel nbEd"><h3 style="margin-top:0">${this.ed ? "✏️ Editar nota" : "➕ Nova nota"}</h3>
      <input id="nbTi" placeholder="Título — ex.: Noradrenalina: diluição padrão" value="${esc(E.ti || "")}" maxlength="140">
      <textarea id="nbTx" rows="5" placeholder="O detalhe que você costuma esquecer… (**negrito** funciona)">${esc(E.tx || "")}</textarea>
      <div class="metaRow"><input id="nbTg" placeholder="🏷️ tags (vírgula): dose, uti, prova" value="${esc(E.tg || "")}"><select id="nbCor">${Object.entries(this.COR).map(([k, v]) => `<option value="${k}" ${k === (E.cor || "") ? "selected" : ""}>${v} ${{ "": "sem cor", r: "urgente", o: "importante", y: "atenção", g: "ok", b: "estudo", p: "pessoal" }[k]}</option>`).join("")}</select>
       <label class="chk2"><input type="checkbox" id="nbPin" ${E.pin ? "checked" : ""}> 📌 Fixar</label><label class="chk2"><input type="checkbox" id="nbLem" ${E.lem !== false ? "checked" : ""}> 🔔 Lembrar (revisão espaçada)</label></div>
      <div class="metaRow"><button class="btn gold" id="nbSave">💾 ${this.ed ? "Salvar alterações" : "Salvar nota"}</button>${this.ed ? `<button class="btn" id="nbCancel">✖ Cancelar</button>` : ""}</div></div>
     <div class="panel"><div class="metaRow"><select id="nbF"><option value="">📚 Todas (${all.length})</option><option value="due" ${this.f === "due" ? "selected" : ""}>🔔 Para hoje (${due.length})</option><option value="pin" ${this.f === "pin" ? "selected" : ""}>📌 Fixadas</option><option value="lem" ${this.f === "lem" ? "selected" : ""}>🔔 Com lembrete</option><option value="ce" ${this.f === "ce" ? "selected" : ""}>📕 Vindas do caderno de erros</option></select>
       <select id="nbTag"><option value="">🏷️ Todas as tags</option>${tags.map(t => `<option ${t === this.tg ? "selected" : ""}>${esc(t)}</option>`).join("")}</select><input id="nbQ" class="grow" placeholder="🔎 Buscar nas notas…" value="${esc(this.q)}"><button class="btn sm" id="nbExp" ${all.length ? "" : "disabled"}>📤 Exportar (.md)</button></div>
      <div class="nbGrid">${l.length ? l.slice(0, this.lim).map(e => this.card(e)).join("") : `<p class="empty">${all.length ? "Nada neste filtro." : "🗒️ Nenhuma nota ainda. Escreva acima o primeiro detalhe que costuma esquecer."}</p>`}</div>
      ${l.length > this.lim ? `<div class="metaRow" style="justify-content:center"><button class="btn" id="nbMore">⬇️ Mostrar mais (${l.length - this.lim})</button></div>` : ""}</div>${CAD.foot("🗒️ Caderno de Notas")}`;
    this.bind();
  },
  card(e) {
    const d = e.lem ? (e.due || 0) <= endOfDay() ? `<span class="pill" style="color:var(--amb)">🔔 hoje</span>` : `<span class="pill">🔔 ${new Date(e.due).toLocaleDateString("pt-BR", { day: "2-digit", month: "2-digit" })}</span>` : "";
    return `<div class="nbCard c-${e.cor || "n"}" data-id="${e.id}"><div class="nbHd">${e.pin ? "📌 " : ""}<b>${this.COR[e.cor || ""]} ${esc(e.ti || "(sem título)")}</b></div><div class="nbTx">${this.md(e.tx || "")}</div>
      <div class="nbFt">${(e.tg || "").split(/[,;]\s*/).filter(Boolean).map(t => `<span class="pill">🏷️ ${esc(t)}</span>`).join("")}${d}${e.n ? `<span class="pill">🔁 ${e.n}×</span>` : ""}<span class="grow"></span><button class="btn sm" data-n="pin" title="Fixar">${e.pin ? "📍" : "📌"}</button><button class="btn sm" data-n="copy" title="Copiar">📋</button><button class="btn sm" data-n="edit" title="Editar">✏️</button><button class="btn sm danger" data-n="del" title="Apagar">🗑️</button></div></div>`;
  },
  bind() {
    $("#nbSave").onclick = async () => {
      const ti = $("#nbTi").value.trim(), tx = $("#nbTx").value.trim(); if (!ti && !tx) return toast("Escreva um título ou um texto.");
      const o = { ti: ti || tx.split("\n")[0].slice(0, 80), tx, tg: $("#nbTg").value.trim(), cor: $("#nbCor").value, pin: $("#nbPin").checked, lem: $("#nbLem").checked };
      const isNew = !this.ed; await this.save(o, this.ed || undefined); this.ed = null; if (isNew) addXP(2, "nota", "e"); toast(isNew ? "🗒️ Nota salva (+2 XP)" : "💾 Nota atualizada"); this.render();
    };
    const cc = $("#nbCancel"); if (cc) cc.onclick = () => { this.ed = null; this.render(); };
    $("#nbF").onchange = e => { this.f = e.target.value; this.render(); };
    $("#nbTag").onchange = e => { this.tg = e.target.value; this.render(); };
    let qT; $("#nbQ").oninput = e => { clearTimeout(qT); qT = setTimeout(() => { this.q = e.target.value; this.render(); const i = $("#nbQ"); if (i) { i.focus(); i.setSelectionRange(i.value.length, i.value.length); } }, 250); };
    $("#nbExp").onclick = () => this.exportMd();
    const mo = $("#nbMore"); if (mo) mo.onclick = () => { this.lim += 40; this.render(); };
    $$(".nbDueR").forEach(r => $$("[data-r]", r).forEach(b => b.onclick = () => this.review(r.dataset.id, b.dataset.r === "1")));
    $$(".nbCard").forEach(c => $$("[data-n]", c).forEach(b => b.onclick = async () => {
      const id = c.dataset.id, e = this.R()[id]; if (!e) return; const a = b.dataset.n;
      if (a === "pin") { e.pin = !e.pin; e.mod = Date.now(); await saveLog(); return this.render(); }
      if (a === "copy") return CAD.copy(`${e.ti}\n\n${e.tx}`, "📋 Nota copiada");
      if (a === "edit") { this.ed = id; this.render(); $("#nbTi").focus(); window.scrollTo({ top: $(".nbEd").offsetTop - 70, behavior: "smooth" }); return; }
      if (a === "del") { if (b.dataset.cf !== "1") { b.dataset.cf = "1"; b.textContent = "Apagar?"; return; } await this.rm(id); toast("🗑️ Nota apagada"); return this.render(); }
    }));
  },
  async review(id, ok) {
    const e = this.R()[id]; if (!e) return; const k = ok ? Math.min(this.IV.length - 1, (e.iv || 0) + (e.n ? 1 : 0)) : 0;
    e.iv = k; e.due = Date.now() + this.IV[k] * DAY; e.n = (e.n || 0) + 1; e.mod = Date.now(); const L = L0(); L.nbR = (L.nbR || 0) + 1;
    if (ok) addXP(1, "lembrei", "e"); await saveLog(); toast(ok ? `✅ Volta em ${this.IV[k]} dia(s)` : "🔁 Volta amanhã"); this.render();
  },
  exportMd() {
    const L = this.items(), out = [`# 🗒️ Caderno de Notas 360X`, ``, `_${CAD.CRED}_ · exportado em ${new Date().toLocaleString("pt-BR")} · ${L.length} notas`, ``];
    for (const e of L) out.push(`## ${e.pin ? "📌 " : ""}${this.COR[e.cor || ""]} ${e.ti || "(sem título)"}`, e.tg ? `🏷️ ${e.tg}` : "", ``, e.tx || "", ``);
    CAD.dl(`Caderno_de_Notas_360X_${today()}.md`, out.join("\n")); toast("📤 Notas exportadas");
  }
};

/* ---------------- 💉 Caderno de Prescrições ---------------- */
const PX = {
  AREA: { cm: ["🩺 Clínica Médica", "#4dd4ff"], uti: ["🏥 Medicina Intensiva", "#b48cff"], cardio: ["🫀 Cardiologia", "#ff6b6b"], emerg: ["🚑 Emergência", "#ffc14d"] },
  data: null, area: lsGet("pxArea") || "", cat: "", q: "", f: "", lim: 30, cur: null,
  async load() {
    if (this.data) return;
    try { const r = await fetch("data/prescricoes.json"); if (!r.ok) throw new Error(r.status); this.data = await r.json(); DB.setMeta("px:data", this.data).catch(() => {}); }
    catch (e) { this.data = (await DB.meta("px:data", null).catch(() => null)) || { itens: [] }; }
    this.idx = new Map(this.data.itens.map(p => [p.id, p]));
  },
  R() { return (S.logs._px = S.logs._px || {}); },
  byId(id) { return this.idx ? this.idx.get(id) : null; },
  kg() { const v = parseFloat(String(lsGet("pxKg") || "").replace(",", ".")); return v > 0 && v < 400 ? v : 0; },
  n: (x, d) => { const r = Math.round(x * 10 ** d) / 10 ** d; return r.toLocaleString("pt-BR", { maximumFractionDigits: d }); },
  fmt(s) {   // {kg:dose:unid:máx} → dose por kg; {mlh:mcg/kg/min:mcg/mL} e {mlhh:dose/kg/h:conc/mL} → mL/h; **negrito**
    const kg = this.kg(), n = this.n;
    return esc(s).replace(/\{kg:([\d.]+):([^:}]+?)(?::([\d.]+))?\}/g, (_, d, u, mx) => { d = +d; const tot = kg ? d * kg : 0, cap = mx && tot > +mx; return `<span class="pxDose">${n(d, 3)} ${u}/kg${kg ? ` → <b>${n(cap ? +mx : tot, tot < 10 ? 2 : 1)} ${u}</b>${cap ? " (dose máxima)" : ""}` : ""}${mx && !kg ? ` (máx. ${n(+mx, 2)} ${u})` : ""}</span>`; })
      .replace(/\{mlh:([\d.]+):([\d.]+)\}/g, (_, d, c) => kg ? `<span class="pxDose">≈ <b>${n(+d * kg * 60 / +c, 1)} mL/h</b> a ${n(+d, 3)} mcg/kg/min · ${n(kg, 1)} kg</span>` : `<span class="pxDose mut">(mL/h: informe o peso)</span>`)
      .replace(/\{mlhh:([\d.]+):([\d.]+)\}/g, (_, d, c) => kg ? `<span class="pxDose">≈ <b>${n(+d * kg / +c, 1)} mL/h</b> a ${n(+d, 3)}/kg/h · ${n(kg, 1)} kg</span>` : `<span class="pxDose mut">(mL/h: informe o peso)</span>`)
      .replace(/\*\*(.+?)\*\*/g, "<b>$1</b>");
  },
  txt(s) { const h = this.fmt(s); const d = document.createElement("div"); d.innerHTML = h; return d.textContent.replace(/\s+/g, " ").trim(); },
  rxHTML(p) { return `<ol class="pxRx">${p.rx.map(l => `<li>${this.fmt(l)}</li>`).join("")}</ol>`; },
  list() {
    const qn = CAD.nz(this.q).split(/\s+/).filter(Boolean), R = this.R();
    return (this.data.itens || []).filter(p => (!this.area || p.area === this.area) && (!this.cat || p.cat === this.cat)
      && (!this.f || (this.f === "fav" ? R[p.id] && R[p.id].f : this.f === "nov" ? !(R[p.id] && R[p.id].v) : this.f === "est" ? R[p.id] && R[p.id].v : this.f === "low" ? CF.low("p:" + p.id) : true))
      && (!qn.length || qn.every(w => (p._s || (p._s = CAD.nz([p.ti, p.cat, p.quando, p.rx.join(" "), p.tags || ""].join(" ")))).includes(w))));
  },
  async open() { await this.load(); this.cur ? this.det(this.cur) : this.render(); },
  render() {
    this.cur = null; const all = this.data.itens || [], R = this.R(), est = all.filter(p => R[p.id] && R[p.id].v).length, l = this.list();
    const cats = [...new Set(all.filter(p => !this.area || p.area === this.area).map(p => p.cat))].sort((a, b) => a.localeCompare(b, "pt"));
    const cnt = a => all.filter(p => p.area === a).length;
    $("#pxHost").innerHTML = `<div class="panel cadHero"><h2 style="margin:0 0 4px">💉 Caderno de Prescrições <span class="pxRxSym">℞</span></h2><p class="metaNow" style="margin:0">${all.length} modelos de prescrição detalhados · quando usar · ℞ passo a passo · monitorização · ajustes · contraindicações · alertas</p>
      <div class="pxWarn">⚠️ <b>Modelos para estudo e apoio à decisão.</b> Antes de prescrever: confira alergias, peso, função renal e hepática, interações, gestação e o protocolo da sua instituição. A dose final é responsabilidade do prescritor.</div>
      <div class="stats" style="margin:10px 0"><div class="stat"><b class="n">${est}</b><span>estudadas</span></div><div class="stat"><b style="color:var(--gold2)">${all.length - est}</b><span>inéditas</span></div><div class="stat"><b style="color:var(--cy)">⭐ ${all.filter(p => R[p.id] && R[p.id].f).length}</b><span>favoritas</span></div></div>
      <div class="metaRow"><label>⚖️ Peso do paciente:</label><input id="pxKg" type="number" inputmode="decimal" min="1" max="350" step="0.1" placeholder="kg" value="${this.kg() || ""}" style="width:90px"><span class="metaNow">${this.kg() ? `doses por kg e mL/h calculados para <b>${this.n(this.kg(), 1)} kg</b>` : "preencha para ver doses por kg e vazões em mL/h"}</span><button class="btn sm" id="pxDayB">🎲 Prescrição do dia</button></div></div>
     <div class="panel"><div class="divTabs"><button class="btn ${!this.area ? "gold" : ""}" data-ar="">📚 Todas (${all.length})</button>${Object.entries(this.AREA).map(([k, [nm]]) => `<button class="btn ${k === this.area ? "gold" : ""}" data-ar="${k}">${nm} (${cnt(k)})</button>`).join("")}</div>
      <div class="metaRow"><select id="pxCat"><option value="">Todas as categorias (${cats.length})</option>${cats.map(c => `<option ${c === this.cat ? "selected" : ""}>${esc(c)}</option>`).join("")}</select>
       <select id="pxF"><option value="">🔎 Todas</option><option value="fav" ${this.f === "fav" ? "selected" : ""}>⭐ Favoritas</option><option value="nov" ${this.f === "nov" ? "selected" : ""}>🆕 Não estudadas</option><option value="est" ${this.f === "est" ? "selected" : ""}>✅ Estudadas</option><option value="low" ${this.f === "low" ? "selected" : ""}>🔴 Confiança baixa</option></select>
       <input id="pxQ" class="grow" placeholder="🔎 Buscar: droga, doença, situação (ex.: noradrenalina, CAD, FA)…" value="${esc(this.q)}"></div>
      <p class="metaNow">${l.length} prescrição(ões) neste filtro</p>
      <div class="pxList">${l.slice(0, this.lim).map(p => `<button class="pxItem" data-id="${p.id}" style="--pxc:${this.AREA[p.area][1]}"><span class="pxTi">${R[p.id] && R[p.id].f ? "⭐ " : ""}${R[p.id] && R[p.id].v ? "✅ " : ""}${esc(p.ti)}</span><span class="pxSub">${this.AREA[p.area][0].split(" ")[0]} ${esc(p.cat)} · ${esc(strip(this.txt(p.quando)).slice(0, 120))}</span></button>`).join("") || `<p class="empty">Nada encontrado.</p>`}</div>
      ${l.length > this.lim ? `<div class="metaRow" style="justify-content:center"><button class="btn" id="pxMore">⬇️ Mostrar mais (${l.length - this.lim})</button></div>` : ""}</div>${CAD.foot("💉 Caderno de Prescrições · " + all.length + " modelos")}`;
    $$("#pxHost [data-ar]").forEach(b => b.onclick = () => { this.area = b.dataset.ar; lsSet("pxArea", this.area); this.cat = ""; this.lim = 30; this.render(); });
    $("#pxCat").onchange = e => { this.cat = e.target.value; this.lim = 30; this.render(); };
    $("#pxF").onchange = e => { this.f = e.target.value; this.lim = 30; this.render(); };
    let qT; $("#pxQ").oninput = e => { clearTimeout(qT); qT = setTimeout(() => { this.q = e.target.value; this.lim = 30; this.render(); const i = $("#pxQ"); if (i) { i.focus(); i.setSelectionRange(i.value.length, i.value.length); } }, 250); };
    $("#pxKg").onchange = e => { const v = parseFloat(String(e.target.value).replace(",", ".")); lsSet("pxKg", v > 0 && v < 400 ? String(v) : ""); this.render(); };
    $("#pxDayB").onclick = () => this.day();
    const mo = $("#pxMore"); if (mo) mo.onclick = () => { this.lim += 30; this.render(); };
    $$("#pxHost .pxItem").forEach(b => b.onclick = () => this.det(b.dataset.id));
  },
  det(id) {
    const p = this.byId(id); if (!p) return this.render(); this.cur = id;
    const R = this.R(), st = R[id] || {}, l = this.list(), i = l.findIndex(x => x.id === id), A = this.AREA[p.area], kg = this.kg();
    const sec = (ic, t, v) => v ? `<div class="pxSec"><h3>${ic} ${t}</h3><div>${Array.isArray(v) ? `<ul>${v.map(x => `<li>${this.fmt(x)}</li>`).join("")}</ul>` : this.fmt(v)}</div></div>` : "";
    $("#pxHost").innerHTML = `<div class="metaRow"><button class="btn sm" id="pxBack">◀ Lista</button><span class="pill" style="color:${A[1]}">${A[0]}</span><span class="pill">${esc(p.cat)}</span><span class="pill">${p.id}</span><span class="grow"></span><span class="metaNow">${i >= 0 ? `${i + 1}/${l.length}` : ""}</span></div>
      <div class="panel pxDet" style="border-top:3px solid ${A[1]}"><h2 style="margin-top:0">💉 ${esc(p.ti)}</h2>
       <div class="metaRow"><label>⚖️ Peso:</label><input id="pxKg2" type="number" inputmode="decimal" min="1" max="350" step="0.1" placeholder="kg" value="${kg || ""}" style="width:90px"><span class="metaNow">${kg ? `cálculos para ${this.n(kg, 1)} kg` : "informe para calcular doses/kg e mL/h"}</span></div>
       ${sec("🎯", "Quando usar", p.quando)}
       <div class="pxSec pxRxBox"><h3>℞ Prescrição</h3>${this.rxHTML(p)}</div>
       ${sec("📈", "Monitorização e metas", p.mon)}${sec("⚖️", "Ajustes (renal, hepático, idoso, gestação)", p.aj)}${sec("⛔", "Contraindicações / quando não usar", p.ci)}${sec("⚠️", "Alertas, erros comuns e pegadinhas", p.al)}
       ${p.ref ? `<div class="qzRef">📚 ${esc(p.ref)} · referência citada de memória — confira a versão vigente</div>` : ""}
       <div class="pxWarn sm">⚠️ Modelo de estudo: ajuste ao paciente e ao protocolo local.</div>
       <div class="metaRow"><button class="btn gold" id="pxCopy">📋 Copiar prescrição</button><button class="btn" id="pxFav">${st.f ? "⭐ Favorita" : "☆ Favoritar"}</button>${st.v ? `<span class="chk on">✅ Estudada</span>` : `<button class="btn" id="pxStudy">☑️ Estudei esta prescrição (+2 XP)</button>`}<button class="btn" id="pxNote">🗒️ Criar nota</button></div>
       ${CF.box("p:" + p.id, { pri: 1 })}</div>
      <div class="metaRow" style="justify-content:center"><button class="btn" id="pxPrev" ${i > 0 ? "" : "disabled"}>◀ Anterior</button><button class="btn gold" id="pxNext" ${i >= 0 && i < l.length - 1 ? "" : "disabled"}>Próxima ▶</button></div>${CAD.foot("💉 Caderno de Prescrições")}`;
    $("#pxBack").onclick = () => this.render();
    $("#pxKg2").onchange = e => { const v = parseFloat(String(e.target.value).replace(",", ".")); lsSet("pxKg", v > 0 && v < 400 ? String(v) : ""); this.det(id); };
    $("#pxCopy").onclick = () => CAD.copy(this.plain(p), "📋 Prescrição copiada — revise antes de usar");
    $("#pxFav").onclick = async () => { const e = R[id] = R[id] || {}; e.f = e.f ? 0 : Date.now(); e.mod = Date.now(); await saveLog(); this.det(id); };
    const sb = $("#pxStudy"); if (sb) sb.onclick = async () => { const e = R[id] = R[id] || {}; e.v = Date.now(); e.mod = Date.now(); const L = L0(); L.pxN = (L.pxN || 0) + 1; addXP(2, "prescrição", "e"); await saveLog(); this.det(id); };
    $("#pxNote").onclick = async () => { await NB.save({ ti: "💉 " + p.ti.slice(0, 120), tx: "✍️ \n\n" + this.plain(p).slice(0, 2500), tg: "prescrição", src: "px" }); toast(`🗒️ Nota criada · <a href="#notas" style="color:var(--gold2)">abrir</a>`); };
    const pv = $("#pxPrev"), nx = $("#pxNext"); if (pv) pv.onclick = () => l[i - 1] && this.det(l[i - 1].id); if (nx) nx.onclick = () => l[i + 1] && this.det(l[i + 1].id);
    window.scrollTo({ top: 0 });
  },
  plain(p) {
    const kg = this.kg(), L = [`${p.ti}`, `(${this.AREA[p.area][0].replace(/^\S+\s/, "")} · ${p.cat}${kg ? ` · peso ${this.n(kg, 1)} kg` : ""})`, ``, `QUANDO USAR: ${this.txt(p.quando)}`, ``, `PRESCRIÇÃO:`];
    p.rx.forEach((x, i) => L.push(`${i + 1}. ${this.txt(x)}`));
    for (const [t, v] of [["MONITORIZAÇÃO", p.mon], ["AJUSTES", p.aj], ["CONTRAINDICAÇÕES", p.ci], ["ALERTAS", p.al]]) if (v) L.push(``, `${t}: ${Array.isArray(v) ? v.map(x => this.txt(x)).join(" · ") : this.txt(v)}`);
    L.push(``, `⚠️ Modelo de estudo — conferir alergias, função renal/hepática, interações e protocolo local.`, `Fonte: Caderno de Prescrições 360X · ${CAD.CRED}`);
    return L.join("\n");
  },
  async go(id) { await this.load(); this.cur = id; if (location.hash !== "#prescricoes") location.hash = "prescricoes"; else this.det(id); },
  async day() { await this.load(); const all = this.data.itens || [], R = this.R(), nov = all.filter(p => !(R[p.id] && R[p.id].v)), pool = nov.length ? nov : all; if (!pool.length) return; let h = 0; for (const ch of today()) h = (h * 31 + ch.charCodeAt(0)) >>> 0; this.go(pool[h % pool.length].id); }
};
