TXT = r"""
@E 🫀 Classificação clínica da hipertensão pulmonar (OMS)?
| Grupo | Causa
| 1 | Hipertensão arterial pulmonar (idiopática, colagenose, drogas, HIV, portopulmonar)
| 2 | Doença do coração esquerdo (mais comum)
| 3 | Doença pulmonar/hipóxia
| 4 | Tromboembolismo crônico (HPTEC)
| 5 | Multifatorial
^ ESC/ERS 2022
@E 🔎 Rastreio de HPTEC após TEP?
= Dispneia persistente > 3 meses após anticoagulação → eco; se sugestivo, **cintilografia V/Q** (melhor exame de rastreio).
= Tratamento: endarterectomia, angioplastia por balão, riociguate.
^ ESC/ERS 2022
@E 😴 STOP-BANG para apneia do sono?
- **S**nore (ronco alto)
- **T**ired (cansaço diurno)
- **O**bserved (apneias presenciadas)
- **P**ressure (HAS)
- **B**MI > 35
- **A**ge > 50
- **N**eck > 40 cm
- **G**ender masculino
= ≥ 3: risco intermediário; ≥ 5: alto risco.
^ Chung 2008
@E 📊 Gravidade da apneia obstrutiva do sono pelo IAH?
| IAH (eventos/h) | Gravidade
| 5–14 | Leve
| 15–29 | Moderada
| ≥ 30 | Grave
= CPAP: IAH ≥ 15, ou ≥ 5 com sintomas/comorbidade CV.
^ AASM
% zones Apneia obstrutiva do sono (IAH) :: Leve = 5–14 eventos/h | Moderada = 15–29 eventos/h | Grave = ≥ 30 eventos/h
@E 🏋️ Síndrome de obesidade-hipoventilação?
= IMC ≥ 30 + **PaCO₂ diurna ≥ 45** sem outra causa.
- Bicarbonato sérico ≥ 27 sugere
- Tratamento: CPAP ou VNI (BiPAP), perda de peso
! Oxigênio isolado piora a hipercapnia.
^ ATS 2019
@E 🩸 Hemoptise maciça: conduta?
- Proteger via aérea; **decúbito sobre o lado que sangra**
- Intubação seletiva/tubo calibroso, broncoscopia
- **Embolização de artéria brônquica**
- Ácido tranexâmico (inalado ou IV) como adjuvante
= Causas: bronquiectasias, TB, câncer, aspergiloma.
^ Revisões
@F 🫁 Bronquiectasias não fibrocísticas: causas e manejo?
- Pós-infecciosa (TB, coqueluche), imunodeficiência, ABPA, discinesia ciliar, DRGE, AR
- Fisioterapia respiratória, solução salina hipertônica
- **Macrolídeo** de longo prazo se ≥ 3 exacerbações/ano
- Erradicar Pseudomonas na 1ª colonização
^ ERS 2017
@F 🧭 Padrões da espirometria: resumo?
| Padrão | VEF₁/CVF | CVF
| Obstrutivo | **↓** (< LIN ou < 0,7) | Normal ou ↓
| Restritivo | Normal ou ↑ | **↓** (confirmar com CPT)
| Misto | ↓ | ↓
^ ATS/ERS 2022
% cmp Padrões espirométricos :: Obstrutivo = VEF1/CVF reduzida. Asma, DPOC, bronquiectasias | Restritivo = VEF1/CVF normal, CVF e CPT reduzidas. Intersticial, obesidade, neuromuscular | Misto = Ambos reduzidos. Confirmar volumes
@F 🫀 Gradiente alvéolo-arterial: como calcular e interpretar?
= PAO₂ = FiO₂ × (760 − 47) − PaCO₂/0,8 → **G(A-a) = PAO₂ − PaO₂**.
- Normal: ~ (idade/4) + 4
- Hipoxemia com gradiente **normal**: hipoventilação, baixa FiO₂
- Gradiente **alto**: V/Q, shunt, difusão
^ Fisiologia respiratória
@F 🧫 Abscesso pulmonar: perfil e tratamento?
- Aspiração em etilistas, dentes ruins, rebaixamento de consciência
- Segmentos posteriores de lobos superiores / superiores de inferiores
- Anaeróbios: **amoxicilina-clavulanato** ou clindamicina por 4–6 semanas
^ IDSA
@F 🧾 Pneumonia por aspiração × pneumonite química?
| | Pneumonite (Mendelson) | Pneumonia aspirativa
| Mecanismo | Ácido gástrico | Bactérias da orofaringe
| Início | Horas | Dias
| Antibiótico | **Não** de rotina | Sim
^ ATS/IDSA 2019
@F 🦠 Pneumonia comunitária: CURB-65?
- **C**onfusão
- **U**reia > 50 mg/dL (> 7 mmol/L)
- **R**espiração ≥ 30
- **B**PA: PAS < 90 ou PAD ≤ 60
- **65** anos
| Pontos | Local
| 0–1 | Ambulatorial
| 2 | Internação
| ≥ 3 | Grave (UTI se 4–5)
^ Lim 2003
% zones CURB-65 e local de tratamento :: 0–1 = Ambulatório | 2 = Internação | 3–5 = Grave, considerar UTI
@F 🏥 Critérios maiores de PAC grave (ATS/IDSA)?
- **Choque séptico** com vasopressor
- **Insuficiência respiratória** com ventilação mecânica
= 1 maior ou ≥ 3 menores (FR ≥ 30, P/F ≤ 250, multilobar, confusão, ureia ≥ 20 mmol/L, leucócitos < 4.000, plaquetas < 100 mil, T < 36 °C, hipotensão com volume) → **UTI**.
^ ATS/IDSA 2019
@F 💊 Tratamento empírico da PAC internada (não grave)?
= **β-lactâmico** (ceftriaxona, ampicilina-sulbactam) **+ macrolídeo**, ou fluoroquinolona respiratória isolada.
- Duração mínima **5 dias** com estabilidade clínica
- Cobrir MRSA/Pseudomonas só com fatores de risco (cultura prévia, internação com ATB IV em 90 dias)
^ ATS/IDSA 2019
@F 🧪 Legionella: pistas?
- Pneumonia grave com **diarreia**, confusão, bradicardia relativa
- **Hiponatremia**, ↑ transaminases, ↑ CK
- Antígeno urinário (sorogrupo 1)
= Tratamento: macrolídeo ou fluoroquinolona.
^ ATS/IDSA 2019
@F 💨 Tosse crônica no adulto: principais causas?
= Tosse > 8 semanas com RX normal:
- **Síndrome da tosse das vias aéreas superiores** (gotejamento pós-nasal)
- **Asma** (incluindo variante tosse)
- **DRGE**
- IECA; bronquite eosinofílica não asmática
^ ACCP 2018
@F 💊 Tosse por IECA?
= Acúmulo de **bradicinina**; até 10–15% dos pacientes; surge em semanas a meses.
= Trocar por **BRA**; melhora em 1–4 semanas (até 3 meses).
^ ACCP 2006
"""
