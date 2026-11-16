"""50 questões geradas a partir do motor: 25 de diagnóstico ácido-base + 25 de cálculo. Alternativas e 'porquê' derivados dos números."""
import random, re
from gaso_engine import analyze, panel, NOME, f

TEMA = {1: "Método e fórmulas", 2: "Acidose com AG elevado", 3: "Acidose hiperclorêmica", 4: "Alcalose metabólica", 5: "Acidose respiratória",
        6: "Alcalose respiratória", 7: "Distúrbios mistos", 8: "Oxigenação", 9: "Gaps e cálculos", 10: "Casos de UTI"}
strip = lambda s: re.sub(r"<[^>]+>", "", s)


def label(codes):
    order = ["AM_AG", "AM_HC", "ALM", "AR_A", "AR_C", "AR_CA", "AR", "ALR_A", "ALR_C", "ALR", "NORMAL"]
    return " + ".join(NOME[c] for c in sorted(set(codes), key=order.index))


def why(R, code, present):
    L = R["lab"]; h, pc = L["hco3"], L["pco2"]; agc = R.get("agc"); dd = R.get("dd"); ex = R.get("exp")
    if code == "AM_AG":
        return f"AG corrigido = {f(agc)} ({'&gt; 12: elevado' if present else 'normal: não há acidose com AG alto'})"
    if code == "AM_HC":
        if present: return f"HCO₃⁻ baixo sem AG que o explique ({'Δ/Δ ' + f(dd) + ' &lt; 0,8' if dd is not None else 'AG ' + f(agc) + ' normal'})"
        return "não há componente hiperclorêmico" + (f" (Δ/Δ {f(dd)} ≥ 0,8)" if dd is not None else "")
    if code == "ALM":
        if present: return ("Δ/Δ " + f(dd) + " &gt; 2" if dd and dd > 2 else f"HCO₃⁻ corrigido = {f(R['hco3c'])} (&gt; 26)" if R.get("hco3c") else f"HCO₃⁻ {f(h,0)} acima do esperado")
        return "HCO₃⁻ não está acima do esperado" + (f" (Δ/Δ {f(dd)} ≤ 2)" if dd is not None else "")
    if code in ("AR", "ALR"):
        if R["prim"] in ("AR", "ALR"):
            return f"PaCO₂ {f(pc,0)} {'alta' if code == 'AR' else 'baixa'} — distúrbio respiratório primário" if present else f"PaCO₂ {f(pc,0)} não indica {NOME[code].lower()}"
        if ex and R["prim"] in ("AM", "ALM", "NL"):
            return f"PaCO₂ {f(pc,0)} {'fora' if present else 'dentro'} da faixa esperada ({f(ex[0])}–{f(ex[1])})"
        return f"PaCO₂ {f(pc,0)} {'alterada' if present else 'compatível'}"
    if code.startswith(("AR_", "ALR_")):
        if ex: return f"HCO₃⁻ {f(h,0)} × esperado agudo/crônico ({f(min(ex))}–{f(max(ex))})"
        return f"HCO₃⁻ {f(h,0)}"
    if code == "NORMAL":
        return "há distúrbio identificável" if not present else "pH, PaCO₂, HCO₃⁻ e AG normais"
    return ""


def variants(codes, R):
    T = set(codes); out = []
    def add(s):
        s = set(s) - {""}
        if "NORMAL" in s and len(s) > 1: return
        if s and s != T and label(s) not in [label(x) for x in out]: out.append(s)
    sw = {"AM_AG": "AM_HC", "AM_HC": "AM_AG", "AR_A": "AR_C", "AR_C": "AR_A", "AR_CA": "AR_A", "ALR_A": "ALR_C", "ALR_C": "ALR_A"}
    for c in list(T):
        if c in sw: add(T - {c} | {sw[c]})
    for c in ("AR", "ALR", "ALM", "AM_HC"):
        if c in T: add(T - {c})
    if R["prim"] in ("AM", "ALM", "NL") and not ({"AR", "ALR"} & T): add(T | {"ALR"}); add(T | {"AR"})
    if "AM_AG" in T and "ALM" not in T: add(T | {"ALM"})
    if "AR_CA" in T: add({"AR_C"}); add({"AR", "ALM"})
    if "ALR_A" in T: add({"AM_HC", "ALR"})
    if T == {"NORMAL"}: out.clear(); add({"AR_A"}); add({"ALR_A"}); add({"AM_HC", "ALR"}); add({"AM_AG", "ALM"})
    pool = [{"AM_AG"}, {"AM_HC"}, {"ALM"}, {"AR_A"}, {"AR_C"}, {"ALR_A"}, {"ALR_C"}, {"AM_AG", "ALR"}, {"AM_AG", "AR"}, {"ALM", "AR"}, {"NORMAL"}]
    for s in pool: add(s)
    return out


def q_dx(qid, t, ctx, lab, exp, pega, rnd):
    R = analyze(lab); assert set(R["codes"]) == set(exp.split("+")), (qid, R["codes"], exp)
    corr = label(R["codes"]); V = variants(R["codes"], R)[:4]
    alts = [corr] + [label(v) for v in V]; rnd.shuffle(alts); gab = alts.index(corr)
    T = set(R["codes"]); por = []
    for a in alts:
        if a == corr:
            s = " → ".join(strip(x) for x in R["steps"][2:]) or strip(R["steps"][-1])
            por.append("Correta: " + (s if len(s) <= 330 else s[:327].rsplit(" ", 1)[0] + "…")); continue
        v = next(x for x in V if label(x) == a)
        fam = lambda c: "AR" if c.startswith("AR") else "ALR" if c.startswith("ALR") else c
        falt = sorted(c for c in T - v if not (c in ("AR", "ALR") and any(fam(x) == c for x in v)))
        sobra = sorted(c for c in v - T if not (c in ("AR", "ALR") and any(fam(x) == c for x in T)))
        if T == {"NORMAL"}:
            L_ = R["lab"]; por.append(f"Incorreta: pH {f(L_['ph'],2)}, PaCO₂ {f(L_['pco2'],0)}, HCO₃⁻ {f(L_['hco3'],0)} e AG {f(R['agc'],0)} estão normais — não há distúrbio ácido-base laboratorial (o alerta aqui é clínico)."); continue
        msg = []
        resp = ("AR_A", "AR_C", "AR_CA", "ALR_A", "ALR_C")
        if len(falt) == 1 and len(sobra) == 1 and falt[0] in resp and sobra[0] in resp and R.get("exp"):
            a_, c_ = R["exp"] if falt[0].startswith("AR") else R["exp"][::-1]
            por.append(f"Incorreta: HCO₃⁻ {f(R['lab']['hco3'],0)} × esperado agudo {f(a_)} e crônico {f(c_)} → o correto é {NOME[falt[0]].lower()}."); continue
        if falt: msg.append("deixa de fora " + ", ".join(NOME[c].lower() for c in falt) + ": " + "; ".join(why(R, c, True) for c in falt))
        if sobra: msg.append("inclui " + ", ".join(NOME[c].lower() for c in sobra) + " indevidamente: " + "; ".join(why(R, c, False) for c in sobra))
        por.append(("Incorreta: " + " · ".join(msg))[:400])
    com = "<b>Passo a passo:</b><br>" + "<br>".join(R["steps"])
    return dict(id=qid, tema=TEMA[t], enun=f"{ctx}{panel(lab)}Qual a interpretação ácido-base correta?", alts=alts, gab=gab, com=com, porque=por, pega=pega)


def q_num(qid, t, enun, corr, wrongs, com, pega, rnd):
    """wrongs: lista de (texto_alternativa, motivo)"""
    alts = [corr] + [w for w, _ in wrongs]; assert len(set(alts)) == 5, (qid, alts)
    mot = {w: m for w, m in wrongs}
    rnd.shuffle(alts); gab = alts.index(corr)
    por = ["Correta: " + strip(com)[:300] if a == corr else "Incorreta: " + mot[a] for a in alts]
    return dict(id=qid, tema=TEMA[t], enun=enun, alts=alts, gab=gab, com=com, porque=por, pega=pega)


DX = [
 (3, "Homem, 35 anos, 4 dias de diarreia aquosa volumosa, sem febre, desidratado.", dict(pco2=30, hco3=15, na=137, k=3.0, ag=9), "AM_HC", "Diarreia = perda de HCO₃⁻ → AG normal (hiperclorêmica)."),
 (2, "DM1, 21 anos, poliúria, vômitos e hálito cetônico; FR 30.", dict(pco2=22, hco3=9, na=133, k=5.1, ag=27, glic=480), "AM_AG", "CAD costuma ter Δ/Δ próximo de 1."),
 (2, "Idoso com pneumonia, PA 80/50, extremidades frias, FR 34.", dict(pco2=22, hco3=14, na=138, ag=24, lac=6.5), "AM_AG+ALR", "Na sepse, PaCO₂ abaixo do Winter é comum (hiperventilação)."),
 (5, "DPOC, PaCO₂ basal desconhecida, 3 dias de piora da dispneia e escarro purulento.", dict(pco2=70, hco3=30, na=139, ag=10), "AR_CA", "HCO₃⁻ entre o esperado agudo e crônico = crônica agudizada."),
 (5, "Encontrado sonolento após uso de heroína; FR 6.", dict(pco2=65, hco3=26, na=140, ag=10), "AR_A", "Aguda: HCO₃⁻ sobe só 1 por 10 de PaCO₂."),
 (4, "Úlcera péptica, vômitos alimentares há 1 semana.", dict(pco2=46, hco3=36, na=135, k=2.7, ag=11), "ALM", "Compensação da alcalose: 0,7 × HCO₃⁻ + 21."),
 (6, "Jovem com crise de ansiedade, parestesias periorais; pulmões limpos.", dict(pco2=26, hco3=21, na=140, ag=10), "ALR_A", "Aguda: HCO₃⁻ cai 2 por 10 de PaCO₂."),
 (6, "Gestante, 32 semanas, assintomática, gasometria de rotina.", dict(pco2=30, hco3=20, na=137, ag=9), "ALR_C", "Gestação: alcalose respiratória crônica fisiológica."),
 (7, "DM1 com CAD que vomitou 'o dia inteiro' por 3 dias.", dict(pco2=37, hco3=20, na=133, k=3.6, ag=30, glic=500), "AM_AG+ALM", "Δ/Δ muito &gt; 2 com HCO₃⁻ quase normal = vômitos escondendo a CAD."),
 (7, "Recém-recuperado de PCR, ventilação irregular com bolsa.", dict(pco2=50, hco3=15, na=140, ag=25, lac=9), "AM_AG+AR", "Acidose dupla: a forma mais rápida de corrigir o pH é ventilar."),
 (7, "DM1 em CAD após 5 dias de diarreia.", dict(pco2=23, hco3=10, na=136, ag=17, glic=390), "AM_AG+AM_HC", "Δ/Δ &lt; 0,8 = acidose hiperclorêmica associada."),
 (7, "Mulher ingeriu grande quantidade de AAS; zumbido, FR 32. pH 'normal'.", dict(pco2=20, hco3=12, na=140, ag=24), "AM_AG+ALR", "pH normal com HCO₃⁻ e PaCO₂ muito baixos = dois distúrbios."),
 (4, "DPOC em furosemida alta, sonolento.", dict(pco2=60, hco3=42, na=134, k=2.9, ag=10), "ALM+AR", "HCO₃⁻ 42 excede a compensação de qualquer hipercapnia crônica de 60 (~31)."),
 (6, "Cirrótico Child C estável, sem infecção.", dict(pco2=25, hco3=18, na=131, ag=9), "ALR_C", "Cirrose: alcalose respiratória crônica (marcador de gravidade)."),
 (3, "DM2 com nefropatia, K⁺ 6,3 recorrente, sem IECA.", dict(pco2=34, hco3=18, na=137, k=6.3, ag=10), "AM_HC", "ATR 4 é a única ATR com hipercalemia."),
 (5, "Obeso IMC 50, sonolência diurna, cefaleia matinal, sem DPOC.", dict(pco2=56, hco3=30, na=140, ag=10), "AR_C", "Obesidade-hipoventilação: HCO₃⁻ ≥ 27 é boa pista."),
 (4, "Gestante de 8 semanas com vômitos incoercíveis.", dict(pco2=32, hco3=30, na=134, k=3.0, ag=11), "ALM+ALR", "Na gestação a PaCO₂ basal já é ~30."),
 (7, "Cirrótico com vômitos e IRA; albumina 2,5.", dict(pco2=30, hco3=24, na=132, ag=22, alb=2.5), "AM_AG+ALM+ALR", "Distúrbio triplo: só com uma alteração respiratória."),
 (5, "Asma grave há 6 h, cansada; 'gasometria normal'.", dict(pco2=42, hco3=24, na=140, ag=10), "NORMAL", "Na crise de asma, PaCO₂ normal é sinal de fadiga."),
 (2, "DM2 em metformina, diarreia e oligúria; lactato 14.", dict(pco2=23, hco3=10, na=136, ag=28, lac=14), "AM_AG", "MALA: hemodiálise remove metformina e corrige a acidose."),
 (3, "Trauma ressuscitado com 9 L de SF; lactato 3.", dict(pco2=29, hco3=14, na=145, ag=16, lac=3), "AM_AG+AM_HC", "Grande parte da acidose pós-SF é cloreto, não hipoperfusão."),
 (5, "Asma quase fatal, silêncio auscultatório.", dict(pco2=58, hco3=26, na=139, ag=10), "AR_A", "IOT: FR baixa e Te longo; aceitar hipercapnia."),
 (4, "DPOC (PaCO₂ basal 60) intubado e ventilado para PaCO₂ 38.", dict(pco2=38, hco3=34, na=139, ag=11), "ALM+ALR", "Alvo da VM no DPOC crônico: pH, não PaCO₂ 40."),
 (7, "Miastenia em crise + diarreia por piridostigmina.", dict(pco2=40, hco3=16, na=139, ag=10), "AM_HC+AR", "PaCO₂ 'normal' na acidose metabólica = falência respiratória."),
 (7, "DRC 4 com vômitos; gasometria quase normal.", dict(pco2=40, hco3=25, na=138, ag=26), "AM_AG+ALM", "AG alto com HCO₃⁻ normal = acidose escondida por alcalose."),
]


def build(rnd):
    Q = []
    for i, (t, ctx, lab, exp, pega) in enumerate(DX, 1):
        Q.append(q_dx(f"QG{len(Q)+1:03d}", t, ctx, lab, exp, pega, rnd))
    # ---------- cálculos ----------
    def winter_q(h, ctx):
        e = 1.5 * h + 8; r = lambda c: f"{f(c-2)} a {f(c+2)} mmHg"
        w = [(r(0.7 * h + 21), "usou a fórmula da ALCALOSE metabólica (0,7 × HCO₃⁻ + 21)."),
             ("38 a 42 mmHg", "considerou que a compensação 'normaliza' a PaCO₂ — ela deve CAIR na acidose metabólica."),
             (r(1.5 * h), "esqueceu o +8 da fórmula de Winter."),
             (r(h + 15 + 10), "usou HCO₃⁻ + 15 (atalho da alcalose metabólica) com erro de soma.")]
        return q_num(f"QG{len(Q)+1:03d}", 1, f"{ctx} HCO₃⁻ = {f(h,0)} mEq/L. Qual a PaCO₂ esperada pela compensação respiratória?",
                     r(e), w, f"Winter: 1,5 × {f(h,0)} + 8 = {f(e)} ± 2 → {r(e)}. Fora dessa faixa há distúrbio respiratório associado.",
                     "Atalho: PaCO₂ ≈ dois últimos dígitos do pH (pH 7,2x → PaCO₂ ≈ 2x).", rnd)
    for h, ctx in [(8, "Cetoacidose diabética grave."), (12, "Acidose láctica por choque séptico."), (15, "Diarreia aguda com acidose."), (18, "Acidose da DRC."), (6, "Intoxicação por metanol.")]:
        Q.append(winter_q(h, ctx))

    def ag_q(t, ctx, na, cl, h, alb):
        ag = na - cl - h; agc = ag + 2.5 * (4 - alb)
        w = [(f(ag), "é o AG sem correção — a hipoalbuminemia esconde ânions não medidos."),
             (f(ag - 2.5 * (4 - alb)), "subtraiu a correção (o AG corrigido é MAIOR quando a albumina é baixa)."),
             (f(ag + (4 - alb)), "usou fator 1 em vez de 2,5 por g/dL de albumina."),
             (f(agc + 4), "somou o K⁺ à fórmula e manteve a referência de 12.")]
        return q_num(f"QG{len(Q)+1:03d}", t, f"{ctx} Na⁺ {na}, Cl⁻ {cl}, HCO₃⁻ {h}, albumina {f(alb)} g/dL. Qual o ânion gap corrigido pela albumina?",
                     f(agc), w, f"AG = {na} − ({cl} + {h}) = {f(ag,0)}; corrigido = {f(ag,0)} + 2,5 × (4 − {f(alb)}) = <b>{f(agc)}</b>.",
                     "Na UTI, AG 'normal' com albumina baixa é armadilha clássica.", rnd)
    for args in [(1, "Paciente séptico em UTI.", 138, 108, 18, 2.0), (9, "Cirrótico com IRA.", 132, 101, 20, 1.8), (2, "Nefrótico com sepse.", 135, 104, 19, 1.6), (10, "Pós-operatório prolongado, desnutrido.", 140, 110, 17, 2.4)]:
        Q.append(ag_q(*args))

    def og_q(ctx, na, glic, ureia, osm):
        oc = 2 * na + glic / 18 + ureia / 6; gap = osm - oc
        w = [(f(osm - (2 * na + glic / 18 + ureia / 2.8)), "dividiu a UREIA por 2,8 (esse divisor é para o BUN)."),
             (f(osm - (2 * na + ureia / 6)), "esqueceu a glicose no cálculo."),
             (f(osm - (na + glic / 18 + ureia / 6)), "usou Na⁺ em vez de 2 × Na⁺."),
             (f(oc), "este é a osmolalidade CALCULADA, não o gap.")]
        return q_num(f"QG{len(Q)+1:03d}", 9, f"{ctx} Na⁺ {na}, glicose {glic}, ureia {ureia} mg/dL, osmolalidade medida {osm} mOsm/kg. Qual o gap osmolar?",
                     f(gap), w, f"Osm calc = 2 × {na} + {glic}/18 + {ureia}/6 = {f(oc)}; gap = {osm} − {f(oc)} = <b>{f(gap)}</b>" + (" → elevado (&gt; 10): álcool tóxico?" if gap > 10 else " → normal."),
                     "Gap osmolar alto + AG alto = metanol/etilenoglicol até prova em contrário.", rnd)
    for args in [("Ingestão de 'cachaça adulterada'.", 140, 110, 36, 335), ("Tentativa de suicídio com anticongelante.", 138, 120, 54, 318), ("Etilista confuso, sem acidose.", 141, 95, 30, 312)]:
        Q.append(og_q(*args))

    def aa_q(ctx, pco2, pao2, idade, patm=760):
        PA = 0.21 * (patm - 47) - pco2 / 0.8; aa = PA - pao2; ex = idade / 4 + 4
        w = [(f(150 - pao2), "usou PAO₂ fixa de 150 (esqueceu de descontar PaCO₂/0,8)."),
             (f(0.21 * patm - pco2 / 0.8 - pao2), "não descontou a pressão de vapor d'água (47 mmHg)."),
             (f(0.21 * (patm - 47) - pco2 * 0.8 - pao2), "multiplicou a PaCO₂ por 0,8 em vez de dividir."),
             (f(PA), "esse é a PAO₂ (alveolar), não o gradiente.")]
        return q_num(f"QG{len(Q)+1:03d}", 8, f"{ctx} Ar ambiente, Patm {patm} mmHg, idade {idade} anos: PaCO₂ {pco2}, PaO₂ {pao2}. Qual o gradiente alvéolo-arterial?",
                     f(aa), w, f"PAO₂ = 0,21 × ({patm} − 47) − {pco2}/0,8 = {f(PA)}; A-a = {f(PA)} − {pao2} = <b>{f(aa)}</b> (esperado ≈ {f(ex)}) → " + ("elevado: V/Q, shunt ou difusão." if aa > ex + 2 else "normal: hipoventilação/PiO₂ baixa."),
                     "A-a normal com hipoxemia: hipoventilação ou altitude; A-a alto: doença pulmonar/shunt.", rnd)
    for args in [("Overdose de opioide.", 70, 55, 30), ("Pneumonia lobar.", 32, 58, 60), ("Suspeita de TEP.", 30, 65, 45), ("Turista em altitude (Patm 520).", 30, 56, 30, 520)]:
        Q.append(aa_q(*args))

    def pf_q(ctx, pao2, fio2, peep):
        pf = pao2 / fio2; cl = "grave (≤ 100)" if pf <= 100 else "moderada (101–200)" if pf <= 200 else "leve (201–300)" if pf <= 300 else "não preenche (&gt; 300)"
        corr = f"P/F {f(pf,0)} — SDRA {cl}"
        others = [x for x in ["grave (≤ 100)", "moderada (101–200)", "leve (201–300)"] if x != cl]
        w = [(f"P/F {f(pao2/(fio2*100),1)} — SDRA grave (≤ 100)", "usou a FiO₂ em porcentagem (×100) no denominador."),
             (f"P/F {f(pf,0)} — SDRA {others[0]}", "o número está certo, mas a faixa de Berlim não."),
             (f"P/F {f(pf,0)} — SDRA {others[1]}", "o número está certo, mas a faixa de Berlim não."),
             (f"P/F {f(pao2/0.21,0)} — não preenche (&gt; 300)", "dividiu pela FiO₂ do ar ambiente, ignorando a FiO₂ real.")]
        return q_num(f"QG{len(Q)+1:03d}", 8, f"{ctx} VM com PEEP {peep}, FiO₂ {round(fio2*100)}%, PaO₂ {pao2}, infiltrado bilateral sem IC. Qual a relação P/F e a classificação de Berlim?",
                     corr, w, f"P/F = {pao2}/{f(fio2,2)} = <b>{f(pf,0)}</b> → SDRA {cl} (com PEEP ≥ 5).", "Sem PEEP/CPAP ≥ 5, não se classifica por Berlim.", rnd)
    Q.append(pf_q("Pneumonia grave.", 84, 0.6, 10)); Q.append(pf_q("Pancreatite grave.", 76, 0.9, 14))

    def resp_q(t, ctx, pco2, cron):
        d = pco2 - 40; a = 24 + 0.1 * d; c = 24 + 0.35 * d; corr = f(c if cron else a)
        w = [(f(a if cron else c), "usou a regra da forma " + ("aguda" if cron else "crônica") + "."),
             (f(24 + d), "somou 1 por 1 mmHg (exagero; a regra é por 10)."), ("24", "não considerou compensação."),
             (f(24 - (0.35 if cron else 0.1) * d), "subtraiu em vez de somar (regra da alcalose respiratória).")]
        return q_num(f"QG{len(Q)+1:03d}", t, f"{ctx} PaCO₂ {pco2} mmHg, distúrbio {'crônico' if cron else 'agudo'} isolado. Qual o HCO₃⁻ esperado?",
                     corr, w, f"{'Crônica' if cron else 'Aguda'}: 24 + {'0,35' if cron else '0,1'} × ({pco2} − 40) = <b>{corr}</b>.", "Valor entre o agudo e o crônico = crônica agudizada.", rnd)
    Q.append(resp_q(5, "DPOC estável.", 60, True)); Q.append(resp_q(5, "Overdose de benzodiazepínico.", 70, False))

    Q.append(q_num(f"QG{len(Q)+1:03d}", 1, "Sem calculadora: PaCO₂ 50 mmHg e HCO₃⁻ 20 mEq/L. Qual o pH aproximado?", "7,22",
                   [("7,32", "errou o [H⁺] (24 × 50/20 = 60, não 48)."), ("7,12", "subtraiu 0,01 a mais por nEq."), ("7,40", "ignorou a acidose (o pH não é 'normal')."), ("7,28", "estimou sem a equação de Henderson.")],
                   "[H⁺] = 24 × PaCO₂/HCO₃⁻ = 24 × 50/20 = 60 nEq/L → pH ≈ 7,80 − 0,60 = <b>7,22</b> (HH: 6,1 + log(20/1,5) = 7,22).", "40 nEq/L = 7,40; cada 1 nEq ≈ 0,01 de pH na faixa 7,20–7,50.", rnd))
    Q.append(q_num(f"QG{len(Q)+1:03d}", 9, "Acidose com Na⁺ 140, Cl⁻ 100, HCO₃⁻ 12, albumina 4. Qual o Δ/Δ e o significado?", "≈ 1,3 — acidose com AG elevado pura",
                   [("≈ 0,75 — AG alto + acidose hiperclorêmica", "inverteu a fração: (24 − HCO₃⁻)/(AG − 12)."), ("≈ 2,3 — AG alto + alcalose metabólica", "usou o AG inteiro (28) no numerador, sem descontar o normal (12)."),
                    ("≈ 1,3 — AG alto + alcalose metabólica", "o valor está certo, mas 0,8–2 indica acidose com AG pura."), ("≈ 1,3 — sem acidose com AG elevado", "AG 28 é claramente elevado.")],
                   "AG = 140 − (100 + 12) = 28; Δ/Δ = (28 − 12)/(24 − 12) = 16/12 ≈ <b>1,3</b> → faixa 0,8–2: acidose com AG elevado pura.", "Δ/Δ &lt; 0,8 hiperclorêmica associada; &gt; 2 alcalose metabólica associada.", rnd))
    Q.append(q_num(f"QG{len(Q)+1:03d}", 9, "Homem de 80 kg com acidose hiperclorêmica grave, HCO₃⁻ 6; alvo inicial 15. Qual o déficit estimado de bicarbonato (fórmula clássica) a repor PELA METADE de início?", "≈ 180 mEq (metade de 360)",
                   [("≈ 360 mEq de uma vez", "é o déficit total; reponha metade e reavalie."), ("≈ 720 mEq", "usou espaço de distribuição 1,0 × peso e repôs tudo de uma vez."), ("≈ 108 mEq", "usou 0,3 × peso (espaço extracelular) e repôs metade."), ("≈ 60 mEq", "subestimou: 1 ampola por 10 kg não é cálculo de déficit.")],
                   "Déficit ≈ 0,5 × 80 × (15 − 6) = 360 mEq → repor ~<b>180 mEq</b> e repetir a gasometria.", "Indicação vem antes do cálculo: bicarbonato é para perda de base, não para acidose láctica/cetoacidose.", rnd))
    Q.append(q_num(f"QG{len(Q)+1:03d}", 9, "CAD com Na⁺ medido 128 e glicose 700. Qual o sódio corrigido e qual sódio usar no ânion gap?", "Na⁺ corrigido ≈ 138–142; no AG usar o Na⁺ MEDIDO (128)",
                   [("Na⁺ corrigido ≈ 138–142; no AG usar o corrigido", "o AG usa o Na⁺ medido (a diluição afeta todos os íons igualmente)."), ("Na⁺ corrigido ≈ 118; no AG usar o medido", "subtraiu a correção (a glicose DILUI o Na⁺, o corrigido é maior)."),
                    ("Na⁺ 128 — não se corrige na CAD", "o corrigido orienta a escolha do soro após a fase inicial."), ("Na⁺ corrigido ≈ 156; no AG usar o medido", "usou fator 4,7 por 100 mg/dL (exagerado).")],
                   "Na⁺ corrigido = 128 + 1,6 a 2,4 × (700 − 100)/100 = 128 + 9,6 a 14,4 ≈ <b>138–142</b>. No AG, sempre o Na⁺ medido.", "Pegadinha clássica: AG com Na⁺ corrigido superestima o AG.", rnd))
    Q.append(q_num(f"QG{len(Q)+1:03d}", 8, "Hb 8 g/dL, SatO₂ 95%, PaO₂ 80 mmHg. Qual o conteúdo arterial de O₂ (CaO₂)?", "≈ 10,4 mL/dL",
                   [("≈ 20 mL/dL", "é o normal com Hb 15; a anemia reduz muito o CaO₂."), ("≈ 7,6 mL/dL", "usou SatO₂ 71% (confundiu com saturação venosa)."), ("≈ 0,24 mL/dL", "é só o O₂ dissolvido (0,003 × PaO₂)."), ("≈ 13,0 mL/dL", "usou Hb 10 no cálculo.")],
                   "CaO₂ = 1,34 × 8 × 0,95 + 0,003 × 80 = 10,18 + 0,24 ≈ <b>10,4 mL/dL</b>.", "Hb pesa muito mais que PaO₂ no conteúdo de O₂.", rnd))
    return Q
