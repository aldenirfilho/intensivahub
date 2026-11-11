TXT = r"""
## 03 🫘 Nefrologia
@ Síndrome nefrótica: definição
# PHEL :: Proteinúria acima de 3,5 g por dia; Hipoalbuminemia; Edema; Lipídios altos
> Síndrome por perda de proteína no glomérulo (lesão do podócito). O sedimento urinário é pobre em células.
^c
@ Síndrome nefrítica: definição
# HEHO :: Hematúria com cilindros hemáticos; Edema; Hipertensão; Oligúria
> Síndrome por inflamação glomerular, de início abrupto. O modelo clássico é a glomerulonefrite pós-estreptocócica.
^c
@ Glomerulopatias com complemento baixo
# "Pobre Lúpus Me Custa Energia" :: Pobre = Pós-infecciosa; Lúpus = Lúpus; Me = Membranoproliferativa; Custa = Crioglobulinemia; Energia = Endocardite
> Dosar C3 e C4 é o primeiro passo para dividir as glomerulonefrites e estreitar o diagnóstico.
^of
@ Doença renal crônica: estágios pela filtração
# 90-60-45-30-15 :: 90 = G1: 90 ou mais, com marcador de lesão; 60 = G2: de 60 a 89; 45 = G3a: de 45 a 59; 30 = G3b: de 30 a 44; 15 = G4: de 15 a 29; Abaixo de 15 = G5
> Classificação KDIGO pela taxa de filtração, combinada à albuminúria para estimar o risco.
! Exige 3 meses de alteração.
^c
@ Doença renal crônica: categorias de albuminúria
# 30 · 300 :: A1 = abaixo de 30 mg/g; A2 = de 30 a 300 mg/g; A3 = acima de 300 mg/g
> A albuminúria prediz progressão renal e risco cardiovascular independentemente da filtração.
^c
@ O que freia a progressão da doença renal crônica
# FREIA :: Finerenona no diabético com albuminúria; Renina: IECA ou BRA na albuminúria; Evitar anti-inflamatório e contraste desnecessário; Inibidor de SGLT2; Alvo de pressão sistólica abaixo de 120–130
> Medidas com evidência de retardar a progressão (ensaios DAPA-CKD, EMPA-KIDNEY e FIDELIO-DKD).
^o
@ Complicações da doença renal crônica a rastrear
# CAMAS :: Cálcio, fósforo e PTH (distúrbio mineral e ósseo); Anemia; Metabólica: acidose; Alto potássio; Sobrecarga de volume e hipertensão
> Complicações que aparecem a partir do estágio 3 e devem ser buscadas ativamente.
^o
@ Fármacos e as arteríolas do glomérulo
# "Aferente × eferente" :: Anti-inflamatório = contrai a aferente (tira a prostaglandina); IECA e BRA = dilatam a eferente (tiram a angiotensina II); Os dois + diurético = a "tripla pancada" no rim
> A filtração depende do tônus das duas arteríolas. A combinação desses fármacos derruba a pressão de filtração.
^c
@ Nefrite intersticial aguda: tríade
# FRE :: Febre; Rash; Eosinofilia
> Reação de hipersensibilidade a fármacos na maioria dos casos. Suspender o agente é o tratamento principal.
! Tríade completa em menos de 15%. Causas: β-lactâmicos, anti-inflamatórios, inibidores de bomba de prótons.
^c
@ Acidose tubular renal: tipos
# 1-2-4 :: 1 = distal: não acidifica a urina, potássio baixo, cálculos; 2 = proximal: perde bicarbonato, potássio baixo, Fanconi; 4 = hipoaldosteronismo: potássio alto (diabético, IECA)
> Acidoses metabólicas com ânion gap normal por defeito tubular. O potássio sérico separa a tipo 4 das demais.
^c
@ Hipocalemia: o potássio urinário orienta
# "Rim poupa ou perde" :: Potássio urinário baixo = perda digestiva ou desvio para a célula; Alto com pressão alta = excesso de mineralocorticoide; Alto com pressão normal = diurético, vômitos, Bartter, Gitelman
> Primeiro passo na hipocalemia sem causa evidente: saber se o rim está perdendo potássio.
^o
@ Cálculo renal: tipos
# "Cálcio manda" :: Oxalato de cálcio = o mais comum; Estruvita = infecção por germe produtor de urease (coraliforme); Ácido úrico = radiotransparente, urina ácida; Cistina = hexagonal, hereditário
> A composição do cálculo define a prevenção. Cerca de 80% são de cálcio.
^c
@ Hematúria glomerular × urológica
# "Dismórfica × isomórfica" :: Glomerular = hemácias dismórficas, acantócitos, cilindros hemáticos, proteinúria; Urológica = hemácias isomórficas, coágulos, sem cilindros
> A morfologia das hemácias na urina indica se a hematúria vem do glomérulo ou da via urinária.
^c
@ Nefropatia por IgA × pós-estreptocócica
# "Dias × semanas" :: IgA = hematúria 1–3 dias depois da infecção, complemento normal; Pós-estreptocócica = 1–3 semanas depois da faringite (3–6 da pele), C3 baixo por até 8 semanas
> O intervalo entre a infecção e a hematúria diferencia as duas. A nefropatia por IgA é a glomerulopatia primária mais comum do mundo.
^c
@ Síndrome pulmão-rim: causas
# GAL :: Goodpasture (antimembrana basal); ANCA: vasculites; Lúpus
> Hemorragia alveolar com glomerulonefrite rapidamente progressiva. Emergência que pede imunossupressão e, em alguns casos, plasmaférese.
^o
@ Rim policístico do adulto: fora do rim
# FACHA :: Fígado com cistos; Aneurisma cerebral; Cólon: divertículos; Hérnias de parede; Atrioventricular: prolapso mitral
> Doença sistêmica, autossômica dominante (genes PKD1 e PKD2). O aneurisma cerebral é a manifestação extrarrenal mais temida.
^o
@ Diuréticos e o segmento do néfron
# "De cima para baixo" :: Túbulo proximal = acetazolamida e inibidor de SGLT2; Alça de Henle = furosemida; Túbulo distal = tiazídico; Coletor = espironolactona e amilorida (poupam potássio)
> Cada classe age em um segmento, o que explica a potência e os efeitos eletrolíticos.
^c
@ Tiazídico: efeitos metabólicos
# hiperGLUC :: G = glicose alta; L = lipídios altos; U = ácido úrico alto; C = cálcio alto; Hipo = sódio, potássio e magnésio baixos
> Efeitos metabólicos dos tiazídicos. A retenção de cálcio é útil em quem tem osteoporose ou cálculo de cálcio.
^c
@ Síndrome nefrótica: causa por perfil
# "Mínima, focal, membranosa" :: Criança = lesão mínima; Adulto jovem e negro = glomeruloesclerose segmentar e focal; Adulto mais velho e branco = membranosa (anti-PLA2R); Diabetes = a causa secundária mais comum
> A epidemiologia orienta a hipótese antes da biópsia renal.
^c
@ Síndrome nefrótica: complicações
# TIDE :: Trombose (veia renal); Infecção (pneumococo, peritonite); Dislipidemia; Eventos renais: lesão aguda
> Complicações da perda urinária de proteínas, como antitrombina e imunoglobulinas.
^o
## 04 🍬 Endocrinologia
@ Diabetes: critérios diagnósticos
# 126 · 200 · 6,5 :: 126 = glicemia de jejum (mg/dL) ou mais; 200 = 2 h depois de 75 g de glicose, ou ao acaso com sintomas; 6,5 = hemoglobina glicada (%) ou mais
> Critérios da ADA e da Sociedade Brasileira de Diabetes para o diagnóstico.
! Sem sintomas clássicos, confirmar com um segundo exame.
^c
@ Pré-diabetes
# 100 · 140 · 5,7 :: 100 = jejum de 100 a 125; 140 = 2 h do teste oral de 140 a 199; 5,7 = glicada de 5,7 a 6,4%
> Faixa de risco aumentado, em que a mudança de estilo de vida reduz a progressão (Diabetes Prevention Program).
^c
@ Complicações microvasculares do diabetes
# RNN :: Retinopatia; Nefropatia; Neuropatia
> Complicações ligadas ao tempo de doença e ao controle glicêmico (ensaios DCCT e UKPDS).
! Rastrear no diagnóstico do tipo 2 e depois de 5 anos no tipo 1.
^c
@ Antidiabéticos com benefício cardiorrenal
# "Coração e rim primeiro" :: Inibidor de SGLT2 = insuficiência cardíaca e doença renal; Agonista de GLP-1 = doença aterosclerótica e obesidade; Metformina = base, se a filtração permitir
> A escolha do antidiabético hoje parte da comorbidade, e não só da hemoglobina glicada.
^c
@ Inibidor de SGLT2: efeitos adversos
# GECA :: Genital: candidíase; Euglicêmica: cetoacidose; Contração de volume e hipotensão; Amputação e gangrena de Fournier (raros)
> Efeitos adversos da classe das gliflozinas. A cetoacidose pode ocorrer com glicemia quase normal.
! Suspender 3 dias antes de cirurgia de grande porte.
^o
@ Doença de Graves: tríade
# BOD :: Bócio difuso; Oftalmopatia; Dermopatia (mixedema pré-tibial)
> Causa mais comum de hipertireoidismo. Oftalmopatia e dermopatia são exclusivas da doença de Graves.
! Anticorpo antirreceptor de TSH positivo.
^c
@ Tireotoxicose com captação baixa
# TIFA :: Tireoidite (subaguda, pós-parto); Iodo e amiodarona; Factícia (uso de hormônio); Ativa em outro lugar: struma ovarii
> Tireotoxicose sem hiperfunção da glândula: as tionamidas não funcionam.
^o
@ Nódulo tireoidiano: suspeita no ultrassom
# MAIS :: Microcalcificações; Altura maior que a largura; Irregularidade das margens; Sólido e hipoecoico
> Características que elevam a categoria no TI-RADS e indicam punção.
^o
@ Síndrome de Cushing: achados mais específicos
# FEMP :: Fraqueza proximal; Estrias violáceas largas; Manchas roxas: equimoses fáceis; Pletora facial
> Sinais que melhor distinguem a síndrome de Cushing da obesidade comum.
^o
@ Cushing: testes de rastreio
# "2 de 3" :: Cortisol salivar da meia-noite = perda do nadir; Cortisol livre urinário de 24 h = produção total; Supressão com 1 mg de dexametasona = cortisol acima de 1,8 µg/dL não suprimiu
> Testes de primeira linha da Endocrine Society. Antes, excluir o uso de corticoide exógeno.
^c
@ Insuficiência adrenal primária × secundária
# "Pele e potássio" :: Primária = hiperpigmentação e potássio alto, ACTH alto; Secundária = pele clara e potássio normal, ACTH baixo ou normal
> Na forma primária falta também aldosterona, e o ACTH alto pigmenta a pele.
^c
@ Hiperaldosteronismo primário: quando rastrear
# HIRA :: Hipocalemia espontânea ou por diurético; Incidentaloma adrenal; Resistente: hipertensão com 3 fármacos; Apneia do sono associada
> Causa mais comum de hipertensão secundária endócrina, e subdiagnosticada.
! Relação aldosterona/renina acima de 30 com aldosterona de 15 ou mais.
^o
@ Neoplasia endócrina múltipla 1: os 3 P
# 3 P :: Paratireoide = hiperparatireoidismo (o mais comum); Pâncreas = gastrinoma e insulinoma; Pituitária = adenoma de hipófise
> Síndrome autossômica dominante por mutação do gene MEN1.
^c
@ Neoplasia endócrina múltipla 2A × 2B
# "Medular + feo" :: 2A = carcinoma medular + feocromocitoma + hiperparatireoidismo; 2B = carcinoma medular + feocromocitoma + neuromas de mucosa e hábito marfanoide; Gene = RET
> Síndromes por mutação do proto-oncogene RET. Indicam tireoidectomia profilática nos portadores.
^c
@ Hipercalcemia: causas
# CHIMPANZEES :: Cálcio em suplemento; Hiperparatireoidismo; Imobilização e iatrogenia (tiazídico, lítio); Milk-alkali: síndrome leite-álcali; Paget; Addison; Neoplasias; Zollinger-Ellison (NEM 1); Excesso de vitamina D; Excesso de vitamina A; Sarcoidose
> Lista ampla de causas de hipercalcemia. O PTH é o exame que divide o raciocínio.
! 90% dos casos: hiperparatireoidismo (ambulatório) ou câncer (internado).
^c
@ Hiperparatireoidismo primário: clínica clássica
# "Ossos, pedras, gemidos e lamentos" :: Ossos = dor óssea e osteoporose; Pedras = nefrolitíase; Gemidos = dor abdominal, constipação, pancreatite; Lamentos = depressão, fadiga, confusão
> Descrição clássica da forma sintomática. Hoje a maioria é achado assintomático em exame de rotina.
^c
@ Osteoporose pela densitometria
# −1 · −2,5 :: Até −1 = normal; De −1 a −2,5 = osteopenia; −2,5 ou menos = osteoporose
> Critério da OMS (1994) pela densitometria de coluna lombar e fêmur proximal, para mulheres na pós-menopausa e homens acima de 50 anos.
! É o T-escore. Fratura por fragilidade faz o diagnóstico sem densitometria.
^c
@ Hiperprolactinemia: causas
# FALHA :: Fármacos (antipsicóticos, metoclopramida); Adenoma (prolactinoma); Lesão da haste hipofisária; Hipotireoidismo primário; Amamentação, gravidez e insuficiência renal
> Antes de pedir ressonância, excluir gravidez, fármacos, hipotireoidismo e insuficiência renal.
^o
@ Síndrome metabólica: 3 de 5
# 3 de 5 :: Cintura = acima de 102 cm no homem e de 88 na mulher; Triglicérides = 150 ou mais; HDL = abaixo de 40 no homem e de 50 na mulher; Pressão = 130/85 ou mais; Glicemia = 100 ou mais
> Critérios do NCEP-ATP III. A definição harmonizada usa cortes de cintura por etnia.
^c
@ Insulinas: tempos de ação
# "Rápida, regular, NPH, basal" :: Ultrarrápida (lispro, asparte) = início em 10–15 min, dura 3–5 h; Regular = início em 30 min, dura 6–8 h; NPH = pico em 4–10 h, dura 12–18 h; Glargina e degludeca = sem pico, 24 h ou mais
> Perfis de ação que permitem montar o esquema basal-bolus.
^c
"""
