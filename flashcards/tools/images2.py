import numpy as np, matplotlib, os
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Polygon
os.makedirs("media", exist_ok=True)
BG, FG, GOLD, CY, RD, GR, AM, PU = "#0e1116", "#e8e6df", "#d4af37", "#4dd4ff", "#ff6b6b", "#5be38a", "#ffc14d", "#b48cff"
plt.rcParams.update({"figure.facecolor": BG, "axes.facecolor": BG, "axes.edgecolor": "#555", "text.color": FG,
    "axes.labelcolor": FG, "xtick.color": "#aaa", "ytick.color": "#aaa", "font.size": 12, "axes.titleweight": "bold"})
def save(fig, n):
    if fig._suptitle is not None: fig._suptitle.set_y(1.04)
    fig.savefig(f"media/{n}", dpi=110, bbox_inches="tight"); plt.close(fig)
def flow(ax, boxes, arrows, title):
    ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 10)
    for (x, y, w, h, t, c) in boxes:
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1", fc="#161c24", ec=c, lw=2.2))
        ax.text(x + w / 2, y + h / 2, t, ha="center", va="center", fontsize=10.5, color=FG)
    for (x1, y1, x2, y2, lab) in arrows:
        ax.annotate("", (x2, y2), (x1, y1), arrowprops=dict(arrowstyle="->", color="#aaa", lw=1.6))
        if lab: ax.text((x1 + x2) / 2 + .1, (y1 + y2) / 2, lab, fontsize=9.5, color=AM)
    ax.set_title(title, color=GOLD, fontsize=14)

# 1 PK/PD
fig, ax = plt.subplots(figsize=(8, 4.4)); t = np.linspace(0, 12, 400)
c = 40 * (np.exp(-0.35 * t) - np.exp(-3 * t)); mic = 6
ax.plot(t, c, color=CY, lw=3); ax.axhline(mic, color=RD, ls="--"); ax.text(10.2, mic + .8, "MIC", color=RD)
ax.fill_between(t, 0, c, where=c > 0, color=GOLD, alpha=.12)
above = t[c > mic]; ax.annotate("", (above[-1], mic - 2), (above[0], mic - 2), arrowprops=dict(arrowstyle="<->", color=GR))
ax.text((above[0] + above[-1]) / 2 - 1.5, mic - 4.8, "fT > MIC (betalactâmicos)", color=GR)
pk = t[np.argmax(c)]; ax.annotate("Cmáx/MIC (aminoglicosídeos)", (pk, c.max()), (pk + 1.5, c.max() + 2), color=AM, arrowprops=dict(arrowstyle="->", color=AM))
ax.text(6.5, 16, "AUC/MIC (vancomicina,\nquinolonas) = área dourada", color=GOLD, fontsize=10.5)
ax.set_xlabel("tempo (h)"); ax.set_ylabel("concentração"); ax.set_ylim(-6, 32); ax.set_title("Parâmetros PK/PD dos antimicrobianos", color=GOLD)
save(fig, "img_pk_pd.png")

# 2 Rumack-Matthew
fig, ax = plt.subplots(figsize=(7.5, 4.6)); h = np.linspace(4, 24, 200)
for c0, col, lab in [(150, AM, "Linha de tratamento (EUA) 150 mcg/mL em 4 h"), (200, RD, "Linha original 200 mcg/mL em 4 h")]:
    ax.plot(h, c0 * 0.5 ** ((h - 4) / 4), color=col, lw=2.6, label=lab)
ax.set_yscale("log"); ax.set_xlabel("horas após ingestão (única, aguda)"); ax.set_ylabel("paracetamol sérico (mcg/mL)")
ax.fill_between(h, 150 * 0.5 ** ((h - 4) / 4), 1000, color=RD, alpha=.08); ax.text(14, 120, "Acima da linha → N-acetilcisteína", color=RD)
ax.legend(facecolor=BG, edgecolor="#555", labelcolor=FG, fontsize=9.5); ax.set_ylim(4, 1000)
ax.set_title("Nomograma de Rumack-Matthew (meia-vida ~4 h)", color=GOLD); save(fig, "img_rumack.png")

# 3 Hipercalemia flow
fig, ax = plt.subplots(figsize=(9, 6))
flow(ax, [(3, 8.5, 4, 1.1, "K⁺ ≥ 6,5 ou alteração no ECG?", GOLD),
          (0.2, 6.1, 3, 1.4, "1  ESTABILIZAR\nGluconato de Ca 10%\n10–30 mL IV", RD),
          (3.5, 6.1, 3, 1.4, "2  SHIFT\nInsulina 10 U + glicose 25 g\nSalbutamol NBZ", AM),
          (6.8, 6.1, 3, 1.4, "3  REMOVER\nFurosemida · quelantes\nDiálise", CY),
          (2, 3.2, 6, 1.4, "Monitor contínuo · glicemia 1/1 h após insulina\nRepetir K⁺ em 1–2 h · tratar a causa (drogas, LRA, acidose)", GR)],
     [(4.2, 8.5, 1.7, 7.5, "sim"), (5, 8.5, 5, 7.5, ""), (5.8, 8.5, 8.3, 7.5, ""), (5, 6.1, 5, 4.6, "")], "Hipercalemia: 3 etapas")
save(fig, "img_hiperk.png")

# 4 Hiponatremia flow
fig, ax = plt.subplots(figsize=(10, 6.4))
flow(ax, [(3.3, 8.6, 3.4, 1, "Na < 135 → Osm plasmática", GOLD),
          (0.2, 6.4, 3, 1.1, "Osm normal/alta\nhiperglicemia, manitol,\npseudo-hipoNa", PU),
          (5.6, 6.4, 4, 1.1, "Osm < 275 (hipotônica)\n→ Osm urinária", CY),
          (3.6, 4.2, 2.8, 1.1, "Uosm < 100\npolidipsia, potomania", GR),
          (6.9, 4.2, 3, 1.1, "Uosm > 100\n→ volemia + Na urinário", AM),
          (5.0, 1.5, 2.4, 1.3, "Hipovolemia\nUNa<30 extrarrenal\nUNa>30 renal", RD),
          (7.6, 1.5, 2.3, 1.3, "Euvolemia UNa>30\nSIADH, hipotireoidismo,\ninsuf. adrenal", CY),
          (0.6, 1.5, 4.0, 1.3, "Hipervolemia (UNa<30)\nIC, cirrose, nefrótica", PU)],
     [(4, 8.6, 1.7, 7.5, ""), (6, 8.6, 7.6, 7.5, ""), (7, 6.4, 5, 5.3, ""), (8, 6.4, 8.4, 5.3, ""), (8, 4.2, 6.2, 2.8, ""), (8.4, 4.2, 8.7, 2.8, ""), (7.5, 4.2, 2.6, 2.8, "")],
     "Hiponatremia: algoritmo diagnóstico")
save(fig, "img_hipona.png")

# 5 Choque hemorrágico bars
fig, ax = plt.subplots(figsize=(8, 4.4)); cls = ["I", "II", "III", "IV"]; loss = [12, 22, 35, 45]; hr = [90, 110, 130, 150]
cols = [GR, AM, "#ff9b4d", RD]; ax.bar(cls, loss, color=cols)
for i, (l, f) in enumerate(zip(loss, hr)): ax.text(i, l + 1, f"~{['<15','15–30','31–40','>40'][i]}%\nFC ~{f}", ha="center", color=FG, fontsize=10)
ax.axvline(1.5, color=FG, ls=":"); ax.text(1.55, 47, "← PA cai a partir da classe III", color=RD, fontsize=10)
ax.set_ylabel("perda volêmica (%)"); ax.set_ylim(0, 55); ax.set_title("Classes de choque hemorrágico (ATLS)", color=GOLD); save(fig, "img_choque_hemorragico.png")

# 6 Vasoespasmo timeline
fig, ax = plt.subplots(figsize=(9, 3.6)); d = np.arange(0, 22)
risk = np.exp(-((d - 8) ** 2) / 14); ax.fill_between(d, risk, color=RD, alpha=.35); ax.plot(d, risk, color=RD, lw=2.5)
ax.axvspan(3, 14, color=AM, alpha=.08); ax.text(3.2, 1.03, "janela de vasoespasmo (dias 3–14, pico 7–10)", color=AM)
ax.annotate("Ressangramento: máximo nas 1ªs 24 h", (0.3, .15), (0.4, .55), color=CY, arrowprops=dict(arrowstyle="->", color=CY))
ax.text(14.5, .5, "Nimodipina 60 mg 4/4 h\n× 21 dias", color=GR)
ax.set_xlabel("dias após a HSA"); ax.set_yticks([]); ax.set_ylim(0, 1.15); ax.set_title("Linha do tempo da HSA", color=GOLD); save(fig, "img_hsa_timeline.png")

# 7 PV pulmonar
fig, ax = plt.subplots(figsize=(7.5, 4.6)); p = np.linspace(0, 45, 300); v = 1000 / (1 + np.exp(-(p - 18) / 4.5))
ax.plot(p, v, color=CY, lw=3); ax.axvspan(10, 28, color=GR, alpha=.1); ax.text(12, 900, "zona segura", color=GR)
ax.annotate("Ponto de inflexão inferior\n(colapso/abertura → PEEP acima)", (10.5, 120), (19, 120), color=AM, arrowprops=dict(arrowstyle="->", color=AM))
ax.annotate("Inflexão superior\n(hiperdistensão)", (28, 940), (31, 600), color=RD, arrowprops=dict(arrowstyle="->", color=RD))
ax.set_xlabel("pressão (cmH₂O)"); ax.set_ylabel("volume (mL)"); ax.set_title("Curva pressão-volume na SDRA", color=GOLD); save(fig, "img_pv_pulmao.png")

# 8 ROC
fig, ax = plt.subplots(figsize=(5.6, 5.2)); x = np.linspace(0, 1, 200)
for k, col, lab in [(1, "#777", "AUC 0,5 (acaso)"), (3, AM, "AUC ≈ 0,75"), (9, GR, "AUC ≈ 0,9")]:
    ax.plot(x, x if k == 1 else 1 - (1 - x) ** k, color=col, lw=2.5, ls="--" if k == 1 else "-", label=lab)
ax.set_xlabel("1 − especificidade (falso-positivo)"); ax.set_ylabel("sensibilidade"); ax.legend(facecolor=BG, edgecolor="#555", labelcolor=FG)
ax.set_title("Curva ROC", color=GOLD); save(fig, "img_roc.png")

# 9 Pirâmide de evidência
fig, ax = plt.subplots(figsize=(7.5, 5.4)); ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 10)
levels = [("Meta-análises", GOLD), ("Ensaios randomizados", GR), ("Coortes", CY), ("Caso-controle", AM), ("Séries/relatos de caso", "#ff9b4d"), ("Opinião de especialista", RD)]
for i, (t, c) in enumerate(levels):
    y0, y1 = 9 - i * 1.45, 9 - (i + 1) * 1.45; w0, w1 = 0.6 + i * 0.75, 0.6 + (i + 1) * 0.75
    ax.add_patch(Polygon([[5 - w1, y1], [5 + w1, y1], [5 + w0, y0], [5 - w0, y0]], fc=c, ec=BG, alpha=.85))
    ax.text(5, (y0 + y1) / 2, t, ha="center", va="center", fontsize=10.5, color="black", weight="bold")
ax.set_title("Pirâmide da evidência (GRADE ajusta a qualidade)", color=GOLD); save(fig, "img_piramide.png")

# 10 CAD flow
fig, ax = plt.subplots(figsize=(9.5, 6))
flow(ax, [(3, 8.6, 4, 1, "CAD: volume 1–1,5 L na 1ª hora", GOLD),
          (3, 6.6, 4, 1.1, "K⁺ ?", CY),
          (0.1, 4.4, 3, 1.2, "< 3,5\nrepor K, ADIAR insulina", RD),
          (3.5, 4.4, 3, 1.2, "3,5–5,0\ninsulina 0,1 U/kg/h\n+ 20–30 mEq K/L", GR),
          (6.9, 4.4, 3, 1.2, "> 5,0\ninsulina, sem K\ndosar 2/2 h", AM),
          (2, 1.6, 6, 1.4, "Glicemia < 250 → SG 5–10% + manter insulina\nResolução: β-OHB < 0,6 + pH ≥ 7,3 → basal SC 1–2 h antes", PU)],
     [(5, 8.6, 5, 7.7, ""), (4, 6.6, 1.6, 5.6, ""), (5, 6.6, 5, 5.6, ""), (6, 6.6, 8.4, 5.6, ""), (5, 4.4, 5, 3.0, "")], "Cetoacidose diabética: fluxo inicial (ADA 2024)")
save(fig, "img_cad.png")

# 11 PA classes
fig, ax = plt.subplots(figsize=(8.5, 4.4)); ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 6.8)
rows = [("Ótima", "< 120", "< 80", GR), ("Normal", "120–129", "80–84", "#8fe3a8"), ("Pré-hipertensão", "130–139", "85–89", AM), ("HAS estágio 1", "140–159", "90–99", "#ff9b4d"), ("HAS estágio 2", "160–179", "100–109", RD), ("HAS estágio 3", "≥ 180", "≥ 110", "#b30000")]
ax.text(1.2, 6.3, "Classe", color=GOLD, weight="bold"); ax.text(5.2, 6.3, "PAS", color=GOLD, weight="bold"); ax.text(7.8, 6.3, "PAD", color=GOLD, weight="bold")
for i, (n, s, d, c) in enumerate(rows):
    y = 5.4 - i * 0.95; ax.add_patch(Rectangle((0.2, y - .35), 9.6, .8, fc=c, alpha=.85))
    tc = "white" if c in (RD, "#b30000") else "black"; ax.text(0.5, y, n, color=tc, weight="bold", va="center"); ax.text(5.2, y, s, color=tc, va="center"); ax.text(7.8, y, d, color=tc, va="center")
ax.set_title("Classificação da PA no consultório (Diretriz Brasileira 2020)", color=GOLD); save(fig, "img_pa_class.png")

# 12 DRC heatmap
fig, ax = plt.subplots(figsize=(7.5, 5)); G = ["G1 ≥90", "G2 60–89", "G3a 45–59", "G3b 30–44", "G4 15–29", "G5 <15"]; A = ["A1 <30", "A2 30–300", "A3 >300"]
risk = np.array([[0, 1, 2], [0, 1, 2], [1, 2, 3], [2, 3, 3], [3, 3, 3], [3, 3, 3]])
cmap = matplotlib.colors.ListedColormap([GR, AM, "#ff8a3d", RD]); ax.imshow(risk, cmap=cmap, aspect="auto")
ax.set_xticks(range(3)); ax.set_xticklabels(A); ax.set_yticks(range(6)); ax.set_yticklabels(G)
for i in range(6):
    for j in range(3): ax.text(j, i, ["baixo", "moderado", "alto", "muito alto"][risk[i, j]], ha="center", va="center", color="black", fontsize=10, weight="bold")
ax.set_xlabel("albuminúria (mg/g)"); ax.set_title("DRC: prognóstico KDIGO (TFG × albuminúria)", color=GOLD); save(fig, "img_drc_heatmap.png")

# 13 GOLD ABE
fig, ax = plt.subplots(figsize=(8, 5)); ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 10)
ax.add_patch(Rectangle((0.5, 5.5), 9, 3.6, fc="#2a1414", ec=RD, lw=2.5)); ax.text(5, 7.3, "E  ·  ≥ 2 exacerbações moderadas ou ≥ 1 internação\nLABA + LAMA (+ ICS se eosinófilos ≥ 300)", ha="center", va="center", color=FG, fontsize=11)
ax.add_patch(Rectangle((0.5, 0.8), 4.4, 4.2, fc="#14241a", ec=GR, lw=2.5)); ax.text(2.7, 2.9, "A\nmMRC 0–1 / CAT < 10\n1 broncodilatador", ha="center", va="center", color=FG, fontsize=11)
ax.add_patch(Rectangle((5.1, 0.8), 4.4, 4.2, fc="#2a2410", ec=AM, lw=2.5)); ax.text(7.3, 2.9, "B\nmMRC ≥ 2 / CAT ≥ 10\nLABA + LAMA", ha="center", va="center", color=FG, fontsize=11)
ax.text(5, 9.6, "0–1 exacerbação sem internação ↓   ·   sintomas →", ha="center", color="#aaa", fontsize=10)
ax.set_title("DPOC: grupos GOLD ABE e tratamento inicial", color=GOLD); save(fig, "img_gold_abe.png")

# 14 Insulinas
fig, ax = plt.subplots(figsize=(8.5, 4.4)); t = np.linspace(0, 26, 500)
def prof(t, on, pk, dur, amp):
    y = np.where(t < on, 0, np.where(t < pk, (t - on) / (pk - on), np.clip(1 - (t - pk) / (dur - pk), 0, 1))); return amp * y
ax.plot(t, prof(t, .2, 1, 4.5, 1), color=RD, lw=2.5, label="Ultrarrápida")
ax.plot(t, prof(t, .5, 2.5, 7, .8), color=AM, lw=2.5, label="Regular")
ax.plot(t, prof(t, 1.5, 6, 16, .6), color=CY, lw=2.5, label="NPH")
ax.plot(t, np.where(t < 1.5, t / 1.5 * .3, .3), color=GR, lw=2.5, label="Glargina/degludeca")
ax.set_xlabel("horas"); ax.set_ylabel("efeito (relativo)"); ax.set_yticks([]); ax.legend(facecolor=BG, edgecolor="#555", labelcolor=FG)
ax.set_title("Perfis de ação das insulinas (esquemático)", color=GOLD); save(fig, "img_insulinas.png")

# 15 CD4
fig, ax = plt.subplots(figsize=(8.5, 4.6)); ax.set_xlim(0, 500); ax.set_ylim(0, 4)
for x0, x1, y, t, c in [(0, 200, 3, "Pneumocistose · candidíase esofágica (< 200)", AM), (0, 100, 2, "Toxoplasmose · criptococose (< 100)", "#ff9b4d"), (0, 50, 1, "MAC · CMV (< 50)", RD)]:
    ax.barh(y, x1 - x0, left=x0, height=.6, color=c); ax.text(x1 + 8, y, t, va="center", ha="right", color=FG)
ax.barh(0.2, 500, height=.25, color=CY, alpha=.5); ax.text(250, .55, "Tuberculose: qualquer CD4", ha="center", color=CY)
ax.set_yticks([]); ax.set_xlabel("CD4 (células/mm³)"); ax.invert_xaxis(); ax.set_title("HIV: infecções oportunistas por faixa de CD4", color=GOLD)
save(fig, "img_cd4.png")

# 16 Anemia VCM
fig, ax = plt.subplots(figsize=(10, 5.6))
flow(ax, [(3.5, 8.4, 3, 1, "Anemia → VCM", GOLD),
          (0.1, 5.2, 3.1, 2.1, "< 80 MICRO\nferro · talassemia\ndoença crônica\nsideroblástica", RD),
          (3.45, 5.2, 3.1, 2.1, "80–100 NORMO\n→ reticulócitos\n↑ hemólise/perda\n↓ DRC, medula, crônica", AM),
          (6.8, 5.2, 3.1, 2.1, "> 100 MACRO\nB12/folato · álcool\nhepatopatia · hipotireoidismo\nSMD · drogas", CY),
          (0.1, 1.6, 3.1, 1.8, "Ferritina < 30 → ferro\nnormal + RDW normal\n→ eletroforese de Hb", RD),
          (6.8, 1.6, 3.1, 1.8, "B12 baixa? ácido\nmetilmalônico ↑\nneuro só na B12", CY)],
     [(4.3, 8.4, 1.7, 7.4, ""), (5, 8.4, 5, 7.4, ""), (5.7, 8.4, 8.3, 7.4, ""), (1.65, 5.2, 1.65, 3.5, ""), (8.35, 5.2, 8.35, 3.5, "")], "Anemia: abordagem pelo VCM")
save(fig, "img_anemia_vcm.png")

# 17 Escada OMS
fig, ax = plt.subplots(figsize=(8.5, 5)); ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 8)
for i, (t, c) in enumerate([("1  Dor leve\nNão opioide\n(dipirona, paracetamol,\nAINE) ± adjuvante", GR), ("2  Dor moderada\nOpioide fraco\n(tramadol, codeína)\n± não opioide", AM), ("3  Dor intensa\nOpioide forte\n(morfina, oxicodona,\nmetadona, fentanil)", RD)]):
    ax.add_patch(Rectangle((0.3 + i * 3.2, 0.4 + i * 2.1), 3.1, 2.0 + (2 - i) * 0 + 0.0, fc=c, alpha=.85))
    ax.text(0.3 + i * 3.2 + 1.55, 0.4 + i * 2.1 + 1.0, t, ha="center", va="center", fontsize=9, color="black", weight="bold")

ax.text(0.4, 7.4, "Adjuvantes: antidepressivo, anticonvulsivante (dor neuropática),\ncorticoide · laxativo sempre com opioide", color=CY, fontsize=10)
ax.set_title("Escada analgésica da OMS", color=GOLD); save(fig, "img_escada_oms.png")
print(len(os.listdir("media")))
