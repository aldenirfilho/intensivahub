"""Mnemônicos 360X — gera data/mnemonicos.json e o .apkg a partir dos arquivos mt*.py (TEMI) e mr*.py (R3).

Formato de cada arquivo (TXT = r\"\"\"...\"\"\"):
  ## 01 🫁 Nome do tema
  @ Para que serve (título)
  # SIGLA :: item 1; item 2; item 3        -> modo sigla: a inicial de cada item confere com cada letra
  # 6-30-15 :: 6 = texto; 30 = texto        -> modo livre: cada item traz o próprio rótulo ("rótulo = texto")
  ! dica ou pegadinha (opcional)
  ^c | ^o | ^cf | ^of                       -> c = clássico, o = original 360X; f = frase validada pelas iniciais
"""
import re, sys, json, glob, hashlib, unicodedata, importlib, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
OUT = "/home/claude/app2"
LET = r"A-Za-zÀ-ÖØ-öø-ÿ"
def base(c): return unicodedata.normalize("NFD", c)[0].upper()
def units(s): return re.findall(rf"[{LET}]|\d+(?:[.,]\d+)?", s)
def first(s):
    m = re.search(rf"\d+(?:[.,]\d+)?|[{LET}]", s); return m.group(0) if m else ""

def parse(txt, div, erros):
    out, tema, cur = [], None, None
    for n, ln in enumerate(txt.strip().splitlines(), 1):
        ln = ln.strip()
        if not ln: continue
        if ln.startswith("##"): tema = ln[2:].strip(); continue
        k, v = ln[0], ln[1:].strip()
        if k == "@": cur = dict(d=div, tema=tema, t=v, m="", k=[], x="", o="o", tp="a", raw=""); out.append(cur)
        elif k == "#": cur["raw"] = v
        elif k == "!": cur["x"] = v
        elif k == "^": cur["o"] = v[0]; cur["f"] = "f" in v[1:]
        else: erros.append(f"linha inválida: {ln[:60]}")
    for c in out:
        if " :: " not in c["raw"]: erros.append(f"sem itens: {c['t']}"); continue
        sig, body = c["raw"].split(" :: ", 1); itens = [i.strip() for i in re.split(r";(?![^()]*\))", body) if i.strip()]   # ";" dentro de parênteses não separa
        c["m"] = sig.strip().strip('"'); frase = sig.strip().startswith('"')
        if all(" = " in i for i in itens):                       # modo livre / frase
            c["tp"] = "f" if frase else "l"
            for i in itens:
                a, b = i.split(" = ", 1); c["k"].append([a.strip(), b.strip()])
                if c.get("f") and base(first(a)) != base(first(b)): erros.append(f"frase: '{a}' ≠ '{b[:25]}' em {c['t']}")
        else:                                                      # modo sigla (validado)
            U = units(c["m"])
            if len(U) != len(itens): erros.append(f"{c['m']}: {len(U)} letras × {len(itens)} itens — {c['t']}"); continue
            for u, i in zip(U, itens):
                f = first(i)
                ok = (f == u) if u[0].isdigit() else (base(f) == base(u)) if f else False
                if not ok: erros.append(f"{c['m']}: letra '{u}' ≠ item '{i[:30]}'")
                c["k"].append([u.upper() if not u[0].isdigit() else u, i])
        if len(c["k"]) < 2: erros.append(f"menos de 2 itens: {c['t']}")
        if c["o"] not in "co": erros.append(f"origem inválida: {c['t']}")
        c["id"] = "n" + ("t" if div == "temi" else "r") + hashlib.md5((div + c["t"]).encode()).hexdigest()[:6]
        for z in ("raw", "f"): c.pop(z, None)
    return out

def load():
    erros, data = [], {"temi": [], "r3": []}
    for div, pat in (("temi", "mt[0-9][0-9].py"), ("r3", "mr[0-9][0-9].py")):
        for f in sorted(glob.glob(os.path.join(HERE, pat))):
            data[div] += parse(importlib.import_module(os.path.basename(f)[:-3]).TXT, div, erros)
    seen = {}
    for div in data:
        for c in data[div]:
            if "id" not in c: continue
            for key in (("id", c["id"]), ("título", div + c["t"].lower()), ("sigla+itens", c["m"] + "|" + "|".join(k[1] for k in c["k"]))):
                if key in seen: erros.append(f"duplicado ({key[0]}): {c['t']}")
                seen[key] = 1
            if not c["tema"]: erros.append(f"sem tema: {c['t']}")
    return data, erros

def apkg(data, path):
    import genanki
    css = (".card{font-family:Inter,Arial,sans-serif;font-size:19px;background:#0b0e13;color:#ece8dc;text-align:left;padding:14px}"
           ".tm{display:inline-block;font-size:12px;padding:2px 10px;border-radius:20px;background:#1d2a36;color:#4dd4ff}"
           ".q{font-size:21px;font-weight:700;color:#e8c56a;margin:10px 0}.mn{font:700 34px Georgia,serif;letter-spacing:3px;color:#d4af37;text-align:center;margin:12px 0}"
           "table{border-collapse:collapse;width:100%}td{padding:6px 8px;border-bottom:1px solid #22303c;vertical-align:top}"
           "td.l{font-weight:700;color:#4dd4ff;white-space:nowrap}.x{margin-top:12px;padding:10px;border-left:4px solid #ffc14d;background:#1a1608;color:#ffd98a}.o{margin-top:8px;font-size:12px;color:#9aa4b2}")
    model = genanki.Model(1607392601, "CÓDICE 360X · Mnemônico", fields=[{"name": n} for n in ("Titulo", "Sigla", "Itens", "Dica", "Tema", "Origem")],
        templates=[{"name": "Mnemônico", "qfmt": '<span class="tm">{{Tema}}</span><div class="q">🧠 Qual é o mnemônico?<br>{{Titulo}}</div>',
                    "afmt": '{{FrontSide}}<hr id="answer"><div class="mn">{{Sigla}}</div>{{Itens}}{{#Dica}}<div class="x">🎯 {{Dica}}</div>{{/Dica}}<div class="o">{{Origem}}</div>'}], css=css)
    esc = lambda s: s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    decks, root = {}, {"temi": "🏥 TEMI 2028::🧠 Mnemônicos 360X", "r3": "🩺 R3 Clínica Médica::🧠 Mnemônicos 360X"}
    for div in ("temi", "r3"):
        for c in data[div]:
            dn = f"{root[div]}::{c['tema']}"
            dk = decks.setdefault(dn, genanki.Deck(int(hashlib.md5(dn.encode()).hexdigest()[:8], 16) + 1_400_000_000, dn))
            itens = "<table>" + "".join(f'<tr><td class="l">{esc(a)}</td><td>{esc(b)}</td></tr>' for a, b in c["k"]) + "</table>"
            dk.add_note(genanki.Note(model=model, fields=[esc(c["t"]), esc(c["m"]), itens, esc(c["x"]), esc(c["tema"]), "Clássico" if c["o"] == "c" else "Original 360X"],
                                     tags=["MN360X", "TEMI" if div == "temi" else "R3"], guid=genanki.guid_for("mn360x", c["id"])))
    genanki.Package(list(decks.values())).write_to_file(path)

if __name__ == "__main__":
    data, erros = load()
    for div in data:
        temas = {}
        for c in data[div]: temas[c["tema"]] = temas.get(c["tema"], 0) + 1
        tp = {t: sum(1 for c in data[div] if c["tp"] == t) for t in "afl"}
        print(div, len(data[div]), "| sigla validada", tp["a"], "· frase", tp["f"], "· livre", tp["l"], "| clássicos", sum(c["o"] == "c" for c in data[div]))
        for t, n in temas.items(): print("   ", n, t)
    print("ERROS", len(erros))
    for e in erros: print("  ✗", e)
    if erros or "--check" in sys.argv: sys.exit(1 if erros else 0)
    total = sum(len(v) for v in data.values())
    json.dump({"versao": "2026.11.11-mn", "temi": data["temi"], "r3": data["r3"]}, open(f"{OUT}/data/mnemonicos.json", "w", encoding="utf8"), ensure_ascii=False, separators=(",", ":"))
    apkg(data, f"{OUT}/downloads/Mnemonicos_360X_{total}.apkg")
    print("ok", total, os.path.getsize(f"{OUT}/data/mnemonicos.json"), "bytes")
