#!/usr/bin/env python3
"""128 cartões 1080×1920 para tela de bloqueio (mesmo desenho do botão 🖼️ do livro) + ZIP,
folha de contato em PDF e roteiro do audiolivro (texto que a voz do aparelho lê, faixa por faixa)."""
import base64
import os
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_book import EIXOS, OUT, carregar  # noqa: E402

LIVRO = os.path.join(OUT, "Axiomas_360X_Edicao_Comentada.html")
DIR = os.path.join(OUT, "cartoes")


def main():
    os.makedirs(DIR, exist_ok=True)
    ax = sorted(carregar(), key=lambda a: a["n"])
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = b.new_page()
        pg.goto("file://" + LIVRO)
        pg.wait_for_timeout(600)
        for a in ax:
            url = pg.evaluate(f"window.cartaoDataURL({a['n']}, .9)")
            open(os.path.join(DIR, f"Axioma_{a['n']:03d}.jpg"), "wb").write(base64.b64decode(url.split(",", 1)[1]))
        # roteiro: o mesmo texto, nos mesmos pedaços, que o audiolivro lê
        partes = []
        for i in range(len(EIXOS)):
            fila = pg.evaluate(f"window.AXLIVRO.fila({i})")
            partes.append("\n".join(x["t"] for x in fila))
        # folha de contato A4 (16 por página)
        imgs = "".join(f'<img src="cartoes/Axioma_{a["n"]:03d}.jpg">' for a in ax)
        folha = os.path.join(OUT, "_contato.html")
        open(folha, "w").write(f"""<!DOCTYPE html><html><head><style>@page{{size:A4;margin:8mm}}body{{margin:0;background:#0b0f16}}
.g{{display:grid;grid-template-columns:repeat(4,1fr);gap:3mm}}img{{width:100%;break-inside:avoid;border-radius:2mm}}</style></head><body><div class="g">{imgs}</div></body></html>""")
        pg2 = b.new_page()
        pg2.goto("file://" + folha)
        pg2.wait_for_timeout(800)
        pg2.pdf(path=os.path.join(OUT, "Axiomas_360X_128_cartoes_folha_de_contato_A4.pdf"), format="A4", print_background=True)
        b.close()
    os.remove(folha)
    rot = os.path.join(OUT, "Axiomas_360X_Audiolivro_roteiro.txt")
    cab = ("AXIOMAS 360X — roteiro do audiolivro (voz do aparelho, um eixo por faixa)\n"
           "Axiomas: Aldenir Rocha de Oliveira Filho · comentários da edição Códice 360X\n\n")
    open(rot, "w", encoding="utf-8").write(cab + "\n\n".join(f"===== FAIXA {i + 1} =====\n{t}" for i, t in enumerate(partes)) + "\n")
    z = os.path.join(OUT, "Axiomas_360X_128_cartoes_tela_de_bloqueio.zip")
    with zipfile.ZipFile(z, "w", zipfile.ZIP_STORED) as zf:
        for a in ax:
            zf.write(os.path.join(DIR, f"Axioma_{a['n']:03d}.jpg"), f"Axiomas_360X_cartoes/Axioma_{a['n']:03d}.jpg")
        zf.writestr("Axiomas_360X_cartoes/LEIA-ME.txt",
                    "128 cartões 1080×1920 (topo livre para o relógio do iPhone).\n"
                    "Um por dia: o 'axioma do dia' do livro começa no nº 1 em 17/11/2026 e segue em ciclo.\n"
                    "iPhone: Fotos → compartilhar → Usar como Papel de Parede.\n"
                    "Axiomas de Aldenir Rocha de Oliveira Filho · Códice 360X.\n")
    print("cartões", len(ax), "· zip", os.path.getsize(z), "bytes · roteiro", os.path.getsize(rot), "bytes")


if __name__ == "__main__":
    main()
