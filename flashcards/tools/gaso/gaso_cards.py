"""Construtores dos cards de gasometria (usados por g01–g10)."""
from gaso_engine import analyze, panel, f

Q_DEF = "❓ Interprete a gasometria passo a passo e defina a conduta."
NUM = "1️⃣ 2️⃣ 3️⃣ 4️⃣ 5️⃣ 6️⃣ 7️⃣ 8️⃣ 9️⃣ 🔟".split()


def K(ctx, lab, exp, dx, causa, cond, peg, q=None, x=None):
    """Caso com laudo: o motor calcula os passos e confere a classificação esperada (exp = 'AM_AG+ALR').
    x (4.14.0): etapas extras do caso guiado — lista de (pergunta, [opções], índice_correto, explicação)."""
    for st in x or []:
        assert len(st) == 4 and 0 <= st[2] < len(st[1]) and len(set(st[1])) == len(st[1]) and st[3], st
    return dict(kind="caso", ctx=ctx, lab=lab, exp=set(exp.split("+")), dx=dx, causa=causa, cond=cond, peg=peg, q=q or Q_DEF, x=x or [])


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
        todos = R["steps"] + R.get("xsteps", [])
        passos = "<br>".join(f"{NUM[i] if i < len(NUM) else str(i + 1) + '.'} {s}" for i, s in enumerate(todos))
        verso = (f"✅ <b>{card['dx']}</b><br>🧮 <i>Classificação: {R['dx']}</i><br>🔎 <b>Passo a passo</b><br>{passos}"
                 f"<br>🩺 <b>Por quê:</b> {card['causa']}<br>⚡ <b>Conduta:</b> {card['cond']}"
                 + "".join(f"<br>🎯 <b>{p}</b> {o[c]}" for p, o, c, e in card.get("x", [])))
        return frente, verso, R
    frente = f"{tag} · {card['frente']}" + (panel(card["lab"]) if card.get("lab") else "")
    verso = f"✅ <b>{card['dx']}</b><br>🔎 {card['crit']}" + (f"<br>⚡ <b>Na prática:</b> {card['cond']}" if card.get("cond") else "")
    return frente, verso, None
