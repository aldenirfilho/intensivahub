#!/usr/bin/env python3
"""Exporta o 💉 Caderno de Prescrições 360X (data/prescricoes.json) para leitura fora do app:
Markdown, HTML de impressão e PDF A4 (capa, sumário, 500 fichas, rodapé com crédito e metadados de autor).
Uso: python3 tools/px/export_caderno.py <APP_DIR> [dd/mm/aaaa]   → grava em tools/px/out/
ALDENIR ROCHA DE OLIVEIRA FILHO · PROJETO 360X"""
import sys, os, re, json, html, asyncio, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
CRED = "ALDENIR ROCHA DE OLIVEIRA FILHO · PROJETO 360X"
TIT = "Caderno de Prescrições 360X"
BASE = "Caderno_de_Prescricoes_360X_500_modelos"
AREA = {"cm": ("🩺", "Clínica Médica", "#1f7a8c"), "uti": ("🏥", "Medicina Intensiva", "#6d4bb3"),
        "cardio": ("❤️", "Cardiologia", "#b3364b"), "emerg": ("🚑", "Emergência", "#b8741a")}
ORD = ["cm", "cardio", "uti", "emerg"]

def num(v):
    v = float(v); s = f"{v:.3f}".rstrip("0").rstrip(".")
    if v >= 1000 and v == int(v): s = f"{int(v):,}".replace(",", ".")
    return s.replace(".", ",") if v < 1000 else s

def tok(s):
    """Sem peso informado: {kg:…} vira a dose por kg; os marcadores de vazão saem (o app calcula)."""
    s = re.sub(r"\{kg:([\d.]+):([^:}]+?)(?::([\d.]+))?\}", lambda m: f"{num(m.group(1))} {m.group(2)}/kg" + (f" (máx. {num(m.group(3))} {m.group(2)})" if m.group(3) else ""), s)
    s = re.sub(r"\s*\{mlhh?:[\d.]+:[\d.]+\}", "", s)
    s = re.sub(r"\(\s*\)", "", s); s = re.sub(r"\s+([,;.)])", r"\1", s); s = re.sub(r"\(\s+", "(", s)
    return re.sub(r"\s{2,}", " ", s).strip()

def md_b(s): return tok(s)
def h(s):
    s = html.escape(tok(s)); return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)

def main():
    D = sys.argv[1] if len(sys.argv) > 1 else "."
    doc = json.load(open(os.path.join(D, "data", "prescricoes.json"), encoding="utf-8"))
    it = doc["itens"]; out = os.path.join(HERE, "out"); os.makedirs(out, exist_ok=True)
    hoje = sys.argv[2] if len(sys.argv) > 2 else datetime.date.today().strftime("%d/%m/%Y")
    groups = []
    for a in ORD:
        cats = []
        for p in it:
            if p["area"] == a and p["cat"] not in cats: cats.append(p["cat"])
        groups.append((a, [(c, [p for p in it if p["area"] == a and p["cat"] == c]) for c in cats]))
    aviso = ("Modelos de prescrição para estudo e apoio à decisão, redigidos de memória a partir das diretrizes citadas em cada ficha. "
             "Não passaram por revisão médica independente. Antes de prescrever, conferir alergias, peso, função renal e hepática, interações, "
             "gestação e o protocolo da instituição. A dose final é responsabilidade do prescritor.")
    campos = [("mon", "📈 Monitorização"), ("aj", "⚖️ Ajustes"), ("ci", "⛔ Contraindicações"), ("al", "⚠️ Alertas")]
    # ---------------- Markdown
    M = [f"# 💉 {TIT} — {doc['n']} modelos", "", f"**Autor: {CRED}**", "", f"Versão do app: {doc['versao']} · exportado em {hoje}", "", f"> ⚠️ {aviso}", "",
         "As doses por kg aparecem como dose/kg; no app, informando o peso, saem o total e a vazão em mL/h.", "", "## Sumário", ""]
    for a, cats in groups:
        e, n, _ = AREA[a]; M.append(f"- {e} **{n}** — {sum(len(ps) for _, ps in cats)} fichas")
        for c, ps in cats: M.append(f"  - {c} ({len(ps)})")
    for a, cats in groups:
        e, n, _ = AREA[a]; M += ["", f"# {e} {n}", ""]
        for c, ps in cats:
            M += [f"## {c}", ""]
            for p in ps:
                M += [f"### {p['id']} · {p['ti']}", "", f"**🎯 Quando usar:** {md_b(p['quando'])}", "", "**℞ Prescrição**", ""]
                M += [f"{i}. {md_b(l)}" for i, l in enumerate(p["rx"], 1)]
                M.append("")
                for k, t in campos:
                    if p.get(k): M += [f"**{t}:** {md_b(p[k])}", ""]
                if p.get("ref"): M += [f"*📚 {p['ref']} — referência citada de memória; confira a versão vigente.*", ""]
    M += ["---", f"{TIT} · {CRED}"]
    open(os.path.join(out, BASE + ".md"), "w", encoding="utf-8").write("\n".join(M) + "\n")
    # ---------------- HTML de impressão
    css = """
@page{size:A4;margin:16mm 14mm 18mm}
*{box-sizing:border-box}html{font-size:9.6pt}
body{margin:0;font-family:'Fira Sans','DejaVu Sans',sans-serif,'Noto Color Emoji';color:#16181d;line-height:1.38}
.capa{height:262mm;background:#0d1016;color:#f2e6c4;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;
 border:1.2mm solid #c9a23a;outline:.3mm solid #22b8d6;outline-offset:-3mm;padding:18mm;break-after:page}
.capa .rx{font-family:'Cardo','GFS Baskerville',serif;font-size:74pt;color:#c9a23a;line-height:1}
.capa h1{font-family:'Cardo','GFS Baskerville',serif;font-size:31pt;letter-spacing:.06em;margin:6mm 0 2mm;color:#f0d98a;font-weight:700}
.capa h2{font-size:13pt;font-weight:400;color:#22b8d6;margin:0 0 10mm;letter-spacing:.14em;text-transform:uppercase}
.capa .n{font-size:12pt;margin:1.5mm 0}.capa .aut{margin-top:14mm;font-size:12.5pt;letter-spacing:.12em;color:#f0d98a;font-weight:600}
.capa .sub{font-size:9.5pt;color:#b9c0cc;margin-top:3mm}
.av{border:.4mm solid #c9a23a;background:#fff8e1;padding:4mm 5mm;border-radius:2mm;margin:0 0 6mm;font-size:10pt}
h1.ar{font-family:'Cardo','GFS Baskerville',serif;font-size:24pt;margin:0 0 4mm;padding:60mm 0 4mm;border-bottom:.8mm solid var(--c);color:var(--c);break-before:page;break-after:avoid}
h1.ar small{display:block;font:400 11pt 'Fira Sans',sans-serif;color:#555;margin-top:2mm}
h2.ct{font-size:13pt;margin:7mm 0 3mm;padding:1.6mm 3mm;background:var(--c);color:#fff;border-radius:1.2mm;break-after:avoid}
.sm h2{font-family:'Cardo',serif;font-size:18pt;margin:0 0 4mm}.sm table{width:100%;border-collapse:collapse}.sm td{padding:1.1mm 2mm;border-bottom:.15mm solid #ddd;vertical-align:top}
.sm td.q{text-align:right;white-space:nowrap;color:#555}.sm tr.a td{font-weight:700;font-size:11pt;border-bottom:.4mm solid #999;padding-top:3.5mm}
.fx{margin:0 0 4.2mm;padding:0 0 3mm;border-bottom:.15mm solid #cfd3da}
.fx h3{font-size:11.2pt;margin:0 0 1.2mm;color:#0d1016;break-after:avoid}.fx h3 span{font-weight:400;color:var(--c);font-size:8.6pt;margin-right:1.5mm}
.fx p{margin:.8mm 0}.fx .q{color:#2b2f38}.fx ol{margin:1.2mm 0 1.6mm;padding:1.8mm 3mm 1.8mm 8.5mm;background:#f4f6f9;border-left:.9mm solid var(--c);border-radius:0 1.2mm 1.2mm 0}
.fx li{margin:.5mm 0}.fx .s{font-size:8.9pt}.fx .s b{color:#0d1016}.fx .r{font-size:8pt;color:#666;font-style:italic}
"""
    H = [f"<!doctype html><html lang='pt-BR'><head><meta charset='utf-8'><title>{TIT} — {doc['n']} modelos</title><meta name='author' content='{CRED}'><style>{css}</style></head><body>",
         f"<section class='capa'><div class='rx'>℞</div><h1>{TIT.upper()}</h1><h2>Códice 360X · TEMI + R3 Clínica Médica</h2>"
         f"<div class='n'><b>{doc['n']} modelos de prescrição</b> com indicação, passo a passo, monitorização, ajustes, contraindicações e alertas</div>"
         + "".join(f"<div class='n'>{AREA[a][0]} {AREA[a][1]} · {sum(len(ps) for _, ps in cats)}</div>" for a, cats in groups) +
         f"<div class='aut'>{CRED}</div><div class='sub'>Versão do app {doc['versao']} · exportado em {hoje}</div></section>",
         f"<section class='sm'><div class='av'>⚠️ <b>Leia antes de usar.</b> {html.escape(aviso)}</div><p>As doses por kg aparecem como dose/kg. No app, ao informar o peso, saem o total da dose e a vazão em mL/h.</p><h2>Sumário</h2><table>"]
    for a, cats in groups:
        e, n, _ = AREA[a]; H.append(f"<tr class='a'><td>{e} {n}</td><td class='q'>{sum(len(ps) for _, ps in cats)} fichas</td></tr>")
        for c, ps in cats: H.append(f"<tr><td>{html.escape(c)}</td><td class='q'>{ps[0]['id']}–{ps[-1]['id']} · {len(ps)}</td></tr>")
    H.append("</table></section>")
    for a, cats in groups:
        e, n, col = AREA[a]
        H.append(f"<div style='--c:{col}'><h1 class='ar'>{e} {n}<small>{sum(len(ps) for _, ps in cats)} fichas · {len(cats)} categorias</small></h1>")
        for c, ps in cats:
            H.append(f"<h2 class='ct'>{html.escape(c)} · {len(ps)}</h2>")
            for p in ps:
                H.append(f"<article class='fx'><h3><span>{p['id']}</span>{html.escape(p['ti'])}</h3><p class='q'><b>🎯 Quando usar:</b> {h(p['quando'])}</p><ol>"
                         + "".join(f"<li>{h(l)}</li>" for l in p["rx"]) + "</ol>"
                         + "".join(f"<p class='s'><b>{t}:</b> {h(p[k])}</p>" for k, t in campos if p.get(k))
                         + (f"<p class='r'>📚 {html.escape(p['ref'])} — referência citada de memória; confira a versão vigente.</p>" if p.get("ref") else "") + "</article>")
        H.append("</div>")
    H.append("</body></html>")
    hp = os.path.join(out, BASE + ".html"); open(hp, "w", encoding="utf-8").write("".join(H))
    # ---------------- PDF
    pp = os.path.join(out, BASE + ".pdf")
    async def pdf():
        from playwright.async_api import async_playwright
        async with async_playwright() as pw:
            b = await pw.chromium.launch(); pg = await b.new_page()
            await pg.goto("file://" + hp); await pg.wait_for_timeout(800)
            foot = ("<div style='width:100%;font:6.5pt sans-serif;color:#666;padding:0 14mm;display:flex;justify-content:space-between'>"
                    f"<span>{TIT} · {CRED}</span><span>modelo de estudo — conferir antes de prescrever · <span class='pageNumber'></span>/<span class='totalPages'></span></span></div>")
            await pg.pdf(path=pp, format="A4", print_background=True, display_header_footer=True, header_template="<span></span>", footer_template=foot,
                         margin={"top": "16mm", "bottom": "18mm", "left": "14mm", "right": "14mm"})
            await b.close()
    asyncio.run(pdf())
    from pypdf import PdfReader, PdfWriter
    r = PdfReader(pp); w = PdfWriter(); w.append(r)
    w.add_metadata({"/Title": f"{TIT} — {doc['n']} modelos", "/Author": CRED, "/Subject": "Modelos de prescrição para estudo — Clínica Médica, Medicina Intensiva, Cardiologia e Emergência",
                    "/Keywords": "prescrição, TEMI, R3 Clínica Médica, Códice 360X, Projeto 360X", "/Creator": "Códice 360X · tools/px/export_caderno.py"})
    w.write(pp)
    print(f"✅ {BASE}.md {os.path.getsize(os.path.join(out, BASE + '.md')) // 1024} KB · .html {os.path.getsize(hp) // 1024} KB · .pdf {os.path.getsize(pp) // 1024} KB · {len(r.pages)} páginas")

if __name__ == "__main__":
    main()
