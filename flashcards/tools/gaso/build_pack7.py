"""Registra 🧪 Gasometria 360X no índice e gera SOMENTE o pack-7-gaso (não toca nos pacotes 1–6).
Uso: python3 build_pack7.py <APP_DIR> <versao>   · pré-requisito: build_gaso.py já rodou."""
import base64, gzip, hashlib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
APP, VERSAO = sys.argv[1], sys.argv[2]
NOME, ROTULO, COLS = "pack-7-gaso", "🧪 Gasometria 360X", ["gaso"]
META = {"gaso": {"id": "gaso", "nome": "Gasometria 360X", "icone": "🧪",
                 "descricao": "300 flashcards de gasometria arterial: método, acidoses (AG alto e hiperclorêmica), alcaloses, distúrbios respiratórios, mistos e triplos, oxigenação (A-a, P/F, DO₂), gaps e casos de UTI — 235 casos com laudo e solução passo a passo calculada pelo motor ácido-base."}}
idx = json.load(open(f"{APP}/data/index.json"))
man = json.load(open(os.path.join(HERE, "gaso_manifest.json")))
decks = [dict(d, pacote=NOME) for d in man["decks"]]
idx["decks"] = [d for d in idx["decks"] if d["colecao"] not in COLS] + decks
cols = []
for cid in COLS:
    c = dict(META[cid]); c["cards"] = sum(d["cards"] for d in decks if d["colecao"] == cid); cols.append(c)
idx["colecoes"] = [c for c in idx["colecoes"] if c["id"] not in COLS] + cols
body = {"formato": "codice360x-pack-v1", "decks": [{"arquivo": d["arquivo"], "colecao": d["colecao"], "j": json.load(open(f"{APP}/{d['arquivo']}"))} for d in decks]}
mini = json.dumps(body, ensure_ascii=False, separators=(",", ":")).encode()
sha = hashlib.sha256(mini).hexdigest()[:16]
gz = gzip.compress(mini, 9, mtime=0)
open(f"{APP}/data/packs/{NOME}.gz.txt", "w").write(base64.b64encode(gz).decode())
open(f"{APP}/data/packs/{NOME}.json", "wb").write(mini)
p = {"nome": NOME, "rotulo": ROTULO, "colecoes": COLS, "gz": f"data/packs/{NOME}.gz.txt", "enc": "b64", "json": f"data/packs/{NOME}.json", "sha": sha,
     "decks": len(decks), "cards": sum(c["cards"] for c in cols), "bytes": len(mini), "gzbytes": os.path.getsize(f"{APP}/data/packs/{NOME}.gz.txt")}
idx["pacotes"] = [x for x in idx["pacotes"] if x["nome"] != NOME] + [p]
idx["versao"] = VERSAO
json.dump(idx, open(f"{APP}/data/index.json", "w"), ensure_ascii=False, indent=1)
print(NOME, p["decks"], "baralhos", p["cards"], "cards", round(p["bytes"] / 1e3), "KB →", round(p["gzbytes"] / 1e3), "KB b64gz · sha", sha)
