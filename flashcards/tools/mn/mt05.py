TXT = r"""
## 09 🩸 Hematologia e transfusão
@ Diamante letal do trauma
# HACH :: Hipotermia; Acidose; Coagulopatia; Hipocalcemia
^c
@ TRALI × TACO
# Pulmão × volume :: TRALI = edema não cardiogênico em até 6 h, com hipotensão, febre e BNP baixo; TACO = sobrecarga com hipertensão e BNP alto, melhora com diurético
^c
@ Hemoglobina: gatilhos de transfusão
# 7 · 8 · 10 :: 7 g/dL = maioria dos pacientes críticos; 8 g/dL = cardiopata estável e cirurgia ortopédica ou cardíaca; 10 g/dL = considerar no infarto agudo
^c
@ Plaquetas: gatilhos de transfusão
# 10 · 20 · 50 · 100 :: 10 mil = profilática sem sangramento e cateter central em sítio compressível; 20 mil = punção lombar; 50 mil = cirurgia de grande porte ou sangramento ativo; 100 mil = neurocirurgia e sangramento no sistema nervoso central
^c
@ Transfusão maciça: números
# 1:1:1 · 1 g · 1,1 · 150 :: 1:1:1 = plasma, plaquetas e hemácias; 1 g + 1 g = ácido tranexâmico em até 3 h; 1,1 mmol/L = cálcio iônico mínimo; 150 mg/dL = fibrinogênio mínimo
^c
@ Escore ISTH de CIVD
# PDFT :: Plaquetas; D-dímero; Fibrinogênio; Tempo de protrombina
! Cinco pontos ou mais = CIVD manifesta.
^c
@ Escore 4 T da trombocitopenia por heparina
# 4 T :: Trombocitopenia = queda acima de 50%; Tempo = entre o 5º e o 10º dia; Trombose = nova ou necrose cutânea; ouTras causas = ausentes
^c
@ Pêntade da púrpura trombocitopênica trombótica
# FATRN :: Febre; Anemia hemolítica microangiopática; Trombocitopenia; Renal: disfunção; Neurológico: alteração
! A pêntade completa é rara: anemia microangiopática com plaquetopenia já basta para suspeitar.
^c
@ Escore PLASMIC
# PLASMIC :: Plaquetas < 30 mil; Lise: hemólise presente; Ausência de câncer ativo; Sem transplante; MCV (VCM) < 90 fL; INR < 1,5; Creatinina < 2,0 mg/dL
! Seis ou sete pontos = alto risco de púrpura trombocitopênica trombótica.
^c
@ Laboratório da síndrome de lise tumoral
# "Sobe PUK, cai Ca" :: P = fósforo sobe; U = ácido úrico sobe; K = potássio sobe; Ca = cálcio cai
^o
@ Reação transfusional aguda: conduta
# PARE :: Parar a transfusão; Acesso mantido com salina; Rever a identificação da bolsa e do paciente; Enviar bolsa e amostras ao banco de sangue
^o
@ O que tem no crioprecipitado
# F-8-13-vW :: F = fibrinogênio; 8 = fator VIII; 13 = fator XIII; vW = fator de von Willebrand
^c
@ Fatores dependentes de vitamina K
# 2-7-9-10 + C e S :: 2, 7, 9 e 10 = fatores pró-coagulantes; C e S = proteínas anticoagulantes; 7 = o de meia-vida mais curta (o INR sobe primeiro)
^c
@ Reversão de anticoagulantes
# Antídotos da anticoagulação :: Varfarina = vitamina K + complexo protrombínico; Heparina = protamina; Dabigatrana = idarucizumabe; Anti-Xa (rivaroxabana, apixabana) = andexanet ou complexo protrombínico
^c
@ Causas de anemia microangiopática
# CHAPS :: CIVD; HELLP; aHUS e síndrome hemolítico-urêmica típica; PTT; Sistêmicas: hipertensão maligna, lúpus e prótese valvar
^o
@ Tromboelastometria: o que repor
# 4 leituras :: Tempo de coagulação longo = fatores (plasma ou complexo protrombínico); FIBTEM baixo = fibrinogênio (crioprecipitado); Firmeza máxima baixa com FIBTEM normal = plaquetas; Lise aumentada = ácido tranexâmico
^c
@ Tríade da hiperviscosidade
# NOS :: Neurológico: cefaleia e confusão; Ocular: visão turva e veias em salsicha; Sangramento de mucosas
^c
@ Plaquetopenia na UTI
# CHIPS :: Consumo: CIVD, circuito extracorpóreo e balão; Heparina e outras drogas; Infecção: sepse (a causa mais comum); Pseudotrombocitopenia pelo EDTA; Sequestro esplênico e diluição
^o
@ Rendimento dos hemocomponentes
# +1 · +30 · 10–15 :: 1 concentrado de hemácias = +1 g/dL de hemoglobina; 1 dose de plaquetas = +30 a 50 mil; Plasma = 10 a 15 mL/kg; Crioprecipitado = 1 unidade para cada 10 kg
^c
@ TTPa prolongado isolado: teste da mistura
# Corrige × não corrige :: Corrige = deficiência de fator (VIII, IX, XI, XII, von Willebrand); Não corrige = inibidor (anticoagulante lúpico, heparina, anti-fator VIII)
^c

## 10 ☠️ Toxicologia e ambiente
@ Síndrome colinérgica muscarínica
# DUMBELS :: Diarreia; Urina: incontinência; Miose; Broncorreia, broncoespasmo e bradicardia; Êmese; Lacrimejamento; Salivação
^c
@ Síndrome colinérgica nicotínica (dias da semana)
# MTWHF :: Midríase; Taquicardia; Weakness: fraqueza; Hipertensão; Fasciculações
^c
@ Síndrome anticolinérgica
# "Seco, vermelho, quente, cego, louco, cheio" :: Seco = pele e mucosas secas; Vermelho = rubor; Quente = hipertermia; Cego = midríase e visão turva; Louco = delirium e alucinações; Cheio = retenção urinária e íleo
^c
@ Antídotos I
# Antídotos I :: Paracetamol = N-acetilcisteína; Opioide = naloxona; Benzodiazepínico = flumazenil (raramente indicado); Organofosforado = atropina e pralidoxima; Metanol e etilenoglicol = fomepizol ou etanol; Betabloqueador = glucagon e insulina em alta dose; Bloqueador de canal de cálcio = cálcio e insulina em alta dose; Digoxina = anticorpo antidigoxina
^c
@ Antídotos II
# Antídotos II :: Cianeto = hidroxocobalamina; Isoniazida = piridoxina; Ferro = deferoxamina; Metemoglobinemia = azul de metileno; Tricíclico = bicarbonato de sódio; Anestésico local = emulsão lipídica 20%; Sulfonilureia = octreotida; Heparina = protamina
^c
@ Miose: causas tóxicas e estruturais
# COPS :: Colinérgicos e clonidina; Opioides; Ponte: hemorragia pontina; Sedativo-hipnóticos
^c
@ Midríase: causas tóxicas
# AAAS :: Anticolinérgicos; Antidepressivos tricíclicos; Abstinência; Simpaticomiméticos
^c
@ Intoxicações em que a diálise ajuda
# I STUMBLE :: Isopropanol; Salicilatos; Teofilina; Uremia; Metanol; Barbitúricos; Lítio; Etilenoglicol
! Também valproato e metformina.
^c
@ O que o carvão ativado não adsorve
# PHAILS :: Pesticidas; Hidrocarbonetos; Ácidos, álcalis e álcoois; Iron: ferro e outros metais; Lítio; Solventes
^c
@ Paracetamol: números
# 150 · 4 h · 150-50-100 :: 150 mg/kg = dose tóxica; 4 h = primeira dosagem válida para o nomograma; 150 µg/mL em 4 h = linha de tratamento; 150-50-100 mg/kg = N-acetilcisteína em 1 h, 4 h e 16 h
^c
@ Intoxicação por salicilato
# Zumbido + duplo distúrbio :: Gasometria = alcalose respiratória com acidose metabólica de ânion gap alto; Tratamento = alcalinizar a urina até pH 7,5–8; Diálise = nível acima de 90–100 mg/dL, rebaixamento, edema pulmonar ou insuficiência renal
! Evitar intubar: a hiperventilação é protetora.
^c
@ Tricíclicos: os 3 C
# 3 C :: Coma = rebaixamento; Convulsão = benzodiazepínico; Cardiotoxicidade = QRS acima de 100 ms pede bicarbonato de sódio
^c
@ Serotoninérgica × neuroléptica maligna
# Horas × dias :: Serotoninérgica = início em horas, clônus, hiper-reflexia, midríase e diarreia (ciproeptadina); Neuroléptica maligna = início em dias, rigidez em cano de chumbo, hiporreflexia e CK alta (dantrolene, bromocriptina)
^c
@ Álcoois tóxicos
# Olho · rim · cetona :: Metanol = cegueira (ácido fórmico); Etilenoglicol = rim, cristais de oxalato e hipocalcemia; Isopropanol = cetose sem acidose
^c
@ Monóxido de carbono: meia-vida da carboxi-hemoglobina
# 320-90-23 :: 320 min = em ar ambiente; 90 min = com O₂ a 100%; 23 min = em câmara hiperbárica
! O oxímetro comum lê saturação falsamente normal.
^c
@ Hipotermia acidental: estágios suíços
# 32-28-24 :: Estágio I (35–32 °C) = consciente e tremendo; Estágio II (32–28 °C) = rebaixado e sem tremor; Estágio III (28–24 °C) = inconsciente com sinais vitais; Estágio IV (abaixo de 24 °C) = sem sinais vitais
^c
@ PCR na hipotermia
# 30 °C :: Abaixo de 30 °C = sem drogas e até 3 choques; Entre 30 e 35 °C = dobrar o intervalo da adrenalina; Potássio acima de 12 mEq/L = reanimação fútil
! Ninguém está morto até estar quente e morto.
^c
@ Golpe de calor
# 40 + SNC :: 40 °C = temperatura central; SNC = disfunção neurológica (delirium, convulsão, coma); 39 °C em 30 min = alvo do resfriamento
! Antitérmico não funciona.
^c
@ Acidentes ofídicos no Brasil
# 4 gêneros :: Botrópico (jararaca) = dor, edema e sangramento; Crotálico (cascavel) = fácies miastênica, rabdomiólise e urina escura; Laquético (surucucu) = quadro botrópico com sinais vagais; Elapídico (coral) = paralisia flácida e insuficiência respiratória
^c
@ Aranhas de importância médica
# 3 aranhas :: Armadeira (Phoneutria) = dor intensa imediata, priapismo e edema pulmonar na criança; Marrom (Loxosceles) = necrose tardia e hemólise; Viúva-negra (Latrodectus) = contraturas, sudorese e hipertensão
^c
@ Tríade do opioide
# MRD :: Miose; Rebaixamento da consciência; Depressão respiratória
^c
@ Organofosforado: conduta
# ASA :: Atropina dobrando a dose a cada 5 min; Secreção pulmonar seca é a meta; Associar pralidoxima
! Não guiar pela pupila nem pela frequência cardíaca.
^o
@ Carvão ativado em doses múltiplas
# "Carvão Que Trata De Fato" :: Carvão = Carbamazepina; Que = Quinina; Trata = Teofilina; De = Dapsona; Fato = Fenobarbital
^of
@ Metemoglobinemia
# 85% · chocolate · 1–2 :: 85% = saturação travada no oxímetro; Chocolate = cor do sangue arterial; 1–2 mg/kg = dose de azul de metileno; G6PD = deficiência contraindica o azul de metileno
^c
"""
