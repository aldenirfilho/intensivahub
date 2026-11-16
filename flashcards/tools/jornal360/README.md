# 📰 Jornal 360 · Pílulas do Dia no Códice 360X

Cada edição do Jornal Diário 360 vira um baralho da coleção **j360** (pacote `pack-9-j360`).

1. Salve `edicoes/AAAA-MM-DD.json` com `data`, `numero`, `tema`, `jornal` (link da leitura no celular) e
   `cards` = lista de `[área, frente, verso, pegadinha, fonte]` (área: TEMI, R3, POCUS, ECG ou VM).
2. Rode `python3 tools/jornal360/build_pack9.py . <versão>` dentro de `flashcards/` (mexe só no pack 9 e no índice).
3. Faça commit: o app mostra “nova versão disponível”.

Conteúdo educativo; doses e cortes vêm das fontes citadas na edição. Siga o protocolo institucional.
