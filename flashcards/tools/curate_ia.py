"""Curadoria de 'Outras IAs' → coleção 'iac' (Outras IAs ✅ curadas).
Lote 1: TEMI 360X 3000 (ia-a-*) — 10 ângulos por conceito fundidos em 1 card + 1 🎯;
conceitos já presentes em IAs 360X ✅ curados (ia360c) são descartados como duplicatas."""
import json, glob, re, os, sys
OUT = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/app2"
DUMP = "--dump" in sys.argv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cur_fix_ia import FIX, DROP, DONE_IA, NAMED_B
st = lambda h: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h or "")).strip()
ROWS = [("ENTENDER", "🧠 Mecanismo"), ("IDENTIFICAR", "🔎 Achado-chave"), ("VERIFICAR", "🧪 Verificar"), ("DECIDIR", "✅ Conduta"),
        ("EVITAR", "⚠️ Evitar"), ("MONITORAR", "📊 Monitorar"), ("PREVER", "🚨 Complicação"), ("DIFERENCIAR", "🔀 Diferencial")]
def ans_of(v): return re.split(r"<br><table|<table|<img|<div", v)[0].strip()
def clean(a):
    a = re.sub(r"\s*Esquema (didático|autoral)[^.]*\.?", "", a); a = re.sub(r"<(?=\s?\d)", "&lt;", a); return a.strip()

def known():
    T = []
    for f in glob.glob(f"{OUT}/data/decks/ia360c-temi-2028-*.json"):
        for c in json.load(open(f))["cards"]: T.append(st(c["frente"] + " | " + c["verso"]).lower())
    return " ¦ ".join(T)

def is_dup(g, C):
    if g["ans"].lower() in C: return True
    hits = sum(1 for v in g["rows"].values() if len(v) > 12 and st(v).lower() in C)
    deep = g["deep"] and len(g["deep"][1]) > 8 and st(g["deep"][1]).lower() in C
    return hits >= 4 or (deep and hits >= 2)

def groups_of(path):
    d = json.load(open(path)); G = []; cur = None
    for c in d["cards"]:
        m = re.match(r"<span class=pill>\S+ (\w+)</span>\s*", c["frente"]); T = m.group(1) if m else ""
        front = c["frente"][m.end():] if m else c["frente"]
        a = clean(ans_of(c["verso"])); imgs = re.findall(r'<img[^>]*data-m="[^"]+"[^>]*>', c["verso"])
        if T == "RECONHECER":
            cur = {"sub": c["subtema"], "front": front, "ans": a, "rows": {}, "imgs": imgs, "fonte": c["fonte"], "deep": None}; G.append(cur)
        elif cur and T in dict(ROWS): cur["rows"][T] = a; cur["imgs"] += imgs
        elif cur and T == "APROFUNDAR":
            q = front.split(" — ", 1)[1] if " — " in front else front; cur["deep"] = (q, a)
    return d, G

def curate_flat_b(path, key_pref):
    d = json.load(open(path)); cards = []
    for i, c in enumerate(d["cards"]):
        key = f"{key_pref}#{i}"
        if key in DROP: continue
        fx = FIX.get(key, {})
        v = c["verso"]
        if "ans" in fx:
            imgs = "".join(re.findall(r'<img[^>]*data-m="[^"]+"[^>]*>', v)); v = "✅ " + fx["ans"] + imgs
        nota = fx.get("nota", c.get("pegadinha", ""))
        cards.append({"subtema": c["subtema"], "frente": fx.get("front", c["frente"]), "verso": v, "pegadinha": nota,
                      "fonte": re.sub(r"\s*·\s*⚠️ gerado por outra IA — não revisado", "", c["fonte"]) + " · ✅ revisado/corrigido por Claude", "tags": ["IAC"] + [t for t in c.get("tags", []) if t in ("TEMI", "R3")]})
    return d, cards

if __name__ == "__main__":
    C = known(); idx = json.load(open(f"{OUT}/data/index.json"))
    if not any(c["id"] == "iac" for c in idx["colecoes"]):
        pos = [c["id"] for c in idx["colecoes"]].index("ia")
        idx["colecoes"].insert(pos, {"id": "iac", "nome": "Outras IAs ✅ curadas", "icone": "🧹", "descricao": "Cards de outras IAs revisados por Claude: duplicatas removidas, ângulos fundidos, correções aplicadas."})
    files, removed, dump, stats = [], [], [], [0, 0, 0]
    for path in sorted(glob.glob(f"{OUT}/data/decks/ia-a-*.json")):
        num = re.search(r"ia-a-(\d\d)-", path).group(1)
        d, G = groups_of(path); tema = d["baralho"].split("::")[-1]; cards = []
        for i, g in enumerate(G):
            key = f"A{num}#{i}"; stats[0] += 1
            if is_dup(g, C) or key in DROP: stats[1] += 1; continue
            fx = FIX.get(key, {})
            if DUMP: dump.append(f"{key} [{tema} / {g['sub']}] Q: {st(g['front'])}\n  A: {st(g['ans'])}\n" + "".join(f"  {lab}: {st(g['rows'].get(T,''))}\n" for T, lab in ROWS) + (f"  🎯 {st(g['deep'][0])} → {st(g['deep'][1])}\n" if g['deep'] else "") + f"  F: {g['fonte'][:70]}")
            tab = "<table class=t>" + "".join(f"<tr><th>{lab}</th><td>{fx.get(T, g['rows'].get(T))}</td></tr>" for T, lab in ROWS if fx.get(T, g['rows'].get(T))) + "</table>"
            img = sorted(set(g["imgs"]))[:1]
            fonte = re.sub(r"\s*·\s*⚠️ gerado por outra IA — não revisado", "", g["fonte"]) + " · ✅ revisado/curado por Claude"
            cards.append({"subtema": g["sub"], "frente": fx.get("front", g["front"]), "verso": f"<b>{fx.get('ans', g['ans'])}</b>" + tab + "".join(img), "pegadinha": fx.get("nota", ""), "fonte": fonte, "tags": ["IAC", "TEMI"]})
            if g["deep"] and key + "d" not in DROP:
                fd = FIX.get(key + "d", {}); q, a = g["deep"]
                cards.append({"subtema": g["sub"], "frente": "🎯 " + fd.get("front", f"{g['ans']} — {q}"), "verso": f"<b>{fd.get('ans', a)}</b>", "pegadinha": fd.get("nota", ""), "fonte": fonte, "tags": ["IAC", "TEMI"]})
        stats[2] += len(cards)
        if "A" not in DONE_IA: continue
        removed.append(f"data/decks/{os.path.basename(path)}")
        if not cards: continue
        fn = os.path.basename(path).replace("ia-a-", "iac-a-")
        media = sorted({m for c in cards for m in re.findall(r'data-m="([^"]+)"', c["verso"])})
        json.dump({"formato": "codice360x-v1", "baralho": f"Outras IAs ✅ curadas::TEMI 360X 3000::{tema}", "cards": cards, "midia": {m: f"data/media/{m}" for m in media}}, open(f"{OUT}/data/decks/{fn}", "w"), ensure_ascii=False)
        files.append({"colecao": "iac", "arquivo": f"data/decks/{fn}", "tema": "Outras IAs ✅ › TEMI 360X 3000 › " + tema, "cards": len(cards), "subtemas": sorted({c["subtema"] for c in cards})})
    for path in sorted(glob.glob(f"{OUT}/data/decks/ia-b-temi-2028-*.json")):
        m = re.search(r"ia-b-temi-2028-(\d\d)-", path); slug = os.path.basename(path)[len("ia-b-temi-2028-"):-5]
        kp = f"B{m.group(1)}" if m else NAMED_B.get(slug)
        if not kp or kp not in DONE_IA: continue
        d, cards = curate_flat_b(path, kp); tema = d["baralho"].split("::")[-1]
        removed.append(f"data/decks/{os.path.basename(path)}"); fn = os.path.basename(path).replace("ia-b-", "iac-b-")
        media = sorted({x for c in cards for x in re.findall(r'data-m="([^"]+)"', c["verso"])})
        json.dump({"formato": "codice360x-v1", "baralho": f"Outras IAs ✅ curadas::TEMI 2028::{tema}", "cards": cards, "midia": {x: f"data/media/{x}" for x in media}}, open(f"{OUT}/data/decks/{fn}", "w"), ensure_ascii=False)
        files.append({"colecao": "iac", "arquivo": f"data/decks/{fn}", "tema": "Outras IAs ✅ › TEMI 2028 › " + tema, "cards": len(cards), "subtemas": sorted({c["subtema"] for c in cards})})
        print(f"{tema}: {len(d['cards'])} → {len(cards)}")
    if DUMP: open("/home/claude/imp/iaA_unique.txt", "w").write("\n".join(dump))
    print("conceitos", stats[0], "duplicados", stats[1], "cards curados", stats[2])
    if DONE_IA and not DUMP:
        idx["decks"] = [x for x in idx["decks"] if x["arquivo"] not in removed and x["colecao"] != "iac"] + files
        for col in idx["colecoes"]: col["cards"] = sum(x["cards"] for x in idx["decks"] if x["colecao"] == col["id"])
        idx["colecoes"] = [c for c in idx["colecoes"] if c["cards"] or c["id"] not in ("iac", "ia")]
        json.dump(idx, open(f"{OUT}/data/index.json", "w"), ensure_ascii=False, indent=1)
