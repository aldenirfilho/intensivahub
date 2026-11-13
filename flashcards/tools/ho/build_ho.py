#!/usr/bin/env python3
"""Gera data/honra.json (aba 🕊️ Honra do CÓDICE 360X).
Uso: python3 tools/ho/build_ho.py <raiz_do_app>
Confere: ids únicos, campos vazios, iniciais das siglas, perguntas e títulos repetidos, links bússola→sigla."""
import sys, os, json, hashlib, unicodedata, importlib.util, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "..")

TEMAS = {
 "af": "🌊 Aflição e angústia", "ra": "🔥 Raiva e conflito", "me": "😰 Medo e ansiedade", "de": "🧭 Decisão e discernimento",
 "di": "💰 Dinheiro e honestidade", "fa": "👪 Família e cuidado com os pais", "pe": "🕊️ Perdão e reconciliação",
 "tr": "⚒️ Trabalho e disciplina", "hu": "🙇 Humildade e orgulho", "pa": "🗣️ Palavra e silêncio",
 "es": "🌅 Esperança, luto e recomeço", "gr": "🙏 Gratidão e fé", "ju": "⚖️ Justiça e integridade", "am": "🤝 Amizade e companhias"}
TRADS = {
 "biblia":   {"n": "Bíblia", "e": "✝️", "c": "#e8c56a"},
 "tora":     {"n": "Torá e sabedoria judaica", "e": "✡️", "c": "#4dd4ff"},
 "mormon":   {"n": "Livro de Mórmon e D&C", "e": "📘", "c": "#8fb8ff"},
 "alcorao":  {"n": "Alcorão", "e": "☪️", "c": "#5be38a"},
 "buda":     {"n": "Buda", "e": "☸️", "c": "#ffc14d"},
 "confucio": {"n": "Confúcio", "e": "☯️", "c": "#ff8fb1"},
 "pontes":   {"n": "Pontes entre tradições", "e": "🌐", "c": "#b48cff"},
}

def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, name + ".py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

QUANDO = {
 "af": "Use quando a aflição apertar e for preciso estabilizar antes de agir.",
 "ra": "Use quando a raiva subir, antes de responder a qualquer provocação.",
 "me": "Use diante do medo ou da ansiedade antecipatória.",
 "de": "Use antes de decisões importantes, sobretudo sob pressão.",
 "di": "Use antes de mexer em dinheiro, contratos ou propostas.",
 "fa": "Use no cuidado diário com a família e com quem envelhece.",
 "pe": "Use quando houver mágoa, conflito ou necessidade de reparar.",
 "tr": "Use para estudar e trabalhar com constância, sem se esgotar.",
 "hu": "Use quando o ego crescer — no elogio, na crítica ou no erro.",
 "pa": "Use antes de falar, escrever ou repassar algo.",
 "es": "Use em perdas, lutos e recomeços.",
 "gr": "Use para fechar o dia e reabrir a perspectiva.",
 "ju": "Use quando a integridade estiver em jogo, mesmo sem ninguém ver.",
 "am": "Use para escolher e cultivar boas companhias."}
def ctxok(ctx, tema): return ctx if len(ctx) >= 70 else "Fonte: " + ctx.rstrip(".") + ". " + QUANDO[tema]

def h(s, n=8): return hashlib.sha1(s.encode()).hexdigest()[:n]
def nz(s): return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").upper()

err = []
cards = []
for f in ["c_biblia", "c_tora", "c_mormon", "c_alcorao", "c_buda", "c_confucio", "c_pontes"]:
    m = load(f)
    for t in m.C:
        if len(t) != 5: err.append(f"{f}: tupla com {len(t)} campos: {t[:2]}"); continue
        tema, ref, q, a, ap = t
        if tema not in TEMAS: err.append(f"{f}: tema {tema}")
        if not all(x.strip() for x in t): err.append(f"{f}: campo vazio em {ref}")
        cards.append({"id": "hc" + h(m.TRAD + ref + q), "tr": m.TRAD, "tema": TEMAS.get(tema, tema), "q": q, "a": a, "r": ref, "ap": ap})

mn = []
for ln in open(os.path.join(HERE, "m_siglas.txt"), encoding="utf-8"):
    ln = ln.rstrip("\n")
    if not ln.strip() or ln.startswith("#"): continue
    p = ln.split("|")
    if len(p) != 7 or p[0] != "A": err.append("linha inválida: " + ln[:60]); continue
    _, tema, sig, tit, its, dica, ctx = p
    items = [i.strip() for i in its.split(";")]
    letters = [c for c in nz(sig) if c.isalpha()]
    if len(letters) != len(items): err.append(f"{sig}: {len(letters)} letras × {len(items)} itens")
    else:
        for L, it in zip(letters, items):
            if nz(it)[0] != L: err.append(f"{sig}: item '{it}' não começa com {L}")
    if tema not in TEMAS: err.append(f"{sig}: tema {tema}"); continue
    ctx = ctxok(ctx, tema)
    mn.append({"id": "hm" + h("s" + sig + tit), "tema": TEMAS.get(tema, tema), "t": tit, "m": sig, "k": [[L, it] for L, it in zip(letters, items)], "x": dica, "c": ctx, "o": "o", "tp": "a"})
for tema, lab, tit, items, dica, ctx in load("m_classicos").L:
    if tema not in TEMAS: err.append(f"{tit}: tema {tema}"); continue
    ctx = ctxok(ctx, tema)
    mn.append({"id": "hm" + h("l" + tit), "tema": TEMAS.get(tema, tema), "t": tit, "m": lab, "k": [list(x) for x in items], "x": dica, "c": ctx, "o": "c", "tp": "l"})
mn.sort(key=lambda m: (list(TEMAS.values()).index(m["tema"]), m["o"] != "c", m["t"]))

bm = load("bussolas")
sigs = {m["m"] for m in mn if m["tp"] == "a"}
bu = []
for i, b in enumerate(bm.B):
    for k in ["e", "t", "sin", "N", "S", "L", "O", "q", "refs", "mn"]:
        if not b.get(k): err.append(f"bússola {b.get('t')}: falta {k}")
    for s in b["mn"]:
        if s not in sigs: err.append(f"bússola {b['t']}: sigla {s} inexistente")
    bu.append(dict(b, id="hb%02d" % (i + 1)))

# repetições
def dup(lst, key, lab):
    seen = {}
    for x in lst:
        k = key(x)
        if k in seen: err.append(f"{lab} repetido: {k}")
        seen[k] = 1
dup(cards, lambda c: c["id"], "id card"); dup(cards, lambda c: nz(c["q"]), "pergunta")
dup(mn, lambda m: m["id"], "id mn"); dup(mn, lambda m: nz(m["t"]), "título mn"); dup([m for m in mn if m["tp"] == "a"], lambda m: m["m"], "sigla")

if err:
    print("\n".join(err)); sys.exit(1)

out = {"versao": "2026.11.11-honra1", "temas": list(TEMAS.values()), "trads": TRADS, "cards": cards, "mn": mn, "bu": bu,
       "filtro": [{"q": q, "w": w, "ok": ok} for q, w, ok in bm.F]}
os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
p = os.path.join(ROOT, "data", "honra.json")
json.dump(out, open(p, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
from collections import Counter
print(f"OK → {p} ({os.path.getsize(p)//1024} KB)")
print("cards:", len(cards), dict(Counter(c["tr"] for c in cards)))
print("mnemônicos:", len(mn), dict(Counter(m["o"] for m in mn)))
print("bússolas:", len(bu), "· filtro:", len(bm.F))
print("cards por tema:", dict(Counter(c["tema"].split(" ", 1)[1] for c in cards)))
