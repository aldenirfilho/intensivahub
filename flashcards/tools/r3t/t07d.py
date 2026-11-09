TXT = r"""
@A ⏱️ Antibiótico de curta duração: evidências?
| Infecção | Duração
| PAC | **5 dias**
| Pielonefrite | 7 dias (fluoroquinolona) / 7–14 β-lactâmico
| Celulite | 5–6 dias
| Infecção intra-abdominal com foco controlado | **4 dias** (STOP-IT)
| Bacteriemia por Gram-negativo não complicada | **7 dias**
| PAV | 7 dias
^ STOP-IT 2015; BALANCE 2024
% cmp Duração curta de antibiótico :: PAC = 5 dias | Intra-abdominal com foco controlado = 4 dias | Bacteriemia Gram-negativa não complicada = 7 dias | Celulite = 5–6 dias
@A 🧪 Infecção intra-abdominal comunitária: tratamento?
= **Ceftriaxona + metronidazol** (ou amoxicilina-clavulanato) + controle de foco.
= Grave/hospitalar: piperacilina-tazobactam ou carbapenêmico.
^ SIS/IDSA 2017
@A 💊 Fosfomicina e nitrofurantoína: pontos-chave?
- **Nitrofurantoína**: só cistite (não atinge rim/sangue); evitar com TFG < 30
- **Fosfomicina** 3 g dose única: cistite, inclusive ESBL
^ IDSA 2025
@B 🦠 COVID-19 no paciente ambulatorial de risco?
= Nirmatrelvir-ritonavir em até 5 dias (alto risco) — atenção às **interações** (ritonavir).
= Internado com O₂: **dexametasona 6 mg** 10 dias (RECOVERY); remdesivir; anticoagulação profilática.
^ IDSA 2024; RECOVERY 2021
@B 🤧 Coqueluche no adulto?
- Tosse paroxística prolongada (> 2 semanas), guincho, vômitos pós-tosse
- **Azitromicina**; profilaxia de contatos
- dTpa na gestação protege o lactente
^ Ministério da Saúde
@C 🧪 HIV e TB: quando iniciar TARV?
= Iniciar TARV em **até 2 semanas** após início do tratamento da TB se CD4 < 50; demais em até 8 semanas.
! **TB meníngea**: adiar TARV 4–8 semanas (mortalidade).
- Rifampicina: dobrar o dolutegravir (50 mg 12/12 h)
^ PCDT HIV 2024
@C 🧠 Leucoencefalopatia multifocal progressiva?
- HIV avançado, natalizumabe, rituximabe
- Déficits focais progressivos; lesões de **substância branca** sem efeito de massa nem realce
- **Vírus JC** no LCR
= Restaurar imunidade (TARV).
^ Revisões
@C 🦠 Citomegalovírus no HIV?
- **Retinite** (CD4 < 50): "queijo com ketchup", perda visual
- Colite, esofagite (úlceras rasas)
= Ganciclovir/valganciclovir.
^ PCDT HIV 2024
@C 🍄 Candidíase esofágica no HIV?
= Odinofagia + candidíase oral → **fluconazol** empírico; EDA se falha.
= Doença definidora de aids.
^ PCDT HIV 2024
@D 🫁 TB com resistência à rifampicina no TRM: conduta?
= Encaminhar à referência; cultura com TS e esquemas para TB-RR/MDR (bedaquilina, linezolida, pretomanida — **BPaLM** 6 meses).
^ OMS 2022; MS 2024
@D 🧬 IGRA × PPD?
| | IGRA | PPD
| BCG prévia | **Não interfere** | Pode falso-positivo
| Visitas | 1 | 2
| Custo | Maior | Menor
= Ambos não distinguem TB latente de ativa.
^ Manual de TB MS 2019
@E 🧪 Sífilis na gestação: tratamento adequado?
= **Penicilina benzatina** conforme estágio, iniciada até **30 dias antes do parto**, com parceiro tratado (para vigilância).
! Alergia: **dessensibilização** (só penicilina trata o feto).
^ PCDT Transmissão Vertical 2022
@E 🦠 Doença inflamatória pélvica: tratamento ambulatorial?
= **Ceftriaxona 500 mg IM** dose única + **doxiciclina 100 mg 12/12 h + metronidazol 500 mg 12/12 h** por 14 dias.
- Internar: abscesso tubo-ovariano, gestante, falha, grave
^ PCDT IST 2022
@E 🧪 Corrimentos vaginais?
| | Vaginose | Tricomoníase | Candidíase
| Corrimento | Acinzentado, **odor de peixe** | Amarelo-esverdeado, bolhoso | Branco grumoso
| pH | **> 4,5** | > 4,5 | < 4,5
| Teste de aminas | **Positivo** | Positivo | Negativo
| Tratamento | Metronidazol | Metronidazol (tratar parceiro) | Fluconazol
^ PCDT IST 2022
% cmp Corrimentos vaginais :: Vaginose bacteriana = Acinzentado, odor de peixe, pH > 4,5, clue cells | Tricomoníase = Amarelo-esverdeado, bolhoso, colo em framboesa | Candidíase = Branco grumoso, pH < 4,5, prurido
@F 🪱 Estrongiloidíase: risco no imunossuprimido?
= **Hiperinfecção** com corticoide/HTLV-1: sepse por Gram-negativos, pneumonite.
= Tratar empiricamente com **ivermectina** antes de imunossupressão em áreas endêmicas.
^ Revisões
@F 🦟 Doença de Chagas aguda: transmissão atual no Brasil?
= Principalmente **oral** (açaí, caldo de cana contaminados) na Amazônia.
- Febre, edema facial, miocardite
= **Benznidazol**.
^ Diretriz Brasileira de Chagas 2023
@F 🧫 Hanseníase: diagnóstico clínico?
= ≥ 1 sinal cardinal:
- Lesão com **alteração de sensibilidade**
- **Espessamento de nervo** periférico com alteração sensitiva/motora/autonômica
- Baciloscopia positiva
^ Ministério da Saúde 2022
@F 🐀 Hantavirose?
- Exposição rural a roedores, febre, mialgia
- Fase cardiopulmonar: **edema pulmonar não cardiogênico**, choque, hemoconcentração, plaquetopenia
= Suporte em UTI (não há antiviral).
^ Ministério da Saúde
@F 🧪 Febre maculosa brasileira?
- Exposição a **carrapato** (capivara, cavalo), febre, cefaleia, mialgia, exantema maculopapular (palmas/plantas)
- Alta letalidade
= **Doxiciclina** imediata (qualquer idade), sem esperar exames.
^ Ministério da Saúde
@F 🌀 Toxoplasmose aguda no imunocompetente?
= Linfadenopatia cervical, síndrome mono-like; autolimitada.
= Tratar: gestante, imunossuprimido, **coriorretinite**.
^ Revisões
@G 🦷 Infecção de prótese articular: princípios?
- Precoce (< 3 meses): desbridamento com retenção do implante (DAIR)
- Crônica: troca em 1 ou 2 tempos
- **Rifampicina** associada para estafilococos com implante
^ IDSA 2013
@G 🦠 Abscesso hepático piogênico × amebiano?
| | Piogênico | Amebiano
| Perfil | Idoso, doença biliar, DM | Jovem, viagem/área endêmica
| Lesões | Múltiplas | **Única**, lobo direito
| Tratamento | **Drenagem** + ATB | **Metronidazol** (drenagem raramente)
^ Revisões
@G 🧠 Encefalite herpética?
- Febre, alteração de comportamento, convulsões, afasia
- RM: **lobo temporal**
- PCR de HSV no LCR
= **Aciclovir IV** imediato (10 mg/kg 8/8 h, 14–21 dias).
^ IDSA 2008
@G 🦠 Infecção de cateter venoso central: quando remover?
- **S. aureus**, Pseudomonas, fungos, micobactérias
- Sepse grave, tromboflebite séptica, endocardite
- Bacteriemia persistente > 72 h
= Estafilococo coagulase-negativo: pode tentar lock + ATB em casos selecionados.
^ IDSA 2009
@H 💉 Vacina da dengue no Brasil?
= **Qdenga** (atenuada, 2 doses): SUS para **10–14 anos** em municípios prioritários; contraindicada em imunossuprimidos e gestantes.
^ Ministério da Saúde 2024
@H 🧪 Profilaxia de raiva pré-exposição?
= Veterinários, profissionais de laboratório, espeleólogos: **2 doses** (0 e 7) com sorologia de controle conforme risco.
^ Ministério da Saúde 2022
@H 🦠 Profilaxia de pneumocistose fora do HIV?
= Prednisona ≥ **20 mg/dia por ≥ 4 semanas** associada a outro imunossupressor, transplantes, rituximabe + corticoide, LLA → **SMX-TMP**.
^ Revisões
@H 🦠 Hepatite B e imunossupressão (rituximabe)?
= Rastrear HBsAg e **anti-HBc** antes.
- HBsAg + ou anti-HBc + com rituximabe: **profilaxia com entecavir/tenofovir** (risco de reativação alto)
^ AGA 2015; EASL 2025
"""
