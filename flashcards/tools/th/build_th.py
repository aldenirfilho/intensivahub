"""Gera a camada TEMI Hardcore 360X (medicina intensiva, nível prova de título): decks JSON, imagens, índice e .apkg."""
import sys, os, json, hashlib, importlib, glob, re, html
sys.path.insert(0, "/home/claude/anki/th"); sys.path.insert(0, "/home/claude/anki/r3t"); sys.path.insert(0, "/home/claude/anki")
import engine; engine.FOOT = "CÓDICE 360X · TEMI 2028 · Hardcore 360X"
from engine import parse, render
OUT = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/app2"
THEMES = [
 ("01", "🫁", "Ventilação Mecânica e SDRA", "vm", "x01", {"A": "Mecânica e monitorização", "B": "SDRA", "C": "Assincronias e modos", "D": "Desmame e extubação", "E": "VNI e alto fluxo", "F": "Situações especiais"}),
 ("02", "💓", "Hemodinâmica e Choque", "hemodinamica", "x02", {"A": "Oxigenação tecidual e fisiologia", "B": "Fluidos e fluido-responsividade", "C": "Vasopressores e inotrópicos", "D": "Monitorização invasiva", "E": "Tipos de choque", "F": "Suporte circulatório mecânico"}),
 ("03", "🦠", "Sepse e Infecções na UTI", "sepse", "x03", {"A": "Sepse e choque séptico", "B": "Antimicrobianos e PK/PD", "C": "Infecções associadas à assistência", "D": "Infecções graves", "E": "Imunossuprimido"}),
 ("04", "🧠", "Neurointensivismo", "neuro", "x04", {"A": "PIC e neuromonitorização", "B": "Trauma cranioencefálico", "C": "AVC e hemorragias", "D": "Status, neuromuscular e coma", "E": "Morte encefálica e pós-PCR"}),
 ("05", "💤", "Sedação, Analgesia e Via Aérea", "sedacao", "x05", {"A": "Analgesia e sedação", "B": "Delirium e PICS", "C": "Bloqueio neuromuscular", "D": "Via aérea e traqueostomia"}),
 ("06", "🫀", "Cardiointensivismo e PCR", "cardio", "x06", {"A": "Parada cardiorrespiratória", "B": "Cuidados pós-PCR", "C": "Coronária e choque cardiogênico", "D": "Arritmias", "E": "IC, TEP, valvas e pericárdio"}),
 ("07", "🫘", "Rim, Ácido-Base e Eletrólitos", "renal", "x07", {"A": "Lesão renal aguda", "B": "Terapia renal substitutiva", "C": "Ácido-base", "D": "Sódio e água", "E": "Potássio, cálcio, magnésio e fósforo"}),
 ("08", "🫃", "Gastro, Fígado e Nutrição", "gastro", "x08", {"A": "Terapia nutricional", "B": "Hemorragia e abdome agudo", "C": "Fígado crítico"}),
 ("09", "🩸", "Hematologia e Transfusão", "hemato", "x09", {"A": "Transfusão", "B": "Coagulação e trombose", "C": "Onco-hematologia crítica"}),
 ("10", "☠️", "Toxicologia e Ambiente", "tox", "x10", {"A": "Princípios e antídotos", "B": "Intoxicações específicas", "C": "Animais peçonhentos", "D": "Temperatura e ambiente"}),
 ("11", "🚑", "Trauma, Queimados e Pós-Operatório", "trauma", "x11", {"A": "Trauma", "B": "Queimados", "C": "Perioperatório e transplantes"}),
 ("12", "🤰", "Obstetrícia Crítica", "obstetricia", "x12", {"A": "Fisiologia e hipertensão", "B": "Hemorragia e emergências do parto", "C": "Outras emergências maternas"}),
 ("13", "🍬", "Endócrino e Metabólico", "endocrino", "x13", {"A": "Crises hiperglicêmicas e glicemia", "B": "Adrenal e tireoide", "C": "Outras emergências metabólicas"}),
 ("14", "⚖️", "Gestão, Ética e Qualidade", "gestao", "x14", {"A": "Escores e indicadores", "B": "Organização e segurança", "C": "Ética e terminalidade", "D": "Evidência e estatística"}),
 ("15", "🩻", "POCUS, Monitorização e Procedimentos", "pocus", "x15", {"A": "Ultrassom pulmonar", "B": "Ecocardiografia à beira-leito", "C": "Monitorização", "D": "Procedimentos"}),
]
def load(prefix):
    out = []
    for f in sorted(glob.glob(f"/home/claude/anki/th/{prefix}[a-z].py")):
        out += parse(importlib.import_module(os.path.basename(f)[:-3]).TXT)
    return out
def main(do_apkg=True):
    os.makedirs(f"{OUT}/data/media", exist_ok=True); os.makedirs("/home/claude/anki/th/img", exist_ok=True)
    idx = json.load(open(f"{OUT}/data/index.json")); idx["decks"] = [d for d in idx["decks"] if not d["arquivo"].startswith("data/decks/th-")]
    total, nimg, all_t = 0, 0, []
    seen = set(re.sub(r"\W", "", f).lower() for f in json.load(open("/home/claude/anki/th/fronts_existentes.json")))
    for num, emo, nome, slug, pref, subs in THEMES:
        cs = load(pref)
        if not cs: continue
        order = list(subs); cs.sort(key=lambda c: order.index(c["t"]))
        cards, midia = [], {}
        for i, c in enumerate(cs):
            assert c["t"] in subs, (num, c["t"], c["f"]); key = re.sub(r"<[^>]+>|\W", "", c["f"]).lower()
            assert key not in seen, ("duplicado", c["f"]); seen.add(key)
            d = {"subtema": subs[c["t"]], "frente": c["f"], "verso": c["b"]}
            if c["x"]: d["pegadinha"] = c["x"]
            if c["s"]: d["fonte"] = c["s"]
            if c["spec"]:
                fn = f"th_{num}_{hashlib.md5(c['spec'].encode()).hexdigest()[:8]}.png"; p = f"/home/claude/anki/th/img/{fn}"
                if not os.path.exists(p): render(c["spec"], p)
                os.system(f"cp {p} {OUT}/data/media/{fn}"); d["imagem"] = fn; midia[fn] = f"data/media/{fn}"; nimg += 1; c["i"] = fn
            d["tags"] = ["TH360X", f"X{num}"]; cards.append(d)
        fn = f"th-{num}-{slug}.json"; baralho = f"TEMI 2028::🔥 Hardcore 360X::{num} {emo} {nome}"
        json.dump({"formato": "codice360x-v1", "baralho": baralho, "cards": cards, "midia": midia}, open(f"{OUT}/data/decks/{fn}", "w"), ensure_ascii=False, indent=1)
        idx["decks"].append({"colecao": "temi", "arquivo": f"data/decks/{fn}", "tema": f"🔥 Hardcore 360X · {num} {emo} {nome}", "cards": len(cards), "subtemas": [s for s in subs.values() if any(c['subtema'] == s for c in cards)]})
        total += len(cards); all_t.append((num, emo, nome, subs, cs)); print(num, nome, len(cards), "cards,", len(midia), "imagens")
    for col in idx["colecoes"]:
        if col["id"] == "temi": col["cards"] = sum(d["cards"] for d in idx["decks"] if d["colecao"] == "temi")
    idx["versao"] = "2026.11.10-th"
    json.dump(idx, open(f"{OUT}/data/index.json", "w"), ensure_ascii=False, indent=1)
    print("TOTAL", total, "cards ·", nimg, "imagens")
    if do_apkg:
        import genanki
        try: from modelo import model
        except ImportError: from build import model
        decks, media = [], set()
        for num, emo, nome, subs, cs in all_t:
            for code, sub in subs.items():
                dn = f"🏥 TEMI 2028::🔥 Hardcore 360X::{num} {emo} {nome}::{sub}"
                dk = genanki.Deck(int(hashlib.md5(dn.encode()).hexdigest()[:8], 16) + 1_300_000_000, dn)
                for c in cs:
                    if c["t"] != code: continue
                    im = c.get("i", "")
                    if im: media.add(f"/home/claude/anki/th/img/{im}")
                    dk.add_note(genanki.Note(model=model, fields=[c["f"], c["b"], f'<img src="{im}">' if im else "", c["x"], c["s"], f"{emo} {nome} › {sub}"], tags=["TH360X", f"X{num}"], guid=genanki.guid_for("th360x", num, c["f"])))
                if dk.notes: decks.append(dk)
        for old in glob.glob(f"{OUT}/downloads/TEMI_Hardcore_360X_*"): os.remove(old)
        pk = genanki.Package(decks); pk.media_files = sorted(media); pk.write_to_file(f"{OUT}/downloads/TEMI_Hardcore_360X_{total}_flashcards.apkg")
def check():
    import re as _r; tot = 0
    for num, emo, nome, slug, pref, subs in THEMES:
        cs = load(pref); tot += len(cs)
        if cs: print(num, nome, len(cs), "imgs", sum(1 for c in cs if c["spec"]))
    print("TOTAL", tot)
if __name__ == "__main__":
    if "--check" in sys.argv: check()
    else: main("--noapkg" not in sys.argv)
