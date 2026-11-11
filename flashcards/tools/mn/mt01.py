TXT = r"""
## 01 🫁 Ventilação mecânica
@ Piora súbita do paciente intubado: o que checar
# DOPE :: Deslocamento do tubo; Obstrução do tubo; Pneumotórax; Equipamento com falha
> Roteiro de resgate quando o paciente em ventilação mecânica dessatura ou piora de repente. Vem do suporte avançado de vida pediátrico e vale para qualquer idade.
! Primeiro gesto: desconectar do ventilador e ventilar com bolsa e O₂ a 100%.
^c
@ Critérios de Berlim para SDRA
# TORA :: Tempo: até 7 dias do insulto; Opacidades bilaterais na imagem; Relação PaO₂/FiO₂ ≤ 300 com PEEP ≥ 5; Ausência de causa cardíaca ou sobrecarga que explique
> Definição de Berlim (2012), a referência das provas para diagnosticar e graduar a SDRA. A definição global de 2023 acrescentou SpO₂/FiO₂ e ultrassom, mas a base é a mesma.
! Leve 200–300, moderada 100–200, grave < 100.
^o
@ Ventilação protetora em três números
# 6-30-15 :: 6 = mL/kg de peso predito; 30 = platô máximo em cmH₂O; 15 = driving pressure máxima em cmH₂O
> Resumo da ventilação protetora que reduziu a mortalidade no ensaio ARMA (2000). A driving pressure foi a variável mais ligada à sobrevida na análise de Amato (2015).
! Driving pressure = platô − PEEP.
^o
@ Posição prona na SDRA (PROSEVA)
# PRONA :: PaO₂/FiO₂ < 150; Recente: SDRA há menos de 36 h; Otimizada antes com PEEP ≥ 5 e FiO₂ ≥ 0,6; No mínimo 16 h por sessão; Até manter P/F ≥ 150 em supino
> Critérios de entrada e de parada do ensaio PROSEVA (2013), que mostrou queda de mortalidade com prona precoce e prolongada na SDRA moderada a grave.
! Contraindicação absoluta: coluna instável.
^o
@ Contraindicações à ventilação não invasiva
# VOMITAR :: Vômitos ou hemorragia digestiva alta; Obstrução de via aérea alta; Máscara não adapta (trauma ou cirurgia de face); Instabilidade hemodinâmica ou arritmia grave; Tosse ineficaz com muita secreção; Agitação ou não colaboração; Rebaixamento de consciência (exceto por hipercapnia)
> Lista para checar antes de colocar a máscara. A VNI mal indicada atrasa a intubação e piora o desfecho, sobretudo na insuficiência respiratória hipoxêmica.
! Coma hipercápnico da DPOC não contraindica: é a melhor indicação.
^o
@ Prontidão para o teste de respiração espontânea
# CHOPE :: Causa da intubação controlada; Hemodinâmica estável; Oxigenação adequada (FiO₂ ≤ 0,4 e PEEP ≤ 8); Paciente com drive respiratório; Equilíbrio ácido-base e eletrolítico aceitável
> Triagem diária de quem já pode fazer o teste de respiração espontânea. Procurar todos os dias encurta o tempo de ventilação mecânica.
^o
@ Sinais de falha no teste de respiração espontânea
# FRASES :: Frequência respiratória > 35; Rebaixamento ou agitação; Arritmia ou FC > 140; Saturação < 90%; Esforço com musculatura acessória; Sudorese e pressão sistólica > 180 ou < 90
> Sinais que mandam interromper o teste de respiração espontânea (30 a 120 min em tubo T ou pressão de suporte baixa) e voltar ao modo anterior.
^o
@ Causas de falha de desmame
# ABCDE :: Airway e pulmão: resistência, complacência e troca; Brain: delirium e sedação residual; Coração: disfunção e edema induzido pelo desmame; Diafragma fraco; Endócrino-metabólico: eletrólitos, tireoide e nutrição
> Roteiro para investigar quem falha repetidamente no teste de respiração espontânea: cada letra é um sistema a revisar antes da próxima tentativa.
! Edema induzido pelo desmame: BNP sobe e surgem linhas B durante o teste.
^c
@ Checagem antes de extubar
# TOSSE :: Tosse eficaz; Obedece a comandos; Secreção pouca; Sem risco de edema de glote (teste de vazamento); Equipe e material de reintubação prontos
> Passar no teste de respiração espontânea não basta: extubar exige também proteger a via aérea. A lista separa "consegue respirar" de "consegue ficar sem tubo".
^o
@ Tratar auto-PEEP no ventilado
# MENOS :: Menor volume-minuto (frequência e volume corrente); Expiração mais longa (I:E de 1:4 a 1:5); Nebulizar broncodilatador; Otimizar o fluxo inspiratório (mais alto); Sedar se houver assincronia
> Conduta no aprisionamento aéreo de asma e DPOC ventilados, em que o ar não sai a tempo e a pressão intratorácica derruba o retorno venoso.
! Colapso súbito no obstrutivo: desconectar o circuito por alguns segundos.
^o
@ Cinco mecanismos de hipoxemia
# SHADE :: Shunt; Hipoventilação; Altitude (baixa pressão inspirada de O₂); Difusão prejudicada; Erro de relação ventilação-perfusão
> Base fisiológica para interpretar qualquer hipoxemia: o gradiente alvéolo-arterial e a resposta ao oxigênio separam os mecanismos.
! Só o shunt não corrige com O₂ a 100%. Gradiente alvéolo-arterial normal = hipoventilação ou altitude.
^o
@ Por que o CO₂ sobe
# "Não quer, não pode, não basta" :: Não quer = drive reduzido (sedativo, lesão central); Não pode = bomba fraca (neuromuscular, fadiga, caixa torácica); Não basta = espaço morto alto ou produção de CO₂ aumentada
> Raciocínio para toda hipercapnia, já que a PaCO₂ depende da ventilação alveolar. Ajuda a decidir entre antídoto, suporte ventilatório e ajuste do ventilador.
^o
@ Assincronias pelo momento do ciclo
# DFC :: Disparo (ineficaz, duplo, auto, reverso); Fluxo (insuficiente ou excessivo); Ciclagem (precoce ou tardia)
> Classificação das assincronias paciente-ventilador pela fase do ciclo em que ocorrem. Assincronia frequente se associa a mais tempo de ventilação.
! A mais comum é o disparo ineficaz, quase sempre por auto-PEEP.
^o
@ Mecanismos de lesão pulmonar induzida pelo ventilador
# "Vento Bravo Abre Buraco Enorme" :: Vento = Volutrauma; Bravo = Barotrauma; Abre = Atelectrauma; Buraco = Biotrauma; Enorme = Ergotrauma (potência mecânica)
> Mecanismos pelos quais o próprio ventilador lesa o pulmão. São a justificativa de volume corrente baixo, PEEP adequada e limite de pressões.
^of
@ ECMO venovenosa: gatilhos do EOLIA
# 50-80-7,25 :: 50 = P/F < 50 por mais de 3 h; 80 = P/F < 80 por mais de 6 h; 7,25 = pH < 7,25 com PaCO₂ ≥ 60 por mais de 6 h
> Critérios de inclusão do ensaio EOLIA (2018), usados na prática para indicar ECMO venovenosa na SDRA grave refratária.
! Sempre depois de otimizar: ventilação protetora, prona e bloqueio neuromuscular.
^c
@ Contraindicações à posição prona
# COLUNA :: Coluna instável (a única absoluta); Olhos e face com trauma ou cirurgia recente; Laparostomia (abdome aberto); Útero gravídico avançado; Neuro: hipertensão intracraniana não controlada; Arritmia grave ou instabilidade
> Checagem antes de pronar. Quase todas as contraindicações são relativas e pesadas contra o risco da hipoxemia refratária.
^o
@ VNI na DPOC exacerbada: três gatilhos
# 7,35-45-25 :: 7,35 = pH abaixo disso; 45 = PaCO₂ acima disso (mmHg); 25 = frequência respiratória acima disso
> A indicação de VNI com maior evidência: na exacerbação de DPOC com acidose respiratória, reduz intubação e mortalidade.
! Reavaliar em 1–2 h: se o pH não melhora, intubar.
^c
@ Índice ROX no cateter nasal de alto fluxo
# ROX 4,88 :: ROX = (SpO₂ ÷ FiO₂) ÷ frequência respiratória; 4,88 ou mais = baixo risco de intubação; Abaixo de 3,85 = alto risco de falha
> Índice validado por Roca (2019) para acompanhar quem está em cateter nasal de alto fluxo e não atrasar a intubação.
! Medir em 2, 6 e 12 horas.
^c
@ Efeitos do cateter nasal de alto fluxo
# PLUMA :: PEEP discreta (2 a 5 cmH₂O); Lavagem do espaço morto nasofaríngeo; Umidificação aquecida; Menor trabalho respiratório; Aporte estável de FiO₂
> Mecanismos que explicam o benefício do cateter nasal de alto fluxo na insuficiência respiratória hipoxêmica (ensaio FLORALI, 2015) e depois da extubação.
^o
@ Peso predito para calcular o volume corrente
# 50 / 45,5 :: Homem = 50 + 0,91 × (altura em cm − 152,4); Mulher = 45,5 + 0,91 × (altura em cm − 152,4)
> O pulmão acompanha a altura, não o peso. Calcular o volume corrente pelo peso real é erro clássico de prova e de plantão, principalmente no obeso.
! Usar a altura, nunca o peso real.
^c
@ Pressão de pico alta: resistência ou complacência?
# Pico × Platô :: Pico alto com platô normal = resistência (broncoespasmo, secreção, tubo dobrado); Pico e platô altos = complacência (pneumotórax, edema, intubação seletiva, auto-PEEP)
> Primeira leitura diante do alarme de pressão alta: a pausa inspiratória mostra se o problema está na via aérea (resistência) ou no pulmão e na caixa torácica (complacência).
^c

## 02 💓 Hemodinâmica e choque
@ Os quatro tipos de choque
# CHOD :: Cardiogênico; Hipovolêmico; Obstrutivo; Distributivo
> Classificação clássica do choque pelo mecanismo. Definir o tipo orienta o primeiro tratamento: volume, inotrópico, desobstrução ou vasopressor.
! Só o distributivo tem débito alto ou normal e resistência baixa.
^o
@ Causas de choque obstrutivo
# TETO :: Tamponamento cardíaco; Embolia pulmonar maciça; Tórax hipertensivo (pneumotórax); Obstrução por auto-PEEP
> Choque obstrutivo se trata desobstruindo, não com volume nem com vasopressor. São as causas a procurar com ultrassom no choque sem explicação.
^o
@ As três janelas da perfusão
# PRC :: Pele: enchimento capilar e livedo; Rim: diurese; Cérebro: nível de consciência
> Três órgãos que mostram a perfusão sem exame de laboratório. Servem para diagnosticar choque e acompanhar a resposta ao tratamento.
! Lactato complementa, mas demora a cair.
^c
@ Quando a variação da pressão de pulso não vale
# LIMITS :: Low: relação FC/FR baixa; Irregular: arritmia; Mecânica com volume corrente < 8 mL/kg; Intra-abdominal: pressão aumentada; Tórax aberto; Spontaneous: respiração espontânea
> Condições em que a variação da pressão de pulso perde validade para prever resposta a volume. Nesses casos, usar a elevação passiva das pernas.
^c
@ Fases da fluidoterapia
# ROSE :: Ressuscitação; Otimização; Sustentação (estabilização); Evacuação (retirada de fluidos)
> Modelo de quatro fases (Malbrain) que lembra que o fluido tem hora de entrar e hora de sair: balanço positivo acumulado se associa a pior desfecho.
^c
@ Fluido é remédio: os 4 D
# 4 D :: Droga = qual fluido; Dose = quanto e em que velocidade; Duração = pelo menor tempo; Descalonamento = retirar quando possível
> Proposta de prescrever fluido como se prescreve antibiótico: com indicação, dose, tempo e plano de retirada.
^c
@ Metas iniciais da ressuscitação
# 65-0,5-2 :: 65 = PAM mínima (mmHg); 0,5 = diurese mínima (mL/kg/h); 2 = lactato alvo abaixo disso (mmol/L)
> Alvos iniciais de ressuscitação no choque séptico, alinhados à Surviving Sepsis Campaign. São ponto de partida, a individualizar.
^c
@ Do que depende a oferta de oxigênio
# CHS :: Coração: débito cardíaco; Hemoglobina; Saturação arterial
> A oferta de oxigênio aos tecidos tem só três componentes ajustáveis. Diante de hipóxia tecidual, pergunta-se qual deles está faltando.
! DO₂ = débito × (1,34 × Hb × SaO₂) × 10.
^o
@ Determinantes do débito cardíaco
# PCPF :: Pré-carga; Contratilidade; Pós-carga; Frequência cardíaca
> Os quatro determinantes sobre os quais agem volume, inotrópicos, vasodilatadores e cronotrópicos. Organizam o raciocínio no baixo débito.
^c
@ Congestão venosa pelo ultrassom (VExUS)
# CHPR :: Cava inferior ≥ 2 cm; Hepática: onda S menor que D ou reversa; Porta: pulsatilidade > 30%; Renal: fluxo venoso interrompido
> Escore de congestão venosa por Doppler (Beaubien-Souligny, 2020), associado a lesão renal aguda no pós-operatório cardíaco. Ajuda a decidir quando parar o volume e retirar fluido.
! Grau 3 = cava dilatada + dois padrões graves.
^o
@ Elevação passiva das pernas: números
# 45-45-90-10 :: 45° = tronco elevado na posição inicial; 45° nas pernas = tronco baixa a zero e pernas sobem; 90 s = janela para medir o débito; 10% = aumento que define resposta
> Teste de resposta a volume que funciona em respiração espontânea e arritmia, por ser uma "autotransfusão" reversível de cerca de 300 mL.
! Medir débito ou integral velocidade-tempo, não a pressão arterial.
^c
@ Estágios SCAI do choque cardiogênico
# ABCDE :: At risk: em risco; Beginning: pré-choque; Classic: hipoperfusão que exige intervenção; Deteriorating: piora apesar do suporte; Extremis: colapso ou PCR
> Classificação da SCAI (2019, revista em 2022) que padroniza a gravidade do choque cardiogênico e orienta a escalada para suporte mecânico.
^c
@ Lactato alto sem hipoperfusão (tipo B)
# FATAL :: Fígado insuficiente; Adrenalina e β2-agonistas; Tiamina em falta; Agentes: metformina, linezolida e propofol; Linfoma e leucemia
> Lactato alto nem sempre é hipoperfusão. Lembrar das causas tipo B evita dar volume a quem não precisa.
^o
@ Por que a saturação venosa central cai
# DASH :: Débito baixo; Anemia; Saturação arterial baixa; Hipermetabolismo: febre, dor, agitação e tremor
> A saturação venosa central reflete o equilíbrio entre oferta e consumo de oxigênio. A sigla lista o que desequilibra essa conta.
^o
@ Três números da perfusão global
# 70-6-1,4 :: 70 = ScvO₂ mínima (%); 6 = gap venoarterial de CO₂ acima do qual o fluxo é insuficiente (mmHg); 1,4 = razão gap de CO₂ ÷ diferença arteriovenosa de O₂ que sugere anaerobiose
> Marcadores para avaliar se o débito cardíaco atende à demanda, úteis quando o lactato demora a cair ou a saturação venosa está normal apesar do choque.
^c
@ Escada do choque séptico refratário
# NVAH :: Noradrenalina: primeira linha; Vasopressina: associar com nora em 0,25–0,5 µg/kg/min; Adrenalina: terceiro agente; Hidrocortisona 200 mg/dia
> Ordem de escalada recomendada pela Surviving Sepsis Campaign no choque séptico que não responde à noradrenalina.
^c
@ Pressões normais no cateter de artéria pulmonar
# 5 · 25/5 · 25/10 · 10 :: Átrio direito = ~5 mmHg; Ventrículo direito = 25/5; Artéria pulmonar = 25/10; Oclusão = ~10
> Valores de referência para interpretar o cateter de Swan-Ganz e reconhecer cada curva enquanto o cateter progride.
^c
@ Tríade de Beck do tamponamento
# HBT :: Hipotensão; Bulhas abafadas; Turgência jugular
> Tríade descrita por Claude Beck em 1935 para o tamponamento agudo. Na prática, quem confirma é o ecocardiograma.
! Presente completa em minoria; pulso paradoxal > 10 mmHg ajuda.
^c
@ Escore de livedo (mottling) de 0 a 5
# Joelho → virilha :: 0 = sem livedo; 1 = área de uma moeda no joelho; 2 = até a borda superior da patela; 3 = até o meio da coxa; 4 = até a virilha; 5 = além da virilha
> Escore de Ait-Oufella (2011): a extensão do livedo a partir do joelho se associa à mortalidade no choque séptico.
^c
@ Tempo de enchimento capilar
# 10-3-30 :: 10 s = compressão da polpa digital; 3 s = limite do normal; 30 min = intervalo de reavaliação na ressuscitação
> Técnica padronizada no ensaio ANDROMEDA-SHOCK (2019), em que guiar a ressuscitação pelo enchimento capilar não foi inferior a guiar pelo lactato.
^c
@ Perfil hemodinâmico dos choques
# Débito · Resistência · PVC :: Hipovolêmico = débito baixo, resistência alta, PVC baixa; Cardiogênico = débito baixo, resistência alta, PVC alta; Distributivo = débito alto ou normal, resistência baixa, PVC baixa; Obstrutivo = débito baixo, resistência alta, PVC alta
> Tabela clássica de prova: diferencia os choques pelo débito, pela resistência vascular e pelas pressões de enchimento.
^c
"""
