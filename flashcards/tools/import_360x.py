"""Importa os 2 baralhos '360X 5000' (outras IAs), sem duplicar perguntas, como coleção 'ia360'."""
import sqlite3, json, re, os, shutil, sys
OUT = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/app2"
SRC = [("d", "/home/claude/imp/d"), ("e", "/home/claude/imp/e")]
AVISO = "⚠️ Gerado por outra IA · não revisado"
strip = lambda h: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h or "")).strip()
key = lambda h: re.sub(r"[^a-z0-9]", "", strip(h).lower().encode("ascii", "ignore").decode())
seen, groups, used_all = set(), {}, set()
for tag, d in SRC:
    mm = json.load(open(f"{d}/media")); ren = {}
    for num, name in mm.items():
        if name.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp")):
            new = f"ia360{tag}_{name}"; ren[name] = new
            shutil.copy(f"{d}/{num}", f"{OUT}/data/media/{new}")
    db = sqlite3.connect(f"{d}/collection.anki2")
    for (flds,) in db.execute("select flds from notes order by id"):
        f = flds.split("\x1f"); k = key(f[0])
        if not k or k in seen: continue
        seen.add(k)
        used = set()
        def fix(h):
            def r(m):
                n = m.group(2)
                if n in ren: used.add(ren[n]); return f'<img{m.group(1)} data-m="{ren[n]}"'
                return m.group(0)
            return re.sub(r'<img([^>]*?)\ssrc=["\']([^"\']+)["\']', r, h or "")
        tema, sub = strip(f[2]) or "Geral", strip(f[3]) or "Geral"
        tipo = strip(f[8])
        tipo = re.sub(r"(TEMI|R3)( \+ R3)? · T360X-\d+", "", tipo).strip()
        root = "R3 Clínica Médica" if re.match(r"^(3[1-9]|4\d)\b", tema) or "R3" in f[8] and "TEMI" not in f[8] else "TEMI 2028"
        g = groups.setdefault((root, tema), {"used": set(), "cards": []})
        g["cards"].append({"subtema": sub, "frente": (f"<div style='font-size:13px;opacity:.8'>{tipo}</div>" if tipo else "") + fix(f[0]),
                           "verso": "✅ " + fix(f[1]) + fix(f[4]) + fix(f[5]), "pegadinha": "",
                           "fonte": strip(f[6])[:300] + " · " + AVISO, "tags": ["IA", "IA_360X_5000", "R3" if root.startswith("R3") else "TEMI"]})
        g["used"] |= used; used_all |= used
for x in os.listdir(f"{OUT}/data/decks"):
    if x.startswith("ia360-"): os.remove(f"{OUT}/data/decks/{x}")
files = []
for (root, tema), g in sorted(groups.items()):
    slug = re.sub(r"[^a-z0-9]+", "-", (root + " " + tema).lower().encode("ascii", "ignore").decode()).strip("-")
    fn = f"ia360-{slug}.json"
    json.dump({"formato": "codice360x-v1", "baralho": f"IAs 360X (5000+5000)::{root}::{tema}", "cards": g["cards"], "midia": {m: f"data/media/{m}" for m in sorted(g["used"])}},
              open(f"{OUT}/data/decks/{fn}", "w"), ensure_ascii=False)
    files.append({"colecao": "ia360", "arquivo": f"data/decks/{fn}", "tema": "IAs 360X › " + root + " › " + tema, "cards": len(g["cards"]), "subtemas": sorted({x["subtema"] for x in g["cards"]})})
# remove imagens não usadas
for x in os.listdir(f"{OUT}/data/media"):
    if x.startswith("ia360") and x not in used_all: os.remove(f"{OUT}/data/media/{x}")
idx = json.load(open(f"{OUT}/data/index.json"))
idx["decks"] = [d for d in idx["decks"] if d.get("colecao") != "ia360"] + files
idx["colecoes"] = [c for c in idx["colecoes"] if c["id"] != "ia360"] + [{"id": "ia360", "nome": "IAs 360X 5000+5000 (não revisado)", "icone": "🗃️", "cards": sum(f["cards"] for f in files)}]
json.dump(idx, open(f"{OUT}/data/index.json", "w"), ensure_ascii=False, indent=1)
print("temas", len(files), "cards", sum(f["cards"] for f in files), "imgs", len(used_all))
