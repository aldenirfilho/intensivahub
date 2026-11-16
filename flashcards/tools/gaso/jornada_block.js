/* ---------- 4.14.0: 📆 Desafios semanais (3 por semana, renovam na segunda-feira) ---------- */
const WC = {
  LV: { leve: ["🟢 Leve", 0.5, 0.6], padrao: ["🟡 Padrão", 1, 1], hard: ["🔴 Hardcore", 2, 1.8] },
  POOL: [   // [id, grupo, ícone, nome, alvo padrão, XP, métrica, descrição]
    ["cards", 0, "🎴", "Maratona da semana", 300, 80, w => w.cards, n => `Responder ${n.toLocaleString("pt-BR")} flashcards`],
    ["rev", 0, "🔁", "Guardião das revisões", 150, 80, w => w.rev, n => `Fazer ${n} revisões`],
    ["novos", 0, "🆕", "Desbravador", 70, 80, w => w.novos, n => `Estudar ${n} cards novos`],
    ["xp", 0, "⚡", "Semana de XP", 1500, 120, w => w.xp, n => `Somar ${n.toLocaleString("pt-BR")} XP na semana`],
    ["q", 1, "❓", "Questionador semanal", 60, 100, w => w.q, n => `Responder ${n} questões`],
    ["sim", 1, "🎯", "Bloco de elite", 2, 100, w => w.sim80, n => `Fechar ${n} bloco(s) de ≥ 10 questões com ≥ 80%`],
    ["gz", 1, "🧪", "Alquimista da semana", 15, 100, w => w.gN, n => `Resolver ${n} casos guiados de gasometria`],
    ["gzp", 1, "⭐", "Precisão ácido-base", 5, 100, w => w.gP, n => `Fechar ${n} casos de gasometria sem erro`],
    ["qc", 1, "📖", "Leitor de comentários", 30, 60, w => w.qc, n => `Ler ${n} comentários de questões`],
    ["dias", 2, "📆", "Presença", 5, 100, w => w.dias, n => `Estudar em ${n} dias da semana`],
    ["micro", 2, "💊", "Micro leitor", 20, 60, w => w.mN, n => `Ler ${n} micropartículas`],
    ["mn", 2, "🧠", "Treino de mnemônicos", 30, 60, w => w.nN, n => `Treinar ${n} mnemônicos`],
    ["honra", 2, "🕊️", "Fôlego e honra", 5, 60, w => w.hon, n => `Fazer ${n} práticas na aba Honra`],
    ["meta", 2, "🏹", "Juramento semanal", 4, 100, w => w.meta, n => `Cumprir a meta de novos em ${n} dias`]],
  lvl() { const w = S.logs._wl; return w && this.LV[w.lvl] ? w.lvl : (this.LV[lsGet("wcLvl")] ? lsGet("wcLvl") : "padrao"); },
  setLvl(l) { if (!this.LV[l]) return; S.logs._wl = { lvl: l, t: Date.now() }; lsSet("wcLvl", l); saveLog(); this.check(); },
  wk(t) { return isoWeek(t || Date.now()); },
  rng(seed) { return () => { seed = seed + 0x6D2B79F5 | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; },
  pick(wk) { const r = this.rng(Math.round(wk / (7 * DAY)) * 7919 + 2028); return [0, 1, 2].map(g => { const l = this.POOL.filter(p => p[1] === g); return l[Math.floor(r() * l.length)]; }); },
  stats(wk) {
    const o = { cards: 0, rev: 0, novos: 0, xp: 0, q: 0, sim80: 0, gN: 0, gP: 0, qc: 0, dias: 0, mN: 0, nN: 0, hon: 0, meta: 0 }, nNew = S.settings.newPerDay || 0;
    for (const [d, l] of dayLogs()) {
      if (isoWeek(new Date(d + "T12:00").getTime()) !== wk) continue;
      o.cards += l.nAns || 0; o.rev += l.nRev || 0; o.novos += l.nNew || 0; o.xp += l.xp || 0; o.q += l.qN || 0; o.qc += l.qcN || 0; o.mN += l.mN || 0; o.nN += l.nN || 0;
      o.sim80 += (l.sims || []).filter(x => x.n >= 10 && x.ok / x.n >= 0.8).length; o.gN += l.gN || 0; o.gP += l.gP || 0;
      o.hon += (l.hN || 0) + (l.hb || 0) + (l.hn ? 1 : 0); if (nNew && (l.nNew || 0) >= nNew) o.meta++;
      if ((l.nAns || 0) + (l.qN || 0) + (l.mN || 0) + (l.nN || 0) + (l.hN || 0) + (l.hb || 0) + (l.gS || 0) + (l.gA || 0) + (l.sims || []).length > 0) o.dias++;
    }
    return o;
  },
  list(wk) {
    wk = wk || this.wk(); const [, k, kx] = this.LV[this.lvl()], st = this.stats(wk), D = (S.logs._wc || {})[wk] || {};
    return this.pick(wk).map(([id, , ic, nome, base, xp, fn, desc]) => {
      let alvo = Math.max(1, Math.round(base * k)); if (id === "dias" || id === "meta") alvo = Math.min(7, alvo);
      const v = fn(st); return { id, ic, nome, alvo, xp: Math.round(xp * kx), v, desc: desc(alvo), done: D[id] || 0 };
    });
  },
  check() {
    const wk = this.wk(), L = this.list(wk), W = (S.logs._wc = S.logs._wc || {}), D = (W[wk] = W[wk] || {}), novas = [];
    for (const c of L) if (!D[c.id] && c.v >= c.alvo) { D[c.id] = Date.now(); novas.push(c); }
    if (!novas.length) { if (!Object.keys(D).length) delete W[wk]; return false; }
    const perfeita = !D.all && L.every(c => D[c.id]); if (perfeita) D.all = Date.now();
    saveLog();
    for (const c of novas) addXP(c.xp, "desafio", "d");
    if (perfeita) addXP(100, "semana perfeita", "d");
    const c = novas[novas.length - 1];
    toast(perfeita ? "🏆 <b>Semana perfeita!</b> Os 3 desafios cumpridos · +100 XP" : `${c.ic} <b>Desafio cumprido!</b> ${esc(c.nome)} · +${c.xp} XP`, 4500);
    if (location.hash === "#jornada") JR.render();
    return true;
  },
  done() { let n = 0, all = 0; for (const D of Object.values(S.logs._wc || {})) { if (!D || typeof D !== "object") continue; n += Object.keys(D).filter(k => k !== "all").length; if (D.all) all++; } return { n, all }; },
  left() { const d = Math.ceil((this.wk() + 7 * DAY - Date.now()) / DAY); return d <= 1 ? "último dia" : `faltam ${d} dias`; },
  html() {
    const L = this.list(), lv = this.lvl(), T = this.done(), ok = L.filter(c => c.done).length;
    return `<div class="panel" id="wcPanel"><div class="wcHead"><h2 style="margin:0">📆 Desafios da semana <small style="color:var(--mut);font-weight:400">${ok}/3 · ${this.left()}</small></h2>
      <div class="wcLvl">${Object.entries(this.LV).map(([k, [n]]) => `<button class="btn sm ${k === lv ? "gold" : ""}" data-wcl="${k}">${n}</button>`).join("")}</div></div>
      <div class="wcGrid">${L.map(c => `<div class="wc ${c.done ? "on" : ""}"><b>${c.ic} ${esc(c.nome)}</b><small>${esc(c.desc)}</small><span class="xpTrack"><i style="width:${Math.min(100, Math.round(100 * c.v / c.alvo))}%"></i></span><small>${Math.min(c.v, c.alvo).toLocaleString("pt-BR")}/${c.alvo.toLocaleString("pt-BR")} · ${c.done ? "✅ cumprido" : `+${c.xp} XP`}</small></div>`).join("")}</div>
      <p class="metaNow">🔄 Renovam toda segunda-feira · fechar os 3 dá +100 XP (🏆 semana perfeita) · você já cumpriu <b>${T.n}</b> desafios e <b>${T.all}</b> semana(s) perfeita(s). O nível vale para a semana inteira e pode ser trocado quando quiser.</p></div>`;
  },
  mini() {
    const L = this.list(), ok = L.filter(c => c.done).length;
    return `<a href="#jornada" class="wcMini">📆 <b>Desafios da semana ${ok}/3</b> · ${L.map(c => `${c.done ? "✅" : c.ic} ${Math.min(c.v, c.alvo).toLocaleString("pt-BR")}/${c.alvo.toLocaleString("pt-BR")}`).join(" · ")} ›</a>`;
  },
  bind(host) { $$("[data-wcl]", host).forEach(b => b.onclick = () => { this.setLvl(b.dataset.wcl); if (location.hash === "#jornada") JR.render(); toast(`📆 Nível dos desafios: ${this.LV[b.dataset.wcl][0]}`); }); } };
function jStats() {
  const days = dayLogs().sort((a, b) => a[0].localeCompare(b[0])), act = l => (l.nAns || 0) + (l.qN || 0) + (l.mN || 0) + (l.nN || 0) + (l.hN || 0) + (l.hb || 0) + (l.hn || 0) + (l.gS || 0) + (l.gA || 0) + (l.sims || []).length > 0;
  const on = new Set(days.filter(([, l]) => act(l)).map(([d]) => d));
  let cur = 0; for (let i = on.has(today()) ? 0 : 1; on.has(dayKey(Date.now() - i * DAY)); i++) cur++;
  let max = 0, run = 0, prev = null, returns = 0, fenix = 0, sinceRet = -1;
  for (const d of [...on].sort()) { const t = new Date(d + "T12:00").getTime(), gap = prev ? Math.round((t - prev) / DAY) : 0; run = prev && gap === 1 ? run + 1 : 1; if (prev && gap >= 8) { returns++; sinceRet = 0; } if (sinceRet >= 0) { sinceRet = gap === 1 || sinceRet === 0 ? run : -1; if (sinceRet >= 7) { fenix++; sinceRet = -1; } } max = Math.max(max, run); prev = t; }
  const sims = days.flatMap(([, l]) => l.sims || []).filter(x => x.n >= 10).map(x => Math.round(100 * x.ok / x.n));
  const Q = S.logs._q || {}, qv = Object.values(Q), qOk = qv.filter(x => x[0]).length;
  const nNew = S.settings.newPerDay || 0, metaDays = days.filter(([, l]) => nNew && (l.nNew || 0) >= nNew).length;
  const wk = {}; for (const [d, l] of days) { const w = isoWeek(new Date(d + "T12:00").getTime()); wk[w] = (wk[w] || 0) + (l.xp || 0); }
  const xs = {}; for (const [, l] of days) for (const [k, v] of Object.entries(l.xs || {})) xs[k] = (xs[k] || 0) + v;
  // 📆 assiduidade: semanas seguidas, mês, fins de semana
  const wOn = [...new Set([...on].map(d => isoWeek(new Date(d + "T12:00").getTime())))].sort((a, b) => a - b);
  let wRun = 0, wMax = 0, wPrev = null; for (const w of wOn) { wRun = wPrev && Math.round((w - wPrev) / (7 * DAY)) === 1 ? wRun + 1 : 1; wMax = Math.max(wMax, wRun); wPrev = w; }
  const thisW = isoWeek(Date.now()), wCur = wOn.length && (wOn[wOn.length - 1] === thisW || wOn[wOn.length - 1] === thisW - 7 * DAY) ? wRun : 0;
  const byMonth = {}; for (const d of on) byMonth[d.slice(0, 7)] = (byMonth[d.slice(0, 7)] || 0) + 1;
  let fds = 0; for (const d of on) { const t = new Date(d + "T12:00"); if (t.getDay() === 6 && on.has(dayKey(t.getTime() + DAY))) fds++; }
  // 🎭 estilo: horário, ritmo, precisão, revisão, diversidade
  const hr = {}; for (const [, l] of days) for (const [h, n] of Object.entries(l.hr || {})) hr[h] = (hr[h] || 0) + n;
  const hsum = (a, b) => { let s = 0; for (let h = a; h <= b; h++) s += hr[h] || 0; return s; };
  const ans = days.map(([, l]) => l.nAns || 0), recent = days.filter(([d]) => d >= dayKey(Date.now() - 30 * DAY));
  const rA = recent.reduce((a, [, l]) => a + (l.nAns || 0), 0), rOk = recent.reduce((a, [, l]) => a + (l.nOk || 0), 0), rDays = recent.filter(([, l]) => act(l)).length;
  const rNew = recent.reduce((a, [, l]) => a + (l.nNew || 0), 0), rRev = recent.reduce((a, [, l]) => a + (l.nRev || 0), 0), rSrc = new Set(recent.flatMap(([, l]) => Object.keys(l.xs || {}).filter(k => k !== "a")));
  // 📚 categorias (pelas coleções ativas)
  const cat = {}, decks = new Set();
  for (const c of S.cards || []) { if (!c.official && c.origin !== "oficial" && !c.col) continue; const k = c.col || "temi", o = cat[k] = cat[k] || { tot: 0, st: 0, mat: 0 }; o.tot++; if (c.srs && c.srs.reps) { o.st++; decks.add(c.deck); if (c.srs.st === "review" && c.srs.ivl >= 21) o.mat++; } }
  const G = S.logs._g || {}, gv = Object.values(G), gq = Object.entries(Q).filter(([id]) => id.startsWith("QG")).map(([, v]) => v), wcd = WC.done();
  return { cur, max: Math.max(max, cur), xp: xpTotal(), lv: levelOf(xpTotal()).lv, sims, qAns: qv.length, qAcc: qv.length ? qOk / qv.length : 0, qc: Object.keys(S.logs._qc || {}).length,
    mic: Object.keys(S.logs._m || {}).length, mn: Object.values(S.logs._n || {}).filter(e => e && (e.s || 0) >= 2).length, hon: Object.values(S.logs._h || {}).filter(e => e && (e.s || 0) >= 2).length,
    hb: days.reduce((a, [, l]) => a + (l.hb || 0), 0), hbu: days.reduce((a, [, l]) => a + (l.hbu || 0) + (l.hf || 0), 0), hn: days.reduce((a, [, l]) => a + (l.hn ? 1 : 0), 0), cards: ans.reduce((a, b) => a + b, 0), metaDays, wk, xs, days,
    dias: on.size, wMax: Math.max(wMax, wCur), wCur, mesMax: Math.max(0, ...Object.values(byMonth)), mes: byMonth[today().slice(0, 7)] || 0, fds, returns, fenix,
    hr, coruja: hsum(0, 4), madrug: hsum(5, 7), noite: hsum(20, 23), maxDay: Math.max(0, ...ans), maxXP: Math.max(0, ...days.map(([, l]) => l.xp || 0)),
    perfDays: days.filter(([, l]) => (l.nAns || 0) >= 50 && l.nOk / l.nAns >= 0.95).length, maxRev: Math.max(0, ...days.map(([, l]) => l.nRev || 0)),
    balDays: days.filter(([, l]) => Object.keys(l.xs || {}).filter(k => k !== "a").length >= 4).length, gota: days.filter(([, l]) => (l.nAns || 0) >= 10 && (l.nAns || 0) <= 40).length,
    explor: decks.size, cat, rA, rOk, rDays, rNew, rRev, rSrc: rSrc.size,
    gN: gv.filter(e => e && e.n).length, gP: gv.filter(e => e && e.p).length, gA: days.reduce((a, [, l]) => a + (l.gA || 0), 0), gqA: gq.length, gqAcc: gq.length ? gq.filter(x => x[0]).length / gq.length : 0, wcN: wcd.n, wcAll: wcd.all };
}
const ACH_G = { prox: "⭐ Próximas", ass: "📆 Assiduidade", cat: "📚 Categorias", des: "🎯 Desempenho", est: "🎭 Estilo", tit: "📜 Títulos", hon: "🕊️ Honra", all: "🏅 Todas" };
const CATS = [["temi", "🏥", "Intensivista", "TEMI 2028"], ["cm", "🩺", "Clínico de Ouro", "R3 Clínica Médica"], ["ecg", "📈", "Leitor de Traçados", "Compêndio de ECG"], ["vmc", "🫁", "Domador do Ventilador", "Curvas de VM"], ["pocus", "🔊", "Vidente do Ultrassom", "POCUS na UTI"],
  ["gaso", "🧪", "Alquimista Ácido-Base", "Gasometria 360X"], ["ouro", "🧩", "Guardião dos Números", "Números de ouro"], ["ia360c", "✅", "Revisor 360X", "IAs 360X curados"], ["iac", "🧹", "Curador das IAs", "Outras IAs"], ["grok", "🤖", "Domador do Grok", "Grok revisado"]];
const ACH = { list: [],
  build() {
    const A = (id, tipo, ic, nome, desc, val, goal, grp) => this.list.push({ id, tipo, ic, nome, desc, val, goal, grp });
    [[3, "medalha", "🔥", "Chama Acesa"], [7, "medalha", "🕯️", "Vigília de 7 Dias"], [14, "trofeu", "⚔️", "Quinzena do Cavaleiro"], [30, "trofeu", "🏰", "Cerco de 30 Dias"], [60, "brasao", "🛡️", "Brasão da Constância"], [100, "brasao", "🐉", "Brasão do Dragão"], [180, "honra", "👑", "Honra da Perseverança"], [365, "honra", "🌟", "Honra ao Mérito Anual"]]
      .forEach(([n, t, ic, nm]) => A("st" + n, t, ic, nm, `Sequência de ${n} dias de estudo seguidos`, s => s.max, n, "ass"));
    const SIM = [[50, "medalha", "🥉", "Medalha de Bronze"], [60, "medalha", "🥈", "Medalha de Prata"], [70, "medalha", "🥇", "Medalha de Ouro"], [80, "trofeu", "🏆", "Troféu de Excelência"], [90, "brasao", "🛡️", "Brasão de Elite"], [100, "honra", "🎖️", "Honra ao Mérito"]];
    for (const [p, t, ic, nm] of SIM) [[1, "I"], [5, "II"], [20, "III"]].forEach(([k, r]) => A(`sim${p}_${k}`, t, ic, `${nm} ${r}`, `${k} simulado(s) ou bloco(s) de questões (≥ 10 itens) com nota ${p === 100 ? "de 100%" : "≥ " + p + "%"}`, s => s.sims.filter(x => x >= p).length, k, "des"));
    [[500, "Iniciado do Códice"], [1000, "Escriba"], [2500, "Bacharel das Runas"], [5000, "Mestre de Armas"], [10000, "Cavaleiro da Ordem"], [25000, "Comendador"], [50000, "Grão-Mestre do Códice"], [100000, "Lenda do TEMI"]]
      .forEach(([n, nm]) => A("xp" + n, "titulo", "📜", nm, `Acumular ${n.toLocaleString("pt-BR")} XP`, s => s.xp, n, "tit"));
    RANKS.forEach((r, i) => { if (i) A("rk" + i, "titulo", r.split(" ")[0], "Título: " + r.split(" ").slice(1).join(" "), `Alcançar o nível ${i * 5 + 1}`, s => s.lv, i * 5 + 1, "tit"); });
    [[10, "medalha"], [50, "medalha"], [100, "trofeu"], [200, "trofeu"], [400, "brasao"], [600, "honra"]].forEach(([n, t]) => A("qa" + n, t, "❓", `Questionador ${n}`, `Responder ${n} questões diferentes`, s => s.qAns, n, "cat"));
    A("acc70", "trofeu", "🎯", "Mira Certeira", "Acerto ≥ 70% com ≥ 50 questões", s => s.qAns >= 50 ? Math.round(100 * s.qAcc) : 0, 70, "des");
    A("acc80", "brasao", "🏹", "Arqueiro de Elite", "Acerto ≥ 80% com ≥ 100 questões", s => s.qAns >= 100 ? Math.round(100 * s.qAcc) : 0, 80, "des");
    A("acc90", "honra", "🦅", "Olho de Águia", "Acerto ≥ 90% com ≥ 200 questões", s => s.qAns >= 200 ? Math.round(100 * s.qAcc) : 0, 90, "des");
    [[10, "medalha"], [50, "medalha"], [100, "trofeu"], [200, "brasao"], [400, "honra"]].forEach(([n, t]) => A("qc" + n, t, "📖", `Leitor de Comentários ${n}`, `Marcar ☑️ ${n} comentários de questões como lidos`, s => s.qc, n, "cat"));
    [[10, "medalha"], [50, "trofeu"], [100, "brasao"], [200, "honra"], [400, "honra"], [600, "honra"]].forEach(([n, t]) => A("mc" + n, t, "💊", `Alquimista ${n}`, `Ler ${n} micropartículas (☑️)`, s => s.mic, n, "cat"));
    [[10, "medalha"], [50, "trofeu"], [150, "brasao"], [300, "honra"], [500, "honra"], [800, "honra"]].forEach(([n, t]) => A("mn" + n, t, "🧠", `Mnemonista ${n}`, `Dominar ${n} mnemônicos (2 acertos seguidos no treino)`, s => s.mn, n, "cat"));
    [[10, "medalha"], [50, "trofeu"], [150, "brasao"], [300, "honra"], [500, "honra"]].forEach(([n, t]) => A("ho" + n, t, "🕊️", `Peregrino da Honra ${n}`, `Dominar ${n} cards ou mnemônicos da aba 🕊️ Honra`, s => s.hon, n, "hon"));
    [[5, "medalha"], [30, "trofeu"], [100, "brasao"]].forEach(([n, t]) => A("hb" + n, t, "🌬️", `Fôlego Sereno ${n}`, `Concluir ${n} respirações guiadas na aba 🕊️ Honra`, s => s.hb, n, "hon"));
    [[1, "medalha"], [7, "trofeu"], [30, "brasao"], [100, "honra"]].forEach(([n, t]) => A("hn" + n, t, "🌙", `Vigília Serena ${n}`, `Concluir o Modo Noite em ${n} noite(s)`, s => s.hn, n, "hon"));
    [[5, "medalha"], [25, "trofeu"], [100, "brasao"]].forEach(([n, t]) => A("hu" + n, t, "🧭", `Bússola de Ouro ${n}`, `Usar ${n} bússolas ou filtros de decisão`, s => s.hbu, n, "hon"));
    [[100, "medalha"], [500, "medalha"], [1000, "trofeu"], [2500, "trofeu"], [5000, "brasao"], [10000, "honra"]].forEach(([n, t]) => A("cd" + n, t, "🎴", `Guardião de ${n.toLocaleString("pt-BR")} cards`, `Responder ${n.toLocaleString("pt-BR")} flashcards`, s => s.cards, n, "cat"));
    [[1, "medalha"], [7, "trofeu"], [30, "brasao"], [100, "honra"]].forEach(([n, t]) => A("mt" + n, t, "🎯", `Juramento Cumprido ${n}`, `Cumprir a meta diária de novos em ${n} dia(s)`, s => s.metaDays, n, "des"));
    A("wkrec", "trofeu", "📈", "Semana Recorde", "Superar sua melhor semana anterior (≥ 500 XP)", s => { const w = Object.entries(s.wk).sort((a, b) => a[0] - b[0]); if (w.length < 2) return 0; const last = w[w.length - 1][1], best = Math.max(...w.slice(0, -1).map(x => x[1])); return last >= 500 && last > best ? 1 : 0; }, 1, "des");
    /* ---------- 4.13.0: 📆 assiduidade ---------- */
    [[10, "medalha", "📅", "Dez Dias de Estrada"], [30, "medalha", "🗓️", "Mês de Presença"], [60, "trofeu", "🏛️", "Coluna do Templo"], [100, "brasao", "💯", "Centurião"], [200, "honra", "⛰️", "Montanha Movida"], [365, "honra", "🌍", "Volta ao Sol"]]
      .forEach(([n, t, ic, nm]) => A("dias" + n, t, ic, nm, `Estudar em ${n} dias diferentes (não precisam ser seguidos)`, s => s.dias, n, "ass"));
    [[4, "medalha", "🧱", "Quatro Semanas Firmes"], [12, "trofeu", "🏗️", "Trimestre Sem Falhas"], [26, "brasao", "🏯", "Semestre de Ferro"], [52, "honra", "🗿", "Ano Inquebrável"]]
      .forEach(([n, t, ic, nm]) => A("sem" + n, t, ic, nm, `Estudar em ${n} semanas seguidas (pelo menos 1 dia por semana)`, s => s.wMax, n, "ass"));
    A("mes20", "trofeu", "🌕", "Lua Cheia", "Estudar em 20 dias do mesmo mês", s => s.mesMax, 20, "ass");
    A("mes28", "brasao", "🌝", "Mês Completo", "Estudar em 28 dias do mesmo mês", s => s.mesMax, 28, "ass");
    [[4, "medalha"], [12, "trofeu"], [26, "brasao"]].forEach(([n, t]) => A("fds" + n, t, "🛡️", `Guardião do Fim de Semana ${n}`, `Estudar sábado E domingo em ${n} fins de semana`, s => s.fds, n, "ass"));
    A("ret1", "medalha", "🚪", "Retorno do Herói", "Voltar a estudar depois de uma pausa de 7+ dias (recomeçar também é vitória)", s => s.returns, 1, "ass");
    A("fenix", "trofeu", "🐦‍🔥", "Fênix", "Depois de uma pausa de 7+ dias, emendar 7 dias seguidos de estudo", s => s.fenix, 1, "ass");
    /* ---------- 4.13.0: 📚 categorias de estudo (por coleção ativa) ---------- */
    const TIER = [[10, "medalha", "🥉", "Aprendiz"], [25, "trofeu", "🥈", "Escudeiro"], [50, "brasao", "🥇", "Cavaleiro"], [100, "titulo", "👑", "Mestre"]];
    for (const [col, ic, nm, lbl] of CATS) for (const [p, t, mi, tn] of TIER)
      A(`cat_${col}_${p}`, t, p === 100 ? ic : mi, `${ic} ${nm} · ${tn}`, `Estudar ${p}% dos cards da coleção ${ic} ${lbl} (cada card respondido ao menos 1 vez)`, s => { const c = s.cat[col]; return c && c.tot ? Math.floor(100 * c.st / c.tot) : 0; }, p, p === 100 ? "tit" : "cat");
    for (const [col, ic, nm, lbl] of CATS.slice(0, 6)) A(`mat_${col}`, "honra", "🌳", `${ic} Raízes Profundas · ${nm}`, `Ter 50% dos cards de ${ic} ${lbl} maduros (intervalo ≥ 21 dias)`, s => { const c = s.cat[col]; return c && c.tot ? Math.floor(100 * c.mat / c.tot) : 0; }, 50, "cat");
    /* ---------- 4.13.0: 🧪 gasometria ---------- */
    [[5, "medalha"], [25, "trofeu"], [100, "brasao"], [235, "honra"]].forEach(([n, t]) => A("gz" + n, t, "🧪", `Decifrador de Gasometrias ${n}`, `Resolver ${n} casos guiados na aba 🧪 Gaso`, s => s.gN, n, "cat"));
    [[10, "trofeu"], [50, "brasao"], [150, "honra"]].forEach(([n, t]) => A("gzp" + n, t, "⭐", `Leitura Perfeita ${n}`, `Resolver ${n} casos guiados sem errar nenhuma etapa`, s => s.gP, n, "des"));
    [[5, "medalha"], [25, "trofeu"]].forEach(([n, t]) => A("gza" + n, t, "🧮", `Analista de Beira-Leito ${n}`, `Usar ${n} vezes o analisador passo a passo`, s => s.gA, n, "cat"));
    [[25, "medalha"], [100, "trofeu"], [145, "brasao"]].forEach(([n, t]) => A("gzq" + n, t, "❓", `Questões de Gasometria ${n}`, `Responder ${n} questões da divisão 🧪 Gasometria`, s => s.gqA, n, "cat"));
    A("gz328", "honra", "🏺", "Mestre dos 328 Casos", "Resolver todos os 328 casos guiados da aba 🧪 Gaso", s => s.gN, 328, "tit");
    /* ---------- 4.14.0: 📆 desafios semanais ---------- */
    [[1, "medalha", "📆", "Primeiro Desafio"], [10, "trofeu", "🗡️", "Desafiante"], [30, "brasao", "🛡️", "Veterano dos Desafios"], [100, "honra", "👑", "Senhor dos Desafios"]]
      .forEach(([n, t, ic, nm]) => A("wc" + n, t, ic, nm, `Cumprir ${n} desafio(s) semanal(is)`, s => s.wcN, n, "ass"));
    [[1, "trofeu", "🏆", "Semana Perfeita"], [4, "brasao", "🌟", "Mês de Ouro"], [12, "honra", "🐉", "Trimestre Lendário"]]
      .forEach(([n, t, ic, nm]) => A("wcp" + n, t, ic, nm, `Cumprir os 3 desafios em ${n} semana(s)`, s => s.wcAll, n, "des"));
    A("gzq80", "titulo", "⚗️", "Senhor das Gasometrias", "Acerto ≥ 80% com ≥ 50 questões de gasometria", s => s.gqA >= 50 ? Math.round(100 * s.gqAcc) : 0, 80, "tit");
    /* ---------- 4.13.0: 🎭 estilo de comportamento ---------- */
    [[100, "medalha"], [500, "trofeu"]].forEach(([n, t]) => A("coruja" + n, t, "🦉", `Coruja do Plantão ${n}`, `Responder ${n} itens entre 0h e 4h59 (madrugada de plantão)`, s => s.coruja, n, "est"));
    [[100, "medalha"], [500, "trofeu"]].forEach(([n, t]) => A("madr" + n, t, "🌅", `Madrugador ${n}`, `Responder ${n} itens entre 5h e 7h59`, s => s.madrug, n, "est"));
    A("noite300", "medalha", "🌙", "Estudante da Lua", "Responder 300 itens entre 20h e 23h59", s => s.noite, 300, "est");
    [[200, "medalha", "🏃", "Maratonista"], [500, "trofeu", "🏃‍♂️", "Ultramaratonista"], [1000, "brasao", "🦾", "Titã do Códice"]].forEach(([n, t, ic, nm]) => A("mara" + n, t, ic, nm, `Responder ${n} flashcards em um único dia`, s => s.maxDay, n, "est"));
    [[1000, "trofeu", "⚡", "Dia Épico"], [2500, "brasao", "🌋", "Dia Lendário"]].forEach(([n, t, ic, nm]) => A("dxp" + n, t, ic, nm, `Fazer ${n.toLocaleString("pt-BR")} XP em um único dia`, s => s.maxXP, n, "est"));
    [[1, "medalha"], [10, "trofeu"], [30, "brasao"]].forEach(([n, t]) => A("perf" + n, t, "💎", `Precisão Cirúrgica ${n}`, `Dias com ≥ 50 respostas e ≥ 95% de acerto: ${n}`, s => s.perfDays, n, "est"));
    [[100, "medalha", "🛡️", "Guardião da Memória"], [300, "trofeu", "🏰", "Fortaleza das Revisões"]].forEach(([n, t, ic, nm]) => A("rev" + n, t, ic, nm, `Fazer ${n} revisões em um único dia`, s => s.maxRev, n, "est"));
    [[25, "medalha"], [75, "trofeu"], [150, "brasao"]].forEach(([n, t]) => A("expl" + n, t, "🧭", `Explorador ${n}`, `Estudar cards de ${n} baralhos diferentes`, s => s.explor, n, "est"));
    [[5, "medalha"], [20, "trofeu"]].forEach(([n, t]) => A("bal" + n, t, "⚖️", `Polímata ${n}`, `Dias em que você ganhou XP em 4+ áreas diferentes: ${n}`, s => s.balDays, n, "est"));
    [[20, "medalha"], [60, "trofeu"]].forEach(([n, t]) => A("gota" + n, t, "💧", `Gota que Fura a Pedra ${n}`, `Dias com uma dose curta e constante (10 a 40 flashcards): ${n}`, s => s.gota, n, "est"));
  },
  got() { return (S.logs._a = S.logs._a || {}); },
  check() {
    if (!this.list.length) this.build();
    WC.check();
    const st = jStats(), G = this.got(), novas = [];
    for (const a of this.list) if (!G[a.id] && a.val(st) >= a.goal) { G[a.id] = Date.now(); novas.push(a); }
    if (!novas.length) return;
    saveLog();
    for (const a of novas) addXP(ACH_BONUS[a.tipo], "conquista", "a");
    const a = novas[novas.length - 1];
    toast(`${a.ic} <b>Nova conquista!</b> ${esc(a.nome)}${novas.length > 1 ? ` (+${novas.length - 1})` : ""} · ${ACH_T[a.tipo]}`, 4500);
    if (location.hash === "#jornada") JR.render();
  } };
function styleOf(st) {   // 🎭 perfil de estilo (últimos 30 dias) — sempre em tom positivo
  const tot = Object.values(st.hr).reduce((a, b) => a + b, 0), fx = [[0, 5, "🦉 Coruja da madrugada"], [6, 11, "🌅 Matinal"], [12, 17, "☀️ Vespertino"], [18, 23, "🌙 Noturno"]];
  let hora = "⏳ horário em medição", best = 0;
  if (tot >= 20) for (const [a, b, n] of fx) { let s = 0; for (let h = a; h <= b; h++) s += st.hr[h] || 0; if (s > best) { best = s; hora = n; } }
  const med = st.rDays ? Math.round(st.rA / st.rDays) : 0, acc = st.rA ? Math.round(100 * st.rOk / st.rA) : 0;
  const ritmo = !st.rDays ? "🌱 começando" : med < 30 ? "💧 Gota constante" : med <= 120 ? "⚙️ Ritmo firme" : "🏃 Maratonista";
  const prec = !st.rA ? "—" : acc >= 90 ? "🎯 Cirúrgico" : acc >= 75 ? "🧱 Consistente" : "🔁 Aprende errando (ótimo para fixar)";
  const foco = st.rNew + st.rRev < 20 ? "—" : st.rRev >= 3 * Math.max(1, st.rNew) ? "🛡️ Guardião da memória (revisões)" : st.rNew >= st.rRev ? "🧭 Desbravador (conteúdo novo)" : "⚖️ Equilibrado (novos + revisões)";
  const div = st.rSrc >= 5 ? "📚 Polímata (5+ áreas)" : st.rSrc >= 3 ? "🧩 Versátil (3–4 áreas)" : "🎯 Focado (1–2 áreas)";
  return { hora, ritmo, prec, foco, div, med, acc, dias: st.rDays };
}
const JR = { grp: lsGet("jrGrp") || "prox",
  async render() { await QZ.load();
    if (!ACH.list.length) ACH.build();
    const st = jStats(), G = ACH.got(), L = levelOf(st.xp), now = Date.now(), wNow = isoWeek(now);
    const d14 = []; for (let i = 13; i >= 0; i--) d14.push(dayKey(now - i * DAY));
    const xp14 = d14.map(d => (S.logs[d] || {}).xp || 0), W = []; for (let i = 11; i >= 0; i--) W.push(isoWeek(now - i * 7 * DAY));
    const wv = W.map(w => st.wk[w] || 0), lab = t => { const d = new Date(+t); return String(d.getDate()).padStart(2, "0") + "/" + String(d.getMonth() + 1).padStart(2, "0"); };
    const rank = Object.entries(st.wk).filter(([, v]) => v > 0).sort((a, b) => b[1] - a[1]), pos = rank.findIndex(([w]) => +w === wNow) + 1;
    const src = Object.entries(XPSRC).map(([k, [n, c]]) => ({ n, c, v: st.xs[k] || 0 })), tot = Object.values(st.xs).reduce((a, b) => a + b, 0) || 1;
    const nGot = ACH.list.filter(a => G[a.id]).length, prog = a => Math.min(1, a.val(st) / a.goal);
    const card = a => { const v = Math.min(a.goal, a.val(st)), ok = G[a.id]; return `<div class="ach ${ok ? "on" : ""}" title="${esc(a.desc)}"><div class="achIc">${ok ? a.ic : "🔒"}</div><div class="achTx"><b>${esc(a.nome)}</b><small>${esc(a.desc)}</small>${ok ? `<small class="achD">✅ ${new Date(G[a.id]).toLocaleDateString("pt-BR")} · ${ACH_T[a.tipo].split(" ")[0]} +${ACH_BONUS[a.tipo]} XP</small>` : `<span class="xpTrack"><i style="width:${Math.round(100 * v / a.goal)}%"></i></span><small>${typeof v === "number" ? v.toLocaleString("pt-BR") : v}/${a.goal.toLocaleString("pt-BR")}</small>`}</div></div>`; };
    const titles = ACH.list.filter(a => G[a.id] && (a.tipo === "titulo" || a.tipo === "honra")).sort((a, b) => G[b.id] - G[a.id]);
    const tt = (S.logs._tt && S.logs._tt.id) || "", tAt = titles.find(a => a.id === tt) || titles[0];
    let shown;
    if (this.grp === "prox") { const pend = ACH.list.filter(a => !G[a.id]).sort((a, b) => prog(b) - prog(a)).slice(0, 12), rec = ACH.list.filter(a => G[a.id]).sort((a, b) => G[b.id] - G[a.id]).slice(0, 6); shown = `<h3 class="achH">🔜 Mais perto de desbloquear</h3><div class="achGrid">${pend.map(card).join("")}</div>${rec.length ? `<h3 class="achH">🆕 Conquistas recentes</h3><div class="achGrid">${rec.map(card).join("")}</div>` : ""}`; }
    else { const lst = ACH.list.filter(a => this.grp === "all" || a.grp === this.grp); shown = Object.entries(ACH_T).map(([t, n]) => { const l = lst.filter(a => a.tipo === t); return l.length ? `<h3 class="achH">${n} <small>(${l.filter(a => G[a.id]).length}/${l.length})</small></h3><div class="achGrid">${l.sort((a, b) => (!!G[b.id]) - (!!G[a.id]) || prog(b) - prog(a)).map(card).join("")}</div>` : ""; }).join(""); }
    const sty = styleOf(st), cats = CATS.filter(([c]) => st.cat[c] && st.cat[c].tot);
    $("#jrHost").innerHTML = `
     <div class="panel jrHead"><div class="jrBig">${L.rank.split(" ")[0]}</div><div class="grow"><h2 style="margin:0">${L.rank} · Nível ${L.lv}</h2>
      ${tAt ? `<div class="jrTitle">🏷️ <b>${esc(tAt.nome)}</b>${titles.length > 1 ? ` <select id="jrTit" aria-label="Escolher título">${titles.map(a => `<option value="${a.id}" ${a === tAt ? "selected" : ""}>${esc(a.nome)}</option>`).join("")}</select>` : ""}</div>` : `<div class="jrTitle">🏷️ <small>Conquiste um 📜 título ou 🎖️ honraria para exibir aqui.</small></div>`}
      <span class="xpTrack" style="height:9px;margin:6px 0"><i style="width:${Math.round(100 * L.cur / L.need)}%"></i></span>
      <small style="color:var(--mut)">${st.xp.toLocaleString("pt-BR")} XP · faltam ${L.need - L.cur} para o nível ${L.lv + 1}</small></div></div>
     <div class="stats"><div class="stat"><b style="color:#ff8f5a">🔥 ${st.cur}</b><span>dias seguidos (recorde ${st.max})</span></div><div class="stat"><b class="n">${((S.logs[today()] || {}).xp || 0)}</b><span>XP hoje</span></div>
      <div class="stat"><b class="rv">${(st.wk[wNow] || 0).toLocaleString("pt-BR")}</b><span>XP nesta semana${pos ? ` · ${pos}º lugar` : ""}</span></div><div class="stat"><b style="color:var(--gold2)">${nGot}/${ACH.list.length}</b><span>conquistas</span></div>
      <div class="stat"><b>📆 ${st.dias}</b><span>dias de estudo · ${st.wCur} sem. seguidas</span></div><div class="stat"><b>🗓️ ${st.mes}</b><span>dias neste mês (recorde ${st.mesMax})</span></div></div>
     ${WC.html()}
     <div class="panel"><h2 style="margin-top:0">🎭 Seu estilo de estudo <small style="color:var(--mut);font-weight:400">(últimos 30 dias)</small></h2>
      <div class="styleChips"><span>${sty.hora}</span><span>${sty.ritmo}${sty.med ? ` · ${sty.med}/dia` : ""}</span><span>${sty.prec}${sty.acc ? ` · ${sty.acc}%` : ""}</span><span>${sty.foco}</span><span>${sty.div}</span></div>
      <p class="metaNow">Não existe estilo certo: o que importa é a constância. Os troféus 🎭 de estilo premiam o seu jeito de estudar — coruja de plantão, madrugador, maratonista ou gota constante.</p></div>
     ${cats.length ? `<div class="panel"><h2 style="margin-top:0">📚 Domínio por categoria</h2><div class="catGrid">${cats.map(([c, ic, nm, lbl]) => { const o = st.cat[c], p = Math.floor(100 * o.st / o.tot), tier = p >= 100 ? "👑 Mestre" : p >= 50 ? "🥇 Cavaleiro" : p >= 25 ? "🥈 Escudeiro" : p >= 10 ? "🥉 Aprendiz" : "🔒 a caminho"; return `<div class="catRow"><b>${ic} ${nm}</b> <small>${lbl}</small><span class="xpTrack"><i style="width:${p}%"></i></span><small>${p}% estudado · ${o.mat.toLocaleString("pt-BR")} maduros · ${tier}</small></div>`; }).join("")}</div></div>` : ""}
     <div class="panel"><h2 style="margin-top:0">📊 Painel de produtividade (XP)</h2><div class="charts">
      <div class="chart"><h3>📅 XP por dia (14 dias)</h3>${barSVG(xp14, d14.map(d => d.slice(8) + "/" + d.slice(5, 7)), ["#e8c56a"])}</div>
      <div class="chart"><h3>🗓️ XP por semana (12 semanas)</h3>${barSVG(wv, W.map(lab), W.map(w => w === wNow ? "#4dd4ff" : "#e8c56a"))}</div>
      <div class="chart" style="grid-column:1/-1"><h3>🧭 De onde vem seu XP</h3>${stackSVG(src.map(x => ({ n: x.n, v: x.v, c: x.c })))}
       <div class="legend">${src.map(x => `<span><i style="background:${x.c}"></i>${x.n}: <b>${x.v.toLocaleString("pt-BR")}</b> (${Math.round(100 * x.v / tot)}%)</span>`).join("")}</div></div></div></div>
     ${DOM.html()}
     <div class="panel"><h2 style="margin-top:0">🏟️ Ranking semanal de XP</h2><p class="metaNow">Suas semanas competem entre si: supere seu próprio recorde. 🥇🥈🥉</p>
      <table class="t jrRank"><tr><th>#</th><th>Semana</th><th>XP</th></tr>${rank.slice(0, 10).map(([w, v], i) => `<tr class="${+w === wNow ? "me" : ""}"><td>${["🥇", "🥈", "🥉"][i] || i + 1 + "º"}</td><td>${lab(w)}${+w === wNow ? " · esta semana" : ""}</td><td><b>${v.toLocaleString("pt-BR")}</b></td></tr>`).join("") || `<tr><td colspan=3>Estude para abrir o ranking.</td></tr>`}</table></div>
     <div class="panel"><h2 style="margin-top:0">🏰 Salão de troféus · Temporada I</h2>
      <div class="achSum">${Object.entries(ACH_T).map(([t, n]) => `<span>${n}: <b>${ACH.list.filter(a => a.tipo === t && G[a.id]).length}/${ACH.list.filter(a => a.tipo === t).length}</b></span>`).join("")}</div>
      <div class="jrChips">${Object.entries(ACH_G).map(([k, n]) => `<button class="btn sm ${k === this.grp ? "gold" : ""}" data-jrg="${k}">${n}${k !== "prox" && k !== "all" ? ` <small>${ACH.list.filter(a => a.grp === k && G[a.id]).length}/${ACH.list.filter(a => a.grp === k).length}</small>` : ""}</button>`).join("")}</div>
      ${shown}
      <p class="metaNow">✨ Bônus por conquista: medalha +20, troféu +40, título +50, brasão +80, honraria +150 XP. Categorias contam os cards das coleções ativas em ⚙️ Ajustes.</p></div>`;
    $$("#jrHost [data-jrg]").forEach(b => b.onclick = () => { this.grp = b.dataset.jrg; lsSet("jrGrp", this.grp); this.render(); });
    WC.bind($("#jrHost"));
    const ts = $("#jrTit"); if (ts) ts.onchange = () => { S.logs._tt = { id: ts.value, t: Date.now() }; saveLog(); this.render(); toast("🏷️ Título atualizado."); };
  } };
