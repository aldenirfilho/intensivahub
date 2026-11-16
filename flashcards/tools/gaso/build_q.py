"""100 questões de gasometria → data/questoes.json (divisão 'gaso'). Uso: python3 build_q.py <APP_DIR> [<APP_DIR2> ...]"""
import json, random, sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import q_auto, q_man

rnd = random.Random(2028)
Q = q_auto.build(rnd)
man = [q for q in q_man.QM if "Gasometria venosa periférica é suficiente" not in q["enun"]]
for q in man:
    idx = list(range(5)); rnd.shuffle(idx)
    q2 = dict(q); q2["alts"] = [q["alts"][i] for i in idx]; q2["porque"] = [q["porque"][i] for i in idx]; q2["gab"] = idx.index(q["gab"])
    q2["id"] = f"QG{len(Q)+1:03d}"
    Q.append(q2)
assert len(Q) == 100, len(Q)
ids = set()
for q in Q:
    assert q["id"] not in ids; ids.add(q["id"])
    assert len(q["alts"]) == 5 and len(set(q["alts"])) == 5, q["id"]
    assert len(q["porque"]) == 5 and all(q["porque"]), q["id"]
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
