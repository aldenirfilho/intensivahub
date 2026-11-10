TXT = r"""
@A 🔥 Classificação de Chicago 4.0: acalasia tipos?
| Tipo | Padrão | Melhor resposta |
| I | Aperistalse sem pressurização | Dilatação/POEM/Heller |
| II | **Pressurização panesofágica** | Melhor prognóstico a qualquer terapia |
| III | **Espástica** (contrações prematuras) | **POEM** (miotomia longa) |
^ Chicago 4.0 (2021)
% cmp Acalasia (Chicago 4.0) :: Tipo I = Aperistalse · dilatação/Heller/POEM | Tipo II = Pressurização · melhor resposta | Tipo III = Espástica · POEM
@A 🔥 Gastrite atrófica autoimune: riscos?
= Anti-célula parietal/anti-fator intrínseco → **deficiência de B12 e ferro**, hipergastrinemia → **tumor neuroendócrino gástrico tipo 1** e adenocarcinoma.
= EDA de vigilância a cada 3 anos (AGA).
^ AGA 2021
@A 🔥 H. pylori refratário: 2ª e 3ª linhas?
- Falha da claritromicina → **quádrupla com bismuto** 14 dias
- Falha da quádrupla → **levofloxacino** (se sensível) ou rifabutina
- **Vonoprazana** aumenta erradicação (dupla com amoxicilina)
! Teste de controle ≥ 4 semanas após, sem IBP por 2 semanas.
^ Maastricht VI 2022 · ACG 2024
@A 🔥 Síndrome de Zollinger-Ellison: diagnóstico?
= Úlceras múltiplas/atípicas + diarreia: **gastrina > 10× o normal com pH gástrico < 2** (suspender IBP com cautela).
- Teste de secretina se duvidoso; 20–25% associados a **NEM 1**
^ ENETS
@B 🔥 Hemorragia digestiva com anticoagulante: reintroduzir quando?
= Após hemostasia, **reintroduzir em ~7 dias** (menos trombose e morte, sem excesso de ressangramento).
- AAS em prevenção secundária: não suspender ou retomar em até 3–5 dias
^ ESGE 2021 · ACG 2022
@B 🔥 Sangramento de varizes gástricas fúndicas (GOV2/IGV1)?
= **Cianoacrilato** endoscópico ou **BRTO**; TIPS como resgate.
^ Baveno VII · AASLD 2024
@B 🔥 Sangramento de intestino delgado: investigação?
= EDA + colonoscopia normais → **cápsula endoscópica** (ou angioTC se ativo) → enteroscopia para terapia.
- Causa mais comum > 40 anos: **angiodisplasia** (Heyde, DRC, Willebrand)
^ ACG 2015
@C 🔥 Retocolite grave aguda: escore e resgate?
- Critérios de **Truelove-Witts**; corticoide IV
- **Dia 3** sem resposta (> 8 evacuações ou 3–8 + PCR > 45, escore de Oxford) → resgate: **infliximabe** ou ciclosporina, ou colectomia
! Rastrear CMV (biópsia) e C. difficile.
^ ECCO 2022
% flow RCU aguda grave :: Internar + corticoide IV + profilaxia TEV >> Excluir C. difficile e CMV >> Dia 3: avaliar resposta (Oxford) >> Sem resposta: infliximabe ou ciclosporina >> Falha em 5–7 dias: colectomia
@C 🔥 Doença de Crohn: fatores de mau prognóstico?
- Diagnóstico **< 30 anos**, doença perianal, ileal extensa, estenose/fístula, úlceras profundas
- Tabagismo, cirurgia prévia
= Indicam biológico precoce (top-down).
^ ECCO 2024
@C 🔥 Vedolizumabe × ustequinumabe × risanquizumabe: mecanismos?
| Droga | Alvo |
| Vedolizumabe | Integrina **α4β7** (seletivo do intestino) |
| Ustequinumabe | IL-12/23 (p40) |
| Risanquizumabe, mirikizumabe, guselkumabe | **IL-23 (p19)** |
| Tofacitinibe, upadacitinibe | JAK |
^ ECCO 2024
@C 🔥 Diarreia por ácidos biliares?
= Pós-colecistectomia ou ressecção ileal, diarreia aquosa → **teste SeHCAT** ou C4 sérico; responde a **colestiramina**.
^ BSG 2018
"""
