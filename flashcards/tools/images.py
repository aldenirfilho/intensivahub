import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
import os
os.makedirs("media", exist_ok=True)
BG, FG, GOLD, CY, RD, GR, AM = "#0e1116", "#e8e6df", "#d4af37", "#4dd4ff", "#ff6b6b", "#5be38a", "#ffc14d"
plt.rcParams.update({"figure.facecolor": BG, "axes.facecolor": BG, "axes.edgecolor": "#555", "text.color": FG,
    "axes.labelcolor": FG, "xtick.color": "#aaa", "ytick.color": "#aaa", "font.size": 12, "axes.titleweight": "bold"})
def save(fig, n):
    if fig._suptitle is not None: fig._suptitle.set_y(1.04)
    fig.savefig(f"media/{n}", dpi=110, bbox_inches="tight"); plt.close(fig)

# 1 VM pressure-time
fig, axs = plt.subplots(1, 3, figsize=(12, 3.6), sharey=True)
for ax, (tit, pk, pl, col) in zip(axs, [("Normal", 22, 18, GR), ("↑ Resistência", 38, 18, AM), ("↓ Complacência", 38, 33, RD)]):
    peep = 5; t = np.linspace(0, 3, 600); p = np.full_like(t, peep, dtype=float)
    ins = t < 1; p[ins] = peep + (pk - peep) * (t[ins] / 1) ** 0.9
    pa = (t >= 1) & (t < 1.5); p[pa] = pl + (pk - pl) * np.exp(-(t[pa] - 1) * 25)
    ex = t >= 1.5; p[ex] = peep + (pl - peep) * np.exp(-(t[ex] - 1.5) * 6)
    ax.plot(t, p, color=col, lw=3); ax.axhline(peep, color="#777", ls=":")
    ax.annotate(f"Ppico {pk}", (1, pk), (1.6, pk + 3), color=FG, arrowprops=dict(arrowstyle="->", color=FG))
    ax.annotate(f"Pplatô {pl}", (1.4, pl), (1.9, pl - 7), color=CY, arrowprops=dict(arrowstyle="->", color=CY))
    ax.text(2.3, peep + 1, "PEEP 5", color="#aaa", fontsize=10)
    ax.set_title(tit, color=col); ax.set_xlabel("tempo (s)"); ax.set_ylim(0, 45)
axs[0].set_ylabel("Pressão (cmH₂O)")
fig.suptitle("VCV com pausa inspiratória: Ppico − Pplatô = resistência | Pplatô − PEEP = driving pressure", color=GOLD)
save(fig, "img_vm_pressao.png")

# 2 O2-Hb curve
fig, ax = plt.subplots(figsize=(7, 4.4)); po = np.linspace(0, 100, 400)
for p50, col, lab in [(26.6, CY, "Normal (P50 ≈ 27)"), (20, GR, "← Esquerda: ↓T, ↓CO₂, alcalose, ↓2,3-DPG, CO, HbF"), (33, RD, "→ Direita: ↑T, ↑CO₂, acidose, ↑2,3-DPG, exercício")]:
    ax.plot(po, 100 * po**2.7 / (po**2.7 + p50**2.7), color=col, lw=2.5, label=lab)
ax.axhline(50, color="#555", ls=":"); ax.axvline(60, color=AM, ls="--"); ax.text(61, 20, "PaO₂ 60 ≈ SatO₂ 90%", color=AM)
ax.set_xlabel("PaO₂ (mmHg)"); ax.set_ylabel("SatO₂ (%)"); ax.legend(fontsize=9, facecolor=BG, edgecolor="#555", labelcolor=FG)
ax.set_title("Curva de dissociação da oxi-hemoglobina — 'CADET, face Right!'", color=GOLD); save(fig, "img_o2hb.png")

# 3 Starling
fig, ax = plt.subplots(figsize=(7, 4.4)); x = np.linspace(0, 10, 300); y = 100 * (1 - np.exp(-x / 2.2))
ax.plot(x, y, color=CY, lw=3)
for x0, col, txt in [(1.5, GR, "Responsivo\nΔ pré-carga → ↑↑ VS"), (7.5, RD, "Não responsivo\n(platô → só congestão)")]:
    y0 = 100 * (1 - np.exp(-x0 / 2.2)); y1 = 100 * (1 - np.exp(-(x0 + 1.2) / 2.2))
    ax.plot([x0, x0 + 1.2], [y0, y0], color=col, lw=2); ax.plot([x0 + 1.2, x0 + 1.2], [y0, y1], color=col, lw=4)
    ax.text(x0 - 0.3, y0 - 22 if x0 < 5 else y0 - 30, txt, color=col, fontsize=11)
ax.set_xlabel("Pré-carga"); ax.set_ylabel("Volume sistólico"); ax.set_xticks([]); ax.set_yticks([])
ax.set_title("Curva de Frank-Starling", color=GOLD); save(fig, "img_starling.png")

# 4 PPV
fig, ax = plt.subplots(figsize=(9, 3.8)); t = np.linspace(0, 10, 3000)
env = 1 + 0.18 * np.sin(2 * np.pi * t / 5)
beat = np.maximum(0, np.sin(2 * np.pi * t * 1.2)) ** 3
p = 70 + 40 * env * beat
ax.plot(t, p, color=RD, lw=1.8); ax.plot(t, 70 + 40 * env, color=GOLD, ls="--", lw=1)
ax.text(1.1, 122, "PPmáx (inspiração)", color=GR); ax.text(3.6, 96, "PPmín (expiração)", color=AM)
ax.set_title("VPP = (PPmáx − PPmín) / média × 100  →  > 13% = responsivo", color=GOLD)
ax.set_xlabel("tempo (s)"); ax.set_ylabel("PA (mmHg)"); save(fig, "img_ppv.png")

# 5 ICP PV
fig, ax = plt.subplots(figsize=(7, 4.4)); v = np.linspace(0, 10, 300); icp = 5 + 1.2 * np.exp(v / 2.3)
ax.plot(v, icp, color=CY, lw=3); ax.axhline(22, color=RD, ls="--"); ax.text(0.2, 24, "PIC 22 — tratar", color=RD)
ax.axvspan(0, 5, color=GR, alpha=0.08); ax.axvspan(5, 10, color=RD, alpha=0.08)
ax.text(0.5, 60, "Compensação\n(LCR/sangue saem)", color=GR); ax.text(5.6, 60, "Descompensação\npequeno ΔV → ↑↑ PIC", color=RD)
ax.set_xlabel("Volume intracraniano"); ax.set_ylabel("PIC (mmHg)"); ax.set_xticks([])
ax.set_title("Monro-Kellie: curva pressão-volume intracraniana", color=GOLD); save(fig, "img_icp_pv.png")

# 6 Lassen
fig, ax = plt.subplots(figsize=(7, 4.2)); m = np.linspace(20, 190, 400)
cbf = np.where(m < 50, 50 * (m - 20) / 30, np.where(m > 150, 50 + (m - 150) * 1.2, 50))
ax.plot(m, cbf, color=CY, lw=3); ax.axvspan(50, 150, color=GR, alpha=0.1)
ax.text(70, 55, "Autorregulação preservada", color=GR); ax.text(22, 30, "Isquemia", color=AM); ax.text(152, 75, "Hiperemia/\nedema", color=RD)
ax.set_xlabel("PAM (mmHg)"); ax.set_ylabel("Fluxo sanguíneo cerebral (mL/100 g/min)")
ax.set_title("Curva de Lassen — no TCE a curva desloca/perde-se", color=GOLD); save(fig, "img_lassen.png")

# 7 ECG hyperkalemia
def g(t, a, mu, s): return a * np.exp(-((t - mu) ** 2) / (2 * s**2))
def beats(t, P, T, qw, pr):
    y = np.zeros_like(t)
    for c in np.arange(0.4, 3, 0.85):
        y += g(t, P, c - pr, 0.035) - g(t, 0.12, c - 0.03 * qw, 0.012 * qw) + g(t, 1.1, c, 0.015 * qw) - g(t, 0.25, c + 0.03 * qw, 0.014 * qw) + g(t, T, c + 0.25 + 0.04 * qw, 0.05 * (1 if T < 0.7 else 0.6) * qw**0.5)
    return y
fig, axs = plt.subplots(4, 1, figsize=(9, 7)); t = np.linspace(0, 3, 3000)
specs = [("Normal", beats(t, .15, .3, 1, .16), GR), ("K⁺ ~6–7: T apiculada e estreita", beats(t, .15, .95, 1, .16), AM),
         ("K⁺ ~7–8: P achatada, PR ↑, QRS largo", beats(t, .04, .8, 2.6, .24), "#ff9b4d"), ("K⁺ > 8–9: onda sinusoidal → FV/assistolia", 0.9 * np.sin(2 * np.pi * t * 1.6), RD)]
for ax, (tt, y, col) in zip(axs, specs):
    ax.plot(t, y, color=col, lw=2); ax.set_title(tt, color=col, fontsize=11, loc="left"); ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values(): sp.set_visible(False)
    ax.grid(color="#3a1d1d", lw=0.5)
fig.suptitle("ECG esquemático da hipercalemia (didático)", color=GOLD); fig.tight_layout(); save(fig, "img_ecg_k.png")

# 8 Capnography
fig, axs = plt.subplots(1, 2, figsize=(11, 3.6))
def capno(t, shark=False):
    y = np.zeros_like(t)
    for c in [0, 4]:
        tt = t - c; ph = (tt > 0.3) & (tt < 2.6)
        if shark: y[ph] = 38 * (1 - np.exp(-(tt[ph] - 0.3) / 0.9))
        else: y[ph] = np.clip(38 * (tt[ph] - 0.3) / 0.25, 0, 35) + np.where(tt[ph] > 0.55, (tt[ph] - 0.55) * 2, 0)
        dn = (tt >= 2.6) & (tt < 2.85); y[dn] = y[ph][-1] * (1 - (tt[dn] - 2.6) / 0.25)
    return y
t = np.linspace(0, 8, 2000)
axs[0].plot(t, capno(t), color=GR, lw=2.5); axs[0].set_title("Normal: I base · II ascensão · III platô · 0 inspiração", color=GR, fontsize=11)
axs[0].text(1.2, 41, "EtCO₂ 35–45", color=CY)
axs[1].plot(t, capno(t, True), color=AM, lw=2.5); axs[1].set_title("'Barbatana de tubarão' = broncoespasmo/obstrução", color=AM, fontsize=11)
for ax in axs: ax.set_ylim(0, 50); ax.set_xlabel("tempo"); ax.set_ylabel("CO₂ (mmHg)")
fig.suptitle("Capnografia | PCR: EtCO₂ < 10 após 20 min = mau prognóstico; ↑ súbito > 35–40 = RCE", color=GOLD); save(fig, "img_capno.png")

# 9 RASS
fig, ax = plt.subplots(figsize=(11, 2.6)); vals = list(range(4, -6, -1))
cols = ["#b30000", "#e03a3a", "#ff7b4d", AM, GR, "#4dbbff", "#3b8fe0", "#2f6fbf", "#2c4f99", "#26336b"]
labs = ["Combativo", "Muito agitado", "Agitado", "Inquieto", "Alerta/calmo", "Sonolento", "Sedação leve", "Moderada", "Profunda", "Não desperta"]
for i, (v, c, l) in enumerate(zip(vals, cols, labs)):
    ax.add_patch(Rectangle((i, 0), 1, 1, color=c)); ax.text(i + .5, .62, f"{v:+d}" if v else "0", ha="center", fontsize=16, weight="bold", color="white")
    ax.text(i + .5, .25, l, ha="center", fontsize=8.5, color="white")
ax.add_patch(Rectangle((4, -.15), 3, 1.3, fill=False, ec=GOLD, lw=3)); ax.text(5.5, -.45, "Alvo usual: RASS −2 a 0", ha="center", color=GOLD, fontsize=12)
ax.set_xlim(0, 10); ax.set_ylim(-.6, 1.2); ax.axis("off"); ax.set_title("Escala RASS", color=GOLD); save(fig, "img_rass.png")

# 10 Acid-base flowchart
fig, ax = plt.subplots(figsize=(10, 6)); ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 10)
def box(x, y, w, h, t, c):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1", fc="#161c24", ec=c, lw=2)); ax.text(x + w / 2, y + h / 2, t, ha="center", va="center", fontsize=10.5, color=FG)
def arr(x1, y1, x2, y2): ax.annotate("", (x2, y2), (x1, y1), arrowprops=dict(arrowstyle="->", color="#aaa", lw=1.5))
box(3.5, 8.6, 3, 1, "pH < 7,35 ou > 7,45?", GOLD)
box(0.3, 6.5, 4, 1.3, "ACIDEMIA\nHCO₃⁻ ↓ → metabólica\nPaCO₂ ↑ → respiratória", RD)
box(5.7, 6.5, 4, 1.3, "ALCALEMIA\nHCO₃⁻ ↑ → metabólica\nPaCO₂ ↓ → respiratória", CY)
arr(4.5, 8.6, 2.3, 7.9); arr(5.5, 8.6, 7.7, 7.9)
box(0.3, 4.2, 4, 1.4, "Compensação\nWinter: 1,5×HCO₃⁻ + 8 ± 2", AM); box(5.7, 4.2, 4, 1.4, "Compensação\n0,7×HCO₃⁻ + 21 ± 2", AM)
arr(2.3, 6.5, 2.3, 5.7); arr(7.7, 6.5, 7.7, 5.7)
box(0.3, 1.9, 4, 1.5, "AG = Na − (Cl + HCO₃⁻)\ncorrigir: + 2,5 × (4 − Alb)", GR); arr(2.3, 4.2, 2.3, 3.5)
box(5.0, 1.9, 4.7, 1.5, "AG alto → Δ/Δ\n<1 + hiperclorêmica | >2 + alcalose\nGap osmolar se suspeita tóxica", GR); arr(4.3, 2.65, 5.0, 2.65)
ax.set_title("Gasometria em 5 passos", color=GOLD, fontsize=14); save(fig, "img_acidobase.png")

# 11 Stevenson
fig, ax = plt.subplots(figsize=(7, 6)); ax.axis("off"); ax.set_xlim(0, 2); ax.set_ylim(0, 2)
q = [(0, 1, "A — Quente & Seco\nCompensado\nAjuste oral", GR), (1, 1, "B — Quente & Úmido\n(mais comum)\nDiurético + vasodilatador", AM),
     (0, 0, "L — Frio & Seco\nVolume cauteloso\n± inotrópico", CY), (1, 0, "C — Frio & Úmido\nPior prognóstico\nInotrópico ± diurético", RD)]
for x, y, t, c in q:
    ax.add_patch(Rectangle((x + .03, y + .03), .94, .94, fc="#161c24", ec=c, lw=3)); ax.text(x + .5, y + .5, t, ha="center", va="center", color=c, fontsize=11.5)
ax.text(.5, 2.03, "SECO (sem congestão)", ha="center", color=FG); ax.text(1.5, 2.03, "ÚMIDO (congesto)", ha="center", color=FG)
ax.text(-.05, 1.5, "QUENTE", rotation=90, va="center", ha="right", color=FG); ax.text(-.05, .5, "FRIO", rotation=90, va="center", ha="right", color=FG)
ax.set_title("Perfis de Stevenson — IC aguda\n", color=GOLD); save(fig, "img_stevenson.png")

# 12 Gamblegram
fig, ax = plt.subplots(figsize=(8, 4.8)); w = .6
def stack(x, parts):
    b = 0
    for v, lab, c in parts:
        ax.bar(x, v, w, bottom=b, color=c, edgecolor=BG); ax.text(x, b + v / 2, f"{lab}\n{v}", ha="center", va="center", fontsize=9.5, color="black" if c in (AM, GR, CY) else "white"); b += v
stack(0, [(140, "Na⁺", "#3b6ea8")]); stack(1, [(104, "Cl⁻", GR), (24, "HCO₃⁻", CY), (12, "AG", AM)])
stack(2.3, [(140, "Na⁺", "#3b6ea8")]); stack(3.3, [(104, "Cl⁻", GR), (10, "HCO₃⁻", CY), (26, "AG ↑", RD)])
ax.set_xticks([0.5, 2.8]); ax.set_xticklabels(["Normal (AG 12)", "Acidose de AG elevado (AG 26)"]); ax.set_ylabel("mEq/L")
ax.set_title("Gamblegram: o 'buraco' de ânions não medidos", color=GOLD); save(fig, "img_gamblegram.png")

# 13 M-mode
rng = np.random.default_rng(1); fig, axs = plt.subplots(1, 2, figsize=(10, 4))
for ax, tit, barcode in [(axs[0], "Sinal da PRAIA — normal", False), (axs[1], "Código de BARRAS — pneumotórax", True)]:
    H, Wd = 200, 300; img = np.zeros((H, Wd))
    rows = rng.random(80) * 0.8 + 0.2
    for i in range(80): img[i, :] = rows[i] * (0.5 + 0.5 * (i % 7 < 3))
    img[80:84, :] = 1.0
    if barcode:
        r2 = rng.random(H - 84) * 0.8 + 0.2
        for i in range(84, H): img[i, :] = r2[i - 84] * (0.4 + 0.6 * ((i // 3) % 2))
    else:
        img[84:, :] = rng.random((H - 84, Wd)) * 0.9
    ax.imshow(img, cmap="gray", aspect="auto"); ax.set_title(tit, color=GR if not barcode else RD); ax.axis("off")
    ax.text(5, 78, "linha pleural", color=AM, fontsize=9)
fig.suptitle("USG pulmonar — modo M (didático)", color=GOLD); save(fig, "img_mmode.png")
print(sorted(os.listdir("media")))
