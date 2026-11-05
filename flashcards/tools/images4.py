"""Ilustrações dos módulos 16 (Ventilação Mecânica) e 17 (USG POCUS)."""
import numpy as np, matplotlib, os
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, Ellipse, Polygon
os.makedirs("media", exist_ok=True)
BG, FG, GOLD, CY, RD, GR, AM, PU, MU = "#0e1116", "#e8e6df", "#d4af37", "#4dd4ff", "#ff6b6b", "#5be38a", "#ffc14d", "#b48cff", "#9aa4b2"
plt.rcParams.update({"figure.facecolor": BG, "axes.facecolor": BG, "text.color": FG, "axes.labelcolor": FG, "xtick.color": MU, "ytick.color": MU, "axes.edgecolor": "#3a4452", "font.size": 11})
def save(fig, n):
    if fig._suptitle is not None:
        try: fig.tight_layout(rect=(0, 0, 1, .88))
        except Exception: pass
    fig.savefig(f"media/{n}", dpi=110, bbox_inches="tight"); plt.close(fig)
def box(ax, x, y, w, h, t, c, fs=10):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08", fc="#161c24", ec=c, lw=2.2)); ax.text(x + w / 2, y + h / 2, t, ha="center", va="center", fontsize=fs, color=FG)
def arr(ax, x1, y1, x2, y2, lab="", c="#aaa"):
    ax.annotate("", (x2, y2), (x1, y1), arrowprops=dict(arrowstyle="->", color=c, lw=1.7))
    if lab: ax.text((x1 + x2) / 2 + .12, (y1 + y2) / 2, lab, fontsize=9.5, color=AM)
def clean(ax):
    for s in ("top", "right"): ax.spines[s].set_visible(False)

# ===================== VENTILAÇÃO =====================
# 1. VCV: pressão, fluxo, volume com pausa
t = np.linspace(0, 4, 800)
fig, axs = plt.subplots(3, 1, figsize=(9, 6.6), sharex=True)
P = np.where(t < 1, 5 + 30 * t / 1 * 0.6 + 12 * (t > 0.02), np.where(t < 1.4, 25, 5 + 20 * np.exp(-(t - 1.4) / .25)))
P = np.where(t < 1, 5 + 12 + 18 * t, P); P[t < .02] = 5
F = np.where(t < 1, 60, np.where(t < 1.4, 0, -80 * np.exp(-(t - 1.4) / .35)))
V = np.where(t < 1, 500 * t, np.where(t < 1.4, 500, 500 * np.exp(-(t - 1.4) / .35)))
for a, y, c, lab in zip(axs, (P, F, V), (AM, CY, GR), ("Pressão (cmH₂O)", "Fluxo (L/min)", "Volume (mL)")):
    a.plot(t, y, c, lw=2.4); a.set_ylabel(lab); clean(a); a.axhline(0, color="#333", lw=.8)
axs[0].annotate("P pico 35\n(resistiva + elástica)", (1, 35), (1.6, 33), color=RD, arrowprops=dict(arrowstyle="->", color=RD), fontsize=10)
axs[0].annotate("P platô 25\n(só elástica)", (1.2, 25), (2.2, 22), color=GOLD, arrowprops=dict(arrowstyle="->", color=GOLD), fontsize=10)
axs[0].axhline(5, color=PU, ls="--", lw=1); axs[0].text(3.3, 6.5, "PEEP 5", color=PU)
axs[0].text(0.05, 30, "ΔP = 25 − 5 = 20\nResist. = (35−25)/1 L/s = 10", fontsize=9.5, color=FG)
axs[1].text(1.05, 12, "pausa inspiratória\n(fluxo zero)", color=MU, fontsize=9)
axs[2].set_xlabel("Tempo (s)"); fig.suptitle("VCV com pausa inspiratória: as 3 curvas", color=GOLD, fontsize=14)
save(fig, "vm_vcv_curvas.png")

# 2. VCV x PCV comparação
fig, axs = plt.subplots(2, 2, figsize=(10, 5.4), sharex=True)
tt = np.linspace(0, 3, 600)
pv = np.where(tt < 1, 5 + 30 * tt, 5 + 30 * np.exp(-(tt - 1) / .2)); fv = np.where(tt < 1, 50, -70 * np.exp(-(tt - 1) / .35))
pp = np.where(tt < 1, 25, 5 + 20 * np.exp(-(tt - 1) / .08)); pp[tt < .03] = 5; fp = np.where(tt < 1, 90 * np.exp(-tt / .3), -70 * np.exp(-(tt - 1) / .35))
for a, y, c in ((axs[0, 0], pv, AM), (axs[1, 0], fv, CY), (axs[0, 1], pp, AM), (axs[1, 1], fp, CY)): a.plot(tt, y, c, lw=2.3); clean(a); a.axhline(0, color="#333", lw=.8)
axs[0, 0].set_title("VCV: fluxo e volume fixos\npressão = variável", color=FG, fontsize=11); axs[0, 1].set_title("PCV: pressão fixa\nfluxo desacelerado e volume = variáveis", color=FG, fontsize=11)
axs[0, 0].set_ylabel("Pressão"); axs[1, 0].set_ylabel("Fluxo")
fig.suptitle("Fluxo quadrado (VCV) × fluxo desacelerado (PCV)", color=GOLD, fontsize=14); save(fig, "vm_vcv_pcv.png")

# 3. Auto-PEEP
tt = np.linspace(0, 4.5, 900)
fig, ax = plt.subplots(figsize=(9.5, 3.8))
f = np.zeros_like(tt)
for s in (0, 1.5, 3):
    m = (tt >= s) & (tt < s + .5); f[m] = 60
    m2 = (tt >= s + .5) & (tt < s + 1.5); f[m2] = -90 * np.exp(-(tt[m2] - s - .5) / .7)
ax.plot(tt, f, CY, lw=2.3); ax.axhline(0, color=MU, lw=1); clean(ax)
for s in (1.5, 3): ax.annotate("fluxo NÃO zera\nantes do próximo ciclo", (s, f[np.searchsorted(tt, s) - 2]), (s - .2, -75), color=RD, fontsize=9.5, arrowprops=dict(arrowstyle="->", color=RD))
ax.set_ylabel("Fluxo (L/min)"); ax.set_xlabel("Tempo (s)")
ax.set_title("Auto-PEEP (hiperinsuflação dinâmica): confirme com pausa expiratória", color=GOLD); save(fig, "vm_autopeep.png")

# 4. Assincronias painel
fig, axs = plt.subplots(2, 2, figsize=(10.5, 6))
tt = np.linspace(0, 4, 800)
def base(a, title, c=CY):
    a.set_title(title, color=FG, fontsize=11); clean(a); a.set_yticks([]); a.axhline(0, color="#333", lw=.8)
# esforço ineficaz
a = axs[0, 0]; f = np.where(tt < .8, 50, np.where(tt < 2, -60 * np.exp(-(tt - .8) / .4), 0))
f += np.where((tt > 1.5) & (tt < 1.8), 18 * np.sin((tt - 1.5) / .3 * np.pi), 0)
a.plot(tt, f, CY, lw=2); base(a, "1) Esforço ineficaz (sem disparo)"); a.annotate("deflexão sem ciclo", (1.65, f[330]), (2.3, 30), color=RD, arrowprops=dict(arrowstyle="->", color=RD), fontsize=9)
# duplo disparo
a = axs[0, 1]; p = np.where(tt < .7, 20.0, np.where(tt < .8, 6.0, np.where(tt < 1.5, 20.0, 5.0))); p[tt < .05] = 5
a.plot(tt, p, AM, lw=2); base(a, "2) Duplo disparo (2 ciclos, 1 esforço)"); a.text(1.7, 15, "risco: VT empilhado\n(até 2× VT) → VILI", color=RD, fontsize=9)
# ciclagem precoce / tardia (PSV)
a = axs[1, 0]; f1 = np.where(tt < .5, 70 * np.exp(-tt / .6), np.where(tt < .7, 0, 0)); f1[(tt >= .5) & (tt < 1.6)] = -55 * np.exp(-(tt[(tt >= .5) & (tt < 1.6)] - .5) / .35)
f1 += np.where((tt > .55) & (tt < .8), 25, 0)
a.plot(tt, f1, CY, lw=2); base(a, "3) Ciclagem precoce: 'entalhe' expiratório"); a.text(1.6, 30, "esforço continua após\no ventilador ciclar", color=AM, fontsize=9)
a = axs[1, 1]; pt = np.where(tt < 1.4, 15.0, 5.0); pt += np.where((tt > 1.1) & (tt < 1.4), 6 * (tt - 1.1) / .3, 0); pt[tt < .05] = 5
a.plot(tt, pt, AM, lw=2); base(a, "4) Ciclagem tardia: pico no fim da inspiração"); a.text(1.7, 13, "paciente expira 'contra'\no ventilador (DPOC!)", color=AM, fontsize=9)
fig.suptitle("Assincronias paciente-ventilador: reconhecer na curva", color=GOLD, fontsize=14); save(fig, "vm_assincronias.png")

# 5. Driving pressure x mortalidade (ilustrativo)
fig, ax = plt.subplots(figsize=(8.5, 4.4))
dp = np.array([8, 11, 14, 17, 20, 23]); rr = np.array([.75, .9, 1.0, 1.25, 1.5, 1.8])
ax.plot(dp, rr, "-o", color=AM, lw=2.5); ax.axvline(15, color=RD, ls="--"); ax.text(15.3, 1.65, "ΔP > 15 cmH₂O\n= alvo de alerta", color=RD)
ax.set_xlabel("Driving pressure (Pplatô − PEEP), cmH₂O"); ax.set_ylabel("Risco relativo de morte\n(esquema)"); clean(ax)
ax.set_title("Driving pressure associa-se à mortalidade na SDRA (Amato 2015) — esquema", color=GOLD, fontsize=12); save(fig, "vm_driving.png")

# 6. Stress index
fig, axs = plt.subplots(1, 3, figsize=(10.5, 3.4), sharey=True)
x = np.linspace(0, 1, 100)
for a, y, t_, c in zip(axs, (x ** 1.6, x, x ** .6), ("SI > 1 (côncava ↑)\nhiperdistensão\n→ ↓ PEEP / VT", "SI = 1 (linear)\ncomplacência constante\n(ideal)", "SI < 1 (convexa)\nrecrutamento tidal\n→ considerar ↑ PEEP"), (RD, GR, AM)):
    a.plot(x, 5 + 25 * y, c, lw=3); a.set_title(t_, color=FG, fontsize=10); clean(a); a.set_xticks([])
axs[0].set_ylabel("Pressão (fluxo constante)"); fig.suptitle("Stress index: forma da curva pressão-tempo em VCV com fluxo quadrado", color=GOLD, fontsize=12)
save(fig, "vm_stress_index.png")

# 7. Curva PV com pontos de inflexão
fig, ax = plt.subplots(figsize=(7.5, 5))
p = np.linspace(0, 45, 300); v = 1500 / (1 + np.exp(-(p - 18) / 4.2))
ax.plot(p, v, CY, lw=3); clean(ax)
ax.plot(10.5, v[np.searchsorted(p, 10.5)], "o", color=AM, ms=10); ax.text(11.5, 150, "PII (inflexão inferior)\n→ recrutamento", color=AM, fontsize=10)
ax.plot(28, v[np.searchsorted(p, 28)], "o", color=RD, ms=10); ax.text(29, 1180, "PIS (inflexão superior)\n→ hiperdistensão", color=RD, fontsize=10)
ax.axvspan(11, 27, color=GR, alpha=.08); ax.text(14, 700, "zona segura\n(ventilar aqui)", color=GR)
ax.set_xlabel("Pressão (cmH₂O)"); ax.set_ylabel("Volume (mL)"); ax.set_title("Curva pressão-volume estática (SDRA)", color=GOLD); save(fig, "vm_pv_inflexao.png")

# 8. Desmame fluxograma
fig, ax = plt.subplots(figsize=(10, 6.2)); ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 10)
box(ax, 2.5, 8.6, 5, 1.1, "Triagem diária: causa resolvendo? FiO₂ ≤ 0,4–0,5, PEEP ≤ 8,\nestável (vasopressor baixo), desperto/RASS 0 a −1", CY, 9.5)
box(ax, 3, 6.6, 4, 1.0, "TRE 30–120 min\nPSV 5–8 / PEEP 0–5 ou tubo T", AM)
box(ax, .2, 4.2, 4, 1.4, "Falhou: FR > 35, SpO₂ < 90%,\nFC > 140, PAS > 180 ou < 90,\nagitação, sudorese, uso acessório", RD, 9)
box(ax, 5.8, 4.2, 4, 1.4, "Passou → avaliar via aérea:\ntosse, secreção, nível de\nconsciência, teste de vazamento", GR, 9)
box(ax, .2, 1.4, 4, 1.6, "Volta à VM confortável (24 h)\nprocurar causa: cardíaca, fraqueza,\nsobrecarga, delirium, nutrição", MU, 9)
box(ax, 5.8, 1.4, 4, 1.6, "EXTUBAR → alto risco:\nCNAF ou VNI preventiva\n(> 65 a, IC, DPOC, hipercapnia)", GOLD, 9)
arr(ax, 5, 8.6, 5, 7.6); arr(ax, 4, 6.6, 2.5, 5.6, "não"); arr(ax, 6, 6.6, 7.5, 5.6, "sim"); arr(ax, 2.2, 4.2, 2.2, 3.0); arr(ax, 7.8, 4.2, 7.8, 3.0)
ax.set_title("Do teste de respiração espontânea (TRE) à extubação", color=GOLD, fontsize=14); save(fig, "vm_desmame.png")

# 9. Tabela PEEP/FiO2 ARDSNet visual
fig, ax = plt.subplots(figsize=(10, 3.6)); ax.axis("off")
fio2 = [.3, .4, .4, .5, .5, .6, .7, .7, .7, .8, .9, .9, .9, 1.0]
peep = [5, 5, 8, 8, 10, 10, 10, 12, 14, 14, 14, 16, 18, "18–24"]
tab = ax.table(cellText=[[f"{x:.1f}" for x in fio2], [str(p) for p in peep]], rowLabels=["FiO₂", "PEEP"], loc="center", cellLoc="center")
tab.auto_set_font_size(False); tab.set_fontsize(11); tab.scale(1, 2.2)
for (r, c), cell in tab.get_celld().items():
    cell.set_edgecolor("#3a4452"); cell.set_facecolor("#161c24" if r else "#1d2633"); cell.get_text().set_color(AM if r == 1 else FG)
ax.set_title("ARDSNet — tabela PEEP baixa / FiO₂ (alvo PaO₂ 55–80 ou SpO₂ 88–95%)", color=GOLD, fontsize=13); save(fig, "vm_peep_tabela.png")

# 10. Equação do movimento / componentes de pressão
fig, ax = plt.subplots(figsize=(9.5, 4.2)); ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 5)
ax.text(5, 4.3, "Pva + Pmus = (VT / C) + (Fluxo × R) + PEEP total", ha="center", fontsize=16, color=GOLD)
for x, t_, c in ((1.3, "Pressão elástica\nVT / Complacência\n→ PLATÔ", AM), (5, "Pressão resistiva\nFluxo × Resistência\n→ PICO − PLATÔ", CY), (8.7, "PEEP total\nPEEP externa + auto-PEEP\n→ PAUSA EXPIRATÓRIA", PU)):
    box(ax, x - 1.4, .8, 2.8, 2.2, t_, c, 10.5)
ax.text(5, .2, "Csr = VT / (Pplatô − PEEPtotal) · normal ≈ 50–80 mL/cmH₂O no paciente intubado", ha="center", fontsize=10, color=MU)
save(fig, "vm_equacao.png")

# 11. Pressão esofágica / transpulmonar
fig, ax = plt.subplots(figsize=(9, 4.4)); ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 6)
ax.add_patch(Ellipse((3, 3), 3.4, 4.2, fc="#1b2533", ec=CY, lw=2.5)); ax.text(3, 3, "Pulmão\nPalv", ha="center", va="center", color=CY, fontsize=12)
ax.add_patch(Ellipse((3, 3), 4.6, 5.4, fc="none", ec=AM, lw=2.5, ls="--")); ax.text(3, .05, "Parede / pleura → Pes ≈ Ppl", ha="center", color=AM)
ax.text(6.2, 4.4, "P transpulmonar (PL) = Palv − Ppl", color=GOLD, fontsize=13)
ax.text(6.2, 3.4, "• PL expiratória ≥ 0 → evita colapso\n  (ajustar PEEP: EPVent)", color=FG, fontsize=10.5)
ax.text(6.2, 2.1, "• PL inspiratória (platô) < 20–25\n  → evita hiperdistensão", color=FG, fontsize=10.5)
ax.text(6.2, .9, "• Útil: obesos, abdome tenso,\n  parede rígida", color=FG, fontsize=10.5)
ax.set_title("Pressão esofágica e transpulmonar", color=GOLD, fontsize=14); save(fig, "vm_transpulmonar.png")

# 12. Capnografia: normal x broncoespasmo x reinalação
fig, axs = plt.subplots(1, 3, figsize=(10.5, 3.2), sharey=True)
x = np.linspace(0, 3, 600)
def cap(shape):
    y = np.zeros_like(x)
    for s in (0, 1.5):
        m = (x >= s) & (x < s + 1)
        u = (x[m] - s)
        y[m] = np.clip(40 * (1 - np.exp(-u / .06)), 0, 40) if shape == "n" else (40 * u / 1 if shape == "b" else 40 * (1 - np.exp(-u / .06)))
        if shape == "b": y[m] = 38 * (1 - np.exp(-u / .45))
    if shape == "r": y = y + 8
    return y
for a, s, t_, c in zip(axs, "nbr", ("Normal: platô alveolar\nretangular", "Broncoespasmo:\n'barbatana de tubarão'", "Reinalação:\nlinha de base ↑"), (GR, AM, RD)):
    a.plot(x, cap(s), c, lw=2.5); a.set_title(t_, color=FG, fontsize=10); clean(a); a.set_xticks([])
axs[0].set_ylabel("EtCO₂ (mmHg)"); fig.suptitle("Capnografia na VM", color=GOLD, fontsize=13); save(fig, "vm_capnografia.png")

# 13. VNI / CNAF indicações (quadro)
fig, ax = plt.subplots(figsize=(10, 4.6)); ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 6)
box(ax, .2, 3.2, 3, 2.4, "VNI — benefício forte\n• DPOC exacerbado\n  (pH 7,25–7,35)\n• EAP cardiogênico", GR, 10)
box(ax, 3.5, 3.2, 3, 2.4, "CNAF — benefício\n• IRpA hipoxêmica\n  (FLORALI)\n• pós-extubação\n  baixo risco", CY, 10)
box(ax, 6.8, 3.2, 3, 2.4, "Cuidado / evitar\n• rebaixamento, vômitos\n• instabilidade grave\n• secreção abundante\n• trauma de face", RD, 9.5)
box(ax, .2, .3, 9.6, 2.2, "Reavaliar em 1–2 h: sem melhora (pH, FR, trabalho respiratório) → intubar sem atraso\nÍndice HACOR > 5 em 1 h (VNI) e ROX < 3,85 em 12 h (CNAF) → alto risco de falha", AM, 10.5)
ax.set_title("Suporte não invasivo: quem se beneficia", color=GOLD, fontsize=14); save(fig, "vm_vni_cnaf.png")

# ===================== POCUS =====================
# 14. Protocolo BLUE
fig, ax = plt.subplots(figsize=(10.5, 6.4)); ax.axis("off"); ax.set_xlim(0, 12); ax.set_ylim(0, 10)
box(ax, 4, 8.7, 4, 1, "Deslizamento pleural?", CY)
box(ax, .3, 6.6, 3.6, 1.2, "SIM + perfil A\n(linhas A bilaterais)", GR, 9.5); box(ax, 4.2, 6.6, 3.6, 1.2, "SIM + perfil B\n(B difusas bilaterais)", AM, 9.5); box(ax, 8.1, 6.6, 3.6, 1.2, "NÃO + perfil A'\n→ procurar lung point", RD, 9.5)
box(ax, .3, 4.3, 3.6, 1.4, "Doppler venoso\nTVP + → TEP\nTVP − → PLAPS?", GR, 9.5); box(ax, 4.2, 4.3, 3.6, 1.4, "EAP hemodinâmico\n(congestão)", AM, 9.5); box(ax, 8.1, 4.3, 3.6, 1.4, "Lung point + →\nPNEUMOTÓRAX", RD, 9.5)
box(ax, .3, 1.6, 3.6, 1.6, "PLAPS + → pneumonia\nA sem PLAPS →\nDPOC / asma", PU, 9.5); box(ax, 4.2, 1.6, 3.6, 1.6, "Perfil A/B ou C\n(consolidação anterior)\n→ pneumonia", PU, 9.5); box(ax, 8.1, 1.6, 3.6, 1.6, "Perfil B' (B sem\ndeslizamento)\n→ pneumonia", PU, 9.5)
for x in (2.1, 6, 9.9): arr(ax, 6, 8.7, x, 7.8); arr(ax, x, 6.6, x, 5.7); arr(ax, x, 4.3, x, 3.2)
ax.set_title("Protocolo BLUE (Lichtenstein): ~90% de acurácia na dispneia aguda", color=GOLD, fontsize=13); save(fig, "pc_blue.png")

# 15. Linhas A x B + modo M
fig, axs = plt.subplots(1, 4, figsize=(12, 3.8))
for a in axs: a.set_xlim(0, 10); a.set_ylim(0, 10); a.set_xticks([]); a.set_yticks([]); a.set_facecolor("#050607")
a = axs[0]; a.add_patch(Rectangle((0, 8.3), 10, .5, color="#ddd")); [a.axhline(y, color="#bbb", lw=3, alpha=.7) for y in (5.6, 2.9)]
for x in (1.2, 8.8): a.add_patch(Rectangle((x - .5, 8.8), 1, 1.2, color="#777"))
a.set_title("Linhas A (reverberação)\nar normal ou PNTX", color=GR, fontsize=10)
a = axs[1]; a.add_patch(Rectangle((0, 8.3), 10, .5, color="#ddd")); [a.add_patch(Polygon([[x - .15, 8.3], [x + .15, 8.3], [x + .35, 0], [x - .35, 0]], color="#ddd", alpha=.85)) for x in (2.5, 5, 7.5)]
a.set_title("Linhas B (cauda de cometa)\n≥ 3 por campo = síndrome intersticial", color=AM, fontsize=10)
a = axs[2]; a.add_patch(Rectangle((0, 6), 10, 4, color="#666")); a.axhline(6, color="#eee", lw=3); a.imshow(np.random.rand(60, 100), extent=(0, 10, 0, 6), cmap="gray", aspect="auto", alpha=.85)
a.set_title("Modo M: 'praia' (seashore)\n= pulmão deslizando", color=GR, fontsize=10)
a = axs[3]; [a.axhline(y, color="#ccc", lw=2) for y in np.linspace(.3, 9.7, 20)]; a.set_title("Modo M: 'código de barras'\n(estratosfera) = sem deslizamento", color=RD, fontsize=10)
fig.suptitle("Artefatos do pulmão: o que cada padrão significa", color=GOLD, fontsize=13); save(fig, "pc_linhas_ab.png")

# 16. LUS score
fig, axs = plt.subplots(1, 4, figsize=(12, 3.4))
lab = ("0 · Linhas A\n(normal)", "1 · ≥ 3 linhas B\nespaçadas", "2 · B coalescentes\n(pulmão branco)", "3 · Consolidação\n(hepatização)")
for i, a in enumerate(axs):
    a.set_xlim(0, 10); a.set_ylim(0, 10); a.set_xticks([]); a.set_yticks([]); a.set_facecolor("#050607"); a.add_patch(Rectangle((0, 8.3), 10, .5, color="#ddd"))
    if i == 0: [a.axhline(y, color="#bbb", lw=3, alpha=.7) for y in (5.6, 2.9)]
    if i == 1: [a.add_patch(Polygon([[x - .12, 8.3], [x + .12, 8.3], [x + .3, 0], [x - .3, 0]], color="#ddd", alpha=.8)) for x in (2, 5, 8)]
    if i == 2: a.add_patch(Rectangle((.5, 0), 9, 8.3, color="#cfcfcf", alpha=.75))
    if i == 3: a.imshow(np.random.rand(40, 60) * .6 + .2, extent=(0, 10, 0, 8.3), cmap="gray", aspect="auto"); [a.plot([2, 3, 4.5], [y, y - 1, y - .5], color="#fff", lw=2) for y in (6, 3.5)]
    a.set_title(lab[i], color=(GR, AM, "#ff9b4d", RD)[i], fontsize=10)
fig.suptitle("LUS score: 12 regiões × 0–3 pontos (0–36) · aeração pulmonar", color=GOLD, fontsize=13); save(fig, "pc_lus_score.png")

# 17. Janelas cardíacas no tórax
fig, ax = plt.subplots(figsize=(7.6, 7)); ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 10)
ax.add_patch(FancyBboxPatch((2, 1), 6, 8, boxstyle="round,pad=0.3", fc="#141a22", ec="#555", lw=2)); ax.add_patch(Ellipse((5.6, 5.4), 2.4, 2.8, fc="#4a1f26", ec=RD, lw=2)); ax.text(5.6, 5.4, "VE", ha="center", va="center", fontsize=26, color=RD)
pts = [(4.0, 6.7, "1 Paraesternal\neixos longo/curto", CY, (0.3, 7.4)), (6.9, 4.4, "2 Apical\n4 câmaras", GR, (8.1, 4.0)), (5.0, 2.3, "3 Subcostal\n4C + VCI", AM, (6.0, 1.3)), (5.0, 8.6, "4 Supraesternal\n(arco aórtico)", PU, (6.0, 9.2))]
for x, y, t_, c, (tx, ty) in pts:
    ax.add_patch(Rectangle((x - .3, y - .15), .6, .3, color=c)); ax.text(tx, ty, t_, color=c, fontsize=10.5)
ax.text(.3, 4.5, "Marcador:\nPEL → ombro D\nPEC → ombro E\nA4C → axila E\n(convenção cardiológica)", fontsize=9, color=MU)
ax.set_title("Janelas do ecocardiograma focado", color=GOLD, fontsize=14); save(fig, "pc_janelas.png")

# 18. VD dilatado e sinal do D
fig, axs = plt.subplots(1, 2, figsize=(10, 4.4))
for a in axs: a.set_xlim(0, 10); a.set_ylim(0, 10); a.axis("off"); a.set_facecolor("#050607")
a = axs[0]; a.add_patch(Circle((6, 5), 2.6, fc="none", ec=GR, lw=3)); a.add_patch(Ellipse((2.8, 5), 2.2, 4.6, fc="none", ec=CY, lw=3)); a.text(6, 5, "VE", ha="center", color=GR, fontsize=14); a.text(2.8, 5, "VD", ha="center", color=CY, fontsize=12)
a.set_title("Normal: VE em 'O'\nVD/VE < 0,6", color=GR, fontsize=11)
a = axs[1]; th = np.linspace(-1.1, 1.1, 50); a.plot(6.5 + 2.4 * np.cos(np.linspace(-1.9, 1.9, 60)), 5 + 2.4 * np.sin(np.linspace(-1.9, 1.9, 60)), GR, lw=3); a.plot([5.7, 5.7], [2.7, 7.3], GR, lw=3)
a.add_patch(Ellipse((3.3, 5), 4.2, 6, fc="none", ec=RD, lw=3)); a.text(6.9, 5, "VE\n'D'", ha="center", color=GR, fontsize=13); a.text(3.3, 5, "VD\ndilatado", ha="center", color=RD, fontsize=12)
a.set_title("Sobrecarga de VD: 'sinal do D'\nVD/VE ≥ 1 → TEP / HP", color=RD, fontsize=11)
fig.suptitle("Paraesternal eixo curto: forma do VE conta a pressão do VD", color=GOLD, fontsize=13); save(fig, "pc_vd_dsign.png")

# 19. VCI
fig, ax = plt.subplots(figsize=(9.5, 4.2)); ax.axis("off")
rows = [["Diâmetro VCI", "Colapso inspiratório\n(ventilação espontânea)", "PAD estimada"], ["≤ 2,1 cm", "> 50%", "3 mmHg (0–5)"], ["≤ 2,1 cm", "< 50%", "8 mmHg (5–10)"], ["> 2,1 cm", "> 50%", "8 mmHg (5–10)"], ["> 2,1 cm", "< 50%", "15 mmHg (10–20)"]]
tab = ax.table(cellText=rows[1:], colLabels=rows[0], loc="center", cellLoc="center"); tab.auto_set_font_size(False); tab.set_fontsize(11.5); tab.scale(1, 2.3)
for (r, c), cell in tab.get_celld().items():
    cell.set_edgecolor("#3a4452"); cell.set_facecolor("#1d2633" if r == 0 else "#161c24"); cell.get_text().set_color(GOLD if r == 0 else (GR if r == 1 else RD if r == 4 else FG))
ax.set_title("VCI → pressão de átrio direito (ASE 2015) · medir 1–2 cm da junção com o AD", color=GOLD, fontsize=12); save(fig, "pc_vci.png")

# 20. VExUS
fig, axs = plt.subplots(3, 3, figsize=(11, 6.4), sharex=True)
x = np.linspace(0, 2, 400)
hv = [(-np.abs(np.sin(np.pi * x * 2)) * 30 - 5 + 10 * (np.sin(np.pi * x * 2) > .95)), (-25 * np.clip(np.sin(np.pi * x * 2 + .8), 0, 1) - 8 * np.clip(np.sin(np.pi * x * 2), 0, 1) - 3), (25 * np.clip(np.sin(np.pi * x * 2 + .8), 0, 1) - 22 * np.clip(np.sin(np.pi * x * 2), 0, 1))]
pv_ = [12 + 1 * np.sin(np.pi * x * 2), 14 + 6 * np.sin(np.pi * x * 2), 14 + 16 * np.sin(np.pi * x * 2)]
rv = [np.where(np.sin(np.pi * x * 2) > 0, 0, -10 - 3 * np.sin(np.pi * x * 4)), np.where((np.sin(np.pi * x * 2) > .3), 0, -12) * 1.0, np.where(np.sin(np.pi * x * 2) > -.2, 0, -14)]
titles = ("Normal", "Leve alteração", "Grave")
for j in range(3):
    for i, (ys, nm, c) in enumerate(((hv, "Veia hepática", CY), (pv_, "Veia porta", AM), (rv, "Venosa intrarrenal", PU))):
        a = axs[i, j]; a.plot(x, ys[j], c, lw=2); a.axhline(0, color="#444", lw=.8); clean(a); a.set_yticks([])
        if j == 0: a.set_ylabel(nm, fontsize=9.5)
        if i == 0: a.set_title(titles[j], color=(GR, AM, RD)[j])
axs[0, 0].text(.05, 8, "S > D", fontsize=9, color=FG); axs[0, 1].text(.05, 5, "S < D", fontsize=9, color=FG); axs[0, 2].text(.05, 18, "S reverso", fontsize=9, color=FG)
axs[1, 0].text(.05, 15, "pulsat. < 30%", fontsize=9, color=FG); axs[1, 1].text(.05, 21, "30–49%", fontsize=9, color=FG); axs[1, 2].text(.05, 32, "≥ 50%", fontsize=9, color=FG)
axs[2, 0].text(.05, 3, "contínuo", fontsize=9, color=FG); axs[2, 1].text(.05, 3, "bifásico", fontsize=9, color=FG); axs[2, 2].text(.05, 3, "monofásico (só D)", fontsize=9, color=FG)
fig.suptitle("VExUS: VCI > 2 cm + Doppler de 3 veias = graduação da congestão venosa (0–3)", color=GOLD, fontsize=12.5); save(fig, "pc_vexus.png")

# 21. VTI
fig, ax = plt.subplots(figsize=(9.5, 4))
x = np.linspace(0, 3, 600); y = np.zeros_like(x)
for s in (.2, 1.2, 2.2): m = (x >= s) & (x < s + .32); y[m] = -110 * np.sin((x[m] - s) / .32 * np.pi)
ax.fill_between(x, y, 0, where=(x >= 1.2) & (x < 1.52), color=CY, alpha=.4); ax.plot(x, y, CY, lw=2.3); ax.axhline(0, color=MU, lw=1); clean(ax)
ax.text(1.55, -80, "VTI = área sob a curva\n(cm) · normal 18–22 cm", color=GOLD, fontsize=11)
ax.text(.0, 20, "Doppler pulsado na VSVE (apical 5C), amostra 0,5 cm abaixo da valva aórtica", color=FG, fontsize=10)
ax.set_ylabel("Velocidade (cm/s)"); ax.set_xlabel("Tempo (s)")
ax.set_title("VTI: 'volume sistólico em centímetros' · VS = VTI × área VSVE (π·r²) · ΔVTI ≥ 10–15% após EPP = responsivo", color=GOLD, fontsize=10.5); save(fig, "pc_vti.png")

# 22. eFAST
fig, ax = plt.subplots(figsize=(7.5, 7.5)); ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 10)
ax.add_patch(FancyBboxPatch((2.4, .6), 5.2, 8.6, boxstyle="round,pad=0.4", fc="#141a22", ec="#555", lw=2))
pts = [(5, 5.9, "1 Subxifoide\n(pericárdio)", RD, (7.9, 6.3)), (6.9, 4.1, "2 QSE\n(esplenorrenal)", AM, (7.9, 3.8)), (3.1, 4.1, "3 QSD — Morison\n(mais sensível)", GOLD, (.0, 3.8)), (5, 1.4, "4 Pelve\n(Douglas / retovesical)", PU, (6.4, .5)), (3.6, 8.0, "5 Tórax ant.\n(PNTX)", CY, (.0, 8.3)), (6.4, 8.0, "", CY, (0, 0)), (2.9, 6.6, "6 Recessos costofrênicos\n(hemotórax)", GR, (.0, 6.5)), (7.1, 6.6, "", GR, (0, 0))]
for x, y, t_, c, (tx, ty) in pts:
    ax.add_patch(Circle((x, y), .28, color=c))
    if t_: ax.text(tx, ty, t_, color=c, fontsize=10)
ax.set_title("eFAST: 6 janelas no trauma", color=GOLD, fontsize=14); save(fig, "pc_efast.png")

# 23. TVP compressão
fig, axs = plt.subplots(1, 2, figsize=(9.5, 3.8))
for a in axs: a.set_xlim(0, 10); a.set_ylim(0, 10); a.axis("off")
a = axs[0]; a.add_patch(Circle((3, 5), 1.4, fc="#123", ec=RD, lw=3)); a.add_patch(Circle((6.4, 5), 1.7, fc="#0b1a2c", ec=CY, lw=3)); a.text(3, 5, "A", ha="center", color=RD, fontsize=14); a.text(6.4, 5, "V", ha="center", color=CY, fontsize=14)
a.set_title("Sem compressão", color=FG)
a = axs[1]; a.add_patch(Circle((3, 4.4), 1.4, fc="#123", ec=RD, lw=3)); a.add_patch(Ellipse((6.4, 4.4), 3.4, .25, fc="#0b1a2c", ec=GR, lw=3)); a.text(3, 4.4, "A", ha="center", color=RD, fontsize=14)
a.text(5, 7.5, "veia colapsa totalmente = sem TVP\nnão colapsa = TVP", ha="center", color=GOLD, fontsize=11)
fig.suptitle("Compressão em 2 pontos (femoral comum + poplítea): veia que não colaba = trombo", color=GOLD, fontsize=12); save(fig, "pc_tvp.png")

# 24. Diafragma
fig, axs = plt.subplots(1, 2, figsize=(10.5, 3.8))
x = np.linspace(0, 6, 600)
a = axs[0]; a.plot(x, 1.8 * np.clip(np.sin(x * 1.3), 0, None), AM, lw=2.5); a.annotate("", (1.2, 1.8), (1.2, 0), arrowprops=dict(arrowstyle="<->", color=GR)); a.text(1.35, .8, "excursão\n(DE)", color=GR); clean(a)
a.set_title("Modo M subcostal: excursão diafragmática\nnormal ≳ 1,5–1,8 cm · < 1 cm = disfunção", color=FG, fontsize=10); a.set_ylabel("cm"); a.set_xticks([])
a = axs[1]; a.set_xlim(0, 10); a.set_ylim(0, 10); a.axis("off")
a.add_patch(Rectangle((1, 4.5), 3, 1.0, color=AM)); a.text(2.5, 3.6, "expiração\nTee 2,0 mm", ha="center", color=FG)
a.add_patch(Rectangle((6, 4.2), 3, 1.6, color=AM)); a.text(7.5, 3.3, "inspiração\nTei 2,8 mm", ha="center", color=FG)
a.text(5, 8, "FE = (Tei − Tee)/Tee = 40%\n< 30% → risco de falha no desmame", ha="center", color=GOLD, fontsize=11)
a.set_title("Zona de aposição: fração de espessamento", color=FG, fontsize=10)
fig.suptitle("Ultrassom do diafragma", color=GOLD, fontsize=13); save(fig, "pc_diafragma.png")

# 25. RUSH
fig, ax = plt.subplots(figsize=(10.5, 4.8)); ax.axis("off")
rows = [["", "Hipovolêmico", "Cardiogênico", "Obstrutivo", "Distributivo"],
        ["BOMBA", "hiperdinâmico,\ncavidades pequenas", "hipocinético,\nVE dilatado", "derrame c/ tamponamento,\nVD dilatado (TEP)", "hiperdinâmico (inicial)"],
        ["TANQUE", "VCI fina, colapsável;\nFAST + / derrame", "VCI pletórica;\nlinhas B; derrame", "VCI pletórica;\nPNTX (sem deslizamento)", "VCI normal/fina;\nfoco (pneumonia, ascite)"],
        ["CANOS", "aneurisma roto /\ndissecção", "normal", "TVP", "normal"]]
tab = ax.table(cellText=rows[1:], colLabels=rows[0], loc="center", cellLoc="center"); tab.auto_set_font_size(False); tab.set_fontsize(9.5); tab.scale(1, 3.2)
for (r, c), cell in tab.get_celld().items():
    cell.set_edgecolor("#3a4452"); cell.set_facecolor("#1d2633" if r == 0 or c == 0 else "#161c24"); cell.get_text().set_color(GOLD if r == 0 or c == 0 else FG)
ax.set_title("Protocolo RUSH: Bomba · Tanque · Canos", color=GOLD, fontsize=14); save(fig, "pc_rush.png")

# 26. Física: frequência x penetração
fig, ax = plt.subplots(figsize=(9, 4))
f = np.array([2, 3.5, 5, 7.5, 10, 12, 15]); pen = 30 / f
ax.plot(f, pen, "-o", color=CY, lw=2.5); clean(ax); ax.set_xlabel("Frequência (MHz)"); ax.set_ylabel("Penetração aprox. (cm)")
for x_, y_, t_ in ((2.5, 13, "Setorial / convexo\n(2–5 MHz): coração, abdome"), (9.5, 5.5, "Linear (7–15 MHz):\nvasos, pleura, nervo")): ax.text(x_, y_, t_, color=AM)
ax.set_title("↑ frequência = ↑ resolução, ↓ penetração", color=GOLD, fontsize=13); save(fig, "pc_fisica.png")

# 27. Tamponamento
fig, ax = plt.subplots(figsize=(10, 4.6)); ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 6)
items = [("1", "Derrame pericárdico\n(circunferencial)", CY), ("2", "Colapso sistólico do AD\n(> 1/3 do ciclo)", AM), ("3", "Colapso diastólico do VD\n(mais específico)", RD), ("4", "VCI pletórica\n> 2,1 cm, < 50% colapso", PU), ("5", "Variação respiratória\nE mitral > 25%\nE tricúspide > 40%", GR)]
for i, (n, t_, c) in enumerate(items):
    x = .1 + i * 2
    ax.add_patch(FancyBboxPatch((x, 1.2), 1.8, 3.2, boxstyle="round,pad=0.06", fc="#161c24", ec=c, lw=2.3)); ax.text(x + .9, 3.8, n, ha="center", color=c, fontsize=20, weight="bold"); ax.text(x + .9, 2.3, t_, ha="center", va="center", fontsize=8.8, color=FG)
ax.text(5, .4, "Tamponamento é diagnóstico CLÍNICO-ecográfico: hipotensão + achados → pericardiocentese guiada", ha="center", color=MU, fontsize=10)
ax.set_title("Sinais ecográficos de tamponamento cardíaco", color=GOLD, fontsize=14); save(fig, "pc_tamponamento.png")

# 28. Derrame pleural — Balik
fig, ax = plt.subplots(figsize=(8.5, 4.4)); ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 6)
ax.add_patch(Rectangle((1, 4.5), 7, .3, color="#ddd")); ax.text(8.2, 4.55, "pleura parietal", color=MU, fontsize=9)
ax.add_patch(Polygon([[1, 4.5], [8, 4.5], [7, 1], [2, 1]], color="#050607")); ax.text(4.5, 3.4, "líquido anecoico", ha="center", color=CY)
ax.add_patch(Ellipse((4.5, .8), 6, 1.2, color="#666")); ax.text(4.5, .7, "pulmão (base)", ha="center", color=FG, fontsize=9)
ax.annotate("", (4.5, 1.4), (4.5, 4.5), arrowprops=dict(arrowstyle="<->", color=AM, lw=2)); ax.text(4.7, 2.5, "Sep (mm)", color=AM)
ax.text(9.9, 2.6, "Balik:\nVolume (mL) ≈ 20 × Sep\n(supino, fim de expiração,\nlinha axilar posterior)\nEx.: 45 mm ≈ 900 mL", ha="right", color=GOLD, fontsize=10.5)
ax.set_title("Estimativa do volume do derrame pleural", color=GOLD, fontsize=13); save(fig, "pc_derrame.png")

# 29. ONSD
fig, ax = plt.subplots(figsize=(8, 4.6)); ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 7)
ax.add_patch(Circle((5, 4.8), 2, fc="#050607", ec="#888", lw=2)); ax.add_patch(Rectangle((4.5, 0), 1, 2.85, fc="#333", ec="#888"))
ax.annotate("", (5, 2.8), (5, 2.0), arrowprops=dict(arrowstyle="<->", color=AM)); ax.text(5.2, 2.35, "3 mm atrás do globo", color=AM, fontsize=9)
ax.annotate("", (4.5, 1.6), (5.5, 1.6), arrowprops=dict(arrowstyle="<->", color=RD, lw=2)); ax.text(5.7, 1.4, "DBNO", color=RD)
ax.text(.2, 6.3, "DBNO > 5,0–5,8 mm → sugere HIC (> 20 mmHg)\nlinear alta frequência, pálpebra fechada, gel abundante,\npotência acústica reduzida (ALARA)", color=GOLD, fontsize=10)
ax.set_title("Diâmetro da bainha do nervo óptico (DBNO)", color=GOLD, fontsize=13); save(fig, "pc_onsd.png")
print("ok", len([f for f in os.listdir("media") if f.startswith(("vm_", "pc_"))]))
