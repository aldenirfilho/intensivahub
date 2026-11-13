"""t65 — 4.9.0: cartões-imagem (Mnemônicos e Honra, favoritos), lembrete .ics do Modo Noite, ?tema=claro."""
import sys, time, base64
from playwright.sync_api import sync_playwright
URL = "http://localhost:8765/index.html"; ok = []; bad = []
def chk(c, m): (ok if c else bad).append(m); print(("✅ " if c else "❌ ") + m)
with sync_playwright() as p:
    br = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
    for vp, lab in [({"width": 390, "height": 844}, "celular"), ({"width": 1366, "height": 900}, "desktop")]:
        ctx = br.new_context(viewport=vp, accept_downloads=True); pg = ctx.new_page(); errs = []; toasts = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(URL + "?tema=claro#mnemonicos"); pg.wait_for_selector(".mnCard", timeout=40000)
        chk(pg.evaluate("document.documentElement.classList.contains('light')"), f"[{lab}] ?tema=claro abre na versão clara")
        pg.evaluate("window._t=[];toast=m=>_t.push(m)")
        pg.locator("[data-img]").first.click(); pg.wait_for_selector(".ciGrid img", timeout=10000)
        src = pg.get_attribute(".ciGrid img", "src"); im = base64.b64decode(src.split(",")[1])
        from PIL import Image; import io; I = Image.open(io.BytesIO(im))
        chk(I.size == (1080, 1920), f"[{lab}] cartão do mnemônico gerado 1080×1920")
        chk(pg.locator(".ciGrid a[download]").count() == 1, f"[{lab}] botão ⬇️ Baixar presente")
        pg.click("#ciX"); chk(pg.locator(".ciOv").count() == 0, f"[{lab}] fecha a janela")
        pg.click("#mnFavImg"); chk(pg.evaluate("_t.some(m=>String(m).includes('Nenhum favorito'))"), f"[{lab}] sem favoritos → aviso")
        pg.locator("[data-fav]").nth(0).click(); pg.locator("[data-fav]").nth(1).click(); pg.click("#mnFavImg")
        pg.wait_for_function("document.querySelectorAll('.ciGrid img').length===2", timeout=10000); chk(True, f"[{lab}] 2 favoritos → 2 cartões")
        pg.click("#ciX")
        # Honra
        pg.evaluate("location.hash='#honra'"); pg.wait_for_selector(".hoSubs"); pg.evaluate("toast=m=>_t.push(m);HO.go('mn')")
        pg.locator("#hoHost [data-img]").first.click(); pg.wait_for_selector(".ciGrid img"); chk(True, f"[{lab}] cartão na aba Honra")
        pg.click("#ciX"); pg.locator("#hoHost [data-fav]").first.click(); pg.click("#hoFavImg"); pg.wait_for_selector(".ciGrid img"); chk(pg.locator(".ciGrid img").count() == 1, f"[{lab}] favoritos da Honra")
        pg.click("#ciX")
        # cartão com mnemônico longo (ajuste de escala) não estoura
        h = pg.evaluate("""(()=>{const m=HO.mnAll().reduce((a,b)=>JSON.stringify(b).length>JSON.stringify(a).length?b:a); const c=document.createElement('canvas').getContext('2d'); let s=1.45; while(s>0.55 && CARDIMG.layout(c,m,s,false)>1730) s-=0.05; return [m.m, s, CARDIMG.layout(c,m,s,false)];})()""")
        chk(h[2] <= 1730, f"[{lab}] maior mnemônico cabe no cartão ({h[0]}, escala {h[1]:.2f})")
        # lembrete
        pg.evaluate("HO.go('noite')"); pg.fill("#ntTime", "03:30")
        with pg.expect_download() as d: pg.click("#ntIcs")
        txt = open(d.value.path(), encoding="utf-8", newline="").read()
        chk("RRULE:FREQ=DAILY" in txt and "BEGIN:VALARM" in txt and "T033000" in txt and "\r\n" in txt and "#honra" in txt, f"[{lab}] .ics diário 03:30 com alarme e link")
        chk(d.value.suggested_filename == "Lembrete_Modo_Noite_360X_0330.ics", f"[{lab}] nome do arquivo ({d.value.suggested_filename})")
        chk(pg.evaluate("localStorage.getItem('ntTime')") == "03:30", f"[{lab}] horário lembrado")
        w = pg.evaluate("document.documentElement.scrollWidth-document.documentElement.clientWidth"); chk(w <= 2, f"[{lab}] sem estouro horizontal no Modo Noite ({w}px)")
        chk(not errs, f"[{lab}] sem erros de JS" + (": " + "; ".join(errs[:3]) if errs else ""))
        ctx.close()
    br.close()
print(f"\n{len(ok)} ok · {len(bad)} falhas"); sys.exit(1 if bad else 0)
