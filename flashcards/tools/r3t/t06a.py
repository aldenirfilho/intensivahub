TXT = r"""
@A 🔍 Classificação das anemias pelo VCM?
| Microcítica (< 80) | Normocítica | Macrocítica (> 100)
| Ferropriva | Doença crônica | B12/folato (megaloblástica)
| Talassemia | Perda aguda, DRC | Álcool, hepatopatia
| Doença crônica (às vezes) | Hemólise (reticulócitos ↑) | Hipotireoidismo, SMD
| Sideroblástica | Medula (aplasia, infiltração) | Drogas (MTX, hidroxiureia, zidovudina)
^ Harrison
% cmp Anemia pelo VCM :: Microcítica < 80 = Ferropriva, talassemia, doença crônica, sideroblástica | Normocítica = Doença crônica, DRC, perda aguda, hemólise, medula | Macrocítica > 100 = B12, folato, álcool, hipotireoidismo, SMD, drogas
@A 🧪 Ferropriva × anemia de doença crônica?
| | Ferropriva | Doença crônica
| Ferritina | **< 30** | Normal ou **↑**
| Saturação de transferrina | ↓ | ↓
| Transferrina/TIBC | **↑** | ↓
| RDW | ↑ | Normal
! Inflamação: ferritina < 100 com saturação < 20% ainda sugere ferropenia.
^ Harrison
@A 🔁 Ferropriva × talassemia minor?
- **Índice de Mentzer**: VCM/hemácias < 13 sugere talassemia; > 13, ferropriva
- Talassemia: hemácias **normais ou altas**, RDW normal, ferritina normal
- Beta-talassemia minor: **HbA2 > 3,5%** na eletroforese
^ Revisões
@A 🩸 Anemia ferropriva em homem ou mulher pós-menopausa?
= Investigar **trato gastrointestinal**: EDA + colonoscopia (± sorologia de doença celíaca).
^ BSG 2021; AGA 2020
@A 🧠 Deficiência de B12 × folato?
| | B12 | Folato
| Neurológico (degeneração combinada da medula) | **Sim** | Não
| Ácido metilmalônico | **↑** | Normal
| Homocisteína | ↑ | ↑
| Causas | Anemia perniciosa, metformina, IBP, gastrectomia, vegano | Álcool, má nutrição, gestação, MTX
^ BMJ 2014
@A 💉 Reposição de B12: oral ou parenteral?
= Oral em **dose alta** (1.000–2.000 µg/dia) é eficaz mesmo na anemia perniciosa (absorção passiva ~1%).
= Parenteral: sintomas neurológicos graves, má adesão, má absorção grave.
^ Cochrane 2018
@A 🔢 Índice de reticulócitos: para que serve?
= Reticulócitos corrigidos = % × (Ht/45); dividir por fator de maturação.
| IPR | Interpretação
| > 2–3 | Medula responde: **hemólise ou perda**
| < 2 | **Hipoproliferativa** (deficiência, medula, DRC)
^ Harrison
@A 🦴 Aplasia de medula: diagnóstico e causas?
= Pancitopenia + reticulócitos baixos + **medula hipocelular** (< 25%).
- Idiopática (autoimune), drogas (cloranfenicol, sulfas, anticonvulsivantes), vírus (hepatite, parvovírus B19), HPN
= Tratamento: transplante (jovens) ou ATG + ciclosporina + eltrombopague.
^ BSH 2024
@B 🧪 Anemia hemolítica autoimune quente × fria?
| | Quente (IgG) | Fria (IgM)
| Coombs direto | IgG ± C3 | **C3**
| Causas | Idiopática, LES, LLC, drogas | Mycoplasma, EBV, linfoma
| Esfregaço | Esferócitos | Aglutinação
| Tratamento | **Corticoide**, rituximabe | Evitar frio, rituximabe, sutimlimabe
^ BSH 2017
@B 🌙 Hemoglobinúria paroxística noturna?
- Hemólise intravascular, **trombose em sítios atípicos** (Budd-Chiari, mesentérica)
- Pancitopenia/aplasia
= Diagnóstico: **citometria de fluxo** (perda de CD55/CD59).
= Tratamento: eculizumabe/ravulizumabe.
^ Revisões
@B 🧬 Anemia falciforme: complicações agudas?
- **Crise álgica** vaso-oclusiva
- **Síndrome torácica aguda** (dor torácica, infiltrado, hipoxemia)
- Sequestro esplênico, crise aplásica (parvovírus B19)
- AVC, priapismo
= Hidroxiureia reduz crises e mortalidade.
^ ASH 2020
@B 🫁 Síndrome torácica aguda na falciforme: tratamento?
- O₂, analgesia, incentivo respiratório
- **Antibiótico** (cefalosporina + macrolídeo)
- **Transfusão** simples; exsanguineotransfusão se grave
! Hidratação excessiva piora.
^ ASH 2020
@C 🩸 Plaquetopenia: primeiro passo?
= Excluir **pseudoplaquetopenia** (agregação por EDTA): esfregaço e coleta com citrato.
- Avaliar drogas (heparina, linezolida, sulfas, quinina)
- Esfregaço: esquizócitos (PTT/SHU/CIVD), blastos
^ ASH
@C 🧪 PTI: tratamento de 1ª linha?
= Tratar se plaquetas < 30 mil ou sangramento.
- **Corticoide**: dexametasona 40 mg 4 dias ou prednisona 1 mg/kg
- **IgIV**: resposta rápida (sangramento, pré-operatório)
- 2ª linha: agonistas de trombopoetina (eltrombopague, romiplostim), rituximabe, esplenectomia
^ ASH 2019
@C 🧱 PTT × SHU × CIVD?
| | PTT | SHU típica | CIVD
| Causa | ↓ ADAMTS13 | Shiga toxina (E. coli O157) | Sepse, trauma, câncer, obstetrícia
| Coagulação (TP/TTPa) | **Normal** | Normal | **Alargada**
| Fibrinogênio | Normal | Normal | **↓**
| Rim | Leve | **Grave** | Variável
| Tratamento | Plasmaférese | Suporte | Tratar a causa
^ ISTH; BSH
% cmp Microangiopatias × CIVD :: PTT = ADAMTS13 < 10%, coagulação normal, neurológico. Plasmaférese | SHU típica = Diarreia por Shiga toxina, LRA grave. Suporte | CIVD = TP e TTPa alargados, fibrinogênio baixo. Tratar a causa
@C 🧮 Escore PLASMIC?
= Plaquetas < 30 mil, hemólise, sem câncer ativo, sem transplante, VCM < 90, RNI < 1,5, creatinina < 2,0.
= **6–7 pontos**: alta probabilidade de PTT.
^ Bendapudi 2017
@C ⏱️ TP × TTPa alargados: raciocínio?
| TP | TTPa | Pensar em
| ↑ | Normal | Fator VII, varfarina, hepatopatia inicial, vitamina K
| Normal | ↑ | Heparina, hemofilia (VIII, IX, XI), FvW, anticoagulante lúpico
| ↑ | ↑ | Hepatopatia, CIVD, fatores comuns (X, V, II), anticoagulação excessiva
= **Teste de mistura**: corrige = deficiência; não corrige = inibidor.
^ Revisões
@D 🧮 Escore de Wells para TEP?
| Item | Pontos
| Sinais de TVP | 3
| TEP mais provável que outro diagnóstico | 3
| FC > 100 | 1,5
| Imobilização/cirurgia recente | 1,5
| TVP/TEP prévio | 1,5
| Hemoptise | 1
| Câncer ativo | 1
= ≤ 4: improvável (D-dímero); > 4: provável (angio-TC).
^ Wells 2000; ESC 2019
@D 🧪 D-dímero ajustado à idade?
= > 50 anos: corte = **idade × 10 µg/L** (FEU).
= Aumenta especificidade sem perder segurança (ADJUST-PE).
- Regras de exclusão: PERC (baixa probabilidade), YEARS
^ ADJUST-PE 2014
@D ⏳ Duração da anticoagulação no TEV?
| Situação | Duração
| Fator transitório maior (cirurgia) | **3 meses**
| Fator transitório menor | 3 meses (considerar mais)
| Não provocado | ≥ 3 meses → considerar **estendida**
| Câncer ativo | Enquanto o câncer estiver ativo
| Recorrente sem fator | Indefinida
^ ESC 2019; CHEST 2021
% zones Duração da anticoagulação no TEV :: Fator transitório maior = 3 meses | Não provocado = ≥ 3 meses, considerar estendida | Câncer ativo = Enquanto ativo | Recorrente sem fator = Indefinida
@D 🎗️ TEV associado a câncer: anticoagulante?
= **DOAC** (apixabana, rivaroxabana, edoxabana) ou HBPM.
! Tumores do TGI/urogenital com lesão luminal: preferir apixabana ou HBPM (mais sangramento com edoxabana/rivaroxabana).
^ ASCO 2023; CARAVAGGIO 2020
@D 🤰 Anticoagulação na gestação?
= **HBPM** (enoxaparina): escolha.
! Varfarina: teratogênica (1º trimestre); DOAC contraindicados.
= Prótese mecânica: regime específico (pode usar varfarina no 2º trimestre se dose baixa).
^ ESC 2018 gestação
@D 🔬 Trombofilias: quando pesquisar?
- TEV em **jovem** (< 50) sem fator
- TEV em sítio **incomum** (cerebral, mesentérico)
- Recorrente, história familiar forte
- Perdas gestacionais (SAF)
! Não testar na fase aguda nem em uso de anticoagulante (proteína C/S, antitrombina).
^ BSH 2022
@D 💉 Profilaxia de TEV no paciente clínico internado?
= Escore de **Pádua ≥ 4** (ou IMPROVE) sem alto risco de sangramento → enoxaparina 40 mg/dia ou heparina 5.000 UI 8/8–12/12 h.
= Contraindicação: compressão pneumática intermitente.
^ ASH 2018; CHEST 2012
"""
