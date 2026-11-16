/* 🧪 GASO_ENG — motor de gasometria 360X (espelho de tools/gaso/gaso_engine.py; mesmas regras e códigos). */
const GASO_ENG = (() => {
  const NOME = { AM_AG: "Acidose metabólica com ânion gap elevado", AM_HC: "Acidose metabólica hiperclorêmica (ânion gap normal)", ALM: "Alcalose metabólica",
    AR_A: "Acidose respiratória aguda", AR_C: "Acidose respiratória crônica", AR_CA: "Acidose respiratória crônica agudizada", ALR_A: "Alcalose respiratória aguda",
    ALR_C: "Alcalose respiratória crônica", AR: "Acidose respiratória", ALR: "Alcalose respiratória", NORMAL: "Equilíbrio ácido-base normal" };
  const ORD = ["AM_AG", "AM_HC", "ALM", "AR_A", "AR_C", "AR_CA", "AR", "ALR_A", "ALR_C", "ALR", "NORMAL"];
  const f = (x, d = 1) => x == null || isNaN(x) ? "—" : Number(x).toFixed(d).replace(".", ",");
  const nz = v => v !== undefined && v !== null && v !== "" && !isNaN(v);
  function prep(lab) {
    const L = Object.assign({}, lab);
    for (const k of Object.keys(L)) if (L[k] === "" || L[k] === null) delete L[k];
    if (nz(L.hco3) && nz(L.pco2) && !nz(L.ph)) L.ph = Math.round((6.1 + Math.log10(L.hco3 / (0.03 * L.pco2))) * 100) / 100;
    if (nz(L.ag) && !nz(L.cl) && nz(L.na)) L.cl = L.na - L.ag - L.hco3;
    delete L.ag;
    if (nz(L.ph) && nz(L.hco3)) L.be = Math.round(0.93 * (L.hco3 - 24.4 + 14.8 * (L.ph - 7.4)) * 10) / 10;
    if (!nz(L.fio2) && nz(L.pao2)) L.fio2 = 0.21;
    return L;
  }
  function analyze(lab) {
    const L = prep(lab), ph = +L.ph, pc = +L.pco2, h = +L.hco3, st = [];
    let codes = [];
    const alb = nz(L.alb) ? +L.alb : null;
    let ag = null, agc = null;
    if (nz(L.na) && nz(L.cl)) { ag = L.na - (+L.cl + h); agc = alb != null ? ag + 2.5 * (4 - alb) : ag; }
    let agHigh = agc != null && agc > 12; const agHidden = agc != null && agc >= 16;
    const R = { lab: L, ag, agc };
    let side;
    if (ph < 7.35) { st.push(`pH ${f(ph, 2)} → <b>acidemia</b>`); side = "acid"; }
    else if (ph > 7.45) { st.push(`pH ${f(ph, 2)} → <b>alcalemia</b>`); side = "alk"; }
    else { st.push(`pH ${f(ph, 2)} → <b>dentro da faixa normal</b> (7,35–7,45): ou não há distúrbio ou há distúrbios que se anulam`); side = "nl"; }
    const winter = () => {
      const e = 1.5 * h + 8; R.exp = [e - 2, e + 2];
      let s = `Winter: 1,5 × ${f(h, 0)} + 8 = ${f(e)} ± 2 (${f(e - 2)}–${f(e + 2)}); PaCO₂ ${f(pc, 0)} → `;
      if (pc > e + 2) { codes.push("AR"); s += "<b>acima</b>: acidose respiratória associada"; }
      else if (pc < e - 2) { codes.push("ALR"); s += "<b>abaixo</b>: alcalose respiratória associada"; }
      else s += "compensação respiratória <b>adequada</b>";
      st.push(s);
    };
    const malk = () => {
      const e = Math.min(0.7 * h + 21, 55); R.exp = [e - 2, e + 2];
      let s = `PaCO₂ esperada = 0,7 × ${f(h, 0)} + 21 = ${f(e)} ± 2 (${f(e - 2)}–${f(e + 2)}); PaCO₂ ${f(pc, 0)} → `;
      if (pc > e + 2) { codes.push("AR"); s += "<b>acima</b>: acidose respiratória associada"; }
      else if (pc < e - 2) { codes.push("ALR"); s += "<b>abaixo</b>: alcalose respiratória associada"; }
      else s += "compensação respiratória <b>adequada</b>";
      st.push(s);
    };
    const racid = () => {
      const d = pc - 40, a = 24 + 0.1 * d, c = 24 + 0.35 * d; R.exp = [a, c];
      let s = `HCO₃⁻ esperado: aguda 24 + 0,1 × ${f(d, 0)} = ${f(a)} · crônica 24 + 0,35 × ${f(d, 0)} = ${f(c)}; HCO₃⁻ ${f(h, 0)} → `;
      if (h < a - 2) { codes.push("AR", "AM?"); s += "<b>abaixo do esperado</b>: acidose metabólica associada"; }
      else if (h <= a + 2 && (h - a) <= (c - h)) { codes.push("AR_A"); s += "<b>aguda</b>"; }
      else if (h >= c - 2 && h <= c + 2) { codes.push("AR_C"); s += "<b>crônica</b> (compensada pelo rim)"; }
      else if (h > c + 2) { codes.push("AR", "ALM"); s += "<b>acima do esperado</b>: alcalose metabólica associada"; }
      else { codes.push("AR_CA"); s += "<b>entre aguda e crônica</b>: crônica agudizada"; }
      st.push(s);
    };
    const ralk = () => {
      const d = 40 - pc, a = 24 - 0.2 * d, c = 24 - 0.4 * d; R.exp = [c, a];
      let s = `HCO₃⁻ esperado: aguda 24 − 0,2 × ${f(d, 0)} = ${f(a)} · crônica 24 − 0,4 × ${f(d, 0)} = ${f(c)}; HCO₃⁻ ${f(h, 0)} → `;
      if (h > a + 2) { codes.push("ALR", "ALM"); s += "<b>acima do esperado</b>: alcalose metabólica associada"; }
      else if (h >= a - 2 && (a - h) <= (h - c)) { codes.push("ALR_A"); s += "<b>aguda</b>"; }
      else if (h >= c - 2 && h <= c + 2) { codes.push("ALR_C"); s += "<b>crônica</b> (compensada pelo rim)"; }
      else if (h < c - 2) { codes.push("ALR", "AM?"); s += "<b>abaixo do esperado</b>: acidose metabólica associada"; }
      else { codes.push("ALR_C"); s += "em compensação (subaguda)"; }
      st.push(s);
    };
    R.side = side; R.prim = "NL";
    if (side === "acid") {
      if (h < 22) { st.push(`HCO₃⁻ ${f(h, 0)} ↓ → distúrbio primário <b>metabólico</b> (acidose metabólica)`); codes.push("AM?"); R.prim = "AM"; winter(); }
      else { st.push(`PaCO₂ ${f(pc, 0)} ↑ → distúrbio primário <b>respiratório</b> (acidose respiratória)`); R.prim = "AR"; racid(); }
    } else if (side === "alk") {
      if (h > 26) { st.push(`HCO₃⁻ ${f(h, 0)} ↑ → distúrbio primário <b>metabólico</b> (alcalose metabólica)`); codes.push("ALM"); R.prim = "ALM"; malk(); }
      else { st.push(`PaCO₂ ${f(pc, 0)} ↓ → distúrbio primário <b>respiratório</b> (alcalose respiratória)`); R.prim = "ALR"; ralk(); }
    } else {
      if (h >= 22 && h <= 26 && pc >= 35 && pc <= 45) st.push("PaCO₂ e HCO₃⁻ normais → sem distúrbio respiratório; olhar o AG (acidose oculta?)");
      else if ((h < 22 && pc > 45) || (h > 26 && pc < 35)) { st.push("HCO₃⁻ e PaCO₂ em sentidos opostos com pH normal → distúrbios opostos que se anulam"); codes.push(...(h < 22 ? ["AM?", "AR"] : ["ALM", "ALR"])); }
      else if (h < 22 && (ph < 7.40 || agHidden || pc >= 35)) { st.push(`HCO₃⁻ ${f(h, 0)} ↓ com pH no lado ácido (ou AG alto) → acidose metabólica; checar compensação`); codes.push("AM?"); winter(); }
      else if (pc < 35) { st.push(`PaCO₂ ${f(pc, 0)} ↓ com pH no lado alcalino → alcalose respiratória; checar compensação`); ralk(); }
      else if (h > 26 && (ph >= 7.40 || pc <= 45)) { st.push(`HCO₃⁻ ${f(h, 0)} ↑ com pH no lado alcalino → alcalose metabólica; checar compensação`); codes.push("ALM"); malk(); }
      else if (pc > 45) { st.push(`PaCO₂ ${f(pc, 0)} ↑ com pH no lado ácido → acidose respiratória; checar compensação`); racid(); }
      else st.push("Valores praticamente normais");
    }
    if (ag != null) {
      let s = `AG = ${f(L.na, 0)} − (${f(L.cl, 0)} + ${f(h, 0)}) = ${f(ag, 0)}`;
      if (alb != null && alb !== 4) s += `; corrigido pela albumina ${f(alb)}: ${f(ag, 0)} + 2,5 × (4 − ${f(alb)}) = <b>${f(agc)}</b>`;
      const amet = codes.includes("AM?");
      s += " → " + ((amet ? agHigh : agHidden) ? "<b>elevado</b>" : agHigh ? "limítrofe (13–15: sem valor isolado)" : "normal");
      st.push(s);
    }
    if (codes.includes("AM?")) { codes = codes.filter(c => c !== "AM?"); codes.push(agHigh ? "AM_AG" : "AM_HC"); }
    else if (!agHidden) agHigh = false;
    if (agHigh) {
      if (!codes.includes("AM_AG")) codes.push("AM_AG");
      if (h < 24) {
        const dd = (agc - 12) / (24 - h); R.dd = dd;
        let s = `Δ/Δ = (${f(agc)} − 12) / (24 − ${f(h, 0)}) = <b>${f(dd)}</b> → `;
        if (dd < 0.8) { s += "&lt; 0,8: acidose hiperclorêmica associada"; codes.push("AM_HC"); }
        else if (dd > 2) { s += "&gt; 2: alcalose metabólica associada"; codes.push("ALM"); }
        else s += "0,8–2: acidose com AG elevado <b>pura</b>";
        st.push(s);
      } else {
        const hc = h + (agc - 12); R.hco3c = hc;
        st.push(`AG elevado com HCO₃⁻ ≥ 24: HCO₃⁻ corrigido = ${f(h, 0)} + (${f(agc)} − 12) = ${f(hc)} → acidose com AG <b>mascarada</b>` + (hc > 26 ? " por alcalose metabólica" : ""));
        if (hc > 26 && !codes.includes("ALM")) codes.push("ALM");
      }
    }
    if (codes.some(c => ["AM_AG", "AM_HC", "ALM"].includes(c))) codes = codes.map(c => ["AR_A", "AR_C", "AR_CA"].includes(c) ? "AR" : ["ALR_A", "ALR_C"].includes(c) ? "ALR" : c);
    if (!codes.length) codes.push("NORMAL");
    codes = [...new Set(codes)];
    if (codes.includes("NORMAL") && codes.length > 1) codes = codes.filter(c => c !== "NORMAL");
    if (nz(L.osm) && nz(L.glic) && nz(L.ureia)) {
      const oc = 2 * L.na + L.glic / 18 + L.ureia / 6, gap = L.osm - oc; R.ogap = gap;
      st.push(`Osm calculada = 2 × ${f(L.na, 0)} + ${f(L.glic, 0)}/18 + ${f(L.ureia, 0)}/6 = ${f(oc)}; gap osmolar = ${f(L.osm, 0)} − ${f(oc)} = <b>${f(gap)}</b> → ` + (gap > 10 ? "<b>elevado</b> (&gt; 10): álcool tóxico?" : "normal"));
    }
    if (nz(L.una) && nz(L.uk) && nz(L.ucl)) {
      const u = +L.una + +L.uk - L.ucl; R.uag = u;
      st.push(`AG urinário = ${f(L.una, 0)} + ${f(L.uk, 0)} − ${f(L.ucl, 0)} = <b>${f(u, 0)}</b> → ` + (u < 0 ? "negativo: NH₄⁺ urinário preservado (perda GI)" : "positivo: falha de excreção de NH₄⁺ (ATR distal)"));
    } else if (nz(L.ucl) && codes.includes("ALM")) {
      const u = +L.ucl;
      st.push(`Cloro urinário ${f(u, 0)} mEq/L → ` + (u < 20 ? "&lt; 20: <b>responsiva a cloreto</b> (volume/cloro)" : u > 40 ? "&gt; 40: <b>resistente a cloreto</b>" : "intermediário"));
    }
    if (nz(L.pao2)) {
      const fi = +(L.fio2 || 0.21), pa = +L.pao2, patm = nz(L.patm) ? +L.patm : 760;
      const PA = fi * (patm - 47) - pc / 0.8, aa = PA - pa, pf = pa / fi; Object.assign(R, { PA, aa, pf });
      let s;
      if (fi <= 0.21 + 1e-6) {
        const ex = (nz(L.idade) ? +L.idade : 40) / 4 + 4; R.aa_exp = ex;
        s = `PAO₂ = 0,21 × (${f(patm, 0)} − 47) − ${f(pc, 0)}/0,8 = ${f(PA)}; A-a = ${f(PA)} − ${f(pa, 0)} = <b>${f(aa)}</b> (esperado ≈ ${f(ex)})`;
        if (pa < 80) s += " → hipoxemia " + (aa <= ex + 2 ? "com A-a <b>normal</b>: hipoventilação (ou PiO₂ baixa)" : "com A-a <b>elevado</b>: V/Q, shunt ou difusão");
        else s += " → oxigenação adequada";
      } else {
        s = `P/F = ${f(pa, 0)}/${f(fi, 2)} = <b>${f(pf, 0)}</b> → ` + (pf <= 100 ? "hipoxemia grave (≤ 100)" : pf <= 200 ? "hipoxemia moderada (101–200)" : pf <= 300 ? "hipoxemia leve (201–300)" : "&gt; 300") + `; PAO₂ ${f(PA, 0)}, A-a ${f(aa, 0)}`;
      }
      st.push(s);
    }
    R.codes = codes.sort((a, b) => ORD.indexOf(a) - ORD.indexOf(b));
    R.steps = st; R.dx = R.codes.map(c => NOME[c]).join(" + ");
    const ex = extras(L); R.x = ex[0]; R.xsteps = ex[1];
    return R;
  }
  const fh = (x, d = 1) => f(Math.floor(x * 10 ** d + 0.5 + 1e-9) / 10 ** d, d);
  const g = (x, d = 1) => Math.abs(x - Math.round(x)) < 1e-9 ? f(x, 0) : fh(x, d);
  const r0 = x => f(Math.floor(x + 0.5), 0);
  /* 4.14.0 · VM e gasometria venosa (espelho de extras() do Python) */
  function extras(L) {
    const X = {}, xs = [], pc = +L.pco2, vm = L.vm, ve = L.ven;
    if (vm) {
      const vc = nz(vm.vc) ? +vm.vc : null, fr = nz(vm.fr) ? +vm.fr : null, pbw = nz(vm.pbw) ? +vm.pbw : null;
      if (vc != null && fr != null) {
        const vmin = vc * fr / 1000; X.ve = vmin;
        let s = `Volume-minuto = ${g(vc)} mL × ${g(fr)} = <b>${fh(vmin)}</b> L/min`;
        if (pbw) {
          X.vckg = vc / pbw; s += `; VC = ${g(vc)}/${g(pbw)} = <b>${fh(vc / pbw)}</b> mL/kg de peso predito` + (vc / pbw > 8.05 ? " (&gt; 8: reduzir)" : "");
          const vr = vc * fr * pc / (pbw * 100 * 37.5); X.vr = vr;
          s += `; razão ventilatória = (${g(vc)} × ${g(fr)} × ${g(pc)}) / (${g(pbw)} × 100 × 37,5) = <b>${fh(vr, 2)}</b> (≈ 1 normal; maior = mais espaço morto)`;
        }
        xs.push(s);
      }
      if (nz(vm.pplat) && nz(vm.peep)) {
        const dp = vm.pplat - vm.peep; X.dp = dp;
        xs.push(`Driving pressure = Pplatô ${g(+vm.pplat)} − PEEP ${g(+vm.peep)} = <b>${g(dp)}</b> cmH₂O → ` + (dp > 15 ? "&gt; 15: lesivo — reduzir VC" : "≤ 15: protetor") + (vm.pplat > 30 ? "; Pplatô &gt; 30: reduzir VC" : ""));
      }
      if (nz(vm.etco2)) {
        const gp = pc - vm.etco2; X.gapet = gp;
        xs.push(`Gap PaCO₂ − EtCO₂ = ${g(pc)} − ${g(+vm.etco2)} = <b>${g(gp)}</b> mmHg → ` + (gp > 5 ? "&gt; 5: <b>espaço morto aumentado</b> (TEP, baixo débito, hiperdistensão, auto-PEEP)" : "2–5: normal"));
      }
      if (nz(vm.alvo) && fr != null) {
        const frn = fr * pc / vm.alvo; X.frn = frn;
        let s = `FR para PaCO₂ alvo ${g(+vm.alvo)}: ${g(fr)} × ${g(pc)}/${g(+vm.alvo)} = <b>${r0(frn)}</b> irpm`;
        if (frn > 35) s += " → acima de 35: risco de auto-PEEP — reduzir espaço morto (trocar HME por umidificador aquecido), prona, ECCO₂R/ECMO";
        if (vc != null) { const vcn = vc * pc / vm.alvo; X.vcn = vcn; s += `; ou VC ${g(vc)} × ${g(pc)}/${g(+vm.alvo)} ≈ ${r0(vcn)} mL` + (pbw ? ` (${fh(vcn / pbw)} mL/kg)` : ""); }
        xs.push(s);
      }
    }
    if (ve) {
      const kind = ve.kind || "central", pv = nz(ve.pco2) ? +ve.pco2 : null;
      if (kind === "periferica") {
        if (nz(ve.ph) && nz(L.ph)) {
          const dph = L.ph - ve.ph; X.dph = dph;
          xs.push(`Venosa periférica × arterial: pH ${fh(+ve.ph, 2)} × ${fh(+L.ph, 2)} (Δ ${fh(dph, 2)}; esperado 0,02–0,05)` + (pv != null ? `; PvCO₂ ${g(pv)} × PaCO₂ ${g(pc)} (Δ ${g(pv - pc)}; esperado ≈ 4–6, concordância ruim no choque)` : "") + (nz(ve.hco3) ? `; HCO₃⁻ ${g(+ve.hco3)} × ${g(+L.hco3)}` : ""));
        }
        return [X, xs];
      }
      if (pv != null) { const gap = pv - pc; X.gapco2 = gap; xs.push(`Gap CO₂ (Pcv−aCO₂) = ${g(pv)} − ${g(pc)} = <b>${g(gap)}</b> mmHg → ` + (gap > 6 ? "&gt; 6: <b>fluxo (débito cardíaco) insuficiente</b> para a produção de CO₂" : "≤ 6: fluxo adequado para o metabolismo")); }
      const sv = nz(ve.sat) ? +ve.sat : null, nm = kind === "mista" ? "SvO₂" : "ScvO₂";
      if (sv != null) xs.push(`${nm} ${g(sv)}% → ` + (sv < 70 ? "&lt; 70%: <b>extração aumentada</b> (oferta de O₂ baixa para o consumo)" : sv > 80 ? "&gt; 80%: <b>extração baixa</b> — fluxo alto ou falha de extração (sepse, microcirculação, shunt)" : "70–80%: faixa-alvo"));
      const sa = nz(L.sat) ? +L.sat : null, hb = nz(L.hb) ? +L.hb : null;
      if (sv != null && sa != null && hb != null && pv != null) {
        const ca = 1.34 * hb * sa / 100 + 0.003 * (nz(L.pao2) ? +L.pao2 : 0), cv = 1.34 * hb * sv / 100 + 0.003 * (nz(ve.pao2) ? +ve.pao2 : 0), d = ca - cv, r = (pv - pc) / d;
        Object.assign(X, { ca, cv, cav: d, ratio: r, ero2: (sa - sv) / sa });
        xs.push(`CaO₂ ${fh(ca)} − CvO₂ ${fh(cv)} = <b>${fh(d)}</b> mL/dL; extração ${r0(100 * (sa - sv) / sa)}%; gap CO₂/Ca−vO₂ = ${g(pv - pc)}/${fh(d)} = <b>${fh(r)}</b> → ` + (r > 1.4 ? "&gt; 1,4: sugere <b>metabolismo anaeróbio</b> (lactato de hipóxia tecidual)" : "≤ 1,4: sem sinal de anaerobiose global"));
      }
    }
    return [X, xs];
  }
  const ROWS = [["ph", "pH", "", 2], ["pco2", "PaCO₂", "mmHg", 0], ["hco3", "HCO₃⁻", "mEq/L", 0], ["be", "BE", "mEq/L", 1], ["pao2", "PaO₂", "mmHg", 0], ["sat", "SatO₂", "%", 0],
    ["na", "Na⁺", "mEq/L", 0], ["k", "K⁺", "mEq/L", 1], ["cl", "Cl⁻", "mEq/L", 0], ["alb", "Albumina", "g/dL", 1], ["lac", "Lactato", "mmol/L", 1], ["glic", "Glicose", "mg/dL", 0],
    ["ureia", "Ureia", "mg/dL", 0], ["cr", "Creatinina", "mg/dL", 1], ["osm", "Osm medida", "mOsm/kg", 0], ["cet", "β-OH-butirato", "mmol/L", 1], ["hb", "Hb", "g/dL", 1],
    ["cohb", "COHb", "%", 0], ["methb", "MetHb", "%", 0], ["svo2", "SvcO₂", "%", 0], ["una", "Na urinário", "mEq/L", 0], ["uk", "K urinário", "mEq/L", 0], ["ucl", "Cl urinário", "mEq/L", 0]];
  function panel(lab, titulo) {
    const L = prep(lab), ven = L.tipo === "venosa", fi = L.fio2, td = "padding:3px 7px;border:1px solid rgba(128,128,128,.35)";
    const hd = titulo || ("🩸 Gasometria " + (ven ? "venosa" : "arterial") + (fi ? ` · FiO₂ ${Math.round(fi * 100)}%` : "") + (L.peep ? ` · PEEP ${L.peep}` : ""));
    const cells = ROWS.filter(([k]) => nz(L[k])).map(([k, n, u, d]) => [ven && k === "pco2" ? "PvCO₂" : ven && k === "pao2" ? "PvO₂" : n, f(+L[k], d), u]);
    let h = `<table class="gaso" style="border-collapse:collapse;margin:8px 0 4px;font-size:15px;line-height:1.35"><tr><th colspan="4" style="${td};text-align:left;background:rgba(77,212,255,.13)">${hd}</th></tr>`;
    for (let i = 0; i < cells.length; i += 2) h += "<tr>" + cells.slice(i, i + 2).map(([n, v, u]) => `<td style="${td}">${n}</td><td style="${td}"><b>${v}</b> <small>${u}</small></td>`).join("") + (i + 1 >= cells.length ? `<td style="${td}"></td><td style="${td}"></td>` : "") + "</tr>";
    h += "</table>";
    const vm = L.vm, ve = L.ven, us = L.us;
    if (vm) h += block("🫁 Ventilador", [["Modo", vm.modo, "", null], ["VC", vm.vc, "mL", 0], ["FR", vm.fr, "irpm", 0], ["PEEP", vm.peep, "cmH₂O", 0], ["Pplatô", vm.pplat, "cmH₂O", 0], ["EtCO₂", vm.etco2, "mmHg", 0], ["Peso predito", vm.pbw, "kg", 0], ["PaCO₂ alvo", vm.alvo, "mmHg", 0]]
      .filter(([, v]) => v !== undefined && v !== null && v !== "").map(([n, v, u, d]) => [n, d == null ? v : f(+v, d), u]), td);
    if (ve) {
      const kind = ve.kind || "central", nm = { central: "🩸 Venosa central (simultânea)", mista: "🩸 Venosa mista (cateter de artéria pulmonar)", periferica: "🩸 Venosa periférica (simultânea)" }[kind];
      const sv = kind === "mista" ? "SvO₂" : kind === "central" ? "ScvO₂" : "SvO₂ periférica";
      h += block(nm, [["pH", ve.ph, "", 2], ["PvCO₂", ve.pco2, "mmHg", 0], ["HCO₃⁻", ve.hco3, "mEq/L", 0], ["PvO₂", ve.pao2, "mmHg", 0], [sv, ve.sat, "%", 0]].filter(([, v]) => nz(v)).map(([n, v, u, d]) => [n, f(+v, d), u]), td);
    }
    if (us) h += `<table class="gaso" style="border-collapse:collapse;margin:4px 0;font-size:15px;line-height:1.35"><tr><td style="${td};background:rgba(255,193,77,.12)">🔊 <b>POCUS:</b> ${us}</td></tr></table>`;
    return h;
  }
  function block(hd, cells, td) {
    let o = `<table class="gaso" style="border-collapse:collapse;margin:4px 0;font-size:15px;line-height:1.35"><tr><th colspan="4" style="${td};text-align:left;background:rgba(77,212,255,.13)">${hd}</th></tr>`;
    for (let i = 0; i < cells.length; i += 2) o += "<tr>" + cells.slice(i, i + 2).map(([n, v, u]) => `<td style="${td}">${n}</td><td style="${td}"><b>${v}</b> <small>${u}</small></td>`).join("") + (i + 1 >= cells.length ? `<td style="${td}"></td><td style="${td}"></td>` : "") + "</tr>";
    return o + "</table>";
  }
  return { analyze, prep, panel, extras, NOME, f };
})();
if (typeof module !== "undefined") module.exports = GASO_ENG;
