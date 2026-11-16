"""Conferência card × texto-fonte das referências de 📜 Escrituras & Axiomas 360X.

Uso: python3 -I verify_escr.py <cards.json> <pasta_fontes> [saida.json]

Fontes esperadas em <pasta_fontes> (todas públicas, baixadas do GitHub ou do bucket da Sefaria):
  acf.json (Almeida Corrigida Fiel, thiagobodruk/biblia) · quran_nasr.json (Helmi Nasr, fawazahmed0/quran-api)
  sefj/*.json (Sefaria, inglês) · bil/ (SuttaCentral bilara-data, Sujato/Brahmali)
  cp/论语/lunyu.json e cp/四书五经/*.json (chinese-poetry) · gita_verse.json + gita_tr.json (gita/gita)
  book-of-mormon.json e doctrine-and-covenants.json (bcbooks/scriptures-json)

Para cada card com fonte automática: confere se o trecho existe e mede a sobreposição de palavras
(só nas fontes em português: Bíblia e Alcorão). Saída: JSON com status por card
(ok · revisar · inexistente · sem_fonte) e o trecho da fonte, para a revisão humana."""
import glob
import json
import os
import re
import sys
import unicodedata

CARDS, SRC = sys.argv[1], sys.argv[2]
OUT = sys.argv[3] if len(sys.argv) > 3 else "verificacao.json"
cards = json.load(open(CARDS))


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(ch for ch in s if unicodedata.category(ch) != "Mn")


STOP = set(norm(w) for w in """que dos das para com por uma como mais não nao seu sua seus suas ele ela eles elas isso
este esta estes estas esse essa pelo pela pelos pelas aos nos nas sobre quem qual quando onde porque pois então
entao também tambem tudo todo toda todos todas mas sem até ate sao são ser foi tem têm vos lhe lhes meu minha teu tua
vosso vossa nosso nossa ao se de do da em no na os as um o a e é dele dela deles delas aquele aquela isto aquilo
há ha haja será sera seja sejam""".split())


def toks(s):
    w = re.findall(r"[a-z]+", norm(s))
    return {x[:5] for x in w if len(x) >= 4 and x not in STOP}


def overlap(card_txt, src_txt):
    a, b = toks(card_txt), toks(src_txt)
    return round(len(a & b) / max(1, len(a)), 2)


def vrange(s):
    a, _, b = s.partition("-")
    return list(range(int(a), int(b or a) + 1))


# ---------- Bíblia (ACF) ----------
alm = json.load(open(os.path.join(SRC, "acf.json"), encoding="utf-8-sig"))
BIB = {b["name"]: b for b in alm}
ALIAS = {"Oseias": "Oséias", "Miqueias": "Miquéias", "Lamentações": "Lamentações de Jeremias",
         "Cântico dos Cânticos": "Cânticos", "Cantares": "Cânticos", "Eclesiastes": "Eclesiastes",
         "Filemon": "Filemom", "Deuteronômio": "Deuteronômio"}


def bible(book, cv):
    b = BIB.get(ALIAS.get(book, book))
    if not b:
        return None, "livro?"
    c, _, v = cv.partition(":")
    c = int(c)
    if c < 1 or c > len(b["chapters"]):
        return "", "capítulo inexistente"
    ch = b["chapters"][c - 1]
    vs = vrange(v) if v else list(range(1, len(ch) + 1))
    if any(i > len(ch) or i < 1 for i in vs):
        return "", "versículo inexistente"
    return " ".join(f"[{i}] " + ch[i - 1] for i in vs), ""


# ---------- Alcorão (Helmi Nasr) ----------
QN = {(x["chapter"], x["verse"]): x["text"] for x in json.load(open(os.path.join(SRC, "quran_nasr.json")))["quran"]}


def quran(cv):
    c, v = cv.split(":")
    vs = vrange(v)
    if any((int(c), i) not in QN for i in vs):
        return "", "versículo inexistente"
    return " ".join(f"[{i}] " + QN[(int(c), i)] for i in vs), ""


# ---------- Sefaria ----------
def strip(h):
    return re.sub(r"<[^>]+>", " ", h)


SEF = {}


def sef(name):
    if name not in SEF:
        f = os.path.join(SRC, "sefj", name + ".json")
        SEF[name] = json.load(open(f))["text"] if os.path.exists(f) else None
    return SEF[name]


def avot(c, v):
    t = sef("Pirkei_Avot")
    try:
        return " || ".join(f"<{j}> " + strip(t[c - 1][j - 1]) for j in (v - 1, v, v + 1) if 1 <= j <= len(t[c - 1])), ""
    except IndexError:
        return "", "trecho inexistente"


def talmud(tract, daf):
    t = sef(tract.replace(" ", "_"))
    if t is None:
        return None, "sem fonte"
    m = re.match(r"(\d+)([ab])", daf)
    i = (int(m.group(1)) - 1) * 2 + (0 if m.group(2) == "a" else 1)
    if i >= len(t) or not t[i]:
        return "", "fólio inexistente"
    return strip(" ".join(t[i]))[:4000], ""


TRACT = {"Shabat": "Shabbat", "Sanhedrin": "Sanhedrin", "Bava Metzia": "Bava Metzia", "Taanit": "Taanit",
         "Nedarim": "Nedarim", "Sotá": "Sotah", "Yoma": "Yoma", "Kidushin": "Kiddushin", "Sucá": "Sukkah",
         "Bava Batra": "Bava Batra", "Eruvin": "Eruvin", "Ketubot": "Ketubot"}

# ---------- Pali (bilara) ----------
BIL = os.path.join(SRC, "bil", "translation", "en")
DHP = {}
for f in glob.glob(os.path.join(BIL, "sujato", "sutta", "kn", "dhp", "*.json")):
    for k, v in json.load(open(f)).items():
        m = re.match(r"dhp(\d+):(\d+)", k)
        if m and int(m.group(2)) >= 1:
            DHP.setdefault(int(m.group(1)), []).append(v)


def dhp(v):
    vs = vrange(v)
    if any(i not in DHP for i in vs):
        return "", "verso inexistente"
    return " ".join(f"[{i}] " + " ".join(DHP[i]).strip() for i in vs), ""


def sutta(code):
    fs = glob.glob(os.path.join(BIL, "sujato", "sutta", "**", code + "_translation-en-sujato.json"), recursive=True)
    if not fs:
        return None, "sem fonte"
    d = json.load(open(fs[0]))
    return " ".join(d.values()), ""


# ---------- Clássicos chineses ----------
CP = os.path.join(SRC, "cp")
LUN = json.load(open(os.path.join(CP, "论语", "lunyu.json")))
MENG = json.load(open(os.path.join(CP, "四书五经", "mengzi.json")))
ZY = json.load(open(os.path.join(CP, "四书五经", "zhongyong.json")))
DX = json.load(open(os.path.join(CP, "四书五经", "daxue.json")))


def lunyu(c, v):
    p = LUN[c - 1]["paragraphs"]
    if v > len(p):
        return "", "parágrafo inexistente"
    return " || ".join(f"<{j}> " + p[j - 1] for j in (v - 1, v, v + 1) if 1 <= j <= len(p)), ""


MENG_BOOK = {"1A": 0, "1B": 1, "2A": 2, "2B": 3, "3A": 4, "3B": 5, "4A": 6, "4B": 7, "5A": 8, "5B": 9, "6A": 10, "6B": 11, "7A": 12, "7B": 13}


def mengzi(code):
    m = re.match(r"(\d[AB])(\d+)", code)
    p = MENG[MENG_BOOK[m.group(1)]]["paragraphs"]
    n = int(m.group(2))
    if n > len(p):
        return "", "parágrafo inexistente"
    return f"<{MENG[MENG_BOOK[m.group(1)]]['chapter']} {n}> " + p[n - 1][:900], ""


# ---------- Gita ----------
GV = json.load(open(os.path.join(SRC, "gita_verse.json")))
GT = json.load(open(os.path.join(SRC, "gita_tr.json")))
GID = {(v["chapter_number"], v["verse_number"]): v["id"] for v in GV}
GEN = {}
for t in GT:
    if t.get("lang") == "english" and t["verse_id"] not in GEN:
        GEN[t["verse_id"]] = t["description"].strip()


def gita(cv):
    c, v = cv.split(".")
    vs = vrange(v)
    if any((int(c), i) not in GID for i in vs):
        return "", "verso inexistente"
    return " ".join(f"[{c}.{i}] " + GEN.get(GID[(int(c), i)], "??") for i in vs), ""


# ---------- Livro de Mórmon e D&C ----------
BOM = {b["book"]: b for b in json.load(open(os.path.join(SRC, "book-of-mormon.json")))["books"]}
DC = {s["section"]: s for s in json.load(open(os.path.join(SRC, "doctrine-and-covenants.json")))["sections"]}
MOR = {"1 Néfi": "1 Nephi", "2 Néfi": "2 Nephi", "3 Néfi": "3 Nephi", "Jacó": "Jacob", "Enos": "Enos",
       "Mosias": "Mosiah", "Alma": "Alma", "Helamã": "Helaman", "Éter": "Ether", "Morôni": "Moroni"}


def bom(book, cv):
    c, v = cv.split(":")
    ch = BOM[MOR[book]]["chapters"][int(c) - 1]["verses"]
    vs = vrange(v)
    if any(i > len(ch) for i in vs):
        return "", "versículo inexistente"
    return " ".join(f"[{i}] " + ch[i - 1]["text"] for i in vs), ""


def dc(cv):
    c, v = cv.split(":")
    vs_ = DC[int(c)]["verses"]
    vs = vrange(v)
    if any(i > len(vs_) for i in vs):
        return "", "versículo inexistente"
    return " ".join(f"[{i}] " + vs_[i - 1]["text"] for i in vs), ""


SUTTA = {"SN 56.11": "sn56.11", "SN 45.8": "sn45.8", "Snp 1.8": "snp1.8", "AN 3.65": "an3.65", "DN 16": "dn16",
         "SN 45.2": "sn45.2", "SN 36.6": "sn36.6", "MN 63": "mn63", "MN 22": "mn22", "AN 5.57": "an5.57",
         "DN 31": "dn31", "MN 21": "mn21", "AN 5.198": "an5.198", "MN 86": "mn86", "DN 13": "dn13",
         "MN 10": "mn10", "MN 118": "mn118"}


def resolve(ref):
    r = ref.strip()
    m = re.match(r"Pirkei Avot (\d+):(\d+)", r)
    if m:
        return ("SEF", "en") + avot(int(m.group(1)), int(m.group(2)))
    m = re.match(r"Talmude · (.+?) (\d+[ab])$", r)
    if m:
        return ("SEF", "en") + talmud(TRACT[m.group(1)], m.group(2))
    m = re.match(r"Mishná · Sanhedrin (\d+):(\d+)", r)
    if m:
        t = sef("Mishnah_Sanhedrin")
        return ("SEF", "en", strip(t[int(m.group(1)) - 1][int(m.group(2)) - 1]), "")
    m = re.match(r"Alcorão (\d+:[\d-]+)", r)
    if m:
        return ("NASR", "pt") + quran(m.group(1))
    m = re.match(r"Dhammapada ([\d-]+)$", r)
    if m:
        return ("DHP", "en") + dhp(m.group(1))
    m = re.search(r"\(((?:SN|AN|MN|DN|Snp) [\d.]+)\)", r)
    if m and m.group(1) in SUTTA:
        return ("SUTTA", "en") + sutta(SUTTA[m.group(1)])
    m = re.match(r"Analectos (\d+)\.(\d+)", r)
    if m:
        return ("LUNYU", "zh") + lunyu(int(m.group(1)), int(m.group(2)))
    m = re.match(r"Mêncio (\d[AB]\d+)", r)
    if m:
        return ("MENGZI", "zh") + mengzi(m.group(1))
    if r.startswith("Doutrina do Meio"):
        return ("ZHONGYONG", "zh", " ".join(ZY["paragraphs"])[:1500], "")
    if r.startswith("Grande Ensinamento"):
        return ("DAXUE", "zh", " ".join(DX["paragraphs"])[:1500], "")
    m = re.match(r"Bhagavad Gita (\d+\.[\d-]+)", r)
    if m:
        return ("GITA", "en") + gita(m.group(1))
    m = re.match(r"Livro de Mórmon · (.+?) (\d+:[\d-]+)", r)
    if m:
        return ("BOM", "en") + bom(m.group(1), m.group(2))
    m = re.match(r"Doutrina e Convênios (\d+:[\d-]+)", r)
    if m:
        return ("DC", "en") + dc(m.group(1))
    m = re.match(r"(.+?) (\d+:[\d-]+)$", r)
    if m:
        t, err = bible(m.group(1), m.group(2))
        if t is not None:
            return ("ACF", "pt", t, err)
    return (None, None, None, "sem fonte automática")


res = []
for c in cards:
    if c["num"] == "20":
        continue
    fonte, lingua, txt, err = resolve(c["ref"])
    st = "sem_fonte" if fonte is None or txt is None else ("inexistente" if err else "a_ler")
    sc = None
    if st == "a_ler" and lingua == "pt":
        sc = overlap(c["msg"], txt)
        st = "ok_auto" if sc >= 0.34 else "revisar"
    res.append(dict(id=c["id"], num=c["num"], ref=c["ref"], msg=c["msg"], fonte=fonte, lingua=lingua,
                    score=sc, status=st, erro=err, trecho=(txt or "")[:1200]))
json.dump(res, open(OUT, "w"), ensure_ascii=False, indent=0)
from collections import Counter
print(Counter(r["status"] for r in res))
print(Counter((r["fonte"], r["status"]) for r in res))
