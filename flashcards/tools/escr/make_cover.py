#!/usr/bin/env python3
"""Capa dura aberta (4ª capa + lombada + 1ª capa) do livro Axiomas 360X — arte e gabarito.

Medidas genéricas de capa dura (case wrap); a gráfica escolhida manda o gabarito final:
  miolo 148×210 mm · cartão da capa 3 mm maior na cabeça, no pé e na frente → 151×216 mm
  dobra/canaleta 7 mm de cada lado da lombada · virada 15 mm em volta · lombada estimada abaixo.
Uso: python3 make_cover.py [paginas] [mm_por_folha]"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_book import AUTOR, BRASAO, font_face, OUT  # noqa: E402

PAG = int(sys.argv[1]) if len(sys.argv) > 1 else 96          # 87 páginas → 96 (cadernos de 16)
FOLHA = float(sys.argv[2]) if len(sys.argv) > 2 else 0.11    # offset 90 g/m² ≈ 0,11 mm por folha
CARTAO = 2.5                                                 # papelão de cada capa (mm)
LOMBADA = round(PAG / 2 * FOLHA + 2 * CARTAO + 1, 1)          # miolo + 2 cartões + folga
VIRA, DOBRA, BW, BH = 15, 7, 151, 216
W = VIRA + BW + DOBRA + LOMBADA + DOBRA + BW + VIRA
H = VIRA + BH + VIRA


def html_capa(guias):
    x_quarta = VIRA
    x_lomb = VIRA + BW + DOBRA
    x_prim = x_lomb + LOMBADA + DOBRA
    g = ""
    if guias:
        linhas = [VIRA, VIRA + BW, x_lomb, x_lomb + LOMBADA, x_prim, x_prim + BW]
        g = "".join(f'<div class="gv" style="left:{x}mm"></div>' for x in linhas)
        g += f'<div class="gh" style="top:{VIRA}mm"></div><div class="gh" style="top:{VIRA + BH}mm"></div>'
        g += (f'<div class="nota">GABARITO GENÉRICO · capa dura {W:.1f}×{H:.0f} mm · lombada {LOMBADA} mm ({PAG} p., {FOLHA} mm/folha) · '
              f'virada {VIRA} mm · dobra {DOBRA} mm · confirmar com a gráfica</div>')
    return f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"><style>{font_face()}
@page{{size:{W}mm {H}mm;margin:0}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:{W}mm;height:{H}mm;position:relative;overflow:hidden;background:#0b0f16;color:#efe6cf;font-family:'LoraLivro',Georgia,serif}}
.fundo{{position:absolute;inset:0;background:radial-gradient(ellipse at {x_prim + BW / 2}mm 45%,rgba(212,175,55,.16),transparent 55%),radial-gradient(ellipse at {x_quarta + BW / 2}mm 55%,rgba(34,184,214,.08),transparent 60%),linear-gradient(180deg,#070a10,#101826)}}
.moldura{{position:absolute;border:0.6mm solid rgba(212,175,55,.6);outline:0.25mm solid rgba(212,175,55,.3);outline-offset:-2.2mm}}
.prim{{position:absolute;left:{x_prim}mm;top:{VIRA}mm;width:{BW}mm;height:{BH}mm;text-align:center}}
.prim .brasao{{width:52mm;height:auto;margin:30mm auto 6mm;display:block}}
.prim .sup{{font-family:-apple-system,'Segoe UI',sans-serif;font-size:7.5pt;letter-spacing:2.5pt;color:#22b8d6;text-transform:uppercase}}
.prim h1{{font-size:30pt;letter-spacing:3pt;color:#d4af37;margin:5mm 0 3mm;font-weight:700}}
.prim .sub{{font-style:italic;font-size:11pt;color:#f3ead2;padding:0 18mm;line-height:1.35}}
.prim .aut{{position:absolute;bottom:22mm;left:0;right:0;font-size:12.5pt;letter-spacing:1.2pt;color:#d4af37;font-variant:small-caps}}
.lomb{{position:absolute;left:{x_lomb}mm;top:{VIRA}mm;width:{LOMBADA}mm;height:{BH}mm;display:flex;align-items:center;justify-content:center}}
.lomb div{{transform:rotate(90deg);white-space:nowrap;font-size:{min(9.5, LOMBADA * 0.85):.1f}pt;color:#d4af37;letter-spacing:1.5pt}}
.lomb b{{color:#22b8d6;font-weight:400;margin:0 3mm}}
.quarta{{position:absolute;left:{x_quarta}mm;top:{VIRA}mm;width:{BW}mm;height:{BH}mm;padding:30mm 20mm 0}}
.quarta blockquote{{font-style:italic;font-size:15pt;line-height:1.4;color:#f3ead2;text-align:center}}
.quarta .who{{text-align:center;font-size:8.5pt;color:#22b8d6;margin-top:4mm;letter-spacing:1pt}}
.quarta p{{font-size:9.5pt;line-height:1.55;margin-top:12mm;color:#e5dcc3;text-align:justify}}
.isbn{{position:absolute;left:{x_quarta + BW - 16 - 42}mm;top:{VIRA + BH - 16 - 24}mm;width:42mm;height:24mm;border:0.3mm dashed rgba(243,234,210,.45);font-family:-apple-system,sans-serif;font-size:6.5pt;color:rgba(243,234,210,.6);display:flex;align-items:center;justify-content:center;text-align:center}}
.gv{{position:absolute;top:0;bottom:0;border-left:0.2mm dashed #22b8d6}}
.gh{{position:absolute;left:0;right:0;border-top:0.2mm dashed #22b8d6}}
.nota{{position:absolute;left:4mm;top:3mm;font-family:-apple-system,sans-serif;font-size:6pt;color:#22b8d6}}
</style></head><body><div class="fundo"></div>
<div class="moldura" style="left:{x_prim + 5}mm;top:{VIRA + 5}mm;width:{BW - 10}mm;height:{BH - 10}mm"></div>
<div class="moldura" style="left:{x_quarta + 5}mm;top:{VIRA + 5}mm;width:{BW - 10}mm;height:{BH - 10}mm"></div>
<div class="quarta"><blockquote>“A prosperidade justa é o reconhecimento da honra e do mérito.”</blockquote><div class="who">AXIOMA 57 · LEMA DA COLEÇÃO</div>
<p>Cento e quarenta e três axiomas formulados entre a beira do leito da terapia intensiva e as conversas sobre família, trabalho, dinheiro e honra. Cada um aparece como o autor o aprovou, seguido de um comentário curto que mostra como se aplica e com quais textos antigos dialoga — da Torá ao Dhammapada, de Sêneca aos Analectos.</p>
<p>Uma edição para ler devagar, um axioma por dia.</p></div>
<div class="isbn">Espaço do código de barras (ISBN)</div>
<div class="lomb"><div>AXIOMAS 360X<b>⚜</b>{AUTOR}</div></div>
<div class="prim">{BRASAO}<div class="sup">Códice 360X · edição comentada</div><h1>AXIOMAS 360X</h1>
<div class="sub">Cento e quarenta e três axiomas de medicina, honra e humanidade</div><div class="aut">{AUTOR}</div></div>
{g}</body></html>"""


def main():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome")
        for guias, nome in ((False, "Axiomas_360X_Capa_Dura_arte.pdf"), (True, "Axiomas_360X_Capa_Dura_gabarito.pdf")):
            f = os.path.join(OUT, nome.replace(".pdf", ".html"))
            open(f, "w", encoding="utf-8").write(html_capa(guias))
            pg = b.new_page()
            pg.goto("file://" + f)
            pg.wait_for_timeout(400)
            pg.pdf(path=os.path.join(OUT, nome), print_background=True, prefer_css_page_size=True)
            if guias:
                pg.set_viewport_size({"width": int(W * 3.78), "height": int(H * 3.78)})
                pg.screenshot(path=os.path.join(OUT, "Axiomas_360X_Capa_Dura_previa.png"), full_page=True)
            pg.close()
        b.close()
    print(f"capa {W:.1f}×{H:.0f} mm · lombada {LOMBADA} mm ({PAG} p.)")


if __name__ == "__main__":
    main()
