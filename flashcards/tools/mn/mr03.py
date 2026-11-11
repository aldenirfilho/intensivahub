TXT = r"""
## 05 🫃 Gastro e hepatologia
@ Dispepsia: sinais de alarme
# ALARMES :: Anemia ferropriva; Linfonodo ou massa palpável; Anos: início depois dos 60; Redução de peso sem explicação; Melena ou hematêmese; Engasgo: disfagia progressiva; Sempre vomitando: vômitos persistentes
! Qualquer um indica endoscopia.
^o
@ Hemorragia digestiva alta: Glasgow-Blatchford
# "Zero vai para casa" :: Itens = ureia, hemoglobina, pressão sistólica, pulso, melena, síncope, hepatopatia, insuficiência cardíaca; 0–1 = baixo risco: alta com endoscopia ambulatorial; Maior = internar e endoscopia em até 24 h
^c
@ H. pylori: quando erradicar
# ÚLCERA :: Úlcera péptica ativa ou prévia; Linfoma MALT; Câncer gástrico precoce ressecado ou familiar de 1º grau; Em uso prolongado de AAS ou anti-inflamatório; Refratária: dispepsia sem melhora; Anemia ferropriva sem causa e púrpura trombocitopênica imune
^o
@ Doença de Crohn × retocolite ulcerativa
# "Boca ao ânus × só cólon" :: Crohn = qualquer segmento, salteada, transmural, fístulas e estenoses, costuma poupar o reto; Retocolite = contínua a partir do reto, só mucosa, diarreia com sangue; Tabagismo = piora o Crohn
^c
@ Doença inflamatória intestinal: fora do intestino
# PEACE :: Pioderma gangrenoso; Eritema nodoso; Artrite e espondilite; Colangite esclerosante primária; Episclerite e uveíte
^o
@ Retocolite grave: Truelove e Witts
# 6 + 1 :: 6 = evacuações com sangue por dia ou mais; + 1 = febre acima de 37,8, FC acima de 90, hemoglobina abaixo de 10,5 ou VHS acima de 30
^c
@ Megacólon tóxico
# 6 cm + toxemia :: 6 cm = dilatação do cólon transverso; Toxemia = febre, taquicardia, leucocitose, anemia
! Colonoscopia e antidiarreicos estão contraindicados.
^c
@ Doença celíaca
# "tTG, biópsia, sem glúten" :: Rastreio = antitransglutaminase IgA + IgA total; Confirmação = biópsia duodenal com atrofia de vilosidades; Tratamento = dieta sem trigo, centeio e cevada; Pele = dermatite herpetiforme
^c
@ Diarreia crônica: três mecanismos
# OSI :: Osmótica: para com o jejum; Secretora: persiste no jejum; Inflamatória: sangue, muco e calprotectina alta
^c
@ Hepatite B: sorologia
# "s, e, c" :: HBsAg = infecção presente; Anti-HBs = imunidade (vacina ou cura); Anti-HBc IgM = infecção aguda; Anti-HBc IgG isolado = contato prévio; HBeAg = replicação alta
^c
@ Hepatites virais: transmissão
# "Vogais pela boca" :: A e E = fecal-oral, não cronificam (a E cronifica no imunossuprimido); B, C e D = sangue e sexo, cronificam; D = só existe com a B
^c
@ Cirrose: complicações
# CHAVES :: Carcinoma hepatocelular; Hepatorrenal; Ascite; Varizes; Encefalopatia; Séptica: peritonite bacteriana espontânea
^o
@ Rastreio de hepatocarcinoma
# 6 meses :: Intervalo = a cada 6 meses; Quem = todo cirrótico e hepatite B de risco; Como = ultrassom, com ou sem alfafetoproteína
^c
@ Ascite: gradiente de albumina soro-ascite
# 1,1 :: 1,1 ou mais = hipertensão portal (cirrose, insuficiência cardíaca, Budd-Chiari); Menor que 1,1 = peritônio doente (carcinomatose, tuberculose) ou síndrome nefrótica; Proteína acima de 2,5 com gradiente alto = origem cardíaca
^c
@ Hemocromatose
# "Diabetes bronzeado" :: Fígado = cirrose e hepatocarcinoma; Pâncreas = diabetes; Pele = bronzeada; Articulações = 2ª e 3ª metacarpofalângicas; Coração e gônadas = miocardiopatia e hipogonadismo; Rastreio = saturação de transferrina acima de 45% com ferritina alta
^c
@ Doença de Wilson
# "Cobre no fígado, no cérebro e no olho" :: Fígado = hepatite, cirrose, falência aguda com hemólise; Cérebro = tremor, distonia, sintomas psiquiátricos; Olho = anéis de Kayser-Fleischer; Exames = ceruloplasmina baixa e cobre urinário alto
^c
@ Colangite: Charcot e Reynolds
# 3 + 2 :: Charcot = febre, icterícia e dor em hipocôndrio direito; Reynolds = Charcot + hipotensão + confusão mental
^c
@ Pancreatite aguda: causas
# I GET SMASHED :: Idiopática; Gallstones: cálculos biliares; Etanol; Trauma; Steroids: corticoide; Mumps: caxumba e outros vírus; Autoimune; Scorpion: escorpião; Hipertrigliceridemia e hipercalcemia; ERCP: pós-colangiografia endoscópica; Drogas
! Cálculo e álcool respondem por ~80%.
^c
@ Icterícia: onde está o problema
# "Antes, dentro, depois" :: Antes do fígado = hemólise: bilirrubina indireta; Dentro do fígado = hepatite, cirrose, Gilbert, colestase intra-hepática; Depois do fígado = obstrução biliar: direta, com colúria e acolia
^c
@ Síndrome do intestino irritável: Roma IV
# 1 · 3 · 6 :: 1 = dia por semana de dor abdominal, em média; 3 = últimos meses com esse padrão; 6 = meses desde o início; 2 de 3 = relação com evacuação, mudança da frequência, mudança da forma das fezes
^c
## 06 🩸 Hematologia
@ Anemia microcítica: causas
# TAIL :: Talassemia; Anemia de doença crônica; Iron: ferropriva; Lead: chumbo e sideroblástica
^c
@ Ferropriva × doença crônica
# "A ferritina decide" :: Ferropriva = ferritina baixa, capacidade de ligação alta, saturação baixa; Doença crônica = ferritina normal ou alta, capacidade de ligação baixa, saturação baixa; Mista = ferritina abaixo de 100 com inflamação
^c
@ Anemia macrocítica: causas
# MACRO :: Mielodisplasia; Álcool e hepatopatia; Cobalamina (B12) e folato baixos; Reticulocitose; Outras: hipotireoidismo e fármacos
^o
@ Deficiência de B12 × folato
# "Só a B12 dá neuro" :: B12 = anemia + neuropatia e síndrome cordonal posterior, ácido metilmalônico alto; Folato = só anemia, homocisteína alta nas duas; Cuidado = folato sozinho pode piorar o quadro neurológico da falta de B12
^c
@ Hemólise: laboratório
# "Sobe RIL, cai H" :: Reticulócitos = sobem; Indireta = bilirrubina sobe; LDH = sobe; Haptoglobina = cai
^o
@ Anemia hemolítica autoimune: quente × fria
# "IgG quente, IgM fria" :: Quente = IgG, hemólise no baço, corticoide; Fria = IgM com complemento, depois de Mycoplasma ou mononucleose, evitar o frio e rituximabe
^c
@ Doença falciforme: crises
# VASTA :: Vaso-oclusiva dolorosa; Aplásica (parvovírus B19); Sequestro esplênico; Torácica aguda; AVC isquêmico
^o
@ Mieloma múltiplo: CRAB
# CRAB :: Cálcio alto; Rim: insuficiência renal; Anemia; Bone: lesões ósseas líticas
! Também fecham diagnóstico: plasmócitos ≥ 60%, relação de cadeias leves ≥ 100 e mais de 1 lesão focal na ressonância.
^c
@ Linfoma: sintomas B
# FPS :: Febre acima de 38 °C; Perda de mais de 10% do peso em 6 meses; Sudorese noturna
^c
@ Linfoma: estadiamento de Ann Arbor
# I-II-III-IV :: I = uma região linfonodal; II = duas ou mais regiões do mesmo lado do diafragma; III = dos dois lados do diafragma; IV = acometimento extranodal difuso
^c
@ Leucemias por idade
# "LLA criança, LLC idoso" :: LLA = criança; LMA = adulto (bastonetes de Auer); LMC = meia-idade, cromossomo Filadélfia t(9;22); LLC = idoso, linfocitose com manchas de Gumprecht
^c
@ Leucemia promielocítica aguda
# "t(15;17), CIVD, ATRA" :: Translocação = t(15;17), PML-RARA; Risco = CIVD com sangramento grave; Tratamento = ATRA imediato na suspeita
^c
@ Policitemia vera: critérios
# "JAK2 + massa + medula" :: Hemoglobina = acima de 16,5 no homem ou de 16 na mulher; Medula = hipercelular com panmielose; JAK2 = mutação presente; Critério menor = eritropoetina baixa
! Prurido depois do banho quente e eritromelalgia.
^c
@ Púrpura trombocitopênica imune
# "Só a plaqueta baixa" :: Diagnóstico = de exclusão: plaquetopenia isolada com esfregaço normal; Tratar = abaixo de 20–30 mil ou com sangramento; Primeira linha = corticoide, com imunoglobulina se for urgente
^c
@ Hemofilias e von Willebrand
# "A8, B9" :: Hemofilia A = fator VIII, TTPa longo, ligada ao X; Hemofilia B = fator IX, TTPa longo, ligada ao X; von Willebrand = a mais comum, sangramento de mucosa, tempo de sangramento longo
^c
@ Trombofilias hereditárias
# "5 hereditárias" :: Fator V de Leiden = a mais comum; Protrombina mutante = G20210A; Proteína C = deficiência; Proteína S = deficiência; Antitrombina = deficiência, a mais trombogênica
^c
@ Síndrome antifosfolípide: critérios
# "Clínica + laboratório × 2" :: Clínica = trombose ou morbidade gestacional; Laboratório = anticoagulante lúpico, anticardiolipina ou anti-β2-glicoproteína I; Confirmação = repetir depois de 12 semanas; Tratamento = varfarina (anticoagulante oral direto falha no triplo-positivo)
^c
@ Varfarina: fármacos que elevam o INR
# FAMA :: Fluconazol e outros azólicos; Amiodarona; Metronidazol; Antibióticos (sulfa e macrolídeos)
! Rifampicina, carbamazepina e fenitoína fazem o contrário.
^o
@ Neutropenia febril: definição
# 38,3 · 500 :: 38,3 = uma medida oral (ou 38 °C por 1 h); 500 = neutrófilos abaixo disso (ou abaixo de 1.000 com queda prevista)
! MASCC de 21 ou mais = baixo risco.
^c
@ Esplenomegalia maciça: causas
# "Meu Lindo Ceará Mostra Grande Esplenomegalia" :: Meu = Mielofibrose; Lindo = Leucemia mieloide crônica; Ceará = Calazar; Mostra = Malária crônica; Grande = Gaucher; Esplenomegalia = Esquistossomose
^of
"""
