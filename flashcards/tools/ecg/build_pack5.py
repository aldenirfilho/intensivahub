"""Registra o Compêndio de ECG no índice e gera SOMENTE o pack-5-ecg (não toca nos pacotes 1–4).

Uso: python3 build_pack5.py <APP_DIR> <versao>
Pré-requisito: build_ecg.py já rodou (gera data/decks/ecg-*.json e tools/ecg/ecg_cards.json).
"""
import base64, gzip, hashlib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
APP, VERSAO = sys.argv[1], sys.argv[2]
NOME, ROTULO, COLS = "pack-5-ecg", "📈 Compêndio de ECG 360X", ["ecg"]
COL = {"id": "ecg", "nome": "Compêndio de ECG 360X", "icone": "📈",
       "descricao": "300 traçados sintéticos didáticos com alterações do ECG — imagem na frente; diagnóstico, critérios, conduta e pegadinha no verso. Toque no traçado para ampliar."}

idx = json.load(open(f"{APP}/data/index.json"))
man = json.load(open(os.path.join(HERE, "ecg_cards.json")))
decks = [dict(d, pacote=NOME) for d in man["decks"]]
idx["decks"] = [d for d in idx["decks"] if d["colecao"] != "ecg"] + decks
COL["cards"] = sum(d["cards"] for d in decks)
idx["colecoes"] = [c for c in idx["colecoes"] if c["id"] != "ecg"] + [COL]
body = {"formato": "codice360x-pack-v1", "decks": [{"arquivo": d["arquivo"], "colecao": d["colecao"], "j": json.load(open(f"{APP}/{d['arquivo']}"))} for d in decks]}
mini = json.dumps(body, ensure_ascii=False, separators=(",", ":")).encode()
sha = hashlib.sha256(mini).hexdigest()[:16]
gz = gzip.compress(mini, 9, mtime=0)
open(f"{APP}/data/packs/{NOME}.gz.txt", "w").write(base64.b64encode(gz).decode())
open(f"{APP}/data/packs/{NOME}.json", "wb").write(mini)
p = {"nome": NOME, "rotulo": ROTULO, "colecoes": COLS, "gz": f"data/packs/{NOME}.gz.txt", "enc": "b64", "json": f"data/packs/{NOME}.json", "sha": sha,
     "decks": len(decks), "cards": COL["cards"], "bytes": len(mini), "gzbytes": os.path.getsize(f"{APP}/data/packs/{NOME}.gz.txt")}
idx["pacotes"] = [x for x in idx["pacotes"] if x["nome"] != NOME] + [p]
idx["versao"] = VERSAO
json.dump(idx, open(f"{APP}/data/index.json", "w"), ensure_ascii=False, indent=1)
print(NOME, p["decks"], "baralhos", p["cards"], "cards", round(p["bytes"] / 1e3), "KB →", round(p["gzbytes"] / 1e3), "KB b64gz · sha", sha)
