import re,sys
LIGHT = """
/*LIGHT-START — versão clara do IntensivaHub (mesma preferência do app: localStorage "theme"; ?tema=claro|escuro) */
html.light{--bg:#f6f8fb;--header:#ffffff;--card:#ffffff;--card2:#eef6fc;--text:#0f172a;--muted:#475569;--blue:#0369a1;--green:#15803d;--yellow:#a16207;--red:#be123c;--border:#cbd5e1;color-scheme:light}
html.light body{background:radial-gradient(circle at top,#e0f2fe 0%,var(--bg) 42%)}
html.light header{background:linear-gradient(135deg,#e0f2fe,#ffffff)}
html.light .card{background:rgba(255,255,255,.97);box-shadow:0 10px 30px rgba(15,23,42,.08)}
html.light .mini-card{background:#f8fafc}
html.light .tag{color:#075985;background:rgba(3,105,161,.08);border-color:rgba(3,105,161,.3)}
html.light .doctor-box,html.light .meta{color:#0c4a6e}
html.light .button{border-color:rgba(15,23,42,.18);background:rgba(15,23,42,.04)}
html.light .button.primary{background:linear-gradient(135deg,#0369a1,#2563eb);color:#fff;border:none}
html.light .alerta,html.light .danger{background:#fff1f2;border-color:#fda4af}
html.light .safe,html.light .success{background:#f0fdf4;border-color:#86efac}
html.light .yellow{background:#fefce8;border-color:#fde047}
html.light a{color:#075985}html.light .button.primary,html.light a.button{color:inherit}html.light .button.primary{background:linear-gradient(135deg,#0369a1,#2563eb);color:#fff;border:none}
html.light th{background:#e0f2fe;color:#0c4a6e}html.light td{background:#ffffff}
html.light footer{background:#eef2f7;color:#475569}
.themeBtn{position:fixed;top:12px;right:12px;z-index:50;padding:8px 12px;border-radius:999px;border:1px solid var(--border);background:var(--card);color:var(--text);font:600 14px Arial,sans-serif;cursor:pointer;box-shadow:0 4px 14px rgba(0,0,0,.18)}
/*LIGHT-END*/
"""
HEAD = '<script>try{var t=new URLSearchParams(location.search).get("tema");if(t)localStorage.setItem("theme",t==="claro"?"light":"dark");if(localStorage.getItem("theme")==="light")document.documentElement.classList.add("light")}catch(e){}</script>'
BTN = '''<button class="themeBtn" id="themeBtn" type="button" aria-label="Alternar versão clara/escura">☀️ Versão clara</button>
<script>(function(){var b=document.getElementById("themeBtn"),h=document.documentElement;function s(){var L=h.classList.contains("light");b.textContent=L?"🌙 Versão escura":"☀️ Versão clara";}s();b.onclick=function(){var L=!h.classList.contains("light");h.classList.toggle("light",L);try{localStorage.setItem("theme",L?"light":"dark")}catch(e){}s();};})();</script>'''
for p in sys.argv[1:]:
    s=open(p,encoding='utf-8').read()
    s=re.sub(r"\n?/\*LIGHT-START.*?/\*LIGHT-END\*/\n?","\n",s,flags=re.S)
    s=s.replace("</style>",LIGHT+"</style>",1)
    if HEAD not in s: s=s.replace("</title>","</title>\n  "+HEAD,1)
    if 'id="themeBtn"' not in s: s=s.replace("</body>",BTN+"\n</body>",1)
    open(p,'w',encoding='utf-8').write(s); print("ok",p)
