import numpy as np, matplotlib, os
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
os.makedirs("media", exist_ok=True)
BG, FG, GOLD, CY, RD, GR, AM, PU = "#0e1116", "#e8e6df", "#d4af37", "#4dd4ff", "#ff6b6b", "#5be38a", "#ffc14d", "#b48cff"
plt.rcParams.update({"figure.facecolor": BG, "axes.facecolor": BG, "text.color": FG, "font.size": 12})
def save(fig, n): fig.savefig(f"media/{n}", dpi=110, bbox_inches="tight"); plt.close(fig)
def box(ax, x, y, w, h, t, c, fs=10.5):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1", fc="#161c24", ec=c, lw=2.2)); ax.text(x + w / 2, y + h / 2, t, ha="center", va="center", fontsize=fs, color=FG)
def arr(ax, x1, y1, x2, y2, lab=""):
    ax.annotate("", (x2, y2), (x1, y1), arrowprops=dict(arrowstyle="->", color="#aaa", lw=1.6))
    if lab: ax.text((x1 + x2) / 2 + .15, (y1 + y2) / 2, lab, fontsize=9.5, color=AM)

# Sepsis-3
fig, ax = plt.subplots(figsize=(9.5, 5.6)); ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 10)
box(ax, 3, 8.4, 4, 1.1, "Suspeita de infecção", CY)
box(ax, 3, 5.8, 4, 1.3, "↑ SOFA ≥ 2 pontos?\n(disfunção orgânica)", AM)
box(ax, 0.2, 3.2, 3.6, 1.2, "Não → infecção\nreavaliar / monitorar", GR)
box(ax, 6.2, 3.2, 3.6, 1.2, "Sim → SEPSE\nmortalidade > 10%", "#ff9b4d")
box(ax, 5.2, 0.4, 4.6, 1.6, "Vasopressor p/ PAM ≥ 65\n+ lactato > 2 mmol/L\napesar de volume → CHOQUE SÉPTICO (> 40%)", RD, 10)
arr(ax, 5, 8.4, 5, 7.2); arr(ax, 4, 5.8, 2, 4.5, "não"); arr(ax, 6, 5.8, 8, 4.5, "sim"); arr(ax, 8, 3.2, 7.5, 2.1)
ax.set_title("Sepsis-3: do diagnóstico ao choque séptico", color=GOLD, fontsize=14); save(fig, "img_sepsis3.png")

# Hora-1
fig, ax = plt.subplots(figsize=(10, 3.8)); ax.axis("off"); ax.set_xlim(0, 10.4); ax.set_ylim(0, 4)
steps = [("1", "Lactato\n(repetir se > 2)", CY), ("2", "Hemoculturas\nantes do ATB", PU), ("3", "Antimicrobiano\namplo ≤ 1 h", RD), ("4", "Cristaloide\n30 mL/kg se hipoperfusão", AM), ("5", "Vasopressor\nse PAM < 65", GR)]
for i, (n, t, c) in enumerate(steps):
    x = 0.2 + i * 2.05; ax.add_patch(FancyBboxPatch((x, 1.0), 1.8, 1.9, boxstyle="round,pad=0.08", fc="#161c24", ec=c, lw=2.5))
    ax.text(x + 0.9, 2.55, n, ha="center", fontsize=20, color=c, weight="bold"); ax.text(x + 0.9, 1.55, t, ha="center", va="center", fontsize=9.6, color=FG)
    if i < 4: ax.annotate("", (x + 2.05, 1.95), (x + 1.85, 1.95), arrowprops=dict(arrowstyle="->", color="#aaa", lw=1.6))
ax.text(5.2, 3.45, "Pacote da 1ª hora (iniciar já; completar o quanto antes)", ha="center", color=GOLD, fontsize=13, weight="bold")
ax.text(5.2, 0.35, "Reavaliar perfusão (TEC, lactato, diurese, mental) e responsividade a volume continuamente", ha="center", color="#9aa4b2", fontsize=10)
save(fig, "img_hora1.png")

# Escada de vasopressores
fig, ax = plt.subplots(figsize=(9, 5.2)); ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 8.6)
lad = [("1", "NORADRENALINA\nalvo PAM ≥ 65", CY), ("2", "+ VASOPRESSINA até 0,03 U/min\n(NA 0,25–0,5 mcg/kg/min)", PU), ("3", "+ HIDROCORTISONA 200 mg/dia\n(NA ≥ 0,25 por ≥ 4 h)", GR), ("4", "+ ADRENALINA\n(ou dobutamina se disfunção cardíaca)", AM), ("5", "Refratário: rever foco, ECO,\nangiotensina II / azul de metileno", RD)]
for i, (n, t, c) in enumerate(lad):
    y = 0.3 + i * 1.6; x = 0.3 + i * 0.9
    ax.add_patch(Rectangle((x, y), 6.4, 1.35, fc=c, alpha=.85)); ax.text(x + 0.35, y + 0.67, n, fontsize=18, weight="bold", color="black", va="center")
    ax.text(x + 3.5, y + 0.67, t, ha="center", va="center", fontsize=10, color="black", weight="bold")
ax.set_title("Choque séptico: escada de vasopressores (SSC 2021)", color=GOLD, fontsize=14); save(fig, "img_vasopressores.png")
print("ok")
