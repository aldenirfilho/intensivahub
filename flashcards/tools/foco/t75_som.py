"""t75 — 4.23.0: 🎧 som de estudo (AMB) no ⏳ Foco + ❓ lote nov/2026 (300 TEMI + 300 R3) nas Questões."""
import sys, json, urllib.request
from playwright.sync_api import sync_playwright
BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8765/"; ok = []; bad = []
def chk(c, m): (ok if c else bad).append(m); print(("✅ " if c else "❌ ") + m)

# ---- dados: questoes.json ----
D = json.load(urllib.request.urlopen(BASE + "data/questoes.json"))
chk({k: len(v) for k, v in D.items()} == {"temi": 900, "r3": 900, "gaso": 145}, f"questoes.json: 900 TEMI · 900 R3 · 145 gaso ({ {k: len(v) for k, v in D.items()} })")
for div, pref in [("temi", "QT"), ("r3", "QR")]:
    L = D[div]; ids = [q["id"] for q in L]; nov = [q for q in L if int(q["id"][2:]) >= 601]
    chk(len(set(ids)) == 900 and ids == sorted(ids), f"{div}: 900 ids únicos e em ordem")
    chk(len(nov) == 300 and all(q.get("lote") == "2026-11" for q in nov) and not any(q.get("lote") for q in L if int(q["id"][2:]) <= 600), f"{div}: 300 novas com lote 2026-11; as 600 antigas sem lote")
    chk(all(len(q["alts"]) == 5 and len(q["porque"]) == 5 and 0 <= q["gab"] <= 4 and q["ref"] and q["pega"] and q["com"] for q in nov), f"{div}: 5 alternativas, 5 porquês, gabarito, comentário, pegadinha e referência")
    g = [sum(q["gab"] == i for q in nov) for i in range(5)]
    chk(min(g) >= 50 and max(g) <= 70, f"{div}: gabaritos equilibrados A–E {g}")
    chk(all("<" not in q["enun"].replace("< ", "") for q in nov), f"{div}: enunciados sem '<' que quebre o HTML")
    en = [q["enun"][:60] for q in nov]
    chk(len(set(en)) == 300, f"{div}: sem enunciados repetidos no lote")

with sync_playwright() as p:
    br = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox", "--autoplay-policy=no-user-gesture-required"])
    for vp, lab in [({"width": 390, "height": 844}, "celular"), ({"width": 1366, "height": 900}, "desktop")]:
        T = f"[{lab}]"
        ctx = br.new_context(viewport=vp); pg = ctx.new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(BASE + "index.html#inicio"); pg.wait_for_function("S && S.cards && S.cards.length>1000", timeout=120000)
        ev = pg.evaluate
        chk(ev("APP_VERSION") == "4.23.0", f"{T} versão 4.23.0")
        # ---- síntese dos 5 sons ----
        s = ev("""(()=>{const o={};for(const k of Object.keys(AMB.T)){const b=AMB.make(k);const d=b.getChannelData(0),e=b.getChannelData(1);let q=0,pk=0,nan=0,dif=0;
          for(let i=0;i<d.length;i++){const v=d[i];if(!isFinite(v))nan++;q+=v*v;pk=Math.max(pk,Math.abs(v));} for(let i=0;i<2000;i++)dif+=Math.abs(d[i]-e[i]);
          o[k]=[+(b.duration).toFixed(1),+Math.sqrt(q/d.length).toFixed(3),+pk.toFixed(2),nan,+Math.abs(d[d.length-1]-d[0]).toFixed(3),+(dif/2000).toFixed(3)]}return o})()""")
        for k, (dur, rms, pk, nan, seam, st) in s.items():
            chk(nan == 0 and 11 <= dur <= 32 and 0.09 <= rms <= 0.15 and pk < 1 and seam < 0.25 and st > 0.001, f"{T} {k}: laço {dur} s, RMS {rms}, pico {pk}, emenda {seam}, estéreo {st}")
        # ---- painel na aba Foco ----
        ev("location.hash='#foco'"); pg.wait_for_timeout(300)
        pg.click("[data-fobase='10']"); pg.wait_for_timeout(200)
        chk(pg.locator("[data-amb^='t:']").count() == 5 and pg.locator("[data-amb='tog']").count() == 1 and pg.locator(".ambVol").count() == 1 and pg.locator("[data-amb='auto']").count() == 1,
            f"{T} painel 🎧: 5 sons, tocar/parar, volume e “junto com o bloco”")
        chk(ev("AMB.sel()") == "rosa" and ev("AMB.vol()") == 35 and not ev("AMB.on"), f"{T} padrão: ruído rosa, volume 35, desligado")
        pg.click("[data-amb='t:chuva']"); pg.wait_for_timeout(150)
        chk(ev("lsGet('ambTipo')") == "chuva" and not ev("AMB.on") and "gold" in pg.locator("[data-amb='t:chuva']").get_attribute("class"), f"{T} escolher 🌧️ chuva não toca sozinho")
        pg.click("[data-amb='tog']"); pg.wait_for_timeout(400)
        chk(ev("AMB.on") and ev("AMB.cur") == "chuva" and ev("AMB.ac.state") == "running" and "Parar" in pg.locator("[data-amb='tog']").inner_text(), f"{T} ▶️ toca a chuva (AudioContext {ev('AMB.ac.state')})")
        chk(ev("AMB.ac === FO.ac"), f"{T} som e bipes do foco usam o mesmo AudioContext")
        pg.locator(".ambVol").first.fill("60"); pg.wait_for_timeout(900)
        chk(ev("lsGet('ambVol')") == "60" and abs(ev("AMB.mg.gain.value") - 0.54) < 0.02 and "60" in pg.locator(".ambVolN").first.inner_text(), f"{T} volume 60 grava e ajusta o ganho ({round(ev('AMB.mg.gain.value'), 3)})")
        pg.click("[data-amb='t:mar']"); pg.wait_for_timeout(300)
        chk(ev("AMB.on") and ev("AMB.cur") == "mar", f"{T} trocar de som com ele tocando muda na hora")
        pg.click("[data-amb='tog']"); pg.wait_for_timeout(200)
        chk(not ev("AMB.on") and "Tocar" in pg.locator("[data-amb='tog']").inner_text(), f"{T} ⏹️ para o som")
        # ---- automático com o bloco ----
        pg.click("[data-amb='auto']"); pg.wait_for_timeout(150)
        chk(ev("lsGet('ambAuto')") == "1" and pg.locator("[data-amb='auto']").get_attribute("aria-pressed") == "true", f"{T} 🔁 junto com o bloco ligado")
        pg.click("[data-foan='livre']"); pg.wait_for_timeout(150); pg.fill("#foNm", "Capítulo de sepse"); pg.click("[data-fo='go']"); pg.wait_for_timeout(500)
        chk(ev("AMB.on") and ev("AMB.autoOn") and ev("FO.run.amb") == "mar", f"{T} começar o bloco liga o som escolhido ({ev('FO.run.amb')})")
        chk(pg.locator(".ambMini").count() == 1 and "Tocando" in pg.locator(".ambMini").inner_text(), f"{T} bloco em curso mostra o controle compacto")
        chk(pg.locator("#foBar .ambBarB").inner_text() == "🎧", f"{T} barra do topo com o botão 🎧")
        ev("FO.run.t0-=10*60000; FO.tick()"); pg.wait_for_timeout(500)
        chk(ev("FO.run") is None and ev("FO.end.amb") == "mar" and not ev("AMB.on"), f"{T} fim do bloco: som desliga sozinho e o resumo guarda o som")
        pg.click("[data-foq='4']"); pg.click("[data-fo='salvar']"); pg.wait_for_timeout(500)
        rec = ev("FO.sessions().slice(-1)[0]")
        chk(rec["amb"] == "mar" and rec["cl"] == 1, f"{T} sessão registrada com amb='mar'")
        # botão da barra durante o bloco (sem automático)
        pg.click("[data-fo='novo']"); pg.wait_for_timeout(200)
        pg.click("[data-amb='auto']"); pg.wait_for_timeout(100)
        chk(ev("lsGet('ambAuto')") == "0", f"{T} 🔁 desligado")
        pg.click("[data-fo='go']"); pg.wait_for_timeout(400)
        chk(not ev("AMB.on") and ev("FO.run.amb") == "" and pg.locator("#foBar .ambBarB").inner_text() == "🔇", f"{T} sem automático o bloco começa em silêncio")
        pg.click("#foBar .ambBarB"); pg.wait_for_timeout(300)
        chk(ev("AMB.on") and ev("FO.run.amb") == "mar" and pg.locator("#foBar .ambBarB").inner_text() == "🎧", f"{T} 🎧 na barra liga o som e marca o bloco")
        pg.click("#foBar .ambBarB"); pg.wait_for_timeout(200)
        chk(not ev("AMB.on") and pg.locator("#foBar .ambBarB").inner_text() == "🔇", f"{T} 🎧 de novo desliga")
        pg.click(".ambMini [data-amb='p:branco']"); pg.wait_for_timeout(300)
        chk(ev("AMB.on") and ev("AMB.cur") == "branco", f"{T} controle compacto troca para ⚪ branco")
        pg.click(".ambMini [data-amb='p:branco']"); pg.wait_for_timeout(200)
        chk(not ev("AMB.on"), f"{T} tocar no som que está tocando desliga")
        ev("FO.run.t0-=10*60000; FO.tick()"); pg.wait_for_timeout(400); pg.click("[data-foq='3']"); pg.click("[data-fo='salvar']"); pg.wait_for_timeout(400)
        # ---- N-de-1 e conquistas ----
        ev("""(()=>{const r=FO.R().s, t=Date.now()-9*864e5; for(let i=0;i<8;i++){const a=i<5?'rosa':''; r['z'+i]={t0:t+i*36e5,dur:10,min:a?9.5:7,dv:a?0:2,rt:1,cl:a?1:0,tr:0,q:4,amb:a,an:'livre',nm:'x',done:1,xp:10}}; FO.save&&FO.save(); ACH.check()})()""")
        n = ev("AMB.n1()")
        chk(n["ok"] and n["com"]["n"] == 7 and n["sem"]["n"] == 3 and n["por"][0][0] in ("rosa", "mar", "branco"), f"{T} N-de-1: 7 com som (mar, branco, 5 rosa) × 3 sem som")
        js = ev("(()=>{const s=jStats();return [s.foAmb,s.foN1]})()")
        chk(js[0] >= 5 and js[1] >= 3, f"{T} jStats foAmb={js[0]} foN1={js[1]}")
        pg.wait_for_timeout(600)
        chk(ev("ACH.got().foamb5") is not None and ev("ACH.got().fon1") is not None, f"{T} conquistas 🎧 Trilha do Foco e 🔬 Cientista de Si")
        pg.click("[data-fosub='som']"); pg.wait_for_timeout(300)
        h = pg.locator("#foHost").inner_text()
        chk(pg.locator(".ambT tr").count() >= 4 and "Com som" in h and "Sem som" in h, f"{T} aba 🎧 Sons com a tabela do experimento")
        chk("Com som você" in h or "sem diferença" in h, f"{T} veredito aparece com ≥ 3 blocos de cada lado")
        chk(pg.locator("#foHost a[href^='https://doi.org/']").count() == 3, f"{T} 📘 3 referências com DOI")
        chk("Proteja a audição" in h and "não tratamento" in h, f"{T} aviso de audição e de que não é tratamento")
        sw = ev("[document.documentElement.scrollWidth, innerWidth]")
        chk(sw[0] <= sw[1], f"{T} aba Sons sem estouro horizontal ({sw})")
        # ---- persistência ----
        pg.reload(); pg.wait_for_function("S && S.cards && S.cards.length>1000", timeout=120000)
        chk(ev("AMB.sel()") == "branco" and ev("AMB.vol()") == 60 and not ev("AMB.on"), f"{T} recarregar mantém som e volume, sem tocar sozinho")
        # ---- questões: lote ----
        ev("location.hash='#questoes'"); pg.wait_for_timeout(1500)
        pg.wait_for_function("QZ.data && QZ.data.temi && QZ.data.temi.length===900", timeout=30000)
        ev("QZ.div='temi'; QZ.tema=''; QZ.home()"); pg.wait_for_timeout(200)
        b = pg.locator("[data-st='lote']")
        chk(b.count() == 1 and "300 inéditas de 300" in b.inner_text(), f"{T} TEMI: botão {b.inner_text() if b.count() else '—'}")
        b.click(); pg.wait_for_timeout(300)
        blk = ev("QZ.block.map(q=>q.id)")
        chk(len(blk) == 20 and all(int(i[2:]) >= 601 for i in blk), f"{T} bloco do lote: 20 questões QT601–QT900")
        chk("📚" in pg.locator("#qzHost").inner_text() or ev("!!QZ.block[0].ref"), f"{T} questão do lote traz referência")
        ev("QZ.div='r3'; QZ.tema=''; QZ.home()"); pg.wait_for_timeout(200)
        b = pg.locator("[data-st='lote']")
        chk(b.count() == 1 and "300 inéditas de 300" in b.inner_text(), f"{T} R3: botão {b.inner_text() if b.count() else '—'}")
        # tema claro
        ev("document.documentElement.classList.add('light'); location.hash='#foco'"); pg.wait_for_timeout(300)
        sw = ev("[document.documentElement.scrollWidth, innerWidth]")
        chk(sw[0] <= sw[1], f"{T} tema claro sem estouro ({sw})")
        chk(not errs, f"{T} sem erro de JS {errs[:2]}")
        ctx.close()
    br.close()
print(f"\n{len(ok)} ok · {len(bad)} falhas"); sys.exit(1 if bad else 0)
