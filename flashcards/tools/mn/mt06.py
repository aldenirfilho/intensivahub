TXT = r"""
## 11 🚑 Trauma, queimados e pós-operatório
@ Avaliação primária do trauma
# XABCDE :: X = hemorragia externa exsanguinante: comprimir e torniquete; A = via aérea com proteção da coluna cervical; B = ventilação e respiração; C = circulação com controle da hemorragia; D = déficit neurológico (Glasgow e pupilas); E = exposição com prevenção da hipotermia
! O que mata primeiro se trata primeiro.
^c
@ História rápida no trauma
# AMPLA :: Alergias; Medicamentos em uso; Passado médico e prenhez; Líquidos e alimentos ingeridos; Ambiente e eventos do trauma
^c
@ Lesões torácicas com risco imediato de vida
# TOPHAT :: Tamponamento cardíaco; Obstrução de via aérea; Pneumotórax hipertensivo; Hemotórax maciço; Aberto: pneumotórax aberto; Traqueobrônquica: lesão da árvore
! Diagnóstico clínico, na avaliação primária — sem esperar tomografia.
^o
@ Choque hemorrágico: classes do ATLS
# I-II-III-IV :: I = até 15% de perda: sinais normais; II = 15–30%: taquicardia e pressão de pulso estreita; III = 30–40%: hipotensão e confusão; IV = mais de 40%: letargia e pressão muito baixa
! A pressão só cai na classe III — taquicardia e pressão de pulso avisam antes.
^c
@ Reanimação de controle de danos
# SANGRA :: Sistólica 80–90 até o controle (hipotensão permissiva); Ácido tranexâmico em até 3 h; Não encher de cristaloide; Glóbulos, plasma e plaquetas 1:1:1; Reaquecer e repor cálcio; Abreviar a cirurgia (controle de danos)
! No trauma craniano grave não se usa hipotensão permissiva.
^o
@ FAST: as quatro janelas
# 4 P :: Pericárdio = janela subxifoide; Peri-hepática = espaço de Morrison; Periesplênica = recesso esplenorrenal; Pelve = fundo de saco
! O E-FAST acrescenta o tórax: pneumotórax e hemotórax.
^c
@ Tríade da embolia gordurosa
# RNP :: Respiratório: hipoxemia; Neurológico: confusão; Petéquias em tórax, axilas e conjuntivas
! Surge 24–72 h depois de fratura de osso longo; tratamento de suporte.
^c
@ Síndrome compartimental: os 6 P
# 6 P :: Pain = dor desproporcional e à extensão passiva (o mais precoce); Parestesia = precoce; Palidez = tardia; Paralisia = tardia; Pulso ausente = muito tardio; Poiquilotermia = membro frio
! Pressão do compartimento a menos de 30 mmHg da diastólica indica fasciotomia.
^c
@ Lesão medular: escala ASIA
# A-B-C-D-E :: A = completa: sem função sacral; B = sensibilidade preservada, sem motricidade; C = motricidade preservada, maioria dos músculos com força < 3; D = maioria dos músculos com força ≥ 3; E = normal
^c
@ Queimados: regra dos nove (adulto)
# 9-9-18-18-18-1 :: 9 = cabeça e pescoço; 9 (cada) = membro superior; 18 = tronco anterior; 18 (2) = tronco posterior; 18 (cada) = membro inferior; 1 = períneo
! A palma do paciente, com os dedos, vale ~1%.
^c
@ Queimados: reposição inicial
# 2-3-4 :: 2 = mL/kg/% no adulto; 3 = mL/kg/% na criança; 4 = mL/kg/% na queimadura elétrica
! Metade nas primeiras 8 h contadas da queimadura; ajustar pela diurese.
^o
@ Lesão inalatória: quando intubar cedo
# ROUCO :: Rouquidão ou estridor; Orofaringe com edema ou bolhas; Ultrapassa 40–50% de superfície queimada; Circunferencial no pescoço ou face profunda; Obnubilação ou hipoxemia
! Escarro com fuligem mostra exposição, mas sozinho não obriga a intubar.
^o
@ Hemotórax: critérios de toracotomia
# 1500 · 200 · 2–4 :: 1500 = mL de saída imediata no dreno; 200 = mL por hora mantidos; 2–4 = horas seguidas com esse débito
^c
@ Febre no pós-operatório: os 5 W
# 5 W :: Wind = pulmão (dias 1–2); Water = urina (dias 3–5); Walking = trombose venosa (dia 5 em diante); Wound = ferida operatória (dias 5–7); Wonder drugs = fármacos e hemoderivados
! Atelectasia como causa de febre é contestada: procurar infecção de verdade.
^c
@ Síndrome de esmagamento: perigos na reperfusão
# CHAMP :: Cálcio baixo; Hipovolemia; Acidose; Mioglobinúria; Potássio alto
! Soro antes de liberar o membro.
^o
@ Trauma abdominal: laparotomia imediata
# HEPA :: Hipotensão com FAST positivo; Evisceração; Peritonite; Ar livre na cavidade
^o
@ Fratura de pelve instável
# CINTA :: Cinta pélvica na altura dos trocânteres; Iniciar transfusão maciça; Não manipular a pelve repetidamente; Tamponamento pré-peritoneal ou angioembolização; Avaliar uretra e reto antes de sondar
^o
@ Hipertermia maligna: conduta
# DOSE :: Desligar o anestésico inalatório; Oxigênio a 100% com hiperventilação; Sódio dantroleno 2,5 mg/kg; Esfriar e tratar hipercalemia e acidose
! Primeiro sinal: CO₂ expirado subindo sem explicação e rigidez de masseter.
^o
## 12 🤰 Obstetrícia crítica
@ Hemorragia pós-parto: os 4 T
# 4 T :: Tônus = atonia uterina (~70%); Trauma = lacerações, ruptura e inversão; Tecido = restos placentários e acretismo; Trombina = coagulopatia
^c
@ Síndrome HELLP
# HELLP :: H = hemólise (esquizócitos, LDH ≥ 600); EL = enzimas hepáticas elevadas (2× o normal ou mais); LP = plaquetas abaixo de 100 mil
! Pode ocorrer sem hipertensão nem proteinúria em 10–20%.
^c
@ Pré-eclâmpsia com sinais de gravidade
# GRÁVIDA :: Grande pressão: 160/110 ou mais; Rim: creatinina > 1,1; Aminotransferases em dobro; Visão turva ou cefaleia persistente; Inundação pulmonar (edema agudo); Dor epigástrica ou em hipocôndrio direito; Abaixo de 100 mil plaquetas
! Proteinúria maciça deixou de ser critério de gravidade.
^o
@ Sulfato de magnésio: esquema e nível
# 4 · 1–2 · 4–7 :: 4 = gramas de ataque em 20 min; 1–2 = gramas por hora, até 24 h depois do parto; 4–7 = mEq/L de nível terapêutico
! Antídoto: gluconato de cálcio 1 g.
^c
@ Toxicidade do magnésio em sequência
# "Reflexo, respiração, ritmo" :: Reflexo = patelar some com 8–10 mEq/L; Respiração = deprime com 12–15 mEq/L; Ritmo = bloqueio e parada acima de 25 mEq/L
! Vigiar reflexo, frequência respiratória e diurese a cada hora.
^o
@ PCR na gestante: o que muda
# ÚTERO :: Útero deslocado com a mão para a esquerda; Tubo precoce (via aérea difícil); Em cima do diafragma: acessos venosos; Retirar o feto em 5 min (cesárea perimortem); Olhar causas obstétricas
! Doses de drogas e energia do choque são as mesmas.
^o
@ Causas de PCR materna (de A a H)
# ABCDEFGH :: Anestesia: complicações; Bleeding: hemorragia; Cardiovascular; Drogas (magnésio, opioide); Embolia pulmonar ou amniótica; Febre: sepse; Gerais: os 5 H e 5 T; Hipertensão: pré-eclâmpsia e eclâmpsia
^c
@ Embolia de líquido amniótico: tríade
# HHC :: Hipóxia súbita; Hipotensão ou PCR; Coagulopatia (CIVD)
! No trabalho de parto ou até 30 min depois; diagnóstico clínico de exclusão.
^c
@ Fisiologia da gestação que muda a UTI
# "Mais volume, menos reserva" :: Débito cardíaco = sobe 30–50%; Volume plasmático = sobe 40–50% (anemia dilucional); PaCO₂ = 28–32 mmHg, com bicarbonato baixo; Capacidade residual funcional = cai 20%: dessatura rápido; Creatinina = cai: 1,0 já é alterada; Coagulação = estado pró-trombótico
^o
@ Uterotônicos em sequência
# "O Elefante Mama Calmamente" :: O = Ocitocina; Elefante = Ergometrina (não na hipertensa); Mama = Misoprostol; Calmamente = Carboprost (não na asmática)
! Ácido tranexâmico 1 g em até 3 h do parto, junto com o primeiro uterotônico.
^of
@ Esteatose aguda da gestação × HELLP
# "Fígado que falha" :: Hipoglicemia = fala a favor de esteatose aguda; Amônia e INR altos = insuficiência hepática verdadeira; Hemólise com plaquetas muito baixas = fala a favor de HELLP; Conduta = parto nos dois casos
^o
@ Microangiopatias da gestação: o parto resolve?
# "Parto resolve?" :: HELLP = sim, em 48–72 h; Esteatose aguda = sim; Púrpura trombocitopênica trombótica = não: plasmaférese; Hemolítico-urêmica atípica = não: bloqueio do complemento
! Piora ou não melhora 72 h depois do parto: pensar nas duas últimas.
^o
@ Cardiomiopatia periparto: definição
# 1 · 5 · 45 :: 1 = último mês de gestação; 5 = até 5 meses depois do parto; 45 = fração de ejeção abaixo de 45%, sem outra causa
^c
@ Crise hipertensiva na gestação: fármacos
# HNL :: Hidralazina intravenosa; Nifedipino oral; Labetalol intravenoso
! Alvo: abaixo de 160/110 em 30–60 min. Evitar IECA e BRA.
^o
@ Sepse materna: focos
# PUMA :: Pielonefrite; Útero: corioamnionite e endometrite; Mama: mastite e abscesso; Aborto infectado e ferida operatória
! Estreptococo do grupo A no puerpério mata em horas.
^o
@ Tromboembolismo na gestante: imagem e tratamento
# "Perna primeiro" :: Perna = Doppler se houver sintoma: positivo já trata; Pulmão = radiografia normal → cintilografia, alterada → angiotomografia; Heparina = de baixo peso molecular (não atravessa a placenta); Proibidos = varfarina e anticoagulantes orais diretos
! D-dímero sobe na gestação normal.
^o
@ Eclâmpsia: conduta
# PARTO :: Proteger a via aérea e lateralizar; Administrar sulfato de magnésio; Reduzir a pressão se 160/110 ou mais; Tirar o feto depois de estabilizar a mãe; Observar 24–48 h (pode ocorrer no puerpério)
! Magnésio é superior a diazepam e fenitoína.
^o
@ Índice de choque na hemorragia obstétrica
# 0,9 · 1,4 · 1,7 :: 0,9 = risco de transfusão maciça; 1,4 = tratamento agressivo imediato; 1,7 = alto risco de desfecho materno grave
! Índice de choque = frequência cardíaca ÷ pressão sistólica.
^c
"""
