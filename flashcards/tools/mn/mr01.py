TXT = r"""
## 01 ❤️ Cardiologia
@ CHA₂DS₂-VASc
# CHA₂DS₂-VASc :: C = insuficiência cardíaca (1); H = hipertensão (1); A₂ = idade de 75 anos ou mais (2); D = diabetes (1); S₂ = AVC ou AIT prévio (2); V = doença vascular (1); A = idade de 65 a 74 anos (1); Sc = sexo feminino (1)
> Escore de Lip (2010) para estimar o risco de AVC na fibrilação atrial não valvar e decidir a anticoagulação.
! Anticoagular com 2 ou mais no homem e 3 ou mais na mulher. A diretriz europeia de 2024 usa a versão sem o sexo.
^c
@ HAS-BLED
# HAS-BLED :: H = hipertensão não controlada; A = alteração renal ou hepática (1 cada); S = AVC prévio; B = sangramento prévio; L = INR lábil; E = idade acima de 65 anos; D = drogas (antiagregante, anti-inflamatório) ou álcool (1 cada)
> Escore de Pisters (2010) para o risco de sangramento na fibrilação atrial. Serve para corrigir fatores modificáveis, não para negar o anticoagulante.
! 3 ou mais = alto risco: corrigir os fatores, não contraindicar a anticoagulação.
^c
@ Critérios de Framingham para insuficiência cardíaca
# 2 ou 1 + 2 :: Diagnóstico = 2 maiores, ou 1 maior + 2 menores; Maiores = dispneia paroxística noturna, turgência jugular, estertores, cardiomegalia, edema agudo, B3, refluxo hepatojugular; Menores = edema de tornozelo, tosse noturna, dispneia de esforço, hepatomegalia, derrame pleural, taquicardia
> Critérios clínicos do estudo de Framingham (1971), úteis onde não há ecocardiograma nem peptídeo natriurético.
^c
@ Classe funcional da NYHA
# I-II-III-IV :: I = sem sintomas nas atividades habituais; II = sintomas nos esforços habituais; III = sintomas em esforços menores que os habituais; IV = sintomas em repouso
> Classificação funcional de 1928, ainda usada para indicar tratamentos e estimar o prognóstico da insuficiência cardíaca.
^c
@ Quarteto da insuficiência cardíaca com fração reduzida
# BISA :: Betabloqueador; Inibidor da neprilisina com BRA (ou IECA); SGLT2: inibidor; Antagonista mineralocorticoide
> Os quatro pilares com redução de mortalidade na fração de ejeção reduzida (PARADIGM-HF, DAPA-HF, EMPEROR-Reduced e RALES).
! Os quatro reduzem mortalidade: iniciar cedo e em sequência rápida.
^o
@ Betabloqueadores com prova de mortalidade na insuficiência cardíaca
# CBM :: Carvedilol; Bisoprolol; Metoprolol succinato
> Só três betabloqueadores reduziram mortalidade em ensaios (COPERNICUS, CIBIS-II e MERIT-HF). Não é efeito de classe.
^c
@ Causas de descompensação da insuficiência cardíaca
# FAILURE :: Falta de adesão a remédio e dieta; Arritmia e anemia; Isquemia e infecção; Líquido e sal em excesso; Upregulation: alto débito (tireotoxicose, gestação); Rim: insuficiência renal; Embolia pulmonar
> Diante de toda descompensação, procurar o fator precipitante. Má adesão e infecção lideram a lista.
^c
@ Dor torácica: os seis diagnósticos que matam
# PET MAC :: Pulmão: embolia; Esôfago: ruptura; Tensão: pneumotórax hipertensivo; Miocárdio: infarto; Aorta: dissecção; Coração: tamponamento
> Seis causas de dor torácica a excluir antes de qualquer outra hipótese, por serem letais e tratáveis.
^c
@ Escore TIMI na síndrome coronariana sem supra
# AMERICA :: Anos: idade de 65 ou mais; Marcadores de necrose elevados; ECG com desvio de ST; Risco: 3 ou mais fatores; Isquemia: 2 ou mais crises de angina em 24 h; Coronária com estenose de 50% ou mais; AAS nos últimos 7 dias
> Escore TIMI de Antman (2000) para estratificar a síndrome coronariana sem supra de ST. Hoje divide espaço com GRACE e HEART.
! 0–2 baixo, 3–4 intermediário, 5–7 alto risco.
^c
@ Endocardite: critérios de Duke
# "2 M, ou 1 M + 3 m, ou 5 m" :: Maiores = hemoculturas típicas e imagem com vegetação, abscesso ou nova regurgitação; Menores = predisposição, febre, fenômenos vasculares, fenômenos imunológicos, cultura que não fecha critério maior; Definitivo = 2 maiores, 1 maior + 3 menores ou 5 menores
> Critérios de Duke (1994, modificados em 2000 e atualizados em 2023) para o diagnóstico de endocardite infecciosa.
^c
@ Endocardite: fenômenos vasculares × imunológicos
# "Vascular × imune" :: Vasculares = êmbolos, infartos sépticos, aneurisma micótico, hemorragia conjuntival, lesões de Janeway; Imunológicos = nódulos de Osler, manchas de Roth, glomerulonefrite, fator reumatoide
> Critérios menores de Duke. Os fenômenos vasculares vêm de êmbolos sépticos; os imunológicos, de imunocomplexos.
! Osler dói; Janeway não.
^c
@ Febre reumática: critérios maiores de Jones
# JONES :: Juntas: poliartrite migratória; O coração: cardite; Nódulos subcutâneos; Eritema marginado; Sydenham: coreia
> Critérios de Jones (revisão de 2015). O diagnóstico exige evidência de infecção estreptocócica mais 2 maiores, ou 1 maior e 2 menores.
^c
@ Pericardite aguda: diagnóstico com 2 de 4
# DADE :: Dor pleurítica que melhora sentado; Atrito pericárdico; Derrame novo; ECG com supra difuso e infra de PR
> Critérios da diretriz europeia (2015). A colchicina reduz a recorrência à metade (ensaios COPE e ICAP).
! Anti-inflamatório + colchicina por 3 meses.
^o
@ Estenose aórtica: tríade
# SAD :: Síncope; Angina; Dispneia
> Sintomas que marcam a virada do prognóstico na estenose aórtica grave e indicam a troca valvar.
! Sobrevida média sem troca valvar: angina 5 anos, síncope 3, dispneia 2.
^c
@ Hipertensão secundária: o ABCDE
# ABCDE :: Apneia do sono e aldosteronismo; Bruits: sopro renal e doença do rim; Catecolaminas, coarctação e Cushing; Drogas e dieta; Eritropoetina e endócrinas (tireoide, paratireoide)
> Investigar hipertensão secundária no jovem, no resistente e quando o início ou a piora são súbitos.
^c
@ Fibrilação atrial: via ABC
# ABC :: Anticoagular para evitar AVC; Bom controle dos sintomas (frequência ou ritmo); Comorbidades e fatores de risco tratados
> Via integrada da diretriz europeia de 2020 (Atrial fibrillation Better Care). A de 2024 a reorganizou como AF-CARE.
^c
@ Síncope de alto risco: regra de São Francisco
# CHESS :: Congestiva: insuficiência cardíaca prévia; Hematócrito abaixo de 30%; ECG anormal; Shortness of breath: dispneia; Sistólica abaixo de 90 mmHg
> San Francisco Syncope Rule (Quinn, 2004) para identificar quem tem risco de evento grave em 7 dias. A validação externa foi irregular.
^c
@ Estatina de alta intensidade
# "A 40–80, R 20–40" :: Atorvastatina = 40–80 mg; Rosuvastatina = 20–40 mg; Efeito = redução do LDL em 50% ou mais
> Dose de alta intensidade, indicada na doença aterosclerótica estabelecida e no risco muito alto.
^c
@ Hipertensão: classes de primeira linha
# ACD :: Antagonistas do sistema renina (IECA ou BRA); Canal de cálcio: bloqueadores; Diuréticos tiazídicos
> Classes com redução de eventos cardiovasculares. A maioria dos pacientes precisa de combinação já no início.
! Betabloqueador só com indicação específica. Nunca IECA junto com BRA.
^c
@ ECG: ordem de leitura
# "Faça Ritmo E Isso Será Infalível" :: Faça = Frequência; Ritmo = Ritmo; E = Eixo; Isso = Intervalos (PR, QRS, QT); Será = Sobrecargas de câmaras; Infalível = Isquemia (ST e T)
> Sequência fixa para ler todo eletrocardiograma sem pular etapas.
^of
## 02 🫁 Pneumologia
@ CURB-65 na pneumonia
# CURB-65 :: C = confusão mental; U = ureia acima de 50 mg/dL; R = frequência respiratória de 30 ou mais; B = pressão sistólica abaixo de 90 ou diastólica até 60; 65 = idade de 65 anos ou mais
> Escore da British Thoracic Society (Lim, 2003) para decidir o local de tratamento da pneumonia comunitária.
! 0–1 ambulatório, 2 internar, 3 ou mais considerar UTI.
^c
@ Escore de Wells para embolia pulmonar
# 3-3-1,5-1,5-1,5-1-1 :: 3 = sinais clínicos de trombose venosa; 3 (2) = embolia é o diagnóstico mais provável; 1,5 = frequência cardíaca acima de 100; 1,5 (2) = imobilização ou cirurgia em 4 semanas; 1,5 (3) = trombose ou embolia prévia; 1 = hemoptise; 1 (2) = câncer ativo
> Escore de Wells (2000) para a probabilidade pré-teste de embolia pulmonar, que define se o próximo passo é D-dímero ou imagem.
! Acima de 4 = provável: direto para a angiotomografia.
^c
@ Regra PERC
# HAD CLOTS :: Hormônio (estrogênio) em uso; Anos: 50 ou mais; DVT: trombose ou embolia prévia; Cuspir sangue: hemoptise; Leg: edema unilateral de perna; Oxigênio: saturação abaixo de 95%; Taquicardia de 100 ou mais; Surgery: cirurgia ou trauma em 4 semanas
> Regra de Kline (2004) para dispensar exames em quem já tem probabilidade clínica baixa.
! Só vale em baixa probabilidade clínica: todos ausentes dispensam o D-dímero.
^c
@ Tríade de Virchow
# ELH :: Estase; Lesão endotelial; Hipercoagulabilidade
> Descrita por Rudolf Virchow no século XIX. Explica todos os fatores de risco de trombose venosa.
^c
@ DPOC: gravidade pelo VEF1
# 80-50-30 :: 80 = GOLD 1: VEF1 de 80% ou mais; 50 = GOLD 2: de 50 a 79%; 30 = GOLD 3: de 30 a 49%; Abaixo de 30 = GOLD 4
> Classificação espirométrica da GOLD. Mede a obstrução, mas não decide sozinha o tratamento.
! Diagnóstico: VEF1/CVF abaixo de 0,70 depois do broncodilatador.
^c
@ DPOC: grupos A, B e E
# A-B-E :: A = 0–1 exacerbação sem internação e poucos sintomas; B = 0–1 exacerbação sem internação e muitos sintomas; E = 2 ou mais exacerbações, ou 1 com internação
> Classificação da GOLD 2023, que fundiu os antigos grupos C e D no grupo E.
! A: um broncodilatador. B e E: dois broncodilatadores de longa ação. E com eosinófilos ≥ 300: considerar corticoide inalatório.
^c
@ Exacerbação de DPOC: critérios de Anthonisen
# DVP :: Dispneia aumentada; Volume de escarro aumentado; Purulência do escarro
> Critérios de Anthonisen (1987) para decidir antibiótico na exacerbação de DPOC.
! Antibiótico se houver purulência + 1 dos outros, ou necessidade de ventilação.
^c
@ O que muda a história natural da DPOC
# PARO :: Parar de fumar; Ar: oxigênio domiciliar no hipoxêmico crônico; Reabilitação pulmonar; Operação redutora de volume em casos selecionados
> Poucas intervenções reduzem a mortalidade na DPOC. Parar de fumar é a principal.
^o
@ Oxigenoterapia domiciliar: indicações
# 55 · 88 · 56–59 :: 55 = PaO₂ de 55 mmHg ou menos; 88 = saturação de 88% ou menos; 56–59 = PaO₂ nessa faixa com cor pulmonale ou hematócrito acima de 55%
> Critérios derivados dos ensaios NOTT e MRC (1980–81), que mostraram ganho de sobrevida com oxigênio prolongado.
! Pelo menos 15 h por dia.
^c
@ Asma: controle em quatro perguntas
# DANA :: Diurnos: sintomas mais de 2 vezes por semana; Atividade limitada; Noturnos: despertar pela asma; Alívio: resgate mais de 2 vezes por semana
> Avaliação de controle da GINA, referente às últimas 4 semanas. Define se o tratamento sobe ou desce de etapa.
! 0 = controlada, 1–2 = parcialmente, 3–4 = não controlada.
^o
@ Asma grave na emergência: sinais de alarme
# CALADO :: Cianose ou saturação abaixo de 92%; Alteração de consciência; Limitação da fala: frases incompletas; Ausculta silenciosa; Débito expiratório abaixo de 33–50% do previsto; O CO₂ normal ou alto na gasometria
> Sinais de crise grave ou quase fatal. Indicam tratamento intensivo e vigilância em sala de emergência ou UTI.
! PaCO₂ "normal" na crise grave é sinal de fadiga.
^o
@ Derrame pleural exsudativo: causas
# PINTE :: Pneumonia (parapneumônico); Infarto pulmonar (embolia); Neoplasia; Tuberculose; Enfermidades autoimunes
> Depois de aplicar os critérios de Light, estas são as causas a investigar no exsudato.
^o
@ Derrame parapneumônico complicado
# 7,2 · 60 · 1000 :: 7,2 = pH abaixo disso; 60 = glicose abaixo disso (mg/dL); 1000 = LDH acima disso
> Parâmetros do líquido que indicam que o antibiótico sozinho não basta e que o derrame precisa de dreno.
! Ou pus, Gram ou cultura positivos: drenar.
^c
@ Nódulo pulmonar: sinais de malignidade
# CRESCE :: Cresce em exames seriados; Rebordo espiculado; Enfisema ou fibrose associados; Superior: lobo superior; Carga tabágica alta e idade; Extensão acima de 8 mm
> Achados que elevam a probabilidade de câncer no nódulo solitário e orientam seguimento (Fleischner), PET ou biópsia.
! Calcificação central, laminar ou em pipoca fala a favor de benigno.
^o
@ Síndrome de Löfgren
# EAF :: Eritema nodoso; Adenopatia hilar bilateral; Febre com artrite de tornozelos
> Apresentação aguda da sarcoidose, descrita por Sven Löfgren. Remite espontaneamente na maioria.
! Forma aguda da sarcoidose, de bom prognóstico.
^c
@ Apneia do sono: STOP-BANG
# STOP-BANG :: S = ronco alto (snoring); T = cansaço diurno (tired); O = apneia observada; P = pressão alta; B = IMC acima de 35; A = idade acima de 50; N = pescoço acima de 40 cm (neck); G = sexo masculino (gender)
> Questionário de Chung (2008) para rastrear apneia obstrutiva do sono, muito usado no pré-operatório.
! 3 ou mais = risco aumentado; 5 ou mais = alto risco.
^c
@ Hipertensão pulmonar: os cinco grupos
# 1 a 5 :: 1 = arterial pulmonar; 2 = por doença do coração esquerdo; 3 = por doença pulmonar ou hipóxia; 4 = tromboembólica crônica; 5 = mecanismos multifatoriais
> Classificação clínica dos simpósios mundiais. O grupo define o tratamento: vasodilatador pulmonar específico nos grupos 1 e 4.
^c
@ Tuberculose: esquema básico
# RIPE :: Rifampicina; Isoniazida; Pirazinamida; Etambutol
> Esquema básico do Ministério da Saúde, em dose fixa combinada, para adultos e adolescentes.
! 2 meses com os quatro + 4 meses de rifampicina e isoniazida.
^c
@ Efeitos adversos do esquema da tuberculose
# "Cada um com seu órgão" :: Rifampicina = suor e urina alaranjados, interações, hepatite; Isoniazida = neuropatia periférica (dar piridoxina) e hepatite; Pirazinamida = hiperuricemia, artralgia e hepatite; Etambutol = neurite óptica (visão de cores)
> Efeito adverso típico de cada fármaco. A hepatotoxicidade é comum a três deles.
^c
@ Tosse crônica com radiografia normal
# GAR :: Gotejamento pós-nasal; Asma; Refluxo gastroesofágico
> Três causas respondem pela maioria das tosses com mais de 8 semanas em não fumante com radiografia normal.
! Antes de investigar: suspender IECA e cessar o tabagismo.
^c
"""
