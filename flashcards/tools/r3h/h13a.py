TXT = r"""
@A 🔥 Rastreio de osteoporose?
- **Mulher ≥ 65 anos** e pós-menopausa < 65 com risco (FRAX)
- Homem: evidência insuficiente (considerar ≥ 70 ou risco)
^ USPSTF 2025
@A 🔥 Rastreio de hepatite C e B no adulto?
- **HCV**: todo adulto 18–79 anos ao menos uma vez
- **HBV**: adultos em risco (CDC 2023: **todos ≥ 18 anos** uma vez com triplo painel)
^ USPSTF 2020 · CDC 2023
@A 🔥 Rastreio de diabetes (USPSTF)?
= **35–70 anos com sobrepeso/obesidade**; repetir a cada 3 anos se normal.
^ USPSTF 2021
@A 🔥 Rastreio de câncer de mama: mudança USPSTF 2024?
= Mamografia **bienal dos 40 aos 74 anos** (antes 50).
! No SUS (MS/INCA): 50–69 bienal; SBM/CBR recomendam a partir dos 40.
^ USPSTF 2024
@B 🔥 Vacina de hepatite B no adulto?
= **Universal 19–59 anos**; ≥ 60 com risco. Esquemas: 3 doses (0-1-6) ou **Heplisav-B 2 doses** (0-1).
- Anti-HBs pós-vacinal em profissional de saúde, dialítico, HIV
^ ACIP 2022
@B 🔥 Vacinas no esplenectomizado?
- Pneumocócica conjugada, **meningocócica ACWY + B**, Hib
- Influenza anual
= Idealmente **≥ 14 dias antes** da esplenectomia eletiva (ou ≥ 14 dias depois).
^ SBIm · ACIP
@C 🔥 Sensibilidade, especificidade e prevalência: o que muda com prevalência?
= **VPP e VPN** mudam com a prevalência; sensibilidade e especificidade **não** (propriedades do teste).
- Prevalência ↑ → VPP ↑, VPN ↓
^ Epidemiologia
@C 🔥 Razão de verossimilhança: interpretação?
| RV | Efeito |
| > 10 | Confirma fortemente |
| 5–10 | Moderado |
| 0,1–0,2 | Moderado para excluir |
| < 0,1 | Exclui fortemente |
= RV+ = sens/(1 − esp); RV− = (1 − sens)/esp.
^ Sackett
% zones Razão de verossimilhança :: < 0,1 = Exclui fortemente | 0,1–0,5 = Pequeno a moderado | 1 = Inútil | 2–10 = Moderado a forte | > 10 = Confirma fortemente
@C 🔥 Viés de imortalidade (immortal time)?
= Em estudos observacionais, o grupo "tratado" ganha tempo em que **não podia morrer** antes de receber o tratamento → superestima benefício.
= Evitar com análise landmark ou exposição tempo-dependente.
^ Suissa 2008
@C 🔥 NNT × NNH: como calcular?
= **NNT = 1/RRA**; NNH = 1/aumento absoluto de risco do evento adverso.
- Exemplo: 10% → 7,5% = RRA 2,5% → NNT **40**
^ Epidemiologia
@C 🔥 Análise de sobrevida: hazard ratio × risco relativo?
= HR é a **razão das taxas instantâneas** ao longo do tempo (assume proporcionalidade); RR compara riscos acumulados em um ponto.
- Curvas que se cruzam: HR enganoso → usar RMST
^ Epidemiologia
@C 🔥 Metanálise: heterogeneidade I²?
= **I² > 50%**: heterogeneidade substancial → efeitos aleatórios, investigar fontes; **funnel plot** assimétrico sugere viés de publicação.
^ Cochrane
@D 🔥 Prevenção quaternária: definição?
= Evitar **sobrediagnóstico e sobretratamento** (iatrogenia) — ex.: rastreios sem benefício, exames de rotina desnecessários.
^ Jamoulle"""
