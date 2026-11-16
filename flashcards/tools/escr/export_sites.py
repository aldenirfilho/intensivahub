#!/usr/bin/env python3
"""Cópias do livro ⚜️ Axiomas 360X e do 🗺️ mapa para outros sites do Projeto 360X.

Uso: python3 export_sites.py <pasta_destino> "<nome do site>"
Cria <pasta_destino>/axiomas-360x.html e mapa-axiomas.html com a volta para o início do site
e os downloads apontando para o Códice 360X (GitHub Pages)."""
import os
import sys

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
CODICE = "https://aldenirfilho.github.io/intensivahub/flashcards/"


def main(dest, site):
    os.makedirs(dest, exist_ok=True)
    livro = open(os.path.join(OUT, "Axiomas_360X_Edicao_Comentada.html"), encoding="utf-8").read()
    livro = livro.replace('<div class="topo"><span class="t">',
                          f'<div class="topo"><a href="../index.html">← {site}</a><span class="t">', 1)
    livro = livro.replace('href="../downloads/', f'href="{CODICE}downloads/')
    livro = livro.replace('<a class="bt" href="mapa-axiomas.html">🗺️ Mapa dos eixos e temas</a>',
                          f'<a class="bt" href="mapa-axiomas.html">🗺️ Mapa dos eixos e temas</a><a class="bt" href="{CODICE}index.html#inicio">📜 Flashcards no Códice 360X</a>', 1)
    open(os.path.join(dest, "axiomas-360x.html"), "w", encoding="utf-8").write(livro)
    mapa = open(os.path.join(OUT, "mapa-axiomas.html"), encoding="utf-8").read()
    mapa = mapa.replace('<a href="../index.html#inicio">← Códice 360X</a>', f'<a href="../index.html">← {site}</a>', 1)
    open(os.path.join(dest, "mapa-axiomas.html"), "w", encoding="utf-8").write(mapa)
    print(dest, "ok")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
