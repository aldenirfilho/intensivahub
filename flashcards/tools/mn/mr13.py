TXT = r"""
## 07 🦠 Infectologia
@ Leptospirose: tratamento
# Leve × grave :: Leve = doxiciclina 100 mg de 12/12 h ou amoxicilina, por 5 a 7 dias; Grave = penicilina cristalina ou ceftriaxona, por 7 dias; Pistas = mialgia na panturrilha, sufusão conjuntival, exposição a enchente; Notificação = compulsória
> Esquema do Ministério da Saúde. Iniciar o antibiótico na suspeita, sem esperar a sorologia.
^c
@ Leishmaniose visceral (calazar)
# FEP :: Febre prolongada; Esplenomegalia volumosa (com hepatomegalia); Pancitopenia com hipergamaglobulinemia
> Tríade da leishmaniose visceral, endêmica no Nordeste. Anfotericina B lipossomal nos graves, com HIV e nos idosos; antimonial nos demais.
^o
@ Esquistossomose mansônica crônica
# Portal pré-sinusoidal :: Hepatoesplenomegalia = baço muito grande e fígado firme; Hipertensão portal = pré-sinusoidal, com varizes e hemorragia; Função hepática = preservada (pouca ascite e icterícia); Tratamento = praziquantel
> Fibrose periportal de Symmers no ultrassom. Sangramento por varizes com função hepática boa é a apresentação clássica.
^c
@ HIV: diagnóstico
# 2 testes rápidos :: Teste rápido = 2 testes de fabricantes diferentes, os dois reagentes confirmam; Discordantes = repetir e confirmar por outro método; Janela = cerca de 30 dias para os testes de 4ª geração; Infecção aguda = a carga viral detecta antes dos anticorpos
> Fluxogramas do Ministério da Saúde para o diagnóstico do HIV. Todo diagnóstico novo deve vir com carga viral e CD4.
^c
@ HIV: tratamento inicial
# TLD :: Tenofovir; Lamivudina; Dolutegravir
> Esquema preferencial do Ministério da Saúde para iniciar a terapia antirretroviral.
! Com rifampicina, dolutegravir 50 mg de 12/12 h. Separar dos antiácidos e do cálcio.
^c
@ HIV com tuberculose: quando iniciar a terapia antirretroviral
# 2 × 8 semanas :: CD4 abaixo de 50 = em até 2 semanas do início do tratamento da tuberculose; Demais = até 8 semanas; Meningite tuberculosa ou criptocócica = adiar de 4 a 8 semanas (risco de inflamação no SNC); Síndrome inflamatória de reconstituição = esperada, manter o tratamento
> Começar cedo reduz mortalidade, exceto nas infecções do sistema nervoso central.
^c
@ Pneumocistose
# DHL alto, CD4 baixo :: Clínica = dispneia progressiva, tosse seca, hipoxemia ao esforço, CD4 abaixo de 200; Exames = DHL alto, infiltrado intersticial bilateral, pneumotórax; Tratamento = sulfametoxazol-trimetoprima por 21 dias; Corticoide = se PaO₂ abaixo de 70 mmHg
> Pneumonia oportunista que define aids. Profilaxia com sulfametoxazol-trimetoprima se CD4 abaixo de 200.
^c
@ Profilaxia pós-exposição ao HIV
# 72 h · 28 dias :: Prazo = iniciar o quanto antes, até 72 horas; Duração = 28 dias; Esquema = tenofovir + lamivudina + dolutegravir; Seguimento = testes em 30 e 90 dias
> PEP para exposição sexual, violência sexual e acidente com material biológico. Avaliar também hepatites, sífilis e contracepção de emergência.
^c
@ Neurossífilis
# Líquor e penicilina IV :: Quando puncionar = sintomas neurológicos, oculares ou auditivos, ou falha de tratamento; Diagnóstico = VDRL no líquor (específico), proteína e células altas; Tratamento = penicilina cristalina de 18 a 24 milhões UI/dia por 14 dias; Seguimento = líquor a cada 6 meses até normalizar
> A penicilina benzatina não atinge nível suficiente no sistema nervoso. A neurossífilis pode ocorrer em qualquer fase.
^c
@ Corrimento uretral
# Ceftriaxona + azitromicina :: Tratamento = ceftriaxona 500 mg IM + azitromicina 1 g VO, dose única; Cobre = gonococo e clamídia ao mesmo tempo; Parcerias = tratar e orientar; Rastrear = HIV, sífilis e hepatites
> Abordagem sindrômica do Ministério da Saúde (PCDT de IST, 2022). Persistência após o tratamento: pensar em Mycoplasma genitalium ou tricomonas.
^c
@ Corrimento vaginal: as causas
# pH e cheiro :: Vaginose bacteriana = pH acima de 4,5, cheiro de peixe (teste das aminas), células-guia, metronidazol; Candidíase = pH normal, prurido, corrimento grumoso, fluconazol ou azólico tópico; Tricomoníase = corrimento bolhoso amarelo-esverdeado, colo em framboesa, metronidazol e tratar a parceria; Cervicite = muco no colo, cobrir gonococo e clamídia
> Diagnóstico diferencial das vulvovaginites. Vaginose e candidíase não são IST e não exigem tratar a parceria.
^c
@ Febre amarela: fases e sinais
# Faget e icterícia :: Fase de infecção = febre, cefaleia, mialgia, bradicardia relativa (sinal de Faget); Remissão = melhora por horas a dias; Fase tóxica = icterícia, hemorragias, lesão renal, transaminases muito altas; Prevenção = vacina conforme o calendário
> Arbovirose com letalidade alta na forma grave. Não há antiviral específico: suporte em UTI.
^c
@ Malária grave: reconhecer e tratar
# Artesunato IV :: Sinais de gravidade = rebaixamento, convulsão, hipoglicemia, acidose, anemia grave, lesão renal, icterícia, sangramento; Agente = quase sempre Plasmodium falciparum; Tratamento = artesunato IV, depois completar com esquema oral; Sem artesunato = artemeter IM
> Toda malária grave é emergência. Suspeitar em quem tem febre e esteve na Amazônia ou na África.
^c
@ Febre tifoide
# Febre em escada :: Clínica = febre progressiva em escada, bradicardia relativa, roséolas no abdome; Complicação = perfuração e sangramento intestinal na 3ª semana; Diagnóstico = hemocultura nas primeiras semanas; Tratamento = ceftriaxona ou azitromicina (ciprofloxacino se sensível)
> Salmonella Typhi transmitida por água e alimentos. O portador crônico na vesícula biliar mantém a transmissão.
^c
@ Endocardite: tratamento empírico
# Nativa × prótese :: Valva nativa comunitária = ampicilina + oxacilina (com ou sem gentamicina), ou vancomicina se risco de MRSA; Prótese precoce ou infecção hospitalar = vancomicina + gentamicina, depois rifampicina; Antes = 3 pares de hemoculturas; Ajustar = sempre pela cultura
> Esquemas iniciais segundo a diretriz europeia de endocardite. Duração de 4 a 6 semanas.
^c
@ Osteomielite
# Estilete, imagem, osso :: Pista = úlcera em que o estilete toca o osso; Imagem = ressonância (a radiografia demora 2 semanas para alterar); Diagnóstico definitivo = biópsia óssea com cultura; Tratamento = antibiótico guiado pela cultura por 6 semanas e desbridar osso necrótico
> Staphylococcus aureus é o agente mais comum; Salmonella na anemia falciforme; Pseudomonas após perfuração na planta do pé.
^c
@ Antibióticos: o efeito adverso de cada um
# Cada classe, um alerta :: Vancomicina = síndrome do homem vermelho e nefrotoxicidade; Linezolida = plaquetopenia e síndrome serotoninérgica; Aminoglicosídeo = nefro e ototoxicidade; Quinolona = tendinite, QT longo, aneurisma de aorta; Sulfametoxazol-trimetoprima = hipercalemia, aumento da creatinina, Stevens-Johnson; Clindamicina = Clostridioides difficile
> Toxicidades marcantes cobradas em prova. A síndrome do homem vermelho é reação à infusão rápida, não alergia.
^c
@ Meningite bacteriana: tratamento empírico do adulto
# Ceftriaxona + corticoide :: Base = ceftriaxona 2 g de 12/12 h; Acima de 50 anos ou imunossuprimido = acrescentar ampicilina (Listeria); Vancomicina = onde há pneumococo resistente; Dexametasona = 0,15 mg/kg de 6/6 h, antes ou junto da 1ª dose
> Não atrasar o antibiótico por causa de exames. A dexametasona reduz sequelas e morte na meningite pneumocócica.
^c
@ Meningite: tomografia antes da punção lombar
# PICADA :: Papiledema; Imunossupressão (HIV, transplante); Convulsão recente (na última semana); Alteração do nível de consciência; Déficit neurológico focal; Antecedente de doença do SNC (tumor, AVC, abscesso)
> Indicações de tomografia antes da punção (IDSA). Havendo indicação, colher hemocultura e dar o antibiótico antes da imagem.
^o
@ Estrongiloidíase: síndrome de hiperinfecção
# Corticoide acorda o verme :: Gatilho = corticoide, transplante ou HTLV-1; Quadro = pneumonia, íleo, sepse e meningite por Gram-negativos; Tratamento = ivermectina; Prevenção = ivermectina empírica antes de imunossuprimir quem veio de área endêmica
> O Strongyloides se autoinfecta e, com imunossupressão, se dissemina levando bactérias do intestino. Mortalidade alta.
^c

## 08 🦴 Reumatologia
@ Artrite reumatoide: critérios ACR/EULAR 2010
# 6 de 10 :: Articulações = de 0 a 5 pontos (mais articulações e menores pontuam mais); Sorologia = fator reumatoide ou anti-CCP, de 0 a 3; Provas inflamatórias = VHS ou PCR alta, 1; Duração = 6 semanas ou mais, 1
> Classificação para artrite inflamatória sem outra explicação. Seis pontos ou mais classificam como artrite reumatoide.
^c
@ Artrite reumatoide: mau prognóstico
# PIOR :: Positividade alta de fator reumatoide e anti-CCP; Inflamação alta com muitas articulações ativas; Osso: erosões precoces; Repercussão fora da articulação (nódulos, vasculite, pulmão)
> Fatores que indicam tratamento mais agressivo desde o início.
^o
@ Artrite reumatoide: estratégia de tratamento
# Metotrexato e alvo :: Âncora = metotrexato desde o diagnóstico; Alvo = remissão ou baixa atividade (tratar até o alvo); Ponte = corticoide em dose baixa pelo menor tempo; Sem meta em 3 a 6 meses = associar biológico (anti-TNF e outros) ou inibidor de JAK
> Recomendações EULAR e SBR. Tratar nos primeiros meses (janela de oportunidade) reduz o dano articular.
^c
@ Antes do biológico: o que rastrear
# THIV :: Tuberculose latente (prova tuberculínica ou IGRA e radiografia); Hepatites B e C; Imunizações em dia (vacinas vivas antes de iniciar); Vírus HIV
> Rastreio antes de anti-TNF e outros imunobiológicos. Tuberculose latente: tratar e iniciar o biológico após 1 mês.
^o
@ Lúpus: o que acompanha a atividade
# DNA sobe, complemento cai :: Anti-DNA = sobe na atividade, sobretudo na nefrite; C3 e C4 = caem na atividade; Anti-Sm e FAN = não acompanham a atividade (servem ao diagnóstico); PCR = costuma ser normal, e alta sugere infecção ou serosite
> Marcadores de atividade do lúpus. Febre com PCR alta no lúpus: procurar infecção antes de aumentar a imunossupressão.
^c
@ Nefrite lúpica: tratamento
# Indução e manutenção :: Indução = micofenolato ou ciclofosfamida + corticoide; Acréscimo = belimumabe ou inibidor de calcineurina em casos selecionados; Manutenção = micofenolato ou azatioprina; Todos = hidroxicloroquina e IECA ou BRA
> Classes III, IV e V recebem imunossupressão (KDIGO 2024 e EULAR). A biópsia renal guia o tratamento.
^c
@ Esclerose sistêmica: crise renal
# IECA salva :: Quadro = hipertensão maligna súbita com lesão renal aguda; Risco = forma difusa, anti-RNA polimerase III, corticoide em dose alta; Tratamento = IECA (captopril) mesmo com a creatinina subindo; Evitar = prednisona acima de 15 mg/dia
> Emergência da esclerodermia. Antes do IECA era quase sempre fatal.
^c
@ Esclerose sistêmica: difusa × limitada
# Scl-70 × centrômero :: Difusa = pele acima de cotovelos e joelhos e no tronco, anti-Scl-70; Difusa, órgãos = doença pulmonar intersticial e crise renal; Limitada = mãos, antebraços e face, anticentrômero (CREST); Limitada, órgão = hipertensão arterial pulmonar tardia
> Duas formas com anticorpos e complicações diferentes.
^c
@ Vasculites ANCA: as três
# PR3 × MPO :: Granulomatose com poliangiite = c-ANCA (PR3), granulomas, sinusite, nariz em sela, pulmão e rim; Poliangiite microscópica = p-ANCA (MPO), sem granuloma, pulmão e rim; Granulomatose eosinofílica = asma e eosinofilia, p-ANCA em 40%, neuropatia; Tratamento = corticoide + rituximabe ou ciclofosfamida
> Vasculites de pequenos vasos associadas ao ANCA, causa importante de síndrome pulmão-rim.
^c
@ Poliarterite nodosa
# MANHÃ :: Mononeurite múltipla; ANCA negativo; Nefro: infarto renal e hipertensão, sem glomerulonefrite; Hepatite B associada; Aneurismas em vasos médios (mesentéricos e renais)
> Vasculite necrosante de vasos médios que poupa o pulmão. Orquite e livedo também são pistas.
^o
@ Arterite de Takayasu
# 40 · 10 :: Idade = início antes dos 40 anos, sobretudo em mulheres; Pressão = diferença acima de 10 mmHg entre os braços; Pulsos = diminuídos ou ausentes, claudicação dos membros superiores; Imagem = estenoses da aorta e ramos na angiotomografia ou angiorressonância
> Vasculite de grandes vasos da mulher jovem, a "doença sem pulso".
^c
@ Vasculite por IgA (Henoch-Schönlein)
# PARA :: Púrpura palpável nas pernas e nádegas, com plaquetas normais; Artrite ou artralgia; Rim: nefrite por IgA; Abdome: dor, sangramento e invaginação
> Vasculite mais comum da infância; no adulto a nefrite tende a ser mais grave.
^o
@ Crioglobulinemia mista
# Hepatite C e C4 baixo :: Causa = hepatite C na maioria; Tríade de Meltzer = púrpura, artralgia e fraqueza; Rim = glomerulonefrite membranoproliferativa; Laboratório = C4 muito baixo e fator reumatoide positivo
> Vasculite por imunocomplexos. Tratar a hepatite C e, nos casos graves, usar rituximabe.
^c
@ Fibromialgia
# Dor difusa e sono :: Clínica = dor difusa por 3 meses ou mais, fadiga, sono não reparador, queixas cognitivas; Exames = normais (excluir hipotireoidismo e polimialgia); Primeira linha = exercício aeróbico e educação; Fármacos = amitriptilina, duloxetina ou pregabalina
> Critérios do ACR de 2016, sem contagem de pontos dolorosos. Opioides devem ser evitados.
^c
@ Osteoartrite: tratamento
# Exercício primeiro :: Base = exercício, fortalecimento e perda de peso; Tópico = anti-inflamatório tópico no joelho e na mão; Oral = anti-inflamatório pelo menor tempo (o paracetamol tem pouco efeito); Infiltração e cirurgia = corticoide intra-articular nas crises e prótese se dor refratária
> Recomendações do ACR e da OARSI. Glucosamina e condroitina sem benefício consistente.
^c
@ Gota: o que precipita a crise
# CARNE :: Cerveja e destilados; AAS em dose baixa, ciclosporina e pirazinamida; Refrigerante e frutose; Nutrição rica em carne vermelha, vísceras e frutos do mar; Elevação por diurético tiazídico ou de alça
> Fatores que elevam o ácido úrico ou mudam bruscamente o seu nível. Começar alopurinol também pode precipitar crise: associar colchicina.
^o
@ Pseudogota: doenças associadas
# HHHH :: Hemocromatose; Hiperparatireoidismo; Hipomagnesemia; Hipofosfatasia
> Deposição de pirofosfato de cálcio, típica do idoso ou associada a doenças metabólicas. Condrocalcinose no joelho e no punho na radiografia.
! Pseudogota antes dos 60 anos: investigar estas causas.
^c
@ Espondilite anquilosante: tratamento
# Anti-inflamatório primeiro :: Primeira linha = anti-inflamatório em dose plena e exercício; Falha de 2 anti-inflamatórios = anti-TNF ou anti-IL-17; Metotrexato e sulfassalazina = só para artrite periférica, não para a coluna; Corticoide sistêmico = não usar
> Recomendações ASAS-EULAR. Uveíte anterior recorrente favorece o anticorpo monoclonal anti-TNF.
^c
@ Síndrome antissintetase
# MARFIM :: Mãos de mecânico; Artrite; Raynaud; Febre; Intersticial: doença pulmonar; Miosite
> Miopatia inflamatória com anti-Jo-1 ou outros anticorpos antissintetase. A doença pulmonar intersticial define o prognóstico.
^o
@ Doença de Still do adulto
# FERA :: Febre diária em picos de 39 °C ou mais; Exantema cor de salmão que some com a febre; Reumatismo: artrite ou artralgia; Alta ferritina com leucocitose neutrofílica
> Diagnóstico de exclusão (critérios de Yamaguchi). Ferritina muito alta e risco de síndrome de ativação macrofágica.
^o

## 09 🧠 Neurologia
@ AVC isquêmico: classificação TOAST
# 5 tipos :: Grandes artérias = aterosclerose com estenose acima de 50%; Cardioembólico = fibrilação atrial, trombo, endocardite; Pequenos vasos = infarto lacunar menor que 1,5 cm; Outra causa definida = dissecção, vasculite, trombofilia; Indeterminado = sem causa ou mais de uma
> Classificação etiológica que orienta a prevenção secundária.
^c
@ Síndromes lacunares
# 5 clássicas :: Motora pura = cápsula interna ou ponte; Sensitiva pura = tálamo; Sensitivo-motora = cápsula e tálamo; Ataxia-hemiparesia = ponte ou cápsula; Disartria-mão desajeitada = ponte
> Infartos pequenos por doença de pequenos vasos (hipertensão, diabetes). Não há afasia, negligência nem alteração do campo visual.
^c
@ Síndrome bulbar lateral (Wallenberg)
# CHAVE :: Cruzada: dor e temperatura alteradas na face do lado da lesão e no corpo do lado oposto; Horner do mesmo lado; Ataxia do mesmo lado; Vertigem, náusea e nistagmo; Engasgo: disfagia e rouquidão (núcleo ambíguo)
> Infarto do bulbo lateral por oclusão da artéria vertebral ou da cerebelar posteroinferior. Em jovem, pensar em dissecção vertebral.
^o
@ Fibrilação atrial depois do AVC: quando anticoagular
# 1-3-6-12 :: AIT = 1 dia; AVC leve = 3 dias; AVC moderado = 6 dias (após imagem sem transformação hemorrágica); AVC grave = 12 dias
> Regra de consenso europeu. O ensaio ELAN (2023) mostrou que iniciar o anticoagulante direto mais cedo é seguro.
^c
@ Hemorragia intraparenquimatosa: a causa pela localização
# Profunda × lobar :: Profunda (núcleos da base, tálamo, ponte, cerebelo) = hipertensão; Lobar no idoso = angiopatia amiloide; Jovem = malformação arteriovenosa, cocaína, anfetamina; Anticoagulado = reverter imediatamente
> A localização sugere a causa. Angiotomografia na hemorragia lobar ou no jovem.
^c
@ Enxaqueca: profilaxia
# 4 crises por mês :: Quando = 4 ou mais dias de crise por mês, ou crises incapacitantes; Opções = propranolol, topiramato, amitriptilina, flunarizina, valproato, candesartana; Novos = anticorpos anti-CGRP e toxina botulínica (forma crônica); Duração = 6 a 12 meses e reavaliar
> A profilaxia é escolhida pelas comorbidades: propranolol na ansiedade e hipertensão, amitriptilina na insônia, topiramato na obesidade.
! Valproato e topiramato são teratogênicos.
^c
@ Enxaqueca: tratamento da crise
# Cedo e sem opioide :: Leve a moderada = anti-inflamatório ou dipirona logo no início; Moderada a grave = triptano; Náusea = metoclopramida ou domperidona; Evitar = opioides e analgésico em 10 a 15 dias ou mais por mês
> O uso excessivo de analgésico transforma a enxaqueca em crônica. Triptano é contraindicado na doença coronária.
^c
@ Hipertensão intracraniana idiopática
# MOPA :: Mulher jovem; Obesidade; Papiledema com pressão de abertura acima de 25 cmH₂O e líquor normal; Acetazolamida e perda de peso no tratamento
> Pseudotumor cerebral. Pode haver paralisia do VI par; o risco é a perda visual permanente.
! Fármacos associados: tetraciclinas, vitamina A e retinoides.
^o
@ Parkinson: tratamento
# Levodopa é a mais eficaz :: Levodopa = a mais eficaz, primeira escolha no idoso; Agonista dopaminérgico = pramipexol, alternativa no jovem (risco de compulsões); IMAO-B = rasagilina ou selegilina, efeito leve; Amantadina = discinesias causadas pela levodopa
> Tratamento sintomático da doença de Parkinson. Discinesias e flutuações motoras aparecem com o tempo de doença.
^c
@ Parkinsonismo atípico: sinais de alarme
# QUEDA :: Quedas precoces (paralisia supranuclear progressiva); Unilateralidade ausente: quadro simétrico desde o início; Exuberante disautonomia precoce (atrofia de múltiplos sistemas); Demência e alucinações precoces (corpos de Lewy); Ausência de resposta à levodopa
> Pistas de que não é doença de Parkinson idiopática. A paralisia do olhar vertical é típica da paralisia supranuclear progressiva.
^o
@ Esclerose múltipla: sinais característicos
# Sinais com nome :: Neurite óptica = dor ao mover o olho e perda visual; Lhermitte = choque ao longo da coluna ao fletir o pescoço; Uhthoff = piora com o calor; Oftalmoplegia internuclear = lesão do fascículo longitudinal medial
> Achados que sugerem doença desmielinizante no adulto jovem. Ressonância com lesões periventriculares e justacorticais.
^c
@ Neuromielite óptica
# Aquaporina 4 :: Anticorpo = anti-aquaporina 4; Medula = mielite longitudinalmente extensa (3 segmentos ou mais); Olho = neurite óptica grave, às vezes bilateral; Área postrema = soluços e vômitos incoercíveis
> Doença distinta da esclerose múltipla. Alguns fármacos da esclerose múltipla (interferona, natalizumabe) a pioram.
^c
@ Miastenia gravis: tratamento
# Sintoma, imunidade, timo :: Sintomático = piridostigmina; Imunossupressão = corticoide e azatioprina (ou outro poupador); Timectomia = timoma, ou anti-receptor de acetilcolina positivo até cerca de 65 anos; Crise = imunoglobulina IV ou plasmaférese
> Doença autoimune da junção neuromuscular. Fazer tomografia de tórax em todo diagnóstico, à procura de timoma.
^c
@ Esclerose lateral amiotrófica
# Superior e inferior juntos :: Neurônio motor = sinais de neurônio superior e inferior no mesmo segmento; Poupa = sensibilidade, esfíncteres e movimentos oculares; Eletroneuromiografia = denervação difusa; Tratamento = riluzol, ventilação não invasiva e gastrostomia no momento certo
> Doença neurodegenerativa progressiva. Fasciculações com reflexos vivos são a pista clínica.
^c
@ Síndrome do túnel do carpo: causas
# MAGRA + D :: Mixedema: hipotireoidismo; Acromegalia; Gestação; Reumatoide: artrite; Amiloidose e diálise; Diabetes
> Compressão do nervo mediano no punho: parestesia noturna do 1º ao 3º dedo, sinais de Phalen e Tinel.
^o
@ Lesões de nervos periféricos clássicas
# Pé caído × mão caída :: Fibular comum = pé caído, por cruzar as pernas ou fratura da cabeça da fíbula; Radial = mão caída, por fratura do úmero ou compressão (paralisia do sábado à noite); Ulnar = mão em garra, lesão no cotovelo; Mediano = mão de bênção na lesão alta
> Lesões compressivas e traumáticas mais cobradas. Diferenciar o pé caído fibular da radiculopatia L5, que também perde a inversão do pé.
^c
@ Pupilas no paciente em coma
# A pupila localiza :: Puntiformes = ponte ou opioide; Médias e fixas = mesencéfalo; Dilatada de um lado = III par, herniação uncal; Pequenas e reativas = causa metabólica ou diencéfalo
> Pupilas reativas sugerem coma metabólico; assimetria nova é sinal de herniação.
^c
@ Paralisia do III par: compressiva × isquêmica
# A pupila decide :: Compressiva = pupila dilatada, com dor, aneurisma de comunicante posterior; Isquêmica = pupila poupada, diabetes e hipertensão; Compressiva, conduta = angiotomografia urgente; Isquêmica, evolução = recupera em semanas a meses
> As fibras pupilares ficam na periferia do nervo e sofrem primeiro com a compressão.
^c
@ Vertigem posicional paroxística benigna
# Dix-Hallpike e Epley :: Clínica = vertigem de segundos ao mudar a posição da cabeça; Diagnóstico = manobra de Dix-Hallpike, nistagmo após latência que se esgota; Tratamento = manobra de Epley (canal posterior); Remédio = antivertiginoso só por pouco tempo
> Causa mais comum de vertigem. Quadro típico dispensa exame de imagem.
^c
@ Epilepsia e gestação
# Fugir do valproato :: Evitar = valproato (malformações e prejuízo cognitivo); Preferir = lamotrigina ou levetiracetam; Ácido fólico = antes e durante a gestação; Lamotrigina = o nível cai na gestação, ajustar a dose
> Planejar a gestação na mulher com epilepsia. Não suspender o anticonvulsivante por conta própria.
^c
"""
