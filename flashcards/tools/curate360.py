"""Curadoria da coleção IAs 360X → coleção 'ia360c' (revisada).
Funde os 10 ângulos de cada conceito em 1 card completo + 1 card de aprofundamento;
aplica correções manuais (cur_fix.py) e só inclui temas listados em DONE (lidos e revisados)."""
import json, glob, re, os, sys
OUT = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/app2"
from cur_fix import FIX, DROP, EXTRA, DONE, DONE_R3
TAG = re.compile(r"^<div style='font-size:13px;opacity:.8'>(.*?)</div>")
strip = lambda h: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h or "")).strip()
ROWS = [("ENTENDER", "🧠 Mecanismo"), ("IDENTIFICAR", "🔎 Achado-chave"), ("VERIFICAR", "🧪 Verificar"), ("DECIDIR", "✅ Conduta"),
        ("EVITAR", "⚠️ Evitar"), ("MONITORAR", "📊 Monitorar"), ("PREVER", "🚨 Complicação"), ("DIFERENCIAR", "🔀 Diferencial")]

def parts(c):
    m = TAG.match(c["frente"]); tag = strip(m.group(1)) if m else ""
    front = TAG.sub("", c["frente"]).strip()
    v = c["verso"][2:] if c["verso"].startswith("✅ ") else c["verso"]
    imgs = re.findall(r"<img[^>]*data-m=\"[^\"]+\"[^>]*>", v)
    ans = re.split(r"<table|<img|<div class=\"imgcap", v)[0].strip()
    return tag, front, ans, imgs

NORM = [("a platô", "o platô"), ("A platô", "O platô"), ("Platô elevada", "Platô elevado"), ("toda platô alta", "todo platô alto"), ("platô elevada", "platô elevado")]
def clean_ans(a):
    a = re.sub(r"\s*Esquema (didático|autoral)[^.]*\.?", "", a)
    a = re.sub(r"<(?=\s?\d)", "&lt;", a)
    for x, y in NORM: a = a.replace(x, y)
    return a.strip()

def curate(path):
    d = json.load(open(path)); tema = d["baralho"].split("::")[-1]
    groups, extras, cur = [], [], None
    for c in d["cards"]:
        tag, front, ans, imgs = parts(c); T = tag.split(" ")[-1].upper() if tag else ""
        if T == "RECONHECER":
            cur = {"sub": c["subtema"], "front": front, "ans": clean_ans(ans), "rows": {}, "imgs": list(imgs), "fonte": c["fonte"], "concept": None, "deep": None}
            groups.append(cur)
        elif cur and T in dict(ROWS):
            cur["rows"][T] = clean_ans(ans); cur["imgs"] += imgs
            if T == "ENTENDER": cur["concept"] = strip(front).split(":")[0].strip()
        elif cur and T == "APROFUNDAR":
            q = re.sub(r"^.*? — ", "", strip(front)) if " — " in strip(front) else strip(front)
            cur["deep"] = (q, clean_ans(ans)); cur["imgs"] += imgs
        elif tag.endswith("Aprofundamento"):
            extras.append({"sub": c["subtema"], "front": strip(front), "ans": clean_ans(ans), "fonte": c["fonte"]})
        # 'Reconhecimento' (cenário → nome do conceito) é redundante com RECONHECER → descartado
    cards = []
    for i, g in enumerate(groups):
        key = f"{tema}#{i}"
        if key in DROP: continue
        fx = FIX.get(key, {})
        tab = "<table class=t>" + "".join(f"<tr><th>{lab}</th><td>{fx.get(T, g['rows'].get(T, '—'))}</td></tr>" for T, lab in ROWS if fx.get(T, g['rows'].get(T))) + "</table>"
        img = sorted(set(g["imgs"]))[:1] or ([f'<img data-m="{fx["img"]}">'] if fx.get("img") else [])
        verso = f"<b>{fx.get('ans', g['ans'])}</b>" + tab + "".join(img)
        nota = fx.get("nota", "")
        cards.append({"subtema": g["sub"], "frente": clean_ans(fx.get("front", g["front"])), "verso": verso, "pegadinha": nota,
                      "fonte": re.sub(r"\s*·\s*⚠️ Gerado por outra IA · não revisado", "", g["fonte"]) + " · ✅ revisado/curado por Claude", "tags": ["IA360C", "TEMI"], "_k": key})
        if g["deep"] and f"{key}d" not in DROP:
            q, a = g["deep"]; fd = FIX.get(f"{key}d", {})
            cards.append({"subtema": g["sub"], "frente": "🎯 " + fd.get("front", q), "verso": f"<b>{fd.get('ans', a)}</b>", "pegadinha": fd.get("nota", f"Conceito: {g['concept'] or ''}"),
                          "fonte": cards[-1]["fonte"], "tags": ["IA360C", "TEMI"], "_k": f"{key}d"})
    deep_txt = " ".join(strip(c["verso"]) for c in cards)
    for j, e in enumerate(extras):
        num = re.findall(r"\d+[,.]?\d*", e["ans"])[:1]
        if num and num[0] in deep_txt or f"{tema}#x{j}" in DROP: continue
        cards.append({"subtema": e["sub"], "frente": "🧮 " + e["front"], "verso": f"<b>{e['ans']}</b>", "pegadinha": "", "fonte": e["fonte"] + " · ✅ revisado", "tags": ["IA360C", "TEMI"], "_k": f"{tema}#x{j}"})
    for x in EXTRA.get(tema, []): cards.append(dict(x, fonte=x.get("fonte", "") + " · ✅ acrescentado na curadoria", tags=["IA360C", "TEMI"]))
    return d, tema, cards

def curate_flat(path):
    """Blocos R3 (1 conceito por card): só revisão — remove duplicatas (DROP 'tema#i') e aplica FIX."""
    d = json.load(open(path)); tema = d["baralho"].split("::")[-1]; cards = []; seen = set()
    for i, c in enumerate(d["cards"]):
        key = f"{tema}#{i}"
        if key in DROP: continue
        fx = FIX.get(key, {}); tag, front, ans, imgs = parts(c)
        v = c["verso"][2:] if c["verso"].startswith("✅ ") else c["verso"]
        v = re.sub(r'<div class="(imgcap|source-note)">.*?</div>', "", v)
        v = re.sub(r"<p>🧠 Fundamento fisiopatológico e semiológico;.*?</p>", "", v)   # rodapé genérico repetido
        for t in re.findall(r"<table>.*?</table>", v):                                  # tabela idêntica: só no 1º card
            if t in seen: v = v.replace(t, "")
            seen.add(t)
        v = clean_ans(v)
        cards.append({"subtema": c["subtema"], "frente": clean_ans(fx.get("front", front)), "verso": "✅ " + fx.get("ans", v), "pegadinha": fx.get("nota", ""),
                      "fonte": re.sub(r"\s*·\s*⚠️ Gerado por outra IA · não revisado", "", c["fonte"]) + " · ✅ revisado por Claude", "tags": ["IA360C", "R3"], "_k": key})
    return d, tema, cards

if __name__ == "__main__":
    idx = json.load(open(f"{OUT}/data/index.json"))
    files, removed = [], []
    for path in sorted(glob.glob(f"{OUT}/data/decks/ia360-temi-2028-*.json")):
        num = re.search(r"ia360-temi-2028-(\d\d)-", path)
        if not num or num.group(1) not in DONE: continue
        d, tema, cards = curate(path)
        _save = True
        media = sorted({m for c in cards for m in re.findall(r'data-m="([^"]+)"', c["verso"])})
        fn = os.path.basename(path).replace("ia360-", "ia360c-")
        for c in cards: c.pop("_k", None)
        json.dump({"formato": "codice360x-v1", "baralho": f"IAs 360X ✅ curados::TEMI 2028::{tema}", "cards": cards, "midia": {m: f"data/media/{m}" for m in media}},
                  open(f"{OUT}/data/decks/{fn}", "w"), ensure_ascii=False)
        files.append({"colecao": "ia360c", "arquivo": f"data/decks/{fn}", "tema": "IAs 360X ✅ › " + tema, "cards": len(cards), "subtemas": sorted({c["subtema"] for c in cards})})
        removed.append(f"data/decks/{os.path.basename(path)}")
        print(f"{tema}: {len(d['cards'])} → {len(cards)}")
    for path in sorted(glob.glob(f"{OUT}/data/decks/ia360-r3-*.json")):
        num = re.search(r"ia360-r3-clnica-mdica-(\d\d)-", path)
        if not num or num.group(1) not in DONE_R3: continue
        d, tema, cards = curate_flat(path)
        for c in cards: c.pop("_k", None)
        media = sorted({m for c in cards for m in re.findall(r'data-m="([^"]+)"', c["verso"])})
        fn = os.path.basename(path).replace("ia360-", "ia360c-")
        json.dump({"formato": "codice360x-v1", "baralho": f"IAs 360X ✅ curados::R3 Clínica Médica::{tema}", "cards": cards, "midia": {m: f"data/media/{m}" for m in media}},
                  open(f"{OUT}/data/decks/{fn}", "w"), ensure_ascii=False)
        files.append({"colecao": "ia360c", "arquivo": f"data/decks/{fn}", "tema": "IAs 360X ✅ › R3 › " + tema, "cards": len(cards), "subtemas": sorted({c["subtema"] for c in cards})})
        removed.append(f"data/decks/{os.path.basename(path)}")
        print(f"R3 {tema}: {len(d['cards'])} → {len(cards)}")
    # tira da coleção bruta os temas já curados (evita duplicar)
    idx["decks"] = [x for x in idx["decks"] if x["arquivo"] not in removed and x.get("colecao") != "ia360c"] + files
    raw = sum(x["cards"] for x in idx["decks"] if x.get("colecao") == "ia360")
    for c in idx["colecoes"]:
        if c["id"] == "ia360": c["cards"] = raw
    idx["colecoes"] = [c for c in idx["colecoes"] if c["id"] != "ia360c"]
    pos = next(i for i, c in enumerate(idx["colecoes"]) if c["id"] == "ia360")
    idx["colecoes"].insert(pos, {"id": "ia360c", "nome": "IAs 360X ✅ curados", "icone": "✅", "cards": sum(f["cards"] for f in files)})
    json.dump(idx, open(f"{OUT}/data/index.json", "w"), ensure_ascii=False, indent=1)
    print("curados", sum(f["cards"] for f in files), "| brutos restantes", raw)
