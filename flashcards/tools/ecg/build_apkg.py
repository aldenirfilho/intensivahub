#!/usr/bin/env python3
"""Pacote Anki do Compêndio de ECG 360X: 300 notas, traçado na frente, 18 subbaralhos.
Uso: python3 build_apkg.py <APP_DIR> <arquivo.apkg>   (requer build_ecg.py já rodado — usa os PNGs em data/media/ecg/)"""
import json, os, sys, genanki

APP, OUT = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
man = json.load(open(os.path.join(HERE, "ecg_cards.json"), encoding="utf-8"))
CSS = """.card{font-family:Inter,-apple-system,'Segoe UI',sans-serif;font-size:19px;line-height:1.5;text-align:left;color:#ece9e1;background:#0e1116;padding:12px 14px}
.tema{display:inline-block;font-size:12.5px;padding:3px 10px;border-radius:12px;background:#1d2a36;color:#cfe9f5;margin-bottom:8px}
.q{font-size:20px;font-weight:600;color:#fff;border-left:4px solid #d4af37;padding-left:10px}
.ecg{margin-top:10px}.ecg img{width:100%;height:auto;border-radius:6px;background:#fff}
hr#answer{border:0;height:2px;background:linear-gradient(90deg,#d4af37,#4dd4ff,transparent);margin:14px 0}
.a{background:#151b23;border:1px solid #2a3442;border-radius:10px;padding:10px 12px}b{color:#fff}
.peg{margin-top:10px;background:#2a2210;border-left:4px solid #ffc14d;border-radius:8px;padding:10px 12px;font-size:16px;color:#ffe9b8}
.src{margin-top:8px;font-size:13px;color:#8a94a3}
.nightMode .card,.night_mode .card{background:#0e1116}"""
M = genanki.Model(1794600001, "ECG 360X · Traçado", fields=[{"name": n} for n in ["Frente", "Traçado", "Verso", "Pegadinha", "Fonte", "Tema"]],
    templates=[{"name": "ECG", "qfmt": "<span class='tema'>{{Tema}}</span><div class='q'>{{Frente}}</div><div class='ecg'>{{Traçado}}</div>",
                "afmt": "{{FrontSide}}<hr id='answer'><div class='a'>{{Verso}}</div>{{#Pegadinha}}<div class='peg'>🎯 <b>Pegadinha / Nerd</b><br>{{Pegadinha}}</div>{{/Pegadinha}}<div class='src'>📚 {{Fonte}}</div>"}], css=CSS)
decks, media = {}, []
for c in man["cards"]:
    dn = c["baralho"]
    if dn not in decks: decks[dn] = genanki.Deck(1794600100 + len(decks), dn)
    img = c["imagem_frente"]; media.append(os.path.join(APP, "data/media/ecg", img))
    decks[dn].add_note(genanki.Note(model=M, guid=genanki.guid_for("ecg360x", c["n"]), tags=[t.replace(" ", "_") for t in c["tags"]],
        fields=[c["frente"], f"<img src='{img}'>", c["verso"], c["pegadinha"], c["fonte"], dn.split("::")[-1]]))
p = genanki.Package(list(decks.values())); p.media_files = media; p.write_to_file(OUT)
print(OUT, os.path.getsize(OUT) // 1024, "KB ·", sum(len(d.notes) for d in decks.values()), "notas ·", len(decks), "baralhos ·", len(media), "imagens")
