/* ---------- ⏳ FOCO 360X (4.22.0): condicionamento de foco e atenção — escada de 5 a 25 min num único tema ---------- */
const FO = {
  DEG: [5, 8, 10, 12, 15, 18, 20, 22, 25],
  DUR: [5, 8, 10, 12, 15, 18, 20, 22, 25, 30, 35, 45],
  PZMAX: 3 * MIN,
  ANC: { deck: ["🎴", "Baralho"], q: ["❓", "Questões"], gaso: ["🧪", "Gasometria"], micro: ["💊", "Micropartículas"], mn: ["🧠", "Mnemônicos"], honra: ["🕊️", "Honra"], livre: ["📖", "Fora do app"] },
  VIEW: { deck: "estudar", q: "questoes", gaso: "gaso", micro: "micro", mn: "mnemonicos", honra: "honra" },
  PH: { deck: "", q: "Ex.: Sepse e choque séptico", gaso: "Ex.: Acidose metabólica com AG alto", micro: "Ex.: Ventilação mecânica", mn: "Ex.: Antídotos", honra: "Ex.: Bússola da paciência", livre: "Ex.: Capítulo de SDRA do livro ou aula de VM" },
  CAUSAS: [["cel", "📱 Celular"], ["pens", "💭 Pensamento"], ["ruido", "🔊 Barulho"], ["sono", "😴 Cansaço ou sono"], ["fome", "🍽️ Fome ou sede"], ["pessoa", "🗣️ Alguém chamou"], ["tedio", "🥱 Tédio"], ["outro", "❔ Outro"]],
  DICA: { cel: "📵 Na próxima, deixe o celular em outro cômodo ou dentro de uma gaveta: longe dos olhos, longe da mão.", pens: "🗒️ Assim que o pensamento surgir, toque em 🗒️, anote em 5 palavras e volte. Ele fica guardado para depois.", ruido: "🎧 Fones com ruído branco ou abafador, ou troque de lugar antes de começar.", sono: "🌬️ Comece por um bloco menor e faça a pausa ativa em pé. Prefira o seu horário de mais energia.", fome: "💧 Água e um lanche leve antes do bloco evitam a interrupção no meio.", pessoa: "🚪 Avise antes: “estou em foco por 25 minutos, depois falo com você”.", tedio: "🔀 Mude o formato sem mudar o tema: dos cards para as questões ou o caso clínico do mesmo assunto.", outro: "🧭 Revise o ritual de largada: ele tira do caminho o que mais interrompe." },
  RIT: [["cel", "📵 Celular no silencioso, virado ou em outro cômodo"], ["agua", "💧 Água por perto"], ["wc", "🚻 Banheiro resolvido"], ["mesa", "🧹 Só o material deste tema na mesa e na tela"], ["notas", "🗒️ Sei onde anotar distrações (botão 🗒️ da barra)"]],
  QL: [null, ["😵", "Disperso"], ["🌫️", "Oscilante"], ["🙂", "Razoável"], ["🎯", "Bom"], ["💎", "Imersão total"]],
  SUBS: [["sessao", "⏳ Sessão"], ["prog", "📈 Progresso"], ["nota", "🗒️ Estacionamento"], ["met", "📘 Método"]],
  sub: lsGet("foSub") || "sessao", run: null, end: null, res: null, brk: null, outV: false, outH: false, ckOn: 0, tk: null, ac: null, wl: null,
  selDur: 0, rit: {}, resp: 0, conf: 0,
  R() { const r = (S.logs._fo = S.logs._fo || {}); if (!r.s || typeof r.s !== "object") r.s = {}; if (!r.p || typeof r.p !== "object") r.p = {}; return r; },
  opt(k, d) { const v = lsGet("fo_" + k); return v === null ? d : v === "1"; },
  setOpt(k, v) { lsSet("fo_" + k, v ? "1" : "0"); },
  ls(k) { try { const v = lsGet(k); return v ? JSON.parse(v) : null; } catch (e) { return null; } },
  mmss(ms) { const s = Math.max(0, Math.ceil(ms / 1000)); return Math.floor(s / 60) + ":" + String(s % 60).padStart(2, "0"); },
  m1(ms) { return Math.round(ms / 6000) / 10; },
  fmt(n) { return (Math.round(n * 10) / 10).toLocaleString("pt-BR"); },
  anc(r) { const a = this.ANC[r.an] || this.ANC.livre; return `${a[0]} ${esc(r.nm || a[1])}`; },
  sessions() { return Object.values(this.R().s).filter(x => x && x.t0).sort((a, b) => a.t0 - b.t0); },

  /* ---- 🪜 escada: refeita a partir do histórico (sincroniza sem conflito entre aparelhos) ---- */
  ladder() {
    const R = this.R(), b = R.b && typeof R.b === "object" ? R.b : null, N = this.DEG.length;
    let i = b ? Math.max(0, Math.min(N - 1, b.d | 0)) : 0, ok = 0, bad = 0, top = i;
    for (const x of this.sessions()) {
      if (!x.lad || (b && (x.te || x.t0) <= b.t) || x.dur !== this.DEG[i]) continue;
      if (x.cl) { ok++; bad = 0; if (ok >= 2 && i < N - 1) { i++; ok = 0; } else if (ok > 2) ok = 2; }
      else if (x.tr) { bad++; ok = 0; if (bad >= 2 && i > 0) { i--; bad = 0; } }
      top = Math.max(top, i);
    }
    return { i, min: this.DEG[i], ok, bad, top: this.DEG[top], last: i === N - 1, set: !!b };
  },
  stats() {
    const ss = this.sessions(), n = ss.length, min = ss.reduce((a, x) => a + (x.min || 0), 0), l7 = ss.slice(-7);
    const avg7 = l7.length ? l7.reduce((a, x) => a + (x.min || 0), 0) / l7.length : 0;
    const days = [...new Set(ss.map(x => dayKey(x.t0)))].sort(); let run = 0, maxRun = 0, prev = 0;
    for (const d of days) { const t = new Date(d + "T12:00").getTime(); run = prev && Math.round((t - prev) / DAY) === 1 ? run + 1 : 1; maxRun = Math.max(maxRun, run); prev = t; }
    let cur = 0; const on = new Set(days); for (let k = on.has(today()) ? 0 : 1; on.has(dayKey(Date.now() - k * DAY)); k++) cur++;
    const ck = ss.reduce((a, x) => [a[0] + ((x.ck || [])[0] || 0), a[1] + ((x.ck || [])[1] || 0)], [0, 0]);
    const cs = {}; for (const x of ss) for (const c of x.cs || []) cs[c] = (cs[c] || 0) + 1;
    return { n, min: Math.round(min), avg7, l7: l7.length, cl: ss.filter(x => x.cl).length, z25: ss.filter(x => x.cl && x.dur >= 25).length, rt: ss.reduce((a, x) => a + (x.rt || 0), 0),
      dv: ss.reduce((a, x) => a + (x.dv || 0), 0), cur, maxRun, ck, cs, top: this.ladder().top, ss, hoje: ss.filter(x => dayKey(x.t0) === today()).length };
  },

  /* ---- ciclo de vida ---- */
  init() {
    this.run = this.ls("foRun"); this.end = this.ls("foEnd"); this.brk = this.ls("foBrk");
    const now = Date.now();
    if (this.run && (!this.run.t0 || now - this.run.t0 > 6 * 3600000)) { this.run = null; lsSet("foRun", ""); }
    if (this.run) {   // app fechado ou recarregado no meio do bloco: o intervalo sem o app conta como fora do tema
      const r = this.run, gap = now - (r.ls || now);
      if (r.pz) { if (now - r.pz > this.PZMAX) { r.pzT += this.PZMAX; r.pz = 0; } }
      else if (gap > 5000 && r.an !== "livre") { r.foT += Math.min(gap, Math.max(0, r.t0 + r.dur * MIN + r.pzT - (r.ls || now))); r.dv++; }
      r.fo = 0; r.ls = now; this.save();
    }
    if (this.brk && now - this.brk.t0 > this.brk.dur * MIN + 30 * MIN) { this.brk = null; lsSet("foBrk", ""); }
    const host = $("header"); if (host && !$("#foBar")) { const d = document.createElement("div"); d.id = "foBar"; d.className = "foBar vozSkip"; d.hidden = true; d.setAttribute("role", "status"); host.appendChild(d); }
    if (!$("#foNote")) { const d = document.createElement("div"); d.id = "foNote"; d.className = "foNote vozSkip"; d.hidden = true;
      d.innerHTML = `<b>🗒️ Estacionar pensamento</b><small>Anote em poucas palavras e volte ao tema. Fica guardado na aba ⏳ Foco.</small><input id="foNoteIn" maxlength="160" placeholder="Ex.: pagar a conta · responder o grupo · pesquisar X" autocomplete="off"><div class="row"><button class="btn gold sm" data-fo="notaOk">💾 Guardar e voltar</button><button class="btn sm" data-fo="notaX">Cancelar</button></div>`;
      document.body.appendChild(d); }
    document.addEventListener("click", e => { const b = e.target.closest("[data-fo],[data-foq],[data-foc],[data-foan],[data-fodur],[data-forit],[data-fobase],[data-fosub],[data-foopt],[data-fopk]"); if (b) this.click(b, e); });
    document.addEventListener("keydown", e => { if (e.target && e.target.id === "foNoteIn") { if (e.key === "Enter") { e.preventDefault(); this.act("notaOk"); } else if (e.key === "Escape") this.act("notaX"); } });
    document.addEventListener("visibilitychange", () => { this.outH = document.visibilityState === "hidden"; if (this.run) { this.sync(); if (!this.outH) this.lock(); } });
    clearInterval(this.tk); this.tk = setInterval(() => this.tick(), 1000);
    this.bar();
  },
  save() { if (this.run) { this.run.ls = Date.now(); lsSet("foRun", JSON.stringify(this.run)); } else lsSet("foRun", ""); },
  times(now = Date.now()) {
    const r = this.run, pz = r.pzT + (r.pz ? now - r.pz : 0), el = Math.max(0, Math.min(r.dur * MIN, now - r.t0 - pz)), fo = Math.min(el, r.foT + (r.fo ? now - r.fo : 0));
    return { el, rem: r.dur * MIN - el, fo, no: Math.max(0, el - fo) };
  },
  isOut() { const r = this.run; return !!r && r.an !== "livre" && !r.pz && (this.outV || this.outH); },
  sync(now = Date.now()) {   // entra ou sai do estado "fora do tema" (outra aba, outro app ou tela apagada)
    const r = this.run; if (!r) return;
    const out = this.isOut();
    if (out && !r.fo) { r.fo = now; r.foS = now; }
    else if (!out && r.fo) { r.foT += now - r.fo; const seg = now - (r.foS || r.fo); r.fo = 0; if (seg > 5000 && !r.pz) { r.dv++; toast("🔁 <b>De volta ao tema.</b> Perceber e voltar também é treino.", 2600); } }
    this.save(); this.bar();
  },
  route(view) {
    if (!this.run) { this.outV = false; return; }
    const ok = this.run.an === "livre" || view === "foco" || view === this.VIEW[this.run.an];
    if (this.outV !== !ok) { this.outV = !ok; this.sync(); }
  },
  tick() {
    const now = Date.now();
    if (this.brk) { const rem = this.brk.t0 + this.brk.dur * MIN - now; if (rem <= 0) { this.brk = null; lsSet("foBrk", ""); this.beep("fim"); toast("☕ <b>Pausa encerrada.</b> Pronto para o próximo bloco?", 4500); this.bar(); if (location.hash === "#foco") this.render(); } else this.paintBrk(rem); }
    const r = this.run; if (!r) return;
    if (r.pz && now - r.pz >= this.PZMAX) { this.act("retoma"); toast("▶️ A pausa de 3 min acabou — o bloco continua.", 3000); }
    if (!r.pz && document.visibilityState === "visible") this.save();
    const T = this.times(now);
    if (T.rem <= 0) return this.finish(true);
    if (this.ckOn && now - this.ckOn > 45000) { this.ckOn = 0; r.nck = now + this.nextCk(); this.bar(); }
    if (this.opt("ck", true) && !r.pz && !this.ckOn && now >= r.nck && T.rem > 2 * MIN && T.el > 2 * MIN && document.visibilityState === "visible" && !this.isOut()) this.ckShow();
    if (!r.half && T.el >= r.dur * MIN / 2 && r.dur >= 8) { r.half = 1; this.save(); toast("⏳ <b>Metade do caminho.</b> Siga no mesmo tema.", 2500); }
    if (!r.l2 && T.rem <= 2 * MIN && r.dur >= 8) { r.l2 = 1; this.save(); toast("🏁 <b>Últimos 2 minutos.</b> Feche o raciocínio.", 2500); }
    this.paint(T);
  },
  nextCk() { return (4 + Math.random() * 4) * MIN; },
  lock() { if (!this.opt("wl", true) || !this.run || !("wakeLock" in navigator)) return; try { navigator.wakeLock.request("screen").then(l => { this.wl = l; }).catch(() => { }); } catch (e) { } },
  unlock() { try { if (this.wl) this.wl.release(); } catch (e) { } this.wl = null; },
  beep(kind) {
    if (this.opt("som", true)) try {
      const C = this.ac || (this.ac = new (window.AudioContext || window.webkitAudioContext)()); if (C.state === "suspended") C.resume();
      const t = C.currentTime, notes = kind === "fim" ? [523.25, 659.25, 783.99] : kind === "ck" ? [880, 1174.66] : [659.25];
      notes.forEach((f, i) => { const o = C.createOscillator(), g = C.createGain(), s = t + i * 0.18; o.type = "sine"; o.frequency.value = f; g.gain.setValueAtTime(0.0001, s); g.gain.exponentialRampToValueAtTime(0.16, s + 0.02); g.gain.exponentialRampToValueAtTime(0.0001, s + 0.6); o.connect(g); g.connect(C.destination); o.start(s); o.stop(s + 0.65); });
    } catch (e) { }
    try { if (navigator.vibrate) navigator.vibrate(kind === "fim" ? [120, 80, 120] : 60); } catch (e) { }
  },
  speak(t) { if (this.opt("voz", false) && VOZ.ok) VOZ.say(t, { label: "Foco" }); },

  /* ---- ações ---- */
  start() {
    const an = lsGet("foAn") || "deck", L = this.ladder(), dur = this.selDur || L.min, now = Date.now();
    let nm = "", prefix = null;
    if (an === "deck") { prefix = ($("#foDeck") || {}).value || lsGet("foDeck") || ""; if (!prefix) return toast("🎴 Escolha o baralho do tema."); lsSet("foDeck", prefix); nm = prefix.split("::").pop(); }
    else { nm = (($("#foNm") || {}).value || "").trim().slice(0, 80); if (an === "livre" && !nm) return toast("📖 Escreva qual é o tema (livro, aula ou artigo)."); lsSet("foNm", nm); }
    const meta = (($("#foMeta") || {}).value || "").trim().slice(0, 140), se = (($("#foSe") || {}).value || "").trim().slice(0, 140);
    if (se) lsSet("foSe", se);
    const nr = this.RIT.filter(([k]) => this.rit[k]).length, rit = nr >= 4 && !!meta ? 1 : 0;
    this.end = null; this.res = null; lsSet("foEnd", ""); this.brk = null; lsSet("foBrk", "");
    this.run = { id: "F" + now.toString(36) + Math.random().toString(36).slice(2, 6), t0: now, dur, an, nm, prefix, lad: dur === L.min ? 1 : 0, deg: L.min, rit, resp: this.resp ? 1 : 0, meta, se,
      pz: 0, pzT: 0, pzN: 0, fo: 0, foT: 0, dv: 0, rt: 0, ck: [0, 0], nck: now + this.nextCk(), half: 0, l2: 0 };
    this.rit = {}; this.resp = 0; this.selDur = 0; this.tmp = {}; this.outH = document.visibilityState === "hidden"; this.outV = false;
    this.beep("ini"); this.lock(); this.save();
    this.speak(`Foco de ${dur} minutos. Tema: ${nm || this.ANC[an][1]}. Começou.`);
    toast(`⏳ <b>Foco de ${dur} min começou</b> · ${this.anc(this.run)}${meta ? " · meta: " + esc(meta) : ""}`, 3500);
    if (an === "deck") { if (Study.prefix === prefix && Study.started) location.hash = "estudar"; else startStudy(prefix); }
    else if (this.VIEW[an]) location.hash = this.VIEW[an];
    else this.render();
    this.route((location.hash || "#inicio").slice(1)); this.bar();
  },
  finish(done) {
    const r = this.run; if (!r) return; const now = Date.now();
    if (r.pz) { r.pzT += now - r.pz; r.pz = 0; }
    if (r.fo) { r.foT += now - r.fo; if (now - (r.foS || r.fo) > 5000) r.dv++; r.fo = 0; }
    const T = this.times(now);
    this.end = { id: r.id, t0: r.t0, dur: r.dur, an: r.an, nm: r.nm, prefix: r.prefix, lad: r.lad, deg: r.deg, rit: r.rit, meta: r.meta, done: done ? 1 : 0,
      el: this.m1(T.el), min: this.m1(T.no), dv: r.dv, rt: r.rt, ck: r.ck, pzN: r.pzN, q: 0, cs: [] };
    this.run = null; this.ckOn = 0; this.save(); lsSet("foEnd", JSON.stringify(this.end)); this.unlock();
    this.beep("fim"); this.speak(done ? "Bloco de foco concluído. Registre como foi." : "Bloco encerrado.");
    toast(done ? "✅ <b>Bloco de foco concluído!</b> Registre como foi." : "⏹️ Bloco encerrado. Registre como foi.", 4000);
    this.sub = "sessao"; lsSet("foSub", "sessao"); this.bar();
    if (location.hash !== "#foco") location.hash = "foco"; else this.render();
  },
  record(skip) {
    const e = this.end; if (!e) return; const L0b = this.ladder(), pct = e.dur ? e.min / e.dur : 0;
    const cl = e.done && pct >= 0.9 && e.dv <= 2 && (skip || e.q >= 3) ? 1 : 0, tr = (!e.done && e.el < 0.6 * e.dur) || pct < 0.7 ? 1 : 0;
    const rec = { t0: e.t0, te: Date.now(), dur: e.dur, an: e.an, nm: e.nm, lad: e.lad, el: e.el, min: e.min, dv: e.dv, rt: e.rt, ck: e.ck, q: skip ? 0 : e.q, cs: skip ? [] : e.cs, done: e.done, cl, tr, rit: e.rit };
    if (e.meta) rec.meta = e.meta;
    this.R().s[e.id] = rec;
    const L1 = this.ladder(), up = L1.i > L0b.i && e.lad, down = L1.i < L0b.i && e.lad;
    const xp = { base: Math.min(e.dur, Math.round(e.min)), cl: cl ? 10 : 0, rit: e.rit ? 5 : 0, rt: Math.min(10, 2 * (e.rt || 0)), ref: skip ? 0 : 3, up: up ? 15 : 0 };
    rec.xp = Object.values(xp).reduce((a, b) => a + b, 0);
    const L = L0(); L.foN = (L.foN || 0) + 1; L.foM = (L.foM || 0) + Math.round(e.min);
    this.res = { rec, xp, up, down, L: L1, top: (e.cs || [])[0] || "" };
    this.end = null; lsSet("foEnd", "");
    saveLog(); if (rec.xp) addXP(rec.xp, "foco", "o");
    if (up) toast(`🪜 <b>Subiu de degrau:</b> agora ${L1.min} min!`, 4500);
    this.render(); this.bar();
  },
  click(b, ev) {
    const d = b.dataset;
    if (d.fo) { ev.preventDefault(); return this.act(d.fo, b); }
    if (d.fosub) { this.sub = d.fosub; lsSet("foSub", d.fosub); return this.render(); }
    if (d.foan) { lsSet("foAn", d.foan); return this.render(); }
    if (d.fodur) { this.selDur = +d.fodur; return this.render(); }
    if (d.forit) { this.rit[d.forit] = !this.rit[d.forit]; b.classList.toggle("on", !!this.rit[d.forit]); b.setAttribute("aria-pressed", this.rit[d.forit] ? "true" : "false"); return; }
    if (d.fobase) { const R = this.R(); R.b = { d: Math.max(0, this.DEG.indexOf(+d.fobase)), t: Date.now() }; saveLog(); this.selDur = 0; this.conf = 0; toast(`🪜 Ponto de partida: <b>${d.fobase} min</b>. A escada sobe com 2 sessões limpas seguidas.`, 4000); return this.render(); }
    if (d.foq && this.end) { this.end.q = +d.foq; lsSet("foEnd", JSON.stringify(this.end)); return this.render(); }
    if (d.foc && this.end) { const c = d.foc, l = this.end.cs = this.end.cs || []; const i = l.indexOf(c); if (i >= 0) l.splice(i, 1); else l.push(c); lsSet("foEnd", JSON.stringify(this.end)); b.classList.toggle("on", i < 0); return; }
    if (d.foopt) { const k = d.foopt, v = !this.opt(k, k !== "voz"); this.setOpt(k, v); b.classList.toggle("on", v); b.setAttribute("aria-pressed", v ? "true" : "false"); if (k === "wl") v ? this.lock() : this.unlock(); return; }
    if (d.fopk) { const R = this.R(), p = R.p[d.fopk]; if (!p) return; if (b.dataset.k === "ok") p.d = Date.now(); else p.del = 1; saveLog(); return this.render(); }
  },
  act(a, b) {
    const r = this.run, now = Date.now();
    switch (a) {
      case "go": return this.start();
      case "volta": if (!r) return; if (r.an === "deck") { if (Study.prefix === r.prefix && Study.started) location.hash = "estudar"; else startStudy(r.prefix); } else location.hash = this.VIEW[r.an] || "foco"; return;
      case "dist": if (!r) return; r.rt++; this.save(); this.bar(); this.paint(); return toast("🔁 <b>Notou e voltou: +1 retorno.</b> É exatamente o músculo que estamos treinando.", 2600);
      case "nota": { const n = $("#foNote"); n.hidden = false; const i = $("#foNoteIn"); i.value = ""; setTimeout(() => i.focus(), 30); return; }
      case "notaX": $("#foNote").hidden = true; return;
      case "notaOk": { const x = ($("#foNoteIn").value || "").trim(); $("#foNote").hidden = true; if (!x) return; const R = this.R(); R.p["P" + now.toString(36) + Math.random().toString(36).slice(2, 5)] = { x: x.slice(0, 160), t: now, d: 0 }; if (r) { r.pk = (r.pk || 0) + 1; this.save(); } saveLog(); toast("🗒️ <b>Estacionado.</b> Agora volte ao tema — depois você resolve.", 2600); if (location.hash === "#foco" && !r) this.render(); return; }
      case "ckS": case "ckN": if (!r) return; r.ck[1]++; if (a === "ckS") r.ck[0]++; else r.rt++; this.ckOn = 0; r.nck = now + this.nextCk(); this.save(); this.bar(); this.paint();
        return toast(a === "ckS" ? "✅ No tema. Siga assim." : "🔁 <b>Percebeu e voltou: +1 retorno.</b>", 2200);
      case "pausa": if (!r || r.pz) return; if (r.pzN >= 1) return toast("⏸️ A pausa de emergência já foi usada neste bloco."); r.pz = now; r.pzN++; this.sync(); this.render(); return toast("⏸️ Pausa de até 3 min. O relógio do bloco parou.", 2600);
      case "retoma": if (!r || !r.pz) return; r.pzT += Math.min(this.PZMAX, now - r.pz); r.pz = 0; this.sync(); this.render(); return;
      case "parar": if (!r) return; if (!this.conf) { this.conf = 1; this.render(); clearTimeout(this._cf); this._cf = setTimeout(() => { this.conf = 0; if (location.hash === "#foco") this.render(); }, 4000); return; } this.conf = 0; return this.finish(false);
      case "sim": if (!r || r.an !== "deck") return; return startSim(null, r.prefix, 50);
      case "salvar": return this.record(false);
      case "pular": return this.record(true);
      case "brk": { const n = this.stats().hoje, dur = n && n % 4 === 0 ? 15 : 5; this.brk = { t0: now, dur }; lsSet("foBrk", JSON.stringify(this.brk)); this.res = null; this.bar(); this.render(); return toast(`☕ Pausa ativa de ${dur} min começou.`, 2500); }
      case "brkEnd": this.brk = null; lsSet("foBrk", ""); this.bar(); this.render(); return;
      case "novo": this.res = null; this.render(); return;
      case "resp": return this.breathe(b);
      case "recal": { const R = this.R(); delete R.b; saveLog(); this.sub = "sessao"; lsSet("foSub", "sessao"); this.render(); return toast("🪜 Escolha de novo o ponto de partida."); }
      case "limpaPk": { const R = this.R(); let n = 0; for (const p of Object.values(R.p)) if (p && p.d && !p.del) { p.del = 1; n++; } saveLog(); this.render(); return toast(`🧹 ${n} item(ns) resolvido(s) arquivado(s).`); }
    }
  },
  breathe(b) {   // 3 ciclos de 4 s inspirando e 6 s soltando (30 s)
    const box = $("#foResp"); if (!box || box.dataset.on) return; box.dataset.on = "1"; let k = 0;
    const step = () => {
      if (k >= 6) { delete box.dataset.on; box.className = "foResp ok"; box.textContent = "✅ 3 respirações"; this.resp = 1; return; }
      const ins = k % 2 === 0; box.className = "foResp " + (ins ? "in" : "out"); box.textContent = (ins ? "🌬️ Inspire… " : "😮‍💨 Solte… ") + (Math.floor(k / 2) + 1) + "/3";
      k++; setTimeout(step, ins ? 4000 : 6000);
    };
    step();
  },
  ckShow() { this.ckOn = Date.now(); this.beep("ck"); this.bar(); },

  /* ---- barra fixa no topo (visível em todas as abas) ---- */
  bar() {
    const el = $("#foBar"); if (!el) return; const r = this.run;
    if (!r && !this.brk && !this.end) { el.hidden = true; el.innerHTML = ""; return; }
    el.hidden = false; el.className = "foBar vozSkip";
    if (this.end && !r) { el.innerHTML = `<a href="#foco" class="foClk">✅ <b>Bloco de foco encerrado</b></a><a class="btn sm gold" href="#foco">📝 Registrar ›</a>`; return; }
    if (!r && this.brk) { el.classList.add("brk"); el.innerHTML = `<a href="#foco" class="foClk">☕ Pausa ativa · <b id="foBT">${this.mmss(this.brk.t0 + this.brk.dur * MIN - Date.now())}</b></a><span class="foNm">levante, água, olhe longe</span><button class="btn sm" data-fo="brkEnd">⏭️ Encerrar pausa</button>`; return; }
    const T = this.times(), out = this.isOut();
    if (r.pz) { el.classList.add("pz"); el.innerHTML = `<a href="#foco" class="foClk">⏸️ Pausa · <b id="foBT">${this.mmss(this.PZMAX - (Date.now() - r.pz))}</b></a><span class="foNm">${this.anc(r)}</span><button class="btn sm gold" data-fo="retoma">▶️ Retomar</button>`; return; }
    if (this.ckOn) { el.classList.add("ck"); el.innerHTML = `<span class="foClk">🧭 <b>Você está no tema agora?</b></span><button class="btn sm gold" data-fo="ckS">✅ Sim</button><button class="btn sm" data-fo="ckN">😵 Divaguei, voltei</button>`; return; }
    if (out) el.classList.add("out");
    el.innerHTML = `<a href="#foco" class="foClk" title="Abrir a aba Foco">⏳ <b id="foBT">${this.mmss(T.rem)}</b></a><span class="foNm">${this.anc(r)}</span><span class="foSt" id="foBS" title="desvios · retornos">↪️ ${r.dv} · 🔁 ${r.rt}</span>`
      + (out ? `<button class="btn sm gold" data-fo="volta">🧭 Fora do tema · ↩️ Voltar</button>` : `<button class="btn sm" data-fo="dist" title="Me distraí e voltei (+1 retorno)" aria-label="Me distraí e voltei">😵 Voltei</button><button class="btn sm" data-fo="nota" title="Estacionar um pensamento" aria-label="Estacionar um pensamento">🗒️</button>`);
  },
  paint(T) {
    const r = this.run; if (!r) return; T = T || this.times();
    const bt = $("#foBT"); if (bt && !r.pz && !this.ckOn) bt.textContent = this.mmss(T.rem); else if (bt && r.pz) bt.textContent = this.mmss(this.PZMAX - (Date.now() - r.pz));
    const bs = $("#foBS"); if (bs) bs.textContent = `↪️ ${r.dv} · 🔁 ${r.rt}`;
    if (location.hash !== "#foco") return;
    const c = $("#foArc"); if (c) c.style.strokeDashoffset = String(339.29 * (T.rem / (r.dur * MIN)));
    const t = $("#foTime"); if (t) t.textContent = r.pz ? "⏸️" : this.mmss(T.rem);
    const nt = $("#foNo"); if (nt) nt.textContent = `${this.fmt(T.no / MIN)} min no tema (${Math.round(100 * T.no / Math.max(1, T.el))}%)`;
    const dv = $("#foDv"); if (dv) dv.textContent = `↪️ ${r.dv} desvio(s) · 🔁 ${r.rt} retorno(s) · 🧭 ${r.ck[0]}/${r.ck[1]} no tema`;
  },
  paintBrk(rem) { const bt = $("#foBT"); if (bt && !this.run) bt.textContent = this.mmss(rem); const t = $("#foBrkT"); if (t) t.textContent = this.mmss(rem); },

  /* ---- aba ⏳ Foco ---- */
  open() { this.render(); },
  head(st, L) {
    const avg = st.avg7, pc = Math.min(100, Math.round(100 * avg / 25));
    const steps = this.DEG.map((m, i) => `<span class="foStep ${i < L.i ? "ok" : i === L.i ? "cur" : ""}" title="${m} min">${m}</span>`).join("");
    return `<div class="panel foHead"><div class="foTop"><div class="foBig">⏳</div><div class="grow"><h2 style="margin:0">Foco 360X</h2><small class="foSub">Condicionamento de foco e atenção: um tema por vez, subindo até 25 minutos.</small></div></div>
     <div class="foLad" aria-label="Escada do foco">${steps}</div>
     <div class="foKpi"><div><b>${L.min} min</b><span>🪜 degrau ${L.i + 1}/${this.DEG.length}${L.last ? " · Zona 25" : ` · ${L.ok}/2 limpas para subir`}</span></div>
      <div><b>${st.l7 ? this.fmt(avg) : "—"} min</b><span>📊 média no tema (últimas ${st.l7 || 7})</span><span class="xpTrack"><i style="width:${pc}%"></i></span></div>
      <div><b>${st.cur}</b><span>🔥 dia(s) seguidos com foco</span></div><div><b>${st.min.toLocaleString("pt-BR")}</b><span>⏱️ minutos no tema (total)</span></div></div></div>`;
  },
  render() {
    const h = $("#foHost"); if (!h) return;
    const st = this.stats(), L = this.ladder();
    const tabs = `<div class="hoSubs foSubs">${this.SUBS.map(([k, l]) => `<button class="btn ${k === this.sub ? "gold" : ""}" data-fosub="${k}">${l}${k === "nota" ? ` (${this.pk().filter(p => !p.d).length})` : ""}</button>`).join("")}</div>`;
    if (!this.run && !this.end && !this.res) { const keep = {}; for (const id of ["foMeta", "foSe", "foNm", "foDeck"]) { const el = $("#" + id); if (el) keep[id] = el.value; } this.tmp = Object.assign(this.tmp || {}, keep); }
    let body = "";
    if (this.sub === "prog") body = this.vProg(st, L); else if (this.sub === "nota") body = this.vNota(); else if (this.sub === "met") body = this.vMet();
    else body = this.run ? this.vRun() : this.end ? this.vEnd() : this.res ? this.vRes() : this.brk ? this.vBrk() : !L.set ? this.vBase() : this.vSetup(L);
    h.innerHTML = this.head(st, L) + tabs + body;
    if (this.run) this.paint();
  },
  vBase() {
    return `<div class="panel foCard"><h3>🪜 Ponto de partida</h3><p>Quanto tempo você consegue hoje, num só tema, <b>sem pegar no celular nem trocar de assunto</b>? Escolha um valor confortável: a escada sobe sozinha quando ficar fácil.</p>
     <div class="foChips">${[5, 8, 10, 12, 15, 20, 25].map(m => `<button class="btn" data-fobase="${m}">${m} min</button>`).join("")}</div>
     <p class="metaNow">Na dúvida, comece por <b>10 min</b>. Duas sessões limpas seguidas sobem um degrau; dois tropeços seguidos descem um, sem culpa: a escada se ajusta a você.</p></div>`;
  },
  decks() { return [...new Set(S.cards.flatMap(c => { const p = c.deck.split("::"); return p.map((_, i) => p.slice(0, i + 1).join("::")); }))].sort((a, b) => a.localeCompare(b, "pt", { numeric: true })); },
  vSetup(L) {
    const an = this.ANC[lsGet("foAn")] ? lsGet("foAn") : "deck", dur = this.selDur || L.min, T = this.tmp || {}, deck = T.foDeck ?? (lsGet("foDeck") || "");
    const ancB = Object.entries(this.ANC).map(([k, [ic, nm]]) => `<button class="btn sm ${k === an ? "gold" : ""}" data-foan="${k}" aria-pressed="${k === an}">${ic} ${nm}</button>`).join("");
    const pick = an === "deck" ? `<select id="foDeck" class="grow" aria-label="Baralho do tema"><option value="">Escolha o baralho…</option>${this.decks().map(n => `<option value="${esc(n)}" ${n === deck ? "selected" : ""}>${esc(n.replace(/[^:]+::/g, "· "))}</option>`).join("")}</select>`
      : `<input id="foNm" class="grow" maxlength="80" placeholder="${esc(this.PH[an])}" value="${esc(T.foNm ?? (lsGet("foNm") || ""))}" aria-label="Tema da sessão">`;
    const durB = this.DUR.map(m => `<button class="btn sm ${m === dur ? "gold" : ""} ${this.DEG.includes(m) ? "" : "x"}" data-fodur="${m}">${m}${m === L.min ? " 🪜" : ""}</button>`).join("");
    const opt = (k, d, lb) => `<button class="btn sm foOpt ${this.opt(k, d) ? "on" : ""}" data-foopt="${k}" aria-pressed="${this.opt(k, d)}">${lb}</button>`;
    return `<div class="panel foCard"><h3>1️⃣ Âncora: o único tema deste bloco</h3><div class="foChips">${ancB}</div><div class="row" style="margin-top:8px">${pick}</div>
      <p class="metaNow">${an === "livre" ? "📖 Fora do app: o relógio corre aqui e as 🧭 checagens perguntam se você segue no tema." : `Sair de ${this.ANC[an][0]} ${this.ANC[an][1]} (outra aba ou outro app) conta como <b>desvio</b> e o tempo fora não entra como foco.`}</p></div>
     <div class="panel foCard"><h3>2️⃣ Duração</h3><div class="foChips">${durB}</div>
      <p class="metaNow">${dur === L.min ? `🪜 <b>Sessão de degrau</b> (${L.min} min): conta para subir a escada.` : `🆓 <b>Sessão livre</b> (${dur} min): dá XP e entra na média, mas não mexe na escada (o degrau atual é ${L.min} min).`}</p></div>
     <div class="panel foCard"><h3>3️⃣ Ritual de largada <small>(1 min · +5 XP)</small></h3>
      <div class="foRit">${this.RIT.map(([k, l]) => `<button class="foChk ${this.rit[k] ? "on" : ""}" data-forit="${k}" aria-pressed="${!!this.rit[k]}">${l}</button>`).join("")}</div>
      <label class="foLbl">🎯 Meta concreta deste bloco<input id="foMeta" maxlength="140" placeholder="Ex.: 30 cards de choque · 10 questões de sepse · 8 páginas do capítulo" value="${esc(T.foMeta || "")}"></label>
      <label class="foLbl">🧭 Se eu me distrair, então…<input id="foSe" maxlength="140" value="${esc(T.foSe ?? (lsGet("foSe") || "anoto no 🗒️ em 5 palavras e volto ao tema"))}"></label>
      <div class="row" style="margin-top:8px"><button class="btn sm" data-fo="resp">🌬️ 3 respirações (30 s)</button><span id="foResp" class="foResp">${this.resp ? "✅ 3 respirações" : ""}</span></div>
      <p class="metaNow">O bônus do ritual vale com 4 dos 5 itens marcados e a meta escrita.</p></div>
     <div class="panel foCard"><h3>⚙️ Durante o bloco</h3><div class="foChips">${opt("som", true, "🔔 Som e vibração")}${opt("ck", true, "🧭 Checagens de presença")}${opt("voz", false, "🗣️ Avisos por voz")}${opt("wl", true, "💡 Tela sempre ligada")}</div>
      <p class="metaNow">🧭 A cada 4 a 8 min, a barra do topo pergunta se você está no tema. Responder com honestidade é o treino: notar a divagação e voltar.</p></div>
     <button class="btn gold foGo" data-fo="go">▶️ Começar foco de ${dur} min</button>`;
  },
  vRun() {
    const r = this.run, out = this.isOut();
    return `<div class="panel foRun ${out ? "out" : ""}"><div class="foRing" role="timer" aria-label="Tempo restante do bloco"><svg viewBox="0 0 120 120" aria-hidden="true"><circle cx="60" cy="60" r="54" class="bg"/><circle id="foArc" cx="60" cy="60" r="54" class="fg" stroke-dasharray="339.29" stroke-dashoffset="339.29"/></svg><div class="foRingT"><b id="foTime">--:--</b><small>${r.dur} min · ${r.lad ? "🪜 degrau" : "🆓 livre"}</small></div></div>
      <div class="foInfo"><div class="foAnc">${this.anc(r)}</div>${r.meta ? `<div class="foMeta">🎯 ${esc(r.meta)}</div>` : ""}${r.se ? `<div class="foMeta">🧭 Se me distrair: ${esc(r.se)}</div>` : ""}
       <div id="foNo" class="foLive"></div><div id="foDv" class="foLive"></div>
       ${r.pz ? `<div class="foMeta">⏸️ Em pausa (até 3 min). O tempo do bloco está parado.</div>` : ""}
       <div class="foChips" style="margin-top:10px">${r.an !== "livre" ? `<button class="btn gold sm" data-fo="volta">↩️ Ir para o tema</button>` : ""}${r.an === "deck" ? `<button class="btn sm" data-fo="sim" title="Quando não houver cards pendentes no baralho">🎲 Simulado do mesmo baralho</button>` : ""}
        <button class="btn sm" data-fo="dist">😵 Me distraí, voltei</button><button class="btn sm" data-fo="nota">🗒️ Estacionar pensamento</button>
        ${r.pz ? `<button class="btn sm gold" data-fo="retoma">▶️ Retomar</button>` : `<button class="btn sm" data-fo="pausa" ${r.pzN ? "disabled" : ""}>⏸️ Pausa de emergência</button>`}
        <button class="btn sm ${this.conf ? "red" : ""}" data-fo="parar">${this.conf ? "⚠️ Toque de novo para encerrar" : "🛑 Encerrar"}</button></div></div></div>
     <p class="metaNow">🔁 <b>Divagar é normal:</b> o treino não é nunca se distrair, é perceber mais cedo e voltar. Cada “😵 voltei” e cada 🧭 respondida com honestidade fortalecem esse retorno.</p>`;
  },
  vEnd() {
    const e = this.end, pct = e.dur ? Math.round(100 * e.min / e.dur) : 0;
    return `<div class="panel foCard foEndC"><h3>${e.done ? "✅ Bloco concluído" : "⏹️ Bloco encerrado antes do tempo"} · ${this.anc(e)}</h3>
     <div class="foKpi"><div><b>${this.fmt(e.el)}/${e.dur}</b><span>⏱️ minutos do bloco</span></div><div><b>${this.fmt(e.min)} min</b><span>🎯 no tema (${pct}%)</span></div><div><b>${e.dv}</b><span>↪️ desvios</span></div><div><b>${e.rt}</b><span>🔁 retornos percebidos</span></div><div><b>${e.ck[0]}/${e.ck[1]}</b><span>🧭 checagens no tema</span></div></div>
     ${e.meta ? `<p class="foMeta">🎯 Meta: ${esc(e.meta)}</p>` : ""}
     <h4>Como foi a qualidade do foco?</h4><div class="foChips">${[1, 2, 3, 4, 5].map(i => `<button class="btn sm ${e.q === i ? "gold" : ""}" data-foq="${i}">${this.QL[i][0]} ${i} · ${this.QL[i][1]}</button>`).join("")}</div>
     <h4>O que mais puxou a sua atenção? <small>(opcional)</small></h4><div class="foChips">${this.CAUSAS.map(([k, l]) => `<button class="foChk ${(e.cs || []).includes(k) ? "on" : ""}" data-foc="${k}">${l}</button>`).join("")}</div>
     <div class="row" style="margin-top:12px"><button class="btn gold" data-fo="salvar" ${e.q ? "" : "disabled"}>💾 Registrar e ver o XP</button><button class="btn sm" data-fo="pular">Pular</button></div>
     ${e.q ? "" : `<p class="metaNow">Escolha a qualidade de 1 a 5 para registrar.</p>`}</div>`;
  },
  vRes() {
    const { rec, xp, up, down, L, top } = this.res, n = this.stats().hoje, longa = n && n % 4 === 0;
    const tit = rec.cl ? "🏅 Sessão limpa!" : rec.tr ? "🌱 Bloco de recalibração" : "👍 Bloco registrado";
    const lad = !rec.lad ? "🆓 Sessão livre: entrou na média e no XP, a escada não mudou." : up ? `🪜 <b>Subiu de degrau!</b> Próximo bloco: <b>${L.min} min</b>.` : down ? `🪜 A escada desceu para <b>${L.min} min</b> para consolidar a base. Isso é ajuste, não fracasso.` : L.last && rec.cl ? "🎯 <b>Zona 25.</b> Agora é manter: 25 minutos limpos viram hábito." : `🪜 Degrau de ${L.min} min: ${L.ok}/2 sessões limpas seguidas para subir.`;
    const parts = [["⏱️ minutos no tema", xp.base], ["🏅 sessão limpa", xp.cl], ["🧘 ritual", xp.rit], ["🔁 retornos", xp.rt], ["📝 reflexão", xp.ref], ["🪜 degrau novo", xp.up]].filter(p => p[1]);
    return `<div class="panel foCard"><h3>${tit}</h3><p>${lad}</p>
     <div class="foXp">${parts.map(([l, v]) => `<span>${l} <b>+${v}</b></span>`).join("")}<span class="tot">Total <b>+${rec.xp} XP</b></span></div>
     ${top && this.DICA[top] ? `<p class="foTip">💡 ${this.DICA[top]}</p>` : rec.dv > 2 ? `<p class="foTip">💡 Vários desvios: na próxima, ative o modo foco do aparelho e deixe só este app aberto.</p>` : ""}
     <div class="row" style="margin-top:10px"><button class="btn gold" data-fo="brk">☕ Pausa ativa de ${longa ? 15 : 5} min</button><button class="btn" data-fo="novo">▶️ Próximo bloco</button><button class="btn sm" data-fosub="prog">📈 Ver progresso</button></div>
     ${longa ? `<p class="metaNow">🍅 Quatro blocos hoje: hora da pausa longa (15 min).</p>` : ""}</div>`;
  },
  vBrk() {
    const rem = this.brk.t0 + this.brk.dur * MIN - Date.now();
    return `<div class="panel foCard foBrk"><h3>☕ Pausa ativa · <b id="foBrkT">${this.mmss(rem)}</b></h3>
     <ul class="foList"><li>🚶 Levante e ande 1 minuto</li><li>💧 Beba água</li><li>👀 Olhe para longe por 20 segundos</li><li>🌬️ Faça 3 respirações lentas</li><li>📵 Evite redes sociais na pausa: elas puxam para longe e a volta fica mais difícil</li></ul>
     <div class="row"><button class="btn gold" data-fo="brkEnd">▶️ Encerrar pausa e montar o próximo bloco</button></div></div>`;
  },
  pk() { return Object.entries(this.R().p).filter(([, p]) => p && !p.del && p.x).map(([id, p]) => Object.assign({ id }, p)).sort((a, b) => b.t - a.t); },
  vNota() {
    const L = this.pk(), ab = L.filter(p => !p.d), ok = L.filter(p => p.d);
    const li = p => `<li class="${p.d ? "ok" : ""}"><span>${esc(p.x)}</span><small>${new Date(p.t).toLocaleString("pt-BR", { day: "2-digit", month: "2-digit", hour: "2-digit", minute: "2-digit" })}</small>${p.d ? "" : `<button class="btn sm" data-fopk="${p.id}" data-k="ok">✅ Resolvido</button>`}<button class="btn sm" data-fopk="${p.id}" data-k="x" aria-label="Apagar">🗑️</button></li>`;
    return `<div class="panel foCard"><h3>🗒️ Estacionamento de distrações</h3><p class="metaNow">O que surgiu durante os blocos fica aqui, para resolver na pausa ou no fim do dia. Anotar tira o peso de lembrar e libera a atenção.</p>
     <div class="row"><button class="btn sm gold" data-fo="nota">➕ Anotar</button>${ok.length ? `<button class="btn sm" data-fo="limpaPk">🧹 Arquivar resolvidos</button>` : ""}</div>
     ${ab.length ? `<h4>Pendentes (${ab.length})</h4><ul class="foPk">${ab.map(li).join("")}</ul>` : `<p>Nada pendente. 🌿</p>`}${ok.length ? `<h4>Resolvidos (${ok.length})</h4><ul class="foPk">${ok.slice(0, 30).map(li).join("")}</ul>` : ""}</div>`;
  },
  vProg(st, L) {
    const last = st.ss.slice(-14), mx = Math.max(25, ...last.map(x => x.dur));
    const bars = last.map(x => `<div class="foBarR" title="${new Date(x.t0).toLocaleString("pt-BR")} · ${this.fmt(x.min)}/${x.dur} min"><span>${new Date(x.t0).toLocaleDateString("pt-BR", { day: "2-digit", month: "2-digit" })}</span><i class="pl" style="width:${100 * x.dur / mx}%"><i class="no ${x.cl ? "cl" : x.tr ? "tr" : ""}" style="width:${Math.min(100, 100 * x.min / x.dur)}%"></i></i><b>${this.fmt(x.min)}${x.cl ? " ✅" : x.tr ? " 🌱" : ""}</b></div>`).join("");
    const cs = Object.entries(st.cs).sort((a, b) => b[1] - a[1]), cn = Object.fromEntries(this.CAUSAS);
    const fx = [[0, 5, "🦉 madrugada"], [6, 11, "🌅 manhã"], [12, 17, "☀️ tarde"], [18, 23, "🌙 noite"]], hb = fx.map(([a, b, n]) => { const l = st.ss.filter(x => { const h = new Date(x.t0).getHours(); return h >= a && h <= b; }); return [n, l.length, l.length ? l.reduce((s, x) => s + (x.dur ? x.min / x.dur : 0), 0) / l.length : 0]; }).filter(x => x[1] >= 2).sort((a, b) => b[2] - a[2]);
    return `<div class="panel foCard"><h3>📈 Progresso</h3><div class="foKpi">
      <div><b>${st.n}</b><span>blocos feitos</span></div><div><b>${st.cl}</b><span>🏅 sessões limpas</span></div><div><b>${st.z25}</b><span>🎯 limpas de 25+ min</span></div>
      <div><b>${st.maxRun}</b><span>🔥 maior sequência de dias</span></div><div><b>${st.rt}</b><span>🔁 retornos percebidos</span></div><div><b>${st.ck[1] ? Math.round(100 * st.ck[0] / st.ck[1]) + "%" : "—"}</b><span>🧭 checagens “no tema”</span></div></div>
      <h4>🪜 Escada</h4><div class="foLad">${this.DEG.map((m, i) => `<span class="foStep ${i < L.i ? "ok" : i === L.i ? "cur" : ""}">${m}</span>`).join("")}</div>
      <p class="metaNow">Degrau atual <b>${L.min} min</b> · maior degrau já alcançado <b>${L.top} min</b>. Regra: 2 sessões limpas seguidas sobem; 2 tropeços seguidos descem. <b>Limpa</b> = bloco completo, ≥ 90% do tempo no tema, até 2 desvios e qualidade ≥ 3. <b>Tropeço</b> = encerrado antes de 60% do tempo ou menos de 70% no tema.</p>
      <button class="btn sm" data-fo="recal">♻️ Recalibrar o ponto de partida</button>
      ${last.length ? `<h4>🗓️ Últimos ${last.length} blocos <small>(minutos no tema / duração)</small></h4><div class="foBars">${bars}</div>` : `<p>Nenhum bloco ainda. Comece pela aba ⏳ Sessão.</p>`}
      ${cs.length ? `<h4>🧲 O que mais puxa a sua atenção</h4><div class="foChips">${cs.map(([k, n]) => `<span class="pill">${cn[k] || k} · ${n}</span>`).join("")}</div>${this.DICA[cs[0][0]] ? `<p class="foTip">💡 ${this.DICA[cs[0][0]]}</p>` : ""}` : ""}
      ${hb.length ? `<h4>🕰️ Seu melhor horário</h4><p>${hb.map(([n, k, p], i) => `${i ? "" : "🥇 "}${n}: <b>${Math.round(100 * p)}%</b> do bloco no tema (${k} blocos)`).join(" · ")}</p>` : ""}</div>`;
  },
  vMet() {
    return `<div class="panel foCard foMet"><h3>📘 Como o treino funciona</h3>
     <ol class="foList">
      <li><b>🪜 Escada progressiva.</b> Você começa num tempo confortável e sobe em passos pequenos (5 → 8 → 10 → 12 → 15 → 18 → 20 → 22 → 25 min) quando o degrau fica fácil, como no treino físico. <small>Princípio de modelagem da análise do comportamento: aumentar a exigência aos poucos.</small></li>
      <li><b>⚓ Um único tema.</b> Cada bloco tem uma âncora: um baralho, as questões de um assunto ou um material fora do app. Trocar de aba ou de app conta como desvio, e o tempo fora não entra como foco.</li>
      <li><b>🔁 Perceber e voltar.</b> A mente divaga muito: num estudo com amostragem pelo celular, as pessoas pensavam em algo diferente do que faziam quase tão frequentemente quanto no que faziam. O treino é notar mais cedo e voltar. Por isso “😵 voltei” e as 🧭 checagens dão XP.</li>
      <li><b>🗒️ Estacionar distrações.</b> Anotar o pensamento intruso e adiar a ação é uma técnica dos programas de terapia cognitivo-comportamental para adultos com TDAH, cujo ensaio clínico mostrou melhora dos sintomas em quem já usava medicação.</li>
      <li><b>🧭 Se… então…</b> Decidir antes o que fazer quando a distração vier (“se eu me distrair, então anoto e volto”) é uma intenção de implementação, estratégia com efeito médio em metanálises de mudança de comportamento. <small>Citado de memória, a conferir.</small></li>
      <li><b>🍅 Blocos e pausas.</b> A técnica Pomodoro alterna 25 min de foco e 5 de pausa, com pausa longa a cada 4 blocos. Uma revisão de escopo de 2025 achou menos fadiga e menos distração com intervalos estruturados do que com pausas livres, mas com poucos ensaios e amostras pequenas.</li>
      <li><b>📵 Ambiente.</b> Celular longe e só o material do tema na mesa. Há estudos que sugerem que a simples presença do celular atrapalha, mas as replicações são inconsistentes: trate como medida de bom senso, não como prova.</li>
     </ol>
     <h4>🏁 Meta</h4><p>Chegar a <b>média de 25 minutos no tema</b> nas últimas 7 sessões. Esse é o título 🏹 Foco Pleno 25 na 🏆 Jornada.</p>
     <h4>📚 Referências (PubMed)</h4><ul class="foList refs">
      <li>Killingsworth MA, Gilbert DT. A wandering mind is an unhappy mind. <i>Science</i> 2010;330:932. <a href="https://doi.org/10.1126/science.1192439" target="_blank" rel="noopener">doi:10.1126/science.1192439</a></li>
      <li>Safren SA et al. Cognitive behavioral therapy vs relaxation with educational support for medication-treated adults with ADHD and persistent symptoms: RCT. <i>JAMA</i> 2010;304:875-80. <a href="https://doi.org/10.1001/jama.2010.1192" target="_blank" rel="noopener">doi:10.1001/jama.2010.1192</a></li>
      <li>Ogut E. Efficacy of the Pomodoro technique… a scoping review. <i>BMC Med Educ</i> 2025;25:1440. <a href="https://doi.org/10.1186/s12909-025-08001-0" target="_blank" rel="noopener">doi:10.1186/s12909-025-08001-0</a></li></ul>
     <p class="metaNow">⚠️ Treino de hábito de estudo, não tratamento. Não substitui avaliação nem acompanhamento profissional para dificuldades de atenção.</p></div>`;
  }
};
