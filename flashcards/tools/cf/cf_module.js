/* ---------------- 🎯 Confiança no domínio 1–5 (4.15.0): caixinha em cada item de todas as abas, soma XP ----------------
   Onde fica: flashcards → no progresso do próprio card (c.cf, sincroniza junto com o card);
              demais itens → S.logs._cf[chave] = [nota 1–5, segundos, XP já dado no dia] (mescla: vence a marcação mais recente).
   Chaves: c:<card> · q:<questão> · m:<micropartícula> · n:<mnemônico> · h:<Honra card/mnemônico> · hb:<bússola> · g:<caso de gaso> · gf:<fórmula>.
   XP = a nota marcada (+1 a +5), uma vez por item por dia; trocar a nota no mesmo dia soma só a diferença para cima (nunca desconta). */
const CF = {
  LV: [null, ["🔴", "Não sei", "#ff6b6b"], ["🟠", "Vago", "#ff9d5c"], ["🟡", "Razoável", "#ffc14d"], ["🟢", "Seguro", "#5be38a"], ["💎", "Domino", "#4dd4ff"]],
  SEC: { c: "🎴 Flashcards", q: "❓ Questões", m: "💊 Micropartículas", n: "🧠 Mnemônicos", h: "🕊️ Honra", hb: "🧭 Bússolas", g: "🧪 Casos de gasometria", gf: "📐 Fórmulas" },
  R() { return (S.logs._cf = S.logs._cf || {}); },
  card(k) { return k.startsWith("c:") ? S.byId.get(k.slice(2)) : null; },
  get(k) { if (k.startsWith("c:")) { const c = this.card(k); return c && Array.isArray(c.cf) ? c.cf : null; } const e = this.R()[k]; return Array.isArray(e) ? e : null; },
  val(k) { const e = this.get(k); return e ? e[0] || 0 : 0; },
  low(k) { const v = this.val(k); return v > 0 && v <= 2; },
  isToday(e) { return !!e && dayKey((e[1] || 0) * 1000) === today(); },
  gotToday(k) { const e = this.get(k); return this.isToday(e) ? e[2] || 0 : 0; },
  slug: s => String(s || "").normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "").slice(0, 40),
  box(k, o = {}) {
    const v = this.val(k), g = this.gotToday(k), L = this.LV, short = o.sm || o.bar;
    return `<div class="cfBox vozSkip${o.sm ? " sm" : ""}${o.pri ? " pri" : ""}${o.bar ? " cfBar" : ""}${v ? " v" + v : ""}" data-cfk="${esc(k)}" role="group" aria-label="Confiança no domínio deste item, de 1 a 5">`
      + `<span class="cfLbl">🎯 ${short ? "Confiança" : "Confiança no domínio"}</span><span class="cfBtns">${[1, 2, 3, 4, 5].map(i => `<button type="button" class="cfB${v === i ? " on" : ""}${v && i < v ? " lit" : ""}" data-cfv="${i}" style="--cfc:${L[i][2]}" aria-pressed="${v === i}" title="${i} · ${L[i][0]} ${L[i][1]} (+${i} XP)"><i aria-hidden="true">${v === i ? "☑" : "☐"}</i>${i}</button>`).join("")}</span>`
      + `<span class="cfSt">${v ? `${L[v][0]} <b>${L[v][1]}</b>${g ? ` · +${g} XP hoje` : ""}` : "marque de 1 a 5 · +1 a +5 XP"}</span></div>`;
  },
  opts(el) { return { sm: el.classList.contains("sm"), pri: el.classList.contains("pri"), bar: el.classList.contains("cfBar") }; },
  paint(k, v) {
    for (const el of $$("[data-cfk]")) if (el.dataset.cfk === k) { const t = document.createElement("div"); t.innerHTML = this.box(k, this.opts(el)); const n = t.firstElementChild; el.replaceWith(n); const b = v && n.querySelector(`[data-cfv="${v}"]`); if (b) b.classList.add("pop"); }
  },
  async set(k, v) {
    v = Math.max(0, Math.min(5, Math.round(+v) || 0)); if (!v) return 0;
    const prev = this.get(k), same = this.isToday(prev); if (same && prev[0] === v) return 0;   // mesma nota no mesmo dia: nada muda
    const given = same ? prev[2] || 0 : 0, gain = Math.max(0, v - given), e = [v, Math.floor(Date.now() / 1000), Math.max(given, v)], c = this.card(k);
    if (k.startsWith("c:")) { if (!c) return 0; c.cf = e; } else this.R()[k] = e;
    const L = L0(); if (!same) L.cfN = (L.cfN || 0) + 1;
    if (gain) addXP(gain, `confiança ${this.LV[v][0]} ${v}`, "f");
    if (c) await saveProg(c);
    await saveLog();
    return gain;
  },
  async pick(el, v) { const k = el.dataset.cfk; await this.set(k, v); this.paint(k, v); },
  primary() {
    if (location.hash === "#estudar") return $("#barAns.on .cfBox") || $("#barHist.on .cfBox");
    return $$(".view.on .cfBox.pri").find(b => b.getClientRects().length) || null;
  },
  lowCards() { return (S.cards || []).filter(c => !c.susp && Array.isArray(c.cf) && c.cf[0] > 0 && c.cf[0] <= 2).map(c => c.id); },
  stats() {
    const d = [0, 0, 0, 0, 0, 0], sec = {};
    const add = (s, v) => { if (!(v >= 1 && v <= 5)) return; d[v]++; const o = sec[s] = sec[s] || { n: 0, sum: 0, low: 0, top: 0 }; o.n++; o.sum += v; if (v <= 2) o.low++; if (v === 5) o.top++; };
    for (const c of S.cards || []) if (Array.isArray(c.cf)) add("c", c.cf[0]);
    for (const [k, e] of Object.entries(S.logs._cf || {})) if (Array.isArray(e)) add(k.slice(0, k.indexOf(":")), e[0]);
    const n = d.reduce((a, b) => a + b, 0), sum = d.reduce((a, b, i) => a + b * i, 0);
    return { d, n, avg: n ? sum / n : 0, sec, low: d[1] + d[2], top: d[5] };
  },
  html() {
    const s = this.stats(), xp = dayLogs().reduce((a, [, l]) => a + ((l.xs || {}).f || 0), 0), low = this.lowCards().length, f1 = x => x.toFixed(1).replace(".", ",");
    const bars = [5, 4, 3, 2, 1].map(i => { const p = s.n ? Math.round(100 * s.d[i] / s.n) : 0; return `<div class="cfRowS"><span>${this.LV[i][0]} ${i} · ${this.LV[i][1]}</span><span class="xpTrack"><i style="width:${p}%;background:${this.LV[i][2]}"></i></span><small>${s.d[i].toLocaleString("pt-BR")} (${p}%)</small></div>`; }).join("");
    const secs = Object.entries(this.SEC).filter(([k]) => s.sec[k]).map(([k, nm]) => { const o = s.sec[k]; return `<tr><td>${nm}</td><td>${o.n.toLocaleString("pt-BR")}</td><td><b>${f1(o.sum / o.n)}</b></td><td>${o.low}</td><td>${o.top}</td></tr>`; }).join("");
    return `<div class="panel" id="cfPanel"><h2 style="margin-top:0">🎯 Confiança no domínio</h2>
      ${s.n ? `<div class="stats"><div class="stat"><b class="n">${s.n.toLocaleString("pt-BR")}</b><span>itens avaliados</span></div><div class="stat"><b style="color:var(--gold2)">${f1(s.avg)}</b><span>média (1–5)</span></div>
        <div class="stat"><b style="color:var(--cy)">💎 ${s.top.toLocaleString("pt-BR")}</b><span>domino (5)</span></div><div class="stat"><b style="color:var(--red)">${s.low.toLocaleString("pt-BR")}</b><span>a reforçar (1–2)</span></div><div class="stat"><b style="color:var(--amb)">${xp.toLocaleString("pt-BR")}</b><span>XP de confiança</span></div></div>
       <div class="cfDist">${bars}</div>${secs ? `<table class="t jrRank cfSec"><tr><th>Seção</th><th>Itens</th><th>Média</th><th>🔴 1–2</th><th>💎 5</th></tr>${secs}</table>` : ""}
       ${low ? `<div class="metaRow"><button class="btn gold" id="cfLowStudy">🔁 Estudar os ${low.toLocaleString("pt-BR")} flashcards com confiança 1–2</button></div>` : ""}` : `<p class="metaNow">Nenhum item avaliado ainda — a caixinha 🎯 aparece em cada item de todas as abas.</p>`}
      <p class="metaNow">🎯 A caixinha <b>1–5</b> aparece em cada flashcard (ao revelar), questão (ao responder), micropartícula, mnemônico, card e bússola da Honra, caso de gasometria e fórmula. Marcar dá <b>+1 a +5 XP</b> — o valor da nota —, uma vez por item por dia; trocar a nota no mesmo dia soma só a diferença. ⌨️ <span class="kbd">Shift</span> + <span class="kbd">1</span>–<span class="kbd">5</span> marca o item da tela. Filtros "🔴 Confiança baixa" em Questões, Mnemônicos e Honra; em 🔎 Buscar: <code>is:conf1</code>…<code>is:conf5</code>, <code>is:confbaixa</code>, <code>is:semconf</code>.</p></div>`;
  },
  bind(host) { const b = $("#cfLowStudy", host); if (b) b.onclick = () => startStudy(null, this.lowCards()); } };
document.addEventListener("click", e => {
  const b = e.target && e.target.closest ? e.target.closest("[data-cfv]") : null; if (!b) return;
  const box = b.closest("[data-cfk]"); if (!box) return; e.preventDefault(); CF.pick(box, +b.dataset.cfv);
});
document.addEventListener("keydown", e => {
  if (!e.shiftKey || e.ctrlKey || e.metaKey || e.altKey || /input|textarea|select/i.test((e.target || {}).tagName || "")) return;
  const m = /^Digit([1-5])$/.exec(e.code || ""); if (!m) return;
  const box = CF.primary(); if (!box) return; e.preventDefault(); CF.pick(box, +m[1]);
});

