"""t66 — 4.10.0: 🔊 Áudio em todo o app (voz do aparelho simulada).
Cards de estudo (frente/verso), questões (enunciado + alternativas, comentário), micropartículas, mnemônicos
(lista e treino), Honra (cards, mnemônicos, bússolas, painéis), Jornada, 🔊 do cabeçalho, tecla L, mini-player,
mãos livres, ajustes, parar ao trocar de aba, sem emoji na fala, sem estouro, sem erro de JS."""
import re
from playwright.sync_api import sync_playwright
URL = "http://localhost:8765/index.html"; ok = []; bad = []
def chk(c, m): (ok if c else bad).append(m); print(("✅ " if c else "❌ ") + m)
STUB = """
window.__spoken=[]; window.__cancel=0; window.__dur=25;
window.SpeechSynthesisUtterance = class { constructor(t){ this.text=t; this.rate=1; this.lang=''; this.voice=null; } };
const V=[{name:'Luciana',lang:'pt-BR',localService:true,default:true},{name:'Felipe',lang:'pt-BR',localService:true},{name:'Samantha',lang:'en-US',localService:true}];
const fake={speaking:false,paused:false,pending:false,onvoiceschanged:null,getVoices(){return V},
  speak(u){ window.__spoken.push({text:u.text,rate:u.rate,lang:u.lang,voice:u.voice&&u.voice.name}); this.speaking=true;
    setTimeout(()=>{ this.speaking=false; u.onend&&u.onend({}); }, window.__dur); },
  cancel(){ window.__cancel++; this.speaking=false; }, pause(){}, resume(){} };
Object.defineProperty(window,'speechSynthesis',{value:fake,configurable:true});
"""
EMO = re.compile("[\U0001F300-\U0001FAFF☀-➿️]")
def spoken(pg): return pg.evaluate("__spoken.filter(x=>x.text.trim()).map(x=>x.text).join(' ')")
def reset(pg): pg.evaluate("VOZ.stop(); __spoken=[]")
def wait_spoken(pg, ms=4000): pg.wait_for_function("__spoken.filter(x=>x.text.trim()).length>0", timeout=ms)
def wait_idle(pg, ms=15000): pg.wait_for_function("!VOZ.busy", timeout=ms)

with sync_playwright() as p:
    br = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
    for vp, lab in [({"width": 390, "height": 844}, "celular"), ({"width": 1366, "height": 900}, "desktop")]:
        ctx = br.new_context(viewport=vp); ctx.add_init_script(STUB); pg = ctx.new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(URL + "#inicio"); pg.wait_for_function("typeof VOZ!=='undefined' && S && S.cards && S.cards.length>1000", timeout=60000)
        chk(pg.evaluate("APP_VERSION") == "4.10.0", f"[{lab}] versão 4.10.0")
        chk(pg.is_visible("#vozBtn"), f"[{lab}] 🔊 no cabeçalho")
        w = pg.evaluate("document.documentElement.scrollWidth-document.documentElement.clientWidth"); chk(w <= 1, f"[{lab}] cabeçalho sem estouro ({w}px)")
        # 🔊 do cabeçalho na tela inicial
        pg.click("#vozBtn"); wait_spoken(pg)
        chk(pg.is_visible("#vozPlayer") and "Tela" in pg.inner_text("#vozPlayer"), f"[{lab}] mini-player aparece com o nome da tela")
        wait_idle(pg); t = spoken(pg); chk(len(t) > 40 and not EMO.search(t), f"[{lab}] lê a tela inicial sem emojis ({len(t)} car.)")
        chk(not pg.is_visible("#vozPlayer"), f"[{lab}] mini-player some ao terminar")
        # ---- Estudo ----
        reset(pg); pg.evaluate("location.hash='#estudar'"); pg.wait_for_function("Study.cur && $('#cardHost').shadowRoot", timeout=20000)
        chk(pg.is_visible("#bVoz"), f"[{lab}] 🔊 Ouvir na barra do card")
        qtxt = pg.evaluate("VOZ.studyText('q')"); atxt0 = pg.evaluate("$('#cardHost').shadowRoot.querySelector('.card').innerText")
        pg.click("#bVoz"); wait_spoken(pg); chk(pg.inner_text("#bVoz") == "⏹️", f"[{lab}] botão vira ⏹️ enquanto lê")
        wait_idle(pg); t = spoken(pg)
        chk(len(t) > 5 and "Resposta" not in t, f"[{lab}] lê só a frente antes de revelar")
        chk(pg.inner_text("#bVoz").startswith("🔊"), f"[{lab}] botão volta a 🔊")
        reset(pg); pg.click("#bShow"); pg.wait_for_timeout(300); pg.click("#bVoz"); wait_spoken(pg); wait_idle(pg); t = spoken(pg)
        fr = pg.evaluate("VOZ.clean(VOZ.studyText('q'))")
        chk(t.startswith("Resposta") and (fr[:40] not in t or len(fr) < 8), f"[{lab}] depois de revelar lê só a resposta")
        chk("📚" not in t and not EMO.search(t), f"[{lab}] resposta sem emojis")
        reset(pg); n_sync = pg.evaluate("(()=>{document.querySelector('#bVoz').click(); return __spoken.filter(x=>x.text.trim()).length})()")
        chk(n_sync >= 1 and pg.evaluate("VOZ._unl"), f"[{lab}] 1ª fala sai no próprio toque (exigência do iPhone) e destrava as próximas"); wait_idle(pg)
        # parar no meio
        reset(pg); pg.evaluate("__dur=400"); pg.click("#bVoz"); wait_spoken(pg); c0 = pg.evaluate("__cancel"); pg.click("#bVoz")
        chk(pg.evaluate("!VOZ.busy") and pg.evaluate("__cancel") > c0 and not pg.is_visible("#vozPlayer"), f"[{lab}] tocar de novo para a leitura")
        # tecla L
        reset(pg); pg.keyboard.press("l"); wait_spoken(pg); chk(pg.evaluate("VOZ.busy"), f"[{lab}] tecla L começa a ouvir"); pg.keyboard.press("l"); chk(pg.evaluate("!VOZ.busy"), f"[{lab}] tecla L para")
        # mini-player: velocidade e pausa
        reset(pg); pg.click("#bVoz"); wait_spoken(pg); pg.click("#vpR"); r = pg.evaluate("VOZ.rate"); chk(abs(r - 1.15) < 1e-6 and pg.evaluate("localStorage.getItem('vozRate')") == "1.15", f"[{lab}] velocidade 1× → 1,15× e fica salva")
        pg.click("#vpP"); chk(pg.evaluate("VOZ.paused") and "▶️" in pg.inner_text("#vpP"), f"[{lab}] ⏸️ pausa")
        n0 = pg.evaluate("__spoken.length"); pg.click("#vpP"); pg.wait_for_function(f"__spoken.length>{n0}", timeout=3000); chk(not pg.evaluate("VOZ.paused"), f"[{lab}] ▶️ continua de onde parou")
        chk(pg.evaluate("__spoken.at(-1).rate") == 1.15 and pg.evaluate("__spoken.at(-1).lang") == "pt-BR", f"[{lab}] fala em pt-BR na velocidade escolhida")
        chk(pg.evaluate("__spoken.at(-1).voice") == "Luciana", f"[{lab}] escolhe voz pt-BR (Luciana)")
        pg.click("#vpS"); pg.evaluate("__dur=25; localStorage.setItem('vozRate','1')")
        # trocar de aba para a leitura
        reset(pg); pg.evaluate("__dur=400"); pg.click("#bVoz"); wait_spoken(pg); pg.evaluate("location.hash='#inicio'"); pg.wait_for_timeout(300)
        chk(pg.evaluate("!VOZ.busy"), f"[{lab}] trocar de aba para a leitura"); pg.evaluate("__dur=25")
        # ---- Questões ----
        reset(pg); pg.evaluate("location.hash='#questoes'"); pg.wait_for_selector("#qzHost [data-st='10']", timeout=20000); pg.click("#qzHost [data-st='10']")
        pg.wait_for_selector("#qzHost .panel.qz > .vozBtn", timeout=5000); chk(True, f"[{lab}] 🔊 na questão")
        pg.click("#qzHost .panel.qz > .vozBtn"); wait_spoken(pg); wait_idle(pg); t = spoken(pg)
        chk(t.startswith("Questão") and "Alternativa A:" in t and "Alternativa D:" in t, f"[{lab}] lê enunciado e alternativas A–E")
        chk("Comentário" not in t and "Gabarito" not in t, f"[{lab}] não entrega o gabarito antes de responder")
        reset(pg); pg.locator("#qzHost .qzAlt").first.click(); pg.wait_for_selector("#qzCom > .vozBtn", timeout=5000)
        pg.click("#qzCom > .vozBtn"); wait_spoken(pg); wait_idle(pg); t = spoken(pg)
        chk(("Correto" in t or "Gabarito" in t) and "Comentário" in t, f"[{lab}] 🔊 do comentário lê resultado + comentário")
        # ---- Micropartículas ----
        reset(pg); pg.evaluate("location.hash='#micro'"); pg.wait_for_selector("#mcHost .mcTop .vozBtn", timeout=20000)
        tit = pg.inner_text("#mcHost .mcTit"); pg.click("#mcHost .mcTop .vozBtn"); wait_spoken(pg); wait_idle(pg); t = spoken(pg)
        chk(EMO.sub("", tit).strip()[:15] in t, f"[{lab}] micropartícula: lê título e texto")
        # ---- Mnemônicos ----
        reset(pg); pg.evaluate("location.hash='#mnemonicos'"); pg.wait_for_selector("#mnHost .mnCard .mnTools .vozBtn", timeout=20000)
        n = pg.evaluate("[...document.querySelectorAll('#mnHost .mnCard')].filter(c=>c.querySelector('.vozBtn')).length"); tot = pg.locator("#mnHost .mnCard").count()
        chk(n == tot and n > 0, f"[{lab}] 🔊 em todos os {tot} mnemônicos da lista")
        sig = pg.inner_text("#mnHost .mnCard .mnSig"); pg.locator("#mnHost .mnCard .vozBtn").first.click(); wait_spoken(pg); wait_idle(pg); t = spoken(pg)
        chk(sig.strip()[:4] in t and "Favoritar" not in t, f"[{lab}] lê título, sigla e itens (sem rótulos dos botões)")
        # mãos livres no treino
        reset(pg); pg.evaluate("localStorage.setItem('vozAuto','1')"); pg.click("#mnHost [data-mode='treino']"); wait_spoken(pg); wait_idle(pg); t = spoken(pg)
        chk("Qual é o mnemônico" in t and pg.evaluate("!document.querySelector('#mnHost .mnTrain .mnSig')"), f"[{lab}] mãos livres: treino lê só a pergunta")
        reset(pg); pg.click("#mnShow"); wait_spoken(pg); wait_idle(pg); t = spoken(pg)
        chk(len(t) > 10, f"[{lab}] mãos livres: lê a resposta ao revelar")
        # mãos livres no estudo
        reset(pg); pg.evaluate("location.hash='#estudar'"); wait_spoken(pg, 8000); wait_idle(pg); t = spoken(pg)
        if pg.evaluate("Study.shown"):
            chk(t.startswith("Resposta"), f"[{lab}] mãos livres: ao voltar a um card já revelado, lê a resposta")
            reset(pg); pg.click("#barAns [data-g='3']"); wait_spoken(pg, 8000); wait_idle(pg); t = spoken(pg)
        chk(len(t) > 5 and not t.startswith("Resposta"), f"[{lab}] mãos livres: card lê a frente ao aparecer")
        reset(pg); pg.click("#bShow"); wait_spoken(pg); wait_idle(pg); chk(spoken(pg).startswith("Resposta"), f"[{lab}] mãos livres: lê o verso ao revelar")
        reset(pg); pg.click("#barAns [data-g='3']"); wait_spoken(pg, 8000); wait_idle(pg); chk(not spoken(pg).startswith("Resposta"), f"[{lab}] mãos livres: próximo card lido sozinho")
        # mãos livres nas questões
        reset(pg); pg.evaluate("QZ.block=null; location.hash='#questoes'"); pg.wait_for_selector("#qzHost [data-st='10']", timeout=20000); pg.click("#qzHost [data-st='10']"); wait_spoken(pg); wait_idle(pg)
        chk(spoken(pg).startswith("Questão"), f"[{lab}] mãos livres: questão lida ao abrir")
        reset(pg); pg.locator("#qzHost .qzAlt").nth(1).click(); wait_spoken(pg); wait_idle(pg); chk("Comentário" in spoken(pg), f"[{lab}] mãos livres: comentário lido ao responder")
        pg.evaluate("localStorage.setItem('vozAuto','0')")
        # ---- Honra ----
        reset(pg); pg.evaluate("location.hash='#honra'"); pg.wait_for_selector(".hoSubs", timeout=20000)
        for sub, sel, lb in [("cards", "#hoHost .hoCard .vozBtn", "cards"), ("mn", "#hoHost .mnCard .vozBtn", "mnemônicos"), ("bussola", "#hoHost .hoComp .vozBtn", "bússolas")]:
            reset(pg); pg.evaluate(f"HO.go('{sub}')"); pg.wait_for_timeout(200)
            if sub == "bussola": pg.locator("#hoHost [data-bu]").first.click()
            try: pg.wait_for_selector(sel, timeout=5000); has = True
            except Exception: has = False
            if has: pg.locator(sel).first.click(); wait_spoken(pg); wait_idle(pg)
            chk(has and len(spoken(pg)) > 15, f"[{lab}] Honra › {lb}: 🔊 lê o conteúdo")
        reset(pg); pg.evaluate("HO.go('hoje')"); pg.wait_for_timeout(300); nb = pg.locator("#hoHost .hoPanel > .vozBtn").count(); chk(nb >= 1, f"[{lab}] Honra › Hoje: {nb} painel(is) com 🔊")
        # ---- Jornada ----
        reset(pg); pg.evaluate("location.hash='#jornada'"); pg.wait_for_timeout(1200); nb = pg.locator("#jrHost .panel > .vozBtn").count(); chk(nb >= 1, f"[{lab}] Jornada: {nb} painel(is) com 🔊")
        # trecho selecionado
        reset(pg); pg.evaluate("location.hash='#inicio'"); pg.wait_for_timeout(500)
        pg.evaluate("(()=>{const h=document.querySelector('#v-inicio h2')||document.querySelector('#v-inicio .panel');const r=document.createRange();r.selectNodeContents(h);const s=getSelection();s.removeAllRanges();s.addRange(r)})()")
        sel = pg.evaluate("String(getSelection()).trim()"); pg.click("#vozBtn"); wait_spoken(pg); wait_idle(pg)
        chk(pg.evaluate("VOZ.label") == "Trecho selecionado" and EMO.sub("", sel).strip()[:10] in spoken(pg), f"[{lab}] 🔊 do topo lê o trecho selecionado")
        pg.evaluate("getSelection().removeAllRanges()")
        # ---- Ajustes ----
        reset(pg); pg.evaluate("location.hash='#ajustes'"); pg.wait_for_selector("#vzVoice", timeout=5000)
        opts = pg.evaluate("[...document.querySelectorAll('#vzVoice option')].map(o=>o.value)"); chk(opts == ["Luciana", "Felipe"], f"[{lab}] lista só vozes em português ({opts})")
        pg.select_option("#vzVoice", "Felipe"); wait_spoken(pg); wait_idle(pg); chk(pg.evaluate("__spoken.at(-1).voice") == "Felipe", f"[{lab}] troca de voz vale na hora")
        pg.check("#vzAuto"); chk(pg.evaluate("localStorage.getItem('vozAuto')") == "1", f"[{lab}] mãos livres salvo"); pg.uncheck("#vzAuto")
        reset(pg); pg.click("#vzTest"); wait_spoken(pg); wait_idle(pg); chk("65 milímetros de mercúrio" in spoken(pg), f"[{lab}] testar voz")
        w = pg.evaluate("document.documentElement.scrollWidth-document.documentElement.clientWidth"); chk(w <= 1, f"[{lab}] Ajustes sem estouro ({w}px)")
        # tema claro
        pg.evaluate("localStorage.setItem('theme','light')"); pg.goto(URL + "#micro"); pg.reload(); pg.wait_for_selector("#mcHost .mcTop .vozBtn", timeout=30000)
        bg = pg.evaluate("getComputedStyle(document.querySelector('.vozBtn')).backgroundColor"); chk(bg in ("rgb(255, 252, 244)",), f"[{lab}] botão acompanha a versão clara ({bg})")
        pg.evaluate("localStorage.removeItem('theme')")
        chk(not errs, f"[{lab}] sem erros de JS" + (": " + "; ".join(errs[:3]) if errs else ""))
        ctx.close()
    # navegador sem voz
    ctx = br.new_context(viewport={"width": 390, "height": 844}); ctx.add_init_script("delete window.speechSynthesis; Object.defineProperty(window,'speechSynthesis',{get(){return undefined},configurable:true}); window.SpeechSynthesisUtterance=undefined;")
    pg = ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(URL + "#micro"); pg.wait_for_selector("#mcHost .mcCard", timeout=40000); pg.wait_for_timeout(400)
    chk(not pg.is_visible("#vozBtn") and pg.locator(".vozBtn").count() == 0, "[sem voz] botões escondidos quando o navegador não fala")
    pg.evaluate("location.hash='#ajustes'"); pg.wait_for_timeout(400); chk("não oferece leitura" in pg.inner_text("#vozSet"), "[sem voz] Ajustes explica")
    chk(not errs, "[sem voz] sem erros de JS" + (": " + "; ".join(errs[:3]) if errs else ""))
    br.close()
print(f"\n{len(ok)} ok · {len(bad)} falhas"); [print("  ❌", b) for b in bad]
