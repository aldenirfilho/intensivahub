"""Converte os .apkg de outras IAs para o formato codice360x-v1 (coleção 'ia')."""
import sqlite3, json, re, os, shutil, sys
OUT = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/app2"
SRC = {"a": "/home/claude/imp/a", "b": "/home/claude/imp/b"}
os.makedirs(f"{OUT}/data/decks", exist_ok=True); os.makedirs(f"{OUT}/data/media", exist_ok=True)
AVISO = "⚠️ gerado por outra IA — não revisado"

def media_copy(d, prefix):
    m = json.load(open(f"{d}/media")); out = {}
    for num, name in m.items():
        new = prefix + name
        shutil.copy(f"{d}/{num}", f"{OUT}/data/media/{new}"); out[name] = new
    return out

def fix_imgs(html, ren, used):
    def r(m):
        src = m.group(2); new = ren.get(src)
        if not new: return m.group(0)
        used.add(new); return f'<img{m.group(1)} data-m="{new}"'
    return re.sub(r'<img([^>]*?)\ssrc=["\']([^"\']+)["\']', r, html)

def clean_src(h): return re.sub(r"<[^>]+>", "", h).strip()

files = []
# ---- A: TEMI 360X 3000
ren = media_copy(SRC["a"], "ia_a_")
c = sqlite3.connect(f"{SRC['a']}/collection.anki2")
decks = {int(k): v["name"] for k, v in json.loads(c.execute("select decks from col").fetchone()[0]).items()}
groups = {}
for flds, did in c.execute("select n.flds, c.did from notes n join cards c on c.nid=n.id order by n.id"):
    f = flds.split("\x1f")  # Frente Verso Tema Subtema Tabela Imagem Fonte Edicao Tipo
    tema = f[2].strip() or decks.get(did, "Geral").split("::")[-1]
    used = set()
    verso = fix_imgs(f[1] + (("<br>" + f[4]) if f[4].strip() else "") + f[5], ren, used)
    tipo = clean_src(f[8])
    groups.setdefault(tema, {"used": set(), "cards": []})
    groups[tema]["used"] |= used
    groups[tema]["cards"].append({"subtema": f[3].strip() or "Geral", "frente": (f"<span class=pill>{tipo}</span> " if tipo else "") + f[0],
        "verso": verso, "fonte": (clean_src(f[6]) + " · " if clean_src(f[6]) else "") + AVISO, "tags": ["IA", "IA_TEMI3000", re.sub(r"\W+", "_", tipo).strip("_") or "card"]})
for tema, g in sorted(groups.items()):
    slug = re.sub(r"[^a-z0-9]+", "-", tema.lower().encode("ascii", "ignore").decode()).strip("-")
    fn = f"ia-a-{slug}.json"
    json.dump({"formato": "codice360x-v1", "baralho": f"Outras IAs::TEMI 360X 3000::{tema}", "cards": g["cards"], "midia": {m: f"data/media/{m}" for m in sorted(g["used"])}},
              open(f"{OUT}/data/decks/{fn}", "w"), ensure_ascii=False)
    files.append({"colecao": "ia", "arquivo": f"data/decks/{fn}", "tema": "TEMI 360X 3000 › " + tema, "cards": len(g["cards"]), "subtemas": sorted({x["subtema"] for x in g["cards"]})})

# ---- B: TEMI + R3 (454)
ren = media_copy(SRC["b"], "ia_b_")
c = sqlite3.connect(f"{SRC['b']}/collection.anki2")
decks = {int(k): v["name"] for k, v in json.loads(c.execute("select decks from col").fetchone()[0]).items()}
groups = {}
for flds, did in c.execute("select n.flds, c.did from notes n join cards c on c.nid=n.id order by n.id"):
    f = flds.split("\x1f")  # Tema Subtema Pergunta Resposta Extra Fonte
    dn = decks.get(did, "Geral")
    root = "R3 Clínica Médica" if "R3" in dn else "TEMI 2028"
    tema = clean_src(dn.split("::")[-1]).strip()
    used = set()
    resp = fix_imgs(f[3], ren, used); extra = fix_imgs(f[4], ren, used)
    if "<img" in f[0] or "<img" in f[2]:
        resp += fix_imgs(re.sub(r"<span[^>]*>.*?</span>", "", f[0]), ren, used)
    groups.setdefault((root, tema), {"used": set(), "cards": []})
    groups[(root, tema)]["used"] |= used
    groups[(root, tema)]["cards"].append({"subtema": clean_src(f[1]) or "Geral", "frente": f[2], "verso": "✅ " + resp, "pegadinha": extra,
        "fonte": (clean_src(f[5]) + " · " if clean_src(f[5]) else "") + AVISO, "tags": ["IA", "IA_TEMI_R3_454", "R3" if root.startswith("R3") else "TEMI"]})
for (root, tema), g in sorted(groups.items()):
    slug = re.sub(r"[^a-z0-9]+", "-", (root + " " + tema).lower().encode("ascii", "ignore").decode()).strip("-")
    fn = f"ia-b-{slug}.json"
    json.dump({"formato": "codice360x-v1", "baralho": f"Outras IAs::Baralho TEMI + R3 (454)::{root}::{tema}", "cards": g["cards"], "midia": {m: f"data/media/{m}" for m in sorted(g["used"])}},
              open(f"{OUT}/data/decks/{fn}", "w"), ensure_ascii=False)
    files.append({"colecao": "ia", "arquivo": f"data/decks/{fn}", "tema": "TEMI + R3 (454) › " + tema, "cards": len(g["cards"]), "subtemas": sorted({x["subtema"] for x in g["cards"]})})

idx = json.load(open(f"{OUT}/data/index.json"))
idx["decks"] = [d for d in idx["decks"] if d.get("colecao") != "ia"] + files
idx["colecoes"] = [c for c in idx["colecoes"] if c["id"] != "ia"] + [{"id": "ia", "nome": "Outras IAs (não revisado)", "icone": "📦", "cards": sum(f["cards"] for f in files)}]
json.dump(idx, open(f"{OUT}/data/index.json", "w"), ensure_ascii=False, indent=1)
print("arquivos", len(files), "cards", sum(f["cards"] for f in files), "imgs", len([x for x in os.listdir(f"{OUT}/data/media") if x.startswith("ia_")]))
