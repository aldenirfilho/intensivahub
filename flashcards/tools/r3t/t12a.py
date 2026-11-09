TXT = r"""
@A 😔 Episódio depressivo maior (DSM-5)?
= ≥ 5 sintomas por ≥ **2 semanas**, incluindo **humor deprimido ou anedonia**:
- Alteração de sono, apetite/peso
- Fadiga, culpa, concentração
- Agitação/lentificação psicomotora
- Ideação suicida
^ DSM-5-TR
@A 📋 PHQ-9: interpretação?
| Escore | Gravidade
| 5–9 | Leve
| 10–14 | Moderada
| 15–19 | Moderadamente grave
| ≥ 20 | Grave
= Item 9 positivo (ideação suicida): avaliar risco **no mesmo dia**.
^ Kroenke 2001
% zones PHQ-9 :: Leve = 5–9 | Moderada = 10–14 | Moderadamente grave = 15–19 | Grave = ≥ 20
@A 💊 Depressão: tratamento inicial e tempo?
- **ISRS** (sertralina, escitalopram) 1ª linha
- Resposta em **4–6 semanas**; ajustar dose antes de trocar
- Manter **6–12 meses** após remissão (1º episódio); ≥ 2 anos se recorrente
- Psicoterapia (TCC) tão eficaz quanto em leve-moderada
^ CANMAT 2023
@A ⚡ Transtorno bipolar: o que evitar?
= **Antidepressivo em monoterapia** (virada maníaca, ciclagem rápida).
- Mania: lítio, valproato, antipsicótico atípico
- Depressão bipolar: quetiapina, lurasidona, lamotrigina (manutenção)
^ CANMAT/ISBD 2018
@A 😰 Transtorno de ansiedade generalizada?
- Preocupação excessiva, difícil de controlar, por ≥ **6 meses**
- Inquietação, fadiga, tensão muscular, insônia
- **GAD-7**
= ISRS/IRSN + TCC; benzodiazepínico só por curto período.
^ DSM-5-TR; CANMAT 2014
@A 💓 Ataque de pânico × SCA?
= Pânico: pico em **10 min**, medo de morrer, parestesias, despersonalização.
! Sempre excluir causas orgânicas (SCA, arritmia, hipertireoidismo, feocromocitoma, abstinência) antes de rotular.
^ DSM-5-TR
@B 🔥 Síndrome neuroléptica maligna?
- **Rigidez em "cano de chumbo"**, hipertermia, rebaixamento, disautonomia
- **CK muito alta**, leucocitose
- Instalação em **dias**, após antipsicótico (ou retirada de levodopa)
= Suspender, suporte, dantrolene, bromocriptina.
^ Revisões
% cmp Serotoninérgica × neuroléptica maligna :: Serotoninérgica = Horas, clônus e hiper-reflexia, midríase, diarreia. Ciproeptadina | Neuroléptica maligna = Dias, rigidez em cano de chumbo, CK muito alta, bradicinesia. Dantrolene
@B 🧂 Lítio: faixa terapêutica e toxicidade?
= Nível **0,6–1,2 mEq/L** (agudo até 1,2; manutenção 0,6–0,8).
- Toxicidade: tremor grosseiro, ataxia, confusão, diarreia
- Crônico: **hipotireoidismo**, **diabetes insípido nefrogênico**, hiperparatireoidismo, DRC
! Aumentam o nível: **tiazídicos**, IECA/BRA, AINE, desidratação.
^ Revisões
% zones Litemia (mEq/L) :: Manutenção = 0,6–0,8 | Mania aguda = Até 1,2 | Toxicidade = > 1,5 | Grave, diálise = > 4,0 ou > 2,5 com sintomas
@B ⚠️ Antipsicóticos atípicos: efeitos metabólicos e outros?
| Droga | Destaque
| **Olanzapina**, clozapina | Ganho de peso, DM, dislipidemia
| Risperidona | **Hiperprolactinemia**, sintomas extrapiramidais
| Quetiapina | Sedação, hipotensão
| Ziprasidona | QT longo
| Aripiprazol | Acatisia; metabolicamente neutro
| **Clozapina** | **Agranulocitose** (hemograma), miocardite, convulsão
^ Revisões
@B 🧪 ISRS: efeitos adversos de destaque?
- Disfunção sexual, náusea
- **Hiponatremia** (idosos)
- **Sangramento** (com AAS/anticoagulante)
- QT longo (citalopram/escitalopram)
- Síndrome de descontinuação (paroxetina)
^ Revisões
@B 💤 Benzodiazepínicos: riscos e retirada?
- Quedas, fraturas, delirium, dependência
- Retirada abrupta: ansiedade, **convulsões**
= Desmame **gradual** (10–25% a cada 2–4 semanas).
- Overdose: depressão respiratória com opioide/álcool; antídoto **flumazenil** (cuidado: convulsão em dependentes)
^ Revisões
@C 💊 Tratamento da dependência de álcool (prevenção de recaída)?
| Droga | Mecanismo | Atenção
| **Naltrexona** | Antagonista opioide | Contraindicada com opioides, hepatopatia grave
| **Acamprosato** | Modulador glutamatérgico | Ajuste renal
| Dissulfiram | Aversivo | Só com adesão supervisionada
| Topiramato | Off-label | 
^ APA 2018
@C 🥶 Abstinência alcoólica: linha do tempo?
| Tempo após última dose | Manifestação
| 6–24 h | Tremor, ansiedade, taquicardia
| 12–48 h | **Convulsões**
| 12–48 h | Alucinose alcoólica (consciência preservada)
| **48–96 h** | **Delirium tremens**
= CIWA-Ar ≥ 8–10: benzodiazepínico guiado por sintoma.
^ ASAM 2020
% flow Abstinência alcoólica: linha do tempo :: 6–24 h: tremor, ansiedade, taquicardia >> 12–48 h: convulsões e alucinose >> 48–96 h: delirium tremens >> Tratar: tiamina + benzodiazepínico guiado pelo CIWA-Ar
@C 🌿 Intoxicação por cocaína: tratamento da HAS/taquicardia?
- **Benzodiazepínico** (1ª linha)
- Nitrato, BCC, fentolamina
! **Evitar betabloqueador** puro (alfa sem oposição) — controverso, mas cai em prova.
- Dor torácica: AAS + nitrato; considerar IAM por vasoespasmo/trombose
^ AHA 2008
@C 💉 Dependência de opioides: tratamento?
- **Buprenorfina** (± naloxona) ou **metadona**
- Naltrexona após desintoxicação
- Kit de **naloxona** para casa
^ ASAM 2020
@D 🆘 Avaliação de risco de suicídio: fatores?
- **Tentativa prévia** (maior preditor)
- Plano, acesso a meios letais, desesperança
- Transtorno mental, abuso de substâncias
- Homem idoso, isolamento, dor crônica, doença grave
= Perguntar diretamente **não** aumenta o risco; restringir meios; não deixar sozinho se alto risco.
^ APA 2003; Ministério da Saúde
@D 😡 Agitação psicomotora: manejo farmacológico?
- Abordagem verbal primeiro
- **Haloperidol + prometazina** IM, ou **midazolam** IM, ou olanzapina IM
- Intoxicação/abstinência: benzodiazepínico
! Evitar olanzapina IM + benzodiazepínico parenteral (depressão respiratória).
^ ABP 2019
@D 🎭 Transtornos somatoformes × factícios × simulação?
| Transtorno | Produção dos sintomas | Motivação
| Sintomas somáticos/conversivo | **Inconsciente** | Inconsciente
| Factício (Munchausen) | Consciente | **Papel de doente**
| Simulação | Consciente | **Ganho externo** (dinheiro, atestado)
^ DSM-5-TR
"""
