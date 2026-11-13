#!/usr/bin/env python3
"""Pacote Anki da aba Honra: baralho "🕊️ Honra 360X" com subbaralhos por tradição (cards) e por tema (mnemônicos).
Uso: python3 tools/ho/build_apkg.py <raiz_do_app> <arquivo.apkg>"""
import json, sys, os, html, genanki

ROOT, OUT = sys.argv[1], sys.argv[2]
D = json.load(open(os.path.join(ROOT, "data/honra.json"), encoding="utf-8"))
e = html.escape
CSS = """.card{font-family:Inter,-apple-system,'Segoe UI',sans-serif;font-size:19px;line-height:1.5;text-align:left;color:#ece9e1;background:#0e1116;padding:14px 16px}
.tr{display:inline-block;font-size:13px;font-weight:700;padding:3px 10px;border-radius:12px;border:1px solid;margin:0 6px 10px 0}
.tema{display:inline-block;font-size:12.5px;padding:3px 10px;border-radius:12px;background:#1d2a36;color:#cfe9f5}
.q{font-size:21px;font-weight:600;color:#fff;border-left:4px solid #d4af37;padding-left:10px}
hr#answer{border:0;height:2px;background:linear-gradient(90deg,#d4af37,#4dd4ff,transparent);margin:14px 0}
.a{font:500 18px/1.55 Georgia,serif}.ref{color:#f3d77a;font-size:14px;margin-top:8px}.ref small{color:#8a94a3}
.ap{margin-top:10px;padding:10px 12px;border-radius:10px;background:#0f2a22;border:1px solid #2f5b45;font-size:16px}.ap b{display:block;color:#5be38a;font-size:13px}
.sig{font:700 34px Georgia,serif;letter-spacing:3px;color:#d4af37;text-align:center;margin:10px 0}
table{border-collapse:collapse;width:100%;font-size:16px}td{padding:6px 8px;border:1px solid #2a3442;vertical-align:top}td.l{color:#4dd4ff;font-weight:700;white-space:nowrap;width:1%}
.x{margin-top:10px;color:#ffc14d;font-size:15px}.c{margin-top:8px;font-size:14px;color:#9aa4b2}.c b{color:#cfe9f5}
.nightMode .card,.night_mode .card{background:#0e1116}"""

M_CARD = genanki.Model(1794500001, "Honra 360X · Card", fields=[{"name": n} for n in ["Pergunta", "Ensinamento", "Referência", "Aplicação", "Tradição", "Tema"]],
    templates=[{"name": "Card", "qfmt": "{{Tradição}}<span class='tema'>{{Tema}}</span><div class='q'>{{Pergunta}}</div>",
                "afmt": "{{FrontSide}}<hr id='answer'><div class='a'>{{Ensinamento}}</div><div class='ref'>📍 {{Referência}} <small>· paráfrase 360X</small></div><div class='ap'><b>🧭 Faça hoje</b>{{Aplicação}}</div>"}], css=CSS)
M_MN = genanki.Model(1794500002, "Honra 360X · Mnemônico", fields=[{"name": n} for n in ["Título", "Sigla", "Itens", "Dica", "Contexto", "Tema", "Origem"]],
    templates=[{"name": "Mnemônico", "qfmt": "<span class='tema'>{{Tema}}</span> <span class='tema'>{{Origem}}</span><div class='q'>🛡️ {{Título}}</div>",
                "afmt": "{{FrontSide}}<hr id='answer'><div class='sig'>{{Sigla}}</div>{{Itens}}{{#Dica}}<div class='x'>🎯 {{Dica}}</div>{{/Dica}}<div class='c'><b>📖 Contexto</b><br>{{Contexto}}</div>"}], css=CSS)

decks = {}
def deck(name):
    if name not in decks: decks[name] = genanki.Deck(1794500100 + len(decks), name)
    return decks[name]

T = D["trads"]
for i, (k, t) in enumerate(T.items()):
    deck(f"🕊️ Honra 360X::🎴 Cards::{i + 1:02d} {t['e']} {t['n']}")
order = {k: i for i, k in enumerate(T)}
for c in D["cards"]:
    t = T[c["tr"]]; dn = f"🕊️ Honra 360X::🎴 Cards::{order[c['tr']] + 1:02d} {t['e']} {t['n']}"
    chip = f"<span class='tr' style='border-color:{t['c']};color:{t['c']}'>{t['e']} {e(t['n'])}</span>"
    deck(dn).add_note(genanki.Note(model=M_CARD, guid=genanki.guid_for(c["id"]), tags=["honra360x", c["tr"]],
        fields=[e(c["q"]), e(c["a"]), e(c["r"]), e(c["ap"]), chip, e(c["tema"])]))
for i, tm in enumerate(D["temas"]):
    deck(f"🕊️ Honra 360X::🛡️ Mnemônicos::{i + 1:02d} {tm}")
for m in D["mn"]:
    dn = f"🕊️ Honra 360X::🛡️ Mnemônicos::{D['temas'].index(m['tema']) + 1:02d} {m['tema']}"
    rows = "".join(f"<tr><td class='l'>{e(a)}</td><td>{e(b)}</td></tr>" for a, b in m["k"])
    deck(dn).add_note(genanki.Note(model=M_MN, guid=genanki.guid_for(m["id"]), tags=["honra360x", "mnemonico", "classico" if m["o"] == "c" else "360x"],
        fields=[e(m["t"]), e(m["m"]), f"<table>{rows}</table>", e(m.get("x", "")), e(m.get("c", "")), e(m["tema"]), "🏛️ Clássico" if m["o"] == "c" else "⚒️ 360X"]))

ds = [d for d in decks.values() if d.notes]
genanki.Package(ds).write_to_file(OUT)
print(OUT, os.path.getsize(OUT) // 1024, "KB ·", sum(len(d.notes) for d in ds), "notas em", len(ds), "baralhos")
