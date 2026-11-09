TXT = r"""
@A 📏 Técnica correta de aferição da PA no consultório?
- Repouso de **5 min**, sentado, costas apoiadas, pés no chão, bexiga vazia
- Manguito no nível do coração, bolsa cobrindo **80%** da circunferência do braço
- **3 medidas** com 1–2 min de intervalo; usar a média das 2 últimas
- 1ª consulta: medir nos **dois braços** e usar o de maior valor
! Manguito pequeno superestima a PA; braço sem apoio também eleva a medida.
^ Diretriz Brasileira de HAS 2020
@A 🎯 Classificação da PA no consultório (Diretriz Brasileira 2020)?
| Categoria | PAS | PAD
| Ótima | < 120 | < 80
| Normal | 120–129 | 80–84
| Pré-hipertensão | 130–139 | 85–89
| HAS estágio 1 | 140–159 | 90–99
| HAS estágio 2 | 160–179 | 100–109
| HAS estágio 3 | ≥ 180 | ≥ 110
! Quando PAS e PAD caem em categorias diferentes, vale a **maior**.
^ Diretriz Brasileira de HAS 2020
% zones Classificação da PA no consultório (mmHg) :: Ótima = < 120/80 | Normal = 120–129 / 80–84 | Pré-HAS = 130–139 / 85–89 | Estágio 1 = 140–159 / 90–99 | Estágio 2 = 160–179 / 100–109 | Estágio 3 = ≥ 180 / ≥ 110
@A 🧪 Exames complementares de rotina na HAS recém-diagnosticada?
- Creatinina com **TFG**, potássio, glicemia, HbA1c se indicado
- Perfil lipídico, ácido úrico
- **Urina 1** e **albuminúria** (relação albumina/creatinina)
- **ECG** de 12 derivações
= Ecocardiograma, MAPA e fundo de olho conforme suspeita.
^ Diretriz Brasileira de HAS 2020
@A 🩸 Lesões de órgão-alvo que reclassificam o risco na HAS?
- **HVE** (ECG ou eco)
- **Albuminúria** 30–300 mg/g ou TFG 30–60
- ITB < 0,9; VOP carótido-femoral > 10 m/s
- Placa carotídea
= Presença de LOA = **alto risco** cardiovascular, independentemente do estágio.
^ Diretriz Brasileira de HAS 2020
@A 💊 Combinações anti-hipertensivas preferenciais?
- IECA ou BRA + **BCC di-hidropiridínico**
- IECA ou BRA + **tiazídico** (preferir clortalidona ou indapamida)
- Triplo: IECA/BRA + BCC + tiazídico
= ❌ **!!IECA + BRA!!** (mais hipercalemia e LRA, sem benefício)
= ❌ Betabloqueador + BCC não di-hidropiridínico (bradicardia, BAV)
^ Diretriz Brasileira de HAS 2020; ONTARGET 2008
% flow Escalonamento do tratamento da HAS :: Combinação dupla em dose baixa (IECA/BRA + BCC ou tiazídico) >> Combinação dupla em dose plena >> Tripla: IECA/BRA + BCC + tiazídico >> HAS resistente: + espironolactona
@A 🤰 Anti-hipertensivos permitidos e proibidos na gestação?
| Permitidos | Contraindicados
| Metildopa | !!IECA!!
| Nifedipino de liberação lenta | !!BRA!!
| Hidralazina (aguda) | Inibidor direto da renina
| Labetalol (onde disponível) | Espironolactona
! IECA/BRA no 2º–3º trimestre: oligoâmnio, insuficiência renal fetal e malformações.
^ FEBRASGO; Diretriz Brasileira de HAS 2020
@A 👴 Alvo pressórico no idoso?
= Idoso hígido: PAS **130–139** (tolerando < 130 se sem hipotensão).
= Idoso frágil: alvo individualizado, PAS < 150 aceitável.
- Medir em pé para pesquisar **hipotensão ortostática**
! SPRINT incluiu idosos ≥ 75 anos com benefício do alvo < 120 (medida automatizada sem observador).
^ Diretriz Brasileira de HAS 2020; SPRINT 2015
@A 🌙 Padrão "non-dipper" na MAPA: o que é e o que significa?
= Queda da PA no sono **< 10%** em relação à vigília.
= Associa-se a maior risco cardiovascular, AOS, DRC, disautonomia.
! "Riser" (PA sobe à noite) tem o pior prognóstico.
^ Diretriz de MAPA/MRPA SBC
@A ⚡ Emergência × urgência hipertensiva: diferença essencial?
| | Urgência | Emergência
| Lesão aguda de órgão-alvo | Não | **Sim**
| Via | Oral | **Intravenosa**
| Local | Ambulatório/PS | UTI
| Velocidade | 24–48 h | ↓ PAM ≤ 25% na 1ª hora
! O valor da PA isolado não define emergência.
^ Diretriz Brasileira de HAS 2020
% cmp Urgência × emergência hipertensiva :: Urgência = PA muito alta SEM lesão aguda de órgão-alvo. Oral, redução em 24–48 h | Emergência = PA alta COM lesão aguda (encefalopatia, EAP, SCA, dissecção, AVC). IV, UTI, PAM -25% na 1ª hora
@A 🩺 Exceções à redução gradual na emergência hipertensiva?
- **Dissecção aórtica**: PAS < 120 e FC < 60 em até 20 min
- **Pré-eclâmpsia grave/eclâmpsia**: PAS < 160 e PAD < 110
- **Feocromocitoma**: redução rápida com alfabloqueador
- **AVC isquêmico** para trombólise: < 185/110
^ ESC 2018; Diretriz Brasileira de HAS 2020
@A 🔍 Rastreio de hiperaldosteronismo primário: quem e como?
= Indicações: HAS resistente, HAS + hipocalemia, HAS estágio 3, incidentaloma adrenal, AOS, história familiar.
= Teste: **relação aldosterona/renina** (aldosterona > 15 ng/dL e relação elevada).
- Corrigir hipocalemia antes
- Suspender espironolactona 4–6 semanas
! Betabloqueador causa falso-positivo (↓ renina); IECA/BRA e diuréticos, falso-negativo.
^ Endocrine Society 2016
@A 💊 Efeitos adversos clássicos dos anti-hipertensivos?
| Droga | Efeito
| IECA | Tosse seca, angioedema, hipercalemia
| BCC di-hidropiridínico | Edema maleolar, cefaleia, rubor
| Tiazídico | Hiponatremia, hipocalemia, hiperuricemia, hiperglicemia
| Espironolactona | Hipercalemia, ginecomastia
| Clonidina | Rebote na suspensão abrupta
| Hidralazina | Lúpus induzido, taquicardia reflexa
^ Farmacologia clínica
@A 🩺 Edema maleolar por anlodipino: como resolver?
= Mecanismo: vasodilatação **arteriolar** sem venodilatação → ↑ pressão capilar.
- Reduzir dose ou associar **IECA/BRA** (venodilatação compensatória)
- Diurético é pouco eficaz
^ Farmacologia clínica
@A 🧂 Medidas não farmacológicas com maior redução de PAS?
| Medida | ↓ PAS aproximada
| Dieta DASH | ~11 mmHg
| Perda de peso (por 10 kg) | 5–20 mmHg
| Restrição de sódio (< 2 g/dia) | ~5–6 mmHg
| Exercício aeróbico | ~5–8 mmHg
| Moderar álcool | ~4 mmHg
^ Diretriz Brasileira de HAS 2020; DASH 1997
@A 🫀 Critérios eletrocardiográficos clássicos de HVE?
- **Sokolow-Lyon**: S(V1) + R(V5 ou V6) ≥ 35 mm
- **Cornell**: R(aVL) + S(V3) > 28 mm (homem) ou > 20 mm (mulher)
- R(aVL) ≥ 11 mm
! ECG tem baixa sensibilidade; o eco é mais sensível.
^ Diretriz de ECG SBC
@A 🧒 HAS no jovem: quando pensar em coarctação da aorta?
- PA nos membros superiores **> membros inferiores** (> 20 mmHg)
- Pulsos femorais **diminuídos e atrasados**
- Sopro interescapular
- RX: costelas com erosão inferior (sinal de Roesler), "sinal do 3"
^ ESC Congenital 2020
@A 🌡️ Feocromocitoma: tríade e diagnóstico?
= Tríade: **cefaleia + sudorese + palpitações** com HAS paroxística ou sustentada.
= Diagnóstico: **metanefrinas plasmáticas livres** ou urinárias fracionadas.
= Pré-operatório: **alfabloqueio** (doxazosina/fenoxibenzamina) por 10–14 dias, depois betabloqueador.
! !!Nunca betabloqueador antes do alfa!!: estímulo alfa sem oposição → crise hipertensiva.
^ Endocrine Society 2014
@A 😴 AOS e HAS resistente: qual a relação?
= AOS é uma das causas secundárias **mais comuns** de HAS resistente.
- Padrão non-dipper, roncos, sonolência, obesidade, pescoço largo
- Rastrear com **STOP-BANG**; diagnóstico por polissonografia
= CPAP reduz modestamente a PA (~2–3 mmHg).
^ Diretriz Brasileira de HAS 2020
@B 💊 Quais betabloqueadores têm benefício comprovado na ICFEr?
- **Carvedilol**
- **Bisoprolol**
- **Metoprolol succinato** (liberação prolongada)
- Nebivolol (idosos, SENIORS)
! Atenolol e propranolol **não** têm evidência na ICFEr.
^ ESC 2021
@B ⚠️ Contraindicações e cuidados com espironolactona na IC?
- Evitar se **K > 5,0** ou TFG < 30
- Monitorar K e creatinina em 1 semana, 4 semanas e periodicamente
- Suspender se K > 5,5
! Associação com IECA + suplemento de K + AINE = hipercalemia grave.
^ RALES 1999; ESC 2021
@B 💧 Diurético na ICFEr: reduz mortalidade?
= **Não** reduz mortalidade: alivia **congestão** e sintomas.
= Usar a menor dose que mantenha euvolemia.
! Hidroclorotiazida associada à furosemida (bloqueio sequencial do néfron) em refratários.
^ ESC 2021
@B 🔋 Indicações de CDI na prevenção primária da IC?
= ICFEr com FEVE **≤ 35%** e NYHA II–III, após ≥ 3 meses de terapia otimizada, expectativa de vida > 1 ano.
- Mais forte na cardiopatia **isquêmica** (> 40 dias pós-IAM)
! DANISH: benefício menor na cardiomiopatia não isquêmica.
^ ESC 2021; DANISH 2016
@B ⚡ Indicações de ressincronização (TRC)?
= FEVE **≤ 35%**, ritmo sinusal, sintomático apesar de terapia otimizada e:
- **BRE com QRS ≥ 150 ms**: maior benefício (classe I)
- BRE com QRS 130–149 ms: benefício
- Sem BRE: benefício menor
^ ESC 2021
@B 🩸 Ferro na IC: quando repor?
= Deficiência de ferro: **ferritina < 100** ou ferritina 100–299 com **saturação de transferrina < 20%**.
= Repor **ferro IV** (carboximaltose ou derisomaltose) em ICFEr/ICFElr sintomática.
- Melhora sintomas e reduz hospitalizações (AFFIRM-AHF, IRONMAN)
! Ferro oral não funciona na IC (IRONOUT-HF).
^ ESC 2023
@B 💉 Ajuste do betabloqueador na IC descompensada?
= Perfil **B**: geralmente **manter** (suspender aumenta mortalidade).
= Choque cardiogênico ou perfil C com baixo débito: reduzir/suspender.
^ SBC 2018; ESC 2021
@B 🫀 ICFEp: o que reduz desfechos?
- **iSGLT2**: EMPEROR-Preserved e DELIVER (↓ hospitalização)
- Controle de PA, FA, obesidade, isquemia
- Diurético para congestão
- Finerenona (FINEARTS-HF) e semaglutida/tirzepatida em obesos (STEP-HFpEF, SUMMIT)
! IECA/BRA/betabloqueador não mostraram redução de mortalidade na ICFEp.
^ ESC 2023; FINEARTS-HF 2024
@B 🔄 Como iniciar sacubitril-valsartana em paciente com IECA?
= Suspender o IECA e aguardar **36 h** (risco de angioedema).
= Vindo de BRA: trocar diretamente.
- Dose inicial 24/26 ou 49/51 mg 12/12 h, titulando até 97/103 mg
! Contraindicado com histórico de angioedema.
^ PARADIGM-HF 2014
@B 📈 Classificação funcional NYHA?
| Classe | Sintomas
| I | Sem limitação
| II | Sintomas com atividades habituais
| III | Sintomas com atividades **menores** que as habituais
| IV | Sintomas em **repouso**
^ NYHA
@B 🔠 Estágios ACC/AHA da IC?
| Estágio | Descrição
| A | Fatores de risco, sem doença estrutural
| B | Doença estrutural, sem sintomas
| C | Doença estrutural com sintomas atuais ou prévios
| D | IC refratária, avançada
! O paciente **não volta** de estágio (diferente da NYHA).
^ AHA/ACC 2022
% zones Estágios ACC/AHA da IC :: A = Risco, sem lesão | B = Lesão estrutural, sem sintomas | C = Sintomas atuais ou prévios | D = Avançada, refratária
@B 🧬 Causas de cardiomiopatia dilatada não isquêmica a investigar?
- **Álcool**, cocaína, anfetaminas
- Quimioterapia (antraciclinas, trastuzumabe)
- Taquicardiomiopatia
- **Doença de Chagas** (Brasil)
- Miocardite, periparto, genética (titina, lamina)
- Endocrinopatias (tireoide, feocromocitoma)
^ ESC 2023 cardiomiopatias
@B 🪲 Cardiopatia chagásica crônica: achados típicos?
- ECG: **BRD + bloqueio divisional anterossuperior esquerdo**
- Arritmias ventriculares, bradiarritmias, morte súbita
- **Aneurisma apical** de VE e trombo
- Tromboembolismo
= Escore de Rassi para prognóstico.
! Benznidazol na forma crônica estabelecida **não** reduziu eventos (BENEFIT).
^ Diretriz Brasileira de Chagas 2023; BENEFIT 2015
% cmp Cardiopatia chagásica crônica :: ECG = BRD + BDAS, arritmia ventricular, BAV | Estrutura = Aneurisma apical, trombo, disfunção sistólica | Desfechos = Morte súbita, IC, embolia
@B ⚖️ Efeitos dos iSGLT2 que o clínico deve antecipar?
- Queda inicial da **TFG** (até 30%, hemodinâmica, esperada)
- **Infecção genital** micótica
- **Cetoacidose euglicêmica** (suspender 3 dias antes de cirurgia)
- Depleção de volume com diurético
^ ESC 2021; ADA 2025
"""
