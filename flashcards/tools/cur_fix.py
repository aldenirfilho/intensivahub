"""Correções manuais da curadoria IAs 360X (chave = 'tema#índice do conceito'; 'd' = card de aprofundamento; 'x' = extra)."""
DONE = {f"{i:02d}" for i in range(1, 31)}
V1, V2, V3, V4, V5 = "01 Ventilação mecânica", "02 Assincronias", "03 Estratégias ventilatórias", "04 SDRA e oxigenação", "05 Via aérea e suporte"
FIX = {
    f"{V1}#0": {"img": "vm_vcv_curvas.png", "nota": "Resistência = (Ppico − Pplatô)/fluxo em L/s. Gradiente pico-platô > 10 cmH₂O sugere problema de via aérea/tubo."},
    f"{V1}#1": {"img": "vm_equacao.png"},
    f"{V1}#3": {"nota": "3 τ ≈ 95% e 5 τ ≈ 99% de esvaziamento. DPOC: R alta + C alta → τ longo → precisa de Te longo."},
    f"{V1}#4": {"img": "vm_autopeep.png"},
    f"{V1}#7": {"img": "vm_transpulmonar.png"},
    f"{V2}#0": {"img": "vm_assincronias.png"},
    f"{V2}#5": {"img": "vm_assincronias.png", "nota": "Duplo disparo pode quase dobrar o VT efetivo (VT empilhado) → volutrauma mesmo com VT programado de 6 mL/kg."},
    f"{V2}#8": {"nota": "P0.1 > 3,5–4 cmH₂O = drive alto; < 1 = drive baixo (sedação/suporte excessivos)."},
    f"{V3}#0": {"img": "vm_vcv_pcv.png"},
    f"{V3}#3": {"nota": "ARDSNet 2000: VT 6 × 12 mL/kg PBW → mortalidade 31% × 39,8%. Alvos: platô ≤ 30 e ΔP ≤ 15."},
    f"{V3}#5": {"img": "vm_desmame.png"},
    f"{V3}#6": {"DECIDIR": "Integrar à clínica; o RSBI isolado não deve atrasar nem substituir o TRE", "nota": "Corte clássico: f/VT > 105 = alta chance de falha (Yang & Tobin 1991)."},
    f"{V3}#7": {"DIFERENCIAR": "Edema laríngeo (estridor) × broncoespasmo × secreção com tosse fraca × EAP de desmame × fraqueza muscular"},
    f"{V4}#0": {"nota": "Definição global 2023/2024: aceita CNAF ≥ 30 L/min, SpO₂/FiO₂ ≤ 315 (SpO₂ ≤ 97%) e USG pulmonar como imagem."},
    f"{V4}#4": {"DIFERENCIAR": "Prona acordado em CNAF e decúbito lateral: outros cenários — não extrapolar o benefício do PROSEVA",
                "nota": "PROSEVA (2013): prona ≥ 16 h/dia em P/F < 150 → mortalidade em 28 dias 16% × 32,8%."},
    f"{V4}#5": {"DIFERENCIAR": "↑ FiO₂ melhora V/Q baixo mas não recruta; PEEP recruta, porém pode sobredistender e ↑ pós-carga do VD",
                "img": "vm_peep_tabela.png", "nota": "ART (2017): recrutamento máximo com PEEP alta ↑ mortalidade → evitar manobras prolongadas de rotina."},
    f"{V4}#6": {"nota": "Shunt > 30% praticamente não responde a ↑ FiO₂ → precisa de PEEP/recrutamento/prona."},
    f"{V5}#6": {"img": "vm_vni_cnaf.png", "nota": "ROX = (SpO₂/FiO₂)/FR: ≥ 4,88 em 2, 6 ou 12 h = baixo risco; < 3,85 em 12 h = alto risco de falha."},
}
DROP = {f"{V5}#x0"}   # duplicava o aprofundamento do corpo estranho
EXTRA = {}

C6, C7, C8, C9, C10 = "06 Choque e perfusão", "07 Hemodinâmica e vasoativos", "08 Sepse SSC 2026", "09 Antimicrobianos", "10 Infecções de UTI"
P11, P12, P13, N14, A15 = "11 POCUS pulmonar", "12 POCUS cardíaco", "13 POCUS hemodinâmico", "14 Nefrologia crítica", "15 Equilíbrio ácido-base"
FIX.update({
    f"{C6}#2": {"img": "img_sepsis3.png"},
    f"{C6}#3": {"img": "pc_rush.png"},
    f"{C6}#7": {"nota": "ScvO₂ < 70% = oferta insuficiente para o consumo; ScvO₂ alta (> 80%) na sepse pode refletir extração prejudicada."},
    f"{C6}#8": {"nota": "Gap PvCO₂ − PaCO₂ > 6 mmHg sugere fluxo (DC) insuficiente, mesmo com ScvO₂ normal."},
    f"{C6}#9": {"nota": "ANDROMEDA-SHOCK (2019): ressuscitação guiada por TEC × lactato → tendência a menor mortalidade com TEC."},
    f"{C7}#0": {"img": "img_vasopressores.png", "nota": "SSC 2026: PAM inicial 65 mmHg; em ≥ 65 anos, sugere faixa 60–65 mmHg."},
    f"{C7}#4": {"img": "pc_vti.png", "nota": "EPP: medir VS/VTI em tempo real (60–90 s); ↑ ≥ 10–15% = responsivo. Não usar a PA isolada como desfecho."},
    f"{C7}#5": {"nota": "VPP > 12–13% com VT ≥ 8 mL/kg, ritmo sinusal e sem esforço. Com VT 6: 'tidal volume challenge' (↑ VPP ≥ 3,5%)."},
    f"{C8}#0": {"img": "img_sepsis3.png", "nota": "SSC 2026 (publicada em 23/03/2026, Crit Care Med): NEWS/MEWS/SIRS em vez de qSOFA isolado para triagem."},
    f"{C8}#3": {"img": "img_hora1.png"},
    f"{C9}#5": {"VERIFICAR": "Hemoculturas de controle até o clareamento e ecocardiograma (ETT; ETE conforme risco e achados)",
                "DIFERENCIAR": "Estafilococo coagulase-negativo (frequente contaminante) — S. aureus no sangue quase nunca é contaminação"},
    f"{C9}#4": {"nota": "Vancomicina em MRSA invasivo: AUC24/MIC 400–600 (assumindo MIC 1 mg/L), preferível ao vale isolado."},
    f"{P11}#0": {"img": "pc_linhas_ab.png"}, f"{P11}#2": {"img": "pc_linhas_ab.png"}, f"{P11}#4": {"img": "pc_derrame.png"},
    f"{P11}#6": {"img": "pc_blue.png"}, f"{P11}#7": {"img": "pc_lus_score.png"},
    f"{P12}#0": {"img": "pc_janelas.png"}, f"{P12}#1": {"img": "pc_vd_dsign.png"},
    f"{P12}#5": {"IDENTIFICAR": "TAPSE < 17 mm sugere disfunção sistólica do VD; medir corretamente e integrar outros índices (S', FAC, septo)"},
    f"{P12}#7": {"img": "pc_tamponamento.png"},
    f"{P13}#0": {"img": "pc_vti.png"}, f"{P13}#2": {"img": "pc_vexus.png"}, f"{P13}#6": {"img": "pc_vci.png"},
    f"{P13}#7": {"img": "pc_rush.png"}, f"{P13}#8": {"img": "pc_tvp.png"}, f"{P13}#9": {"img": "pc_efast.png"},
    f"{A15}#0": {"img": "img_acidobase.png"},
})
DROP |= {f"{C10}#x0", f"{C10}#x1", f"{C10}#8d"}

DONE_R3 = {"31", "32", "33", "34"}
R31 = "31 Cardiologia clínica"
DROP |= {f"{R31}#{i}" for i in (54, 64, 69, 149, 159)}   # perguntas duplicadas
FIX.update({f"{R31}#16": {"nota": "Washout de 36 h IECA → ARNI: risco de angioedema pela inibição combinada de ECA e neprilisina."},
            f"{R31}#60": {"nota": "Benefício também em BRE com QRS 130–149 ms (menor) e em não-BRE com QRS ≥ 150 ms (classe IIa)."}})

# ── TEMI 16–30 (lote 3) ──
E16, K17, A18, N19, T20 = "16 Distúrbios eletrolíticos", "17 Cardiologia crítica", "18 Arritmias e PCR", "19 Neurologia crítica", "20 TCE e AVC"
S21, H22, E23, G24, O25 = "21 Sedação e analgesia", "22 Hematologia e coagulação", "23 Endocrinologia", "24 Gastro e hepatologia", "25 Emergências oncológicas"
T26, P27, M28, U29, Q30 = "26 Trauma e pós-operatório", "27 Pneumologia clínica", "28 Clínica médica integrada", "29 Nutrição e prevenção", "30 Procedimentos e ética"
FIX.update({
    f"{E16}#0": {"img": "img_hipona.png"},
    f"{E16}#4": {"img": "img_hiperk.png"},
    f"{K17}#6": {"img": "pc_vd_dsign.png", "nota": "AHA/ACC 2026 (Circulation, 19/02/2026): categorias A–E substituem baixo/intermediário/alto risco; D = choque normotenso incipiente, E = hipotensão persistente/PCR. PERT classe 1 em C–E."},
    f"{S21}#2": {"img": "img_rass.png"},
    f"{S21}#5d": {"nota": "PADIS focused update (Crit Care Med, mar/2025). Contraponto: o ensaio A2B (2025) não mostrou extubação mais rápida com α2-agonistas × propofol."},
    f"{H22}#0d": {"nota": "AABB (Ann Intern Med, ago/2025), baseada em MINT + REALITY (4.311 pacientes): mortalidade em 30 d 81 × 93/1.000 com estratégia liberal."},
    f"{H22}#4": {"nota": "ISTH 2025: fases pré-CIVD → CIVD precoce → CIVD franca; no escore franco, D-dímero > 3× LSN = 2 pts e > 7× LSN = 3 pts (≥ 5 = CIVD franca)."},
    f"{T26}#0": {"img": "pc_efast.png"},
    f"{T26}#1": {"img": "pc_linhas_ab.png"},
})
DROP |= {f"{H22}#x0", f"{G24}#x0", f"{Q30}#x0"}   # duplicavam 0d, 9d e o card 7

# ── R3 32–34 ──
R32, R33, R34 = "32 Pneumologia clínica", "33 Infectologia clínica", "34 Nefrologia clínica"
DROP |= {f"{R32}#{i}" for i in (46, 131, 156, 166)}
DROP |= {f"{R33}#{i}" for i in (16, 32, 77, 101, 134, 154, 167, 201)}
DROP |= {f"{R34}#{i}" for i in (112, 214)}
FIX.update({
    f"{R32}#16": {"front": "Confirmação de asma no adulto — Qual reversibilidade broncodilatadora a GINA usa em adultos?",
                  "nota": "ERS/ATS 2021 propõe outro critério: ↑ > 10% do previsto (VEF1 ou CVF)."},
    f"{R32}#150": {"nota": "ESC/ERS 2022: HP = PAPm > 20 mmHg; pré-capilar = POAP ≤ 15 + RVP > 2 UW."},
    f"{R33}#40": {"front": "Pneumocistose: profilaxia — Segundo as diretrizes NIH de infecções oportunistas, quando iniciar profilaxia em quem está sem TARV ou iniciando?"},
    f"{R33}#36": {"nota": "Prednisona 40 mg 2×/dia (d1–5) → 40 mg/dia (d6–10) → 20 mg/dia (d11–21)."},
})

# ── R3 35–36 ──
DONE_R3 |= {"35", "36"}
R35, R36 = "35 Endocrinologia clínica", "36 Gastroenterologia e hepatologia"
FIX.update({
    f"{R35}#97": {"nota": "Limiar mudou: ADA 2009 segurava a insulina com K⁺ < 3,3; o consenso ADA/EASD 2024 usa K⁺ < 3,5 mmol/L. Prova antiga pode cobrar 3,3."},
    f"{R35}#86": {"nota": "Consenso hiperglicêmico 2024 (ADA/EASD/JBDS/AACE/DTS): BHB ≥ 3,0 mmol/L ou cetonúria ≥ 2+."},
    f"{R36}#57": {"nota": "ICA/ADQI 2024: avaliar volemia; se indicado, reposição (albumina ou cristaloide) e reavaliar em 24 h — o antigo 'albumina 1 g/kg por 48 h' saiu."},
})

# ── Lote final: R3 37–40 + todos os blocos nomeados (zera a coleção bruta) ──
DONE_R3 |= {"37", "38", "39", "40"}
DONE_NAMED = True   # cura todos os ia360-*.json sem número (TEMI e R3) com chave "TEMI/<tema>" ou "R3/<tema>"
FIX.update({
    "TEMI/Hematologia e oncologia#148": {"nota": "Exceção atual: AABB (Ann Intern Med, ago/2025) sugere estratégia liberal (Hb < 10 g/dL) no IAM hospitalizado."},
    "TEMI/Cardiologia R3#9": {"nota": "ESC 2026 (Køber/Adamo, ago/2026) eliminou a IC levemente reduzida: FE < 50% = reduzida; ≥ 50% = preservada."},
    "TEMI/Nefrologia e metabolismo renal#219": {"nota": "BICARICU-2 (JAMA 2025): diálise até o dia 28 em 35% × 50% — bicarbonato pode adiar/evitar TRS, sem mudar mortalidade."},
    "TEMI/Pneumologia R3#36": {"nota": "GOLD 2026 rebaixou o limiar do grupo E para ≥ 1 exacerbação moderada ou grave no último ano (antes: ≥ 2 moderadas ou ≥ 1 internação)."},
})
