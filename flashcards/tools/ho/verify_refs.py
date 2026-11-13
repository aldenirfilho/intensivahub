"""Conferência card × texto-fonte das referências da aba Honra (4.9.0: 352/352).

Uso: python3 -I tools/ho/verify_refs.py <pasta_fontes> [tradicao]
<pasta_fontes>: almeida_acf.json, bom.json, dc.json, quran_nasr.json, lunyu.json,
pali/*.json (bilara/Sujato), sef/*.json (API v3 da Sefaria). Lê os c_*.py desta pasta."""
import json, re, sys, os, glob, importlib.util

SRC = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
cards = []
for f in ["c_biblia", "c_tora", "c_mormon", "c_alcorao", "c_buda", "c_confucio", "c_pontes"]:
    s = importlib.util.spec_from_file_location(f, os.path.join(HERE, f + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
    for v in vars(m).values():
        if isinstance(v, list) and v and isinstance(v[0], tuple):
            cards += [{"f": f, "i": i, "ref": t[1], "q": t[2], "e": t[3]} for i, t in enumerate(v)]

alm = json.load(open(os.path.join(SRC, "almeida_acf.json"), encoding="utf-8-sig"))
BIB = {b["name"]: b for b in alm}
ABR = {"Mt": "Mateus", "Êx": "Êxodo", "1Tm": "1 Timóteo", "Pv": "Provérbios", "Rm": "Romanos",
       "Sl": "Salmos", "Lc": "Lucas", "Gn": "Gênesis", "Tg": "Tiago", "Miqueias": "Miquéias"}
bom = json.load(open(os.path.join(SRC, "bom.json")))
BOM = {b["book"]: b for b in bom["books"]}
MOR = {"1 Néfi": "1 Nephi", "2 Néfi": "2 Nephi", "3 Néfi": "3 Nephi", "Jacó": "Jacob", "Enos": "Enos",
       "Mosias": "Mosiah", "Alma": "Alma", "Helamã": "Helaman", "Éter": "Ether", "Morôni": "Moroni"}
dc = json.load(open(os.path.join(SRC, "dc.json")))
DC = {s["section"]: s for s in dc["sections"]}
qn = json.load(open(os.path.join(SRC, "quran_nasr.json")))["quran"]
QN = {(x["chapter"], x["verse"]): x["text"] for x in qn}
lun = json.load(open(os.path.join(SRC, "lunyu.json")))
DHP = {}
for f in glob.glob(os.path.join(SRC, "pali", "dhp*.json")):
    for k, v in json.load(open(f)).items():
        m = re.match(r"dhp(\d+):(\d+)", k)
        if m and int(m.group(2)) >= 1:
            DHP.setdefault(int(m.group(1)), []).append(v)


def vrange(s):
    a, _, b = s.partition("-")
    return list(range(int(a), int(b or a) + 1))


def bible(book, cv):
    b = BIB.get(ABR.get(book, book))
    if not b:
        return None
    c, v = cv.split(":")
    ch = b["chapters"][int(c) - 1]
    return " ".join(f"[{i}] " + ch[i - 1] for i in vrange(v) if i <= len(ch))


def bomtxt(book, cv):
    b = BOM[MOR[book]]
    c, v = cv.split(":")
    ch = b["chapters"][int(c) - 1]["verses"]
    return " ".join(f"[{i}] " + ch[i - 1]["text"] for i in vrange(v))


def dctxt(cv):
    c, v = cv.split(":")
    vs = DC[int(c)]["verses"]
    return " ".join(f"[{i}] " + vs[i - 1]["text"] for i in vrange(v))


def quran(cv):
    c, v = cv.split(":")
    return " ".join(f"[{i}] " + QN.get((int(c), i), "??") for i in vrange(v))


def lunyu(cv):
    c, v = cv.split(":")
    p = lun[int(c) - 1]["paragraphs"]
    i = int(v)
    return " || ".join(f"<{j}> " + p[j - 1] for j in (i - 1, i, i + 1) if 1 <= j <= len(p))


def dhp(v):
    return " ".join(f"[{i}] " + " ".join(DHP.get(i, ["??"])).strip() for i in vrange(v))


def sutta(code):
    f = os.path.join(SRC, "pali", code + ".json")
    t = " ".join(json.load(open(f)).values())
    return f"({len(t)} chars) " + t[:260]


def sef(name):
    f = os.path.join(SRC, "sef", name + ".json")
    if not os.path.exists(f):
        return None
    t = json.load(open(f))["versions"][0]["text"]
    return t


def strip(h):
    return re.sub(r"<[^>]+>", "", h)


def resolve(ref):
    r = ref.strip()
    m = re.match(r"(?:Mishná,?\s*)?Sanhedrin 4:5", r)
    if m:
        return "SEF " + strip(" ".join(sef("Mishnah_Sanhedrin.4.5") if isinstance(sef("Mishnah_Sanhedrin.4.5"), list) else [sef("Mishnah_Sanhedrin.4.5")]))[:700]
    if "Shabat 31a" in r:
        t = sef("Shabbat.31a")
        t = strip(" ".join(t))
        i = t.find("hateful")
        return "SEF …" + t[max(0, i - 500):i + 200]
    m = re.match(r"(?:Pirkei )?Avot (\d+):(\d+)", r)
    if m:
        t = sef(f"Pirkei_Avot.{m.group(1)}")
        n = int(m.group(2))
        return "SEF " + " || ".join(f"<{j}> " + strip(t[j - 1]) for j in (n - 1, n, n + 1) if 1 <= j <= len(t))
    m = re.match(r"Alcorão (\d+:[\d-]+)", r)
    if m:
        return "NASR " + quran(m.group(1))
    m = re.match(r"D&C (\d+:[\d-]+)|Doutrina e Convênios (\d+:[\d-]+)", r)
    if m:
        return "DC " + dctxt(m.group(1) or m.group(2))
    m = re.match(r"Analectos (\d+:\d+)", r)
    if m:
        return "LUNYU " + lunyu(m.group(1))
    m = re.match(r"Dhammapada ([\d-]+)", r)
    if m:
        return "DHP " + dhp(m.group(1))
    m = re.search(r"\((AN|SN|MN|DN|Sn) ([\d.]+)\)|^(MN|DN|SN|AN) ([\d.]+)$", r)
    if m:
        k = (m.group(1) or m.group(3)).lower().replace("sn", "sn") + (m.group(2) or m.group(4))
        if (m.group(1) or "") == "Sn":
            k = "snp" + m.group(2)
        return "SUTTA " + sutta(k)
    m = re.match(r"(.+?) (\d+:[\d-]+)$", r)
    if m:
        bk = m.group(1)
        if bk in MOR:
            return "BOM " + bomtxt(bk, m.group(2))
        t = bible(bk, m.group(2))
        if t:
            return "ACF " + t
    return "?? sem fonte automática"


only = sys.argv[2] if len(sys.argv) > 2 else None
for c in cards:
    if only and c["f"] != only:
        continue
    parts = c["ref"].split(" · ") if c["f"] == "c_pontes" else [c["ref"]]
    print(f"### {c['f'][2:]}#{c['i']} | {c['ref']}")
    print("  CARD:", c["e"][:220])
    for p in parts:
        try:
            print("  >", p, "=>", resolve(p)[:600])
        except Exception as ex:
            print("  >", p, "=> ERRO", type(ex).__name__, ex)
