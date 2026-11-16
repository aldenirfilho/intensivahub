"""Gerador sintético de curvas de ventilação mecânica (didático) — CÓDICE 360X.

Modelo monocompartimental: Paw + Pmus = R·F + Pel(V), Pel(V) = E·V·(1 + nl·V) (nl>0 hiperdistensão, nl<0 recrutamento).
Modos: VCV (quadrada/descendente, pausa), PCV, PRVC, PSV, CPAP, SIMV (VCV + PS), APRV.
Esforço do paciente (Pmus) programável: regular, explícito, reverso (atrelado ao ciclo), expiração ativa, soluço.
Eventos: pausa inspiratória/expiratória, oclusão P0.1, desconexão, mudança de R/C, vazamento, secreção, oscilação cardíaca.
Saída: tela de ventilador (Paw, Fluxo, Volume [, Pes]) ou loops P-V e F-V, com painel numérico opcional.
"""
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont

DT = 0.005
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"; FONTB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
COL = dict(bg=(9, 13, 19), grid=(32, 42, 54), axis=(70, 84, 100), txt=(205, 214, 224), dim=(120, 134, 150),
           P=(255, 210, 63), F=(61, 220, 132), V=(77, 212, 255), Pes=(255, 140, 66), alarm=(255, 86, 86))


def effort(t, t0, A, tr=0.5, tf=0.4):
    tau = t - t0
    if tau < 0 or tau > tr + tf: return 0.0
    if tau < tr: return A * (1 - math.cos(math.pi * tau / tr)) / 2
    return A * (1 + math.cos(math.pi * (tau - tr) / tf)) / 2


def simulate(sp, seed=0):
    rng = random.Random(seed)
    mode = sp.get("mode", "VCV"); R = sp.get("R", 10.0); Re = sp.get("Re", R + 5); C = sp.get("C", 50.0) / 1000.0
    nl = sp.get("nl", 0.0); PEEP = sp.get("peep", 5.0); RR = sp.get("rr", 16); Vt = sp.get("vt", 450) / 1000.0
    Ti = sp.get("ti", 0.9); pause = sp.get("pause", 0.0); flowpat = sp.get("flow", "square")
    Pinsp = sp.get("pinsp", 15.0); PS = sp.get("ps", 10.0); rise = sp.get("rise", 0.08); ets = sp.get("ets", 0.25)
    trig = sp.get("trig", 0.04); dur = sp.get("dur", 12.0); warm = sp.get("warm", 12.0); T = dur + warm
    vf = sp.get("vflow")  # fluxo VCV fixo (L/s) opcional
    # esforços
    eff = []
    pe = sp.get("eff")  # dict(rate, amp, tr, tf, jitter, t0) ou lista de (t, A, tr, tf)
    if isinstance(pe, dict):
        t = pe.get("t0", 0.7); per = 60.0 / pe.get("rate", 18)
        while t < T + 2:
            if not pe.get("skip") or rng.random() > pe["skip"]:
                a_ = pe.get("amp", 4) * (rng.uniform(0.85, 1.15) if pe.get("var", True) else 1.0)
                if pe.get("weakfrac") and rng.random() < pe["weakfrac"]: a_ *= 0.3
                eff.append((t, a_, pe.get("tr", 0.5), pe.get("tf", 0.4)))
            t += per * rng.uniform(1 - pe.get("jitter", 0.06), 1 + pe.get("jitter", 0.06))
    elif isinstance(pe, list):
        eff = [(a + warm, b, c, d) for a, b, c, d in pe]
    hic = sp.get("hiccup")  # (period, amp)
    if hic:
        t = 0.9
        while t < T: eff.append((t, hic[1], 0.06, 0.12)); t += hic[0]
    actexp = sp.get("actexp", 0.0)  # expiração ativa (cmH2O, negativo no Pmus) após cada ciclo
    rev = sp.get("reverse")  # (atraso s, amp, tr, tf, fração dos ciclos)
    def stepval(key, t, base):
        ev = sp.get(key)
        if ev and t >= ev[0] + warm: return ev[1]
        return base
    leak = sp.get("leak", 0.0)  # L/s por sqrt(cmH2O)
    n = int(T / DT); out = {k: np.zeros(n) for k in ("t", "P", "F", "V", "Pes", "Fd")}
    V = PEEP * C; phase = "exp"; tb = -10.0; tlast_machine = -10.0; ph_t0 = 0.0; Fpk = 0.0; Vbreath0 = V; Vd = 0.0
    breaths = []; cur = None; k = 0; pr_target = Pinsp; prvc_p = sp.get("prvc_p0", 8.0)
    holds_i = [x + warm for x in sp.get("hold_insp", ())]; holds_e = [x + warm for x in sp.get("hold_exp", ())]
    hold_len = sp.get("hold_len", 2.5); simv_mand = True; nb = 0; hold_until = -1; hold_kind = None
    disc = sp.get("disconnect"); aprv = sp.get("aprv")  # (Phigh, Plow, Thigh, Tlow)
    occl = sorted(sp.get("occl", ()))
    rev_eff = []
    for i in range(n):
        t = i * DT
        Rr = stepval("stepR", t, R); Cc = stepval("stepC", t, C * 1000) / 1000.0; Ree = stepval("stepR", t, Re)
        Pm = sum(effort(t, *e) for e in eff if -1 < t - e[0] < 3) + sum(effort(t, *e) for e in rev_eff if -1 < t - e[0] < 3)
        if actexp and not sp.get("nti") and phase == "exp" and 0.05 < t - ph_t0 < 0.9: Pm -= actexp * math.sin(math.pi * min(1, (t - ph_t0) / 0.9))
        Pel = V / Cc * (1 + nl * V)
        machine_due = (t - tlast_machine) >= 60.0 / RR
        dis = disc and t >= disc + warm
        if dis:
            P = 0.0; F = (Pm - Pel) / Ree * 0.0 - V / (Ree * Cc) * 0.3; V += F * DT; out["t"][i] = t; out["P"][i] = 0; out["F"][i] = 0; out["V"][i] = 0; out["Pes"][i] = Pel - Pm; out["Fd"][i] = 0; continue
        if aprv:
            Ph, Pl, Th, Tl = aprv; cyc = (t % (Th + Tl)); P = Pl + (Ph - Pl) * (1 - math.exp(-min(cyc, Th) / 0.05)) if cyc < Th else Pl + (Ph - Pl) * math.exp(-(cyc - Th) / 0.03)
            if cyc < DT: breaths.append(dict(t=t, kind="APRV", trig="mand", n=0))
            drive = P + Pm - Pel; F = drive / (Rr if drive > 0 else Ree)
            V += F * DT; rec(out, i, t, P, F, V, Pel, Pm, leak); continue
        if phase == "hold":
            F = 0.0; P = Pel - Pm
            if t >= hold_until:
                phase = "exp" if hold_kind == "i" else phase_after_hold(); ph_t0 = t
                if hold_kind == "e": phase = "exp"; tlast_machine = t - 60.0 / RR  # dispara já
            rec(out, i, t, P, F, V, Pel, Pm, leak); continue
        if phase == "exp" and occl and occl[0] + warm <= t:
            occl.pop(0); phase = "hold"; hold_kind = "o"; hold_until = t + sp.get("occl_len", 1.2); ph_t0 = t
            rec(out, i, t, Pel - Pm, 0.0, V, Pel, Pm, leak); continue
        if phase == "exp":
            P = PEEP
            F = (P + Pm - Pel) / (Ree if (V - PEEP * Cc) > -1 else Rr)
            if F > 0: F = (P + Pm - Pel) / Rr
            elif sp.get("flim") and (t - ph_t0) > 0.07: F = max(F, -(sp["flim"] * max(V - PEEP * Cc, 0) ** 1.7 + 0.03))
            start = None
            if mode in ("VCV", "PCV", "PRVC") and machine_due: start = "mand"
            refr = (t - ph_t0) > sp.get("refr", 0.35)
            if mode == "SIMV" and machine_due and ((refr and F > trig) or (t - tlast_machine) >= 60.0 / RR + 1.2): start = "mand"
            if start is None and refr and F > trig and mode in ("VCV", "PCV", "PRVC", "PSV", "SIMV"): start = "pat"
            if start is None and refr and sp.get("autotrig") and (t - ph_t0) > sp["autotrig"]: start = "auto"
            if start is None and mode == "PSV" and sp.get("apnea") and (t - tb) > sp["apnea"]: start = "backup"
            if mode == "CPAP" and F > 0 and (t - ph_t0) > 0.3 and Vd < 0.01:
                breaths.append(dict(t=t, kind="spont")); ph_t0 = t; Vd = 0.0
            if start:
                nb += 1
                he = [h for h in holds_e if h <= t]
                if he and start == "mand":
                    holds_e.remove(he[0])
                    phase = "hold"; hold_kind = "e"; hold_until = t + hold_len; ph_t0 = t
                    rec(out, i, t, Pel - Pm, 0.0, V, Pel, Pm, leak); continue
                kind = "VCV" if mode in ("VCV",) or (mode == "SIMV" and start == "mand") else ("PSV" if mode in ("PSV",) or (mode == "SIMV") else mode)
                if start == "backup": kind = "PCV"
                if mode == "SIMV" and start == "mand": tlast_machine = t
                phase = "insp"; ph_t0 = t; tb = t; Fpk = 0.0; Vbreath0 = V; Vd = 0.0
                if start in ("mand", "auto") or mode in ("VCV", "PCV", "PRVC"): tlast_machine = t
                cur = dict(t=t, kind=kind, trig=start, n=nb); breaths.append(cur)
                hi_ = [h for h in holds_i if h <= t]
                if hi_: holds_i.remove(hi_[0]); cur["hold"] = True
                if rev and rng.random() < rev[4]: rev_eff.append((t + rev[0], rev[1], rev[2], rev[3]))
                if mode == "PRVC" and len(breaths) > 1:
                    vt_last = breaths[-2].get("vt", 0); prvc_p = min(35, max(5, prvc_p + max(-3, min(3, (Vt - vt_last) / Cc * 0.5)))) if vt_last else prvc_p
        if phase == "insp":
            tau = t - ph_t0; kind = cur["kind"]
            if kind == "VCV":
                tf_ = Ti - pause
                if vf: fset = vf
                else: fset = Vt / tf_ if flowpat == "square" else 2 * Vt / tf_ * 0.75
                if tau < tf_:
                    if flowpat == "square": F = fset
                    else: F = fset * (1 - 0.66 * tau / tf_)
                    P = Rr * F + Pel - Pm
                    if sp.get("plimit") and P >= sp["plimit"]: phase = "exp"; ph_t0 = t; cur["vt"] = V - Vbreath0; F = 0.0; P = sp["plimit"]
                elif tau < Ti:
                    F = 0.0; P = Pel - Pm
                else:
                    if cur.get("hold") and tau < Ti + hold_len: F = 0.0; P = Pel - Pm
                    else: phase = "exp"; ph_t0 = t; cur["vt"] = V - Vbreath0; F = 0; P = PEEP
            else:
                if actexp and sp.get("nti") and tau > sp["nti"]: Pm -= actexp * min(1.0, (tau - sp["nti"]) / 0.15)
                tgt = PEEP + (Pinsp if kind == "PCV" else prvc_p if kind == "PRVC" else PS)
                P = PEEP + (tgt - PEEP) * (1 - math.exp(-tau / max(rise, 0.01) * 3)) if rise > 0 else tgt
                F = (P + Pm - Pel) / Rr
                if Pm < 0 and kind == "PSV": P += -Pm * 0.6; F = max(F, 0.0)
                Fpk = max(Fpk, F)
                if kind in ("PCV", "PRVC"):
                    if tau >= Ti and not (cur.get("hold") and tau < Ti + hold_len): phase = "exp"; ph_t0 = t; cur["vt"] = V - Vbreath0
                    elif tau >= Ti: F = 0.0; P = Pel - Pm
                else:
                    Fc = F + (leak * math.sqrt(max(P, 0)) if leak else 0.0)
                    if (tau > 0.12 and Fc <= ets * Fpk) or tau > sp.get("timax", 3.0):
                        phase = "exp"; ph_t0 = t; cur["vt"] = V - Vbreath0
        V += F * DT; Vd += F * DT
        rec(out, i, t, P, F, V, Pel, Pm, leak)
    # janela exibida
    s = int(warm / DT)
    if sp.get("foff"): out["Fd"] = out["Fd"] + sp["foff"]
    stA = sorted(int(round(b["t"] / DT)) for b in breaths); Vfull = np.zeros(n); acc = 0.0; j = 0
    for i in range(n):
        while j < len(stA) and i >= stA[j]: acc = 0.0; j += 1
        acc += out["Fd"][i] * DT; Vfull[i] = acc
    out["Vfull"] = Vfull
    res = {k: v[s:] for k, v in out.items()}; res["t"] = res["t"] - warm
    res["breaths"] = [dict(b, t=b["t"] - warm) for b in breaths if b["t"] >= warm - 0.01]
    # artefatos de exibição
    rng2 = np.random.default_rng(seed)
    if sp.get("secret"):
        a = sp["secret"]; f = 9 + 3 * rng2.random()
        sw = ((res["t"] * f) % 1.0 - 0.5) * 2 * a * (1 + 0.3 * rng2.standard_normal(len(res["t"])))
        mask = np.where(res["F"] < -0.02, 1.0, 0.35)
        res["Fd"] = res["Fd"] + sw * mask; res["P"] = res["P"] + sw * mask * 1.8
    if sp.get("overshoot"):
        for bb in res["breaths"]:
            i0 = int(bb["t"] / DT)
            if 0 <= i0 < len(res["t"]):
                tt = np.arange(0, min(int(0.35 / DT), len(res["t"]) - i0)) * DT
                res["P"][i0:i0 + len(tt)] += sp["overshoot"] * np.exp(-tt / 0.06) * np.sin(np.pi * np.clip(tt / 0.05, 0, 1)) + 0.0
    if sp.get("cardio"):
        hr = sp["cardio"]; ca = sp.get("cardio_amp", 1.0); res["Fd"] = res["Fd"] + 0.035 * ca * np.sin(2 * np.pi * hr / 60 * res["t"]); res["P"] = res["P"] + 0.25 * ca * np.sin(2 * np.pi * hr / 60 * res["t"] + 1)
    res["Fd"] = res["Fd"] + 0.004 * rng2.standard_normal(len(res["t"])); res["P"] = res["P"] + 0.04 * rng2.standard_normal(len(res["t"]))
    # volume exibido: integral do fluxo medido, zerado a cada início de inspiração
    Vdisp = res["Vfull"].copy()
    if sp.get("vclamp", True) and not sp.get("leak"): Vdisp = np.maximum(Vdisp, -0.02)
    res["Vd"] = Vdisp; res["sp"] = sp
    return res


def F_prev_pos(out, i): return out["F"][i - 1] > 0 if i else True
def phase_after_hold(): return "exp"


def rec(out, i, t, P, F, V, Pel, Pm, leak):
    out["t"][i] = t; out["P"][i] = P; out["F"][i] = F; out["V"][i] = V; out["Pes"][i] = 5 + (Pel * 0.3) - Pm
    out["Fd"][i] = F + (leak * math.sqrt(max(P, 0)) if leak else 0.0)


# ---------------------------------------------------------------- métricas para o painel
def metrics(r):
    sp = r["sp"]; P, F, Vd, t = r["P"], r["Fd"], r["Vd"], r["t"]; bs = r["breaths"]
    m = {}
    if bs:
        last = [b for b in bs if b["t"] < t[-1] - 2.5] or bs
        b = last[-1]; i0 = int(b["t"] / DT); i1 = min(len(t) - 1, i0 + int(2.5 / DT))
        m["Ppico"] = float(np.max(P[i0:i1])); m["VT"] = float(np.max(Vd[i0:i1]) * 1000)
        m["FR"] = round(len(bs) * 60 / (t[-1] - t[0]))
        pz = sp.get("pause", 0)
        if pz >= 0.2 and b["kind"] == "VCV":
            ip = i0 + int((sp.get("ti", 0.9) - 0.05) / DT); m["Pplat"] = float(P[ip])
    return m


# ---------------------------------------------------------------- desenho
def _font(sz, b=False): return ImageFont.truetype(FONTB if b else FONT, sz)


def _panel(d, x, y, w, h, ts, ys, lo, hi, col, label, unit, k, ticks, fill=False):
    d.rectangle([x, y, x + w, y + h], outline=COL["grid"], width=max(1, k))
    for tv in ticks:
        yy = y + h - (tv - lo) / (hi - lo) * h
        d.line([x, yy, x + w, yy], fill=COL["grid"] if tv != 0 else COL["axis"], width=max(1, k if tv == 0 else 1))
        d.text((x - 8 * k, yy), f"{tv:g}", fill=COL["dim"], font=_font(12 * k), anchor="rm")
    t0, t1 = ts[0], ts[-1]
    for s in range(int(math.ceil(t0)), int(t1) + 1):
        xx = x + (s - t0) / (t1 - t0) * w; d.line([xx, y, xx, y + h], fill=COL["grid"], width=1)
    pts = [(x + (tt - t0) / (t1 - t0) * w, y + h - (min(max(v, lo), hi) - lo) / (hi - lo) * h) for tt, v in zip(ts[::2], ys[::2])]
    if fill:
        y0 = y + h - (0 - lo) / (hi - lo) * h
        poly = [(pts[0][0], y0)] + pts + [(pts[-1][0], y0)]
        d.polygon(poly, fill=tuple(int(c * 0.28) for c in col))
    d.line(pts, fill=col, width=int(2.2 * k), joint="curve")
    d.text((x + 8 * k, y + 6 * k), label, fill=col, font=_font(15 * k, True))
    d.text((x + 8 * k, y + 24 * k), unit, fill=COL["dim"], font=_font(12 * k))


def _ticks(lo, hi, n=4):
    span = hi - lo; step = [1, 2, 5, 10, 20, 25, 50, 100, 200, 250, 500, 1000][0]
    for s in [1, 2, 5, 10, 20, 25, 50, 100, 200, 250, 500, 1000]:
        if span / s <= n: step = s; break
    a = math.ceil(lo / step) * step; out = []
    while a <= hi + 1e-9: out.append(round(a, 6)); a += step
    return out


def render(r, path, title="", lay="3", panel=None, notes=(), mode_label=None, k=2):
    sp = r["sp"]; W, H = 1400 * k, (880 if lay != "loops" else 900) * k
    im = Image.new("RGB", (W, H), COL["bg"]); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 44 * k], fill=(16, 22, 30))
    d.text((18 * k, 22 * k), title, fill=COL["txt"], font=_font(20 * k, True), anchor="lm")
    d.text((W - 18 * k, 22 * k), "ventilador sintético didático · CÓDICE 360X", fill=COL["dim"], font=_font(14 * k), anchor="rm")
    if mode_label: d.text((W // 2, 22 * k), mode_label, fill=COL["txt"], font=_font(17 * k, True), anchor="mm")
    ts = r["t"]; P = r["P"]; F = r["Fd"] * 60; V = r["Vd"] * 1000
    pw = 1080 * k if panel else 1290 * k; x0 = 80 * k
    def rng_(a, pad, lo=None, hi=None):
        mn, mx = float(np.min(a)), float(np.max(a)); mn = min(mn, 0) if lo is None else lo; mx = mx if hi is None else hi
        sp_ = (mx - mn) or 1; return mn - sp_ * pad, mx + sp_ * pad
    if lay in ("3", "3pes", "2"):
        chans = [("P", P, "Pressão (Paw)", "cmH2O", COL["P"], False), ("F", F, "Fluxo", "L/min", COL["F"], True)]
        if lay != "2": chans.append(("V", V, "Volume", "mL", COL["V"], True))
        if lay == "3pes": chans.append(("Pes", r["Pes"], "Pressão esofágica", "cmH2O", COL["Pes"], False))
        top = 60 * k; avail = H - top - 40 * k; gap = 14 * k; h = (avail - gap * (len(chans) - 1)) / len(chans)
        for j, (key, ys, lab, unit, col, fill) in enumerate(chans):
            lo, hi = rng_(ys, 0.08)
            if key == "P": lo, hi = min(-2, lo), max(hi, 20); lo = math.floor(lo / 5) * 5; hi = math.ceil(hi / 5) * 5
            if key == "F": m = max(abs(lo), abs(hi), 30); lo, hi = -m, m
            if key == "V": lo = min(lo, -50); hi = max(hi, 300)
            y = top + j * (h + gap)
            _panel(d, x0, y, pw, h, ts, ys, lo, hi, col, lab, unit, k, _ticks(lo, hi), fill)
            for nt in notes:
                if nt[1] == key:
                    xx = x0 + (nt[0] - ts[0]) / (ts[-1] - ts[0]) * pw
                    d.text((xx, y + 10 * k), nt[2], fill=COL["txt"], font=_font(13 * k, True), anchor="mt")
        d.text((x0 + pw / 2, H - 16 * k), "tempo (s)", fill=COL["dim"], font=_font(13 * k), anchor="mm")
    else:  # loops
        bw = 600 * k; bh = 520 * k; top = 70 * k
        _loop(d, x0, top, bw, bh, P, V, "Pressão (cmH2O)", "Volume (mL)", COL["P"], k, r)
        _loop(d, x0 + bw + 90 * k, top, bw, bh, V, F, "Volume (mL)", "Fluxo (L/min)", COL["F"], k, r)
        y = top + bh + 50 * k; h = H - y - 40 * k
        lo, hi = rng_(P, 0.1); lo = min(lo, -2)
        _panel(d, x0, y, (bw * 2 + 90 * k), h, ts, P, lo, hi, COL["P"], "Paw", "cmH2O", k, _ticks(lo, hi, 3))
    if panel:
        px = x0 + pw + 30 * k; py = 70 * k
        for lab, val in panel:
            d.rectangle([px, py, W - 18 * k, py + 82 * k], outline=COL["grid"], width=k)
            d.text((px + 12 * k, py + 10 * k), lab, fill=COL["dim"], font=_font(14 * k))
            d.text((W - 30 * k, py + 54 * k), str(val), fill=COL["txt"], font=_font(28 * k, True), anchor="rm")
            py += 94 * k
    im = im.resize((W // k, H // k), Image.LANCZOS)
    im.quantize(colors=96, method=Image.Quantize.FASTOCTREE).save(path, optimize=True)


def _loop(d, x, y, w, h, X, Y, lx, ly, col, k, r):
    n = len(X); ib = [int(b["t"] / DT) for b in r["breaths"]]
    seg = (ib[-3], ib[-2]) if len(ib) >= 3 else (0, n - 1)
    xs, ys = X[seg[0]:seg[1]], Y[seg[0]:seg[1]]
    def lim(a):
        mn, mx = float(min(np.min(a), 0)), float(np.max(a)); s = (mx - mn) or 1; return mn - 0.1 * s, mx + 0.1 * s
    xl, xh = lim(xs); yl, yh = lim(ys)
    if ly.startswith("Fluxo"): m = max(abs(yl), abs(yh)); yl, yh = -m, m
    d.rectangle([x, y, x + w, y + h], outline=COL["grid"], width=k)
    for tv in _ticks(xl, xh, 5):
        xx = x + (tv - xl) / (xh - xl) * w; d.line([xx, y, xx, y + h], fill=COL["grid"] if tv else COL["axis"], width=1 if tv else k)
        d.text((xx, y + h + 6 * k), f"{tv:g}", fill=COL["dim"], font=_font(12 * k), anchor="mt")
    for tv in _ticks(yl, yh, 5):
        yy = y + h - (tv - yl) / (yh - yl) * h; d.line([x, yy, x + w, yy], fill=COL["grid"] if tv else COL["axis"], width=1 if tv else k)
        d.text((x - 6 * k, yy), f"{tv:g}", fill=COL["dim"], font=_font(12 * k), anchor="rm")
    pts = [(x + (a - xl) / (xh - xl) * w, y + h - (b - yl) / (yh - yl) * h) for a, b in zip(xs[::2], ys[::2])]
    d.line(pts, fill=col, width=int(2.4 * k), joint="curve")
    d.text((x + w / 2, y + h + 26 * k), lx, fill=COL["dim"], font=_font(13 * k), anchor="mt")
    d.text((x + 8 * k, y + 8 * k), ly, fill=col, font=_font(14 * k, True))


def make(sp, path, title, seed=0):
    r = simulate(sp, seed)
    pan = None
    if sp.get("panel"):
        m = metrics(r); pan = []
        for key in sp["panel"]:
            if isinstance(key, tuple): pan.append(key)
            elif key == "Ppico": pan.append(("Ppico (cmH2O)", f"{m.get('Ppico', 0):.0f}"))
            elif key == "Pplat": pan.append(("Pplatô (cmH2O)", f"{m['Pplat']:.0f}" if "Pplat" in m else "—"))
            elif key == "PEEP": pan.append(("PEEP (cmH2O)", f"{sp.get('peep', 5):g}"))
            elif key == "VT": pan.append(("VT exp (mL)", f"{m.get('VT', 0):.0f}"))
            elif key == "FR": pan.append(("FR total (irpm)", f"{m.get('FR', 0)}"))
    render(r, path, title=title, lay=sp.get("lay", "3"), panel=pan, notes=sp.get("notes", ()), mode_label=sp.get("label"))
    return r
