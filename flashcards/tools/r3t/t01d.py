TXT = r"""
@A 🧂 Diuréticos tiazídicos: qual preferir na HAS?
= **Clortalidona** e **indapamida** (tiazídico-like): meia-vida longa, evidência em desfechos (ALLHAT, HYVET).
! Hidroclorotiazida 12,5–25 mg tem menor potência anti-hipertensiva.
^ Diretriz Brasileira de HAS 2020
@A 🫘 Hipertensão renovascular: quando suspeitar?
- HAS de início < 30 anos (displasia fibromuscular) ou > 55 grave
- **Piora da creatinina > 30%** após IECA/BRA
- EAP súbito recorrente ("flash")
- Sopro abdominal, assimetria renal > 1,5 cm
^ AHA
@B 🫀 Ivabradina na IC: indicação?
= ICFEr sintomática, FEVE ≤ 35%, **ritmo sinusal com FC ≥ 70** apesar de betabloqueador em dose máxima tolerada (SHIFT).
! Só funciona em ritmo sinusal (inibe corrente If do nó sinusal).
^ SHIFT 2010; ESC 2021
@B 💊 Hidralazina + nitrato na IC?
= ICFEr em **afrodescendentes** (A-HeFT) ou intolerância a IECA/BRA/ARNI (DRC avançada, hipercalemia).
^ A-HeFT 2004; ESC 2021
@B 💊 Digoxina na IC: papel atual?
= Reduz **hospitalizações**, não mortalidade (DIG); útil para controle de FC na FA com IC.
- Nível alvo 0,5–0,9 ng/mL
^ DIG 1997
@C 🧪 Troponina ultrassensível: algoritmo 0/1 h?
= Valores muito baixos na admissão ou sem variação em 1 h → **exclusão** (VPN > 99%).
= Valor alto ou variação significativa → **inclusão** (IAM).
= Zona intermediária: repetir em 3 h.
^ ESC 2023 SCA
% flow Algoritmo 0/1 h da troponina ultrassensível :: Troponina na chegada (0 h) >> Muito baixa ou sem variação em 1 h: exclui IAM >> Alta ou variação significativa: confirma IAM >> Zona intermediária: repetir em 3 h e reavaliar
@C 🫀 Choque cardiogênico pós-IAM: medidas com evidência?
- **Revascularização precoce** da artéria culpada (SHOCK)
- Apenas a culpada na ICP (CULPRIT-SHOCK)
- Noradrenalina como vasopressor
- Impella CP em IAMCSST selecionado (DanGer Shock 2024)
! Balão intra-aórtico de rotina sem benefício (IABP-SHOCK II).
^ ESC 2023
@C 🧬 Infarto do VD: tratamento?
- **Volume** cauteloso (pré-carga dependente)
- **Evitar nitratos e diuréticos**
- Manter sincronia AV (tratar BAV)
- Reperfusão precoce
^ ESC 2023
@D 🫀 Fibrilação atrial: controle de frequência agudo?
| FEVE | Opções
| > 40% | Betabloqueador, **diltiazem/verapamil**, digoxina
| ≤ 40% | Betabloqueador (cautela), **amiodarona**, digoxina
! Não usar BCC não di-hidropiridínico na ICFEr.
^ ESC 2024
@D ⚡ Taquicardia de QRS largo: critério mais simples?
= Na dúvida, tratar como **TV**, sobretudo com cardiopatia estrutural.
- Pistas de TV: dissociação AV, batimentos de captura/fusão, concordância precordial, eixo extremo
! Verapamil em TV pode causar colapso.
^ Brugada 1991; AHA 2020
@D 🧠 Escore HAS-BLED?
- **H**AS não controlada
- **A**lteração renal/hepática (1 cada)
- **S**troke prévio
- **B**leeding (sangramento prévio/predisposição)
- **L**abile RNI
- **E**lderly (> 65)
- **D**rogas (antiagregante/AINE) ou álcool (1 cada)
= ≥ 3: alto risco → **corrigir fatores**, não contraindicar anticoagulação.
^ ESC 2024
@E 🔊 Manobras e sopros: regra geral?
| Manobra | Efeito na maioria dos sopros
| Inspiração | ↑ sopros **direitos** (Rivero-Carvallo)
| Valsalva/em pé | ↓ (exceto **CMH** e **prolapso mitral**, que aumentam)
| Agachamento | ↑ (exceto CMH e prolapso)
| Handgrip | ↑ regurgitações (IM, IAo), ↓ EAo
^ Semiologia
@F 🍳 Lipídios: Friedewald e quando não usar?
= **LDL = CT − HDL − TG/5**.
= Inválido com TG > 400 → LDL direto ou equação de Martin/Sampson.
= Coleta **sem jejum** é aceita na maioria dos casos.
^ SBC 2017/2025
@F 💓 Atividade física recomendada no adulto?
= **150–300 min/semana** de atividade moderada (ou 75–150 vigorosa) + **fortalecimento muscular 2×/semana**.
^ OMS 2020
@G 🩸 Dissecção de aorta: classificação de Stanford?
| Tipo | Acometimento | Conduta
| A | **Aorta ascendente** | **Cirurgia** de emergência
| B | Apenas descendente (após subclávia esquerda) | Clínico; endovascular se complicada
= Controle: FC < 60 e PAS 100–120 (**esmolol** primeiro, depois vasodilatador).
^ ESC 2024 aorta
% cmp Dissecção aórtica (Stanford) :: Tipo A = Aorta ascendente. Cirurgia de emergência | Tipo B = Só descendente. Tratamento clínico; endovascular se complicada
@G 🌬️ Embolia pulmonar: estratificação de risco?
| Risco | Critério | Conduta
| Alto | **Instabilidade** | Trombólise
| Intermediário-alto | PESI alto + VD disfunção + troponina | Anticoagular, monitorar (resgate)
| Intermediário-baixo | 1 ou nenhum desses | Anticoagular
| Baixo | sPESI 0 | Alta precoce possível
^ ESC 2019
% zones Estratificação do TEP (ESC) :: Baixo = sPESI 0, alta precoce | Intermediário-baixo = VD ou troponina | Intermediário-alto = VD + troponina | Alto = Instabilidade, trombólise
@G 🦵 Isquemia aguda de membro: 6 Ps?
- **P**ain (dor), **P**allor (palidez), **P**ulselessness
- **P**arestesia, **P**aralisia, **P**oiquilotermia
= Heparina IV + avaliação vascular imediata (embolectomia/trombólise).
! Paralisia e perda sensitiva = membro ameaçado.
^ ESC 2024
"""
