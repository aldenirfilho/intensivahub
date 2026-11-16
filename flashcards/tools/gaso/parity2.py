"""Paridade Python × JS dos extras 4.14.0 (VM, venosa, POCUS): gera /tmp/parity2.json com x, xsteps e painel."""
import json, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gaso_engine import analyze, panel
rnd = random.Random(414); out = []
for i in range(3000):
    lab = dict(pco2=rnd.randint(18, 95), hco3=rnd.randint(6, 45), na=rnd.randint(128, 150), cl=rnd.randint(85, 118))
    if rnd.random() < .7: lab.update(pao2=rnd.randint(45, 250), fio2=rnd.choice([0.21, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0]), sat=rnd.randint(80, 100), hb=round(rnd.uniform(6, 15), 1))
    if rnd.random() < .6:
        vm = dict(modo=rnd.choice(["VCV", "PCV", "PSV"]), vc=rnd.randint(250, 650), fr=rnd.randint(8, 34), peep=rnd.randint(5, 18))
        if rnd.random() < .7: vm["pplat"] = vm["peep"] + rnd.randint(6, 22)
        if rnd.random() < .6: vm["etco2"] = max(10, lab["pco2"] - rnd.randint(0, 25))
        if rnd.random() < .7: vm["pbw"] = rnd.randint(45, 80)
        if rnd.random() < .6: vm["alvo"] = rnd.choice([35, 40, 45, 50, 55, 60])
        lab["vm"] = vm
    if rnd.random() < .6:
        k = rnd.choice(["central", "mista", "periferica"])
        ve = dict(kind=k, pco2=lab["pco2"] + rnd.randint(1, 16))
        if k != "periferica": ve.update(sat=rnd.randint(40, 88), pao2=rnd.randint(25, 50))
        else: ve.update(ph=round(7.0 + rnd.random() * 0.5, 2), hco3=lab["hco3"] + rnd.randint(0, 3))
        lab["ven"] = ve
    if rnd.random() < .3: lab["us"] = "linhas B difusas bilaterais; VCI 2,3 cm sem variação"
    R = analyze(lab)
    out.append(dict(lab=lab, codes=R["codes"], x=R["x"], xsteps=R["xsteps"], panel=panel(lab)))
json.dump(out, open("/tmp/parity2.json", "w"), ensure_ascii=False)
print("casos", len(out))
