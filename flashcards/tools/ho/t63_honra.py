"""t63 — aba 🕊️ Honra: abas internas, cards, treino, mnemônicos, bússolas, filtro, respiração, persistência, sem internet, celular/desktop."""
import json, sys, time
from playwright.sync_api import sync_playwright
URL = "http://localhost:8765/index.html"
ok = []; bad = []
def chk(c, m): (ok if c else bad).append(m); print(("✅ " if c else "❌ ") + m)

with sync_playwright() as p:
    br = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
    for vp, lab in [({"width": 390, "height": 844}, "celular"), ({"width": 1366, "height": 900}, "desktop")]:
        ctx = br.new_context(viewport=vp); pg = ctx.new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(URL + "#honra"); pg.wait_for_selector("#hoHost .hoSubs", timeout=30000)
        D = json.load(open("data/honra.json"))
        chk(pg.locator('#nav a[data-v="honra"]').count() == 1, f"[{lab}] aba 🕊️ Honra no menu")
        chk(pg.locator(".hoSubs [data-sub]").count() == 8, f"[{lab}] 8 abas internas")
        chk(pg.locator(".hoChip").count() == len(D["bu"]), f"[{lab}] {len(D['bu'])} bússolas no 'Como você está agora?'")
        pg.click("#hoMsg"); chk(pg.locator(".hoCard .hoRef").count() == 1, f"[{lab}] mensagem de hoje sob demanda")
        pg.locator("[data-hz=hz1]").check(); time.sleep(.3)
        chk(pg.evaluate("S.logs[today()].hz1") == 1, f"[{lab}] exame da noite grava")
        # cards
        pg.click('[data-sub=cards]'); pg.wait_for_selector(".hoCard")
        chk(pg.locator(".hoCard").count() == 24, f"[{lab}] lista mostra 24 cards")
        n = pg.evaluate("HO.list().length"); chk(n == len(D["cards"]), f"[{lab}] {n} cards carregados")
        pg.select_option("#hoTr", "alcorao"); chk(pg.evaluate("HO.list().every(c=>c.tr==='alcorao')"), f"[{lab}] filtro por tradição")
        pg.select_option("#hoTr", ""); pg.fill("#hoQ", "Liahona"); time.sleep(.5)
        chk(pg.evaluate("HO.list().length") >= 1 and "Liahona" in pg.inner_text("#hoHost"), f"[{lab}] busca 'Liahona'")
        pg.fill("#hoQ", ""); time.sleep(.5)
        pg.click('[data-mode=treino]'); pg.wait_for_selector("#hoShow")
        chk(pg.locator(".hoAp").count() == 0, f"[{lab}] treino esconde a resposta antes de revelar")
        pg.click("#hoHint"); chk(pg.locator(".hoRef").count() == 1, f"[{lab}] dica mostra a referência")
        pg.click("#hoShow"); pg.click('[data-g="2"]'); time.sleep(.2)
        pg.keyboard.press("Space"); pg.keyboard.press("3"); time.sleep(.2)
        R = pg.evaluate("S.logs._h"); chk(len(R) == 2 and all(v["n"] == 1 for v in R.values()), f"[{lab}] 2 treinos gravados em _h (clique e teclado)")
        chk(pg.evaluate("S.logs[today()].hN") == 2, f"[{lab}] contador diário hN")
        # mnemônicos
        pg.click('[data-sub=mn]'); pg.click('[data-mode=lista]'); pg.wait_for_selector(".mnSig")
        chk(pg.evaluate("HO.list().length") == len(D["mn"]), f"[{lab}] {len(D['mn'])} mnemônicos")
        pg.select_option("#hoFilt", "c"); chk(pg.evaluate("HO.list().every(m=>m.o==='c')"), f"[{lab}] filtro clássicos")
        pg.select_option("#hoFilt", "")
        # bússola
        pg.click('[data-sub=bussola]'); pg.locator(".hoChip").nth(2).click(); pg.wait_for_selector(".hoRose")
        chk(pg.locator(".hoDir").count() == 4 and pg.locator(".hoCenter").count() == 1, f"[{lab}] rosa dos ventos N/S/L/O")
        chk(pg.locator(".hoCompT").inner_text().find("PIX") >= 0, f"[{lab}] bússola do PIX urgente abre")
        chk(pg.locator(".mnGrid .mnCard").count() == 3, f"[{lab}] 3 mnemônicos ligados à bússola")
        pg.click("#hoBuOk"); chk(pg.evaluate("S.logs[today()].hbu") == 1, f"[{lab}] uso da bússola registrado")
        pg.locator(".hoRefB").first.click(); pg.wait_for_selector(".hoCard")
        chk(pg.evaluate("HO.sub") == "cards" and pg.evaluate("HO.list().length") >= 1, f"[{lab}] fonte da bússola leva aos cards")
        pg.click('[data-sub=bussola]'); pg.locator(".hoChip").first.click()
        chk(pg.locator(".hoAl").inner_text().find("188") >= 0, f"[{lab}] bússola de aflição mostra CVV 188")
        # filtro
        pg.click('[data-sub=filtro]')
        for i, f in enumerate(D["filtro"]):
            pg.click(f'[data-fa="{i}"][data-v="{1 if f["ok"] else 0}"]')
        chk(pg.locator(".hoVer.g").count() == 1, f"[{lab}] filtro todo 'bom' = verde")
        pg.click('[data-fa="8"][data-v="1"]'); chk(pg.locator(".hoVer.r").count() == 1, f"[{lab}] PIX/dados marcado = vermelho")
        pg.click("#hoFOk"); chk(pg.evaluate("S.logs[today()].hf") == 1, f"[{lab}] filtro registrado")
        # respiração
        pg.click('[data-sub=fluxo]'); pg.select_option("#hoBrN", "3"); pg.click('[data-br=suspiro]'); pg.click("#hoBrGo")
        chk(pg.locator("#hoBrStop").count() == 1, f"[{lab}] respiração inicia (botão Parar)")
        time.sleep(1.2); ph = pg.inner_text("#hoPh"); chk(ph in ("Inspire", "Mais um pouco", "Expire devagar"), f"[{lab}] fase exibida: {ph}")
        pg.wait_for_function("(S.logs[today()]||{}).hb===1", timeout=40000); chk(True, f"[{lab}] 3 ciclos concluídos → hb=1")
        # xp e conquistas
        chk(pg.evaluate("(S.logs[today()].xs||{}).h") > 0, f"[{lab}] XP na fonte 🕊️ Honra")
        chk(pg.evaluate("ACH.list.filter(a=>/^(ho|hb|hu|hn)\\d/.test(a.id)).length") == 15, f"[{lab}] 15 conquistas da Honra")
        # estouro horizontal
        for s in ["hoje", "noite", "cards", "mn", "bussola", "filtro", "fluxo", "meus"]:
            pg.evaluate(f"HO.go('{s}')"); time.sleep(.15)
            w = pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
            if w > 2: chk(False, f"[{lab}] estouro horizontal em {s}: {w}px")
        chk(True, f"[{lab}] sem estouro horizontal nas 8 abas")
        # persistência após recarregar + sem internet
        pg.wait_for_timeout(800); pg.reload(); pg.wait_for_selector("#hoHost .hoSubs", timeout=30000)
        chk(len(pg.evaluate("S.logs._h || {}")) == 2, f"[{lab}] progresso persiste após recarregar")
        ctx.route("**/data/honra.json", lambda r: r.abort()); pg.reload(); pg.wait_for_selector("#hoHost .hoSubs", timeout=30000)
        pg.evaluate("HO.go('cards')"); time.sleep(.3)
        chk(pg.evaluate("HO.data.cards.length") == len(D["cards"]), f"[{lab}] abre sem internet (cópia no aparelho)")
        chk(not errs, f"[{lab}] sem erros de JS" + (": " + "; ".join(errs[:3]) if errs else ""))
        pg.screenshot(path=f"/tmp/t63_{lab}.png", full_page=False)
        ctx.close()
    # mescla _h entre dois aparelhos
    ctx = br.new_context(); pg = ctx.new_page(); pg.goto(URL + "#honra"); pg.wait_for_selector("#hoHost .hoSubs", timeout=30000)
    r = pg.evaluate("""() => { const A = {_h: {x: {n: 2, ok: 1, s: 1, t: 10, f: 5}}}, B = {_h: {x: {n: 3, ok: 2, s: 2, t: 20, u: 7}, y: {n: 1, t: 1}}};
      const m = mergeLogs(A, B); return m._h; }""")
    chk(r["x"]["n"] == 3 and r["x"]["f"] == 5 and r["x"]["u"] == 7 and "y" in r, "mescla _h: treino mais recente + favoritos + itens novos")
    br.close()
print(f"\n{len(ok)} ok · {len(bad)} falhas"); sys.exit(1 if bad else 0)
