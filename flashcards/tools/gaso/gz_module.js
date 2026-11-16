/* ---------------- 🧪 Gasometria 360X (4.13.0): casos guiados, analisador de beira-leito e fórmulas ---------------- */
const GZ = { NCARD: 450, NQ: 145, data: null, sub: lsGet("gzSub") || "casos", tema: "", cur: null, si: 0, picked: null, hits: 0, last: null,
  ROOT: "🧪 Gasometria 360X",
  async load() {   // cópia no aparelho para abrir sem internet
    if (this.data) return;
    try { const r = await fetch("data/gaso.json"); if (!r.ok) throw new Error(r.status); this.data = await r.json(); DB.setMeta("gz:data", this.data).catch(() => {}); }
    catch (e) { this.data = (await DB.meta("gz:data", null).catch(() => null)) || { casos: [] }; }
  },
  async open() { await this.load(); this.render(); },
  G() { return (S.logs._g = S.logs._g || {}); },
  temas() { return [...new Set(this.data.casos.map(c => c.deck))]; },
  list() { return this.data.casos.filter(c => !this.tema || c.deck === this.tema); },
  head() {
    const G = this.G(), all = this.data.casos, feitos = all.filter(c => G[c.n]).length, perf = all.filter(c => G[c.n] && G[c.n].p).length;
    const tabs = [["casos", "🎯 Casos guiados"], ["analisar", "🧮 Analisador"], ["formulas", "📐 Fórmulas"]];
    return `<div class="panel gzHero"><h2 style="margin:0 0 4px">🧪 Gasometria 360X</h2><p class="metaNow" style="margin:0">${this.NCARD} flashcards · ${this.NQ} questões · ${all.length} casos guiados · analisador com VM e venosa</p>
      <div class="metaRow" style="margin-top:10px"><button class="btn gold" id="gzStudy">🎴 Estudar os ${this.NCARD} flashcards</button><button class="btn" id="gzQz">❓ ${this.NQ} questões</button></div>
      <div class="stats" style="margin-top:10px"><div class="stat"><b class="n">${feitos}</b><span>casos resolvidos</span></div><div class="stat"><b style="color:var(--gold2)">${perf}</b><span>perfeitos ⭐</span></div><div class="stat"><b class="rv">${all.length - feitos}</b><span>inéditos</span></div></div></div>
      <div class="divTabs">${tabs.map(([k, v]) => `<button class="btn ${k === this.sub ? "gold" : ""}" data-gzsub="${k}">${v}</button>`).join("")}</div>`;
  },
  render() {
    const host = $("#gzHost"); if (!host) return;
    let body = "";
    if (this.sub === "casos") body = this.cur ? this.caseHTML() : this.casosHome();
    else if (this.sub === "analisar") body = this.formHTML();
    else body = this.formulasHTML();
    host.innerHTML = (this.cur && this.sub === "casos" ? "" : this.head()) + body;
    $$("#gzHost [data-gzsub]").forEach(b => b.onclick = () => { this.sub = b.dataset.gzsub; lsSet("gzSub", this.sub); this.cur = null; this.render(); });
    const st = $("#gzStudy"); if (st) st.onclick = () => startStudy(this.ROOT);
    const qz = $("#gzQz"); if (qz) qz.onclick = async () => { await QZ.load(); QZ.div = "gaso"; lsSet("qzDiv", "gaso"); QZ.tema = ""; QZ.block = null; location.hash = "questoes"; setTimeout(() => QZ.home(), 50); };
    this.bind(host);
  },
  casosHome() {
    const G = this.G(), l = this.list(), ined = l.filter(c => !G[c.n]).length, err = l.filter(c => G[c.n] && !G[c.n].p).length;
    return `<div class="panel"><div class="metaRow"><label>📚 Tema:</label><select id="gzTema"><option value="">Todos os temas (${this.data.casos.length})</option>${this.temas().map(t => `<option ${t === this.tema ? "selected" : ""} value="${esc(t)}">${esc(t)}</option>`).join("")}</select></div>
      <div class="metaRow"><button class="btn gold" data-gzgo="new">▶️ Caso inédito (${ined})</button><button class="btn" data-gzgo="any">🎲 Qualquer caso</button><button class="btn" data-gzgo="err" ${err ? "" : "disabled"}>🔁 Refazer imperfeitos (${err})</button></div>
      <p class="metaNow">🧭 Cada caso tem de 4 a 9 etapas: pH → distúrbio primário → compensação → ânion gap/Δ/Δ → oxigenação → diagnóstico; nos temas 11–13 entram também ventilador, POCUS, gap CO₂/ScvO₂ e a conduta. ✨ +3 XP por etapa certa, +10 se o caso sair perfeito. Atalhos: <span class="kbd">1</span>–<span class="kbd">6</span> responder · <span class="kbd">Enter</span> avançar.</p></div>`;
  },
  start(mode) {
    const G = this.G(), l = this.list(), sh = a => a[Math.floor(Math.random() * a.length)];
    const pool = mode === "new" ? l.filter(c => !G[c.n]) : mode === "err" ? l.filter(c => G[c.n] && !G[c.n].p) : l;
    if (!pool.length) return toast(mode === "new" ? "🏆 Você já resolveu todos os casos deste tema!" : "Nenhum caso nesse filtro.");
    this.cur = sh(pool.filter(c => c !== this.last).length ? pool.filter(c => c !== this.last) : pool); this.last = this.cur; this.si = 0; this.picked = null; this.hits = 0; this.render(); window.scrollTo({ top: 0 });
  },
  caseHTML() {
    const c = this.cur, s = c.steps[this.si], done = this.si >= c.steps.length;
    const trail = c.steps.slice(0, this.si).map((x, i) => `<div class="gzDone">${x.p} <b>${x.o[x.c]}</b></div>`).join("");
    let box;
    if (done) {
      const perf = this.hits === c.steps.length;
      box = `<div class="gzEnd ${perf ? "ok" : ""}"><div class="gzScore">${perf ? "⭐ Caso perfeito!" : `✅ ${this.hits}/${c.steps.length} etapas`}</div>
        <h3 style="margin:6px 0">✅ ${c.dx}</h3><div class="qzExp"><b>🩺 Por quê:</b> ${c.causa}<br><b>⚡ Conduta:</b> ${c.cond}<div class="qzPega">🎯 <b>Pegadinha:</b> ${c.peg}</div></div>
        <div class="metaRow" style="justify-content:space-between"><button class="btn" id="gzBack">◀ Lista de casos</button><button class="btn gold" id="gzNextCase">▶️ Próximo caso</button></div></div>`;
    } else {
      box = `<div class="gzStep"><div class="gzQ">${s.p}</div><div class="qzAlts">${s.o.map((o, i) => `<button class="qzAlt ${this.picked != null ? (i === s.c ? "ok" : i === this.picked ? "bad" : "") : ""}" data-gzo="${i}" ${this.picked != null ? "disabled" : ""}><b>${i + 1}</b><span>${o}</span></button>`).join("")}</div>
        ${this.picked != null ? `<div class="qzRes ${this.picked === s.c ? "ok" : "bad"}">${this.picked === s.c ? "✅ Isso!" : `❌ Resposta: <b>${s.o[s.c]}</b>`}</div><div class="qzExp gzExp">🔎 ${s.e}</div>
        <div class="metaRow" style="justify-content:flex-end"><button class="btn gold" id="gzNext">${this.si + 1 < c.steps.length ? "Próxima etapa ▶" : "🏁 Ver diagnóstico e conduta"}</button></div>` : ""}</div>`;
    }
    return `<div id="studyTop"><div class="grow">🧪 <b>Caso #${String(c.n).padStart(3, "0")}</b> · ${esc(c.deck.slice(3))}</div><div class="cnt">${Math.min(this.si + 1, c.steps.length)}/${c.steps.length} · ✅ ${this.hits}</div></div>
      <div class="progress"><i style="width:${100 * this.si / c.steps.length}%"></i></div>
      <div class="panel gzCase"><div class="gzCtx">${c.ctx}</div>${GASO_ENG.panel(c.lab)}${trail}${box}</div>
      ${done ? "" : `<div class="metaRow" style="justify-content:center"><button class="btn" id="gzQuit">⏹️ Sair do caso</button></div>`}`;
  },
  pick(i) {
    const c = this.cur; if (!c || this.picked != null || this.si >= c.steps.length) return; const s = c.steps[this.si]; if (i >= s.o.length) return;
    this.picked = i; const ok = i === s.c; if (ok) { this.hits++; addXP(3, "etapa", "g"); }
    const L = L0(); L.gS = (L.gS || 0) + 1; if (ok) L.gSok = (L.gSok || 0) + 1; this.hr(L); saveLog(); this.render();
  },
  next() {
    const c = this.cur; if (!c || this.picked == null) return; this.si++; this.picked = null;
    if (this.si >= c.steps.length) {
      const G = this.G(), e = G[c.n] || { n: 0, p: 0, b: 0 }, perf = this.hits === c.steps.length, L = L0();
      e.n = (e.n || 0) + 1; e.b = Math.max(e.b || 0, Math.round(100 * this.hits / c.steps.length)); if (perf) e.p = (e.p || 0) + 1; e.t = Date.now(); G[c.n] = e;
      L.gN = (L.gN || 0) + 1; if (perf) { L.gP = (L.gP || 0) + 1; addXP(10, "caso perfeito", "g"); }
      saveLog();
    }
    this.render(); window.scrollTo({ top: 0 });
  },
  hr(L) { const h = new Date().getHours(); L.hr = L.hr || {}; L.hr[h] = (L.hr[h] || 0) + 1; },
  F: [["ph", "pH (opcional)", "0.01"], ["pco2", "PaCO₂ mmHg *", "1"], ["hco3", "HCO₃⁻ mEq/L *", "0.1"], ["na", "Na⁺", "1"], ["cl", "Cl⁻", "1"], ["alb", "Albumina g/dL", "0.1"],
      ["pao2", "PaO₂ mmHg", "1"], ["fio2", "FiO₂ %", "1"], ["idade", "Idade", "1"], ["lac", "Lactato", "0.1"], ["glic", "Glicose mg/dL", "1"], ["ureia", "Ureia mg/dL", "1"], ["osm", "Osm medida", "1"],
      ["una", "Na urinário", "1"], ["uk", "K urinário", "1"], ["ucl", "Cl urinário", "1"]],
  F2: [["fr", "FR irpm", "1"], ["vc", "VC mL", "1"], ["peep", "PEEP", "1"], ["pplat", "Pplatô", "1"], ["etco2", "EtCO₂ mmHg", "1"], ["alt", "Altura cm", "1"], ["alvo", "PaCO₂ alvo", "1"],
      ["pvco2", "PvCO₂ central", "1"], ["scvo2", "ScvO₂ %", "1"], ["hb", "Hb g/dL", "0.1"], ["sat", "SaO₂ %", "1"]],
  formHTML() {
    const v = lsGet("gzForm") ? JSON.parse(lsGet("gzForm")) : {};
    return `<div class="panel"><h2 style="margin-top:0">🧮 Analisador passo a passo</h2>
      <p class="metaNow">Digite os valores do laudo. Só PaCO₂ e HCO₃⁻ são obrigatórios; Na⁺ + Cl⁻ liberam o ânion gap; PaO₂ (+ FiO₂ e idade) libera A-a e P/F; osmolalidade, glicose e ureia liberam o gap osmolar.</p>
      <div class="gzForm">${this.F.map(([k, l, s]) => `<label>${l}<input type="number" inputmode="decimal" step="${s}" id="gzf_${k}" value="${v[k] != null ? esc(String(v[k])) : ""}"></label>`).join("")}</div>
      <details class="gzMore" ${["fr", "vc", "pvco2", "scvo2"].some(k => v[k] != null) ? "open" : ""}><summary>🫁 Ventilador e 🩸 venosa central (opcional): FR para a PaCO₂ alvo, driving pressure, espaço morto, gap CO₂ e ScvO₂</summary>
       <div class="gzForm2">${this.F2.map(([k, l, s]) => `<label>${l}<input type="number" inputmode="decimal" step="${s}" id="gzf_${k}" value="${v[k] != null ? esc(String(v[k])) : ""}"></label>`).join("")}
        <label>Sexo (peso predito)<select id="gzf_sexo"><option value="M" ${v.sexo !== "F" ? "selected" : ""}>Masculino</option><option value="F" ${v.sexo === "F" ? "selected" : ""}>Feminino</option></select></label></div></details>
      <div class="metaRow"><button class="btn gold" id="gzRun">🔎 Interpretar</button><button class="btn" id="gzEx">🎲 Exemplo de caso</button><button class="btn" id="gzClr">🧽 Limpar</button></div>
      <div id="gzOut"></div>
      <p class="metaNow">⚠️ Ferramenta didática: aplica fórmulas consagradas (Winter, compensações, AG corrigido, Δ/Δ, A-a, P/F) e não substitui o julgamento clínico nem a gasometria repetida.</p></div>`;
  },
  run() {
    const lab = {}, xv = {}; for (const [k] of this.F) { const el = $("#gzf_" + k); if (el && el.value !== "") lab[k] = parseFloat(String(el.value).replace(",", ".")); }
    for (const [k] of this.F2) { const el = $("#gzf_" + k); if (el && el.value !== "") xv[k] = parseFloat(String(el.value).replace(",", ".")); }
    const sx = ($("#gzf_sexo") || {}).value || "M";
    lsSet("gzForm", JSON.stringify(Object.assign({}, lab, xv, { sexo: sx })));
    if (xv.fr != null || xv.vc != null) {
      const vm = { modo: "informado" }; for (const k of ["fr", "vc", "peep", "pplat", "etco2", "alvo"]) if (xv[k] != null) vm[k] = xv[k];
      if (xv.alt > 100) vm.pbw = Math.round((sx === "F" ? 45.5 : 50) + 0.91 * (xv.alt - 152.4));
      lab.vm = vm;
    }
    if (xv.hb != null) lab.hb = xv.hb;
    if (xv.sat != null) lab.sat = xv.sat;
    if (xv.pvco2 != null || xv.scvo2 != null) { lab.ven = { kind: "central" }; if (xv.pvco2 != null) lab.ven.pco2 = xv.pvco2; if (xv.scvo2 != null) lab.ven.sat = xv.scvo2; }
    if (!(lab.pco2 > 0) || !(lab.hco3 > 0)) { $("#gzOut").innerHTML = `<div class="qzRes bad">Informe pelo menos PaCO₂ e HCO₃⁻.</div>`; return; }
    if (lab.fio2 != null) lab.fio2 = lab.fio2 > 1 ? lab.fio2 / 100 : lab.fio2;
    const R = GASO_ENG.analyze(lab), hh = 6.1 + Math.log10(lab.hco3 / (0.03 * lab.pco2)), warn = lab.ph != null && Math.abs(lab.ph - hh) > 0.05;
    const L = L0(); L.gA = (L.gA || 0) + 1; saveLog(); addXP(1, "análise", "g");
    $("#gzOut").innerHTML = `${warn ? `<div class="qzRes bad">⚠️ Laudo possivelmente incoerente: pH medido ${GASO_ENG.f(lab.ph, 2)} × calculado por Henderson-Hasselbalch ${GASO_ENG.f(hh, 2)}. Confira coleta/digitação antes de interpretar.</div>` : ""}
      ${GASO_ENG.panel(lab, "🩸 Laudo informado")}<div class="gzDx">✅ <b>${R.dx}</b></div><ol class="gzSteps">${R.steps.concat(R.xsteps || []).map(s => `<li>${s}</li>`).join("")}</ol>`;
  },
  formulasHTML() {
    const F = [["🧭 Henderson-Hasselbalch", "pH = 6,1 + log [HCO₃⁻ / (0,03 × PaCO₂)] · atalho [H⁺] = 24 × PaCO₂ / HCO₃⁻"], ["🔴 Winter (acidose metabólica)", "PaCO₂ esperada = 1,5 × HCO₃⁻ + 8 ± 2"],
      ["🔵 Alcalose metabólica", "PaCO₂ esperada = 0,7 × HCO₃⁻ + 21 ± 2 (raramente &gt; 55)"], ["🫁 Acidose respiratória", "HCO₃⁻ +1 (aguda) ou +3,5 (crônica) por 10 de PaCO₂"],
      ["🌬️ Alcalose respiratória", "HCO₃⁻ −2 (aguda) ou −4 (crônica) por 10 de PaCO₂"], ["🧪 Ânion gap", "AG = Na⁺ − (Cl⁻ + HCO₃⁻) · normal 8–12 · corrigido = AG + 2,5 × (4 − albumina)"],
      ["⚖️ Δ/Δ", "(AG − 12) / (24 − HCO₃⁻): &lt; 0,8 + hiperclorêmica · 0,8–2 pura · &gt; 2 + alcalose metabólica"], ["🍷 Gap osmolar", "Osm medida − (2 Na⁺ + glicose/18 + ureia/6) · &gt; 10 = álcool tóxico?"],
      ["🚽 AG urinário", "Na⁺u + K⁺u − Cl⁻u · negativo = perda GI · positivo = ATR distal"], ["🧂 Cloro urinário", "&lt; 20 responsiva a cloreto · &gt; 40 resistente"],
      ["💨 Gradiente A-a", "PAO₂ = FiO₂ × (Patm − 47) − PaCO₂/0,8 · A-a esperado ≈ idade/4 + 4"], ["🫁 P/F (Berlim, PEEP ≥ 5)", "leve 201–300 · moderada 101–200 · grave ≤ 100"],
      ["🩸 CaO₂ e DO₂", "CaO₂ = 1,34 × Hb × SatO₂ + 0,003 × PaO₂ · DO₂ = DC × CaO₂ × 10"], ["🧊 Déficit de HCO₃⁻", "0,5 × peso × (alvo − atual) — repor metade e reavaliar"],
      ["🍬 Na⁺ na hiperglicemia", "Na⁺ corrigido = Na⁺ + 1,6–2,4 × (glicose − 100)/100 (no AG use o medido)"], ["⚙️ Ajuste da VM", "FR nova ≈ FR atual × PaCO₂ atual / PaCO₂ desejada"],
      ["🧍 Peso predito", "homem 50 + 0,91 × (altura − 152,4) · mulher 45,5 + 0,91 × (altura − 152,4) · VC 6 mL/kg"], ["🫁 Driving pressure", "Pplatô − PEEP ≤ 15 cmH₂O · Pplatô ≤ 30"],
      ["💨 Gap PaCO₂ − EtCO₂", "normal 2–5 mmHg · maior = espaço morto (TEP, baixo débito, hiperdistensão)"], ["📊 Razão ventilatória", "(VE × PaCO₂) / (peso predito × 100 × 37,5) · ≈ 1 normal"],
      ["🩸 Gap CO₂ venoarterial", "PcvCO₂ − PaCO₂ &gt; 6 mmHg = fluxo (débito) insuficiente"], ["🧮 Gap CO₂ / Ca−vO₂", "&gt; ~1,4 sugere metabolismo anaeróbio (cortes variam)"],
      ["🩸 ScvO₂", "&lt; 70% extração alta · 70–80% alvo · &gt; 80% extração baixa/falha de extração"], ["❤️ Fick", "DC = VO₂ / (CaO₂ − CvO₂) × 10"]];
    return `<div class="panel"><h2 style="margin-top:0">📐 Fórmulas de bolso</h2><div class="gzForms">${F.map(([t, d]) => `<div class="gzF"><b>${t}</b><span>${d}</span></div>`).join("")}</div>
      <p class="metaNow">💡 Ordem de leitura: pH → primário → compensação → AG corrigido → Δ/Δ → oxigenação. Pratique nos 🎯 casos guiados.</p></div>`;
  },
  bind(host) {
    $$("#gzHost .gzForm2 input").forEach(i => i.onkeydown = e => { if (e.key === "Enter") { e.preventDefault(); this.run(); } });
    const tm = $("#gzTema", host); if (tm) tm.onchange = e => { this.tema = e.target.value; this.render(); };
    $$("#gzHost [data-gzgo]").forEach(b => b.onclick = () => this.start(b.dataset.gzgo));
    $$("#gzHost [data-gzo]").forEach(b => b.onclick = () => this.pick(+b.dataset.gzo));
    const nx = $("#gzNext", host); if (nx) nx.onclick = () => this.next();
    const q = $("#gzQuit", host); if (q) q.onclick = () => { this.cur = null; this.render(); };
    const bk = $("#gzBack", host); if (bk) bk.onclick = () => { this.cur = null; this.render(); };
    const nc = $("#gzNextCase", host); if (nc) nc.onclick = () => this.start("new");
    const rn = $("#gzRun", host); if (rn) rn.onclick = () => this.run();
    const cl = $("#gzClr", host); if (cl) cl.onclick = () => { lsSet("gzForm", "{}"); this.render(); };
    const ex = $("#gzEx", host); if (ex) ex.onclick = () => { const c = this.data.casos[Math.floor(Math.random() * this.data.casos.length)]; const v = Object.assign({}, c.lab); delete v.ph; if (v.fio2) v.fio2 = Math.round(v.fio2 * 100);
      if (v.vm) { for (const k of ["fr", "vc", "peep", "pplat", "etco2", "alvo"]) if (v.vm[k] != null) v[k] = v.vm[k]; if (v.vm.pbw) { v.alt = Math.round((v.vm.pbw - 50) / 0.91 + 152.4); v.sexo = "M"; } }
      if (v.ven && v.ven.kind !== "periferica") { if (v.ven.pco2 != null) v.pvco2 = v.ven.pco2; if (v.ven.sat != null) v.scvo2 = v.ven.sat; }
      delete v.vm; delete v.ven; delete v.us; lsSet("gzForm", JSON.stringify(v)); this.render(); this.run(); toast(`🎲 ${c.ctx.slice(0, 90)}…`, 4500); };
    $$("#gzHost .gzForm input").forEach(i => i.onkeydown = e => { if (e.key === "Enter") { e.preventDefault(); this.run(); } });
  },
  key(e) {
    if (location.hash !== "#gaso" || this.sub !== "casos" || !this.cur) return;
    if (/^(INPUT|SELECT|TEXTAREA)$/.test((e.target || {}).tagName || "")) return;
    const c = this.cur; if (this.si >= c.steps.length) return;
    if (this.picked == null) { const n = "123456".indexOf(e.key); if (n >= 0) { e.preventDefault(); this.pick(n); } }
    else if (e.key === "Enter") { e.preventDefault(); this.next(); }
  } };
document.addEventListener("keydown", e => GZ.key(e));
