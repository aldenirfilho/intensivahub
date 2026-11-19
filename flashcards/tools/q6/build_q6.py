#!/usr/bin/env python3
"""🖼️ Questões ilustradas (app 4.24.0): +200 TEMI (QT901–QT1100) e +200 R3 Clínica Médica (QR901–QR1100) → data/questoes.json,
com figura sintética própria em pacotes de mídia data/media/qi/{qt,qr}-NN.json (20 imagens por pacote, base64).
Fonte: tools/q6/t*.py (TEMI) e r*.py (R3). Cada item: (tema, enunciado, [(alternativa, porquê)×5 — correta primeiro], comentário, pegadinha, referência, figura).
Append idempotente: mantém as questões 1–900 e a divisão gaso; substitui só os ids ≥ 901.
Uso: python3 tools/q6/build_q6.py <APP_DIR> [--check] [--no-img] [--force] [--only QT905,QR910] [--sheets]"""
import json, sys, os, hashlib, random, re, importlib, collections, base64, time
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "q5"))
from build_q5 import mk, TT, TR, toks   # mesmas regras de embaralhamento e campos do lote anterior

LOTE = "2026-11-il"; PER_PACK = 20; FIRST = 901
OUT = os.path.join(HERE, "out"); PNG = os.path.join(OUT, "img")
ALT = {"ecg": "Eletrocardiograma", "vm": "Curvas do ventilador mecânico", "us": "Imagem de ultrassom à beira do leito (POCUS)", "mon": "Tela de monitor multiparamétrico",
       "lines": "Gráfico", "bars": "Gráfico de barras", "tab": "Tabela de exames", "km": "Curvas de Kaplan-Meier", "forest": "Gráfico de floresta (metanálise)",
       "roc": "Curvas ROC", "flow": "Fluxograma", "gamble": "Gamblegrama", "nomo": "Nomograma de Rumack-Matthew", "ep": "Eletroforese de proteínas séricas",
       "rotem": "Tromboelastometria (ROTEM)", "spiro": "Curva fluxo-volume (espirometria)", "pvloop": "Alças pressão-volume do ventrículo esquerdo",
       "o2hb": "Curvas de dissociação da hemoglobina", "eeg": "Eletroencefalograma", "cxr": "Radiografia de tórax", "ct": "Tomografia de crânio",
       "micro": "Imagem de microscopia", "scint": "Cintilografia de tireoide", "body": "Mapa corporal"}


def load(prefix):
    its = []
    for i in range(1, 21):
        f = f"{prefix}{i}"
        if not os.path.exists(os.path.join(HERE, f + ".py")): continue
        for it in importlib.import_module(f).Q:
            assert len(it) == 7, (f, it[1][:60]); assert isinstance(it[6], dict) and "k" in it[6], (f, it[1][:60], "figura")
            its.append(it)
    return its


def build(pref, prefix, MAP):
    import figs
    its = load(prefix); P = [i % 5 for i in range(len(its))]; random.Random("lote-2026-11-il-" + pref).shuffle(P); out = []
    for i, it in enumerate(its):
        qid = f"{pref}{FIRST + i}"; q = mk(qid, *it[:6], MAP, P[i]); q["lote"] = LOTE
        sp = it[6]; ext = figs.ext(sp); pk = f"{pref.lower()}-{i // PER_PACK + 1:02d}"
        q["fig"] = {"p": f"data/media/qi/{pk}.json", "k": qid + ext, "alt": ALT.get(sp["k"], "Figura") + " (figura sintética didática)"}
        q["_spec"] = sp; out.append(q)
    return out


def _render(job):
    import figs
    qid, sp, path = job
    seed = int(hashlib.md5(qid.encode()).hexdigest(), 16) % 9973 + 11
    t = time.time()
    try: n = figs.render(sp, path, f"Figura {qid}", seed=seed)
    except Exception as e: print("❌", qid, sp.get("k"), e, flush=True); raise
    return qid, n, time.time() - t


def sheets(L, d):
    from PIL import Image
    os.makedirs(d, exist_ok=True)
    for k in range(0, len(L), 9):
        ims = []
        for q in L[k:k + 9]:
            im = Image.open(os.path.join(PNG, q["fig"]["k"])).convert("RGB"); w = 520; ims.append(im.resize((w, int(im.height * w / im.width))))
        rows = [ims[i:i + 3] for i in range(0, len(ims), 3)]; H = sum(max(i.height for i in r) for r in rows); S = Image.new("RGB", (1560, H), "white"); y = 0
        for r in rows:
            x = 0
            for i in r: S.paste(i, (x, y)); x += 520
            y += max(i.height for i in r)
        S.save(os.path.join(d, f"{L[k]['id']}.jpg"), quality=72)


if __name__ == "__main__":
    APP = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "."
    only = set(sys.argv[sys.argv.index("--only") + 1].split(",")) if "--only" in sys.argv else None
    NEW = {"temi": build("QT", "t", TT), "r3": build("QR", "r", TR)}
    p = os.path.join(APP, "data", "questoes.json"); d = json.load(open(p, encoding="utf-8")); rep = []
    for k, L in NEW.items():
        old = [q for q in d[k] if int(q["id"][2:]) < FIRST]; assert len(old) == 900, (k, len(old))
        TK = [(q["id"], toks(q["enun"] + " " + q["alts"][q["gab"]])) for q in old]; seen = []
        for q in L:
            t = toks(q["enun"] + " " + q["alts"][q["gab"]])
            for qid, t2 in TK + seen:
                j = len(t & t2) / max(1, len(t | t2))
                if j >= 0.5: rep.append(f"⚠️ {q['id']} ~ {qid} (Jaccard {j:.2f}): {q['enun'][:70]}")
            seen.append((q["id"], t))
        print(k, len(L), "novas · gabaritos", dict(sorted(collections.Counter("ABCDE"[q["gab"]] for q in L).items())),
              "· figuras", dict(collections.Counter(q["_spec"]["k"] for q in L).most_common()))
        print("   temas", dict(collections.Counter(q["tema"] for q in L).most_common()))
    print("\n".join(rep) if rep else "✅ sem enunciados muito parecidos (Jaccard < 0,5)")
    if "--no-img" not in sys.argv:
        os.makedirs(PNG, exist_ok=True); cache_p = os.path.join(OUT, "spec_hash.json")
        cache = json.load(open(cache_p)) if os.path.exists(cache_p) and "--force" not in sys.argv else {}
        jobs = []
        for L in NEW.values():
            for q in L:
                h = hashlib.md5(json.dumps([q["_spec"], q["id"], 3], sort_keys=True, ensure_ascii=False).encode()).hexdigest()
                path = os.path.join(PNG, q["fig"]["k"])
                if (only and q["id"] in only) or (not only and (cache.get(q["id"]) != h or not os.path.exists(path))): jobs.append((q["id"], q["_spec"], path)); cache[q["id"]] = h
        t0 = time.time()
        with Pool(4) as pool:
            for i, (qid, n, dt) in enumerate(pool.imap_unordered(_render, jobs, chunksize=2)):
                if dt > 6 or i % 50 == 0: print(f"   {qid} {n // 1024} KB {dt:.1f}s", flush=True)
        json.dump(cache, open(cache_p, "w"), indent=0); print(len(jobs), "figuras geradas em", f"{time.time() - t0:.0f}s")
        if "--sheets" in sys.argv:
            for L in NEW.values(): sheets([q for q in L if not only or q["id"] in only], os.path.join(OUT, "sheets"))
    if "--check" in sys.argv: sys.exit(0)
    # pacotes de mídia
    md = os.path.join(APP, "data", "media", "qi"); os.makedirs(md, exist_ok=True); tot = 0
    for L in NEW.values():
        packs = collections.OrderedDict()
        for q in L: packs.setdefault(q["fig"]["p"], []).append(q["fig"]["k"])
        for pth, keys in packs.items():
            itens = {kk: base64.b64encode(open(os.path.join(PNG, kk), "rb").read()).decode() for kk in keys}
            json.dump({"formato": "codice360x-midia-v1", "tipo": "image/png", "itens": itens}, open(os.path.join(APP, pth), "w"), separators=(",", ":"))
            tot += os.path.getsize(os.path.join(APP, pth))
    for L in NEW.values():
        for q in L: q.pop("_spec", None)
    for k, L in NEW.items(): d[k] = [q for q in d[k] if int(q["id"][2:]) < FIRST] + L
    json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False)
    json.dump(NEW, open(os.path.join(HERE, "q6_questoes.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print(p, os.path.getsize(p) // 1024, "KB ·", {k: len(v) for k, v in d.items()}, "· pacotes de mídia", tot // 1024, "KB")
