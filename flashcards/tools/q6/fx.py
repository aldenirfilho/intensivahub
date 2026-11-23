"""Atalhos para escrever as especificações das figuras nas fontes t*.py / r*.py (questões ilustradas 4.24.0)."""


def E(n, lay=None, **over):
    d = {"k": "ecg", "n": n}
    if over: d["over"] = over
    if lay: d["lay"] = lay
    return d
def V(n, **over): return {"k": "vm", "n": n, **({"over": over} if over else {})}
def U(n): return {"k": "us", "n": n}
def MON(ch, num=(), **k): return {"k": "mon", "ch": list(ch), "num": list(num), **k}
def LN(series, **k): return {"k": "lines", "series": list(series), **k}
def S(y, lab=None, **k): return {"y": list(y), "lab": lab, **k}
def BR(cats, groups, **k): return {"k": "bars", "cats": list(cats), "groups": list(groups), **k}
def G(v, lab=None, **k): return {"v": list(v), "lab": lab, **k}
def TB(cols, rows, **k): return {"k": "tab", "cols": list(cols), "rows": [list(r) for r in rows], **k}
def CX(*mods, **k): return {"k": "cxr", "mods": list(mods), **k}
def CT(*mods, **k): return {"k": "ct", "mods": list(mods), **k}
def MI(modo, tipo, **k): return {"k": "micro", "modo": modo, "tipo": tipo, **k}
def FL(nodes, edges, **k): return {"k": "flow", "nodes": list(nodes), "edges": list(edges), **k}
def KM(arms, tmax, **k): return {"k": "km", "arms": list(arms), "tmax": tmax, **k}
def FO(rows, **k): return {"k": "forest", "rows": list(rows), **k}
def ROC(curves, **k): return {"k": "roc", "curves": list(curves), **k}
def EEG(tipo, **k): return {"k": "eeg", "tipo": tipo, **k}
def ROT(ch, **k): return {"k": "rotem", "ch": list(ch), **k}
def SP(tipo, **k): return {"k": "spiro", "tipo": tipo, **k}
def PV(*loops, **k): return {"k": "pvloop", "loops": [{"tipo": t, "lab": l} for t, l in loops], **k}
def O2(curves, **k): return {"k": "o2hb", "curves": list(curves), **k}
def EP(tipo, **k): return {"k": "ep", "tipo": tipo, **k}
def SC(tipo, **k): return {"k": "scint", "tipo": tipo, **k}
def BD(frente=(), costas=(), **k): return {"k": "body", "frente": list(frente), "costas": list(costas), **k}
def GB(cols): return {"k": "gamble", "cols": list(cols)}
def NOMO(pts): return {"k": "nomo", "pts": list(pts)}

# canais do monitor
def ecg(n, **k): return {"t": "ecg", "n": n, **k}
def art(s=120, d=70, **k): return {"t": "art", "s": s, "d": d, **k}
def pleth(**k): return {"t": "pleth", **k}
def co2(et=38, tipo="normal", **k): return {"t": "co2", "et": et, "tipo": tipo, **k}
def cvp(tipo="normal", **k): return {"t": "cvp", "tipo": tipo, **k}
def icp(tipo="normal", m=12, **k): return {"t": "icp", "tipo": tipo, "m": m, **k}
