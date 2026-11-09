"""Junta os baralhos do índice em 4 pacotes (.json.gz + .json mínimo de reserva). Rodar POR ÚLTIMO, após qualquer build que mexa no índice."""
import json, gzip, hashlib, os, sys
APP = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/app2"
GRUPOS = [("pack-1-temi", "🏥 TEMI 2028 + 🥇 Números de ouro", ["temi", "ouro"]), ("pack-2-r3", "🩺 R3 Clínica Médica", ["cm"]), ("pack-3-ia360c", "🤖 IAs 360X curados", ["ia360c"]), ("pack-4-outras", "🧹 Outras IAs + Grok", ["iac", "grok"])]
idx = json.load(open(f"{APP}/data/index.json"))
os.makedirs(f"{APP}/data/packs", exist_ok=True)
for f in os.listdir(f"{APP}/data/packs"): os.remove(f"{APP}/data/packs/{f}")
cols_ok = {c for _, _, cs in GRUPOS for c in cs}
falta = {d["colecao"] for d in idx["decks"]} - cols_ok
assert not falta, f"coleção sem pacote: {falta}"
pacotes = []
for nome, rotulo, cols in GRUPOS:
    decks = [d for d in idx["decks"] if d["colecao"] in cols]
    body = {"formato": "codice360x-pack-v1", "decks": [{"arquivo": d["arquivo"], "colecao": d["colecao"], "j": json.load(open(f"{APP}/{d['arquivo']}"))} for d in decks]}
    mini = json.dumps(body, ensure_ascii=False, separators=(",", ":")).encode()
    sha = hashlib.sha256(mini).hexdigest()[:16]
    import base64
    gz = gzip.compress(mini, 9, mtime=0)
    open(f"{APP}/data/packs/{nome}.gz.txt", "w").write(base64.b64encode(gz).decode())
    open(f"{APP}/data/packs/{nome}.json", "wb").write(mini)
    for d in decks: d["pacote"] = nome
    pacotes.append({"nome": nome, "rotulo": rotulo, "colecoes": cols, "gz": f"data/packs/{nome}.gz.txt", "enc": "b64", "json": f"data/packs/{nome}.json", "sha": sha, "decks": len(decks), "cards": sum(d["cards"] for d in decks), "bytes": len(mini), "gzbytes": os.path.getsize(f"{APP}/data/packs/{nome}.gz.txt")})
    print(nome, len(decks), "baralhos", round(len(mini) / 1e6, 2), "MB →", round(pacotes[-1]["gzbytes"] / 1e6, 2), "MB gz")
idx["pacotes"] = pacotes
json.dump(idx, open(f"{APP}/data/index.json", "w"), ensure_ascii=False, indent=1)
