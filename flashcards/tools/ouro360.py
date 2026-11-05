"""🧩 Números de ouro 360X — lacunas (cloze) de doses, alvos e cortes; complementa as 42 do Grok sem repeti-las."""
import json, sys
OUT = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/app2"
T = {  # subtema: [(frente cloze, extra, fonte)]
"🫁 Ventilação e via aérea": [
 ("Driving pressure (Pplatô − PEEP total) associada a menor mortalidade na SDRA: abaixo de {{c1::15 cmH2O}}.", "Mediação estatística, não meta randomizada.", "Amato, NEJM 2015"),
 ("Mechanical power associado a maior mortalidade acima de cerca de {{c1::17 J/min}}.", "Integra VT, FR, pressões e fluxo.", "Serpa Neto, ICM 2018"),
 ("Teste de respiração espontânea: PSV de {{c1::5–8 cmH2O}} ou tubo T por {{c2::30–120 minutos}}.", "PSV 15 não é TRE.", "Consensos de desmame"),
 ("Drive respiratório alto quando a P0.1 passa de {{c1::3,5–4 cmH2O}}.", "P0.1 < 1 sugere sedação/suporte excessivos.", "Telias et al."),
 ("Teste de vazamento do balonete: vazamento abaixo de {{c1::110 mL}} sugere edema laríngeo.", "Corticoide horas antes de extubar no alto risco.", "Miller & Cole, Chest 1996"),
 ("Definição global de SDRA: CNAF com fluxo ≥ {{c1::30 L/min}} e S/F ≤ {{c2::315}} com SpO₂ ≤ {{c3::97%}}.", "SpO₂ 100% invalida o S/F.", "Matthay, AJRCCM 2023"),
 ("EOLIA: mortalidade em 60 dias de {{c1::35%}} com ECMO-VV versus {{c2::46%}} no controle.", "p = 0,09; cruzamento de 28% para ECMO.", "Combes, NEJM 2018"),
 ("Ultrassom do diafragma: excursão < {{c1::10 mm}} ou fração de espessamento < {{c2::30%}} prediz falha de desmame.", "Refinamento, não substitui o TRE.", "POCUS de desmame"),
],
"🫀 Hemodinâmica e vasoativos": [
 ("Elevação passiva das pernas positiva: aumento de débito/VS ≥ {{c1::10%}}.", "Medir fluxo, não pressão.", "Monnet & Teboul"),
 ("VPP prediz resposta a volume se > {{c1::12–13%}}, com VT ≥ {{c2::8 mL/kg}}, ritmo sinusal e sem esforço.", "Com VT 6: tidal volume challenge.", "Fisiologia coração-pulmão"),
 ("Fluid challenge clássico: {{c1::250–500 mL}} de cristaloide em {{c2::10–15 minutos}}, com reavaliação.", "Sem meta de reavaliação não é teste.", "Cecconi, ICM 2014"),
 ("ScvO₂ alvo ≥ {{c1::70%}}; gap venoarterial de CO₂ > {{c2::6 mmHg}} sugere fluxo insuficiente.", "ScvO₂ alta não prova perfusão na sepse.", "Fisiologia do transporte de O₂"),
 ("Tempo de enchimento capilar normal: ≤ {{c1::3 segundos}}.", "ANDROMEDA-SHOCK.", "Hernández, JAMA 2019"),
 ("Choque cardiogênico (SHOCK): PAS < 90 com índice cardíaco < {{c1::2,2 L/min/m²}}; cardiac power output < {{c2::0,6 W}} prediz morte.", "CPO = PAM × DC / 451.", "SHOCK trial; Fincke 2004"),
 ("SSC sugere acrescentar vasopressina quando a noradrenalina estiver em {{c1::0,25–0,5 µg/kg/min}}.", "Dose fixa 0,03 U/min.", "SSC 2021/2026"),
 ("Hidrocortisona no choque séptico: iniciar com noradrenalina ≥ {{c1::0,25 µg/kg/min}} por pelo menos {{c2::4 horas}}.", "200 mg/dia.", "SSC 2021"),
 ("VTI da via de saída do VE normal: cerca de {{c1::18–22 cm}}.", "VS = VTI × área da VSVE.", "Ecocardiografia"),
 ("VCI < {{c1::2,1 cm}} com colapso > {{c2::50%}} estima PAD em torno de 3 mmHg.", "Mente com PEEP alta e PIA alta.", "ASE"),
 ("TAPSE abaixo de {{c1::17 mm}} sugere disfunção sistólica do VD.", "Integrar S' e FAC.", "ASE/EACVI"),
 ("Escore de ultrassom pulmonar (LUS): 12 regiões × 0–3 = máximo de {{c1::36}} pontos.", "Útil para seguir aeração.", "Consenso LUS"),
],
"🦠 Sepse e antimicrobianos": [
 ("Vancomicina no MRSA grave: alvo de AUC24/MIC de {{c1::400–600}}.", "Preferível ao vale isolado.", "ASHP/IDSA 2020"),
 ("Piperacilina-tazobactam em infusão estendida: cada dose correndo em {{c1::4 horas}}.", "Sempre após dose de ataque.", "Lodise 2007; SSC"),
 ("Amicacina em dose única diária: {{c1::15–20 mg/kg}}; alvo de pico/MIC ≥ {{c2::8–10}}.", "Ajuste de intervalo pela função renal.", "PK/PD de aminoglicosídeos"),
 ("Procalcitonina para suspender: queda ≥ {{c1::80%}} do pico ou valor < {{c2::0,5 ng/mL}}.", "Ajuda a parar, não a começar.", "SAPS, Lancet ID 2016"),
 ("Duração da PAV na maioria dos casos: {{c1::7 dias}}.", "Inclusive não fermentadores, se boa resposta.", "IDSA/ATS 2016"),
 ("Bacteremia por S. aureus não complicada: mínimo de {{c1::14 dias}} de terapia IV.", "Complicada: 4–6 semanas.", "IDSA MRSA 2011"),
 ("Sepse com lactato inicial elevado: remedir em {{c1::2–4 horas}}.", "Queda orienta a ressuscitação; não perseguir normalização a qualquer custo.", "SSC"),
],
"⚡ PCR e arritmias": [
 ("RCP de qualidade: {{c1::100–120}} compressões/min, profundidade de {{c2::5–6 cm}}.", "Fração de compressão > 80%.", "AHA 2025"),
 ("EtCO₂ < {{c1::10 mmHg}} após 20 minutos de RCP com via aérea avançada indica prognóstico muito ruim.", "Nunca critério isolado.", "AHA"),
 ("Desfibrilação bifásica: {{c1::120–200 J}} conforme o fabricante (ou carga máxima).", "Choque único, retomar RCP.", "AHA"),
 ("Cardioversão sincronizada: FA {{c1::120–200 J}}; flutter e TSV {{c2::50–100 J}} (bifásico).", "Sincronizar sempre.", "AHA"),
 ("Adenosina na TSV: {{c1::6 mg}} em bolus rápido; se falhar, {{c2::12 mg}}.", "Flush de 20 mL.", "AHA"),
 ("TV monomórfica estável: amiodarona {{c1::150 mg}} IV em 10 minutos.", "Depois 1 mg/min por 6 h.", "AHA"),
 ("TEP alto risco: alteplase {{c1::100 mg}} IV em {{c2::2 horas}}.", "Na PCR: bolus 50 mg.", "ESC 2019; AHA/ACC 2026"),
 ("IAM com supra: porta-balão ≤ {{c1::90 minutos}}; porta-agulha ≤ {{c2::30 minutos}}.", "Transferência: até 120 min.", "AHA/ACC; ESC"),
],
"🧠 Neurointensivismo": [
 ("TCE grave: tratar PIC acima de {{c1::22 mmHg}}; PPC alvo de {{c2::60–70 mmHg}}.", "BTF 4ª edição.", "BTF 2016"),
 ("Manitol {{c1::0,25–1 g/kg}}; segurar se osmolaridade > {{c2::320 mOsm/kg}}.", "No hipotenso, salino hipertônico.", "Neurocrítico"),
 ("HIP espontânea: PAS alvo de cerca de {{c1::140 mmHg}} (faixa 130–150), evitando < 130.", "INTERACT2/ATACH-2.", "AHA/ASA 2022"),
 ("HSA antes de tratar o aneurisma: PAS < {{c1::160 mmHg}} é razoável.", "Depois, nimodipino e euvolemia.", "AHA/ASA 2023"),
 ("Tenecteplase no AVC: {{c1::0,25 mg/kg}} em bolus, máximo {{c2::25 mg}}.", "Alternativa à alteplase.", "AHA/ASA; ensaios AcT e EXTEND-IA TNK"),
 ("Trombectomia na oclusão de grande vaso anterior: até {{c1::24 horas}} em selecionados por imagem.", "DAWN/DEFUSE-3.", "AHA/ASA"),
 ("Midazolam IM no estado de mal (> 40 kg): {{c1::10 mg}}.", "RAMPART.", "Silbergleit, NEJM 2012"),
 ("Morte encefálica (CFM 2.173): temperatura > {{c1::35 °C}}, SpO₂ > 94% e PAS ≥ 100 ou PAM ≥ 65; teste de apneia positivo com PaCO₂ > {{c2::55 mmHg}}.", "Dois exames clínicos + complementar.", "Resolução CFM 2.173/2017"),
],
"💧 Rim, eletrólitos e ácido-base": [
 ("Hipercalemia: insulina regular {{c1::10 U}} IV com {{c2::25 g}} de glicose.", "Efeito em 15–30 min; vigie hipoglicemia.", "Consensos de hipercalemia"),
 ("Hiponatremia grave sintomática (europeia): NaCl 3% {{c1::150 mL}} em 20 minutos, até 2–3 vezes.", "Meta: +5 mmol/L na 1ª hora.", "ESE/ESICM/ERA 2014"),
 ("Hipernatremia crônica: correção máxima de {{c1::10–12 mmol/L}} em 24 h.", "Aguda (< 48 h) pode ser mais rápida.", "Diretrizes de disnatremia"),
 ("KCl IV: até {{c1::10 mEq/h}} em veia periférica e até {{c2::20 mEq/h}} em central com monitor.", "Nunca em bolus.", "Prática de reposição"),
 ("Alcalose metabólica: PaCO₂ esperada = {{c1::0,7 × HCO₃ + 21}} (± 2).", "Winter é só para acidose metabólica.", "Regras de Boston"),
 ("Acidose respiratória: HCO₃ sobe {{c1::1}} (aguda) ou {{c2::4}} (crônica) a cada 10 mmHg de PaCO₂.", "Alcalose respiratória: cai 2 e 5.", "Regras de Boston"),
 ("Gap osmolar anormal: acima de {{c1::10 mOsm/kg}}.", "Pense em metanol e etilenoglicol.", "Toxicologia"),
 ("Anticoagulação com citrato: razão cálcio total/iônico > {{c1::2,5}} sugere acúmulo de citrato.", "Comum na falência hepática.", "KDIGO CRRT"),
 ("Hipofosfatemia grave: fósforo abaixo de {{c1::1 mg/dL}}.", "Reponha IV.", "Síndrome de realimentação"),
],
"🩸 Sangue, nutrição e antídotos": [
 ("Plaqueta: profilática < {{c1::10 mil}}; procedimento/sangramento < {{c2::50 mil}}; neurocirurgia < {{c3::100 mil}}.", "Punção lombar em geral ≥ 40–50 mil.", "AABB/ICTMG; prática transfusional"),
 ("Fibrinogênio: repor no sangramento abaixo de {{c1::150 mg/dL}} (1,5 g/L).", "Crioprecipitado ou concentrado.", "Diretriz europeia de trauma 2023"),
 ("Reversão de varfarina com sangramento grave: CCP 4F {{c1::25–50 UI/kg}} conforme INR + vitamina K {{c2::10 mg}} IV.", "Plasma só sem CCP.", "ACC 2020; ASH"),
 ("Idarucizumabe para dabigatrana: {{c1::5 g}} IV.", "Duas ampolas de 2,5 g.", "RE-VERSE AD"),
 ("Protamina: {{c1::1 mg}} para cada 100 U de heparina não fracionada das últimas 2–3 h.", "Máximo de 50 mg.", "Farmacologia"),
 ("Plasma fresco: {{c1::10–15 mL/kg}}.", "Não corrige INR levemente alterado.", "AABB"),
 ("Proteína no crítico: {{c1::1,2–2,0 g/kg/dia}}.", "Progressão gradual.", "ASPEN 2022"),
 ("Wernicke: tiamina {{c1::500 mg}} IV 3×/dia.", "Antes da glicose no risco.", "EFNS 2010"),
 ("Emulsão lipídica 20% na intoxicação por anestésico local: bolus de {{c1::1,5 mL/kg}}.", "Depois 0,25 mL/kg/min.", "ASRA 2020"),
 ("Glucagon na intoxicação por betabloqueador: {{c1::3–10 mg}} IV em bolus.", "Vômito é comum.", "Toxicologia"),
 ("Naloxona no paciente com respiração: {{c1::0,04–0,4 mg}} IV titulada.", "Evita abstinência abrupta.", "Toxicologia"),
 ("Organofosforado: atropina {{c1::1–2 mg}} IV, dobrando a cada 5 minutos até secar a secreção.", "Alvo: pulmão seco, não pupila.", "Eddleston, Lancet 2008"),
 ("Tricíclico com QRS > {{c1::100 ms}}: bicarbonato de sódio {{c2::1–2 mEq/kg}} em bolus.", "Alvo de pH 7,45–7,55.", "Toxicologia"),
 ("Paracetamol: dose aguda potencialmente tóxica ≥ {{c1::150 mg/kg}}.", "Nomograma a partir de 4 h.", "Rumack-Matthew"),
],
}
R3 = {
"🩺 Endócrino e metabolismo": [
 ("Pré-diabetes (ADA): jejum {{c1::100–125 mg/dL}}, HbA1c {{c2::5,7–6,4%}} ou TOTG 2 h {{c3::140–199 mg/dL}}.", "", "ADA 2026"),
 ("CAD (consenso 2024): beta-hidroxibutirato ≥ {{c1::3 mmol/L}}, pH < {{c2::7,3}} e/ou HCO₃ < {{c3::18 mmol/L}}.", "Glicose ≥ 200 ou diabetes prévio.", "Consenso hiperglicêmico 2024"),
 ("EHH (consenso 2024): glicose ≥ {{c1::600 mg/dL}} e osmolalidade efetiva > {{c2::300 mOsm/kg}}.", "Sem cetose/acidose importantes.", "Consenso hiperglicêmico 2024"),
 ("Hipoglicemia: nível 1 < {{c1::70 mg/dL}}; nível 2 < {{c2::54 mg/dL}}; nível 3 = precisa de ajuda.", "", "ADA"),
 ("Metformina contraindicada com TFGe < {{c1::30}}; não iniciar entre 30 e 45.", "Ajustar dose de 30–45.", "ADA / FDA"),
 ("Hiperparatireoidismo assintomático vai à cirurgia se cálcio > {{c1::1 mg/dL}} acima do LSN ou idade < {{c2::50}} anos.", "Também osteoporose, litíase, ClCr < 60.", "Quinto workshop internacional 2022"),
 ("Osteoporose densitométrica: T-score ≤ {{c1::−2,5}}.", "Fratura por fragilidade também define.", "OMS"),
 ("Insuficiência adrenal: cortisol das 8 h < {{c1::3–5 µg/dL}} confirma; acima de cerca de {{c2::15 µg/dL}} torna improvável.", "Varia com o ensaio.", "Endocrine Society"),
 ("Incidentaloma adrenal com densidade ≤ {{c1::10 UH}} na TC sem contraste: adenoma rico em lípides.", "Ainda pesquisar secreção.", "ESE 2023"),
],
"🫀 Cardio e pulmão": [
 ("Meta pressórica na maioria dos adultos hipertensos: < {{c1::130/80 mmHg}}.", "", "AHA/ACC 2025; SBC"),
 ("LDL no muito alto risco: < {{c1::55 mg/dL}} e redução ≥ {{c2::50%}}.", "", "ESC/EAS 2019; SBC"),
 ("IC aguda improvável com BNP < {{c1::100 pg/mL}} ou NT-proBNP < {{c2::300 pg/mL}}.", "Obesidade reduz BNP.", "ESC 2021"),
 ("Fenótipos de IC: reduzida ≤ {{c1::40%}}; levemente reduzida {{c2::41–49%}}; preservada ≥ 50%.", "", "Definição universal de IC"),
 ("CDI na prevenção primária: FE ≤ {{c1::35%}} apesar de terapia otimizada; TRC com BRE e QRS ≥ {{c2::150 ms}}.", "", "ESC/AHA"),
 ("DPOC (GOLD): VEF1/CVF pós-broncodilatador < {{c1::0,70}}.", "", "GOLD 2026"),
 ("Reversibilidade na asma (GINA): VEF1 ↑ ≥ {{c1::12%}} e ≥ {{c2::200 mL}}.", "", "GINA"),
 ("Oxigênio domiciliar: PaO₂ ≤ {{c1::55 mmHg}} ou SpO₂ ≤ {{c2::88%}} em repouso, estável.", "56–59 com cor pulmonale/policitemia.", "GOLD"),
 ("Hipertensão pulmonar: PAPm > {{c1::20 mmHg}}; pré-capilar com POAP ≤ 15 e RVP > {{c2::2 UW}}.", "", "ESC/ERS 2022"),
 ("Critérios de Light: proteína P/S > {{c1::0,5}}, LDH P/S > {{c2::0,6}} ou LDH pleural > {{c3::2/3}} do LSN sérico.", "Um basta para exsudato.", "Light 1972"),
 ("Derrame parapneumônico com pH < {{c1::7,20}}: drenar.", "Pus dispensa pH.", "BTS 2023"),
 ("Hipoventilação da obesidade: IMC ≥ {{c1::30}} e PaCO₂ diurna ≥ {{c2::45 mmHg}}.", "HCO₃ < 27 torna improvável.", "ATS 2019"),
],
"🦠 Gastro, infecto, hemato e nefro": [
 ("FIB-4 < {{c1::1,3}} = baixo risco de fibrose avançada; > {{c2::2,67}} = alto risco.", "Acima de 65 anos o corte baixo sobe para 2,0.", "AASLD/EASL"),
 ("Glasgow-Blatchford de {{c1::0–1}} permite manejo ambulatorial da HDA.", "", "ESGE 2021"),
 ("Paracentese > {{c1::5 L}}: albumina {{c2::6–8 g}} por litro retirado.", "", "AASLD 2021"),
 ("Inclusão na lista de transplante hepático: MELD ≥ {{c1::15}}.", "", "AASLD"),
 ("Esofagite eosinofílica: ≥ {{c1::15}} eosinófilos por campo de grande aumento.", "Biopsiar níveis diferentes.", "AGA 2020"),
 ("Hepatite C curada: RNA indetectável {{c1::12 semanas}} após o fim do tratamento.", "Cirrótico segue vigiando CHC.", "AASLD/IDSA"),
 ("Vigilância de CHC no cirrótico: ultrassom ± AFP a cada {{c1::6 meses}}.", "", "AASLD 2023"),
 ("Sífilis: resposta adequada = queda de {{c1::4 vezes}} (duas diluições) no VDRL.", "1:32 → 1:8.", "CDC 2021; MS"),
 ("Infecção latente por TB (MS): PPD ≥ {{c1::5 mm}} indica tratamento nos grupos elegíveis.", "IGRA alternativo.", "Manual MS 2019"),
 ("Neurotoxoplasmose provável: CD4 < {{c1::100}} + IgG positiva + lesões com realce anelar.", "Profilaxia com SMX-TMP.", "NIH OI"),
 ("Ferropenia: ferritina < {{c1::30 ng/mL}}; na IC, < 100 ou 100–299 com saturação < {{c2::20%}}.", "", "ESC 2023; AGA"),
 ("PTT: PLASMIC ≥ {{c1::6}} = alta probabilidade; ADAMTS13 < {{c2::10%}} confirma.", "Plasmaférese não espera o exame.", "ISTH 2020"),
 ("TIH: escore 4Ts de {{c1::6–8}} = alta probabilidade.", "0–3 = baixa.", "ASH 2018"),
 ("SIADH: Na urinário > {{c1::30 mmol/L}} e osmolalidade urinária > {{c2::100 mOsm/kg}} com plasma hipotônico.", "Euvolêmico.", "ESE 2014"),
 ("DRC: alteração por ≥ {{c1::3 meses}}; albuminúria A3 > {{c2::300 mg/g}}.", "", "KDIGO 2024"),
 ("Gota: ácido úrico alvo < {{c1::6 mg/dL}} (< 5 com tofos).", "", "ACR 2020"),
],
}
idx = json.load(open(f"{OUT}/data/index.json"))
idx["decks"] = [d for d in idx["decks"] if d["colecao"] != "ouro"]
idx["colecoes"] = [c for c in idx["colecoes"] if c["id"] != "ouro"]
tot = 0
for root, data, fn in (("TEMI 2028", T, "ouro-temi.json"), ("R3 Clínica Médica", R3, "ouro-r3.json")):
    cards = [{"subtema": s, "frente": f, "verso": x, "pegadinha": "", "fonte": src + " · ✍️ Claude 360X", "tags": ["OURO", "cloze"]}
             for s, lst in data.items() for (f, x, src) in lst]
    json.dump({"formato": "codice360x-v1", "baralho": f"🧩 Números de ouro 360X::{root}", "midia": {}, "cards": cards}, open(f"{OUT}/data/decks/{fn}", "w"), ensure_ascii=False)
    idx["decks"].append({"colecao": "ouro", "arquivo": f"data/decks/{fn}", "tema": f"🧩 {root}", "cards": len(cards), "subtemas": list(data)})
    tot += len(cards); print(root, len(cards), "notas", sum(f.count("{{c") for s in data.values() for (f, _, _) in s), "lacunas")
idx["colecoes"].insert(0, {"id": "ouro", "nome": "Números de ouro 360X", "icone": "🧩", "cards": tot})
json.dump(idx, open(f"{OUT}/data/index.json", "w"), ensure_ascii=False)
