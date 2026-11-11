TXT = r"""
## 09 🧠 Neurologia
@ Cefaleia: sinais de alarme
# SNOOP :: Sistêmicos: febre, perda de peso, câncer, HIV; Neurológicos: déficit focal, confusão; Onset súbito (em trovoada); Older: início depois dos 50 anos; Padrão que mudou ou progride
^c
@ Enxaqueca: critérios POUND
# POUND :: Pulsátil; One day: dura de 4 a 72 h; Unilateral; Náusea ou vômito; Disabling: incapacitante
! 4 de 5 = enxaqueca muito provável.
^c
@ Cefaleia em salvas
# "Olho, relógio, oxigênio" :: Dor = unilateral, orbitária, excruciante, de 15 a 180 min; Autonômicos = lacrimejamento, hiperemia, rinorreia e ptose do mesmo lado; Padrão = mesma hora do dia, em surtos; Crise = oxigênio a 100% e sumatriptano subcutâneo; Profilaxia = verapamil
^c
@ Parkinson: sinais cardinais
# TRAP :: Tremor de repouso; Rigidez em roda denteada; Acinesia e bradicinesia; Postura instável
^c
@ Demências: a pista de cada uma
# "Memória, alucinação, comportamento, degraus" :: Alzheimer = memória recente primeiro; Corpos de Lewy = alucinações visuais, flutuação e parkinsonismo; Frontotemporal = comportamento e linguagem, mais jovem; Vascular = evolução em degraus com fatores de risco
^c
@ Demências potencialmente reversíveis
# DEMENTIA :: Drogas; Emocional: depressão; Metabólica: B12 e tireoide; Enxergar e escutar: déficits sensoriais; Normobárica: hidrocefalia de pressão normal; Tumor e hematoma subdural; Infecção: sífilis e HIV; Álcool
^c
@ Hidrocefalia de pressão normal: tríade
# "Marcha, urina, memória" :: Marcha = apráxica, magnética (a primeira a aparecer); Urina = incontinência; Memória = demência
^c
@ Esclerose múltipla: diagnóstico
# "Tempo e espaço" :: Disseminação no espaço = lesões em 2 ou mais regiões típicas (periventricular, justacortical, infratentorial, medula); Disseminação no tempo = novo surto, lesões de idades diferentes ou bandas oligoclonais; Clínica típica = neurite óptica, mielite parcial, oftalmoplegia internuclear
^c
@ Miastenia gravis × Lambert-Eaton
# "Piora × melhora com o uso" :: Miastenia = fatigabilidade, ptose e diplopia, anticorpo antirreceptor de acetilcolina, timoma; Lambert-Eaton = força melhora com a repetição, arreflexia, disautonomia, câncer de pulmão de pequenas células
^c
@ Neurônio motor superior × inferior
# "Hiper × hipo" :: Superior = espasticidade, hiper-reflexia, Babinski, pouca atrofia; Inferior = flacidez, arreflexia, atrofia e fasciculações; Os dois juntos = esclerose lateral amiotrófica
^c
@ AVC: território pela clínica
# "Perna, braço e face, visão" :: Cerebral anterior = perna mais fraca que o braço; Cerebral média = face e braço, afasia (esquerda) ou negligência (direita); Cerebral posterior = hemianopsia homônima; Vertebrobasilar = síndromes cruzadas, vertigem, diplopia
^c
@ Ataque isquêmico transitório: escore ABCD²
# ABCD² :: A = idade de 60 anos ou mais (1); B = pressão de 140/90 ou mais (1); C = clínica: fraqueza unilateral (2) ou só fala (1); D = duração: 60 min ou mais (2), de 10 a 59 min (1); D² = diabetes (1)
! 4 ou mais: dupla antiagregação por 21 dias.
^c
@ Vertigem aguda: HINTS
# HINTS :: HI = impulso da cabeça: normal no central; N = nistagmo: vertical ou que muda de direção no central; TS = teste de skew: desvio vertical no central
! Um achado central basta para pedir ressonância.
^c
@ Primeira crise epiléptica: quando tratar
# "2 crises, ou 1 com risco" :: Duas crises = não provocadas, com mais de 24 h de intervalo; Uma crise com risco alto = lesão na imagem, EEG epileptiforme ou crise no sono; Crise provocada = tratar a causa, sem fármaco de manutenção
^c
@ Antiepilépticos: efeito marcante de cada um
# "Cada um com seu efeito" :: Valproato = teratogênico, ganho de peso, tremor, fígado; Carbamazepina = hiponatremia, rash, indução enzimática; Fenitoína = hiperplasia gengival, hirsutismo, ataxia; Lamotrigina = rash grave se a dose subir rápido; Topiramato = cálculo renal, perda de peso, lentificação
^c
@ Neuropatia periférica: causas
# DAVITU :: Diabetes; Álcool; Vitamina B12 baixa; Infecciosas: hanseníase e HIV; Tóxicas e fármacos (quimioterapia, isoniazida); Uremia
! No Brasil, sempre lembrar de hanseníase.
^o
@ Os doze pares cranianos
# "Oh Oh Oh To Touch And Feel Very Good Velvet Ah Heaven" :: Oh = Olfatório; Oh (2) = Óptico; Oh (3) = Oculomotor; To = Troclear; Touch = Trigêmeo; And = Abducente; Feel = Facial; Very = Vestibulococlear; Good = Glossofaríngeo; Velvet = Vago; Ah = Acessório; Heaven = Hipoglosso
^cf
@ Pares cranianos: sensitivo, motor ou misto
# "Some Say Marry Money But My Brother Says Big Brains Matter More" :: Some = Sensitivo (I); Say = Sensitivo (II); Marry = Motor (III); Money = Motor (IV); But = Both: misto (V); My = Motor (VI); Brother = Both: misto (VII); Says = Sensitivo (VIII); Big = Both: misto (IX); Brains = Both: misto (X); Matter = Motor (XI); More = Motor (XII)
^cf
@ Síndrome de Horner
# PMA :: Ptose; Miose; Anidrose
! Com dor cervical: dissecção de carótida. Com dor no ombro: tumor de Pancoast.
^c
@ Encefalopatia de Wernicke: tríade
# COA :: Confusão; Oftalmoplegia; Ataxia
! Tiamina antes da glicose.
^c
## 10 🎗️ Oncologia
@ Cinco emergências oncológicas
# "5 emergências" :: Compressão medular = dor nas costas + déficit: dexametasona e ressonância; Veia cava superior = edema de face e pescoço; Hipercalcemia = hidratação e bisfosfonato; Lise tumoral = hidratação e rasburicase; Neutropenia febril = antibiótico em 1 h
^c
@ Compressão medular neoplásica
# "Dor, depois déficit" :: Primeiro sintoma = dor nas costas que piora deitado; Depois = fraqueza, nível sensitivo, esfíncteres; Conduta = dexametasona imediata + ressonância de toda a coluna; Definitivo = cirurgia e/ou radioterapia
^c
@ Síndrome da veia cava superior: causas
# PLT :: Pulmão: câncer; Linfoma; Trombose por cateter
^o
@ Escala de desempenho ECOG
# 0 a 4 :: 0 = assintomático; 1 = sintomático, mas ambulatorial; 2 = acamado menos da metade do dia; 3 = acamado mais da metade do dia; 4 = restrito ao leito
^c
@ Rastreamento de câncer de colo e de mama
# "Colo 25–64, mama 50–69" :: Colo do útero = dos 25 aos 64 anos; Mama = mamografia a cada 2 anos dos 50 aos 69 (recomendação clássica do Ministério da Saúde); Atenção = em 2025 foi anunciada ampliação da faixa da mamografia — conferir a norma vigente
^c
@ Rastreamento de câncer de pulmão
# 50–80 · 20 · 15 :: 50–80 = idade em anos; 20 = maços-ano ou mais; 15 = parou há menos de 15 anos (ou ainda fuma)
! Tomografia de baixa dose anual.
^c
@ Rastreamento de câncer colorretal
# 45 · 10 · 1 :: 45 = idade de início no risco médio (50 em várias diretrizes); 10 = anos entre colonoscopias normais; 1 = ano entre testes de sangue oculto
^c
@ Marcadores tumorais
# "Marcador não rastreia" :: CEA = colorretal (seguimento); CA 19-9 = pâncreas e vias biliares; CA 125 = ovário; Alfafetoproteína = hepatocarcinoma e tumor germinativo não seminoma; β-hCG = tumor germinativo e coriocarcinoma; PSA = próstata
^c
@ Câncer de pulmão: síndromes paraneoplásicas
# "Pequenas células faz hormônio" :: Pequenas células = SIADH, Cushing por ACTH ectópico, Lambert-Eaton; Escamoso = hipercalcemia por PTHrP; Adenocarcinoma = osteoartropatia hipertrófica
^c
@ Câncer de pulmão: central × periférico
# "Central × periférico" :: Centrais = escamoso e pequenas células; Periféricos = adenocarcinoma (o mais comum, também em não fumantes) e grandes células
^c
@ Tumores que mais dão metástase óssea
# PB KTL :: Próstata; Breast: mama; Kidney: rim; Tireoide; Lung: pulmão
! Próstata dá lesões blásticas; rim e tireoide, líticas.
^c
@ Metástase cerebral: de onde vem
# "Pulmão na frente" :: Pulmão = o mais comum; Mama = o segundo; Melanoma = o que mais sangra; Rim e colorretal = os seguintes
^c
@ Quimioterápicos: toxicidade de cada um
# "Cada droga, um órgão" :: Doxorrubicina = coração; Bleomicina = pulmão (fibrose); Cisplatina = rim, ouvido e vômito; Vincristina = nervo periférico e íleo; Ciclofosfamida = bexiga (cistite hemorrágica: usar mesna); Metotrexato = mucosa, fígado e medula
^c
@ Imunoterapia: eventos adversos
# "Tudo que termina em ite" :: Pele = dermatite (o mais precoce); Intestino = colite; Fígado = hepatite; Pulmão = pneumonite; Endócrino = tireoidite, hipofisite, adrenalite; Conduta = suspender e corticoide a partir do grau 2
^c
@ Quimioterapia muito emetogênica: profilaxia
# ONDA :: Olanzapina; NK1: antagonista (aprepitanto); Dexametasona; Antagonista de serotonina (ondansetrona)
^o
@ Dor: escada analgésica da OMS
# 3 degraus :: 1 = dor leve: analgésico comum e anti-inflamatório; 2 = moderada: opioide fraco; 3 = intensa: opioide forte; Sempre = adjuvantes, pela boca e pelo relógio
^c
@ Câncer de mama: subtipos e tratamento
# "O receptor decide" :: Luminal (receptor hormonal positivo) = hormonioterapia; HER2 positivo = trastuzumabe; Triplo-negativo = quimioterapia, pior prognóstico
^c
@ Câncer colorretal hereditário
# "Lynch × polipose" :: Lynch = sem polipose, instabilidade de microssatélites, também endométrio e ovário; Polipose adenomatosa familiar = gene APC, centenas de pólipos, colectomia profilática
^c
@ Tumor de testículo: marcadores
# "Seminoma não faz alfa" :: Seminoma = alfafetoproteína sempre normal; Não seminoma = alfafetoproteína e β-hCG altas; LDH = volume tumoral
^c
@ Linfonodo suspeito
# DURO :: Duro e indolor; Um centímetro e meio ou mais, crescendo; Região supraclavicular; Organizado em bloco: aderido e fixo
! Supraclavicular esquerdo (Virchow) aponta para o abdome.
^o
"""
