"""📜 Escrituras & Axiomas 360X no Códice: gera os baralhos do app, registra a coleção "escr" no índice,
monta SOMENTE o pack-8-escr (não toca nos pacotes 1–7) e publica o livro do autor em autor/.
Uso: python3 build_pack8.py <APP_DIR> <versao>   · pré-requisito: build.py e make_book.py já rodaram (pasta out/)."""
import base64, gzip, hashlib, html, json, os, re, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build  # noqa: E402

APP, VERSAO = sys.argv[1], sys.argv[2]
NOME, ROTULO, COLS = "pack-8-escr", "📜 Escrituras & Axiomas 360X", ["escr"]
RAIZ = "📜 Escrituras & Axiomas 360X"
AUTOR = "Dr. Aldenir Rocha de Oliveira Filho"
e = html.escape

decks, cards, erros = build.carregar()
assert not erros and len(cards) == build.TOTAL, (erros, len(cards))

def frente(c):
    emo, tnome, cor = build.TEMAS[c["tema"]]
    mito, autor = c["selo"] == "mito", c["selo"] == "autor"
    perg = ("🕵️ A quem costumam atribuir — e quem disse de verdade?" if mito else
            "⚜️ Que axioma do autor é este? (nome · eixo)" if autor else
            "🔎 Qual é a fonte? (tradição · livro · capítulo/versículo)")
    borda = "#ef4444" if mito else "#d4af37"
    return (f'<div style="font-size:13px;margin-bottom:8px"><span style="display:inline-block;padding:2px 9px;border-radius:999px;'
            f'background:{cor};color:#0b0f16;font-weight:600">{emo} {e(tnome)}</span></div>'
            f'<div style="font-family:Georgia,\'Times New Roman\',serif;font-size:1.15em;line-height:1.5;border-left:4px solid {borda};'
            f'padding:8px 14px;border-radius:6px;background:rgba(212,175,55,.07){";font-style:italic" if autor else ""}">“{e(c["msg"])}”</div>'
            f'<div style="margin-top:10px;font-weight:600;color:#22b8d6">{perg}</div>')

def verso(c):
    mito, autor = c["selo"] == "mito", c["selo"] == "autor"
    rot = "🔎 <b>Origem real:</b>" if mito else "📖 <b>Comentário da edição:</b>" if autor else "💡 <b>Lição:</b>"
    nota = build.LINGUA_NOTA.get(c["lingua"], "Tradução livre")
    selo = {"canonico": f"✅ Texto de fonte localizada · {nota}",
            "tradicional": f"⚠️ Atribuição tradicional — fonte primária incerta · {nota}",
            "mito": "🕵️ MITO DE ATRIBUIÇÃO — a frase circula com o nome errado",
            "autor": f"⚜️ Axioma autoral · {c['meta']['sit'] if c['meta'] else ''} · texto do catálogo Axiomas 360X, sem alteração"}[c["selo"]] + build.conf_txt(c)
    linhas = [f'📍 <b>{e(c["ref"])}</b>']
    if c["capinfo"]:
        linhas.append(f'📚 {e(c["capinfo"])}')
    linhas.append(f'🏛️ {e(c["trad"])}')
    corpo = "<br>".join(linhas)
    return (f'{corpo}<div style="margin-top:10px;padding:9px 12px;border-radius:9px;border:1px solid rgba(34,184,214,.45);'
            f'background:rgba(34,184,214,.07)">{rot} {e(c["licao"])}</div>'
            f'<div style="margin-top:8px;font-size:12.5px;opacity:.8">{selo}</div>')

def fonte(c):
    if c["selo"] == "autor":
        return f"✍️ Axioma de {AUTOR.replace('Dr. ', '')} · Axiomas 360X nº {c['meta']['n']} · comentário da edição Códice 360X · livro completo em ⚜️ Autor"
    return f"📜 Escrituras & Axiomas 360X · organização e axiomas: {AUTOR}"

os.makedirs(f"{APP}/data/decks", exist_ok=True)
man = []
for num, nome, *_ in decks:
    cs = [c for c in cards if c["num"] == num]
    baralho = f"{RAIZ}::{num} {nome}"
    slug = build.slug(nome).lower()[:40].strip("_")
    arq = f"data/decks/escr-{num}-{slug}.json"
    j = {"formato": "codice360x-v1", "baralho": baralho, "cards": [
        {"frente": frente(c), "verso": verso(c), "pegadinha": e(c["nerd"]), "fonte": fonte(c),
         "tags": ["ESCR", f"ESCR_T{num}", "tema_" + build.slug(build.TEMAS[c["tema"]][1]).lower()] + (["AUTOR_ALDENIR"] if c["selo"] == "autor" else [])}
        for c in cs]}
    json.dump(j, open(f"{APP}/{arq}", "w"), ensure_ascii=False, indent=0)
    man.append({"colecao": "escr", "arquivo": arq, "tema": f"{num} {nome}", "cards": len(cs), "subtemas": [f"{num} {nome}"], "pacote": NOME})

META = {"escr": {"id": "escr", "nome": "Escrituras & Axiomas 360X", "icone": "📜",
                 "descricao": f"{build.TOTAL} flashcards de mensagens que importam: Torá, Salmos, Provérbios, Profetas, Evangelhos, Cartas, Talmude, Alcorão, "
                              "Budismo, Confúcio, Taoísmo, Hinduísmo, Estoicos, filosofia, outras tradições, medicina, personalidades, mitos de citação "
                              f"e os 149 Axiomas 360X do autor com comentários. Organização e axiomas: {AUTOR}."}}
idx = json.load(open(f"{APP}/data/index.json"))
idx["decks"] = [d for d in idx["decks"] if d["colecao"] not in COLS] + man
cols = []
for cid in COLS:
    c = dict(META[cid]); c["cards"] = sum(d["cards"] for d in man if d["colecao"] == cid); cols.append(c)
idx["colecoes"] = [c for c in idx["colecoes"] if c["id"] not in COLS] + cols
body = {"formato": "codice360x-pack-v1", "decks": [{"arquivo": d["arquivo"], "colecao": d["colecao"], "j": json.load(open(f"{APP}/{d['arquivo']}"))} for d in man]}
mini = json.dumps(body, ensure_ascii=False, separators=(",", ":")).encode()
sha = hashlib.sha256(mini).hexdigest()[:16]
gz = gzip.compress(mini, 9, mtime=0)
open(f"{APP}/data/packs/{NOME}.gz.txt", "w").write(base64.b64encode(gz).decode())
open(f"{APP}/data/packs/{NOME}.json", "wb").write(mini)
p = {"nome": NOME, "rotulo": ROTULO, "colecoes": COLS, "gz": f"data/packs/{NOME}.gz.txt", "enc": "b64", "json": f"data/packs/{NOME}.json", "sha": sha,
     "decks": len(man), "cards": sum(c["cards"] for c in cols), "bytes": len(mini), "gzbytes": os.path.getsize(f"{APP}/data/packs/{NOME}.gz.txt")}
idx["pacotes"] = [x for x in idx["pacotes"] if x["nome"] != NOME] + [p]
idx["versao"] = VERSAO
json.dump(idx, open(f"{APP}/data/index.json", "w"), ensure_ascii=False, indent=1)
print(NOME, p["decks"], "baralhos", p["cards"], "cards", round(p["bytes"] / 1e3), "KB →", round(p["gzbytes"] / 1e3), "KB b64gz · sha", sha)

# livro do autor (página) + downloads
OUT = os.path.join(HERE, "out")
livro = open(os.path.join(OUT, "Axiomas_360X_Edicao_Comentada.html"), encoding="utf-8").read()
livro = livro.replace('<div class="topo"><span class="t">', '<div class="topo"><a href="../index.html#inicio">← Códice 360X</a><span class="t">', 1)
os.makedirs(f"{APP}/autor", exist_ok=True)
open(f"{APP}/autor/axiomas-360x.html", "w", encoding="utf-8").write(livro)
os.makedirs(f"{APP}/downloads", exist_ok=True)
shutil.copy(os.path.join(OUT, "mapa-axiomas.html"), f"{APP}/autor/mapa-axiomas.html")
for fn in ("Axiomas_360X_Edicao_Comentada_A5.pdf", f"Escrituras_Axiomas_360X_{build.TOTAL}_flashcards.apkg",
           "Axiomas_360X_149_cartoes_tela_de_bloqueio.zip", "Axiomas_360X_149_cartoes_folha_de_contato_A4.pdf",
           "Axiomas_360X_Audiolivro_roteiro.txt", "Axiomas_360X_Mapa_dos_Eixos.pdf",
           "Axiomas_360X_Miolo_Impressao_A5_sangria3mm.pdf", "Axiomas_360X_Capa_Dura_arte.pdf", "Axiomas_360X_Capa_Dura_gabarito.pdf"):
    shutil.copy(os.path.join(OUT, fn), f"{APP}/downloads/{fn}")
print("livro → autor/axiomas-360x.html", os.path.getsize(f"{APP}/autor/axiomas-360x.html"), "bytes · downloads ok")
