"""Gera a coleção 🧪 Gasometria 360X: 13 baralhos (450 cards), casos guiados (data/gaso.json) e manifesto.
4.14.0: baralhos 11–13 (VM, POCUS, venosa/gap CO₂/inotrópicos) com etapas extras; os baralhos 1–10 saem idênticos à 4.13.0.
Uso: python3 build_gaso.py <APP_DIR>
"""
import importlib, json, os, random, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from gaso_cards import render
from gaso_engine import analyze, panel, NOME, r0

APP = sys.argv[1]
ROOT = "🧪 Gasometria 360X"
FONTE = ("Síntese 360X de fisiologia ácido-base e de diretrizes consagradas (ADA/CAD, SSC, Berlim/SDRA, KDIGO, toxicologia clínica) — conferir na diretriz vigente. "
         "Caso e valores fictícios, coerentes por Henderson-Hasselbalch e conferidos pelo motor de gasometria 360X — não é paciente real.")
FONTE2 = ("Síntese 360X de fisiologia e de diretrizes/estudos consagrados (ARDSNet/SDRA, EOLIA, SSC 2021, protocolos BLUE/RUSH/VExUS, literatura de gap CO₂ e ScvO₂) — conferir na diretriz vigente. "
          "Caso e valores fictícios, coerentes por Henderson-Hasselbalch e conferidos pelo motor de gasometria 360X — não é paciente real.")
THEMES = []
for i in range(1, 14):
    m = importlib.import_module(f"g{i:02d}")
    THEMES.append(getattr(m, f"T{i:02d}"))
assert len(THEMES) == 13 and all(len(c) == (30 if i < 10 else 50) for i, (_, c) in enumerate(THEMES)), [len(c) for _, c in THEMES]

slug = lambda s: re.sub(r"[^a-z0-9]+", "-", s.lower().encode("ascii", "ignore").decode()).strip("-")[:40]
OPC_PH = ["Acidemia (pH &lt; 7,35)", "Alcalemia (pH &gt; 7,45)", "pH na faixa normal (7,35–7,45)"]
OPC_PRIM = ["Acidose metabólica", "Alcalose metabólica", "Acidose respiratória", "Alcalose respiratória", "pH normal: distúrbio misto (ou nenhum) — não há 'primário' isolado"]
PRIM_I = {"AM": 0, "ALM": 1, "AR": 2, "ALR": 3}

n = 0; decks = []; manifest = []; casos = []; seen_dx = set(); all_dx = set(); all_dx2 = set()
pre = []
for t_i, (tit, cards) in enumerate(THEMES, 1):
    for c in cards:
        if c["kind"] == "caso":
            d = analyze(c["lab"])["dx"]; all_dx2.add(d)
            if t_i <= 10: all_dx.add(d)   # pool antigo: casos 1–10 ficam idênticos à 4.13.0
all_dx = sorted(all_dx); all_dx2 = sorted(all_dx2)
for t_i, (tit, cards) in enumerate(THEMES, 1):
    out = []
    for c in cards:
        n += 1
        fr, vs, R = render(c, n)
        dx = c["dx"]
        assert dx not in seen_dx, f"diagnóstico repetido: {dx}"; seen_dx.add(dx)
        for k in ("cond", "peg"):
            assert c.get(k), f"#{n} campo vazio {k}"
        fonte = FONTE if t_i <= 10 else FONTE2
        card = {"frente": fr, "verso": vs, "pegadinha": c["peg"], "fonte": fonte, "tags": ["GASO", f"GASO_T{t_i:02d}", "TEMI2028", "R3CM"]}
        out.append(card)
        manifest.append(dict(n=n, baralho=f"{ROOT}::{tit}", frente=fr, verso=vs, pegadinha=c["peg"], fonte=fonte, tags=card["tags"]))
        if c["kind"] != "caso":
            continue
        # -------- caso guiado (aba 🧪 Gaso) --------
        steps = []
        s0 = R["steps"]
        ph = R["lab"]["ph"]
        steps.append(dict(p="1️⃣ O pH indica…", o=OPC_PH, c=0 if ph < 7.35 else 1 if ph > 7.45 else 2, e=s0[0]))
        cprim = 4 if R["side"] == "nl" else PRIM_I[R["prim"]]
        steps.append(dict(p="2️⃣ Qual o distúrbio primário?", o=OPC_PRIM, c=cprim, e=s0[1] if len(s0) > 1 else ""))
        codes = set(R["codes"]); comp = next((s for s in s0 if s.startswith(("Winter", "PaCO₂ esperada", "HCO₃⁻ esperado"))), "")
        if R["side"] != "nl" and comp:
            if R["prim"] in ("AM", "ALM"):
                o = ["Adequada (distúrbio simples)", "Insuficiente → acidose respiratória associada", "Excessiva → alcalose respiratória associada"]
                cc = 1 if "AR" in codes else 2 if "ALR" in codes else 0
            elif R["prim"] == "AR":
                o = ["Aguda", "Crônica (compensada)", "Crônica agudizada", "Com distúrbio metabólico associado"]
                cc = 0 if "AR_A" in codes else 1 if "AR_C" in codes else 2 if "AR_CA" in codes else 3
            else:
                o = ["Aguda", "Crônica (compensada)", "Com distúrbio metabólico associado"]
                cc = 0 if "ALR_A" in codes else 1 if "ALR_C" in codes else 2
            steps.append(dict(p="3️⃣ Compensação / cronicidade?", o=o, c=cc, e=comp))
        if R.get("ag") is not None:
            o = ["AG normal (sem acidose com AG alto)", "AG elevado — acidose com AG alto pura", "AG elevado + acidose hiperclorêmica associada", "AG elevado + alcalose metabólica associada"]
            if "AM_AG" not in codes: cc = 0
            elif "AM_HC" in codes: cc = 2
            elif "ALM" in codes: cc = 3
            else: cc = 1
            e = " · ".join(s for s in s0 if s.startswith(("AG =", "Δ/Δ", "AG elevado com")))
            steps.append(dict(p="4️⃣ Ânion gap (corrigido) e Δ/Δ?", o=o, c=cc, e=e))
        if R["lab"].get("pao2") is not None:
            fi = R["lab"].get("fio2") or 0.21
            if fi <= 0.21 + 1e-6:
                o = ["Oxigenação adequada", "Hipoxemia com A-a NORMAL (hipoventilação ou PiO₂ baixa)", "Hipoxemia com A-a ELEVADO (V/Q, shunt, difusão)"]
                cc = 0 if R["lab"]["pao2"] >= 80 else 1 if R["aa"] <= R["aa_exp"] + 2 else 2
            else:
                o = ["P/F &gt; 300", "P/F 201–300 (leve)", "P/F 101–200 (moderada)", "P/F ≤ 100 (grave)"]
                pf = R["pf"]; cc = 0 if pf > 300 else 1 if pf > 200 else 2 if pf > 100 else 3
            steps.append(dict(p="🫁 Oxigenação?", o=o, c=cc, e=s0[-1]))
        # -------- 4.14.0: etapas automáticas de VM e venosa --------
        X, xs = R.get("x", {}), R.get("xsteps", [])
        pick = lambda key: next((t for t in xs if key in t), "")
        if "gapet" in X:
            steps.append(dict(p="🫁 Gap PaCO₂ − EtCO₂?", o=["2–5 mmHg: normal", "&gt; 5 mmHg: espaço morto aumentado"], c=1 if X["gapet"] > 5 else 0, e=pick("Gap PaCO₂ − EtCO₂")))
        if "frn" in X:
            vm = R["lab"]["vm"]; ok = r0(X["frn"]); cand = [ok, r0(vm["fr"] * vm["alvo"] / R["lab"]["pco2"]), r0(vm["fr"]), r0(X["frn"] * 1.4)]
            opts = []
            for o in cand:
                if o not in opts: opts.append(o)
            k = 1
            while len(opts) < 4:
                o = r0(X["frn"] + 4 * k)
                if o not in opts: opts.append(o)
                k += 1
            rr = random.Random(n * 31); rr.shuffle(opts)
            steps.append(dict(p="⚙️ FR para atingir a PaCO₂ alvo (VC mantido)?", o=[f"{o} irpm" for o in opts], c=opts.index(ok), e=pick("FR para PaCO₂ alvo")))
        if "gapco2" in X:
            steps.append(dict(p="🩸 Gap CO₂ venoarterial (Pcv−aCO₂)?", o=["≤ 6 mmHg: fluxo adequado para o metabolismo", "&gt; 6 mmHg: fluxo (débito) insuficiente"], c=1 if X["gapco2"] > 6 else 0, e=pick("Gap CO₂ (Pcv")))
        ve = R["lab"].get("ven") or {}
        if ve.get("sat") is not None and ve.get("kind", "central") != "periferica":
            sv = ve["sat"]; nm = "SvO₂" if ve.get("kind") == "mista" else "ScvO₂"
            steps.append(dict(p=f"🩸 {nm} {sv}%?", o=["&lt; 70%: extração aumentada (oferta baixa para o consumo)", "70–80%: faixa-alvo", "&gt; 80%: extração baixa (fluxo alto ou falha de extração)"],
                              c=0 if sv < 70 else 2 if sv > 80 else 1, e=" · ".join(t for t in (pick(f"{nm} {sv}"), pick("gap CO₂/Ca−vO₂")) if t)))
        rnd = random.Random(n * 7919)
        wrong = [d for d in (all_dx if t_i <= 10 else all_dx2) if d != R["dx"]]
        # distratores "vizinhos": compartilham algum componente com a resposta
        near = [d for d in wrong if any(NOME[c] in d for c in codes)]
        pool = (rnd.sample(near, min(2, len(near))) if near else [])
        pool += rnd.sample([d for d in wrong if d not in pool], 3 - len(pool))
        opts = pool + [R["dx"]]; rnd.shuffle(opts)
        steps.append(dict(p="✅ Diagnóstico ácido-base final?", o=opts, c=opts.index(R["dx"]), e=R["dx"]))
        for p_, o_, c_, e_ in c.get("x", []):
            steps.append(dict(p=p_, o=o_, c=c_, e=e_))
        casos.append(dict(n=n, t=t_i, deck=tit, ctx=c["ctx"], steps=steps, dx=dx, causa=c["causa"], cond=c["cond"], peg=c["peg"],
                          lab={k: v for k, v in R["lab"].items() if k not in ("be",) and v is not None}, codes=R["codes"]))
    arq = f"data/decks/gaso-{t_i:02d}-{slug(tit[3:])}.json"
    json.dump({"formato": "codice360x-v1", "baralho": f"{ROOT}::{tit}", "cards": out}, open(f"{APP}/{arq}", "w"), ensure_ascii=False, indent=0)
    decks.append(dict(colecao="gaso", arquivo=arq, tema=tit, cards=len(out), subtemas=[tit]))

json.dump({"formato": "codice360x-gaso-v1", "casos": casos}, open(f"{APP}/data/gaso.json", "w"), ensure_ascii=False, separators=(",", ":"))
json.dump(dict(decks=decks, cards=manifest), open(os.path.join(HERE, "gaso_manifest.json"), "w"), ensure_ascii=False, indent=0)
print("baralhos:", len(decks), "cards:", n, "casos guiados:", len(casos), "· gaso.json", os.path.getsize(f"{APP}/data/gaso.json") // 1024, "KB")
