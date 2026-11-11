TXT = r"""
## 15 🚑 Emergências clínicas
@ Abdome agudo: cinco tipos
# 5 tipos :: Inflamatório = apendicite, colecistite, diverticulite, pancreatite; Obstrutivo = brida, hérnia, tumor; Perfurativo = úlcera, divertículo; Vascular = isquemia mesentérica, aneurisma roto; Hemorrágico = prenhez ectópica rota, cisto roto
> Classificação sindrômica do abdome agudo, que orienta o exame de imagem e a urgência cirúrgica.
^c
@ Apendicite: escore de Alvarado
# MANTRELS :: Migração da dor; Anorexia; Náusea e vômito; Tenderness: dor em fossa ilíaca direita (2 pontos); Rebote: descompressão dolorosa; Elevação da temperatura; Leucocitose (2 pontos); Shift: desvio à esquerda
> Escore de Alvarado (1986). Pontuação baixa ajuda a excluir apendicite.
! 7 ou mais = apendicite provável.
^c
@ Síncope: três grupos de causa
# ROC :: Reflexa (vasovagal, situacional); Ortostática; Cardíaca (arritmia, estrutural)
> Classificação da diretriz europeia de síncope (2018).
! A cardíaca é a que mata: ECG em todos.
^c
@ Trombose venosa profunda: escore de Wells
# "2 ou mais = provável" :: 1 ponto cada = câncer ativo, imobilização, acamado ou cirurgia recente, dor no trajeto venoso, edema de todo o membro, panturrilha 3 cm maior, cacifo, colaterais superficiais, trombose prévia; −2 = diagnóstico alternativo tão provável quanto; Conduta = improvável pede D-dímero, provável pede ultrassom
> Escore de Wells para trombose venosa profunda, na versão de dois níveis (2003).
^c
@ Hemorragia digestiva alta: antes da endoscopia
# "Antes da endoscopia" :: Acessos = dois calibrosos, com volume; Hemoglobina = transfundir abaixo de 7 (8 no coronariopata); Inibidor de bomba = intravenoso; Endoscopia = em até 24 h; Varicosa suspeita = vasoativo e antibiótico já
> A estabilização vem antes da endoscopia. A estratégia restritiva de transfusão reduziu a mortalidade (Villanueva, 2013).
^c
@ Cefaleia em trovoada: causas
# "A pior da vida, em 1 minuto" :: Hemorragia subaracnóidea = a primeira a excluir; Vasoconstrição cerebral reversível = recorrente, com gatilhos; Dissecção cervical = dor no pescoço e Horner; Trombose venosa cerebral = puerpério e anticoncepcional; Apoplexia hipofisária = alteração visual
> Cefaleia que atinge a intensidade máxima em menos de 1 minuto. Tomografia e, se normal, punção lombar ou angiotomografia.
^c
@ Crise convulsiva × síncope
# "Língua, confusão, cor" :: Convulsão = mordedura lateral da língua, confusão prolongada depois, cianose; Síncope = palidez e sudorese antes, recuperação rápida, abalos breves podem ocorrer
> Abalos breves ocorrem na síncope convulsiva. O que mais diferencia é a recuperação.
^c
@ Hipoglicemia: regra 15-15
# 15-15 :: 15 = gramas de carboidrato rápido, se consciente; 15 (2) = minutos para repetir a glicemia; Inconsciente = glicose a 50% na veia ou glucagon intramuscular
> Regra prática da ADA para a hipoglicemia no paciente acordado.
^c
@ Pressão muito alta: emergência, urgência ou pseudocrise
# "A lesão aguda de órgão decide" :: Emergência = com lesão aguda de órgão-alvo: fármaco intravenoso em terapia intensiva; Urgência = sem lesão aguda: fármaco oral, reduzir em 24–48 h; Pseudocrise = pressão alta por dor ou ansiedade: tratar a causa
> A maioria dos pacientes com pressão muito alta no pronto-socorro não tem emergência hipertensiva.
^c
@ Hemoptise maciça: conduta
# "O lado que sangra para baixo" :: Posição = decúbito lateral sobre o lado que sangra; Via aérea = tubo calibroso, intubação seletiva se preciso; Localizar = tomografia e broncoscopia; Tratar = embolização de artéria brônquica
> O que mata é a asfixia, não a perda de sangue. Proteger o pulmão sadio é a prioridade.
^c
@ Cólica renal: quando internar ou desobstruir
# FIRA :: Febre ou infecção; Insuficiência renal ou rim único; Refratária: dor que não cede; Anúria ou obstrução bilateral
> A maioria das cólicas renais se trata em casa. Estes critérios indicam internação e avaliação urológica.
! Cálculo obstrutivo infectado = desobstrução urgente.
^o
@ Lombalgia: bandeiras vermelhas
# TUNA FISH :: Trauma; Unexplained: perda de peso sem explicação; Neurológico: déficit, anestesia em sela, esfíncteres; Anos: mais de 50; Febre; Intravenosas: uso de drogas; Steroid: uso de corticoide; História de câncer
> Sinais que sugerem fratura, tumor, infecção ou compressão neural e justificam imagem.
^c
@ Síndrome da cauda equina
# "Sela, bexiga, pernas" :: Sela = anestesia perineal; Bexiga = retenção urinária (o mais sensível) ou incontinência; Pernas = dor e fraqueza bilaterais; Conduta = ressonância e descompressão de urgência
> Compressão das raízes lombossacras, em geral por hérnia volumosa. O atraso deixa sequela esfincteriana.
^c
@ Olho vermelho: sinais de gravidade
# "Dor, visão, pupila" :: Dor = intensa (conjuntivite só arde); Visão = turva ou reduzida; Pupila = fixa em média midríase (glaucoma) ou irregular (uveíte); Hiperemia = ao redor da córnea; Conduta = oftalmologista no mesmo dia
> Sinais que separam a conjuntivite das causas que ameaçam a visão: glaucoma agudo, uveíte, ceratite e esclerite.
^c
@ Embolia pulmonar: estratificação de risco
# "Alto, intermediário, baixo" :: Alto = hipotensão ou choque: reperfusão; Intermediário-alto = ventrículo direito disfuncionante + troponina: anticoagular e vigiar; Intermediário-baixo = só um dos dois; Baixo = sPESI zero: considerar alta precoce
> Estratificação da diretriz europeia (2019), que define o tratamento e o local de internação.
^c
@ Embolia pulmonar: sPESI
# 80-110-100-90 :: 80 = idade acima de 80 anos; 110 = frequência cardíaca de 110 ou mais; 100 = sistólica abaixo de 100; 90 = saturação abaixo de 90%; + 2 = câncer e doença cardiopulmonar crônica
> Versão simplificada do Pulmonary Embolism Severity Index (Jiménez, 2010).
! Zero pontos = baixo risco.
^c
@ Tétano: profilaxia no ferimento
# "10 anos × 5 anos" :: Ferimento limpo = reforço se a última dose foi há mais de 10 anos; Ferimento de alto risco = reforço se foi há mais de 5 anos; Vacinação incerta ou menos de 3 doses = vacina, mais imunoglobulina ou soro no ferimento de alto risco
> Conduta conforme o tipo de ferimento e a história vacinal.
^c
@ Acidente com material biológico: regra dos 3
# 0,3 · 3 · 30 :: 0,3% = risco de HIV no acidente percutâneo; 3% = risco de hepatite C (aproximado); 30% = risco de hepatite B com fonte HBeAg positiva, sem vacina
> Riscos aproximados de transmissão por acidente percutâneo.
! Profilaxia do HIV: iniciar em até 2 h (limite de 72 h), por 28 dias.
^c
@ Dor torácica: escore HEART
# HEART :: História; ECG; Anos: idade; Risco: fatores; Troponina
> Escore de Six e Backus (2008) para a dor torácica no pronto-socorro.
! Cada item vale de 0 a 2. De 0 a 3 = baixo risco.
^c
@ Agitação psicomotora: sequência
# "Verbal, oral, injetável, contenção" :: 1 = manejo verbal e ambiente seguro; 2 = medicação oral oferecida; 3 = intramuscular (haloperidol com ou sem prometazina, ou midazolam); 4 = contenção mecânica pelo menor tempo, com reavaliação
> Sequência do menos para o mais restritivo. A contenção é o último recurso.
^c
"""
