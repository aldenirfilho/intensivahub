TXT = r"""
@D 🫁 Diagnóstico de tuberculose pulmonar no Brasil?
- **Teste rápido molecular (TRM-TB)**: detecta TB e resistência à **rifampicina**
- Baciloscopia (2 amostras) onde não há TRM
- **Cultura** com teste de sensibilidade (retratamento, HIV, populações vulneráveis)
^ Manual de TB MS 2019/2024
@D 💊 Esquema básico de TB e efeitos de cada droga?
| Droga | Efeito característico
| Rifampicina | Urina/suor laranja, interações (CYP), hepatite, plaquetopenia
| Isoniazida | **Neuropatia periférica** (dar piridoxina), hepatite
| Pirazinamida | **Hiperuricemia**, artralgia, hepatite
| Etambutol | **Neurite óptica** (cores)
= 2 RIPE + 4 RI (6 meses); meníngea e osteoarticular: 2 RIPE + 10 RI.
^ Manual de TB MS 2019
% cmp Efeitos adversos do RIPE :: Rifampicina = Fluidos laranja, interações, hepatite | Isoniazida = Neuropatia periférica (piridoxina), hepatite | Pirazinamida = Hiperuricemia, artralgia, hepatite | Etambutol = Neurite óptica
@D 🧪 Hepatotoxicidade do RIPE: conduta?
= Suspender o esquema se:
- ALT/AST > **5× LSN** sem sintomas
- > **3× LSN** com sintomas ou icterícia
= Reintroduzir sequencialmente após normalizar: **rifampicina + etambutol** → isoniazida → pirazinamida.
^ Manual de TB MS 2019
@D 🔬 TB latente: quem tratar?
- PPD ≥ 5 mm ou IGRA + em: **HIV**, contatos, imunossupressão, anti-TNF, transplante, alterações fibróticas no RX
- PPD ≥ 10 mm: conversão recente, diabetes, silicose, DRC dialítica
= Esquemas: **3HP** (isoniazida + rifapentina semanal, 12 doses), 4R ou 6–9H.
^ Manual de TB MS 2024
@D 🫙 TB pleural: diagnóstico?
- Exsudato **linfocítico**, ADA > 40
- Baciloscopia do líquido raramente positiva
- **Biópsia pleural**: granuloma caseoso
- Poucas células mesoteliais (< 5%)
^ Manual de TB MS 2019
@D 🧠 TB meníngea: pontos-chave?
- Subaguda, paralisia de pares cranianos (VI), hidrocefalia
- LCR: linfócitos, **glicose muito baixa**, proteína alta, ADA ↑
- Tratamento 12 meses + **corticoide** (dexametasona)
^ Manual de TB MS 2019
@E 🧪 Sífilis: interpretação de testes?
| Treponêmico | Não treponêmico (VDRL) | Interpretação
| + | + | Sífilis ativa (ou recente tratada)
| + | − | Cicatriz sorológica, sífilis muito recente ou tardia
| − | + | Falso-positivo (gestação, LES, SAF)
^ PCDT IST 2022
@E 💉 Tratamento da sífilis por estágio?
| Estágio | Tratamento
| Recente (primária, secundária, latente < 1 ano) | **Penicilina benzatina 2,4 MUI** dose única
| Tardia (latente > 1 ano/indeterminada, terciária) | 2,4 MUI semanal por **3 semanas**
| Neurossífilis | Penicilina cristalina IV 14 dias
= Controle: VDRL trimestral; queda de **2 diluições** em 6 meses = resposta.
^ PCDT IST 2022
% zones Sífilis: tratamento pelo estágio :: Recente < 1 ano = Benzatina 2,4 MUI dose única | Tardia ou indeterminada = Benzatina 2,4 MUI semanal x 3 | Neurossífilis = Cristalina IV por 14 dias
@E 🔴 Úlceras genitais: diferencial?
| Doença | Úlcera | Linfonodo
| Sífilis primária | **Indolor**, endurada, única | Indolor
| Herpes | **Dolorosas**, múltiplas vesículas | Doloroso
| Cancroide | Dolorosa, base purulenta | Supurativo
| Linfogranuloma venéreo | Pequena, transitória | **Bubão**, fístula
| Donovanose | Indolor, sangrante, "vermelho-carne" | Pseudobubão
^ PCDT IST 2022
% cmp Úlceras genitais :: Sífilis = Indolor, endurada, única. Benzatina | Herpes = Dolorosas, vesículas múltiplas. Aciclovir | Cancroide = Dolorosa, purulenta, bubão. Azitromicina | Linfogranuloma = Bubão com fístula. Doxiciclina 21 dias
@E 💧 Uretrite: tratamento sindrômico?
= **Ceftriaxona 500 mg IM** dose única (gonococo) + **azitromicina 1 g** VO (clamídia).
= Alternativa para clamídia: doxiciclina 7 dias.
- Tratar parcerias
^ PCDT IST 2022
@E 🧬 HPV: vacinação no Brasil?
= Dose única para meninos e meninas de **9–14 anos** (desde 2024), com faixas ampliadas e esquemas para imunossuprimidos.
^ Ministério da Saúde 2024
@F 🦟 Dengue: classificação e grupos de manejo?
| Grupo | Critério | Manejo
| A | Sem sinal de alarme, sem risco | Hidratação oral, casa
| B | Comorbidade/risco social ou prova do laço + | Hemograma, observação
| C | **Sinais de alarme** | Hidratação IV, internação
| D | **Choque**/sangramento grave | UTI, 20 mL/kg em 20 min
^ Ministério da Saúde 2024
% zones Dengue: grupos de manejo :: Grupo A = Sem alarme. Hidratação oral | Grupo B = Risco ou sangramento de pele. Hemograma | Grupo C = Sinais de alarme. Soro IV, internação | Grupo D = Choque. UTI
@F 🚨 Sinais de alarme da dengue?
- Dor abdominal **intensa e contínua**
- Vômitos persistentes
- Acúmulo de líquidos (ascite, derrame)
- Hipotensão postural, lipotimia
- Hepatomegalia > 2 cm
- Sangramento de mucosa
- Letargia/irritabilidade
- **Aumento progressivo do hematócrito**
^ Ministério da Saúde 2024
@F 🦟 Chikungunya × dengue × Zika?
| | Dengue | Chikungunya | Zika
| Febre | Alta | Alta | Baixa/ausente
| Artralgia | Moderada | **Intensa, incapacitante, crônica** | Leve
| Exantema | 3º–6º dia | 2º–5º dia | **Precoce, pruriginoso**
| Conjuntivite | Rara | Rara | **Frequente**
| Gravidade | Choque/plasma | Artrite crônica | Microcefalia, Guillain-Barré
^ Ministério da Saúde
@F 🐀 Leptospirose: quadro e tratamento?
- Exposição a enchente/esgoto
- Febre, **mialgia de panturrilha**, sufusão conjuntival
- Síndrome de Weil: icterícia rubínica, LRA **hipocalêmica**, hemorragia pulmonar
= Leve: doxiciclina; grave: **penicilina cristalina** ou ceftriaxona.
^ Ministério da Saúde
@F 🦟 Malária: tratamento por espécie no Brasil?
| Espécie | Tratamento
| P. vivax | Cloroquina + **primaquina** (ou tafenoquina) — cura radical dos hipnozoítos
| P. falciparum não grave | Artemeter-lumefantrina + primaquina dose única
| Grave (qualquer) | **Artesunato IV**
! Primaquina: pesquisar **G6PD** e contraindicada na gestação.
^ Guia de Malária MS 2021
@F 🪱 Esquistossomose mansônica?
- Hepatoesplenomegalia, **hipertensão portal pré-sinusoidal** com função hepática preservada
- Fibrose de Symmers; varizes
- Mielorradiculopatia
= **Praziquantel**.
^ Ministério da Saúde
@F 🪳 Leishmaniose visceral (calazar)?
- Febre prolongada, **esplenomegalia volumosa**, pancitopenia, hipergamaglobulinemia
- Diagnóstico: rK39, aspirado de medula
= **Anfotericina B lipossomal** (1ª escolha no Brasil em grupos de risco) ou antimonial.
^ Ministério da Saúde
@F 🐕 Raiva: profilaxia pós-exposição?
= Depende do animal e do tipo de lesão:
- Cão/gato observável sadio: **observar 10 dias**
- Lesão grave ou animal suspeito/silvestre/morcego: **vacina + soro/imunoglobulina**
- Lavar o ferimento com água e sabão abundante
^ Ministério da Saúde 2022
@F 🧫 Febre amarela: pontos de prova?
- Bifásica; icterícia, hemorragia, LRA; **sinal de Faget** (bradicardia relativa)
- Transaminases muito altas (AST > ALT)
= Vacina atenuada: **contraindicada** em imunossuprimidos e gestantes (avaliar risco).
^ Ministério da Saúde
@F 🧪 Histoplasmose × paracoccidioidomicose?
| | Histoplasmose | Paracoccidioidomicose
| Exposição | Cavernas, morcegos, aves | **Trabalhador rural**, tabagista
| Clínica | Pneumonia, disseminada no HIV | Lesões orais (estomatite moriforme), pulmão, adrenal
| Tratamento | Itraconazol; anfotericina se grave | Itraconazol ou SMX-TMP
^ Revisões
"""
