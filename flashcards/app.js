/* CÓDICE 360X · Flashcards — app estático (GitHub Pages)
   Armazenamento: IndexedDB (neste aparelho). Importa .apkg (Anki 2.1 legado e 2.1.50+), JSON CÓDICE e TXT/CSV. */
"use strict";
const APP_VERSION = "1.0.0";
const DAY = 86400000, MIN = 60000;
const $ = (s, el = document) => el.querySelector(s);
const $$ = (s, el = document) => [...el.querySelectorAll(s)];
const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const strip = h => String(h || "").replace(/<style[\s\S]*?<\/style>/gi, "").replace(/<[^>]+>/g, " ").replace(/&nbsp;/g, " ").replace(/&[a-z]+;/gi, " ").replace(/\s+/g, " ").trim();
const today = () => { const d = new Date(); return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0"); };
const endOfDay = () => { const d = new Date(); d.setHours(23, 59, 59, 999); return d.getTime(); };
function hash(str) { let h1 = 0xdeadbeef, h2 = 0x41c6ce57; for (let i = 0; i < str.length; i++) { const c = str.charCodeAt(i); h1 = Math.imul(h1 ^ c, 2654435761); h2 = Math.imul(h2 ^ c, 1597334677); } h1 = Math.imul(h1 ^ (h1 >>> 16), 2246822507) ^ Math.imul(h2 ^ (h2 >>> 13), 3266489909); h2 = Math.imul(h2 ^ (h2 >>> 16), 2246822507) ^ Math.imul(h1 ^ (h1 >>> 13), 3266489909); return (h2 >>> 0).toString(36) + (h1 >>> 0).toString(36); }
function toast(msg, ms = 2600) { const t = $("#toast"); t.innerHTML = msg; t.style.display = "block"; clearTimeout(toast._t); toast._t = setTimeout(() => t.style.display = "none", ms); }

/* ---------------- Estilo padrão dos cards CÓDICE ---------------- */
const CODICE_CSS = `.card{font-family:Inter,-apple-system,"Segoe UI",Roboto,sans-serif;font-size:19px;line-height:1.5;text-align:left;color:#ece9e1;background:#0e1116;padding:14px 16px;border-radius:14px;border:1px solid #2a3442}
.tema{display:inline-block;font-size:13px;color:#0e1116;background:linear-gradient(90deg,#d4af37,#f3d77a);padding:3px 10px;border-radius:12px;font-weight:700;margin-bottom:10px}
.q{font-size:22px;font-weight:600;color:#fff;border-left:4px solid #4dd4ff;padding-left:10px}
hr#answer{border:0;height:2px;background:linear-gradient(90deg,#d4af37,#4dd4ff,transparent);margin:14px 0}
.a{background:#151b23;border:1px solid #2a3442;border-radius:10px;padding:12px 14px}
b{color:#fff}.r{color:#ff6b6b!important}.g{color:#5be38a!important}.y{color:#ffc14d!important}.c{color:#4dd4ff!important}
table.t{color:#ece9e1;border-collapse:collapse;width:100%;margin:8px 0;font-size:16px}
table.t th{background:#1d2a36;color:#4dd4ff;padding:6px 8px;border:1px solid #33414f;text-align:left}
table.t td{color:#ece9e1;padding:6px 8px;border:1px solid #2a3442;vertical-align:top}
table.t tr:nth-child(even) td{background:#121820}
ul{margin:6px 0;padding-left:22px}li{margin:3px 0}
.img{margin-top:12px;text-align:center}.img img,.img svg{max-width:100%;height:auto;border-radius:8px;border:1px solid #2a3442}
.peg{margin-top:12px;background:#2a2210;border-left:4px solid #ffc14d;border-radius:6px;padding:10px 12px;font-size:16px;color:#ffe9b8}
.src{margin-top:10px;font-size:13px;color:#8a94a3}
.cloze{color:#4dd4ff;font-weight:700}
@media(max-width:560px){.card{font-size:17px;padding:12px}.q{font-size:19px}table.t{font-size:14px}}`;

/* ---------------- IndexedDB ---------------- */
const DB = {
  db: null,
  open() {
    return new Promise((res, rej) => {
      let r;
      try { r = indexedDB.open("codice360x", 1); } catch (e) { return rej(e); }
      r.onupgradeneeded = () => {
        const d = r.result;
        d.createObjectStore("cards", { keyPath: "id" });
        d.createObjectStore("media", { keyPath: "name" });
        d.createObjectStore("styles", { keyPath: "id" });
        d.createObjectStore("meta", { keyPath: "k" });
      };
      r.onsuccess = () => { DB.db = r.result; res(); };
      r.onerror = () => rej(r.error);
    });
  },
  tx(store, mode = "readonly") { return DB.db.transaction(store, mode).objectStore(store); },
  all(store) { return new Promise((res, rej) => { const q = DB.tx(store).getAll(); q.onsuccess = () => res(q.result); q.onerror = () => rej(q.error); }); },
  get(store, key) { return new Promise((res, rej) => { const q = DB.tx(store).get(key); q.onsuccess = () => res(q.result); q.onerror = () => rej(q.error); }); },
  putMany(store, items) {
    return new Promise((res, rej) => {
      if (!items.length) return res();
      const t = DB.db.transaction(store, "readwrite"), s = t.objectStore(store);
      items.forEach(i => s.put(i)); t.oncomplete = () => res(); t.onerror = () => rej(t.error);
    });
  },
  put(store, item) { return DB.putMany(store, [item]); },
  delMany(store, keys) { return new Promise((res, rej) => { const t = DB.db.transaction(store, "readwrite"), s = t.objectStore(store); keys.forEach(k => s.delete(k)); t.oncomplete = () => res(); t.onerror = () => rej(t.error); }); },
  clear(store) { return new Promise((res, rej) => { const q = DB.tx(store, "readwrite").clear(); q.onsuccess = () => res(); q.onerror = () => rej(q.error); }); },
  async meta(k, def) { const r = await DB.get("meta", k); return r ? r.v : def; },
  setMeta(k, v) { return DB.put("meta", { k, v }); },
};

/* ---------------- Estado ---------------- */
const S = { cards: [], byId: new Map(), styles: new Map(), mediaURL: new Map(), settings: null, log: null };
const DEFAULTS = { newPerDay: 20, revPerDay: 300, steps: [1, 10], relearn: [10], grad: 1, easy: 4, startEase: 2.5, maxIvl: 3650, learnAhead: 20 };

async function loadAll() {
  S.cards = await DB.all("cards");
  S.byId = new Map(S.cards.map(c => [c.id, c]));
  S.styles = new Map((await DB.all("styles")).map(s => [s.id, s.css]));
  S.settings = Object.assign({}, DEFAULTS, await DB.meta("settings", {}));
  S.log = await DB.meta("log:" + today(), { d: today(), nNew: 0, nRev: 0, nAns: 0, nOk: 0, ms: 0 });
  if (S.log.d !== today()) S.log = { d: today(), nNew: 0, nRev: 0, nAns: 0, nOk: 0, ms: 0 };
}
const saveLog = () => DB.setMeta("log:" + today(), S.log);

/* ---------------- Repetição espaçada (SM-2 estilo Anki) ---------------- */
function newSRS() { return { st: "new", due: 0, ivl: 0, ease: S.settings?.startEase || 2.5, reps: 0, lapses: 0, step: 0 }; }
function schedule(srs, g, now = Date.now()) {
  const st = S.settings, o = Object.assign({}, srs);
  const fuzz = d => d < 3 ? d : Math.round(d * (0.95 + Math.random() * 0.1));
  const toReview = (ivl) => { o.st = "review"; o.ivl = Math.min(st.maxIvl, Math.max(1, ivl)); o.due = now + fuzz(o.ivl) * DAY; o.step = 0; };
  o.reps++;
  if (o.st === "new" || o.st === "learn") {
    const steps = st.steps.length ? st.steps : [1];
    if (o.st === "new") o.step = 0;
    o.st = "learn";
    if (g === 1) { o.step = 0; o.due = now + steps[0] * MIN; }
    else if (g === 2) { const m = o.step === 0 && steps.length > 1 ? (steps[0] + steps[1]) / 2 : steps[o.step] * 1.2; o.due = now + m * MIN; }
    else if (g === 3) { if (o.step + 1 >= steps.length) toReview(st.grad); else { o.step++; o.due = now + steps[o.step] * MIN; } }
    else toReview(st.easy);
  } else if (o.st === "relearn") {
    const steps = st.relearn.length ? st.relearn : [10];
    if (g === 1) { o.step = 0; o.due = now + steps[0] * MIN; }
    else if (g === 2) { o.due = now + steps[o.step] * 1.5 * MIN; }
    else if (g === 3) { if (o.step + 1 >= steps.length) toReview(o.ivl || 1); else { o.step++; o.due = now + steps[o.step] * MIN; } }
    else toReview((o.ivl || 1) + 1);
  } else {
    const ivl = o.ivl || 1;
    if (g === 1) { o.lapses++; o.ease = Math.max(1.3, o.ease - 0.2); o.ivl = 1; o.st = "relearn"; o.step = 0; o.due = now + (st.relearn[0] || 10) * MIN; }
    else if (g === 2) { o.ease = Math.max(1.3, o.ease - 0.15); toReview(Math.max(ivl + 1, Math.round(ivl * 1.2))); }
    else if (g === 3) { toReview(Math.max(ivl + 1, Math.round(ivl * o.ease))); }
    else { o.ease += 0.15; toReview(Math.max(ivl + 2, Math.round(ivl * o.ease * 1.3))); }
  }
  return o;
}
function fmtIvl(ms) {
  const m = ms / MIN;
  if (m < 60) return Math.max(1, Math.round(m)) + " min";
  if (m < 1440) return Math.round(m / 60) + " h";
  const d = m / 1440;
  if (d < 30) return Math.round(d) + " d";
  if (d < 365) return (d / 30).toFixed(1).replace(".0", "") + " m";
  return (d / 365).toFixed(1).replace(".0", "") + " a";
}

/* ---------------- Contagens e fila ---------------- */
function inDeck(c, prefix) { return !prefix || c.deck === prefix || c.deck.startsWith(prefix + "::"); }
function counts(prefix) {
  const now = Date.now(), eod = endOfDay();
  let n = 0, l = 0, r = 0;
  for (const c of S.cards) {
    if (c.susp || !inDeck(c, prefix)) continue;
    const s = c.srs;
    if (s.st === "new") n++;
    else if (s.st === "learn" || s.st === "relearn") { if (s.due <= now + S.settings.learnAhead * MIN) l++; }
    else if (s.due <= eod) r++;
  }
  const newLeft = Math.max(0, S.settings.newPerDay - S.log.nNew), revLeft = Math.max(0, S.settings.revPerDay - S.log.nRev);
  return { n: Math.min(n, newLeft), l, r: Math.min(r, revLeft), nAll: n };
}
const Study = { prefix: null, ids: null, cur: null, shown: false, undo: [], t0: 0, total: 0, done: 0 };
function nextCard() {
  const now = Date.now(), eod = endOfDay(), st = S.settings;
  const pool = S.cards.filter(c => !c.susp && (Study.ids ? Study.ids.has(c.id) : inDeck(c, Study.prefix)));
  if (Study.ids) { // estudo filtrado (busca): ordem de vencimento, inclui não vencidos
    const notDone = pool.filter(c => !Study.seen.has(c.id) || ((c.srs.st === "learn" || c.srs.st === "relearn") && c.srs.due <= now + st.learnAhead * MIN));
    notDone.sort((a, b) => (Study.seen.has(a.id) - Study.seen.has(b.id)) || a.srs.due - b.srs.due);
    return notDone[0] || null;
  }
  const learnDue = pool.filter(c => (c.srs.st === "learn" || c.srs.st === "relearn") && c.srs.due <= now).sort((a, b) => a.srs.due - b.srs.due);
  if (learnDue.length) return learnDue[0];
  const revLeft = st.revPerDay - S.log.nRev, newLeft = st.newPerDay - S.log.nNew;
  const rev = revLeft > 0 ? pool.filter(c => c.srs.st === "review" && c.srs.due <= eod).sort((a, b) => a.srs.due - b.srs.due) : [];
  const nw = newLeft > 0 ? pool.filter(c => c.srs.st === "new").sort((a, b) => a.ord - b.ord) : [];
  // intercala: 1 novo a cada 4 revisões
  if (rev.length && (!nw.length || (S.log.nRev % 5 !== 4))) return rev[0];
  if (nw.length) return nw[0];
  if (rev.length) return rev[0];
  const ahead = pool.filter(c => (c.srs.st === "learn" || c.srs.st === "relearn") && c.srs.due <= now + st.learnAhead * MIN).sort((a, b) => a.srs.due - b.srs.due);
  return ahead[0] || null;
}

/* ---------------- Renderização segura do card ---------------- */
function sanitize(html) {
  const doc = new DOMParser().parseFromString(`<div id="__r">${html}</div>`, "text/html");
  doc.querySelectorAll("script,iframe,object,embed,link,meta,base,form").forEach(e => e.remove());
  doc.querySelectorAll("*").forEach(el => {
    [...el.attributes].forEach(a => {
      const n = a.name.toLowerCase(), v = a.value.trim().toLowerCase();
      if (n.startsWith("on") || ((n === "href" || n === "src" || n === "xlink:href") && v.startsWith("javascript:"))) el.removeAttribute(a.name);
    });
  });
  return doc.getElementById("__r").innerHTML;
}
async function mediaURL(name) {
  if (S.mediaURL.has(name)) return S.mediaURL.get(name);
  const m = await DB.get("media", name);
  if (!m) return null;
  const u = URL.createObjectURL(m.blob); S.mediaURL.set(name, u); return u;
}
async function renderInto(host, html, styleId) {
  const root = host.shadowRoot || host.attachShadow({ mode: "open" });
  const css = S.styles.get(styleId) || CODICE_CSS;
  root.innerHTML = `<style>:host{display:block}${styleId === "codice" ? "" : CODICE_BASE_WRAP}${css}</style><div class="card nightMode night_mode">${sanitize(html)}</div>`;
  for (const img of root.querySelectorAll("[data-m]")) {
    const u = await mediaURL(img.getAttribute("data-m"));
    if (u) img.setAttribute("src", u); else img.setAttribute("alt", "🖼️ imagem ausente: " + img.getAttribute("data-m"));
  }
}
const CODICE_BASE_WRAP = `.card{border-radius:14px;padding:14px 16px;min-height:200px;overflow-x:auto} img{max-width:100%;height:auto} table{max-width:100%}`;

/* ---------------- Formato CÓDICE (JSON) → HTML ---------------- */
function imgHTML(v) {
  if (!v) return "";
  v = String(v).trim();
  if (v.startsWith("<svg")) return `<div class=img>${v}</div>`;
  if (/^(data:|https?:)/i.test(v)) return `<div class=img><img src="${esc(v)}"></div>`;
  return `<div class=img><img data-m="${esc(v.replace(/^.*\//, ""))}"></div>`;
}
function renderCloze(text, n, answer) {
  return text.replace(/\{\{c(\d+)::([\s\S]*?)(?:::([\s\S]*?))?\}\}/g, (m, num, body, hint) => {
    if (+num !== n) return body;
    return answer ? `<span class=cloze>${body}</span>` : `<span class=cloze>[${hint ? esc(strip(hint)) : "..."}]</span>`;
  });
}
function codiceHTML(c, clozeN) {
  const tail = c.deck.split("::").slice(-1)[0];
  let qf = c.f, af = c.f;
  if (clozeN) { qf = renderCloze(c.f, clozeN, false); af = renderCloze(c.f, clozeN, true); }
  const head = `<div class=tema>${esc(tail)}</div>`;
  const q = `${head}<div class=q>${qf}</div>`;
  const a = `${head}<div class=q>${af}</div><hr id=answer>` + (c.b ? `<div class=a>${c.b}</div>` : "") + imgHTML(c.img) +
    (c.x ? `<div class=peg>🎯 <b>Pegadinha / Nerd</b><br>${c.x}</div>` : "") + (c.s ? `<div class=src>📚 ${c.s}</div>` : "");
  return { q, a };
}
const pick = (o, ...ks) => { for (const k of ks) { if (o[k] != null && o[k] !== "") return o[k]; } return ""; };
function normalizeCards(obj, forcedDeck) {
  const rootDeck = forcedDeck || pick(obj, "baralho", "deck", "deckName") || "Importados::" + today();
  const list = Array.isArray(obj) ? obj : (obj.cards || obj.flashcards || obj.notes || []);
  const out = [];
  list.forEach((r, i) => {
    if (typeof r !== "object" || !r) return;
    const f = String(pick(r, "frente", "front", "pergunta", "question", "q", "Frente", "Front"));
    if (!f.trim()) return;
    let deck = forcedDeck ? forcedDeck : (pick(r, "baralho", "deck") || rootDeck);
    const sub = pick(r, "subtema", "subtopic", "subdeck", "subtopico");
    if (sub && !String(deck).endsWith("::" + sub)) deck += "::" + sub;
    let tags = pick(r, "tags", "etiquetas"); if (typeof tags === "string") tags = tags.split(/[\s,]+/).filter(Boolean); if (!Array.isArray(tags)) tags = [];
    const base = { deck: String(deck).replace(/\s*::\s*/g, "::"), f, b: String(pick(r, "verso", "back", "resposta", "answer", "a", "Verso", "Back")),
      x: String(pick(r, "pegadinha", "extra", "nerd", "dica", "curiosidade")), s: String(pick(r, "fonte", "source", "referencia", "ref")),
      img: pick(r, "imagem", "image", "img", "svg"), tags };
    const clozes = [...new Set([...f.matchAll(/\{\{c(\d+)::/g)].map(m => +m[1]))].sort((a, b) => a - b);
    if (clozes.length) clozes.forEach(n => out.push(Object.assign({}, base, { cloze: n })));
    else out.push(base);
  });
  return out;
}
function extractJSON(text) {
  text = text.replace(/[“”]/g, '"').replace(/ /g, " ");
  const blocks = [...text.matchAll(/```(?:json)?\s*([\s\S]*?)```/gi)].map(m => m[1]);
  const cands = blocks.length ? blocks : [text.slice(Math.min(...["{", "["].map(ch => text.indexOf(ch) < 0 ? 1e9 : text.indexOf(ch))))];
  const out = [];
  for (let c of cands) {
    c = c.trim(); if (!c) continue;
    try { out.push(JSON.parse(c)); continue; } catch (e) { }
    try { out.push(JSON.parse(c.replace(/,\s*([}\]])/g, "$1"))); continue; } catch (e) { }
    const end = Math.max(c.lastIndexOf("}"), c.lastIndexOf("]")); // tenta cortar lixo no fim
    try { out.push(JSON.parse(c.slice(0, end + 1).replace(/,\s*([}\]])/g, "$1"))); } catch (e) { throw new Error("JSON inválido: " + e.message); }
  }
  return out;
}
function parseTextLines(text, deck) {
  const lines = text.split(/\r?\n/).map(l => l.trim()).filter(Boolean);
  const out = [];
  for (const l of lines) {
    if (/^#/.test(l)) continue;
    let parts = l.includes("\t") ? l.split("\t") : l.includes(" ;; ") ? l.split(" ;; ") : l.includes(";") ? l.split(";") : l.includes("|") ? l.split("|") : null;
    if (!parts || parts.length < 2) continue;
    if (/^(frente|front|pergunta)$/i.test(parts[0].trim())) continue;
    out.push({ frente: parts[0].trim(), verso: parts[1].trim(), pegadinha: (parts[2] || "").trim(), tags: (parts[3] || "").trim() });
  }
  return normalizeCards({ baralho: deck || "Importados::" + today(), cards: out });
}
async function storeMediaMap(midia, baseURL) {
  const items = [];
  for (const [name, v] of Object.entries(midia || {})) {
    try {
      let blob;
      if (String(v).startsWith("data:")) blob = await (await fetch(v)).blob();
      else if (/^<svg/i.test(String(v))) blob = new Blob([v], { type: "image/svg+xml" });
      else blob = await (await fetch(new URL(v, baseURL || location.href))).blob();
      items.push({ name, blob });
    } catch (e) { console.warn("mídia falhou", name, e); }
  }
  await DB.putMany("media", items);
  items.forEach(i => { if (S.mediaURL.has(i.name)) { URL.revokeObjectURL(S.mediaURL.get(i.name)); S.mediaURL.delete(i.name); } });
  return items.length;
}
/* Insere/atualiza cards preservando progresso. Retorna {novos, atualizados} */
async function upsert(rawCards, origin) {
  let maxOrd = S.cards.reduce((m, c) => Math.max(m, c.ord || 0), 0);
  const put = []; let novos = 0, atual = 0;
  for (const r of rawCards) {
    const id = r.id || "c:" + hash(r.deck + "|" + strip(r.f) + "|" + (r.cloze || 0));
    const { q, a } = r.q ? { q: r.q, a: r.a } : codiceHTML(r, r.cloze);
    const old = S.byId.get(id);
    const card = Object.assign(old || { id, srs: newSRS(), ord: ++maxOrd, created: Date.now(), susp: false, marked: false }, {
      deck: r.deck, q, a, style: r.style || "codice", tags: r.tags || [], origin: origin || "import",
      txt: (strip(q) + " " + strip(a) + " " + (r.tags || []).join(" ")).toLowerCase(),
    });
    if (old) atual++; else novos++;
    put.push(card);
  }
  // dedupe ids na mesma importação
  const uniq = [...new Map(put.map(c => [c.id, c])).values()];
  await DB.putMany("cards", uniq);
  uniq.forEach(c => { if (!S.byId.has(c.id)) S.cards.push(c); S.byId.set(c.id, c); });
  return { novos, atual };
}

/* ---------------- Leitor de .apkg ---------------- */
let SQLp = null;
function loadSQL() {
  if (SQLp) return SQLp;
  SQLp = new Promise((res, rej) => {
    const s = document.createElement("script"); s.src = "lib/sql-asm.js";
    s.onload = () => initSqlJs().then(res, rej); s.onerror = () => rej(new Error("não carregou sql.js"));
    document.head.appendChild(s);
  });
  return SQLp;
}
const isZstd = u8 => u8.length > 4 && u8[0] === 0x28 && u8[1] === 0xb5 && u8[2] === 0x2f && u8[3] === 0xfd;
const unz = u8 => isZstd(u8) ? fzstd.decompress(u8) : u8;
/* protobuf mínimo: retorna {campo: [valores]} (bytes para length-delimited, número para varint) */
function pb(u8) {
  const out = {}; let i = 0;
  const varint = () => { let r = 0, s = 0, b; do { b = u8[i++]; r += (b & 0x7f) * Math.pow(2, s); s += 7; } while (b & 0x80); return r; };
  while (i < u8.length) {
    const key = varint(), f = Math.floor(key / 8), w = key & 7; let v;
    if (w === 0) v = varint(); else if (w === 2) { const len = varint(); v = u8.subarray(i, i + len); i += len; }
    else if (w === 1) { i += 8; continue; } else if (w === 5) { i += 4; continue; } else break;
    (out[f] = out[f] || []).push(v);
  }
  return out;
}
const td = new TextDecoder();
const pbStr = (o, f) => o[f] && o[f][0] instanceof Uint8Array ? td.decode(o[f][0]) : "";

function renderTemplate(tpl, F, ord, answer, front, extra) {
  let s = tpl.replace(/\{\{\s*FrontSide\s*\}\}/g, front || "");
  for (let k = 0; k < 8; k++) {
    const n = s.replace(/\{\{([#^])\s*([^}]+?)\s*\}\}([\s\S]*?)\{\{\/\s*\2\s*\}\}/g, (m, t, name, body) => {
      const key = name.split(":").pop().trim(); const val = String(F[key] ?? extra[key] ?? "").replace(/<br\s*\/?>|&nbsp;|\s/gi, "");
      return (t === "#" ? !!val : !val) ? body : "";
    });
    if (n === s) break; s = n;
  }
  s = s.replace(/\{\{([^{}#^\/][^{}]*)\}\}/g, (m, expr) => {
    const parts = expr.split(":").map(x => x.trim()); const name = parts.pop(); const filters = parts;
    let v = F[name] ?? extra[name];
    if (v == null) return "";
    if (filters.includes("type")) return "";
    if (filters.includes("cloze")) v = renderCloze(v, ord + 1, answer);
    if (filters.includes("text")) v = esc(strip(v));
    if (filters.includes("hint")) v = `<details><summary>💡 dica</summary>${v}</details>`;
    if (filters.some(f => f.startsWith("tts"))) return "";
    return v;
  });
  return s.replace(/\[sound:[^\]]+\]/g, "");
}
function fixMediaRefs(html) {
  return html.replace(/<img([^>]*?)\ssrc=(["'])([^"']+)\2/gi, (m, pre, q, src) =>
    /^(data:|https?:|blob:)/i.test(src) ? m : `<img${pre} data-m="${esc(decodeURIComponent(src))}"`);
}
async function importApkg(file, forcedDeck, log) {
  log("📦 Lendo pacote… (carregando motor SQLite, ~1,4 MB na 1ª vez)");
  const zip = await JSZip.loadAsync(file);
  const SQL = await loadSQL();
  let colName = zip.file("collection.anki21b") ? "collection.anki21b" : zip.file("collection.anki21") ? "collection.anki21" : "collection.anki2";
  if (!zip.file(colName)) throw new Error("Arquivo não parece um .apkg do Anki (sem collection).");
  const colBytes = unz(await zip.file(colName).async("uint8array"));
  const db = new SQL.Database(colBytes);
  const q = (sql) => { const r = db.exec(sql); if (!r.length) return []; const { columns, values } = r[0]; return values.map(v => Object.fromEntries(columns.map((c, i) => [c, v[i]]))); };
  const tables = q("select name from sqlite_master where type='table'").map(r => r.name);
  const models = {}, decks = {};
  if (tables.includes("notetypes")) {
    for (const nt of q("select id,name,config from notetypes")) {
      const cfg = pb(nt.config); const kind = cfg[1] ? cfg[1][0] : 0;
      models[nt.id] = { name: nt.name, type: kind === 1 ? 1 : 0, css: pbStr(cfg, 3), flds: [], tmpls: [] };
    }
    for (const f of q("select ntid,ord,name from fields order by ntid,ord")) models[f.ntid] && models[f.ntid].flds.push(f.name);
    for (const t of q("select ntid,ord,name,config from templates order by ntid,ord")) {
      const c = pb(t.config); models[t.ntid] && (models[t.ntid].tmpls[t.ord] = { qfmt: pbStr(c, 1), afmt: pbStr(c, 2) });
    }
    for (const d of q("select id,name from decks")) decks[d.id] = String(d.name).replace(/\x1f/g, "::");
  } else {
    const col = q("select models,decks from col")[0];
    for (const [id, m] of Object.entries(JSON.parse(col.models))) models[id] = { name: m.name, type: m.type, css: m.css, flds: m.flds.sort((a, b) => a.ord - b.ord).map(f => f.name), tmpls: m.tmpls.sort((a, b) => a.ord - b.ord).map(t => ({ qfmt: t.qfmt, afmt: t.afmt })) };
    for (const [id, d] of Object.entries(JSON.parse(col.decks))) decks[id] = d.name;
  }
  // mídia
  const mediaFile = zip.file("media");
  let map = {};
  if (mediaFile) {
    const raw = await mediaFile.async("uint8array");
    const txt = td.decode(raw.subarray(0, 1));
    if (txt === "{") map = JSON.parse(td.decode(raw));
    else { const ents = pb(unz(raw))[1] || []; ents.forEach((e, i) => { map[String(i)] = pbStr(pb(e), 1); }); }
  }
  const mItems = [];
  for (const [num, name] of Object.entries(map)) {
    const f = zip.file(num); if (!f || !name) continue;
    const bytes = unz(await f.async("uint8array"));
    const ext = name.split(".").pop().toLowerCase();
    const type = { png: "image/png", jpg: "image/jpeg", jpeg: "image/jpeg", gif: "image/gif", webp: "image/webp", svg: "image/svg+xml" }[ext] || "application/octet-stream";
    mItems.push({ name, blob: new Blob([bytes], { type }) });
  }
  await DB.putMany("media", mItems);
  log(`🖼️ ${mItems.length} imagens/mídias`);
  // estilos
  const styleRows = Object.entries(models).map(([id, m]) => ({ id: "m:" + id, css: m.css || "" }));
  await DB.putMany("styles", styleRows); styleRows.forEach(s => S.styles.set(s.id, s.css));
  const rows = q("select c.id cid,c.did,c.odid,c.ord,n.mid,n.flds,n.tags,n.guid from cards c join notes n on c.nid=n.id order by c.id");
  log(`🎴 ${rows.length} cards encontrados — montando…`);
  const raw = [];
  for (const r of rows) {
    const m = models[r.mid]; if (!m) continue;
    const vals = String(r.flds).split("\x1f"); const F = {}; m.flds.forEach((n, i) => F[n] = vals[i] || "");
    const deckName = forcedDeck || decks[r.odid || r.did] || decks[r.did] || "Importados";
    const tpl = m.type === 1 ? m.tmpls[0] : m.tmpls[r.ord];
    if (!tpl) continue;
    const extra = { Tags: String(r.tags || "").trim(), Deck: deckName, Subdeck: deckName.split("::").pop(), Card: "", Type: m.name };
    const qh = fixMediaRefs(renderTemplate(tpl.qfmt, F, r.ord, false, "", extra));
    const ah = fixMediaRefs(renderTemplate(tpl.afmt, F, r.ord, true, qh, extra));
    raw.push({ id: "a:" + r.guid + ":" + r.ord, deck: deckName, q: qh, a: ah, style: "m:" + r.mid, tags: String(r.tags || "").trim().split(/\s+/).filter(Boolean) });
  }
  db.close();
  return upsert(raw, "apkg:" + file.name);
}

/* ---------------- Importação genérica ---------------- */
async function importText(text, forcedDeck, log, origin, baseURL) {
  const t = text.trim();
  if (/^[\[{]|```/.test(t) || t.includes('"cards"') || t.includes('"frente"')) {
    const objs = extractJSON(t); let tot = { novos: 0, atual: 0 };
    for (const o of objs) {
      if (o && o.formato === "codice360x-backup-v1") { await restoreBackup(o); log("🛟 Backup restaurado."); return { novos: o.cards.length, atual: 0 }; }
      const nm = await storeMediaMap(o.midia || o.media, baseURL);
      if (nm) log(`🖼️ ${nm} imagens`);
      const r = await upsert(normalizeCards(o, forcedDeck), origin || "json");
      tot.novos += r.novos; tot.atual += r.atual;
    }
    return tot;
  }
  const cards = parseTextLines(t, forcedDeck);
  if (!cards.length) throw new Error("Não reconheci o formato. Cole o JSON da IA ou linhas 'frente ; verso'.");
  return upsert(cards, origin || "texto");
}
async function importFiles(files, forcedDeck) {
  const logEl = $("#impLog"); const box = document.createElement("div"); box.className = "panel"; logEl.prepend(box);
  const log = m => { box.innerHTML += `<div>${m}</div>`; };
  for (const f of files) {
    log(`<b>📄 ${esc(f.name)}</b>`);
    try {
      let r;
      if (/\.(apkg|colpkg)$/i.test(f.name)) r = await importApkg(f, forcedDeck, log);
      else r = await importText(await f.text(), forcedDeck, log, "arquivo:" + f.name);
      log(`✅ <b class="rv">${r.novos} novos</b> · ${r.atual} atualizados (progresso mantido)`);
    } catch (e) { console.error(e); log(`❌ <span style="color:var(--red)">${esc(e.message || e)}</span>`); }
  }
  refreshHome();
}

/* ---------------- Baralho oficial (deste repositório) ---------------- */
async function loadOfficial(btn) {
  btn && (btn.disabled = true);
  try {
    const idx = await (await fetch("data/index.json", { cache: "no-cache" })).json();
    let tot = { novos: 0, atual: 0 }, i = 0;
    for (const d of idx.decks) {
      i++; btn && (btn.textContent = `⏳ ${i}/${idx.decks.length} · ${d.tema}`);
      const url = new URL(d.arquivo, location.href);
      const r = await importText(await (await fetch(url, { cache: "no-cache" })).text(), null, () => { }, "oficial", location.href);
      tot.novos += r.novos; tot.atual += r.atual;
    }
    await DB.setMeta("official", idx.versao);
    toast(`✅ Baralho oficial: <b>${tot.novos}</b> novos · ${tot.atual} atualizados`, 4000);
  } catch (e) { console.error(e); toast("❌ Não consegui baixar o baralho oficial: " + esc(e.message)); }
  refreshHome();
}

/* ---------------- Backup ---------------- */
async function blobToDataURL(b) { return new Promise(r => { const fr = new FileReader(); fr.onload = () => r(fr.result); fr.readAsDataURL(b); }); }
async function exportBackup() {
  toast("⏳ Gerando backup…");
  const media = {}; for (const m of await DB.all("media")) media[m.name] = await blobToDataURL(m.blob);
  const data = { formato: "codice360x-backup-v1", app: APP_VERSION, data: new Date().toISOString(), cards: await DB.all("cards"), styles: await DB.all("styles"), meta: await DB.all("meta"), media };
  const blob = new Blob([JSON.stringify(data)], { type: "application/json" });
  const a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = `codice360x-backup-${today()}.json`; document.body.appendChild(a); a.click(); a.remove();
  toast(`✅ Backup com ${data.cards.length} cards baixado.`);
}
async function restoreBackup(o) {
  for (const s of ["cards", "styles", "meta", "media"]) await DB.clear(s);
  await DB.putMany("cards", o.cards || []); await DB.putMany("styles", o.styles || []); await DB.putMany("meta", o.meta || []);
  const items = []; for (const [name, v] of Object.entries(o.media || {})) items.push({ name, blob: await (await fetch(v)).blob() });
  await DB.putMany("media", items);
  S.mediaURL.forEach(u => URL.revokeObjectURL(u)); S.mediaURL.clear();
  await loadAll();
}

/* ---------------- UI: Início ---------------- */
function buildTree() {
  const root = { kids: new Map() };
  for (const c of S.cards) { let node = root, path = []; for (const p of c.deck.split("::")) { path.push(p); if (!node.kids.has(p)) node.kids.set(p, { name: p, full: path.join("::"), kids: new Map() }); node = node.kids.get(p); } }
  return root;
}
const openDecks = new Set(JSON.parse(localStorageGet("openDecks") || "[]"));
function localStorageGet(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
function localStorageSet(k, v) { try { localStorage.setItem(k, v); } catch (e) { } }
function treeHTML(node) {
  const kids = [...node.kids.values()].sort((a, b) => a.name.localeCompare(b.name, "pt", { numeric: true }));
  return kids.map(k => {
    const c = counts(k.full), has = k.kids.size > 0, open = openDecks.has(k.full);
    return `<li><div class="dk" data-deck="${esc(k.full)}"><span class="tg" data-tg="${esc(k.full)}">${has ? (open ? "▾" : "▸") : "·"}</span><span class="nm">${esc(k.name)}</span>
      <span class="cnt n">${c.n || ""}</span><span class="cnt l">${c.l || ""}</span><span class="cnt rv">${c.r || ""}</span></div>
      ${has ? `<ul class="tree sub ${open ? "open" : ""}">${treeHTML(k)}</ul>` : ""}</li>`;
  }).join("");
}
async function refreshHome() {
  const all = counts(null), tot = S.cards.length, sus = S.cards.filter(c => c.susp).length;
  const mature = S.cards.filter(c => c.srs.st === "review" && c.srs.ivl >= 21).length;
  const acc = S.log.nAns ? Math.round(100 * S.log.nOk / S.log.nAns) : 0;
  $("#stats").innerHTML = `<div class="stat"><b class="n">${all.n}</b><span>novos hoje</span></div><div class="stat"><b class="rv">${all.r + all.l}</b><span>revisões pendentes</span></div>
   <div class="stat"><b>${S.log.nAns}</b><span>respondidos hoje · ${acc}% ✓</span></div><div class="stat"><b style="color:var(--gold2)">${tot}</b><span>cards · ${mature} maduros</span></div>`;
  const off = await DB.meta("official", null);
  let ver = null; try { ver = (await (await fetch("data/index.json", { cache: "no-cache" })).json()).versao; } catch (e) { }
  $("#officialBox").innerHTML = off && off === ver
    ? `<div class="row"><div class="grow">🏛️ <b>Baralho oficial TEMI 2028</b> instalado <span class="pill">${esc(off)}</span></div><button class="btn sm" id="offBtn">🔄 Reinstalar/atualizar</button></div>`
    : `<div class="row"><div class="grow">🏛️ <b>Baralho oficial TEMI 2028 — 600 cards</b> em 15 temas e 77 subtemas, com ilustrações.${off ? " <span class='pill'>nova versão disponível</span>" : ""}</div><button class="btn gold" id="offBtn">📥 ${off ? "Atualizar" : "Instalar"} baralho oficial</button></div>`;
  $("#offBtn").onclick = e => loadOfficial(e.currentTarget);
  $("#tree").innerHTML = tot ? treeHTML(buildTree()) : `<li class="empty">Nenhum card ainda. Instale o baralho oficial acima ou vá em 📥 Importar.</li>`;
  fillDeckSelects();
}
function fillDeckSelects() {
  const names = [...new Set(S.cards.flatMap(c => { const p = c.deck.split("::"); return p.map((_, i) => p.slice(0, i + 1).join("::")); }))].sort((a, b) => a.localeCompare(b, "pt", { numeric: true }));
  const opts = names.map(n => `<option value="${esc(n)}">${esc(n.replace(/[^:]+::/g, "· "))}</option>`).join("");
  $("#qDeck").innerHTML = `<option value="">Todos os baralhos</option>` + opts;
  $("#delDeck").innerHTML = `<option value="">Escolha um baralho…</option>` + opts;
}
$("#tree").addEventListener("click", e => {
  const tg = e.target.closest("[data-tg]");
  if (tg && tg.textContent !== "·") { const k = tg.dataset.tg; openDecks.has(k) ? openDecks.delete(k) : openDecks.add(k); localStorageSet("openDecks", JSON.stringify([...openDecks])); refreshHome(); return; }
  const dk = e.target.closest("[data-deck]"); if (dk) startStudy(dk.dataset.deck);
});
$("#studyAll").onclick = () => startStudy(null);

/* ---------------- UI: Estudo ---------------- */
function startStudy(prefix, ids) {
  Study.prefix = prefix; Study.ids = ids ? new Set(ids) : null; Study.seen = new Set(); Study.undo = []; Study.done = 0;
  const c = counts(prefix); Study.total = ids ? ids.length : c.n + c.l + c.r;
  location.hash = "estudar"; showCard();
}
async function showCard() {
  const c = nextCard(); Study.cur = c; Study.shown = false;
  $("#studyDeck").textContent = Study.ids ? "🔎 Estudo filtrado (resultados da busca)" : "📚 " + (Study.prefix || "Todos os baralhos");
  const cc = counts(Study.prefix);
  $("#studyCounts").innerHTML = Study.ids ? `<span class="cnt">${Study.done}/${Study.total}</span>` : `<span class="cnt n">${cc.n}</span> <span class="cnt l">${cc.l}</span> <span class="cnt rv">${cc.r}</span>`;
  $("#prog").style.width = Study.total ? Math.min(100, 100 * Study.done / Math.max(Study.total, Study.done + 1)) + "%" : "0";
  if (!c) {
    $("#cardHost").style.display = "none"; $("#studyTools").style.display = "none";
    $("#studyEmpty").style.display = "block";
    const nxt = S.cards.filter(x => !x.susp && x.srs.st !== "new" && inDeck(x, Study.prefix)).map(x => x.srs.due).sort((a, b) => a - b)[0];
    $("#studyEmpty").innerHTML = `<div style="font-size:46px">🏆</div><h2>Missão cumprida!</h2><p>Hoje: <b>${S.log.nAns}</b> respostas · <b>${S.log.nAns ? Math.round(100 * S.log.nOk / S.log.nAns) : 0}%</b> de acerto.</p>
      ${nxt ? `<p style="color:var(--mut)">Próximo card vence em <b>${fmtIvl(Math.max(MIN, nxt - Date.now()))}</b>.</p>` : ""}
      <a class="btn gold" href="#inicio">🏠 Voltar ao início</a>`;
    bars(null); return;
  }
  $("#cardHost").style.display = "block"; $("#studyTools").style.display = "flex"; $("#studyEmpty").style.display = "none";
  $("#bMark").textContent = c.marked ? "🚩 Desmarcar" : "🚩 Marcar";
  await renderInto($("#cardHost"), c.q, c.style);
  Study.t0 = Date.now(); bars("show"); window.scrollTo({ top: 0 });
}
function bars(which) {
  $("#barShow").classList.toggle("on", which === "show" && location.hash === "#estudar");
  $("#barAns").classList.toggle("on", which === "ans" && location.hash === "#estudar");
}
async function reveal() {
  const c = Study.cur; if (!c || Study.shown) return; Study.shown = true;
  await renderInto($("#cardHost"), c.a, c.style);
  const now = Date.now();
  for (let g = 1; g <= 4; g++) { const s = schedule(c.srs, g, now); $("#i" + g).textContent = fmtIvl(s.due - now); }
  bars("ans");
  const ans = $("#cardHost").shadowRoot.querySelector("#answer"); if (ans && ans.getBoundingClientRect().top > innerHeight * 0.6) ans.scrollIntoView({ behavior: "smooth", block: "start" });
}
async function answer(g) {
  const c = Study.cur; if (!c || !Study.shown) return;
  Study.undo.push({ id: c.id, srs: Object.assign({}, c.srs), log: Object.assign({}, S.log) });
  const wasNew = c.srs.st === "new", wasRev = c.srs.st === "review";
  c.srs = schedule(c.srs, g);
  if (wasNew) S.log.nNew++; if (wasRev) S.log.nRev++;
  S.log.nAns++; if (g > 1) S.log.nOk++; S.log.ms += Math.min(60000, Date.now() - Study.t0);
  Study.seen.add(c.id); if (g > 1 || Study.ids) Study.done++;
  await DB.put("cards", c); await saveLog(); showCard();
}
async function undo() {
  const u = Study.undo.pop(); if (!u) return toast("Nada para desfazer.");
  const c = S.byId.get(u.id); c.srs = u.srs; S.log = u.log; Study.done = Math.max(0, Study.done - 1);
  await DB.put("cards", c); await saveLog(); Study.cur = c; Study.shown = false;
  await renderInto($("#cardHost"), c.q, c.style); bars("show"); toast("↩️ Desfeito");
}
$("#bShow").onclick = reveal;
$$("#barAns [data-g]").forEach(b => b.onclick = () => answer(+b.dataset.g));
$("#bUndo").onclick = undo;
$("#bEnd").onclick = () => { location.hash = "inicio"; };
$("#bSusp").onclick = async () => { const c = Study.cur; if (!c) return; c.susp = true; await DB.put("cards", c); toast("⏸️ Suspenso (reative em 🔎 Buscar → is:suspenso)"); showCard(); };
$("#bMark").onclick = async () => { const c = Study.cur; if (!c) return; c.marked = !c.marked; await DB.put("cards", c); $("#bMark").textContent = c.marked ? "🚩 Desmarcar" : "🚩 Marcar"; toast(c.marked ? "🚩 Marcado" : "Desmarcado"); };
document.addEventListener("keydown", e => {
  if (location.hash !== "#estudar" || /input|textarea|select/i.test(e.target.tagName)) return;
  if ((e.code === "Space" || e.key === "Enter") && !Study.shown) { e.preventDefault(); reveal(); }
  else if (Study.shown && ["1", "2", "3", "4"].includes(e.key)) answer(+e.key);
  else if (Study.shown && (e.code === "Space" || e.key === "Enter")) { e.preventDefault(); answer(3); }
  else if (e.key === "z" || e.key === "Z") undo();
  else if (e.key === "m" || e.key === "M") $("#bMark").click();
  else if (e.key === "s" || e.key === "S") $("#bSusp").click();
});

/* ---------------- UI: Buscar ---------------- */
let lastResults = [];
function search() {
  const raw = $("#q").value.trim(), deckSel = $("#qDeck").value;
  const terms = [], filt = { tag: [], deck: [], is: [] };
  (raw.match(/"[^"]+"|'[^']+'|\S+/g) || []).forEach(t => {
    const m = t.match(/^(tag|deck|is):(.+)$/i);
    if (m) filt[m[1].toLowerCase()].push(m[2].toLowerCase()); else terms.push(t.replace(/^["']|["']$/g, "").toLowerCase());
  });
  const now = Date.now(), eod = endOfDay();
  const norm = s => s.normalize("NFD").replace(/[̀-ͯ]/g, "");
  const nterms = terms.map(norm);
  const res = S.cards.filter(c => {
    if (deckSel && !inDeck(c, deckSel)) return false;
    if (filt.deck.some(d => !norm(c.deck.toLowerCase()).includes(norm(d)))) return false;
    if (filt.tag.some(t => !c.tags.some(x => x.toLowerCase().includes(t)))) return false;
    for (const i of filt.is) {
      if (i === "new" && c.srs.st !== "new") return false;
      if (i === "due" && !(c.srs.st !== "new" && c.srs.due <= eod)) return false;
      if (i === "marcado" && !c.marked) return false;
      if (i === "suspenso" && !c.susp) return false;
      if (i === "dificil" && c.srs.lapses < 3) return false;
    }
    if (nterms.length) { const t = norm(c.txt || ""); if (!nterms.every(x => t.includes(x))) return false; }
    return true;
  });
  lastResults = res;
  $("#qInfo").textContent = `${res.length} card(s)` + (res.length > 150 ? " — mostrando 150" : "");
  $("#qRes").innerHTML = res.slice(0, 150).map(c => `<div class="res" data-id="${esc(c.id)}"><div class="hd"><div class="q">${esc(strip(c.q).slice(0, 180))}</div>
    <span class="pill">${c.srs.st === "new" ? "novo" : c.srs.st === "review" ? fmtIvl(c.srs.ivl * DAY) : "aprendendo"}</span>${c.marked ? "🚩" : ""}${c.susp ? "⏸️" : ""}</div>
    <div class="bd"><div style="font-size:12px;color:var(--mut);margin-bottom:6px">📚 ${esc(c.deck)}</div><div class="host"></div>
    <div class="row" style="margin-top:8px"><button class="btn sm" data-act="susp">${c.susp ? "▶️ Reativar" : "⏸️ Suspender"}</button><button class="btn sm" data-act="mark">${c.marked ? "Desmarcar" : "🚩 Marcar"}</button>
    <button class="btn sm" data-act="reset">♻️ Reiniciar</button><button class="btn sm danger" data-act="del">🗑️ Apagar</button></div></div></div>`).join("");
}
let qT; $("#q").addEventListener("input", () => { clearTimeout(qT); qT = setTimeout(search, 180); });
$("#qDeck").addEventListener("change", search);
$("#qRes").addEventListener("click", async e => {
  const box = e.target.closest(".res"); if (!box) return; const c = S.byId.get(box.dataset.id);
  const act = e.target.closest("[data-act]")?.dataset.act;
  if (!act) { if (e.target.closest(".hd")) { box.classList.toggle("open"); if (box.classList.contains("open")) renderInto($(".host", box), c.a, c.style); } return; }
  if (act === "susp") c.susp = !c.susp;
  if (act === "mark") c.marked = !c.marked;
  if (act === "reset") c.srs = newSRS();
  if (act === "del") { if (box.dataset.confirm !== "1") { box.dataset.confirm = "1"; e.target.textContent = "Confirmar?"; return; } await DB.delMany("cards", [c.id]); S.cards = S.cards.filter(x => x.id !== c.id); S.byId.delete(c.id); box.remove(); toast("🗑️ Apagado"); return; }
  await DB.put("cards", c); search();
});
$("#qStudy").onclick = () => { if (!lastResults.length) return toast("Faça uma busca primeiro."); startStudy(null, lastResults.filter(c => !c.susp).map(c => c.id)); };

/* ---------------- UI: Importar ---------------- */
const drop = $("#drop"), fileIn = $("#file");
drop.onclick = () => fileIn.click();
fileIn.onchange = () => { importFiles([...fileIn.files], null); fileIn.value = ""; };
["dragenter", "dragover"].forEach(ev => drop.addEventListener(ev, e => { e.preventDefault(); drop.classList.add("hov"); }));
["dragleave", "drop"].forEach(ev => drop.addEventListener(ev, e => { e.preventDefault(); drop.classList.remove("hov"); }));
drop.addEventListener("drop", e => importFiles([...e.dataTransfer.files], null));
$("#pasteGo").onclick = async () => {
  const t = $("#paste").value; if (!t.trim()) return toast("Cole o texto primeiro.");
  const deck = $("#pasteDeck").value.trim() || null;
  const box = document.createElement("div"); box.className = "panel"; $("#impLog").prepend(box);
  try { const r = await importText(t, deck, m => box.innerHTML += `<div>${m}</div>`, "colado"); box.innerHTML += `<div>✅ <b class="rv">${r.novos} novos</b> · ${r.atual} atualizados</div>`; $("#paste").value = ""; refreshHome(); }
  catch (e) { box.innerHTML += `<div>❌ <span style="color:var(--red)">${esc(e.message)}</span></div>`; }
};

/* ---------------- UI: Prompt IA ---------------- */
const TEMAS = ["01 🦠 Sepse e Choque Séptico", "02 🫁 Ventilação Mecânica e SDRA", "03 ❤️ Hemodinâmica e Choque", "04 ⚗️ Distúrbios Ácido-Base", "05 🧂 Eletrólitos", "06 🫘 Rim, LRA e TRS", "07 🧠 Neurointensivismo", "08 😴 Sedação, Analgesia e Delirium", "09 ⚡ Cardiointensivismo e PCR", "10 🧫 Infecção e Antimicrobianos", "11 🩸 Hematologia, Coagulação e Transfusão", "12 🍬 Endocrinologia no Crítico", "13 🫃 Gastro, Fígado e Nutrição", "14 🚑 Trauma, Toxicologia e Ambiental", "15 ⚖️ Ética, Escores, Qualidade e POCUS", "16 ➕ Extras / Outro tema"];
$("#pTema").innerHTML = TEMAS.map(t => `<option>${t}</option>`).join("");
function buildPrompt() {
  const tema = $("#pTema").value, sub = $("#pSub").value.trim() || "(subtemas variados dentro do tema)", n = $("#pN").value, nivel = $("#pNivel").value, tipo = $("#pTipo").value, img = $("#pImg").value === "1", mat = $("#pMat").value.trim();
  const estilo = tipo === "cloze" ? "TODOS os cards em formato de lacuna (cloze): em \"frente\" escreva a frase com {{c1::termo}} (pode usar c2, c3 na mesma frase); \"verso\" traz o complemento/explicação." :
    tipo === "basico" ? "Todos os cards no formato pergunta → resposta." : "Maioria pergunta → resposta; cerca de 1 em cada 4 no formato lacuna (cloze) com {{c1::termo}} na \"frente\".";
  return `Você é um gerador de flashcards de alta qualidade para o app CÓDICE 360X (estudo para a prova de título TEMI/AMIB em Medicina Intensiva e R3 de Clínica Médica).

🎯 TAREFA
Crie exatamente ${n} flashcards sobre: ${tema.replace(/^\d+\s*\S+\s*/, "")} › ${sub}.
Nível: ${nivel}. Idioma: português do Brasil.
${mat ? `\n📄 MATERIAL-BASE (use APENAS este conteúdo como fonte factual; não acrescente dados que não estejam nele):\n"""\n${mat}\n"""\n` : ""}
✅ REGRAS DE CONTEÚDO
1. Um conceito por card. Pergunta direta e específica (critério, corte numérico, dose, conduta, droga de escolha, contraindicação, ensaio clínico marcante, pegadinha de prova).
2. Baseie-se em diretrizes atuais e ensaios clínicos de referência. Preencha "fonte" com a referência curta (ex.: "SSC 2021", "KDIGO 2012", "PROSEVA NEJM 2013"). NUNCA invente referência, dose ou número; na dúvida, não crie o card.
3. ${estilo}
4. "verso": curto e escaneável (≤ 60 palavras OU uma tabela pequena). Comece com 1 emoji. Use <b>negrito</b> nos números-chave e as cores: <b class=r>perigo/erro</b>, <b class=g>alvo/correto</b>, <b class=y>atenção</b>, <b class=c>destaque</b>.
5. Tabelas em HTML simples: <table class=t><tr><th>A</th><th>B</th></tr><tr><td>..</td><td>..</td></tr></table>. Listas: <ul><li>..</li></ul>. Quebra de linha: <br>.
6. "pegadinha": 1 frase com a pegadinha de prova, o erro comum ou uma curiosidade nerd.
7. "subtema": nome curto do subtema (3–5 palavras) para organizar o baralho.
8. "tags": 2–4 palavras-chave sem espaços (ex.: "vasopressor", "SSC2021").
${img ? `9. "imagem": quando um esquema visual ajudar MUITO (curva, algoritmo, escala, comparação), desenhe um SVG inline simples: <svg viewBox="0 0 600 300" xmlns="http://www.w3.org/2000/svg">…</svg>, fundo transparente, textos em fill="#e8e6df" font-size 16–20, cores #4dd4ff #d4af37 #ff6b6b #5be38a, sem <script>, sem imagens externas. No máximo 1 SVG a cada 5 cards; nos demais deixe "imagem": "".` : `9. "imagem": deixe sempre "".`}

📦 FORMATO DE SAÍDA (obrigatório)
Responda SOMENTE com um único bloco \`\`\`json válido, sem nenhum texto antes ou depois, exatamente nesta estrutura:
\`\`\`json
{
  "formato": "codice360x-v1",
  "baralho": "TEMI 2028::${tema.replace(/"/g, "")}",
  "cards": [
    {
      "subtema": "…",
      "frente": "…",
      "verso": "…",
      "pegadinha": "…",
      "fonte": "…",
      "tags": ["…", "…"],
      "imagem": ""
    }
  ]
}
\`\`\`
Use aspas duplas, escape aspas internas com \\", sem vírgula sobrando no fim. Atributos HTML sem aspas (ex.: class=t) para não quebrar o JSON.
Se a resposta ficar longa demais, entregue em partes de no máximo 25 cards, cada parte como um bloco JSON completo, e avise "Parte 1/2".`;
}
function updPrompt() { $("#pOut").textContent = buildPrompt(); }
["#pTema", "#pSub", "#pN", "#pNivel", "#pTipo", "#pImg", "#pMat"].forEach(s => $(s).addEventListener("input", updPrompt));
$("#pCopy").onclick = async () => {
  const t = buildPrompt();
  try { await navigator.clipboard.writeText(t); toast("📋 Prompt copiado! Cole na IA."); }
  catch (e) { const r = document.createRange(); r.selectNodeContents($("#pOut")); const s = getSelection(); s.removeAllRanges(); s.addRange(r); toast("Selecionei o texto — use Copiar do sistema."); }
};

/* ---------------- UI: Ajustes ---------------- */
function fillSettings() {
  const s = S.settings; $("#sNew").value = s.newPerDay; $("#sRev").value = s.revPerDay; $("#sSteps").value = s.steps.join(" "); $("#sGrad").value = s.grad + " " + s.easy;
  $("#aboutBox").innerHTML = `CÓDICE 360X v${APP_VERSION} · ${S.cards.length} cards neste aparelho · Repetição espaçada estilo Anki (SM-2).<br>Código aberto em <a href="https://github.com/aldenirfilho/intensivahub/tree/main/flashcards" target="_blank" rel="noopener">github.com/aldenirfilho/intensivahub</a>. Conteúdo educativo — não substitui julgamento clínico nem diretrizes institucionais.`;
}
$("#sSave").onclick = async () => {
  const nums = s => s.split(/[\s,;]+/).map(Number).filter(x => x > 0);
  const g = nums($("#sGrad").value);
  Object.assign(S.settings, { newPerDay: Math.max(0, +$("#sNew").value || 0), revPerDay: Math.max(0, +$("#sRev").value || 0), steps: nums($("#sSteps").value).length ? nums($("#sSteps").value) : [1, 10], grad: g[0] || 1, easy: g[1] || 4 });
  const { newPerDay, revPerDay, steps, grad, easy } = S.settings;
  await DB.setMeta("settings", { newPerDay, revPerDay, steps, grad, easy }); toast("💾 Ajustes salvos"); refreshHome();
};
$("#bkExp").onclick = exportBackup;
$("#bkImp").onclick = () => $("#bkFile").click();
$("#bkFile").onchange = async () => { const f = $("#bkFile").files[0]; if (!f) return; try { await restoreBackup(JSON.parse(await f.text())); toast("🛟 Backup restaurado"); refreshHome(); fillSettings(); } catch (e) { toast("❌ " + esc(e.message)); } };
function confirmAction(msg, fn) {
  $("#confirmBox").innerHTML = `<div class="panel" style="border-color:var(--red)">${msg}<div class="row" style="margin-top:8px"><button class="btn danger" id="cfYes">Sim, confirmar</button><button class="btn" id="cfNo">Cancelar</button></div></div>`;
  $("#cfNo").onclick = () => $("#confirmBox").innerHTML = "";
  $("#cfYes").onclick = async () => { $("#confirmBox").innerHTML = ""; await fn(); refreshHome(); fillSettings(); };
}
$("#delGo").onclick = () => { const d = $("#delDeck").value; if (!d) return; const ids = S.cards.filter(c => inDeck(c, d)).map(c => c.id);
  confirmAction(`Apagar <b>${ids.length}</b> cards de <b>${esc(d)}</b>?`, async () => { await DB.delMany("cards", ids); const set = new Set(ids); S.cards = S.cards.filter(c => !set.has(c.id)); ids.forEach(i => S.byId.delete(i)); toast("🗑️ Baralho apagado"); }); };
$("#resetProg").onclick = () => confirmAction("Zerar o progresso de <b>todos</b> os cards?", async () => { S.cards.forEach(c => c.srs = newSRS()); await DB.putMany("cards", S.cards); toast("♻️ Progresso zerado"); });
$("#wipe").onclick = () => confirmAction("Apagar <b>tudo</b> (cards, imagens, progresso)? Faça um backup antes.", async () => { for (const s of ["cards", "styles", "meta", "media"]) await DB.clear(s); await loadAll(); toast("💣 Tudo apagado"); });

/* ---------------- Roteamento ---------------- */
function route() {
  const v = (location.hash || "#inicio").slice(1);
  const valid = ["inicio", "estudar", "buscar", "importar", "prompt", "ajustes"];
  const view = valid.includes(v) ? v : "inicio";
  $$(".view").forEach(s => s.classList.toggle("on", s.id === "v-" + view));
  $$("#nav a").forEach(a => a.classList.toggle("on", a.dataset.v === view));
  if (view === "inicio") refreshHome();
  if (view === "estudar") { if (!Study.cur && Study.prefix === null && !Study.ids && !Study.started) { Study.started = true; startStudy(null); return; } bars(Study.cur ? (Study.shown ? "ans" : "show") : null); }
  else bars(null);
  if (view === "buscar") search();
  if (view === "prompt") updPrompt();
  if (view === "ajustes") fillSettings();
}
window.addEventListener("hashchange", route);

(async function init() {
  try { await DB.open(); await loadAll(); }
  catch (e) { document.querySelector("main").innerHTML = `<div class="panel">❌ Este navegador bloqueou o armazenamento local (modo privado?). Abra em uma aba normal.<br><small>${esc(e.message || e)}</small></div>`; return; }
  route();
  if (window.__selftest) window.__selftest();
})();
