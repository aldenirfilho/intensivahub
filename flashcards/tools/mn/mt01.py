TXT = r"""
## 01 🫁 Ventilação mecânica
@ Piora súbita do paciente intubado: o que checar
# DOPE :: Deslocamento do tubo; Obstrução do tubo; Pneumotórax; Equipamento com falha
! Primeiro gesto: desconectar do ventilador e ventilar com bolsa e O₂ a 100%.
^c
@ Critérios de Berlim para SDRA
# TORA :: Tempo: até 7 dias do insulto; Opacidades bilaterais na imagem; Relação PaO₂/FiO₂ ≤ 300 com PEEP ≥ 5; Ausência de causa cardíaca ou sobrecarga que explique
! Leve 200–300, moderada 100–200, grave < 100.
^o
@ Ventilação protetora em três números
# 6-30-15 :: 6 = mL/kg de peso predito; 30 = platô máximo em cmH₂O; 15 = driving pressure máxima em cmH₂O
! Driving pressure = platô − PEEP.
^o
@ Posição prona na SDRA (PROSEVA)
# PRONA :: PaO₂/FiO₂ < 150; Recente: SDRA há menos de 36 h; Otimizada antes com PEEP ≥ 5 e FiO₂ ≥ 0,6; No mínimo 16 h por sessão; Até manter P/F ≥ 150 em supino
! Contraindicação absoluta: coluna instável.
^o
@ Contraindicações à ventilação não invasiva
# VOMITAR :: Vômitos ou hemorragia digestiva alta; Obstrução de via aérea alta; Máscara não adapta (trauma ou cirurgia de face); Instabilidade hemodinâmica ou arritmia grave; Tosse ineficaz com muita secreção; Agitação ou não colaboração; Rebaixamento de consciência (exceto por hipercapnia)
! Coma hipercápnico da DPOC não contraindica: é a melhor indicação.
^o
@ Prontidão para o teste de respiração espontânea
# CHOPE :: Causa da intubação controlada; Hemodinâmica estável; Oxigenação adequada (FiO₂ ≤ 0,4 e PEEP ≤ 8); Paciente com drive respiratório; Equilíbrio ácido-base e eletrolítico aceitável
^o
@ Sinais de falha no teste de respiração espontânea
# FRASES :: Frequência respiratória > 35; Rebaixamento ou agitação; Arritmia ou FC > 140; Saturação < 90%; Esforço com musculatura acessória; Sudorese e pressão sistólica > 180 ou < 90
^o
@ Causas de falha de desmame
# ABCDE :: Airway e pulmão: resistência, complacência e troca; Brain: delirium e sedação residual; Coração: disfunção e edema induzido pelo desmame; Diafragma fraco; Endócrino-metabólico: eletrólitos, tireoide e nutrição
! Edema induzido pelo desmame: BNP sobe e surgem linhas B durante o teste.
^c
@ Checagem antes de extubar
# TOSSE :: Tosse eficaz; Obedece a comandos; Secreção pouca; Sem risco de edema de glote (teste de vazamento); Equipe e material de reintubação prontos
^o
@ Tratar auto-PEEP no ventilado
# MENOS :: Menor volume-minuto (frequência e volume corrente); Expiração mais longa (I:E de 1:4 a 1:5); Nebulizar broncodilatador; Otimizar o fluxo inspiratório (mais alto); Sedar se houver assincronia
! Colapso súbito no obstrutivo: desconectar o circuito por alguns segundos.
^o
@ Cinco mecanismos de hipoxemia
# SHADE :: Shunt; Hipoventilação; Altitude (baixa pressão inspirada de O₂); Difusão prejudicada; Erro de relação ventilação-perfusão
! Só o shunt não corrige com O₂ a 100%. Gradiente alvéolo-arterial normal = hipoventilação ou altitude.
^o
@ Por que o CO₂ sobe
# "Não quer, não pode, não basta" :: Não quer = drive reduzido (sedativo, lesão central); Não pode = bomba fraca (neuromuscular, fadiga, caixa torácica); Não basta = espaço morto alto ou produção de CO₂ aumentada
^o
@ Assincronias pelo momento do ciclo
# DFC :: Disparo (ineficaz, duplo, auto, reverso); Fluxo (insuficiente ou excessivo); Ciclagem (precoce ou tardia)
! A mais comum é o disparo ineficaz, quase sempre por auto-PEEP.
^o
@ Mecanismos de lesão pulmonar induzida pelo ventilador
# "Vento Bravo Abre Buraco Enorme" :: Vento = Volutrauma; Bravo = Barotrauma; Abre = Atelectrauma; Buraco = Biotrauma; Enorme = Ergotrauma (potência mecânica)
^of
@ ECMO venovenosa: gatilhos do EOLIA
# 50-80-7,25 :: 50 = P/F < 50 por mais de 3 h; 80 = P/F < 80 por mais de 6 h; 7,25 = pH < 7,25 com PaCO₂ ≥ 60 por mais de 6 h
! Sempre depois de otimizar: ventilação protetora, prona e bloqueio neuromuscular.
^c
@ Contraindicações à posição prona
# COLUNA :: Coluna instável (a única absoluta); Olhos e face com trauma ou cirurgia recente; Laparostomia (abdome aberto); Útero gravídico avançado; Neuro: hipertensão intracraniana não controlada; Arritmia grave ou instabilidade
^o
@ VNI na DPOC exacerbada: três gatilhos
# 7,35-45-25 :: 7,35 = pH abaixo disso; 45 = PaCO₂ acima disso (mmHg); 25 = frequência respiratória acima disso
! Reavaliar em 1–2 h: se o pH não melhora, intubar.
^c
@ Índice ROX no cateter nasal de alto fluxo
# ROX 4,88 :: ROX = (SpO₂ ÷ FiO₂) ÷ frequência respiratória; 4,88 ou mais = baixo risco de intubação; Abaixo de 3,85 = alto risco de falha
! Medir em 2, 6 e 12 horas.
^c
@ Efeitos do cateter nasal de alto fluxo
# PLUMA :: PEEP discreta (2 a 5 cmH₂O); Lavagem do espaço morto nasofaríngeo; Umidificação aquecida; Menor trabalho respiratório; Aporte estável de FiO₂
^o
@ Peso predito para calcular o volume corrente
# 50 / 45,5 :: Homem = 50 + 0,91 × (altura em cm − 152,4); Mulher = 45,5 + 0,91 × (altura em cm − 152,4)
! Usar a altura, nunca o peso real.
^c
@ Pressão de pico alta: resistência ou complacência?
# Pico × Platô :: Pico alto com platô normal = resistência (broncoespasmo, secreção, tubo dobrado); Pico e platô altos = complacência (pneumotórax, edema, intubação seletiva, auto-PEEP)
^c

## 02 💓 Hemodinâmica e choque
@ Os quatro tipos de choque
# CHOD :: Cardiogênico; Hipovolêmico; Obstrutivo; Distributivo
! Só o distributivo tem débito alto ou normal e resistência baixa.
^o
@ Causas de choque obstrutivo
# TETO :: Tamponamento cardíaco; Embolia pulmonar maciça; Tórax hipertensivo (pneumotórax); Obstrução por auto-PEEP
^o
@ As três janelas da perfusão
# PRC :: Pele: enchimento capilar e livedo; Rim: diurese; Cérebro: nível de consciência
! Lactato complementa, mas demora a cair.
^c
@ Quando a variação da pressão de pulso não vale
# LIMITS :: Low: relação FC/FR baixa; Irregular: arritmia; Mecânica com volume corrente < 8 mL/kg; Intra-abdominal: pressão aumentada; Tórax aberto; Spontaneous: respiração espontânea
^c
@ Fases da fluidoterapia
# ROSE :: Ressuscitação; Otimização; Sustentação (estabilização); Evacuação (retirada de fluidos)
^c
@ Fluido é remédio: os 4 D
# 4 D :: Droga = qual fluido; Dose = quanto e em que velocidade; Duração = pelo menor tempo; Descalonamento = retirar quando possível
^c
@ Metas iniciais da ressuscitação
# 65-0,5-2 :: 65 = PAM mínima (mmHg); 0,5 = diurese mínima (mL/kg/h); 2 = lactato alvo abaixo disso (mmol/L)
^c
@ Do que depende a oferta de oxigênio
# CHS :: Coração: débito cardíaco; Hemoglobina; Saturação arterial
! DO₂ = débito × (1,34 × Hb × SaO₂) × 10.
^o
@ Determinantes do débito cardíaco
# PCPF :: Pré-carga; Contratilidade; Pós-carga; Frequência cardíaca
^c
@ Congestão venosa pelo ultrassom (VExUS)
# CHPR :: Cava inferior ≥ 2 cm; Hepática: onda S menor que D ou reversa; Porta: pulsatilidade > 30%; Renal: fluxo venoso interrompido
! Grau 3 = cava dilatada + dois padrões graves.
^o
@ Elevação passiva das pernas: números
# 45-45-90-10 :: 45° = tronco elevado na posição inicial; 45° nas pernas = tronco baixa a zero e pernas sobem; 90 s = janela para medir o débito; 10% = aumento que define resposta
! Medir débito ou integral velocidade-tempo, não a pressão arterial.
^c
@ Estágios SCAI do choque cardiogênico
# ABCDE :: At risk: em risco; Beginning: pré-choque; Classic: hipoperfusão que exige intervenção; Deteriorating: piora apesar do suporte; Extremis: colapso ou PCR
^c
@ Lactato alto sem hipoperfusão (tipo B)
# FATAL :: Fígado insuficiente; Adrenalina e β2-agonistas; Tiamina em falta; Agentes: metformina, linezolida e propofol; Linfoma e leucemia
^o
@ Por que a saturação venosa central cai
# DASH :: Débito baixo; Anemia; Saturação arterial baixa; Hipermetabolismo: febre, dor, agitação e tremor
^o
@ Três números da perfusão global
# 70-6-1,4 :: 70 = ScvO₂ mínima (%); 6 = gap venoarterial de CO₂ acima do qual o fluxo é insuficiente (mmHg); 1,4 = razão gap de CO₂ ÷ diferença arteriovenosa de O₂ que sugere anaerobiose
^c
@ Escada do choque séptico refratário
# NVAH :: Noradrenalina: primeira linha; Vasopressina: associar com nora em 0,25–0,5 µg/kg/min; Adrenalina: terceiro agente; Hidrocortisona 200 mg/dia
^c
@ Pressões normais no cateter de artéria pulmonar
# 5 · 25/5 · 25/10 · 10 :: Átrio direito = ~5 mmHg; Ventrículo direito = 25/5; Artéria pulmonar = 25/10; Oclusão = ~10
^c
@ Tríade de Beck do tamponamento
# HBT :: Hipotensão; Bulhas abafadas; Turgência jugular
! Presente completa em minoria; pulso paradoxal > 10 mmHg ajuda.
^c
@ Escore de livedo (mottling) de 0 a 5
# Joelho → virilha :: 0 = sem livedo; 1 = área de uma moeda no joelho; 2 = até a borda superior da patela; 3 = até o meio da coxa; 4 = até a virilha; 5 = além da virilha
^c
@ Tempo de enchimento capilar
# 10-3-30 :: 10 s = compressão da polpa digital; 3 s = limite do normal; 30 min = intervalo de reavaliação na ressuscitação
^c
@ Perfil hemodinâmico dos choques
# Débito · Resistência · PVC :: Hipovolêmico = débito baixo, resistência alta, PVC baixa; Cardiogênico = débito baixo, resistência alta, PVC alta; Distributivo = débito alto ou normal, resistência baixa, PVC baixa; Obstrutivo = débito baixo, resistência alta, PVC alta
^c
"""
