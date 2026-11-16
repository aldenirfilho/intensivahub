# 🔎 Conferência das referências — 📜 Escrituras & Axiomas 360X (16/11/2026)

**Resultado:** 1.000 referências revisadas · **735 conferidas no texto-fonte** · 264 revisadas sem o texto-fonte à mão · **0 referência errada encontrada** · 1 numeração a confirmar.

## 📊 Por subbaralho

| # | Subbaralho | Cards | Conferidos no texto-fonte | Fonte usada |
|---|---|---|---|---|
| 01–07 | Bíblia (Torá → Apocalipse) | 385 | **385** | Almeida Corrigida Fiel (thiagobodruk/biblia) |
| 08 | Talmude, Mishná & Pirkei Avot | 60 | **60** | Sefaria (bucket público sefaria-export, tradução William Davidson/Steinsaltz) |
| 09 | Alcorão | 100 | **100** | Tradução Helmi Nasr (fawazahmed0/quran-api) |
| 10 | Budismo | 80 | **73** | SuttaCentral bilara-data (Sujato; Vinaya: Brahmali) |
| 11 | Confúcio, Mêncio & Clássicos | 60 | **57** | Texto chinês (chinese-poetry: 論語, 孟子, 中庸, 大學) |
| 12 | Taoísmo | 40 | **29** | Tao Te Ching, trad. Legge (Gutenberg nº 216, espelho GITenberg) |
| 13 | Hinduísmo | 40 | **19** | Bhagavad Gita (gita/gita) |
| 16 | Outras tradições | 40 | **12** | Livro de Mórmon e D&C (bcbooks/scriptures-json) |
| 14, 15, 17, 18, 19 | Estoicos, filosofia, medicina, personalidades, mitos | 195 | 0 | revisados sem o texto-fonte à mão (2 de Epicteto conferidos por amostragem: Discursos 1.15 e 2.17) |

## ⚙️ Método
1. `verify_escr.py` resolve cada referência no texto-fonte e marca **inexistente** se o capítulo/versículo não existe → **nenhum caso**.
2. Fontes em português (Bíblia, Alcorão): sobreposição de palavras entre o card e o versículo; abaixo de 34% vai para leitura humana (19 casos; todos corretos — paráfrases).
3. Fontes em inglês, chinês e sânscrito: leitura humana de cada par card × trecho (220 casos); Talmude e Mishná por busca da frase-chave no fólio.
4. Os 12 cards com pontuação mais baixa entre os aprovados automaticamente foram relidos: corretos.

## ⏳ A confirmar (1)
- **ESC-14-051 · Sêneca, Sobre a Providência 5.9** — "O fogo prova o ouro; a desgraça, os homens fortes" (*Ignis aurum probat, miseria fortes viros*). A frase existe no capítulo 5; edições a numeram como 5.9 ou 5.10. Conferir no texto latino antes de imprimir.

## 📝 Nuances registradas (não são erros)
- **Dhammapada 6** — segue a leitura clássica ("aqui todos haveremos de morrer"); Sujato traduz "contenhamo-nos".
- **Talmude, Sanhedrin 37a** — o texto impresso do Bavli diz "uma vida *de Israel*"; a forma universal está em manuscritos da Mishná (Kaufmann) e no Yerushalmi.
- **Provérbios 29:18** — "visão" segue o hebraico *chazon*; a ACF traz "profecia".
- **Alcorão 94:7** — "empenha-te em outra tarefa" é leitura interpretativa; Nasr traz "esforça-te em orar".
- **Analectos** — numeração moderna (ctext) com Legge entre parênteses; **Mêncio** — numeração clássica 2A6 etc. (o arquivo chinês divide os parágrafos de outro modo; os 6 trechos estão no livro certo).
- **Meditações** — numeração moderna (Farquharson/Hays); a tradução Casaubon numera diferente.

## 🧰 Reproduzir
```bash
python3 -I tools/escr/verify_escr.py cards.json <pasta_fontes> verif.json
```
`conferencia.json` guarda o status de cada card (fonte · memória · pendente) e alimenta a linha "🔎 conferido no texto-fonte: …" no verso do card (Anki e app).
