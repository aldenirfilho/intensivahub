"""🖼️ Despachante das figuras das questões ilustradas (4.24.0).
spec["k"]: ecg | vm | us (motores do Compêndio de ECG e de VM/POCUS, por número do card, com semente nova) | lines | bars | tab | km | forest | roc |
flow | gamble | nomo | ep | rotem | spiro | pvloop | o2hb | mon | eeg | cxr | ct | micro | scint | body"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
for p in ("ecg", "vmpocus"): sys.path.insert(0, os.path.join(HERE, "..", p))
sys.path.insert(0, HERE)
import figs_core as C, figs_mon as MO, figs_img as I
from PIL import Image

JPG = {"cxr", "ct", "micro", "scint", "us"}
_ECG = _VP = None


def ext(spec): return ".jpg" if spec["k"] in JPG else ".png"


def ecg_card(n):
    global _ECG
    if _ECG is None:
        from build_ecg import cards_flat
        _ECG = {c["n"]: c for c in cards_flat()}
    return _ECG[n]


def vp_card(kind, n):
    global _VP
    if _VP is None:
        import build_vp as B
        _VP = {("vm", c["n"]): c for c in B.flat(B.VM_THEMES, "vm")}; _VP.update({("us", c["n"]): c for c in B.flat(B.US_THEMES, "us")})
    return _VP[(kind, n)]


def render(spec, path, title, seed=1):
    k = spec["k"]
    if k == "ecg":
        from ecg_gen import build, render as er
        sp = dict(ecg_card(spec["n"])["sp"]); sp.update(spec.get("over", {}))
        L, lay = build(sp, seed=seed); er(L, spec.get("lay", lay), title=title, path=path)
    elif k == "vm":
        from vm_gen import make
        sp = {kk: v for kk, v in vp_card("vm", spec["n"])["sp"].items() if kk != "kind"}; sp.update(spec.get("over", {}))
        make(sp, path, title, seed=seed)
    elif k == "us":
        import us_modes as M, us_scenes as S
        sp = vp_card("us", spec["n"])["sp"]; tmp = path[:-4] + ".tmp.png"; kk = sp["kind"]
        if kk == "b": M.single(tmp, title, getattr(S, sp["scene"])(seed=seed, **sp["args"]), sub=sp.get("sub", ""), seed=seed)
        elif kk == "pair": M.pair(tmp, title, getattr(S, sp["a"][0])(seed=seed, **sp["a"][1]), getattr(S, sp["b"][0])(seed=seed, **sp["b"][1]), sp["la"], sp["lb"], sub=sp.get("sub", ""), seed=seed)
        elif kk == "mml": M.mm_lung(tmp, title, sp["mk"], seed=seed, sub=sp.get("sub", ""), **sp["p"])
        elif kk == "mmt": M.mm_track(tmp, title, sp["mk"], seed=seed, sub=sp.get("sub", ""), **sp["p"])
        elif kk == "dop": M.doppler(tmp, title, sp["dk"], seed=seed, sub=sp.get("sub", ""), **sp["p"])
        im = Image.open(tmp); w = 1100
        if im.width > w: im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
        im.convert("RGB").save(path, quality=80, optimize=True, progressive=True); os.remove(tmp)
    elif k == "mon": MO.monitor(dict(spec, seed=seed), path, title)
    elif k == "eeg": MO.eeg(dict(spec, seed=seed), path, title)
    elif k in ("cxr", "ct", "micro", "scint", "body"): getattr(I, k)(dict(spec, seed=spec.get("seed", seed)), path, title)
    else: getattr(C, k)(spec, path, title)
    return os.path.getsize(path)
