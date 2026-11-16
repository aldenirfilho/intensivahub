"""Construtores dos cards de gasometria (usados por g01–g10)."""
from gaso_engine import analyze, panel, f

Q_DEF = "❓ Interprete a gasometria passo a passo e defina a conduta."
NUM = "1️⃣ 2️⃣ 3️⃣ 4️⃣ 5️⃣ 6️⃣ 7️⃣ 8️⃣ 9️⃣ 🔟".split()


def K(ctx, lab, exp, dx, causa, cond, peg, q=None):
    """Caso com laudo: o motor calcula os passos e confere a classificação esperada (exp = 'AM_AG+ALR')."""
    return dict(kind="caso", ctx=ctx, lab=lab, exp=set(exp.split("+")), dx=dx, causa=causa, cond=cond, peg=peg, q=q or Q_DEF)


def C(frente, dx, crit, cond, peg, lab=None):
    """Card conceitual (com laudo opcional, sem conferência de classificação)."""
    return dict(kind="conceito", frente=frente, dx=dx, crit=crit, cond=cond, peg=peg, lab=lab)


def render(card, n):
    tag = f"🧪 <b>Gaso #{n:03d}</b>"
    if card["kind"] == "caso":
        R = analyze(card["lab"])
        got = set(R["codes"])
        assert got == card["exp"], f"Gaso #{n}: motor {sorted(got)} ≠ esperado {sorted(card['exp'])} · {card['dx']}"
        frente = f"{tag} · {card['ctx']}{panel(card['lab'])}{card['q']}"
        passos = "<br>".join(f"{NUM[i]} {s}" for i, s in enumerate(R["steps"]))
        verso = (f"✅ <b>{card['dx']}</b><br>🧮 <i>Classificação: {R['dx']}</i><br>🔎 <b>Passo a passo</b><br>{passos}"
                 f"<br>🩺 <b>Por quê:</b> {card['causa']}<br>⚡ <b>Conduta:</b> {card['cond']}")
        return frente, verso, R
    frente = f"{tag} · {card['frente']}" + (panel(card["lab"]) if card.get("lab") else "")
    verso = f"✅ <b>{card['dx']}</b><br>🔎 {card['crit']}" + (f"<br>⚡ <b>Na prática:</b> {card['cond']}" if card.get("cond") else "")
    return frente, verso, None
