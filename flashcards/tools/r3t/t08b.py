TXT = r"""
@E 🔙 Lombalgia inflamatória × mecânica?
| | Inflamatória | Mecânica
| Início | **< 40–45 anos**, insidioso | Qualquer idade
| Rigidez matinal | > 30 min | < 30 min
| Exercício | **Melhora** | Piora
| Repouso | Piora | Melhora
| Despertar noturno | 2ª metade da noite | Raro
^ ASAS 2009
% cmp Lombalgia inflamatória × mecânica :: Inflamatória = < 45 anos, rigidez > 30 min, melhora com exercício, piora no repouso, dor noturna | Mecânica = Piora com esforço, melhora no repouso, rigidez curta
@E 🦴 Espondilite anquilosante: achados?
- HLA-B27 (~90%)
- **Sacroiliíte** (RM detecta precoce), coluna em "bambu", sindesmófitos
- **Uveíte anterior aguda**, entesite, dactilite
- Insuficiência aórtica, BAV
= AINE → anti-TNF/anti-IL-17.
^ ASAS-EULAR 2022
@E 🦵 Artrite reativa?
- 1–4 semanas após **uretrite** (Chlamydia) ou **disenteria** (Salmonella, Shigella, Campylobacter, Yersinia)
- Oligoartrite assimétrica de MMII
- Tríade: artrite + uretrite + conjuntivite
- Ceratodermia blenorrágica, balanite circinada
^ Revisões
@E 🧴 Artrite psoriásica?
- Comprometimento de **IFD**, dactilite ("dedo em salsicha"), **onicólise**/pitting
- "Lápis na xícara" no RX; artrite mutilante
- Pode preceder a psoríase cutânea
= CASPAR; MTX, anti-TNF, anti-IL-17, anti-IL-23.
^ CASPAR 2006; GRAPPA 2021
@F 💎 Gota × pseudogota?
| | Gota | Pseudogota (CPPD)
| Cristal | Urato monossódico, **agulha**, birrefringência **negativa** | Pirofosfato de cálcio, **romboide**, birrefringência **fracamente positiva**
| Local | 1ª MTF (podagra) | **Joelho**, punho
| RX | Erosões em "saca-bocado" | **Condrocalcinose**
^ ACR/EULAR
% cmp Gota × pseudogota :: Gota = Urato em agulha, birrefringência negativa, podagra, erosões em saca-bocado | Pseudogota = Pirofosfato romboide, fracamente positiva, joelho e punho, condrocalcinose
@F 🔬 Pseudogota: investigar o quê?
= CPPD em < 60 anos ou poliarticular: **hemocromatose**, **hiperparatireoidismo**, **hipomagnesemia**, hipofosfatasia, hipotireoidismo.
^ EULAR 2011
@F 💊 Hipouricemiante na gota: quando e como?
- Indicações: **≥ 2 crises/ano**, tofos, erosão radiográfica, (1ª crise com DRC ≥ 3, ácido úrico > 9 ou litíase)
- **Alopurinol** em dose baixa, titular até **ácido úrico < 6** (< 5 com tofos)
- Profilaxia com colchicina por 3–6 meses ao iniciar
! Pesquisar HLA-B*58:01 em asiáticos/afrodescendentes (SJS).
^ ACR 2020
% flow Tratamento da gota crônica :: Indicação: ≥ 2 crises/ano, tofo ou erosão >> Alopurinol em dose baixa + profilaxia com colchicina >> Titular até ácido úrico < 6 mg/dL >> Refratário: febuxostate, benzbromarona ou pegloticase
@F ⚠️ Drogas que elevam o ácido úrico?
- **Tiazídicos** e diuréticos de alça
- AAS em dose baixa
- Ciclosporina, tacrolimus
- Pirazinamida, etambutol
- Álcool (cerveja), frutose
! **Losartana** e fenofibrato reduzem o ácido úrico.
^ ACR 2020
@F 🦠 Artrite séptica: agentes e conduta?
| Contexto | Agente
| Adulto geral | **S. aureus**
| Jovem sexualmente ativo | Gonococo (poliartralgia, tenossinovite, pústulas)
| Usuário de drogas IV | S. aureus, Pseudomonas (esternoclavicular)
| Falciforme | Salmonella (osteomielite)
= Punção (> 50 mil leucócitos) + ATB + **drenagem**.
^ Revisões
@F 🧪 Líquido sinovial: classificação?
| Tipo | Leucócitos/mm³
| Normal | < 200
| Não inflamatório (OA) | 200–2.000
| Inflamatório (AR, cristais) | 2.000–50.000
| Séptico | **> 50.000** (> 75% PMN)
^ Revisões
% zones Líquido sinovial (leucócitos/mm³) :: Normal = < 200 | Não inflamatório = 200–2.000 | Inflamatório = 2.000–50.000 | Séptico = > 50.000
@G 🦵 Osteoartrite × artrite reumatoide nas mãos?
| | Osteoartrite | AR
| Articulações | **IFD** (Heberden), IFP (Bouchard), 1ª carpometacarpal | **MCF, IFP, punhos**
| Rigidez | < 30 min | > 1 h
| Laboratório | Normal | VHS/PCR, FR, anti-CCP
| RX | Osteófitos, esclerose | Erosões, osteopenia periarticular
^ Revisões
@G 😩 Fibromialgia?
- Dor difusa > 3 meses, fadiga, sono não reparador, alterações cognitivas
- Índice de dor generalizada + escala de gravidade de sintomas (ACR 2016)
- Exames normais
= **Exercício aeróbico** (maior evidência), TCC, duloxetina, amitriptilina, pregabalina.
^ ACR 2016; EULAR 2017
@G 🔥 Doença de Still do adulto?
- Febre em picos diários, **rash asalmonado** evanescente, artrite
- Leucocitose neutrofílica, **ferritina muito alta** (fração glicosilada < 20%)
- FAN e FR negativos (critérios de Yamaguchi)
! Complicação: síndrome de ativação macrofágica.
^ Yamaguchi 1992
@G 🦴 Síndrome do túnel do carpo?
- Parestesias noturnas em território do **mediano** (1º ao 3º dedo e metade do 4º)
- **Tinel** e **Phalen** positivos
- Associações: gestação, hipotireoidismo, DM, acromegalia, amiloidose, AR
= Eletroneuromiografia confirma.
^ AAOS 2016
@G 🧪 Diagnóstico de FAN: padrões e associações?
| Padrão | Associação
| Homogêneo | LES, lúpus induzido (anti-dsDNA, histona)
| Pontilhado grosso | Anti-Sm, anti-RNP
| Pontilhado fino | Anti-Ro, anti-La (Sjögren)
| Centromérico | **Esclerodermia limitada**
| Nucleolar | Esclerodermia difusa
| Pontilhado fino denso (DFS70) | **Indivíduos saudáveis**
^ Consenso Brasileiro de FAN (HEp-2)
"""
