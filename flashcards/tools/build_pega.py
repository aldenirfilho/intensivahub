"""Deck de pegadinhas: 1 card por questão (frente = caso, verso = resposta + pegadinha + comentário)."""
import json, re, os, sys, hashlib, glob, html
sys.path.insert(0, "/home/claude/anki")
APP = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/app2"
Q = json.load(open(f"{APP}/data/questoes.json"))
DIV = {"temi": ("TEMI 2028::🎯 Pegadinhas 360X", "temi", "pega-temi.json", "🏥 TEMI"), "r3": ("R3 Clínica Médica::🎯 Pegadinhas 360X", "cm", "pega-r3.json", "🩺 R3")}
LT = lambda t: re.sub(r"<(?![a-zA-Z/!])", "&lt;", t)
IMG = re.compile(r'<img[^>]*src="data/media/([^"]+)"[^>]*>')
idx = json.load(open(f"{APP}/data/index.json"))
idx["decks"] = [d for d in idx["decks"] if not d["arquivo"].startswith("data/decks/pega-")]
allc = {}
for div, (deck, col, fn, lab) in DIV.items():
    cards, midia = [], {}
    for q in sorted(Q[div], key=lambda q: (q["tema"], q["id"])):
        enun = q["enun"]; m = IMG.search(enun); img = ""
        if m: img = m.group(1); midia[img] = f"data/media/{img}"
        resp = q["alts"][q["gab"]]
        verso = f"<b class=c>✅ Resposta:</b> {resp}"
        if q.get("com"): verso += f"<br><br>💬 {q['com']}"
        c = {"subtema": q["tema"], "frente": LT(f"🎯 {enun}"), "verso": LT(verso), "pegadinha": LT(q["pega"]), "fonte": f"Banco de questões CÓDICE 360X · {q['id']}", "tags": ["PEGA360X", div.upper(), q["id"]]}
        if img: c["_img"] = img
        cards.append(c)
    json.dump({"formato": "codice360x-v1", "baralho": deck, "cards": [{k: v for k, v in c.items() if k != "_img"} for c in cards], "midia": midia}, open(f"{APP}/data/decks/{fn}", "w"), ensure_ascii=False, indent=1)
    subs = sorted({c["subtema"] for c in cards})
    idx["decks"].append({"colecao": col, "arquivo": f"data/decks/{fn}", "tema": f"🎯 Pegadinhas 360X · {lab}", "cards": len(cards), "subtemas": subs})
    allc[div] = (deck, cards); print(div, len(cards), "cards,", len(subs), "temas,", len(midia), "imagens")
for c in idx["colecoes"]: c["cards"] = sum(d["cards"] for d in idx["decks"] if d["colecao"] == c["id"])
idx["versao"] = "2026.11.09-pega"
json.dump(idx, open(f"{APP}/data/index.json", "w"), ensure_ascii=False, indent=1)
import genanki
from modelo import model
decks, media = [], set()
for div, (deck, cards) in allc.items():
    root = ("🏥 " if div == "temi" else "🩺 ") + deck
    by = {}
    for c in cards: by.setdefault(c["subtema"], []).append(c)
    for sub, cs in by.items():
        name = f"{root}::{sub}"; dk = genanki.Deck(int(hashlib.md5(name.encode()).hexdigest()[:8], 16) + 1_200_000_000, name)
        for c in cs:
            im = c.get("_img", "")
            if im: media.add(f"/home/claude/anki/qimg/{im}")
            dk.add_note(genanki.Note(model=model, fields=[IMG.sub(f'<img src="{im}">', c["frente"]), c["verso"], "", c["pegadinha"], c["fonte"], f"🎯 Pegadinhas › {sub}"], tags=["PEGA360X", div.upper()], guid=genanki.guid_for("pega360x", c["tags"][2])))
        decks.append(dk)
for old in glob.glob(f"{APP}/downloads/Pegadinhas_360X_*"): os.remove(old)
pk = genanki.Package(decks); pk.media_files = sorted(media)
out = f"{APP}/downloads/Pegadinhas_360X_{sum(len(c) for _, c in allc.values())}_cards.apkg"; pk.write_to_file(out); print(out)
