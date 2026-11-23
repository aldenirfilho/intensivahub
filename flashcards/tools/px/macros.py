"""Linhas padronizadas reaproveitadas nas 500 prescrições (expandidas pelo build_px.py).
Uma linha "@NOME" na lista rx vira o texto abaixo. ALDENIR ROCHA DE OLIVEIRA FILHO · PROJETO 360X"""
M = {
    # dieta
    "@DIETA": "Dieta oral livre conforme aceitação; adaptar às comorbidades (hipossódica na HAS/IC, para diabético no DM)",
    "@DIETA_DM": "Dieta para diabético, fracionada em 6 refeições; carboidratos distribuídos ao longo do dia",
    "@DIETA_HS": "Dieta hipossódica (até 2 g de sódio/dia)",
    "@DIETA_BRANDA": "Dieta branda / pastosa conforme aceitação, com cabeceira elevada durante as refeições",
    "@ZERO": "Dieta zero (jejum) até reavaliação",
    "@ZERO_SNG": "Dieta zero; sonda nasogástrica aberta em frasco se vômitos ou distensão",
    "@ENTERAL": "Nutrição enteral por sonda iniciada em 24–48 h (trofismo 10–20 mL/h, progredir conforme tolerância até a meta de 25 kcal/kg/dia e 1,2–2 g/kg/dia de proteína)",
    # acesso, hidratação
    "@AVP": "Acesso venoso periférico salinizado",
    "@AVP2": "Dois acessos venosos periféricos calibrosos (14–18 G)",
    "@HV_MANUT": "Hidratação de manutenção só se ingesta oral insuficiente: Ringer lactato ou SF 0,9% 25–30 mL/kg/dia (menos na IC/DRC), com KCl conforme potássio",
    # monitorização
    "@SSVV": "Sinais vitais, dor (0–10) e diurese de 6/6 h; avisar se PAS < 90 mmHg, FC > 120 bpm, FR > 24 irpm, SpO₂ < 92% ou Tax ≥ 38 °C",
    "@SSVV4": "Sinais vitais de 4/4 h e escala de dor; avisar se PAS < 90 mmHg, FC > 120 bpm, FR > 24 irpm, SpO₂ < 92%, Tax ≥ 38 °C ou rebaixamento",
    "@UTI_MON": "Monitorização contínua (ECG, SpO₂, PA não invasiva ou invasiva); sinais vitais de 1/1 h",
    "@BH": "Balanço hídrico de 6/6 h e de 24 h; peso diário",
    "@DIURESE_H": "Diurese horária (sonda vesical de demora se necessário); meta ≥ 0,5 mL/kg/h",
    "@HGT": "Glicemia capilar antes das refeições e às 22 h (de 6/6 h se dieta zero ou enteral contínua)",
    "@HGT_UTI": "Glicemia capilar de 4/4 h (alvo 140–180 mg/dL); insulina IV contínua se 2 medidas > 180 mg/dL",
    "@NEURO_CHECK": "Escala de Glasgow e pupilas de 1/1 h nas primeiras 24 h; avisar se queda ≥ 2 pontos",
    # glicemia
    "@INS_CORR": "Insulina regular SC conforme glicemia capilar: 141–180: 2 UI · 181–240: 4 UI · 241–300: 6 UI · 301–350: 8 UI · > 350: 10 UI e avisar o médico",
    "@HIPO": "Se glicemia < 70 mg/dL: consciente → 15 g de glicose VO; jejum ou rebaixado → glicose 50% 40 mL IV (20 g); repetir glicemia em 15 min",
    # profilaxias
    "@TEV": "Profilaxia de TEV (se Padua ≥ 4 e sem sangramento): enoxaparina 40 mg SC 1×/dia — ClCr < 30: 20 mg/dia ou HNF 5.000 UI SC 12/12 h; IMC ≥ 40: 40 mg 12/12 h",
    "@TEV_HNF": "Profilaxia de TEV: heparina não fracionada 5.000 UI SC 8/8 h (preferir na DRC grave e quando pode haver procedimento)",
    "@TEV_MEC": "Profilaxia mecânica de TEV (compressão pneumática intermitente) enquanto a anticoagulação estiver contraindicada",
    "@IBP_PROF": "Pantoprazol 40 mg IV 1×/dia SÓ se risco de úlcera de estresse (VM > 48 h, coagulopatia, choque, sangramento GI prévio); suspender quando o risco cessar",
    "@MUC": "Profilaxia de lesão por pressão: mudança de decúbito 2/2 h, colchão pneumático e proteção de calcâneos",
    "@QUEDA": "Precauções de queda e de broncoaspiração; grades elevadas",
    "@CAB": "Cabeceira elevada a 30–45°",
    "@DELIRIUM": "Prevenção de delirium: reorientação, óculos e aparelho auditivo, luz natural de dia e escuro à noite, sono protegido, mobilização precoce; evitar contenção e benzodiazepínico",
    "@FISIO": "Fisioterapia motora e respiratória; mobilização precoce conforme tolerância",
    "@HIGIENE_VM": "Higiene oral com escovação dentária 12/12 h (sem clorexidina de rotina); interrupção diária da sedação e teste de respiração espontânea quando elegível",
    # sintomáticos
    "@DIPI": "Dipirona 1 g IV ou VO 6/6 h se dor ou febre (Tax ≥ 37,8 °C)",
    "@PARA": "Paracetamol 750 mg VO 6/6 h se dor ou febre (máx. 3 g/dia; 2 g/dia em hepatopata, etilista ou desnutrido)",
    "@ONDA": "Ondansetrona 4 mg IV 8/8 h se náuseas ou vômitos (evitar se QTc > 500 ms)",
    "@BROMO": "Bromoprida 10 mg IV 8/8 h se náuseas (evitar em Parkinson e em obstrução intestinal)",
    "@LACTU_CONST": "Lactulose 15–20 mL VO 12/12 h se sem evacuar há 48 h; suspender se diarreia",
    "@O2": "O₂ por cateter nasal 1–5 L/min se SpO₂ < 92% (alvo 92–96%)",
    "@O2_DPOC": "O₂ por cateter nasal 1–2 L/min ou máscara de Venturi 24–28% com alvo de SpO₂ 88–92%",
    # isolamento e culturas
    "@CULT": "Hemoculturas 2 amostras (punções diferentes) e culturas do foco ANTES do antibiótico, sem atrasar a 1ª dose",
    "@ISO_CONT": "Precaução de contato (avental e luvas; estetoscópio exclusivo)",
    "@ISO_GOT": "Precaução de gotículas (máscara cirúrgica; quarto privativo ou coorte)",
    "@ISO_AER": "Precaução aérea: quarto privativo (de preferência com pressão negativa) e máscara N95/PFF2 para a equipe",
    # exames
    "@LAB": "Hemograma, ureia, creatinina, sódio e potássio na admissão e a cada 24–48 h",
    "@LAB_UTI": "Hemograma, função renal, eletrólitos (Na, K, Mg, P, Ca iônico), gasometria arterial e lactato diários",
    "@ECG": "ECG de 12 derivações na admissão",
}
