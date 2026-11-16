"""Gerador de traçados de ECG sintéticos (didáticos) — CÓDICE 360X · Compêndio de ECG.

Modelo: dipolo cardíaco 3D (x esquerda+, y inferior+, z anterior+) feito de componentes gaussianos
(P, QRS, T, U) projetados nas 12 derivações; ST/T por derivação via "overlays"; motor de ritmo com
eventos atriais e ventriculares (bloqueios, ectopias, FA, flutter, TV, TdP, FV, marca-passo, artefatos).
Papel: 25 mm/s · 10 mm/mV. NÃO é ECG real: é ilustração didática.
"""
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FS = 500
LEADS = ["I", "II", "III", "aVR", "aVL", "aVF", "V1", "V2", "V3", "V4", "V5", "V6"]
def _fr(deg): r = math.radians(deg); return (math.cos(r), math.sin(r), 0.0)
LV = {"I": _fr(0), "II": _fr(60), "III": _fr(120), "aVR": _fr(-150), "aVL": _fr(-30), "aVF": _fr(90),
      "V1": (-0.42, 0.0, 0.91), "V2": (-0.07, 0.0, 1.0), "V3": (0.26, 0.0, 0.97), "V4": (0.5, 0.1, 0.87),
      "V5": (0.82, 0.1, 0.57), "V6": (0.98, 0.1, 0.17), "V4R": (-0.5, 0.1, 0.87)}
GAIN = {l: (1.5 if l.startswith("V") else 1.0) for l in LV}

def g(t, c, s): return np.exp(-0.5 * ((t - c) / s) ** 2)
def ga(t, c, s1, s2): s = np.where(t < c, s1, s2); return np.exp(-0.5 * ((t - c) / s) ** 2)
def sstep(x): x = np.clip(x, 0, 1); return x * x * (3 - 2 * x)
def unit(v): v = np.array(v, float); n = np.linalg.norm(v); return v / n if n else v
def rot(v, ax, deg):  # rotação de um vetor em torno de um eixo
    v = np.array(v, float); k = unit(ax); a = math.radians(deg)
    return v * math.cos(a) + np.cross(k, v) * math.sin(a) + k * np.dot(k, v) * (1 - math.cos(a))

# ---------------- morfologias de QRS: (dt desde o início, sigma, vetor, amplitude) + duração + vetor T + amp T
NORMAL = dict(c=[(0.012, 0.007, (-0.35, 0.15, 0.55), 0.25), (0.038, 0.010, (0.55, 0.5, 0.25), 1.1),
                 (0.052, 0.010, (0.5, 0.3, -0.8), 0.9), (0.072, 0.008, (-0.1, -0.5, -0.6), 0.3)],
              d=0.09, T=(0.55, 0.55, 0.35), Ta=0.32)
def M(**k):
    m = {**NORMAL, **k}; return m
MORPH = {
 "N": NORMAL,
 "rbbb": M(c=NORMAL["c"] + [(0.105, 0.017, (-0.75, 0.05, 0.7), 0.75)], d=0.13, T=(0.65, 0.5, -0.25), Ta=0.3),
 "irbbb": M(c=NORMAL["c"] + [(0.085, 0.010, (-0.6, 0.0, 0.7), 0.35)], d=0.105),
 "lbbb": M(c=[(0.035, 0.018, (0.55, 0.25, -0.75), 1.0), (0.090, 0.022, (0.75, 0.15, -0.65), 1.15)], d=0.15, T=(-0.6, -0.15, 0.7), Ta=0.45),
 "ilbbb": M(c=[(0.03, 0.014, (0.55, 0.35, -0.6), 1.0), (0.07, 0.016, (0.7, 0.25, -0.55), 0.9)], d=0.11, T=(0.0, 0.3, 0.3), Ta=0.2),
 "lafb": M(c=[(0.012, 0.007, (-0.1, 0.55, 0.3), 0.3), (0.042, 0.012, (0.75, -0.55, -0.2), 1.35), (0.06, 0.01, (0.4, -0.3, -0.7), 0.7)], d=0.10, T=(0.6, 0.35, 0.3)),
 "lpfb": M(c=[(0.012, 0.007, (0.4, -0.45, 0.2), 0.3), (0.042, 0.012, (-0.35, 0.95, -0.2), 1.35), (0.06, 0.01, (0.0, 0.5, -0.8), 0.7)], d=0.10, T=(0.3, 0.6, 0.3)),
 "lvh": M(c=[(0.012, 0.007, (-0.35, 0.15, 0.55), 0.25), (0.040, 0.011, (0.6, 0.35, 0.1), 2.0), (0.056, 0.011, (0.45, 0.2, -0.9), 2.0), (0.078, 0.008, (-0.1, -0.4, -0.5), 0.3)], d=0.10, T=(0.55, 0.5, 0.3)),
 "rvh": M(c=[(0.012, 0.007, (-0.3, 0.2, 0.5), 0.25), (0.040, 0.012, (-0.55, 0.8, 0.6), 1.4), (0.06, 0.01, (0.3, 0.3, -0.5), 0.4)], d=0.10, T=(0.4, 0.6, -0.3)),
 "lowv": M(c=[(a, s, v, amp * 0.33) for a, s, v, amp in NORMAL["c"]], Ta=0.13),
 "qinf": M(c=[(0.018, 0.010, (0.1, -0.85, 0.1), 0.55)] + NORMAL["c"][1:], d=0.10),
 "qant": M(c=[(0.014, 0.009, (0.2, 0.2, -0.9), 0.45)] + NORMAL["c"][1:], d=0.10),
 "qlat": M(c=[(0.016, 0.009, (-0.9, 0.2, 0.2), 0.5)] + NORMAL["c"][1:], d=0.10),
 "prwp": M(c=[(0.012, 0.007, (-0.35, 0.15, 0.1), 0.15), (0.040, 0.010, (0.75, 0.5, -0.05), 1.1), (0.054, 0.010, (0.45, 0.3, -0.85), 0.95), (0.072, 0.008, (-0.1, -0.5, -0.6), 0.3)]),
 "post": M(c=[(0.012, 0.007, (-0.35, 0.15, 0.55), 0.25), (0.036, 0.011, (0.3, 0.4, 0.85), 1.1), (0.052, 0.010, (0.7, 0.4, 0.0), 0.8), (0.072, 0.008, (-0.1, -0.5, -0.6), 0.3)], T=(0.55, 0.55, -0.2)),
 "tca": M(c=NORMAL["c"] + [(0.095, 0.016, (-0.85, -0.35, 0.2), 0.75)], d=0.13, Ta=0.3),
 "paced": M(c=[(0.04, 0.024, (0.45, -0.7, -0.5), 1.15), (0.10, 0.024, (0.55, -0.55, -0.6), 0.85)], d=0.16, T=(-0.5, 0.6, 0.6), Ta=0.45),
 "lvpace": M(c=[(0.04, 0.022, (-0.7, 0.4, 0.5), 1.0), (0.095, 0.022, (-0.6, 0.3, 0.7), 0.8)], d=0.15, T=(0.6, -0.3, -0.6), Ta=0.4),
 "pvc_rvot": M(c=[(0.045, 0.026, (0.25, 0.85, -0.6), 1.5), (0.105, 0.024, (0.2, 0.8, -0.5), 0.9)], d=0.16, T=(-0.25, -0.8, 0.6), Ta=0.55),
 "pvc_lv": M(c=[(0.045, 0.026, (-0.6, -0.55, 0.75), 1.5), (0.105, 0.024, (-0.5, -0.4, 0.8), 0.9)], d=0.16, T=(0.6, 0.5, -0.7), Ta=0.55),
 "pvc_lvinf": M(c=[(0.045, 0.026, (-0.45, 0.7, 0.7), 1.5), (0.105, 0.024, (-0.4, 0.6, 0.8), 0.9)], d=0.16, T=(0.5, -0.6, -0.7), Ta=0.55),
 "vt_lbbb": M(c=[(0.05, 0.03, (0.3, -0.3, -0.85), 1.4), (0.12, 0.03, (0.4, -0.2, -0.8), 0.9)], d=0.17, T=(-0.3, 0.3, 0.8), Ta=0.5),
 "vt_nw": M(c=[(0.05, 0.03, (-0.75, -0.6, 0.3), 1.5), (0.12, 0.03, (-0.6, -0.6, 0.4), 0.9)], d=0.17, T=(0.6, 0.6, -0.3), Ta=0.5),
 "vt_posconc": M(c=[(0.05, 0.03, (0.2, 0.3, 0.95), 1.5), (0.12, 0.03, (0.1, 0.3, 0.95), 0.9)], d=0.17, T=(-0.2, -0.3, -0.9), Ta=0.5),
 "vt_negconc": M(c=[(0.05, 0.03, (-0.2, 0.6, -0.95), 1.4), (0.12, 0.03, (-0.1, 0.5, -0.9), 0.9)], d=0.17, T=(0.2, -0.4, 0.9), Ta=0.5),
}
def wpw(vec, short=True):  # delta (rampa lenta) + QRS largo; vetor do delta depende da via acessória
    c = [(0.03, 0.026, unit(vec), 0.62)] + [(a + 0.045, s * 1.25, v, amp) for a, s, v, amp in NORMAL["c"][1:]]
    return M(c=c, d=0.13, T=tuple(-x for x in unit(vec) * 0.6 + np.array(NORMAL["T"]) * 0.4), Ta=0.25)
MORPH["rbbb_lafb"] = M(c=MORPH["lafb"]["c"] + [(0.105, 0.017, (-0.75, 0.05, 0.7), 0.75)], d=0.13, T=(0.65, 0.3, -0.25), Ta=0.3)
MORPH["rbbb_lpfb"] = M(c=MORPH["lpfb"]["c"] + [(0.105, 0.017, (-0.75, 0.05, 0.7), 0.75)], d=0.13, T=(0.5, 0.6, -0.25), Ta=0.3)
MORPH["ivcd"] = M(c=[(a * 1.35, s * 1.4, v, amp) for a, s, v, amp in NORMAL["c"]], d=0.125, Ta=0.3)
MORPH["hcm"] = M(c=[(0.014, 0.008, (-0.85, -0.2, 0.35), 0.75)] + MORPH["lvh"]["c"][1:], d=0.10, T=(0.55, 0.5, 0.3))
MORPH["fasc"] = M(c=[(a * 0.9, s * 0.9, v, amp) for a, s, v, amp in MORPH["rbbb_lafb"]["c"]], d=0.12, T=(0.5, 0.4, -0.3), Ta=0.35)
MORPH["hyperk"] = M(c=[(0.035, 0.03, (0.45, 0.6, -0.35), 1.2), (0.115, 0.035, (0.65, 0.35, -0.55), 1.0)], d=0.19, T=(0.5, 0.6, 0.35), Ta=0.5)
MORPH["sine"] = M(c=[(0.07, 0.055, (0.5, 0.7, -0.3), 1.35)], d=0.2, T=(-0.5, -0.65, 0.3), Ta=0.9)
MORPH["wpw_ll"] = wpw((-0.6, 0.35, 0.7))       # via lateral esquerda: delta negativo em I/aVL, positivo em V1 (tipo A)
MORPH["wpw_ps"] = wpw((0.5, -0.75, 0.55))      # póstero-septal: delta negativo em III/aVF
MORPH["wpw_rf"] = wpw((0.85, 0.4, -0.35))      # parede livre direita: delta negativo em V1 (tipo B)
MORPH["wpw_ll_wide"] = M(c=[(0.0, 0.03, unit((-0.6, 0.35, 0.7)), 1.3), (0.07, 0.03, (-0.3, 0.5, 0.8), 0.6)], d=0.16, T=(0.5, -0.3, -0.6), Ta=0.4)

def morph(key, scale=1.0, width=1.0, rotdeg=0.0, rotax=(0, 0, 1)):
    m = MORPH[key] if isinstance(key, str) else key
    c = [(a * width, s * width, (rot(v, rotax, rotdeg) if rotdeg else v), amp * scale) for a, s, v, amp in m["c"]]
    return {**m, "c": c, "d": m["d"] * width}

# ---------------- ondas P
PM = {"s": [(0.0, 0.022, (0.5, 0.8, 0.2), 0.14)],
      "lae": [(-0.02, 0.018, (0.35, 0.85, 0.45), 0.11), (0.035, 0.02, (0.75, 0.35, -0.7), 0.15)],
      "rae": [(0.0, 0.019, (0.25, 0.95, 0.35), 0.30)],
      "bae": [(-0.02, 0.018, (0.25, 0.95, 0.45), 0.26), (0.04, 0.02, (0.75, 0.35, -0.7), 0.15)],
      "inv": [(0.0, 0.020, (0.3, -0.9, 0.2), 0.13)], "retro": [(0.0, 0.018, (0.1, -0.95, 0.1), 0.12)],
      "e1": [(0.0, 0.02, (0.9, 0.2, -0.3), 0.13)], "e2": [(0.0, 0.02, (-0.4, 0.8, 0.5), 0.15)], "e3": [(0.0, 0.024, (0.6, -0.4, 0.6), 0.12)],
      "e4": [(0.0, 0.018, (-0.2, 0.6, -0.7), 0.10)], "low": [(0.0, 0.022, (0.5, 0.8, 0.2), 0.05)], "peaked_flat": [(0.0, 0.03, (0.5, 0.8, 0.2), 0.04)]}

class ECG:
    def __init__(s, dur=10.0, seed=0):
        s.dur = dur; s.t = np.arange(int(dur * FS)) / FS; s.rng = np.random.default_rng(seed); random.seed(seed)
        s.D = np.zeros((3, len(s.t))); s.ov = {l: np.zeros(len(s.t)) for l in LV}; s.spk = []; s.beats = []; s.P = []
    def addv(s, comps, t0, scale=1.0):
        for a, sg, v, amp in comps:
            s.D += np.outer(np.array(v, float) * amp * scale, g(s.t, t0 + a, sg))
    def p(s, t0, kind="s", scale=1.0):
        s.P.append((t0, kind)); s.addv(PM[kind] if isinstance(kind, str) else kind, t0, scale)
    def beat(s, t0, m="N", qt=None, tscale=1.0, scale=1.0, tvec=None, u=0.0, width=1.0, rotdeg=0.0, rotax=(0, 0, 1), notT=False, tw=1.0, t_sig=None):
        mm = morph(m, scale, width, rotdeg, rotax)
        t_on = t0 - mm.get("pre", 0.0)
        s.addv(mm["c"], t_on)
        J = t_on + mm["d"]
        qt = qt or 0.40
        tp = t_on + qt - 0.09 * tw
        if not notT:
            tv = np.array(tvec if tvec is not None else (rot(mm["T"], rotax, rotdeg) if rotdeg else mm["T"]), float)
            s1, s2 = t_sig or (0.055 * tw, 0.038 * tw)
            s.D += np.outer(unit(tv) * mm["Ta"] * tscale, ga(s.t, tp, s1, s2))
            if u: s.D += np.outer(unit((0.5, 0.5, 0.5)) * u, g(s.t, tp + 0.13, 0.03))
        s.beats.append(dict(on=t_on, J=J, tp=tp, te=tp + 0.09 * tw, m=m))
        return J
    # ------------ overlays por derivação (alinhados a cada batimento)
    def st(s, per_lead, shape="flat", beats=None, mm_per=0.1):
        for b in (s.beats if beats is None else beats):
            J, tp, te = b["J"], b["tp"], b["te"]
            x = s.t
            if shape == "flat": w = sstep((x - J + 0.004) / 0.025) * (1 - sstep((x - tp) / (te - tp + 0.04)))
            elif shape == "concave": w = sstep((x - J) / 0.05) * (0.55 + 0.45 * np.clip((x - J) / (tp - J), 0, 1)) * (1 - sstep((x - tp) / (te - tp + 0.03)))
            elif shape == "downslope": w = np.clip((x - J) / (tp - J + 1e-3), 0, 1) ** 0.8 * (1 - sstep((x - tp - 0.02) / (te - tp + 0.05))) + 0.15 * sstep((x - J) / 0.02) * (x < te)
            elif shape == "upslope": w = sstep((x - J + 0.004) / 0.015) * (1 - np.clip((x - J) / (tp - J), 0, 1)) * (x < tp)
            elif shape == "coved": w = sstep((x - J + 0.006) / 0.012) * np.exp(-np.clip(x - J, 0, None) / 0.11) * (x < te + 0.04)
            elif shape == "saddle": w = sstep((x - J + 0.006) / 0.012) * (1 - 0.65 * g(x, J + 0.07, 0.035)) * (1 - sstep((x - tp) / (te - tp + 0.03)))
            elif shape == "scoop": w = np.sin(np.pi * np.clip((x - J) / (tp - J + 0.02), 0, 1)) ** 0.6
            elif shape == "pr": w = None
            for l, v in per_lead.items():
                s.ov[l] += v * mm_per * w
    def pr_seg(s, per_lead, mm_per=0.1):
        for t0, k in s.P:
            w = sstep((s.t - t0 - 0.045) / 0.02) * (1 - sstep((s.t - t0 - 0.14) / 0.03))
            for l, v in per_lead.items(): s.ov[l] += v * mm_per * w
    def tmod(s, per_lead, beats=None, shape="inv"):
        """multiplica/acrescenta T por derivação: inv (inverte com fator), biph (Wellens A), giant, peak"""
        for b in (s.beats if beats is None else beats):
            tp = b["tp"]
            for l, v in per_lead.items():
                if shape == "biph": s.ov[l] += 0.1 * (v * 0.6 * g(s.t, tp - 0.05, 0.028) - v * 1.6 * g(s.t, tp + 0.035, 0.045))
                elif shape == "deep": s.ov[l] += -0.1 * v * ga(s.t, tp, 0.06, 0.05)
                elif shape == "tall": s.ov[l] += 0.1 * v * ga(s.t, tp, 0.05, 0.035)
                elif shape == "peak": s.ov[l] += 0.1 * v * ga(s.t, tp - 0.03, 0.028, 0.022)
                elif shape == "u": s.ov[l] += 0.1 * v * g(s.t, tp + 0.13, 0.032)
                elif shape == "bifid": s.ov[l] += 0.1 * v * (g(s.t, tp + 0.085, 0.03) - 0.55 * g(s.t, tp + 0.03, 0.02))
                elif shape == "flat": s.ov[l] += -0.1 * v * ga(s.t, tp, 0.05, 0.04)
    def notch(s, per_lead, dt=0.012, sig=0.006, beats=None):  # épsilon / J (Osborn) / pseudo-r'
        for b in (s.beats if beats is None else beats):
            for l, v in per_lead.items(): s.ov[l] += 0.1 * v * g(s.t, b["J"] + dt, sig)
    def spike(s, t0, amp=1.2): s.spk.append((t0, amp))
    # ------------ atividade atrial contínua
    def flutter(s, rate=300, vec=(0.1, -0.9, 0.35), amp=0.17, t0=0.0, t1=None):
        f = rate / 60; ph = (s.t * f) % 1.0; saw = np.where(ph < 0.7, 1 - ph / 0.7 * 2, -1 + (ph - 0.7) / 0.3 * 2)
        w = ((s.t >= t0) & (s.t < (t1 or s.dur))).astype(float); s.D += np.outer(unit(vec) * amp, saw * w)
    def fib(s, amp=0.06, t0=0.0, t1=None):
        w = ((s.t >= t0) & (s.t < (t1 or s.dur))).astype(float); sig = np.zeros(len(s.t))
        for k in range(6):
            f = s.rng.uniform(5.5, 9); sig += s.rng.uniform(0.5, 1) * np.sin(2 * np.pi * f * s.t + s.rng.uniform(0, 6.28)) * (0.6 + 0.4 * np.sin(2 * np.pi * s.rng.uniform(0.2, 0.7) * s.t + s.rng.uniform(0, 6)))
        s.D += np.outer(unit((0.1, 0.4, 0.9)) * amp / 2.5, sig * w)
    def vf(s, amp=0.6, t0=0.0, t1=None):
        w = ((s.t >= t0) & (s.t < (t1 or s.dur))).astype(float)
        for k in range(5):
            f = s.rng.uniform(3.5, 6.5); v = unit(s.rng.normal(size=3)); env = 0.55 + 0.45 * np.sin(2 * np.pi * s.rng.uniform(0.15, 0.5) * s.t + s.rng.uniform(0, 6))
            s.D += np.outer(v * amp / 2.2, np.sin(2 * np.pi * f * s.t + s.rng.uniform(0, 6)) * env * w)
    def noise(s, base=0.012, wander=0.0, tremor=0.0, emg=0.0, hum=0.0, motion=None):
        n = len(s.t); s.nz = {}
        for l in LV:
            x = s.rng.normal(0, base, n)
            if wander: x += wander * np.sin(2 * np.pi * 0.25 * s.t + s.rng.uniform(0, 6)) + wander * 0.5 * np.sin(2 * np.pi * 0.11 * s.t + 1)
            if tremor: x += tremor * np.sin(2 * np.pi * 5.2 * s.t + s.rng.uniform(0, 6)) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.3 * s.t)) * (1.2 if l in ("I", "II", "III", "aVR", "aVL", "aVF") else 0.4)
            if emg: x += s.rng.normal(0, emg, n) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.5 * s.t + s.rng.uniform(0, 6)))
            if hum: x += hum * np.sin(2 * np.pi * 60 * s.t)
            if motion and l in motion.get("leads", LV):
                a, b = motion["t"]; m = ((s.t > a) & (s.t < b))
                x += m * motion.get("amp", 0.8) * np.sin(2 * np.pi * motion.get("f", 3.2) * s.t) * (1 if l != "aVR" else -1)
            s.nz[l] = x
    def leads(s, swap=None, dextro=False, extra=()):
        out = {}
        for l in list(LEADS) + list(extra):
            v = np.array(LV[l]);
            if dextro: v = v * np.array([-1, 1, 1]) if not l.startswith("V") else np.array(LV[{"V1": "V2", "V2": "V1"}.get(l, l)]) * np.array([-1, 1, 1])
            x = GAIN[l] * (v @ s.D) + s.ov[l] + (s.nz.get(l, 0) if hasattr(s, "nz") else 0)
            out[l] = x
        for t0, amp in s.spk:
            i = int(t0 * FS)
            if 0 <= i < len(s.t) - 2:
                for l in out: out[l][i] += amp * (0.7 if l.startswith("V") else 0.5) * (1 if l not in ("aVR",) else -1); out[l][i + 1] -= 0.15 * amp
        if swap == "LA-RA":
            I, II, III, aVR, aVL = out["I"], out["II"], out["III"], out["aVR"], out["aVL"]
            out["I"], out["II"], out["III"], out["aVR"], out["aVL"] = -I, III.copy(), II.copy(), aVL.copy(), aVR.copy()
        if swap == "LA-LL":
            I, II, III, aVL, aVF = out["I"], out["II"], out["III"], out["aVL"], out["aVF"]
            out["I"], out["II"], out["III"], out["aVL"], out["aVF"] = II.copy(), I.copy(), -III, aVF.copy(), aVL.copy()
        if swap == "V1-V3": out["V1"], out["V3"] = out["V3"], out["V1"]
        return out

# ---------------- motor de ritmo (gera P e batimentos)
def qt_for(rr, qtc=0.41): return max(0.24, min(0.62, qtc * math.sqrt(max(rr, 0.25))))

def run_sinus(e, rate=72, pr=0.16, m="N", pk="s", var=0.0, qtc=0.41, start=0.25, drops=(), **bk):
    t = start; rr = 60 / rate; i = 0
    while t < e.dur + 0.5:
        e.p(t, pk)
        if i not in drops: e.beat(t + pr, m, qt=qt_for(rr, qtc), **bk)
        t += rr * (1 + var * math.sin(i * 0.9)); i += 1
    return e

def build(spec, seed=0):
    """spec: dict(rhythm=..., params...). Devolve (leads dict, nome do layout)."""
    e = ECG(seed=seed); r = spec.get("r", "sinus"); rng = random.Random(seed)
    m = spec.get("m", "N"); pk = spec.get("pk", "s"); qtc = spec.get("qtc", 0.41); rate = spec.get("rate", 72); pr = spec.get("pr", 0.16)
    bk = {k: spec[k] for k in ("tscale", "u", "scale", "tw", "t_sig", "width") if k in spec}
    if spec.get("tvec") is not None: bk["tvec"] = spec["tvec"]
    if r == "sinus":
        run_sinus(e, rate, pr, m, pk, spec.get("var", 0), qtc, **bk)
    elif r == "alternans":
        t = 0.3; rr = 60 / rate; i = 0
        while t < e.dur + 0.5: e.p(t, pk); e.beat(t + pr, m, qt=qt_for(rr, qtc), scale=(1.0 if i % 2 else 0.55), **{k: v for k, v in bk.items() if k != "scale"}); t += rr; i += 1
    elif r == "pause":  # parada sinusal / bloqueio sinoatrial
        t = 0.3; rr = 60 / rate; i = 0
        while t < e.dur + 0.5:
            e.p(t, pk); e.beat(t + pr, m, qt=qt_for(rr, qtc), **bk); i += 1
            t += (spec.get("gap", 2 * rr) if i == spec.get("at", 4) else rr)
    elif r == "avb1": run_sinus(e, rate, spec.get("pr", 0.34), m, pk, 0, qtc, **bk)
    elif r == "wenck":
        n = spec.get("n", 4); t = 0.3; rr = 60 / rate; i = 0; prs = [0.18 + 0.11 * (1 - 0.55 ** k) / 0.45 for k in range(n - 1)]
        while t < e.dur + 0.5:
            k = i % n; e.p(t, pk)
            if k < n - 1: e.beat(t + prs[k], m, qt=qt_for(rr, qtc), **bk)
            t += rr; i += 1
    elif r == "mobitz2":
        n = spec.get("n", 4); t = 0.3; rr = 60 / rate; i = 0
        while t < e.dur + 0.5:
            e.p(t, pk)
            if i % n != n - 1: e.beat(t + spec.get("pr", 0.17), m, qt=qt_for(rr, qtc), **bk)
            t += rr; i += 1
    elif r == "avb2to1" or r == "avbhigh":
        n = 2 if r == "avb2to1" else spec.get("n", 3); t = 0.3; rr = 60 / rate; i = 0
        while t < e.dur + 0.5:
            e.p(t, pk)
            if i % n == 0: e.beat(t + pr, m, qt=qt_for(rr * n, qtc), **bk)
            t += rr; i += 1
    elif r == "chb":
        a = spec.get("arate", 85); v = spec.get("vrate", 38); em = spec.get("esc", "N")
        t = 0.15;
        while t < e.dur + 0.5: e.p(t, pk); t += 60 / a
        t = 0.55
        while t < e.dur + 0.5: e.beat(t, em, qt=qt_for(60 / v, qtc) if em == "N" else 0.48, **bk); t += 60 / v
    elif r == "junc":
        t = 0.4; rr = 60 / rate
        while t < e.dur + 0.5:
            e.beat(t, m, qt=qt_for(rr, qtc), **bk)
            if spec.get("retro"): e.p(t + 0.07, "retro")
            t += rr
    elif r == "af" or r == "afpre":
        mean = 60 / rate; t = 0.35; e.fib(spec.get("famp", 0.07))
        while t < e.dur + 0.5:
            mm = m if r == "af" else rng.choice(["wpw_ll", "wpw_ll_wide", "wpw_ll_wide"])
            nxt = max(0.23 if r == "afpre" else 0.32, rng.uniform(0.55, 1.45) * mean)
            if spec.get("ashman") and len(e.beats) >= 2 and (t - e.beats[-1]["on"]) < 0.62 * (e.beats[-1]["on"] - e.beats[-2]["on"]): mm = "rbbb"
            e.beat(t, mm, qt=qt_for(mean, qtc), **bk); t += nxt
    elif r == "afreg":
        e.fib(spec.get("famp", 0.06)); t = 0.5; rr = 60 / rate
        while t < e.dur + 0.5: e.beat(t, spec.get("esc", "N"), qt=qt_for(rr, qtc), **bk); t += rr
    elif r == "flutter":
        ar = spec.get("arate", 300); cond = spec.get("cond", 4); e.flutter(ar, spec.get("fvec", (0.1, -0.9, 0.35)), spec.get("famp", 0.24))
        fl = 60 / ar; t = 0.2; k = 0; seq = cond if isinstance(cond, (list, tuple)) else [cond]
        while t < e.dur + 0.5:
            c = seq[k % len(seq)]; e.beat(t + 0.22, m, qt=qt_for(c * fl, qtc), **bk); t += c * fl; k += 1
    elif r == "svt":  # AVNRT/AVRT/TA
        kind = spec.get("kind", "avnrt"); rr = 60 / rate; t = 0.3
        while t < e.dur + 0.5:
            e.beat(t, m, qt=qt_for(rr, qtc), **({**bk, "scale": 0.6} if spec.get("r_alt") and len(e.beats) % 2 else bk))
            if kind == "avnrt": e.notch({"V1": 0.9, "II": -0.4, "III": -0.5, "aVF": -0.45}, dt=0.005, sig=0.008, beats=e.beats[-1:])
            if kind == "avrt": e.p(t + 0.12, "retro")
            if kind == "at": e.p(t + rr - 0.13, spec.get("pk", "e1"))
            t += rr
    elif r == "mat":
        t = 0.3; ks = ["s", "e1", "e2", "e3", "e4"]
        while t < e.dur + 0.5:
            k = rng.choice(ks); prx = rng.uniform(0.11, 0.22); e.p(t, k); e.beat(t + prx, m, qt=qt_for(0.5, qtc), **bk); t += rng.uniform(0.38, 0.62)
    elif r == "wap":
        t = 0.3; ks = ["s", "e1", "e2", "e3", "inv"]; rr = 60 / rate
        while t < e.dur + 0.5:
            k = rng.choice(ks); e.p(t, k); e.beat(t + rng.uniform(0.12, 0.2), m, qt=qt_for(rr, qtc), **bk); t += rr * rng.uniform(0.9, 1.12)
    elif r == "ectopy":  # sinusal + extrassístoles programadas
        rr = 60 / rate; t = 0.3; i = 0; pat = spec.get("pat", {})  # i -> tipo
        every = spec.get("every"); kind = spec.get("kind", "pvc_rvot")
        while t < e.dur + 0.5:
            typ = pat.get(i) or (kind if every and i % every == every - 1 else None)
            if typ is None: e.p(t, pk); e.beat(t + pr, m, qt=qt_for(rr, qtc), **bk); t += rr
            elif typ in ("pac", "pac_ab", "pac_bl"):
                tc = t - rr * 0.35; e.p(tc, "e1")
                if typ != "pac_bl": e.beat(tc + 0.15, "rbbb" if typ == "pac_ab" else m, qt=qt_for(rr, qtc), **bk)
                t = tc + rr * 1.05
            elif typ == "pjc": tc = t - rr * 0.3; e.beat(tc, m, qt=qt_for(rr, qtc), **bk); e.p(tc + 0.06, "retro"); t = tc + rr * 1.1
            elif typ == "interp": e.p(t, pk); e.beat(t + pr, m, qt=qt_for(rr, qtc), **bk); e.beat(t + pr + rr * 0.55, "pvc_rvot", qt=0.36); t += rr * 1.0; e.p(t, pk); e.beat(t + pr + 0.06, m, qt=qt_for(rr, qtc), **bk); t += rr
            elif typ == "ront": e.beat(t - rr + pr + 0.30, "pvc_lv", qt=0.42); t += rr
            elif typ.startswith("pvc") or typ.startswith("run"):
                tc = t - rr * 0.38
                n = int(typ.split(":")[1]) if ":" in typ else 1; morph_ = spec.get("vmorph", "pvc_rvot") if typ.startswith("run") else typ
                for j in range(n): e.beat(tc + j * spec.get("vrr", 0.36) + pr, morph_ if not spec.get("multi") else rng.choice(["pvc_rvot", "pvc_lv", "pvc_lvinf"]), qt=0.42)
                e.p(t, pk)  # P sinusal escondida/dissociada
                t = t + rr * (1 if n == 1 else n * 0.6)
            elif typ == "fusion": e.p(t, pk); e.beat(t + pr - 0.03, "pvc_rvot", scale=0.45, qt=qt_for(rr, qtc)); e.beat(t + pr, m, scale=0.55, qt=qt_for(rr, qtc), notT=True); t += rr
            i += 1
    elif r == "vt":
        rr = 60 / rate; t = 0.25; vm = spec.get("vm", "vt_lbbb"); i = 0
        while t < e.dur + 0.5:
            if spec.get("bidir"): e.beat(t, "pvc_lv" if i % 2 else "pvc_lvinf", qt=0.34)
            elif i in spec.get("cap", ()): e.beat(t - 0.06, "N", qt=0.3)
            elif i in spec.get("fus", ()): e.beat(t - 0.02, "N", qt=0.3, scale=0.55, notT=True); e.beat(t, vm, scale=0.5, qt=0.3 + 0.1 * rr)
            else: e.beat(t, vm, qt=0.3 + 0.1 * rr, **{k: v for k, v in bk.items() if k != "scale"})
            t += rr; i += 1
        if spec.get("dissoc", True) and not spec.get("bidir"):
            tp = 0.1
            while tp < e.dur: e.p(tp, "s"); tp += 60 / spec.get("arate", 80)
    elif r == "slowvent":  # RIVA / idioventricular / escape
        rr = 60 / rate; t = 0.3
        while t < e.dur + 0.5: e.beat(t, spec.get("vm", "pvc_lv"), qt=0.46); t += rr
        if spec.get("sinus"):
            tp = 0.15
            while tp < e.dur: e.p(tp, "s"); tp += 60 / spec["sinus"]
    elif r == "tdp":
        rr = 60 / rate; t = 2.6; k = 0
        for j, tt in enumerate((0.3, 1.45)): e.p(tt, "s"); e.beat(tt + 0.16, m, qt=0.62, tscale=1.2, u=0.08)
        e.beat(2.25, "pvc_lv", qt=0.4)
        while t < e.dur + 0.5:
            env = 0.45 + 0.75 * abs(math.sin(k * 0.42)); e.beat(t, "vt_lbbb", width=1.05, scale=env, rotdeg=k * 22, rotax=(0.2, 0.3, 1), qt=0.27, tscale=0.6); t += rr; k += 1
    elif r == "vf": e.vf(spec.get("amp", 0.65))
    elif r == "asystole":
        if spec.get("pwaves"):
            t = 0.3
            while t < e.dur: e.p(t, "s"); t += 60 / spec["pwaves"]
    elif r == "paced":
        mode = spec.get("mode", "VVI"); rr = 60 / rate; t = 0.35; i = 0
        while t < e.dur + 0.5:
            fail = i in spec.get("fail", ()); unders = spec.get("under")
            if i in spec.get("over", ()): t += rr; i += 1; continue
            if mode in ("AAI", "DDD"): e.spike(t, 0.9); e.p(t + 0.01, "s")
            if mode == "AAI": e.beat(t + 0.18, "N", qt=qt_for(rr, qtc))
            if mode == "DDD": e.spike(t + 0.16, 1.3); e.beat(t + 0.165, spec.get("pm", "paced"), qt=0.42, **bk)
            if mode == "VVI":
                e.spike(t, 1.3)
                if not fail: e.beat(t + 0.005, spec.get("pm", "paced"), qt=0.42, **bk)
            t += rr; i += 1
        if spec.get("sinus"):  # ritmo próprio (para falha de sensibilidade)
            tp = 0.6
            while tp < e.dur: e.p(tp, "s"); e.beat(tp + 0.16, "N", qt=0.38); tp += 60 / spec["sinus"]
    elif r == "cycle":  # sinusal alternando morfologias (bloqueio alternante, pré-excitação intermitente)
        rr = 60 / rate; t = 0.3; i = 0; cyc = spec["mc"]; prs = spec.get("prs")
        while t < e.dur + 0.5:
            mm = cyc[i % len(cyc)]; e.p(t, pk); e.beat(t + (prs[i % len(prs)] if prs else pr), mm, qt=qt_for(rr, qtc), **bk); t += rr; i += 1
    elif r == "ratedep":  # bloqueio de ramo dependente da frequência
        t = 0.3; i = 0
        while t < e.dur + 0.5:
            fast = t > e.dur * 0.45; rr = 60 / (spec.get("r2", 105) if fast else rate)
            e.p(t, pk); e.beat(t + pr, spec.get("m2", "lbbb") if fast else m, qt=qt_for(rr, qtc), **bk); t += rr; i += 1
    elif r == "tachybrady":
        e.fib(0.07, 0, 4.4); t = 0.3
        while t < 4.2: e.beat(t, "N", qt=0.3); t += rng.uniform(0.33, 0.5)
        t = 4.2 + spec.get("gap", 3.1)
        while t < e.dur + 0.5: e.p(t, pk); e.beat(t + pr, "N", qt=0.44); t += 60 / spec.get("brate", 42)
    elif r == "svt_term":
        t = 0.3; rr = 60 / rate
        while t < 4.6: e.beat(t, m, qt=0.27); t += rr
        t += spec.get("gap", 1.6)
        while t < e.dur + 0.5: e.p(t, pk); e.beat(t + pr, m, qt=0.4); t += 60 / 75
    elif r == "pvt":  # TV polimórfica com QT normal (isquemia)
        t = 0.3
        for j in range(3): e.p(t, "s"); e.beat(t + 0.16, "N", qt=0.38); t += 0.8
        k = 0
        while t < e.dur + 0.5:
            e.beat(t, rng.choice(["vt_lbbb", "pvc_lv", "vt_nw", "pvc_lvinf", "pvc_rvot"]), qt=0.28, scale=rng.uniform(0.6, 1.2), tscale=0.6); t += rng.uniform(0.21, 0.3); k += 1
    # sobreposições
    for ov in spec.get("ov", []):
        kind = ov[0]
        if kind == "st": e.st(ov[1], ov[2] if len(ov) > 2 else "flat")
        elif kind == "pr": e.pr_seg(ov[1])
        elif kind == "t": e.tmod(ov[1], shape=ov[2] if len(ov) > 2 else "deep")
        elif kind == "notch": e.notch(ov[1], *(ov[2:] if len(ov) > 2 else ()))
    e.noise(**spec.get("noise", {}))
    L = e.leads(swap=spec.get("swap"), dextro=spec.get("dextro", False), extra=("V4R",) if spec.get("v4r") else ())
    if spec.get("v4r"):
        L["V4R"] = L["V4R"] + spec.get("v4r") * 0.1 * np.concatenate([np.zeros(1), np.ones(len(e.t) - 1)]) * sum((sstep((e.t - b["J"]) / 0.02) * (1 - sstep((e.t - b["tp"]) / 0.12))) for b in e.beats)
    return L, spec.get("lay", "12")

# ---------------- desenho no papel milimetrado
PXMM = 7; SS = 2
COL_MIN, COL_MAJ, COL_BG, COL_TR = (245, 196, 196), (228, 140, 140), (255, 249, 248), (20, 20, 24)
def font(sz, bold=False):
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf" % ("-Bold" if bold else ""), sz)

def render(L, lay="12", title="", path=None):
    k = PXMM * SS
    if lay == "12": rows = [["I", "aVR", "V1", "V4"], ["II", "aVL", "V2", "V5"], ["III", "aVF", "V3", "V6"], ["II*"]]; rowh = 30
    elif lay == "12r": rows = [["I", "aVR", "V1", "V4"], ["II", "aVL", "V2", "V5"], ["III", "aVF", "V3", "V6"], ["V4R*"]]; rowh = 30
    elif lay == "r1": rows = [["II*"]]; rowh = 36
    elif lay == "r2": rows = [["V1*"], ["II*"]]; rowh = 32
    elif lay == "r3": rows = [["I*"], ["II*"], ["V1*"]]; rowh = 30
    else: raise ValueError(lay)
    Wmm = 10 + 250 + 6; Hmm = 12 + rowh * len(rows) + 4
    W, H = int(Wmm * k), int(Hmm * k)
    im = Image.new("RGB", (W, H), COL_BG); d = ImageDraw.Draw(im)
    for xm in range(int(Wmm) + 1):
        d.line([(xm * k, 0), (xm * k, H)], fill=COL_MAJ if xm % 5 == 0 else COL_MIN, width=(3 if xm % 5 == 0 else 1))
    for ym in range(int(Hmm) + 1):
        d.line([(0, ym * k), (W, ym * k)], fill=COL_MAJ if ym % 5 == 0 else COL_MIN, width=(3 if ym % 5 == 0 else 1))
    fb = font(int(3.4 * k / 1.0 / 1.0)); fs = font(int(2.6 * k))
    d.rectangle([0, 0, W, int(7.2 * k)], fill=(255, 252, 250))
    d.text((int(3 * k), int(1.4 * k)), title, font=font(int(3.4 * k), True), fill=(110, 30, 30))
    d.text((W - int(118 * k), int(1.9 * k)), "25 mm/s · 10 mm/mV · traçado sintético didático · CÓDICE 360X", font=fs, fill=(140, 90, 90))
    x0 = 10
    for ri, row in enumerate(rows):
        yb = 12 + rowh * ri + rowh / 2 + 2
        # pulso de calibração 1 mV
        cx = [(3, 0), (4, 0), (4, 10), (9, 10), (9, 0), (10, 0)]
        d.line([((2 + a) * k * 0.9, (yb - b) * k) for a, b in cx], fill=COL_TR, width=int(0.28 * k))
        ncol = len(row); seg = 250 / ncol
        for ci, name in enumerate(row):
            full = name.endswith("*"); ld = name.rstrip("*")
            sig = L[ld]; n = len(sig)
            i0 = 0 if full else int(ci * 2.5 * FS); i1 = n if full else int((ci + 1) * 2.5 * FS)
            xs = x0 + (0 if full else ci * seg) + np.arange(i1 - i0) / FS * 25.0
            ys = yb - np.clip(sig[i0:i1], -(rowh / 20 + 0.35), rowh / 20 + 0.35) * 10.0
            pts = list(zip((xs * k).tolist(), (ys * k).tolist()))
            d.line(pts, fill=COL_TR, width=int(0.30 * k), joint="curve")
            d.text(((x0 + (0 if full else ci * seg) + 1.2) * k, (yb - rowh / 2 + 1.8) * k), ld, font=fb, fill=(25, 25, 60))
            if not full and ci > 0:
                xx = (x0 + ci * seg) * k; d.line([(xx, (yb - 3) * k), (xx, (yb + 3) * k)], fill=COL_TR, width=int(0.3 * k))
    im = im.resize((W // SS, H // SS), Image.LANCZOS)
    im = im.quantize(colors=48, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    if path: im.save(path, optimize=True)
    return im
