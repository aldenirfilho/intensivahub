TXT = r"""
@A 🎗️ Rastreamento de câncer de mama no Brasil?
= Ministério da Saúde/INCA: mamografia **bienal 50–69 anos**; desde 2025 o SUS garante acesso a partir dos **40 anos** sob demanda.
= SBM/CBR/FEBRASGO: anual a partir dos 40 anos.
= Alto risco (BRCA, radioterapia torácica jovem): RM + mamografia anual a partir de 25–30 anos.
^ INCA; Ministério da Saúde 2025; SBM 2023
@A 🎗️ Rastreamento de câncer de colo uterino?
= SUS: citologia **25–64 anos**, a cada 3 anos após 2 normais anuais; transição para **teste de DNA-HPV** a cada 5 anos.
- Imunossuprimidas: início após início da vida sexual, anual
- Não rastrear < 25 anos nem histerectomia total por doença benigna
^ INCA 2016; Diretriz HPV 2024
@A 🎗️ Câncer de próstata: rastreamento?
= **Decisão compartilhada** 55–69 anos (USPSTF); Ministério da Saúde/INCA não recomendam rastreio populacional.
- PSA ± toque retal
- Benefício pequeno, risco de sobrediagnóstico e sobretratamento
^ USPSTF 2018; INCA
@A 🧬 Síndromes hereditárias de câncer?
| Síndrome | Gene | Tumores
| Mama-ovário hereditário | **BRCA1/2** | Mama, ovário, próstata, pâncreas
| Lynch | **MLH1, MSH2, MSH6, PMS2** | Colorretal (direito), endométrio, ovário, estômago
| Polipose adenomatosa familiar | **APC** | Centenas de pólipos, colorretal ~100%
| Li-Fraumeni | **TP53** | Sarcoma, mama, cérebro, adrenal
^ NCCN 2025
% cmp Síndromes hereditárias de câncer :: BRCA1/2 = Mama, ovário, próstata, pâncreas | Lynch = Colorretal direito, endométrio, ovário | PAF (APC) = Centenas de pólipos, colorretal ~100% | Li-Fraumeni (TP53) = Sarcoma, mama, SNC, adrenal
@A 🧪 Critérios de Amsterdam II (Lynch)? Regra 3-2-1
- **3** familiares com câncer associado a Lynch (1 deles parente de 1º grau dos outros 2)
- **2** gerações sucessivas
- **1** diagnosticado antes dos **50 anos**
- PAF excluída
^ Amsterdam II 1999
@A 🚬 Fatores de risco evitáveis de câncer?
- **Tabaco** (principal)
- Álcool, obesidade, sedentarismo
- Infecções: **HPV** (colo, orofaringe), **HBV/HCV** (fígado), **H. pylori** (estômago), EBV, HTLV-1
- Radiação UV, carnes processadas
^ OMS/IARC
@B 🫃 Câncer colorretal: lado direito × esquerdo?
| | Direito | Esquerdo
| Apresentação | **Anemia ferropriva**, massa | Alteração do hábito intestinal, obstrução, sangue vivo
| Biologia | MSI-H, BRAF | KRAS, melhor prognóstico
^ NCCN 2025
@B 🎗️ CEA: utilidade?
= **Seguimento** pós-tratamento do câncer colorretal (recidiva).
! Não serve para rastreio: eleva em tabagistas, cirrose, DII.
^ ASCO
@B 🫁 Estadiamento do câncer de pulmão de pequenas células?
| Limitado | Extenso
| Um hemitórax, um campo de radioterapia | Além de um campo
| Quimiorradioterapia | Quimioimunoterapia
= Muito sensível à quimioterapia, mas recidiva precoce; metástase cerebral frequente.
^ NCCN 2025
@B 🧪 Câncer de testículo: marcadores?
| Tipo | Marcador
| Seminoma puro | **β-hCG** pode subir; **AFP normal**
| Não seminomatoso | **AFP** e/ou β-hCG
| Todos | LDH (carga tumoral)
! AFP elevada exclui seminoma puro.
^ NCCN 2025
@B 🎗️ Câncer de ovário?
- Sintomas vagos: distensão, saciedade precoce, dor pélvica
- **CA-125** (seguimento; elevado também em endometriose, ascite)
- BRCA: testagem para todas com carcinoma epitelial
= Inibidores de PARP na manutenção.
^ NCCN 2025
@B 🧪 Carcinoma renal: tríade clássica e paraneoplásicas?
= Hematúria + dor lombar + massa (rara completa).
- **Policitemia** (EPO), hipercalcemia (PTHrp), HAS (renina)
- Disfunção hepática sem metástase (Stauffer)
- **Varicocele** à esquerda que não esvazia deitado
^ Revisões
@B 🧪 Tumores neuroendócrinos/carcinoide?
- Síndrome carcinoide: **flushing**, diarreia, broncoespasmo, valvopatia direita
- Geralmente com **metástase hepática** (escapa do metabolismo hepático)
- **5-HIAA urinário** elevado; cromogranina A
= Análogos de somatostatina.
^ ENETS
@C 🧠 Síndromes paraneoplásicas e tumores associados?
| Síndrome | Tumor típico
| SIADH | Pequenas células
| Cushing ectópico | Pequenas células, carcinoide
| Hipercalcemia (PTHrp) | Escamoso (pulmão, cabeça e pescoço), mama, rim
| Lambert-Eaton | Pequenas células
| Dermatomiosite | Ovário, pulmão, TGI
| Policitemia | Rim, fígado, hemangioblastoma
| Acantose nigricans maligna | Gástrico
^ Revisões
% cmp Paraneoplásicas: tumor típico :: SIADH / Cushing / Lambert-Eaton = Pequenas células | Hipercalcemia PTHrp = Escamoso de pulmão | Dermatomiosite = Ovário, pulmão, TGI | Policitemia = Carcinoma renal, hepatocarcinoma
@C 🦠 Trousseau: síndrome?
= **Tromboflebite migratória** associada a adenocarcinoma (pâncreas, estômago, pulmão).
= Tratamento com **HBPM** (resistente à varfarina).
^ Revisões
@C 🧪 Marcadores tumorais: associação?
| Marcador | Tumor
| CEA | Colorretal (seguimento)
| CA 19-9 | Pâncreas, vias biliares
| CA-125 | Ovário
| CA 15-3 | Mama
| AFP | Hepatocarcinoma, testículo não seminoma
| β-hCG | Testículo, coriocarcinoma
| PSA | Próstata
^ ASCO
@C 🔎 Metástase de sítio primário desconhecido: abordagem?
- Biópsia com **imuno-histoquímica** (CK7/CK20, TTF-1, PSA)
- TC de tórax, abdome e pelve; mamografia; PSA
- Identificar subgrupos tratáveis (linfoma, germinativo, mama, próstata)
^ ESMO 2023
@D 🧊 Neutropenia febril: definição e escore de risco?
= Neutrófilos **< 500** (ou < 1.000 com queda prevista) + T ≥ 38,3 °C ou ≥ 38 °C por 1 h.
= **MASCC ≥ 21**: baixo risco → tratamento oral ambulatorial possível (amoxicilina-clavulanato + ciprofloxacino).
= Alto risco: **cefepima/piperacilina-tazobactam IV em até 1 h**.
^ IDSA 2010; ASCO 2018
% flow Neutropenia febril :: Neutrófilos < 500 + febre ≥ 38,3 °C >> Hemoculturas e escore MASCC >> Alto risco: cefepima ou piperacilina-tazobactam IV em até 1 hora >> Baixo risco (MASCC ≥ 21): via oral ambulatorial possível
@D 🔥 Síndrome de lise tumoral: critérios laboratoriais (Cairo-Bishop)?
= ≥ 2 em até 3 dias antes ou 7 após a quimioterapia:
- **Ácido úrico** ≥ 8
- **Potássio** ≥ 6
- **Fósforo** ≥ 4,5
- **Cálcio** ≤ 7 (cai)
= Clínica: LRA, arritmia, convulsão.
^ Cairo-Bishop 2004
% cmp Lise tumoral: tétrade laboratorial :: Ácido úrico = Sobe (≥ 8) | Potássio = Sobe (≥ 6) | Fósforo = Sobe (≥ 4,5) | Cálcio = CAI (≤ 7)
@D 🦴 Compressão medular metastática?
- Dor dorsal que **piora deitado**, depois déficit motor, sensitivo, esfíncteres
- **RM de toda a coluna** urgente
- **Dexametasona** imediata
- Radioterapia ± cirurgia descompressiva
^ NICE 2023
% flow Compressão medular metastática :: Dor dorsal que piora deitado em paciente oncológico >> Dexametasona imediata >> RM de toda a coluna com urgência >> Radioterapia ± cirurgia descompressiva
@D 🫀 Síndrome de veia cava superior?
- Edema facial e de MMSS, pletora, circulação colateral
- Causas: câncer de pulmão (pequenas células), linfoma, trombose de cateter
= Obter **histologia** antes do corticoide (linfoma); **stent** para alívio rápido.
^ Revisões
@D 🧠 Metástases cerebrais: manejo inicial?
- **Dexametasona** se edema sintomático
- Anticonvulsivante só se crise (não profilático)
- Radiocirurgia, radioterapia, ressecção conforme número/tamanho
^ ASCO/SNO 2022
@E 💊 Imunoterapia (checkpoint): eventos adversos imunomediados?
- **Colite**, **hepatite**, **pneumonite**
- Endócrinos: **hipofisite**, tireoidite, insuficiência adrenal, **DM1 fulminante**
- Miocardite (rara e grave), nefrite, rash
= Grau ≥ 2: suspender e **corticoide**; endocrinopatias: reposição hormonal.
^ ASCO 2021
@E 🤢 Náusea e vômito por quimioterapia: profilaxia?
| Risco emético | Profilaxia
| Alto (cisplatina) | **Antagonista 5-HT3 + NK1 (aprepitanto) + dexametasona + olanzapina**
| Moderado | 5-HT3 + dexametasona (± NK1)
| Baixo | Dexametasona ou 5-HT3
^ ASCO 2020
@E 🫀 Cardiotoxicidade dos quimioterápicos?
| Droga | Efeito
| **Antraciclinas** (doxorrubicina) | Cardiomiopatia **dose-dependente**, irreversível
| **Trastuzumabe** | Disfunção **reversível**, não dose-dependente
| 5-FU/capecitabina | Vasoespasmo coronariano
| Inibidores de checkpoint | Miocardite
^ ESC 2022 cardio-oncologia
@E 💊 Toxicidades clássicas de quimioterápicos?
| Droga | Toxicidade
| Cisplatina | **Nefrotoxicidade**, ototoxicidade, hipomagnesemia
| Ciclofosfamida/ifosfamida | **Cistite hemorrágica** (mesna)
| Bleomicina | **Fibrose pulmonar**
| Vincristina | **Neuropatia**, SIADH
| Metotrexato | Mucosite, mielotoxicidade (resgate com ácido folínico)
| Oxaliplatina | Neuropatia ao frio
^ Farmacologia oncológica
@E 🦷 Mucosite e hipercalcemia: manejo resumido?
= Mucosite: higiene oral, crioterapia, analgesia.
= Hipercalcemia da malignidade: **soro + calcitonina + zoledronato** (ou denosumabe na DRC).
^ MASCC; Revisões
@E 🩸 Fatores de crescimento (G-CSF): quando?
= Profilaxia primária se risco de neutropenia febril **≥ 20%** pelo esquema (ou 10–20% com fatores do paciente).
^ ASCO 2015
"""
