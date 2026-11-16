"""Gera o Compêndio de ECG 360X: 300 traçados sintéticos (PNG) + 18 baralhos codice360x-v1.

Uso: python3 build_ecg.py <APP_DIR> [--only N,N,...] [--no-img]
Saídas: <APP>/data/decks/ecg-NN-slug.json, <APP>/data/media/ecg/ecg_NNN.png (fonte) + ecg-NN.json (pacote base64 servido ao app), tools/ecg/ecg_cards.json
"""
import base64, html, json, os, re, sys, time, unicodedata
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import k01_ritmo, k02_conducao, k03_taqui, k04_isquemia, k05_metabolico, k06_outros

THEMES = k01_ritmo.THEMES + k02_conducao.THEMES + k03_taqui.THEMES + k04_isquemia.THEMES + k05_metabolico.THEMES + k06_outros.THEMES
ROOT = "📈 Compêndio de ECG 360X"
FONTE = ("Síntese 360X de critérios eletrocardiográficos consagrados (conferir na diretriz vigente). "
         "Traçado sintético didático gerado por computador — não é ECG de paciente.")
Q = "Qual a principal alteração deste traçado?"


def esc(s): return html.escape(s, quote=False)


def slug(name):
    s = re.sub(r"^\d+\s*\S+\s*", "", name)
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:40].strip("-")


def cards_flat():
    out, n = [], 0
    for ti, (tema, lst) in enumerate(THEMES, 1):
        for k in lst:
            n += 1
            out.append(dict(n=n, ti=ti, tema=tema, **k))
    return out


def render_one(card):
    from ecg_gen import build, render
    path = card["_path"]
    L, lay = build(card["sp"], seed=card["n"] * 7 + 3)
    render(L, lay, title=f"ECG #{card['n']:03d}", path=path)
    return card["n"], os.path.getsize(path)


def main():
    app = sys.argv[1]; only = None; noimg = "--no-img" in sys.argv
    if "--only" in sys.argv: only = {int(x) for x in sys.argv[sys.argv.index("--only") + 1].split(",")}
    cards = cards_flat()
    assert len(THEMES) == 18, len(THEMES)
    assert len(cards) == 300, len(cards)
    dxs = [c["dx"] for c in cards]
    dup = {d for d in dxs if dxs.count(d) > 1}
    assert not dup, dup
    for c in cards:
        for f in ("ctx", "dx", "crit", "cond", "peg"): assert c[f] and c[f].strip(), (c["n"], f)
    mdir = os.path.join(app, "data/media/ecg"); os.makedirs(mdir, exist_ok=True)
    for c in cards: c["_path"] = os.path.join(mdir, f"ecg_{c['n']:03d}.png")
    if not noimg:
        todo = [c for c in cards if only is None or c["n"] in only]
        t0 = time.time()
        with Pool(2) as p:
            for n, sz in p.imap_unordered(render_one, todo, chunksize=4):
                if n % 25 == 0: print(f"  img {n:03d} {sz // 1024} KB · {time.time() - t0:.0f}s", flush=True)
    # baralhos
    ddir = os.path.join(app, "data/decks"); flat = []
    decks = []
    for ti, (tema, lst) in enumerate(THEMES, 1):
        cs = [c for c in cards if c["ti"] == ti]
        nome = f"ecg-{ti:02d}-{slug(tema)}.json"
        midia, out, itens = {}, [], {}
        bundle = f"data/media/ecg/ecg-{ti:02d}.json"   # 1 arquivo por tema (limite de arquivos do artifact)
        for c in cs:
            img = f"ecg_{c['n']:03d}.png"; midia[img] = f"{bundle}#{img}"
            itens[img] = base64.b64encode(open(c["_path"], "rb").read()).decode()
            card = {
                "frente": f"📈 <b>ECG #{c['n']:03d}</b> · {esc(c['ctx'])}<br>❓ {esc(c['q'] or Q)}",
                "imagem_frente": img,
                "verso": f"✅ <b>{esc(c['dx'])}</b><br>🔎 {esc(c['crit'])}<br>⚡ <b>Conduta:</b> {esc(c['cond'])}",
                "pegadinha": esc(c["peg"]),
                "fonte": FONTE,
                "tags": ["ECG", f"ECG_T{ti:02d}", "TEMI2028", "R3CM", "tracado_sintetico"],
            }
            out.append(card); flat.append(dict(card, baralho=f"{ROOT}::{tema}", n=c["n"]))
        json.dump({"formato": "codice360x-midia-v1", "tipo": "image/png", "itens": itens}, open(os.path.join(app, bundle), "w"), separators=(",", ":"))
        deck = {"formato": "codice360x-v1", "baralho": f"{ROOT}::{tema}", "midia": midia, "cards": out}
        json.dump(deck, open(os.path.join(ddir, nome), "w"), ensure_ascii=False, indent=1)
        decks.append(dict(colecao="ecg", arquivo=f"data/decks/{nome}", tema=tema, cards=len(out), subtemas=[]))
    json.dump(dict(decks=decks, cards=flat), open(os.path.join(HERE, "ecg_cards.json"), "w"), ensure_ascii=False, indent=1)
    print("baralhos:", len(decks), "cards:", sum(d["cards"] for d in decks))


if __name__ == "__main__":
    main()
