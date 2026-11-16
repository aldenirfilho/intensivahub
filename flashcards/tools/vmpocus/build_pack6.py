"""Registra 🫁 Curvas de VM 360X + 🔊 POCUS na UTI 360X no índice e gera SOMENTE o pack-6-vmpocus (não toca nos pacotes 1–5).

Uso: python3 build_pack6.py <APP_DIR> <versao>
Pré-requisito: build_vp.py já rodou (gera data/decks/{vmc,pocus}-*.json e tools/vmpocus/vp_cards.json).
"""
import base64, gzip, hashlib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
APP, VERSAO = sys.argv[1], sys.argv[2]
NOME, ROTULO, COLS = "pack-6-vmpocus", "🫁 Curvas de VM + 🔊 POCUS 360X", ["vmc", "pocus"]
META = {
    "vmc": {"id": "vmc", "nome": "Curvas de VM 360X", "icone": "🫁",
            "descricao": "150 telas sintéticas de ventilador (pressão, fluxo, volume, Pes e alças) — modos, mecânica, auto-PEEP, assincronias, SDRA, alarmes e desmame. Imagem na frente; diagnóstico, critérios, conduta e pegadinha no verso."},
    "pocus": {"id": "pocus", "nome": "POCUS na UTI 360X", "icone": "🔊",
              "descricao": "150 imagens sintéticas de ultrassom point-of-care (modo B, modo M e Doppler) — pulmão, derrame, coração, VD/TEP, pericárdio, VCI/VTI, VExUS, eFAST/RUSH/BLUE, vascular, neuro, diafragma e estômago."},
}

idx = json.load(open(f"{APP}/data/index.json"))
man = json.load(open(os.path.join(HERE, "vp_cards.json")))
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
