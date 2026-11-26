# 🧠 Mnemônicos 360X (app 4.26.0)

**Autor: ALDENIR ROCHA DE OLIVEIRA FILHO · PROJETO 360X**

| Divisão | Mnemônicos | Arquivos |
|---|---|---|
| 🏛️ TEMI 2028 | 408 | `mt01`–`mt10.py` + `extra_sdra.json` |
| 🩺 R3 Clínica Médica | **700** (400 + 300 novos na 4.26.0) | `mr01`–`mr10.py` (originais) · `mr11`–`mr15.py` (novos, 20 por tema) |
| **Total** | **1.108** | `data/mnemonicos.json` · `downloads/Mnemonicos_360X_1108.apkg` |

## ▶️ Gerar

```bash
python3 tools/mn/build_mn.py . --check   # só valida
python3 tools/mn/build_mn.py .           # grava data/mnemonicos.json e o .apkg em downloads/
```

A validação confere cada sigla letra a letra contra a inicial de cada item, exige contexto em todos e recusa título ou conteúdo repetido.

## ✍️ Formato

```
## 01 ❤️ Cardiologia
@ Título
# SIGLA :: item 1; item 2; item 3          (modo sigla: as iniciais têm de bater com as letras)
# 6-30-15 :: 6 = texto; 30 = texto         (modo livre: cada item traz o próprio rótulo)
> contexto (obrigatório)
! dica ou pegadinha (opcional)
^c | ^o                                     (c = clássico da literatura, o = sigla criada no 360X)
```

`;` dentro de parênteses não separa itens.

## ☑️ Checagem dos itens (4.26.0)

| Arquivo | Papel |
|---|---|
| `ck_426.js` | módulo `MNCK`: caixinha em cada item, modo ☑️ Checklist, progresso, exportação e zerar |
| `ck_426.css` | estilos (o tema claro é gerado por `tools/theme/build_light.py`) |
| `inject_426.py` | encaixa o módulo em `app.js` e `index.html` (recusa rodar duas vezes) |
| `t77_ck.py` | teste Playwright em computador e celular: `python3 tools/mn/t77_ck.py 700` |

Registro em `S.logs._nc { id: { b: "1010", c, x, mod } }`, sincronizado pelo `mod` mais recente. Completar um mnemônico dá +1 XP uma única vez.

> ⚠️ Conteúdo de estudo redigido a partir da literatura citada em cada contexto; doses, cortes e esquemas devem ser conferidos na versão vigente das diretrizes.
