TXT = r"""
@D 🧩 Tipos de demência: pistas clínicas?
| Tipo | Pista
| Alzheimer | **Memória episódica** precoce, progressão gradual
| Vascular | Degraus, sinais focais, disfunção executiva
| Corpos de Lewy | **Flutuação**, alucinações visuais, parkinsonismo, sensibilidade a antipsicótico
| Frontotemporal | **Comportamento**/linguagem, jovem (< 65)
| Hidrocefalia de pressão normal | Marcha + incontinência + demência
^ DSM-5; Revisões
% cmp Demências: pistas :: Alzheimer = Memória episódica, progressiva | Vascular = Degraus, sinais focais | Corpos de Lewy = Flutuação, alucinação visual, parkinsonismo | Frontotemporal = Comportamento, linguagem, < 65 anos
@D 🧪 Demência: causas reversíveis a excluir?
- **B12**, **TSH**, sífilis (VDRL), HIV
- **Depressão** (pseudodemência)
- Drogas (anticolinérgicos, benzodiazepínicos)
- Hidrocefalia de pressão normal, hematoma subdural
= Neuroimagem em todos.
^ AAN
@D 💊 Tratamento sintomático do Alzheimer?
- **Inibidores da colinesterase** (donepezila, rivastigmina, galantamina): leve a grave
- **Memantina** (antagonista NMDA): moderada a grave
- Anti-amiloide (lecanemabe, donanemabe): fase inicial com amiloide confirmado; risco de **ARIA**
! Inibidores de colinesterase: bradicardia, síncope.
^ AAN; Clarity AD 2023
@D 🧠 Parkinsonismo atípico: sinais de alerta?
- Má resposta à levodopa
- Quedas precoces
- **Paralisia supranuclear progressiva**: olhar vertical para baixo limitado
- **Atrofia de múltiplos sistemas**: disautonomia grave, ataxia
- Degeneração corticobasal: apraxia, membro alienígena
^ MDS
@D 🎲 Tremor essencial × parkinsoniano?
| | Essencial | Parkinsoniano
| Tipo | **Postural/ação** | **Repouso**
| Local | Mãos, cabeça, voz | Mãos ("contar dinheiro"), assimétrico
| Álcool | Melhora | —
| Tratamento | **Propranolol**, primidona | Levodopa, agonistas
^ MDS 2018
% cmp Tremor essencial × parkinsoniano :: Essencial = Postural e de ação, bilateral, cabeça e voz, melhora com álcool. Propranolol ou primidona | Parkinsoniano = Repouso, assimétrico, bradicinesia e rigidez. Levodopa
@D 💊 Complicações da levodopa?
- Flutuações: **wearing-off**, on-off
- **Discinesias** de pico de dose
- Hipotensão ortostática, náusea, alucinações
= Agonistas dopaminérgicos: **transtorno de controle de impulsos** (jogo, compras).
^ MDS 2018
@D 🧠 Antipsicótico em paciente com Parkinson/Lewy?
= Preferir **quetiapina** ou **clozapina** (pimavanserina onde disponível).
! Haloperidol e risperidona: piora grave do parkinsonismo e síndrome neuroléptica.
^ MDS 2019
@D 🦵 Síndrome das pernas inquietas?
- Urgência de mover as pernas, piora em repouso e à **noite**, alivia com movimento
- Dosar **ferritina**: repor ferro se < 75 ng/mL
- Associações: DRC, gestação, neuropatia
= Gabapentinoides (1ª linha); agonistas dopaminérgicos (risco de augmentation).
^ AASM 2024
@E 🧩 Esclerose múltipla: critérios e exames?
= Disseminação no **espaço** e no **tempo** (McDonald 2017).
- RM: lesões periventriculares, justacorticais, infratentoriais, medulares
- **Bandas oligoclonais** no LCR substituem disseminação temporal
- Clínica: neurite óptica, mielite, oftalmoplegia internuclear, Lhermitte, Uhthoff
^ McDonald 2017
@E 💊 Surto de EM: tratamento?
= **Metilprednisolona 1 g/dia por 3–5 dias**; plasmaférese se refratário.
= Terapia modificadora para reduzir surtos (interferon, glatirâmer, fingolimode, natalizumabe, ocrelizumabe).
! Natalizumabe: risco de **LEMP** (JC vírus).
^ ECTRIMS/EAN 2018
@E 👁️ Neuromielite óptica × esclerose múltipla?
| | NMO | EM
| Anticorpo | **Anti-aquaporina 4** | Bandas oligoclonais
| Mielite | **Longitudinal extensa** (≥ 3 segmentos) | Curta
| Neurite óptica | Grave, bilateral | Unilateral, leve
| Interferon | **Piora** | Benefício
^ IPND 2015
@E ⚡ Guillain-Barré: quadro e diagnóstico?
- Fraqueza **ascendente simétrica**, **arreflexia**, após infecção (Campylobacter, Zika)
- LCR: **dissociação proteinocitológica** (proteína ↑, células normais)
- ENMG: desmielinizante ou axonal
- Disautonomia
= **IgIV** ou plasmaférese; corticoide **não**.
^ EAN/PNS 2023
% flow Guillain-Barré :: Fraqueza ascendente + arreflexia após infecção >> LCR: dissociação proteinocitológica; ENMG >> Monitorar CVF (20/30/40) e disautonomia >> IgIV ou plasmaférese; corticoide não
@E 😴 Miastenia gravis?
- Fraqueza **fatigável**, ptose, diplopia, piora ao fim do dia
- Anticorpos **anti-receptor de acetilcolina** (ou anti-MuSK)
- ENMG com estimulação repetitiva (decremento)
- TC de tórax: **timoma**
= Piridostigmina, corticoide, imunossupressor; timectomia.
^ MGFA 2020
@E 💊 Drogas que pioram a miastenia?
- **Aminoglicosídeos**, fluoroquinolonas, macrolídeos
- **Magnésio**
- Betabloqueadores, BCC
- Bloqueadores neuromusculares
- Contraste iodado (raro), estatinas, checkpoint inhibitors
^ MGFA 2020
@E 🎗️ Lambert-Eaton × miastenia?
| | Lambert-Eaton | Miastenia
| Anticorpo | Anti-**canal de cálcio** pré-sináptico | Anti-receptor de ACh
| Fraqueza | Proximal de MMII | Ocular, bulbar
| Esforço repetido | **Melhora** (facilitação) | Piora
| Reflexos | **Diminuídos** | Normais
| Associação | **Pequenas células** | Timoma
^ Revisões
% cmp Lambert-Eaton × miastenia gravis :: Lambert-Eaton = Pré-sináptico (canal de cálcio), melhora com esforço, hiporreflexia, carcinoma de pequenas células | Miastenia = Pós-sináptico (receptor ACh), piora com esforço, ocular/bulbar, timoma
@E 🦵 ELA (esclerose lateral amiotrófica)?
- Sinais de **neurônio motor superior e inferior** juntos
- Fasciculações, atrofia, hiper-reflexia, Babinski
- **Poupa** sensibilidade, motricidade ocular e esfíncteres
= Riluzol, edaravona; VNI e gastrostomia.
^ Revisões
@E 🔦 Neuropatia periférica: causas mais comuns?
- **Diabetes** (sensitiva distal em "bota e luva")
- Álcool, deficiência de **B12**
- Hipotireoidismo, DRC, HIV, hanseníase (Brasil)
- Drogas: quimioterapia, isoniazida, metronidazol
^ AAN
@F 🧠 Escala de coma de Glasgow?
| Item | Pontos
| Abertura ocular | 1–4
| Resposta verbal | 1–5
| Resposta motora | 1–6
= ≤ 8: coma → considerar via aérea definitiva. Versão atual inclui **reatividade pupilar** (GCS-P).
^ Teasdale 1974/2014
@F 🌀 Delirium: diagnóstico e causas?
= Início **agudo**, curso **flutuante**, **desatenção** + pensamento desorganizado ou alteração de consciência (CAM).
- Causas: infecção, drogas (anticolinérgicos, benzodiazepínicos, opioides), retenção urinária, dor, hipóxia, distúrbios metabólicos, abstinência
^ CAM; NICE 2023
@F 💫 Vertigem central × periférica (HINTS)?
| | Periférica | Central
| **H**ead Impulse | **Anormal** (sacada corretiva) | Normal
| **N**istagmo | Unidirecional, horizontal | Muda de direção, vertical
| **T**est of Skew | Normal | Desvio presente
= HINTS sugestivo de central → RM (AVC de fossa posterior).
^ Kattah 2009
% cmp Vertigem: protocolo HINTS :: Periférica = Impulso cefálico ANORMAL, nistagmo unidirecional, skew normal | Central (AVC) = Impulso cefálico NORMAL, nistagmo que muda de direção, skew presente
@F 🔄 Vertigem posicional paroxística benigna?
- Vertigem de segundos ao **mudar a posição da cabeça**
- **Dix-Hallpike** positivo (nistagmo torcional com latência)
= Manobra de **Epley** (canal posterior); sem medicação.
^ AAO-HNS 2017
@F 😐 Paralisia facial periférica × central?
| | Periférica (Bell) | Central
| Fronte | **Acometida** | Poupada
| Causa | Bell, zóster (Ramsay Hunt), Lyme | AVC, tumor
= Bell: **prednisona** em até 72 h (± antiviral em casos graves); proteger a córnea.
^ AAO-HNS 2013
"""
