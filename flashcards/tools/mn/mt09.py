TXT = r"""
## 01 🫁 Ventilação mecânica
@ Hipoxemia refratária na SDRA: escada de resgate
# POBRE :: Prona por 16 h ou mais; Otimizar a PEEP; Bloqueador neuromuscular nas primeiras 48 h; Restringir fluidos depois da ressuscitação; ECMO venovenosa em centro de referência
! Óxido nítrico inalado melhora a oxigenação, mas não a sobrevida.
> Sequência de medidas quando a relação PaO₂/FiO₂ segue abaixo de 150 apesar da ventilação protetora. A prona é a que tem maior evidência de redução de mortalidade (PROSEVA).
^o
@ Alto risco de falha de extubação
# IDOSA :: Idade acima de 65 anos; DPOC moderada a grave; Obesidade (IMC acima de 30); Secreção abundante com tosse fraca; APACHE II acima de 12 no dia da extubação
! Também contam insuficiência cardíaca, desmame difícil e ventilação por mais de 7 dias.
> Critérios dos ensaios de Hernández (2016) para definir quem recebe suporte preventivo depois de extubar: ventilação não invasiva, cateter nasal de alto fluxo ou os dois.
^o
@ Desmame: simples, difícil e prolongado
# 1 · 3 · 7 :: Simples = extubado no primeiro teste de respiração espontânea; Difícil = até 3 testes ou até 7 dias depois do primeiro; Prolongado = mais de 3 testes ou mais de 7 dias
> Classificação da conferência de consenso de 2007 (Boles). O desmame prolongado concentra a mortalidade e os dias de ventilação.
^c
@ PEEP: efeitos sobre a circulação
# "Menos retorno, menos pós-carga do VE" :: Retorno venoso = cai, e com ele a pré-carga do ventrículo direito; Pós-carga do ventrículo direito = sobe quando há hiperdistensão alveolar; Pós-carga do ventrículo esquerdo = cai, o que ajuda na insuficiência cardíaca; Hipovolêmico = é quem mais hipotende
> Interação coração-pulmão sob pressão positiva. Explica a hipotensão depois de intubar e o benefício da pressão positiva no edema agudo de pulmão.
^o
@ Pressão de oclusão (P0,1): leitura do drive
# 1,5 · 3,5 :: Abaixo de 1,5 cmH₂O = drive baixo: rever sedação e excesso de suporte; De 1,5 a 3,5 = faixa-alvo; Acima de 3,5 = drive alto: risco de lesão pulmonar autoinfligida
> Queda da pressão na via aérea nos primeiros 100 ms de um esforço contra a via ocluída. A maioria dos ventiladores mede de forma automática e ajuda a ajustar o suporte.
^c
@ Causas de SDRA
# PASTA :: Pneumonia; Aspiração de conteúdo gástrico; Sepse de foco não pulmonar; Trauma grave e transfusão; Afogamento, pancreatite e inalação tóxica
> Pneumonia e sepse respondem pela maioria dos casos. Identificar e tratar a causa é parte do tratamento, junto com a ventilação protetora.
^o
@ Hipercapnia permissiva: quando evitar
# VIDA :: Ventrículo direito em falência ou hipertensão pulmonar grave; Intracraniana: hipertensão; Doença coronariana instável e arritmia; Acidose metabólica grave associada
> Tolerar PaCO₂ alta, com pH acima de 7,20, é o preço do volume corrente baixo. Nestas situações o CO₂ alto é mal tolerado e pede outra estratégia.
^o
@ Como escolher a PEEP na SDRA
# "Tabela, complacência, esôfago, imagem" :: Tabela PEEP-FiO₂ = método do ARDSNet, simples e validado; Melhor complacência = titulação decremental depois de recrutar; Pressão esofágica = manter a transpulmonar expiratória entre 0 e 10; Tomografia de impedância = equilíbrio entre colapso e hiperdistensão
! Recrutamento agressivo de rotina aumentou a mortalidade (ensaio ART, 2017).
> Nenhum método se mostrou superior em desfecho clínico. A PEEP mais alta beneficia a SDRA moderada a grave com pulmão recrutável.
^o
## 02 💓 Hemodinâmica e choque
@ Resposta a volume: cortes dos testes dinâmicos
# 13 · 10 · 5 :: Variação da pressão de pulso = acima de 13% (zona cinzenta de 9 a 13); Elevação passiva das pernas = aumento de 10% no débito; Oclusão ao fim da expiração = aumento de 5% no débito; Minidesafio de 100 mL = aumento de 10% na integral velocidade-tempo
> Só metade dos pacientes em choque aumenta o débito com volume. Os testes dinâmicos preveem a resposta sem dar o fluido que pode não ajudar.
^c
@ Pressão arterial: o que cada componente informa
# "Sistólica, diastólica, pulso, média" :: Sistólica = volume sistólico e rigidez arterial; Diastólica = tônus vascular: baixa indica vasoplegia e pede vasopressor cedo; Pressão de pulso = estreita sugere volume sistólico baixo; Média = pressão de perfusão dos órgãos
> Leitura da curva arterial antes de qualquer monitor avançado. A diastólica baixa com taquicardia é o sinal de vasodilatação grave no choque séptico.
^o
@ Suporte circulatório mecânico: dispositivos
# "Balão, Impella, ECMO" :: Balão intra-aórtico = cerca de 0,5 L/min: reduz a pós-carga e melhora a perfusão coronariana; Impella = de 2,5 a 5,5 L/min: descarrega o ventrículo esquerdo; ECMO venoarterial = de 4 a 6 L/min: suporte de coração e pulmão, mas aumenta a pós-carga do ventrículo esquerdo
> Opções no choque cardiogênico refratário a drogas. O balão não reduziu a mortalidade no IABP-SHOCK II; a bomba microaxial reduziu no DanGer Shock (2024), em infarto com supra.
^o
@ Choque vasoplégico refratário: resgates
# "Azul, B12, angiotensina" :: Azul de metileno = bloqueia a via do óxido nítrico; Hidroxocobalamina = sequestra óxido nítrico; Angiotensina II = sobe a pressão no choque distributivo (ensaio ATHOS-3); Antes dos resgates = vasopressina e hidrocortisona já otimizadas
> Para a hipotensão que persiste com doses altas de noradrenalina, comum na sepse e depois de circulação extracorpórea. Sobem a pressão; ganho de sobrevida não está demonstrado.
^o
@ Curva de pressão venosa central: ondas
# A-C-X-V-Y :: Átrio contrai; Cúspides da tricúspide se fecham; X: descenso pelo relaxamento atrial; Ventrículo em sístole: o átrio enche com a valva fechada; Y: descenso pela abertura da tricúspide
! Onda a em canhão = dissociação atrioventricular. Onda v gigante = insuficiência tricúspide. Descenso y apagado = tamponamento.
> A forma da curva informa mais que o número. A medida é feita ao final da expiração.
^c
@ Vasopressores: equivalência em noradrenalina
# "Tudo vira noradrenalina" :: Adrenalina = 1 para 1; Dopamina = dose ÷ 100; Fenilefrina = dose ÷ 10; Vasopressina = 0,04 U/min equivalem a cerca de 0,1 µg/kg/min
> Soma das doses em "equivalentes de noradrenalina", usada em ensaios e para definir choque refratário, em geral acima de 0,5 µg/kg/min.
^c
@ Falência aguda do ventrículo direito: conduta
# PROVA :: Pré-carga na medida: sem excesso de volume; Ritmo sinusal preservado; Oxigenar e evitar hipercapnia e acidose; Vasopressor para sustentar a perfusão coronariana; Aumentar a contratilidade e aliviar a pós-carga (dobutamina, milrinona, óxido nítrico)
! Intubar e ventilar com pressão positiva pode precipitar o colapso.
> Embolia pulmonar, SDRA, infarto de ventrículo direito e hipertensão pulmonar descompensada. O ventrículo direito tolera mal o aumento da pós-carga e depende da pressão arterial para se perfundir.
^o
@ Quando parar de dar volume
# CHEIO :: Congestão pulmonar: linhas B novas; Hipoxemia em piora; Elevação da pressão venosa sem ganho de débito; Intra-abdominal: pressão em alta; Onda venosa alterada no Doppler (VExUS)
> Sinais de que o limite de tolerância ao fluido foi atingido. A partir daí, cada bolus soma congestão sem melhorar a perfusão.
^o
## 03 🦠 Sepse e infecções
@ Sepse: prazo do antibiótico (SSC 2021)
# 1 h · 3 h :: Choque séptico ou sepse muito provável = antibiótico em até 1 hora; Sepse possível sem choque = investigar rápido e dar em até 3 horas se a suspeita persistir; Baixa probabilidade de infecção = adiar e observar
> A Surviving Sepsis Campaign de 2021 graduou a urgência pela probabilidade de infecção e pela presença de choque, para reduzir antibiótico desnecessário.
^c
@ Betalactamases: classes de Ambler
# Ambler A-B-C-D :: Classe A = ESBL e KPC (serina): ceftazidima-avibactam cobre a KPC; Classe B = metalobetalactamases (NDM, VIM, IMP): aztreonam com ceftazidima-avibactam; Classe C = AmpC: cefepime ou carbapenêmico; Classe D = OXA-48 em enterobactérias e OXA-23 em Acinetobacter
> Classificação molecular das betalactamases. Saber a classe da carbapenemase define qual dos novos antibióticos funciona.
^c
@ Pneumonia do ventilador: risco de germe multirresistente
# CASAS :: Choque séptico no momento da pneumonia; Antibiótico intravenoso nos últimos 90 dias; SDRA antes da pneumonia; A partir de 5 dias de internação; Substituição renal aguda antes da pneumonia
> Fatores da diretriz IDSA/ATS (2016) que indicam cobertura empírica ampliada, com dois antipseudomonas e cobertura de MRSA conforme a flora local.
^o
@ Candidemia: conduta
# OLHE :: Olho: fundo de olho em todos; Linha central retirada; Hemocultura repetida até negativar; Equinocandina, por 14 dias depois da primeira cultura negativa
! Ecocardiograma se a candidemia persistir ou houver prótese valvar.
> Candida em hemocultura nunca é contaminação. A endoftalmite e a endocardite mudam a duração e a escolha do tratamento.
^o
@ Bacteremia por Staphylococcus aureus: conduta
# ECOA :: Ecocardiograma (transesofágico se houver risco alto); Cultura de controle em 48–72 h; Origem: achar e remover o foco; Antibiótico intravenoso por 14 dias no mínimo, e 4–6 semanas na forma complicada
! Sensível à meticilina: oxacilina ou cefazolina, não vancomicina.
> Staphylococcus aureus em hemocultura tem mortalidade de 20–30% e alta taxa de focos metastáticos. O pacote com parecer do infectologista reduz mortes.
^o
@ Antifúngicos: o buraco de cada um
# "O que cada um não cobre" :: Fluconazol = Candida krusei, parte das glabrata e fungos filamentosos; Equinocandinas = Cryptococcus, e penetram mal em urina, olho e sistema nervoso; Anfotericina B = Candida lusitaniae e Aspergillus terreus; Voriconazol = agentes da mucormicose
> Falhas de espectro que orientam a escolha empírica e a troca depois da identificação da espécie.
^o
@ Cateter venoso central: pacote de inserção
# LIMPA :: Lavar as mãos; Inserir longe da femoral; Máxima barreira estéril; Pele com clorexidina alcoólica; Avaliar todo dia se o cateter ainda é necessário
> Cinco medidas do estudo de Pronovost (Michigan, 2006), que levou a infecção de corrente sanguínea associada a cateter a perto de zero.
^o
## 04 🧠 Neurointensivismo
@ Hemorragia subaracnóidea: escala de Hunt-Hess
# I a V :: I = assintomático ou cefaleia leve; II = cefaleia moderada a intensa e rigidez de nuca, sem déficit além de par craniano; III = sonolência, confusão ou déficit focal leve; IV = estupor e hemiparesia; V = coma e postura de descerebração
> Escala clínica de 1968 que estima o risco cirúrgico e o prognóstico. A da federação mundial de neurocirurgia (WFNS) usa o Glasgow e o déficit motor.
^c
@ Hemorragia subaracnóidea: escala de Fisher modificada
# 0 a 4 :: 0 = sem sangue; 1 = lâmina fina, sem sangue ventricular; 2 = lâmina fina, com sangue ventricular; 3 = sangue espesso, sem ventricular; 4 = sangue espesso, com ventricular
> Gradua a quantidade de sangue na tomografia e prediz o vasoespasmo sintomático, cujo risco cresce de 0 a 4.
^c
@ AVC isquêmico: trombectomia mecânica em números
# 6 · 24 · 6 · 6 :: 6 h = janela padrão a partir do início; 24 h = janela estendida com seleção por imagem (DAWN e DEFUSE 3); NIHSS = 6 ou mais; ASPECTS = 6 ou mais; Oclusão = carótida interna ou segmento M1
! Trombolisar quem é elegível, sem atrasar a trombectomia.
> Critérios clássicos dos ensaios de oclusão de grande vaso. Ensaios mais recentes ampliaram a indicação para infartos extensos (ASPECTS de 3 a 5).
^c
@ Hemorragia intracerebral: pacote de cuidados
# PAGA :: Pressão sistólica abaixo de 140 em 1 hora; Anticoagulação revertida em 1 hora; Glicemia tratada; Antitérmico para a febre
> Pacote do ensaio INTERACT3 (2023), que melhorou o desfecho funcional ao aplicar as quatro medidas juntas e cedo.
^o
@ Fármacos que pioram a miastenia gravis
# "Antibiótico, magnésio, coração, bloqueador" :: Antibióticos = aminoglicosídeos, quinolonas e macrolídeos; Magnésio = reduz a liberação de acetilcolina; Cardiovasculares = betabloqueador e procainamida; Bloqueadores neuromusculares = sensibilidade aumentada aos adespolarizantes; Corticoide em dose alta = piora transitória no início
> Lista para revisar a prescrição do miastênico internado. Infecção e fármacos são os principais gatilhos da crise miastênica.
^o
@ Infarto maligno da cerebral média: craniectomia
# 60 · 48 · 50% :: 60 anos = idade até a qual o benefício é maior; 48 h = prazo a partir do início; 50% = infarto de pelo menos metade do território da cerebral média
! Acima de 60 anos, reduz a morte ao custo de mais sobreviventes com sequela grave (DESTINY II).
> Análise conjunta dos ensaios DECIMAL, DESTINY e HAMLET: a descompressão precoce reduz muito a mortalidade do edema maligno.
^c
@ Escala FOUR de coma
# 4 × 4 :: Olhos = abertura e rastreio; Motor = resposta dos membros; Tronco = reflexos pupilar, corneano e de tosse; Respiração = padrão respiratório e disparo no ventilador
! Cada componente vale de 0 a 4; o total vai de 0 a 16.
> Escala de Wijdicks (2005), alternativa ao Glasgow no paciente intubado, por não depender da resposta verbal e por avaliar o tronco.
^c
## 05 💤 Sedação e via aérea
@ Sedativos: o traço de cada um
# "Rápido, leve, acumula, preserva" :: Propofol = início e fim rápidos, hipotensão e triglicérides altos; Dexmedetomidina = sedação leve sem deprimir a respiração, bradicardia; Midazolam = acumula: mais delirium e mais tempo de ventilação; Cetamina = analgesia e broncodilatação, preserva a pressão
> As diretrizes PADIS preferem propofol ou dexmedetomidina a benzodiazepínicos para sedar o adulto ventilado.
^o
@ Síndrome de infusão do propofol
# BRASA :: Bradiarritmia e padrão de Brugada no ECG; Rabdomiólise; Acidose lática; Soro lipêmico: triglicérides altos; Anúria: lesão renal com hipercalemia
! Risco maior acima de 4 mg/kg/h por mais de 48 h.
> Complicação rara e grave por falha da cadeia respiratória mitocondrial. Suspender o propofol ao primeiro sinal; monitorar CK e triglicérides nas infusões longas.
^o
@ Sugamadex: dose pela profundidade do bloqueio
# 2 · 4 · 16 :: 2 mg/kg = bloqueio moderado, com 2 respostas na sequência de quatro estímulos; 4 mg/kg = bloqueio profundo, com 1 a 2 respostas pós-tetânicas; 16 mg/kg = reversão imediata depois de rocurônio em dose de sequência rápida
> Encapsula rocurônio e vecurônio. Torna o rocurônio em dose alta uma opção reversível quando a intubação e a ventilação falham.
^c
@ Despertar diário: quando não fazer
# BICAS :: Bloqueador neuromuscular em uso; Isquemia miocárdica nas últimas 24 h; Convulsão ou abstinência alcoólica em tratamento; Agitação em escalada de dose; Subida da pressão intracraniana
> Critérios de segurança do ensaio ABC (Girard, 2008), que juntou o despertar diário ao teste de respiração espontânea e reduziu dias de ventilação e mortalidade em 1 ano.
^o
@ Laringoscopia: graus de Cormack-Lehane
# I a IV :: I = toda a glote visível; II = só a parte posterior da glote; III = só a epiglote; IV = nem a epiglote
> Classificação de 1984 da visão à laringoscopia direta. Os graus III e IV definem laringoscopia difícil e pedem bougie ou videolaringoscópio.
^c
@ Confirmar a intubação: o que vale
# "Capnografia manda" :: Capnografia em onda = o padrão: sem curva, o tubo está no esôfago até prova em contrário; Visão direta = tubo passando entre as cordas vocais; Ausculta e condensação = falham com frequência; Ultrassom = opção quando não há capnógrafo; Radiografia = mostra a profundidade, não o lugar
! Na PCR, a curva fica baixa, mas existe se o tubo está na traqueia e há compressões.
> A intubação esofágica não reconhecida é evento evitável e fatal. As diretrizes exigem capnografia em forma de onda em toda intubação.
^c
## 06 🫀 Cardiointensivismo e PCR
@ Infarto com supra de ST: metas de tempo
# 10 · 30 · 90 · 120 :: 10 min = eletrocardiograma depois do primeiro contato; 30 min = porta-agulha, se a escolha for trombólise; 90 min = porta-balão em hospital com hemodinâmica; 120 min = limite para angioplastia por transferência: acima disso, trombolisar; 2 a 24 h = coronariografia depois de trombólise eficaz
> Tempo é músculo. A estratégia fármaco-invasiva é a regra onde não há hemodinâmica próxima.
^c
@ Trombólise: contraindicações absolutas
# DANTAS :: Dissecção de aorta suspeita; AVC hemorrágico em qualquer época; Neoplasia ou malformação vascular intracraniana; Trauma craniano ou facial importante em 3 meses; AVC isquêmico em 3 meses; Sangramento ativo (exceto menstruação)
> Lista das diretrizes para o infarto com supra. Na contraindicação absoluta, a reperfusão é por angioplastia.
^o
@ Bloqueios atrioventriculares
# "PR longo, PR cresce, PR fixo, dissociação" :: 1º grau = PR acima de 200 ms e toda onda P conduz; 2º grau Mobitz I = PR aumenta até uma P bloquear (nodal, em geral benigno); 2º grau Mobitz II = PR fixo e bloqueio súbito (infranodal: marca-passo); 3º grau = ondas P e QRS sem relação
> O nível do bloqueio define o risco. Os infranodais (Mobitz II e bloqueio total com QRS largo) progridem para assistolia e respondem mal à atropina.
^c
@ Taquicardia de QRS largo: a favor de ventricular
# "Na dúvida, é ventricular" :: Dissociação atrioventricular = batimentos de captura e de fusão; Concordância = QRS todo positivo ou todo negativo nas precordiais; Complexo RS = ausente nas precordiais ou com mais de 100 ms; Derivação aVR = onda R inicial dominante; História = infarto prévio ou cardiopatia estrutural
> Critérios de Brugada (1991) e de Vereckei. Cerca de 80% das taquicardias de QRS largo são ventriculares; tratar como tal é mais seguro.
^c
@ Torsades de pointes: conduta
# MAPA :: Magnésio 2 g na veia; Acelerar o coração: marca-passo ou isoproterenol; Potássio mantido entre 4,5 e 5; Afastar os fármacos que alongam o QT
! Com instabilidade, desfibrilar.
> Taquicardia ventricular polimórfica do QT longo, que depende de pausas. Amiodarona e outros antiarrítmicos que alongam o QT pioram o quadro.
^o
@ Insuficiência cardíaca aguda: causas a tratar de imediato
# CHAMPIT :: Coronariana aguda: síndrome; Hipertensiva: emergência; Arritmia; Mecânica: ruptura ou insuficiência valvar aguda; Pulmonar: embolia; Infecção; Tamponamento
> Mnemônico da diretriz europeia de insuficiência cardíaca (2021) para as causas que exigem tratamento específico já na primeira hora.
^c
@ ECMO venoarterial: complicações
# MALHAS :: Membro isquêmico pela cânula arterial femoral; Arlequim: hipoxemia na metade superior do corpo; Left: ventrículo esquerdo distendido pela pós-carga; Hemorragia e hemólise; AVC e outros eventos tromboembólicos; Sepse relacionada às cânulas
> Problemas próprios da canulação periférica. O cateter de perfusão distal e a descompressão do ventrículo esquerdo previnem dois deles.
^o
## 07 🫘 Rim, ácido-base e eletrólitos
@ Hipernatremia: déficit de água e ritmo
# 0,6 · 140 · 10 :: Déficit de água = 0,6 × peso × (sódio ÷ 140 − 1), com 0,5 na mulher e no idoso; Ritmo na crônica = até 10 a 12 mEq/L em 24 h; Aguda, com menos de 48 h = pode corrigir rápido; Somar = as perdas que continuam
> Estimativa do volume de água livre a repor. Corrigir rápido demais a hipernatremia crônica causa edema cerebral.
^c
@ Hipocalemia: reposição intravenosa
# 10 · 20 · 40 :: 10 mEq/h = máximo em veia periférica; 20 mEq/h = em veia central, com monitor; 40 mEq/h = só em emergência, com monitor; 20 mEq = sobem o potássio em cerca de 0,25 mEq/L
! Corrigir o magnésio junto: sem ele, o potássio não sobe.
> Regras de segurança para repor potássio. Nunca em bolus; evitar solução com glicose, que desloca o potássio para dentro da célula.
^c
@ Hipofosfatemia grave: consequências
# FRACO :: Fraqueza respiratória e falha de desmame; Rabdomiólise; Arritmia e disfunção miocárdica; Confusão e convulsão; Oxigênio mal liberado aos tecidos e hemólise
> Fósforo abaixo de 1 mg/dL esgota o ATP. Aparece na realimentação, na cetoacidose tratada, na alcalose respiratória e na terapia renal contínua.
^o
@ Rabdomiólise: conduta
# 5.000 · 300 :: CK acima de 5.000 = risco de lesão renal aguda; Diurese-alvo = 200 a 300 mL/h com cristaloide; Bicarbonato e manitol = sem benefício comprovado; Cálcio = repor só se houver sintoma ou hipercalemia grave; Diálise = pelas indicações habituais
> A mioglobina lesa o túbulo renal. Volume cedo e generoso é a única medida de eficácia aceita.
^c
@ Bicarbonato na acidose metabólica: quando considerar
# 7,20 + rim :: pH de 7,20 ou menos com lesão renal aguda = benefício no ensaio BICAR-ICU (2018); Hipercalemia grave e intoxicação por tricíclico ou salicilato = indicações à parte; Perda de bicarbonato (diarreia, acidose tubular) = repor; Acidose lática e cetoacidose = tratar a causa
> No BICAR-ICU, o bicarbonato não reduziu a mortalidade no conjunto, mas reduziu diálise e mortes no subgrupo com lesão renal aguda.
^c
@ Hipocalcemia: sinais
# CATS :: Convulsão; Arritmia e QT longo; Tetania (sinais de Chvostek e de Trousseau); Sibilo, estridor e laringoespasmo
! Completa-se com "go numb": dormência perioral e nas extremidades.
> Mnemônico clássico em inglês ("CATS go numb"). Na UTI, medir sempre o cálcio iônico; atenção depois de transfusão maciça e de paratireoidectomia.
^c
@ Síndrome cardiorrenal: cinco tipos
# Tipos 1 a 5 :: 1 = insuficiência cardíaca aguda leva a lesão renal aguda; 2 = insuficiência cardíaca crônica leva a doença renal crônica; 3 = lesão renal aguda leva a disfunção cardíaca aguda; 4 = doença renal crônica leva a cardiopatia; 5 = doença sistêmica, como a sepse, atinge os dois
> Classificação de Ronco (2008). No tipo 1, a congestão venosa pesa mais que o baixo débito na piora renal.
^c
## 08 🫃 Gastro, fígado e nutrição
@ Pancreatite aguda: falência orgânica pelo escore de Marshall
# 3 sistemas :: Respiratório = relação PaO₂/FiO₂; Renal = creatinina; Cardiovascular = pressão sistólica e resposta a volume; Falência = 2 pontos ou mais em qualquer sistema
> Escore de Marshall modificado, adotado pela classificação de Atlanta revisada para definir falência orgânica.
^c
@ Pancreatite aguda: conduta inicial
# RADAR :: Ringer lactato em ritmo moderado; Analgesia; Dieta oral precoce, conforme a tolerância; Antibiótico só com infecção comprovada; Retirar a causa: colangiografia endoscópica na colangite e colecistectomia na mesma internação
> O ensaio WATERFALL (2022) mostrou que a hidratação agressiva causa mais sobrecarga de volume, sem benefício.
^o
@ Insuficiência hepática aguda: conduta
# SALVA :: Sódio entre 145 e 150 para prevenir edema cerebral; Acetilcisteína, mesmo sem paracetamol; Listar cedo: contato com o centro de transplante; Vigiar glicemia, infecção e sangramento; Amônia acima de 150: risco de herniação, considerar terapia renal contínua
> Sem transplante, a mortalidade é alta. O edema cerebral é a principal causa de morte nas formas hiperagudas.
^o
@ Falência hepática crônica agudizada: seis órgãos
# "Seis órgãos do CLIF" :: Fígado = bilirrubina de 12 mg/dL ou mais; Rim = creatinina de 2 mg/dL ou mais, ou diálise; Cérebro = encefalopatia grau III ou IV; Coagulação = INR de 2,5 ou mais; Circulação = uso de vasopressor; Respiração = PaO₂/FiO₂ de 200 ou menos
> Definições do consórcio europeu (estudo CANONIC, 2013). O número de órgãos em falência gradua a síndrome e estima a mortalidade em 28 dias.
^c
@ Pseudo-obstrução aguda do cólon (Ogilvie)
# 12 cm · 2 mg :: 12 cm = diâmetro do ceco a partir do qual cresce o risco de perfuração; 2 mg = neostigmina intravenosa em 3 a 5 min, com monitor e atropina à mão; Antes = corrigir eletrólitos e suspender opioide e anticolinérgico; Falha = descompressão por colonoscopia
> Dilatação do cólon sem obstrução mecânica, no paciente grave ou operado. A neostigmina resolveu a maioria dos casos no ensaio de Ponec (1999).
^c
@ Síndrome compartimental abdominal: conduta
# SONDA :: Sondas gástrica e retal para esvaziar o tubo digestivo; Ocupantes de espaço drenados (ascite, hematoma); Neuromuscular: bloqueio e sedação para relaxar a parede; Diurético ou diálise para balanço negativo; Abrir o abdome se for refratária
> Degraus clínicos da sociedade do compartimento abdominal antes da laparotomia descompressiva, indicada quando a disfunção orgânica progride.
^o
@ Intolerância à dieta enteral: conduta
# PASSO :: Procinético: eritromicina ou metoclopramida; Abaixar a velocidade, sem suspender; Sonda pós-pilórica; Suspender opioide e sedativo em excesso; Olhar eletrólitos e glicemia
> Vômito, distensão e resíduo gástrico alto. A meta é manter a via enteral funcionando, e não trocá-la cedo pela parenteral.
^o
"""
