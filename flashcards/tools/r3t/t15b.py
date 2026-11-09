TXT = r"""
@A 🩺 Dor torácica no PS: causas que matam?
- **SCA**
- **Dissecção de aorta**
- **TEP**
- **Pneumotórax hipertensivo**
- **Tamponamento**
- **Ruptura de esôfago** (Boerhaave)
^ Revisões
@A 🫁 Insuficiência respiratória: tipo 1 × tipo 2?
| Tipo | Gasometria | Exemplos
| 1 (hipoxêmica) | PaO₂ < 60, PaCO₂ normal/baixa | Pneumonia, SDRA, EAP, TEP
| 2 (hipercápnica) | **PaCO₂ > 45–50**, pH ↓ | DPOC, neuromuscular, sedação, obesidade-hipoventilação
^ Revisões
% cmp Insuficiência respiratória :: Tipo 1 hipoxêmica = PaO2 < 60, PaCO2 normal. Pneumonia, EAP, SDRA, TEP | Tipo 2 hipercápnica = PaCO2 > 45–50, acidose. DPOC, neuromuscular, sedativos
@A 💨 Cateter nasal de alto fluxo: indicação?
= Insuficiência respiratória **hipoxêmica** (FLORALI) e pós-extubação; conforto e menos intubação em selecionados.
= Índice **ROX** (SpO₂/FiO₂ ÷ FR) < 3,85 em 12 h prevê falha.
^ FLORALI 2015; Roca 2019
@A 🧠 Rebaixamento de consciência: primeiras medidas?
- ABC, **glicemia capilar**
- **Tiamina** antes de glicose em etilista/desnutrido
- Naloxona se suspeita de opioide
- TC de crânio, eletrólitos, gasometria, toxicológico
^ Revisões
@A 🫀 Síncope no PS: escores?
= **San Francisco** (CHESS): ICC, Hematócrito < 30, ECG anormal, dispneia (Shortness of breath), PAS < 90.
= Canadian Syncope Risk Score.
^ ESC 2018
@A 🩸 Choque: classificação hemodinâmica?
| Tipo | DC | RVS | Pressão de enchimento
| Hipovolêmico | ↓ | ↑ | ↓
| Cardiogênico | ↓ | ↑ | **↑**
| Distributivo | ↑ (ou normal) | **↓** | ↓/normal
| Obstrutivo | ↓ | ↑ | ↑ (VD)
^ Vincent NEJM 2013
% cmp Tipos de choque :: Hipovolêmico = Débito baixo, RVS alta, pressões baixas | Cardiogênico = Débito baixo, RVS alta, pressões ALTAS | Distributivo = Débito normal/alto, RVS BAIXA | Obstrutivo = TEP, tamponamento, pneumotórax
@A 💉 Noradrenalina em acesso periférico?
= Aceitável por curto período (< 24 h) em veia calibrosa proximal, com vigilância de extravasamento (fentolamina se ocorrer).
^ SSC 2021
@A 🧪 Lactato elevado sem hipoperfusão?
- **Metformina**, adrenalina (β2)
- Hepatopatia, convulsão
- Linezolida, deficiência de tiamina
- Neoplasias (efeito Warburg)
^ Revisões
@B 🧪 Intoxicação por benzodiazepínico: flumazenil?
! Pode precipitar **convulsões** em dependentes crônicos ou coingestão de tricíclicos/pró-convulsivantes.
= Suporte ventilatório é a base; flumazenil em casos selecionados (ex. sedação iatrogênica em não dependentes).
^ Goldfrank
@B 💊 Intoxicação por betabloqueador/BCC?
- Bradicardia, hipotensão, hipoglicemia (β), **hiperglicemia** (BCC)
= Cálcio IV, **glucagon**, **insulina em alta dose** (1 U/kg/h + glicose), vasopressor, emulsão lipídica, ECMO.
^ Goldfrank; Revisões
@C 🌡️ Febre no internado: causas não infecciosas?
- **TEV**, flebite
- **Drogas** (febre medicamentosa: β-lactâmicos, anticonvulsivantes)
- Transfusão, pancreatite, gota
- Neoplasia, abstinência, insuficiência adrenal
^ Revisões
@C 💩 Constipação no internado: escalonamento?
- Mobilização, hidratação, revisar drogas
- **Macrogol** ou lactulose; bisacodil/sene
- Opioide: metilnaltrexona/naloxegol se refratária
! Fecaloma: toque retal antes de laxativos estimulantes.
^ Revisões
@C 🧠 Alta hospitalar segura: checklist?
- **Reconciliação medicamentosa**
- Plano escrito e sinais de alarme
- Consulta de retorno marcada (7–14 dias)
- Pendências de exames
- Rede de cuidado/cuidador
^ Revisões
@C 💊 Reconciliação medicamentosa: para que serve?
= Comparar medicações de casa × prescrição hospitalar × alta para evitar **omissões, duplicidades e interações** (principal erro na transição de cuidado).
^ OMS High 5s
@C 🦠 Precauções de isolamento?
| Tipo | Exemplos
| Contato | MRSA, ESBL/KPC, C. difficile (sabão), escabiose
| Gotículas | Influenza, meningococo, coqueluche
| **Aerossóis** (N95, quarto pressão negativa) | **TB**, sarampo, varicela
^ CDC/ANVISA
% cmp Precauções de isolamento :: Contato = Germes multirresistentes, C. difficile, escabiose | Gotículas = Influenza, meningococo, coqueluche | Aerossóis (N95) = Tuberculose, sarampo, varicela
@C 🧼 Higienização das mãos: 5 momentos (OMS)?
- Antes de tocar o paciente
- Antes de procedimento asséptico
- Após risco de exposição a fluidos
- Após tocar o paciente
- Após tocar superfícies próximas
! C. difficile: **água e sabão** (álcool não mata esporos).
^ OMS 2009
@C 💉 Sondagem vesical de demora: indicações apropriadas?
- Retenção/obstrução
- Débito urinário em críticos
- Cirurgias selecionadas
- Lesão sacral/perineal em incontinente
- Cuidados de fim de vida
= Remover **o quanto antes** (ITU associada).
^ CDC 2009
@D ⛰️ Mal agudo da montanha?
= Cefaleia + náusea/fadiga após subida > 2.500 m; edema pulmonar e cerebral nas formas graves.
= **Descer**, O₂; acetazolamida (prevenção), dexametasona (cerebral), nifedipino (pulmonar).
^ WMS 2019
@D ⚡ Choque elétrico e raio: cuidados?
- **ECG** e monitorização (arritmias)
- CK, função renal (rabdomiólise)
- Queimaduras de entrada/saída; síndrome compartimental
- Raio: assistolia/apneia → priorizar RCP nas vítimas "aparentemente mortas" (triagem reversa)
^ Revisões
@D 🧊 Congelamento: tratamento?
= Reaquecimento rápido em água a **37–39 °C**; evitar recongelar; analgesia; iloprosta/trombólise em casos graves.
^ WMS 2019
"""
