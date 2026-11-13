/* ---------------- 🔊 Áudio: leitura em voz alta (voz do próprio aparelho, sem internet) ----------------
   Botão 🔊 em cada card, questão, micropartícula, mnemônico, card/bússola/painel da Honra, no card de estudo
   e no cabeçalho (lê a tela atual ou o trecho selecionado). Mãos livres: lê sozinho a frente e o verso.
   Ajustes no aparelho: vozName, vozRate, vozAuto, vozSrc (localStorage). Fonte: tools/voz/voz.js */
const VOZ = {
  rates: [0.8, 1, 1.15, 1.3, 1.5, 1.7], chunks: [], k: 0, tok: 0, btn: null, label: "", paused: false, lastAuto: "",
  get ok() { return typeof window !== "undefined" && "speechSynthesis" in window && typeof SpeechSynthesisUtterance !== "undefined"; },
  get rate() { const r = parseFloat(lsGet("vozRate")); return r >= 0.5 && r <= 2 ? r : 1; },
  get auto() { return lsGet("vozAuto") === "1"; },
  get src() { return lsGet("vozSrc") === "1"; },
  voices() { try { return speechSynthesis.getVoices() || []; } catch (e) { return []; } },
  ptVoices() { return this.voices().filter(v => /^pt/i.test(v.lang)).sort((a, b) => this.score(b) - this.score(a)); },
  score(v) {
    let s = 0; if (/pt[-_]BR/i.test(v.lang)) s += 10;
    if (/luciana|francisca|thalita|google portugu|felipe|daniel|antonio|maria/i.test(v.name)) s += 3;
    if (/enhanced|premium|neural|natural|online/i.test(v.name)) s += 2; if (v.localService) s += 1; return s;
  },
  voice() { const n = lsGet("vozName"), all = this.voices(); return (n && all.find(v => v.name === n)) || this.ptVoices()[0] || null; },

  /* ---- texto → fala em português ---- */
  UN: [[/mmHg/g, " milímetros de mercúrio"], [/cmH2O|cmH₂O/g, " centímetros de água"], [/mEq\/L/g, " miliequivalentes por litro"], [/mmol\/L/g, " milimols por litro"],
    [/mg\/kg\/h/g, " miligramas por quilo por hora"], [/mcg\/kg\/min|µg\/kg\/min|μg\/kg\/min/g, " microgramas por quilo por minuto"], [/mL\/kg\/h/gi, " mililitros por quilo por hora"],
    [/mL\/kg/gi, " mililitros por quilo"], [/mg\/kg/g, " miligramas por quilo"], [/U\/kg\/h/g, " unidades por quilo por hora"], [/U\/kg/g, " unidades por quilo"], [/g\/kg/g, " gramas por quilo"],
    [/kcal\/kg/g, " quilocalorias por quilo"], [/mg\/dL/g, " miligramas por decilitro"], [/g\/dL/g, " gramas por decilitro"], [/mL\/min/gi, " mililitros por minuto"], [/L\/min/g, " litros por minuto"],
    [/mL\/h/gi, " mililitros por hora"], [/(\d)\s?mcg\b|(\d)\s?µg\b|(\d)\s?μg\b/g, (m, a, b, c) => (a || b || c) + " microgramas"], [/(\d)\s?mg\b/g, "$1 miligramas"], [/(\d)\s?mL\b/gi, "$1 mililitros"],
    [/(\d)\s?kg\b/g, "$1 quilos"], [/(\d)\s?g\b/g, "$1 gramas"], [/(\d)\s?h\b/g, "$1 horas"], [/(\d)\s?min\b/g, "$1 minutos"], [/(\d)\s?bpm\b/g, "$1 batimentos por minuto"], [/(\d)\s?irpm\b/g, "$1 incursões por minuto"],
    [/(\d)\s?°C/g, "$1 graus"], [/(\d)\s?mOsm\/kg/g, "$1 miliosmóis por quilo"], [/(\d)\s?UI\b/g, "$1 unidades internacionais"], [/(\d)\s?x\/dia/g, "$1 vezes ao dia"], [/(\d)\s?x\s?(\d)/g, "$1 vezes $2"]],
  SY: [[/≥/g, " maior ou igual a "], [/≤/g, " menor ou igual a "], [/≠/g, " diferente de "], [/≈/g, " aproximadamente "], [/±/g, " mais ou menos "], [/×/g, " vezes "],
    [/\s>\s?(?=\d)/g, " maior que "], [/\s<\s?(?=\d)/g, " menor que "], [/[→⇒➜➔⟶]/g, ", então, "], [/↑/g, " aumento de "], [/↓/g, " queda de "], [/~\s?(?=\d)/g, "cerca de "],
    [/(\d)\s?[–—-]\s?(\d)/g, "$1 a $2"], [/\be\/ou\b/g, "e ou"], [/(\d)\/(\d)/g, "$1 por $2"], [/(\p{L}\d?)\/(?=\p{L})/gu, "$1 sobre "], [/\[\s?(\.\.\.|…)\s?\]/g, " lacuna "], [/::/g, ", "], [/\bvs\.?\s/gi, " versus "], [/\bp\.\s?ex\.?/gi, "por exemplo"], [/\bex\.:/gi, "exemplo:"],
    [/\bc\/\s?(?=\p{L})/gu, "com "], [/\bs\/\s?(?=\p{L})/gu, "sem "], [/\bDx\b/g, "diagnóstico"], [/\bTx\b/g, "tratamento"], [/\bpct\b/gi, "paciente"], [/\bpcts\b/gi, "pacientes"],
    [/₂/g, "2"], [/₃/g, "3"], [/²/g, " ao quadrado"], [/³/g, " ao cubo"], [/(\d)\s?%/g, "$1 por cento"], [/\s&\s/g, " e "], [/[•·▪︎■□◆◇►▶◀◂▸]/g, ", "], [/[*_#`|]/g, " "], [/[✓✔☑]/g, " "], [/[✗✘☒]/g, " "]],
  clean(t) {
    t = String(t || "").replace(/[\p{Extended_Pictographic}\u{1F1E6}-\u{1F1FF}️‍⃣]/gu, " ");
    for (const [a, b] of this.UN) t = t.replace(a, b);
    for (const [a, b] of this.SY) t = t.replace(a, b);
    return t.replace(/[ \t]+/g, " ").replace(/\s*\n[\s\n]*/g, "\n").split("\n").map(s => s.trim()).filter(s => /[\p{L}\p{N}]/u.test(s))
      .map(s => /[.!?:;…]$/.test(s) ? s : s + ".").join(" ").replace(/\s+([,.;:!?])/g, "$1").replace(/([,.;:])\1+/g, "$1").trim();
  },
  split(t) {   // pedaços curtos: o Chrome corta falas longas e o iPhone respeita melhor as pausas
    const out = [], max = 210;
    for (const s of t.split(/(?<=[.!?;:])\s+/)) {
      if (s.length <= max) { out.push(s); continue; }
      let cur = ""; for (const w of s.split(/(?<=,)\s+|\s+/)) { if ((cur + " " + w).length > max && cur) { out.push(cur); cur = w; } else cur = cur ? cur + " " + w : w; }
      if (cur) out.push(cur);
    }
    const m = []; for (const s of out) { if (m.length && (m[m.length - 1] + " " + s).length <= max) m[m.length - 1] += " " + s; else m.push(s); }
    return m.filter(Boolean);
  },
  /* texto visível de um elemento (ignora botões, campos, atalhos e, por padrão, as fontes) */
  textOf(el, o = {}) {
    if (!el) return "";
    const out = [], BL = /^(DIV|P|LI|TR|TD|TH|H[1-6]|HR|BR|SECTION|ARTICLE|UL|OL|TABLE|BLOCKQUOTE|DT|DD|FIGCAPTION|SUMMARY|DETAILS|HEADER|FOOTER)$/;
    let on = !o.after, stop = false;
    const skip = ".vozBtn,.vozSkip,.kbd,[aria-hidden='true'],.mnTools,.mcN,.chk" + (this.src ? "" : ",.src,.qzRef") + (o.skip ? "," + o.skip : "");
    const walk = n => {
      if (stop) return;
      if (n.nodeType === 3) { if (on) out.push(n.nodeValue); return; }
      if (n.nodeType !== 1 && n.nodeType !== 11) return;
      if (n.nodeType === 1) {
        if (o.after && n === o.after) { on = true; return; }
        if (o.before && n === o.before) { stop = true; return; }
        if (/^(SCRIPT|STYLE|BUTTON|INPUT|SELECT|TEXTAREA|SVG|NOSCRIPT|TEMPLATE|IMG|CANVAS|VIDEO|AUDIO|OPTION)$/i.test(n.tagName)) return;
        if (n.matches && n.matches(skip)) return;
        let cs = null; try { cs = getComputedStyle(n); } catch (e) { }
        if (cs && (cs.display === "none" || cs.visibility === "hidden")) return;
        const bl = BL.test(n.tagName) || (cs && /block|flex|grid|list-item|table/.test(cs.display));
        if (bl && on) out.push("\n");
        for (const c of n.childNodes) walk(c);
        if (bl && on) out.push("\n");
      } else for (const c of n.childNodes) walk(c);
    };
    walk(el); return out.join("");
  },

  /* ---- fala ---- */
  say(text, o = {}) {
    if (!this.ok) { toast("🔇 Este navegador não tem leitura em voz. No iPhone, use o Safari ou o app pela tela inicial."); return false; }
    const t = this.clean(text), was = this.busy || !!(speechSynthesis.speaking || speechSynthesis.pending); this.stop(true);
    if (!t) { toast("🔇 Nada para ler aqui."); return false; }
    this.unlock();
    this.chunks = this.split(t); this.k = 0; this.paused = false; this.label = o.label || "Lendo"; this.srcEl = o.el || null; this.btn = o.btn || null;
    const tok = ++this.tok; if (this.btn) { this.btn.classList.add("on"); this.btn.dataset.ic = this.btn.textContent; this.btn.textContent = "⏹️"; }
    this.player(); if (was) setTimeout(() => { if (tok === this.tok) this.next(tok); }, 60); else this.next(tok); return true;
  },
  /* iPhone/iPad: a 1ª fala precisa nascer de um toque; uma fala muda "destrava" o restante (mãos livres) */
  unlock() { if (this._unl || !this.ok) return; this._unl = true; try { const u = new SpeechSynthesisUtterance(" "); u.volume = 0; u.lang = "pt-BR"; speechSynthesis.speak(u); } catch (e) { } },
  next(tok) {
    if (tok !== this.tok || this.paused) return;
    if (this.k >= this.chunks.length) return this.done();
    const u = new SpeechSynthesisUtterance(this.chunks[this.k]), v = this.voice();
    u.lang = v ? v.lang : "pt-BR"; if (v) u.voice = v; u.rate = this.rate; u.pitch = 1;
    u.onend = () => { if (tok !== this.tok || this.paused) return; this.k++; this.prog(); this.next(tok); };
    u.onerror = e => { if (tok !== this.tok) return; const er = e && e.error; if (er === "interrupted" || er === "canceled") return;
      if (er === "not-allowed") { this._unl = false; toast("🔇 O navegador bloqueou o áudio: toque em 🔊 de novo."); return this.done(); }
      if (this.k === 0) { toast("🔇 A voz deste aparelho não respondeu. Veja ⚙️ Ajustes › 🔊 Áudio."); return this.done(); }
      this.k++; this.next(tok); };
    this.u = u; try { speechSynthesis.speak(u); } catch (e) { this.done(); }
    this.prog();
  },
  pause() {
    if (!this.chunks.length) return;
    if (this.paused) { this.paused = false; const tok = ++this.tok; this.player(); setTimeout(() => this.next(tok), 40); }
    else { this.paused = true; this.tok++; try { speechSynthesis.cancel(); } catch (e) { } this.player(); }
  },
  stop(silent) {
    this.tok++; this.paused = false; this.chunks = []; this.k = 0;
    try { if (this.ok) speechSynthesis.cancel(); } catch (e) { }
    if (this.btn) { this.btn.classList.remove("on"); if (this.btn.dataset.ic) this.btn.textContent = this.btn.dataset.ic; }
    this.btn = null; this.srcEl = null; if (!silent) this.player();
  },
  done() { const b = this.btn; this.chunks = []; this.k = 0; if (b) { b.classList.remove("on"); if (b.dataset.ic) b.textContent = b.dataset.ic; } this.btn = null; this.srcEl = null; this.player(); },
  get busy() { return this.chunks.length > 0; },
  setRate(r) { lsSet("vozRate", String(r)); if (this.busy && !this.paused) { const tok = ++this.tok; try { speechSynthesis.cancel(); } catch (e) { } setTimeout(() => this.next(tok), 60); } this.player(); },
  /* mini-player fixo enquanto lê */
  player() {
    let p = $("#vozPlayer");
    if (!this.busy) { if (p) p.classList.remove("on"); $$(".vozHdr").forEach(b => b.textContent = "🔊"); return; }
    if (!p) { p = document.createElement("div"); p.id = "vozPlayer"; p.setAttribute("role", "region"); p.setAttribute("aria-label", "Leitura em voz alta"); document.body.appendChild(p); }
    p.innerHTML = `<span class="vpL">🔊 <b>${esc(this.label)}</b> <small id="vpN">${Math.min(this.k + 1, this.chunks.length)}/${this.chunks.length}</small></span>
      <button class="btn sm" id="vpP" aria-label="${this.paused ? "Continuar" : "Pausar"}">${this.paused ? "▶️" : "⏸️"}</button><button class="btn sm" id="vpR" aria-label="Velocidade">${this.rate.toString().replace(".", ",")}×</button><button class="btn sm" id="vpS" aria-label="Parar">⏹️</button>`;
    $("#vpP").onclick = () => this.pause(); $("#vpS").onclick = () => this.stop();
    $("#vpR").onclick = () => { const i = this.rates.indexOf(this.rate); this.setRate(this.rates[(i + 1) % this.rates.length]); };
    const bar = $(".bar.on"); p.style.bottom = (bar ? bar.offsetHeight + 10 : 14) + "px";
    p.classList.add("on"); $$(".vozHdr").forEach(b => b.textContent = "⏹️");
  },
  prog() { const n = $("#vpN"); if (n) n.textContent = Math.min(this.k + 1, this.chunks.length) + "/" + this.chunks.length; },

  /* ---- card de estudo (shadow DOM): frente antes de revelar, verso depois ---- */
  studyText(part) {
    const host = $("#cardHost"), root = host && host.shadowRoot, card = root && root.querySelector(".card"); if (!card) return "";
    const ans = root.querySelector("#answer");
    if (part === "a" && ans) return "Resposta. " + this.textOf(card, { after: ans });
    return this.textOf(card, ans ? { before: ans } : {});
  },
  study(btn) {
    if (this.busy && this.btn === btn) return this.stop();
    const hist = Study.view != null, part = hist || Study.shown ? "a" : "q";
    this.say(this.studyText(part), { label: part === "a" ? "Resposta do card" : "Pergunta do card", btn });
  },
  autoStudy(part) { if (this.auto && location.hash === "#estudar") this.say(this.studyText(part), { label: part === "a" ? "Resposta do card" : "Pergunta do card", btn: $("#bVoz") }); },

  /* ---- pontos com 🔊 em cada tela ---- */
  SPOTS: [
    { sel: "#qzHost .panel.qz", label: "Questão", auto: true, txt: el => { const e = el.querySelector(".qzEnun"), A = [...el.querySelectorAll(".qzAlt")];
      return "Questão. " + VOZ.textOf(e) + "\n" + A.map((b, i) => "Alternativa " + "ABCDE"[i] + ": " + VOZ.textOf(b.querySelector("span") || b)).join("\n"); } },
    { sel: "#qzCom", label: "Comentário", auto: true, need: ".qzRes" },
    { sel: "#mcHost .mcCard", label: "Micropartícula", slot: ".mcTop", auto: true },
    { sel: ".mnCard", label: "Mnemônico", slot: ".mnTools,.mcTop", auto: el => el.classList.contains("mnTrain") },
    { sel: "#hoHost .hoComp", label: "Bússola", slot: ".hoCompT" },
    { sel: "#hoHost .hoPanel", label: "Honra", not: ".mnCard,.hoComp,.hoForm,input,textarea,select,.hoBreath,.hoTimer", min: 40 },
    { sel: "#jrHost .panel", label: "Jornada", not: "input,select,textarea", min: 60 },
  ],
  decorate() {
    if (!this.ok) return;
    if (this.busy && this.srcEl && !this.srcEl.isConnected) this.stop();
    const v = $(".view.on"); if (!v) return;
    let autoEl = null, autoSp = null;
    for (const sp of this.SPOTS) for (const el of v.querySelectorAll(sp.sel)) {
      if (el.dataset.voz) continue;
      if (sp.need && !el.querySelector(sp.need)) continue;
      if (sp.not && el.querySelector(sp.not)) continue;
      if (sp.min && (el.textContent || "").trim().length < sp.min) continue;
      el.dataset.voz = "1";
      const b = document.createElement("button"); b.className = "vozBtn"; b.type = "button"; b.textContent = "🔊"; b.title = "Ouvir " + sp.label.toLowerCase() + " (L)"; b.setAttribute("aria-label", b.title);
      b.onclick = ev => { ev.stopPropagation(); if (this.busy && this.btn === b) return this.stop(); this.say(this.spotText(sp, el), { label: sp.label, btn: b, el }); };
      const slot = sp.slot && sp.slot.split(",").map(s => el.querySelector(s)).find(Boolean);
      if (slot) { b.classList.add("inl"); slot.appendChild(b); } else el.insertBefore(b, el.firstChild);
      const au = typeof sp.auto === "function" ? sp.auto(el) : sp.auto;
      if (au && !autoEl) { autoEl = el; autoSp = sp; autoEl._vb = b; }
    }
    if (autoEl && this.auto) { const t = this.spotText(autoSp, autoEl), sig = autoSp.label + "|" + t.slice(0, 300); if (sig !== this.lastAuto) { this.lastAuto = sig; this.say(t, { label: autoSp.label, btn: autoEl._vb, el: autoEl }); } }
  },
  spotText(sp, el) { return sp.txt ? sp.txt(el) : this.textOf(el, { skip: sp.sel === "#qzCom" ? "" : "#qzCom" }); },
  /* 🔊 do cabeçalho: trecho selecionado → card de estudo → tela inteira */
  screen(btn) {
    if (this.busy) return this.stop();
    const sel = String(window.getSelection ? window.getSelection() : "").trim();
    if (sel.length > 2) return this.say(sel, { label: "Trecho selecionado" });
    if (location.hash === "#estudar" && $("#cardHost").style.display !== "none") return this.study($("#bVoz"));
    const v = $(".view.on"); this.say(this.textOf(v, { skip: ".foot,#hlBar,.divTabs,.mnBar" }), { label: "Tela: " + (($("#nav a.on") || {}).textContent || "").replace(/[\p{Extended_Pictographic}️]/gu, "").trim() });
  },
  key(e) {
    if (/input|textarea|select/i.test(e.target.tagName) || e.metaKey || e.ctrlKey || e.altKey) return false;
    if (e.key !== "l" && e.key !== "L") return false;
    e.preventDefault();
    if (this.busy) { this.stop(); return true; }
    if (location.hash === "#estudar") { this.study($("#bVoz")); return true; }
    const b = $(".view.on .vozBtn"); if (b) b.click(); else this.screen();
    return true;
  },
  /* ⚙️ Ajustes › Áudio */
  settings() {
    const h = $("#vozSet"); if (!h) return;
    if (!this.ok) { h.innerHTML = `<h3>🔊 Áudio</h3><p class="metaNow">🔇 Este navegador não oferece leitura em voz. No iPhone/iPad funciona no Safari e no app instalado pela tela inicial.</p>`; return; }
    const pv = this.ptVoices(), cur = this.voice(), all = this.voices();
    const opts = (pv.length ? pv : all).map(v => `<option value="${esc(v.name)}" ${cur && v.name === cur.name ? "selected" : ""}>${esc(v.name)} · ${esc(v.lang)}</option>`).join("");
    h.innerHTML = `<h3>🔊 Áudio · leitura em voz alta</h3>
      <p class="metaNow">Toque em 🔊 em qualquer card, questão, micropartícula, mnemônico ou painel. O 🔊 do topo lê a tela inteira (ou o trecho que você selecionar). Atalho: <span class="kbd">L</span> ouvir/parar. Usa a voz do próprio aparelho: funciona sem internet e não gasta dados.</p>
      <div class="grid2"><div><label>🗣️ Voz</label><select id="vzVoice">${opts || `<option value="">Voz padrão em português</option>`}</select></div>
       <div><label>⏩ Velocidade: <b id="vzRv">${this.rate.toString().replace(".", ",")}×</b></label><input type="range" id="vzRate" min="0.6" max="2" step="0.05" value="${this.rate}"></div></div>
      <div class="metaRow"><label class="chkL"><input type="checkbox" id="vzAuto" ${this.auto ? "checked" : ""}> 🎧 <b>Mãos livres:</b> ler sozinho a pergunta ao aparecer e a resposta ao revelar (flashcards, questões, micropartículas e treino de mnemônicos)</label></div>
      <div class="metaRow"><label class="chkL"><input type="checkbox" id="vzSrc" ${this.src ? "checked" : ""}> 📚 Ler também as fontes e referências dos cards e questões</label></div>
      <div class="metaRow"><button class="btn" id="vzTest">▶️ Testar voz</button><span class="metaNow">${pv.length} voz(es) em português neste aparelho${pv.length ? "" : " — instale em Ajustes do sistema › Acessibilidade › Conteúdo falado › Vozes › Português (Brasil)"}.</span></div>`;
    $("#vzVoice").onchange = e => { lsSet("vozName", e.target.value); this.say("Voz escolhida. Bons estudos!", { label: "Teste" }); };
    $("#vzRate").oninput = e => { $("#vzRv").textContent = (+e.target.value).toString().replace(".", ",") + "×"; };
    $("#vzRate").onchange = e => this.setRate(+e.target.value);
    $("#vzAuto").onchange = e => { lsSet("vozAuto", e.target.checked ? "1" : "0"); toast(e.target.checked ? "🎧 Mãos livres ligado" : "🎧 Mãos livres desligado"); };
    $("#vzSrc").onchange = e => lsSet("vozSrc", e.target.checked ? "1" : "0");
    $("#vzTest").onclick = () => this.say("Códice 360X. Pressão arterial média maior ou igual a 65 milímetros de mercúrio. Bons estudos, doutor!", { label: "Teste de voz" });
  },
  init() {
    const hb = $("#vozBtn"); if (hb) { if (!this.ok) hb.style.display = "none"; else hb.onclick = () => this.screen(hb); }
    const sb = $("#bVoz"); if (sb) { if (!this.ok) sb.style.display = "none"; else sb.onclick = () => this.study(sb); }
    if (!this.ok) return;
    try { speechSynthesis.onvoiceschanged = () => { if (location.hash === "#ajustes") this.settings(); }; } catch (e) { }
    const m = $("main"); let t = 0;
    if (m && typeof MutationObserver !== "undefined") new MutationObserver(() => { clearTimeout(t); t = setTimeout(() => this.decorate(), 40); }).observe(m, { childList: true, subtree: true });
    window.addEventListener("hashchange", () => { if (this.busy) this.stop(); this.lastAuto = ""; setTimeout(() => this.decorate(), 80); });
    document.addEventListener("keydown", e => { if (this.key(e)) e.stopImmediatePropagation(); }, true);
    window.addEventListener("pagehide", () => this.stop(true));
    const un = () => { if (this.auto) this.unlock(); document.removeEventListener("pointerdown", un, true); }; document.addEventListener("pointerdown", un, true);
  } };
