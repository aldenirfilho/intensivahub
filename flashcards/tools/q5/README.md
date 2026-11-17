# ❓ Lote nov/2026 — +300 TEMI e +300 R3 Clínica Médica (app 4.23.0)

| Divisão | Ids novos | Fontes |
|---|---|---|
| 🏥 TEMI | QT601–QT900 | `t1.py` … `t8.py` |
| 🩺 R3 Clínica Médica | QR601–QR900 | `r1.py` … `r7.py` |

- **Formato de cada item:** `(tema, enunciado, [(alternativa, porquê) × 5, a correta primeiro], comentário, pegadinha, referência)`.
- **Builder:** `python3 tools/q5/build_q5.py . [--check]`.
  - Posição do gabarito equilibrada por divisão (semente fixa).
  - Alternativas numéricas em ordem crescente.
  - Campo `"lote": "2026-11"` em cada questão nova.
  - Append idempotente: as questões 1–600 e a divisão gaso ficam intactas.
- **No app:** botão **🆕 Lote nov/2026 · X inéditas de 300** na aba ❓ Questões (blocos de 20, inéditas primeiro).

## 🧹 Controle de duplicatas

1. **Jaccard ≥ 0,5** (no próprio builder) sobre enunciado + alternativa correta, contra o banco 1–600 e dentro do lote.
2. **Cosseno TF-IDF ≥ 0,40**: varredura extra, revisada à mão.
   - Conceito igual com a mesma resposta: o item é substituído.
   - Ângulo diferente (ex.: técnica × limiar da elevação passiva das pernas): o item fica.
3. **Rascunhos descartados:** `drop.py` guarda os 183 itens do 1º rascunho que repetiam conceitos do banco (136 TEMI + 47 R3).
   - Eles foram trocados por temas novos, conferidos por busca de palavras-chave (`t7.py`, `t8.py`, `r7.py` e trocas pontuais).
   - Na revisão final, mais 19 itens (12 + 7) foram trocados pelo mesmo motivo.

## ⚠️ Limites

- As referências são citadas de memória (diretriz/estudo e ano), **a conferir** antes de uso clínico ou de material publicado.
- Ferramenta de estudo para prova; não substitui diretriz institucional nem julgamento clínico.
