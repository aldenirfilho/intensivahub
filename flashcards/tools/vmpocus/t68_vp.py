"""t68 — 4.12.0: 🫁 Curvas de VM 360X (150) + 🔊 POCUS na UTI 360X (150) com imagem na frente + zoom genérico.
Coleções 'vmc' e 'pocus' no índice e no pack-6, 10+10 baralhos, 300 cards, 300 imagens carregam, imagem na frente e no verso,
diagnóstico só no verso, zoom abre/amplia/fecha, sem estouro (celular e desktop), sem erro de JS. Uso: python3 vp_t68.py [URL]"""
import sys
from playwright.sync_api import sync_playwright
URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8765/index.html"; ok = []; bad = []
def chk(c, m): (ok if c else bad).append(m); print(("✅ " if c else "❌ ") + m)
SETS = [("🫁 Curvas de VM 360X", "vm", "Curva VM #077", "vmc", 150, 10), ("🔊 POCUS na UTI 360X", "us", "POCUS #054", "pocus", 150, 10)]
with sync_playwright() as p:
    br = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
    for vp, lab in [({"width": 390, "height": 844}, "celular"), ({"width": 1366, "height": 900}, "desktop")]:
        ctx = br.new_context(viewport=vp); pg = ctx.new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(URL + "#inicio"); pg.wait_for_function("S && S.cards && S.cards.length>1000", timeout=90000)
        chk(pg.evaluate("APP_VERSION") >= "4.12.0", f"[{lab}] versão ≥ 4.12.0 ({pg.evaluate('APP_VERSION')})")
        for ROOT, cls, sample, cid, N, ND in SETS:
            T = f"[{lab}·{cid}]"
            n = pg.evaluate(f"S.official.filter(c=>c.deck.startsWith({ROOT!r})).length"); chk(n == N, f"{T} {N} cards carregados ({n})")
            nd = pg.evaluate(f"new Set(S.official.filter(c=>c.deck.startsWith({ROOT!r})).map(c=>c.deck)).size"); chk(nd == ND, f"{T} {ND} baralhos ({nd})")
            nids = pg.evaluate(f"new Set(S.official.filter(c=>c.deck.startsWith({ROOT!r})).map(c=>c.id)).size"); chk(nids == N, f"{T} ids únicos ({nids})")
            act = pg.evaluate(f"S.cards.filter(c=>c.deck.startsWith({ROOT!r})).length"); chk(act == N, f"{T} coleção ativa por padrão ({act})")
            res = pg.evaluate("""async(R)=>{const cs=S.official.filter(c=>c.deck.startsWith(R));let okc=0,front=0,noDx=0,clsok=0;const bad=[];
              for(const c of cs){const m=c.q.match(/data-m="([^"]+)"/); if(!m){bad.push('sem img '+c.id);continue}
                if(c.a.indexOf(m[0])<0||c.a.indexOf(m[0])>c.a.indexOf('<hr id=answer>')) bad.push('verso '+c.id);
                front++; if(!/✅/.test(c.q)) noDx++; if(/class="img fig (vm|us)"/.test(c.q)) clsok++;
                const u=await mediaURL(m[1]); const im=new Image(); await new Promise(r=>{im.onload=im.onerror=r; im.src=u});
                if(im.naturalWidth>1000) okc++; else bad.push('carga '+m[1]);}
              return {okc,front,noDx,clsok,bad:bad.slice(0,5),n:cs.length}}""", ROOT)
            chk(res["front"] == N, f"{T} imagem na FRENTE dos {N} cards ({res['front']})")
            chk(res["okc"] == N, f"{T} {N} imagens carregam (naturalWidth>1000) ({res['okc']}) {res['bad']}")
            chk(res["noDx"] == N, f"{T} frente não revela o diagnóstico ({res['noDx']})")
            chk(res["clsok"] == N, f"{T} classe genérica 'img fig {cls}' com legenda/alt próprios ({res['clsok']})")
            pg.evaluate("location.hash='#estudar'"); pg.wait_for_timeout(600)
            pg.evaluate(f"(async()=>{{const c=S.official.find(c=>c.deck.startsWith({ROOT!r})&&c.q.includes({sample!r})); $('#studyEmpty').style.display='none'; $('#cardHost').style.display='block'; await renderInto($('#cardHost'), c.q, 'codice', c.deck); window.__c=c}})()")
            pg.wait_for_function("(()=>{const r=$('#cardHost').shadowRoot; const i=r&&r.querySelector('.img.fig img'); return i&&i.complete&&i.naturalWidth>0})()", timeout=15000)
            chk(True, f"{T} card renderiza com a imagem no estudo")
            alt = pg.evaluate("$('#cardHost').shadowRoot.querySelector('.img.fig img').alt")
            chk(("ventilador" in alt) if cls == "vm" else ("POCUS" in alt), f"{T} texto alternativo adequado ({alt})")
            iw = pg.evaluate("(()=>{const r=$('#cardHost').shadowRoot,i=r.querySelector('.img.fig img'),c=r.querySelector('.card');return [i.getBoundingClientRect().width,c.getBoundingClientRect().width]})()")
            chk(iw[0] <= iw[1] + 1 and iw[0] > iw[1] * 0.8, f"{T} imagem ocupa a largura do card sem estourar ({iw[0]:.0f}/{iw[1]:.0f}px)")
            w = pg.evaluate("document.documentElement.scrollWidth-document.documentElement.clientWidth"); chk(w <= 1, f"{T} página sem estouro horizontal ({w}px)")
            pg.evaluate("$('#cardHost').shadowRoot.querySelector('.img.fig img').click()")
            chk(pg.is_visible("#zoomBox") and pg.evaluate("$('#zoomBox').classList.contains('fit')"), f"{T} 🔍 toque abre o zoom (modo ajustar)")
            z0 = pg.evaluate("$('#zoomBox img').getBoundingClientRect().width")
            pg.click("#zoomBox [data-z='+']"); pg.click("#zoomBox [data-z='+']")
            z2 = pg.evaluate("$('#zoomBox img').getBoundingClientRect().width")
            chk(z2 > z0 * 1.8, f"{T} ➕ amplia ({z0:.0f}→{z2:.0f}px)")
            pg.keyboard.press("Escape"); chk(not pg.is_visible("#zoomBox"), f"{T} Esc fecha o zoom")
            pg.evaluate("(async()=>{await renderInto($('#cardHost'), __c.a, 'codice', __c.deck)})()"); pg.wait_for_timeout(500)
            vt = pg.evaluate("$('#cardHost').shadowRoot.querySelector('.card').innerText")
            chk("✅" in vt and "Conduta" in vt and "sintética" in vt and "Pegadinha" in vt, f"{T} verso: diagnóstico + conduta + pegadinha + aviso de imagem sintética")
            chk(pg.evaluate("!!$('#cardHost').shadowRoot.querySelector('.img.fig img') && $('#cardHost').shadowRoot.querySelector('.img.fig img').naturalWidth>0"), f"{T} imagem também no verso")
        # ECG continua com a classe própria
        e = pg.evaluate("S.official.filter(c=>c.deck.startsWith('📈')).every(c=>/class=\"img ecg\"/.test(c.q))")
        chk(e, f"[{lab}] 📈 cards de ECG mantêm a classe 'img ecg'")
        cols = pg.evaluate("fetch('data/index.json').then(r=>r.json()).then(j=>[j.colecoes.find(c=>c.id==='vmc'), j.colecoes.find(c=>c.id==='pocus'), j.pacotes.find(p=>p.nome==='pack-6-vmpocus')])")
        chk(cols[0] and cols[0]["cards"] == 150 and cols[1] and cols[1]["cards"] == 150 and cols[2] and cols[2]["cards"] == 300, f"[{lab}] índice: coleções 🫁/🔊 e pack-6 com 300 cards")
        chk(not errs, f"[{lab}] sem erro de JS {errs[:2]}")
        ctx.close()
    br.close()
print(f"\n{len(ok)} ✅ · {len(bad)} ❌"); sys.exit(1 if bad else 0)
