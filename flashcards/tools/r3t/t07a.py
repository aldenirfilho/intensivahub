TXT = r"""
@A 💊 Espectro dos β-lactâmicos (resumo)?
| Droga | Cobre bem | Não cobre
| Penicilina/amoxicilina | Estreptococo, enterococo (amoxi) | S. aureus produtor de penicilinase
| Oxacilina/cefazolina | **MSSA** | MRSA, enterococo
| Ceftriaxona | Pneumococo, Gram-negativos comunitários | Pseudomonas, enterococo
| Cefepima | Pseudomonas + Gram-positivos | ESBL (variável), anaeróbios
| Piperacilina-tazobactam | Pseudomonas + anaeróbios | ESBL grave (MERINO)
| Meropeném | **ESBL**, Pseudomonas, anaeróbios | MRSA, KPC
^ Sanford; IDSA 2024
@A 🛡️ Bactérias "ESKAPE" e a droga de escolha?
| Germe | Escolha
| MRSA | Vancomicina, linezolida, daptomicina (não pulmão)
| Enterococo VRE | Linezolida, daptomicina
| ESBL | **Carbapenêmico**
| KPC | Ceftazidima-avibactam, meropeném-vaborbactam
| Acinetobacter | Ampicilina-sulbactam (dose alta), polimixina, cefiderocol
| Pseudomonas DTR | Ceftolozana-tazobactam, ceftazidima-avibactam
^ IDSA 2024
% cmp Resistência bacteriana: droga de escolha :: MRSA = Vancomicina ou linezolida | ESBL = Carbapenêmico | KPC = Ceftazidima-avibactam | Metalo (NDM) = Ceftazidima-avibactam + aztreonam
@A ⚠️ Daptomicina: por que não usar na pneumonia?
= É **inativada pelo surfactante** pulmonar.
- Efeitos: CPK ↑ (miopatia), pneumonia eosinofílica
^ Farmacologia
@A 🧪 Vancomicina: monitorização moderna?
= Alvo **AUC/MIC 400–600** (por software bayesiano), em vez de vale 15–20.
- Nefrotoxicidade aumenta com piperacilina-tazobactam associada
^ ASHP/IDSA 2020
@A 💉 Aminoglicosídeos: toxicidades?
- **Nefrotoxicidade** (NTA, reversível)
- **Ototoxicidade** (irreversível, vestibular/coclear)
- Bloqueio neuromuscular (piora miastenia)
= Dose única diária reduz nefrotoxicidade.
^ Farmacologia
@A ⚡ Fluoroquinolonas: efeitos adversos?
- **Tendinopatia/ruptura** de tendão (idoso, corticoide)
- QT longo, disglicemia
- Aneurisma/dissecção de aorta
- Neuropatia, efeitos no SNC
- C. difficile
= Evitar em infecções simples (cistite, sinusite) se houver alternativa.
^ FDA 2018
@A 🔬 Linezolida: cuidados?
- **Mielossupressão** (plaquetopenia) após 2 semanas
- **Síndrome serotoninérgica** com ISRS (inibe MAO)
- Neuropatia óptica/periférica, acidose láctica
^ Farmacologia
@A 🧾 SMX-TMP: efeitos importantes?
- **Hipercalemia** (efeito amilorida-like)
- ↑ creatinina sem ↓ TFG
- Rash, Stevens-Johnson, mielossupressão
- Potencializa **varfarina**
^ Farmacologia
@A 🧫 Metronidazol: pontos de prova?
- Efeito **dissulfiram** com álcool
- Gosto metálico, neuropatia periférica
- Cobre anaeróbios, Giardia, Trichomonas, ameba
^ Farmacologia
@B 🦠 Agentes de PAC por contexto?
| Contexto | Agente
| Mais comum geral | **Pneumococo**
| Etilista, aspiração | Klebsiella, anaeróbios
| DPOC | H. influenzae, Moraxella
| Pós-influenza | **S. aureus**
| Jovem, sintomas extrapulmonares | Mycoplasma
| Diarreia, hiponatremia | Legionella
^ ATS/IDSA 2019
@B 💊 PAC ambulatorial sem comorbidade?
= **Amoxicilina** 1 g 8/8 h (ou doxiciclina; macrolídeo se resistência local < 25%).
= Com comorbidade: amoxicilina-clavulanato + macrolídeo, ou fluoroquinolona respiratória.
- Duração **5 dias**
^ ATS/IDSA 2019
@B 🏥 Pneumonia hospitalar: definição e tratamento?
= Surge **≥ 48 h** após internação (não estava incubando).
- Sem risco de MDR: piperacilina-tazobactam, cefepima, levofloxacino
- Risco de MDR/choque: dupla cobertura Gram-negativa + MRSA
- Duração **7 dias**
^ IDSA/ATS 2016
@B 👂 Faringite estreptocócica: critérios de Centor?
- Febre > 38 °C
- **Exsudato** tonsilar
- Adenopatia cervical anterior dolorosa
- **Ausência de tosse**
- (McIsaac: idade 3–14 +1; ≥ 45 −1)
= 0–1: sem teste; 2–3: teste rápido; 4: testar/tratar.
= Tratamento: **penicilina benzatina** ou amoxicilina 10 dias.
^ IDSA 2012
@B 🤧 Sinusite aguda bacteriana: quando suspeitar?
- Sintomas > **10 dias** sem melhora
- Quadro grave: febre ≥ 39 °C + secreção purulenta ≥ 3–4 dias
- **"Dupla piora"** após melhora inicial
= Amoxicilina ± clavulanato 5–7 dias.
^ IDSA 2012
@B 🦠 Influenza: quem trata com oseltamivir?
- **Internados** e quadros graves
- Grupos de risco: > 65 anos, gestantes, puérperas, imunossuprimidos, doenças crônicas, < 2 anos
= Iniciar **independentemente** do tempo de sintomas nesses grupos (ideal < 48 h).
^ Ministério da Saúde 2023; CDC
@C 🧪 Diagnóstico de HIV no Brasil?
= 2 testes rápidos de fabricantes diferentes (reagentes) ou imunoensaio + **carga viral**/Western blot.
- Janela: imunoensaio de 4ª geração ~**15–20 dias**
- Infecção aguda: síndrome mono-like, rash, úlceras → carga viral
^ Ministério da Saúde 2018
@C 💊 TARV inicial preferencial no Brasil?
= **Tenofovir + lamivudina + dolutegravir** (TDF/3TC + DTG).
- Iniciar em **todos**, idealmente em até 7 dias
- Exceções para adiar: meningite criptocócica (4–6 semanas), TB meníngea
^ PCDT HIV 2024
@C 🦠 Profilaxias primárias no HIV pelo CD4?
| CD4 | Profilaxia | Contra
| < 200 | SMX-TMP | **Pneumocistose**
| < 100 + IgG toxo + | SMX-TMP | **Toxoplasmose**
| < 50 | Azitromicina (se TARV não supressora) | MAC
= TB latente (PPD ≥ 5 mm ou IGRA +): isoniazida ou rifapentina, qualquer CD4.
^ PCDT HIV 2024
% zones Profilaxias no HIV pelo CD4 :: CD4 < 200 = SMX-TMP para pneumocistose | CD4 < 100 = SMX-TMP para toxoplasmose (IgG +) | CD4 < 50 = Azitromicina para MAC se sem supressão
@C 🧠 Lesões cerebrais no HIV: diagnóstico diferencial?
| | Toxoplasmose | Linfoma primário do SNC
| Lesões | **Múltiplas**, anelares, núcleos da base | Única, periventricular
| Sorologia | IgG + | Variável
| Pista | Melhora com tratamento empírico em 10–14 dias | **EBV no LCR**, PET/SPECT
= Tratamento: sulfadiazina + pirimetamina + ácido folínico.
^ PCDT HIV 2024
% cmp Lesão cerebral no HIV :: Toxoplasmose = Múltiplas lesões anelares em núcleos da base, IgG positiva, resposta em 2 semanas | Linfoma do SNC = Lesão única periventricular, EBV no líquor, sem resposta à terapia
@C 🍄 Meningite criptocócica: manejo?
- **Antígeno criptocócico** (soro/LCR), tinta da China
- Pressão de abertura alta → **punções de alívio**
- Indução: anfotericina lipossomal + flucitosina; manutenção: fluconazol
- **Adiar TARV 4–6 semanas** (COAT)
^ OMS 2022
@C 🔄 Síndrome inflamatória de reconstituição imune (SIRI)?
= Piora paradoxal de infecção oportunista semanas após iniciar TARV, com queda da carga viral e subida do CD4.
- Mais com TB, cripto, CMV; CD4 baixo inicial
- Manter TARV; corticoide em casos moderados (TB)
^ PCDT HIV 2024
@C 💊 PrEP e PEP para HIV?
| | PrEP | PEP
| Quando | Antes da exposição (contínua ou sob demanda) | Até **72 h** após exposição
| Esquema | TDF + FTC (ou cabotegravir injetável) | TDF + 3TC + DTG
| Duração | Contínua | **28 dias**
^ PCDT PrEP/PEP 2024
% cmp PrEP × PEP para HIV :: PrEP = Antes da exposição. TDF + FTC contínua ou sob demanda | PEP = Até 72 h após exposição. TDF + 3TC + DTG por 28 dias
@C 👶 Prevenção da transmissão vertical do HIV?
- TARV na gestante (carga viral indetectável)
- **Zidovudina IV** no parto se carga viral > 1.000 ou desconhecida
- Cesárea eletiva se CV > 1.000 ou desconhecida após 34 semanas
- AZT para o recém-nascido; **não amamentar**
^ PCDT Transmissão Vertical 2022
"""
