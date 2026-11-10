TXT = r"""
@A 🔥 Estadiamento KDIGO da LRA?
| Estágio | Creatinina | Diurese |
| 1 | 1,5–1,9× basal ou ↑ ≥ 0,3 mg/dL em 48 h | < 0,5 mL/kg/h por 6–12 h |
| 2 | 2,0–2,9× | < 0,5 por ≥ 12 h |
| 3 | ≥ 3× ou ≥ 4,0 mg/dL ou TRS | < 0,3 por ≥ 24 h ou anúria ≥ 12 h |
^ KDIGO 2012
@A 🔥 Teste de estresse com furosemida?
= Furosemida **1 mg/kg** (1,5 se já usava): diurese **< 200 mL em 2 h** prediz progressão para LRA estágio 3/necessidade de diálise.
^ Chawla 2013
@A 🔥 Nefropatia por cilindros (rim do mieloma)?
- LRA + **gap proteico/Bence-Jones**; fita urinária pouco positiva (não detecta cadeia leve)
- Cadeias leves livres séricas **> 1.500 mg/L** sugerem (< 500 torna improvável)
= Tratar o mieloma rápido (bortezomibe + dexametasona); evitar AINE, contraste, desidratação.
^ IMWG
@A 🔥 Nefropatia por ácido aristolóquico/ervas e nefrite intersticial crônica: pista?
= DRC com **sedimento pobre, proteinúria baixa**, anemia desproporcional e risco de **carcinoma urotelial**.
^ KDIGO
@A 🔥 Síndrome cardiorrenal tipo 1: manejo?
= Piora renal na IC aguda geralmente por **congestão venosa** (não hipoperfusão): descongestionar mesmo com creatinina subindo.
! "Piora da função renal" com descongestão eficaz **não** tem pior prognóstico.
^ ESC 2021
@A 🔥 LRA associada a vancomicina + piperacilina-tazobactam?
= Combinação associada a **mais LRA** que vancomicina + cefepime/meropenem; usar **AUC-guided** (400–600) para vancomicina.
^ IDSA/ASHP 2020
@B 🔥 KDIGO 2024: estratificação de risco da DRC?
= Matriz **TFG (G1–G5) × albuminúria (A1 < 30, A2 30–300, A3 > 300 mg/g)**.
- Calculadora **KFRE** para risco de falência renal em 2 e 5 anos (encaminhar se > 3–5% em 5 anos)
^ KDIGO 2024
% zones Albuminúria (RAC) :: A1 < 30 mg/g = Normal a leve | A2 30–300 mg/g = Moderadamente aumentada | A3 > 300 mg/g = Gravemente aumentada
@B 🔥 iSGLT2 na DRC: limite de TFG para iniciar?
= Iniciar com **TFG ≥ 20** (com ou sem DM) e manter até diálise (DAPA-CKD, EMPA-KIDNEY).
! Queda inicial de TFG até 30% é esperada (hemodinâmica) — não suspender.
^ KDIGO 2024
@B 🔥 Hipercalemia limitando IECA/BRA na DRC?
= Usar **patiromer** ou **ciclossilicato de zircônio** para manter o bloqueio do SRAA, dieta orientada, corrigir acidose.
! Suspender IECA por K⁺ leve é erro comum.
^ KDIGO 2024
@B 🔥 Anemia da DRC: quando iniciar AEE e meta?
= Iniciar se **Hb < 10** após repor ferro (ferritina > 100 / TSAT > 20%); meta **10–11,5**, não > 13.
- Inibidores de HIF (roxadustate, daprodustate): alternativa oral
^ KDIGO
@C 🔥 Nefropatia membranosa: anti-PLA2R e conduta?
= **Anti-PLA2R** positivo em ~70% (primária); título acompanha atividade.
- Risco baixo: IECA/BRA e observação 6 meses
- Moderado/alto: **rituximabe** (MENTOR) ou ciclofosfamida + corticoide
! Anti-PLA2R negativo: buscar câncer, lúpus (classe V), hepatite B, drogas.
^ KDIGO 2021
@C 🔥 GESF primária × secundária (adaptativa)?
| | Primária | Secundária |
| Síndrome nefrótica completa | **Sim** (albumina baixa, edema) | Geralmente não |
| Apagamento de podócitos | **Difuso** | Segmentar |
| Causas | Fator circulante | Obesidade, nefrectomia, HIV, refluxo, genética (APOL1) |
= Só a primária recebe imunossupressão.
^ KDIGO 2021
@C 🔥 Nefropatia por IgA: tratamento atual?
- Proteinúria > 0,5–1 g/dia: **IECA/BRA máximo + iSGLT2**
- Alto risco persistente: **budesonida de liberação entérica**, **sparsentan** (dual endotelina/AT1)
^ KDIGO 2024 · PROTECT · NefIgArd
@C 🔥 GN membranoproliferativa: classificação moderna?
- **Mediada por imunocomplexo**: hepatite C (crioglobulinemia), LES, infecção crônica, gamopatia
- **Glomerulopatia C3** (complemento alternativo): C3 baixo, C4 normal
^ KDIGO 2021
@C 🔥 Nefrite lúpica classe III/IV: indução atual?
- Micofenolato ou ciclofosfamida em baixa dose (Euro-Lupus) + corticoide
- Terapia tripla: + **belimumabe** (BLISS-LN) ou + **voclosporina** (AURORA)
- Hidroxicloroquina para todos
^ KDIGO 2024
@C 🔥 SHU atípica: suspeita e tratamento?
= MAT (anemia hemolítica, plaquetopenia, LRA) com **ADAMTS13 > 10%** e sem STEC → desregulação do complemento.
= **Eculizumabe/ravulizumabe**; vacinar contra meningococo.
^ KDIGO 2017
% cmp Microangiopatias trombóticas :: PTT = ADAMTS13 < 10% · plasmaférese + caplacizumabe | SHU-STEC = Diarreia sanguinolenta · suporte | SHU atípica = Complemento · eculizumabe
@C 🔥 Doença anti-MBG: quando NÃO tratar?
= **Dependente de diálise na apresentação + 100% crescentes + sem hemorragia pulmonar** → recuperação renal improvável (risco > benefício).
^ KDIGO 2021
@C 🔥 Glomerulonefrite associada a infecção estafilocócica?
= IgA dominante, em **idoso diabético** com infecção ativa (pele, endocardite); complemento pode estar baixo.
= Tratar a infecção; **não** imunossuprimir.
^ KDIGO 2021
"""
