# 🤖 Prompt-mestre · gerar flashcards para o CÓDICE 360X

Funciona no **Claude, ChatGPT, Grok, Gemini, DeepSeek** ou qualquer IA de texto.

> 💡 O jeito mais fácil é usar a aba **🤖 Prompt IA** do app: ela preenche este prompt automaticamente com tema, subtema, quantidade e material. Use este arquivo quando quiser copiar à mão.

---

## 📋 Copie a partir daqui

````text
Você é um gerador de flashcards de alta qualidade para o app CÓDICE 360X (estudo para a prova de título TEMI/AMIB em Medicina Intensiva e R3 de Clínica Médica).

🎯 TAREFA
Crie exatamente [N] flashcards sobre: [TEMA] › [SUBTEMA].
Nível: Prova TEMI (AMIB) – avançado. Idioma: português do Brasil.

📄 MATERIAL-BASE (opcional — apague esta seção se não for usar)
Use APENAS o conteúdo abaixo como fonte factual; não acrescente dados que não estejam nele:
"""
[COLE AQUI O TEXTO DA AULA / APOSTILA / DIRETRIZ]
"""

✅ REGRAS DE CONTEÚDO
1. Um conceito por card. Pergunta direta e específica (critério, corte numérico, dose, conduta, droga de escolha, contraindicação, ensaio clínico marcante, pegadinha de prova).
2. Baseie-se em diretrizes atuais e ensaios clínicos de referência. Preencha "fonte" com a referência curta (ex.: "SSC 2021", "KDIGO 2012", "PROSEVA NEJM 2013"). NUNCA invente referência, dose ou número; na dúvida, não crie o card.
3. Maioria pergunta → resposta; cerca de 1 em cada 4 no formato lacuna (cloze) com {{c1::termo}} na "frente".
4. "verso": curto e escaneável (≤ 60 palavras OU uma tabela pequena). Comece com 1 emoji. Use <b>negrito</b> nos números-chave e as cores: <b class=r>perigo/erro</b>, <b class=g>alvo/correto</b>, <b class=y>atenção</b>, <b class=c>destaque</b>.
5. Tabelas em HTML simples: <table class=t><tr><th>A</th><th>B</th></tr><tr><td>..</td><td>..</td></tr></table>. Listas: <ul><li>..</li></ul>. Quebra de linha: <br>.
6. "pegadinha": 1 frase com a pegadinha de prova, o erro comum ou uma curiosidade nerd.
7. "subtema": nome curto do subtema (3–5 palavras) para organizar o baralho.
8. "tags": 2–4 palavras-chave sem espaços (ex.: "vasopressor", "SSC2021").
9. "imagem": quando um esquema visual ajudar MUITO (curva, algoritmo, escala, comparação), desenhe um SVG inline simples: <svg viewBox="0 0 600 300" xmlns="http://www.w3.org/2000/svg">…</svg>, fundo transparente, textos em fill="#e8e6df" font-size 16–20, cores #4dd4ff #d4af37 #ff6b6b #5be38a, sem <script>, sem imagens externas. No máximo 1 SVG a cada 5 cards; nos demais deixe "imagem": "".

📦 FORMATO DE SAÍDA (obrigatório)
Responda SOMENTE com um único bloco ```json válido, sem nenhum texto antes ou depois, exatamente nesta estrutura:
```json
{
  "formato": "codice360x-v1",
  "baralho": "TEMI 2028::[NN EMOJI TEMA]",
  "cards": [
    {
      "subtema": "…",
      "frente": "…",
      "verso": "…",
      "pegadinha": "…",
      "fonte": "…",
      "tags": ["…", "…"],
      "imagem": ""
    }
  ]
}
```
Use aspas duplas, escape aspas internas com \", sem vírgula sobrando no fim. Atributos HTML sem aspas (ex.: class=t) para não quebrar o JSON.
Se a resposta ficar longa demais, entregue em partes de no máximo 25 cards, cada parte como um bloco JSON completo, e avise "Parte 1/2".
````

---

## 🧩 Dicas por IA

| IA | Dica |
|---|---|
| **Claude** | Ótimo para SVG e tabelas. Peça até 40 cards por resposta. |
| **ChatGPT** | Se tiver "executar código", peça: *"salve também como arquivo .json para download"* → arraste o arquivo no app. |
| **Grok / Gemini** | Peça 20–25 por vez. Se vier texto fora do JSON, não tem problema: o app ignora. |
| **Qualquer uma** | Para usar sua apostila: cole o texto no campo **Material-base** → a IA fica presa ao seu material. |

## 🏷️ Nomes de baralho dos temas oficiais

Use exatamente estes nomes em `"baralho"` para os cards novos caírem dentro do tema certo:

```
TEMI 2028::01 🦠 Sepse e Choque Séptico
TEMI 2028::02 🫁 Ventilação Mecânica e SDRA
TEMI 2028::03 ❤️ Hemodinâmica e Choque
TEMI 2028::04 ⚗️ Distúrbios Ácido-Base
TEMI 2028::05 🧂 Eletrólitos
TEMI 2028::06 🫘 Rim, LRA e TRS
TEMI 2028::07 🧠 Neurointensivismo
TEMI 2028::08 😴 Sedação, Analgesia e Delirium
TEMI 2028::09 ⚡ Cardiointensivismo e PCR
TEMI 2028::10 🧫 Infecção e Antimicrobianos
TEMI 2028::11 🩸 Hematologia, Coagulação e Transfusão
TEMI 2028::12 🍬 Endocrinologia no Crítico
TEMI 2028::13 🫃 Gastro, Fígado e Nutrição
TEMI 2028::14 🚑 Trauma, Toxicologia e Ambiental
TEMI 2028::15 ⚖️ Ética, Escores, Qualidade e POCUS
```

## 🧾 Formato aceito pelo app (referência técnica)

| Campo | Obrigatório | Aceita também |
|---|---|---|
| `frente` | ✅ | `front`, `pergunta`, `question` |
| `verso` | ✅ | `back`, `resposta`, `answer` |
| `subtema` | — | `subtopic`, `subdeck` → vira sub-baralho |
| `pegadinha` | — | `extra`, `nerd`, `dica` |
| `fonte` | — | `source`, `referencia` |
| `imagem` | — | SVG inline, `data:image/...`, URL, ou nome de arquivo presente em `"midia"` |
| `tags` | — | lista ou texto separado por vírgulas |
| `midia` (raiz) | — | `{ "nome.png": "data:image/png;base64,..." }` |

Cloze: `{{c1::resposta}}` e `{{c1::resposta::dica}}` → gera 1 card por número (c1, c2…).
