TXT = r"""
## 15 🩻 POCUS e procedimentos
@ Protocolo BLUE: perfis e diagnósticos
# A-B-C :: Perfil A com trombose venosa = embolia pulmonar; Perfil A sem trombose, com consolidação posterior = pneumonia; Perfil A sem nada = asma ou DPOC; Perfil B = edema pulmonar cardiogênico; Perfil A sem deslizamento, com ponto pulmonar = pneumotórax; Perfis B sem deslizamento, A/B e C = pneumonia
^c
@ Pneumotórax no ultrassom
# "3 ausências + 1 ponto" :: Sem deslizamento = sensível, pouco específico; Sem linhas B = uma linha B exclui naquele ponto; Sem pulso pulmonar = pulso presente exclui; Ponto pulmonar = 100% específico
^o
@ Choque indiferenciado: protocolo RUSH
# "Bomba, tanque, canos" :: Bomba = coração: contratilidade, derrame e ventrículo direito; Tanque = cava, pulmão, pleura e abdome; Canos = aorta e veias profundas
^c
@ Tamponamento no ecocardiograma
# "Derrame, colapso, cava" :: Derrame = pericárdico, em geral circunferencial; Colapso = átrio direito na sístole e ventrículo direito na diástole; Cava = dilatada e sem variação; Doppler = variação respiratória do fluxo mitral acima de 25%
^o
@ Sobrecarga aguda do ventrículo direito no eco
# "VD em apuros" :: VD/VE = maior que 1 no apical de quatro câmaras; Septo = retificado, ventrículo esquerdo em D; McConnell = parede livre parada com ápice preservado; 60/60 = aceleração pulmonar < 60 ms com gradiente tricúspide < 60 mmHg; TAPSE = abaixo de 17 mm
^o
@ Veia cava inferior: leitura rápida
# 2,1 · 50% :: Menor que 2,1 cm com colapso > 50% = pressão atrial direita ~3 mmHg; Maior que 2,1 cm com colapso < 50% = ~15 mmHg; Combinações intermediárias = ~8 mmHg; No ventilado = distensibilidade > 18% sugere resposta a volume
^c
@ Trombose venosa: compressão em dois pontos
# 2 pontos :: Ponto 1 = veia femoral comum, na junção com a safena; Ponto 2 = veia poplítea; Positivo = veia que não colapsa com a compressão
^c
@ Linhas A e linhas B
# A × B :: Linhas A = horizontais, repetição da pleura: pulmão aerado (ou pneumotórax); Linhas B = verticais, apagam as A e vão até o fim da tela: síndrome intersticial; Patológico = 3 ou mais linhas B por campo
^c
@ Técnica de Seldinger
# "Pode Guiar Depois Coloca E Radiografa" :: Pode = Punção com agulha; Guiar = Guia metálico pela agulha; Depois = Dilatador sobre o guia; Coloca = Cateter sobre o guia; E = Extrair o guia; Radiografa = Radiografia de controle
! Nunca soltar o guia.
^of
@ Critérios de Light
# 0,5 · 0,6 · 2/3 :: 0,5 = proteína pleural ÷ sérica acima disso; 0,6 = LDH pleural ÷ sérica acima disso; 2/3 = LDH pleural acima de dois terços do limite superior sérico
! Um critério basta para exsudato.
^c
@ Líquor: padrões
# "Bactéria come açúcar" :: Bacteriana = neutrófilos, glicose baixa, proteína alta; Viral = linfócitos, glicose normal; Tuberculosa e fúngica = linfócitos, glicose baixa, proteína muito alta; Guillain-Barré = proteína alta com poucas células
^o
@ Drenagem torácica: triângulo de segurança
# Triângulo :: Anterior = borda lateral do peitoral maior; Posterior = borda anterior do grande dorsal; Inferior = linha do 5º espaço intercostal; Ápice = abaixo da axila
! Entrar rente à borda superior da costela de baixo.
^c
@ Cateter venoso central: risco por sítio
# "Subclávia infecta menos, fura mais" :: Subclávia = menos infecção e trombose, mais pneumotórax; Jugular = intermediária; Femoral = mais infecção e trombose
^o
@ Linha arterial: teste da onda quadrada
# "Onda quadrada" :: Normal = 1–2 oscilações depois do flush; Amortecida = nenhuma oscilação: subestima a sistólica (bolha, coágulo, dobra); Ressonante = muitas oscilações: superestima a sistólica; Pressão média = pouco afetada nos dois casos
^c
@ Capnograma: quatro fases
# I-II-III-0 :: I = espaço morto anatômico (linha de base); II = subida: mistura com ar alveolar; III = platô alveolar (o fim é o ETCO₂); 0 = descida inspiratória
! Fase III inclinada ("barbatana de tubarão") = obstrução ao fluxo.
^c
@ Paracentese de grande volume
# 5 · 6–8 :: 5 = litros: acima disso a albumina é obrigatória; 6–8 = gramas de albumina por litro retirado; Local = quadrante inferior esquerdo, lateral ao reto abdominal
^c
@ Punção lombar: contraindicações
# PIPA :: Plaquetas baixas ou anticoagulação; Infecção no local da punção; Pressão intracraniana alta com lesão expansiva; Abscesso epidural suspeito
^o
@ Vasoespasmo no Doppler transcraniano: Lindegaard
# 3 · 6 :: Menor que 3 = hiperemia; De 3 a 6 = vasoespasmo leve a moderado; Maior que 6 = vasoespasmo grave
! Lindegaard = velocidade média da cerebral média ÷ carótida interna extracraniana.
^c
"""
