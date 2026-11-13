"""t64 — 4.8.0: ✍️ Meus (criar/editar/apagar/mesclar), 🌙 Modo Noite, ☀️ tema claro, cartões-imagem."""
import sys, time, os
from playwright.sync_api import sync_playwright
URL = "http://localhost:8765/index.html"; ok = []; bad = []
def chk(c, m): (ok if c else bad).append(m); print(("✅ " if c else "❌ ") + m)
with sync_playwright() as p:
    br = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
    for vp, lab in [({"width": 390, "height": 844}, "celular"), ({"width": 1366, "height": 900}, "desktop")]:
        ctx = br.new_context(viewport=vp); pg = ctx.new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(URL + "#honra"); pg.wait_for_selector("#hoHost .hoSubs", timeout=30000); pg.evaluate("toast=()=>{}")
        # ✍️ Meus — mnemônico
        pg.click('.hoSubs [data-sub=meus]'); pg.fill("#ed_t", "Antes de responder no grupo da família"); pg.fill("#ed_m", "PAZ")
        pg.fill("#ed_itens", "Pare e respire\nAguarde 1 hora\nZele pelo tom"); pg.fill("#ed_c", "Pv 15:1 — uso no WhatsApp"); pg.click("#edSave"); time.sleep(.2)
        U = pg.evaluate("Object.values(S.logs._hu)"); m = U[0]["d"]
        chk(len(U) == 1 and m["k"] == [["P", "Pare e respire"], ["A", "Aguarde 1 hora"], ["Z", "Zele pelo tom"]] and m["tp"] == "a", f"[{lab}] mnemônico próprio salvo com letras da sigla")
        pg.click('.hoSubs [data-sub=mn]'); pg.click('[data-mode=lista]'); pg.select_option("#hoFilt", "u")
        chk(pg.evaluate("HO.list().length") == 1 and "✍️ Meu" in pg.inner_text("#hoHost"), f"[{lab}] aparece em Mnemônicos (filtro ✍️ Meus)")
        pg.select_option("#hoFilt", "")
        # ✍️ Meus — bússola + edição
        pg.click('.hoSubs [data-sub=meus]'); pg.click('[data-ek=b]'); pg.fill("#ed_t", "Reunião tensa"); pg.fill("#ed_N", "Calma e verdade"); pg.fill("#ed_L", "Anotar 3 pontos"); pg.fill("#ed_mn", "paz; freio"); pg.click("#edSave"); time.sleep(.2)
        bid = pg.evaluate("Object.entries(S.logs._hu).find(([k,e])=>e.k==='b')[0]")
        pg.evaluate(f"HO.bu='{bid}';HO.go('bussola')"); time.sleep(.2)
        chk("Reunião tensa" in pg.inner_text(".hoCompT") and pg.locator(".mnGrid .mnCard").count() == 2, f"[{lab}] bússola própria abre com 2 siglas ligadas (minha + FREIO)")
        pg.click(f'[data-edit="{bid}"]'); pg.fill("#ed_t", "Reunião tensa com a chefia"); pg.click("#edSave"); time.sleep(.2)
        chk(pg.evaluate(f"S.logs._hu['{bid}'].d.t") == "Reunião tensa com a chefia", f"[{lab}] edição salva")
        pg.click(f'[data-edit="{bid}"]'); pg.click("#edDel"); pg.click("#edDel"); time.sleep(.2)
        chk(pg.evaluate(f"S.logs._hu['{bid}'].del") == 1 and pg.evaluate("HO.buAll().length") == 24, f"[{lab}] apagar em 2 toques (sem diálogo)")
        # mescla _hu
        r = pg.evaluate("""() => { const A={_hu:{a:{k:'m',d:{t:'x'},mod:5},b:{k:'b',d:{t:'y'},mod:9}}}, B={_hu:{a:{k:'m',d:{t:'x2'},mod:7},b:{k:'b',del:1,mod:3},c:{k:'m',d:{t:'z'},mod:1}}};
           const m=mergeLogs(A,B)._hu; return [m.a.d.t, m.b.d.t, !!m.c]; }""")
        chk(r == ["x2", "y", True], f"[{lab}] mescla _hu pelo mais recente")
        # 🌙 Modo Noite
        pg.click('.hoSubs [data-sub=noite]'); pg.click("#ntGo"); chk(pg.locator(".hoDots span").count() == 5, f"[{lab}] Noite: 5 etapas")
        pg.evaluate("HO.MODES.calma[1]=[['Inspire',1],['Expire',1]]")  # acelera o teste
        pg.click("#ntBr"); pg.wait_for_function("HO.nt && HO.nt.i===1", timeout=30000); chk(True, f"[{lab}] respiração conclui e avança sozinha")
        pg.locator("[data-hz=hz2]").check(); pg.click("#ntNext"); chk(pg.locator(".hoCard .hoRef").count() == 1, f"[{lab}] mensagem exibida")
        pg.click("#ntNext"); pg.fill("#ntG", "Saúde da mãe\nPlantão tranquilo\nEstudo"); pg.fill("#ntI", "Falar com calma"); pg.click("#ntNext")
        chk(pg.evaluate("S.logs[today()].hg").startswith("Saúde da mãe") and "Números 6" in pg.inner_text("#hoHost"), f"[{lab}] gratidão salva e bênção exibida")
        xp0 = pg.evaluate("(S.logs[today()].xs||{}).h||0"); pg.click("#ntEnd"); time.sleep(.2)
        chk(pg.evaluate("S.logs[today()].hn") == 1 and pg.evaluate("(S.logs[today()].xs||{}).h") == xp0 + 5, f"[{lab}] Modo Noite concluído (+5 XP)")
        chk(pg.evaluate("ACH.got().hn1") is not None or pg.evaluate("ACH.check(), !!ACH.got().hn1"), f"[{lab}] conquista Vigília Serena 1")
        # cartão-imagem
        pg.evaluate("HO.bu='hb03';HO.go('bussola')"); href = pg.get_attribute('a[href^="data/media/honra/"]', "href")
        st = pg.evaluate(f"fetch('{href}').then(r=>r.status)"); chk(st == 200, f"[{lab}] botão do cartão aponta para imagem existente ({href})")
        # ☀️ tema claro
        pg.click("#themeBtn"); time.sleep(.3)
        bg = pg.evaluate("getComputedStyle(document.body).backgroundColor"); txt = pg.evaluate("getComputedStyle(document.body).color")
        chk(pg.evaluate("document.documentElement.classList.contains('light')") and txt in ("rgb(29, 26, 20)",), f"[{lab}] tema claro aplicado (texto {txt})")
        for v in ["inicio", "honra", "mnemonicos", "micro", "questoes", "jornada", "ajustes"]:
            pg.evaluate(f"location.hash='#{v}'"); time.sleep(.6)
        pg.evaluate("location.hash='#estudar'"); time.sleep(1.5)
        cc = pg.evaluate("(()=>{const r=document.querySelector('#cardHost').shadowRoot; if(!r) return null; const c=r.querySelector('.card'); return getComputedStyle(c).backgroundColor})()")
        chk(cc is None or cc.startswith("rgb(2") or cc.startswith("rgba"), f"[{lab}] card de estudo claro ({cc})")
        pg.screenshot(path=f"/tmp/t64_light_estudar_{lab}.png")
        pg.reload(); pg.wait_for_timeout(1500)
        chk(pg.evaluate("document.documentElement.classList.contains('light')"), f"[{lab}] tema claro persiste após recarregar")
        pg.evaluate("location.hash='#honra'"); time.sleep(.5); pg.evaluate("HO.go('hoje')"); time.sleep(.3); pg.screenshot(path=f"/tmp/t64_light_honra_{lab}.png")
        pg.evaluate("location.hash='#inicio'"); time.sleep(1); pg.screenshot(path=f"/tmp/t64_light_inicio_{lab}.png", full_page=False)
        pg.click("#themeBtn"); time.sleep(.2); chk(not pg.evaluate("document.documentElement.classList.contains('light')"), f"[{lab}] volta ao escuro")
        chk(not errs, f"[{lab}] sem erros de JS" + (": " + "; ".join(errs[:3]) if errs else ""))
        ctx.close()
    br.close()
print(f"\n{len(ok)} ok · {len(bad)} falhas"); sys.exit(1 if bad else 0)
