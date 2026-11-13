#!/usr/bin/env python3
"""Cartões-imagem das bússolas (tela de bloqueio 1080×1920, JPG) + PDF A4 para imprimir (4 por página).
Uso: python3 tools/ho/cards_img.py <raiz_do_app> <pasta_pdf>"""
import json, sys, os, html
from playwright.sync_api import sync_playwright
from PIL import Image

ROOT = sys.argv[1]; OUT = sys.argv[2] if len(sys.argv) > 2 else "/tmp"
D = json.load(open(os.path.join(ROOT, "data/honra.json"), encoding="utf-8"))
dst = os.path.join(ROOT, "data/media/honra"); os.makedirs(dst, exist_ok=True)
e = html.escape

CSS = """*{box-sizing:border-box}body{margin:0;width:1080px;height:1920px;font-family:Inter,'Segoe UI',system-ui,sans-serif;color:#ece9e1;
background:radial-gradient(900px 700px at 50% 0%,#2a2140 0%,#0b0e13 62%),#0b0e13;overflow:hidden}
.fr{position:absolute;inset:34px;border:3px solid #d4af37;border-radius:46px;box-shadow:inset 0 0 0 10px #0b0e13,inset 0 0 0 12px #d4af3755}
.wrap{position:absolute;inset:70px 76px;display:flex;flex-direction:column}
.top{text-align:center;font:700 26px Cinzel,Georgia,serif;letter-spacing:6px;color:#f3d77a;opacity:.85}
.em{font-size:92px;text-align:center;margin:300px 0 4px}
h1{font:700 52px/1.15 Cinzel,Georgia,serif;text-align:center;margin:0 0 18px;color:#f3d77a;letter-spacing:1px}
.q{margin:4px auto 26px;width:420px;height:420px;border-radius:50%;border:4px solid #d4af37;display:flex;align-items:center;justify-content:center;text-align:center;padding:46px;
background:radial-gradient(#231b3d,#0d1118);font:italic 33px/1.32 Georgia,serif;box-shadow:0 0 60px #d4af3730}
.g{display:grid;grid-template-columns:1fr 1fr;gap:22px}
.d{border-radius:22px;padding:18px 22px;background:#121925;border:2px solid #2a3442;font-size:26px;line-height:1.32}
.d b{display:block;font-size:23px;letter-spacing:1px;margin-bottom:8px}
.n{border-color:#d4af37}.n b{color:#f3d77a}.l{border-color:#5be38a}.l b{color:#5be38a}.o{border-color:#4dd4ff}.o b{color:#4dd4ff}.s{border-color:#ff6b6b}.s b{color:#ff6b6b}
.al{margin-top:18px;border-radius:20px;padding:16px 22px;background:#3a1416;border:2px solid #ff6b6b;font:700 24px/1.32 Inter,sans-serif;color:#ffd6d6;text-align:center}
.ft{margin-top:auto;text-align:center;font-size:22px;color:#9aa4b2;line-height:1.5}.ft i{color:#f3d77a;font-style:normal}"""

def page(b):
    al = f'<div class="al">{e(b["al"])}</div>' if b.get("al") else ""
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="fr"></div><div class="wrap">
<div class="top">⚜ CÓDICE 360X · BÚSSOLA DE HONRA ⚜</div><div class="em">{b['e']}</div><h1>{e(b['t'])}</h1>
<div class="q">{e(b['q'])}</div>
<div class="g"><div class="d n"><b>⬆ NORTE · PRINCÍPIO</b>{e(b['N'])}</div><div class="d l"><b>➡ LESTE · FAÇA AGORA</b>{e(b['L'])}</div>
<div class="d o"><b>⬅ OESTE · ESPERE E CONSULTE</b>{e(b['O'])}</div><div class="d s"><b>⬇ SUL · EVITE</b>{e(b['S'])}</div></div>{al}
<div class="ft"><i>{' · '.join(e(r) for r in b['refs'][:4])}</i><br>🛡️ {' · '.join(b['mn'])}</div></div></body></html>"""

files = []
with sync_playwright() as p:
    br = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
    pg = br.new_page(viewport={"width": 1080, "height": 1920})
    for b in D["bu"]:
        pg.set_content(page(b)); pg.wait_for_timeout(120)
        f = os.path.join(dst, b["id"] + ".jpg"); pg.screenshot(path=f, type="jpeg", quality=86); files.append(f)
        # conferência: nada pode ultrapassar a moldura
        over = pg.evaluate("document.querySelector('.wrap').scrollHeight > document.querySelector('.wrap').clientHeight + 2")
        if over: print("⚠️ conteúdo excede o cartão:", b["id"], b["t"])
    br.close()

# PDF A4 (300 dpi), 4 cartões por página
W, H = 2480, 3508; cw, ch = 1150, 1650; pages = []
for i in range(0, len(files), 4):
    pgimg = Image.new("RGB", (W, H), "white")
    for j, f in enumerate(files[i:i + 4]):
        im = Image.open(f).convert("RGB").resize((int(1080 * ch / 1920), ch), Image.LANCZOS)
        x = 60 + (j % 2) * (cw + 60) + (cw - im.width) // 2; y = 70 + (j // 2) * (ch + 60)
        pgimg.paste(im, (x, y))
    pages.append(pgimg)
pdf = os.path.join(OUT, "Bussolas_de_Honra_360X_24_cartoes_A4.pdf")
pages[0].save(pdf, save_all=True, append_images=pages[1:], resolution=300)
print(len(files), "cartões ·", sum(os.path.getsize(f) for f in files) // 1024, "KB ·", pdf, os.path.getsize(pdf) // 1024, "KB")
