#!/usr/bin/env python3
"""🗺️ Mapa dos 10 eixos + Armorial com os 138 Axiomas 360X (página interativa + PNG + PDF).
Anel de eixos; cada axioma é um ponto colorido pelo tema; as curvas douradas ligam os axiomas
que os comentários citam entre si; escolher um tema liga todos os axiomas daquele tema."""
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build import TEMAS  # noqa: E402
from make_book import AUTOR, EIXOS, OUT, carregar, font_face  # noqa: E402


def ligacoes(ax):
    pares = set()
    for a in ax:
        for m in re.finditer(r"axiomas? ((?:\d+(?:\s*(?:,|e|a|–|-)\s*)?)+)", a["com"]):
            seq = m.group(1)
            nums = [int(x) for x in re.findall(r"\d+", seq)]
            if re.search(r"\d+\s*(?:a|–|-)\s*\d+", seq) and len(nums) == 2 and nums[1] - nums[0] <= 8:
                nums = list(range(nums[0], nums[1] + 1))
            for x in nums:
                if 1 <= x <= 138 and x != a["n"]:
                    pares.add(tuple(sorted((a["n"], x))))
    return sorted(pares)


def pagina(ax):
    dados = [dict(n=a["n"], t=a["tit"], e=a["eixo"], m=a["tema"], x=a["enun"]) for a in sorted(ax, key=lambda a: a["n"])]
    eix = [dict(k=k, r=r, t=t) for k, r, t, _ in EIXOS]
    tem = {k: dict(emo=v[0], nome=v[1], cor=v[2]) for k, v in TEMAS.items() if any(a["tema"] == k for a in ax)}
    return f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Mapa dos Axiomas 360X — eixos e temas · {AUTOR}</title>
<style>{font_face()}
body{{margin:0;background:#070a10;color:#efe6cf;font-family:-apple-system,'Segoe UI',Roboto,sans-serif}}
.topo{{display:flex;justify-content:space-between;align-items:center;gap:8px;padding:9px 14px;border-bottom:1px solid #3b3220;background:#0b0f16;position:sticky;top:0;z-index:3;font-size:13px}}
.topo a{{color:#d4af37;text-decoration:none}}.topo b{{font-family:'LoraLivro',Georgia,serif;color:#d4af37;font-size:15px}}
.wrap{{display:grid;grid-template-columns:minmax(0,1fr) 320px;gap:14px;padding:12px;max-width:1500px;margin:auto}}
@media(max-width:900px){{.wrap{{grid-template-columns:1fr}}}}
svg{{width:100%;height:auto;display:block;background:radial-gradient(circle at 50% 50%,#121a26,#070a10 70%);border:1px solid #2c3a4f;border-radius:14px}}
.lado{{border:1px solid #2c3a4f;border-radius:14px;padding:12px;background:#0b111a;font-size:13.5px}}
.lado h2{{font-family:'LoraLivro',Georgia,serif;color:#d4af37;font-size:17px;margin:4px 0 8px}}
.chips{{display:flex;flex-wrap:wrap;gap:6px}}.chip{{border:1px solid #3b4a62;border-radius:999px;padding:4px 9px;cursor:pointer;background:#111a28;color:#e5dcc3;font-size:12.5px}}
.chip.on{{border-color:#d4af37;box-shadow:0 0 0 1px #d4af37 inset}}
#info{{margin-top:12px;border-top:1px solid #2c3a4f;padding-top:10px;min-height:120px}}
#info .n{{color:#22b8d6;font-size:11px;letter-spacing:2px;text-transform:uppercase}}#info h3{{font-family:'LoraLivro',Georgia,serif;color:#d4af37;margin:4px 0}}
#info blockquote{{font-family:'LoraLivro',Georgia,serif;font-style:italic;margin:6px 0;color:#f3ead2;line-height:1.45}}
#info a{{color:#22b8d6}}
.dot{{cursor:pointer;transition:opacity .2s}}.fraco{{opacity:.12}}
.eixo-lbl{{font-family:'LoraLivro',Georgia,serif;fill:#d4af37;font-size:15px}}
.leg{{color:#9fb3c8;font-size:12px;margin-top:10px;line-height:1.5}}
</style></head><body>
<div class="topo"><b>🗺️ Mapa dos Axiomas 360X</b><span><a href="axiomas-360x.html">📖 Livro</a> · <a href="../index.html#inicio">← Códice 360X</a></span></div>
<div class="wrap"><div><svg id="mapa" viewBox="0 0 1200 1200" role="img" aria-label="Mapa radial: 11 eixos e 138 axiomas"></svg></div>
<div class="lado"><h2>Temas</h2><div class="chips" id="chips"></div>
<div class="leg">● ponto = axioma (cor do tema) · arco interno = eixo · <span style="color:#d4af37">curva dourada</span> = um comentário cita o outro axioma · escolha um tema para ligar todos os axiomas dele.</div>
<div id="info"><div class="n">toque num ponto</div><h3>Axiomas 360X</h3><blockquote>138 axiomas em 10 eixos e o Armorial.</blockquote><div>{AUTOR}</div></div></div></div>
<script>const AX={json.dumps(dados, ensure_ascii=False)};const EIX={json.dumps(eix, ensure_ascii=False)};const TEM={json.dumps(tem, ensure_ascii=False)};const LIG={json.dumps(ligacoes(ax))};
{JS}</script></body></html>"""


JS = r"""
(function(){
const NS='http://www.w3.org/2000/svg',svg=document.getElementById('mapa'),C=600,R1=250,R2=455;
const el=(t,a,p)=>{const e=document.createElementNS(NS,t);for(const k in a)e.setAttribute(k,a[k]);(p||svg).appendChild(e);return e};
const esc=s=>s.replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const total=AX.length,gap=0.035,pos={};let ang=-Math.PI/2;
const span=(2*Math.PI-gap*EIX.length)/total;
const gEix=el('g',{}),gLig=el('g',{}),gTema=el('g',{}),gDot=el('g',{});
el('circle',{cx:C,cy:C,r:R1-70,fill:'none',stroke:'rgba(212,175,55,.25)','stroke-width':1});
el('text',{x:C,y:C-14,'text-anchor':'middle',fill:'#d4af37','font-size':34,'font-family':'LoraLivro,Georgia,serif'}).textContent='⚜ AXIOMAS 360X';
el('text',{x:C,y:C+22,'text-anchor':'middle',fill:'#22b8d6','font-size':15}).textContent='10 eixos · Armorial · 138 axiomas';
el('text',{x:C,y:C+48,'text-anchor':'middle',fill:'#b9ab86','font-size':13}).textContent='Aldenir Rocha de Oliveira Filho';
EIX.forEach((E,i)=>{const lista=AX.filter(a=>a.e===E.k);const a0=ang,a1=ang+span*lista.length;
  const arc=(r)=>`M ${C+r*Math.cos(a0)} ${C+r*Math.sin(a0)} A ${r} ${r} 0 ${a1-a0>Math.PI?1:0} 1 ${C+r*Math.cos(a1)} ${C+r*Math.sin(a1)}`;
  el('path',{d:arc(R1),fill:'none',stroke:i%2?'#22b8d6':'#d4af37','stroke-width':10,'stroke-linecap':'round',opacity:.8},gEix);
  const am=(a0+a1)/2,lx=C+(R1-38)*Math.cos(am),ly=C+(R1-38)*Math.sin(am);
  const t=el('text',{x:lx,y:ly+5,'text-anchor':'middle',class:'eixo-lbl'},gEix);t.textContent=E.r;
  const tt=el('title',{},t);tt.textContent=E.t+' · '+lista.length+' axiomas';
  lista.forEach((a,j)=>{const th=a0+span*(j+.5);const rr=R2+(j%2?18:-18);pos[a.n]={x:C+rr*Math.cos(th),y:C+rr*Math.sin(th),th};
    el('line',{x1:C+(R1+8)*Math.cos(th),y1:C+(R1+8)*Math.sin(th),x2:pos[a.n].x,y2:pos[a.n].y,stroke:'rgba(159,179,200,.14)'},gEix)});
  ang=a1+gap});
const curva=(p,q)=>{const mx=(p.x+q.x)/2,my=(p.y+q.y)/2;const k=.35;return `M ${p.x} ${p.y} Q ${C+(mx-C)*k} ${C+(my-C)*k} ${q.x} ${q.y}`};
LIG.forEach(([a,b])=>el('path',{d:curva(pos[a],pos[b]),fill:'none',stroke:'rgba(212,175,55,.55)','stroke-width':1.6,'data-a':a,'data-b':b},gLig));
const dots={};
AX.forEach(a=>{const T=TEM[a.m],p=pos[a.n];const d=el('circle',{cx:p.x,cy:p.y,r:11,fill:T.cor,stroke:'#070a10','stroke-width':2,class:'dot','data-n':a.n,'data-m':a.m},gDot);
  const tx=el('text',{x:p.x+(Math.cos(p.th)>0?15:-15),y:p.y+4,'text-anchor':Math.cos(p.th)>0?'start':'end',fill:'#9fb3c8','font-size':11,class:'dot','data-n':a.n},gDot);tx.textContent=a.n;
  const ti=el('title',{},d);ti.textContent=`${a.n} · ${a.t}`;dots[a.n]=[d,tx];
  const ver=()=>mostra(a);d.addEventListener('click',ver);tx.addEventListener('click',ver)});
function mostra(a){const T=TEM[a.m];const E=EIX.find(e=>e.k===a.e);
  document.getElementById('info').innerHTML=`<div class="n">Axioma ${a.n} · ${esc(E.t)}</div><h3>${esc(a.t)}</h3><blockquote>${esc(a.x)}</blockquote><div>${T.emo} ${esc(T.nome)}</div><p><a href="axiomas-360x.html#ax-${a.n}">📖 Ler com o comentário</a></p>`;
  const viz=new Set([a.n]);LIG.forEach(([x,y])=>{if(x===a.n)viz.add(y);if(y===a.n)viz.add(x)});
  realce(n=>viz.has(n),[...gLig.children].map(c=>[c,+c.dataset.a===a.n||+c.dataset.b===a.n]));history.replaceState(null,'','#ax-'+a.n)}
function realce(f,ls){Object.entries(dots).forEach(([n,[d,t]])=>{const on=f(+n);d.classList.toggle('fraco',!on);t.classList.toggle('fraco',!on)});
  if(ls)ls.forEach(([c,on])=>c.setAttribute('opacity',on?1:.08))}
let temaOn=null;const chips=document.getElementById('chips');
Object.entries(TEM).forEach(([k,T])=>{const n=AX.filter(a=>a.m===k).length;const b=document.createElement('button');b.className='chip';b.textContent=`${T.emo} ${T.nome} · ${n}`;b.style.borderColor=T.cor;
  b.onclick=()=>{temaOn=temaOn===k?null:k;[...chips.children].forEach(c=>c.classList.toggle('on',c===b&&temaOn));gTema.innerHTML='';
    if(!temaOn){realce(()=>true,[...gLig.children].map(c=>[c,true]));return}
    const lista=AX.filter(a=>a.m===k).sort((x,y)=>pos[x.n].th-pos[y.n].th);
    for(let i=0;i<lista.length;i++){const p=pos[lista[i].n],q=pos[lista[(i+1)%lista.length].n];if(lista.length>1)el('path',{d:curva(p,q),fill:'none',stroke:T.cor,'stroke-width':2.2,opacity:.85},gTema)}
    realce(n=>AX.find(a=>a.n===n).m===k,[...gLig.children].map(c=>[c,false]))};chips.appendChild(b)});
const h=location.hash.match(/^#ax-(\d+)$/);if(h){const a=AX.find(x=>x.n===+h[1]);if(a)mostra(a)}
})();
"""


def main():
    ax = carregar()
    f = os.path.join(OUT, "mapa-axiomas.html")
    open(f, "w", encoding="utf-8").write(pagina(ax))
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = b.new_page(viewport={"width": 1500, "height": 1000})
        erros = []
        pg.on("pageerror", lambda e: erros.append(str(e)))
        pg.goto("file://" + f)
        pg.wait_for_timeout(700)
        pg.add_style_tag(content=".topo{display:none}")
        pg.locator("#mapa").screenshot(path=os.path.join(OUT, "Axiomas_360X_Mapa_dos_Eixos.png"))
        pg.pdf(path=os.path.join(OUT, "Axiomas_360X_Mapa_dos_Eixos.pdf"), width="420mm", height="300mm", print_background=True)
        b.close()
    print("mapa", os.path.getsize(f), "bytes · ligações", len(ligacoes(ax)), "· erros JS", erros)


if __name__ == "__main__":
    main()
