"""🖥️ Monitor multiparamétrico, cateter de artéria pulmonar, PIC e EEG sintéticos (questões ilustradas 4.24.0)."""
import os, sys, math
import numpy as np
from figs_core import mfig, save_fig
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "ecg"))

COL = {"ecg": "#36e27a", "art": "#ff4d4d", "pleth": "#48d8ff", "co2": "#f5d33d", "cvp": "#7fa8ff", "pap": "#ffb347", "icp": "#e98bff", "flush": "#ff4d4d", "resp": "#f0f0f0"}
LAB = {"ecg": "II", "art": "ART", "pleth": "Pleth", "co2": "CO₂", "cvp": "PVC", "pap": "AP", "icp": "PIC", "flush": "ART · teste de flush", "resp": "Resp"}
FS = 250


def _ecg_signal(ch, dur, seed):
    """Derivação II do motor de ECG do Compêndio (por número do card ou spec)."""
    import ecg_gen
    if "n" in ch:
        from build_ecg import cards_flat
        sp = dict(next(c for c in cards_flat() if c["n"] == ch["n"])["sp"])
    else: sp = dict(ch.get("sp", {}))
    sp.update(ch.get("over", {}))
    L, _ = ecg_gen.build(sp, seed=seed)
    s = np.asarray(L["II"], float); n = len(s); fs0 = ecg_gen.FS
    t0 = np.arange(n) / fs0; t = np.arange(int(dur * FS)) / FS
    return np.interp(t % (n / fs0), t0, s)


def _beats_from_ecg(sig, hr_hint=None):
    from scipy.signal import find_peaks
    d = np.abs(np.gradient(sig)); pk, _ = find_peaks(d, distance=int(0.24 * FS), prominence=np.percentile(d, 99) * 0.45)
    out = []
    for p in pk:
        if not out or p - out[-1] > int(0.24 * FS): out.append(p)
    return np.array(out) / FS


def _art(t, beats, sbp=120, dbp=70, ppv=0, rr=15, damp="ok", alt=False, parad=0, notch=True):
    y = np.full_like(t, float(dbp))
    for i, b in enumerate(beats):
        rrint = (beats[i + 1] - b) if i + 1 < len(beats) else 0.8
        ph = math.sin(2 * math.pi * b * rr / 60)
        pp = (sbp - dbp) * (1 + (ppv / 200) * ph) * (0.78 if alt and i % 2 else 1.0) - (parad * (0.5 - 0.5 * ph) if parad else 0)
        if damp == "over": pp *= 0.55
        tt = t - b - 0.06; m = (tt >= 0) & (tt < rrint); u = tt[m]; T = max(rrint - 0.06, 0.25)
        tr = 0.10 if damp != "over" else 0.2
        up = np.where(u < tr, np.sin(np.pi / 2 * np.clip(u / tr, 0, 1)), 1.0)
        f = up * (0.5 * np.exp(-np.clip(u - tr, 0, None) / 0.10) + 0.5) * np.clip(1 - u / T, 0, 1) ** 1.2
        f = f / max(f.max(), 1e-6) if len(f) else f
        if notch and damp == "ok": f = f - 0.07 * np.exp(-0.5 * ((u - 0.30) / 0.016) ** 2) + 0.04 * np.exp(-0.5 * ((u - 0.34) / 0.025) ** 2)
        if damp == "under": f = f + 0.30 * np.exp(-u / 0.08) * np.sin(2 * np.pi * u / 0.07) * (u > 0.05)
        y[m] = dbp + pp * f
    return y


def _pleth(t, beats, amp=1.0, var=0):
    y = np.zeros_like(t)
    for b in beats:
        tt = t - b - 0.22; m = (tt >= -0.05) & (tt < 1.2); u = tt[m]
        y[m] += amp * (1 + var / 100 * math.sin(2 * math.pi * b * 15 / 60)) * (np.exp(-0.5 * ((u - 0.13) / 0.07) ** 2) + 0.35 * np.exp(-0.5 * ((u - 0.38) / 0.09) ** 2))
    return y


def _co2(t, ch):
    tp = ch.get("tipo", "normal"); rr = ch.get("rr", 14); et = ch.get("et", 38); y = np.zeros_like(t); per = 60 / rr
    for k in range(int(t[-1] / per) + 2):
        b = k * per; ti = per * 0.38; m = (t >= b) & (t < b + per); u = t[m] - b
        if tp in ("eso", "flat"): v = (et * np.exp(-k * 1.2)) * np.clip((u - ti) / 0.2, 0, 1) * np.clip((per - u) / 0.25, 0, 1) if tp == "eso" else u * 0
        else:
            e = et
            if tp == "drop" and b > t[-1] * 0.5: e = 0
            if tp == "rosc": e = 14 if b < t[-1] * 0.5 else et
            if tp == "fall": e = et * (1 - 0.65 * min(1, b / t[-1]))
            up = np.clip((u - ti) / (0.09 if tp not in ("obst",) else 0.55), 0, 1)
            if tp == "obst": up = np.clip((u - ti) / (per - ti - 0.15), 0, 1) ** 0.45
            plateau = e * (0.92 + 0.08 * np.clip((u - ti) / (per - ti), 0, 1))
            down = np.clip((per - u) / 0.12, 0, 1)
            v = plateau * up * down
            if tp == "cleft": v = v - e * 0.28 * np.exp(-0.5 * ((u - (ti + (per - ti) * 0.55)) / 0.07) ** 2) * (u > ti)
            if tp == "rebreath": v = np.maximum(v, ch.get("base", 8))
        y[m] = v
    if tp == "cpr": y = ch.get("et", 12) * (0.5 + 0.5 * np.clip(np.sin(2 * np.pi * t * 110 / 60), 0, 1)) * (0.6 + 0.4 * np.sin(2 * np.pi * t * 10 / 60) ** 2)
    if tp == "rebreath" and False: pass
    return y


def _cvp(t, beats, tipo="normal", m_=8):
    y = np.full_like(t, float(m_))
    for i, b in enumerate(beats):
        g = lambda c, s, a: a * np.exp(-0.5 * ((t - b - c) / s) ** 2)
        if tipo == "normal": y += g(-0.04, 0.05, 3) + g(0.08, 0.03, 1.2) - g(0.18, 0.06, 2.5) + g(0.42, 0.06, 2.6) - g(0.58, 0.07, 2.2)
        elif tipo == "cannon": y += (g(0.18, 0.05, 11) if i % 3 == 1 else g(-0.04, 0.05, 2.5)) + g(0.42, 0.06, 2.2) - g(0.58, 0.07, 2)
        elif tipo == "tr": y += g(-0.04, 0.05, 2) + g(0.28, 0.12, 10) - g(0.58, 0.07, 3.5)
        elif tipo == "tamp": y += g(-0.04, 0.05, 2.6) - g(0.2, 0.06, 3.4) + g(0.42, 0.06, 2)
        elif tipo == "fa": y += g(0.42, 0.07, 2.8) - g(0.6, 0.07, 2.2)
    return y


def _icp(t, beats, mean=12, tipo="normal", amp=6, trend=None):
    y = np.full_like(t, float(mean) - amp * .3)
    for b in beats:
        g = lambda c, s, a: a * np.exp(-0.5 * ((t - b - c) / s) ** 2)
        if tipo == "normal": y += g(0.09, 0.03, amp) + g(0.2, 0.05, amp * .7) + g(0.36, 0.05, amp * .45)
        else: y += g(0.09, 0.03, amp * .6) + g(0.22, 0.07, amp * 1.15) + g(0.38, 0.05, amp * .5)
    return y


def monitor(sp, path, title):
    """sp: ch=[{t: ecg|art|pleth|co2|cvp|pap|icp|flush|resp, ...}], num=[(rótulo, valor, cor-chave, unidade)], dur, hr (sem ecg), irr, sub"""
    dur = sp.get("dur", 6.0); t = np.arange(int(dur * FS)) / FS; seed = sp.get("seed", 3); chs = sp["ch"]
    ecg = None; beats = None
    for ch in chs:
        if ch["t"] == "ecg": ecg = _ecg_signal(ch, dur, seed); beats = _beats_from_ecg(ecg)
    if beats is None or sp.get("hr"):
        hr = sp.get("hr", 80); rng = np.random.default_rng(seed); b = 0.2; beats = []
        while b < dur: beats.append(b); b += 60 / hr * (1 + (rng.uniform(-.25, .25) if sp.get("irr") else 0))
        beats = np.array(beats)
    if sp.get("pulseless"): beats = np.array([])
    n = len(chs); fig = mfig(1.0 + 1.25 * n, w=11.0, title=title, dark=True)
    for i, ch in enumerate(chs):
        h = 0.84 / n; ax = fig.add_axes((0.035, 0.9 - (i + 1) * h + 0.012, 0.68, h - 0.02)); ax.set_facecolor("#0b0f14"); ax.grid(False)
        for s in ax.spines.values(): s.set_visible(False)
        k = ch["t"]; c = COL[k]
        if k == "ecg": y = ecg
        elif k == "art": y = _art(t, beats, ch.get("s", 120), ch.get("d", 70), ch.get("ppv", 0), ch.get("rr", 15), ch.get("damp", "ok"), ch.get("alt", False), ch.get("parad", 0))
        elif k == "pleth": y = _pleth(t, beats, var=ch.get("var", 0))
        elif k == "co2": y = _co2(t, ch)
        elif k == "cvp": y = _cvp(t, beats, ch.get("tipo", "normal"), ch.get("m", 8))
        elif k == "icp": y = _icp(t, beats, ch.get("m", 12), ch.get("tipo", "normal"), ch.get("amp", 6))
        elif k == "resp": y = np.sin(2 * np.pi * t * ch.get("rr", 16) / 60) * (1 if not ch.get("apnea") else np.where(t < dur / 2, 1, 0.03))
        elif k == "flush": y = _flush(t, ch.get("tipo", "ok"))
        elif k == "pap": y = _pap(t, beats, ch)
        if ch.get("flat"): y = y * 0 + (ch.get("flat_v", 0)) + np.random.default_rng(1).normal(0, 0.01, len(t))
        ax.plot(t, y, color=c, lw=1.6); ax.set_xlim(0, dur)
        lo, hi = ch.get("ylim", (None, None))
        if lo is not None: ax.set_ylim(lo, hi)
        ax.set_xticks([])
        if k in ("art", "co2", "cvp", "icp", "pap", "flush"): ax.tick_params(axis="y", colors="#7c8594", labelsize=8)
        else: ax.set_yticks([])
        ax.text(0.003, 0.97, ch.get("lab", LAB[k]), transform=ax.transAxes, va="top", color=c, fontsize=11, fontweight="bold")
        for x0, txt in ch.get("marks", []): ax.annotate(txt, (x0, ax.get_ylim()[1]), xytext=(0, -18), textcoords="offset points", ha="center", va="top", color="#e8c66a", fontsize=9.5, fontweight="bold")
    # painel numérico
    nums = sp.get("num", []); x0 = 0.74
    for j, (lab, val, key, un) in enumerate(nums):
        y0 = 0.86 - j * (0.82 / max(len(nums), 1))
        fig.text(x0, y0, lab, color=COL.get(key, "#ddd"), fontsize=11, fontweight="bold", va="top")
        fig.text(0.985, y0 - 0.005, str(val), color=COL.get(key, "#ddd"), fontsize=26 if len(str(val)) < 9 else 20, fontweight="bold", ha="right", va="top")
        fig.text(x0, y0 - 0.045, un, color="#7c8594", fontsize=9, va="top")
    if sp.get("sub"): fig.text(0.035, 0.02, sp["sub"], color="#c8ccd4", fontsize=10.5)
    save_fig(fig, path, colors=64)


def _flush(t, tipo):
    y = np.zeros_like(t); b0 = 1.0; sbp, dbp = 120, 70
    beats = np.arange(0.2, t[-1], 0.75)
    base = _art(t, beats, sbp, dbp, damp="ok")
    m = (t > b0) & (t < b0 + 0.45); y = base.copy(); y[m] = 300
    tt = t - (b0 + 0.45); after = tt >= 0
    if tipo == "ok": ring = -120 * np.exp(-tt / 0.03) * np.cos(2 * np.pi * tt / 0.06)
    elif tipo == "over": ring = 230 * np.exp(-tt / 0.22) - 0
    else: ring = -150 * np.exp(-tt / 0.18) * np.cos(2 * np.pi * tt / 0.06)
    w = after & (tt < 0.9)
    if tipo == "over": y[w] = np.maximum(base[w], dbp + ring[w] * 0.5)
    else: y[w] = base[w] + ring[w]
    return y


def _pap(t, beats, ch):
    """Inserção do cateter de Swan-Ganz: segmentos AD → VD → AP → POAP ao longo do tempo (ch['seq'] = [(até_s, região)])."""
    y = np.zeros_like(t); seq = ch.get("seq", [(1.5, "ra"), (3.2, "rv"), (4.8, "pa"), (99, "wedge")]); vgiant = ch.get("v", False)
    for i, b in enumerate(beats):
        reg = next(r for until, r in seq if b < until)
        g = lambda c, s, a: a * np.exp(-0.5 * ((t - b - c) / s) ** 2)
        m = (t >= b) & (t < (beats[i + 1] if i + 1 < len(beats) else t[-1] + 1))
        if reg == "ra": seg = 5 + g(-0.04, 0.05, 3) + g(0.42, 0.06, 3) - g(0.2, 0.06, 2)
        elif reg == "rv": seg = 4 + 21 * np.clip(np.sin(np.pi * np.clip((t - b - 0.06) / 0.32, 0, 1)), 0, 1) ** .6 + 2 * np.clip((t - b - 0.5) / 0.3, 0, 1)
        elif reg == "pa": seg = 12 + 14 * np.clip(np.sin(np.pi * np.clip((t - b - 0.08) / 0.34, 0, 1)), 0, 1) ** .7 * np.exp(-np.clip(t - b - 0.25, 0, None) / 0.8) + 3 * np.exp(-np.clip(t - b - 0.42, 0, None) / 0.4) * (t - b > 0.42)
        else: seg = ch.get("w", 12) + g(0.05, 0.06, 3) + (g(0.5, 0.09, 18) if vgiant else g(0.5, 0.07, 3)) - g(0.3, 0.06, 2)
        y[m] = seg[m]
    return y


def eeg(sp, path, title):
    """sp: tipo: normal|burst|iso|gpd|nc|tri|delta ; sub"""
    tp = sp["tipo"]; dur = sp.get("dur", 10); t = np.arange(int(dur * FS)) / FS; rng = np.random.default_rng(sp.get("seed", 5))
    chans = ["Fp1-F7", "F7-T3", "T3-T5", "T5-O1", "Fp2-F8", "F8-T4", "T4-T6", "T6-O2", "Fz-Cz", "Cz-Pz"]
    fig = mfig(6.4, w=11, title=title); ax = fig.add_axes((0.1, 0.1, 0.88, 0.78)); ax.set_facecolor("#ffffff")
    for i, ch in enumerate(chans):
        noise = np.convolve(rng.normal(0, 1, len(t)), np.ones(8) / 8, mode="same")
        if tp == "normal": y = 0.6 * noise + (1.4 if "O" in ch or "T5" in ch or "T6" in ch else 0.5) * np.sin(2 * np.pi * 10 * t + rng.uniform(0, 6)) * (0.7 + 0.3 * np.sin(2 * np.pi * 0.3 * t))
        elif tp == "iso": y = 0.05 * noise
        elif tp == "burst":
            env = np.zeros_like(t)
            for b0 in np.arange(0.5, dur, 3.2): env += ((t > b0) & (t < b0 + 0.9)).astype(float)
            y = env * (2.6 * noise + 1.5 * np.sin(2 * np.pi * 6 * t)) + 0.05 * noise
        elif tp == "gpd":
            y = 0.4 * noise
            for p in np.arange(0.3, dur, 1.0): y += 3.2 * np.exp(-0.5 * ((t - p) / 0.04) ** 2) - 1.2 * np.exp(-0.5 * ((t - p - 0.12) / 0.06) ** 2)
        elif tp == "nc":
            y = 0.3 * noise
            for p in np.arange(0.2, dur, 1 / 3): y += 3.0 * np.exp(-0.5 * ((t - p) / 0.02) ** 2) + 1.6 * np.sin(2 * np.pi * 3 * (t - p)) * ((t > p) & (t < p + 0.3))
        elif tp == "tri":
            y = 0.5 * noise
            for p in np.arange(0.4, dur, 0.55): y += -0.8 * np.exp(-0.5 * ((t - p) / 0.03) ** 2) + 2.4 * np.exp(-0.5 * ((t - p - 0.08) / 0.04) ** 2) - 1.0 * np.exp(-0.5 * ((t - p - 0.22) / 0.06) ** 2)
        elif tp == "delta": y = 0.5 * noise + 2.0 * np.sin(2 * np.pi * 1.5 * t + rng.uniform(0, 6)) + 0.8 * np.sin(2 * np.pi * 2.3 * t)
        ax.plot(t, y * 0.32 - i * 2.0, color="#1d2433", lw=0.9)
        ax.text(-0.1, -i * 2.0, ch, ha="right", va="center", fontsize=9.5, color="#1d2433")
    ax.set_xlim(0, dur); ax.set_ylim(-len(chans) * 2.0, 1.6); ax.set_yticks([]); ax.set_xticks(range(0, int(dur) + 1)); ax.grid(axis="x", alpha=.35)
    ax.set_xlabel("segundos (montagem bipolar longitudinal)")
    if sp.get("sub"): ax.set_title(sp["sub"], loc="left", fontsize=11.5)
    save_fig(fig, path, colors=48)
