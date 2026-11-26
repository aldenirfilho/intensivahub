TXT = r"""
## 10 🎗️ Oncologia
@ Câncer de pulmão: tratamento pelo tipo
# Pequenas × não pequenas :: Pequenas células = quimio e radioterapia (muito sensível, mas recidiva); Não pequenas inicial = cirurgia; Mutação de EGFR ou ALK = terapia-alvo (adenocarcinoma, muitas vezes em não fumante); PD-L1 alto = imunoterapia
> Abordagem por histologia e biologia molecular. Pesquisar alterações moleculares em todo adenocarcinoma avançado.
^c
@ Câncer de mama: fatores de risco
# Estrogênio e genes :: Hormonal = menarca precoce, menopausa tardia, nuliparidade, primeira gestação após os 30 anos; Exposição = terapia hormonal combinada, álcool, obesidade após a menopausa; Genético = BRCA1, BRCA2 e história familiar; Outros = radioterapia no tórax na juventude, mama densa, hiperplasia atípica
> Maior exposição ao estrogênio ao longo da vida aumenta o risco. Amamentação e atividade física protegem.
^c
@ Câncer colorretal: direito × esquerdo
# Anemia × obstrução :: Cólon direito = anemia ferropriva, massa palpável, sangue oculto; Cólon esquerdo = mudança do hábito intestinal, fezes em fita, obstrução; Reto = sangue vivo, tenesmo, evacuação incompleta; Anemia ferropriva no homem ou na mulher após a menopausa = colonoscopia
> A localização muda a apresentação: o cólon direito é largo e o conteúdo líquido, então o tumor sangra sem obstruir.
^c
@ Câncer gástrico: sinais de doença avançada
# Linfonodos e implantes :: Virchow = linfonodo supraclavicular esquerdo; Irmã Maria José = nódulo umbilical; Krukenberg = metástase em ovário; Prateleira de Blumer = implante no fundo de saco ao toque retal; Leser-Trélat = surgimento súbito de muitas ceratoses seborreicas
> Sinais com nome próprio que indicam doença disseminada e mudam a intenção do tratamento.
^c
@ Hepatocarcinoma: diagnóstico sem biópsia
# Realce e lavagem :: Quem = cirrótico (ou portador de hepatite B) com nódulo de 1 cm ou mais; Imagem = realce na fase arterial com lavagem na fase portal ou tardia (LI-RADS 5); Biópsia = só se a imagem não for típica; Alfafetoproteína = ajuda, mas não diagnostica sozinha
> Critério por imagem aceito no fígado cirrótico, dispensando a biópsia. O rastreio é ultrassom a cada 6 meses.
^c
@ Câncer de pâncreas: pistas
# CID-T :: Courvoisier-Terrier: vesícula palpável e indolor; Icterícia indolor progressiva; Diabetes de início recente e perda de peso no idoso; Trousseau: tromboflebite migratória
> Adenocarcinoma da cabeça do pâncreas. O CA 19-9 serve para seguimento, não para diagnóstico nem rastreio.
^o
@ Carcinoma de células renais
# HDM :: Hematúria; Dor no flanco; Massa palpável
> Tríade clássica, presente em menos de 10%; hoje a maioria é achado de imagem. Paraneoplásicas: policitemia, hipercalcemia, febre, disfunção hepática sem metástase (Stauffer).
! Varicocele à esquerda que não esvazia deitado: pensar em trombo na veia renal.
^o
@ Câncer de próstata: rastreio
# Decisão compartilhada :: Quem discutir = homens de 50 a 69 anos (a partir dos 45 se negro ou com história familiar); Exame = PSA (com ou sem toque retal); Ministério da Saúde = não recomenda rastreio populacional; Risco do rastreio = sobrediagnóstico e tratamento de tumores indolentes
> Tema com recomendações divergentes entre sociedades e governo. A decisão deve ser individual e informada.
^c
@ Síndromes paraneoplásicas neurológicas
# O anticorpo aponta o tumor :: Anti-Hu = câncer de pulmão de pequenas células, encefalomielite e neuropatia sensitiva; Anti-Yo = ovário e mama, degeneração cerebelar; Anti-NMDA = teratoma de ovário, encefalite com psicose e discinesias; Anti-canal de cálcio = Lambert-Eaton, câncer de pulmão de pequenas células
> Quadros neurológicos que podem preceder o diagnóstico do câncer em meses.
^c
@ Síndrome de lise tumoral: critérios de Cairo-Bishop
# 8 · 6 · 4,5 · 7 :: Ácido úrico = 8 mg/dL ou mais; Potássio = 6 mEq/L ou mais; Fósforo = 4,5 mg/dL ou mais; Cálcio = 7 mg/dL ou menos; Lise clínica = laboratorial + lesão renal, arritmia ou convulsão
> Lise laboratorial: 2 ou mais alterações entre 3 dias antes e 7 dias depois da quimioterapia. Risco alto em linfomas agressivos e leucemias com muitos blastos.
^c
@ Câncer e trombose: escore de Khorana
# Khorana :: Sítio muito alto = estômago e pâncreas (2 pontos); Sítio alto = pulmão, linfoma, ginecológico, bexiga, testículo (1); Plaquetas = 350 mil ou mais (1); Hemoglobina = abaixo de 10 g/dL ou uso de eritropoetina (1); Leucócitos = acima de 11 mil (1); IMC = 35 ou mais (1)
> Estima o risco de trombose no paciente ambulatorial em quimioterapia. Com 2 pontos ou mais, considerar profilaxia.
^c
@ Síndrome carcinoide
# FLUSH :: Flushing: rubor facial; Lesão valvar do lado direito (tricúspide e pulmonar); Urina com ácido 5-hidroxi-indolacético alto; Sibilância (broncoespasmo); Hipermotilidade: diarreia
> Tumor neuroendócrino do intestino com metástase hepática. Tratamento com análogos da somatostatina.
^o
@ Câncer de cabeça e pescoço: fatores de risco
# Tabaco, álcool e vírus :: Tabaco e álcool = sinergia, carcinoma espinocelular de boca, laringe e faringe; HPV 16 = orofaringe (amígdala, base da língua), melhor prognóstico; Epstein-Barr = nasofaringe; Sinal de alerta = rouquidão por mais de 3 semanas ou úlcera oral que não cicatriza
> Rouquidão persistente e úlcera que não fecha pedem laringoscopia e biópsia.
^c
@ Câncer de mama: tamoxifeno × inibidor de aromatase
# Pré × pós-menopausa :: Tamoxifeno = pré-menopausa (também serve na pós); Tamoxifeno, riscos = trombose e câncer de endométrio; Inibidor de aromatase = pós-menopausa (anastrozol, letrozol, exemestano); Inibidor, riscos = osteoporose e artralgia
> Hormonioterapia dos tumores com receptor hormonal positivo, por 5 a 10 anos.
^c
@ Terapias-alvo: efeitos marcantes
# Cada alvo, um efeito :: Anti-EGFR (cetuximabe, erlotinibe) = erupção acneiforme e hipomagnesemia; Anti-VEGF (bevacizumabe) = hipertensão, proteinúria, sangramento e perfuração intestinal; Anti-HER2 (trastuzumabe) = disfunção cardíaca reversível; Imatinibe = edema e retenção hídrica
> Toxicidades diferentes das quimioterapias clássicas. A erupção do anti-EGFR costuma indicar boa resposta.
^c
@ Nódulo pulmonar sólido incidental: Fleischner
# 6 · 8 mm :: Abaixo de 6 mm = sem seguimento no baixo risco (opcional em 12 meses no alto risco); 6 a 8 mm = tomografia em 6 a 12 meses; Acima de 8 mm = tomografia em 3 meses, PET-CT ou biópsia; Não vale para = rastreio de câncer, menores de 35 anos ou quem tem câncer
> Recomendações da Sociedade Fleischner (2017) para nódulo achado por acaso.
^c
@ Síndrome de Lynch: critérios de Amsterdam II
# 3-2-1 :: 3 = três familiares com câncer do espectro de Lynch, um deles parente de 1º grau dos outros dois; 2 = duas gerações seguidas afetadas; 1 = um diagnóstico antes dos 50 anos; Exclusão = polipose adenomatosa familiar
> Critérios clínicos. Hoje se pesquisa instabilidade de microssatélites ou imuno-histoquímica em todo câncer colorretal.
^c
@ Sangramento depois da menopausa
# 4 mm :: Regra = todo sangramento após a menopausa é câncer de endométrio até prova em contrário; Endométrio de 4 mm ou menos no ultrassom transvaginal = risco baixo; Acima de 4 mm = biópsia de endométrio; Sangramento persistente = biópsia mesmo com endométrio fino
> Obesidade, tamoxifeno e estrogênio sem progestágeno aumentam o risco de câncer de endométrio.
^c
@ Cânceres curáveis só com quimioterapia
# Linfoma, leucemia, germinativo :: Linfomas = Hodgkin e difuso de grandes células B; Leucemias agudas = sobretudo na criança; Tumor de células germinativas = testículo, mesmo metastático; Coriocarcinoma gestacional = metotrexato
> Tumores muito sensíveis à quimioterapia, em que a intenção é curar mesmo com doença avançada.
^c
@ Câncer causado por infecção
# Vírus e bactérias :: HPV = colo uterino, orofaringe, ânus, pênis; Hepatites B e C = hepatocarcinoma; Helicobacter pylori = adenocarcinoma gástrico e linfoma MALT; Epstein-Barr = Burkitt, nasofaringe, Hodgkin; HTLV-1 = leucemia/linfoma de células T do adulto; HHV-8 = sarcoma de Kaposi
> Cânceres que podem ser prevenidos com vacina (HPV, hepatite B) ou tratando a infecção.
^c

## 11 👵 Geriatria e paliativos
@ Delirium: Confusion Assessment Method (CAM)
# 1 + 2 + (3 ou 4) :: 1 = início agudo e curso flutuante; 2 = desatenção; 3 = pensamento desorganizado; 4 = alteração do nível de consciência
> Instrumento de Inouye (1990) para diagnosticar delirium na enfermaria e no pronto-socorro: exige 1 e 2, mais 3 ou 4.
^c
@ Delirium: tratamento
# Causa e ambiente :: Primeiro = procurar e tratar a causa (infecção, fármaco, dor, retenção urinária, distúrbio metabólico); Ambiente = orientação, óculos e aparelho auditivo, sono, mobilização; Antipsicótico = haloperidol em dose baixa só se agitação perigosa; Benzodiazepínico = só na abstinência de álcool ou de benzodiazepínico
> A forma hipoativa é a mais comum e tem pior prognóstico. Antipsicótico não previne nem encurta o delirium.
^c
@ Mini-Exame do Estado Mental: cortes pela escolaridade
# 20 · 25 · 26,5 · 28 · 29 :: Analfabeto = 20; 1 a 4 anos de estudo = 25; 5 a 8 anos = 26,5; 9 a 11 anos = 28; 12 anos ou mais = 29
> Pontos de corte de Brucki e colaboradores (2003). Abaixo do valor sugere déficit cognitivo e exige avaliação completa.
^c
@ Depressão no idoso: Escala de Depressão Geriátrica
# GDS-15 :: Itens = 15 perguntas de sim ou não; Corte = acima de 5 pontos sugere depressão; 11 ou mais = depressão grave provável; Uso = rastreio, não diagnóstico
> Instrumento validado no Brasil. No idoso a depressão costuma vir com queixas físicas e cognitivas.
^c
@ Teste Timed Up and Go
# 12 segundos :: Tarefa = levantar da cadeira, andar 3 metros, voltar e sentar; Normal = até 10 segundos; Acima de 12 = risco maior de quedas; Acima de 20 = dependência na mobilidade
> Teste rápido de mobilidade e risco de quedas na consulta.
^c
@ Lesão por pressão: estágios
# 1 a 4 :: 1 = eritema que não clareia, pele íntegra; 2 = perda parcial da pele (bolha ou erosão rasa); 3 = perda total da pele com gordura visível; 4 = exposição de músculo, tendão ou osso
> Classificação NPIAP (2016). Também existem a lesão não classificável e a lesão tissular profunda.
^c
@ Escala de Braden
# 6 domínios :: Domínios = percepção sensorial, umidade, atividade, mobilidade, nutrição, fricção e cisalhamento; Pontuação = de 6 a 23; Risco = 18 ou menos; Risco alto = 12 ou menos
> Avaliação do risco de lesão por pressão na admissão e periodicamente.
^c
@ Imobilidade: complicações
# TÓPICOS :: Tromboembolismo venoso; Óssea: osteoporose; Pressão: lesão de pele; Infecção urinária e pneumonia; Constipação e fecaloma; Ortostática: hipotensão; Sarcopenia e contraturas
> Complicações do idoso acamado. Mobilização precoce é a melhor prevenção.
^o
@ Incontinência urinária: os tipos
# Esforço, urgência, transbordamento :: Esforço = perde ao tossir ou rir, fisioterapia do assoalho pélvico; Urgência = bexiga hiperativa, treino vesical e antimuscarínico ou mirabegrona; Transbordamento = retenção com resíduo alto (próstata, bexiga neurogênica), tratar a obstrução; Funcional = barreira física ou cognitiva para chegar ao banheiro
> Antimuscarínicos pioram a cognição do idoso: preferir mirabegrona.
^c
@ Hiperplasia prostática: tratamento
# Alfa × 5-alfa :: Alfabloqueador = tansulosina, alívio em dias (hipotensão postural); Inibidor da 5-alfa-redutase = finasterida, próstata acima de 30 a 40 mL, efeito em meses; PSA = cai à metade com finasterida; Cirurgia = retenção recorrente, cálculo vesical, hidronefrose
> A combinação dos dois reduz a progressão nas próstatas grandes.
^c
@ Constipação por opioide
# Laxante sempre :: Regra = prescrever laxante junto com o opioide; Escolha = estimulante (bisacodil, sene) + osmótico (lactulose, macrogol); Refratária = antagonista periférico (metilnaltrexona, naloxegol); Excluir = fecaloma e obstrução
> Efeito adverso que não sofre tolerância com o tempo.
^c
@ Escala de Edmonton (ESAS)
# 9 sintomas :: Sintomas = dor, cansaço, náusea, depressão, ansiedade, sonolência, apetite, bem-estar, falta de ar; Pontuação = de 0 a 10 cada; Uso = rastreio e acompanhamento em cuidados paliativos; Quem responde = de preferência o próprio paciente
> Avaliação de sintomas em cuidados paliativos, repetida para medir resposta ao tratamento.
^c
@ Ronco da morte
# Escopolamina e posição :: Causa = secreção na via aérea de quem não consegue engolir; Medidas = decúbito lateral, cabeceira elevada, reduzir hidratação; Fármaco = escopolamina (hioscina) ou atropina sublingual; Aspiração = evitar de rotina
> Sinal de morte iminente que incomoda mais a família que o paciente: acolher e explicar.
^c
@ Desnutrição no idoso
# 5% em 6 meses :: Perda de peso = 5% em 6 meses (ou 10% em 1 ano) é relevante; Triagem = Mini Avaliação Nutricional (MAN); Causas = doença, depressão, dentes, fármacos, isolamento, pobreza; Conduta = suplemento oral e tratar a causa
> A desnutrição aumenta quedas, infecções e mortalidade no idoso.
^c
@ Vacinas do idoso
# Gripe, pneumo, zóster :: Influenza = anual; Pneumocócica = conjugada (VPC13, 15 ou 20) e polissacarídica (VPP23), conforme o esquema; Herpes-zóster = vacina recombinante a partir dos 50 anos; dT = reforço a cada 10 anos (dTpa se contato com bebê)
> Calendário do idoso (SBIm e Ministério da Saúde). Confira a disponibilidade de cada vacina no SUS.
^c
@ Cascata de prescrição
# Remédio para efeito de remédio :: Anlodipino = edema → furosemida; IECA = tosse → antitussígeno; Metoclopramida = parkinsonismo → levodopa; Anti-inflamatório = pressão alta → anti-hipertensivo
> Iatrogenia comum: o efeito adverso é interpretado como doença nova e tratado com outro remédio.
^c
@ Escala Clínica de Fragilidade
# 1 a 9 :: 1 a 3 = robusto a bem controlado; 4 = vulnerável (lento, cansa fácil); 5 a 6 = fragilidade leve a moderada; 7 a 8 = fragilidade grave a muito grave; 9 = doente terminal
> Escala de Rockwood (versão de 9 pontos), baseada em julgamento clínico. Prediz mortalidade e ajuda a decidir intensidade de tratamento.
^c
@ Critérios STOPP/START
# Parar × começar :: STOPP = medicamentos potencialmente inapropriados (benzodiazepínico, anticolinérgico, anti-inflamatório na DRC); START = omissões de tratamento indicado; Exemplos START = estatina, anticoagulante na FA, IECA na IC, vitamina D com cálcio; Uso = revisão de medicação no idoso
> Critérios europeus (versão 3, de 2023). Complementam os critérios de Beers.
^c
@ Via subcutânea em cuidados paliativos
# Pode × não pode :: Podem = morfina, midazolam, haloperidol, escopolamina, metoclopramida, ondansetrona, dexametasona, furosemida, ceftriaxona; Não usar = diazepam, fenitoína, clorpromazina (irritantes); Vantagem = conforto, sem acesso venoso; Hidratação = até cerca de 1.500 mL por dia (hipodermóclise)
> Via de escolha em paliativos quando a via oral não é possível.
^c
@ Hipotensão ortostática: tratamento
# SALVE :: Sal e água liberados (se não houver IC); Ajustar ou suspender fármacos (alfabloqueador, diurético, nitrato, antidepressivo); Levantar em etapas; Vestes compressivas (meia e cinta abdominal); Elevar a cabeceira à noite
> Medidas não farmacológicas primeiro; depois fludrocortisona ou midodrina.
^o

## 12 🧩 Psiquiatria
@ Síndrome serotoninérgica: critérios de Hunter
# Clônus manda :: Clônus espontâneo = basta; Clônus induzível ou ocular = com agitação ou sudorese; Tremor = com reflexos aumentados; Hipertonia = com temperatura acima de 38 °C e clônus
> Critérios em quem usou serotoninérgico. Começa em horas, com clônus e reflexos vivos, ao contrário da síndrome neuroléptica maligna.
^c
@ Depressão: duração do tratamento
# 4–6 semanas · 6–12 meses :: Avaliar resposta = em 4 a 6 semanas na dose adequada; Primeiro episódio = manter de 6 a 12 meses após a remissão; 2 episódios = 2 anos ou mais; 3 ou mais, ou graves = considerar tempo indefinido
> Parar cedo é a principal causa de recaída. A retirada deve ser gradual.
^c
@ Depressão resistente
# 2 falhas :: Definição = sem resposta a 2 antidepressivos em dose e tempo adequados; Antes = checar adesão, diagnóstico (bipolaridade) e comorbidades; Potencializar = lítio ou antipsicótico atípico (aripiprazol, quetiapina); Outras opções = trocar de classe, eletroconvulsoterapia, escetamina
> Cerca de um terço não remite com os primeiros tratamentos (STAR*D).
^c
@ Eletroconvulsoterapia: indicações
# CRISE :: Catatonia; Risco de suicídio iminente; Inanição: recusa alimentar; Sintomas psicóticos na depressão grave; Esgotadas as opções (refratária) e gestação com quadro grave
> A eletroconvulsoterapia é o tratamento mais eficaz para a depressão grave. O efeito adverso principal é amnésia transitória.
^o
@ Síndrome de descontinuação de antidepressivo
# FINISH :: Flu-like: sintomas gripais; Insônia e sonhos vívidos; Náusea; Instabilidade e tontura; Sensoriais: parestesias e choques; Hiperexcitação: ansiedade e irritabilidade
> Mais comum com paroxetina e venlafaxina, de meia-vida curta. Retirar aos poucos; a fluoxetina raramente causa.
^c
@ Transtorno bipolar: o remédio pela fase
# Mania × depressão × manutenção :: Mania = lítio, valproato ou antipsicótico atípico, e suspender antidepressivo; Depressão bipolar = quetiapina, lurasidona ou lamotrigina; Manutenção = lítio (reduz suicídio), lamotrigina para prevenir depressão; Evitar = antidepressivo isolado (vira mania)
> Escolha do tratamento pela fase da doença.
^c
@ Lítio: monitorização
# 0,6–1,2 · 1,5 :: Litemia = 0,6 a 1,2 mEq/L (manutenção de 0,6 a 0,8); Toxicidade = acima de 1,5; Coleta = 12 h depois da última dose; Exames = TSH, creatinina e cálcio a cada 6 a 12 meses
> Faixa terapêutica estreita. Na gestação há risco (baixo) de anomalia de Ebstein.
^c
@ Valproato: efeitos adversos
# HEPAT :: Hepatotoxicidade; Engorda; Pancreatite; Amônia alta: encefalopatia; Teratogenicidade (tubo neural) e trombocitopenia
> Evitar em mulheres em idade fértil sem contracepção eficaz.
^o
@ Carbamazepina: efeitos adversos
# Sódio, sangue e pele :: Hiponatremia = SIADH; Sangue = leucopenia e, raramente, agranulocitose ou aplasia; Pele = Stevens-Johnson (HLA-B*15:02 em asiáticos); Indutor enzimático = reduz anticoncepcional e varfarina e acelera o próprio metabolismo
> Monitorar sódio e hemograma. Muitas interações por indução do citocromo P450.
^c
@ Antipsicóticos: monitorização metabólica
# Basal, 12 semanas, anual :: O que medir = peso e IMC, cintura, pressão, glicemia e lipídios; Quando = antes de iniciar, em 12 semanas e depois anual (peso mensal no início); Maior risco = clozapina e olanzapina; Menor risco = aripiprazol, ziprasidona, lurasidona
> Consenso ADA/APA (2004). Síndrome metabólica é a principal causa de morte precoce na esquizofrenia.
^c
@ Abstinência alcoólica: escala CIWA-Ar
# 8 · 15 :: Escala = CIWA-Ar com 10 itens (máximo de 67); Até 8 a 10 = leve, benzodiazepínico conforme os sintomas; 10 a 15 = moderada, benzodiazepínico; Acima de 15 = grave, doses maiores e monitorização
> Tratamento guiado por sintomas. Diazepam ou clordiazepóxido; lorazepam na hepatopatia grave; tiamina antes da glicose.
^c
@ Opioides: intoxicação × abstinência
# Miose × midríase :: Intoxicação = miose, bradipneia, sonolência, naloxona; Abstinência = midríase, piloereção, rinorreia, lacrimejamento, bocejos, diarreia; Gravidade = a abstinência é muito desconfortável, mas raramente fatal; Tratamento = metadona ou buprenorfina, clonidina para os sintomas
> Quadros opostos na clínica. A naloxona pode precipitar abstinência no dependente.
^c
@ Tabagismo: tratamento farmacológico
# Reposição, bupropiona, vareniclina :: Reposição de nicotina = adesivo + goma ou pastilha (combinar é melhor); Bupropiona = evitar em convulsão e transtorno alimentar; Vareniclina = a mais eficaz isolada (no EAGLES, segura também em doença psiquiátrica); Sempre = com abordagem comportamental
> Medicação dobra ou triplica a chance de parar de fumar.
^c
@ Insônia: higiene do sono e controle de estímulos
# SONO :: Sair da cama se não dormir em 20 minutos; Os mesmos horários todos os dias; Nada de telas, cafeína e álcool à noite; Ocupar a cama só para dormir e para sexo
> A terapia cognitivo-comportamental para insônia é a primeira linha. Evitar benzodiazepínico crônico.
^o
@ Sintoma sem explicação: somático, factício ou simulação
# Intenção e ganho :: Sintomas somáticos = sofrimento real, sintomas não intencionais; Factício = produz sintomas de propósito para ser paciente (Munchausen); Simulação = produz sintomas para ganho externo (dinheiro, afastamento); Conversivo = déficit neurológico sem causa orgânica, não intencional
> O que separa os quadros é a intenção e o tipo de ganho.
^c
@ Risco de suicídio: conduta
# Perguntar não induz :: Perguntar = diretamente sobre a ideação, o que não aumenta o risco; Risco alto = plano, meios, intenção ou tentativa recente → observação contínua e internação; Restringir meios = medicamentos, armas, pesticidas; Seguimento = contato próximo depois da alta (período de maior risco)
> Avaliação e manejo do risco de suicídio na prática clínica.
^c
@ Transtornos de ansiedade: tratamento
# ISRS e terapia :: Primeira linha = ISRS ou IRSN (sertralina, escitalopram, venlafaxina) + TCC; Início = dose baixa e subir aos poucos (a ansiedade pode piorar no começo); Benzodiazepínico = só por pouco tempo; Alternativas = pregabalina (ansiedade generalizada), buspirona
> Tratamento de ansiedade generalizada, pânico e fobia social.
^c
@ Anorexia nervosa: quando internar
# Peso, coração, eletrólitos :: Peso = IMC abaixo de 15 (ou abaixo de 75% do esperado); Coração = frequência abaixo de 40 bpm, hipotensão, arritmia, síncope; Eletrólitos = potássio ou fósforo baixos; Outros = ideação suicida ou falha do tratamento ambulatorial
> Os cortes variam entre as diretrizes. A realimentação exige reposição de fósforo e monitorização.
^c
@ TDAH no adulto: tratamento
# Estimulante primeiro :: Primeira linha = estimulantes (metilfenidato, lisdexanfetamina); Alternativas = atomoxetina, bupropiona; Monitorar = pressão, frequência, apetite, sono e peso; Associar = psicoeducação e terapia cognitivo-comportamental
> Tratamento farmacológico e não farmacológico do TDAH no adulto.
^c
@ Esquizofrenia: fatores de bom prognóstico
# Agudo, tardio, positivo :: Início = tardio e agudo, com fator desencadeante; Sintomas = positivos e de humor predominam; Antes = bom funcionamento social e profissional; Contexto = apoio familiar e adesão ao tratamento
> Fatores clássicos de melhor evolução. Sexo feminino também tem melhor prognóstico.
^c
"""
