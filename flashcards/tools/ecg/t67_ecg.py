"""t67 — 4.11.0: 📈 Compêndio de ECG 360X (300 cards com traçado na frente) + 🔍 zoom de imagens.
Coleção 'ecg' no índice e no pack-5, 18 baralhos, 300 cards, 300 imagens carregam, traçado na frente e no verso,
diagnóstico só no verso, zoom abre/amplia/fecha, sem estouro (celular e desktop), sem erro de JS. Uso: python3 ecg_t67.py [URL]"""
import sys
from playwright.sync_api import sync_playwright
URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8765/index.html"; ok = []; bad = []
def chk(c, m): (ok if c else bad).append(m); print(("✅ " if c else "❌ ") + m)
ROOT = "📈 Compêndio de ECG 360X"
with sync_playwright() as p:
    br = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
    for vp, lab in [({"width": 390, "height": 844}, "celular"), ({"width": 1366, "height": 900}, "desktop")]:
        ctx = br.new_context(viewport=vp); pg = ctx.new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(URL + "#inicio"); pg.wait_for_function("S && S.cards && S.cards.length>1000", timeout=90000)
        chk(pg.evaluate("APP_VERSION") == "4.11.0", f"[{lab}] versão 4.11.0")
        n = pg.evaluate(f"S.official.filter(c=>c.deck.startsWith({ROOT!r})).length")
        chk(n == 300, f"[{lab}] 300 cards do Compêndio de ECG carregados ({n})")
        nd = pg.evaluate(f"new Set(S.official.filter(c=>c.deck.startsWith({ROOT!r})).map(c=>c.deck)).size")
        chk(nd == 18, f"[{lab}] 18 baralhos de ECG ({nd})")
        nids = pg.evaluate(f"new Set(S.official.filter(c=>c.deck.startsWith({ROOT!r})).map(c=>c.id)).size")
        chk(nids == 300, f"[{lab}] ids únicos ({nids})")
        act = pg.evaluate(f"S.cards.filter(c=>c.deck.startsWith({ROOT!r})).length")
        chk(act == 300, f"[{lab}] coleção ativa por padrão ({act} cards no estudo)")
        # todas as imagens carregam
        res = pg.evaluate("""async()=>{const cs=S.official.filter(c=>c.deck.startsWith('📈'));let okc=0,front=0,noDx=0;const bad=[];
          for(const c of cs){const m=c.q.match(/data-m="([^"]+)"/); if(!m){bad.push('sem img '+c.id);continue}
            if(c.a.indexOf(m[0])<0||c.a.indexOf(m[0])>c.a.indexOf('<hr id=answer>')) bad.push('verso '+c.id);
            front++; if(!/✅/.test(c.q)) noDx++;
            const u=await mediaURL(m[1]); const im=new Image(); await new Promise(r=>{im.onload=im.onerror=r; im.src=u});
            if(im.naturalWidth>1000) okc++; else bad.push('carga '+m[1]);}
          return {okc,front,noDx,bad:bad.slice(0,5),n:cs.length}}""")
        chk(res["front"] == 300, f"[{lab}] traçado na FRENTE dos 300 cards ({res['front']})")
        chk(res["okc"] == 300, f"[{lab}] 300 imagens carregam (naturalWidth>1000) ({res['okc']}) {res['bad']}")
        chk(res["noDx"] == 300, f"[{lab}] frente não revela o diagnóstico ({res['noDx']})")
        # estudar um card de ECG
        pg.evaluate("location.hash='#estudar'"); pg.wait_for_timeout(800)
        pg.evaluate(f"(async()=>{{const c=S.official.find(c=>c.deck.startsWith({ROOT!r})&&c.q.includes('ECG #170')); $('#studyEmpty').style.display='none'; $('#cardHost').style.display='block'; await renderInto($('#cardHost'), c.q, 'codice', c.deck); window.__c=c}})()")
        pg.wait_for_function("(()=>{const r=$('#cardHost').shadowRoot; const i=r&&r.querySelector('.img.ecg img'); return i&&i.complete&&i.naturalWidth>0})()", timeout=15000)
        chk(True, f"[{lab}] card de ECG renderiza com o traçado no estudo")
        iw = pg.evaluate("(()=>{const r=$('#cardHost').shadowRoot,i=r.querySelector('.img.ecg img'),c=r.querySelector('.card');return [i.getBoundingClientRect().width,c.getBoundingClientRect().width]})()")
        chk(iw[0] <= iw[1] + 1 and iw[0] > iw[1] * 0.8, f"[{lab}] traçado ocupa a largura do card sem estourar ({iw[0]:.0f}/{iw[1]:.0f}px)")
        w = pg.evaluate("document.documentElement.scrollWidth-document.documentElement.clientWidth"); chk(w <= 1, f"[{lab}] página sem estouro horizontal ({w}px)")
        # zoom
        pg.evaluate("$('#cardHost').shadowRoot.querySelector('.img.ecg img').click()")
        chk(pg.is_visible("#zoomBox") and pg.evaluate("$('#zoomBox').classList.contains('fit')"), f"[{lab}] 🔍 toque abre o zoom (modo ajustar)")
        z0 = pg.evaluate("$('#zoomBox img').getBoundingClientRect().width")
        pg.click("#zoomBox [data-z='+']"); pg.click("#zoomBox [data-z='+']")
        z2 = pg.evaluate("$('#zoomBox img').getBoundingClientRect().width"); sc = pg.evaluate("(()=>{const s=$('#zoomBox .zscroll');return s.scrollWidth>s.clientWidth})()")
        chk(z2 > z0 * 1.8 and sc, f"[{lab}] ➕ amplia e permite rolar ({z0:.0f}→{z2:.0f}px)")
        chk(pg.inner_text("#zLv").strip() == "2.5×", f"[{lab}] indicador de nível (2.5×)")
        pg.click("#zoomBox [data-z='fit']"); chk(pg.evaluate("$('#zoomBox').classList.contains('fit')"), f"[{lab}] ↔️ volta a ajustar")
        pg.keyboard.press("Escape"); chk(not pg.is_visible("#zoomBox"), f"[{lab}] Esc fecha o zoom")
        pg.evaluate("$('#cardHost').shadowRoot.querySelector('.img.ecg img').click()"); pg.click("#zoomBox [data-z='x']")
        chk(not pg.is_visible("#zoomBox"), f"[{lab}] ✖ fecha o zoom")
        chk(not pg.evaluate("document.documentElement.classList.contains('zoomOpen')"), f"[{lab}] rolagem da página liberada ao fechar")
        # verso
        pg.evaluate("(async()=>{await renderInto($('#cardHost'), __c.a, 'codice', __c.deck)})()"); pg.wait_for_timeout(500)
        vt = pg.evaluate("$('#cardHost').shadowRoot.querySelector('.card').innerText")
        chk("✅" in vt and "Conduta" in vt and "sintético" in vt, f"[{lab}] verso: diagnóstico + conduta + aviso de traçado sintético")
        chk(pg.evaluate("!!$('#cardHost').shadowRoot.querySelector('.img.ecg img') && $('#cardHost').shadowRoot.querySelector('.img.ecg img').naturalWidth>0"), f"[{lab}] traçado também no verso")
        # imagens antigas (verso) continuam e também ganham zoom
        has_old = pg.evaluate("(async()=>{const c=S.official.find(c=>/data-m=/.test(c.a)&&!c.deck.startsWith('📈')); if(!c) return 'none'; await renderInto($('#cardHost'), c.a, 'codice', c.deck); const i=$('#cardHost').shadowRoot.querySelector('.img img'); if(!i) return 'noimg'; await new Promise(r=>{if(i.complete) r(); else {i.onload=i.onerror=r}}); i.click(); return $('#zoomBox').classList.contains('on')?'ok':'nozoom'})()")
        chk(has_old in ("ok", "none"), f"[{lab}] imagens dos outros cards também abrem no zoom ({has_old})")
        pg.keyboard.press("Escape")
        # coleção no ajuste
        cols = pg.evaluate("fetch('data/index.json').then(r=>r.json()).then(j=>[j.colecoes.find(c=>c.id==='ecg'), j.pacotes.find(p=>p.nome==='pack-5-ecg')])")
        chk(cols[0] and cols[0]["cards"] == 300 and cols[1] and cols[1]["cards"] == 300, f"[{lab}] índice: coleção 📈 e pack-5 com 300 cards")
        chk(not errs, f"[{lab}] sem erro de JS {errs[:2]}")
        ctx.close()
    br.close()
print(f"\n{len(ok)} ✅ · {len(bad)} ❌"); sys.exit(1 if bad else 0)
