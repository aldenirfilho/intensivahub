#!/usr/bin/env python3
"""Teste Playwright da ☑️ checagem dos mnemônicos (4.26.0) — computador 1280×900 e celular 390×844.
Servidor: python3 -m http.server 8765 (na pasta flashcards). Uso: python3 tools/mn/t77_ck.py [esperado_r3]
ALDENIR ROCHA DE OLIVEIRA FILHO · PROJETO 360X"""
import asyncio, sys, json
from playwright.async_api import async_playwright
URL = "http://localhost:8765/index.html"
EXP_R3 = int(sys.argv[1]) if len(sys.argv) > 1 else 0
res = []
def ok(c, msg): res.append((bool(c), msg)); print(("✅ " if c else "❌ ") + msg)

async def run(b, tag, vp):
    ctx = await b.new_context(viewport=vp, accept_downloads=True); pg = await ctx.new_page(); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda m: m.type == "error" and "favicon" not in m.text and errs.append(m.text))
    await pg.goto(URL + "#mnemonicos"); await pg.wait_for_timeout(2500)
    ok(await pg.evaluate("APP_VERSION") == "4.26.0", f"{tag} versão 4.26.0")
    await pg.click("#mnHost [data-div='r3']"); await pg.wait_for_timeout(500)
    n3 = await pg.evaluate("MN.all().length")
    if EXP_R3: ok(n3 == EXP_R3, f"{tag} R3 tem {EXP_R3} mnemônicos ({n3})")
    ok(await pg.locator("#mnHost [data-mode='check']").count() == 1, f"{tag} botão ☑️ Checklist")
    # 📖 Consultar: caixinha em cada item
    first = await pg.evaluate("MN.list()[0]"); fid, nk = first["id"], len(first["k"])
    ok(await pg.locator(f"#mnHost .mnCard [data-nck='{fid}']").count() == nk, f"{tag} {nk} caixinhas no 1º cartão")
    await pg.click(f"#mnHost .mnCard [data-nck='{fid}'][data-i='0']"); await pg.wait_for_timeout(200)
    ok(await pg.inner_text(f"[data-ckchip='{fid}']") == f"☑️ 1/{nk}", f"{tag} marcar 1 item → chip 1/{nk}")
    ok(await pg.evaluate(f"S.logs._nc['{fid}'].b.startsWith('1')"), f"{tag} registro _nc salvo")
    xp0 = await pg.evaluate("xpTotal()")
    await pg.click(f"#mnHost .mnCard [data-ckall='{fid}'][data-v='1']"); await pg.wait_for_timeout(300)
    ok(await pg.inner_text(f"[data-ckchip='{fid}']") == f"☑️ {nk}/{nk}", f"{tag} ☑️ Marcar todos → {nk}/{nk}")
    ok(await pg.evaluate("xpTotal()") == xp0 + 1, f"{tag} +1 XP ao completar")
    await pg.click(f"#mnHost .mnCard [data-ckall='{fid}'][data-v='0']"); await pg.wait_for_timeout(200)
    await pg.click(f"#mnHost .mnCard [data-ckall='{fid}'][data-v='1']"); await pg.wait_for_timeout(200)
    ok(await pg.evaluate("xpTotal()") == xp0 + 1, f"{tag} limpar e marcar de novo não dá XP duplicado")
    ok(await pg.inner_text("#mnCkN") == "1", f"{tag} contador do cabeçalho: 1 checado")
    # recarregar: persiste
    await pg.reload(); await pg.wait_for_timeout(2500)
    if await pg.evaluate("MN.div") != "r3": await pg.click("#mnHost [data-div='r3']"); await pg.wait_for_timeout(400)
    ok(await pg.inner_text(f"[data-ckchip='{fid}']") == f"☑️ {nk}/{nk}", f"{tag} checagem persiste após recarregar")
    # ☑️ Checklist
    await pg.click("#mnHost [data-mode='check']"); await pg.wait_for_timeout(500)
    nt = await pg.locator("#mnHost details.ckTema").count(); ntm = await pg.evaluate("new Set(MN.all().map(x => x.tema)).size")
    ok(nt == ntm and nt >= 15, f"{tag} checklist com {nt} temas")
    ok("1 de " in await pg.inner_text("#ckTot"), f"{tag} total geral mostra 1 checado")
    d0 = pg.locator("#mnHost details.ckTema").first
    if not await d0.get_attribute("open"): await d0.locator("summary").click(); await pg.wait_for_timeout(300)
    rows = await d0.locator(".ckRow").count(); tn = await pg.evaluate("MN.list().filter(m => m.tema === MN.all()[0].tema).length")
    ok(rows == tn, f"{tag} 1º tema abre com {tn} linhas ({rows})")
    m2 = await pg.evaluate("MN.list()[1]"); id2 = m2["id"]
    await pg.click(f"#mnHost .ckRow[data-ckrow='{id2}'] .ckX"); await pg.wait_for_timeout(200)
    ok(await pg.locator(f"#mnHost .ckRow[data-ckrow='{id2}'] .ckItems").is_visible(), f"{tag} ▾ mostra os itens")
    await pg.click(f"#mnHost .ckRow[data-ckrow='{id2}'] .ckItems [data-i='0']"); await pg.wait_for_timeout(200)
    ok(await pg.inner_text(f"[data-ckn='{id2}']") == f"1/{len(m2['k'])}", f"{tag} item no checklist → 1/{len(m2['k'])}")
    ok(await pg.evaluate(f"document.querySelector('.nck.big[data-ckall=\"{id2}\"]').classList.contains('part')"), f"{tag} caixa grande fica parcial (–)")
    await pg.click(f"#mnHost .nck.big[data-ckall='{id2}']"); await pg.wait_for_timeout(250)
    ok(await pg.evaluate(f"MNCK.st(MN.all().find(m => m.id === '{id2}'))") == 2, f"{tag} caixa grande completa o mnemônico")
    ok(await pg.inner_text("[data-cktn='t0']").__await__() if False else (await pg.inner_text("[data-cktn='t0']")).startswith("✓ 2/"), f"{tag} progresso do tema atualiza (✓ 2/…)")
    # filtro ☑️ Checados
    await pg.select_option("#mnFilt", "ck"); await pg.wait_for_timeout(400)
    ok(await pg.locator("#mnHost .ckRow").count() == 2, f"{tag} filtro ☑️ Checados → 2")
    await pg.select_option("#mnFilt", "ckp"); await pg.wait_for_timeout(300)
    ok(await pg.locator("#mnHost .ckRow").count() == 0, f"{tag} filtro ◐ em andamento → 0")
    await pg.select_option("#mnFilt", ""); await pg.wait_for_timeout(300)
    # busca no checklist
    await pg.fill("#mnQ", m2["m"]); await pg.wait_for_timeout(700)
    ok(await pg.locator(f"#mnHost .ckRow[data-ckrow='{id2}']").count() == 1, f"{tag} busca encontra no checklist")
    await pg.fill("#mnQ", ""); await pg.wait_for_timeout(700)
    # abrir todos os temas
    await pg.click("#ckOpenAll"); await pg.wait_for_timeout(600)
    tot = await pg.locator("#mnHost .ckRow").count()
    ok(tot == n3, f"{tag} ▾ Abrir os temas → {n3} linhas ({tot})")
    # exportar
    async with pg.expect_download() as dl: await pg.click("#ckExp")
    d = await dl.value; p = await d.path(); txt = open(p, encoding="utf-8").read()
    ok(txt.count("### [x]") == 2 and "ALDENIR ROCHA DE OLIVEIRA FILHO · PROJETO 360X" in txt and txt.count("### [") == n3, f"{tag} exportação .md com {n3} mnemônicos, 2 checados e crédito")
    # sem estouro horizontal
    ow = await pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
    ok(ow <= 1, f"{tag} sem estouro horizontal ({ow})")
    if tag == "celular": await pg.screenshot(path="/tmp/ck_mob.png")
    else: await pg.screenshot(path="/tmp/ck_desk.png")
    # zerar (dois toques)
    await pg.click("#ckReset"); await pg.wait_for_timeout(200)
    ok("Confirmar" in await pg.inner_text("#ckReset"), f"{tag} 1º toque em zerar pede confirmação")
    await pg.click("#ckReset"); await pg.wait_for_timeout(300)
    ok(await pg.evaluate("MNCK.tot(MN.all()).it") == 0, f"{tag} 2º toque zera a checagem")
    # sincronização
    mg = await pg.evaluate("""(() => { const L = { _nc: { a: { b: '10', c: 0, mod: 5 }, b: { b: '1', c: 1, mod: 9 } } }, R = { _nc: { a: { b: '11', c: 1, mod: 7 }, b: { b: '0', c: 0, mod: 3 } } };
      const o = mergeLogs(L, R)._nc; return o.a.b + '|' + o.b.b; })()""")
    ok(mg == "11|1", f"{tag} mergeLogs junta _nc pelo mais recente ({mg})")
    # tema claro
    await pg.evaluate("document.documentElement.classList.add('light')"); await pg.wait_for_timeout(200)
    bg = await pg.evaluate("getComputedStyle(document.querySelector('.ckTema')).backgroundColor")
    ok(bg not in ("rgba(0, 0, 0, 0)",), f"{tag} tema claro aplica fundo ({bg})")
    if tag == "celular": await pg.screenshot(path="/tmp/ck_mob_light.png")
    ok(not errs, f"{tag} sem erro de JS {errs[:2]}")
    await ctx.close()

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        await run(b, "computador", {"width": 1280, "height": 900})
        await run(b, "celular", {"width": 390, "height": 844})
        await b.close()
    bad = [m for c, m in res if not c]
    print(f"\n{len(res) - len(bad)}/{len(res)} ok"); sys.exit(1 if bad else 0)
asyncio.run(main())
