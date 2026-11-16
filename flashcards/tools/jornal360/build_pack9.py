"""📰 Jornal 360 · Pílulas do Dia no Códice: um baralho por edição (coleção "j360"), monta SOMENTE o pack-9-j360.
Uso: python3 build_pack9.py <APP_DIR> <versao>   · lê tools/jornal360/edicoes/AAAA-MM-DD.json (uma por edição)."""
import base64, gzip, hashlib, html, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
APP, VERSAO = sys.argv[1], sys.argv[2]
NOME, ROTULO, COLS = "pack-9-j360", "📰 Jornal 360 · Pílulas do Dia", ["j360"]
ICON = {"TEMI": "🏆", "R3": "🩺", "POCUS": "🔊", "ECG": "🫀", "VM": "🫁"}
e = html.escape
eds = sorted((json.load(open(os.path.join(HERE, "edicoes", f))) for f in os.listdir(os.path.join(HERE, "edicoes")) if f.endswith(".json")),
             key=lambda d: d["data"], reverse=True)
man = []
for ed in eds:
    d = ed["data"]; dbr = "/".join(reversed(d.split("-")))
    nome = f"{dbr} · nº {ed['numero']:03d} · {ed['tema']}"
    arq = f"data/decks/j360-{d}.json"
    cards = []
    for area, frente, verso, peg, fonte in ed["cards"]:
        cards.append({"subtema": f"{ICON.get(area, '💊')} {area}",
            "frente": f'<div style="font-size:12px;margin-bottom:6px;opacity:.85">📰 Jornal 360 · {dbr} · {ICON.get(area, "💊")} {area}</div>{e(frente)}',
            "verso": verso + f'<div style="margin-top:8px;font-size:12px"><a href="{e(ed["jornal"])}" target="_blank" rel="noopener">📱 Ler as Pílulas do dia</a></div>',
            "pegadinha": e(peg), "fonte": f"{e(fonte)} · Pílulas do Dia, Jornal Diário 360 ({dbr})",
            "tags": ["J360", f"J360_{d}", area]})
    json.dump({"formato": "codice360x-v1", "baralho": f"{ROTULO}::{nome}", "cards": cards}, open(f"{APP}/{arq}", "w"), ensure_ascii=False, indent=0)
    man.append({"colecao": "j360", "arquivo": arq, "tema": nome, "cards": len(cards),
                "subtemas": sorted({c["subtema"] for c in cards}), "pacote": NOME})
idx = json.load(open(f"{APP}/data/index.json"))
idx["decks"] = [x for x in idx["decks"] if x["colecao"] not in COLS] + man
col = {"id": "j360", "nome": "Jornal 360 · Pílulas do Dia", "icone": "📰",
       "descricao": "Um baralho por edição do Jornal Diário 360 com os conceitos das Pílulas do Dia (TEMI, R3, POCUS, ECG e VM), fontes citadas e link para a edição completa no celular.",
       "cards": sum(x["cards"] for x in man)}
idx["colecoes"] = [c for c in idx["colecoes"] if c["id"] not in COLS] + [col]
body = {"formato": "codice360x-pack-v1", "decks": [{"arquivo": x["arquivo"], "colecao": x["colecao"], "j": json.load(open(f"{APP}/{x['arquivo']}"))} for x in man]}
mini = json.dumps(body, ensure_ascii=False, separators=(",", ":")).encode()
sha = hashlib.sha256(mini).hexdigest()[:16]
gz = gzip.compress(mini, 9, mtime=0)
open(f"{APP}/data/packs/{NOME}.gz.txt", "w").write(base64.b64encode(gz).decode())
open(f"{APP}/data/packs/{NOME}.json", "wb").write(mini)
p = {"nome": NOME, "rotulo": ROTULO, "colecoes": COLS, "gz": f"data/packs/{NOME}.gz.txt", "enc": "b64", "json": f"data/packs/{NOME}.json", "sha": sha,
     "decks": len(man), "cards": col["cards"], "bytes": len(mini), "gzbytes": os.path.getsize(f"{APP}/data/packs/{NOME}.gz.txt")}
idx["pacotes"] = [x for x in idx["pacotes"] if x["nome"] != NOME] + [p]
idx["versao"] = VERSAO
json.dump(idx, open(f"{APP}/data/index.json", "w"), ensure_ascii=False, indent=1)
print(NOME, p["decks"], "baralhos", p["cards"], "cards · sha", sha)
