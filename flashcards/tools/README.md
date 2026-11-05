# 🧰 tools · gerador do baralho oficial

| Arquivo | Conteúdo |
|---|---|
| `cards_a/b/c.py` | 300 cards da v1 (temas 01–15) |
| `new_a/b/c.py` | 300 cards da v2, cada um com o código do subtema (`N("A", frente, verso, pegadinha, fonte)`) |
| `dataset.py` | temas, subtemas e o mapa de subtema dos cards v1 |
| `images.py` | desenha as 13 ilustrações (matplotlib) em `./media` |
| `modelo.py` | estilo e modelo de nota do .apkg |
| `export.py` | gera `data/decks/*.json`, `data/index.json`, `INDICE_CARDS.md` e `downloads/*.apkg` |

```bash
pip install genanki matplotlib
cd flashcards/tools
python3 export.py ..          # regenera tudo a partir dos .py
# (opcional) python3 images.py && python3 export.py ..   # redesenha as ilustrações
```

Para acrescentar cards a um tema: inclua `N("letra_do_subtema", "pergunta", "resposta", "pegadinha", "fonte")` na lista do tema em `new_*.py`
(ou crie um subtema novo no dicionário do tema em `dataset.py`), rode `export.py` e altere `"versao"` se quiser forçar o aviso de atualização no app.
