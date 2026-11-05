# ➕ Como adicionar mais flashcards

Há **3 caminhos**. Escolha pelo objetivo:

| Caminho | Tempo | Fica onde | Quando usar |
|---|---|---|---|
| 🅰️ **IA → Colar no app** | ~1 min | Só no seu aparelho | Dia a dia (recomendado) |
| 🅱️ **Arquivo .apkg / .json** | ~30 s | Só no seu aparelho | Baralho pronto do Anki ou arquivo que a IA gerou |
| 🅲 **Oficializar no GitHub** | ~3 min | Para todos os aparelhos, versionado | Cards revisados que você quer manter para sempre |

---

## 🅰️ IA → Colar (o mais rápido)

1. No app, aba **🤖 Prompt IA**
2. Escolha **tema**, escreva o **subtema** (ex.: *Hiponatremia na HSA*), a **quantidade** e, se quiser, cole seu **material-base**
3. **📋 Copiar prompt** → abra Claude / ChatGPT / Grok / Gemini → cole → enviar
4. Na resposta, copie o bloco JSON (pode copiar a resposta inteira)
5. App → **📥 Importar** → cole na caixa → **✅ Importar**

✅ Pronto: os cards aparecem em **🏠 Início**, dentro do tema e do subtema certos.

> 🔁 Importou de novo o mesmo card? Ele é **atualizado**, não duplicado, e o progresso é mantido.

## 🅱️ Arquivo

- Arraste (ou toque e escolha) na área **📦** da aba **📥 Importar**:
  - `.apkg` do Anki (inclusive de outras pessoas e do AnkiWeb) — imagens e cloze inclusos
  - `.json` gerado pela IA
  - `.txt`/`.csv` com `frente ; verso ; pegadinha ; tags` (uma linha por card)

## 🅲 Oficializar no GitHub (fica no "baralho oficial")

**Pelo site do GitHub (sem programar):**

1. Salve o JSON da IA como arquivo, ex.: `16-extras.json`
2. GitHub → `intensivahub/flashcards/data/decks/` → **Add file → Upload files** → envie → **Commit**
3. Abra `flashcards/data/index.json` → ✏️ editar → adicione no fim da lista `decks`:
   ```json
   ,{"colecao": "temi", "arquivo": "data/decks/16-extras.json", "tema": "16 ➕ Extras", "cards": 20, "subtemas": []}
   ```
   e altere `"versao"` (ex.: `"2026.11.20-620"`) → **Commit**
4. Em ~1 min o app mostra **"nova versão disponível"** → **Atualizar baralho oficial**

**Pelo Claude:** mande o JSON (ou o material) e peça: *"adicione estes cards ao baralho oficial do CÓDICE 360X no intensivahub"*.

**Pelo código** (pasta `tools/`): edite os arquivos `new_*.py`/`cards_*.py`, rode `python3 export2.py ..` e faça commit — isso regera os JSON, o índice e o `.apkg` de uma vez.

---

## ✅ Checklist de qualidade antes de oficializar

- [ ] Um conceito por card, pergunta específica
- [ ] Número, dose e corte conferidos na fonte original
- [ ] Campo `fonte` preenchido (diretriz/ensaio + ano)
- [ ] Verso curto (≤ 60 palavras ou uma tabela)
- [ ] Sem dados de pacientes
