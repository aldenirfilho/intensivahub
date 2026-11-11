TXT = r"""
## 03 🦠 Sepse e infecções
@ qSOFA
# HAT :: Hipotensão (PAS ≤ 100); Alteração do nível de consciência; Taquipneia (FR ≥ 22)
> Triagem à beira do leito proposta no Sepsis-3 (2016). A Surviving Sepsis Campaign de 2021 recomenda não usá-la como única ferramenta de rastreio.
! Serve para alertar, não para definir sepse: a sensibilidade é baixa.
^c
@ Os seis sistemas do SOFA
# "Rapaz Corajoso Faz Cirurgia No Rim" :: Rapaz = Respiratório (PaO₂/FiO₂); Corajoso = Coagulação (plaquetas); Faz = Fígado (bilirrubina); Cirurgia = Cardiovascular (PAM e vasopressor); No = Neurológico (Glasgow); Rim = Renal (creatinina e diurese)
> Escore de disfunção orgânica que define sepse no Sepsis-3: aumento de 2 pontos ou mais na presença de infecção suspeita.
^of
@ Pacote da primeira hora da sepse
# CLAVE :: Culturas antes do antibiótico; Lactato (repetir se > 2); Antibiótico de amplo espectro; Volume 30 mL/kg se hipotensão ou lactato ≥ 4; Elevar a PAM a 65 com noradrenalina
> Pacote de 1 hora da Surviving Sepsis Campaign: o que iniciar imediatamente ao reconhecer sepse ou choque séptico.
^o
@ Onde procurar o foco da sepse
# PUPILA :: Pulmão; Urinário; Pele e partes moles; Intra-abdominal; Linha vascular (cateter); Articulação, osso, endocárdio e meninges
> Roteiro para buscar a origem da infecção quando ela não é óbvia. Sem achar o foco, não há como controlá-lo.
^o
@ Controle do foco: os 3 D
# 3 D :: Drenar = abscessos e coleções; Desbridar = tecido necrótico; Dispositivo = retirar o que estiver infectado
> Antibiótico não trata coleção nem tecido morto. O controle do foco deve ocorrer o quanto antes, de preferência nas primeiras 6 a 12 horas.
^c
@ Prevenção da pneumonia associada à ventilação
# CABEÇA :: Cabeceira entre 30° e 45°; Avaliação diária de sedação e de extubação; Balonete entre 20 e 30 cmH₂O; Evitar troca rotineira do circuito; Cuidado oral; Aspiração subglótica
> Pacote de medidas para reduzir a pneumonia associada à ventilação, infecção frequente na UTI e ligada a mais dias de ventilação.
^o
@ Bactérias do grupo ESKAPE
# ESKAPE :: Enterococcus faecium; Staphylococcus aureus; Klebsiella pneumoniae; Acinetobacter baumannii; Pseudomonas aeruginosa; Enterobacter
> Sigla de Rice (2008) para as bactérias que "escapam" dos antibióticos e concentram a resistência hospitalar.
^c
@ Enterobactérias com AmpC induzível
# HECKY :: Hafnia alvei; Enterobacter cloacae; Citrobacter freundii; Klebsiella aerogenes; Yersinia enterocolitica
> Bactérias com betalactamase AmpC cromossômica, que pode ser induzida durante o tratamento. O risco é maior com Enterobacter cloacae, Klebsiella aerogenes e Citrobacter freundii.
! Preferir cefepime ou carbapenêmico: a ceftriaxona pode selecionar resistência durante o tratamento.
^c
@ Candida score
# Candida score ≥ 3 :: Nutrição parenteral = 1 ponto; Cirurgia = 1 ponto; Colonização multifocal = 1 ponto; Sepse grave = 2 pontos
> Escore de León (2006) para estimar o risco de candidíase invasiva no paciente crítico não neutropênico e apoiar o antifúngico empírico.
^c
@ Quando o cateter venoso tem de sair
# TIRES :: Túnel ou bolsa infectados; Instabilidade ou sepse grave; Refratária: bacteremia além de 72 h; Endocardite ou tromboflebite supurativa; S. aureus, Pseudomonas e Candida
> Situações em que manter o cateter impede a cura da infecção de corrente sanguínea, segundo as diretrizes da IDSA.
^o
@ Parâmetro de eficácia de cada antimicrobiano
# T · P · A :: Tempo acima da CIM = β-lactâmicos (infusão estendida); Pico sobre a CIM = aminoglicosídeos (dose única diária); Área sob a curva sobre a CIM = vancomicina e quinolonas
> Farmacodinâmica: cada classe mata bactérias de um jeito, e isso define como infundir e como monitorar o nível sérico.
^c
@ Antibióticos com ação contra Pseudomonas
# CAMPAQ :: Cefepime e ceftazidima; Aminoglicosídeos; Meropenem e imipenem; Piperacilina-tazobactam; Aztreonam; Quinolonas (ciprofloxacino e levofloxacino)
> Lista para o empírico quando há risco de Pseudomonas: antibiótico recente, bronquiectasia, ventilação prolongada ou neutropenia.
! Ertapenem não cobre Pseudomonas.
^o
@ Antibióticos com ação contra MRSA
# VaLiDa TeC :: Va = Vancomicina; Li = Linezolida; Da = Daptomicina (não serve para pneumonia); Te = Teicoplanina; C = Ceftarolina
> Opções quando há risco ou confirmação de Staphylococcus aureus resistente à meticilina. A escolha depende do sítio da infecção.
^o
@ Duração curta de antibiótico: quatro números
# 5-7-7-4 :: 5 dias = pneumonia comunitária com boa evolução; 7 dias = pneumonia associada à ventilação; 7 dias (2) = bacteremia por gram-negativo não complicada; 4 dias = infecção intra-abdominal com foco controlado
> Tempos curtos apoiados por ensaios como PneumA (pneumonia do ventilador), STOP-IT (infecção abdominal) e Yahav (bacteremia por gram-negativo).
^c
@ Critérios de SIRS
# TFFL :: Temperatura > 38 ou < 36 °C; Frequência cardíaca > 90; Frequência respiratória > 20 ou PaCO₂ < 32; Leucócitos > 12 mil, < 4 mil ou > 10% de bastões
> Critérios de 1991 (Bone). Sensíveis e pouco específicos; ainda aparecem em escores, em protocolos de triagem e em questões.
! Saiu da definição de sepse em 2016, mas ainda cai em prova.
^c
@ Doenças de precaução por aerossóis
# TSV :: Tuberculose pulmonar ou laríngea; Sarampo; Varicela e zóster disseminado
> Partículas menores que 5 micra ficam suspensas no ar e exigem precaução por aerossóis, diferente da precaução por gotículas.
! Quarto com pressão negativa e máscara N95/PFF2.
^c
@ Clostridioides difficile grave
# 15 / 1,5 :: 15 mil = leucócitos acima disso; 1,5 = creatinina acima disso (mg/dL); Fulminante = choque, íleo ou megacólon
> Critérios de gravidade da IDSA/SHEA (2018), que orientam o tratamento e a avaliação cirúrgica na forma fulminante.
^c
@ Procalcitonina para suspender antibiótico
# 0,5 ou 80% :: 0,5 = valor (ng/mL) abaixo do qual considerar suspender; 80% = queda em relação ao pico que autoriza suspender
> Regra de parada usada nos ensaios PRORATA e SAPS, em que guiar pela procalcitonina reduziu os dias de antibiótico sem aumentar a mortalidade.
^c
@ Febre não infecciosa na UTI
# PAGART :: Pancreatite; Abstinência; Gota e artrite por cristal; Adrenal insuficiente; Reação a fármaco ou transfusão; Trombose venosa e embolia
> Nem toda febre na UTI é infecção. Lembrar das causas não infecciosas evita antibiótico desnecessário.
! Febre central (hemorragia no sistema nervoso) é diagnóstico de exclusão.
^o
@ Infecções em que o corticoide entra
# "Meu Pulmão Tem Choque Pesado" :: Meu = Meningite bacteriana (dexametasona); Pulmão = Pneumocistose com PaO₂ < 70; Tem = Tuberculose meníngea; Choque = Choque séptico em vasopressor; Pesado = Pneumonia comunitária grave
> Situações infecciosas em que o corticoide adjuvante tem evidência de benefício. Fora delas, tende a prejudicar.
^of

## 04 🧠 Neurointensivismo
@ Escala de coma de Glasgow: pontuação máxima
# OVM 4-5-6 :: Olhos = 4; Verbal = 5; Motor = 6
> Escala de Teasdale e Jennett (1974), linguagem universal do nível de consciência. Escore de 8 ou menos define coma e costuma indicar via aérea definitiva.
^c
@ Resposta motora do Glasgow, de 6 a 1
# OLRFEN :: Obedece a comandos; Localiza a dor; Retira à dor; Flexão anormal (decorticação); Extensão anormal (descerebração); Nenhuma resposta
> O componente motor é o que mais pesa no prognóstico do Glasgow. Pontua-se sempre a melhor resposta obtida.
^c
@ Tríade de Cushing
# HBR :: Hipertensão arterial; Bradicardia; Respiração irregular
> Resposta do tronco encefálico à hipertensão intracraniana grave, descrita por Harvey Cushing em 1901.
! Sinal tardio de hipertensão intracraniana com herniação iminente.
^c
@ Medidas gerais na hipertensão intracraniana
# NORMAS :: Normotermia e normocapnia (PaCO₂ 35–40); Oxigenação adequada; Reta e elevada: cabeça neutra a 30°; Manter a pressão de perfusão cerebral ≥ 60; Analgesia e sedação; Sódio ≥ 140 e sem solução hipotônica
> Medidas de primeira camada para todo paciente com hipertensão intracraniana, antes de osmoterapia, hiperventilação transitória ou cirurgia.
^o
@ Herniação uncal
# MHR :: Midríase do mesmo lado; Hemiparesia do lado oposto; Rebaixamento da consciência
> O úncus do lobo temporal comprime o terceiro nervo e o pedúnculo cerebral. É emergência: osmoterapia e neurocirurgia.
^c
@ Reconhecer o AVC
# SAMU :: Sorriso torto; Abraço: um braço cai; Música: fala alterada; Urgente: ligar 192
> Versão brasileira das escalas pré-hospitalares (FAST, Cincinnati) para o leigo reconhecer o AVC e acionar o serviço de emergência.
^c
@ Trombólise no AVC isquêmico: números
# 4,5 · 185/110 · 0,9 :: 4,5 h = janela; 185/110 = pressão máxima antes de trombolisar; 0,9 mg/kg = alteplase (máximo 90 mg, 10% em bolus); 180/105 = pressão máxima nas 24 h seguintes
> Números da trombólise intravenosa no AVC isquêmico, vindos dos ensaios NINDS (até 3 h) e ECASS III (até 4,5 h).
^c
@ Complicações da hemorragia subaracnóidea
# CHAVE-R :: Convulsão; Hidrocefalia; Atordoamento miocárdico e edema pulmonar neurogênico; Vasoespasmo e isquemia tardia (dias 4 a 14); Eletrólitos: hiponatremia; Ressangramento (primeiras 24 h)
> A hemorragia subaracnóidea aneurismática mata pelo sangramento e, depois, pelas complicações. A sigla organiza a vigilância das duas primeiras semanas.
^o
@ Estado de mal epiléptico: linha do tempo
# 5-20-40-60 :: 0–5 min = estabilizar, glicemia e acesso; 5–20 min = benzodiazepínico; 20–40 min = segunda linha (levetiracetam, valproato ou fenitoína); 40–60 min = anestésico em infusão com EEG
> Linha do tempo da American Epilepsy Society (2016). O ensaio ESETT (2019) mostrou eficácia semelhante entre os três fármacos de segunda linha.
^c
@ Morte encefálica no Brasil: pré-requisitos
# 6-35-100-94 :: 6 h = observação mínima (24 h se a causa for hipóxico-isquêmica); 35 °C = temperatura mínima; 100 mmHg = pressão sistólica mínima (ou PAM 65); 94% = saturação mínima
> Condições que precisam estar corrigidas antes de abrir o protocolo de morte encefálica, segundo a Resolução CFM 2.173/2017.
^c
@ Morte encefálica no Brasil: etapas
# CCAC :: Clínico: primeiro exame; Clínico de novo: segundo exame por outro médico; Apneia: um teste com PaCO₂ > 55; Complementar: fluxo, EEG ou cintilografia
> Sequência obrigatória do protocolo brasileiro. A notificação é compulsória e o diagnóstico independe de doação de órgãos.
! Resolução CFM 2.173/2017.
^c
@ Reflexos de tronco testados na morte encefálica
# PCOVT :: Pupilar (fotomotor); Corneopalpebral; Oculocefálico; Vestíbulo-calórico; Tosse
> Reflexos examinados em cada um dos dois exames clínicos. A ausência de todos demonstra a falência do tronco encefálico.
^c
@ Guillain-Barré: quando intubar
# 20-30-40 :: 20 = capacidade vital abaixo de 20 mL/kg; 30 = pressão inspiratória máxima pior que −30 cmH₂O; 40 = pressão expiratória máxima abaixo de 40 cmH₂O
> Regra à beira do leito para indicar intubação eletiva nas doenças neuromusculares, antes da hipercapnia e da parada respiratória.
^c
@ Causas de coma
# AEIOU TIPS :: Álcool; Epilepsia, eletrólitos e encefalopatia; Insulina: hipo ou hiperglicemia; Opioides e overdose; Uremia; Trauma e temperatura; Infecção; Psiquiátrico e porfiria; Stroke (AVC), sangramento subaracnóideo e choque
> Lista ampla de diagnósticos diferenciais do rebaixamento de consciência sem causa evidente. A glicemia capilar vem antes de tudo.
^c
@ Osmoterapia na hipertensão intracraniana
# 1 · 250 · 30 :: Manitol = 0,25 a 1 g/kg em bolus (osmolaridade < 320); Salina 3% = 250 mL em bolus; Salina 20–23% = 30 mL por acesso central
> Doses dos agentes hiperosmolares usados como ponte até o tratamento definitivo da hipertensão intracraniana.
^c
@ Trauma craniano grave: alvos
# 22 · 60–70 · 100 :: 22 = pressão intracraniana a tratar (mmHg); 60–70 = pressão de perfusão cerebral alvo; 100–110 = pressão sistólica mínima conforme a idade; 35–40 = PaCO₂ alvo
> Alvos da Brain Trauma Foundation (4ª edição, 2016) para o trauma cranioencefálico grave.
^c
@ ICH score da hemorragia intracerebral
# GIVII :: Glasgow: 3–4 vale 2 pontos e 5–12 vale 1; Idade ≥ 80 anos; Volume ≥ 30 mL; Intraventricular; Infratentorial
> Escore de Hemphill (2001) que estima a mortalidade em 30 dias da hemorragia intracerebral. Não deve, sozinho, justificar limitação de suporte.
^c
@ Volume do hematoma pela fórmula ABC/2
# ABC/2 :: A = maior diâmetro (cm); B = diâmetro perpendicular a A; C = número de cortes com sangue × espessura do corte; ÷ 2 = volume em mL
> Método de Kothari (1996) para estimar o volume do hematoma na tomografia sem software. O volume é um dos principais preditores de desfecho.
^c
@ Mau prognóstico depois de PCR (72 h ou mais)
# PENSEI :: Pupilas e córneas sem reflexo; EEG maligno (surto-supressão ou supressão); N20 ausente bilateralmente no potencial evocado; Status mioclônico nas primeiras 72 h; Enolase > 60 µg/L em 48–72 h; Imagem com lesão anóxica difusa
> Preditores usados no algoritmo ERC/ESICM (2021) de prognóstico neurológico após PCR. A avaliação é multimodal e nunca antes de 72 horas.
! Exige pelo menos dois preditores e ausência de sedação residual.
^o
@ Sinais de fratura de base de crânio
# GOBH :: Guaxinim: equimose periorbital; Otorreia ou rinorreia de liquor; Battle: equimose retroauricular; Hemotímpano
> Sinais clínicos que indicam fratura da base do crânio, mesmo antes da tomografia.
! Não passar sonda nasal.
^o
"""
