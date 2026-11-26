/* ---------------- ☑️ 4.26.0: checagem dos itens dos mnemônicos (checklist de todos) ----------------
   ALDENIR ROCHA DE OLIVEIRA FILHO · PROJETO 360X
   Cada item (letra) de um mnemônico vira uma caixinha. No 📖 Consultar a caixinha fica ao lado de cada linha;
   no modo ☑️ Checklist aparecem todos os mnemônicos da divisão, agrupados por tema, com progresso por tema e geral.
   Registro em S.logs._nc { id: { b: "1010", c: 0|1, x: 0|1, mod } } — b = itens checados na ordem, c = todos checados,
   x = XP do mnemônico completo já concedido (uma vez só). Sincroniza pelo `mod` mais recente (regra do _hu/_ce). */
const NCRES = () => (S.logs._nc = S.logs._nc || {});
const MNCK = { open: new Set(), ro: new Set(), all: false, rz: 0, _tk: null,
  bits(m) { const e = NCRES()[m.id], b = e && !e.del && typeof e.b === "string" ? e.b : ""; return m.k.map((_, i) => b[i] === "1"); },
  n(m) { return this.bits(m).filter(Boolean).length; },
  st(m) { const n = this.n(m); return n === 0 ? 0 : n >= m.k.length ? 2 : 1; },
  pc: (a, b) => b ? Math.round(100 * a / b) : 0,
  save(m, arr) {
    const R = NCRES(), old = R[m.id] || {}, full = arr.length > 0 && arr.every(Boolean), x = old.x || 0;
    R[m.id] = { b: arr.map(v => v ? "1" : "0").join(""), c: full ? 1 : 0, x: x || (full ? 1 : 0), mod: Date.now() };
    const L = L0(); L.nC = (L.nC || 0) + 1;
    if (full && !x) { addXP(1, "mnemônico checado", "n"); toast("☑️ Mnemônico checado por inteiro! +1 XP"); }
    saveLog();
  },
  toggle(m, i) { const a = this.bits(m); a[i] = !a[i]; this.save(m, a); },
  setAll(m, v) { this.save(m, m.k.map(() => v)); },
  tot(l) { let full = 0, part = 0, it = 0, itT = 0; for (const m of l) { const n = this.n(m); it += n; itT += m.k.length; if (n >= m.k.length) full++; else if (n) part++; } return { n: l.length, full, part, it, itT }; },
  totTxt(T) { return `${T.full} de ${T.n} mnemônicos checados por inteiro · ${T.part} em andamento · ${T.it}/${T.itT} itens`; },
  grpTxt(T) { return `✓ ${T.full}/${T.n} · ${T.it}/${T.itT} itens`; },
  tk(t) { if (!this._tk || this._tk.div !== MN.div) this._tk = { div: MN.div, ts: [...new Set(MN.all().map(x => x.tema))] }; return "t" + this._tk.ts.indexOf(t); },
  chip(m) { const n = this.n(m), s = this.st(m); return `<span class="ckChip${s === 2 ? " f" : s ? " p" : ""}" data-ckchip="${m.id}" title="Itens checados">☑️ ${n}/${m.k.length}</span>`; },
  cell(m, i, on) { return `<td class="ck"><button class="nck${on ? " on" : ""}" data-nck="${m.id}" data-i="${i}" aria-pressed="${on}" aria-label="Checar o item ${esc(m.k[i][0])}">${on ? "✓" : ""}</button></td>`; },
  bar(m) { return `<div class="ckBar"><button class="btn sm" data-ckall="${m.id}" data-v="1">☑️ Marcar todos</button><button class="btn sm" data-ckall="${m.id}" data-v="0">↺ Limpar</button></div>`; },
  row(m) {
    const a = this.bits(m), n = a.filter(Boolean).length, s = n === 0 ? 0 : n >= a.length ? 2 : 1;
    return `<div class="ckRow${s === 2 ? " full" : ""}${this.ro.has(m.id) ? " open" : ""}" data-ckrow="${m.id}"><div class="ckHd">
      <button class="nck big${s === 2 ? " on" : s ? " part" : ""}" data-ckall="${m.id}" data-v="t" aria-label="Checar o mnemônico inteiro">${s === 2 ? "✓" : s ? "–" : ""}</button>
      <div class="ckT" data-cko="${m.id}"><b>${esc(m.t)}</b><small>${esc(m.m)}</small></div><span class="ckN" data-ckn="${m.id}">${n}/${a.length}</span><button class="ckX" data-cko="${m.id}" aria-label="Mostrar os itens">▾</button></div>
      <ul class="ckItems">${m.k.map((k, i) => `<li${a[i] ? ' class="on"' : ""}><button class="nck${a[i] ? " on" : ""}" data-nck="${m.id}" data-i="${i}" aria-pressed="${a[i]}" aria-label="Checar o item ${esc(k[0])}">${a[i] ? "✓" : ""}</button><span><b>${esc(k[0])}</b> ${esc(k[1])}</span></li>`).join("")}</ul></div>`;
  },
  rows(tk) { return MN.list().filter(m => this.tk(m.tema) === tk).map(m => this.row(m)).join(""); },
  view(l) {
    const all = MN.all(), A = this.tot(all), grp = new Map();
    for (const m of l) { if (!grp.has(m.tema)) grp.set(m.tema, []); grp.get(m.tema).push(m); }
    const force = !!(MN.tema || MN.q.trim()) || grp.size === 1, armed = this.rz > Date.now();
    const temas = [...grp].map(([t, ms]) => { const k = this.tk(t), T = this.tot(ms), op = force || this.all || this.open.has(k);
      return `<details class="ckTema" data-ckt="${k}"${op ? " open" : ""}><summary><span class="ckTn">${esc(t)}</span><span class="ckN" data-cktn="${k}">${this.grpTxt(T)}</span></summary>
        <div class="ckProg sm"><i data-cktb="${k}" style="width:${this.pc(T.it, T.itT)}%"></i></div><div class="ckBody" data-ckb="${k}">${op ? ms.map(m => this.row(m)).join("") : ""}</div></details>`; }).join("");
    return `<div class="panel ckPanel"><div class="ckTop"><div><b>☑️ Checklist · ${esc(DIVS[MN.div] || MN.div)}</b><div class="ckN" id="ckTot">${this.totTxt(A)}</div></div>
      <div class="ckBtns"><button class="btn sm" id="ckOpenAll">${this.all ? "▸ Fechar os temas" : "▾ Abrir os temas"}</button><button class="btn sm" id="ckExp">📋 Exportar (.md)</button><button class="btn sm danger" id="ckReset">${armed ? `⚠️ Confirmar: zerar ${l.length}` : "🔄 Zerar este filtro"}</button></div></div>
      <div class="ckProg"><i id="ckTotBar" style="width:${this.pc(A.it, A.itT)}%"></i></div>
      <p class="metaNow">Toque na caixinha de cada item para checar; a caixa grande marca o mnemônico inteiro e ▾ mostra os itens.${l.length !== all.length ? ` Filtro atual: ${l.length} de ${all.length}.` : ""}</p></div>
      ${l.length ? temas : `<p class="empty">Nenhum mnemônico neste filtro.</p>`}`;
  },
  paint(host, m) {
    const a = this.bits(m), n = a.filter(Boolean).length, s = this.st(m), id = m.id;
    $$(`[data-nck="${id}"]`, host).forEach(b => { const on = !!a[+b.dataset.i]; b.classList.toggle("on", on); b.textContent = on ? "✓" : ""; b.setAttribute("aria-pressed", on); const r = b.closest("tr,li"); if (r) r.classList.toggle("on", on); });
    $$(`[data-ckchip="${id}"]`, host).forEach(c => { c.outerHTML = this.chip(m); });
    $$(`[data-ckn="${id}"]`, host).forEach(c => { c.textContent = `${n}/${a.length}`; });
    $$(`.nck.big[data-ckall="${id}"]`, host).forEach(b => { b.classList.toggle("on", s === 2); b.classList.toggle("part", s === 1); b.textContent = s === 2 ? "✓" : s ? "–" : ""; });
    $$(`[data-ckrow="${id}"]`, host).forEach(r => r.classList.toggle("full", s === 2));
    const all = MN.all(), A = this.tot(all), mk = $("#mnCkN", host); if (mk) mk.textContent = A.full;
    if (MN.mode !== "check") return;
    const k = this.tk(m.tema), T = this.tot(MN.list().filter(x => x.tema === m.tema));
    const tn = $(`[data-cktn="${k}"]`, host), tb = $(`[data-cktb="${k}"]`, host), tt = $("#ckTot", host), tg = $("#ckTotBar", host);
    if (tn) tn.textContent = this.grpTxt(T); if (tb) tb.style.width = this.pc(T.it, T.itT) + "%";
    if (tt) tt.textContent = this.totTxt(A); if (tg) tg.style.width = this.pc(A.it, A.itT) + "%";
  },
  reset(l) { const R = NCRES(), t = Date.now(); let z = 0; for (const m of l) { const e = R[m.id]; if (e && (e.b || "").includes("1")) { R[m.id] = { b: "", c: 0, x: e.x || 0, mod: t }; z++; } } saveLog(); toast(`🔄 Checagem zerada em ${z} mnemônico(s)`); },
  exp(l) {
    const T = this.tot(l), out = [`# ☑️ Checklist de mnemônicos — ${DIVS[MN.div] || MN.div}`, "", `**ALDENIR ROCHA DE OLIVEIRA FILHO · PROJETO 360X** · Códice 360X ${APP_VERSION} · ${new Date().toLocaleDateString("pt-BR")}`, "", `Progresso: ${this.totTxt(T)}`, ""];
    let cur = null;
    for (const m of l) {
      if (m.tema !== cur) { cur = m.tema; const ms = l.filter(x => x.tema === cur); out.push(`## ${cur} (${this.tot(ms).full}/${ms.length})`, ""); }
      const a = this.bits(m); out.push(`### [${a.every(Boolean) ? "x" : " "}] ${m.t} — ${m.m}`); m.k.forEach((k, i) => out.push(`- [${a[i] ? "x" : " "}] **${k[0]}** — ${k[1]}`)); out.push("");
    }
    out.push("---", "CÓDICE 360X · ALDENIR ROCHA DE OLIVEIRA FILHO · PROJETO 360X");
    CAD.dl(`Checklist_mnemonicos_${MN.div.toUpperCase()}_${today()}.md`, out.join("\n")); toast("📋 Checklist exportado");
  },
  bind(host) {
    host.onclick = e => {
      const b = e.target.closest("[data-nck],[data-ckall],[data-cko]"); if (!b || !host.contains(b)) return;
      const id = b.dataset.nck || b.dataset.ckall || b.dataset.cko, m = MN.all().find(x => x.id === id); if (!m) return;
      if (b.dataset.nck) this.toggle(m, +b.dataset.i);
      else if (b.dataset.ckall) this.setAll(m, b.dataset.v === "1" ? true : b.dataset.v === "0" ? false : this.st(m) !== 2);
      else { const r = b.closest(".ckRow"); if (r) { r.classList.toggle("open"); if (r.classList.contains("open")) this.ro.add(id); else this.ro.delete(id); } return; }
      this.paint(host, m);
    };
    $$("details.ckTema", host).forEach(d => d.ontoggle = () => { const k = d.dataset.ckt, bd = d.querySelector(".ckBody"); if (d.open) { this.open.add(k); if (bd && !bd.children.length) bd.innerHTML = this.rows(k); } else this.open.delete(k); });
    const oa = $("#ckOpenAll", host), ex = $("#ckExp", host), rz = $("#ckReset", host);
    if (oa) oa.onclick = () => { this.all = !this.all; if (!this.all) this.open.clear(); MN.render(); };
    if (ex) ex.onclick = () => this.exp(MN.list());
    if (rz) rz.onclick = () => {
      if (this.rz > Date.now()) { this.rz = 0; this.reset(MN.list()); }
      else { this.rz = Date.now() + 4000; setTimeout(() => { if (this.rz && this.rz <= Date.now() + 100) { this.rz = 0; if (MN.mode === "check") MN.render(); } }, 4100); }
      MN.render();
    };
  } };
