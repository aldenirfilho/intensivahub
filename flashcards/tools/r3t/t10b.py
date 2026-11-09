TXT = r"""
@A 🧬 Testagem genética germinativa: quem encaminhar?
- Câncer de mama < 45–50 anos, triplo-negativo, masculino, bilateral
- **Ovário** (qualquer idade), pâncreas, próstata metastático
- Colorretal/endométrio com **instabilidade de microssatélites** (Lynch)
- Familiares com mutação conhecida
^ NCCN 2025
@A 🍷 Álcool e câncer?
= Associado a câncer de boca, faringe, laringe, **esôfago (escamoso)**, fígado, colorretal e **mama** — sem dose segura.
^ OMS/IARC
@B 🎗️ Câncer de mama: subtipos e terapia-alvo?
| Subtipo | Terapia
| RH+/HER2− (luminal) | **Hormonioterapia** (tamoxifeno, inibidor de aromatase) ± inibidor de CDK4/6
| HER2+ | **Trastuzumabe**, pertuzumabe, T-DXd
| Triplo-negativo | Quimioterapia, imunoterapia, sacituzumabe, PARP (BRCA)
^ NCCN 2025
% cmp Câncer de mama por subtipo :: Luminal RH+ HER2- = Hormonioterapia ± inibidor de CDK4/6 | HER2+ = Trastuzumabe, pertuzumabe, T-DXd | Triplo-negativo = Quimioterapia, imunoterapia, PARP se BRCA
@B 💊 Tamoxifeno × inibidores de aromatase: efeitos?
| Tamoxifeno | Inibidores de aromatase
| **TEV**, câncer de **endométrio** | **Osteoporose**, artralgia
| Fogachos | Fogachos, dislipidemia
| Pré e pós-menopausa | Só pós-menopausa (ou supressão ovariana)
^ Revisões
@B 🎗️ Câncer de próstata metastático: base do tratamento?
= **Privação androgênica** (análogo de GnRH ou orquiectomia) + intensificação (abiraterona, enzalutamida, darolutamida, docetaxel).
! Flare com agonista GnRH: antiandrógeno nas primeiras semanas.
^ NCCN 2025
@B 🎗️ Câncer de cabeça e pescoço: HPV?
= Orofaringe HPV+: **não fumantes**, jovens, **melhor prognóstico**.
= Tabaco/álcool: laringe, boca, hipofaringe.
^ NCCN 2025
@C 🧪 Hipoglicemia tumoral (tumores não ilhotas)?
= Grandes tumores mesenquimais/fibroso solitário produzindo **IGF-2**: insulina e peptídeo C **baixos**.
^ Revisões
@C 🧠 Degeneração cerebelar paraneoplásica?
= Ataxia subaguda com anticorpos **anti-Yo** (mama, ovário) ou anti-Hu (pequenas células).
^ Revisões
@D 🩸 Hiperleucocitose/leucostase?
= Leucócitos > 100 mil (LMA) com dispneia, hipoxemia, confusão, AVC.
= **Hidroxiureia**, quimioterapia urgente, hidratação; leucaférese em casos selecionados.
! Evitar transfusão de hemácias (↑ viscosidade).
^ Revisões
@D 🫀 Tamponamento neoplásico?
= Derrame pericárdico maligno (pulmão, mama, linfoma): **pericardiocentese** + janela pericárdica se recorrente.
^ ESC 2015
@D 🧪 Hipercalcemia da malignidade: mecanismos?
| Mecanismo | Tumor
| **PTHrp** (humoral, 80%) | Escamosos, mama, rim
| Osteólise local | Mieloma, mama
| Calcitriol | **Linfomas**
| PTH ectópico | Raro
^ Revisões
@E 💉 Extravasamento de quimioterápico vesicante?
= Parar infusão, aspirar, **não lavar**; antraciclina: **dexrazoxano**; compressas frias (antraciclinas) ou quentes (alcaloides da vinca).
^ ESMO-EONS 2012
@E 🩹 Síndrome mão-pé?
= Eritrodisestesia palmoplantar com **capecitabina**, 5-FU, doxorrubicina lipossomal, multiquinases.
= Reduzir dose, emolientes, ureia tópica.
^ Revisões
@E 🧪 Colite por inibidor de checkpoint: manejo?
| Grau | Conduta
| 1 | Sintomático, manter
| 2 | Suspender; **prednisona 1 mg/kg**
| 3–4 | Metilprednisolona IV; refratário: **infliximabe** ou vedolizumabe
^ ASCO 2021
@E 🧠 Fadiga oncológica: abordagem?
- Tratar anemia, hipotireoidismo, depressão, dor, insônia
- **Exercício** (maior evidência)
- Metilfenidato em casos selecionados
^ NCCN 2025
"""
