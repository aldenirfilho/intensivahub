TXT = r"""
@A 💉 Tipos de insulina e perfil?
| Insulina | Início | Pico | Duração
| Ultrarrápida (lispro, asparte, glulisina) | 10–15 min | 1–2 h | 3–5 h
| Regular | 30 min | 2–3 h | 6–8 h
| NPH | 1–2 h | 4–8 h | 10–16 h
| Glargina U100 / detemir | 1–2 h | Sem pico | ~24 h
| Degludeca / glargina U300 | — | Sem pico | > 24–42 h
^ ADA 2025
@A 🧪 Cetoacidose euglicêmica: pistas?
= Acidose com cetonemia e glicemia **< 250**.
- **iSGLT2**, gestação, jejum prolongado, álcool, cirurgia
= Tratar com insulina **+ glicose** desde o início.
^ ADA 2024
@A 🍬 Estado hiperglicêmico hiperosmolar?
- Glicemia **> 600**, osmolalidade efetiva > 300, sem cetoacidose importante
- Idosos, desidratação grave, rebaixamento
= Prioridade: **volume** (déficit ~ 8–10 L); insulina em dose menor depois de iniciar hidratação.
^ ADA 2024
@A 🧓 Metas do DM no idoso?
| Perfil | HbA1c
| Saudável | < 7,0–7,5%
| Complexo/intermediário | < 8,0%
| Muito complexo/frágil | Evitar hipoglicemia e hiperglicemia sintomática
^ ADA 2025
@A 🔬 MODY: quando pensar?
- Diagnóstico **< 25–35 anos**, magro, sem autoimunidade
- **Herança autossômica dominante** (3 gerações)
- MODY 3 (HNF1A): ótima resposta a **sulfonilureia**
- MODY 2 (GCK): hiperglicemia leve estável, geralmente sem tratamento
^ ADA 2025
@B 🧊 Coma mixedematoso: tratamento?
- **Levotiroxina IV** (ataque 200–400 µg)
- **Hidrocortisona** até excluir insuficiência adrenal
- Suporte ventilatório, reaquecimento passivo
- Tratar fator precipitante (infecção)
^ ATA 2014
@B 🔥 Tempestade tireoidiana: tratamento em ordem?
- **Betabloqueador** (propranolol)
- **Tionamida** (PTU preferível)
- **Iodo** ≥ 1 h após a tionamida
- **Corticoide**
- Suporte e resfriamento
^ ATA 2016
% flow Tempestade tireoidiana :: Betabloqueador (propranolol) >> Tionamida: PTU ou metimazol >> Iodo pelo menos 1 hora depois >> Hidrocortisona + suporte e tratar o gatilho
@B 🧪 Eutireoidiano doente (síndrome do T3 baixo)?
= Doença grave: **T3 baixo**, rT3 alto, TSH normal/baixo, T4 normal ou baixo.
= **Não tratar**; reavaliar após recuperação.
^ Revisões
@B 🎗️ Câncer de tireoide: tipos?
| Tipo | Pista
| Papilífero | Mais comum, **corpos de psamoma**, linfonodos, bom prognóstico
| Folicular | Disseminação **hematogênica** (osso, pulmão)
| Medular | **Calcitonina**, CEA, NEM 2 (RET)
| Anaplásico | Idoso, crescimento rápido, péssimo prognóstico
^ ATA 2015
@C 🧬 NEM 1 × NEM 2?
| NEM 1 (3 Ps) | NEM 2A | NEM 2B
| Paratireoide | Medular de tireoide | Medular de tireoide
| Pâncreas (gastrinoma, insulinoma) | Feocromocitoma | Feocromocitoma
| Pituitária | Hiperparatireoidismo | Neuromas mucosos, habitus marfanoide
^ Revisões
% cmp Neoplasias endócrinas múltiplas :: NEM 1 = Paratireoide, pâncreas, pituitária (MEN1) | NEM 2A = Medular de tireoide, feocromocitoma, hiperparatireoidismo (RET) | NEM 2B = Medular, feocromocitoma, neuromas mucosos, marfanoide
@C 🧪 Hiperaldosteronismo primário: confirmação e tratamento?
- Teste confirmatório (infusão salina, captopril, sobrecarga de sal)
- TC de adrenais; **cateterismo de veias adrenais** antes de cirurgia
- Adenoma unilateral: **adrenalectomia**
- Hiperplasia bilateral: **espironolactona**
^ Endocrine Society 2016
@C 💊 Insulinoma: tríade de Whipple?
- Sintomas de hipoglicemia
- **Glicemia baixa** documentada
- Alívio com glicose
= Insulina e **peptídeo C altos** na hipoglicemia (factícia com insulina: peptídeo C baixo).
^ Endocrine Society 2009
% cmp Hipoglicemia com insulina alta :: Insulinoma = Insulina e peptídeo C ALTOS, sulfonilureia negativa | Sulfonilureia = Insulina e peptídeo C altos, dosagem de sulfonilureia positiva | Insulina exógena = Insulina alta, peptídeo C BAIXO
@D 🧠 SIADH × diabetes insípido no pós-operatório de hipófise?
= Resposta trifásica: **DI** (dias 1–5) → **SIADH** (dias 5–10) → DI permanente.
! Monitorar Na diariamente.
^ Revisões
@D 🧪 Hipopituitarismo: hormônios afetados primeiro?
= Ordem típica de perda: **GH → LH/FSH → TSH → ACTH** (prolactina pode subir por efeito haste).
^ Revisões
@E 🦴 Hipocalcemia pós-tireoidectomia?
= Hipoparatireoidismo (transitório ou permanente): parestesias, Chvostek, Trousseau.
= Cálcio oral + **calcitriol**; IV se sintomática grave.
^ Revisões
@E 🧪 Osteoporose secundária: o que investigar?
- **Corticoide**, hipogonadismo, hipertireoidismo, hiperparatireoidismo
- Deficiência de vitamina D, doença celíaca
- Mieloma, DRC, álcool, IBP crônico, inibidores de aromatase
= Exames: cálcio, fósforo, PTH, 25-OH-D, TSH, creatinina, eletroforese.
^ Endocrine Society
@E 🧮 FRAX: para que serve?
= Probabilidade em **10 anos** de fratura maior e de quadril; orienta tratamento em osteopenia.
= No Brasil, usa-se o FRAX Brasil com limiares do ABOM/SBEM.
^ FRAX
@E 💊 Osteoporose induzida por corticoide?
= Prednisona ≥ **2,5–5 mg/dia por ≥ 3 meses**: cálcio, vitamina D, densitometria; bisfosfonato conforme risco.
^ ACR 2022
@F 🧂 Hirsutismo: quando investigar tumor?
- Início **rápido**, virilização (clitoromegalia, voz grave)
- Testosterona > 150–200 ng/dL (ovário)
- **DHEA-S** > 700 µg/dL (adrenal)
^ Endocrine Society 2018
@F 🧪 Ginecomastia: causas?
- Fisiológica (puberdade, idoso), obesidade
- Drogas: **espironolactona**, cetoconazol, cimetidina, antiandrogênicos, anabolizantes, maconha
- Cirrose, hipertireoidismo, hipogonadismo
- Tumores produtores de **hCG** (testículo, pulmão)
^ Revisões
"""
