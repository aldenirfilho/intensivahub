"""Recursos de tela do livro Axiomas 360X (4.17.0): 🎧 audiolivro com a voz do aparelho,
🃏 axioma do dia com cartão 1080×1920 e atalho para o 🗺️ mapa dos eixos. Nada disso vai para o PDF."""
import html
import json

CSS = """
.so-tela{font-family:-apple-system,'Segoe UI',Roboto,sans-serif}
.painel{max-width:760px;margin:18px auto;padding:16px 18px;border:1px solid #3b3220;border-radius:14px;background:linear-gradient(180deg,#121a26,#0b0f16);color:#efe6cf}
.painel h2{font-family:'LoraLivro',Georgia,serif;color:#d4af37;font-size:20px;margin:0 0 10px;letter-spacing:.5px}
.painel .lin{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:8px 0}
.painel button,.painel select,.painel a.bt{font:inherit;font-size:14px;padding:8px 12px;border-radius:10px;border:1px solid #6b5626;background:#1b2433;color:#f3e7c4;cursor:pointer;text-decoration:none}
.painel button:hover,.painel a.bt:hover{border-color:#d4af37}
.painel button.pri{background:#d4af37;color:#1a1408;border-color:#d4af37;font-weight:700}
.painel .faixas{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:6px;margin-top:8px}
.painel .faixas button{text-align:left;font-size:13px}
.painel .faixas button.on{border-color:#22b8d6;box-shadow:0 0 0 1px #22b8d6 inset}
.painel .agora{font-size:13px;color:#9fd8e6;min-height:18px}
.painel .dia{border:1px solid #2c3a4f;border-radius:12px;padding:12px 14px;background:#0e141e}
.painel .dia .n{color:#22b8d6;font-size:12px;letter-spacing:2px;text-transform:uppercase}
.painel .dia h3{font-family:'LoraLivro',Georgia,serif;color:#d4af37;margin:4px 0 6px;font-size:18px}
.painel .dia blockquote{font-family:'LoraLivro',Georgia,serif;font-style:italic;margin:0;color:#f3ead2;font-size:16px;line-height:1.5}
.painel .cartao{margin-top:10px;display:none}
.painel .cartao img{max-width:220px;border-radius:12px;border:1px solid #6b5626;display:block}
.painel small{color:#b9ab86}
.ouvir-eixo{display:inline-block;margin:6px 0 2px;font-family:-apple-system,'Segoe UI',Roboto,sans-serif;font-size:13px;padding:6px 11px;border-radius:9px;border:1px solid var(--ouro,#9c7a2b);background:transparent;color:var(--ouro,#9c7a2b);cursor:pointer}
article.ax.lendo{outline:2px solid #22b8d6;outline-offset:6px;border-radius:6px;background:rgba(34,184,214,.06)}
#mini{position:fixed;left:50%;transform:translateX(-50%);bottom:max(10px,env(safe-area-inset-bottom));z-index:9;display:none;gap:6px;align-items:center;padding:8px 10px;border-radius:14px;border:1px solid #6b5626;background:rgba(11,15,22,.95);color:#efe6cf;box-shadow:0 6px 24px rgba(0,0,0,.45);max-width:calc(100vw - 20px)}
#mini.on{display:flex}#mini button{font:inherit;font-size:15px;padding:7px 10px;border-radius:9px;border:1px solid #6b5626;background:#1b2433;color:#f3e7c4;cursor:pointer}#mini span{font-size:12px;color:#9fd8e6;max-width:46vw;overflow:hidden;white-space:nowrap;text-overflow:ellipsis}
@media print{.so-tela,.ouvir-eixo,#mini{display:none!important}article.ax.lendo{outline:none;background:none}}
"""


def painel(eixos):
    faixas = "".join(f'<button data-faixa="{i}">▶️ {html.escape(r)} · {html.escape(t)}</button>' for i, (_, r, t, _) in enumerate(eixos))
    return f"""<section class="so-tela painel" id="leitor">
<h2>🃏 Axioma do dia</h2>
<div class="dia" id="dia"></div>
<div class="lin"><button class="pri" id="btCartao">🖼️ Cartão para a tela de bloqueio</button><button id="btOuvirDia">🔊 Ouvir</button><a class="bt" id="btIrDia" href="#">📖 Ler no livro</a></div>
<div class="cartao" id="cartao"><img id="cartaoImg" alt="Cartão do axioma do dia, 1080 por 1920"><div class="lin"><a class="bt" id="cartaoBaixar" download>⬇️ Baixar JPG</a><small>No iPhone: toque e segure a imagem → “Salvar na Fotos” → Ajustes › Papel de Parede.</small></div></div>
<h2 style="margin-top:18px">🎧 Audiolivro · um eixo por faixa</h2>
<div class="lin"><button class="pri" id="btPlay">▶️ Ouvir do início</button><button id="btPausa" disabled>⏸️ Pausar</button><button id="btParar" disabled>⏹️ Parar</button><button id="btProx" disabled>⏭️ Próxima faixa</button></div>
<div class="lin"><label>Velocidade <select id="selVel"><option>0.8</option><option>0.9</option><option selected>1</option><option>1.15</option><option>1.3</option><option>1.5</option></select></label>
<label>Voz <select id="selVoz"></select></label>
<label><input type="checkbox" id="chkCom" checked> ler os comentários</label>
<label><input type="checkbox" id="chkRolar" checked> acompanhar o texto</label></div>
<div class="agora" id="agora">Voz do próprio aparelho, em português · funciona sem internet depois de aberto.</div>
<div class="faixas" id="faixas">{faixas}</div>
<div class="lin" style="margin-top:14px"><a class="bt" href="mapa-axiomas.html">🗺️ Mapa dos eixos e temas</a><a class="bt so-gh" href="../downloads/Axiomas_360X_145_cartoes_tela_de_bloqueio.zip">🗂️ 145 cartões (ZIP)</a><a class="bt so-gh" href="../downloads/Axiomas_360X_Audiolivro_roteiro.txt">📜 Roteiro do audiolivro</a></div>
<small>O cartão e a voz são gerados no seu aparelho; nada é enviado para fora.</small>
</section>
<div id="mini" class="so-tela" role="region" aria-label="Controles do audiolivro"><button id="mPausa" aria-label="Pausar ou continuar">⏸️</button><button id="mProx" aria-label="Próxima faixa">⏭️</button><button id="mParar" aria-label="Parar">⏹️</button><span id="mTxt"></span><button id="mTopo" aria-label="Voltar ao painel">🎧</button></div>"""


def script(ax, eixos):
    dados = [dict(n=a["n"], t=a["tit"], e=a["eixo"], x=a["enun"], c=a["com"]) for a in sorted(ax, key=lambda a: a["n"])]
    eix = [dict(k=k, r=r, t=t) for k, r, t, _ in eixos]
    return "<script>const AX=" + json.dumps(dados, ensure_ascii=False) + ";const EIX=" + json.dumps(eix, ensure_ascii=False) + ";\n" + JS + "</script>"


JS = r"""
(function(){
const $=s=>document.querySelector(s);
const sorted=AX.slice().sort((a,b)=>a.n-b.n);
const porEixo=EIX.map(E=>sorted.filter(a=>a.e===E.k));
/* ---------- 🃏 axioma do dia: 17/11/2026 = axioma 1, um por dia, em ciclo ---------- */
function axDoDia(d){d=d||new Date();const base=Date.UTC(2026,10,17);const dia=Math.floor((Date.UTC(d.getFullYear(),d.getMonth(),d.getDate())-base)/864e5);return sorted[((dia%145)+145)%145]}
function esc(s){return s.replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]))}
const hoje=axDoDia();
if(!/github\.io$/.test(location.hostname))document.querySelectorAll('.so-gh').forEach(a=>a.remove());
function eixoNome(k){const E=EIX.find(x=>x.k===k);return E?E.t:k}
if($('#dia')){$('#dia').innerHTML=`<div class="n">Axioma ${hoje.n} · ${esc(eixoNome(hoje.e))}</div><h3>${esc(hoje.t)}</h3><blockquote>${esc(hoje.x)}</blockquote>`;$('#btIrDia').href='#ax-'+hoje.n}
/* ---------- cartão 1080×1920 (topo livre para o relógio do iPhone) ---------- */
function linhas(ctx,txt,larg){const out=[];let l='';for(const w of txt.split(/\s+/)){const t=l?l+' '+w:w;if(ctx.measureText(t).width>larg&&l){out.push(l);l=w}else l=t}if(l)out.push(l);return out}
async function desenhar(a,cv,comData){
  try{await document.fonts.load("italic 52px LoraLivro");await document.fonts.load("700 54px LoraLivro")}catch(e){}
  const W=1080,H=1920;cv.width=W;cv.height=H;const g=cv.getContext('2d');
  const bg=g.createLinearGradient(0,0,0,H);bg.addColorStop(0,'#070a10');bg.addColorStop(.45,'#0d1420');bg.addColorStop(1,'#111a28');g.fillStyle=bg;g.fillRect(0,0,W,H);
  const rad=g.createRadialGradient(W/2,1180,60,W/2,1180,760);rad.addColorStop(0,'rgba(212,175,55,.10)');rad.addColorStop(1,'rgba(212,175,55,0)');g.fillStyle=rad;g.fillRect(0,0,W,H);
  g.strokeStyle='rgba(212,175,55,.55)';g.lineWidth=3;g.strokeRect(46,46,W-92,H-92);g.strokeStyle='rgba(212,175,55,.25)';g.lineWidth=1.5;g.strokeRect(60,60,W-120,H-120);
  g.fillStyle='#d4af37';g.font='34px serif';g.textAlign='center';for(const [x,y] of [[60,60],[W-60,60],[60,H-60],[W-60,H-60]])g.fillText('✦',x,y+12);
  /* faixa 0–640 livre para hora e notificações */
  g.fillStyle='#22b8d6';g.font='600 30px -apple-system,Segoe UI,Roboto,sans-serif';
  const sp='AXIOMA '+a.n;g.fillText(sp.split('').join(String.fromCharCode(8202)),W/2,700);
  g.fillStyle='#d4af37';g.font='700 54px LoraLivro,Georgia,serif';let ty=790;for(const l of linhas(g,a.t,840).slice(0,3)){g.fillText(l,W/2,ty);ty+=66}
  g.font='30px serif';g.fillText('✦  ✦  ✦',W/2,ty+18);
  let fs=54,ls;for(;fs>=34;fs-=2){g.font=`italic ${fs}px LoraLivro,Georgia,serif`;ls=linhas(g,'“'+a.x+'”',830);if(ls.length*fs*1.42<=1560-(ty+90))break}
  g.fillStyle='#f3ead2';let y=ty+100;for(const l of ls){g.fillText(l,W/2,y);y+=fs*1.42}
  g.fillStyle='#22b8d6';g.font='500 28px -apple-system,Segoe UI,Roboto,sans-serif';g.fillText(eixoNome(a.e),W/2,1690);
  g.fillStyle='#d4af37';g.font='600 30px LoraLivro,Georgia,serif';g.fillText('⚜ Axiomas 360X · Aldenir Rocha de Oliveira Filho',W/2,1748);
  if(comData){g.fillStyle='rgba(243,234,210,.55)';g.font='24px -apple-system,Segoe UI,Roboto,sans-serif';const d=new Date();g.fillText('axioma do dia · '+d.toLocaleDateString('pt-BR'),W/2,1796)}
  return cv;
}
window.cartaoDataURL=async function(n,q){const a=sorted.find(x=>x.n===n);const cv=await desenhar(a,document.createElement('canvas'),false);return cv.toDataURL('image/jpeg',q||.9)};
if($('#btCartao'))$('#btCartao').onclick=async()=>{const cv=await desenhar(hoje,document.createElement('canvas'),true);const u=cv.toDataURL('image/jpeg',.92);$('#cartaoImg').src=u;$('#cartaoBaixar').href=u;$('#cartaoBaixar').download=`Axioma_${String(hoje.n).padStart(3,'0')}_do_dia.jpg`;$('#cartao').style.display='block'};
/* ---------- 🎧 audiolivro (Web Speech API, voz do aparelho) ---------- */
const S=window.speechSynthesis;const V={q:[],i:0,on:false,f:-1,gen:0,voz:null,rate:1};
function limpa(t){return t.replace(/[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}\u{FE0F}]/gu,'').replace(/nº/g,'número').replace(/\s—\s/g,', ').replace(/[“”"]/g,'').replace(/\s+/g,' ').trim()}
function pedacos(t){const fr=limpa(t).split(/(?<=[.!?;:])\s+/);const out=[];let cur='';for(let s of fr){while(s.length>200){let k=s.lastIndexOf(',',200);if(k<60)k=s.lastIndexOf(' ',200);out.push((cur?cur+' ':'')+s.slice(0,k+1));cur='';s=s.slice(k+1).trim()}if((cur+' '+s).length>200){if(cur)out.push(cur);cur=s}else cur=cur?cur+' '+s:s}if(cur)out.push(cur);return out}
function fila(fi){const E=EIX[fi];const L=[{t:`Faixa ${fi+1}. ${E.r==='⚜'?'':'Eixo '+E.r+'.'} ${E.t}.`}];for(const a of porEixo[fi]){L.push({t:`Axioma ${a.n}. ${a.t}.`,n:a.n});pedacos(a.x).forEach(p=>L.push({t:p,n:a.n}));if($('#chkCom')&&$('#chkCom').checked){L.push({t:'Comentário.',n:a.n});pedacos(a.c).forEach(p=>L.push({t:p,n:a.n}))}}return L}
function marca(n){document.querySelectorAll('article.ax.lendo').forEach(x=>x.classList.remove('lendo'));if(!n)return;const el=document.getElementById('ax-'+n);if(!el)return;el.classList.add('lendo');if(!$('#chkRolar')||$('#chkRolar').checked)el.scrollIntoView({behavior:'smooth',block:'center'})}
function ui(){const on=V.on;$('#btPausa').disabled=!(on||V.q.length);$('#btParar').disabled=!(on||V.q.length);$('#btProx').disabled=!(V.f>=0&&V.f<EIX.length-1);$('#btPausa').textContent=on?'⏸️ Pausar':'▶️ Continuar';$('#btPlay').textContent=on?'🔁 Recomeçar':'▶️ Ouvir do início';document.querySelectorAll('#faixas button').forEach((b,i)=>b.classList.toggle('on',i===V.f));const it=V.q[V.i];const mini=$('#mini');if(mini){mini.classList.toggle('on',V.q.length>0&&(V.on||V.i<V.q.length));$('#mPausa').textContent=on?'⏸️':'▶️';$('#mProx').disabled=!(V.f>=0&&V.f<EIX.length-1);$('#mTxt').textContent=V.f>=0?`Faixa ${V.f+1} · ${EIX[V.f].t}`:'Axioma do dia'}$('#agora').textContent=V.f<0?'Voz do próprio aparelho, em português · funciona sem internet depois de aberto.':`🎧 Faixa ${V.f+1}/${EIX.length} · ${EIX[V.f].t}${it&&it.n?' · axioma '+it.n:''}${on?'':' · pausado'}`}
function falar(){if(!V.on)return;if(V.i>=V.q.length){if(V.f>=0&&V.f<EIX.length-1){faixa(V.f+1);return}V.on=false;marca(0);ui();return}const it=V.q[V.i];const g=V.gen;const u=new SpeechSynthesisUtterance(it.t);u.lang='pt-BR';if(V.voz)u.voice=V.voz;u.rate=V.rate;u.onend=()=>{if(g!==V.gen)return;V.i++;falar()};u.onerror=e=>{if(g!==V.gen)return;if(e.error==='interrupted'||e.error==='canceled')return;V.i++;falar()};if(it.n)marca(it.n);ui();S.speak(u)}
function faixa(fi){V.gen++;S.cancel();V.f=fi;V.q=fila(fi);V.i=0;V.on=true;falar()}
function pausa(){if(V.on){V.on=false;V.gen++;S.cancel();ui()}else if(V.q.length){V.on=true;falar()}}
function parar(){V.on=false;V.gen++;S.cancel();V.q=[];V.i=0;V.f=-1;marca(0);ui()}
function vozes(){const sel=$('#selVoz');if(!sel||!S)return;const vs=S.getVoices().filter(v=>/^pt/i.test(v.lang));sel.innerHTML=vs.map((v,i)=>`<option value="${i}">${esc(v.name)} (${v.lang})</option>`).join('')||'<option>padrão do aparelho</option>';let k=vs.findIndex(v=>/pt-BR/i.test(v.lang)&&/Luciana|Francisca|Google|Natural/i.test(v.name));if(k<0)k=vs.findIndex(v=>/pt-BR/i.test(v.lang));try{const s=localStorage.getItem('axVoz');if(s&&vs[+s])k=+s}catch(e){}if(k>=0){sel.value=k;V.voz=vs[k]}sel.onchange=()=>{V.voz=vs[+sel.value]||null;try{localStorage.setItem('axVoz',sel.value)}catch(e){}}}
if(!S){const p=$('#leitor');if(p)$('#agora').textContent='Este navegador não tem voz sintetizada; o audiolivro funciona no Safari, Chrome e Edge.';document.querySelectorAll('#btPlay,#btOuvirDia,.ouvir-eixo,#faixas button').forEach(b=>b.disabled=true)}else{vozes();S.onvoiceschanged=vozes;
  try{const r=localStorage.getItem('axVel');if(r){V.rate=+r;$('#selVel').value=r}}catch(e){}
  $('#selVel').onchange=()=>{V.rate=+$('#selVel').value;try{localStorage.setItem('axVel',$('#selVel').value)}catch(e){}};
  $('#btPlay').onclick=()=>faixa(0);$('#mPausa').onclick=pausa;$('#mParar').onclick=parar;$('#mProx').onclick=()=>faixa(V.f+1);$('#mTopo').onclick=()=>$('#leitor').scrollIntoView({behavior:'smooth'});$('#btPausa').onclick=pausa;$('#btParar').onclick=parar;$('#btProx').onclick=()=>faixa(V.f+1);
  document.querySelectorAll('#faixas button').forEach(b=>b.onclick=()=>faixa(+b.dataset.faixa));
  document.querySelectorAll('.ouvir-eixo').forEach(b=>b.onclick=()=>faixa(+b.dataset.faixa));
  $('#btOuvirDia').onclick=()=>{V.gen++;S.cancel();V.f=-1;V.q=[{t:`Axioma ${hoje.n}. ${hoje.t}.`,n:hoje.n}].concat(pedacos(hoje.x).map(t=>({t,n:hoje.n})));V.i=0;V.on=true;falar()};
}
window.AXLIVRO={axDoDia,pedacos,fila,estado:()=>({on:V.on,f:V.f,i:V.i,q:V.q.length})};
})();
"""
