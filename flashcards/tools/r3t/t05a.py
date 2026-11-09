TXT = r"""
@A 🔥 DRGE: sinais de alarme que indicam EDA?
- **Disfagia**, odinofagia
- Perda de peso, anemia, sangramento
- Vômitos persistentes, massa
- Início > 50–60 anos
= Sem alarme: teste terapêutico com **IBP 8 semanas**.
^ ACG 2022
@A 🧪 Esôfago de Barrett: definição e vigilância?
= Metaplasia **intestinal** (colunar com células caliciformes) ≥ 1 cm acima da JEG.
| Achado | EDA de controle
| Sem displasia | 3–5 anos
| Displasia de baixo grau | Ablação endoscópica ou 12 meses
| Displasia de alto grau | **Ressecção/ablação endoscópica**
^ ACG 2022
@A 🌀 Acalasia: diagnóstico?
- Disfagia para **sólidos e líquidos** desde o início
- Esofagograma: "**bico de pássaro**"
- **Manometria de alta resolução** (padrão-ouro): relaxamento do EEI ausente, aperistalse
- EDA para excluir pseudoacalasia (tumor de cárdia)
= No Brasil: lembrar **Chagas** (megaesôfago).
^ ACG 2020
@A 🍽️ Disfagia orofaríngea × esofágica?
| | Orofaríngea | Esofágica
| Queixa | Dificuldade de iniciar, tosse, regurgitação nasal | "Entala" após engolir
| Causas | AVC, Parkinson, miastenia, ELA | Anel, estenose, acalasia, câncer
| Exame | Videodeglutograma | EDA
^ WGO
@A 🌾 Esofagite eosinofílica?
- Jovem atópico, **impactação alimentar**, disfagia
- EDA: anéis, sulcos longitudinais, exsudato
- Biópsia: **≥ 15 eosinófilos/campo**
= Tratamento: IBP, budesonida deglutida, dieta de eliminação, dupilumabe.
^ AGA 2020
@A 🦠 H. pylori: quem testar?
- Úlcera péptica ativa ou prévia
- Linfoma MALT, câncer gástrico precoce ressecado
- Dispepsia não investigada (< 60 anos)
- Uso crônico de AAS/AINE, anemia ferropriva inexplicada, PTI
- Familiar de 1º grau com câncer gástrico
^ Maastricht VI 2022
@A 💊 Erradicação do H. pylori: esquemas?
- **Quádrupla com bismuto** (IBP + bismuto + tetraciclina + metronidazol) 14 dias — preferível em resistência alta
- Tripla (IBP + amoxicilina + claritromicina) 14 dias onde resistência à claritromicina < 15%
- Controle de cura: **teste respiratório** ou antígeno fecal ≥ 4 semanas após ATB (IBP suspenso 2 semanas)
^ Maastricht VI 2022; IV Consenso Brasileiro
% flow Erradicação do H. pylori :: Indicação confirmada (úlcera, MALT, dispepsia, AAS crônico) >> Quádrupla com bismuto por 14 dias (ou tripla se baixa resistência) >> Suspender IBP 2 semanas e antibiótico 4 semanas >> Controle de cura: teste respiratório ou antígeno fecal
@A 🩹 Úlcera péptica: quando suspeitar de Zollinger-Ellison?
- Úlceras **múltiplas, refratárias**, em locais atípicos (jejuno)
- **Diarreia** associada
- NEM-1
= Gastrina elevada com pH gástrico ácido (suspender IBP).
^ Revisões
@A 🎯 Dispepsia funcional: critérios de Roma IV?
= ≥ 1: plenitude pós-prandial, saciedade precoce, dor ou queimação epigástrica; sem lesão estrutural na EDA; sintomas por 3 meses com início há ≥ 6.
- Tratamento: testar/tratar H. pylori, IBP, tricíclico em dose baixa, procinético
^ Roma IV 2016
@B 🩸 Escore de Glasgow-Blatchford?
= Ureia, Hb, PAS, FC, melena, síncope, hepatopatia e IC.
= **0–1**: baixo risco → manejo ambulatorial com EDA eletiva.
^ ESGE 2021
@B ⏱️ HDA não varicosa: tempo da endoscopia?
- Em até **24 h** após ressuscitação (alto risco)
- EDA < 6 h **não** reduziu mortalidade (Lau NEJM 2020)
- IBP IV em bolus antes da EDA pode reduzir estigmas
- Eritromicina IV 30–120 min antes melhora a visualização
^ ESGE 2021; Lau 2020
@B 🔍 Classificação de Forrest e conduta?
| Forrest | Achado | Risco de ressangramento | Terapia endoscópica
| Ia | Sangramento em jato | Alto | Sim
| Ib | Em porejamento | Alto | Sim
| IIa | Vaso visível | Alto | Sim
| IIb | Coágulo aderido | Intermediário | Considerar
| IIc | Hematina | Baixo | Não
| III | Base limpa | Baixo | Não
^ ESGE 2021
% zones Classificação de Forrest :: Ia = Sangramento em jato | Ib = Porejamento | IIa = Vaso visível | IIb = Coágulo aderido | IIc = Hematina plana | III = Base limpa
@B 🍷 Mallory-Weiss?
= Laceração na junção esofagogástrica após **vômitos** intensos (etilismo).
= Geralmente autolimitado; terapia endoscópica se sangramento ativo.
! Boerhaave: ruptura **transmural** com mediastinite (enfisema, sinal de Hamman) — emergência cirúrgica.
^ Revisões
@B 🔴 Hemorragia digestiva baixa: abordagem?
- Excluir HDA (ureia alta, instabilidade → EDA)
- Estável: **colonoscopia** após preparo em 24 h
- Instável: **angio-TC** → embolização
= Causas: diverticulose (mais comum em idosos), angiodisplasia, colite isquêmica, neoplasia, hemorroidas.
^ ACG 2023
% flow Hemorragia digestiva baixa :: Excluir HDA (ureia alta, instabilidade: EDA) >> Estável: colonoscopia em até 24 h após preparo >> Instável: angio-TC >> Sangramento ativo na angio-TC: embolização
@B 🕳️ Sangramento obscuro: próximos passos?
= EDA e colonoscopia negativas → **cápsula endoscópica** (ou enteroscopia, angio-TC).
- Angiodisplasias (estenose aórtica: síndrome de Heyde)
- Divertículo de Meckel em jovens (cintilografia)
^ ACG 2015
@C 🔥 Crohn × retocolite ulcerativa?
| | Crohn | RCU
| Local | Boca ao ânus (íleo terminal) | **Reto** em continuidade
| Lesão | **Transmural**, salteada | Mucosa, contínua
| Fístulas/estenoses | **Sim** | Não
| Granulomas | Sim | Não
| Tabagismo | Piora | "Protege"
| Anticorpo | ASCA | p-ANCA
^ ACG 2018/2025
% cmp Doença de Crohn × retocolite ulcerativa :: Crohn = Transmural, salteada, íleo terminal, fístulas, granulomas, tabagismo piora | RCU = Mucosa, contínua desde o reto, sangue nas fezes, p-ANCA, tabagismo protege
@C 🔥 RCU grave: critérios de Truelove-Witts?
= ≥ 6 evacuações sanguinolentas/dia + ≥ 1:
- FC > 90
- Temperatura > 37,8 °C
- Hb < 10,5
- VHS > 30
= Internar, corticoide IV, profilaxia de TEV; resgate no D3–5 (infliximabe/ciclosporina).
^ Truelove 1955; ECCO 2022
@C 🧪 Antes de iniciar biológico/imunossupressor na DII?
- Rastrear **TB latente** (PPD/IGRA + RX)
- Hepatite B (HBsAg, anti-HBc), hepatite C, HIV
- Vacinas inativadas em dia; vivas antes
- TPMT antes de azatioprina
^ ECCO 2021
@C 🌾 Doença celíaca: diagnóstico?
- **Anti-transglutaminase IgA** + IgA total
- Confirmação: **biópsia duodenal** (atrofia vilositária, Marsh)
- Fazer **com glúten** na dieta
= Associações: DM1, tireoidite, Down, dermatite herpetiforme, osteoporose.
^ ACG 2023
@C 💩 Diarreia crônica: inflamatória × osmótica × secretora?
| Tipo | Pistas
| Osmótica | Melhora em jejum, gap osmolar fecal > 125
| Secretora | Persiste em jejum, noturna, gap < 50
| Inflamatória | Sangue, leucócitos, **calprotectina ↑**
| Disabsortiva | Esteatorreia, perda de peso
^ AGA 2019
@C 🦠 Clostridioides difficile: tratamento?
| Episódio | Tratamento
| 1º não grave/grave | **Fidaxomicina** ou vancomicina oral 10 dias
| Fulminante | Vancomicina oral 500 mg 6/6 h + metronidazol IV ± retal
| Recorrência | Fidaxomicina, bezlotoxumabe, **transplante fecal**
= Grave: leucócitos > 15 mil ou creatinina > 1,5.
^ IDSA/SHEA 2021
@C 🩸 Colite isquêmica?
- Idoso, dor abdominal leve seguida de **hematoquezia**
- Áreas de "watershed": **flexura esplênica** e retossigmoide
- Maioria autolimitada
! Isquemia mesentérica aguda: dor **desproporcional** ao exame, FA, lactato alto → angio-TC.
^ ACG 2015"""
