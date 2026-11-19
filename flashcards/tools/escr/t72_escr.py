"""t72 — 4.16.0: coleção 📜 Escrituras & Axiomas 360X (1136 cards, 20 baralhos) + ⚜️ livro do autor + créditos."""
import sys
from playwright.sync_api import sync_playwright
URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8765/index.html"; ok = []; bad = []
def chk(c, m): (ok if c else bad).append(m); print(("✅ " if c else "❌ ") + m)
ROOT = "📜 Escrituras & Axiomas 360X"
with sync_playwright() as p:
    br = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
    for vp, lab in [({"width": 390, "height": 844}, "celular"), ({"width": 1366, "height": 900}, "desktop")]:
        ctx = br.new_context(viewport=vp); pg = ctx.new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(URL + "#inicio"); pg.wait_for_function("S && S.cards && S.cards.length>1000", timeout=120000)
        T = f"[{lab}]"
        chk(pg.evaluate("APP_VERSION") == "4.23.1", f"{T} versão 4.23.1")
        col = pg.evaluate("(S.index.colecoes||[]).find(c=>c.id==='escr')")
        chk(bool(col) and col["cards"] == 1136, f"{T} coleção escr no índice com 1136 cards")
        r = pg.evaluate(f"(()=>{{const cs=S.official.filter(c=>c.deck.startsWith({ROOT!r}+'::'));return [cs.length,new Set(cs.map(c=>c.deck)).size,new Set(cs.map(c=>c.id)).size]}})()")
        chk(r == [1136, 20, 1136], f"{T} 1136 cards em 20 baralhos, ids únicos ({r})")
        ax = pg.evaluate(f"S.official.filter(c=>c.deck.startsWith({ROOT!r}+'::20 ')).length")
        chk(ax == 136, f"{T} baralho 20 ⚜️ Axiomas com 136 cards ({ax})")
        chk("Escrituras" in pg.inner_text("#tree"), f"{T} coleção aparece na árvore de baralhos")
        chk("Aldenir Rocha de Oliveira Filho" in pg.inner_text("#homeFoot") and pg.locator("#homeFoot a[href='autor/axiomas-360x.html']").count() == 1, f"{T} créditos do autor e link do livro no rodapé do início")
        chk(pg.locator("#nav a[href='autor/axiomas-360x.html']").count() == 1, f"{T} aba ⚜️ Autor no menu")
        pg.evaluate("location.hash='#estudar'"); pg.wait_for_timeout(400)
        for num, marca in [("20", "Comentário da edição"), ("09", "Surata"), ("19", "Origem real")]:
            pg.evaluate(f"(async()=>{{const c=S.official.find(c=>c.deck.startsWith({ROOT!r}+'::{num} ')); $('#studyEmpty').style.display='none'; $('#cardHost').style.display='block'; await renderInto($('#cardHost'), c.a, 'codice', c.deck)}})()")
            pg.wait_for_timeout(500)
            vt = pg.evaluate("$('#cardHost').shadowRoot.querySelector('.card').innerText")
            chk(marca in vt, f"{T} verso do baralho {num} traz “{marca}”")
            w = pg.evaluate("(()=>{const r=$('#cardHost').shadowRoot,c=r.querySelector('.card');return [c.scrollWidth,c.clientWidth]})()")
            chk(w[0] <= w[1] + 2, f"{T} baralho {num}: card sem estouro horizontal ({w})")
        pg.evaluate("location.hash='#ajustes'"); pg.wait_for_timeout(500)
        chk(pg.locator("#colsBox input[data-col='escr']").count() == 1, f"{T} coleção desligável em ⚙️ Ajustes")
        pg.evaluate("location.hash='#jornada'"); pg.wait_for_timeout(800)
        chk(pg.evaluate("ACH.list.some(a=>/Guardião das Escrituras/.test(a.nome+a.desc))"), f"{T} conquistas da categoria Escrituras na Jornada")
        pg.goto(URL.replace("index.html", "autor/axiomas-360x.html")); pg.wait_for_load_state("load")
        chk(pg.locator("article.ax").count() == 136, f"{T} livro com 136 axiomas")
        chk("ALDENIR ROCHA DE OLIVEIRA FILHO" in pg.inner_text(".capa").upper() and pg.locator(".ax .com").count() == 136, f"{T} capa com o autor e comentário em todos")
        sw = pg.evaluate("[document.documentElement.scrollWidth, innerWidth]")
        chk(sw[0] <= sw[1] + 1, f"{T} livro sem estouro horizontal ({sw})")
        pg.click(".topo a[href='../index.html#inicio']"); pg.wait_for_function("S && S.cards && S.cards.length>1000", timeout=120000)
        chk(True, f"{T} link ← Códice volta ao app")
        pg.evaluate("document.documentElement.classList.add('light')"); pg.wait_for_timeout(200)
        chk(not errs, f"{T} sem erros de JS {errs[:2]}")
        ctx.close()
    br.close()
print(f"\n{len(ok)} ok · {len(bad)} falhas"); sys.exit(1 if bad else 0)
