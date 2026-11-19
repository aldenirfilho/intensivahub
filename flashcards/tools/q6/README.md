# 🖼️ Lote ilustrado (app 4.24.0) — 400 questões com figura

**QT901–QT1100** (TEMI 2028) e **QR901–QR1100** (R3 Clínica Médica), lote `2026-11-il`.
Cada questão tem uma **figura sintética didática** própria (`fig: {p, k, alt}`), guardada em pacotes de mídia base64
`data/media/qi/{qt,qr}-NN.json` (20 figuras por pacote, PNG ou JPG).

## ▶️ Uso

```bash
python3 tools/q6/build_q6.py .            # gera figuras (cache em tools/q6/out/), pacotes e data/questoes.json
python3 tools/q6/build_q6.py . --check --no-img   # só valida (gabaritos, temas, duplicatas Jaccard ≥ 0,5)
python3 tools/q6/build_q6.py . --only QT950 QR1001 --force   # refaz figuras específicas
python3 tools/q6/build_q6.py . --sheets   # folhas de contato para conferência visual
```

## 🗂️ Arquivos

| Arquivo | Papel |
|---|---|
| `t1.py`–`t9.py` | 200 questões TEMI (tema, enunciado, 5 alternativas com porquê — a correta primeiro —, comentário, pegadinha, referência, figura) |
| `r1.py`–`r8.py` | 200 questões R3 CM |
| `fx.py` | atalhos das figuras: `E()` ECG do compêndio, `V()` VM, `U()` POCUS, `MON()` monitor, `CX()` RX, `CT()` TC, `MI()` microscopia, `TB()` tabela, `LN()` curvas, `FL()` fluxograma, `KM/FO/ROC`, `ROT`, `SP`, `PV`, `EP`, `SC`, `BD`… |
| `figs.py` | despachante `render(spec, path)` |
| `figs_core.py` | gráficos, tabelas, fluxos, KM, forest, ROC, ROTEM, espirometria, alças PV, eletroforese |
| `figs_mon.py` | telas de monitor (ECG, PAI, pleth, capnografia, PVC, PIC, Swan-Ganz) e EEG |
| `figs_img.py` | RX de tórax, TC de crânio, lâminas (sangue, Gram, sedimento, cristais, FAN), cintilografia, mapa corporal |
| `build_q6.py` | montagem: posição do gabarito balanceada (`mk` do q5), checagem de duplicatas contra 1–900, render, pacotes |

## ⚠️ Regras

- Figuras são **sintéticas e didáticas** (não são exames reais de pacientes).
- `tools/q5/build_q5.py` preserva os ids ≥ 901 ao ser rodado de novo.
- O app escolhe o tipo da imagem pela extensão da chave (`.jpg`/`.png`) ou pelo início do base64.
