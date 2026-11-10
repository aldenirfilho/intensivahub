TXT = r"""
@A 🔥 Síndrome de Lynch: rastreio e vigilância?
- Critérios de **Amsterdam II** / Bethesda; hoje: **IHQ de MMR ou MSI em todo câncer colorretal e de endométrio**
- Colonoscopia a cada **1–2 anos** a partir de 20–25 anos (conforme gene)
- **AAS 600 mg/dia** reduz câncer (CAPP2)
^ NCCN 2025
@A 🔥 BRCA1/2: condutas de redução de risco?
- RM de mama anual a partir de 25 anos + mamografia a partir de 30
- **Salpingo-ooforectomia** 35–40 (BRCA1) / 40–45 (BRCA2)
- Mastectomia bilateral redutora: opção
^ NCCN 2025
@A 🔥 Li-Fraumeni (TP53): cuidado peculiar?
= **Evitar radiação ionizante** (TC, RT quando possível) → rastreio com **RM de corpo inteiro** anual (protocolo Toronto).
^ NCCN
@B 🔥 Câncer de mama HR+/HER2− avançado: 1ª linha?
= **Inibidor de CDK4/6** (ribociclibe, palbociclibe, abemaciclibe) + inibidor de aromatase/fulvestranto.
- Via PI3K/AKT alterada (PIK3CA, AKT1, PTEN): alpelisibe, capivasertibe ou inavolisibe, conforme resistência endócrina
- HER2-low: **trastuzumabe deruxtecana**
^ NCCN 2025 · DESTINY-Breast04
@B 🔥 Trastuzumabe deruxtecana: toxicidade a vigiar?
= **Doença pulmonar intersticial/pneumonite** (pode ser fatal) → suspender e corticoide se ≥ grau 2.
^ FDA
@B 🔥 Câncer colorretal metastático: biomarcadores que mudam conduta?
| Biomarcador | Implicação |
| **RAS** mutado | **Anti-EGFR não funciona** |
| BRAF V600E | Encorafenibe + cetuximabe |
| **dMMR/MSI-H** | **Imunoterapia** (pembrolizumabe) 1ª linha |
| HER2 amplificado | Anti-HER2 |
| Lado direito | Pior resposta a anti-EGFR |
^ NCCN 2025
@B 🔥 Câncer de próstata: PSMA-PET e terapias?
- **PSMA-PET** para estadiamento de alto risco e recidiva bioquímica
- Resistente à castração: **lutécio-177-PSMA**, inibidores de PARP (BRCA)
^ EAU 2025 · VISION
@B 🔥 Carcinoma hepatocelular avançado: 1ª linha?
= **Atezolizumabe + bevacizumabe** (IMbrave150) ou durvalumabe + tremelimumabe (HIMALAYA).
! Antes do bevacizumabe: **EDA e tratar varizes** (sangramento).
^ BCLC 2022
@B 🔥 Câncer de rim metastático: 1ª linha?
= **Imunoterapia combinada**: pembrolizumabe + axitinibe/lenvatinibe, nivolumabe + ipilimumabe/cabozantinibe.
^ NCCN 2025
@B 🔥 Câncer de pulmão de pequenas células extenso: 1ª linha?
= Platina + etoposídeo + **anti-PD-L1** (atezolizumabe/durvalumabe); RT torácica selecionada; **tarlatamabe** (BiTE DLL3) em 2ª linha.
^ NCCN 2025
@C 🔥 Síndromes paraneoplásicas neurológicas: anticorpo → tumor?
| Anticorpo | Síndrome | Tumor |
| **Anti-Hu** | Neuronopatia sensitiva, encefalite límbica | Pequenas células |
| **Anti-Yo** | Degeneração cerebelar | **Ovário/mama** |
| Anti-Ri | Opsoclonus-mioclonus | Mama, pulmão |
| Anti-Ma2 | Encefalite límbica/tronco | **Testículo** |
| Anti-VGCC | Lambert-Eaton | Pequenas células |
^ PNS-Care 2021
% cmp Anticorpos paraneoplásicos :: Anti-Hu = Neuronopatia sensitiva · pequenas células | Anti-Yo = Cerebelo · ovário e mama | Anti-Ma2 = Encefalite · testículo
@C 🔥 Hipoglicemia por tumor não ilhota?
= Tumor mesenquimal grande (fibroso solitário) secreta **IGF-2** → insulina e peptídeo C **suprimidos**, razão IGF-2/IGF-1 > 10.
^ Endocrine Society
@C 🔥 CEA e CA 19-9: usos corretos?
= **Seguimento** (recidiva) e resposta — **não** para rastreio nem diagnóstico isolado.
! CA 19-9 indetectável em **Lewis-negativos** (~5–10%) e falso-positivo na colestase.
^ ASCO
@C 🔥 Dermatomiosite paraneoplásica: anticorpos de maior risco?
= **Anti-TIF1-γ** e anti-NXP2 → rastreio extenso (TC tórax/abdome/pelve, mamografia, CA-125/US transvaginal, colonoscopia).
^ IMACS 2023
"""
