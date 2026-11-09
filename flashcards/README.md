# 🛡️ CÓDICE 360X · Flashcards TEMI

> App próprio de flashcards com **repetição espaçada** (estilo Anki) para a prova **TEMI 2028** (AMIB) e o **R3 de Clínica Médica**.
> **v5.4 · app 4.2.0 · 8.732 notas + 800 questões + 200 micropartículas** — 🏛️ TEMI 2028 **1.625** · 🩺 R3 **334** + ⚡ **R3 Turbo 360X 1.000** (128 imagens didáticas; [.apkg](downloads/R3_Turbo_360X_1000_flashcards.apkg)) · 🧩 Números de ouro **103** · ✅ IAs 360X curados **4.582** · 🤖 Grok **303** · 🧹 Outras IAs curadas **785** (curadoria 100%) · ❓ Questões 400 TEMI + 400 R3 (lotes 1–3: +300 casos longos por divisão) com comentário por alternativa · 🗺️ Mapa de domínio por tema (questões + simulados) · 💊 Micropartículas com comentário · 🏆 Jornada: 69 conquistas (medalhas, troféus, títulos, brasões, honrarias), ranking semanal e painel de XP · 📱/🖥️ celular e desktop.

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
| 🏛️ Coleções oficiais | **TEMI 2028: 1.625 cards** (15 temas + 16 🫁 Ventilação Mecânica 502 + 17 🔊 USG POCUS 503) · **R3 Clínica Médica: 334** · **Outras IAs: 3.864** (Dr Aldenir 864 + 3000) · **IAs 360X: 7.233** (2 baralhos de 5.000 sem duplicatas; só no GitHub Pages) |
| 📊 Painel | Previsão de revisões (14 dias), atividade dos últimos 30 dias com % de acerto, progresso por coleção e por tema |
| 🧠 Repetição espaçada | Algoritmo SM-2 estilo Anki (De novo / Difícil / Bom / Fácil), limites diários configuráveis |
| 📦 Importa `.apkg` | Pacotes do Anki (legado e Anki 2.1.50+), com imagens, cloze e estilos |
| 🤖 Importa JSON de IA | Cole a resposta do Claude, ChatGPT, Grok ou Gemini — o app limpa ` ```json ` e texto extra |
| 📝 Importa TXT/CSV | Linhas `frente ; verso ; pegadinha ; tags` |
| 🔎 Busca | Texto livre + filtros `tag:` `deck:` `is:new` `is:due` `is:marcado` `is:dificil` → **estudar os resultados** |
| 🚩 Marcar / ⏸️ Suspender / ↩️ Desfazer | Durante o estudo (atalhos M, S, Z) |
| 🛟 Backup | Exporta/restaura tudo (cards + imagens + progresso) em um `.json` → leva para outro aparelho |
| 📥 Também para o Anki | [`TEMI_2028_1625`](downloads/TEMI_2028_1625_flashcards.apkg) · [`TEMI_VM_POCUS_1005`](downloads/TEMI_2028_VM_POCUS_1005_flashcards.apkg) · [`R3_Clinica_Medica_334`](downloads/R3_Clinica_Medica_334_flashcards.apkg) |

## ➕ Adicionar mais cards

Veja **[COMO_ADICIONAR.md](COMO_ADICIONAR.md)** — resumo:

1. Aba **🤖 Prompt IA** → escolha tema, subtema e quantidade → **📋 Copiar prompt**
2. Cole no Claude / ChatGPT / Grok / Gemini
3. Copie o bloco JSON da resposta → aba **📥 Importar** → **Colar** → **✅ Importar**

Prompt-mestre completo: **[PROMPT_IA.md](PROMPT_IA.md)** · Método de pesquisa: **[METODO_PESQUISA.md](METODO_PESQUISA.md)** · Lista dos cards oficiais: **[INDICE_CARDS.md](INDICE_CARDS.md)**

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
