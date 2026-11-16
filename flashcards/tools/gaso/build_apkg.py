#!/usr/bin/env python3
"""Pacote Anki 🧪 Gasometria 360X: 450 flashcards (13 subbaralhos) + 145 questões (subbaralho ❓).
Uso: python3 build_apkg.py <arquivo.apkg>   (requer build_gaso.py e build_q.py já rodados)"""
import json, os, sys, genanki
OUT = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
man = json.load(open(os.path.join(HERE, "gaso_manifest.json"), encoding="utf-8"))
Q = json.load(open(os.path.join(HERE, "gaso_questoes.json"), encoding="utf-8"))
CSS = """.card{font-family:Inter,-apple-system,'Segoe UI',sans-serif;font-size:18px;line-height:1.5;text-align:left;color:#ece9e1;background:#0e1116;padding:12px 14px}
.tema{display:inline-block;font-size:12.5px;padding:3px 10px;border-radius:12px;background:#2a1a0e;color:#ffd9b8;margin-bottom:8px}
.q{font-size:18px;color:#fff;border-left:4px solid #d4af37;padding-left:10px}
table{max-width:100%}hr#answer{border:0;height:2px;background:linear-gradient(90deg,#d4af37,#ff9d5c,transparent);margin:14px 0}
.a{background:#151b23;border:1px solid #2a3442;border-radius:10px;padding:10px 12px}b{color:#fff}
.alt{margin:4px 0;padding:6px 9px;border:1px solid #2a3442;border-radius:8px}.alt.ok{border-color:#5be38a;background:#10261a}
.peg{margin-top:10px;background:#2a2210;border-left:4px solid #ffc14d;border-radius:8px;padding:10px 12px;font-size:15.5px;color:#ffe9b8}
.src{margin-top:8px;font-size:12.5px;color:#8a94a3}"""
MC = genanki.Model(1794800001, "Gasometria 360X · Card", fields=[{"name": n} for n in ["Frente", "Verso", "Pegadinha", "Fonte", "Tema"]],
    templates=[{"name": "Card", "qfmt": "<span class='tema'>{{Tema}}</span><div class='q'>{{Frente}}</div>",
                "afmt": "{{FrontSide}}<hr id='answer'><div class='a'>{{Verso}}</div>{{#Pegadinha}}<div class='peg'>🎯 <b>Pegadinha</b><br>{{Pegadinha}}</div>{{/Pegadinha}}<div class='src'>📚 {{Fonte}}</div>"}], css=CSS)
MQ = genanki.Model(1794800002, "Gasometria 360X · Questão", fields=[{"name": n} for n in ["Enunciado", "Alternativas", "Gabarito", "Comentario", "Porque", "Pegadinha", "Tema"]],
    templates=[{"name": "Questão", "qfmt": "<span class='tema'>❓ {{Tema}}</span><div class='q'>{{Enunciado}}</div>{{Alternativas}}",
                "afmt": "{{FrontSide}}<hr id='answer'><div class='a'>✅ <b>Gabarito: {{Gabarito}}</b><br>{{Comentario}}</div><div class='a' style='margin-top:8px'><b>🔍 Alternativa por alternativa</b><br>{{Porque}}</div>{{#Pegadinha}}<div class='peg'>🎯 <b>Pegadinha de prova</b><br>{{Pegadinha}}</div>{{/Pegadinha}}"}], css=CSS)
decks = {}
def D(n):
    if n not in decks: decks[n] = genanki.Deck(1794800100 + len(decks), n)
    return decks[n]
for c in man["cards"]:
    D(c["baralho"]).add_note(genanki.Note(model=MC, guid=genanki.guid_for("gaso360x", c["n"]), tags=c["tags"],
        fields=[c["frente"], c["verso"], c["pegadinha"], c["fonte"], c["baralho"].split("::")[-1]]))
L = "ABCDE"
for q in Q:
    g = int(q["gab"])
    alts = "".join(f"<div class='alt'><b>{L[i]}</b> {a}</div>" for i, a in enumerate(q["alts"]))
    pq = "<br>".join(f"<b>{L[i]}</b> {'✅' if i == g else '❌'} {p}" for i, p in enumerate(q["porque"]))
    D("🧪 Gasometria 360X::❓ Questões comentadas").add_note(genanki.Note(model=MQ, guid=genanki.guid_for("gaso360xq", q["id"]),
        tags=["GASO", "GASO_QUESTAO", "TEMI2028", "R3CM"], fields=[q["enun"], alts, f"{L[g]} — {q['alts'][g]}", q["com"], pq, q.get("pega", ""), q["tema"]]))
genanki.Package(list(decks.values())).write_to_file(OUT)
print(OUT, os.path.getsize(OUT) // 1024, "KB ·", sum(len(d.notes) for d in decks.values()), "notas ·", len(decks), "baralhos")
