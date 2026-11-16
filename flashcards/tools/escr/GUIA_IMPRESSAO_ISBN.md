# 🏛️ Axiomas 360X — versão impressa em capa dura + guia de ISBN (16/11/2026)

> Tudo aqui foi **preparado**, nada foi solicitado, pago ou enviado. Cada passo com custo ou envio depende de você.

## 📦 Arquivos prontos
| Arquivo | O que é |
|---|---|
| `Axiomas_360X_Miolo_Impressao_A5_sangria3mm.pdf` | Miolo 154×216 mm (A5 148×210 + 3 mm de sangria), **83 páginas**, margens espelhadas (miolo 23 mm do lado da costura), numeração no pé, com a página **“Sobre o autor”** reservada |
| `Axiomas_360X_Capa_Dura_arte.pdf` | Capa dura aberta (4ª capa + lombada + 1ª capa), 357×246 mm, sem guias |
| `Axiomas_360X_Capa_Dura_gabarito.pdf` | A mesma capa com as linhas de dobra, lombada e virada marcadas |
| `make_book.py` · `make_cover.py` | Geradores: refazem tudo depois de cada ajuste |

## ✅ Antes de imprimir (em ordem)
1. ✍️ **Revisar os 128 comentários** (lotes de 10 em andamento) — aprovar, reescrever ou cortar.
2. 🖊️ **Escrever o “Sobre o autor”** (6 a 10 linhas; o que você quer que o leitor saiba — formação, prática, por que escreve). Só entra o que você escrever.
3. 🔎 Confirmar a numeração pendente (Sêneca, *Sobre a Providência* 5.9 ou 5.10 — está no baralho, não no livro).
4. 🔢 **ISBN** (passos abaixo) → o número entra na ficha da edição e o código de barras na 4ª capa (caixa tracejada).
5. 📐 Pedir o **gabarito da gráfica** e refazer a capa com a lombada real:
   `python3 make_cover.py <páginas> <espessura_mm_por_folha>` (hoje: 96 p. × 0,11 mm → lombada ≈ 11,3 mm).
6. 🧾 Completar o miolo até múltiplo de 16 (83 → 96 p.: guardas, “Anotações” ou páginas em branco) — a gráfica costuma pedir.
7. 👀 **Prova física** de 1 exemplar antes da tiragem.

## 🔢 ISBN no Brasil — como funciona
- 🏢 **Quem emite:** a **Câmara Brasileira do Livro (CBL)**, agência brasileira do ISBN desde 2020 (antes era a Biblioteca Nacional). Pedido on-line no site da CBL.
- 👤 **Pessoa física pode:** o autor se cadastra como **autor-editor** (com CPF).
- 📚 **Um ISBN por formato:** o impresso em capa dura tem um; um e-book/PDF à venda teria outro.
- 📝 **Dados pedidos:** título, autor, formato, número de páginas, dimensões, assunto/classificação, idioma, data prevista.
- 🏷️ **Código de barras:** EAN-13 gerado a partir do ISBN (a CBL oferece; gráficas também geram) → vai na caixa da 4ª capa.
- 🗂️ **Ficha catalográfica (CIP):** feita por bibliotecário com registro no CRB (a CBL também oferece o serviço) → entra no verso da folha de rosto.
- 💰 **Valores:** mudam; conferir na tabela da CBL no dia do pedido.

## ⚖️ Depois de publicar
- 📮 **Depósito legal** (Lei 10.994/2004): enviar exemplar(es) à **Biblioteca Nacional** — conferir quantidade e prazo no site da BN.
- ©️ **Direito autoral** existe desde a criação (Lei 9.610/1998); o registro no Escritório de Direitos Autorais (EDA/BN) é opcional e serve de prova de data.
- ✍️ **Créditos:** os axiomas são seus; os comentários estão assinalados como “comentário da edição Códice 360X, com assistência do Claude (Anthropic)”. Se você reescrever um comentário, ele passa a ser seu — basta trocar a nota na ficha.

## 🎨 Sugestões de acabamento (para orçar)
- 📄 Miolo: papel pólen 80 g (leitura confortável) ou offset 90 g.
- 📕 Capa dura: papelão 2,5 mm, laminação fosca + **hot stamping dourado** no título e no brasão.
- 🎀 Guardas em azul-obsidiana; fitilho marcador dourado.
