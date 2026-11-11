TXT = r"""
## 05 🫃 Gastro e hepatologia
@ Dispepsia: sinais de alarme
# ALARMES :: Anemia ferropriva; Linfonodo ou massa palpável; Anos: início depois dos 60; Redução de peso sem explicação; Melena ou hematêmese; Engasgo: disfagia progressiva; Sempre vomitando: vômitos persistentes
> Sinais que afastam a dispepsia funcional e pedem investigação de câncer ou úlcera complicada.
! Qualquer um indica endoscopia.
^o
@ Hemorragia digestiva alta: Glasgow-Blatchford
# "Zero vai para casa" :: Itens = ureia, hemoglobina, pressão sistólica, pulso, melena, síncope, hepatopatia, insuficiência cardíaca; 0–1 = baixo risco: alta com endoscopia ambulatorial; Maior = internar e endoscopia em até 24 h
> Escore de Blatchford (2000), que usa só dados clínicos e laboratoriais, antes da endoscopia.
^c
@ H. pylori: quando erradicar
# ÚLCERA :: Úlcera péptica ativa ou prévia; Linfoma MALT; Câncer gástrico precoce ressecado ou familiar de 1º grau; Em uso prolongado de AAS ou anti-inflamatório; Refratária: dispepsia sem melhora; Anemia ferropriva sem causa e púrpura trombocitopênica imune
> Indicações de erradicação do consenso de Maastricht e do consenso brasileiro.
^o
@ Doença de Crohn × retocolite ulcerativa
# "Boca ao ânus × só cólon" :: Crohn = qualquer segmento, salteada, transmural, fístulas e estenoses, costuma poupar o reto; Retocolite = contínua a partir do reto, só mucosa, diarreia com sangue; Tabagismo = piora o Crohn
> Diferenças de localização, profundidade e complicações entre as duas doenças inflamatórias intestinais.
^c
@ Doença inflamatória intestinal: fora do intestino
# PEACE :: Pioderma gangrenoso; Eritema nodoso; Artrite e espondilite; Colangite esclerosante primária; Episclerite e uveíte
> Manifestações extraintestinais. Algumas acompanham a atividade da doença; a colangite esclerosante e a espondilite não.
^o
@ Retocolite grave: Truelove e Witts
# 6 + 1 :: 6 = evacuações com sangue por dia ou mais; + 1 = febre acima de 37,8, FC acima de 90, hemoglobina abaixo de 10,5 ou VHS acima de 30
> Critérios de Truelove e Witts (1955) para a colite aguda grave, que indica internação e corticoide intravenoso.
^c
@ Megacólon tóxico
# 6 cm + toxemia :: 6 cm = dilatação do cólon transverso; Toxemia = febre, taquicardia, leucocitose, anemia
> Complicação de colite grave, inflamatória ou infecciosa. Há risco de perfuração: avaliação cirúrgica precoce.
! Colonoscopia e antidiarreicos estão contraindicados.
^c
@ Doença celíaca
# "tTG, biópsia, sem glúten" :: Rastreio = antitransglutaminase IgA + IgA total; Confirmação = biópsia duodenal com atrofia de vilosidades; Tratamento = dieta sem trigo, centeio e cevada; Pele = dermatite herpetiforme
> Enteropatia autoimune desencadeada pelo glúten em pessoas com HLA-DQ2 ou DQ8. Testar ainda em dieta com glúten.
^c
@ Diarreia crônica: três mecanismos
# OSI :: Osmótica: para com o jejum; Secretora: persiste no jejum; Inflamatória: sangue, muco e calprotectina alta
> A resposta ao jejum e o gap osmolar fecal separam os mecanismos.
^c
@ Hepatite B: sorologia
# "s, e, c" :: HBsAg = infecção presente; Anti-HBs = imunidade (vacina ou cura); Anti-HBc IgM = infecção aguda; Anti-HBc IgG isolado = contato prévio; HBeAg = replicação alta
> Leitura dos marcadores da hepatite B. O anti-HBc IgM cobre a janela imunológica.
^c
@ Hepatites virais: transmissão
# "Vogais pela boca" :: A e E = fecal-oral, não cronificam (a E cronifica no imunossuprimido); B, C e D = sangue e sexo, cronificam; D = só existe com a B
> Vias de transmissão e potencial de cronificação de cada vírus.
^c
@ Cirrose: complicações
# CHAVES :: Carcinoma hepatocelular; Hepatorrenal; Ascite; Varizes; Encefalopatia; Séptica: peritonite bacteriana espontânea
> Marcam a passagem da cirrose compensada para a descompensada, com queda acentuada da sobrevida.
^o
@ Rastreio de hepatocarcinoma
# 6 meses :: Intervalo = a cada 6 meses; Quem = todo cirrótico e hepatite B de risco; Como = ultrassom, com ou sem alfafetoproteína
> O intervalo se baseia no tempo de duplicação do tumor. A detecção precoce permite tratamento curativo.
^c
@ Ascite: gradiente de albumina soro-ascite
# 1,1 :: 1,1 ou mais = hipertensão portal (cirrose, insuficiência cardíaca, Budd-Chiari); Menor que 1,1 = peritônio doente (carcinomatose, tuberculose) ou síndrome nefrótica; Proteína acima de 2,5 com gradiente alto = origem cardíaca
> Primeiro exame do líquido ascítico: separa a hipertensão portal das outras causas com cerca de 97% de acurácia.
^c
@ Hemocromatose
# "Diabetes bronzeado" :: Fígado = cirrose e hepatocarcinoma; Pâncreas = diabetes; Pele = bronzeada; Articulações = 2ª e 3ª metacarpofalângicas; Coração e gônadas = miocardiopatia e hipogonadismo; Rastreio = saturação de transferrina acima de 45% com ferritina alta
> Sobrecarga de ferro por mutação do gene HFE (C282Y). O tratamento é a flebotomia.
^c
@ Doença de Wilson
# "Cobre no fígado, no cérebro e no olho" :: Fígado = hepatite, cirrose, falência aguda com hemólise; Cérebro = tremor, distonia, sintomas psiquiátricos; Olho = anéis de Kayser-Fleischer; Exames = ceruloplasmina baixa e cobre urinário alto
> Defeito do gene ATP7B, com acúmulo de cobre. Pensar em hepatopatia ou distúrbio do movimento em jovens.
^c
@ Colangite: Charcot e Reynolds
# 3 + 2 :: Charcot = febre, icterícia e dor em hipocôndrio direito; Reynolds = Charcot + hipotensão + confusão mental
> Tríade de Charcot (1877) e pêntade de Reynolds (1959). A colangite grave exige drenagem biliar urgente.
^c
@ Pancreatite aguda: causas
# I GET SMASHED :: Idiopática; Gallstones: cálculos biliares; Etanol; Trauma; Steroids: corticoide; Mumps: caxumba e outros vírus; Autoimune; Scorpion: escorpião; Hipertrigliceridemia e hipercalcemia; ERCP: pós-colangiografia endoscópica; Drogas
> Lista clássica das causas de pancreatite aguda.
! Cálculo e álcool respondem por ~80%.
^c
@ Icterícia: onde está o problema
# "Antes, dentro, depois" :: Antes do fígado = hemólise: bilirrubina indireta; Dentro do fígado = hepatite, cirrose, Gilbert, colestase intra-hepática; Depois do fígado = obstrução biliar: direta, com colúria e acolia
> O tipo de bilirrubina e as enzimas hepáticas localizam o defeito e direcionam o exame de imagem.
^c
@ Síndrome do intestino irritável: Roma IV
# 1 · 3 · 6 :: 1 = dia por semana de dor abdominal, em média; 3 = últimos meses com esse padrão; 6 = meses desde o início; 2 de 3 = relação com evacuação, mudança da frequência, mudança da forma das fezes
> Critérios de Roma IV (2016), baseados em sintomas, na ausência de sinais de alarme.
^c
## 06 🩸 Hematologia
@ Anemia microcítica: causas
# TAIL :: Talassemia; Anemia de doença crônica; Iron: ferropriva; Lead: chumbo e sideroblástica
> VCM abaixo de 80 fL. A ferritina é o primeiro exame; a eletroforese de hemoglobina entra se o ferro for normal.
^c
@ Ferropriva × doença crônica
# "A ferritina decide" :: Ferropriva = ferritina baixa, capacidade de ligação alta, saturação baixa; Doença crônica = ferritina normal ou alta, capacidade de ligação baixa, saturação baixa; Mista = ferritina abaixo de 100 com inflamação
> As duas anemias mais comuns da prática. A ferritina é reagente de fase aguda e pode enganar na inflamação.
^c
@ Anemia macrocítica: causas
# MACRO :: Mielodisplasia; Álcool e hepatopatia; Cobalamina (B12) e folato baixos; Reticulocitose; Outras: hipotireoidismo e fármacos
> VCM acima de 100 fL. A megaloblástica (B12 e folato) e a não megaloblástica têm investigações diferentes.
^o
@ Deficiência de B12 × folato
# "Só a B12 dá neuro" :: B12 = anemia + neuropatia e síndrome cordonal posterior, ácido metilmalônico alto; Folato = só anemia, homocisteína alta nas duas; Cuidado = folato sozinho pode piorar o quadro neurológico da falta de B12
> A B12 participa da síntese de mielina. O ácido metilmalônico alto é específico da deficiência de B12.
^c
@ Hemólise: laboratório
# "Sobe RIL, cai H" :: Reticulócitos = sobem; Indireta = bilirrubina sobe; LDH = sobe; Haptoglobina = cai
> Quatro exames que confirmam a destruição de hemácias. O teste de Coombs direto separa a causa imune da não imune.
^o
@ Anemia hemolítica autoimune: quente × fria
# "IgG quente, IgM fria" :: Quente = IgG, hemólise no baço, corticoide; Fria = IgM com complemento, depois de Mycoplasma ou mononucleose, evitar o frio e rituximabe
> O Coombs direto mostra a classe do anticorpo. O corticoide funciona na quente; na fria, evitar o frio e usar rituximabe.
^c
@ Doença falciforme: crises
# VASTA :: Vaso-oclusiva dolorosa; Aplásica (parvovírus B19); Sequestro esplênico; Torácica aguda; AVC isquêmico
> Complicações agudas da doença falciforme. A síndrome torácica aguda é a principal causa de morte no adulto.
^o
@ Mieloma múltiplo: CRAB
# CRAB :: Cálcio alto; Rim: insuficiência renal; Anemia; Bone: lesões ósseas líticas
> Lesões de órgão-alvo que definem o mieloma sintomático e indicam tratamento (critérios do IMWG, 2014).
! Também fecham diagnóstico: plasmócitos ≥ 60%, relação de cadeias leves ≥ 100 e mais de 1 lesão focal na ressonância.
^c
@ Linfoma: sintomas B
# FPS :: Febre acima de 38 °C; Perda de mais de 10% do peso em 6 meses; Sudorese noturna
> Sintomas constitucionais que acrescentam a letra B ao estádio e pioram o prognóstico.
^c
@ Linfoma: estadiamento de Ann Arbor
# I-II-III-IV :: I = uma região linfonodal; II = duas ou mais regiões do mesmo lado do diafragma; III = dos dois lados do diafragma; IV = acometimento extranodal difuso
> Estadiamento de Ann Arbor (1971), hoje aplicado com PET-CT na classificação de Lugano.
^c
@ Leucemias por idade
# "LLA criança, LLC idoso" :: LLA = criança; LMA = adulto (bastonetes de Auer); LMC = meia-idade, cromossomo Filadélfia t(9;22); LLC = idoso, linfocitose com manchas de Gumprecht
> A idade e o tipo de célula orientam a hipótese diante de leucocitose com blastos ou linfócitos.
^c
@ Leucemia promielocítica aguda
# "t(15;17), CIVD, ATRA" :: Translocação = t(15;17), PML-RARA; Risco = CIVD com sangramento grave; Tratamento = ATRA imediato na suspeita
> Subtipo M3 da leucemia mieloide aguda. É emergência: a mortalidade precoce vem do sangramento, e a doença é altamente curável.
^c
@ Policitemia vera: critérios
# "JAK2 + massa + medula" :: Hemoglobina = acima de 16,5 no homem ou de 16 na mulher; Medula = hipercelular com panmielose; JAK2 = mutação presente; Critério menor = eritropoetina baixa
> Critérios da OMS: os três maiores, ou os dois primeiros com o critério menor. Há risco de trombose; o alvo é hematócrito abaixo de 45%.
! Prurido depois do banho quente e eritromelalgia.
^c
@ Púrpura trombocitopênica imune
# "Só a plaqueta baixa" :: Diagnóstico = de exclusão: plaquetopenia isolada com esfregaço normal; Tratar = abaixo de 20–30 mil ou com sangramento; Primeira linha = corticoide, com imunoglobulina se for urgente
> Destruição imune de plaquetas. O risco de sangramento grave é baixo acima de 30 mil.
^c
@ Hemofilias e von Willebrand
# "A8, B9" :: Hemofilia A = fator VIII, TTPa longo, ligada ao X; Hemofilia B = fator IX, TTPa longo, ligada ao X; von Willebrand = a mais comum, sangramento de mucosa, tempo de sangramento longo
> Coagulopatias hereditárias mais comuns. As hemofilias dão hemartrose; a doença de von Willebrand dá sangramento de mucosas.
^c
@ Trombofilias hereditárias
# "5 hereditárias" :: Fator V de Leiden = a mais comum; Protrombina mutante = G20210A; Proteína C = deficiência; Proteína S = deficiência; Antitrombina = deficiência, a mais trombogênica
> Pesquisar em trombose antes dos 50 anos, em sítio incomum ou com história familiar. O resultado raramente muda o tratamento agudo.
^c
@ Síndrome antifosfolípide: critérios
# "Clínica + laboratório × 2" :: Clínica = trombose ou morbidade gestacional; Laboratório = anticoagulante lúpico, anticardiolipina ou anti-β2-glicoproteína I; Confirmação = repetir depois de 12 semanas; Tratamento = varfarina (anticoagulante oral direto falha no triplo-positivo)
> Critérios de Sydney (2006), revistos por ACR/EULAR em 2023. O ensaio TRAPS mostrou mais eventos com rivaroxabana nos triplo-positivos.
^c
@ Varfarina: fármacos que elevam o INR
# FAMA :: Fluconazol e outros azólicos; Amiodarona; Metronidazol; Antibióticos (sulfa e macrolídeos)
> Inibidores do metabolismo da varfarina (CYP2C9). Ao associar, monitorar o INR e reduzir a dose.
! Rifampicina, carbamazepina e fenitoína fazem o contrário.
^o
@ Neutropenia febril: definição
# 38,3 · 500 :: 38,3 = uma medida oral (ou 38 °C por 1 h); 500 = neutrófilos abaixo disso (ou abaixo de 1.000 com queda prevista)
> Emergência oncológica: antibiótico antipseudomonas na primeira hora. O escore MASCC seleciona quem pode tratar em casa.
! MASCC de 21 ou mais = baixo risco.
^c
@ Esplenomegalia maciça: causas
# "Meu Lindo Ceará Mostra Grande Esplenomegalia" :: Meu = Mielofibrose; Lindo = Leucemia mieloide crônica; Ceará = Calazar; Mostra = Malária crônica; Grande = Gaucher; Esplenomegalia = Esquistossomose
> Baço que cruza a linha média ou chega à fossa ilíaca. No Brasil, calazar e esquistossomose entram na lista.
^of
"""
