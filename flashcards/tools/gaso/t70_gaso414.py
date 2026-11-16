"""t70 — 4.14.0: baralhos 11–13 (VM × gaso, POCUS × gaso, venosa/gap CO₂/inotrópicos), etapas extras nos casos guiados,
analisador com VM e venosa, 45 questões novas e 📆 desafios semanais na Jornada. Uso: python3 t70_gaso414.py [URL]"""
import sys
from playwright.sync_api import sync_playwright
URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8765/index.html"; ok = []; bad = []
def chk(c, m): (ok if c else bad).append(m); print(("✅ " if c else "❌ ") + m)
ROOT = "🧪 Gasometria 360X"
with sync_playwright() as p:
    br = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
    for vp, lab in [({"width": 390, "height": 844}, "celular"), ({"width": 1366, "height": 900}, "desktop")]:
        ctx = br.new_context(viewport=vp); pg = ctx.new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(URL + "#inicio"); pg.wait_for_function("S && S.cards && S.cards.length>1000", timeout=90000)
        T = f"[{lab}]"
        chk(pg.evaluate("APP_VERSION") == "4.14.0", f"{T} versão 4.14.0")
        # ---------- baralhos novos ----------
        for num, nome, marca in [("11", "VM", "🫁 Ventilador"), ("12", "POCUS", "🔊 <b>POCUS:</b>"), ("13", "venosa", "🩸 Venosa")]:
            r = pg.evaluate(f"""(()=>{{const cs=S.official.filter(c=>c.deck.startsWith({ROOT!r}+"::{num} "));
               return [cs.length, cs.filter(c=>c.q.includes({marca!r})).length, cs.filter(c=>!/✅/.test(c.q.split('<hr id=answer>')[0])).length, new Set(cs.map(c=>c.id)).size]}})()""")
            chk(r[0] == 50 and r[3] == 50, f"{T} baralho {num} ({nome}): 50 cards, ids únicos ({r[0]}/{r[3]})")
            chk(r[1] >= 20, f"{T} baralho {num}: laudos com bloco '{marca[:12]}' na frente ({r[1]})")
            chk(r[2] == 50, f"{T} baralho {num}: frente sem spoiler ({r[2]})")
        tot = pg.evaluate(f"S.official.filter(c=>c.deck.startsWith({ROOT!r})).length"); chk(tot == 450, f"{T} coleção com 450 cards ({tot})")
        pg.evaluate("location.hash='#estudar'"); pg.wait_for_timeout(400)
        pg.evaluate(f"(async()=>{{const c=S.official.find(c=>c.deck.startsWith({ROOT!r}+'::13 ')&&c.q.includes('🩸 Venosa')); $('#studyEmpty').style.display='none'; $('#cardHost').style.display='block'; await renderInto($('#cardHost'), c.a, 'codice', c.deck)}})()")
        pg.wait_for_timeout(600)
        vt = pg.evaluate("$('#cardHost').shadowRoot.querySelector('.card').innerText")
        chk("Gap CO₂" in vt and "Conduta" in vt, f"{T} verso do caso venoso traz gap CO₂ no passo a passo e conduta")
        tw = pg.evaluate("(()=>{const r=$('#cardHost').shadowRoot,c=r.querySelector('.card');return [Math.max(...[...r.querySelectorAll('table')].map(t=>t.getBoundingClientRect().width)),c.getBoundingClientRect().width]})()")
        chk(tw[0] <= tw[1] + 1, f"{T} tabelas (arterial + venosa) cabem no card ({tw[0]:.0f}/{tw[1]:.0f}px)")
        # ---------- casos guiados com etapas novas ----------
        pg.evaluate("location.hash='#gaso'"); pg.wait_for_selector("#gzHost .gzHero")
        chk("328 casos guiados" in pg.inner_text("#gzHost .gzHero") and "450 flashcards" in pg.inner_text("#gzHost .gzHero"), f"{T} hero: 450 flashcards · 328 casos")
        info = pg.evaluate("""(()=>{const c=GZ.data.casos.find(c=>c.lab.vm&&c.lab.vm.alvo&&c.steps.some(s=>s.p.startsWith('⚙️ FR')));GZ.tema='';GZ.cur=c;GZ.si=0;GZ.picked=null;GZ.hits=0;GZ.render();
           const s=c.steps.find(s=>s.p.startsWith('⚙️ FR')), R=GASO_ENG.analyze(c.lab);return [c.n, s.o[s.c], Math.floor(R.x.frn+0.5), c.steps.length]})()""")
        chk(info[1] == f"{info[2]} irpm", f"{T} caso #{info[0]}: etapa '⚙️ FR para a PaCO₂ alvo' com resposta calculada ({info[1]})")
        chk(pg.evaluate("!!$('#gzHost .gzCase table') && $('#gzHost .gzCase').innerText.includes('Ventilador')"), f"{T} caso de VM mostra o bloco do ventilador")
        for k in range(info[3]):
            c = pg.evaluate("GZ.cur.steps[GZ.si].c"); pg.click(f"#gzHost [data-gzo='{c}']"); pg.wait_for_selector("#gzNext"); pg.click("#gzNext")
        pg.wait_for_selector("#gzHost .gzEnd"); chk("Caso perfeito" in pg.inner_text("#gzHost .gzEnd"), f"{T} caso de VM resolvido sem erro ({info[3]} etapas)")
        v = pg.evaluate("""(()=>{const c=GZ.data.casos.find(c=>c.lab.ven&&c.lab.ven.kind!=='periferica'&&c.steps.some(s=>s.p.startsWith('🩸 Gap')));GZ.cur=c;GZ.si=0;GZ.picked=null;GZ.hits=0;GZ.render();
           return [c.steps.map(s=>s.p), $('#gzHost .gzCase').innerText.includes('Venosa')]})()""")
        chk(any(p_.startswith("🩸 Gap") for p_ in v[0]) and any(("ScvO₂" in p_) or ("SvO₂" in p_) for p_ in v[0]) and v[1], f"{T} caso venoso com etapas de gap CO₂ e ScvO₂/SvO₂")
        chk(pg.evaluate("GZ.data.casos.filter(c=>c.steps.length>6).every(c=>c.steps.length<=9)") and pg.evaluate("GZ.data.casos.length") == 328, f"{T} 328 casos, no máximo 9 etapas")
        chk(pg.evaluate("GZ.data.casos.filter(c=>c.t>10).every(c=>c.steps.filter(s=>s.o.length<2||s.c<0||s.c>=s.o.length||new Set(s.o).size!==s.o.length).length===0)"), f"{T} etapas novas bem formadas (gabarito válido, opções únicas)")
        w = pg.evaluate("document.documentElement.scrollWidth-document.documentElement.clientWidth"); chk(w <= 1, f"{T} caso sem estouro horizontal ({w}px)")
        pg.evaluate("GZ.cur=null; GZ.render()")
        # ---------- analisador com VM e venosa ----------
        pg.click("#gzHost [data-gzsub=analisar]"); pg.wait_for_selector("#gzRun")
        pg.click("#gzHost .gzMore summary")
        for k_, v_ in [("pco2", "60"), ("hco3", "26"), ("na", "139"), ("cl", "104"), ("pao2", "70"), ("fio2", "50"), ("fr", "20"), ("vc", "400"), ("peep", "12"), ("pplat", "28"), ("etco2", "42"), ("alt", "170"), ("alvo", "45"), ("pvco2", "69"), ("scvo2", "62"), ("hb", "10"), ("sat", "92")]:
            pg.fill(f"#gzf_{k_}", v_)
        pg.click("#gzRun"); pg.wait_for_selector("#gzOut .gzDx")
        out = pg.inner_text("#gzOut")
        chk("FR para PaCO₂ alvo 45" in out and "= 27 irpm" in out, f"{T} analisador calcula a FR para a PaCO₂ alvo (27 irpm)")
        chk("Driving pressure" in out and "Gap PaCO₂ − EtCO₂" in out and "razão ventilatória" in out, f"{T} analisador: driving pressure, gap EtCO₂ e razão ventilatória")
        chk("Gap CO₂ (Pcv−aCO₂) = 69 − 60 = 9" in out and "ScvO₂ 62%" in out and "gap CO₂/Ca−vO₂" in out, f"{T} analisador: gap CO₂, ScvO₂ e razão gap/Ca−vO₂")
        chk("66" in pg.inner_text("#gzOut table") or "Peso predito" in out, f"{T} peso predito calculado pela altura")
        chk(pg.evaluate("$$('#gzHost .gzForm2 input').length") == 11 and pg.evaluate("$$('#gzHost .gzForm input').length") == 16, f"{T} 16 campos principais + 11 opcionais")
        pg.evaluate("GZ.render()"); chk(pg.evaluate("$('#gzf_alvo').value") == "45", f"{T} campos opcionais persistem")
        w = pg.evaluate("document.documentElement.scrollWidth-document.documentElement.clientWidth"); chk(w <= 1, f"{T} analisador sem estouro ({w}px)")
        # ---------- questões ----------
        pg.evaluate("location.hash='#questoes'"); pg.wait_for_selector("#qzHost [data-div]")
        q = pg.evaluate("(()=>{const g=QZ.data.gaso;return [g.length, g.slice(100).map(q=>q.id), [...new Set(g.slice(100).map(q=>q.tema))]]})()")
        chk(q[0] == 145 and q[1][0] == "QG101" and q[1][-1] == "QG145", f"{T} 145 questões (QG101–QG145 novas)")
        chk(len(q[2]) == 3, f"{T} 3 temas novos nas questões {q[2]}")
        pg.click("#qzHost [data-div=gaso]"); pg.wait_for_selector("#qzTema"); pg.select_option("#qzTema", "VM × gasometria")
        pg.click("#qzHost [data-st='10']"); pg.wait_for_selector("#qzHost .qzAlt"); pg.keyboard.press("B"); pg.wait_for_selector("#qzHost .qzRes")
        chk("VM × gasometria" in pg.inner_text("#qzHost"), f"{T} questão nova respondida pelo filtro de tema")
        pg.click("#qzQuit"); pg.wait_for_timeout(200)
        # ---------- 📆 desafios semanais ----------
        pg.evaluate("location.hash='#inicio'"); pg.wait_for_timeout(400)
        chk(pg.evaluate("!!$('#metaHome .wcMini')"), f"{T} faixa de desafios na tela inicial")
        pg.evaluate("location.hash='#jornada'"); pg.wait_for_selector("#wcPanel")
        chk(pg.evaluate("$$('#wcPanel .wc').length") == 3 and pg.evaluate("$$('#wcPanel [data-wcl]').length") == 3, f"{T} 3 desafios e 3 níveis")
        grp = pg.evaluate("WC.pick(WC.wk()).map(p=>p[1]).join(',')"); chk(grp == "0,1,2", f"{T} um desafio de cada grupo ({grp})")
        same = pg.evaluate("JSON.stringify(WC.pick(WC.wk()).map(p=>p[0]))===JSON.stringify(WC.pick(WC.wk()+3600e3).map(p=>p[0]))")
        nxt = pg.evaluate("[0,1,2,3,4,5].map(i=>WC.pick(WC.wk()+i*7*DAY).map(p=>p[0]).join('/')).filter((v,i,a)=>a.indexOf(v)===i).length")
        chk(same and nxt >= 3, f"{T} sorteio estável na semana e variado entre semanas ({nxt} combinações em 6 semanas)")
        a0 = pg.evaluate("WC.list().map(c=>c.alvo)"); pg.click("#wcPanel [data-wcl=hard]"); pg.wait_for_timeout(300)
        a1 = pg.evaluate("WC.list().map(c=>c.alvo)"); chk(all(y >= x for x, y in zip(a0, a1)) and a1 != a0, f"{T} nível 🔴 Hardcore aumenta os alvos {a0}→{a1}")
        chk(pg.evaluate("S.logs._wl && S.logs._wl.lvl==='hard'"), f"{T} nível salvo para sincronizar (S.logs._wl)")
        pg.click("#wcPanel [data-wcl=padrao]"); pg.wait_for_timeout(200)
        xp0 = pg.evaluate("xpTotal()")
        pg.evaluate("""(()=>{const wk=WC.wk();for(let i=0;i<7;i++){const d=dayKey(wk+i*DAY+12*3600e3);const L=S.logs[d]=S.logs[d]||{};
          Object.assign(L,{nAns:(L.nAns||0)+400,nOk:(L.nOk||0)+380,nRev:200,nNew:100,qN:100,qcN:50,gN:20,gP:10,mN:30,nN:40,hN:6});L.sims=(L.sims||[]).concat([{k:"q",deck:"x",ok:10,n:10,t:Date.now()},{k:"q",deck:"x",ok:10,n:10,t:Date.now()}]);L.xp=(L.xp||0)+300;}
          ACH.check()})()""")
        pg.wait_for_timeout(1200)
        st = pg.evaluate("(()=>{const D=(S.logs._wc||{})[WC.wk()]||{};return [Object.keys(D).filter(k=>k!=='all').length, !!D.all, WC.done()]})()")
        chk(st[0] == 3 and st[1], f"{T} os 3 desafios cumpridos e semana perfeita registrada ({st})")
        xs = pg.evaluate("Object.values(S.logs).filter(l=>l&&l.xs&&l.xs.d).reduce((a,l)=>a+l.xs.d,0)")
        chk(xs >= 3 * 60 + 100, f"{T} XP dos desafios na fonte 📆 ({xs})")
        pg.wait_for_timeout(800)
        got = pg.evaluate("Object.keys(S.logs._a||{})"); chk("wc1" in got and "wcp1" in got, f"{T} conquistas 'Primeiro Desafio' e 'Semana Perfeita'")
        chk(pg.evaluate("ACH.list.filter(a=>/^wcp?\\d/.test(a.id)).length") == 7, f"{T} 7 conquistas de desafio")
        chk(pg.evaluate("new Set(ACH.list.map(a=>a.id)).size===ACH.list.length") and pg.evaluate("ACH.list.length") >= 195, f"{T} conquistas com ids únicos ({pg.evaluate('ACH.list.length')})")
        pg.evaluate("JR.render()"); pg.wait_for_selector("#wcPanel")
        chk(pg.evaluate("$$('#wcPanel .wc.on').length") == 3, f"{T} painel mostra os 3 desafios cumpridos")
        again = pg.evaluate("WC.check()"); chk(again is False, f"{T} desafio cumprido não paga XP duas vezes")
        mg = pg.evaluate("mergeLogs({_wl:{lvl:'leve',t:1}},{_wl:{lvl:'hard',t:2}})._wl.lvl + mergeLogs({_wc:{'1':{cards:5}}},{_wc:{'1':{q:7},'2':{xp:9}}})._wc['1'].q")
        chk(mg == "hard7", f"{T} sincronização: nível mais recente vence e desafios se somam ({mg})")
        w = pg.evaluate("document.documentElement.scrollWidth-document.documentElement.clientWidth"); chk(w <= 1, f"{T} Jornada sem estouro ({w}px)")
        pg.evaluate("document.documentElement.classList.add('light')"); pg.evaluate("JR.render()"); pg.wait_for_selector("#wcPanel")
        bgL = pg.evaluate("getComputedStyle($('#wcPanel .wc')).backgroundImage + getComputedStyle($('#wcPanel .wc')).backgroundColor")
        chk("15, 21, 29" not in bgL, f"{T} tema claro aplica cores aos desafios")
        chk(not errs, f"{T} sem erro de JS {errs[:2]}")
        ctx.close()
    br.close()
print(f"\n{len(ok)} ok · {len(bad)} falhas"); sys.exit(1 if bad else 0)
