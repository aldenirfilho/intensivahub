TXT = r"""
## 03 🦠 Sepse e infecções
@ qSOFA
# HAT :: Hipotensão (PAS ≤ 100); Alteração do nível de consciência; Taquipneia (FR ≥ 22)
! Serve para alertar, não para definir sepse: a sensibilidade é baixa.
^c
@ Os seis sistemas do SOFA
# "Rapaz Corajoso Faz Cirurgia No Rim" :: Rapaz = Respiratório (PaO₂/FiO₂); Corajoso = Coagulação (plaquetas); Faz = Fígado (bilirrubina); Cirurgia = Cardiovascular (PAM e vasopressor); No = Neurológico (Glasgow); Rim = Renal (creatinina e diurese)
^of
@ Pacote da primeira hora da sepse
# CLAVE :: Culturas antes do antibiótico; Lactato (repetir se > 2); Antibiótico de amplo espectro; Volume 30 mL/kg se hipotensão ou lactato ≥ 4; Elevar a PAM a 65 com noradrenalina
^o
@ Onde procurar o foco da sepse
# PUPILA :: Pulmão; Urinário; Pele e partes moles; Intra-abdominal; Linha vascular (cateter); Articulação, osso, endocárdio e meninges
^o
@ Controle do foco: os 3 D
# 3 D :: Drenar = abscessos e coleções; Desbridar = tecido necrótico; Dispositivo = retirar o que estiver infectado
^c
@ Prevenção da pneumonia associada à ventilação
# CABEÇA :: Cabeceira entre 30° e 45°; Avaliação diária de sedação e de extubação; Balonete entre 20 e 30 cmH₂O; Evitar troca rotineira do circuito; Cuidado oral; Aspiração subglótica
^o
@ Bactérias do grupo ESKAPE
# ESKAPE :: Enterococcus faecium; Staphylococcus aureus; Klebsiella pneumoniae; Acinetobacter baumannii; Pseudomonas aeruginosa; Enterobacter
^c
@ Enterobactérias com AmpC induzível
# HECKY :: Hafnia alvei; Enterobacter cloacae; Citrobacter freundii; Klebsiella aerogenes; Yersinia enterocolitica
! Preferir cefepime ou carbapenêmico: a ceftriaxona pode selecionar resistência durante o tratamento.
^c
@ Candida score
# Candida score ≥ 3 :: Nutrição parenteral = 1 ponto; Cirurgia = 1 ponto; Colonização multifocal = 1 ponto; Sepse grave = 2 pontos
^c
@ Quando o cateter venoso tem de sair
# TIRES :: Túnel ou bolsa infectados; Instabilidade ou sepse grave; Refratária: bacteremia além de 72 h; Endocardite ou tromboflebite supurativa; S. aureus, Pseudomonas e Candida
^o
@ Parâmetro de eficácia de cada antimicrobiano
# T · P · A :: Tempo acima da CIM = β-lactâmicos (infusão estendida); Pico sobre a CIM = aminoglicosídeos (dose única diária); Área sob a curva sobre a CIM = vancomicina e quinolonas
^c
@ Antibióticos com ação contra Pseudomonas
# CAMPAQ :: Cefepime e ceftazidima; Aminoglicosídeos; Meropenem e imipenem; Piperacilina-tazobactam; Aztreonam; Quinolonas (ciprofloxacino e levofloxacino)
! Ertapenem não cobre Pseudomonas.
^o
@ Antibióticos com ação contra MRSA
# VaLiDa TeC :: Va = Vancomicina; Li = Linezolida; Da = Daptomicina (não serve para pneumonia); Te = Teicoplanina; C = Ceftarolina
^o
@ Duração curta de antibiótico: quatro números
# 5-7-7-4 :: 5 dias = pneumonia comunitária com boa evolução; 7 dias = pneumonia associada à ventilação; 7 dias (2) = bacteremia por gram-negativo não complicada; 4 dias = infecção intra-abdominal com foco controlado
^c
@ Critérios de SIRS
# TFFL :: Temperatura > 38 ou < 36 °C; Frequência cardíaca > 90; Frequência respiratória > 20 ou PaCO₂ < 32; Leucócitos > 12 mil, < 4 mil ou > 10% de bastões
! Saiu da definição de sepse em 2016, mas ainda cai em prova.
^c
@ Doenças de precaução por aerossóis
# TSV :: Tuberculose pulmonar ou laríngea; Sarampo; Varicela e zóster disseminado
! Quarto com pressão negativa e máscara N95/PFF2.
^c
@ Clostridioides difficile grave
# 15 / 1,5 :: 15 mil = leucócitos acima disso; 1,5 = creatinina acima disso (mg/dL); Fulminante = choque, íleo ou megacólon
^c
@ Procalcitonina para suspender antibiótico
# 0,5 ou 80% :: 0,5 = valor (ng/mL) abaixo do qual considerar suspender; 80% = queda em relação ao pico que autoriza suspender
^c
@ Febre não infecciosa na UTI
# PAGART :: Pancreatite; Abstinência; Gota e artrite por cristal; Adrenal insuficiente; Reação a fármaco ou transfusão; Trombose venosa e embolia
! Febre central (hemorragia no sistema nervoso) é diagnóstico de exclusão.
^o
@ Infecções em que o corticoide entra
# "Meu Pulmão Tem Choque Pesado" :: Meu = Meningite bacteriana (dexametasona); Pulmão = Pneumocistose com PaO₂ < 70; Tem = Tuberculose meníngea; Choque = Choque séptico em vasopressor; Pesado = Pneumonia comunitária grave
^of

## 04 🧠 Neurointensivismo
@ Escala de coma de Glasgow: pontuação máxima
# OVM 4-5-6 :: Olhos = 4; Verbal = 5; Motor = 6
^c
@ Resposta motora do Glasgow, de 6 a 1
# OLRFEN :: Obedece a comandos; Localiza a dor; Retira à dor; Flexão anormal (decorticação); Extensão anormal (descerebração); Nenhuma resposta
^c
@ Tríade de Cushing
# HBR :: Hipertensão arterial; Bradicardia; Respiração irregular
! Sinal tardio de hipertensão intracraniana com herniação iminente.
^c
@ Medidas gerais na hipertensão intracraniana
# NORMAS :: Normotermia e normocapnia (PaCO₂ 35–40); Oxigenação adequada; Reta e elevada: cabeça neutra a 30°; Manter a pressão de perfusão cerebral ≥ 60; Analgesia e sedação; Sódio ≥ 140 e sem solução hipotônica
^o
@ Herniação uncal
# MHR :: Midríase do mesmo lado; Hemiparesia do lado oposto; Rebaixamento da consciência
^c
@ Reconhecer o AVC
# SAMU :: Sorriso torto; Abraço: um braço cai; Música: fala alterada; Urgente: ligar 192
^c
@ Trombólise no AVC isquêmico: números
# 4,5 · 185/110 · 0,9 :: 4,5 h = janela; 185/110 = pressão máxima antes de trombolisar; 0,9 mg/kg = alteplase (máximo 90 mg, 10% em bolus); 180/105 = pressão máxima nas 24 h seguintes
^c
@ Complicações da hemorragia subaracnóidea
# CHAVE-R :: Convulsão; Hidrocefalia; Atordoamento miocárdico e edema pulmonar neurogênico; Vasoespasmo e isquemia tardia (dias 4 a 14); Eletrólitos: hiponatremia; Ressangramento (primeiras 24 h)
^o
@ Estado de mal epiléptico: linha do tempo
# 5-20-40-60 :: 0–5 min = estabilizar, glicemia e acesso; 5–20 min = benzodiazepínico; 20–40 min = segunda linha (levetiracetam, valproato ou fenitoína); 40–60 min = anestésico em infusão com EEG
^c
@ Morte encefálica no Brasil: pré-requisitos
# 6-35-100-94 :: 6 h = observação mínima (24 h se a causa for hipóxico-isquêmica); 35 °C = temperatura mínima; 100 mmHg = pressão sistólica mínima (ou PAM 65); 94% = saturação mínima
^c
@ Morte encefálica no Brasil: etapas
# CCAC :: Clínico: primeiro exame; Clínico de novo: segundo exame por outro médico; Apneia: um teste com PaCO₂ > 55; Complementar: fluxo, EEG ou cintilografia
! Resolução CFM 2.173/2017.
^c
@ Reflexos de tronco testados na morte encefálica
# PCOVT :: Pupilar (fotomotor); Corneopalpebral; Oculocefálico; Vestíbulo-calórico; Tosse
^c
@ Guillain-Barré: quando intubar
# 20-30-40 :: 20 = capacidade vital abaixo de 20 mL/kg; 30 = pressão inspiratória máxima pior que −30 cmH₂O; 40 = pressão expiratória máxima abaixo de 40 cmH₂O
^c
@ Causas de coma
# AEIOU TIPS :: Álcool; Epilepsia, eletrólitos e encefalopatia; Insulina: hipo ou hiperglicemia; Opioides e overdose; Uremia; Trauma e temperatura; Infecção; Psiquiátrico e porfiria; Stroke (AVC), sangramento subaracnóideo e choque
^c
@ Osmoterapia na hipertensão intracraniana
# 1 · 250 · 30 :: Manitol = 0,25 a 1 g/kg em bolus (osmolaridade < 320); Salina 3% = 250 mL em bolus; Salina 20–23% = 30 mL por acesso central
^c
@ Trauma craniano grave: alvos
# 22 · 60–70 · 100 :: 22 = pressão intracraniana a tratar (mmHg); 60–70 = pressão de perfusão cerebral alvo; 100–110 = pressão sistólica mínima conforme a idade; 35–40 = PaCO₂ alvo
^c
@ ICH score da hemorragia intracerebral
# GIVII :: Glasgow: 3–4 vale 2 pontos e 5–12 vale 1; Idade ≥ 80 anos; Volume ≥ 30 mL; Intraventricular; Infratentorial
^c
@ Volume do hematoma pela fórmula ABC/2
# ABC/2 :: A = maior diâmetro (cm); B = diâmetro perpendicular a A; C = número de cortes com sangue × espessura do corte; ÷ 2 = volume em mL
^c
@ Mau prognóstico depois de PCR (72 h ou mais)
# PENSEI :: Pupilas e córneas sem reflexo; EEG maligno (surto-supressão ou supressão); N20 ausente bilateralmente no potencial evocado; Status mioclônico nas primeiras 72 h; Enolase > 60 µg/L em 48–72 h; Imagem com lesão anóxica difusa
! Exige pelo menos dois preditores e ausência de sedação residual.
^o
@ Sinais de fratura de base de crânio
# GOBH :: Guaxinim: equimose periorbital; Otorreia ou rinorreia de liquor; Battle: equimose retroauricular; Hemotímpano
! Não passar sonda nasal.
^o
"""
