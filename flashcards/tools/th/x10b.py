TXT = r"""
@C 🔥 Acidente laquético (surucucu): o que o diferencia do botrópico?
= Quadro local semelhante (dor, edema, sangramento, coagulopatia) **mais síndrome vagal**: bradicardia, hipotensão, cólica, diarreia e vômitos.
= Soro antilaquético ou antibotrópico-laquético, **10 a 20 ampolas**.
^ MS · Manual de acidentes por animais peçonhentos
@C 🔥 Acidente elapídico (coral verdadeira): quadro e tratamento?
= **Bloqueio neuromuscular**: ptose, oftalmoplegia, fraqueza progressiva e **insuficiência respiratória**; pouca reação local.
- Todo caso é potencialmente grave: **soro antielapídico, 10 ampolas**
- **Neostigmina** (precedida de atropina) como teste e ponte; ventilação mecânica
^ MS · Manual de acidentes por animais peçonhentos
@C 🔥 Acidente por Lonomia (taturana): síndrome e tratamento?
= Dor em queimação após contato com lagartas; horas depois, **síndrome hemorrágica por consumo** (gengivorragia, equimoses, hematúria, sangramento intracraniano) e lesão renal.
= **Soro antilonômico**: 5 ampolas (moderado) ou 10 (grave); evitar plasma/crioprecipitado antes do soro.
^ MS · Manual de acidentes por animais peçonhentos
@C 🔥 Picadas múltiplas de abelhas: quando há risco de vida sem alergia?
= **> 500 picadas** (toxicidade direta): **rabdomiólise, hemólise, lesão renal aguda**, lesão miocárdica e hepática.
= Retirar os ferrões por **raspagem**, hidratação vigorosa, corticoide e anti-histamínico; diálise precoce. Não há soro disponível de rotina.
^ MS · Manual de acidentes por animais peçonhentos
@C 🔥 Foneutrismo (aranha armadeira): sinais de gravidade?
= Dor imediata intensa. Grave (mais em crianças): **priapismo, sudorese profusa, vômitos, arritmia, choque e edema agudo de pulmão**.
= Bloqueio anestésico local para a dor; **soro antiaracnídico** nos casos moderados (2–4 ampolas) e graves (5–10).
^ MS · Manual de acidentes por animais peçonhentos
@C 🔥 Escorpionismo grave: mecanismo do edema pulmonar?
= Tempestade autonômica com **disfunção miocárdica aguda** (tipo catecolaminérgica) → edema **cardiogênico** e choque.
= Soro antiescorpiônico (4–6 ampolas no grave), ventilação, **dobutamina** e vasodilatador conforme a hemodinâmica; volume com cautela.
^ MS · Cupo 2015
@C 🔥 Soro antiveneno: reação precoce e conduta?
= Anafilática ou anafilactoide nas primeiras 2 h.
- Infusão **sem teste de sensibilidade**; equipe e adrenalina prontas
- Reação: **parar a infusão**, adrenalina IM, anti-histamínico, corticoide; reiniciar mais devagar após controle
- **Doença do soro**: 5–24 dias depois (febre, artralgia, urticária) → corticoide
^ MS · Manual de acidentes por animais peçonhentos
@D 🔥 Intermação (heat stroke): definição, tipos e complicações?
= Temperatura central **> 40 °C + disfunção do sistema nervoso central**.
- **Clássica**: idoso, onda de calor, pele seca
- **Por esforço**: jovem, sudorese presente, mais rabdomiólise
- Complicações: CIVD, insuficiência hepática (pico em 48–72 h), lesão renal, SDRA
^ Epstein NEJM 2019
@D 🔥 Hipotermia acidental: estadiamento suíço?
| Estágio | Clínica | Temperatura estimada |
| I | Consciente, **tremendo** | 35–32 °C |
| II | Sonolento, **sem tremor** | 32–28 °C |
| III | Inconsciente, com sinais vitais | 28–24 °C |
| IV | Morte aparente | < 24 °C |
^ Durrer 2003 · ERC 2021
% zones Hipotermia acidental (estágios suíços) :: I · 35–32 °C = Consciente, tremendo | II · 32–28 °C = Sonolento, sem tremor | III · 28–24 °C = Inconsciente, com sinais vitais | IV · < 24 °C = Morte aparente · ECMO
@D 🔥 Hipotermia: achados do ECG e risco de arritmia?
- **Onda J de Osborn** (entalhe no fim do QRS), bradicardia, prolongamento de PR, QRS e QT, fibrilação atrial lenta
- **< 28 °C**: miocárdio irritável → fibrilação ventricular com manipulação brusca
- **Afterdrop**: queda adicional da temperatura central ao reaquecer a periferia
^ Brown NEJM 2012
@D 🔥 Hipotermia com PCR: quem vai para reaquecimento extracorpóreo?
= PCR presenciada ou sem sinais de asfixia prévia, sem trauma letal.
- Escore **HOPE** estima a sobrevida (melhor que o potássio isolado)
- **Potássio > 12 mmol/L** (adulto): reanimação fútil
- Só declarar óbito após reaquecer a **32–35 °C**
^ ERC 2021 · Pasquier 2018
@D 🔥 Afogamento: o que NÃO fazer e prognóstico?
- **Não** tentar drenar água (Heimlich); **sem** antibiótico ou corticoide profiláticos
- Imobilização cervical só com história de mergulho/trauma
- Mau prognóstico: submersão **> 10 min**, RCP > 25 min, sem retorno da circulação na cena
= Ventilação protetora com PEEP; observar 6–8 h os que têm sintomas leves.
^ Szpilman NEJM 2012
@D 🔥 Edema pulmonar e edema cerebral de altitude?
| | Edema pulmonar (HAPE) | Edema cerebral (HACE) |
| Quadro | Dispneia em repouso, tosse rósea, 2–4 dias | Ataxia, confusão, coma |
| Tratamento | **Descida**, O₂, **nifedipina**; sildenafila | **Descida**, O₂, **dexametasona 8 mg → 4 mg 6/6 h** |
| Prevenção | Ascensão lenta, nifedipina | Acetazolamida |
^ Wilderness Medical Society 2019
@D 🔥 Embolia gasosa arterial (mergulho ou iatrogênica): conduta?
= Déficit neurológico súbito ou colapso após emersão rápida, punção torácica ou acesso central.
- **O₂ a 100%**, posição **supina horizontal**, volume
- **Oxigenoterapia hiperbárica** o mais cedo possível
! Embolia **venosa** (cateter central): decúbito lateral esquerdo com cabeça baixa e aspirar pelo cateter.
^ UHMS · Muth 2000
@D 🔥 Vítimas de raio: particularidades?
- **Triagem reversa**: atender primeiro quem parece morto (apneia prolongada e assistolia reversíveis)
- Ceraunoparalisia (paralisia transitória de membros), ruptura timpânica, figuras de Lichtenberg
- Queimadura profunda é rara (ao contrário da alta voltagem)
^ ERC 2021
@D 🔥 Inalação de fumaça: três lesões e três condutas?
- **Térmica de via aérea alta**: edema progressivo → intubação precoce
- **Química de via aérea baixa**: broncoscopia, toalete, ventilação protetora; heparina e N-acetilcisteína nebulizadas (evidência limitada)
- **Sistêmica**: monóxido de carbono (O₂ a 100%) e **cianeto** (hidroxocobalamina se lactato muito alto)
^ ABA
@D 🔥 Hipertermias induzidas por drogas: como distinguir?
| | Gatilho | Tônus | Tratamento |
| Hipertermia maligna | Halogenados, succinilcolina | Rigidez, masseter | Dantrolene |
| Neuroléptica maligna | Antagonista dopaminérgico | Rigidez plástica, lenta (dias) | Bromocriptina/dantrolene |
| Serotoninérgica | Serotoninérgicos | **Clônus, hiper-reflexia**, rápida (horas) | Ciproeptadina |
| Anticolinérgica | Atropínicos | Normal, pele seca | Fisostigmina |
| Simpatomimética | Cocaína, anfetaminas | Agitação, sudorese | Benzodiazepínico |
^ Goldfrank
"""
