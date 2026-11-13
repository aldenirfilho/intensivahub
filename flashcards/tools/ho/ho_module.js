
/* ---------------- 🕊️ Honra: guia espiritual, bússolas de decisão e fluxo ----------------
   Dados em data/honra.json (gerado por tools/ho/build_ho.py). Cópia no aparelho para abrir sem internet.
   Progresso em S.logs._h (mesmo formato de _n: n, ok, s, t, f, u) — sincroniza junto com os registros.
   Registro do dia: hN (treinos), hb (sessões de respiração), hf (filtros), hbu (bússolas), hz1–hz3 (exame da noite), hn (Modo Noite concluído), hg (gratidão/intenção).
   Itens próprios (✍️ Meus) em S.logs._hu: { id: { k: "m"|"b", d: {...}, mod, del } } — vence o mod mais recente. */
const HRES = () => (S.logs._h = S.logs._h || {}), HURES = () => (S.logs._hu = S.logs._hu || {});
const HO = { sub: lsGet("hoSub") || "hoje", data: null, tr: "", tema: "", filt: "", q: "", mode: "lista", lim: 24, cur: null, shown: false, hint: false, sess: { n: 0, ok: 0 },
  bu: null, fa: {}, fDone: false, msg: null, br: null,
  SUBS: [["hoje", "📜 Hoje"], ["noite", "🌙 Noite"], ["cards", "🎴 Cards"], ["mn", "🛡️ Mnemônicos"], ["bussola", "🧭 Bússolas"], ["filtro", "⚖️ Filtro"], ["fluxo", "🌬️ Fluxo"], ["meus", "✍️ Meus"]],
  ed: null, nt: null,
  nz: s => String(s || "").normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase(),
  async load() {
    if (this.data) return;
    try { const r = await fetch("data/honra.json"); if (!r.ok) throw new Error(r.status); this.data = await r.json(); DB.setMeta("ho:data", this.data).catch(() => {}); }
    catch (e) { this.data = (await DB.meta("ho:data", null).catch(() => null)) || { cards: [], mn: [], bu: [], filtro: [], temas: [], trads: {} }; }
  },
  async open() { await this.load(); this.render(); },
  st(id) { return HRES()[id] || {}; },
  dom(id) { return (this.st(id).s || 0) >= 2; },
  fav(id) { const e = this.st(id); return (e.f || 0) > (e.u || 0); },
  T(k) { return (this.data.trads || {})[k] || { n: k, e: "📖", c: "#9aa4b2" }; },
  chip(k) { const t = this.T(k); return `<span class="hoTr" style="border-color:${t.c};color:${t.c}">${t.e} ${esc(t.n)}</span>`; },
  mine(k) { return Object.entries(HURES()).filter(([, e]) => e && e.k === k && !e.del && e.d).map(([id, e]) => Object.assign({}, e.d, { id, o: "u", mod: e.mod })); },
  mnAll() { return this.mine("m").concat(this.data.mn); },
  buAll() { return this.mine("b").concat(this.data.bu); },
  all() { return this.sub === "mn" ? this.mnAll() : this.data.cards; },
  list() {
    const q = this.nz(this.q).trim(), f = this.filt, mnK = this.sub === "mn";
    return this.all().filter(x => (!this.tema || x.tema === this.tema) && (mnK || !this.tr || x.tr === this.tr)
      && (!f || (f === "fav" && this.fav(x.id)) || (f === "pend" && !this.dom(x.id)) || (f === "dom" && this.dom(x.id)) || (f === "c" && x.o === "c") || (f === "o" && x.o === "o") || (f === "u" && x.o === "u"))
      && (!q || this.nz(mnK ? x.t + " " + x.m + " " + x.k.map(k => k.join(" ")).join(" ") + " " + (x.x || "") + " " + (x.c || "") : x.q + " " + x.a + " " + x.r + " " + x.ap + " " + this.T(x.tr).n).includes(q)));
  },
  favBtn(id) { return `<button class="mnFav" data-fav="${id}" title="Favoritar" aria-label="Favoritar">${this.fav(id) ? "⭐" : "☆"}</button>`; },
  foot(id) { const e = this.st(id); return e.n ? `<div class="mnFoot">${this.dom(id) ? "✅ Dominado" : "🎯 Em treino"} · ${e.n} treino(s), ${e.ok || 0} acerto(s)</div>` : ""; },
  back(c) { return `<div class="hoA">${esc(c.a)}</div><div class="hoRef">📍 ${esc(c.r)} <small>· paráfrase 360X</small></div><div class="hoAp"><b>🧭 Faça hoje</b>${esc(c.ap)}</div>`; },
  cardC(c) {
    return `<div class="mnCard hoCard${this.dom(c.id) ? " dom" : ""}"><div class="mcTop">${this.chip(c.tr)}<span class="mnTools"><span class="pill">${esc(c.tema)}</span>${this.favBtn(c.id)}</span></div>
      <div class="mnTit">${esc(c.q)}</div>${this.back(c)}${this.foot(c.id)}</div>`;
  },
  cardM(m) {
    return `<div class="mnCard${this.dom(m.id) ? " dom" : ""}"><div class="mcTop"><span class="pill">${esc(m.tema)}</span><span class="mnTools">${this.orig(m)}${this.favBtn(m.id)}</span></div>
      <div class="mnTit">${esc(m.t)}</div>${MN.sig(m)}${MN.body(m)}${this.foot(m.id)}</div>`;
  },
  orig(m) { return m.o === "u" ? `<span class="mnOrig u" title="Criado por você">✍️ Meu</span>` : MN.orig(m);
  },
  tabs() { return `<div class="hoSubs">${this.SUBS.map(([k, l]) => `<button class="btn ${k === this.sub ? "gold" : ""}" data-sub="${k}">${l}</button>`).join("")}</div>`; },
  head() {
    const D = this.data, mnK = this.sub === "mn", all = this.all(), nDom = all.filter(x => this.dom(x.id)).length, nFav = all.filter(x => this.fav(x.id)).length, hoje = (S.logs[today()] || {}).hN || 0;
    const temas = D.temas.concat(all.map(x => x.tema).filter(t => !D.temas.includes(t))).filter((t, i, a) => a.indexOf(t) === i && all.some(x => x.tema === t));
    const F = [["", "Todos"], ["pend", "🎯 Ainda não dominados"], ["dom", "✅ Dominados"], ["fav", "⭐ Favoritos"]].concat(mnK ? [["c", "🏛️ Clássicos das tradições"], ["o", "⚒️ Criados no 360X"], ["u", "✍️ Meus"]] : []);
    return `<div class="metaRow"><button class="btn ${this.mode === "lista" ? "cy" : ""}" data-mode="lista">📖 Consultar</button><button class="btn ${this.mode === "treino" ? "cy" : ""}" data-mode="treino">🎲 Treinar</button>
      <span class="metaNow">🕊️ Dominados: <b>${nDom}</b>/${all.length} · ⭐ ${nFav} · hoje: ${hoje} treino(s)</span></div>
     <div class="progress"><i style="width:${all.length ? 100 * nDom / all.length : 0}%"></i></div>
     <div class="mnBar">${mnK ? "" : `<select id="hoTr"><option value="">Todas as tradições (${all.length})</option>${Object.entries(D.trads).map(([k, t]) => `<option value="${k}" ${k === this.tr ? "selected" : ""}>${t.e} ${esc(t.n)} (${all.filter(x => x.tr === k).length})</option>`).join("")}</select>`}
      <select id="hoTema"><option value="">Todos os temas</option>${temas.map(t => `<option ${t === this.tema ? "selected" : ""} value="${esc(t)}">${esc(t)} (${all.filter(x => x.tema === t).length})</option>`).join("")}</select>
      <select id="hoFilt">${F.map(([v, l]) => `<option value="${v}" ${v === this.filt ? "selected" : ""}>${l}</option>`).join("")}</select>
      ${this.mode === "lista" ? `<input type="search" id="hoQ" placeholder="🔎 Buscar palavra, livro ou referência" value="${esc(this.q)}">` : ""}</div>`;
  },
  pool() {
    const l = this.list(), show = l.slice(0, this.lim), mnK = this.sub === "mn";
    return l.length ? `<p class="metaNow">${l.length} ${mnK ? "mnemônico(s)" : "card(s)"} neste filtro${mnK ? " · 🏛️ lista clássica da tradição · ⚒️ sigla criada aqui" : " · textos parafraseados, com a referência para conferir no original"}</p>
      <div class="mnGrid">${show.map(x => mnK ? this.cardM(x) : this.cardC(x)).join("")}</div>
      ${l.length > show.length ? `<div class="metaRow" style="justify-content:center"><button class="btn" id="hoMore">⬇️ Mostrar mais (${l.length - show.length} restantes)</button></div>` : ""}` : `<p class="empty">Nada neste filtro.</p>`;
  },
  train() {
    const x = this.cur, l = this.list(), mnK = this.sub === "mn";
    if (!x) return `<p class="empty">Nada neste filtro para treinar.</p>`;
    const top = mnK ? `<div class="mcTop"><span class="pill">${esc(x.tema)}</span><span class="mnTools">${this.orig(x)}${this.favBtn(x.id)}</span></div>`
      : `<div class="mcTop">${this.chip(x.tr)}<span class="mnTools"><span class="pill">${esc(x.tema)}</span>${this.favBtn(x.id)}</span></div>`;
    const ses = `<p class="metaNow" style="text-align:center">Sessão: <b>${this.sess.ok}</b> lembrado(s) de ${this.sess.n} · ${l.length} no filtro · ⌨️ <span class="kbd">Espaço</span> revelar · <span class="kbd">1</span> <span class="kbd">2</span> <span class="kbd">3</span> responder</p>`;
    const q = mnK ? `<div class="mnAsk">🛡️ Qual é o mnemônico?</div><div class="mnTit">${esc(x.t)}</div>` : `<div class="mnAsk">🕊️ O que ensina?</div><div class="mnTit">${esc(x.q)}</div>`;
    if (!this.shown) return `<div class="mnCard mnTrain">${top}${q}
      ${this.hint ? (mnK ? MN.sig(x) : `<div class="hoRef" style="text-align:center">📍 ${esc(x.r)}</div>`) : ""}
      <div class="mnAns">${this.hint ? "" : `<button class="btn" id="hoHint">💡 ${mnK ? "Mostrar só a sigla" : "Mostrar a referência"}</button>`}<button class="btn gold" id="hoShow">👁️ Revelar</button></div></div>${ses}`;
    return `<div class="mnCard mnTrain">${top}${q}${mnK ? MN.sig(x) + MN.body(x) : this.back(x)}
      <div class="mnAns"><button class="btn danger" data-g="0">❌ Não lembrei</button><button class="btn" data-g="1">🟡 Em parte (+1 XP)</button><button class="btn gold" data-g="2">✅ Lembrei (+2 XP)</button></div></div>${ses}`;
  },
  pick() {
    const l = this.list().filter(x => !this.cur || x.id !== this.cur.id), R = HRES();
    if (!l.length) { this.cur = this.list()[0] || null; this.hint = this.shown = false; return; }
    const sc = x => { const e = R[x.id]; return e && e.n ? (e.s || 0) * 1e13 + (e.t || 0) : -1; };
    const ord = l.map(x => [sc(x), Math.random(), x]).sort((a, b) => a[0] - b[0] || a[1] - b[1]);
    const pool = ord[0][0] < 0 ? ord.filter(y => y[0] < 0) : ord.slice(0, Math.min(5, ord.length));
    this.cur = pool[Math.floor(Math.random() * pool.length)][2]; this.hint = this.shown = false;
  },
  answer(g) {
    const x = this.cur; if (!x || !this.shown) return;
    const R = HRES(), e = R[x.id] = Object.assign({}, R[x.id] || {}), L = L0(), was = (e.s || 0) >= 2;
    e.n = (e.n || 0) + 1; e.t = Date.now();
    if (g === 2) { e.ok = (e.ok || 0) + 1; e.s = (e.s || 0) + 1; } else e.s = g === 1 ? Math.min(e.s || 0, 1) : 0;
    L.hN = (L.hN || 0) + 1; this.sess.n++; if (g === 2) this.sess.ok++;
    if (g) addXP(g, "honra", "h");
    if (!was && e.s >= 2) toast("🕊️ Dominado!");
    saveLog(); this.pick(); this.render();
  },
  toggleFav(id, btn) { const R = HRES(), e = R[id] = Object.assign({}, R[id] || {}), on = (e.f || 0) > (e.u || 0); e[on ? "u" : "f"] = Date.now(); if (btn) btn.textContent = on ? "☆" : "⭐"; saveLog(); },
  dayIdx(n) { const d = today(); let h = 0; for (const ch of d) h = (h * 31 + ch.charCodeAt(0)) >>> 0; return h % n; },
  hoje() {
    const D = this.data, L = S.logs[today()] || {}, c = this.msg, nDomC = D.cards.filter(x => this.dom(x.id)).length, nDomM = this.mnAll().filter(x => this.dom(x.id)).length, BU = this.buAll();
    const Z = [["hz1", "🤝 Fui leal ao agir pelos outros?"], ["hz2", "🫱 Fui digno de confiança com quem convivo?"], ["hz3", "📖 Pratiquei o que aprendi?"]];
    return `<div class="hoHero"><div class="hoBrasao">🕊️</div><div><h2 style="margin:0">Honra & Guia Espiritual</h2><p class="metaNow" style="margin:4px 0 0">${D.cards.length} cards de 6 tradições · ${this.mnAll().length} mnemônicos de honra · ${BU.length} bússolas · filtro de decisão · respiração</p></div></div>
     <div class="panel hoPanel hoNtCall"><div><b>🌙 Modo Noite · 5 minutos</b><br><span class="metaNow">Respiração → exame → mensagem → gratidão → bênção. ${L.hn ? "✅ Feito hoje." : ""}</span></div><button class="btn gold" data-sub="noite">▶️ Começar</button></div>
     <div class="panel hoPanel"><h3 style="margin-top:0">🧭 Como você está agora?</h3><p class="metaNow">Toque no que mais se parece com o momento — abre a bússola daquela situação.</p>
      <div class="hoChips">${BU.map(b => `<button class="hoChip" data-bu="${b.id}">${b.e} ${esc(b.t)}</button>`).join("")}</div></div>
     <div class="panel hoPanel"><h3 style="margin-top:0">📜 Mensagem de hoje</h3>
      ${c ? `<div class="mnCard hoCard">${`<div class="mcTop">${this.chip(c.tr)}<span class="pill">${esc(c.tema)}</span></div>`}<div class="mnTit">${esc(c.q)}</div>${this.back(c)}</div>
        <div class="metaRow" style="justify-content:center"><button class="btn" id="hoMsg2">🔄 Outra mensagem</button></div>` : `<div class="metaRow"><button class="btn gold" id="hoMsg">📜 Mostrar a mensagem de hoje</button><span class="metaNow">Aparece só quando você pedir.</span></div>`}</div>
     <div class="grid2">
      <div class="panel hoPanel"><h3 style="margin-top:0">🌙 Exame da noite (Zengzi)</h3><p class="metaNow">Analectos 1:4 — três perguntas antes de dormir. +1 XP cada.</p>
       ${Z.map(([k, l]) => `<label class="hoChk"><input type="checkbox" data-hz="${k}" ${L[k] ? "checked disabled" : ""}> ${l}</label>`).join("")}</div>
      <div class="panel hoPanel"><h3 style="margin-top:0">📊 Seu caminho</h3>
       <div class="hoStat"><b>${nDomC}</b><span>cards dominados de ${D.cards.length}</span></div><div class="hoStat"><b>${nDomM}</b><span>mnemônicos dominados de ${this.mnAll().length}</span></div>
       <div class="hoStat"><b>${L.hb || 0}</b><span>respirações guiadas hoje</span></div><div class="hoStat"><b>${(L.hf || 0) + (L.hbu || 0)}</b><span>bússolas e filtros usados hoje</span></div></div></div>
     <p class="foot">🛡️ Conteúdo de reflexão e formação de caráter, com respeito a cada tradição; os textos são paráfrases com referência para conferir no original. 📖 Numeração: Bíblia e Salmos como na Almeida (hebraica; Bíblias católicas numeram vários Salmos com 1 a menos) · Alcorão na numeração padrão de Kufa (a da tradução de Helmi Nasr) · Analectos: número moderno (ctext) e, entre parênteses, o de James Legge. Não substitui orientação religiosa, psicológica, médica ou jurídica. Em sofrimento intenso: <b>CVV 188</b> (24 h) · <b>SAMU 192</b>.</p>`;
  },
  bussola() {
    const D = this.data, BU = this.buAll(), b = BU.find(x => x.id === this.bu);
    const chips = `<div class="hoChips">${BU.map(x => `<button class="hoChip${x.id === this.bu ? " on" : ""}" data-bu="${x.id}">${x.e} ${esc(x.t)}</button>`).join("")}</div>`;
    if (!b) return `<div class="panel hoPanel"><h3 style="margin-top:0">🧭 Escolha a situação</h3>${chips}</div>`;
    const mns = (b.mn || []).map(s => this.mnAll().find(m => m.m === s)).filter(Boolean), used = ((S.logs[today()] || {}).hbuL || "").split(",").includes(b.id);
    return `<div class="hoComp"><div class="hoCompT">${b.e} ${esc(b.t)}</div><div class="hoSin">🔎 <b>Sinais:</b> ${esc(b.sin)}</div>
       ${b.al ? `<div class="hoAl">${esc(b.al)}</div>` : ""}
       <div class="hoRose"><div class="hoDir dn"><b>⬆️ Norte · princípio</b>${esc(b.N)}</div><div class="hoDir do"><b>⬅️ Oeste · espere e consulte</b>${esc(b.O)}</div>
        <div class="hoCenter"><span>🧭</span><i>${esc(b.q)}</i></div><div class="hoDir dl"><b>➡️ Leste · faça agora</b>${esc(b.L)}</div><div class="hoDir ds"><b>⬇️ Sul · evite</b>${esc(b.S)}</div></div>
       <div class="hoRefs"><b>📍 Fontes:</b> ${(b.refs || []).map(r => `<button class="hoRefB" data-ref="${esc(r.split(" (")[0])}">${esc(r)}</button>`).join("")}</div>
       <div class="metaRow" style="justify-content:flex-end">${b.o === "u" ? `<span class="mnOrig u">✍️ Minha bússola</span><button class="btn" data-edit="${b.id}">✏️ Editar</button>` : `<a class="btn" href="data/media/honra/${b.id}.jpg" target="_blank" rel="noopener" download="Bussola_360X_${b.id}.jpg">🖼️ Cartão para tela de bloqueio</a>`}${used ? `<span class="chk on">✅ Bússola usada hoje</span>` : `<button class="btn gold" id="hoBuOk">☑️ Usei esta bússola (+2 XP)</button>`}</div></div>
     ${mns.length ? `<h3>🛡️ Mnemônicos desta bússola</h3><div class="mnGrid">${mns.map(m => this.cardM(m)).join("")}</div>` : ""}
     <div class="panel hoPanel"><h3 style="margin-top:0">Outras situações</h3>${chips}</div>`;
  },
  filtro() {
    const F = this.data.filtro, A = this.fa, ans = F.filter((_, i) => A[i] != null).length;
    let good = 0, tot = 0, red = [];
    F.forEach((f, i) => { if (A[i] == null) return; tot += f.w; if (A[i] === f.ok) good += f.w; else if (!f.ok && f.w >= 3) red.push(f.q); });
    const pct = tot ? Math.round(100 * good / tot) : 0;
    let v = "";
    if (ans === F.length) v = red.length ? `<div class="hoVer r">🔴 <b>Pare.</b> Sinal de alerta: ${red.map(esc).join(" · ")}<br>Não decida hoje. Verifique por outro canal e fale com alguém de confiança.</div>`
      : pct >= 85 ? `<div class="hoVer g">🟢 <b>Sinal verde (${pct}%).</b> Decisão bem fundamentada. Registre o porquê e siga em paz.</div>`
      : `<div class="hoVer y">🟡 <b>Espere 24–72 h (${pct}%).</b> Consulte alguém de confiança e responda de novo amanhã.</div>`;
    return `<div class="panel hoPanel"><h3 style="margin-top:0">⚖️ Filtro de Qualidade da Decisão 360X</h3><p class="metaNow">Pense numa decisão concreta e responda com honestidade. ${ans}/${F.length} respondidas.</p>
      ${F.map((f, i) => `<div class="hoFq"><span>${i + 1}. ${esc(f.q)}${f.w >= 3 ? " <b title=\"Peso alto\">⚠️</b>" : ""}</span><span class="hoYN"><button class="btn sm ${A[i] === true ? "cy" : ""}" data-fa="${i}" data-v="1">Sim</button><button class="btn sm ${A[i] === false ? "cy" : ""}" data-fa="${i}" data-v="0">Não</button></span></div>`).join("")}
      ${v}<div class="metaRow" style="justify-content:flex-end"><button class="btn" id="hoFReset">🔄 Novo filtro</button>${v && !this.fDone ? `<button class="btn gold" id="hoFOk">☑️ Registrar (+2 XP)</button>` : this.fDone ? `<span class="chk on">✅ Registrado</span>` : ""}</div></div>
     <p class="foot">Pergunta-mãe: <b>HONRA</b> — Honesto? Outros afetados? Necessário agora? Reversível? Alinhado aos valores? · Dois ⚠️ marcados no lado errado = golpe ou impulso até prova em contrário.</p>`;
  },
  MODES: { caixa: ["🟦 Caixa 4-4-4-4", [["Inspire", 4], ["Segure", 4], ["Expire", 4], ["Segure", 4]]], calma: ["🌊 Calmante 4-6", [["Inspire", 4], ["Expire", 6]]], suspiro: ["😮‍💨 Suspiro duplo", [["Inspire", 2], ["Mais um pouco", 1], ["Expire devagar", 6]]] },
  ANCORAS: ["Aquietai-vos (Salmos 46:10)", "Com a dificuldade vem a facilidade (Alcorão 94:5)", "Inspirando, sei que inspiro (MN 118)", "Paz à tua alma (D&C 121:7)", "O sábio não se angustia (Analectos 9:29)", "O Senhor te dê a paz (Números 6:26)", "Basta a cada dia o seu mal (Mateus 6:34)"],
  fluxo() {
    const m = lsGet("hoBr") || "calma", n = +(lsGet("hoBrN") || 6), b = this.br;
    return `<div class="panel hoPanel"><h3 style="margin-top:0">🌬️ Fluxo & Respiração</h3>
      <p class="metaNow">Aqui, "fluxo" é regular respiração e atenção: expirar mais longo que inspirar ajuda o corpo a sair do modo de alerta. Técnica de relaxamento, não tratamento.</p>
      <div class="metaRow">${Object.entries(this.MODES).map(([k, v]) => `<button class="btn ${k === m ? "cy" : ""}" data-br="${k}" ${b ? "disabled" : ""}>${v[0]}</button>`).join("")}
       <select id="hoBrN" ${b ? "disabled" : ""}>${[3, 6, 10, 15].map(x => `<option ${x === n ? "selected" : ""} value="${x}">${x} ciclos</option>`).join("")}</select></div>
      <div class="hoBreath"><div class="hoOrb" id="hoOrb"><span id="hoPh">${b ? "" : "Pronto"}</span><small id="hoCt"></small></div><div class="hoAnc" id="hoAnc">${esc(this.ANCORAS[this.dayIdx(this.ANCORAS.length)])}</div></div>
      <div class="metaRow" style="justify-content:center">${b ? `<button class="btn danger" id="hoBrStop">⏹️ Parar</button>` : `<button class="btn gold" id="hoBrGo">▶️ Começar (+3 XP ao concluir)</button>`}</div></div>`;
  },
  brStart(m, n, onDone) {
    m = m || lsGet("hoBr") || "calma"; n = n || +(lsGet("hoBrN") || 6); const ph = this.MODES[m][1];
    this.br = { m, n, c: 0, i: 0, t: 0, sub: this.sub, onDone }; this.render(true); this.brStep(ph);
  },
  brStep(ph) {
    const b = this.br; if (!b || location.hash !== "#honra" || this.sub !== b.sub) { this.br = null; return; }
    if (b.i >= ph.length) { b.i = 0; b.c++; if (b.c % 2 === 0) { const a = $("#hoAnc"); if (a) a.textContent = this.ANCORAS[(this.dayIdx(this.ANCORAS.length) + b.c / 2) % this.ANCORAS.length]; } }
    if (b.c >= b.n) { this.br = null; const L = L0(); L.hb = (L.hb || 0) + 1; addXP(3, "respiração", "h"); saveLog(); if (b.onDone) return b.onDone(); toast("🌬️ Respiração concluída. Que a paz te acompanhe."); this.render(); return; }
    const [lab, sec] = ph[b.i], orb = $("#hoOrb"), p = $("#hoPh"), ct = $("#hoCt");
    if (!orb) { this.br = null; return; }
    const sc = /Inspire|Mais/.test(lab) ? (lab === "Mais um pouco" ? 1.18 : 1.1) : /Expire/.test(lab) ? 0.62 : null;
    orb.style.transitionDuration = sec + "s"; if (sc) orb.style.transform = `scale(${sc})`;
    p.textContent = lab; let left = sec; ct.textContent = `${left}s · ciclo ${b.c + 1}/${b.n}`;
    clearInterval(b.iv); b.iv = setInterval(() => { left--; if (left > 0 && ct) ct.textContent = `${left}s · ciclo ${b.c + 1}/${b.n}`; }, 1000);
    b.t = setTimeout(() => { clearInterval(b.iv); b.i++; this.brStep(ph); }, sec * 1000);
  },
  brStop() { const b = this.br; if (b) { clearTimeout(b.t); clearInterval(b.iv); } this.br = null; this.render(); },
  render(force) {
    if (!this.data) return;
    const host = $("#hoHost"); if (!host) return;
    if (this.br && this.sub !== this.br.sub) this.brStop();
    let body = "";
    if (this.sub === "hoje") body = this.hoje();
    else if (this.sub === "bussola") body = this.bussola();
    else if (this.sub === "filtro") body = this.filtro();
    else if (this.sub === "meus") body = this.meus();
    else if (this.sub === "noite") { if (this.br && this.br.sub === "noite" && $("#hoOrb") && !force) return; body = this.noite(); }
    else if (this.sub === "fluxo") { if (this.br && $("#hoOrb") && !force) return; body = this.fluxo(); }
    else { if (this.mode === "treino" && (!this.cur || !this.list().some(x => x.id === this.cur.id))) this.pick(); body = this.head() + (this.mode === "treino" ? this.train() : this.pool()); }
    host.innerHTML = this.tabs() + body;
    this.bind();
  },
  go(sub) { this.sub = sub; lsSet("hoSub", sub); this.lim = 24; this.cur = null; this.sess = { n: 0, ok: 0 }; this.render(); const h = $("#hoHost"); if (h) h.scrollIntoView({ block: "start" }); },
  bind() {
    const host = $("#hoHost"), $h = s => $(s, host);
    $$("[data-sub]", host).forEach(b => b.onclick = () => { if (this.br) this.brStop(); this.go(b.dataset.sub); });
    $$("[data-mode]", host).forEach(b => b.onclick = () => { this.mode = b.dataset.mode; this.lim = 24; this.cur = null; this.sess = { n: 0, ok: 0 }; this.render(); });
    const tr = $h("#hoTr"), t = $h("#hoTema"), f = $h("#hoFilt"), q = $h("#hoQ"), more = $h("#hoMore"), hint = $h("#hoHint"), show = $h("#hoShow");
    if (tr) tr.onchange = e => { this.tr = e.target.value; this.lim = 24; this.cur = null; this.render(); };
    if (t) t.onchange = e => { this.tema = e.target.value; this.lim = 24; this.cur = null; this.render(); };
    if (f) f.onchange = e => { this.filt = e.target.value; this.lim = 24; this.cur = null; this.render(); };
    if (q) q.oninput = e => { this.q = e.target.value; this.lim = 24; clearTimeout(this._qt); this._qt = setTimeout(() => { this.render(); const n = $("#hoQ"); if (n) { n.focus(); n.setSelectionRange(n.value.length, n.value.length); } }, 250); };
    if (more) more.onclick = () => { this.lim += 24; this.render(); };
    if (hint) hint.onclick = () => { this.hint = true; this.render(); };
    if (show) show.onclick = () => { this.shown = true; this.render(); };
    $$("[data-g]", host).forEach(b => b.onclick = () => this.answer(+b.dataset.g));
    $$("[data-fav]", host).forEach(b => b.onclick = () => this.toggleFav(b.dataset.fav, b));
    $$("[data-bu]", host).forEach(b => b.onclick = () => { this.bu = b.dataset.bu; this.go("bussola"); });
    $$("[data-ref]", host).forEach(b => b.onclick = () => { this.q = b.dataset.ref; this.tr = ""; this.tema = ""; this.filt = ""; this.mode = "lista"; this.go("cards"); });
    const bo = $h("#hoBuOk"); if (bo) bo.onclick = () => { const L = L0(), ids = (L.hbuL || "").split(",").filter(Boolean); if (ids.includes(this.bu)) return; ids.push(this.bu); L.hbuL = ids.join(","); L.hbu = ids.length; addXP(2, "bússola", "h"); saveLog(); this.render(); };
    const m1 = $h("#hoMsg"), m2 = $h("#hoMsg2"), C = this.data.cards;
    if (m1) m1.onclick = () => { this.msg = C[this.dayIdx(C.length)]; this.render(); };
    if (m2) m2.onclick = () => { this.msg = C[Math.floor(Math.random() * C.length)]; this.render(); };
    $$("[data-hz]", host).forEach(c => c.onchange = () => { if (!c.checked) return; const L = L0(); if (L[c.dataset.hz]) return; L[c.dataset.hz] = 1; addXP(1, "exame da noite", "h"); saveLog(); c.disabled = true; });
    $$("[data-fa]", host).forEach(b => b.onclick = () => { this.fa[+b.dataset.fa] = b.dataset.v === "1"; this.render(); });
    const fr = $h("#hoFReset"), fo = $h("#hoFOk");
    if (fr) fr.onclick = () => { this.fa = {}; this.fDone = false; this.render(); };
    if (fo) fo.onclick = () => { this.fDone = true; const L = L0(); L.hf = (L.hf || 0) + 1; addXP(2, "filtro de decisão", "h"); saveLog(); this.render(); };
    $$("[data-br]", host).forEach(b => b.onclick = () => { lsSet("hoBr", b.dataset.br); this.render(); });
    const bn = $h("#hoBrN"); if (bn) bn.onchange = e => lsSet("hoBrN", e.target.value);
    const bg = $h("#hoBrGo"), bs = $h("#hoBrStop");
    if (bg) bg.onclick = () => this.brStart();
    this.bindMeus(host); this.bindNoite(host);
    if (bs) bs.onclick = () => this.brStop();
  },
  /* ---- ✍️ Meus: criar e editar mnemônicos e bússolas próprios ---- */
  meus() {
    const E = this.ed || (this.ed = { k: "m" }), mns = this.mine("m"), bus = this.mine("b"), T = this.data.temas.concat(["✍️ Pessoal"]);
    const v = k => esc(E[k] == null ? "" : E[k]), inp = (k, ph, big) => big ? `<textarea id="ed_${k}" rows="${big}" placeholder="${ph}">${v(k)}</textarea>` : `<input id="ed_${k}" placeholder="${ph}" value="${v(k)}">`;
    const temaSel = `<select id="ed_tema">${T.map(t => `<option ${t === (E.tema || "✍️ Pessoal") ? "selected" : ""}>${esc(t)}</option>`).join("")}</select>`;
    const itens = E.k === "m" && Array.isArray(E.k2) ? E.k2 : null;
    if (E.k === "m" && E.itens == null && itens) E.itens = itens.map(x => x[0] + " — " + x[1]).join("\n");
    const form = E.k === "m" ? `<div class="hoForm">
       <label>Tema ${temaSel}</label><label>Título (pergunta) ${inp("t", "Ex.: Antes de responder a uma mensagem difícil")}</label>
       <label>Sigla ou rótulo ${inp("m", "Ex.: CALMA")}</label>
       <label>Itens — um por linha (“C — Conte até 10” ou só o texto; as letras da sigla viram rótulos) ${inp("itens", "Conte até 10 (Enter) Afaste-se (Enter) …", 5)}</label>
       <label>🎯 Dica (opcional) ${inp("x", "Frase curta para lembrar")}</label><label>📖 Contexto / fonte (opcional) ${inp("c", "Ex.: Tiago 1:19 — quando uso", 2)}</label></div>`
      : `<div class="hoForm"><label>Emoji e título <span class="hoRow">${inp("e", "🧭")}${inp("t", "Ex.: Reunião tensa com a chefia")}</span></label>
       <label>🔎 Sinais (como reconhecer) ${inp("sin", "O que sinto ou percebo quando isso acontece", 2)}</label>
       <label>⬆️ Norte · princípio ${inp("N", "O valor que me guia", 2)}</label><label>⬇️ Sul · evitar ${inp("S", "O que eu não quero fazer", 2)}</label>
       <label>➡️ Leste · faça agora ${inp("L", "Ação de até 10 minutos", 2)}</label><label>⬅️ Oeste · espere e consulte ${inp("O", "Quem consultar, quanto esperar", 2)}</label>
       <label>🧭 Pergunta-chave ${inp("q", "A pergunta que me centra")}</label><label>📍 Fontes (separe com ;) ${inp("refs", "Provérbios 15:1; Alcorão 41:34")}</label>
       <label>🛡️ Siglas ligadas (separe com ;) ${inp("mn", "FREIO; PAUSA")}</label><label>⚠️ Alerta (opcional) ${inp("al", "Ex.: telefone de apoio")}</label></div>`;
    const row = (x, lab) => `<div class="hoMine"><span>${lab}</span><button class="btn sm" data-edit="${x.id}">✏️ Editar</button></div>`;
    return `<div class="panel hoPanel"><h3 style="margin-top:0">✍️ ${E.id ? "Editar" : "Criar"} ${E.k === "m" ? "mnemônico" : "bússola"}</h3>
      <div class="metaRow">${E.id ? "" : `<button class="btn ${E.k === "m" ? "cy" : ""}" data-ek="m">🛡️ Mnemônico</button><button class="btn ${E.k === "b" ? "cy" : ""}" data-ek="b">🧭 Bússola</button>`}</div>${form}
      <div class="metaRow" style="justify-content:flex-end">${E.id ? `<button class="btn danger" id="edDel">${E.delAsk ? "⚠️ Toque de novo para apagar" : "🗑️ Apagar"}</button><button class="btn" id="edNew">✖️ Cancelar</button>` : ""}<button class="btn gold" id="edSave">💾 Salvar</button></div>
      <p class="metaNow">Seus itens entram nas abas 🛡️ Mnemônicos (filtro ✍️ Meus), 🧭 Bússolas e no treino, e sincronizam entre aparelhos.</p></div>
     <div class="grid2"><div class="panel hoPanel"><h3 style="margin-top:0">🛡️ Meus mnemônicos (${mns.length})</h3>${mns.length ? mns.map(m => row(m, `<b>${esc(m.m)}</b> · ${esc(m.t)}`)).join("") : `<p class="metaNow">Nenhum ainda.</p>`}</div>
      <div class="panel hoPanel"><h3 style="margin-top:0">🧭 Minhas bússolas (${bus.length})</h3>${bus.length ? bus.map(b => row(b, `${b.e || "🧭"} ${esc(b.t)}`)).join("") : `<p class="metaNow">Nenhuma ainda.</p>`}</div></div>`;
  },
  edRead() { const E = this.ed; $$("#hoHost [id^=ed_]").forEach(el => E[el.id.slice(3)] = el.value); return E; },
  edSave() {
    const E = this.edRead(), t = (E.t || "").trim(), sp = s => String(s || "").split(/[;\n]/).map(x => x.trim()).filter(Boolean);
    let d;
    if (E.k === "m") {
      const sig = (E.m || "").trim(), lines = String(E.itens || "").split("\n").map(x => x.trim()).filter(Boolean);
      if (!t || !sig || !lines.length) return toast("Preencha título, sigla e ao menos um item.");
      const letters = [...sig.normalize("NFD").replace(/[̀-ͯ]/g, "")].filter(c => /[A-Za-z0-9]/.test(c));
      const k = lines.map((l, i) => { const m = l.match(/^(.{1,14}?)\s+[—–-]\s+(.+)$/); return m ? [m[1], m[2]] : [letters.length === lines.length ? letters[i].toUpperCase() : String(i + 1), l]; });
      d = { tema: E.tema || "✍️ Pessoal", t, m: sig, k, x: (E.x || "").trim(), c: (E.c || "").trim(), tp: letters.length === lines.length ? "a" : "l" };
    } else {
      if (!t || !(E.N || E.S || E.L || E.O)) return toast("Preencha o título e ao menos uma direção.");
      d = { e: (E.e || "🧭").trim() || "🧭", t, sin: (E.sin || "").trim(), N: (E.N || "").trim(), S: (E.S || "").trim(), L: (E.L || "").trim(), O: (E.O || "").trim(), q: (E.q || "").trim() || "O que é certo fazer agora?", refs: sp(E.refs), mn: sp(E.mn).map(x => x.toUpperCase()), al: (E.al || "").trim() };
    }
    const id = E.id || "hu" + Date.now().toString(36) + Math.random().toString(36).slice(2, 5);
    HURES()[id] = { k: E.k, d, mod: Date.now() }; saveLog(); addXP(2, "criação própria", "h");
    toast(E.id ? "💾 Atualizado" : "✅ Criado e sincronizando"); this.ed = { k: E.k }; this.render();
  },
  edOpen(id) {
    const e = HURES()[id]; if (!e || !e.d) return;
    this.ed = Object.assign({ id, k: e.k }, e.d);
    if (e.k === "m") { this.ed.itens = e.d.k.map(x => x[0] + " — " + x[1]).join("\n"); }
    else { this.ed.refs = (e.d.refs || []).join("; "); this.ed.mn = (e.d.mn || []).join("; "); }
    this.go("meus");
  },
  bindMeus(host) {
    $$("[data-edit]", host).forEach(b => b.onclick = () => this.edOpen(b.dataset.edit));
    if (this.sub !== "meus") return;
    $$("[data-ek]", host).forEach(b => b.onclick = () => { this.ed = { k: b.dataset.ek }; this.render(); });
    const sv = $("#edSave", host), dl = $("#edDel", host), nw = $("#edNew", host);
    if (sv) sv.onclick = () => this.edSave();
    if (nw) nw.onclick = () => { this.ed = { k: this.ed.k }; this.render(); };
    if (dl) dl.onclick = () => { const E = this.edRead(); if (!E.delAsk) { E.delAsk = 1; return this.render(); } HURES()[E.id] = { k: E.k, del: 1, mod: Date.now() }; saveLog(); toast("🗑️ Apagado"); this.ed = { k: E.k }; this.render(); };
  },
  /* ---- 🌙 Modo Noite: 5 minutos guiados ---- */
  NT: [["🌬️", "Respirar", 90], ["🌙", "Exame da noite", 60], ["📜", "Mensagem", 60], ["🙏", "Gratidão e intenção", 60], ["✨", "Bênção", 30]],
  noite() {
    const N = this.nt, L = S.logs[today()] || {};
    if (!N) return `<div class="panel hoPanel hoNt"><div class="hoNtMoon">🌙</div><h2 style="margin:6px 0">Modo Noite · 5 minutos</h2>
      <p class="metaNow">Uma sequência curta para fechar o dia em paz. Avance no seu ritmo; a barra só sugere o tempo.</p>
      <ol class="hoNtList">${this.NT.map(([e, t, s]) => `<li>${e} <b>${t}</b> <small>· ${s >= 60 ? s / 60 + " min" : s + " s"}</small></li>`).join("")}</ol>
      ${L.hn ? `<p class="chk on">✅ Você já fez o Modo Noite hoje — pode repetir quando quiser.</p>` : ""}
      <button class="btn gold" id="ntGo">▶️ Começar</button></div>`;
    const [e, tit, sec] = this.NT[N.i], dots = this.NT.map((x, i) => `<span class="${i < N.i ? "ok" : i === N.i ? "on" : ""}">${x[0]}</span>`).join("");
    let body = "";
    if (N.i === 0) body = `<div class="hoBreath"><div class="hoOrb" id="hoOrb"><span id="hoPh">${this.br ? "" : "Pronto"}</span><small id="hoCt"></small></div><div class="hoAnc" id="hoAnc">${esc(this.ANCORAS[this.dayIdx(this.ANCORAS.length)])}</div></div>
      <div class="metaRow" style="justify-content:center">${this.br ? `<button class="btn danger" id="hoBrStop">⏹️ Parar</button>` : `<button class="btn gold" id="ntBr">▶️ Respirar 9 ciclos (4-6)</button>`}</div>`;
    else if (N.i === 1) body = [["hz1", "🤝 Fui leal ao agir pelos outros hoje?"], ["hz2", "🫱 Fui digno de confiança com quem convivo?"], ["hz3", "📖 Pratiquei o que aprendi?"]].map(([k, l]) => `<label class="hoChk"><input type="checkbox" data-hz="${k}" ${L[k] ? "checked disabled" : ""}> ${l}</label>`).join("") + `<p class="metaNow">Analectos 1:4 — o exame diário de Zengzi. Sem culpa: só observar e ajustar amanhã.</p>`;
    else if (N.i === 2) { const c = this.msg || (this.msg = this.data.cards[this.dayIdx(this.data.cards.length)]); body = `<div class="mnCard hoCard"><div class="mcTop">${this.chip(c.tr)}<span class="pill">${esc(c.tema)}</span></div><div class="mnTit">${esc(c.q)}</div>${this.back(c)}</div>`; }
    else if (N.i === 3) body = `<div class="hoForm"><label>🙏 Três gratidões de hoje <textarea id="ntG" rows="3" placeholder="1.\n2.\n3.">${esc((L.hg || "").split("||")[0] || "")}</textarea></label>
      <label>🎯 Uma intenção para amanhã <input id="ntI" placeholder="Ex.: falar com calma no plantão" value="${esc((L.hg || "").split("||")[1] || "")}"></label></div><p class="metaNow">Fica guardado só no seu registro do dia.</p>`;
    else body = `<div class="hoBless">“Que o Senhor te abençoe e te guarde;<br>que faça resplandecer o seu rosto sobre ti;<br>que volte para ti o seu olhar e te dê a paz.”<small>Números 6:24-26 · paráfrase</small></div>
      <p class="metaNow" style="text-align:center">Solte o dia. O que ficou pendente espera por amanhã. 🌙</p>`;
    return `<div class="panel hoPanel hoNt"><div class="hoDots">${dots}</div><h2 style="margin:8px 0 4px">${e} ${tit}</h2>
      <div class="hoTimer"><i style="animation-duration:${sec}s" key="${N.i}-${N.k || 0}"></i></div>${body}
      <div class="metaRow" style="justify-content:space-between"><button class="btn" id="ntBack" ${N.i ? "" : "disabled"}>◀ Voltar</button>
      ${N.i < this.NT.length - 1 ? `<button class="btn gold" id="ntNext">Próximo ▶</button>` : `<button class="btn gold" id="ntEnd">✅ Concluir (+5 XP)</button>`}</div></div>`;
  },
  ntSave() { const g = $("#ntG"), i = $("#ntI"); if (g || i) { const L = L0(); L.hg = (g ? g.value : "") + "||" + (i ? i.value : ""); saveLog(); } },
  bindNoite(host) {
    if (this.sub !== "noite") return;
    const go = $("#ntGo", host), nx = $("#ntNext", host), bk = $("#ntBack", host), en = $("#ntEnd", host), br = $("#ntBr", host);
    if (go) go.onclick = () => { this.nt = { i: 0, k: Date.now() }; this.render(); };
    if (br) br.onclick = () => this.brStart("calma", 9, () => { this.nt.i = 1; this.nt.k = Date.now(); this.render(); });
    if (nx) nx.onclick = () => { if (this.br) this.brStop(); this.ntSave(); this.nt.i++; this.nt.k = Date.now(); this.render(); };
    if (bk) bk.onclick = () => { if (this.br) this.brStop(); this.ntSave(); this.nt.i = Math.max(0, this.nt.i - 1); this.nt.k = Date.now(); this.render(); };
    if (en) en.onclick = () => { const L = L0(), first = !L.hn; L.hn = 1; if (first) addXP(5, "modo noite", "h"); saveLog(); this.nt = null; toast("🌙 Boa noite. Que a paz te acompanhe."); this.render(); };
  },
  key(e) {
    if ((this.sub !== "cards" && this.sub !== "mn") || this.mode !== "treino" || !this.cur) return;
    if (!this.shown) { if (e.code === "Space" || e.key === "Enter") { e.preventDefault(); this.shown = true; this.render(); } else if (e.key === "d" || e.key === "D") { e.preventDefault(); this.hint = true; this.render(); } return; }
    const g = "123".indexOf(e.key); if (g >= 0) { e.preventDefault(); this.answer(g); }
  } };
