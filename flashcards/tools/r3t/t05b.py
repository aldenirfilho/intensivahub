TXT = r"""
@D 🥃 Pancreatite aguda: critérios diagnósticos?
= 2 de 3:
- Dor epigástrica típica (em faixa, para dorso)
- **Lipase ou amilase ≥ 3× LSN**
- Imagem característica
! TC precoce não é rotina: indicar só se dúvida diagnóstica ou piora após 72 h.
^ Atlanta revisada 2012; ACG 2024
@D 📊 Gravidade da pancreatite (Atlanta revisada)?
| Gravidade | Critério
| Leve | Sem falência orgânica nem complicação
| Moderada | Falência **transitória** (< 48 h) ou complicação local
| Grave | Falência orgânica **persistente** (> 48 h)
^ Atlanta revisada 2012
% zones Gravidade da pancreatite aguda (Atlanta) :: Leve = Sem falência orgânica | Moderada = Falência < 48 h ou complicação local | Grave = Falência orgânica > 48 h
@D 🫧 Coleções na pancreatite?
| < 4 semanas | > 4 semanas
| Coleção fluida aguda | **Pseudocisto** (com parede)
| Coleção necrótica aguda | **Necrose encapsulada (WON)**
= Necrose infectada (gás na TC, piora): ATB + drenagem **postergada** (step-up, ≥ 4 semanas).
^ Atlanta 2012; PANTER 2010
@D 🍺 Pancreatite crônica: tríade e tratamento?
= Dor abdominal + **esteatorreia** + **diabetes**; calcificações pancreáticas.
- Cessar álcool e tabaco
- Reposição de **enzimas pancreáticas** com as refeições
- Analgesia escalonada; tratar DM pancreatogênico
^ ACG 2020
@D 🟡 Colelitíase sintomática × assintomática?
- **Assintomática**: geralmente não operar
- Exceções: vesícula em porcelana, cálculo > 3 cm, pólipo ≥ 10 mm, anemia falciforme
- Cólica biliar: **colecistectomia** eletiva
^ SAGES; EASL 2016
@D 🌡️ Colangite aguda: critérios (Tokyo)?
= Tríade de **Charcot**: febre + icterícia + dor em hipocôndrio direito.
= Pêntade de **Reynolds**: + hipotensão + confusão.
- Tratamento: ATB + **drenagem biliar** (CPRE); urgência no grau III
^ Tokyo Guidelines 2018
% flow Colangite aguda (Tokyo 2018) :: Suspeita: febre, icterícia, dor (Charcot) >> Hemoculturas e antibiótico >> Graduar gravidade I, II ou III >> Drenagem biliar: urgente no grau III, precoce no II
@D 🔍 Coledocolitíase: probabilidade e conduta?
| Risco | Critério | Conduta
| Alto | Colangite, cálculo no colédoco no USG, bilirrubina > 4 com colédoco dilatado | **CPRE**
| Intermediário | Colédoco dilatado, provas alteradas, > 55 anos | **Colangio-RM ou EUS**
| Baixo | Nenhum | Colecistectomia
^ ASGE 2019
% zones Coledocolitíase: risco e conduta :: Baixo = Colecistectomia | Intermediário = Colangio-RM ou ecoendoscopia | Alto = CPRE
@D 🎈 Sinal de Courvoisier-Terrier?
= Vesícula **palpável e indolor** + icterícia → obstrução **neoplásica** distal (cabeça de pâncreas, periampular).
^ Semiologia
@D 🎗️ Câncer de pâncreas: marcador e apresentação?
- Icterícia indolor, perda de peso, dor dorsal, DM de início recente em idoso
- **CA 19-9** (seguimento; falso-positivo na colestase)
- Sinal de Trousseau: tromboflebite migratória
^ NCCN 2025
@E 🦠 Sorologia da hepatite B: interpretação?
| HBsAg | Anti-HBc total | Anti-HBs | Situação
| + | + (IgM) | − | Aguda
| + | + (IgG) | − | **Crônica**
| − | + | + | Curada (imune por infecção)
| − | − | + | **Vacinado**
| − | + | − | Cicatriz isolada/oculta/janela
^ CDC; PCDT Hepatite B 2023
% cmp Sorologia da hepatite B :: HBsAg + anti-HBc IgM = Infecção aguda | HBsAg + anti-HBc IgG = Infecção crônica | Anti-HBc + anti-HBs = Curado | Só anti-HBs = Vacinado
@E 🧪 Hepatite C: diagnóstico e tratamento?
- Rastreio: **anti-HCV**; confirmação: **HCV-RNA**
- DAA pangenotípicos: **sofosbuvir + velpatasvir** 12 semanas ou glecaprevir + pibrentasvir 8 semanas
- Cura (RVS12) > 95%
! Antes do DAA: pesquisar HBV (risco de reativação).
^ PCDT Hepatite C 2023
@E 🍷 Hepatite alcoólica: gravidade e tratamento?
- AST/ALT **> 1,5–2**, AST < 400, icterícia, febre, leucocitose
- **Maddrey ≥ 32** ou MELD > 20: grave
- **Prednisolona 40 mg** por 28 dias (Lille no D7 < 0,45 = resposta)
! Excluir infecção e sangramento antes do corticoide.
^ AASLD 2019; STOPAH 2015
@E 🧬 Hemocromatose hereditária?
- **Saturação de transferrina > 45%** e ferritina alta
- Mutação **C282Y** homozigota (HFE)
- Cirrose, DM ("diabetes bronzeado"), artropatia (2ª e 3ª MCF), cardiomiopatia, hipogonadismo
= Tratamento: **flebotomias** (alvo ferritina 50–100).
^ EASL 2022
@E 🟢 Doença de Wilson?
- Jovem com hepatopatia + sintomas **neuropsiquiátricos**
- **Anel de Kayser-Fleischer**
- Ceruloplasmina baixa, cobre urinário 24 h alto
- Hepatite fulminante com hemólise e **fosfatase alcalina baixa**
= Quelantes (penicilamina, trientina) e zinco.
^ AASLD 2022
@E 🔬 Padrões de lesão hepática pelo fator R?
= **R = (ALT/LSN) ÷ (FA/LSN)**
| R | Padrão
| ≥ 5 | Hepatocelular
| 2–5 | Misto
| ≤ 2 | Colestático
^ DILI ACG 2021
% zones Fator R na lesão hepática :: Colestático = R ≤ 2 | Misto = R entre 2 e 5 | Hepatocelular = R ≥ 5
@E ⚖️ Lei de Hy na lesão hepática por drogas?
= ALT > 3× LSN + bilirrubina > 2× LSN (sem colestase) → mortalidade ~10%.
= Drogas: amoxicilina-clavulanato (mais comum), isoniazida, AINE, antiepilépticos.
^ FDA; ACG 2021
@E 🩸 Colangite biliar primária × colangite esclerosante primária?
| | CBP | CEP
| Perfil | Mulher de meia-idade | Homem jovem
| Marcador | **Antimitocôndria** | p-ANCA, colangio-RM em "contas de rosário"
| Associação | Sjögren, tireoidite | **Retocolite ulcerativa**
| Tratamento | Ácido ursodesoxicólico | Sem terapia eficaz; vigilância de colangiocarcinoma
^ EASL 2017/2022
@F 🧮 Child-Pugh: parâmetros?
- **Bilirrubina**
- **Albumina**
- **RNI**
- **Ascite**
- **Encefalopatia**
| Pontos | Classe
| 5–6 | A
| 7–9 | B
| 10–15 | C
^ Child-Pugh
% zones Classificação de Child-Pugh :: Child A = 5–6 pontos | Child B = 7–9 pontos | Child C = 10–15 pontos
@F 💧 Paracentese: GASA (gradiente soro-ascite de albumina)?
| GASA | Proteína no líquido | Causa
| ≥ 1,1 | < 2,5 | **Cirrose**
| ≥ 1,1 | ≥ 2,5 | IC, Budd-Chiari
| < 1,1 | — | Carcinomatose, TB, pancreatite, nefrótica
^ AASLD 2021
@F 🧂 Tratamento da ascite na cirrose?
- Restrição de **sódio** (< 2 g/dia)
- **Espironolactona 100 mg + furosemida 40 mg** (proporção 100:40)
- Ascite tensa: paracentese de grande volume + **albumina 6–8 g/L** retirado (> 5 L)
- Refratária: paracenteses seriadas, **TIPS**, transplante
! Evitar AINE e IECA/BRA na ascite.
^ AASLD 2021
@F 🔁 Profilaxia de PBE?
| Situação | Profilaxia
| HDA na cirrose | **Ceftriaxona** 7 dias
| PBE prévia | Norfloxacino (ou ciprofloxacino) contínuo
| Proteína ascítica < 1,5 + disfunção | Primária (considerar)
^ AASLD 2021
@F 🩸 Profilaxia primária de sangramento varicoso?
= Varizes de médio/grosso calibre ou com sinais vermelhos:
- **Carvedilol** (preferido) ou propranolol
- Ou **ligadura elástica**
= Carvedilol também reduz descompensação (PREDESCI).
^ Baveno VII 2022
@F 🧠 Graus de encefalopatia hepática (West Haven)?
| Grau | Achado
| 1 | Alteração sutil, sono invertido
| 2 | Letargia, desorientação, **asterixe**
| 3 | Sonolência, confusão intensa
| 4 | Coma
^ AASLD/EASL 2014
@F 🏥 MELD: para que serve?
= Prioriza a fila de **transplante hepático** (bilirrubina, RNI, creatinina, ± sódio e albumina no MELD 3.0).
= MELD ≥ 15: considerar avaliação para transplante.
^ UNOS; MELD 3.0 2021
"""
