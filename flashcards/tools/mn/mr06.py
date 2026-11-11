TXT = r"""
## 11 👵 Geriatria e paliativos
@ Gigantes da geriatria: os 5 I
# 5 I :: Imobilidade = e suas complicações; Instabilidade = quedas; Incontinência = urinária e fecal; Insuficiência cognitiva = demência, delirium e depressão; Iatrogenia = polifarmácia
^c
@ Fragilidade: fenótipo de Fried
# FELPA :: Fraqueza de preensão; Exaustão; Lentidão da marcha; Perda de peso não intencional; Atividade física baixa
! 3 ou mais = frágil; 1–2 = pré-frágil.
^c
@ Delirium × demência × depressão
# "Início, atenção, curso" :: Delirium = agudo, atenção ruim, flutuante; Demência = insidiosa, atenção preservada no início, progressiva; Depressão = semanas, respostas "não sei", humor baixo
^c
@ Avaliação geriátrica ampla: domínios
# "Função primeiro" :: Funcional = atividades básicas (Katz) e instrumentais (Lawton); Cognição = miniexame e MoCA; Humor = escala de depressão geriátrica; Mobilidade = Timed Up and Go e quedas; Nutrição = miniavaliação nutricional; Social e fármacos = suporte e polifarmácia
^c
@ Atividades básicas de vida diária
# DEATH :: Dressing: vestir-se; Eating: alimentar-se; Ambulating: transferir-se e andar; Toileting: usar o banheiro e continência; Higiene: banho
^c
@ Atividades instrumentais de vida diária
# SHAFT :: Shopping: fazer compras; Housework: tarefas da casa; Accounting: cuidar do dinheiro; Food: preparar a comida; Transporte, telefone e tomar remédios
! As instrumentais se perdem antes das básicas.
^c
@ Quedas no idoso: fatores de risco
# CAIR :: Cognição prejudicada; Ambiente inseguro; Instabilidade de marcha e fraqueza; Remédios (sedativos, anti-hipertensivos) e redução da visão
^o
@ Incontinência urinária transitória
# DIAPPERS :: Delirium; Infecção urinária; Atrofia vaginal; Pharma: fármacos; Psicológicas: depressão; Excesso de diurese (hiperglicemia, diurético); Restrição de mobilidade; Stool: fecaloma
^c
@ Fármacos a evitar no idoso
# BAAS :: Benzodiazepínicos e hipnóticos Z; Anticolinérgicos (tricíclicos, anti-histamínicos de 1ª geração); Anti-inflamatórios; Sulfonilureias de longa ação
^o
@ Sarcopenia: três passos
# "Força, massa, desempenho" :: Provável = força baixa (preensão abaixo de 27 kg no homem e de 16 na mulher); Confirmada = força baixa + massa muscular baixa; Grave = também desempenho ruim (marcha de 0,8 m/s ou menos)
^c
@ Hipotensão ortostática
# 20 · 10 · 3 :: 20 = queda da sistólica (mmHg); 10 = queda da diastólica; 3 = minutos em pé
^c
@ Cuidados paliativos: a pergunta-surpresa
# "Eu me surpreenderia?" :: Pergunta = eu me surpreenderia se este paciente morresse em 12 meses?; Resposta "não" = indica avaliação de cuidados paliativos; Não substitui = a avaliação funcional e de sintomas
^c
@ Dor total de Cicely Saunders
# FESE :: Física; Emocional; Social; Espiritual
^c
@ Morfina: conversões e regras
# 3:1 · 1/6 :: 3:1 = dose oral para intravenosa; 1/6 = da dose diária como resgate; Laxante = desde o primeiro dia
! A constipação é o único efeito sem tolerância.
^c
@ Opioides: efeitos adversos
# SONECA :: Sedação; Obstipação; Náusea e vômito; Espasmo de esfíncter e retenção urinária; Coceira; Apneia: depressão respiratória
^o
@ Dispneia no fim de vida
# MOVA :: Morfina em dose baixa; Oxigênio só se houver hipoxemia; Ventilador de mão dirigido ao rosto; Ansiolítico se houver ansiedade
^o
@ Sedação paliativa
# "Refratário, proporcional, consentido" :: Indicação = sintoma refratário em doença terminal; Dose = a mínima que alivia; Fármaco = midazolam (primeira escolha); Não é = eutanásia: a intenção é aliviar, não abreviar a vida
^c
@ Últimas horas de vida: sinais
# "Morte iminente" :: Respiração = irregular, com pausas, ruidosa; Circulação = extremidades frias e livedo; Consciência = sonolência e delirium; Ingestão = para de comer e beber; Conduta = suspender o que não conforta e tratar sintomas
^c
@ Diretivas antecipadas de vontade
# "A vontade prevalece" :: O quê = desejos sobre cuidados para quando não puder se expressar; Vale = sobre a opinião dos familiares; Registro = no prontuário basta; Limite = não se cumpre o que contrariar o Código de Ética
^c
@ Polifarmácia
# 5 · 10 :: 5 ou mais = polifarmácia; 10 ou mais = hiperpolifarmácia; Cascata de prescrição = tratar efeito adverso com outro fármaco
^c
## 12 🧩 Psiquiatria
@ Depressão maior: critérios
# SIG E CAPS :: Sono alterado; Interesse perdido (anedonia); Guilt: culpa ou inutilidade; Energia baixa; Concentração ruim; Apetite ou peso alterados; Psicomotricidade lenta ou agitada; Suicídio: ideação
! 5 de 9 por 2 semanas, com humor deprimido ou anedonia.
^c
@ Mania: DIG FAST
# DIG FAST :: Distraibilidade; Impulsividade e indiscrição; Grandiosidade; Fuga de ideias; Atividade aumentada; Sono: menos necessidade; Taquilalia: pressão de fala
! 3 ou mais por 1 semana (4 se o humor for só irritável).
^c
@ Ansiedade generalizada
# 6 meses · 3 de 6 :: 6 meses = preocupação excessiva na maioria dos dias; 3 de 6 = inquietação, fadiga, concentração ruim, irritabilidade, tensão muscular, sono alterado
^c
@ Transtorno de pânico
# "Ataque + medo do próximo" :: Ataque = pico em 10 min com 4 ou mais sintomas; Critério = ataques inesperados recorrentes + 1 mês de preocupação ou evitação; Tratamento = inibidor de recaptação de serotonina e terapia cognitivo-comportamental
^c
@ Esquizofrenia: critérios
# "2 de 5, 6 meses" :: Sintomas = delírios, alucinações, discurso desorganizado, comportamento desorganizado, sintomas negativos; Regra = 2 ou mais por 1 mês, com pelo menos um dos três primeiros; Duração = 6 meses de alteração
^c
@ Sintomas negativos: os 5 A
# 5 A :: Afeto = embotado; Alogia = pobreza de fala; Avolição = falta de iniciativa; Anedonia = perda do prazer; Associalidade = isolamento
^c
@ Antipsicóticos: efeitos extrapiramidais no tempo
# "Horas, dias, semanas, anos" :: Horas = distonia aguda (biperideno); Dias = acatisia (propranolol); Semanas = parkinsonismo; Anos = discinesia tardia
^c
@ Síndrome neuroléptica maligna: FEVER
# FEVER :: Febre; Encefalopatia; Vitais instáveis (disautonomia); Enzimas: CK elevada; Rigidez em cano de chumbo
^c
@ Lítio: efeitos adversos
# LMNOP :: L = lítio; M = movimento: tremor fino; N = nefrogênico: diabetes insípido; O = hipotireoidismo; P = prenhez: anomalia de Ebstein
^c
@ O que eleva o nível de lítio
# DAI :: Diurético tiazídico; Anti-inflamatório; IECA e BRA
! Desidratação e dieta sem sal também.
^o
@ Abstinência alcoólica: linha do tempo
# 6-12-48-72 :: 6 = horas: tremor, ansiedade, insônia; 12 = horas (até 48): convulsões; 48 = horas (de 12 a 48): alucinose com consciência clara; 72 = horas (de 48 a 96): delirium tremens
! Benzodiazepínico guiado por sintomas + tiamina.
^c
@ Rastreio de uso nocivo de álcool: CAGE
# CAGE :: Cut down: já tentou reduzir; Annoyed: irrita-se com críticas; Guilty: sente culpa; Eye-opener: bebe ao acordar
! 2 ou mais = rastreio positivo.
^c
@ Fatores de risco na avaliação psiquiátrica: SAD PERSONS
# SAD PERSONS :: Sexo masculino; Anos: menos de 19 ou mais de 45; Depressão; Prévia: tentativa anterior; Etanol e outras drogas; Racionalidade perdida (psicose); Suporte social ausente; Organizado: plano estruturado; No spouse: sem parceiro; Sickness: doença crônica
! Ajuda a lembrar os fatores; não substitui a avaliação clínica, e a pontuação prediz mal.
^c
@ Anorexia nervosa × bulimia nervosa
# "O peso diferencia" :: Anorexia = peso baixo, medo de engordar, distorção da imagem corporal; Bulimia = peso normal ou alto, compulsão seguida de purgação; Sinais de purgação = sinal de Russell, erosão dentária, parótidas aumentadas, potássio baixo
^c
@ Transtornos de personalidade: grupos
# A-B-C :: A = estranhos: paranoide, esquizoide, esquizotípica; B = dramáticos: antissocial, borderline, histriônica, narcisista; C = ansiosos: evitativa, dependente, obsessivo-compulsiva
^c
@ Inibidores de recaptação de serotonina: os 5 S
# 5 S :: Sexual = disfunção; Sono = insônia ou sonolência; Sódio = hiponatremia no idoso; Sangramento = com anti-inflamatório ou anticoagulante; Serotoninérgica = síndrome, com outros serotoninérgicos
^o
@ Antidepressivo pelo perfil do paciente
# "Escolha pelo efeito colateral" :: Mirtazapina = sono e apetite (idoso emagrecido); Bupropiona = sem disfunção sexual, ajuda a parar de fumar, baixa o limiar convulsivo; Tricíclico = dor neuropática, mas anticolinérgico e cardiotóxico; Duloxetina e venlafaxina = dor crônica, podem subir a pressão
^c
@ TDAH: tríade
# DIH :: Desatenção; Impulsividade; Hiperatividade
! Sintomas antes dos 12 anos, em 2 ou mais ambientes.
^c
@ Transtorno bipolar: tipo I × tipo II
# "Mania × hipomania" :: Tipo I = pelo menos um episódio de mania (7 dias ou internação); Tipo II = hipomania (4 dias) + depressão maior, sem mania; Tratamento = estabilizador de humor — antidepressivo sozinho pode virar o humor
^c
@ Benzodiazepínicos no idoso: riscos
# QCD :: Quedas; Confusão; Dependência
^o
"""
