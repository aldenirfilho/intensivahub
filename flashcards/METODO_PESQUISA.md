# 🔬 Método de pesquisa · como produzir e encontrar cards de alto rendimento

Dois sentidos de "pesquisa", ambos cobertos aqui:

1. **🔎 Pesquisar dentro do app** (achar, revisar e atacar pontos fracos)
2. **📚 Pesquisar fontes** para criar cards novos com segurança

---

## 1️⃣ 🔎 Busca dentro do app

Aba **🔎 Buscar** — digite e os resultados aparecem na hora. Depois use **🎴 Estudar resultados**.

| Quero… | Digite |
|---|---|
| Tudo sobre um assunto | `noradrenalina` · `"driving pressure"` |
| Só um tema | escolha no seletor de baralho, ou `deck:sepse` |
| Cards que marquei com 🚩 | `is:marcado` |
| Meus pontos fracos (errei ≥ 3×) | `is:dificil` |
| Revisões vencidas | `is:due` |
| Ainda não estudados | `is:new` |
| Suspensos (para reativar) | `is:suspenso` |
| Por tag | `tag:v2` (cards novos) · `tag:T07` (tema 07) |
| Combinar | `deck:neuro is:dificil` · `hipercalemia is:new` |

> A busca ignora acentos (`hipercalemia` = `hipercalêmia`) e procura em pergunta, resposta, pegadinha, fonte e tags.

### 🎯 Rotina semanal (15 min)

1. `is:dificil` → **Estudar resultados** (ataca as falhas recorrentes)
2. `is:marcado` → reescreva com a IA os cards confusos (prompt com *material-base* = o card + a fonte)
3. Veja qual tema tem mais `is:dificil` → gere +20 cards desse tema na aba **🤖 Prompt IA**

---

## 2️⃣ 📚 Pesquisar fontes para criar cards

### Fluxo em 5 passos

| # | Passo | Ferramenta |
|---|---|---|
| 1 | **Mapear** o que cai: edital TEMI vigente (AMIB) + temas das provas anteriores | site da AMIB |
| 2 | **Escolher a fonte primária** pela hierarquia abaixo | tabela "Hierarquia" |
| 3 | **Extrair** números, cortes, doses e condutas → colar como *material-base* no prompt | 🤖 Prompt IA |
| 4 | **Conferir** cada número no texto original (nunca confiar só na IA) | checklist |
| 5 | **Importar, estudar, marcar** os confusos e refinar | 📥 / 🔎 |

### 🏛️ Hierarquia de fontes (da mais forte para a mais fraca)

| Nível | Fonte | Exemplos |
|---|---|---|
| 🥇 | Diretrizes de sociedades | Surviving Sepsis, KDIGO, Brain Trauma Foundation, AHA/ACC, ESC, IDSA, ADA, ESPEN/ASPEN, AMIB, Ministério da Saúde, CFM/ANVISA (legislação) |
| 🥈 | Ensaios clínicos marcantes | NEJM, JAMA, Lancet (ex.: ARMA, PROSEVA, NICE-SUGAR, TTM2) |
| 🥉 | Revisões sistemáticas / meta-análises | Cochrane, Intensive Care Med |
| 4 | Tratados e plataformas de revisão | UpToDate, livros-texto de UTI |
| 5 | Resumos de cursinho / IA | ⚠️ só como ponto de partida, sempre conferir |

### 🔍 Buscas prontas no PubMed

```
"sepsis"[Title] AND (guideline[pt] OR "practice guideline"[pt]) AND 2021:2026[dp]
"acute respiratory distress syndrome"[Title] AND randomized controlled trial[pt] AND 2020:2026[dp]
("hyponatremia"[Title]) AND (review[pt]) AND "intensive care"
"<tema>" AND (guideline[pt] OR consensus[ti]) AND "critical care"
```

Filtros úteis: **Article type** → Guideline / Randomized Controlled Trial · **Publication date** → últimos 5 anos.

### ✅ Checklist anti-erro (antes de importar)

- [ ] O número do card bate com a fonte original? (dose, unidade, corte)
- [ ] A recomendação é **forte** ("recomenda") ou **fraca** ("sugere")? O card diz isso?
- [ ] A diretriz é a versão mais recente? (anote o ano em `fonte`)
- [ ] Existe pegadinha clássica de prova sobre isso? → campo `pegadinha`
- [ ] O card tem **um** conceito só?

### 🧠 Tipos de card que mais rendem na prova

| Tipo | Exemplo |
|---|---|
| Corte numérico | "Alvo de PPC no TCE?" |
| Droga de escolha | "1ª linha no EME?" |
| Conduta por cenário | "Hipercalemia com QRS largo: 1º passo?" |
| Ensaio clínico → resultado | "PROSEVA mostrou…?" |
| Contraindicação | "Quando NÃO usar succinilcolina?" |
| Comparação | "TRALI × TACO" (tabela) |
| Legislação BR | "ME: intervalo entre exames?" |

---

🛡️ Dica de ouro: peça à IA **"liste as 10 pegadinhas mais cobradas sobre [tema] na prova TEMI e transforme em cards"** e confira cada uma na fonte.
