"""Gera Curvas de VM 360X (150) + POCUS na UTI 360X (150): imagens sintéticas, pacotes de mídia por tema e 20 baralhos.

Uso: python3 build_vp.py <APP_DIR> [--only vm|pocus] [--no-img] [--ids N,N]
Saídas: <APP>/data/decks/{vmc,pocus}-NN-slug.json · <APP>/data/media/vp/{vm,us}-NN.json (base64) · PNG-fonte em data/media/vp/png/
        tools/vmpocus/vp_cards.json (manifesto para pack e Anki)
"""
import base64, html, json, os, re, sys, time, unicodedata
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import vm_cards, vm_cards2, vm_cards3, vm_cards4
VM_THEMES = vm_cards.THEMES + vm_cards2.THEMES + vm_cards3.THEMES + vm_cards4.THEMES
try:
    import us_cards, us_cards2
    US_THEMES = us_cards.THEMES + us_cards2.THEMES
except ImportError:
    US_THEMES = []
COLS = {"vm": ("vmc", "🫁 Curvas de VM 360X", "Curva VM", "vm"), "us": ("pocus", "🔊 POCUS na UTI 360X", "POCUS", "us")}
FONTE = ("Síntese 360X de conceitos consagrados de ventilação mecânica e ultrassom point-of-care (conferir na diretriz vigente). "
         "Imagem sintética didática gerada por computador — não é exame de paciente.")
QV = "O que esta curva mostra e qual a conduta?"; QU = "Qual o achado e qual a conduta?"


def esc(s): return html.escape(s, quote=False)


def slug(name):
    s = re.sub(r"^\d+\s*\S+\s*", "", name); s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:40].strip("-")


def flat(themes, kind):
    out, n = [], 0
    for ti, (tema, lst) in enumerate(themes, 1):
        for k in lst: n += 1; out.append(dict(n=n, ti=ti, tema=tema, kind=kind, **k))
    return out


def render_one(card):
    sp = card["sp"]; path = card["_path"]; label = f"{COLS[card['kind']][2]} #{card['n']:03d}"; seed = card["n"] * 11 + (3 if card["kind"] == "vm" else 7)
    if card["kind"] == "vm":
        from vm_gen import make
        make({k: v for k, v in sp.items() if k != "kind"}, path, label, seed=seed)
    else:
        import us_modes as M, us_scenes as S
        k = sp["kind"]
        if k == "b": M.single(path, label, getattr(S, sp["scene"])(seed=seed, **sp["args"]), sub=sp.get("sub", ""), seed=seed)
        elif k == "pair": M.pair(path, label, getattr(S, sp["a"][0])(seed=seed, **sp["a"][1]), getattr(S, sp["b"][0])(seed=seed, **sp["b"][1]), sp["la"], sp["lb"], sub=sp.get("sub", ""), seed=seed)
        elif k == "mml": M.mm_lung(path, label, sp["mk"], seed=seed, sub=sp.get("sub", ""), **sp["p"])
        elif k == "mmt": M.mm_track(path, label, sp["mk"], seed=seed, sub=sp.get("sub", ""), **sp["p"])
        elif k == "dop": M.doppler(path, label, sp["dk"], seed=seed, sub=sp.get("sub", ""), **sp["p"])
        else: raise ValueError(k)
    return card["kind"], card["n"], os.path.getsize(path)


def main():
    app = sys.argv[1]; noimg = "--no-img" in sys.argv
    only = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None
    ids = {int(x) for x in sys.argv[sys.argv.index("--ids") + 1].split(",")} if "--ids" in sys.argv else None
    sets = [("vm", VM_THEMES), ("us", US_THEMES)]
    pdir = os.path.join(app, "data/media/vp/png"); os.makedirs(pdir, exist_ok=True)
    allc = []
    for kind, themes in sets:
        if only and only != kind: continue
        cs = flat(themes, kind)
        dxs = [c["dx"] for c in cs]; dup = {d for d in dxs if dxs.count(d) > 1}
        assert not dup, dup
        for c in cs:
            for f in ("ctx", "dx", "crit", "cond", "peg"): assert c[f] and c[f].strip(), (kind, c["n"], f)
            c["_path"] = os.path.join(pdir, f"{kind}_{c['n']:03d}.png")
        print(kind, len(themes), "temas", len(cs), "cards")
        allc += cs
    if not noimg:
        todo = [c for c in allc if ids is None or c["n"] in ids]; t0 = time.time()
        with Pool(2) as p:
            for kind, n, sz in p.imap_unordered(render_one, todo, chunksize=3):
                if n % 25 == 0: print(f"  {kind} {n:03d} {sz // 1024} KB · {time.time() - t0:.0f}s", flush=True)
    man = json.load(open(os.path.join(HERE, "vp_cards.json"))) if os.path.exists(os.path.join(HERE, "vp_cards.json")) and only else {"decks": [], "cards": []}
    if only: man["decks"] = [d for d in man["decks"] if not d["arquivo"].split("/")[-1].startswith(COLS[only][0] + "-")]; man["cards"] = [c for c in man["cards"] if c["kind"] != only]
    for kind, themes in sets:
        if only and only != kind: continue
        col, root, lab, pre = COLS[kind]
        for ti, (tema, lst) in enumerate(themes, 1):
            cs = [c for c in allc if c["kind"] == kind and c["ti"] == ti]
            nome = f"{col}-{ti:02d}-{slug(tema)}.json"; bundle = f"data/media/vp/{pre}-{ti:02d}.json"
            midia, out, itens = {}, [], {}
            for c in cs:
                img = f"{pre}_{c['n']:03d}.png"; midia[img] = f"{bundle}#{img}"
                itens[img] = base64.b64encode(open(c["_path"], "rb").read()).decode()
                card = {"frente": f"{'🫁' if kind == 'vm' else '🔊'} <b>{lab} #{c['n']:03d}</b> · {esc(c['ctx'])}<br>❓ {esc(c['q'] or (QV if kind == 'vm' else QU))}",
                        "imagem_frente": img,
                        "verso": f"✅ <b>{esc(c['dx'])}</b><br>🔎 {esc(c['crit'])}<br>⚡ <b>Conduta:</b> {esc(c['cond'])}",
                        "pegadinha": esc(c["peg"]), "fonte": FONTE,
                        "tags": ["VM" if kind == "vm" else "POCUS", f"{pre.upper()}_T{ti:02d}", "TEMI2028", "imagem_sintetica"]}
                out.append(card); man["cards"].append(dict(card, baralho=f"{root}::{tema}", n=c["n"], kind=kind))
            json.dump({"formato": "codice360x-midia-v1", "tipo": "image/png", "itens": itens}, open(os.path.join(app, bundle), "w"), separators=(",", ":"))
            json.dump({"formato": "codice360x-v1", "baralho": f"{root}::{tema}", "midia": midia, "cards": out}, open(os.path.join(app, "data/decks", nome), "w"), ensure_ascii=False, indent=1)
            man["decks"].append(dict(colecao=col, arquivo=f"data/decks/{nome}", tema=tema, cards=len(out), subtemas=[]))
    json.dump(man, open(os.path.join(HERE, "vp_cards.json"), "w"), ensure_ascii=False, indent=1)
    print("baralhos:", len(man["decks"]), "cards:", len(man["cards"]))


if __name__ == "__main__":
    main()
