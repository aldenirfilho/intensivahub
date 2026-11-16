"""Modo M, Doppler espectral e layouts compostos do POCUS 360X."""
import math
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import gaussian_filter
from us_core import bmode, frame, paste_bmode, save, fnt
import us_scenes as S

YEL = (255, 230, 90); GRN = (120, 255, 140); WHT = (230, 230, 230); DIM = (150, 155, 160)


def _gray(a):
    g = (np.clip(a, 0, 1) * 255).astype(np.uint8); return Image.fromarray(np.stack([g, g, g], -1))


def _mm_frame(im, d, M, box, k, zmax, tlen, label):
    x0, y0, x1, y1 = [v * k for v in box]
    img = _gray(M).resize((x1 - x0, y1 - y0), Image.BILINEAR); im.paste(img, (x0, y0))
    d.rectangle([x0, y0, x1, y1], outline=(60, 60, 60), width=k)
    for cm in range(0, int(zmax) + 1):
        yy = y0 + cm / zmax * (y1 - y0); d.line([x1 + 6 * k, yy, x1 + 14 * k, yy], fill=WHT, width=k)
        if cm % 2 == 0 or zmax <= 6: d.text((x1 + 18 * k, yy), f"{cm}", fill=WHT, font=fnt(12 * k), anchor="lm")
    for s in range(0, int(tlen) + 1):
        xx = x0 + s / tlen * (x1 - x0); d.line([xx, y1, xx, y1 + 8 * k], fill=WHT, width=k)
    d.text((x0, y1 + 12 * k), "1 s / divisão", fill=DIM, font=fnt(12 * k))
    if label: d.text((x0, y0 - 8 * k), label, fill=WHT, font=fnt(15 * k, True), anchor="ls")
    return lambda t, z: (x0 + t / tlen * (x1 - x0), y0 + z / zmax * (y1 - y0))


def _cal(d, pa, pb, txt, k, side=1):
    n = 14
    for i in range(0, n, 2):
        q0 = (pa[0] + (pb[0] - pa[0]) * i / n, pa[1] + (pb[1] - pa[1]) * i / n); q1 = (pa[0] + (pb[0] - pa[0]) * (i + 1) / n, pa[1] + (pb[1] - pa[1]) * (i + 1) / n)
        d.line([q0, q1], fill=YEL, width=2 * k)
    for q in (pa, pb): d.line([q[0] - 7 * k, q[1], q[0] + 7 * k, q[1]], fill=YEL, width=2 * k)
    d.text((max(pa[0], pb[0]) + 10 * k * side, (pa[1] + pb[1]) / 2), txt, fill=YEL, font=fnt(16 * k, True), anchor="lm" if side > 0 else "rm")


# ------------------------------------------------------------------------------------------------ MODO M
def mm_lung(path, title, kind="slide", seed=0, sub="Modo M · pulmão", hr=80, k=2, point_frac=0.5):
    rng = np.random.default_rng(seed)
    sc = S.lung(probe="linear", depth=6, pat="A", seed=seed, linear_w=4.0); D, X, Z = bmode(sc, seed=seed)
    nb = D.shape[1]; prof = D[:, nb // 2]; ns = len(prof); nt = 700; zp = int(1.3 / 6 * ns)
    M = np.tile(prof[:, None], (1, nt)) * (1 + 0.04 * rng.standard_normal((1, nt)))
    def sand(cols):
        n = rng.random((ns - zp, cols)); n = gaussian_filter(n, (1.2, 1.4)); n = (n - n.min()) / (n.max() - n.min())
        return 0.25 + 0.55 * n ** 1.5
    if kind == "slide": M[zp + 3:, :] = sand(nt)[3:]
    elif kind == "point":
        seg = int(nt * point_frac / 2.5)
        on = np.zeros(nt, bool)
        for j in range(0, nt, int(nt / 2.5)): on[j:j + seg] = True
        S_ = sand(nt); M[zp + 3:, on] = S_[3:, on]
    elif kind == "pulse":
        for j in range(nt):
            if (j * 4.0 / nt * hr / 60) % 1.0 < 0.06: M[zp + 3:, j] = np.maximum(M[zp + 3:, j], 0.45 + 0.1 * rng.random(ns - zp - 3))
    im, d = frame(title=title, sub=sub, k=k)
    tp = paste_bmode(im, d, sc, D, (420, 80, 780, 400), k=k)
    sc.marks = []; xa, za = tp(0, 0); xb, zb = tp(0, 6); d.line([xa, za, xb, zb], fill=GRN, width=k)
    _mm_frame(im, d, M, (60, 440, 1120, 860), k, 6, 4, "Modo M (linha verde)")
    save(im, path, k)


def mm_track(path, title, kind, seed=0, k=2, **p):
    """kind: ivc (dmax, dmin, mech='esp'|'vm'), tapse (mm), epss (mm), diaph (cm, paradox=False)."""
    rng = np.random.default_rng(seed); nt = 700; tlen = 4.0; t = np.linspace(0, tlen, nt)
    zmax = {"ivc": 8.0, "tapse": 16.0, "epss": 12.0, "diaph": 14.0}[kind]; ns = 500; z = np.linspace(0, zmax, ns)
    base = gaussian_filter(rng.random((ns, 1)), (3, 0))[:, 0]; base = 0.25 + 0.35 * (base - base.min()) / (np.ptp(base) + 1e-9)
    M = np.tile(base[:, None], (1, nt))
    def put_line(zt, w=0.08, amp=0.95):
        for j in range(nt): M[:, j] = np.maximum(M[:, j], amp * np.exp(-((z - zt[j]) / w) ** 2))
    def fill(z1, z2, val=0.02):
        for j in range(nt): M[(z > z1[j]) & (z < z2[j]), j] = val
    resp = 0.5 - 0.5 * np.cos(2 * np.pi * t / p.get("rper", 4.0))  # 0 → 1 (inspiração)
    hr = p.get("hr", 85); ph = (t * hr / 60) % 1.0
    im, d = frame(title=title, sub=p.get("sub", ""), k=k)
    if kind == "ivc":
        dmax, dmin = p["dmax"], p["dmin"]; zc = 5.0
        dia = dmax - (dmax - dmin) * (resp if p.get("mech", "esp") == "esp" else (1 - resp))
        fill(zc - dia / 2, zc + dia / 2); put_line(zc - dia / 2); put_line(zc + dia / 2)
        mp = _mm_frame(im, d, M + 0.03 * rng.standard_normal(M.shape), (80, 120, 1100, 840), k, zmax, tlen, "Modo M · veia cava inferior (2 cm da junção com o AD)")
        jmax = int(np.argmax(dia)); jmin = int(np.argmin(dia))
        _cal(d, mp(t[jmax], zc - dmax / 2), mp(t[jmax], zc + dmax / 2), f"{dmax:.1f} cm".replace(".", ","), k)
        _cal(d, mp(t[jmin], zc - dmin / 2), mp(t[jmin], zc + dmin / 2), f"{dmin:.1f} cm".replace(".", ","), k)
    elif kind == "tapse":
        a = p["mm"] / 10; sys_ = np.where(ph < 0.35, np.sin(np.pi * ph / 0.35), 0) ** 1.0; zt = 11.0 - a * sys_
        fill(zt - 4.0, zt - 0.6, 0.03); put_line(zt, 0.15); put_line(zt + 0.4, 0.2, 0.6)
        mp = _mm_frame(im, d, M + 0.03 * rng.standard_normal(M.shape), (80, 120, 1100, 840), k, zmax, tlen, "Modo M · anel tricúspide lateral (apical 4C)")
        j = int(np.argmin(zt[: nt // 2])); j0 = max(0, j - int(0.33 * nt / tlen * 60 / hr))
        _cal(d, mp(t[j], zt[j0]), mp(t[j], zt[j]), f"TAPSE {p['mm']:.0f} mm", k)
    elif kind == "epss":
        e = p["mm"] / 10; zs = 4.0 + 0.15 * np.sin(2 * np.pi * ph)
        put_line(zs, 0.35, 0.7); fill(zs + 0.4, np.full(nt, 9.0), 0.03)
        Ew = np.exp(-((ph - 0.55) / 0.06) ** 2); Aw = 0.6 * np.exp(-((ph - 0.85) / 0.04) ** 2)
        zm = 8.0 - (8.0 - (4.4 + e)) * np.clip(Ew + Aw, 0, 1); put_line(zm, 0.07, 0.95); put_line(np.full(nt, 9.2), 0.25, 0.7)
        mp = _mm_frame(im, d, M + 0.03 * rng.standard_normal(M.shape), (80, 120, 1100, 840), k, zmax, tlen, "Modo M · paraesternal longo, ponta do folheto anterior mitral")
        j = int(np.argmin(zm[: nt // 2 + 40])); _cal(d, mp(t[j], zs[j] + 0.4), mp(t[j], zm[j]), f"EPSS {p['mm']:.0f} mm", k)
    elif kind == "diaph":
        a = p["cm"]; sgn = -1 if p.get("paradox") else 1; zt = 8.0 - sgn * a * resp
        put_line(zt, 0.18, 1.0); fill(zt + 0.3, np.full(nt, zmax + 1), 0.0) if False else None
        mp = _mm_frame(im, d, M + 0.03 * rng.standard_normal(M.shape), (80, 120, 1100, 840), k, zmax, tlen, "Modo M · hemidiafragma direito (subcostal, janela hepática)")
        j0 = int(np.argmin(resp[: nt // 2 + 50])); j1 = int(np.argmax(resp))
        _cal(d, mp(t[j1], zt[j0]), mp(t[j1], zt[j1]), f"{abs(a):.1f} cm".replace(".", ","), k)
    save(im, path, k)


# ------------------------------------------------------------------------------------------------ DOPPLER ESPECTRAL
def doppler(path, title, kind, seed=0, k=2, **p):
    rng = np.random.default_rng(seed); T = p.get("T", 4.0); nt = 900; t = np.linspace(0, T, nt); hr = p.get("hr", 80); per = 60 / hr
    ph = (t % per) / per; beat = (t // per).astype(int)
    env = np.zeros(nt); env2 = None; unit = "cm/s"; vmax = 100; notes = []
    if kind == "vti":
        var = p.get("var", 0.0); vpk = p.get("vpk", 90)
        mod = 1 + var / 2 * np.sin(2 * np.pi * t / p.get("rper", 4.0))
        s = np.clip((ph - 0.08) / 0.34, 0, 1); env = -vpk * mod * np.where((s > 0) & (s < 1), np.sin(np.pi * s) ** 1.3, 0); vmax = max(120, vpk * 1.4)
        b0 = 1; m0 = beat == b0; vti = np.sum(-env[m0]) * (t[1] - t[0])
        notes.append((float(t[m0][np.argmin(env[m0])]), float(np.min(env[m0])) - 12, f"VTI {vti:.0f} cm"))
        if var:
            vmx = [float(-np.min(env[beat == b])) for b in range(int(T / per)) if np.any(beat == b)]
            notes.append((T * 0.75, -vmax * 0.92, f"Vpico máx {max(vmx):.0f} · mín {min(vmx):.0f} cm/s"))
    elif kind == "hv":
        pat = p.get("pat", "normal"); Sa, Da = {"normal": (-45, -25), "leve": (-22, -35), "grave": (30, -40)}[pat]
        env = (12 * np.exp(-((ph - 0.05) / 0.04) ** 2) + Sa * np.exp(-((ph - 0.3) / 0.08) ** 2) + 8 * np.exp(-((ph - 0.52) / 0.04) ** 2) + Da * np.exp(-((ph - 0.72) / 0.07) ** 2))
        vmax = 70; notes += [(per * 0.3, Sa + (-10 if Sa < 0 else 10), "S"), (per * 0.72, Da - 10, "D")]
    elif kind == "pv":
        pf = p.get("pf", 0.2); vm = p.get("vm", 22)
        env = vm * (1 - pf * (0.5 + 0.5 * np.cos(2 * np.pi * ph))) if pf < 1 else vm * (1 - pf * (0.5 + 0.5 * np.cos(2 * np.pi * ph)))
        vmax = 45
    elif kind == "irv":
        pat = p.get("pat", "cont"); vmax = 50
        art = 35 * np.exp(-((ph - 0.25) / 0.07) ** 2) + 12
        if pat == "cont": ven = -(14 + 2 * np.sin(2 * np.pi * ph))
        elif pat == "bi": ven = -(14 * np.exp(-((ph - 0.3) / 0.1) ** 2) + 12 * np.exp(-((ph - 0.75) / 0.09) ** 2))
        else: ven = -(18 * np.exp(-((ph - 0.75) / 0.08) ** 2))
        env, env2 = art, ven
    elif kind == "mitral":
        E, A = p.get("E", 80), p.get("A", 60); dt = p.get("dt", 0.18)
        if p.get("var"): E = E * (1 + p["var"] / 2 * np.sin(2 * np.pi * t / p.get("rper", 4.0)))
        env = E * np.where(ph > 0.45, np.exp(-((ph - 0.5) / 0.045) ** 2) * (ph < 0.5) + np.exp(-(ph - 0.5) / (dt / per * 0.6)) * (ph >= 0.5) * (ph < 0.78), 0) + A * np.exp(-((ph - 0.9) / 0.035) ** 2)
        Em = float(np.max(E)) if np.ndim(E) else E; vmax = max(120, Em * 1.4); notes += [(per * 0.5, Em + 10, "E"), (per * 0.9, A + 10, "A")]
        if p.get("var"): notes.append((T * 0.7, Em + 30, f"E máx {Em:.0f} · mín {float(np.min(E)):.0f} cm/s"))
    elif kind == "tr":
        vp = p.get("v", 3.0) * 100; unit = "m/s"; s = np.clip((ph - 0.05) / 0.4, 0, 1)
        if p.get("ao"): s = np.clip((ph - 0.1) / 0.32, 0, 1)
        env = -vp * np.where((s > 0) & (s < 1), np.sin(np.pi * s) ** 0.6, 0); vmax = max(400, vp * 1.3)
        notes.append((per * 0.25, -vp - 25, f"Vmáx {p.get('v', 3.0):.1f} m/s".replace(".", ",")))
    elif kind == "rvot":
        at = p.get("at", 0.12); vp = p.get("vpk", 60); s = np.clip((ph - 0.08) / 0.34, 0, 1)
        shape = np.where(s * 0.34 * per < at, (s * 0.34 * per / at), np.clip(1 - (s * 0.34 * per - at) / (0.34 * per - at), 0, 1))
        if p.get("notch"): shape *= 1 - 0.45 * np.exp(-((s - 0.55) / 0.07) ** 2)
        env = -vp * np.where((s > 0) & (s < 1), shape, 0); vmax = 100
        notes.append((per * 0.25, -vp - 14, f"TA {at * 1000:.0f} ms"))
    nv = 360; v = np.linspace(-vmax, vmax, nv)
    G = np.zeros((nv, nt))
    for e in [env] + ([env2] if env2 is not None else []):
        for j in range(nt):
            ev = e[j]
            if abs(ev) < 1: continue
            if ev > 0: m = (v > 0.05 * ev) & (v <= ev); rel = v[m] / ev
            else: m = (v < 0.05 * ev) & (v >= ev); rel = v[m] / ev
            G[m, j] = np.maximum(G[m, j], 0.35 + 0.65 * rel ** 2)
    G = G * (0.65 + 0.5 * rng.random(G.shape)); G = gaussian_filter(G, (1.0, 0.6)); G += 0.04 * rng.random(G.shape)
    im, d = frame(title=title, sub=p.get("sub", ""), k=k)
    x0, y0, x1, y1 = 70 * k, 110 * k, 1110 * k, 760 * k
    img = _gray(G[::-1]).resize((x1 - x0, y1 - y0), Image.BILINEAR); im.paste(img, (x0, y0))
    yb = y0 + (y1 - y0) / 2; d.line([x0, yb, x1, yb], fill=(90, 160, 255), width=k)
    for vv in np.linspace(-vmax, vmax, 9):
        yy = y0 + (vmax - vv) / (2 * vmax) * (y1 - y0); d.line([x1, yy, x1 + 8 * k, yy], fill=WHT, width=k)
        lab = f"{vv / 100:.1f}".replace(".", ",") if unit == "m/s" else f"{vv:.0f}"
        d.text((x1 + 12 * k, yy), lab, fill=WHT, font=fnt(12 * k), anchor="lm")
    d.text((x1 + 12 * k, y0 - 14 * k), unit, fill=DIM, font=fnt(12 * k), anchor="lm")
    # ECG
    ye = 820 * k; ecg = np.zeros(nt)
    for b in range(int(T / per) + 1):
        tq = b * per + 0.02
        ecg += 1.0 * np.exp(-((t - tq) / 0.012) ** 2) - 0.25 * np.exp(-((t - tq - 0.03) / 0.015) ** 2) + 0.25 * np.exp(-((t - tq - 0.28) / 0.05) ** 2) + 0.12 * np.exp(-((t - tq + 0.15) / 0.03) ** 2)
    pts = [(x0 + tt / T * (x1 - x0), ye - e * 30 * k) for tt, e in zip(t, ecg)]; d.line(pts, fill=(80, 230, 120), width=2 * k)
    for (tt, vv, txt) in notes:
        d.text((x0 + tt / T * (x1 - x0), y0 + (vmax - vv) / (2 * vmax) * (y1 - y0)), txt, fill=YEL, font=fnt(17 * k, True), anchor="mm")
    save(im, path, k)


# ------------------------------------------------------------------------------------------------ LAYOUTS
def single(path, title, sc, sub="", seed=0, k=2):
    D, X, Z = bmode(sc, seed=seed); im, d = frame(title=title, sub=sub, k=k)
    paste_bmode(im, d, sc, D, (150, 90, 1050, 870), k=k); save(im, path, k)


def pair(path, title, scA, scB, labA, labB, sub="", seed=0, k=2):
    im, d = frame(title=title, sub=sub, k=k)
    for sc, box, lab in ((scA, (40, 130, 570, 860), labA), (scB, (630, 130, 1160, 860), labB)):
        D, X, Z = bmode(sc, seed=seed); paste_bmode(im, d, sc, D, box, k=k, label=lab)
    save(im, path, k)
