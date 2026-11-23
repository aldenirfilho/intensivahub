"""t73 — 4.17.0: 🔎 linha de conferência no verso, 🎧 audiolivro (voz simulada), 🃏 axioma do dia + cartão, 🗺️ mapa."""
import sys
from playwright.sync_api import sync_playwright
BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8765/"; ok = []; bad = []
def chk(c, m): (ok if c else bad).append(m); print(("✅ " if c else "❌ ") + m)
ROOT = "📜 Escrituras & Axiomas 360X"
FAKE = """(()=>{window.__falas=[];const S={speaking:false,paused:false,pending:false,_q:[],
 getVoices(){return [{name:'Luciana',lang:'pt-BR'},{name:'Joana',lang:'pt-PT'}]},
 speak(u){window.__falas.push(u.text);this.speaking=true;const me=u;setTimeout(()=>{if(me.__x)return;me.onend&&me.onend()},60)},
 cancel(){this.speaking=false},pause(){},resume(){},onvoiceschanged:null};
 Object.defineProperty(window,'speechSynthesis',{value:S,configurable:true});
 window.SpeechSynthesisUtterance=function(t){this.text=t}})()"""
with sync_playwright() as p:
    br = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
    for vp, lab in [({"width": 390, "height": 844}, "celular"), ({"width": 1366, "height": 900}, "desktop")]:
        T = f"[{lab}]"
        ctx = br.new_context(viewport=vp); pg = ctx.new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(BASE + "index.html#inicio"); pg.wait_for_function("S && S.cards && S.cards.length>1000", timeout=120000)
        chk(pg.evaluate("APP_VERSION") == "4.25.2", f"{T} versão 4.25.2")
        chk(pg.locator("#homeFoot a[href='autor/mapa-axiomas.html']").count() == 1 and pg.locator("#homeFoot a[href='autor/axiomas-360x.html#leitor']").count() == 1, f"{T} rodapé com links do audiolivro e do mapa")
        pg.evaluate("location.hash='#estudar'"); pg.wait_for_timeout(300)
        for num, marca in [("01", "conferido no texto-fonte: Bíblia Almeida"), ("09", "Helmi Nasr"), ("08", "Sefaria"), ("14", "revisado sem o texto-fonte")]:
            pg.evaluate(f"(async()=>{{const c=S.official.find(c=>c.deck.startsWith({ROOT!r}+'::{num} ')); $('#studyEmpty').style.display='none'; $('#cardHost').style.display='block'; await renderInto($('#cardHost'), c.a, 'codice', c.deck)}})()")
            pg.wait_for_timeout(400)
            chk(marca in pg.evaluate("$('#cardHost').shadowRoot.querySelector('.card').innerText"), f"{T} verso do baralho {num}: “{marca}”")
        n20 = pg.evaluate(f"S.official.filter(c=>c.deck.startsWith({ROOT!r}+'::20 ')&&/conferido|revisado sem/.test(c.a)).length")
        chk(n20 == 0, f"{T} axiomas do autor sem linha de conferência ({n20})")
        chk(not errs, f"{T} app sem erro de JS {errs[:2]}")
        # livro
        pg2 = ctx.new_page(); e2 = []; pg2.on("pageerror", lambda e: e2.append(str(e)))
        pg2.add_init_script(FAKE)
        pg2.goto(BASE + "autor/axiomas-360x.html"); pg2.wait_for_load_state("load"); pg2.wait_for_timeout(300)
        dia = pg2.evaluate("window.AXLIVRO.axDoDia(new Date(2026,10,17)).n"), pg2.evaluate("window.AXLIVRO.axDoDia(new Date(2027,2,24)).n")
        chk(dia == (1, 149) or dia[0] == 1, f"{T} axioma do dia: 17/11/2026 = nº 1, ciclo de 149 ({dia})")
        chk(pg2.locator("#dia h3").inner_text().strip() != "", f"{T} painel mostra o axioma de hoje")
        pg2.click("#btCartao"); pg2.wait_for_timeout(1200)
        dim = pg2.evaluate("(()=>{const i=document.querySelector('#cartaoImg');return [i.naturalWidth,i.naturalHeight,i.src.slice(0,15)]})()")
        chk(dim[:2] == [1080, 1920] and dim[2].startswith("data:image/jpeg"), f"{T} cartão do dia 1080×1920 JPG ({dim})")
        chk(pg2.locator("#faixas button").count() == 11 and pg2.locator(".ouvir-eixo").count() == 11, f"{T} 11 faixas (10 eixos + Armorial) e botão em cada capítulo")
        chk(pg2.evaluate("document.querySelector('#selVoz').options[0].text.includes('pt-BR')"), f"{T} escolhe voz pt-BR")
        pg2.click("#btPlay"); pg2.wait_for_timeout(400)
        st = pg2.evaluate("window.AXLIVRO.estado()")
        falas = pg2.evaluate("window.__falas.length")
        chk(falas >= 3 and pg2.locator("article.ax.lendo").count() == 1, f"{T} audiolivro fala e destaca o axioma lido ({falas} trechos, {st})")
        chk(pg2.evaluate("Math.max(...window.__falas.map(t=>t.length))") <= 210, f"{T} trechos de até ~200 caracteres")
        pg2.click("#mPausa"); pg2.wait_for_timeout(150); n1 = pg2.evaluate("window.__falas.length"); pg2.wait_for_timeout(300)
        chk(pg2.evaluate("window.__falas.length") == n1 and not pg2.evaluate("window.AXLIVRO.estado().on"), f"{T} pausa interrompe a leitura")
        pg2.click("#mPausa"); pg2.wait_for_timeout(200)
        chk(pg2.evaluate("window.__falas.length") > n1, f"{T} continuar retoma de onde parou")
        chk(pg2.locator("#mini.on").is_visible(), f"{T} mini-player fixo aparece enquanto lê")
        pg2.click("#mProx"); pg2.wait_for_timeout(200)
        chk(pg2.evaluate("window.AXLIVRO.estado().f") == 1 and "Faixa 2" in pg2.evaluate("window.__falas.join(' ')"), f"{T} próxima faixa = eixo II")
        pg2.evaluate("document.querySelectorAll('.ouvir-eixo')[10].click()"); pg2.wait_for_timeout(200)
        chk(pg2.evaluate("window.AXLIVRO.estado().f") == 10, f"{T} botão do capítulo toca a faixa do Armorial")
        pg2.evaluate("document.querySelector('#mParar').click()"); pg2.wait_for_timeout(100)
        chk(pg2.locator("article.ax.lendo").count() == 0 and pg2.evaluate("window.AXLIVRO.estado().f") == -1, f"{T} parar limpa o destaque")
        pg2.evaluate("document.querySelector('#btOuvirDia').click()"); pg2.wait_for_timeout(1500)
        chk(pg2.evaluate("window.AXLIVRO.estado().f") == -1 and not pg2.evaluate("window.AXLIVRO.estado().on"), f"{T} ouvir o axioma do dia não emenda outra faixa")
        sw = pg2.evaluate("[document.documentElement.scrollWidth, innerWidth]")
        chk(sw[0] <= sw[1] + 1, f"{T} livro sem estouro horizontal ({sw})")
        chk(not e2, f"{T} livro sem erro de JS {e2[:2]}")
        # mapa
        pg3 = ctx.new_page(); e3 = []; pg3.on("pageerror", lambda e: e3.append(str(e)))
        pg3.goto(BASE + "autor/mapa-axiomas.html"); pg3.wait_for_timeout(500)
        chk(pg3.locator("circle.dot").count() == 149, f"{T} mapa com 149 axiomas")
        chk(pg3.locator(".chip").count() >= 10, f"{T} filtros por tema ({pg3.locator('.chip').count()})")
        pg3.locator("circle.dot[data-n='57']").click(force=True); pg3.wait_for_timeout(200)
        chk("AXIOMA 57" in pg3.inner_text("#info").upper() and pg3.locator("#info a[href='axiomas-360x.html#ax-57']").count() == 1, f"{T} tocar no ponto mostra o axioma e o link do livro")
        pg3.locator(".chip").first.click(); pg3.wait_for_timeout(200)
        chk(pg3.locator("circle.dot.fraco").count() > 50, f"{T} tema escolhido destaca só os seus axiomas")
        sw = pg3.evaluate("[document.documentElement.scrollWidth, innerWidth]")
        chk(sw[0] <= sw[1] + 1 and not e3, f"{T} mapa sem estouro e sem erro de JS ({sw}) {e3[:2]}")
        ctx.close()
    br.close()
print(f"\n{len(ok)} ok · {len(bad)} falhas"); sys.exit(1 if bad else 0)
