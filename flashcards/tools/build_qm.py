"""Gera data/questoes.json e data/micro.json (TEMI e R3) a partir de qm/*.py."""
import json, random, re, sys, importlib, hashlib, shutil, os
sys.path.insert(0, "/home/claude/anki/qm")
OUT = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/app2"
TEMA_MAP = {"Endócrino e metabólico": "Endocrinologia", "Gastro intensiva": "Gastro e nutrição", "Nutrição": "Gastro e nutrição", "Obstetrícia na UTI": "Obstetrícia", "Ética e morte encefálica": "Ética, paliativos e morte encefálica", "Ética e cuidados paliativos": "Ética, paliativos e morte encefálica", "LRA e diálise": "Nefrologia e distúrbios"}
def mk(qid, tema, enun, alts, gab, com, porque=None, pega="", img=None):
    tema = TEMA_MAP.get(tema, tema)
    correct = alts["ABCDE".index(gab)]; pairs = list(zip(alts, porque or [""] * 5))
    if not all(re.match(r"^[~\d]", a) for a in alts):
        random.Random(int(hashlib.md5(qid.encode()).hexdigest(), 16)).shuffle(pairs)
    a2 = [p[0] for p in pairs]
    if img:
        shutil.copy(f"/home/claude/anki/qimg/{img}", f"{OUT}/data/media/{img}")
        enun = enun + f'<img class="qzImg" src="data/media/{img}" alt="Esquema didático">'
    q = {"id": qid, "tema": tema, "enun": enun, "alts": a2, "gab": a2.index(correct), "com": com}
    if porque: q["porque"] = [p[1] for p in pairs]
    if pega: q["pega"] = pega
    return q
def qs(mods, xmods, pref, newmods):
    X = sum((importlib.import_module(m).X for m in xmods), []); out = []
    for m in mods:
        for tema, enun, alts, gab, com in importlib.import_module(m).Q:
            i = len(out); x = X[i] if i < len(X) else (None, "")
            out.append(mk(f"{pref}{i+1:03d}", tema, enun, alts, gab, com, x[0], x[1]))
    for m in newmods:
        for tema, enun, alts, gab, com, porque, pega, img in importlib.import_module(m).Q:
            out.append(mk(f"{pref}{len(out)+1:03d}", tema, enun, alts, gab, com, porque, pega, img))
    return out
Q = {"temi": qs(["qt1", "qt2", "qt3", "qt4"], ["xt1", "xt2"], "QT", ["nqt1","nqt2","nqt3","nqt4","nqt5"]), "r3": qs(["qr1", "qr2", "qr3", "qr4"], ["xr1", "xr2"], "QR", ["nqr1","nqr2","nqr3","nqr4","nqr5"])}
from mt import M as MT
from mr import M as MR
from cmt import C
MT = [m for m in MT if m[2] not in ("Profilaxia de úlcera", "Índice de choque")]
MT = [tuple(x.replace("Aperte 10 s o dedo indicador por 10 s.", "Pressione a polpa do dedo por 10 s e conte.") for x in m) for m in MT]
mic = lambda L, p: [{"id": f"{p}{i+1:03d}", "tema": t, "emoji": e, "titulo": ti, "texto": tx, "gancho": g, "comentario": C.get(ti, "")} for i, (t, e, ti, tx, g) in enumerate(L)]
MC = {"temi": mic(MT, "MT"), "r3": mic(MR, "MR")}
json.dump(Q, open(f"{OUT}/data/questoes.json", "w"), ensure_ascii=False)
json.dump(MC, open(f"{OUT}/data/micro.json", "w"), ensure_ascii=False)
from collections import Counter
for k in Q: print(k, len(Q[k]), Counter("ABCDE"[q["gab"]] for q in Q[k]), "porque", sum(1 for q in Q[k] if q.get("porque")), "micro", len(MC[k]), "com", sum(1 for m in MC[k] if m["comentario"]))
