#!/usr/bin/env python3
"""Monta data/prescricoes.json com os 500 modelos do 💉 Caderno de Prescrições 360X.
Uso: python3 tools/px/build_px.py <APP_DIR> [--check]
Fontes: tools/px/px01.py … pxNN.py — cada arquivo tem AREA ("cm" | "uti" | "cardio" | "emerg") e L = [P(...), …].
P(cat, ti, quando, rx, mon, aj, ci, al, ref, tags="")
  - rx: lista de linhas da prescrição; "@MACRO" vira a linha padronizada de macros.py.
  - tokens: {kg:dose:unid[:máx]} · {mlh:mcg/kg/min:mcg/mL} · {mlhh:dose/kg/h:conc/mL} (o app calcula pelo peso).
ALDENIR ROCHA DE OLIVEIRA FILHO · PROJETO 360X"""
import sys, os, re, json, glob, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from macros import M
CRED = "ALDENIR ROCHA DE OLIVEIRA FILHO · PROJETO 360X"
AREAS = {"cm": "Clínica Médica", "uti": "Medicina Intensiva", "cardio": "Cardiologia", "emerg": "Emergência"}
META = {"cm": 170, "cardio": 110, "uti": 120, "emerg": 100}
TOK = re.compile(r"\{(kg|mlh|mlhh):[^}]*\}")
TOK_OK = re.compile(r"^\{(kg:[\d.]+:[^:}]+(:[\d.]+)?|mlh:[\d.]+:[\d.]+|mlhh:[\d.]+:[\d.]+)\}$")

def P(cat, ti, quando, rx, mon="", aj="", ci="", al="", ref="", tags=""):
    return dict(cat=cat, ti=ti, quando=quando, rx=rx, mon=mon, aj=aj, ci=ci, al=al, ref=ref, tags=tags)

def load():
    out = []
    for f in sorted(glob.glob(os.path.join(HERE, "px[0-9][0-9].py"))):
        spec = importlib.util.spec_from_file_location(os.path.basename(f)[:-3], f); m = importlib.util.module_from_spec(spec)
        m.P = P; spec.loader.exec_module(m)
        for p in m.L: p["area"] = m.AREA; p["_f"] = os.path.basename(f); out.append(p)
    return out

def main():
    D = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "."
    check = "--check" in sys.argv
    L, err, seen = load(), [], {}
    for i, p in enumerate(L, 1):
        p["id"] = f"PX{i:03d}"; rx = []
        for l in p["rx"]:
            if l.startswith("@"):
                if l not in M: err.append(f"{p['id']} macro desconhecida {l}"); continue
                rx.append(M[l])
            else: rx.append(l)
        p["rx"] = rx
        for k in ("cat", "ti", "quando"):
            if not str(p.get(k, "")).strip(): err.append(f"{p['id']} sem {k}")
        if len(rx) < 4: err.append(f"{p['id']} ({p['ti'][:40]}) com só {len(rx)} linhas de ℞")
        if not (p["mon"] and p["al"]): err.append(f"{p['id']} ({p['ti'][:40]}) sem monitorização ou alertas")
        k = re.sub(r"\W+", " ", p["ti"].lower()).strip()
        if k in seen: err.append(f"{p['id']} título repetido de {seen[k]}: {p['ti']}")
        seen[k] = p["id"]
        for fld in ("quando", "mon", "aj", "ci", "al"):
            v = p[fld]
            for x in (v if isinstance(v, list) else [v]):
                for t in TOK.finditer(x):
                    if not TOK_OK.match(t.group(0)): err.append(f"{p['id']} token inválido {t.group(0)}")
        for x in rx:
            for t in TOK.finditer(x):
                if not TOK_OK.match(t.group(0)): err.append(f"{p['id']} token inválido {t.group(0)}")
            if "@" in x and re.search(r"(^|\s)@[A-Z_]+", x): err.append(f"{p['id']} macro no meio da linha: {x[:50]}")
    cnt = {a: sum(1 for p in L if p["area"] == a) for a in AREAS}
    print("total", len(L), cnt, "· categorias", len({(p['area'], p['cat']) for p in L}))
    for e in err[:60]: print("⚠️", e)
    if err: print(f"⚠️ {len(err)} problema(s)")
    if check: return
    if err: sys.exit("corrija antes de gerar")
    itens = [{k: p[k] for k in ("id", "area", "cat", "ti", "quando", "rx", "mon", "aj", "ci", "al", "ref", "tags") if p.get(k) not in ("", None, "—")} for p in L]
    doc = {"formato": "codice360x-px-v1", "versao": "4.25.0", "autor": CRED, "titulo": "💉 Caderno de Prescrições 360X",
           "aviso": "Modelos de prescrição para estudo e apoio à decisão. Conferir alergias, peso, função renal e hepática, interações, gestação e o protocolo institucional. A dose final é responsabilidade do prescritor.",
           "n": len(itens), "areas": {a: {"nome": AREAS[a], "n": cnt[a]} for a in AREAS}, "itens": itens}
    os.makedirs(os.path.join(D, "data"), exist_ok=True)
    js = json.dumps(doc, ensure_ascii=False, separators=(",", ":"))
    open(os.path.join(D, "data", "prescricoes.json"), "w", encoding="utf-8").write(js)
    print(f"✅ data/prescricoes.json · {len(itens)} prescrições · {len(js)//1024} KB")

if __name__ == "__main__":
    main()
