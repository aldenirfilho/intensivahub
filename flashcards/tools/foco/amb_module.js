/* ---------------- 🎧 Som de estudo (4.23.0): ruídos e ambientes gerados no próprio aparelho (Web Audio, sem arquivos nem internet) ---------------- */
const AMB = {
  T: {
    rosa: ["🌸", "Ruído rosa", "Mais grave que o branco, lembra chuva fina constante. Bom ponto de partida."],
    chuva: ["🌧️", "Chuva", "Chuva no telhado com pingos soltos: ruído rosa filtrado + gotas."],
    marrom: ["🟤", "Ruído marrom", "Grave e abafado, como cachoeira ao longe. Mascara bem conversa e TV."],
    mar: ["🌊", "Ondas do mar", "Ondas lentas (6 a 10 s) que sobem e descem. Ritmo calmo para a respiração."],
    branco: ["⚪", "Ruído branco", "Chiado de TV fora do ar: todas as frequências por igual. É o mais estudado."]
  },
  SR: 32000, ac: null, mg: null, src: null, sg: null, cur: "", buf: {}, on: false, autoOn: false, _vt: 0,
  sel() { const v = lsGet("ambTipo"); return this.T[v] ? v : "rosa"; },
  vol() { const v = lsGet("ambVol"); return v === null || v === "" || isNaN(+v) ? 35 : Math.max(0, Math.min(100, +v)); },
  auto() { return lsGet("ambAuto") === "1"; },
  gain(v) { return 1.5 * Math.pow((v == null ? this.vol() : v) / 100, 2); },
  ctx() {
    const C = (typeof FO !== "undefined" && FO.ac) || this.ac || new (window.AudioContext || window.webkitAudioContext)();
    this.ac = C; if (typeof FO !== "undefined") FO.ac = C;
    if (C.state === "suspended") C.resume();
    if (!this.mg) { this.mg = C.createGain(); this.mg.gain.value = this.gain(); this.mg.connect(C.destination); }
    return C;
  },

  /* ---- síntese: cada som é um laço de 12–24 s com emenda cruzada (sem estalo na volta) ---- */
  make(tipo) {
    const sr = this.SR, R = Math.random, F = Math.round(0.6 * sr);
    let waves = null, len = Math.round((tipo === "chuva" ? 18 : 12) * sr);
    if (tipo === "mar") { waves = []; let tot = 0; while (tot < 22 * sr) { const d = Math.round((6.5 + 4 * R()) * sr); waves.push(d); tot += d; } len = tot; }
    const C = this.ctx(), out = C.createBuffer(2, len, sr);
    for (let ch = 0; ch < 2; ch++) {
      const n = len + F, g = new Float32Array(n);
      let b0 = 0, b1 = 0, b2 = 0, b3 = 0, b4 = 0, b5 = 0, b6 = 0, br = 0, hp = 0, hx = 0, lp = 0, lm = 0;
      const aHP = 1 / (1 + 2 * Math.PI * 400 / sr), aLP = 1 - Math.exp(-2 * Math.PI * 6000 / sr);
      for (let i = 0; i < n; i++) {
        const w = R() * 2 - 1;
        b0 = 0.99886 * b0 + w * 0.0555179; b1 = 0.99332 * b1 + w * 0.0750759; b2 = 0.969 * b2 + w * 0.153852;
        b3 = 0.8665 * b3 + w * 0.3104856; b4 = 0.55 * b4 + w * 0.5329522; b5 = -0.7616 * b5 - w * 0.016898;
        const pk = b0 + b1 + b2 + b3 + b4 + b5 + b6 + w * 0.5362; b6 = w * 0.115926;
        br = (br + 0.02 * w) / 1.02; const bw = br * 3.5;
        if (tipo === "branco") g[i] = w;
        else if (tipo === "rosa") g[i] = pk;
        else if (tipo === "marrom") g[i] = bw;
        else if (tipo === "chuva") { hp = aHP * (hp + pk - hx); hx = pk; lp += aLP * (hp - lp); g[i] = lp + 0.35 * bw; }
        else g[i] = 0.65 * bw + 0.35 * pk;
      }
      if (tipo === "chuva") {   // pingos: senoides curtas e amortecidas, com clique de ruído no começo
        const nd = Math.round(len / sr * 22);
        for (let k = 0; k < nd; k++) {
          const p = Math.floor(R() * n), f = 1800 + R() * 3600, tau = (0.0015 + R() * 0.006) * sr, a = 0.08 + Math.pow(R(), 3) * 0.9, L = Math.min(n - p, Math.round(6 * tau)), ph = R() * 6.28;
          for (let j = 0; j < L; j++) { const e = Math.exp(-j / tau); g[p + j] += a * e * (Math.sin(ph + 2 * Math.PI * f * j / sr) + (j < tau * 0.5 ? (R() * 2 - 1) * 0.6 : 0)); }
        }
      }
      if (tipo === "mar") {   // envelope das ondas (mesmo desenho nos 2 canais, levemente defasado) + brilho que acompanha a crista
        const off = ch ? Math.round(0.25 * sr) : 0, env = new Float32Array(n); let p = 0;
        for (const d of waves) { const up = Math.round(d * (0.35 + 0.1 * R())), pk2 = 0.75 + 0.25 * R();
          for (let j = 0; j < d; j++) { const x = j < up ? Math.pow(Math.sin(Math.PI / 2 * j / up), 2) : Math.exp(-3.2 * (j - up) / (d - up)) * (1 - (j - up) / (d - up) * 0.04); env[(p + j + off) % len] = 0.22 + 0.78 * pk2 * x; }
          p += d; }
        for (let i = len; i < n; i++) env[i] = env[i - len];
        for (let i = 0; i < n; i++) { const fc = 250 + 2600 * env[i] * env[i], a = 1 - Math.exp(-2 * Math.PI * fc / sr); lm += a * (g[i] - lm); g[i] = lm * env[i] * 2.2; }
      }
      // emenda: os primeiros F amostras recebem o "rabo" do ruído com cruzamento linear → laço contínuo
      const d = out.getChannelData(ch);
      for (let i = 0; i < len; i++) d[i] = i < F ? g[i] * (i / F) + g[len + i] * (1 - i / F) : g[i];
      let s = 0; for (let i = 0; i < len; i++) s += d[i] * d[i];
      const k = 0.12 / Math.sqrt(s / len || 1e-9); for (let i = 0; i < len; i++) d[i] = Math.max(-0.98, Math.min(0.98, d[i] * k));
    }
    return out;
  },

  /* ---- tocar / parar ---- */
  play(tipo, quiet) {
    tipo = this.T[tipo] ? tipo : this.sel();
    try {
      const C = this.ctx(), t = C.currentTime;
      if (this.src && this.cur === tipo) return this.paint();
      this.halt(0.8);
      const b = this.buf[tipo] || (this.buf = { [tipo]: this.make(tipo) })[tipo];
      const s = C.createBufferSource(), g = C.createGain(); s.buffer = b; s.loop = true;
      g.gain.setValueAtTime(0.0001, t); g.gain.linearRampToValueAtTime(1, t + 2.5);
      s.connect(g); g.connect(this.mg); s.start(t, Math.random() * b.duration * 0.9);
      this.src = s; this.sg = g; this.cur = tipo; this.on = true; lsSet("ambTipo", tipo);
      if (FO.run) { FO.run.amb = tipo; FO.save(); }
      if (!quiet) toast(`${this.T[tipo][0]} <b>${this.T[tipo][1]}</b> tocando · volume ${this.vol()}%`, 2200);
    } catch (e) { toast("🎧 Este navegador não liberou o áudio. Toque de novo no botão do som."); }
    this.paint();
  },
  halt(sec) {
    if (!this.src) return; const C = this.ac, s = this.src, g = this.sg, t = C.currentTime;
    try { g.gain.cancelScheduledValues(t); g.gain.setValueAtTime(g.gain.value, t); g.gain.linearRampToValueAtTime(0.0001, t + sec); s.stop(t + sec + 0.05); } catch (e) { }
    this.src = null; this.sg = null;
  },
  stop(sec) { this.halt(sec == null ? 1.5 : sec); this.on = false; this.cur = ""; this.autoOn = false; this.paint(); },
  toggle() { this.on ? this.stop() : this.play(this.sel()); },
  setVol(v) {
    v = Math.max(0, Math.min(100, Math.round(+v || 0))); lsSet("ambVol", String(v));
    if (this.mg && this.ac) { const t = this.ac.currentTime; this.mg.gain.cancelScheduledValues(t); this.mg.gain.setTargetAtTime(this.gain(v), t, 0.08); }
    $$(".ambVolN").forEach(e => e.textContent = v + "%"); $$(".ambVol").forEach(e => { if (+e.value !== v) e.value = v; });
  },

  /* ---- ligação com o ⏳ Foco ---- */
  blockStart() { if (this.auto() && !this.on) { this.play(this.sel(), true); this.autoOn = true; } if (FO.run) FO.run.amb = this.on ? this.cur : ""; },
  blockEnd() { if (this.autoOn) this.stop(3); },
  init() {
    document.addEventListener("click", e => { const b = e.target.closest("[data-amb]"); if (!b) return; e.preventDefault(); this.act(b.dataset.amb, b); });
    document.addEventListener("input", e => { if (e.target.classList && e.target.classList.contains("ambVol")) this.setVol(e.target.value); });
    if (FO.run && FO.run.amb && this.auto()) {   // app recarregado no meio de um bloco com som: retoma no primeiro toque (o navegador exige um gesto)
      const go = () => { document.removeEventListener("pointerdown", go, true); if (FO.run && !this.on) { this.play(FO.run.amb, true); this.autoOn = true; } };
      document.addEventListener("pointerdown", go, true);
    }
  },
  act(a, b) {
    if (a === "tog") return this.toggle();
    if (a === "stop") return this.stop();
    if (a === "auto") { const v = !this.auto(); lsSet("ambAuto", v ? "1" : "0"); b.classList.toggle("on", v); b.setAttribute("aria-pressed", String(v)); return toast(v ? "🔁 O som vai ligar junto com cada bloco de foco e desligar no fim." : "🔁 Som automático desligado."); }
    if (a.startsWith("t:")) { const k = a.slice(2); lsSet("ambTipo", k); return this.on ? this.play(k) : this.paint(); }
    if (a.startsWith("p:")) { const k = a.slice(2); return this.on && this.cur === k ? this.stop() : this.play(k); }
  },
  paint() {
    $$("[data-amb^='t:'],[data-amb^='p:']").forEach(e => { const k = e.dataset.amb.slice(2), live = this.on && this.cur === k; e.classList.toggle("gold", e.dataset.amb.startsWith("t:") ? k === (this.on ? this.cur : this.sel()) : live); e.classList.toggle("live", live); });
    $$("[data-amb='tog']").forEach(e => { e.textContent = this.on ? `⏹️ ${this.T[this.cur][0]} Parar` : `▶️ ${this.T[this.sel()][0]} Tocar`; e.classList.toggle("live", this.on); });
    $$(".ambBarB").forEach(e => { e.textContent = this.on ? "🎧" : "🔇"; e.title = this.on ? `${this.T[this.cur][1]} tocando — toque para parar` : "Ligar o som de fundo"; });
    $$(".ambNow").forEach(e => e.innerHTML = this.on ? `🔊 Tocando: <b>${this.T[this.cur][0]} ${this.T[this.cur][1]}</b>` : "🔇 Silêncio");
  },

  /* ---- interface ---- */
  vol_(cls) { const v = this.vol(); return `<label class="ambVolL ${cls || ""}">🔉 <input type="range" class="ambVol" min="0" max="100" step="1" value="${v}" aria-label="Volume do som de fundo"> <b class="ambVolN">${v}%</b></label>`; },
  mini() {
    return `<div class="ambMini"><span class="ambNow">${this.on ? `🔊 Tocando: <b>${this.T[this.cur][0]} ${this.T[this.cur][1]}</b>` : "🔇 Silêncio"}</span>
      <div class="foChips">${Object.entries(this.T).map(([k, [ic, nm]]) => `<button class="btn sm ${this.on && this.cur === k ? "gold live" : ""}" data-amb="p:${k}" title="${esc(nm)}">${ic}</button>`).join("")}<button class="btn sm" data-amb="stop">🔇</button></div>${this.vol_()}</div>`;
  },
  panel() {
    const sel = this.on ? this.cur : this.sel();
    return `<div class="panel foCard ambCard"><h3>🎧 Som de fundo <small>(opcional)</small></h3>
      <div class="foChips">${Object.entries(this.T).map(([k, [ic, nm]]) => `<button class="btn sm ${k === sel ? "gold" : ""} ${this.on && this.cur === k ? "live" : ""}" data-amb="t:${k}" title="${esc(this.T[k][2])}">${ic} ${nm}</button>`).join("")}</div>
      <div class="row" style="margin-top:8px;gap:10px;flex-wrap:wrap"><button class="btn sm ${this.on ? "live" : ""}" data-amb="tog">${this.on ? `⏹️ ${this.T[this.cur][0]} Parar` : `▶️ ${this.T[sel][0]} Tocar`}</button>${this.vol_()}
       <button class="btn sm foOpt ${this.auto() ? "on" : ""}" data-amb="auto" aria-pressed="${this.auto()}">🔁 Junto com o bloco</button></div>
      <p class="metaNow">💡 Comece pelo <b>🌸 rosa</b> ou pela <b>🌧️ chuva</b>, volume baixo (abaixo de uma conversa). Se atrapalhar, desligue: em quem não tem TDAH o ruído piorou o desempenho. Detalhes e a sua comparação pessoal em <a href="#foco" data-fosub="som" style="color:var(--cy)">🎧 Sons</a>.</p></div>`;
  },
  n1() {   // comparação N-de-1: blocos com som × sem som (só os registrados a partir da 4.23.0, que guardam o campo amb)
    const ss = FO.sessions().filter(x => "amb" in x && x.dur), g = { com: [], sem: [] };
    for (const x of ss) g[x.amb ? "com" : "sem"].push(x);
    const m = l => l.length ? { n: l.length, pc: l.reduce((a, x) => a + Math.min(1, (x.min || 0) / x.dur), 0) / l.length, min: l.reduce((a, x) => a + (x.min || 0), 0) / l.length, dv: l.reduce((a, x) => a + (x.dv || 0), 0) / l.length, cl: l.filter(x => x.cl).length / l.length } : null;
    const por = {}; for (const x of g.com) (por[x.amb] = por[x.amb] || []).push(x);
    return { com: m(g.com), sem: m(g.sem), por: Object.entries(por).map(([k, l]) => [k, m(l)]).sort((a, b) => b[1].pc - a[1].pc), ok: g.com.length >= 3 && g.sem.length >= 3 };
  },
  vSom() {
    const r = this.n1(), P = x => Math.round(100 * x) + "%", row = (lb, x) => x ? `<tr><td>${lb}</td><td>${x.n}</td><td><b>${P(x.pc)}</b></td><td>${FO.fmt(x.min)}</td><td>${FO.fmt(x.dv)}</td><td>${P(x.cl)}</td></tr>` : `<tr><td>${lb}</td><td colspan="5">ainda sem blocos</td></tr>`;
    let ver = "";
    if (r.ok) { const d = r.com.pc - r.sem.pc; ver = Math.abs(d) < 0.05 ? "⚖️ Por enquanto, sem diferença clara (menos de 5 pontos). Use o que for mais agradável." : d > 0 ? `🟢 Com som você ficou <b>${Math.round(100 * d)} pontos</b> a mais no tema. Vale manter.` : `🔴 Sem som você ficou <b>${Math.round(-100 * d)} pontos</b> a mais no tema. Para você, o silêncio parece melhor.`; }
    else ver = `🧪 Faltam blocos para comparar: ${r.com ? r.com.n : 0}/3 com som e ${r.sem ? r.sem.n : 0}/3 sem som.`;
    return `${this.panel()}
     <div class="panel foCard"><h3>🔬 Seu experimento N-de-1</h3>
      <p>O app guarda, em cada bloco de foco, se havia som e qual. Alterne por 2 semanas (ex.: <b>dias pares com som, ímpares sem</b>) e veja o resultado <b>em você</b>, que é o que importa.</p>
      <div class="tblWrap"><table class="t ambT"><tr><th></th><th>blocos</th><th>% no tema</th><th>min no tema</th><th>desvios</th><th>limpos</th></tr>${row("🎧 Com som", r.com)}${row("🔇 Sem som", r.sem)}${r.por.map(([k, x]) => row(`&nbsp;&nbsp;${this.T[k] ? this.T[k][0] + " " + this.T[k][1] : k}`, x)).join("")}</table></div>
      <p class="foTip">${ver}</p><small class="metaNow">Contam só os blocos registrados a partir da versão 4.23.0. É uma comparação simples, sem estatística: trate como pista, não como prova.</small></div>
     <div class="panel foCard foMet"><h3>📘 O que a ciência diz</h3><ol class="foList">
      <li><b>🧠 Ruído e TDAH.</b> Uma metanálise de 13 estudos (335 crianças e jovens universitários com TDAH ou muitos sintomas) achou <b>benefício pequeno</b> do ruído branco ou rosa em tarefas de atenção no laboratório (g ≈ 0,25). Nos participantes <b>sem</b> TDAH, o efeito foi <b>negativo</b> (g ≈ −0,21). Não houve estudos com ruído marrom.</li>
      <li><b>🎚️ Nem todo mundo responde igual.</b> Em 43 crianças com TDAH, quem tinha perfil mais <b>desatento</b> melhorou com ruído; quem tinha perfil mais <b>hiperativo/impulsivo</b> piorou. Daí o experimento N-de-1 acima.</li>
      <li><b>🌀 Por que funcionaria.</b> A hipótese é a da <b>ressonância estocástica</b> (modelo de excitação cerebral moderada): um pouco de ruído ajudaria um sistema com pouca excitação de base a detectar sinais. É hipótese, não mecanismo comprovado.</li>
      <li><b>👶 Limites.</b> Quase tudo foi feito em crianças e jovens, em tarefas de laboratório, por poucos minutos. Não há dados sólidos para adultos estudando 25 min, nem para chuva ou mar (são variações de ruído rosa/marrom com textura).</li>
      <li><b>👂 Proteja a audição.</b> Use o <b>menor volume que ainda “apaga” o ambiente</b>, abaixo do nível de uma conversa. Em fone, prefira volume do aparelho até ~60% e faça pausas: a OMS recomenda limitar a exposição a som alto <small>(citado de memória, a conferir)</small>.</li>
      <li><b>📱 Na prática.</b> O som é gerado no próprio aparelho (não gasta internet). No iPhone, o modo silencioso pode emudecer o som do navegador; com a tela bloqueada o som para. Ao recarregar o app no meio de um bloco, o som volta no primeiro toque na tela.</li></ol>
      <h4>📚 Referências (PubMed)</h4><ul class="foList refs">
       <li>Nigg JT, Bruton A, Kozlowski MB, Johnstone JM, Karalunas SL. Systematic review and meta-analysis: do white noise or pink noise help with task performance in youth with ADHD or with elevated attention problems? <i>J Am Acad Child Adolesc Psychiatry</i> 2024;63(8):778-88. <a href="https://doi.org/10.1016/j.jaac.2023.12.014" target="_blank" rel="noopener">doi:10.1016/j.jaac.2023.12.014</a></li>
       <li>Söderlund GBW, Hadjikhani N, Thorsson M et al. Sensory white noise in clinical ADHD: who benefits from noise, and who performs worse? <i>Scand J Child Adolesc Psychiatr Psychol</i> 2024;12(1):92-9. <a href="https://doi.org/10.2478/sjcapp-2024-0010" target="_blank" rel="noopener">doi:10.2478/sjcapp-2024-0010</a></li>
       <li>Jostrup E, Nyström M, Söderlund GBW et al. The influence of noise perception and parent-rated developmental characteristics on white noise benefits in children. <i>J Eye Mov Res</i> 2026;19(1):18. <a href="https://doi.org/10.3390/jemr19010018" target="_blank" rel="noopener">doi:10.3390/jemr19010018</a></li></ul>
      <p class="metaNow">⚠️ Ferramenta de ambiente de estudo, não tratamento. Não substitui avaliação nem acompanhamento profissional.</p></div>`;
  }
};
