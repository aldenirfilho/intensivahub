TXT = r"""
## 07 🫘 Rim, ácido-base e eletrólitos
@ Indicações de diálise de urgência
# AEIOU :: Acidose refratária; Eletrólitos: hipercalemia refratária; Intoxicações dialisáveis; Overload: sobrecarga de volume; Uremia: pericardite, encefalopatia e sangramento
^c
@ Acidose com ânion gap elevado (clássico)
# MUDPILES :: Metanol; Uremia; Diabetes: cetoacidose; Paraldeído e propilenoglicol; Isoniazida e intoxicação por ferro; Lactato; Etilenoglicol; Salicilatos
^c
@ Acidose com ânion gap elevado (atual)
# GOLD MARK :: Glicóis: etileno e propileno; Oxoprolina (paracetamol crônico); L-lactato; D-lactato; Metanol; Aspirina; Renal: uremia; Ketoacidose (cetoacidose)
^c
@ Acidose com ânion gap normal
# DURAS :: Diarreia; Ureterossigmoidostomia e fístulas; Renal: acidose tubular; Acetazolamida; Salina em excesso
^o
@ Alcalose metabólica pelo cloro urinário
# Cloro 20 :: Abaixo de 20 = responde a cloreto (vômitos, diurético prévio, pós-hipercapnia); Acima de 20 = resistente (hiperaldosteronismo, Bartter, Gitelman, diurético em uso)
^c
@ Compensação esperada na acidose metabólica (Winter)
# 1,5 × HCO₃ + 8 :: PaCO₂ esperada = 1,5 × bicarbonato + 8 (± 2); Acima do esperado = acidose respiratória associada; Abaixo do esperado = alcalose respiratória associada
^c
@ Compensação nos distúrbios respiratórios
# 1-4-2-5 :: 1 = bicarbonato sobe 1 na acidose aguda (a cada 10 de PaCO₂); 4 = sobe 4 na acidose crônica; 2 = cai 2 na alcalose aguda; 5 = cai 5 na alcalose crônica
^c
@ Ânion gap
# 12 · 2,5 :: Fórmula = sódio − (cloro + bicarbonato); 12 = valor normal (± 4); 2,5 = somar para cada 1 g/dL de albumina abaixo de 4
^c
@ Delta-delta
# 1 · 2 :: Abaixo de 1 = acidose hiperclorêmica associada; Entre 1 e 2 = ânion gap elevado puro; Acima de 2 = alcalose metabólica associada
^c
@ Tratamento da hipercalemia
# C BIG K D :: Cálcio estabiliza a membrana; Beta-2 agonista e bicarbonato; Insulina; Glicose; Kayexalate: resina de troca; Diurético ou diálise
! O cálcio não baixa o potássio: só protege o coração por 30–60 min.
^c
@ ECG da hipercalemia em sequência
# "Tenda, Plana, Largo, Seno" :: Tenda = T apiculada; Plana = P achatada e PR longo; Largo = QRS alargado; Seno = onda sinusoidal antes da parada
^o
@ Hiponatremia hipotônica pela volemia
# Hipo · Eu · Hiper :: Hipovolêmica = perdas (diurético, diarreia, perdedora de sal); Euvolêmica = SIADH, hipotireoidismo, insuficiência adrenal e polidipsia; Hipervolêmica = insuficiência cardíaca, cirrose e síndrome nefrótica
^c
@ Causas de SIADH
# SIADH :: SNC: AVC, trauma e meningite; Intratorácica: pneumonia, tuberculose e ventilação; Antidepressivos e anticonvulsivantes; Dor, náusea e pós-operatório; Hormônio ectópico: carcinoma de pequenas células
^o
@ Correção do sódio: limites
# 150 · 4–6 · 8 :: 150 mL de salina 3% = bolus na hiponatremia grave sintomática; 4–6 mEq/L = aumento que reverte os sintomas; 8 mEq/L = máximo em 24 h; 6 mEq/L = máximo se alto risco de desmielinização
^c
@ Risco de desmielinização osmótica
# HADES :: Hipocalemia; Alcoolismo; Desnutrição; Enfermidade hepática avançada; Sódio ≤ 105 mEq/L
^o
@ Hipercalcemia grave: tratamento
# SoCaZo + 3 D :: So = Soro fisiológico 200–300 mL/h; Ca = Calcitonina 4 UI/kg (efeito rápido, some em 48 h); Zo = Zoledronato 4 mg (age em 2 a 4 dias); D1 = Denosumabe se refratária ou com insuficiência renal; D2 = Diálise se grave com anúria; D3 = Dexametasona ou prednisona em linfoma e granulomatoses
^o
@ Lesão renal aguda: estágios KDIGO
# 1,5 · 2 · 3 :: Estágio 1 = creatinina 1,5 a 1,9 vez ou + 0,3 mg/dL, diurese < 0,5 por 6–12 h; Estágio 2 = 2 a 2,9 vezes, diurese < 0,5 por 12 h ou mais; Estágio 3 = 3 vezes ou mais, ≥ 4,0 mg/dL ou diálise, diurese < 0,3 por 24 h ou anúria por 12 h
^c
@ Pré-renal ou necrose tubular?
# FENa 1% :: FENa < 1% = pré-renal; FENa > 2% = necrose tubular aguda; FE de ureia < 35% = pré-renal (vale com diurético); Sódio urinário < 20 = pré-renal
^c
@ Terapia renal contínua: números
# 25 · 20% · 2,5 :: 20–25 mL/kg/h = dose de efluente a entregar; 20–25% = teto da fração de filtração; 2,5 = razão cálcio total ÷ iônico que indica acúmulo de citrato
^c
@ Gasometria em seis passos
# 6 passos :: 1 = pH: acidemia ou alcalemia; 2 = PaCO₂ e bicarbonato: qual explica o pH; 3 = compensação esperada; 4 = ânion gap corrigido pela albumina; 5 = delta-delta; 6 = gap osmolar se o ânion gap for alto sem causa
^o
@ Osmolaridade calculada e gap osmolar
# 2 Na + Gli/18 + Ur/6 :: Osmolaridade = 2 × sódio + glicose ÷ 18 + ureia ÷ 6; Gap osmolar = medida − calculada; 10 = limite do gap normal
^c
@ Causas de gap osmolar elevado
# ME DIE :: Metanol; Etilenoglicol; Diuréticos osmóticos (manitol); Isopropanol; Etanol
^c

## 08 🫃 Gastro, fígado e nutrição
@ Checklist diário FAST HUG
# FAST HUG :: Feeding: nutrição; Analgesia; Sedação mínima; Tromboprofilaxia; Head up: cabeceira elevada; Úlcera de estresse: profilaxia se houver risco; Glicemia controlada
^c
@ FAST HUG ampliado: BID
# BID :: Bowel: função intestinal; Invasivos: retirar cateteres e sondas; Descalonar antibióticos
^c
@ Síndrome de realimentação
# "Fome Para Muito Tempo" :: Fome = Fósforo baixo; Para = Potássio baixo; Muito = Magnésio baixo; Tempo = Tiamina em falta
! Repor tiamina antes de alimentar e progredir a dieta devagar.
^of
@ Metas de nutrição no crítico
# 25 · 1,3 · 48 h :: 25 kcal/kg/dia = meta calórica depois da fase aguda; 1,3 g/kg/dia = proteína; 24–48 h = prazo para iniciar a enteral; 70% = oferta suficiente na primeira semana
^c
@ Quando adiar a nutrição enteral
# FOICES :: Fístula de alto débito sem acesso distal; Obstrução intestinal; Isquemia mesentérica; Choque não controlado; Estômago com resíduo > 500 mL em 6 h; Sangramento digestivo ativo e síndrome compartimental abdominal
^o
@ Hemorragia varicosa: conduta
# VEIAS :: Vasoconstritor esplâncnico (terlipressina ou octreotida); Endoscopia em até 12 h com ligadura; Infecção: ceftriaxona profilática; Alvo de hemoglobina 7–8 g/dL; Shunt: TIPS precoce nos de alto risco
^o
@ Child-Pugh
# BATEA :: Bilirrubina; Albumina; Tempo de protrombina (INR); Encefalopatia; Ascite
! A = 5–6 pontos, B = 7–9, C = 10–15.
^c
@ MELD
# BIC :: Bilirrubina; INR; Creatinina
! O MELD-Na acrescenta o sódio.
^c
@ Precipitantes de encefalopatia hepática
# HEPÁTICA :: Hemorragia digestiva; Eletrólitos: hipocalemia e hiponatremia; Psicotrópicos: benzodiazepínicos e opioides; Alcalose; TIPS; Infecção (pensar em peritonite espontânea); Constipação; Azotemia por desidratação ou diurético
^o
@ Encefalopatia hepática: graus de West Haven
# I-II-III-IV :: I = inversão do sono e desatenção; II = letargia, desorientação e flapping; III = sonolência, confusão, responde a estímulos; IV = coma
^c
@ Peritonite bacteriana espontânea: números
# 250 · 1,5 · 1,1 :: 250 = neutrófilos por mm³ no líquido que fecham o diagnóstico; 1,5 g/kg = albumina no dia 1 (e 1 g/kg no dia 3); 1,1 = gradiente de albumina soro-ascite que indica hipertensão portal
^c
@ Diagnóstico de pancreatite aguda
# DAI :: Dor abdominal típica; Amilase ou lipase ≥ 3 vezes o normal; Imagem compatível
! Bastam dois dos três.
^o
@ Pancreatite: gravidade pela Atlanta revisada
# 48 h :: Leve = sem falência orgânica nem complicação local; Moderadamente grave = falência orgânica por menos de 48 h ou complicação local; Grave = falência orgânica por mais de 48 h
^c
@ Pressão intra-abdominal
# 12 · 20 :: 12 mmHg = hipertensão intra-abdominal; 20 mmHg = síndrome compartimental se houver nova disfunção orgânica; Graus = I 12–15, II 16–20, III 21–25, IV acima de 25
^c
@ King's College no paracetamol
# 7,3 ou 6,5 + 3,4 + III :: pH < 7,3 = critério isolado depois da ressuscitação; INR > 6,5 = junto com os dois seguintes; Creatinina > 3,4 mg/dL = junto com os outros; Encefalopatia grau III ou IV = junto com os outros
^c
@ Definição de insuficiência hepática aguda
# 1,5 · 26 :: INR ≥ 1,5 = coagulopatia; Encefalopatia = qualquer grau; 26 semanas = duração máxima da doença; Sem cirrose = fígado previamente normal
^c
@ Isquemia mesentérica aguda: tipos
# ETNV :: Embolia arterial (a mais comum); Trombose arterial; Não oclusiva (baixo fluxo); Venosa: trombose
! Dor desproporcional ao exame físico.
^c
@ Quem precisa de profilaxia de úlcera de estresse
# VaCa ChoQue :: Va = Ventilação mecânica por mais de 48 h; Ca = Coagulopatia; Cho = Choque; Que = Queimado grave e trauma craniano ou medular
^o
@ Diarreia na UTI
# DIE :: Drogas: antibiótico, procinético e sorbitol; Infecção: Clostridioides difficile; Enteral: fórmula e velocidade
^o
@ Classificação de Forrest
# Ia → III :: Ia = sangramento em jato; Ib = sangramento em babação; IIa = vaso visível; IIb = coágulo aderido; IIc = hematina; III = base limpa
! Tratamento endoscópico de Ia a IIa.
^c
@ Síndrome hepatorrenal: critérios
# ASCITE :: Ascite com cirrose; Sem choque; Creatinina em ascensão (critério KDIGO); Inalterada após 48 h de albumina sem diurético; Tóxicos renais ausentes; Exame de urina e ultrassom normais
^o
@ Hepatite alcoólica: escores
# 32 · 0,45 :: 32 = Maddrey acima disso indica corticoide; 0,45 = Lille acima disso no dia 7 significa não respondedor
^c
"""
