TXT = r"""
@A 🍬 Critérios diagnósticos de diabetes?
| Exame | Diabetes | Pré-diabetes
| Glicemia de jejum | ≥ 126 | 100–125
| TOTG 2 h | ≥ 200 | 140–199
| HbA1c | ≥ 6,5% | 5,7–6,4%
| Glicemia ao acaso + sintomas | ≥ 200 | —
= Sem sintomas: confirmar com 2º exame alterado.
^ ADA 2025; SBD 2024
% zones Diagnóstico de DM pela HbA1c :: Normal = < 5,7% | Pré-diabetes = 5,7–6,4% | Diabetes = ≥ 6,5%
@A 🩸 Quando a HbA1c não é confiável?
- Anemia ferropriva (↑ falsa), hemólise e perda sanguínea (↓ falsa)
- Hemoglobinopatias, transfusão recente
- Gestação, DRC avançada, eritropoetina
= Usar glicemias, frutosamina ou CGM.
^ ADA 2025
@A 🎯 Metas glicêmicas no DM2?
| Parâmetro | Meta geral
| HbA1c | < 7% (idoso frágil < 8–8,5%)
| Jejum/pré-prandial | 80–130 mg/dL
| Pós-prandial | < 180 mg/dL
| CGM: tempo no alvo (70–180) | > 70%
| Tempo < 70 | < 4%
^ ADA 2025
@A 💊 Escolha da 2ª droga no DM2 por comorbidade?
| Comorbidade | Preferir
| DCV aterosclerótica | **GLP-1 RA** ou iSGLT2
| IC | **iSGLT2**
| DRC | **iSGLT2** (± GLP-1 RA)
| Obesidade | Tirzepatida, semaglutida
| Custo | Sulfonilureia, pioglitazona, NPH
^ ADA 2025
% cmp DM2: segunda droga por comorbidade :: DCV aterosclerótica = GLP-1 RA ou iSGLT2 | IC = iSGLT2 | DRC = iSGLT2 ± GLP-1 RA | Obesidade = Tirzepatida ou semaglutida
@A ⚠️ Efeitos adversos importantes dos antidiabéticos?
| Classe | Efeito
| Metformina | Diarreia, ↓ B12, acidose láctica (rara)
| Sulfonilureia | **Hipoglicemia**, ganho de peso
| Pioglitazona | Edema, **IC**, fratura, ganho de peso
| iSGLT2 | Infecção genital, cetoacidose euglicêmica
| GLP-1 RA | Náusea, pancreatite (?), colelitíase
| iDPP-4 | Saxagliptina: ↑ internação por IC
^ ADA 2025
@A 💉 Insulinização no DM2: como iniciar?
= Basal **10 U** ou **0,1–0,2 U/kg** à noite, titulando 2 U a cada 3 dias até jejum no alvo.
- Indicação: HbA1c > 10% ou glicemia ≥ 300, sintomas catabólicos
- Se basal > 0,5 U/kg sem controle: adicionar prandial ou GLP-1
^ ADA 2025
@A 🌙 Fenômeno do alvorecer × efeito Somogyi?
| | Alvorecer | Somogyi
| Glicemia às 3 h | Normal | **Baixa**
| Mecanismo | Hormônios contrarreguladores | Hipoglicemia noturna → rebote
| Conduta | ↑ basal ou ajustar horário | **↓ insulina noturna**
! CGM praticamente desmistificou o Somogyi, mas cai em prova.
^ Revisões
@A 🧊 Hipoglicemia: classificação e tratamento?
| Nível | Glicemia
| 1 | < 70 mg/dL
| 2 | < 54 mg/dL
| 3 | Grave: precisa de ajuda de terceiros
= Regra dos 15: **15 g de carboidrato**, reavaliar em 15 min. Inconsciente: glicose IV ou glucagon.
^ ADA 2025
@A 👁️ Rastreamento de complicações microvasculares no DM2?
- **Fundo de olho** ao diagnóstico e anual
- **Albuminúria + TFG** anual
- **Pé**: monofilamento + pulsos anual (cada consulta se risco)
= No DM1: iniciar 5 anos após o diagnóstico.
^ ADA 2025
@A 🦶 Pé diabético infectado: classificação e tratamento?
- Leve: celulite < 2 cm → cefalexina/amoxicilina-clavulanato oral
- Moderada: > 2 cm ou profunda → considerar internação
- Grave: SIRS → internar, ATB IV amplo
- **Osteomielite**: probe-to-bone, RM; 6 semanas de ATB ou ressecção
^ IWGDF/IDSA 2023
@A 🧬 Suspeita de DM1 ou LADA no adulto?
- Magro, jovem, perda de peso, cetose
- Rápida falência de orais
- **Anti-GAD**, anti-IA2, anti-ZnT8 positivos; peptídeo C baixo
^ ADA 2025
@A 🤰 Diabetes gestacional: diagnóstico (Brasil)?
= Jejum na 1ª consulta: **92–125** = DMG; ≥ 126 = DM prévio.
= TOTG 75 g entre **24–28 semanas**: jejum ≥ 92, 1 h ≥ 180, 2 h ≥ 153 (1 valor basta).
- Tratamento: dieta, exercício; **insulina** 1ª linha farmacológica (metformina alternativa)
^ FEBRASGO/SBD/OPAS 2017
@A 🧪 Neuropatia diabética dolorosa: tratamento?
- **Duloxetina**, **pregabalina/gabapentina**, amitriptilina (1ª linha)
- Capsaicina tópica
! Opioide não é recomendado de rotina.
^ ADA 2025
@B 🦋 Interpretação de TSH e T4 livre?
| TSH | T4L | Diagnóstico
| ↑ | ↓ | Hipotireoidismo primário
| ↑ | Normal | Hipotireoidismo subclínico
| ↓ | ↑ | Hipertireoidismo primário
| ↓ | Normal | Hipertireoidismo subclínico (ver T3)
| ↓ ou normal | ↓ | **Hipotireoidismo central**
| Normal/↑ | ↑ | TSH-oma, resistência
^ ATA
% cmp Função tireoidiana :: TSH alto + T4L baixo = Hipotireoidismo primário | TSH baixo + T4L alto = Hipertireoidismo | TSH baixo/normal + T4L baixo = Central (hipófise) | TSH normal/alto + T4L alto = TSH-oma ou resistência
@B 💊 Levotiroxina: como usar?
- Dose plena ~**1,6 µg/kg/dia**; idoso/cardiopata: 12,5–25 µg e titular
- Jejum, 30–60 min antes do café
- Separar 4 h de **cálcio, ferro**, IBP, sucralfato
- Ajustar TSH a cada **6–8 semanas**
^ ATA 2014
@B 🔥 Causas de tireotoxicose pela captação de iodo?
| Captação | Causa
| **Alta difusa** | Graves
| Alta focal | Adenoma tóxico, bócio multinodular tóxico
| **Baixa** | Tireoidite (subaguda, pós-parto, silenciosa, amiodarona tipo 2), iodo exógeno, factícia
^ ATA 2016
@B 💊 Tionamidas: efeitos adversos graves?
- **Agranulocitose** (febre, dor de garganta → hemograma e suspender)
- Hepatotoxicidade: **PTU** (necrose hepática) > metimazol (colestase)
- Vasculite ANCA (PTU)
= PTU: 1º trimestre e tempestade tireoidiana; metimazol nos demais.
^ ATA 2016
@B 🎯 Nódulo tireoidiano: quando puncionar?
| Classificação USG | PAAF se
| TI-RADS 5 | ≥ 1,0 cm
| TI-RADS 4 | ≥ 1,5 cm
| TI-RADS 3 | ≥ 2,5 cm
| TI-RADS 1–2 | Não
= TSH baixo: cintilografia antes (nódulo quente raramente é maligno).
^ ACR TI-RADS 2017
@B 📑 Classificação de Bethesda?
| Categoria | Conduta
| I Não diagnóstica | Repetir
| II Benigno | Seguimento
| III AUS | Repetir/molecular
| IV Neoplasia folicular | Lobectomia/molecular
| V Suspeito | Cirurgia
| VI Maligno | Cirurgia
^ Bethesda 2023
% zones Bethesda (citologia tireoidiana) :: I = Não diagnóstica | II = Benigno | III = Atipia indeterminada | IV = Neoplasia folicular | V = Suspeito de malignidade | VI = Maligno
@B 👀 Oftalmopatia de Graves: cuidados?
- Exclusiva de **Graves**
- Piora com **tabagismo** e iodo radioativo
- Moderada-grave ativa: corticoide IV (metilprednisolona); teprotumumabe
= Iodo radioativo em oftalmopatia ativa: profilaxia com prednisona.
^ EUGOGO 2021
@B 🤰 Tireoide na gestação?
- Hipotireoidia em uso: **↑ dose 25–30%** ao confirmar gravidez
- TSH alvo < 2,5 no 1º trimestre (ou limite do método)
- Hipertireoidismo: PTU no 1º trimestre, metimazol depois
! Hiperêmese gravídica e hCG: TSH baixo transitório (não tratar).
^ ATA 2017 gestação
"""
