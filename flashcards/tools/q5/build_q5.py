#!/usr/bin/env python3
"""❓ Lote nov/2026 (4.23.0): +300 TEMI (QT601–QT900) e +300 R3 Clínica Médica (QR601–QR900) → data/questoes.json.
Fonte: tools/q5/t1..t8.py (TEMI) e r1..r7.py (R3); itens listados em drop.py são ignorados (duplicatas do banco 1–600). Cada item: (tema, enunciado, [(alternativa, porquê)×5 — a correta PRIMEIRO], comentário, pegadinha, referência).
O builder embaralha as alternativas de forma determinística (semente = id) e grava o campo "lote": "2026-11".
Append idempotente: remove ids ≥ 601 da divisão e acrescenta o lote; as questões 1–600 e a divisão gaso ficam intactas.
Uso: python3 tools/q5/build_q5.py <APP_DIR> [--check]"""
import json, sys, os, hashlib, random, re, importlib, collections

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
TT = {"SE": "Sepse e choque", "HD": "Hemodinâmica", "VM": "Ventilação e SDRA", "DV": "Desmame e VNI", "SD": "Sedação e delirium", "PC": "PCR e pós-PCR",
      "NE": "Neurointensivismo", "CA": "Cardiologia intensiva", "IN": "Infecções na UTI", "NF": "Nefrologia e distúrbios", "EL": "Eletrólitos", "AB": "Ácido-base",
      "EN": "Endocrinologia", "GN": "Gastro e nutrição", "HE": "Hematologia", "TX": "Toxicologia", "TR": "Trauma e queimados", "OB": "Obstetrícia",
      "ET": "Ética, paliativos e morte encefálica", "PO": "POCUS", "ON": "Oncologia na UTI", "QS": "Qualidade e segurança", "ES": "Estatística", "MG": "Medicina intensiva geral"}
TR = {"CD": "Cardiologia", "IF": "Infectologia", "PN": "Pneumologia", "GA": "Gastroenterologia", "NR": "Nefrologia", "ED": "Endocrinologia", "RE": "Reumatologia",
      "HM": "Hematologia", "NL": "Neurologia", "OC": "Oncologia", "GE": "Geriatria", "PS": "Psiquiatria", "DE": "Dermatologia", "MP": "Medicina preventiva", "MB": "MBE", "CI": "Clínica integrada"}
LOTE = "2026-11"
NUM = re.compile(r"^[~≈<>≥≤]?\s*-?\d")


def lead(a):
    m = re.search(r"-?\d+(?:[.,]\d+)?", a.replace(".", "").replace(",", ".") if re.match(r"^[~≈<>≥≤]?\s*-?\d{1,3}(\.\d{3})+", a) else a.replace(",", "."))
    return float(m.group(0)) if m else 0.0


def mk(qid, tema, enun, pairs, com, pega, ref, MAP, pos=None):
    assert tema in MAP, (qid, tema)
    assert len(pairs) == 5 and all(len(p) == 2 and p[0].strip() and p[1].strip() for p in pairs), (qid, "pares")
    assert len({p[0].strip().lower() for p in pairs}) == 5, (qid, "alternativas repetidas")
    assert enun.strip() and com.strip() and pega.strip() and ref.strip(), (qid, "campos")
    rest = [1, 2, 3, 4]; random.Random(int(hashlib.md5(qid.encode()).hexdigest(), 16)).shuffle(rest)
    p = pos if pos is not None else int(hashlib.md5(qid.encode()).hexdigest(), 16) % 5
    order = rest[:p] + [0] + rest[p:]   # gabarito na posição p (posições balanceadas por divisão)
    if all(NUM.match(p[0]) for p in pairs): order.sort(key=lambda i: lead(pairs[i][0]))   # alternativas numéricas em ordem crescente
    return {"id": qid, "tema": MAP[tema], "enun": enun.strip(), "alts": [pairs[i][0].strip() for i in order], "gab": order.index(0),
            "com": com.strip(), "porque": [pairs[i][1].strip() for i in order], "pega": pega.strip(), "ref": ref.strip(), "lote": LOTE}


try:
    from drop import DROP
except ImportError:
    DROP = []
DROPS = set(DROP)


def build(pref, files, MAP):
    its = []
    for f in files:
        if not os.path.exists(os.path.join(HERE, f + ".py")): continue
        for it in importlib.import_module(f).Q:
            assert len(it) == 6, (f, it[1][:60])
            if it[1].strip()[:60] in DROPS: continue   # duplicata de conceito do banco 1–600 (ver drop.py)
            its.append(it)
    P = [i % 5 for i in range(len(its))]; random.Random("lote-2026-11-" + pref).shuffle(P)
    return [mk(f"{pref}{601 + i:03d}", *it, MAP, P[i]) for i, it in enumerate(its)]


def toks(s): return set(re.findall(r"[a-zà-ú0-9]{4,}", re.sub(r"<[^>]+>", " ", s.lower())))


if __name__ == "__main__":
    APP = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "."
    NEW = {"temi": build("QT", [f"t{i}" for i in range(1, 9)], TT), "r3": build("QR", [f"r{i}" for i in range(1, 9)], TR)}
    p = os.path.join(APP, "data", "questoes.json"); d = json.load(open(p, encoding="utf-8"))
    rep = []
    for k, L in NEW.items():
        old = [q for q in d[k] if int(q["id"][2:]) <= 600]
        assert len(old) == 600, (k, len(old))
        TK = [(q["id"], toks(q["enun"] + " " + q["alts"][q["gab"]])) for q in old]; seen = []
        for q in L:
            t = toks(q["enun"] + " " + q["alts"][q["gab"]])
            for qid, t2 in TK + seen:
                j = len(t & t2) / max(1, len(t | t2))
                if j >= 0.5: rep.append(f"⚠️ {q['id']} ~ {qid} (Jaccard {j:.2f}): {q['enun'][:70]}")
            seen.append((q["id"], t))
        print(k, len(L), "novas · gabaritos", dict(sorted(collections.Counter("ABCDE"[q["gab"]] for q in L).items())),
              "· temas", dict(collections.Counter(q["tema"] for q in L).most_common()))
        d[k] = old + L + [q for q in d[k] if int(q["id"][2:]) > 900]  # preserva o lote ilustrado (tools/q6, ≥ 901)
    print("\n".join(rep) if rep else "✅ sem enunciados muito parecidos (Jaccard < 0,5)")
    if "--check" not in sys.argv:
        json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False)
        json.dump(NEW, open(os.path.join(HERE, "q5_questoes.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
        print(p, os.path.getsize(p) // 1024, "KB ·", {k: len(v) for k, v in d.items()})
