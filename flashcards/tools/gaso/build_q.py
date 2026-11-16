"""145 questões de gasometria → data/questoes.json (divisão 'gaso'): QG001–QG100 (4.13.0, idênticas) + QG101–QG145 (4.14.0).
Uso: python3 build_q.py <APP_DIR> [<APP_DIR2> ...]"""
import json, random, sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import q_auto, q_man, q_man2

rnd = random.Random(2028)
Q = q_auto.build(rnd)
man = [q for q in q_man.QM if "Gasometria venosa periférica é suficiente" not in q["enun"]]
for q in man:
    idx = list(range(5)); rnd.shuffle(idx)
    q2 = dict(q); q2["alts"] = [q["alts"][i] for i in idx]; q2["porque"] = [q["porque"][i] for i in idx]; q2["gab"] = idx.index(q["gab"])
    q2["id"] = f"QG{len(Q)+1:03d}"
    Q.append(q2)
assert len(Q) == 100, len(Q)
# QG001–QG100 congeladas como publicadas na 4.13.0 (o gerador automático usa conjuntos → ordem pode variar entre execuções)
FROZEN = os.path.join(HERE, "gaso_questoes_v413.json")
if os.path.exists(FROZEN):
    Q = json.load(open(FROZEN, encoding="utf-8"))[:100]
rnd2 = random.Random(2029)
for q in q_man2.QM2:
    idx = list(range(5)); rnd2.shuffle(idx)
    q2 = dict(q); q2["alts"] = [q["alts"][i] for i in idx]; q2["porque"] = [q["porque"][i] for i in idx]; q2["gab"] = idx.index(q["gab"])
    q2["id"] = f"QG{len(Q)+1:03d}"
    Q.append(q2)
assert len(Q) == 145, len(Q)
ids = set()
for q in Q:
    assert q["id"] not in ids; ids.add(q["id"])
    assert len(q["alts"]) == 5 and len(set(q["alts"])) == 5, q["id"]
    assert len(q["porque"]) == 5 and (all(q["porque"]) or int(q["id"][2:]) <= 100), q["id"]
    assert 0 <= q["gab"] < 5 and q["com"] and q["pega"] and q["tema"], q["id"]
    q["porque"] = [p.replace("Correta: ", "").replace("Incorreta: ", "") for p in q["porque"]]
from collections import Counter
print("questões:", len(Q), "· gabaritos:", dict(sorted(Counter(q["gab"] for q in Q).items())), "· temas:", len(set(q["tema"] for q in Q)))
for app in sys.argv[1:]:
    p = f"{app}/data/questoes.json"; d = json.load(open(p))
    d["gaso"] = Q
    json.dump(d, open(p, "w"), ensure_ascii=False)
    print(p, os.path.getsize(p) // 1024, "KB")
json.dump(Q, open(os.path.join(HERE, "gaso_questoes.json"), "w"), ensure_ascii=False, indent=0)
