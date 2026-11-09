TXT = r"""
@E 🦠 Leucemia aguda: sinais e diagnóstico?
- **Pancitopenia** ou leucocitose com **blastos**
- Infecções, sangramento, anemia, dor óssea, hiperplasia gengival (LMA M4/M5)
= Diagnóstico: **≥ 20% de blastos** na medula (OMS).
! Leucocitose > 100 mil: leucostase (dispneia, confusão) → citorredução.
^ OMS 2022; ELN 2022
@E 🧬 LMC: marcador e tratamento?
- Leucocitose com **desvio à esquerda escalonado**, basofilia, esplenomegalia
- **Cromossomo Philadelphia** t(9;22) — **BCR-ABL1**
= Inibidores de tirosina-quinase: **imatinibe**, dasatinibe, nilotinibe.
^ ELN 2020
@E 🔴 Neoplasias mieloproliferativas: JAK2?
| Doença | Achado principal | Mutação
| Policitemia vera | **Hb/Ht elevados**, prurido aquagênico | JAK2 (~95%)
| Trombocitemia essencial | Plaquetas > 450 mil | JAK2, CALR, MPL
| Mielofibrose | Hemácias em lágrima, esplenomegalia maciça | JAK2, CALR, MPL
^ OMS 2022
% cmp Neoplasias mieloproliferativas :: Policitemia vera = Hemoglobina alta, prurido aquagênico, JAK2 ~95%. Flebotomia + AAS | Trombocitemia essencial = Plaquetas > 450 mil. Trombose e sangramento | Mielofibrose = Dacriócitos, esplenomegalia maciça, medula seca
@E 🩸 Policitemia vera: tratamento?
- **Flebotomia**: alvo Ht < 45%
- **AAS** em dose baixa
- Citorredução (hidroxiureia) se alto risco: > 60 anos ou trombose prévia
^ ELN 2018
@E 🔁 Policitemia secundária: causas?
- Hipoxemia: DPOC, AOS, altitude, cardiopatia cianótica
- Tabagismo (carboxi-hemoglobina)
- **Testosterona** exógena
- Tumores com EPO: carcinoma renal, hepatocarcinoma, hemangioblastoma
= EPO **normal/alta** (na PV está baixa).
^ Revisões
@E 🧪 Síndrome mielodisplásica?
- Idoso, citopenias, **macrocitose**
- Displasia na medula, blastos < 20%
- Del(5q): resposta à lenalidomida
= Risco de evolução para LMA (IPSS-R).
^ OMS 2022
@F 🦴 Mieloma múltiplo: critérios CRAB?
- **C**álcio elevado
- **R**enal (creatinina > 2 ou ClCr < 40)
- **A**nemia (Hb < 10)
- **B**one (lesões líticas)
= + biomarcadores SLiM: plasmócitos ≥ 60%, cadeia leve envolvida/não envolvida ≥ 100, > 1 lesão focal na RM.
^ IMWG 2014
% cmp Mieloma múltiplo: CRAB :: Cálcio = Hipercalcemia | Renal = Rim do mieloma, cadeias leves | Anemia = Hb < 10 g/dL | Bone = Lesões líticas, fraturas
@F 🔬 MGUS × mieloma latente × mieloma?
| | Proteína M | Plasmócitos | CRAB
| MGUS | < 3 g/dL | < 10% | Não
| Mieloma latente | ≥ 3 g/dL ou | 10–60% | Não
| Mieloma | — | ≥ 10% | **Sim** (ou SLiM)
= MGUS evolui ~1%/ano.
^ IMWG 2014
@F 🌡️ Sintomas B no linfoma?
- **Febre** > 38 °C
- **Sudorese noturna** profusa
- **Perda de peso > 10%** em 6 meses
= Modificam o estadiamento (sufixo B) e o prognóstico.
^ Lugano 2014
@F 🧬 Linfomas não Hodgkin: associações etiológicas?
| Linfoma | Associação
| MALT gástrico | **H. pylori** (erradicar pode curar)
| Burkitt | EBV, t(8;14), MYC
| Linfoma de células T do adulto | **HTLV-1**
| Primário de SNC | HIV/imunossupressão (EBV)
| Folicular | t(14;18), BCL2
^ OMS 2022
@F 🫙 Amiloidose AL?
- Proteinúria nefrótica, cardiomiopatia restritiva, **macroglossia**, púrpura periorbitária
- Neuropatia, hepatomegalia
= Biópsia (gordura abdominal) com **vermelho Congo** (birrefringência verde-maçã).
^ Revisões
@F 🔥 Síndrome de hiperviscosidade?
- Waldenström (IgM), mieloma
- Cefaleia, alteração visual (veias retinianas em "salsicha"), sangramento mucoso
= **Plasmaférese** urgente.
^ Revisões
@G 🧊 Transfusão de plaquetas: limiares?
| Situação | Limiar
| Profilática (estável) | < 10 mil
| Febre/sepse | < 20 mil
| Punção lombar | < 40–50 mil
| CVC | < 10–20 mil
| Cirurgia maior/sangramento | < 50 mil
| Neurocirurgia | < 100 mil
! Não transfundir em PTT e TIH (exceto sangramento grave).
^ AABB 2025
@G 🩸 Plasma × crioprecipitado × complexo protrombínico?
| Produto | Contém | Uso
| Plasma | Todos os fatores | Coagulopatia com sangramento
| Crioprecipitado | **Fibrinogênio**, VIII, XIII, FvW | Fibrinogênio < 150–200
| CCP 4F | II, VII, IX, X | **Reversão de varfarina**
^ Revisões
@G 🧬 Hemácias irradiadas e filtradas: quando?
| Irradiadas (prevenir DECH) | Filtradas/leucorreduzidas
| Transplante de medula | Transplante, politransfundidos
| Imunodeficiência grave | Reação febril prévia
| Doadores parentes | Evitar CMV e aloimunização HLA
| Fludarabina, Hodgkin | 
^ Ministério da Saúde
"""
