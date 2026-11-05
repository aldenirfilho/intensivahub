"""Gera os dados do app (JSON por tema), o .apkg de 600 cards e o índice."""
import json, os, shutil, sys, hashlib, genanki, re, html
from dataset import all_themes
from modelo import CSS, model

OUT = sys.argv[1] if len(sys.argv) > 1 else ".."
os.makedirs(f"{OUT}/data/decks", exist_ok=True)
os.makedirs(f"{OUT}/data/media", exist_ok=True)
os.makedirs(f"{OUT}/downloads", exist_ok=True)
MEDIA = "media" if os.path.isdir("media") else f"{OUT}/data/media"  # images.py gera em ./media
if MEDIA == "media":
    for f in os.listdir("media"):
        shutil.copy(f"media/{f}", f"{OUT}/data/media/{f}")

themes = all_themes()
index = {"formato": "codice360x-index-v1", "versao": "2026.11.05-600", "titulo": "TEMI 2028 · Baralho oficial", "decks": []}
decks, media, total, md = [], set(), 0, []
for th in themes:
    root = f"TEMI 2028::{th['num']} {th['emo']} {th['nome']}"
    cards = []
    for c in th["cards"]:
        d = {"subtema": c["sub"], "frente": c["f"], "verso": c["b"]}
        if c["x"]: d["pegadinha"] = c["x"]
        if c["s"]: d["fonte"] = c["s"]
        if c["i"]: d["imagem"] = c["i"]
        d["tags"] = ["TEMI2028", f"T{th['num']}", c["orig"]]
        cards.append(d)
    used = sorted({c["i"] for c in th["cards"] if c["i"]})
    deck = {"formato": "codice360x-v1", "baralho": root, "cards": cards,
            "midia": {m: f"data/media/{m}" for m in used}}
    fn = f"{th['num']}-{th['slug']}.json"
    json.dump(deck, open(f"{OUT}/data/decks/{fn}", "w"), ensure_ascii=False, indent=1)
    index["decks"].append({"arquivo": f"data/decks/{fn}", "tema": f"{th['num']} {th['emo']} {th['nome']}", "cards": len(cards),
                           "subtemas": list(th["subs"].values())})
    # apkg
    for code, sub in th["subs"].items():
        dname = f"🏥 TEMI 2028::{th['num']} {th['emo']} {th['nome']}::{sub}"
        did = int(hashlib.md5(dname.encode()).hexdigest()[:8], 16) + 1_000_000_000
        dk = genanki.Deck(did, dname)
        for c in th["cards"]:
            if c["t"] != code: continue
            img = f'<img src="{c["i"]}">' if c["i"] else ""
            if c["i"]: media.add(f"{MEDIA}/{c['i']}")
            dk.add_note(genanki.Note(model=model, fields=[c["f"], c["b"], img, c["x"], c["s"], f"{th['emo']} {th['nome']} › {sub}"],
                tags=["TEMI2028", f"T{th['num']}", c["orig"]], guid=genanki.guid_for("temi2028-600", th["num"], c["f"])))
            total += 1
        decks.append(dk)
    md.append(f"\n## {th['num']} {th['emo']} {th['nome']} ({len(cards)})\n")
    for code, sub in th["subs"].items():
        md.append(f"\n### {sub}\n")
        for c in th["cards"]:
            if c["t"] == code:
                md.append(f"- {re.sub('<[^>]+>', '', html.unescape(c['f']))} {'🆕' if c['orig']=='v2' else ''}\n")
json.dump(index, open(f"{OUT}/data/index.json", "w"), ensure_ascii=False, indent=1)
pkg = genanki.Package(decks); pkg.media_files = sorted(media)
pkg.write_to_file(f"{OUT}/downloads/TEMI_2028_600_flashcards.apkg")
open(f"{OUT}/INDICE_CARDS.md", "w").write("# 📚 Índice dos 600 flashcards — TEMI 2028\n\n🆕 = cards novos da v2 · organizados por tema › subtema\n" + "".join(md))
print("TOTAL", total, "temas", len(themes), "subdecks", len(decks))
