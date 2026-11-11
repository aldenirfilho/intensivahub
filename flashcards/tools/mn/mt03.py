TXT = r"""
## 05 💤 Sedação e via aérea
@ Pacote ABCDEF
# ABCDEF :: Analgesia primeiro: avaliar e tratar a dor; Both: despertar e respiração espontânea diários; Choice: escolha do sedativo e do analgésico; Delirium: avaliar, prevenir e tratar; Early mobility: mobilização precoce; Família engajada
> Pacote da Society of Critical Care Medicine (ICU Liberation). A adesão se associa a menos delirium, menos tempo de ventilação e menor mortalidade.
^c
@ CAM-ICU: os quatro critérios
# FINP :: Flutuação ou início agudo; Inatenção; Nível de consciência alterado (RASS diferente de zero); Pensamento desorganizado
> Ferramenta validada (Ely, 2001) para detectar delirium no paciente ventilado. Sem busca ativa, o delirium hipoativo passa despercebido.
! Delirium = os dois primeiros + um dos dois últimos.
^o
@ Os 7 P da sequência rápida
# 7 P :: 1º = Preparação; 2º = Pré-oxigenação; 3º = Pré-tratamento e otimização hemodinâmica; 4º = Paralisia com indução; 5º = Posicionamento; 6º = Passagem do tubo com confirmação; 7º = Pós-intubação
> Roteiro clássico da sequência rápida de intubação (Walls). Ajuda a não pular etapas na via aérea de emergência.
^c
@ Material para intubar
# SOAP-ME :: Sucção; Oxigênio; Airway: tubos, lâminas e bougie; Posição e pré-oxigenação; Monitor e medicações; EtCO₂: capnografia
> Checagem do material antes de induzir. Faltar um item no meio da intubação é falha evitável.
^c
@ Prever laringoscopia difícil
# LEMON :: Look: olhar externo; Evaluate: regra 3-3-2; Mallampati; Obstrução e obesidade; Neck: mobilidade cervical
> Avaliação rápida da via aérea anatomicamente difícil na emergência, difundida pelo manual de Walls.
^c
@ Regra 3-3-2
# 3-3-2 :: 3 dedos = abertura da boca; 3 dedos (2) = do mento ao hioide; 2 dedos = do hioide à cartilagem tireoide
> Mede com os dedos se há espaço para alinhar os eixos e deslocar a língua na laringoscopia direta. É o "E" do LEMON.
^c
@ Prever ventilação difícil com máscara
# OBESO :: Obesidade; Barba; Edêntulo; Sono com ronco ou apneia; Old: idade acima de 55 anos
> Preditores de dificuldade para ventilar com bolsa-válvula-máscara, baseados no estudo de Langeron (2000).
^c
@ Prever dispositivo supraglótico difícil
# RODS :: Restrição da abertura bucal; Obstrução; Distorção da via aérea; Stiff: pulmão ou coluna rígidos
> Preditores de falha do dispositivo supraglótico, o plano de resgate quando a laringoscopia falha.
^c
@ Prever cricotireoidostomia difícil
# SHORT :: Surgery: cirurgia cervical prévia; Hematoma ou infecção; Obesidade; Radioterapia; Tumor
> Preditores de dificuldade no acesso cirúrgico à via aérea. Identificar antes muda o planejamento do plano D.
^c
@ Via aérea fisiologicamente difícil
# CRASH :: Consumo de oxigênio aumentado; Right ventricle: falência de ventrículo direito; Acidose metabólica grave; Saturação baixa apesar da pré-oxigenação; Hipotensão
> Via aérea fisiologicamente difícil: o risco está no colapso durante a indução, e não na anatomia. Pede otimização antes de intubar.
^c
@ Escore MACOCHA
# MACOCHA :: Mallampati III ou IV (5 pontos); Apneia do sono (2); Cervical: mobilidade reduzida (1); Opening: abertura bucal < 3 cm (1); Coma (1); Hipoxemia grave (1); Anestesista ausente: operador não anestesista (1)
> Escore de De Jong (2013), desenvolvido e validado especificamente para prever intubação difícil na UTI.
! Três pontos ou mais = intubação difícil na UTI.
^c
@ Tubo traqueal: números de bolso
# 21 · 23 · 20–30 :: 21 cm = fixação no lábio na mulher; 23 cm = fixação no lábio no homem; 3–5 cm = distância da ponta à carina na radiografia; 20–30 cmH₂O = pressão do balonete
> Números para conferir a posição do tubo e evitar intubação seletiva, extubação acidental e lesão traqueal pelo balonete.
^c
@ Doses da sequência rápida
# 0,3 · 1–2 · 1,2 · 1,5 :: Etomidato = 0,3 mg/kg; Cetamina = 1–2 mg/kg; Rocurônio = 1,2 mg/kg; Succinilcolina = 1–1,5 mg/kg
> Doses por peso dos fármacos mais usados na sequência rápida. Subdose de bloqueador neuromuscular piora as condições de intubação.
! No choque, reduzir o indutor e não o bloqueador.
^c
@ Quando não usar succinilcolina
# HIPER-K :: Hipertermia maligna; Imobilização prolongada; Paralisia por denervação (AVC, lesão medular após 72 h); Esmagamento e grande queimado após 24–48 h; Rabdomiólise e miopatias; K⁺ sérico já elevado
> A succinilcolina eleva o potássio em cerca de 0,5 mEq/L e, quando há receptores extrajuncionais em excesso, pode causar hipercalemia fatal.
^o
@ Hipotensão depois de intubar
# HIPO :: Hipovolemia desmascarada; Indutores: vasodilatação e depressão miocárdica; Pressão positiva reduz o retorno venoso; Obstrução: pneumotórax e auto-PEEP
> A hipotensão pós-intubação é frequente e se associa a maior mortalidade. Conhecer os mecanismos permite antecipar com volume e vasopressor.
^o
@ Escalas de dor e sedação: cortes
# 5 · 3 · 0 :: BPS = 3 a 12, dor se acima de 5; CPOT = 0 a 8, dor se 3 ou mais; RASS = −5 a +4, alvo entre −1 e 0
> Escalas recomendadas pelas diretrizes PADIS (2018) para dor no paciente que não se comunica e para titular a sedação.
^c
@ RASS de +4 a −5
# +4 → −5 :: +4 = combativo; +3 = muito agitado; +2 = agitado; +1 = inquieto; 0 = alerta e calmo; −1 = sonolento, sustenta o olhar por mais de 10 s; −2 = sedação leve, olhar por menos de 10 s; −3 = moderada, move-se à voz sem olhar; −4 = profunda, só responde ao toque; −5 = não despertável
> Escala de Richmond (Sessler, 2002), a mais usada para titular sedação. Também é o primeiro passo do CAM-ICU.
^c
@ Sequência de quatro estímulos (TOF)
# 4-3-2-1-0 :: 4 respostas = menos de 75% de bloqueio; 3 respostas = 75%; 2 respostas = 80%; 1 resposta = 90%; 0 resposta = 100%
> Monitorização do bloqueio neuromuscular por estimulação de nervo periférico. Evita dose excessiva e acúmulo do bloqueador.
! Alvo no bloqueio contínuo: 1 a 2 respostas.
^c
@ Precipitantes de delirium
# DELÍRIO :: Drogas: benzodiazepínico, anticolinérgico e opioide; Eletrólitos e distúrbios metabólicos; Luz e ruído à noite (privação de sono); Infecção; Retenção urinária e fecal; Imobilidade e contenção; Oxigênio baixo e falência de órgãos
> Fatores modificáveis a corrigir antes de pensar em fármaco: o tratamento do delirium é remover a causa.
^o
@ Via aérea difícil: planos A a D
# A-B-C-D :: A = laringoscopia (máximo 3 tentativas + 1 do mais experiente); B = dispositivo supraglótico; C = máscara facial; D = cricotireoidostomia (bisturi, bougie, tubo)
> Algoritmo da Difficult Airway Society (2015, com versão para o paciente crítico em 2018) para a intubação que falha.
^c
@ Pré-oxigenação
# 3 · 8 · 15 :: 3 min = volume corrente com O₂ a 100%; 8 = capacidades vitais em 60 s; 15 L/min = cateter nasal mantido durante a apneia
> Trocar o nitrogênio dos pulmões por oxigênio prolonga a apneia segura. No paciente crítico, a reserva é curta e a dessaturação é rápida.
! No hipoxêmico, pré-oxigenar com ventilação não invasiva.
^c

## 06 🫀 Cardiointensivismo e PCR
@ Causas reversíveis de PCR: 5 H
# 5 H :: Hipovolemia = volume e sangue; Hipóxia = via aérea e oxigênio; H⁺ = acidose; Hipo ou hipercalemia = cálcio, bicarbonato e insulina; Hipotermia = reaquecer
> Causas a buscar durante a reanimação, sobretudo em atividade elétrica sem pulso e assistolia, em que não há choque a dar.
^c
@ Causas reversíveis de PCR: 5 T
# 5 T :: Tensão no tórax = pneumotórax hipertensivo; Tamponamento = pericardiocentese; Toxinas = antídoto; Trombose pulmonar = trombólise; Trombose coronariana = reperfusão
> Completa as causas reversíveis da PCR. O ultrassom durante a checagem de ritmo ajuda a achar tamponamento, pneumotórax e sobrecarga de ventrículo direito.
^c
@ RCP de alta qualidade: números
# 100-5-30:2-10 :: 100–120 = compressões por minuto; 5–6 cm = profundidade; 30:2 = sem via aérea avançada; 10 s = pausa máxima; 2 min = troca de quem comprime
> Componentes de qualidade das diretrizes da AHA e do ILCOR. Compressão bem feita e desfibrilação precoce são o que mais muda a sobrevida.
^c
@ Drogas da PCR
# 1 · 300 · 150 :: Adrenalina = 1 mg a cada 3–5 min; Amiodarona = 300 mg e depois 150 mg; Lidocaína = 1 a 1,5 mg/kg
> Doses do suporte avançado de vida. A adrenalina aumenta o retorno da circulação (ensaio PARAMEDIC2), com efeito incerto no desfecho neurológico.
^c
@ Cuidados depois do retorno da circulação
# ROSC :: Reperfusão: ECG e coronariografia se houver supra; Oxigenação 92–98% e normocapnia; Suporte pressórico: PAM ≥ 65; Controle de temperatura e de crises
> Cuidados pós-PCR das diretrizes. O ensaio TTM2 (2021) não mostrou benefício de 33 °C sobre a normotermia com prevenção ativa da febre.
! Evitar febre por pelo menos 72 h.
^o
@ Classificação de Killip
# I-II-III-IV :: I = sem congestão; II = estertores em bases ou terceira bulha; III = edema agudo de pulmão; IV = choque cardiogênico
> Classificação de Killip e Kimball (1967) para o infarto agudo: quanto maior a classe, maior a mortalidade hospitalar.
^c
@ Perfis da insuficiência cardíaca aguda
# Quente/frio × seco/úmido :: A = quente e seco; B = quente e úmido (diurético e vasodilatador); L = frio e seco (volume com cautela); C = frio e úmido (inotrópico ou vasopressor e diurético)
> Classificação de Stevenson pela perfusão e pela congestão, avaliadas à beira do leito. O perfil B é o mais comum; o C tem o pior prognóstico.
^c
@ Edema agudo de pulmão: conduta
# POND :: Posição sentada; Oxigênio e ventilação não invasiva; Nitrato; Diurético
> Tratamento inicial do edema agudo de pulmão cardiogênico, sobretudo o hipertensivo, em que o vasodilatador vale mais que o diurético.
! A morfina saiu da rotina.
^c
@ Taquiarritmia instável: os 4 D
# 4 D :: Diminuição da pressão = hipotensão ou choque; Dor torácica = isquemia; Dispneia = congestão pulmonar; Diminuição da consciência = síncope ou rebaixamento
> Critérios de instabilidade do ACLS: havendo qualquer um atribuível à arritmia, o tratamento é elétrico, não farmacológico.
! Presente qualquer um: cardioversão elétrica sincronizada.
^c
@ Adenosina
# 6-12-12 :: 6 mg = primeira dose em bolus rápido; 12 mg = segunda dose; 12 mg (3ª) = pode repetir
> Fármaco de escolha na taquicardia supraventricular regular estável, depois da manobra vagal. A meia-vida é de segundos: exige bolus seguido de flush.
^c
@ Cardioversão sincronizada: energia inicial
# 50 · 100 · 120 :: 50–100 J = flutter e taquicardia supraventricular; 100 J = taquicardia ventricular monomórfica; 120–200 J = fibrilação atrial
> Energias iniciais sugeridas pelo ACLS com aparelho bifásico. O choque é sincronizado para não cair sobre a onda T.
^c
@ Bradicardia instável
# ATDA :: Atropina 1 mg a cada 3–5 min (máximo 3 mg); Transcutâneo: marca-passo; Dopamina 5–20 µg/kg/min; Adrenalina 2–10 µg/min
> Sequência do ACLS na bradicardia com sinais de instabilidade. A atropina costuma falhar no bloqueio infranodal.
^c
@ Fármacos que alongam o QT
# ABCDE do QT :: A = Antiarrítmicos (classes IA e III); B = antiBióticos (macrolídeos e quinolonas); C = antipsiCóticos; D = antiDepressivos; E = antiEméticos e Eletrólitos baixos (K, Mg, Ca)
> Classes que prolongam o QT e predispõem a torsades de pointes. No paciente crítico, as associações e os distúrbios eletrolíticos somam o risco.
^c
@ Complicações mecânicas do infarto: 3 rupturas
# 3 R :: Ruptura de parede livre = tamponamento; Ruptura de septo = sopro novo com shunt; Ruptura de músculo papilar = insuficiência mitral aguda
> Complicações que surgem em geral entre o 2º e o 7º dia do infarto. Ficaram raras com a reperfusão, mas seguem letais sem cirurgia.
^o
@ Critérios hemodinâmicos de choque cardiogênico
# 90 · 2,2 · 15 :: 90 = pressão sistólica abaixo disso por 30 min; 2,2 = índice cardíaco abaixo disso (L/min/m²); 15 = pressão de oclusão acima disso (mmHg)
> Definição hemodinâmica clássica, usada no ensaio SHOCK (1999), para quando há medida invasiva disponível.
^c
@ Vasoativos e seus receptores
# α · β · V :: Noradrenalina = α1 muito maior que β1; Adrenalina = β em dose baixa e α em dose alta; Dobutamina = β1 maior que β2; Vasopressina = receptor V1; Milrinona = inibe a fosfodiesterase 3
> Saber o receptor de cada droga permite escolher pelo efeito desejado: vasoconstrição, inotropismo ou os dois.
^c
@ Órgãos-alvo na emergência hipertensiva
# COCAR :: Cérebro; Olho; Coração; Aorta; Rim
> A emergência hipertensiva é definida pela lesão aguda de órgão-alvo, e não pelo valor da pressão.
^o
@ Quanto baixar a pressão na emergência hipertensiva
# 25% · 160/100 · 24–48 h :: 25% = redução máxima da PAM na primeira hora; 160/100 = alvo entre 2 e 6 h; 24–48 h = prazo para normalizar
> Baixar rápido demais causa isquemia cerebral, coronariana e renal, porque a autorregulação está deslocada no hipertenso crônico.
! Exceções: dissecção de aorta (sistólica < 120 em 20 min) e AVC.
^c
@ Critérios de Sgarbossa
# 5-3-2 :: 5 pontos = supra ≥ 1 mm concordante com o QRS; 3 pontos = infra ≥ 1 mm em V1 a V3; 2 pontos = supra ≥ 5 mm discordante
> Critérios de Sgarbossa (1996) para diagnosticar infarto com bloqueio de ramo esquerdo ou marca-passo. Smith propôs depois a versão modificada, com a razão ST/S.
! Três pontos ou mais sugerem infarto no bloqueio de ramo esquerdo.
^c
@ Dissecção de aorta: Stanford
# AB :: Ascendente envolvida: cirurgia; Baixo da subclávia: só descendente, tratamento clínico
> Classificação que define a conduta: o tipo A é emergência cirúrgica; o tipo B não complicado se trata com controle de frequência e de pressão.
^c
"""
