"""v2: gera as coleções TEMI 2028 (600) e R3 Clínica Médica (300) para o app, .apkg e índice."""
import json, os, shutil, sys, hashlib, genanki, re, html
from dataset import all_themes
from dataset_cm import cm_themes, TEMI_IMG
try:
    from modelo import CSS, model
except ImportError:
    from build import CSS, model

OUT = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/app2"
for d in ("data/decks", "data/media", "downloads"): os.makedirs(f"{OUT}/{d}", exist_ok=True)
MEDIA = "media" if os.path.isdir("media") else f"{OUT}/data/media"
if MEDIA == "media":
    for f in os.listdir("media"): shutil.copy(f"media/{f}", f"{OUT}/data/media/{f}")

temi = all_themes()
used_img = 0
for th in temi:
    for c in th["cards"]:
        if not c["i"]:
            for k, img in TEMI_IMG.items():
                if k in c["f"]: c["i"] = img; used_img += 1
assert used_img == len(TEMI_IMG), f"imagens encaixadas {used_img}/{len(TEMI_IMG)}"

COLS = [("TEMI 2028", "🏥", "temi", temi, "TEMI2028"), ("R3 Clínica Médica", "🩺", "cm", cm_themes(), "R3CM")]
index = {"formato": "codice360x-index-v2", "versao": "2026.11.05-900", "colecoes": [], "decks": []}
md = []
for root, icon, key, themes, tag in COLS:
    index["colecoes"].append({"id": key, "nome": root, "icone": icon, "cards": sum(len(t["cards"]) for t in themes)})
    decks, media, total = [], set(), 0
    md.append(f"\n# {icon} {root}\n")
    for th in themes:
        deckroot = f"{root}::{th['num']} {th['emo']} {th['nome']}"
        cards = []
        for c in th["cards"]:
            d = {"subtema": c["sub"], "frente": c["f"], "verso": c["b"]}
            if c["x"]: d["pegadinha"] = c["x"]
            if c["s"]: d["fonte"] = c["s"]
            if c["i"]: d["imagem"] = c["i"]
            d["tags"] = [tag, f"T{th['num']}", c["orig"]]
            cards.append(d)
        used = sorted({c["i"] for c in th["cards"] if c["i"]})
        fn = f"{key}-{th['num']}-{th['slug'].replace('cm-', '')}.json"
        json.dump({"formato": "codice360x-v1", "baralho": deckroot, "cards": cards, "midia": {m: f"data/media/{m}" for m in used}},
                  open(f"{OUT}/data/decks/{fn}", "w"), ensure_ascii=False, indent=1)
        index["decks"].append({"colecao": key, "arquivo": f"data/decks/{fn}", "tema": f"{th['num']} {th['emo']} {th['nome']}", "cards": len(cards), "subtemas": list(th["subs"].values())})
        md.append(f"\n## {th['num']} {th['emo']} {th['nome']} ({len(cards)})\n")
        for code, sub in th["subs"].items():
            dname = f"{icon} {root}::{th['num']} {th['emo']} {th['nome']}::{sub}"
            dk = genanki.Deck(int(hashlib.md5(dname.encode()).hexdigest()[:8], 16) + 1_000_000_000, dname)
            md.append(f"\n### {sub}\n")
            for c in th["cards"]:
                if c["t"] != code: continue
                if c["i"]: media.add(f"{MEDIA}/{c['i']}")
                dk.add_note(genanki.Note(model=model, fields=[c["f"], c["b"], f'<img src="{c["i"]}">' if c["i"] else "", c["x"], c["s"], f"{th['emo']} {th['nome']} › {sub}"],
                    tags=[tag, f"T{th['num']}", c["orig"]], guid=genanki.guid_for(key + "-v2", th["num"], c["f"])))
                total += 1
                md.append(f"- {re.sub('<[^>]+>', '', html.unescape(c['f']))}{' 🖼️' if c['i'] else ''}\n")
            decks.append(dk)
    pkg = genanki.Package(decks); pkg.media_files = sorted(media)
    pkg.write_to_file(f"{OUT}/downloads/{'TEMI_2028_600' if key == 'temi' else 'R3_Clinica_Medica_300'}_flashcards.apkg")
    print(root, total, "cards ·", len(decks), "subbaralhos ·", len(media), "imagens")
json.dump(index, open(f"{OUT}/data/index.json", "w"), ensure_ascii=False, indent=1)
open(f"{OUT}/INDICE_CARDS.md", "w").write("# 📚 Índice dos flashcards · CÓDICE 360X\n\n🖼️ = card com ilustração · organizados por coleção › tema › subtema\n" + "".join(md))
