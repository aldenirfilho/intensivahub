TXT = r"""
@D 🔥 Brugada: drogas e situações que desmascaram?
- **Febre** (tratar agressivamente com antitérmico)
- Bloqueadores de sódio: **flecainida, propafenona, procainamida** (também usados no teste provocativo), tricíclicos, lítio
- Cocaína, álcool em excesso, hipercalemia
^ brugadadrugs.org
@D 🔥 QT longo congênito: gatilho por subtipo?
| Tipo | Canal | Gatilho típico |
| LQT1 | KCNQ1 (IKs) | **Exercício, natação** |
| LQT2 | KCNH2 (IKr) | **Estímulo auditivo**, pós-parto |
| LQT3 | SCN5A (INa) | **Sono/repouso** |
= LQT1/2: betabloqueador (nadolol/propranolol); LQT3: mexiletina pode ajudar.
^ ESC 2022
% cmp QT longo congênito :: LQT1 = Exercício e natação · KCNQ1 | LQT2 = Susto/despertador · pós-parto · KCNH2 | LQT3 = Sono e bradicardia · SCN5A
@D 🔥 Flecainida/propafenona: contraindicação?
= **Cardiopatia estrutural** (IAM prévio, FE reduzida, HVE importante, DAC) — mortalidade ↑ no CAST.
! Na FA, associar bloqueador do nó AV: risco de **flutter 1:1** com QRS largo.
^ CAST 1989 · ESC 2024 FA
@D 🔥 Fenômeno de Ashman?
= Batimento com **aberração (BRD)** após ciclo longo seguido de ciclo curto na FA.
! Não confundir com TV não sustentada.
^ ECG clássico
@D 🔥 Ablação de FA como 1ª linha?
= Paroxística sintomática em jovem: **ablação de 1ª linha** é opção (EARLY-AF, STOP-AF First).
- ICFEr + FA: ablação ↓ mortalidade e internação (CASTLE-AF, CASTLE-HTx)
^ ESC 2024
@D 🔥 Oclusão percutânea do apêndice atrial esquerdo?
= FA com **contraindicação** a anticoagulação de longo prazo (sangramento grave recorrente).
- Exige antitrombótico por curto período após o implante
^ ESC 2024
@D 🔥 TV × TSV com aberrância: critérios que favorecem TV?
- **Dissociação AV**, batimentos de fusão/captura
- Concordância precordial (tudo + ou tudo −)
- Ausência de RS nas precordiais; R inicial em aVR (Vereckei)
= Na dúvida, tratar como **TV**.
^ Brugada 1991 · Vereckei 2008
@D 🔥 Intoxicação digitálica: ECG e conduta?
- Taquicardia atrial com BAV, **TV bidirecional**, ritmo juncional acelerado
- **Fab antidigoxina**: arritmia grave, K > 5–5,5, digoxina muito alta
! Cálcio IV na hipercalemia digitálica: controverso, evitar como rotina.
^ Goldfrank
@E 🔥 Escore de cálcio valvar na EAo baixo gradiente com FE preservada?
= Sugere estenose grave: **≥ 2.000 UA (homem)** ou **≥ 1.200 UA (mulher)** na TC.
^ ESC 2021
@E 🔥 Síndrome de Heyde?
= **Estenose aórtica + sangramento GI por angiodisplasia**, com Willebrand adquirido (tipo 2A por cisalhamento).
= Melhora após troca valvar.
^ NEJM 2003
@E 🔥 Critérios de Duke-ISCVID 2023: o que entrou?
- **PET-CT** e TC cardíaca como critério de imagem
- PCR/sequenciamento como microbiológico; **Enterococcus faecalis** e outros como típicos
- Achado cirúrgico como maior
^ Fowler 2023
@E 🔥 Endocardite com hemocultura negativa: principais agentes?
- **Coxiella burnetii** (sorologia fase I), **Bartonella** (sem-teto, gatos)
- Brucella, Tropheryma whipplei, fungos, HACEK, uso prévio de antibiótico
^ ESC 2023
@E 🔥 Endocardite + AVC isquêmico: quando operar?
= Indicação cirúrgica presente e AVC isquêmico **sem hemorragia e sem coma**: operar **sem esperar**.
! AVC hemorrágico: adiar ≥ 4 semanas, em geral.
^ ESC 2023
@E 🔥 Trombose de prótese mecânica obstrutiva: conduta?
- Instável/grave: **cirurgia de urgência**
- Sem condição cirúrgica ou centro sem cirurgia: **trombólise**
- Não obstrutiva pequena: otimizar anticoagulação
^ ESC 2021
@E 🔥 TAVI × cirurgia: corte de idade (ESC 2021)?
= **≥ 75 anos** ou alto risco → TAVI transfemoral; **< 75 anos** e baixo risco → cirurgia.
! Valva bicúspide, aorta e anatomia pesam na decisão do Heart Team.
^ ESC 2021
% zones EAo grave: estratégia :: < 75 anos + baixo risco = Troca cirúrgica | Zona cinzenta = Heart Team decide | ≥ 75 anos ou alto risco = TAVI transfemoral
"""
