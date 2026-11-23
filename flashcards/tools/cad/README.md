# 📕🗒️💉 Cadernos (app 4.25.0)

**Autor: ALDENIR ROCHA DE OLIVEIRA FILHO · PROJETO 360X**

Três seções novas do Códice 360X:

| Seção | Rota | O que faz | Onde guarda |
|---|---|---|---|
| 📕 **Caderno de Erros** | `#erros` | Guarda e mescla itens de qualquer seção: flashcards, questões, mnemônicos, micropartículas, casos e fórmulas de gasometria, Honra, prescrições e trechos/tabelas selecionados na tela. Tem nota "por que errei", etiquetas, refazer, revisão mesclada e marcação de dominado. | `S.logs._ce` |
| 🗒️ **Caderno de Notas** | `#notas` | Notas-lembrete dos detalhes que costuma esquecer, com cor, etiquetas, busca e revisão espaçada (1, 3, 7, 15, 30, 60 e 120 dias). | `S.logs._nb` |
| 💉 **Caderno de Prescrições** | `#prescricoes` | 500 modelos de prescrição com "quando usar", ℞ passo a passo, monitorização, ajustes, contraindicações e alertas; doses por kg e vazões em mL/h calculadas pelo peso informado. | `data/prescricoes.json` + `S.logs._px` |

Os três registros entram na sincronização (`mergeLogs`): vale o item com `mod` mais recente; exclusão vira lápide `{mod, del: 1}`.

## ▶️ Como o código entra no app

```bash
python3 tools/cad/inject_425.py .          # injeta cad_module.js + cad_425.css em app.js e index.html (recusa se já injetado)
python3 tools/theme/build_light.py index.html   # refaz as regras do tema claro
python3 tools/cad/t76_cad.py               # teste Playwright (computador 1280×900 e celular 390×844)
```

| Arquivo | Papel |
|---|---|
| `cad_module.js` | módulos `CAD` (comum), `CE` (erros), `NB` (notas) e `PX` (prescrições) |
| `cad_425.css` | estilos das três seções e ajustes do cabeçalho no celular |
| `inject_425.py` | substituições em `app.js` (versão, `CF.box`, `mergeLogs`, rotas, conquistas, XP) e em `index.html` (abas, botão 📕, seções) |
| `t76_cad.py` | 39 verificações por tamanho de tela |

## 📕 Como um item chega ao Caderno de Erros

- Botão **📕 Caderno** dentro da caixa 🎯 de confiança (`CF.box`) — aparece em todas as seções.
- **Automático**: questão respondida errado (ligado por padrão) e flashcard marcado "De novo" (desligado por padrão); os dois se ajustam no próprio caderno.
- **Trecho ou tabela**: selecionar o texto na tela e tocar no 📕 do cabeçalho.

Chaves: `c:` flashcard · `q:` questão · `m:` micropartícula · `n:` mnemônico · `h:`/`hb:` Honra · `g:`/`gf:` gasometria · `p:` prescrição · `s:` trecho.
