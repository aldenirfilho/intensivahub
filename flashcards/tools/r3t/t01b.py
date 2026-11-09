TXT = r"""
@C 🩺 Classificação clínica da dor torácica?
| Tipo | Critérios
| Angina típica | 3 de 3: retroesternal, desencadeada por esforço/estresse, alivia com repouso/nitrato
| Angina atípica | 2 de 3
| Dor não anginosa | 0–1 de 3
^ ESC 2019 síndromes coronarianas crônicas
@C 🔬 Escolha do teste na suspeita de DAC estável?
- Probabilidade baixa-intermediária: **angio-TC de coronárias**
- Intermediária-alta: teste funcional (cintilografia, eco de estresse, RM)
- Alta probabilidade ou alto risco: **cateterismo**
! Teste ergométrico tem baixa sensibilidade e não é possível com BRE ou marca-passo.
^ ESC 2019; SBC 2024
@C 💊 Tratamento antianginoso e de prevenção na DAC crônica?
- Prevenção: **AAS**, **estatina de alta potência**, IECA se DM/HAS/IC/DRC
- Sintoma: betabloqueador ou BCC; nitrato de ação rápida
- 2ª linha: nitrato de longa ação, ivabradina, trimetazidina, ranolazina
! ISCHEMIA: revascularização em DAC estável não reduziu mortalidade vs tratamento clínico otimizado.
^ ISCHEMIA 2020; ESC 2019
@C 🧪 Definição universal de IAM?
= ↑ e/ou ↓ de **troponina** com ≥ 1 valor > **percentil 99** + evidência de isquemia:
- Sintomas isquêmicos
- Alterações novas de ECG (ST, BRE novo, Q patológica)
- Perda nova de miocárdio viável/alteração segmentar na imagem
- Trombo na coronariografia
^ 4ª Definição Universal de IAM 2018
@C 🔢 Tipos de IAM?
| Tipo | Mecanismo
| 1 | Ruptura de placa com trombo
| 2 | Desequilíbrio oferta/demanda (anemia, taquiarritmia, choque)
| 3 | Morte súbita antes da troponina
| 4a | Relacionado à ICP
| 5 | Relacionado à cirurgia de revascularização
! Lesão miocárdica ≠ IAM: troponina alta **sem** isquemia (sepse, miocardite, TEP).
^ 4ª Definição Universal 2018
@C 📍 Parede do IAM e derivações com supra de ST?
| Parede | Derivações | Artéria provável
| Anterior | V1–V4 | DA
| Lateral | D1, aVL, V5–V6 | Circunflexa/diagonal
| Inferior | D2, D3, aVF | Coronária direita (80%)
| VD | V3R, V4R | CD proximal
| Posterior | Infra V1–V3 (supra V7–V9) | Cx ou CD
^ Diretriz de ECG SBC
% cmp Parede do IAM no ECG :: Anterior = V1–V4 · descendente anterior | Lateral = D1, aVL, V5–V6 · circunflexa | Inferior = D2, D3, aVF · coronária direita | VD = V3R–V4R · CD proximal | Posterior = Infra V1–V3 · supra V7–V9
@C ⏱️ Metas de tempo no IAM com supra de ST?
| Meta | Tempo
| Primeiro contato médico → ECG | ≤ 10 min
| Porta-balão (hospital com hemodinâmica) | ≤ 60 min
| Contato → ICP (com transferência) | ≤ 120 min
| Se não for possível: porta-agulha | ≤ 10–30 min
| ICP após trombólise (fármaco-invasiva) | 2–24 h
^ ESC 2023 SCA
% flow Reperfusão no IAMCSST :: ECG em até 10 min do primeiro contato >> ICP primária possível em até 120 min? Sim: ICP primária >> Não: fibrinólise em até 10–30 min >> Coronariografia em 2–24 h (ou resgate imediato se falha)
@C 🚫 Contraindicações absolutas à fibrinólise?
- AVC hemorrágico prévio em qualquer época
- AVC isquêmico nos últimos **6 meses**
- Neoplasia ou malformação do SNC
- TCE ou cirurgia maior nas últimas 3 semanas
- Sangramento ativo (exceto menstruação), dissecção aórtica
- Punções não compressíveis nas últimas 24 h
^ ESC 2023
@C 🩸 Dupla antiagregação após SCA: escolha do inibidor P2Y12?
- **Ticagrelor** ou **prasugrel** preferidos ao clopidogrel
- Prasugrel: !!contraindicado com AVC/AIT prévio!!; cautela > 75 anos e < 60 kg
- Clopidogrel: com anticoagulação oral ou alto risco de sangramento
= Duração padrão: **12 meses**.
^ PLATO 2009; TRITON 2007; ESC 2023
@C 💊 Medicações na alta pós-IAM?
- **AAS** + inibidor P2Y12 (12 meses)
- **Estatina** de alta intensidade (LDL < 55)
- **Betabloqueador** (sobretudo se FEVE ≤ 40%)
- **IECA/BRA** (FEVE ≤ 40%, DM, HAS, DRC)
- Eplerenona se FEVE ≤ 40% com IC ou DM
- Reabilitação cardíaca
! REDUCE-AMI: betabloqueador sem benefício com FEVE preservada.
^ ESC 2023; REDUCE-AMI 2024
@C ⚠️ Complicações mecânicas do IAM e quando aparecem?
| Complicação | Achado
| Ruptura de músculo papilar | IM aguda, EAP, sopro sistólico (inferior)
| Comunicação interventricular | Sopro holossistólico, frêmito, salto de O₂ no VD
| Ruptura de parede livre | Tamponamento, AESP
| Aneurisma de VE | Supra persistente, trombo, IC
= Geralmente **3–5 dias** após o IAM (pico 24 h a 7 dias).
^ ESC 2023
@C 🧠 Síndrome de Dressler?
= Pericardite autoimune **semanas** após IAM ou cirurgia cardíaca.
= Febre, dor pleurítica, atrito, derrame.
- Tratamento: AAS em dose alta + colchicina (evitar outros AINE e corticoide precoce pós-IAM)
^ ESC 2015 pericárdio
@C 🫀 Angina de Prinzmetal (vasoespástica)?
- Dor em **repouso**, madrugada, supra transitório de ST
- Jovens, tabagistas, cocaína
- Tratamento: **BCC** e nitrato
! Betabloqueador não seletivo pode piorar (alfa sem oposição).
^ ESC 2019
@C 👩 MINOCA: o que é e causas?
= IAM com coronárias **sem obstrução ≥ 50%**.
- Ruptura/erosão de placa, vasoespasmo, dissecção espontânea (SCAD)
- Embolia coronariana, Takotsubo e miocardite (diagnósticos diferenciais)
= Ressonância cardíaca é o exame-chave.
^ AHA 2019 MINOCA
@C 🎈 Takotsubo?
- Mulheres pós-menopausa, estresse físico ou emocional
- **Balonamento apical** com contração basal preservada
- Coronárias sem obstrução; recuperação em semanas
! Pode cursar com obstrução de via de saída: evitar inotrópico.
^ InterTAK 2018
@C 🎲 Escores de risco na SCA sem supra?
| Escore | Uso
| GRACE | Mortalidade; > 140 = alto risco (invasivo < 24 h)
| TIMI | 7 itens, prognóstico
| HEART | Dor torácica no PS (alta precoce se baixo risco)
| CRUSADE | Risco de sangramento
^ ESC 2023
@D 🧭 Eixo elétrico pelo método de D1 e aVF?
| D1 | aVF | Eixo
| + | + | Normal (0 a +90°)
| + | − | Desvio à esquerda (confirmar com D2)
| − | + | Desvio à direita
| − | − | Desvio extremo
^ Diretriz de ECG SBC
@D 🧱 Bloqueios atrioventriculares: diferenças?
| Tipo | Achado | Local
| 1º grau | PR > 200 ms | Nodal
| 2º Mobitz I | PR alonga até falhar | Nodal, benigno
| 2º Mobitz II | PR fixo e falha súbita | Infranodal → MP
| 2:1 | Indeterminado | Avaliar QRS
| 3º grau | Dissociação AV | MP
^ Diretriz de ECG SBC
% zones Bloqueios atrioventriculares :: 1º grau = PR > 200 ms, todos conduzem | Mobitz I = PR alonga até onda P bloqueada | Mobitz II = PR fixo, bloqueio súbito, infranodal | BAV total = Dissociação AV, escape
@D ⚡ BRD × BRE no ECG?
| | BRD | BRE
| QRS | ≥ 120 ms | ≥ 120 ms
| V1 | **rSR'** ("orelha de coelho") | QS ou rS largo
| V6/D1 | S empastada | R larga, entalhada, sem q
| Significado | Pode ser normal | Quase sempre doença estrutural
! BRE novo com dor torácica: aplicar critérios de **Sgarbossa**.
^ Diretriz de ECG SBC
@D 🫀 Critérios de Sgarbossa (IAM com BRE)?
| Critério | Pontos
| Supra de ST ≥ 1 mm concordante com QRS | 5
| Infra de ST ≥ 1 mm em V1–V3 | 3
| Supra de ST ≥ 5 mm discordante | 2
= ≥ 3 pontos: alta especificidade para IAM.
! Smith modificado: supra discordante / profundidade da S ≥ 25%.
^ Sgarbossa 1996; Smith 2012
@D 🌀 FA: controle de ritmo × frequência?
= EAST-AFNET 4: controle de **ritmo precoce** (< 1 ano do diagnóstico) reduziu eventos CV.
- Frequência: alvo FC repouso **< 110** (RACE II) no assintomático
- Ritmo: sintomáticos, FA recente, IC por taquicardiomiopatia
! Ablação na ICFEr reduziu mortalidade (CASTLE-AF).
^ EAST-AFNET 4 2020; ESC 2024
@D 🧮 Escore CHA₂DS₂-VA (ESC 2024)?
| Fator | Pontos
| IC | 1
| HAS | 1
| Idade ≥ 75 | 2
| DM | 1
| AVC/AIT/embolia | 2
| Doença vascular | 1
| Idade 65–74 | 1
= ≥ 2: anticoagular; 1: considerar.
! ESC 2024 retirou o sexo feminino do escore (CHA₂DS₂-VA).
^ ESC 2024 FA
@D 💊 DOAC na FA: quando NÃO usar?
- **Estenose mitral moderada a grave**
- **Prótese valvar mecânica**
- SAF tripla positiva
- TFG < 15 (maioria)
= Nesses casos: **varfarina**.
! Bioprótese e outras valvopatias: DOAC permitido.
^ ESC 2024; RE-ALIGN 2013
@D 💊 Ajuste de dose dos DOAC na FA?
| Droga | Dose reduzida quando
| Apixabana 2,5 mg 12/12 h | 2 de 3: idade ≥ 80, peso ≤ 60 kg, creatinina ≥ 1,5
| Rivaroxabana 15 mg/dia | ClCr 15–49
| Dabigatrana 110 mg 12/12 h | Idade ≥ 80, risco de sangramento
| Edoxabana 30 mg/dia | ClCr 15–50, peso ≤ 60 kg, inibidor de P-gp
! Dabigatrana: evitar ClCr < 30.
^ ESC 2024
@D ⚡ Cardioversão de FA e anticoagulação?
- FA < 48 h (e baixo risco): cardioverter com anticoagulação iniciada
- FA ≥ 48 h ou incerta: **3 semanas** de anticoagulação antes, ou ETE sem trombo
- Após: anticoagular **4 semanas** no mínimo (longo prazo conforme escore)
! ESC 2024 sugere preferir ≤ 24 h para dispensar o pré-tratamento.
^ ESC 2024
% flow Cardioversão eletiva da FA :: Instável? Cardioversão elétrica imediata >> Estável: duração < 24–48 h? Cardioverter com anticoagulação >> ≥ 48 h ou incerta: 3 semanas de anticoagulação OU ETE sem trombo >> Após: anticoagular ≥ 4 semanas
@D 🔁 Flutter atrial típico?
= Macrorreentrada **cavotricuspídea**; ondas F em "dente de serra" em D2, D3, aVF; frequência atrial ~300, condução 2:1 (FC ~150).
- **Ablação** é curativa (> 90%)
- Anticoagulação igual à FA
^ ESC 2019 TSV
@D ⚡ Síndrome de Wolff-Parkinson-White?
- PR curto, **onda delta**, QRS alargado
- FA pré-excitada: QRS largo irregular e rápido
- !!Evitar adenosina, BCC, betabloqueador, digoxina!! na FA pré-excitada
- Tratar com **procainamida** ou cardioversão; ablação definitiva
^ ESC 2019 TSV
@D 🔢 QT longo: causas e risco?
= QTc > 450 ms (homem) / > 460 ms (mulher); **> 500 ms** = alto risco de torsades.
- Drogas: macrolídeos, quinolonas, haloperidol, ondansetrona, metadona, amiodarona
- Hipocalemia, hipomagnesemia, hipocalcemia
- Congênito
= Torsades: **sulfato de magnésio 2 g IV**.
^ AHA 2010; CredibleMeds
@D 💓 Síncope: sinais de alto risco?
- Síncope ao **esforço** ou deitado
- Palpitação precedendo
- Cardiopatia estrutural, IC, FEVE baixa
- ECG alterado: BAV Mobitz II/total, QT longo, Brugada, pré-excitação
- História familiar de morte súbita
= Alto risco → internar e monitorizar.
^ ESC 2018 síncope
@D 🫀 Indicações de marca-passo definitivo?
- BAV total ou 2º grau Mobitz II (sem causa reversível)
- Doença do nó sinusal **sintomática**
- BAV 2:1 infranodal
- Bloqueio alternante de ramo
! Excluir causas reversíveis: hipercalemia, drogas (betabloqueador, digoxina), IAM inferior, Lyme.
^ ESC 2021 marca-passo
"""
