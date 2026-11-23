# 💉 Caderno de Prescrições 360X — 500 modelos (app 4.25.0)

**Autor: ALDENIR ROCHA DE OLIVEIRA FILHO · PROJETO 360X**

> ⚠️ **Modelos para estudo e apoio à decisão.** Foram redigidos de memória a partir das diretrizes citadas em cada ficha e **não passaram por revisão médica independente**. Antes de prescrever: conferir alergias, peso, função renal e hepática, interações, gestação e o protocolo da instituição. A dose final é responsabilidade do prescritor.

## 📊 Conteúdo

| Área | Fichas | Arquivos | Categorias |
|---|---|---|---|
| 🩺 Clínica Médica | 170 | `px01`–`px04` | admissão e sintomáticos, infectologia, endocrinologia, distúrbios hidroeletrolíticos, gastro/hepatologia, nefrologia, pneumologia, hematologia, neurologia, reumatologia, paliativos/oncologia, geriatria |
| ❤️ Cardiologia | 110 | `px05`–`px06` | síndromes coronarianas, insuficiência cardíaca, valvopatias, pericárdio, aorta/vascular, prevenção e lipídios, arritmias, hipertensão, perioperatório |
| 🏥 Medicina Intensiva | 120 | `px07`–`px08` | sepse e infecção grave, sedoanalgesia e delirium, ventilação, nutrição e cuidados diários, choque e hemodinâmica, neurointensivismo, rim e metabolismo, abdome, intoxicações graves e fim de vida |
| 🚑 Emergência | 100 | `px09`–`px10` | reanimação e via aérea, respiratório, neurologia de urgência, metabólico, abdome, psiquiatria, infecções e profilaxias, trauma e acidentes, toxicologia, gineco-obstetrícia/urologia/ORL/olho/pele |

Cada ficha: `id`, `area`, `cat`, `ti`, `quando` (indicação), `rx` (linhas da prescrição), `mon`, `aj`, `ci`, `al`, `ref`, `tags`.

## ▶️ Uso

```bash
python3 tools/px/build_px.py . --check   # só valida
python3 tools/px/build_px.py .           # gera data/prescricoes.json
python3 tools/px/export_caderno.py .     # exporta Markdown, HTML e PDF A4 (183 páginas) em tools/px/out/ (fora do Git)
```

A validação exige pelo menos 4 linhas de ℞, monitorização e alertas preenchidos, título único e fichas sem macro ou marcador malformado.

## ✍️ Como escrever uma ficha

```python
P(CAT, "Título", "Quando usar.",
  ["Linha 1 da prescrição", "@TEV", "Droga 0,1 mg/kg ({kg:0.1:mg:10})"],
  mon="…", aj="…", ci="…", al="…", ref="Diretriz e ano", tags="palavras de busca")
```

| Marcador | O app mostra |
|---|---|
| `{kg:dose:unidade[:máx]}` | dose por kg e o total para o peso informado, respeitando a dose máxima |
| `{mlh:mcg/kg/min:mcg/mL}` | vazão em mL/h para a dose e a concentração indicadas |
| `{mlhh:dose/kg/h:conc/mL}` | vazão em mL/h para doses por hora |
| `@MACRO` (linha inteira) | linha padronizada de `macros.py` (dieta, acesso, profilaxias, monitorização…) |

Campo com `"—"` não é gravado no JSON (a seção some da ficha).

## 🔎 O que foi e o que não foi conferido

- ✅ Conferido por programa: 500 fichas, títulos e ids únicos, marcadores bem formados, concentrações das soluções coerentes com as vazões calculadas, abertura das 500 fichas no app.
- ⚠️ Não conferido: revisão clínica ficha a ficha contra o texto vigente de cada diretriz. As referências foram citadas de memória; doses de soros antiveneno e profilaxias seguem os manuais do Ministério da Saúde e devem ser confrontadas com a nota técnica em vigor.
