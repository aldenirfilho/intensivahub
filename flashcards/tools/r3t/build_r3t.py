"""Gera a camada R3 Turbo 360X: decks JSON, imagens, índice e .apkg."""
import sys, os, json, hashlib, importlib, glob, re, html
sys.path.insert(0, "/home/claude/anki/r3t"); sys.path.insert(0, "/home/claude/anki")
from engine import parse, render
OUT = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/app2"
THEMES = [
 ("01", "🫀", "Cardiologia", "cardio", "t01", {"A": "Hipertensão", "B": "Insuficiência cardíaca", "C": "Doença coronariana", "D": "ECG e arritmias", "E": "Valvopatias e endocardite", "F": "Lipídios e prevenção", "G": "Pericárdio, miocárdio e vascular"}),
 ("02", "🫁", "Pneumologia", "pneumo", "t02", {"A": "Asma", "B": "DPOC", "C": "Pleura, nódulo e câncer", "D": "Intersticiais e sarcoidose", "E": "Circulação pulmonar e sono", "F": "Infecções e função pulmonar"}),
 ("03", "🫘", "Nefrologia", "nefro", "t03", {"A": "Lesão renal aguda", "B": "Doença renal crônica", "C": "Glomerulopatias", "D": "Sódio e água", "E": "Potássio, cálcio, fósforo e magnésio", "F": "Ácido-base", "G": "Litíase, ITU e túbulo-intersticial"}),
 ("04", "🍬", "Endocrinologia", "endo", "t04", {"A": "Diabetes", "B": "Tireoide", "C": "Adrenal", "D": "Hipófise", "E": "Osteometabólico e paratireoide", "F": "Obesidade e outros"}),
 ("05", "🫃", "Gastroenterologia e Hepatologia", "gastro", "t05", {"A": "Esôfago e estômago", "B": "Hemorragia digestiva", "C": "Intestino e DII", "D": "Pâncreas e vias biliares", "E": "Hepatites e fígado", "F": "Cirrose e complicações"}),
 ("06", "🩸", "Hematologia", "hemato", "t06", {"A": "Anemias", "B": "Hemólise e hemoglobinopatias", "C": "Plaquetas e hemostasia", "D": "Trombose e anticoagulação", "E": "Leucemias e mieloproliferativas", "F": "Linfomas e mieloma", "G": "Transfusão"}),
 ("07", "🦠", "Infectologia", "infecto", "t07", {"A": "Antimicrobianos", "B": "Pneumonia e vias aéreas", "C": "HIV", "D": "Tuberculose", "E": "IST e sífilis", "F": "Endemias tropicais", "G": "SNC, pele e outros sítios", "H": "Imunização e profilaxias"}),
 ("08", "🦴", "Reumatologia", "reumato", "t08", {"A": "Artrite reumatoide", "B": "LES e SAF", "C": "Outras colagenoses", "D": "Vasculites", "E": "Espondiloartrites", "F": "Cristais e artrites", "G": "Partes moles e osteoartrite"}),
 ("09", "🧠", "Neurologia", "neuro", "t09", {"A": "AVC", "B": "Cefaleias", "C": "Epilepsia", "D": "Demências e movimento", "E": "Neuroimunologia e neuromuscular", "F": "Coma, delirium e outros"}),
 ("10", "🎗️", "Oncologia Clínica", "onco", "t10", {"A": "Rastreamento e genética", "B": "Tumores sólidos", "C": "Paraneoplásicas e marcadores", "D": "Urgências oncológicas", "E": "Toxicidade e suporte"}),
 ("11", "👴", "Geriatria e Paliativos", "geriatria", "t11", {"A": "Avaliação geriátrica", "B": "Síndromes geriátricas", "C": "Polifarmácia", "D": "Cuidados paliativos"}),
 ("12", "🧘", "Psiquiatria na Clínica", "psiq", "t12", {"A": "Humor e ansiedade", "B": "Psicofármacos", "C": "Substâncias", "D": "Urgências psiquiátricas"}),
 ("13", "📊", "Preventiva e MBE", "prev", "t13", {"A": "Rastreamentos", "B": "Vacinação do adulto", "C": "Epidemiologia e MBE", "D": "Ética e saúde pública"}),
 ("14", "🧴", "Dermatologia e Alergia", "dermato", "t14", {"A": "Farmacodermias", "B": "Alergia e urticária", "C": "Dermatoses na clínica"}),
 ("15", "🚑", "Emergências e Enfermaria", "emerg", "t15", {"A": "Emergências clínicas", "B": "Intoxicações", "C": "Enfermaria e perioperatório", "D": "Distúrbios ambientais e outros"}),
]
def load(prefix):
    out = []
    for f in sorted(glob.glob(f"/home/claude/anki/r3t/{prefix}*.py")):
        out += parse(importlib.import_module(os.path.basename(f)[:-3]).TXT)
    return out
def main(do_apkg=True):
    os.makedirs(f"{OUT}/data/media", exist_ok=True); os.makedirs("/home/claude/anki/r3t/img", exist_ok=True)
    idx = json.load(open(f"{OUT}/data/index.json")); idx["decks"] = [d for d in idx["decks"] if not d["arquivo"].startswith("data/decks/r3t-")]
    total, nimg, seen, all_t = 0, 0, set(), []
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
                fn = f"r3t_{num}_{hashlib.md5(c['spec'].encode()).hexdigest()[:8]}.png"; p = f"/home/claude/anki/r3t/img/{fn}"
                if not os.path.exists(p): render(c["spec"], p)
                os.system(f"cp {p} {OUT}/data/media/{fn}"); d["imagem"] = fn; midia[fn] = f"data/media/{fn}"; nimg += 1; c["i"] = fn
            d["tags"] = ["R3T360X", f"T{num}"]; cards.append(d)
        fn = f"r3t-{num}-{slug}.json"; baralho = f"R3 Clínica Médica::⚡ Turbo 360X::{num} {emo} {nome}"
        json.dump({"formato": "codice360x-v1", "baralho": baralho, "cards": cards, "midia": midia}, open(f"{OUT}/data/decks/{fn}", "w"), ensure_ascii=False, indent=1)
        idx["decks"].append({"colecao": "cm", "arquivo": f"data/decks/{fn}", "tema": f"⚡ Turbo 360X · {num} {emo} {nome}", "cards": len(cards), "subtemas": [s for s in subs.values() if any(c['subtema'] == s for c in cards)]})
        total += len(cards); all_t.append((num, emo, nome, subs, cs)); print(num, nome, len(cards), "cards,", len(midia), "imagens")
    for col in idx["colecoes"]:
        if col["id"] == "cm": col["cards"] = sum(d["cards"] for d in idx["decks"] if d["colecao"] == "cm")
    idx["versao"] = "2026.11.09-r3t"
    json.dump(idx, open(f"{OUT}/data/index.json", "w"), ensure_ascii=False, indent=1)
    print("TOTAL", total, "cards ·", nimg, "imagens")
    if do_apkg:
        import genanki
        try: from modelo import model
        except ImportError: from build import model
        decks, media = [], set()
        for num, emo, nome, subs, cs in all_t:
            for code, sub in subs.items():
                dn = f"🩺 R3 Clínica Médica::⚡ Turbo 360X::{num} {emo} {nome}::{sub}"
                dk = genanki.Deck(int(hashlib.md5(dn.encode()).hexdigest()[:8], 16) + 1_100_000_000, dn)
                for c in cs:
                    if c["t"] != code: continue
                    im = c.get("i", "")
                    if im: media.add(f"/home/claude/anki/r3t/img/{im}")
                    dk.add_note(genanki.Note(model=model, fields=[c["f"], c["b"], f'<img src="{im}">' if im else "", c["x"], c["s"], f"{emo} {nome} › {sub}"], tags=["R3T360X", f"T{num}"], guid=genanki.guid_for("r3t360x", num, c["f"])))
                if dk.notes: decks.append(dk)
        for old in glob.glob(f"{OUT}/downloads/R3_Turbo_360X_*"): os.remove(old)
        pk = genanki.Package(decks); pk.media_files = sorted(media); pk.write_to_file(f"{OUT}/downloads/R3_Turbo_360X_{total}_flashcards.apkg")
if __name__ == "__main__": main("--noapkg" not in sys.argv)
