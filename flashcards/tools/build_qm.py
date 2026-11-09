"""Gera data/questoes.json e data/micro.json (TEMI e R3) a partir de qm/*.py."""
import json, random, re, sys, importlib, hashlib
sys.path.insert(0, "/home/claude/anki/qm")
OUT = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/app2"
def qs(mods, pref):
    out = []
    for m in mods:
        for tema, enun, alts, gab, com in importlib.import_module(m).Q:
            i = len(out) + 1; qid = f"{pref}{i:03d}"; correct = alts["ABCDE".index(gab)]
            if not all(re.match(r"^[~\d]", a) for a in alts):
                rnd = random.Random(int(hashlib.md5(qid.encode()).hexdigest(), 16)); alts = alts[:]; rnd.shuffle(alts)
            out.append({"id": qid, "tema": tema, "enun": enun, "alts": alts, "gab": alts.index(correct), "com": com})
    return out
Q = {"temi": qs(["qt1", "qt2", "qt3", "qt4"], "QT"), "r3": qs(["qr1", "qr2", "qr3", "qr4"], "QR")}
from mt import M as MT
from mr import M as MR
MT = [m for m in MT if m[2] not in ("Profilaxia de úlcera", "Índice de choque")]
MT = [tuple(x.replace("Aperte 10 s o dedo indicador por 10 s.", "Pressione a polpa do dedo por 10 s e conte.") for x in m) for m in MT]
mic = lambda L, p: [{"id": f"{p}{i+1:03d}", "tema": t, "emoji": e, "titulo": ti, "texto": tx, "gancho": g} for i, (t, e, ti, tx, g) in enumerate(L)]
MC = {"temi": mic(MT, "MT"), "r3": mic(MR, "MR")}
json.dump(Q, open(f"{OUT}/data/questoes.json", "w"), ensure_ascii=False)
json.dump(MC, open(f"{OUT}/data/micro.json", "w"), ensure_ascii=False)
from collections import Counter
for k in Q: print(k, len(Q[k]), Counter("ABCDE"[q["gab"]] for q in Q[k]), "micro", len(MC[k]))
