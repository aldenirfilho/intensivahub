"""Importa o baralho do Grok (TEMI 2028 + R3 CM, 303 notas) como coleção 'grok' — lido por inteiro e corrigido."""
import sqlite3, json, os, re, shutil, sys
SRC = "/home/claude/imp/grok"; OUT = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/app2"
# (índice da nota, campo, antigo, novo)
FIX = [
 (9, 7, None, "Driving pressure usa a PEEP <b>total</b> (extrínseca + auto-PEEP). Calcular com a PEEP programada quando há auto-PEEP <b>superestima</b> a driving pressure real."),
 (67, 7, "Linha zolidá", "Linezolida"),
 (77, 6, "SpO2 em torno de 92–98%", "SpO2 90–98% (AHA 2025; ERC/ESICM 2025 preferem 94–98%)"),
 (121, 6, "Winter: PaCO2 esperada = <b>62</b> (faixa 60 a 64). PaCO2 medida = 46. Delta-delta (AG − 12 + HCO3) = <b>38</b>.",
  "Winter <b>não se aplica</b> à alcalose. PaCO2 esperada = 0,7 × HCO3 + 21 = <b>46,2</b> (± 2). PaCO2 medida = 46 → compensação adequada."),
 (121, 6, "A PaCO2 subiu em torno de 0,5–0,7 mmHg para cada 1 mEq de HCO3 acima de 24, então a compensação está plausível.",
  "A PaCO2 sobe ~0,7 mmHg por 1 mEq de HCO3 acima de 24: compensação plausível."),
 (122, 6, "Winter: PaCO2 esperada = <b>57,5</b> (faixa 55,5 a 59,5). PaCO2 medida = 60. Delta-delta (AG − 12 + HCO3) = <b>28</b>.",
  "Distúrbio primário respiratório (Winter não se aplica). HCO3 esperado crônico = 24 + 4 × 2 = <b>32</b> → 33 compatível. pH esperado ~7,34; pH 7,40 sugere leve alcalose metabólica associada (diurético?)."),
 (123, 6, "Winter: PaCO2 esperada = <b>47</b> (faixa 45 a 49). PaCO2 medida = 60. Delta-delta (AG − 12 + HCO3) = <b>24</b>.",
  "Distúrbio primário respiratório (Winter não se aplica). HCO3 esperado agudo = 24 + 1 × 2 = <b>26</b> → compatível."),
 (130, 6, "Água corporal = 0,5 × 60 = <b>27 L</b>", "Água corporal = 0,45 × 60 = <b>27 L</b>"),
 (142, 6, "36 / 0,2 =", "36 / 0,25 ="),
 (143, 6, "18 / 0,5 =", "18 / 0,45 ="),
 (167, 6, "etiomilato", "etomidato"),
 (175, 6, " Sulfato? Não.", ""),
 (207, 6, "Brugarda", "Brugada"),
]
def slug(s): 
    import unicodedata
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")
c = sqlite3.connect(f"{SRC}/collection.anki2")
models = {int(k): v for k, v in json.loads(c.execute("select models from col").fetchone()[0]).items()}
decknames = json.loads(c.execute("select decks from col").fetchone()[0])
nid2did = {}
for nid, did in c.execute("select nid, did from cards"): nid2did.setdefault(nid, did)
media = json.load(open(f"{SRC}/media")); os.makedirs(f"{OUT}/data/media", exist_ok=True)
for k, v in media.items(): shutil.copy(f"{SRC}/{k}", f"{OUT}/data/media/grok_{v}")
notes = c.execute("select id, mid, flds, tags from notes order by id").fetchall()
used = set()
decks = {}
for i, (nid, mid, flds, tags) in enumerate(notes):
    f = flds.split("\x1f")
    for (j, fi, old, new) in FIX:
        if j != i: continue
        if old is None: f[fi] = new
        else:
            assert old in f[fi], (i, old); f[fi] = f[fi].replace(old, new)
        used.add((j, old))
    dn = decknames[str(nid2did[nid])]["name"]
    root, tema = dn.split("::")[0], dn.split("::")[-1]
    root = "TEMI 2028" if root.startswith("TEMI") else "R3 Clínica Médica"
    key = (root, tema)
    tg = ["GROK"] + tags.split()
    if "Cloze" in models[mid]["name"]:
        card = {"subtema": "🧩 Números de ouro", "frente": f[0], "verso": f[1], "pegadinha": "", "fonte": f[2] + " · ✅ revisado por Claude", "tags": tg}
    else:
        img = f[9].strip()
        dica = f"<div class=src>💡 {f[5]}</div>" if f[5].strip() else ""
        card = {"subtema": f[1], "frente": f"{f[2]} {f[4]}", "verso": f[6] + dica, "pegadinha": f[7], "fonte": f[8] + " · ✅ revisado por Claude", "tags": tg}
        if img: card["imagem"] = "grok_" + img
    decks.setdefault(key, []).append(card)
assert len(used) == len(FIX), len(used)
idx = json.load(open(f"{OUT}/data/index.json"))
idx["decks"] = [d for d in idx["decks"] if d["colecao"] != "grok"]
idx["colecoes"] = [x for x in idx["colecoes"] if x["id"] != "grok"]
total = 0
for (root, tema), cards in sorted(decks.items()):
    fn = f"data/decks/grok-{slug(root)}-{slug(tema)}.json"
    mids = sorted({c.get("imagem") for c in cards if c.get("imagem")})
    json.dump({"formato": "codice360x-v1", "baralho": f"Grok ✅ revisado::{root}::{tema}", "midia": {m: f"data/media/{m}" for m in mids}, "cards": cards},
              open(f"{OUT}/{fn}", "w"), ensure_ascii=False)
    idx["decks"].append({"colecao": "grok", "arquivo": fn, "tema": f"{root} · {tema}", "cards": len(cards), "subtemas": sorted({c['subtema'] for c in cards})})
    total += len(cards)
idx["colecoes"].insert(len(idx["colecoes"]) - 1, {"id": "grok", "nome": "Grok ✅ revisado", "icone": "🤖", "cards": total})
json.dump(idx, open(f"{OUT}/data/index.json", "w"), ensure_ascii=False)
print("grok:", total, "notas em", len(decks), "baralhos")
