"""🧪 Motor de gasometria 360X — interpretação passo a passo (abordagem fisiológica/Boston + AG + Δ/Δ + oxigenação).

Convenções (as mesmas do app, em gaso_engine.js):
- pH por Henderson-Hasselbalch: 6,1 + log10(HCO3 / (0,03 × PaCO2)).
- Faixas: pH 7,35–7,45 · PaCO2 35–45 · HCO3 22–26 · AG 8–12 (referência 12) · albumina 4,0.
- Winter: PaCO2 esperada = 1,5 × HCO3 + 8 ± 2.   Alcalose metabólica: 0,7 × HCO3 + 21 ± 2.
- Acidose respiratória: HCO3 sobe 1 (aguda) ou 3,5 (crônica) por 10 de PaCO2.  Alcalose respiratória: cai 2 (aguda) ou 4 (crônica) por 10.
- AG corrigido = AG + 2,5 × (4 − albumina).  Δ/Δ = (AGc − 12) / (24 − HCO3): < 0,8 AG + hiperclorêmica · 0,8–2 AG pura · > 2 AG + alcalose metabólica.
- Osm calc = 2 Na + glicose/18 + ureia/6 (ureia em mg/dL).  Gap osmolar > 10 = suspeita de álcool tóxico.
- PAO2 = FiO2 × (Patm − 47) − PaCO2/0,8.  Gradiente A-a esperado em ar ambiente ≈ idade/4 + 4.  P/F = PaO2/FiO2.
"""
import math

NOME = {"AM_AG": "Acidose metabólica com ânion gap elevado", "AM_HC": "Acidose metabólica hiperclorêmica (ânion gap normal)",
        "ALM": "Alcalose metabólica", "AR_A": "Acidose respiratória aguda", "AR_C": "Acidose respiratória crônica",
        "AR_CA": "Acidose respiratória crônica agudizada", "ALR_A": "Alcalose respiratória aguda", "ALR_C": "Alcalose respiratória crônica",
        "AR": "Acidose respiratória", "ALR": "Alcalose respiratória", "NORMAL": "Equilíbrio ácido-base normal"}
ORD = ["AM_AG", "AM_HC", "ALM", "AR_A", "AR_C", "AR_CA", "AR", "ALR_A", "ALR_C", "ALR", "NORMAL"]


def f(x, d=1):
    """número em pt-BR"""
    if x is None: return "—"
    s = f"{x:.{d}f}" if d else f"{round(x):d}"
    return s.replace(".", ",")


def ph_hh(hco3, pco2):
    return 6.1 + math.log10(hco3 / (0.03 * pco2))


def sbe(ph, hco3):
    return 0.93 * (hco3 - 24.4 + 14.8 * (ph - 7.4))


def prep(lab):
    """completa o laudo: pH (HH), Cl a partir do AG-alvo, BE."""
    L = dict(lab)
    if L.get("hco3") is not None and L.get("pco2") is not None and L.get("ph") is None:
        L["ph"] = round(ph_hh(L["hco3"], L["pco2"]), 2)
    if L.get("ag") is not None and L.get("cl") is None and L.get("na") is not None:
        L["cl"] = L["na"] - L["ag"] - L["hco3"]
    L.pop("ag", None)
    if L.get("ph") is not None and L.get("hco3") is not None:
        L["be"] = round(sbe(L["ph"], L["hco3"]), 1)
    L.setdefault("fio2", 0.21 if L.get("pao2") is not None else None)
    return L


def analyze(lab):
    L = prep(lab)
    ph, pc, h = L["ph"], L["pco2"], L["hco3"]
    codes, st = [], []
    alb = L.get("alb")
    ag = agc = None
    if L.get("na") is not None and L.get("cl") is not None:
        ag = L["na"] - (L["cl"] + h)
        agc = ag + 2.5 * (4.0 - alb) if alb is not None else ag
    agHigh = agc is not None and agc > 12
    agHidden = agc is not None and agc >= 16   # sem acidose metabólica evidente, só conta AG ≥ 16 (ΔAG ≥ 4)
    R = {"lab": L, "ag": ag, "agc": agc}

    # 1) pH
    if ph < 7.35: st.append(f"pH {f(ph,2)} → <b>acidemia</b>"); side = "acid"
    elif ph > 7.45: st.append(f"pH {f(ph,2)} → <b>alcalemia</b>"); side = "alk"
    else: st.append(f"pH {f(ph,2)} → <b>dentro da faixa normal</b> (7,35–7,45): ou não há distúrbio ou há distúrbios que se anulam"); side = "nl"

    def winter():
        e = 1.5 * h + 8; R["exp"] = (e - 2, e + 2)
        s = f"Winter: 1,5 × {f(h,0)} + 8 = {f(e)} ± 2 ({f(e-2)}–{f(e+2)}); PaCO₂ {f(pc,0)} → "
        if pc > e + 2: codes.append("AR"); s += "<b>acima</b>: acidose respiratória associada"
        elif pc < e - 2: codes.append("ALR"); s += "<b>abaixo</b>: alcalose respiratória associada"
        else: s += "compensação respiratória <b>adequada</b>"
        st.append(s)

    def malk_comp():
        e = min(0.7 * h + 21, 55); R["exp"] = (e - 2, e + 2)
        s = f"PaCO₂ esperada = 0,7 × {f(h,0)} + 21 = {f(e)} ± 2 ({f(e-2)}–{f(e+2)}); PaCO₂ {f(pc,0)} → "
        if pc > e + 2: codes.append("AR"); s += "<b>acima</b>: acidose respiratória associada"
        elif pc < e - 2: codes.append("ALR"); s += "<b>abaixo</b>: alcalose respiratória associada"
        else: s += "compensação respiratória <b>adequada</b>"
        st.append(s)

    def racid():
        d = pc - 40; a, c = 24 + 0.1 * d, 24 + 0.35 * d; R["exp"] = (a, c)
        s = f"HCO₃⁻ esperado: aguda 24 + 0,1 × {f(d,0)} = {f(a)} · crônica 24 + 0,35 × {f(d,0)} = {f(c)}; HCO₃⁻ {f(h,0)} → "
        if h < a - 2: codes.append("AR"); codes.append("AM?"); s += "<b>abaixo do esperado</b>: acidose metabólica associada"
        elif h <= a + 2 and (h - a) <= (c - h): codes.append("AR_A"); s += "<b>aguda</b>"
        elif c - 2 <= h <= c + 2: codes.append("AR_C"); s += "<b>crônica</b> (compensada pelo rim)"
        elif h > c + 2: codes.append("AR"); codes.append("ALM"); s += "<b>acima do esperado</b>: alcalose metabólica associada"
        else: codes.append("AR_CA"); s += "<b>entre aguda e crônica</b>: crônica agudizada"
        st.append(s)

    def ralk():
        d = 40 - pc; a, c = 24 - 0.2 * d, 24 - 0.4 * d; R["exp"] = (c, a)
        s = f"HCO₃⁻ esperado: aguda 24 − 0,2 × {f(d,0)} = {f(a)} · crônica 24 − 0,4 × {f(d,0)} = {f(c)}; HCO₃⁻ {f(h,0)} → "
        if h > a + 2: codes.append("ALR"); codes.append("ALM"); s += "<b>acima do esperado</b>: alcalose metabólica associada"
        elif h >= a - 2 and (a - h) <= (h - c): codes.append("ALR_A"); s += "<b>aguda</b>"
        elif c - 2 <= h <= c + 2: codes.append("ALR_C"); s += "<b>crônica</b> (compensada pelo rim)"
        elif h < c - 2: codes.append("ALR"); codes.append("AM?"); s += "<b>abaixo do esperado</b>: acidose metabólica associada"
        else: codes.append("ALR_C"); s += "em compensação (subaguda)"
        st.append(s)

    # 2–3) distúrbio primário + compensação
    R["side"] = side; R["prim"] = "NL"
    if side == "acid":
        if h < 22:
            st.append(f"HCO₃⁻ {f(h,0)} ↓ → distúrbio primário <b>metabólico</b> (acidose metabólica)"); codes.append("AM?"); R["prim"] = "AM"; winter()
        else:
            st.append(f"PaCO₂ {f(pc,0)} ↑ → distúrbio primário <b>respiratório</b> (acidose respiratória)"); R["prim"] = "AR"; racid()
    elif side == "alk":
        if h > 26:
            st.append(f"HCO₃⁻ {f(h,0)} ↑ → distúrbio primário <b>metabólico</b> (alcalose metabólica)"); codes.append("ALM"); R["prim"] = "ALM"; malk_comp()
        else:
            st.append(f"PaCO₂ {f(pc,0)} ↓ → distúrbio primário <b>respiratório</b> (alcalose respiratória)"); R["prim"] = "ALR"; ralk()
    else:
        if 22 <= h <= 26 and 35 <= pc <= 45:
            st.append("PaCO₂ e HCO₃⁻ normais → sem distúrbio respiratório; olhar o AG (acidose oculta?)")
        elif (h < 22 and pc > 45) or (h > 26 and pc < 35):
            st.append("HCO₃⁻ e PaCO₂ em sentidos opostos com pH normal → distúrbios opostos que se anulam")
            codes += ["AM?", "AR"] if h < 22 else ["ALM", "ALR"]
        elif h < 22 and (ph < 7.40 or agHidden or pc >= 35):
            st.append(f"HCO₃⁻ {f(h,0)} ↓ com pH no lado ácido (ou AG alto) → acidose metabólica; checar compensação"); codes.append("AM?"); winter()
        elif pc < 35:
            st.append(f"PaCO₂ {f(pc,0)} ↓ com pH no lado alcalino → alcalose respiratória; checar compensação"); ralk()
        elif h > 26 and (ph >= 7.40 or pc <= 45):
            st.append(f"HCO₃⁻ {f(h,0)} ↑ com pH no lado alcalino → alcalose metabólica; checar compensação"); codes.append("ALM"); malk_comp()
        elif pc > 45:
            st.append(f"PaCO₂ {f(pc,0)} ↑ com pH no lado ácido → acidose respiratória; checar compensação"); racid()
        else:
            st.append("Valores praticamente normais")

    # 4) ânion gap + Δ/Δ
    if ag is not None:
        s = f"AG = {f(L['na'],0)} − ({f(L['cl'],0)} + {f(h,0)}) = {f(ag,0)}"
        if alb is not None and alb != 4.0: s += f"; corrigido pela albumina {f(alb)}: {f(ag,0)} + 2,5 × (4 − {f(alb)}) = <b>{f(agc)}</b>"
        amet = "AM?" in codes
        s += " → " + ("<b>elevado</b>" if (agHigh if amet else agHidden) else ("limítrofe (13–15: sem valor isolado)" if agHigh else "normal"))
        st.append(s)
    if "AM?" in codes:
        codes.remove("AM?")
        codes.append("AM_AG" if agHigh else "AM_HC")
    elif not agHidden: agHigh = False
    if agHigh:
        if "AM_AG" not in codes: codes.append("AM_AG")
        if h < 24:
            dd = (agc - 12) / (24 - h); R["dd"] = dd
            s = f"Δ/Δ = ({f(agc)} − 12) / (24 − {f(h,0)}) = <b>{f(dd)}</b> → "
            if dd < 0.8: s += "&lt; 0,8: acidose hiperclorêmica associada"; codes.append("AM_HC")
            elif dd > 2: s += "&gt; 2: alcalose metabólica associada"; codes.append("ALM")
            else: s += "0,8–2: acidose com AG elevado <b>pura</b>"
            st.append(s)
        else:
            hc = h + (agc - 12); R["hco3c"] = hc
            st.append(f"AG elevado com HCO₃⁻ ≥ 24: HCO₃⁻ corrigido = {f(h,0)} + ({f(agc)} − 12) = {f(hc)} → acidose com AG <b>mascarada</b>" + (" por alcalose metabólica" if hc > 26 else ""))
            if hc > 26 and "ALM" not in codes: codes.append("ALM")
    # distúrbio respiratório + metabólico concomitante → rótulo respiratório genérico (aguda/crônica perde sentido)
    if any(c in codes for c in ("AM_AG", "AM_HC", "ALM")):
        codes = ["AR" if c in ("AR_A", "AR_C", "AR_CA") else "ALR" if c in ("ALR_A", "ALR_C") else c for c in codes]
    if not codes: codes.append("NORMAL")
    codes = list(dict.fromkeys(codes))
    if "NORMAL" in codes and len(codes) > 1: codes.remove("NORMAL")

    # 5) gap osmolar, AG urinário, cloro urinário
    if L.get("osm") is not None and L.get("glic") is not None and L.get("ureia") is not None:
        oc = 2 * L["na"] + L["glic"] / 18 + L["ureia"] / 6; gap = L["osm"] - oc; R["ogap"] = gap
        st.append(f"Osm calculada = 2 × {f(L['na'],0)} + {f(L['glic'],0)}/18 + {f(L['ureia'],0)}/6 = {f(oc)}; gap osmolar = {f(L['osm'],0)} − {f(oc)} = <b>{f(gap)}</b> → " + ("<b>elevado</b> (&gt; 10): álcool tóxico?" if gap > 10 else "normal"))
    if L.get("una") is not None and L.get("uk") is not None and L.get("ucl") is not None:
        u = L["una"] + L["uk"] - L["ucl"]; R["uag"] = u
        st.append(f"AG urinário = {f(L['una'],0)} + {f(L['uk'],0)} − {f(L['ucl'],0)} = <b>{f(u,0)}</b> → " + ("negativo: NH₄⁺ urinário preservado (perda GI)" if u < 0 else "positivo: falha de excreção de NH₄⁺ (ATR distal)"))
    elif L.get("ucl") is not None and "ALM" in codes:
        u = L["ucl"]
        st.append(f"Cloro urinário {f(u,0)} mEq/L → " + ("&lt; 20: <b>responsiva a cloreto</b> (volume/cloro)" if u < 20 else "&gt; 40: <b>resistente a cloreto</b>" if u > 40 else "intermediário"))

    # 6) oxigenação
    if L.get("pao2") is not None:
        fi, pa = L.get("fio2") or 0.21, L["pao2"]; patm = L.get("patm", 760)
        PA = fi * (patm - 47) - pc / 0.8; aa = PA - pa; pf = pa / fi; R.update(PA=PA, aa=aa, pf=pf)
        if fi <= 0.21 + 1e-6:
            ex = (L.get("idade") or 40) / 4 + 4; R["aa_exp"] = ex
            s = f"PAO₂ = 0,21 × ({f(patm,0)} − 47) − {f(pc,0)}/0,8 = {f(PA)}; A-a = {f(PA)} − {f(pa,0)} = <b>{f(aa)}</b> (esperado ≈ {f(ex)})"
            if pa < 80: s += " → hipoxemia " + ("com A-a <b>normal</b>: hipoventilação (ou PiO₂ baixa)" if aa <= ex + 2 else "com A-a <b>elevado</b>: V/Q, shunt ou difusão")
            else: s += " → oxigenação adequada"
        else:
            s = f"P/F = {f(pa,0)}/{f(fi,2)} = <b>{f(pf,0)}</b>"
            s += " → " + ("hipoxemia grave (≤ 100)" if pf <= 100 else "hipoxemia moderada (101–200)" if pf <= 200 else "hipoxemia leve (201–300)" if pf <= 300 else "&gt; 300")
            s += f"; PAO₂ {f(PA,0)}, A-a {f(aa,0)}"
        st.append(s)

    R["codes"] = sorted(codes, key=ORD.index)
    R["steps"] = st
    R["dx"] = " + ".join(NOME[c] for c in R["codes"])
    return R


# ---------- laudo HTML (frente do card / enunciado) ----------
def panel(lab, titulo=None):
    L = prep(lab)
    tipo = L.get("tipo", "arterial")
    fi = L.get("fio2")
    hd = titulo or ("🩸 Gasometria " + tipo + (f" · FiO₂ {round(fi*100)}%" if fi else "") + (f" · PEEP {L['peep']}" if L.get("peep") else ""))
    rows = [("pH", L.get("ph"), "", 2), ("PaCO₂" if tipo == "arterial" else "PvCO₂", L.get("pco2"), "mmHg", 0), ("HCO₃⁻", L.get("hco3"), "mEq/L", 0), ("BE", L.get("be"), "mEq/L", 1),
            ("PaO₂" if tipo == "arterial" else "PvO₂", L.get("pao2"), "mmHg", 0), ("SatO₂", L.get("sat"), "%", 0),
            ("Na⁺", L.get("na"), "mEq/L", 0), ("K⁺", L.get("k"), "mEq/L", 1), ("Cl⁻", L.get("cl"), "mEq/L", 0), ("Albumina", L.get("alb"), "g/dL", 1),
            ("Lactato", L.get("lac"), "mmol/L", 1), ("Glicose", L.get("glic"), "mg/dL", 0), ("Ureia", L.get("ureia"), "mg/dL", 0), ("Creatinina", L.get("cr"), "mg/dL", 1),
            ("Osm medida", L.get("osm"), "mOsm/kg", 0), ("β-OH-butirato", L.get("cet"), "mmol/L", 1), ("Hb", L.get("hb"), "g/dL", 1),
            ("COHb", L.get("cohb"), "%", 0), ("MetHb", L.get("methb"), "%", 0), ("SvcO₂", L.get("svo2"), "%", 0),
            ("Na urinário", L.get("una"), "mEq/L", 0), ("K urinário", L.get("uk"), "mEq/L", 0), ("Cl urinário", L.get("ucl"), "mEq/L", 0)]
    cells = [(n, f(v, d), u) for n, v, u, d in rows if v is not None]
    td = "padding:3px 7px;border:1px solid rgba(128,128,128,.35)"
    out = [f'<table class="gaso" style="border-collapse:collapse;margin:8px 0 4px;font-size:15px;line-height:1.35">',
           f'<tr><th colspan="4" style="{td};text-align:left;background:rgba(77,212,255,.13)">{hd}</th></tr>']
    for i in range(0, len(cells), 2):
        pair = cells[i:i + 2]
        tds = "".join(f'<td style="{td}">{n}</td><td style="{td}"><b>{v}</b> <small>{u}</small></td>' for n, v, u in pair)
        if len(pair) == 1: tds += f'<td style="{td}"></td><td style="{td}"></td>'
        out.append(f"<tr>{tds}</tr>")
    out.append("</table>")
    return "".join(out)


if __name__ == "__main__":
    T = [  # (lab, esperado) — exemplos clássicos
        (dict(pco2=24, hco3=10, na=140, cl=100, alb=4.0), {"AM_AG"}),                 # CAD: Winter 23 ±2, AG 30, Δ/Δ 1,3
        (dict(pco2=30, hco3=18, na=140, cl=112), {"AM_HC"}),                           # diarreia: Winter 35 ± 2 → 30 < 33 → +ALR
        (dict(pco2=48, hco3=34, na=140, cl=92), {"ALM"}),                              # vômitos: 0,7×34+21=44,8 ±2 → 48 > 46,8 → +AR
        (dict(pco2=60, hco3=26, na=140, cl=104), {"AR_A"}),
        (dict(pco2=60, hco3=31, na=140, cl=98), {"AR_C"}),
        (dict(pco2=25, hco3=21, na=140, cl=108), {"ALR_A"}),
        (dict(pco2=25, hco3=18, na=140, cl=110), {"ALR_C"}),
        (dict(pco2=20, hco3=12, na=140, cl=100), {"AM_AG", "ALR"}),                   # salicilato
        (dict(pco2=40, hco3=24, na=140, cl=96), {"AM_AG", "ALM"}),                    # pH normal, AG 20
        (dict(pco2=55, hco3=12, na=140, cl=104, alb=4), {"AM_AG", "AR"}),             # PCR
    ]
    T[1] = (dict(pco2=34, hco3=18, na=140, cl=112), {"AM_HC"})
    T[2] = (dict(pco2=45, hco3=34, na=140, cl=94), {"ALM"})
    ok = 0
    for lab, exp in T:
        r = analyze(lab); g = set(r["codes"]); ok += g == exp
        print("✅" if g == exp else "❌", r["lab"]["ph"], sorted(g), "esperado", sorted(exp), "|", r["dx"])
    print(ok, "/", len(T))
