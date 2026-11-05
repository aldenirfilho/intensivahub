"""Correções manuais da curadoria IAs 360X (chave = 'tema#índice do conceito'; 'd' = card de aprofundamento; 'x' = extra)."""
DONE = {"01", "02", "03", "04", "05"}
V1, V2, V3, V4, V5 = "01 Ventilação mecânica", "02 Assincronias", "03 Estratégias ventilatórias", "04 SDRA e oxigenação", "05 Via aérea e suporte"
FIX = {
    f"{V1}#0": {"img": "vm_vcv_curvas.png", "nota": "Resistência = (Ppico − Pplatô)/fluxo em L/s. Gradiente pico-platô > 10 cmH₂O sugere problema de via aérea/tubo."},
    f"{V1}#1": {"img": "vm_equacao.png"},
    f"{V1}#3": {"nota": "3 τ ≈ 95% e 5 τ ≈ 99% de esvaziamento. DPOC: R alta + C alta → τ longo → precisa de Te longo."},
    f"{V1}#4": {"img": "vm_autopeep.png"},
    f"{V1}#7": {"img": "vm_transpulmonar.png"},
    f"{V2}#0": {"img": "vm_assincronias.png"},
    f"{V2}#5": {"img": "vm_assincronias.png", "nota": "Duplo disparo pode quase dobrar o VT efetivo (VT empilhado) → volutrauma mesmo com VT programado de 6 mL/kg."},
    f"{V2}#8": {"nota": "P0.1 > 3,5–4 cmH₂O = drive alto; < 1 = drive baixo (sedação/suporte excessivos)."},
    f"{V3}#0": {"img": "vm_vcv_pcv.png"},
    f"{V3}#3": {"nota": "ARDSNet 2000: VT 6 × 12 mL/kg PBW → mortalidade 31% × 39,8%. Alvos: platô ≤ 30 e ΔP ≤ 15."},
    f"{V3}#5": {"img": "vm_desmame.png"},
    f"{V3}#6": {"DECIDIR": "Integrar à clínica; o RSBI isolado não deve atrasar nem substituir o TRE", "nota": "Corte clássico: f/VT > 105 = alta chance de falha (Yang & Tobin 1991)."},
    f"{V3}#7": {"DIFERENCIAR": "Edema laríngeo (estridor) × broncoespasmo × secreção com tosse fraca × EAP de desmame × fraqueza muscular"},
    f"{V4}#0": {"nota": "Definição global 2023/2024: aceita CNAF ≥ 30 L/min, SpO₂/FiO₂ ≤ 315 (SpO₂ ≤ 97%) e USG pulmonar como imagem."},
    f"{V4}#4": {"DIFERENCIAR": "Prona acordado em CNAF e decúbito lateral: outros cenários — não extrapolar o benefício do PROSEVA",
                "nota": "PROSEVA (2013): prona ≥ 16 h/dia em P/F < 150 → mortalidade em 28 dias 16% × 32,8%."},
    f"{V4}#5": {"DIFERENCIAR": "↑ FiO₂ melhora V/Q baixo mas não recruta; PEEP recruta, porém pode sobredistender e ↑ pós-carga do VD",
                "img": "vm_peep_tabela.png", "nota": "ART (2017): recrutamento máximo com PEEP alta ↑ mortalidade → evitar manobras prolongadas de rotina."},
    f"{V4}#6": {"nota": "Shunt > 30% praticamente não responde a ↑ FiO₂ → precisa de PEEP/recrutamento/prona."},
    f"{V5}#6": {"img": "vm_vni_cnaf.png", "nota": "ROX = (SpO₂/FiO₂)/FR: ≥ 4,88 em 2, 6 ou 12 h = baixo risco; < 3,85 em 12 h = alto risco de falha."},
}
DROP = {f"{V5}#x0"}   # duplicava o aprofundamento do corpo estranho
EXTRA = {}
