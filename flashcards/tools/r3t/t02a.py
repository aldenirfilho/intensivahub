TXT = r"""
@A 🌬️ Diagnóstico funcional de asma na espirometria?
= Obstrução (VEF₁/CVF reduzida) com **prova broncodilatadora positiva**: ↑ VEF₁ **≥ 12% e ≥ 200 mL**.
- Espirometria normal não exclui: variabilidade do PFE > 10%, broncoprovocação com metacolina
- FeNO > 50 ppb sugere inflamação T2
^ GINA 2024
@A 🎯 Controle da asma (GINA) nas últimas 4 semanas?
- Sintomas diurnos > 2×/semana?
- Despertar noturno por asma?
- SABA de alívio > 2×/semana?
- Limitação de atividade?
| Respostas "sim" | Controle
| 0 | Controlada
| 1–2 | Parcialmente controlada
| 3–4 | Não controlada
^ GINA 2024
% zones Controle da asma (GINA, 4 semanas) :: Controlada = 0 itens | Parcial = 1–2 itens | Não controlada = 3–4 itens
@A 🪜 Etapas do tratamento da asma em adultos (via preferencial GINA)?
| Etapa | Tratamento
| 1–2 | CI-formoterol **conforme necessidade**
| 3 | CI-formoterol dose baixa de manutenção + alívio (MART)
| 4 | CI-formoterol dose média (MART)
| 5 | + LAMA, fenotipagem, biológico, azitromicina
! SABA isolado sem CI **não** é mais recomendado.
^ GINA 2024
% flow Asma: via preferencial (GINA) :: Etapas 1–2: CI-formoterol só quando necessário >> Etapa 3: MART com dose baixa >> Etapa 4: MART com dose média >> Etapa 5: LAMA, fenotipagem e biológico
@A 💉 Biológicos na asma grave e seus alvos?
| Droga | Alvo | Indicação
| Omalizumabe | IgE | Alérgica com IgE elevada
| Mepolizumabe, reslizumabe | IL-5 | Eosinofílica
| Benralizumabe | Receptor IL-5 | Eosinofílica
| Dupilumabe | Receptor IL-4α (IL-4/IL-13) | Eosinofílica/FeNO alto
| Tezepelumabe | TSLP | Inclusive T2-baixa
^ GINA 2024
@A 🚨 Crise asmática grave: sinais?
- Fala em **palavras**, uso de musculatura acessória
- FR > 30, FC > 120, SpO₂ < 90%
- PFE ≤ 50% do previsto
= Risco de vida: **tórax silencioso**, cianose, confusão, PaCO₂ normal ou alta.
^ GINA 2024
@A 💊 Tratamento da crise asmática no PS?
- **SABA** repetido (salbutamol 4–10 jatos a cada 20 min na 1ª hora)
- **Ipratrópio** na crise grave
- **Corticoide sistêmico** precoce (prednisona 40–50 mg 5–7 dias)
- O₂ para SpO₂ 93–95%
- Sulfato de magnésio IV na grave refratária
! Antibiótico **não** é rotina.
^ GINA 2024
@A 🍷 Doença respiratória exacerbada por AAS (DREA)?
= Tríade de **Samter**: asma + polipose nasal + intolerância a AAS/AINE (inibição da COX-1).
- Evitar AINE não seletivos; inibidores de COX-2 geralmente tolerados
- Dessensibilização com AAS e dupilumabe são opções
^ GINA 2024
@A 🫁 ABPA (aspergilose broncopulmonar alérgica)?
- Asma ou fibrose cística de difícil controle
- **IgE total > 500**, IgE específica para Aspergillus
- Eosinofilia, bronquiectasias centrais, impactação mucoide
= Tratamento: corticoide sistêmico ± itraconazol.
^ ISHAM 2024
@B 🧪 Eosinófilos e corticoide inalatório na DPOC?
| Eosinófilos/µL | CI
| < 100 | Pouco benefício (mais pneumonia)
| 100–300 | Considerar se exacerbador
| ≥ 300 | **Benefício** claro
! Asma concomitante: CI sempre.
^ GOLD 2025
@B 🫁 Exacerbação de DPOC: quando antibiótico?
= Critérios de **Anthonisen**: ↑ dispneia, ↑ volume do escarro, **escarro purulento**.
- Antibiótico se escarro purulento + 1 outro critério, ou VM
- Corticoide: prednisona **40 mg por 5 dias** (REDUCE)
^ GOLD 2025; REDUCE 2013
@B 🏠 Oxigenoterapia domiciliar na DPOC: critérios?
- PaO₂ **≤ 55 mmHg** ou SpO₂ ≤ 88% em repouso
- PaO₂ 56–59 com cor pulmonale, edema ou hematócrito > 55%
= ≥ 15 h/dia, reavaliar em 60–90 dias.
^ NOTT 1980; MRC 1981; GOLD 2025
@B 🧬 Deficiência de alfa-1 antitripsina: quando pesquisar?
- DPOC em **jovem** (< 45 anos) ou pouco tabagista
- Enfisema **panlobular de bases**
- Hepatopatia inexplicada, paniculite, vasculite c-ANCA
= Dosar alfa-1 antitripsina sérica uma vez em todo DPOC (OMS).
^ GOLD 2025; ATS/ERS
@B 💪 O que reduz mortalidade na DPOC?
- **Cessar tabagismo**
- **O₂ domiciliar** em hipoxêmicos
- **VNI domiciliar** em hipercápnicos pós-exacerbação
- Terapia tripla em exacerbadores (IMPACT, ETHOS)
- Reabilitação pulmonar após exacerbação
- Cirurgia redutora em casos selecionados
^ GOLD 2025
@B 🧘 Reabilitação pulmonar na DPOC?
= Melhora dispneia, capacidade de exercício e qualidade de vida; reduz internações quando iniciada após exacerbação.
= Indicada nos grupos B e E.
^ GOLD 2025
@C 💧 Critérios de Light para exsudato?
= ≥ 1 critério:
- Proteína pleural/sérica **> 0,5**
- LDH pleural/sérica **> 0,6**
- LDH pleural > **2/3 do limite superior** sérico
! Transudato em uso de diurético pode parecer exsudato: gradiente de albumina > 1,2 g/dL confirma transudato.
^ Light 1972
@C 🔬 Causas de derrame pleural por tipo?
| Transudato | Exsudato
| IC (mais comum) | Pneumonia (parapneumônico)
| Cirrose (hidrotórax) | Neoplasia
| Síndrome nefrótica | Tuberculose
| Hipoalbuminemia | TEP (pode ser ambos)
| Diálise peritoneal | Colagenoses, pancreatite
^ BTS 2023
% cmp Derrame pleural :: Transudato = IC, cirrose, síndrome nefrótica, hipoalbuminemia | Exsudato = Pneumonia, câncer, tuberculose, TEP, colagenose, pancreatite
@C 🧪 Pistas bioquímicas no líquido pleural?
| Achado | Pensar em
| ADA > 40 U/L + linfócitos | **Tuberculose**
| Glicose < 60 | Empiema, AR, TB, neoplasia
| Amilase alta | Pancreatite, ruptura esofágica
| TG > 110 mg/dL | **Quilotórax**
| pH < 7,2 | Drenagem (parapneumônico complicado)
| Hematócrito > 50% do sangue | Hemotórax
^ BTS 2023
@C 🎈 Pneumotórax espontâneo: conduta?
- Primário pequeno e assintomático: **observação**
- Primário sintomático/grande: aspiração ou dreno fino
- Secundário (DPOC): dreno e internação
- Recorrência: **pleurodese**/videotoracoscopia
^ BTS 2023
@C 🔵 Nódulo sólido incidental: seguimento (Fleischner)?
| Tamanho | Baixo risco | Alto risco
| < 6 mm | Sem seguimento | TC opcional em 12 meses
| 6–8 mm | TC 6–12 meses | TC 6–12 e 18–24 meses
| > 8 mm | PET-CT, biópsia ou TC em 3 meses | Idem
^ Fleischner 2017
@C 🧬 Câncer de pulmão: tipos e associações?
| Tipo | Pistas
| Adenocarcinoma | Periférico, não fumantes, mulheres, EGFR/ALK
| Escamoso | Central, cavitação, **hipercalcemia (PTHrp)**
| Pequenas células | Central, **SIADH, Cushing ectópico, Lambert-Eaton**
| Grandes células | Periférico, ginecomastia
^ ESMO; NCCN
@C 🎯 Por que pesquisar mutações no adenocarcinoma de pulmão?
= Alvos com terapia específica: **EGFR** (osimertinibe), **ALK** (alectinibe), ROS1, BRAF, KRAS G12C, MET, RET, NTRK; **PD-L1** para imunoterapia.
^ NCCN 2025
@C 👁️ Síndrome de Pancoast?
= Tumor de ápice pulmonar: dor no ombro/braço (plexo braquial C8–T1) + **síndrome de Horner** (ptose, miose, anidrose).
^ Semiologia
@D 🧱 Padrão restritivo na espirometria e confirmação?
= VEF₁/CVF normal ou alta, CVF reduzida → confirmar com **CPT < 80%** (pletismografia).
- DLCO baixa: doença do parênquima (intersticial)
- DLCO normal: parede torácica, neuromuscular, obesidade
^ ATS/ERS 2022
@D 🧩 DLCO: o que aumenta e o que diminui?
| ↑ DLCO | ↓ DLCO
| Hemorragia alveolar | Enfisema
| Policitemia | Doença intersticial
| Asma | TEP crônico, hipertensão pulmonar
| Shunt E→D | Anemia
^ ATS/ERS 2017
% cmp DLCO na prova de função pulmonar :: Aumenta = Hemorragia alveolar, policitemia, asma, shunt | Diminui = Enfisema, intersticial, doença vascular pulmonar, anemia
@D 🍯 Padrão de PIU na TC (pneumonia intersticial usual)?
- Reticulação **subpleural e basal**
- **Faveolamento**
- Bronquiectasias de tração
- Ausência de achados atípicos (vidro fosco predominante, nódulos, cistos)
= Com quadro clínico compatível e sem causa: **FPI** (dispensa biópsia).
^ ATS/ERS/JRS/ALAT 2022
@D 🔁 Fibrose pulmonar progressiva: tratamento?
= Antifibrótico (**nintedanibe**) também em intersticiais não-FPI progressivas (INBUILD), como esclerodermia e PH crônica.
^ INBUILD 2019; ATS 2022
@D 🐦 Pneumonite de hipersensibilidade?
- Antígeno inalado: aves (pulmão do criador de pássaros), mofo, feno
- TC: vidro fosco, nódulos centrolobulares, **aprisionamento aéreo** (mosaico)
- LBA com **linfocitose** (> 30%)
= Pilar: **afastar o antígeno**; corticoide se grave.
^ ATS 2020
@D 🌸 Sarcoidose: estágios radiológicos (Scadding)?
| Estágio | RX
| 0 | Normal
| I | Adenopatia hilar bilateral
| II | Adenopatia + infiltrado
| III | Infiltrado sem adenopatia
| IV | Fibrose
^ Scadding 1961
% zones Sarcoidose: estágios de Scadding :: 0 = RX normal | I = Adenopatia hilar bilateral | II = Adenopatia + parênquima | III = Parênquima sem adenopatia | IV = Fibrose
@D 🌸 Sarcoidose: achados extrapulmonares e laboratoriais?
- Uveíte, eritema nodoso, lúpus pérnio
- Paralisia facial, cardíaca (BAV, morte súbita)
- **Hipercalcemia/hipercalciúria** (1-alfa-hidroxilase nos granulomas)
- ECA sérica elevada (inespecífica)
= Biópsia: granulomas **não caseosos**.
^ ATS 2020
@D 🌡️ Síndrome de Löfgren?
= Eritema nodoso + adenopatia hilar bilateral + artrite de tornozelos ± febre.
= Forma aguda de sarcoidose com **excelente prognóstico** (dispensa biópsia).
^ ATS 2020
"""
