import genanki

CSS = """
.card{font-family:-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;font-size:19px;line-height:1.5;
 text-align:left;color:#ece9e1;background:#0e1116;padding:14px 16px;}
.tema{display:inline-block;font-size:13px;letter-spacing:.5px;color:#0e1116;background:linear-gradient(90deg,#d4af37,#f3d77a);
 padding:3px 10px;border-radius:12px;font-weight:700;margin-bottom:10px;}
.q{font-size:22px;font-weight:600;color:#fff;border-left:4px solid #4dd4ff;padding-left:10px;}
hr#answer{border:0;height:2px;background:linear-gradient(90deg,#d4af37,#4dd4ff,transparent);margin:14px 0;}
.a{background:#151b23;border:1px solid #2a3442;border-radius:10px;padding:12px 14px;}
b{color:#fff}
.r{color:#ff6b6b!important}.g{color:#5be38a!important}.y{color:#ffc14d!important}.c{color:#4dd4ff!important}
table.t{color:#ece9e1;border-collapse:collapse;width:100%;margin:8px 0;font-size:16px;}
table.t th{background:#1d2a36;color:#4dd4ff;padding:6px 8px;border:1px solid #33414f;text-align:left;}
table.t td{color:#ece9e1;padding:6px 8px;border:1px solid #2a3442;vertical-align:top;}
table.t tr:nth-child(even) td{background:#121820;}
ul{margin:6px 0;padding-left:22px}li{margin:3px 0}
.img{margin-top:12px;text-align:center}.img img{max-width:100%;border-radius:8px;border:1px solid #2a3442}
.peg{margin-top:12px;background:#2a2210;border-left:4px solid #ffc14d;border-radius:6px;padding:10px 12px;font-size:16px;color:#ffe9b8}
.src{margin-top:10px;font-size:13px;color:#8a94a3}
.nightMode .card, .card.nightMode{background:#0e1116;color:#ece9e1}
"""

model = genanki.Model(
  1728450112, "TEMI 2028 · Códice Visual",
  fields=[{"name": n} for n in ["Frente", "Verso", "Imagem", "Pegadinha", "Fonte", "Tema"]],
  templates=[{"name": "Card 1",
    "qfmt": '<div class=tema>{{Tema}}</div><div class=q>{{Frente}}</div>',
    "afmt": '{{FrontSide}}<hr id=answer><div class=a>{{Verso}}</div>{{#Imagem}}<div class=img>{{Imagem}}</div>{{/Imagem}}'
            '{{#Pegadinha}}<div class=peg>🎯 <b>Pegadinha / Nerd</b><br>{{Pegadinha}}</div>{{/Pegadinha}}'
            '{{#Fonte}}<div class=src>📚 {{Fonte}}</div>{{/Fonte}}'}],
  css=CSS)

