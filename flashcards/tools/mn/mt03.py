TXT = r"""
## 05 💤 Sedação e via aérea
@ Pacote ABCDEF
# ABCDEF :: Analgesia primeiro: avaliar e tratar a dor; Both: despertar e respiração espontânea diários; Choice: escolha do sedativo e do analgésico; Delirium: avaliar, prevenir e tratar; Early mobility: mobilização precoce; Família engajada
^c
@ CAM-ICU: os quatro critérios
# FINP :: Flutuação ou início agudo; Inatenção; Nível de consciência alterado (RASS diferente de zero); Pensamento desorganizado
! Delirium = os dois primeiros + um dos dois últimos.
^o
@ Os 7 P da sequência rápida
# 7 P :: 1º = Preparação; 2º = Pré-oxigenação; 3º = Pré-tratamento e otimização hemodinâmica; 4º = Paralisia com indução; 5º = Posicionamento; 6º = Passagem do tubo com confirmação; 7º = Pós-intubação
^c
@ Material para intubar
# SOAP-ME :: Sucção; Oxigênio; Airway: tubos, lâminas e bougie; Posição e pré-oxigenação; Monitor e medicações; EtCO₂: capnografia
^c
@ Prever laringoscopia difícil
# LEMON :: Look: olhar externo; Evaluate: regra 3-3-2; Mallampati; Obstrução e obesidade; Neck: mobilidade cervical
^c
@ Regra 3-3-2
# 3-3-2 :: 3 dedos = abertura da boca; 3 dedos (2) = do mento ao hioide; 2 dedos = do hioide à cartilagem tireoide
^c
@ Prever ventilação difícil com máscara
# OBESO :: Obesidade; Barba; Edêntulo; Sono com ronco ou apneia; Old: idade acima de 55 anos
^c
@ Prever dispositivo supraglótico difícil
# RODS :: Restrição da abertura bucal; Obstrução; Distorção da via aérea; Stiff: pulmão ou coluna rígidos
^c
@ Prever cricotireoidostomia difícil
# SHORT :: Surgery: cirurgia cervical prévia; Hematoma ou infecção; Obesidade; Radioterapia; Tumor
^c
@ Via aérea fisiologicamente difícil
# CRASH :: Consumo de oxigênio aumentado; Right ventricle: falência de ventrículo direito; Acidose metabólica grave; Saturação baixa apesar da pré-oxigenação; Hipotensão
^c
@ Escore MACOCHA
# MACOCHA :: Mallampati III ou IV (5 pontos); Apneia do sono (2); Cervical: mobilidade reduzida (1); Opening: abertura bucal < 3 cm (1); Coma (1); Hipoxemia grave (1); Anestesista ausente: operador não anestesista (1)
! Três pontos ou mais = intubação difícil na UTI.
^c
@ Tubo traqueal: números de bolso
# 21 · 23 · 20–30 :: 21 cm = fixação no lábio na mulher; 23 cm = fixação no lábio no homem; 3–5 cm = distância da ponta à carina na radiografia; 20–30 cmH₂O = pressão do balonete
^c
@ Doses da sequência rápida
# 0,3 · 1–2 · 1,2 · 1,5 :: Etomidato = 0,3 mg/kg; Cetamina = 1–2 mg/kg; Rocurônio = 1,2 mg/kg; Succinilcolina = 1–1,5 mg/kg
! No choque, reduzir o indutor e não o bloqueador.
^c
@ Quando não usar succinilcolina
# HIPER-K :: Hipertermia maligna; Imobilização prolongada; Paralisia por denervação (AVC, lesão medular após 72 h); Esmagamento e grande queimado após 24–48 h; Rabdomiólise e miopatias; K⁺ sérico já elevado
^o
@ Hipotensão depois de intubar
# HIPO :: Hipovolemia desmascarada; Indutores: vasodilatação e depressão miocárdica; Pressão positiva reduz o retorno venoso; Obstrução: pneumotórax e auto-PEEP
^o
@ Escalas de dor e sedação: cortes
# 5 · 3 · 0 :: BPS = 3 a 12, dor se acima de 5; CPOT = 0 a 8, dor se 3 ou mais; RASS = −5 a +4, alvo entre −1 e 0
^c
@ RASS de +4 a −5
# +4 → −5 :: +4 = combativo; +3 = muito agitado; +2 = agitado; +1 = inquieto; 0 = alerta e calmo; −1 = sonolento, sustenta o olhar por mais de 10 s; −2 = sedação leve, olhar por menos de 10 s; −3 = moderada, move-se à voz sem olhar; −4 = profunda, só responde ao toque; −5 = não despertável
^c
@ Sequência de quatro estímulos (TOF)
# 4-3-2-1-0 :: 4 respostas = menos de 75% de bloqueio; 3 respostas = 75%; 2 respostas = 80%; 1 resposta = 90%; 0 resposta = 100%
! Alvo no bloqueio contínuo: 1 a 2 respostas.
^c
@ Precipitantes de delirium
# DELÍRIO :: Drogas: benzodiazepínico, anticolinérgico e opioide; Eletrólitos e distúrbios metabólicos; Luz e ruído à noite (privação de sono); Infecção; Retenção urinária e fecal; Imobilidade e contenção; Oxigênio baixo e falência de órgãos
^o
@ Via aérea difícil: planos A a D
# A-B-C-D :: A = laringoscopia (máximo 3 tentativas + 1 do mais experiente); B = dispositivo supraglótico; C = máscara facial; D = cricotireoidostomia (bisturi, bougie, tubo)
^c
@ Pré-oxigenação
# 3 · 8 · 15 :: 3 min = volume corrente com O₂ a 100%; 8 = capacidades vitais em 60 s; 15 L/min = cateter nasal mantido durante a apneia
! No hipoxêmico, pré-oxigenar com ventilação não invasiva.
^c

## 06 🫀 Cardiointensivismo e PCR
@ Causas reversíveis de PCR: 5 H
# 5 H :: Hipovolemia = volume e sangue; Hipóxia = via aérea e oxigênio; H⁺ = acidose; Hipo ou hipercalemia = cálcio, bicarbonato e insulina; Hipotermia = reaquecer
^c
@ Causas reversíveis de PCR: 5 T
# 5 T :: Tensão no tórax = pneumotórax hipertensivo; Tamponamento = pericardiocentese; Toxinas = antídoto; Trombose pulmonar = trombólise; Trombose coronariana = reperfusão
^c
@ RCP de alta qualidade: números
# 100-5-30:2-10 :: 100–120 = compressões por minuto; 5–6 cm = profundidade; 30:2 = sem via aérea avançada; 10 s = pausa máxima; 2 min = troca de quem comprime
^c
@ Drogas da PCR
# 1 · 300 · 150 :: Adrenalina = 1 mg a cada 3–5 min; Amiodarona = 300 mg e depois 150 mg; Lidocaína = 1 a 1,5 mg/kg
^c
@ Cuidados depois do retorno da circulação
# ROSC :: Reperfusão: ECG e coronariografia se houver supra; Oxigenação 92–98% e normocapnia; Suporte pressórico: PAM ≥ 65; Controle de temperatura e de crises
! Evitar febre por pelo menos 72 h.
^o
@ Classificação de Killip
# I-II-III-IV :: I = sem congestão; II = estertores em bases ou terceira bulha; III = edema agudo de pulmão; IV = choque cardiogênico
^c
@ Perfis da insuficiência cardíaca aguda
# Quente/frio × seco/úmido :: A = quente e seco; B = quente e úmido (diurético e vasodilatador); L = frio e seco (volume com cautela); C = frio e úmido (inotrópico ou vasopressor e diurético)
^c
@ Edema agudo de pulmão: conduta
# POND :: Posição sentada; Oxigênio e ventilação não invasiva; Nitrato; Diurético
! A morfina saiu da rotina.
^c
@ Taquiarritmia instável: os 4 D
# 4 D :: Diminuição da pressão = hipotensão ou choque; Dor torácica = isquemia; Dispneia = congestão pulmonar; Diminuição da consciência = síncope ou rebaixamento
! Presente qualquer um: cardioversão elétrica sincronizada.
^c
@ Adenosina
# 6-12-12 :: 6 mg = primeira dose em bolus rápido; 12 mg = segunda dose; 12 mg (3ª) = pode repetir
^c
@ Cardioversão sincronizada: energia inicial
# 50 · 100 · 120 :: 50–100 J = flutter e taquicardia supraventricular; 100 J = taquicardia ventricular monomórfica; 120–200 J = fibrilação atrial
^c
@ Bradicardia instável
# ATDA :: Atropina 1 mg a cada 3–5 min (máximo 3 mg); Transcutâneo: marca-passo; Dopamina 5–20 µg/kg/min; Adrenalina 2–10 µg/min
^c
@ Fármacos que alongam o QT
# ABCDE do QT :: A = Antiarrítmicos (classes IA e III); B = antiBióticos (macrolídeos e quinolonas); C = antipsiCóticos; D = antiDepressivos; E = antiEméticos e Eletrólitos baixos (K, Mg, Ca)
^c
@ Complicações mecânicas do infarto: 3 rupturas
# 3 R :: Ruptura de parede livre = tamponamento; Ruptura de septo = sopro novo com shunt; Ruptura de músculo papilar = insuficiência mitral aguda
^o
@ Critérios hemodinâmicos de choque cardiogênico
# 90 · 2,2 · 15 :: 90 = pressão sistólica abaixo disso por 30 min; 2,2 = índice cardíaco abaixo disso (L/min/m²); 15 = pressão de oclusão acima disso (mmHg)
^c
@ Vasoativos e seus receptores
# α · β · V :: Noradrenalina = α1 muito maior que β1; Adrenalina = β em dose baixa e α em dose alta; Dobutamina = β1 maior que β2; Vasopressina = receptor V1; Milrinona = inibe a fosfodiesterase 3
^c
@ Órgãos-alvo na emergência hipertensiva
# COCAR :: Cérebro; Olho; Coração; Aorta; Rim
^o
@ Quanto baixar a pressão na emergência hipertensiva
# 25% · 160/100 · 24–48 h :: 25% = redução máxima da PAM na primeira hora; 160/100 = alvo entre 2 e 6 h; 24–48 h = prazo para normalizar
! Exceções: dissecção de aorta (sistólica < 120 em 20 min) e AVC.
^c
@ Critérios de Sgarbossa
# 5-3-2 :: 5 pontos = supra ≥ 1 mm concordante com o QRS; 3 pontos = infra ≥ 1 mm em V1 a V3; 2 pontos = supra ≥ 5 mm discordante
! Três pontos ou mais sugerem infarto no bloqueio de ramo esquerdo.
^c
@ Dissecção de aorta: Stanford
# AB :: Ascendente envolvida: cirurgia; Baixo da subclávia: só descendente, tratamento clínico
^c
"""
