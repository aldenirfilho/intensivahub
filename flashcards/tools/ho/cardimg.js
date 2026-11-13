/* ---------------- 🖼️ Cartões-imagem de mnemônicos (canvas 1080×1920, funciona sem internet) ----------------
   Usado nas abas 🧠 Mnemônicos e 🕊️ Honra: botão 🖼️ em cada card e "Cartões dos ⭐ favoritos".
   Topo livre (≈300 px) para o relógio da tela de bloqueio do iPhone. */
const CARDIMG = {
  W: 1080, H: 1920,
  rr(x, a, b, w, h, r) { x.beginPath(); x.moveTo(a + r, b); x.arcTo(a + w, b, a + w, b + h, r); x.arcTo(a + w, b + h, a, b + h, r); x.arcTo(a, b + h, a, b, r); x.arcTo(a, b, a + w, b, r); x.closePath(); },
  wrap(x, t, maxW) { const ws = String(t || "").split(/\s+/), L = []; let l = ""; for (const w of ws) { const k = l ? l + " " + w : w; if (x.measureText(k).width > maxW && l) { L.push(l); l = w; } else l = k; } if (l) L.push(l); return L; },
  layout(x, m, s, draw, y0) {
    const W = this.W, F = (wt, px, fam) => `${wt} ${Math.round(px * s)}px ${fam}`, SANS = "Inter, -apple-system, 'Segoe UI', Roboto, sans-serif", SER = "Georgia, 'Times New Roman', serif";
    let y = y0 || 330;
    x.textAlign = "center"; x.font = F(600, 28, SANS); x.fillStyle = "#9aa4b2"; if (draw) x.fillText(String(m.tema || ""), W / 2, y); y += 70 * s;
    x.font = F(700, 48, SER); x.fillStyle = "#f3d77a";
    for (const l of this.wrap(x, m.t, 880)) { if (draw) x.fillText(l, W / 2, y); y += 60 * s; }
    let sz = 120 * Math.min(s, 1.2); x.font = `700 ${sz}px ${SER}`; while (x.measureText(m.m).width > 900 && sz > 44) { sz -= 4; x.font = `700 ${sz}px ${SER}`; }
    y += sz * 0.95; x.fillStyle = "#d4af37"; if (draw) x.fillText(m.m, W / 2, y); y += 80 * s;
    x.textAlign = "left"; x.font = F(700, 38, SANS);
    const labW = Math.min(300 * s, Math.max(...m.k.map(k => x.measureText(String(k[0])).width)) + 10), X0 = 110, X1 = X0 + labW + 24, maxT = W - 110 - X1;
    for (const [lab, txt] of m.k) {
      x.font = F(700, 38, SANS); x.fillStyle = "#4dd4ff"; if (draw) x.fillText(String(lab), X0, y);
      x.font = F(400, 34, SANS); x.fillStyle = "#ece9e1";
      const ls = this.wrap(x, txt, maxT); ls.forEach((l, i) => { if (draw) x.fillText(l, X1, y + i * 44 * s); }); y += Math.max(1, ls.length) * 44 * s + 18 * s;
    }
    if (m.x) {
      x.font = F(600, 30, SANS); const ls = this.wrap(x, "🎯 " + m.x, W - 300), h = ls.length * 40 * s + 50 * s; y += 10 * s;
      if (draw) { x.fillStyle = "rgba(255,193,77,.12)"; x.strokeStyle = "rgba(255,193,77,.6)"; x.lineWidth = 2; this.rr(x, 110, y - 34 * s, W - 220, h, 20); x.fill(); x.stroke(); x.fillStyle = "#ffd98a"; ls.forEach((l, i) => x.fillText(l, 140, y + i * 40 * s)); }
      y += h;
    }
    return y;
  },
  draw(m) {
    const W = this.W, H = this.H, c = document.createElement("canvas"); c.width = W; c.height = H; const x = c.getContext("2d");
    x.fillStyle = "#0b0e13"; x.fillRect(0, 0, W, H);
    const g = x.createRadialGradient(W / 2, 0, 40, W / 2, 0, 1150); g.addColorStop(0, "#2a2140"); g.addColorStop(1, "rgba(11,14,19,0)"); x.fillStyle = g; x.fillRect(0, 0, W, H);
    x.strokeStyle = "#d4af37"; x.lineWidth = 4; this.rr(x, 34, 34, W - 68, H - 68, 46); x.stroke();
    x.strokeStyle = "rgba(212,175,55,.35)"; x.lineWidth = 2; this.rr(x, 48, 48, W - 96, H - 96, 38); x.stroke();
    x.textAlign = "center"; x.fillStyle = "#f3d77a"; x.font = "700 26px Georgia, serif"; x.fillText("⚜  CÓDICE 360X · MNEMÔNICO  ⚜", W / 2, 110);
    let s = 1.45; while (s > 0.55 && this.layout(x, m, s, false) > H - 190) s -= 0.05;
    const free = (H - 190) - this.layout(x, m, s, false);   // centraliza o bloco abaixo da faixa do relógio
    this.layout(x, m, s, true, 330 + Math.max(0, free * 0.45));
    x.textAlign = "center"; x.font = "500 24px Inter, sans-serif"; x.fillStyle = "#9aa4b2";
    x.fillText((m.o === "c" ? "🏛️ Clássico" : m.o === "u" ? "✍️ Meu" : "⚒️ 360X") + " · treine no CÓDICE 360X", W / 2, H - 100);
    return c;
  },
  slug: t => String(t || "cartao").normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[^A-Za-z0-9]+/g, "_").slice(0, 40),
  show(list, titulo) {
    list = (list || []).filter(Boolean);
    if (!list.length) return toast("⭐ Nenhum favorito neste filtro — toque na ☆ de um mnemônico primeiro.");
    const max = 40, ov = document.createElement("div"); ov.className = "ciOv";
    ov.innerHTML = `<div class="ciBox"><div class="ciTop"><b>🖼️ ${esc(titulo || "Cartão-imagem")} · ${Math.min(list.length, max)}${list.length > max ? ` de ${list.length}` : ""}</b><button class="btn sm" id="ciX">✖️ Fechar</button></div>
      <p class="metaNow">📱 iPhone: toque e segure a imagem → “Salvar na Fotos” (serve de tela de bloqueio). 💻 Computador: ⬇️ Baixar.</p><div class="ciGrid"></div></div>`;
    document.body.appendChild(ov);
    const grid = ov.querySelector(".ciGrid"), close = () => ov.remove();
    ov.querySelector("#ciX").onclick = close; ov.onclick = e => { if (e.target === ov) close(); };
    list.slice(0, max).forEach((m, i) => setTimeout(() => {
      const url = this.draw(m).toDataURL("image/jpeg", 0.9), f = document.createElement("figure");
      f.innerHTML = `<img src="${url}" alt="${esc(m.t)}"><figcaption>${esc(m.m)}</figcaption><a class="btn sm" download="Mnemonico_360X_${this.slug(m.m)}.jpg" href="${url}">⬇️ Baixar</a>`;
      grid.appendChild(f);
    }, i * 30));
  } };
