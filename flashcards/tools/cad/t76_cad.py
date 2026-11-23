"""Teste dos 📕🗒️💉 Cadernos (4.25.0). Uso: python3 tools/cad/t76_cad.py [url]  — ALDENIR ROCHA DE OLIVEIRA FILHO · PROJETO 360X"""
import asyncio, sys, json
from playwright.async_api import async_playwright
URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8765/index.html"
R = []
def ok(c, m): R.append((bool(c), m)); print(("✅" if c else "❌"), m)
async def run(vp, tag):
    async with async_playwright() as p:
        b = await p.chromium.launch(); ctx = await b.new_context(viewport=vp); pg = await ctx.new_page()
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda m: m.type == "error" and "favicon" not in m.text and errs.append(m.text))
        await pg.goto(URL + "#inicio"); await pg.wait_for_timeout(2500)
        ok(await pg.evaluate("APP_VERSION") == "4.25.0", f"{tag} versão 4.25.0")
        for v in ["erros", "notas", "prescricoes"]: ok(await pg.locator(f'#nav a[data-v="{v}"]').count() == 1, f"{tag} aba {v} no menu")
        ok(await pg.locator("#metaHome .cadStrip").count() == 1, f"{tag} faixa dos cadernos na tela inicial")
        # 💉 prescrições
        await pg.goto(URL + "#prescricoes"); await pg.wait_for_timeout(1200)
        n = await pg.locator("#pxHost .pxItem").count(); ok(n >= 10, f"{tag} lista de prescrições ({n})")
        tot = await pg.evaluate("({n: PX.data.itens.length, a: Object.fromEntries(Object.keys(PX.AREA).map(k => [k, PX.data.itens.filter(p => p.area === k).length]))})")
        ok(tot["n"] == 500 and tot["a"] == {"cm": 170, "uti": 120, "cardio": 110, "emerg": 100}, f"{tag} 500 prescrições em 4 áreas {tot}")
        for ar, q in [("cm", 170), ("uti", 120), ("cardio", 110), ("emerg", 100)]:
            await pg.click(f"#pxHost [data-ar='{ar}']"); await pg.wait_for_timeout(250)
            ok(f"{q} prescri" in await pg.inner_text("#pxHost"), f"{tag} aba {ar} filtra {q}")
        await pg.click("#pxHost [data-ar='']"); await pg.wait_for_timeout(250)
        ok(await pg.locator("#pxCat option").count() == 41, f"{tag} 40 categorias no seletor")
        await pg.fill("#pxKg", "70"); await pg.dispatch_event("#pxKg", "change"); await pg.wait_for_timeout(300)
        await pg.fill("#pxQ", "meningite"); await pg.wait_for_timeout(600)
        await pg.locator("#pxHost .pxItem").first.click(); await pg.wait_for_timeout(400)
        txt = await pg.inner_text("#pxHost .pxDet")
        ok("10,5 mg" in txt or "10 mg" in txt, f"{tag} dose por kg calculada (dexametasona 0,15 mg/kg → máx 10 mg)")
        ok(await pg.locator("#pxHost .cfBox .ceB").count() == 1, f"{tag} botão 📕 na prescrição")
        await pg.click("#pxStudy"); await pg.wait_for_timeout(300)
        ok(await pg.evaluate("Object.values(S.logs._px||{}).some(e=>e.v)"), f"{tag} prescrição marcada como estudada")
        await pg.click("#pxHost .ceB"); await pg.wait_for_timeout(500)
        ok(await pg.evaluate("Object.keys(S.logs._ce||{}).some(k=>k.startsWith('p:'))"), f"{tag} prescrição salva no caderno de erros")
        # doses: mL/h, dose máxima, todas as 500 renderizam sem token cru
        r = await pg.evaluate("""(() => { const g = t => PX.txt(PX.data.itens.find(p => p.ti === t).rx.join(' | '));
            const out = { nora: g('Choque séptico — noradrenalina'), alt: g('AVC isquêmico agudo — trombólise com alteplase'), cad: g('Cetoacidose diabética — protocolo completo') };
            lsSet('pxKg', '120'); out.alt120 = g('AVC isquêmico agudo — trombólise com alteplase'); lsSet('pxKg', '70');
            let cru = 0, vazio = 0; for (const p of PX.data.itens) { const h = PX.rxHTML(p) + PX.plain(p) + ['quando','mon','aj','ci','al'].map(k => PX.fmt(p[k] || '')).join(''); if (/\\{(kg|mlh|mlhh):/.test(h)) cru++; if (!p.quando || !p.mon || !p.al || !p.ref || p.rx.length < 4) vazio++; }
            return Object.assign(out, { cru, vazio }); })()""")
        ok("6,6 mL/h" in r["nora"], f"{tag} noradrenalina 0,1 mcg/kg/min a 64 mcg/mL → 6,6 mL/h (70 kg)")
        ok("63 mg" in r["alt"], f"{tag} alteplase 0,9 mg/kg → 63 mg (70 kg)")
        ok("90 mg (dose máxima)" in r["alt120"], f"{tag} alteplase respeita a dose máxima de 90 mg (120 kg)")
        ok("1050 mL" in r["cad"].replace(".", "") and "7 UI" in r["cad"], f"{tag} CAD: 15 mL/kg → 1.050 mL e 0,1 UI/kg/h → 7 UI")
        ok(r["cru"] == 0 and r["vazio"] == 0, f"{tag} 500 prescrições renderizam sem token cru nem campo obrigatório vazio ({r['cru']}/{r['vazio']})")
        n_det = await pg.evaluate("(() => { let n = 0; for (const p of PX.data.itens) { PX.det(p.id); if (document.querySelector('#pxHost .pxDet h2')) n++; } PX.render(); return n; })()")
        ok(n_det == 500, f"{tag} as 500 fichas abrem ({n_det})")
        # ❓ questão errada → automático
        await pg.goto(URL + "#questoes"); await pg.wait_for_timeout(1500)
        await pg.click("#qzHost [data-st='10']"); await pg.wait_for_timeout(600)
        gab = await pg.evaluate("QZ.block[QZ.i].gab"); await pg.click(f"#qzHost .qzAlt[data-a='{(gab + 1) % 5}']"); await pg.wait_for_timeout(500)
        ok(await pg.evaluate("Object.entries(S.logs._ce||{}).some(([k,e])=>k.startsWith('q:')&&e.src==='a'&&!e.del)"), f"{tag} questão errada entrou sozinha")
        ok("No caderno" in await pg.inner_text("#qzHost .cfBox .ceB"), f"{tag} botão mostra 'No caderno ✓'")
        # 💊 micro: salvar pelo botão + trecho pela seleção
        await pg.goto(URL + "#micro"); await pg.wait_for_timeout(1200)
        await pg.click("#mcHost .ceB"); await pg.wait_for_timeout(500)
        ok(await pg.evaluate("Object.keys(S.logs._ce||{}).some(k=>k.startsWith('m:'))"), f"{tag} micropartícula salva")
        await pg.evaluate("(()=>{const el=document.querySelector('#mcHost .mcTxt');const r=document.createRange();r.selectNodeContents(el);const s=getSelection();s.removeAllRanges();s.addRange(r);})()"); await pg.wait_for_timeout(400)
        await pg.click("#ceHdr"); await pg.wait_for_timeout(500)
        ok(await pg.evaluate("Object.keys(S.logs._ce||{}).some(k=>k.startsWith('s:'))"), f"{tag} trecho selecionado salvo pelo 📕 do cabeçalho")
        # 📕 caderno
        await pg.goto(URL + "#erros"); await pg.wait_for_timeout(800)
        rows = await pg.locator("#ceHost .ceRow").count(); ok(rows >= 4, f"{tag} caderno lista {rows} itens")
        await pg.locator("#ceHost .ceHd").first.click(); await pg.wait_for_timeout(1200)
        ok("carregando" not in await pg.inner_text("#ceHost .ceBody"), f"{tag} item abre com conteúdo")
        await pg.fill("#ceHost .ceNo", "Errei a dose de ataque"); await pg.click("#ceHost [data-a='save']"); await pg.wait_for_timeout(400)
        ok(await pg.evaluate("Object.values(S.logs._ce).some(e=>e.no==='Errei a dose de ataque')"), f"{tag} nota do erro salva")
        await pg.click("#ceRev"); await pg.wait_for_timeout(1200)
        ok(await pg.locator("#ceRvShow").count() == 1, f"{tag} revisão mesclada abre")
        await pg.keyboard.press("Space"); await pg.wait_for_timeout(900); await pg.keyboard.press("2"); await pg.wait_for_timeout(900)
        ok(await pg.evaluate("Object.values(S.logs._ce).some(e=>e.n>=1)"), f"{tag} revisão registrada")
        await pg.click("#ceRvQuit"); await pg.wait_for_timeout(400)
        await pg.click("#ceSelAll"); await pg.wait_for_timeout(300); await pg.click("#ceMerge"); await pg.wait_for_timeout(1500)
        ok(await pg.evaluate("Object.values(S.logs._nb||{}).some(e=>e.tg==='mesclagem')"), f"{tag} mesclagem virou nota")
        # 🗒️ notas
        await pg.goto(URL + "#notas"); await pg.wait_for_timeout(600)
        await pg.fill("#nbTi", "Noradrenalina diluição"); await pg.fill("#nbTx", "4 mg em 250 mL = **16 mcg/mL**"); await pg.fill("#nbTg", "dose, uti"); await pg.click("#nbSave"); await pg.wait_for_timeout(500)
        ok(await pg.locator("#nbHost .nbCard").count() >= 2, f"{tag} nota criada e listada")
        await pg.evaluate("(()=>{for(const e of Object.values(S.logs._nb)) e.due=Date.now()-1000; })()"); await pg.evaluate("NB.render()"); await pg.wait_for_timeout(300)
        ok(await pg.locator("#nbHost .nbDueR").count() >= 2, f"{tag} notas vencidas aparecem em 🔔 Relembrar hoje")
        await pg.locator("#nbHost .nbDueR [data-r='1']").first.click(); await pg.wait_for_timeout(400)
        ok(await pg.evaluate("Object.values(S.logs._nb).some(e=>e.n===1 && e.due>Date.now())"), f"{tag} 'Lembrei' reagenda a nota")
        # sem estouro horizontal
        for v in ["erros", "notas", "prescricoes"]:
            await pg.goto(URL + "#" + v); await pg.wait_for_timeout(700)
            ow = await pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth"); ok(ow <= 1, f"{tag} #{v} sem estouro horizontal ({ow}px)")
        await pg.screenshot(path=f"/tmp/cad_{tag}_px.png")
        await pg.goto(URL + "#erros"); await pg.wait_for_timeout(700); await pg.screenshot(path=f"/tmp/cad_{tag}_ce.png", full_page=True)
        await pg.goto(URL + "#notas"); await pg.wait_for_timeout(700); await pg.screenshot(path=f"/tmp/cad_{tag}_nb.png", full_page=True)
        ok(not errs, f"{tag} sem erro de JS {errs[:3]}")
        await b.close()
asyncio.run(run({"width": 1280, "height": 900}, "desk"))
asyncio.run(run({"width": 390, "height": 844}, "mob"))
f = [m for c, m in R if not c]; print(f"\n{len(R) - len(f)}/{len(R)} ok"); sys.exit(1 if f else 0)
