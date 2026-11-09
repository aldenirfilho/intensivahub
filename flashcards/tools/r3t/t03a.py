TXT = r"""
@A 📈 Estágios KDIGO da lesão renal aguda?
| Estágio | Creatinina | Diurese
| 1 | ↑ ≥ 0,3 em 48 h ou 1,5–1,9× basal | < 0,5 mL/kg/h por 6–12 h
| 2 | 2,0–2,9× | < 0,5 por ≥ 12 h
| 3 | ≥ 3× ou ≥ 4,0 ou TRS | < 0,3 por ≥ 24 h ou anúria ≥ 12 h
^ KDIGO 2012
% zones KDIGO: estágios da LRA :: Estágio 1 = Cr ×1,5–1,9 ou +0,3 em 48 h | Estágio 2 = Cr ×2,0–2,9 | Estágio 3 = Cr ×3, ≥ 4,0 ou diálise
@A 🔍 LRA pré-renal × NTA: índices urinários?
| | Pré-renal | NTA
| FeNa | **< 1%** | > 2%
| FeUreia (com diurético) | < 35% | > 50%
| Na urinário | < 20 | > 40
| Osm urinária | > 500 | < 350
| Sedimento | Cilindros hialinos | **Cilindros granulosos "marrom-barrento"**
^ KDIGO; Harrison
% cmp LRA pré-renal × necrose tubular aguda :: Pré-renal = FeNa < 1%, Na urinário < 20, urina concentrada, cilindros hialinos | NTA = FeNa > 2%, Na urinário > 40, urina isostenúrica, cilindros granulosos
@A 💉 Nefropatia por contraste: prevenção?
- Identificar risco: **TFG < 30** (ou < 45 com DM), LRA
- **Hidratação** com cristaloide isotônico nos de alto risco
- Menor volume de contraste, iso/hipo-osmolar
- Suspender AINE; metformina conforme TFG
! N-acetilcisteína e bicarbonato **sem benefício** (PRESERVE).
^ PRESERVE 2018; ACR 2023
@A 🧪 Causas de LRA com sedimento ativo?
| Achado | Pensar em
| Hemácias dismórficas + cilindros hemáticos | Glomerulonefrite
| Leucócitos + cilindros leucocitários, eosinofilúria | Nefrite intersticial, pielonefrite
| Cristais em agulha | Ácido úrico (lise tumoral)
| Cristais em envelope | Oxalato (etilenoglicol)
| Pigmento heme sem hemácias | Rabdomiólise, hemólise
^ Harrison
@A 🩸 Rabdomiólise: dica do EAS?
= Fita reagente **positiva para sangue** com **poucas ou nenhuma hemácia** no sedimento (mioglobina).
- CK > 5× LSN; LRA se CK > 15–20 mil
- Hipercalemia, hiperfosfatemia, **hipocalcemia** inicial
^ Bosch NEJM 2009
@A 🚿 Indicações de diálise de urgência (AEIOU)?
- **A**cidose grave refratária (pH < 7,1–7,15)
- **E**letrólitos: hipercalemia refratária
- **I**ntoxicação dialisável (lítio, metanol, etilenoglicol, salicilato)
- **O**verload: congestão refratária
- **U**remia: pericardite, encefalopatia, sangramento
^ KDIGO 2012
% cmp Diálise de urgência (AEIOU) :: Acidose = pH < 7,1 refratário | Eletrólitos = Hipercalemia refratária | Intoxicação = Lítio, metanol, etilenoglicol, salicilato | Overload = Congestão refratária | Uremia = Pericardite, encefalopatia, sangramento
@A 🚫 Obstrução urinária como causa de LRA?
= Sempre pedir **USG** na LRA sem causa clara: hidronefrose.
- Homem idoso: HPB; mulher: neoplasia pélvica
- Anúria súbita: obstrução bilateral ou rim único
! Pós-desobstrução: poliúria (diurese pós-obstrutiva).
^ KDIGO
@B 🗺️ Classificação da DRC: TFG × albuminúria (KDIGO)?
| Albuminúria | mg/g
| A1 | < 30
| A2 | 30–300
| A3 | > 300
= Combinar estágio G (1–5) com A (1–3) → mapa de risco (verde, amarelo, laranja, vermelho).
= DRC: alteração por **> 3 meses**.
^ KDIGO 2024
% zones Albuminúria na DRC (relação albumina/creatinina) :: A1 = < 30 mg/g | A2 = 30–300 mg/g | A3 = > 300 mg/g
@B 🛡️ Nefroproteção na DRC com albuminúria?
- **IECA ou BRA** em dose máxima tolerada
- **iSGLT2** (TFG ≥ 20)
- **Finerenona** na DRC diabética com albuminúria (TFG ≥ 25)
- **GLP-1** (semaglutida) no DM2 (FLOW)
- PA < 120 sistólica se tolerado (KDIGO), estatina
^ KDIGO 2024; FLOW 2024
@B 🩸 Anemia da DRC: alvo de hemoglobina?
= Iniciar AEE com Hb < 10; alvo **10–11,5 g/dL**; não ultrapassar 13.
= Antes: repor ferro (ferritina > 200 e saturação > 20% em diálise).
! TREAT: Hb alta com darbepoetina aumentou AVC.
^ KDIGO 2012; TREAT 2009
@B 💊 Metformina e função renal?
| TFG | Conduta
| ≥ 45 | Dose plena
| 30–44 | Reduzir dose (máx. 1.000 mg/dia)
| < 30 | **Suspender**
^ FDA 2016; KDIGO 2022 DM
@B 🧪 Por que a creatinina sobe com trimetoprima e cimetidina?
= Bloqueiam a **secreção tubular** de creatinina: elevação sem queda real da TFG.
= Confirmar com cistatina C ou ureia estável.
^ Farmacologia renal
@B 🧮 Equação recomendada para estimar a TFG?
= **CKD-EPI 2021** (sem fator raça).
= Cistatina C combinada melhora a acurácia em extremos de massa muscular (sarcopenia, amputados, fisiculturistas).
^ KDIGO 2024
@B 🩺 Encaminhamento ao nefrologista?
- TFG **< 30**
- Albuminúria **> 300 mg/g** persistente
- Queda rápida da TFG (> 25% ou > 5 mL/min/ano)
- Hematúria glomerular, HAS resistente, K persistentemente alto
- Litíase recorrente, doença hereditária
^ KDIGO 2024
@B 🏠 Terapias renais substitutivas: opções?
- **Transplante** (melhor sobrevida)
- **Hemodiálise** (fístula arteriovenosa preferível ao cateter)
- **Diálise peritoneal** (preserva função residual)
- Tratamento conservador em idosos frágeis
= Preparar acesso quando TFG < 15–20.
^ KDIGO
@C 🔬 Síndrome nefrítica × nefrótica?
| | Nefrítica | Nefrótica
| Proteinúria | < 3,5 g/dia | **≥ 3,5 g/dia**
| Hematúria | **Dismórfica**, cilindros hemáticos | Discreta ou ausente
| HAS/oligúria | Sim | Menos
| Outros | Edema, ↑ creatinina | Albumina < 3, dislipidemia, lipidúria
^ KDIGO 2021 glomerular
% cmp Síndrome nefrítica × nefrótica :: Nefrítica = Hematúria dismórfica, cilindros hemáticos, HAS, oligúria, proteinúria < 3,5 g | Nefrótica = Proteinúria ≥ 3,5 g, albumina < 3, edema, dislipidemia, trombose
@C 🧒 GN pós-estreptocócica?
- 1–3 semanas após faringite (ou 3–6 após impetigo)
- Síndrome nefrítica, **C3 baixo** (normaliza em 6–8 semanas)
- ASLO elevado
= Tratamento de suporte (diurético, anti-hipertensivo).
! C3 baixo por > 8 semanas: pensar em GN membranoproliferativa/C3.
^ KDIGO 2021
@C 🧩 Glomerulopatias e complemento?
| Complemento baixo | Complemento normal
| Pós-infecciosa | IgA
| Lúpus | Vasculite ANCA
| Membranoproliferativa/C3 | Anti-MBG (Goodpasture)
| Crioglobulinemia (hepatite C) | GESF, membranosa, lesão mínima
| Endocardite, shunt | 
^ KDIGO 2021
@C ⚡ GN rapidamente progressiva: classificação?
| Tipo | Imunofluorescência | Exemplos
| I | Linear | Anti-MBG (Goodpasture)
| II | Granular | Lúpus, IgA, pós-infecciosa
| III | Pauci-imune | Vasculite ANCA
= Crescentes > 50% dos glomérulos; urgência (corticoide em pulso).
^ KDIGO 2021
@C 🧸 Lesão mínima?
- Principal causa de nefrótica em **crianças**
- Adultos: AINE, linfoma de Hodgkin
- Microscopia óptica normal; **apagamento dos podócitos** na eletrônica
= Excelente resposta a corticoide.
^ KDIGO 2021
@C 🧱 GESF (glomeruloesclerose segmentar e focal)?
- Causa comum de nefrótica em adultos negros
- Secundária: **HIV**, obesidade, heroína, refluxo, APOL1
- Resposta pior ao corticoide; inibidores de calcineurina
^ KDIGO 2021
@C 🧬 Nefropatia membranosa?
- Principal causa de nefrótica idiopática em adultos brancos
- **Anti-PLA2R** positivo em ~70% (primária)
- Secundária: neoplasias, hepatite B, lúpus classe V, ouro, AINE
- Maior risco de **trombose da veia renal**
= Rituximabe para risco moderado/alto (MENTOR).
^ KDIGO 2021; MENTOR 2019
@C 🩸 Anticoagulação profilática na síndrome nefrótica?
= Considerar com **albumina < 2,0–2,5 g/dL**, sobretudo na membranosa, se baixo risco de sangramento.
^ KDIGO 2021
@C 🍬 Nefropatia diabética: quando suspeitar de outra causa?
- Ausência de **retinopatia** no DM1
- Início rápido da proteinúria ou TFG caindo rápido
- **Hematúria** dismórfica, sedimento ativo
- Proteinúria em < 5 anos de DM1
= Considerar biópsia.
^ KDIGO 2022 DM
"""
