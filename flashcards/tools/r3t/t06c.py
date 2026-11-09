TXT = r"""
@A 🧪 Esfregaço de sangue periférico: achados e significados?
| Achado | Significado
| **Esquizócitos** | Microangiopatia (PTT, SHU, CIVD, prótese)
| Esferócitos | AHAI, esferocitose
| Dacriócitos | **Mielofibrose**, infiltração medular
| Corpúsculos de Howell-Jolly | **Asplenia**
| Hipersegmentação neutrofílica | Megaloblástica
| Bastonetes de Auer | Leucemia mieloide aguda
| Hemácias em alvo | Talassemia, hepatopatia
^ Revisões
% cmp Esfregaço periférico :: Esquizócitos = Microangiopatia: PTT, SHU, CIVD | Esferócitos = AHAI ou esferocitose | Dacriócitos = Mielofibrose | Howell-Jolly = Asplenia
@A 🧬 Talassemias: tipos e clínica?
| Tipo | Clínica
| Alfa: 1 gene deletado | Silenciosa
| Alfa: 2 genes | Traço (microcitose leve)
| Alfa: 3 genes | **Doença da HbH**
| Alfa: 4 genes | Hidropsia fetal (Hb Bart)
| Beta minor | Microcitose, **HbA2 ↑**
| Beta major | Anemia grave, transfusões, sobrecarga de ferro
^ Revisões
@A 🧪 Anemia sideroblástica?
- **Sideroblastos em anel** na medula (coloração de Perls)
- Causas: álcool, **isoniazida** (sem piridoxina), chumbo, deficiência de cobre, SMD, hereditária
^ Revisões
@B 🧪 Hemólise por prótese valvar ou microangiopatia mecânica?
= Esquizócitos, LDH alto, haptoglobina baixa; avaliar disfunção/vazamento paravalvar.
^ Revisões
@C 🧪 Trombocitose: reativa × primária?
| | Reativa | Primária (TE)
| Causas | Ferropenia, infecção, inflamação, esplenectomia, câncer | JAK2/CALR/MPL
| Trombose | Rara | **Sim**
| PCR/VHS | Altos | Normais
^ Revisões
@C 🩸 Trombocitopenia induzida por heparina: escore 4T?
- **T**rombocitopenia (queda > 50%)
- **T**iming: **5–10 dias** após início
- **T**rombose nova
- ou**T**ras causas ausentes
= Alta probabilidade: suspender **toda** heparina, iniciar não heparínico (argatrobana, fondaparinux, DOAC).
^ ASH 2018
% flow Suspeita de TIH :: Queda de plaquetas > 50% entre 5 e 10 dias de heparina >> Calcular escore 4T >> 4T intermediário/alto: suspender toda heparina e iniciar anticoagulante não heparínico >> Confirmar com anti-PF4 e teste funcional; varfarina só com plaquetas > 150 mil
@C 🧪 CIVD: escore ISTH?
= Plaquetas, **D-dímero**, TP e **fibrinogênio**; ≥ 5 pontos = CIVD manifesta.
= Tratar a causa; repor plaquetas/crio/plasma se sangramento.
^ ISTH 2001
@C 💊 Reversão dos anticoagulantes?
| Droga | Reversão
| Varfarina | **CCP 4F** + vitamina K IV
| Dabigatrana | **Idarucizumabe**
| Anti-Xa (apixabana, rivaroxabana) | **Andexanet** ou CCP 4F
| Heparina não fracionada | Protamina (total)
| Enoxaparina | Protamina (parcial)
^ ASH 2018; ACC 2020
@D 🧪 SAF: anticoagulante de escolha?
= **Varfarina** (RNI 2–3) na SAF trombótica.
! DOAC: mais eventos na SAF **tripla positiva** e trombose arterial (TRAPS) — evitar.
^ EULAR 2019
@D 🦵 TVP distal isolada (panturrilha)?
= Sintomática com risco de extensão: anticoagular 3 meses; baixo risco: **USG seriado** em 2 semanas.
^ CHEST 2021
@D 🫁 TEP subsegmentar isolado?
= Sem TVP e baixo risco de recorrência: **vigilância** pode ser opção; câncer/internado: anticoagular.
^ CHEST 2021
@D 🧪 Filtro de veia cava: indicação?
= **Contraindicação absoluta** à anticoagulação em TEV agudo (proximal).
= Retirar assim que possível anticoagular.
! Não reduz mortalidade (PREPIC 2).
^ ESC 2019; PREPIC 2 2015
@E 🔬 LMA: o que muda o prognóstico?
| Favorável | Desfavorável
| t(15;17) — LPA | Cariótipo complexo
| t(8;21), inv(16) | TP53, FLT3-ITD alto
| NPM1 sem FLT3 | Monossomia 5/7
^ ELN 2022
@E 🧬 Leucemia de células pilosas?
= Homem de meia-idade, **pancitopenia + esplenomegalia maciça**, monocitopenia, medula "seca"; **BRAF V600E**, TRAP+.
= Cladribina.
^ Revisões
@E 🧪 Leucocitose: reação leucemoide × LMC?
| | Reação leucemoide | LMC
| Fosfatase alcalina leucocitária | **Alta** | **Baixa**
| Basofilia | Não | **Sim**
| BCR-ABL | Negativo | Positivo
| Causas | Infecção grave, C. difficile, corticoide | Neoplasia
^ Revisões
@F 🧪 Linfadenopatia: quando biopsiar?
- Linfonodo > **2 cm**, duro, aderido, > 4–6 semanas
- Supraclavicular (alto risco de malignidade)
- Sintomas B, idade > 40
= Preferir **biópsia excisional** (arquitetura) a PAAF.
^ Revisões
@F 🧪 Gamopatia: eletroforese e imunofixação?
= Pico monoclonal na eletroforese (gama) → **imunofixação** identifica a cadeia; **cadeias leves livres** séricas (kappa/lambda) completam.
! Mieloma de cadeias leves pode ter eletroforese "normal".
^ IMWG
@F 💊 Mieloma: tratamento e suporte?
- Indução com tripla/quádrupla (daratumumabe, lenalidomida, bortezomibe, dexametasona)
- Transplante autólogo em elegíveis
- **Bisfosfonato**/denosumabe (doença óssea)
- Profilaxia de TEV (lenalidomida), aciclovir (bortezomibe)
^ IMWG 2024
@G 🧪 Prova cruzada e tipagem: compatibilidade ABO?
| Receptor | Hemácias compatíveis | Plasma compatível
| O | O | **Todos**
| A | A, O | A, AB
| B | B, O | B, AB
| AB | **Todos** | AB
= Doador universal de hemácias: **O negativo**; de plasma: **AB**.
^ Ministério da Saúde
@G 🩸 Transfusão maciça: protocolo?
= ≥ 10 CH em 24 h (ou ≥ 4 em 1 h).
- Razão **1:1:1** (CH:plasma:plaquetas)
- **Ácido tranexâmico** em até 3 h (trauma)
- Corrigir **cálcio** (citrato), hipotermia, acidose
- Fibrinogênio guiado por ROTEM/Clauss
^ PROPPR 2015; CRASH-2
"""
