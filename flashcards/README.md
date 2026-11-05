# 🛡️ CÓDICE 360X · Flashcards TEMI

> App próprio de flashcards com **repetição espaçada** (estilo Anki) para a prova **TEMI 2028** (AMIB) e o **R3 de Clínica Médica**.
> **900 cards** (600 TEMI + 300 Clínica Médica) · 132 subtemas · 30 ilustrações e gráficos · uma cor por tema.

☁️ **Versão com sincronização automática entre aparelhos:** página do Claude (privada, abre logado) — o progresso fica na sua conta.
💾 **Esta versão (GitHub Pages):** mesma interface, salva só no aparelho (use Backup para levar o progresso).

🔗 **Abrir o app:** https://aldenirfilho.github.io/intensivahub/flashcards/

---

## ⚡ Em 30 segundos

| Passo | O que fazer |
|---|---|
| 1️⃣ | Abra o link acima (no celular: menu do navegador → **Adicionar à tela inicial** para virar app) |
| 2️⃣ | As coleções oficiais já vêm carregadas (TEMI 2028 + R3 Clínica Médica) — ative/desative em ⚙️ Ajustes |
| 3️⃣ | Toque em um tema ou subtema → **Espaço** mostra a resposta → **1–4** para responder |

## 🎴 O que tem dentro

| Recurso | Detalhe |
|---|---|
| 🏛️ Coleções oficiais | **TEMI 2028: 600 cards** (15 temas, 77 subtemas) · **R3 Clínica Médica: 300 cards** (15 temas, 55 subtemas) · 30 ilustrações |
| 📊 Painel | Previsão de revisões (14 dias), atividade dos últimos 30 dias com % de acerto, progresso por coleção e por tema |
| 🧠 Repetição espaçada | Algoritmo SM-2 estilo Anki (De novo / Difícil / Bom / Fácil), limites diários configuráveis |
| 📦 Importa `.apkg` | Pacotes do Anki (legado e Anki 2.1.50+), com imagens, cloze e estilos |
| 🤖 Importa JSON de IA | Cole a resposta do Claude, ChatGPT, Grok ou Gemini — o app limpa ` ```json ` e texto extra |
| 📝 Importa TXT/CSV | Linhas `frente ; verso ; pegadinha ; tags` |
| 🔎 Busca | Texto livre + filtros `tag:` `deck:` `is:new` `is:due` `is:marcado` `is:dificil` → **estudar os resultados** |
| 🚩 Marcar / ⏸️ Suspender / ↩️ Desfazer | Durante o estudo (atalhos M, S, Z) |
| 🛟 Backup | Exporta/restaura tudo (cards + imagens + progresso) em um `.json` → leva para outro aparelho |
| 📥 Também para o Anki | [`TEMI_2028_600`](downloads/TEMI_2028_600_flashcards.apkg) · [`R3_Clinica_Medica_300`](downloads/R3_Clinica_Medica_300_flashcards.apkg) |

## ➕ Adicionar mais cards

Veja **[COMO_ADICIONAR.md](COMO_ADICIONAR.md)** — resumo:

1. Aba **🤖 Prompt IA** → escolha tema, subtema e quantidade → **📋 Copiar prompt**
2. Cole no Claude / ChatGPT / Grok / Gemini
3. Copie o bloco JSON da resposta → aba **📥 Importar** → **Colar** → **✅ Importar**

Prompt-mestre completo: **[PROMPT_IA.md](PROMPT_IA.md)** · Método de pesquisa: **[METODO_PESQUISA.md](METODO_PESQUISA.md)** · Lista dos 600 cards: **[INDICE_CARDS.md](INDICE_CARDS.md)**

## 🗂️ Estrutura

```
flashcards/
├── index.html · app.js          → o app (HTML + JS puro, sem servidor)
├── lib/                         → JSZip, fzstd, sql.js (leitura de .apkg no navegador)
├── data/index.json              → lista dos baralhos oficiais
├── data/decks/NN-tema.json      → 15 arquivos, formato codice360x-v1
├── data/media/                  → ilustrações
├── downloads/                   → .apkg de 600 cards para o Anki
├── tools/                       → scripts Python que geram os dados e o .apkg
└── *.md                         → guias
```

## 🔒 Privacidade e limites

- Os cards e o progresso ficam **só no seu navegador** (IndexedDB). Nada é enviado a servidor.
- Para usar em 2 aparelhos: ⚙️ Ajustes → **Exportar backup** → **Restaurar backup** no outro.
- Limpar dados do navegador apaga o progresso → faça backup de vez em quando.

## ⚠️ Aviso

Conteúdo **educativo** para preparação de prova. Não substitui julgamento clínico, diretrizes atualizadas nem protocolos institucionais. Confira sempre o edital TEMI vigente e as versões mais recentes das diretrizes citadas em cada card.

---
🛡️ Projeto 360X · Dr. Aldenir Rocha · Medicina Intensiva
