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
    return R;
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
    return h + "</table>";
  }
  return { analyze, prep, panel, NOME, f };
})();
if (typeof module !== "undefined") module.exports = GASO_ENG;
