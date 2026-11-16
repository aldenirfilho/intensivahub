#!/usr/bin/env python3
"""Livro "Axiomas 360X — Edição comentada" (HTML para tela + PDF A5 de impressão)."""
import base64, html, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ax1 import AX1
from ax2 import AX2
from build import TEMAS
import book_extras as BX

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "out")
AUTOR = "Aldenir Rocha de Oliveira Filho"
DATA = "16 de novembro de 2026"

EIXOS = [
    ("I · Fundamentos", "I", "Fundamentos", "Os primeiros axiomas tratam da expansão humana, dos limites da posse e da partilha que preserva a dignidade. Aqui nasce a ideia de prosperidade justa."),
    ("II · Médicos", "II", "Axiomas médicos", "Nascidos à beira do leito: diagnóstico a tempo, raciocínio fisiológico e prudência terapêutica."),
    ("III · Vida honrada", "III", "Vida honrada", "O preço da formação, a força dos detalhes, a humildade e o equilíbrio de uma vida inteira."),
    ("IV · Conquista e amor", "IV", "Conquista, inspiração, amor e família", "Pequenas conquistas, o melhor investimento, o amor e o tripé que sustenta a família."),
    ("V · Humanidade", "V", "Humanidade e universalidade", "Dignidade, confiança, inveja vencida, mérito e a vida em comunidade — na família e na empresa."),
    ("VI · Poupar e preservar", "VI", "Poupar, preservar e reconstruir", "Poupança com propósito, desapego, objetos que contam histórias e o cuidado com quem não pode pedir ajuda."),
    ("VII · Curiosidade e exemplo", "VII", "Curiosidade, dom e exemplo", "A curiosidade como motor, o dom, o raciocínio em cascata e o exemplo que se deixa."),
    ("VIII · Limite e cuidado", "VIII", "Limite, fluxo e cuidado", "O limite como forma de cuidado: o freio que protege, a dose certa e a coragem de dizer “cheguei ao meu limite”."),
    ("IX · Harmonia e homeostase", "IX", "Harmonia e homeostase", "A doença como batalha pela homeostase, o meio e a harmonia — e as hipóteses de pesquisa do autor."),
    ("X · Vigília e estratégia", "X", "Vigília, time e estratégia na UTI", "A noite na terapia intensiva, o time multiprofissional e a mente intensa que traça a estratégia."),
    ("Armorial", "⚜", "Armorial do Realmetaverso", "Os brasões e a competição justa, em paz."),
]

def carregar():
    ax = []
    for l in (AX1 + AX2).strip().split("\n"):
        if not l.strip():
            continue
        n, tit, eixo, sit, data, tema, enun, com = [x.strip() for x in l.split(" | ")]
        ax.append(dict(n=int(n), tit=tit, eixo=eixo, sit=sit, data=data, tema=tema, enun=enun, com=com))
    assert len(ax) == 135 and sorted(a["n"] for a in ax) == list(range(1, 136)), "numeração incompleta"
    return ax

def font_face():
    out = []
    for fn, style in (("Lora.woff2", "normal"), ("Lora-Italic.woff2", "italic")):
        b64 = base64.b64encode(open(os.path.join(BASE, "fonts", fn), "rb").read()).decode()
        out.append(f"@font-face{{font-family:'LoraLivro';font-style:{style};font-weight:400 700;src:url(data:font/woff2;base64,{b64}) format('woff2')}}")
    return "\n".join(out)

BRASAO = """<svg class="brasao" viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f3d67a"/><stop offset="1" stop-color="#a87e2a"/></linearGradient></defs>
<path d="M100 8 L188 34 L188 118 C188 176 146 214 100 232 C54 214 12 176 12 118 L12 34 Z" fill="#10151f" stroke="url(#g)" stroke-width="6"/>
<path d="M100 24 L172 45 L172 118 C172 166 138 198 100 214 C62 198 28 166 28 118 L28 45 Z" fill="none" stroke="#22d3ee" stroke-width="2" opacity=".8"/>
<path d="M100 52 C112 70 116 88 100 108 C84 88 88 70 100 52 Z M100 108 C92 92 70 86 62 100 C56 112 70 124 82 116 M100 108 C108 92 130 86 138 100 C144 112 130 124 118 116 M76 126 H124 M100 108 V150" fill="none" stroke="url(#g)" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
<text x="100" y="190" text-anchor="middle" font-family="LoraLivro,Georgia,serif" font-size="30" font-weight="700" fill="url(#g)" letter-spacing="3">360X</text>
</svg>"""

CSS = """
:root{--papel:#f8f2e4;--tinta:#2b241a;--ouro:#9c7a2b;--ouro2:#d4af37;--ciano:#0e7490;--fundo:#0b0f16}
*{box-sizing:border-box}
html{background:var(--fundo)}
body{margin:0;font-family:'LoraLivro',Georgia,'Times New Roman',serif;color:var(--tinta);line-height:1.62;font-size:18px;-webkit-font-smoothing:antialiased}
.livro{max-width:760px;margin:0 auto;padding:0 0 40px}
.pg{background:var(--papel);margin:22px 12px;padding:56px 60px;border-radius:6px;box-shadow:0 10px 40px rgba(0,0,0,.5);position:relative}
.pg::before{content:"";position:absolute;inset:12px;border:1px solid rgba(156,122,43,.35);border-radius:3px;pointer-events:none}
.capa{background:radial-gradient(130% 120% at 50% 0%,#1c2431 0%,#0f141d 55%,#080b11 100%);color:#efe6cf;text-align:center;padding:70px 40px 60px}
.capa::before{border-color:rgba(212,175,55,.55)}
.brasao{width:170px;height:auto;margin:0 auto 26px;display:block;filter:drop-shadow(0 0 18px rgba(212,175,55,.25))}
.capa .sup{letter-spacing:.42em;font-size:.72em;color:#7dd3e0;text-transform:uppercase}
.capa h1{font-size:3.1em;letter-spacing:.08em;margin:.25em 0 .1em;color:#f1d27a;font-weight:700}
.capa .sub{font-style:italic;font-size:1.15em;color:#e8dcc0}
.capa .aut{margin-top:46px;font-size:1.05em;letter-spacing:.12em;text-transform:uppercase;color:#f1d27a}
.capa .ed{margin-top:8px;font-size:.8em;color:#a9a08a}
.rosto{text-align:center;padding-top:90px;padding-bottom:90px}
.rosto .aut{font-variant:small-caps;letter-spacing:.08em;font-size:1.1em}
.rosto h1{font-size:2.2em;margin:.6em 0 .1em;letter-spacing:.06em}
.rosto .sub{font-style:italic}
.rosto .loc{margin-top:70px;font-size:.9em;color:#5d513c}
.ficha{font-size:.82em;color:#4a4030}
.ficha h2{font-size:1em;text-transform:uppercase;letter-spacing:.2em;color:var(--ouro)}
.ficha .box{border:1px solid rgba(156,122,43,.45);padding:14px 16px;margin-top:10px}
.epi{text-align:center;padding:110px 70px}
.epi blockquote{font-style:italic;font-size:1.45em;margin:0;line-height:1.5}
.epi .who{margin-top:18px;font-variant:small-caps;letter-spacing:.06em;color:#5d513c}
h2.sec{font-size:1.05em;text-transform:uppercase;letter-spacing:.24em;color:var(--ouro);text-align:center;margin:0 0 1.2em}
.nota p{text-align:justify;hyphens:auto}
.sum ol{list-style:none;padding:0;margin:0}
.sum li{display:flex;align-items:baseline;gap:10px;padding:7px 0;border-bottom:1px dotted rgba(156,122,43,.45)}
.sum .r{font-weight:700;color:var(--ouro);min-width:2.6em}
.sum a{color:var(--tinta);text-decoration:none;flex:1}
.sum .q{font-size:.85em;color:#6b5f48}
.cap{padding-top:70px}
.cap .num{text-align:center;font-size:3.4em;color:var(--ouro);line-height:1;letter-spacing:.06em}
.cap h2{text-align:center;font-size:1.65em;margin:.25em 0 .2em;letter-spacing:.03em}
.cap .intro{text-align:center;font-style:italic;color:#5d513c;max-width:520px;margin:0 auto 10px}
.orn{text-align:center;color:var(--ouro);letter-spacing:.8em;margin:26px 0;font-size:.9em}
.ax{margin:0 0 34px;break-inside:avoid;page-break-inside:avoid}
.ax .n{font-size:.8em;letter-spacing:.24em;text-transform:uppercase;color:var(--ouro)}
.ax h3{font-size:1.18em;margin:.15em 0 .5em;font-variant:small-caps;letter-spacing:.03em}
.ax blockquote{margin:0 0 12px;padding:2px 0 2px 18px;border-left:3px solid var(--ouro2);font-style:italic;font-size:1.08em;line-height:1.55}
.ax .com{margin:0 0 6px;text-align:justify;hyphens:auto}
.ax .com .lbl{font-variant:small-caps;letter-spacing:.06em;color:var(--ciano);font-style:normal;font-weight:700}
.ax .meta{font-size:.74em;color:#6b5f48;letter-spacing:.02em}
.selo{display:inline-block;font-size:.95em;padding:0 7px;border-radius:999px;border:1px solid rgba(156,122,43,.6);margin-left:4px}
.selo.prop{border-color:#0e7490;color:#0e7490}
.selo.conf{border-color:#3f7d3a;color:#3f7d3a}
.ind{columns:2;column-gap:28px;font-size:.78em}
.ind div{break-inside:avoid;padding:2px 0}
.ind a{color:var(--tinta);text-decoration:none}
.ind b{color:var(--ouro);display:inline-block;min-width:2.2em}
.colo{text-align:center;font-size:.85em;color:#4a4030;padding:80px 50px}
.colo .brasao{width:70px;margin-bottom:12px}
.topo{position:sticky;top:0;z-index:5;display:flex;justify-content:space-between;align-items:center;gap:8px;padding:8px 14px;background:rgba(11,15,22,.92);backdrop-filter:blur(6px);border-bottom:1px solid #3b3220;font-family:-apple-system,'Segoe UI',Roboto,sans-serif;font-size:13px}
.topo a{color:#e7c66a;text-decoration:none;font-weight:600}
.topo .t{color:#a5b4c3}
@media (max-width:600px){body{font-size:16.5px}.pg{padding:38px 24px;margin:12px 6px}.capa h1{font-size:2.3em}.epi{padding:70px 26px}.ind{columns:1}}
@media print{
 @page{size:A5;margin:16mm 14mm 18mm}
 @page:first{margin:0}
 html,body{background:#fff}
 body{font-size:10.6pt}
 .topo{display:none}
 .livro{max-width:none;padding:0}
 .pg{background:#fff;box-shadow:none;margin:0;padding:0;border-radius:0;break-after:page;page-break-after:always}
 .pg::before{display:none}
 .pg.capa{background:radial-gradient(130% 120% at 50% 0%,#1c2431 0%,#0f141d 55%,#080b11 100%) !important;height:210mm;width:148mm;padding:34mm 14mm 0;-webkit-print-color-adjust:exact;print-color-adjust:exact;overflow:hidden}
 .rosto{padding-top:40mm}
 .epi{padding:55mm 10mm 0}
 .cap{padding-top:0}
 .cap .num{margin-top:12mm}
 .colo{padding-top:50mm}
 a{color:inherit}
}
"""


PRINT_CSS = """
@media print{
@page{size:154mm 216mm;margin:20mm 18mm 22mm 23mm}
@page:first{margin:20mm 18mm 22mm 23mm}
@page:right{margin:20mm 18mm 22mm 23mm}
@page:left{margin:20mm 23mm 22mm 18mm}
}
.pg.sobre .espaco{border:1px dashed #b8a578;min-height:110mm;padding:8mm;color:#9a8a62;font-style:italic;font-size:9.5pt;border-radius:4px}
"""

def selo(sit):
    cls = {"Proposta do autor": "prop", "Confirmado pelo autor": "conf"}.get(sit, "")
    return f'<span class="selo {cls}">{html.escape(sit)}</span>'

def montar(ax, edicao="tela"):
    tela = edicao == "tela"
    e = html.escape
    por = {k: sorted([a for a in ax if a["eixo"] == k], key=lambda a: a["n"]) for k, *_ in EIXOS}
    assert sum(len(v) for v in por.values()) == 135, "eixo desconhecido"
    P = []
    P.append(f"""<section class="pg capa" id="capa">{BRASAO}
<div class="sup">Códice 360X · Edição comentada</div>
<h1>AXIOMAS 360X</h1>
<div class="sub">Cento e vinte e oito axiomas de medicina, honra e humanidade</div>
<div class="aut">{AUTOR}</div>
<div class="ed">1ª edição comentada · {DATA}</div></section>""")
    if not tela:
        P.pop()  # a capa dura é um arquivo à parte; o miolo começa na folha de rosto
    else:
        P.append(BX.painel(EIXOS))
    P.append(f"""<section class="pg rosto"><div class="aut">{AUTOR}</div>
<h1>Axiomas 360X</h1><div class="sub">Edição comentada</div>
<div class="loc">Sobral · Ceará · Brasil<br>{DATA}</div></section>""")
    P.append(f"""<section class="pg ficha"><h2>Créditos e ficha da edição</h2>
<div class="box"><b>Autor dos axiomas:</b> {AUTOR}.<br>
<b>Título:</b> Axiomas 360X — edição comentada.<br>
<b>Texto dos axiomas:</b> transcrito sem alteração do catálogo “Axiomas 360X”, mantido pelo autor (versões lapidadas, consulta de {DATA}).<br>
<b>Comentários:</b> edição Códice 360X, escritos com assistência do Claude (Anthropic) e assinalados como “Comentário” em cada axioma — não são palavras do autor.<br>
<b>Edição:</b> digital (HTML e PDF), 1ª edição comentada. Sem ISBN.<br>
<b>Organização:</b> 135 axiomas em dez eixos e o Armorial do Realmetaverso. Os axiomas 101 a 135 aparecem sob o eixo de tema mais próximo, como no catálogo, até o autor confirmar os eixos XI a XX.<br>
<b>Selos:</b> <i>Lapidado</i> (versão editada e aprovada), <i>Confirmado pelo autor</i> e <i>Proposta do autor</i> (ideia ou hipótese ainda em aberto; hipóteses de pesquisa não são conduta médica).<br>
<b>Tipografia:</b> Lora (SIL Open Font License).<br>
<b>Uso:</b> as ideias podem circular livremente; o crédito ao autor é devido (axioma 109).</div></section>""")
    P.append(f"""<section class="pg epi"><blockquote>“A prosperidade justa é o reconhecimento da honra e do mérito.”</blockquote>
<div class="who">— lema central da coleção · axioma 57</div></section>""")
    P.append("""<section class="pg nota"><h2 class="sec">Nota da edição</h2>
<p>Este livro reúne os axiomas que o autor formulou entre 6 e 12 de novembro de 2026 — alguns nascidos à beira do leito, outros em conversas sobre família, trabalho, dinheiro e honra. Cada axioma aparece como foi aprovado no catálogo do autor, com número, título e eixo.</p>
<p>Depois do texto vem um <b>comentário</b> curto, escrito para esta edição: o que o axioma propõe, como se aplica e, quando cabe, com quais textos antigos ele dialoga — da Torá ao Dhammapada, de Sêneca aos Analectos. Esses diálogos remetem ao baralho “Escrituras &amp; Axiomas 360X”, do qual este livro é a seção de créditos do autor.</p>
<p>Os axiomas médicos e as hipóteses de pesquisa (93, 103 e 105) não substituem diretrizes nem a avaliação de cada paciente. São registros de raciocínio clínico e de ideias a testar.</p></section>""")
    sm = "".join(f'<li><span class="r">{r}</span><a href="#eixo-{i}">{e(t)}</a><span class="q">{len(por[k])} axiomas</span></li>' for i, (k, r, t, _) in enumerate(EIXOS))
    P.append(f'<section class="pg sum"><h2 class="sec">Sumário</h2><ol>{sm}<li><span class="r">·</span><a href="#indice">Índice numérico</a><span class="q">1–135</span></li></ol></section>')
    for i, (k, r, t, intro) in enumerate(EIXOS):
        blocos = []
        for a in por[k]:
            emo, tnome, _ = TEMAS[a["tema"]]
            d = f"{a['data'][8:10]}/{a['data'][5:7]}/{a['data'][:4]}"
            blocos.append(f"""<article class="ax" id="ax-{a['n']}"><div class="n">Axioma {a['n']}</div><h3>{e(a['tit'])}</h3>
<blockquote>{e(a['enun'])}</blockquote>
<p class="com"><span class="lbl">Comentário.</span> {e(a['com'])}</p>
<div class="meta">Registrado em {d} · {emo} {e(tnome)} · {selo(a['sit'])}</div></article>""")
        P.append(f"""<section class="pg cap" id="eixo-{i}"><div class="num">{r}</div><h2>{e(t)}</h2><p class="intro">{e(intro)}</p>{f'<button class="ouvir-eixo" data-faixa="{i}">🎧 Ouvir este eixo</button>' if tela else ''}<div class="orn">✦ ✦ ✦</div>
{''.join(blocos)}</section>""")
    ind = "".join(f'<div><b>{a["n"]}</b><a href="#ax-{a["n"]}">{e(a["tit"].replace("Axioma ", "").replace("Hipótese ", "Hipótese "))}</a></div>' for a in sorted(ax, key=lambda a: a["n"]))
    P.append(f'<section class="pg" id="indice"><h2 class="sec">Índice numérico</h2><div class="ind">{ind}</div></section>')
    if not tela:
        P.append("""<section class="pg sobre"><h2 class="sec">Sobre o autor</h2>
<div class="espaco">Espaço reservado — texto a ser escrito pelo autor antes da impressão.</div></section>""")
    P.append(f"""<section class="pg colo">{BRASAO}<p><b>Axiomas 360X — edição comentada</b><br>{AUTOR}<br>Sobral · Ceará · {DATA}</p>
<p>Composto em Lora. Parte do Códice 360X e do baralho “Escrituras &amp; Axiomas 360X”.<br>As ideias circulam; o crédito permanece.</p></section>""")
    topo = '<div class="topo"><span class="t">⚜️ Axiomas 360X · edição comentada</span><a href="#sumario-link" onclick="document.querySelector(\'.sum\').scrollIntoView({behavior:\'smooth\'});return false">📑 Sumário</a></div>'
    if tela:
        topo = topo.replace('<a href="#sumario-link"', '<span class="lk"><a href="#leitor">🎧 Ouvir · 🃏 do dia</a> <a href="mapa-axiomas.html">🗺️ Mapa</a> <a href="#sumario-link"').replace('📑 Sumário</a></div>', '📑 Sumário</a></span></div>')
    extra_css = BX.CSS if tela else PRINT_CSS
    extra_js = BX.script(ax, EIXOS) if tela else ""
    return f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Axiomas 360X — edição comentada · {AUTOR}</title><meta name="author" content="{AUTOR}">
<style>{font_face()}{CSS}{extra_css}</style></head><body>{topo if tela else ''}<main class="livro">{''.join(P)}</main>{extra_js}</body></html>"""

def pdf_de(html_path, pdf_path, a5=True):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = b.new_page()
        pg.goto("file://" + html_path)
        pg.wait_for_timeout(500)
        kw = dict(format="A5") if a5 else {}
        pg.pdf(path=pdf_path, print_background=True, prefer_css_page_size=True, display_header_footer=True,
               header_template="<span></span>",
               footer_template='<div style="width:100%;text-align:center;font-family:Georgia,serif;font-size:7.5pt;color:#8a7a55">— <span class="pageNumber"></span> —</div>',
               **kw)
        b.close()
    print("pdf", os.path.basename(pdf_path), os.path.getsize(pdf_path), "bytes")


def main():
    ax = carregar()
    caminho = os.path.join(OUT, "Axiomas_360X_Edicao_Comentada.html")
    open(caminho, "w", encoding="utf-8").write(montar(ax, "tela"))
    print("html", os.path.getsize(caminho), "bytes")
    pdf_de(caminho, os.path.join(OUT, "Axiomas_360X_Edicao_Comentada_A5.pdf"))
    imp = os.path.join(OUT, "Axiomas_360X_Miolo_Impressao.html")
    open(imp, "w", encoding="utf-8").write(montar(ax, "impressa"))
    pdf_de(imp, os.path.join(OUT, "Axiomas_360X_Miolo_Impressao_A5_sangria3mm.pdf"), a5=False)


if __name__ == "__main__":
    main()
