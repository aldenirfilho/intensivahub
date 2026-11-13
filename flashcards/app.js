/* CÓDICE 360X · Flashcards v2
   - Coleções oficiais (TEMI 2028 + R3 Clínica Médica) carregadas dos arquivos do app
   - Cards do usuário + progresso em IndexedDB (cache local) e, numa página do Claude, sincronizados
     automaticamente na nuvem do artifact (db por usuário) — mesmo login = mesmo progresso em todos os aparelhos.
   - Fora do Claude (GitHub Pages, iPhone/computador): sincroniza por um Gist secreto do GitHub (Hub) com a mesma chave em todos os aparelhos.
   - Ponte copiar/colar junta o progresso entre o app do GitHub e a página do Claude.
   - Importa .apkg (Anki legado e 2.1.50+), JSON de qualquer IA e TXT/CSV. */
"use strict";
const APP_VERSION = "4.9.0";
const DAY = 86400000, MIN = 60000;
const $ = (s, el = document) => el.querySelector(s);
const $$ = (s, el = document) => [...el.querySelectorAll(s)];
const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const strip = h => String(h || "").replace(/<style[\s\S]*?<\/style>/gi, "").replace(/<svg[\s\S]*?<\/svg>/gi, " ").replace(/<[^>]+>/g, " ").replace(/&nbsp;/g, " ").replace(/&[a-z]+;/gi, " ").replace(/\s+/g, " ").trim();
const dayKey = (t = Date.now()) => { const d = new Date(t); return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0"); };
const today = () => dayKey();
const endOfDay = () => { const d = new Date(); d.setHours(23, 59, 59, 999); return d.getTime(); };
function hash(str) { let h1 = 0xdeadbeef, h2 = 0x41c6ce57; for (let i = 0; i < str.length; i++) { const c = str.charCodeAt(i); h1 = Math.imul(h1 ^ c, 2654435761); h2 = Math.imul(h2 ^ c, 1597334677); } h1 = Math.imul(h1 ^ (h1 >>> 16), 2246822507) ^ Math.imul(h2 ^ (h2 >>> 13), 3266489909); h2 = Math.imul(h2 ^ (h2 >>> 16), 2246822507) ^ Math.imul(h1 ^ (h1 >>> 13), 3266489909); return (h2 >>> 0).toString(36) + (h1 >>> 0).toString(36); }
function hnum(str) { let h = 2166136261; for (let i = 0; i < str.length; i++) { h ^= str.charCodeAt(i); h = Math.imul(h, 16777619); } return h >>> 0; }
function toast(msg, ms = 2600) { const t = $("#toast"); t.innerHTML = msg; t.style.display = "block"; clearTimeout(toast._t); toast._t = setTimeout(() => t.style.display = "none", ms); }
const lsGet = k => { try { return localStorage.getItem(k); } catch (e) { return null; } };
const lsSet = (k, v) => { try { localStorage.setItem(k, v); } catch (e) { } };

/* ---------------- Cores por tema ---------------- */
const PAL = ["#4dd4ff", "#5be38a", "#ff6b6b", "#b48cff", "#ffc14d", "#ff8a3d", "#f06bd0", "#2dd4bf", "#ffd166", "#7aa2ff", "#e85d75", "#a3e635", "#38bdf8", "#f59e0b", "#c084fc"];
function accentFor(deck) {
  const p = String(deck || "").split("::"), m = (p[1] || "").match(/^(\d{1,2})\s/);
  if (!m) return PAL[hnum(p[0] || "") % PAL.length];
  const n = +m[1] - 1, off = /cl[ií]nica/i.test(p[0]) ? 7 : 0;
  return PAL[(n + off) % PAL.length];
}
const CODICE_CSS = `.card{--acc:#4dd4ff;font-family:Inter,-apple-system,"Segoe UI",Roboto,sans-serif;font-size:19px;line-height:1.5;text-align:left;color:#ece9e1;background:radial-gradient(600px 220px at 100% 0%,color-mix(in srgb,var(--acc) 14%,transparent),transparent 70%),#0e1116;padding:14px 16px;border-radius:14px;border:1px solid color-mix(in srgb,var(--acc) 35%,#2a3442);overflow-x:auto}
.tema{display:inline-block;font-size:13px;color:#0e1116;background:linear-gradient(90deg,var(--acc),#f3d77a);padding:3px 10px;border-radius:12px;font-weight:700;margin-bottom:10px}
.q{font-size:22px;font-weight:600;color:#fff;border-left:4px solid var(--acc);padding-left:10px}
hr#answer{border:0;height:2px;background:linear-gradient(90deg,#d4af37,var(--acc),transparent);margin:14px 0}
.a{background:#151b23;border:1px solid #2a3442;border-left:4px solid var(--acc);border-radius:10px;padding:12px 14px}
b{color:#fff}.r{color:#ff6b6b!important}.g{color:#5be38a!important}.y{color:#ffc14d!important}.c{color:#4dd4ff!important}
table.t{color:#ece9e1;border-collapse:collapse;width:100%;margin:8px 0;font-size:16px;border-radius:8px;overflow:hidden}
table.t th{background:color-mix(in srgb,var(--acc) 22%,#141b24);color:#fff;padding:7px 8px;border:1px solid #33414f;text-align:left}
table.t td{color:#ece9e1;padding:6px 8px;border:1px solid #2a3442;vertical-align:top}
table.t tr:nth-child(even) td{background:#121820}
table.t td:first-child{font-weight:600;color:color-mix(in srgb,var(--acc) 55%,#fff)}
ul{margin:6px 0;padding-left:22px}li{margin:3px 0}li::marker{color:var(--acc)}
img,svg{max-width:100%;height:auto}
.img{margin-top:12px;text-align:center}.img img,.img svg{max-width:100%;height:auto;border-radius:10px;border:1px solid #2a3442}
.peg{margin-top:12px;background:#2a2210;border-left:4px solid #ffc14d;border-radius:8px;padding:10px 12px;font-size:16px;color:#ffe9b8}
.src{margin-top:10px;font-size:13px;color:#8a94a3}
.cloze{color:var(--acc);font-weight:700;border-bottom:2px dotted var(--acc)}
.pill{display:inline-block;font-size:12px;padding:2px 8px;border-radius:20px;background:color-mix(in srgb,var(--acc) 25%,#1d2a36);color:#fff;margin-right:6px;vertical-align:2px}
.teaching-img{max-width:100%;border-radius:10px}.imgcap{font-size:12px;color:#8a94a3;text-align:center}
@media(max-width:560px){.card{font-size:17px;padding:12px}.q{font-size:19px}table.t{font-size:14px}}`;
const CODICE_LIGHT = `.card{color:#322d20;background:radial-gradient(600px 220px at 100% 0%,color-mix(in srgb,var(--acc) 14%,transparent),transparent 70%),#f8f9fa;border:1px solid color-mix(in srgb,var(--acc) 35%,#f0f2f5)}.tema{color:#f8f9fa;background:linear-gradient(90deg,var(--acc),#8c6f0d)}.q{color:#292929}hr#answer{background:linear-gradient(90deg,#a68824,var(--acc),transparent)}.a{background:#f6f7f9;border:1px solid #f0f2f5}b{color:#292929}.r{color:#990000!important}.g{color:#16833c!important}.y{color:#996400!important}.c{color:#007499!important}table.t{color:#322d20}table.t th{background:color-mix(in srgb,var(--acc) 22%,#f5f7f9);color:#292929;border:1px solid #eef1f4}table.t td{color:#322d20;border:1px solid #f0f2f5}table.t tr:nth-child(even) td{background:#f6f8fa}table.t td:first-child{color:color-mix(in srgb,var(--acc) 55%,#292929)}.img img,.img svg{border:1px solid #f0f2f5}.peg{background:#faf8f4;border-left:4px solid #996400;color:#996a00}.src{color:#4a525e}.pill{background:color-mix(in srgb,var(--acc) 25%,#f2f5f8);color:#292929}.imgcap{color:#4a525e}`;   // gerado por tools/theme/build_light.py (tema claro dos cards)
const isLight = () => document.documentElement.classList.contains("light");

/* ---------------- IndexedDB (cache local) ---------------- */
const DB = {
  db: null,
  open() {
    return new Promise((res, rej) => {
      let r; try { r = indexedDB.open("codice360x", 2); } catch (e) { return rej(e); }
      r.onupgradeneeded = (ev) => {
        const d = r.result, tx = r.transaction;
        for (const s of ["user", "prog", "media", "styles", "meta"]) if (!d.objectStoreNames.contains(s)) d.createObjectStore(s, { keyPath: s === "media" ? "name" : s === "meta" ? "k" : "id" });
        if (ev.oldVersion === 1 && d.objectStoreNames.contains("cards")) { // migração da v1
          tx.objectStore("cards").openCursor().onsuccess = e => {
            const cur = e.target.result; if (!cur) { d.deleteObjectStore("cards"); return; }
            const c = cur.value, mod = Date.now();
            if (c.srs && c.srs.reps) tx.objectStore("prog").put({ id: c.id, s: c.srs, susp: !!c.susp, mk: !!c.marked, mod });
            if (c.origin !== "oficial") tx.objectStore("user").put({ id: c.id, deck: c.deck, q: c.q, a: c.a, style: c.style || "codice", tags: c.tags || [], mod, created: c.created || mod });
            cur.continue();
          };
        }
      };
      r.onsuccess = () => { DB.db = r.result; res(); };
      r.onerror = () => rej(r.error);
    });
  },
  tx(store, mode = "readonly") { return DB.db.transaction(store, mode).objectStore(store); },
  all(store) { return new Promise((res, rej) => { const q = DB.tx(store).getAll(); q.onsuccess = () => res(q.result); q.onerror = () => rej(q.error); }); },
  get(store, key) { return new Promise((res, rej) => { const q = DB.tx(store).get(key); q.onsuccess = () => res(q.result); q.onerror = () => rej(q.error); }); },
  putMany(store, items) { return new Promise((res, rej) => { if (!items.length) return res(); const t = DB.db.transaction(store, "readwrite"), s = t.objectStore(store); items.forEach(i => s.put(i)); t.oncomplete = () => res(); t.onerror = () => rej(t.error); }); },
  put(store, item) { return DB.putMany(store, [item]); },
  delMany(store, keys) { return new Promise((res, rej) => { if (!keys.length) return res(); const t = DB.db.transaction(store, "readwrite"), s = t.objectStore(store); keys.forEach(k => s.delete(k)); t.oncomplete = () => res(); t.onerror = () => rej(t.error); }); },
  clear(store) { return new Promise((res, rej) => { const q = DB.tx(store, "readwrite").clear(); q.onsuccess = () => res(); q.onerror = () => rej(q.error); }); },
  async meta(k, def) { const r = await DB.get("meta", k); return r ? r.v : def; },
  setMeta(k, v) { return DB.put("meta", { k, v }); },
};

/* ---------------- Estado ---------------- */
const DEFAULTS = { newPerDay: 20, revPerDay: 300, steps: [1, 10], relearn: [10], grad: 1, easy: 4, startEase: 2.5, maxIvl: 3650, learnAhead: 20, cols: { temi: true, cm: true, ia: true } };
const S = { cards: [], byId: new Map(), official: [], user: new Map(), prog: new Map(), styles: new Map(), mediaURL: new Map(), mediaPath: {}, settings: null, settingsMod: 0, logs: {}, index: null };
const emptyLog = () => ({ nNew: 0, nRev: 0, nAns: 0, nOk: 0, ms: 0 });
const L0 = () => (S.logs[today()] = S.logs[today()] || emptyLog());
/* ---------- XP · níveis · registro de atividade (sincroniza junto com os logs) ---------- */
const act = l => !l ? 0 : (l.nAns === undefined && !l.xp ? Object.keys(l).length : (l.nAns || 0) + (l.qN || 0) + (l.mN || 0) + (l.nN || 0) + (l.sims || []).length + (l.xp || 0) / 1000);
const dayLogs = () => Object.entries(S.logs).filter(([k]) => /^\d/.test(k));
const QRES = () => (S.logs._q = S.logs._q || {}), MRES = () => (S.logs._m = S.logs._m || {}), NRES = () => (S.logs._n = S.logs._n || {});
const RANKS = ["🪶 Aprendiz", "🛡️ Escudeiro", "⚔️ Cavaleiro", "🏰 Paladino", "📜 Mestre", "👑 Grão-Mestre", "🐉 Lenda"];
function xpTotal() { return dayLogs().reduce((s, [, l]) => s + (l.xp || 0), 0); }
function levelOf(xp) { let lv = 1, need = 100, acc = 0; while (xp >= acc + need) { acc += need; lv++; need = 100 + 50 * (lv - 1); } return { lv, cur: xp - acc, need, rank: RANKS[Math.min(RANKS.length - 1, Math.floor((lv - 1) / 5))] }; }
function xpBadge() { const el = $("#xpBadge"); if (!el) return; const t = xpTotal(), L = levelOf(t), d = (S.logs[today()] || {}).xp || 0; el.innerHTML = `<b>${L.rank} · Nv ${L.lv}</b><span class="xpTrack"><i style="width:${Math.round(100 * L.cur / L.need)}%"></i></span><small>${t.toLocaleString("pt-BR")} XP · hoje +${d}</small>`; el.title = `Faltam ${L.need - L.cur} XP para o nível ${L.lv + 1}`; }
function addXP(n, why, src) {
  if (!n) return; const L = L0(), before = levelOf(xpTotal()).lv; L.xp = (L.xp || 0) + n; L.xs = L.xs || {}; L.xs[src || "c"] = (L.xs[src || "c"] || 0) + n; xpBadge();
  clearTimeout(addXP._t); addXP._t = setTimeout(() => ACH.check(), 400);
  const pop = $("#xpPop"); if (pop) { pop.textContent = `+${n} XP${why ? " · " + why : ""}`; pop.classList.remove("go"); void pop.offsetWidth; pop.classList.add("go"); }
  const after = levelOf(xpTotal()); if (after.lv > before) toast(`🎉 Subiu para o nível ${after.lv} — ${after.rank}!`, 4000);
}
function addSim(rec) { const L = L0(); (L.sims = L.sims || []).push(Object.assign({ t: Date.now() }, rec)); }
const limNew = L => S.settings.newPerDay + (L.xNew || 0), limRev = L => S.settings.revPerDay + (L.xRev || 0);
function metaBarHTML(compact) {
  const L = L0(), ln = limNew(L), lr = limRev(L), pn = ln ? Math.min(100, 100 * L.nNew / ln) : 100, pr = lr ? Math.min(100, 100 * L.nRev / lr) : 100;
  const col = p => p >= 100 ? "var(--ok,#5be38a)" : p >= 80 ? "var(--gold2)" : "var(--cy)";
  const b = (ic, lb, v, lim, pc) => `<div class="mbItem"><div class="mbLbl">${ic} ${lb} <b>${v}</b>/${lim}${pc >= 100 ? " ✅" : ""}</div><div class="mbTrack"><i style="width:${pc}%;background:${col(pc)}"></i></div></div>`;
  return `<div class="metaBar${compact ? " compact" : ""}">${compact ? "" : `<div class="mbHead">🎯 <b>Meta de hoje</b> <a href="#" class="mbEdit" data-medit="1">✏️ editar</a></div>`}<div class="mbRow">${b("🆕", "Novos", L.nNew, ln, pn)}${b("🔁", "Revisões", L.nRev, lr, pr)}</div></div>`;
}
function metaWarn() {
  const L = L0(), ln = limNew(L), lr = limRev(L); let msg = "";
  if (ln && !L.w80n && L.nNew >= Math.ceil(0.8 * ln) && L.nNew < ln) { L.w80n = 1; msg = `🔔 80% da meta de novos (${L.nNew}/${ln})`; }
  if (lr >= 10 && !L.w80r && L.nRev >= Math.ceil(0.8 * lr) && L.nRev < lr) { L.w80r = 1; msg = msg ? msg + " · " : ""; msg += `🔔 80% da meta de revisões (${L.nRev}/${lr})`; }
  if (msg) toast(msg + " — ao chegar em 100% você pode ampliar.", 3800);
}

/* ---------------- Repetição espaçada (SM-2 estilo Anki) ---------------- */
function newSRS() { return { st: "new", due: 0, ivl: 0, ease: S.settings?.startEase || 2.5, reps: 0, lapses: 0, step: 0 }; }
function schedule(srs, g, now = Date.now()) {
  const st = S.settings, o = Object.assign({}, srs);
  const fuzz = d => d < 3 ? d : Math.round(d * (0.95 + Math.random() * 0.1));
  const toReview = ivl => { o.st = "review"; o.ivl = Math.min(st.maxIvl, Math.max(1, ivl)); o.due = now + fuzz(o.ivl) * DAY; o.step = 0; };
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
    else if (g === 2) o.due = now + steps[o.step] * 1.5 * MIN;
    else if (g === 3) { if (o.step + 1 >= steps.length) toReview(o.ivl || 1); else { o.step++; o.due = now + steps[o.step] * MIN; } }
    else toReview((o.ivl || 1) + 1);
  } else {
    const ivl = o.ivl || 1;
    if (g === 1) { o.lapses++; o.ease = Math.max(1.3, o.ease - 0.2); o.ivl = 1; o.st = "relearn"; o.step = 0; o.due = now + (st.relearn[0] || 10) * MIN; }
    else if (g === 2) { o.ease = Math.max(1.3, o.ease - 0.15); toReview(Math.max(ivl + 1, Math.round(ivl * 1.2))); }
    else if (g === 3) toReview(Math.max(ivl + 1, Math.round(ivl * o.ease)));
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

/* ---------------- Nuvem (página do Claude) ---------------- */
const NP = 32, NU = 48;
const shardP = id => "p" + String(hnum(id) % NP).padStart(2, "0");
const shardU = id => "u" + String(hnum(id) % NU).padStart(2, "0");
const ST = { new: "n", learn: "l", review: "r", relearn: "rl" }, STR = { n: "new", l: "learn", r: "review", rl: "relearn" };
const encP = p => [ST[p.s.st] || "n", Math.round(p.s.due), p.s.ivl, Math.round(p.s.ease * 100) / 100, p.s.reps, p.s.lapses, p.s.step, p.susp ? 1 : 0, p.mk ? 1 : 0, p.mod, p.hl && p.hl.length ? p.hl : 0];
const decP = (id, a) => ({ id, s: { st: STR[a[0]] || "new", due: a[1], ivl: a[2], ease: a[3], reps: a[4], lapses: a[5], step: a[6] }, susp: !!a[7], mk: !!a[8], mod: a[9], hl: Array.isArray(a[10]) ? a[10] : [] });
const Cloud = {
  db: null, col: null, uid: null, assets: null, dl: null, on: false, busy: false, timer: null, lastSync: 0, err: "", mediaMap: {},
  dirty: { p: new Set(), u: new Set(), st: false, media: false },
  setStatus(kind, txt) { const el = $("#sync"); if (!el) return; el.className = "sync " + kind; el.textContent = txt; },
  async init() {
    if (!window.claude || typeof window.claude.use !== "function") { this.setStatus("", "💾 Só neste aparelho"); return; }
    this.setStatus("busy", "⏳ Conectando…");
    try {
      const [user, db] = await Promise.all([claude.use("user"), claude.use("db")]);
      this.dl = await claude.use("downloads").catch(() => null);
      if (!user || !db) { this.setStatus("", "💾 Só neste aparelho"); return; }
      const uid = await user.id();
      if (!uid) { this.setStatus("", "💾 Entre na conta para sincronizar"); return; }
      this.uid = uid; this.db = db; this.col = db.collection("data/users/" + uid);
      this.assets = await claude.use("assets").catch(() => null);
      const snap = await Promise.race([this.col.get(), new Promise((_, r) => setTimeout(() => r(new Error("tempo esgotado")), 15000))]);
      const seen = { p: new Map(), u: new Map() };
      for (const d of snap.docs) this.applyDoc(d.id, d.data(), seen);
      // o que existe localmente e está mais novo/ausente na nuvem → enviar
      for (const p of S.prog.values()) if ((seen.p.get(p.id) || 0) < p.mod) this.dirty.p.add(shardP(p.id));
      for (const u of S.user.values()) if ((seen.u.get(u.id) || 0) < u.mod) this.dirty.u.add(shardU(u.id));
      if (!snap.docs.some(d => d.id === "state")) this.dirty.st = true;
      this.on = true; this.lastSync = Date.now();
      rebuildCards(); rerender();
      this.unsub = this.col.onSnapshot(qs => {
        let changed = false;
        for (const ch of qs.docChanges()) { if (ch.type === "removed" || ch.doc.metadata.hasPendingWrites) continue; if (this.applyDoc(ch.doc.id, ch.doc.data(), null)) changed = true; }
        if (changed) { rebuildCards(); if (location.hash !== "#estudar") rerender(); }
        this.lastSync = Date.now(); if (!this.busy) this.setStatus("ok", "☁️ Sincronizado");
      }, e => { this.err = e.code || String(e); this.setStatus("err", "⚠️ Sync pausado"); });
      this.setStatus("ok", "☁️ Sincronizado");
      this.schedule(500);
    } catch (e) { console.warn("nuvem", e); this.err = e.code || e.message || String(e); this.setStatus("err", "⚠️ Sem nuvem (local)"); }
  },
  /* aplica um documento remoto ao estado local; retorna true se mudou algo */
  applyDoc(id, data, seen) {
    if (!data) return false; let changed = false;
    if (id === "state") {
      if ((data.settingsMod || 0) > S.settingsMod && data.settings) { const oldCols = JSON.stringify(S.settings.cols); S.settings = Object.assign({}, DEFAULTS, data.settings); S.settings.cols = Object.assign({ temi: true, cm: true, ia: true }, S.settings.cols || {}); S.settingsMod = data.settingsMod; DB.setMeta("settings", { v: data.settings, mod: data.settingsMod }); changed = true; if (JSON.stringify(S.settings.cols) !== oldCols) loadOfficial().then(() => { rebuildCards(); rerender(); }); }
      const ml = mergeLogs(S.logs, data.logs || {}); if (stable(syncLogs(ml)) !== stable(syncLogs(S.logs))) { S.logs = ml; changed = true; }
      if (data.session && (!S.session || data.session.mod > S.session.mod)) { S.session = data.session; DB.setMeta("session", S.session); changed = true; }
      if (S.session && (!data.session || S.session.mod > data.session.mod)) this.dirty.st = true;
      if (changed) DB.setMeta("logs", S.logs);
      // se meu log local de algum dia é maior, preciso enviar
      if (stable(syncLogs(S.logs)) !== stable(syncLogs(data.logs || {}))) this.dirty.st = true;
      if ((data.settingsMod || 0) < S.settingsMod) this.dirty.st = true;
    } else if (/^p\d\d$/.test(id)) {
      const put = [];
      for (const [cid, a] of Object.entries(data.c || {})) {
        const r = decP(cid, a); seen && seen.p.set(cid, r.mod);
        const l = S.prog.get(cid);
        if (!l || r.mod > l.mod) { S.prog.set(cid, r); put.push(r); changed = true; }
        else if (l.mod > r.mod) this.dirty.p.add(id);
      }
      DB.putMany("prog", put);
    } else if (/^u\d\d$/.test(id)) {
      const put = [], del = [];
      for (const [cid, o] of Object.entries(data.c || {})) {
        seen && seen.u.set(cid, o.m);
        const l = S.user.get(cid), tm = this.tomb && this.tomb.get(cid);
        if (tm && tm >= (o.m || 0)) { if (!o.x) this.dirty.u.add(id); continue; }
        if (!l || o.m > l.mod) {
          changed = true;
          if (o.x) { S.user.delete(cid); del.push(cid); }
          else { const u = { id: cid, deck: o.d, q: o.q, a: o.a, style: o.st || "codice", tags: o.t || [], mod: o.m, created: o.c || o.m }; S.user.set(cid, u); put.push(u); }
        } else if (l.mod > o.m) this.dirty.u.add(id);
      }
      DB.putMany("user", put); DB.delMany("user", del);
    } else if (id === "media") {
      Object.assign(this.mediaMap, data.m || {});
    }
    return changed;
  },
  async pull() {
    if (!this.on || this.busy) return;
    try {
      const snap = await this.col.get(); let ch = false;
      for (const d of snap.docs) if (this.applyDoc(d.id, d.data(), null)) ch = true;
      this.lastSync = Date.now(); this.setStatus("ok", "☁️ Sincronizado " + new Date().toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" }));
      if (ch) { rebuildCards(); if (location.hash !== "#estudar") rerender(); }
      if (this.dirty.p.size || this.dirty.u.size || this.dirty.st) this.schedule(300);
    } catch (e) { this.setStatus("err", "⚠️ Sem conexão — salvo no aparelho"); }
  },
  markP(id) { this.dirty.p.add(shardP(id)); this.schedule(); Hub.markP(id); },
  markU(id) { this.dirty.u.add(shardU(id)); this.schedule(); Hub.markU(id); },
  markSt() { this.dirty.st = true; this.schedule(); Hub.markSt(); },
  schedule(ms = 2500) { if (!this.on) return; clearTimeout(this.timer); this.timer = setTimeout(() => this.flush(), ms); },
  async flush() {
    if (!this.on || this.busy) return; this.busy = true; this.setStatus("busy", "⏳ Sincronizando…");
    try {
      for (const sh of [...this.dirty.p]) {
        this.dirty.p.delete(sh); const ref = this.col.doc(sh);
        const remote = await ref.get(); if (remote.exists) this.applyDoc(sh, remote.data(), null); this.dirty.p.delete(sh);
        const c = {}; for (const p of S.prog.values()) if (shardP(p.id) === sh) c[p.id] = encP(p);
        await ref.set({ c, v: 1 });
      }
      for (const sh of [...this.dirty.u]) {
        this.dirty.u.delete(sh); const ref = this.col.doc(sh);
        const remote = await ref.get(); if (remote.exists) this.applyDoc(sh, remote.data(), null); this.dirty.u.delete(sh);
        const c = {}; if (remote.exists) for (const [k, o] of Object.entries(remote.data().c || {})) if (o.x && !S.user.has(k)) c[k] = o;
        for (const u of S.user.values()) if (shardU(u.id) === sh) c[u.id] = { d: u.deck, q: u.q, a: u.a, st: u.style, t: u.tags, m: u.mod, c: u.created };
        for (const [k, m] of (this.tomb || new Map())) if (shardU(k) === sh && !S.user.has(k)) c[k] = { x: 1, m };
        await ref.set({ c, v: 1 });
      }
      if (this.dirty.st) {
        this.dirty.st = false; const ref = this.col.doc("state"); const r = await ref.get(); if (r.exists) this.applyDoc("state", r.data(), null); this.dirty.st = false;
        const logs = syncLogs(S.logs);
        const { cols, newPerDay, revPerDay, steps, grad, easy } = S.settings;
        await ref.set({ settings: { cols, newPerDay, revPerDay, steps, grad, easy }, settingsMod: S.settingsMod, logs, session: S.session || null, app: APP_VERSION });
      }
      if (this.dirty.media) { this.dirty.media = false; await this.col.doc("media").set({ m: this.mediaMap }); }
      this.lastSync = Date.now(); this.err = ""; this.setStatus("ok", "☁️ Sincronizado " + new Date().toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" }));
    } catch (e) {
      console.warn("flush", e); this.err = e.code || e.message || String(e);
      this.setStatus("err", e.code === "quota_exceeded" ? "⚠️ Nuvem cheia" : "⚠️ Erro de sync"); this.schedule(20000);
    } finally { this.busy = false; if (this.dirty.p.size || this.dirty.u.size || this.dirty.st || this.dirty.media) this.schedule(1500); }
  },
  async uploadMedia(name, blob) {
    if (!this.assets || this.mediaMap[name]) return;
    const ext = name.split(".").pop().toLowerCase();
    const type = { png: "image/png", jpg: "image/jpeg", jpeg: "image/jpeg", gif: "image/gif", webp: "image/webp", svg: "image/svg+xml" }[ext];
    if (!type) return;
    try { const r = await this.assets.upload(blob, { type }); this.mediaMap[name] = r.id; this.dirty.media = true; this.schedule(); } catch (e) { console.warn("upload", name, e.code || e); }
  },
};


/* ---------------- Sincronização universal 360X ----------------
   • Hub GitHub (Gist secreto): funciona no app do GitHub Pages em qualquer aparelho (iPhone, Mac, PC).
     Mesma chave em todos os aparelhos → progresso, XP, questões e ajustes mesclados automaticamente.
   • Nuvem do Claude (Cloud, acima): funciona na página do Claude.
   • Ponte (copiar/colar): leva o progresso entre o app do GitHub e a página do Claude, que é isolada
     por segurança (não pode acessar o GitHub).
   Regra de mescla: por card vence o mais recente (mod); registros diários campo a campo (máximo);
   questões por data da última resposta; nada é apagado por falta de dado do outro lado. */
const stable = v => v === null || typeof v !== "object" ? JSON.stringify(v) : Array.isArray(v) ? "[" + v.map(stable).join(",") + "]" : "{" + Object.keys(v).sort().map(k => JSON.stringify(k) + ":" + stable(v[k])).join(",") + "}";
function mergeDay(a, b) {
  if (!a || typeof a !== "object") return b; if (!b || typeof b !== "object") return a;
  const o = Object.assign({}, a);
  for (const [k, v] of Object.entries(b)) {
    const x = o[k];
    if (typeof v === "number") o[k] = Math.max(typeof x === "number" ? x : -Infinity, v);
    else if (Array.isArray(v)) { const L = Array.isArray(x) ? x : [], seen = new Set(L.map(s => stable(s))); o[k] = L.concat(v.filter(s => !seen.has(stable(s)))); }
    else if (v && typeof v === "object") o[k] = mergeDay(x && typeof x === "object" ? x : null, v);
    else if (x === undefined) o[k] = v;
  }
  return o;
}
function mergeLogs(L, R) {
  const out = Object.assign({}, L);
  for (const [k, rv] of Object.entries(R || {})) {
    if (k === "_q") {
      const o = Object.assign({}, out._q || {});
      for (const [id, e] of Object.entries(rv || {})) { const c = o[id]; if (!Array.isArray(e)) continue; if (!c || (e[3] || 0) > (c[3] || 0) || ((e[3] || 0) === (c[3] || 0) && (e[1] || 0) > (c[1] || 0))) o[id] = e; }
      out._q = o;
    } else if (k === "_hu") {   // itens próprios da aba Honra: vence o mod mais recente (inclui exclusões)
      const o = Object.assign({}, out._hu || {});
      for (const [id, e] of Object.entries(rv || {})) { if (!e || typeof e !== "object") continue; const c = o[id]; if (!c || (e.mod || 0) > (c.mod || 0)) o[id] = e; }
      out._hu = o;
    } else if (k === "_n" || k === "_h") {   // mnemônicos e 🕊️ Honra: treino pelo registro mais recente; favorito pelos carimbos de tempo
      const o = Object.assign({}, out[k] || {});
      for (const [id, e] of Object.entries(rv || {})) {
        if (!e || typeof e !== "object") continue; const c = o[id];
        if (!c || typeof c !== "object") { o[id] = e; continue; }
        const st = (e.t || 0) > (c.t || 0) ? e : c, x = {};
        for (const f of ["n", "ok", "s", "t"]) if (st[f] !== undefined) x[f] = st[f];
        const fv = Math.max(e.f || 0, c.f || 0), uf = Math.max(e.u || 0, c.u || 0); if (fv) x.f = fv; if (uf) x.u = uf;
        o[id] = x;
      }
      out[k] = o;
    } else out[k] = mergeDay(out[k], rv);
  }
  return out;
}
const syncLogs = logs => { const o = {}, days = Object.keys(logs || {}).filter(k => /^\d/.test(k)).sort().slice(-120); for (const k of Object.keys(logs || {})) if (!/^\d/.test(k) || days.includes(k)) o[k] = logs[k]; return o; };
const encU = u => ({ d: u.deck, q: u.q, a: u.a, st: u.style, t: u.tags, m: u.mod, c: u.created });

const Sync = {
  /* fotografia completa do estado local (para Gist e Ponte) */
  snapshot() {
    const p = {}, u = {}; for (const x of S.prog.values()) p[x.id] = encP(x);
    for (const x of S.user.values()) u[x.id] = encU(x);
    for (const [k, m] of (Cloud.tomb || new Map())) if (!S.user.has(k)) u[k] = { x: 1, m };
    const { cols, newPerDay, revPerDay, steps, grad, easy } = S.settings;
    return { p, u, st: { settings: { cols, newPerDay, revPerDay, steps, grad, easy }, settingsMod: S.settingsMod, logs: syncLogs(S.logs), session: S.session || null } };
  },
  /* aplica dados remotos; devolve o que mudou aqui e o que o outro lado precisa receber */
  async apply(snap, { full = true } = {}) {
    const res = { changed: 0, upP: new Set(), upU: new Set(), upSt: false, gotP: 0 };
    const putP = [], putU = [], delU = [];
    if (snap.p) {
      for (const [id, a] of Object.entries(snap.p)) {
        const r = decP(id, a), l = S.prog.get(id);
        if (!l || r.mod > l.mod) { S.prog.set(id, r); putP.push(r); res.gotP++; Cloud.dirty.p.add(shardP(id)); }
        else if (l.mod > r.mod) res.upP.add(id);
      }
      if (full) for (const id of S.prog.keys()) if (!(id in snap.p)) res.upP.add(id);
    }
    if (snap.u) {
      for (const [id, o] of Object.entries(snap.u)) {
        const l = S.user.get(id), tm = Cloud.tomb && Cloud.tomb.get(id);
        if (tm && tm >= (o.m || 0)) { if (!o.x) res.upU.add(id); continue; }
        if (!l || (o.m || 0) > l.mod) {
          if (o.x) { if (l) { S.user.delete(id); delU.push(id); (Cloud.tomb = Cloud.tomb || new Map()).set(id, o.m); } }
          else { const x = { id, deck: o.d, q: o.q, a: o.a, style: o.st || "codice", tags: o.t || [], mod: o.m, created: o.c || o.m }; S.user.set(id, x); putU.push(x); }
          Cloud.dirty.u.add(shardU(id));
        } else if (l.mod > (o.m || 0)) res.upU.add(id);
      }
      if (full) { for (const id of S.user.keys()) if (!(id in snap.u)) res.upU.add(id); for (const id of (Cloud.tomb || new Map()).keys()) if (!(id in snap.u)) res.upU.add(id); }
    }
    if (snap.st) {
      const d = snap.st;
      if ((d.settingsMod || 0) > S.settingsMod && d.settings) { S.settings = Object.assign({}, DEFAULTS, S.settings, d.settings); S.settings.cols = Object.assign({ temi: true, cm: true, ia: true }, S.settings.cols || {}); S.settingsMod = d.settingsMod; await DB.setMeta("settings", { v: S.settings, mod: S.settingsMod }); res.changed++; Cloud.dirty.st = true; }
      else if ((d.settingsMod || 0) < S.settingsMod) res.upSt = true;
      if (d.session && (!S.session || (d.session.mod || 0) > (S.session.mod || 0))) { S.session = d.session; await DB.setMeta("session", S.session); Cloud.dirty.st = true; }
      else if (S.session && (!d.session || (S.session.mod || 0) > (d.session.mod || 0))) res.upSt = true;
      const m = mergeLogs(S.logs, d.logs || {});
      if (stable(syncLogs(m)) !== stable(syncLogs(S.logs))) { S.logs = m; await DB.setMeta("logs", S.logs); res.changed++; Cloud.dirty.st = true; }
      if (stable(syncLogs(m)) !== stable(syncLogs(d.logs || {}))) res.upSt = true;
    } else if (full) res.upSt = true;
    if (putP.length) await DB.putMany("prog", putP);
    if (putU.length) await DB.putMany("user", putU);
    if (delU.length) { await DB.delMany("user", delU); await DB.setMeta("tomb", [...Cloud.tomb]); }
    res.changed += putP.length + putU.length + delU.length;
    if (Cloud.on && res.changed) Cloud.schedule(1500);
    if (res.changed) { rebuildCards(); xpBadge(); if (location.hash !== "#estudar") rerender(); }
    return res;
  },
};

/* ---------- Hub GitHub (Gist secreto) ---------- */
const Hub = {
  API: "https://api.github.com", DESC: "CÓDICE 360X · sincronização de estudo (não apagar)", NP: 16, NU: 4,
  cfg: null, on: false, busy: false, timer: null, firstMark: 0, etag: "", lastSync: 0, err: "", devs: {}, dirty: { p: new Set(), u: new Set(), st: false }, again: false,
  inClaude() { return !!(window.claude && typeof window.claude.use === "function"); },
  shP(id) { return "p" + String(hnum(id) % this.NP).padStart(2, "0"); },
  shU(id) { return "u" + (hnum(id) % this.NU); },
  devName() {
    const ua = navigator.userAgent, pwa = (window.navigator.standalone || matchMedia("(display-mode: standalone)").matches) ? " (app)" : "";
    const b = /iPhone/.test(ua) ? "iPhone" : /iPad/.test(ua) || (/Mac/.test(ua) && navigator.maxTouchPoints > 1) ? "iPad" : /Android/.test(ua) ? "Android" : /Mac/.test(ua) ? "Mac" : /Windows/.test(ua) ? "Windows" : "Computador";
    return b + pwa;
  },
  load() { try { this.cfg = JSON.parse(lsGet("hub360") || "null"); } catch (e) { this.cfg = null; } if (this.cfg && !this.cfg.dev) { this.cfg.dev = "d" + Math.random().toString(36).slice(2, 10); this.save(); } },
  save() { lsSet("hub360", JSON.stringify(this.cfg)); },
  status(kind, txt) { if (!this.inClaude()) Cloud.setStatus(kind, txt); },
  hhmm(t) { return new Date(t).toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" }); },
  async req(path, opt = {}) {
    const h = Object.assign({ Authorization: "Bearer " + this.cfg.token, Accept: "application/vnd.github+json" }, opt.headers || {});
    const r = await fetch(this.API + path, Object.assign({}, opt, { headers: h, cache: "no-store" }));
    if (r.status === 401) throw Object.assign(new Error("Chave inválida ou expirada"), { code: 401 });
    if (r.status === 403 || r.status === 404) { const t = await r.text().catch(() => ""); throw Object.assign(new Error(/rate limit/i.test(t) ? "Limite do GitHub atingido — tente em alguns minutos" : "A chave não tem a permissão “gist”"), { code: r.status }); }
    return r;
  },
  init() {
    this.load();
    if (this.inClaude() || !this.cfg || !this.cfg.token || !this.cfg.gist) { if (!this.inClaude()) this.status("", "☁️ Ativar sync"); return; }
    this.on = true; this.status("busy", "⏳ GitHub…"); this.sync(true);
  },
  /* conectar com a chave: acha o gist do CÓDICE ou cria um; depois resgata tudo o que existe aqui */
  async connect(token, name) {
    this.cfg = { token: token.trim(), gist: "", dev: (this.cfg && this.cfg.dev) || "d" + Math.random().toString(36).slice(2, 10), name: name || this.devName() };
    try {
      let id = "";
      for (let page = 1; page <= 3 && !id; page++) {
        const r = await this.req(`/gists?per_page=100&page=${page}`); const list = await r.json();
        const g = list.find(x => x.description === this.DESC); if (g) id = g.id; if (list.length < 100) break;
      }
      if (!id) {
        const r = await this.req("/gists", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ description: this.DESC, public: false, files: { "codice360x.json": { content: JSON.stringify({ v: 1, criado: new Date().toISOString(), app: APP_VERSION }) } } }) });
        if (!r.ok) throw new Error("Não consegui criar o gist (" + r.status + ")");
        id = (await r.json()).id;
      }
      this.cfg.gist = id; this.save(); this.on = true; this.etag = "";
      const n = await this.sync(true);
      return n;
    } catch (e) { this.cfg = null; lsSet("hub360", "null"); this.on = false; throw e; }
  },
  disconnect() { this.on = false; this.cfg = null; lsSet("hub360", "null"); clearTimeout(this.timer); this.status("", "☁️ Ativar sync"); },
  markP(id) { if (!this.on) return; this.dirty.p.add(this.shP(id)); this.schedule(); },
  markU(id) { if (!this.on) return; this.dirty.u.add(this.shU(id)); this.schedule(); },
  markSt() { if (!this.on) return; this.dirty.st = true; this.schedule(); },
  schedule(ms = 6000) {
    if (!this.on) return; const now = Date.now(); if (!this.firstMark) this.firstMark = now;
    clearTimeout(this.timer); this.timer = setTimeout(() => this.sync(), Math.max(0, Math.min(ms, this.firstMark + 30000 - now)));
  },
  async readFiles(g) {
    const out = {};
    for (const [name, f] of Object.entries(g.files || {})) {
      let txt = f.content;
      if (f.truncated && f.raw_url) txt = await (await fetch(f.raw_url, { cache: "no-store" })).text();
      try { out[name.replace(/\.json$/, "")] = JSON.parse(txt); } catch (e) { }
    }
    return out;
  },
  /* puxa → mescla → envia só os fragmentos com novidade daqui. Devolve nº de itens enviados no 1º resgate */
  async sync(rescue = false) {
    if (!this.on) return 0; if (this.busy) { this.again = true; return 0; }
    this.busy = true; clearTimeout(this.timer); this.firstMark = 0; this.status("busy", "⏳ Sincronizando…");
    let sent = 0;
    try {
      const r = await this.req(`/gists/${this.cfg.gist}`, { headers: this.etag && !rescue ? { "If-None-Match": this.etag } : {} });
      if (r.status === 404) throw new Error("Gist não encontrado");
      if (r.status !== 304) {
        if (!r.ok) throw new Error("GitHub respondeu " + r.status);
        this.etag = r.headers.get("ETag") || ""; const g = await r.json(), F = await this.readFiles(g);
        const snap = { p: {}, u: {} }; let hasP = false, hasU = false;
        for (const [k, v] of Object.entries(F)) {
          if (/^p\d\d$/.test(k)) { Object.assign(snap.p, v.c || {}); hasP = true; }
          else if (/^u\d$/.test(k)) { Object.assign(snap.u, v.c || {}); hasU = true; }
          else if (k === "st") snap.st = v;
          else if (k === "meta") this.devs = v.devs || {};
        }
        const res = await Sync.apply(snap, { full: true });
        res.upP.forEach(id => this.dirty.p.add(this.shP(id))); res.upU.forEach(id => this.dirty.u.add(this.shU(id))); if (res.upSt) this.dirty.st = true;
        if (res.gotP && !rescue) toast(`☁️ ${res.gotP} card(s) atualizados de outro aparelho`);
      }
      if (this.dirty.p.size || this.dirty.u.size || this.dirty.st) {
        const files = {}, P = [...this.dirty.p], U = [...this.dirty.u]; this.dirty.p.clear(); this.dirty.u.clear();
        for (const sh of P) { const c = {}; for (const x of S.prog.values()) if (this.shP(x.id) === sh) c[x.id] = encP(x); files[sh + ".json"] = { content: JSON.stringify({ c }) }; sent += Object.keys(c).length; }
        for (const sh of U) { const c = {}; for (const x of S.user.values()) if (this.shU(x.id) === sh) c[x.id] = encU(x); for (const [k, m] of (Cloud.tomb || new Map())) if (this.shU(k) === sh && !S.user.has(k)) c[k] = { x: 1, m }; files[sh + ".json"] = { content: JSON.stringify({ c }) }; }
        if (this.dirty.st || rescue) { this.dirty.st = false; files["st.json"] = { content: JSON.stringify(Sync.snapshot().st) }; }
        this.devs[this.cfg.dev] = { n: this.cfg.name || this.devName(), t: Date.now(), app: APP_VERSION };
        files["meta.json"] = { content: JSON.stringify({ v: 1, app: APP_VERSION, t: Date.now(), devs: this.devs }) };
        const w = await this.req(`/gists/${this.cfg.gist}`, { method: "PATCH", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ files }) });
        if (!w.ok) { P.forEach(s => this.dirty.p.add(s)); U.forEach(s => this.dirty.u.add(s)); this.dirty.st = true; throw new Error("Falha ao enviar (" + w.status + ")"); }
        this.etag = w.headers.get("ETag") || "";
      }
      this.lastSync = Date.now(); this.err = ""; this.status("ok", "☁️ GitHub ✓ " + this.hhmm(this.lastSync));
    } catch (e) {
      console.warn("hub", e); this.err = e.message || String(e);
      this.status("err", e.code === 401 || e.code === 403 ? "⚠️ Chave do GitHub" : navigator.onLine === false ? "📴 Offline — salvo aqui" : "⚠️ Sync pausado");
      if (rescue) { this.busy = false; throw e; }
      clearTimeout(this.timer); this.timer = setTimeout(() => this.sync(), 30000);
    } finally { this.busy = false; if (this.again) { this.again = false; this.schedule(1000); } }
    if (/^#ajustes/.test(location.hash)) renderSyncUI();
    return sent;
  },
};

/* ---------- Ponte (copiar/colar) entre o app do GitHub e a página do Claude ---------- */
const Ponte = {
  async pack() {
    const json = JSON.stringify(Object.assign({ f: "c360x-ponte-1", t: Date.now(), app: APP_VERSION }, Sync.snapshot()));
    const u8 = new TextEncoder().encode(json);
    const b64 = b => { let s = ""; for (let i = 0; i < b.length; i += 0x8000) s += String.fromCharCode.apply(null, b.subarray(i, i + 0x8000)); return btoa(s); };
    if (typeof CompressionStream === "function") { try { const z = new Uint8Array(await new Response(new Blob([u8]).stream().pipeThrough(new CompressionStream("gzip"))).arrayBuffer()); return "C360X-Z:" + b64(z); } catch (e) { } }
    return "C360X-J:" + b64(u8);
  },
  async unpack(txt) {
    txt = String(txt || "").replace(/\s+/g, ""); const m = txt.match(/C360X-([ZJ]):([A-Za-z0-9+/=]+)/); if (!m) throw new Error("Código não reconhecido — copie de novo no outro app");
    const bin = atob(m[2]), u8 = new Uint8Array(bin.length); for (let i = 0; i < bin.length; i++) u8[i] = bin.charCodeAt(i);
    const raw = m[1] === "Z" ? new Uint8Array(await new Response(new Blob([u8]).stream().pipeThrough(new DecompressionStream("gzip"))).arrayBuffer()) : u8;
    const o = JSON.parse(new TextDecoder().decode(raw)); if (o.f !== "c360x-ponte-1") throw new Error("Formato desconhecido");
    return o;
  },
  async importar(txt) {
    const o = await this.unpack(txt), res = await Sync.apply(o, { full: false });
    if (Hub.on) { Hub.dirty.st = true; S.prog.forEach(p => Hub.dirty.p.add(Hub.shP(p.id))); Hub.schedule(500); }
    if (Cloud.on) { Cloud.dirty.st = true; Cloud.schedule(500); }
    return res;
  },
};

/* ---------------- Montagem dos cards ---------------- */
function progOf(id) { return S.prog.get(id); }
function cardFrom(base) {
  const p = progOf(base.id);
  return Object.assign(base, { srs: p ? p.s : newSRS(), susp: p ? p.susp : false, marked: p ? p.mk : false, hl: p && p.hl ? p.hl : [] });
}
function rebuildCards() {
  const cols = S.settings.cols || {};
  const list = [];
  for (const o of S.official) if (cols[o.col] !== false) list.push(cardFrom(o));
  let k = 100000; for (const u of [...S.user.values()].sort((a, b) => (a.created || 0) - (b.created || 0))) {
    list.push(cardFrom({ id: u.id, deck: u.deck, q: u.q, a: u.a, style: u.style || "codice", tags: u.tags || [], ord: k++, user: true, txt: (strip(u.q) + " " + strip(u.a) + " " + (u.tags || []).join(" ")).toLowerCase() }));
  }
  S.cards = list; S.byId = new Map(list.map(c => [c.id, c]));
}
async function saveProg(c) {
  const p = { id: c.id, s: c.srs, susp: !!c.susp, mk: !!c.marked, hl: c.hl || [], mod: Date.now() };
  S.prog.set(c.id, p); await DB.put("prog", p); Cloud.markP(c.id);
}
async function saveLog() { await DB.setMeta("logs", S.logs); Cloud.markSt(); }
async function saveSettings() { S.settingsMod = Date.now(); await DB.setMeta("settings", { v: S.settings, mod: S.settingsMod }); Cloud.markSt(); }

/* ---------------- Formato CÓDICE (JSON) ---------------- */
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
  return {
    q: `${head}<div class=q>${qf}</div>`,
    a: `${head}<div class=q>${af}</div><hr id=answer>` + (c.b ? `<div class=a>${c.b}</div>` : "") + imgHTML(c.img) +
      (c.x ? `<div class=peg>🎯 <b>Pegadinha / Nerd</b><br>${c.x}</div>` : "") + (c.s ? `<div class=src>📚 ${c.s}</div>` : ""),
  };
}
const pick = (o, ...ks) => { for (const k of ks) { if (o[k] != null && o[k] !== "") return o[k]; } return ""; };
function normalizeCards(obj, forcedDeck) {
  const rootDeck = forcedDeck || pick(obj, "baralho", "deck", "deckName") || "Meus cards::" + today();
  const list = Array.isArray(obj) ? obj : (obj.cards || obj.flashcards || obj.notes || []);
  const out = [];
  list.forEach(r => {
    if (typeof r !== "object" || !r) return;
    const f = String(pick(r, "frente", "front", "pergunta", "question", "q", "Frente", "Front"));
    if (!f.trim()) return;
    let deck = forcedDeck ? forcedDeck : (pick(r, "baralho", "deck") || rootDeck);
    const sub = pick(r, "subtema", "subtopic", "subdeck", "subtopico");
    if (sub && !String(deck).endsWith("::" + sub)) deck += "::" + sub;
    let tags = pick(r, "tags", "etiquetas"); if (typeof tags === "string") tags = tags.split(/[\s,]+/).filter(Boolean); if (!Array.isArray(tags)) tags = [];
    const base = { deck: String(deck).replace(/\s*::\s*/g, "::"), f, b: String(pick(r, "verso", "back", "resposta", "answer", "a", "Verso", "Back")),
      x: String(pick(r, "pegadinha", "extra", "nerd", "dica", "curiosidade")), s: String(pick(r, "fonte", "source", "referencia", "ref")), img: pick(r, "imagem", "image", "img", "svg"), tags };
    const clozes = [...new Set([...f.matchAll(/\{\{c(\d+)::/g)].map(m => +m[1]))].sort((a, b) => a - b);
    if (clozes.length) clozes.forEach(n => out.push(Object.assign({}, base, { cloze: n }))); else out.push(base);
  });
  return out;
}
const rawId = r => "c:" + hash(r.deck + "|" + strip(r.f) + "|" + (r.cloze || 0));
function extractJSON(text) {
  text = text.replace(/[“”]/g, '"').replace(/ /g, " ");
  const blocks = [...text.matchAll(/```(?:json)?\s*([\s\S]*?)```/gi)].map(m => m[1]);
  const cands = blocks.length ? blocks : [text.slice(Math.min(...["{", "["].map(ch => text.indexOf(ch) < 0 ? 1e9 : text.indexOf(ch))))];
  const out = [];
  for (let c of cands) {
    c = c.trim(); if (!c) continue;
    try { out.push(JSON.parse(c)); continue; } catch (e) { }
    try { out.push(JSON.parse(c.replace(/,\s*([}\]])/g, "$1"))); continue; } catch (e) { }
    const end = Math.max(c.lastIndexOf("}"), c.lastIndexOf("]"));
    try { out.push(JSON.parse(c.slice(0, end + 1).replace(/,\s*([}\]])/g, "$1"))); } catch (e) { throw new Error("JSON inválido: " + e.message); }
  }
  return out;
}
function parseTextLines(text, deck) {
  const out = [];
  for (const l of text.split(/\r?\n/).map(l => l.trim()).filter(Boolean)) {
    if (/^#/.test(l)) continue;
    const parts = l.includes("\t") ? l.split("\t") : l.includes(" ;; ") ? l.split(" ;; ") : l.includes(";") ? l.split(";") : l.includes("|") ? l.split("|") : null;
    if (!parts || parts.length < 2 || /^(frente|front|pergunta)$/i.test(parts[0].trim())) continue;
    out.push({ frente: parts[0].trim(), verso: parts[1].trim(), pegadinha: (parts[2] || "").trim(), tags: (parts[3] || "").trim() });
  }
  return normalizeCards({ baralho: deck || "Meus cards::" + today(), cards: out });
}
async function storeMediaMap(midia) {
  const items = [];
  for (const [name, v] of Object.entries(midia || {})) {
    try {
      let blob;
      if (String(v).startsWith("data:")) blob = await (await fetch(v)).blob();
      else if (/^<svg/i.test(String(v))) blob = new Blob([v], { type: "image/svg+xml" });
      else blob = await (await fetch(new URL(v, location.href))).blob();
      items.push({ name, blob });
    } catch (e) { console.warn("mídia falhou", name, e); }
  }
  await DB.putMany("media", items);
  for (const i of items) { if (S.mediaURL.has(i.name)) { URL.revokeObjectURL(S.mediaURL.get(i.name)); S.mediaURL.delete(i.name); } Cloud.uploadMedia(i.name, i.blob); }
  return items.length;
}
/* grava cards do usuário (substitui conteúdo, mantém progresso) */
async function upsertUser(raws) {
  const now = Date.now(); let novos = 0, atual = 0; const put = [];
  for (const r of raws) {
    const id = r.id || rawId(r);
    if (S.official.some(o => o.id === id)) { atual++; continue; }
    const { q, a } = r.q ? { q: r.q, a: r.a } : codiceHTML(r, r.cloze);
    const old = S.user.get(id);
    const u = { id, deck: r.deck, q, a, style: r.style || "codice", tags: r.tags || [], mod: now, created: old ? old.created : now + put.length };
    old ? atual++ : novos++;
    S.user.set(id, u); put.push(u); Cloud.markU(id); if (Cloud.tomb) Cloud.tomb.delete(id);
  }
  await DB.putMany("user", put); rebuildCards();
  return { novos, atual };
}

/* ---------------- Coleções oficiais ---------------- */
// Carregamento robusto: concorrência limitada, novas tentativas e cópia local (IndexedDB) de cada baralho.
const sleep = ms => new Promise(r => setTimeout(r, ms));
async function fetchJSON(url, tries = 3, fresh = false) {
  let err;
  for (let i = 0; i < tries; i++) {
    try {
      const r = await fetch(url, { cache: fresh || i ? "no-cache" : "default" });
      if (!r.ok) throw new Error(r.status + " " + url);
      return await r.json();
    } catch (e) { err = e; if (i < tries - 1) await sleep(500 * (i + 1) * (i + 1)); }
  }
  throw err;
}
async function fetchPack(p, tries = 3) {
  let err;
  for (let i = 0; i < tries; i++) {
    try {
      if (typeof DecompressionStream !== "undefined" && p.gz) {
        const r = await fetch(p.gz + "?v=" + p.sha, { cache: i ? "no-cache" : "default" });
        if (!r.ok) throw new Error(r.status + " " + p.gz);
        let buf;
        if (p.enc === "b64") { const t = (await r.text()).trim(); buf = Uint8Array.from(atob(t), ch => ch.charCodeAt(0)); }
        else buf = new Uint8Array(await r.arrayBuffer());
        if (buf[0] === 0x1f && buf[1] === 0x8b) {
          const st = new Blob([buf]).stream().pipeThrough(new DecompressionStream("gzip"));
          return JSON.parse(await new Response(st).text());
        }
        return JSON.parse(new TextDecoder().decode(buf)); // servidor já descompactou
      }
      return await fetchJSON(p.json + "?v=" + p.sha, 1);
    } catch (e) {
      err = e; console.warn("pacote, tentativa", i + 1, p.nome, e);
      if (i === tries - 1 && p.json) { try { return await fetchJSON(p.json + "?v=" + p.sha, 2); } catch (e2) { err = e2; } }
      else await sleep(500 * (i + 1) * (i + 1));
    }
  }
  throw err;
}
let officialRetry = 0;
async function loadOfficial() {
  let idx = null, offline = false;
  try { idx = await fetchJSON("data/index.json", 3, true); }
  catch (e) { console.error(e); idx = await DB.meta("offIndex", null).catch(() => null); offline = true; }
  if (!idx) { toast("⚠️ Sem conexão para baixar as coleções. Seus cards próprios e o progresso continuam salvos."); scheduleOfficialRetry(); return; }
  S.index = idx;
  if (!offline) DB.setMeta("offIndex", idx).catch(() => {});
  const cols = (S.settings && S.settings.cols) || {};
  const decks = idx.decks.filter(d => cols[d.colecao || "temi"] !== false);
  const cachedVer = await DB.meta("offCacheVer", "").catch(() => ""), needCache = cachedVer !== idx.versao;
  const res = new Array(decks.length), failed = []; let next = 0, fromCache = 0;
  // 1) Pacotes: cópia local atual (sem download) → .json.gz → .json; o que faltar cai para os arquivos individuais
  const packData = {}, packStat = { local: 0, rede: 0, velho: 0, falhou: 0 };
  const packs = (idx.pacotes || []).filter(p => p.colecoes.some(c => cols[c] !== false));
  await Promise.all(packs.map(async p => {
    const c = await DB.meta("pack:" + p.nome, null).catch(() => null);
    const use = data => (data.decks || []).forEach(x => packData[x.arquivo] = x.j);
    if (c && c.sha === p.sha && !S.forcePacks) { use(c.data); packStat.local++; return; }
    if (!offline) {
      try { const data = await fetchPack(p); use(data); packStat.rede++; DB.setMeta("pack:" + p.nome, { sha: p.sha, data }).catch(() => {}); return; }
      catch (e) { console.warn("pacote falhou", p.nome, e); }
    }
    if (c) { use(c.data); packStat.velho++; return; }
    packStat.falhou++;
  }));
  decks.forEach((d, i) => { if (packData[d.arquivo]) res[i] = packData[d.arquivo]; });
  S.packStat = Object.assign(packStat, { total: packs.length, at: Date.now() });
  async function worker() {
    while (next < decks.length) {
      const i = next++, d = decks[i]; if (res[i]) continue; let j = null;
      if (!offline) {
        try { j = await fetchJSON(d.arquivo); if (needCache) DB.setMeta("deck:" + d.arquivo, j).catch(() => {}); }
        catch (e) { console.warn("baralho falhou", d.arquivo, e); }
      }
      if (!j) { j = await DB.meta("deck:" + d.arquivo, null).catch(() => null); if (j) fromCache++; else failed.push(d.arquivo); }
      res[i] = j;
    }
  }
  await Promise.all(Array.from({ length: Math.min(6, decks.length) }, worker));
  if (!failed.length && !offline && needCache && !packs.length) DB.setMeta("offCacheVer", idx.versao).catch(() => {});
  const list = []; let ord = 0;
  decks.forEach((d, i) => {
    const j = res[i]; if (!j) return;
    Object.assign(S.mediaPath, j.midia || {});
    for (const r of normalizeCards(j)) {
      const { q, a } = codiceHTML(r, r.cloze);
      list.push({ id: rawId(r), deck: r.deck, q, a, style: "codice", tags: r.tags, ord: ord++, col: d.colecao || "temi", official: true,
        txt: (strip(r.f) + " " + strip(r.b) + " " + strip(r.x) + " " + strip(r.s) + " " + r.tags.join(" ")).toLowerCase() });
    }
  });
  if (list.length || !S.official) S.official = list;
  if (failed.length) { toast(`⚠️ ${failed.length} de ${decks.length} baralhos não baixaram agora; vou tentar de novo sozinho. O restante já está liberado.`); scheduleOfficialRetry(); }
  else if (offline || fromCache || packStat.velho) toast(`📦 Sem internet estável: usando a cópia salva no aparelho.`);
  if (!failed.length) officialRetry = 0;
  packInfo();
}
function packInfo() {
  const el = document.getElementById("colsInfo"), p = S.packStat; if (!el || !p) return;
  const h = new Date(p.at).toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" });
  el.textContent = ` 📦 ${p.total} pacotes · ${p.local} já no aparelho · ${p.rede} baixados${p.velho ? ` · ${p.velho} cópia antiga` : ""}${p.falhou ? ` · ${p.falhou} via arquivos avulsos` : ""} · ${(S.official || []).length} cards · ${h}`;
}
document.addEventListener("click", async e => {
  if (!e.target.closest || !e.target.closest("#reloadCols")) return;
  toast("⏳ Baixando as coleções de novo…"); await DB.setMeta("offCacheVer", "").catch(() => {}); S.forcePacks = true;
  officialRetry = 0; await loadOfficial(); S.forcePacks = false; rebuildCards(); try { rerender(); } catch (er) { route(); }
  toast(`✅ ${S.official.length} cards oficiais carregados`);
});
function scheduleOfficialRetry() {
  if (officialRetry >= 4) return; officialRetry++;
  setTimeout(async () => { await loadOfficial(); rebuildCards(); try { rerender(); } catch (e) { route(); } }, 15000 * officialRetry);
}

/* ---------------- Renderização segura ---------------- */
function sanitize(html) {
  const doc = new DOMParser().parseFromString(`<div id="__r">${html}</div>`, "text/html");
  doc.querySelectorAll("script,iframe,object,embed,link,meta,base,form").forEach(e => e.remove());
  doc.querySelectorAll("*").forEach(el => [...el.attributes].forEach(a => {
    const n = a.name.toLowerCase(), v = a.value.trim().toLowerCase();
    if (n.startsWith("on") || ((n === "href" || n === "src" || n === "xlink:href") && v.startsWith("javascript:"))) el.removeAttribute(a.name);
  }));
  return doc.getElementById("__r").innerHTML;
}
async function mediaURL(name) {
  if (S.mediaURL.has(name)) return S.mediaURL.get(name);
  if (S.mediaPath[name]) return S.mediaPath[name];
  const m = await DB.get("media", name);
  if (m) { const u = URL.createObjectURL(m.blob); S.mediaURL.set(name, u); return u; }
  if (Cloud.mediaMap[name]) return "/_blob/" + Cloud.mediaMap[name];
  return null;
}
async function renderInto(host, html, styleId, deck) {
  const root = host.shadowRoot || host.attachShadow({ mode: "open" });
  const css = S.styles.get(styleId) || CODICE_CSS;
  const extra = styleId === "codice" ? "" : `.card{border-radius:14px;padding:14px 16px;min-height:200px;overflow-x:auto} img{max-width:100%;height:auto} table{max-width:100%}`;
  root.innerHTML = `<style>:host{display:block}${extra}${css}${HL_CSS}</style><style id="lt">${isLight() ? CODICE_LIGHT : ""}</style><div class="card${isLight() ? "" : " nightMode night_mode"}" style="--acc:${accentFor(deck)}">${sanitize(html)}</div>`;
  for (const img of root.querySelectorAll("[data-m]")) {
    const u = await mediaURL(img.getAttribute("data-m"));
    if (u) img.setAttribute("src", u); else img.setAttribute("alt", "🖼️ imagem ausente: " + img.getAttribute("data-m"));
  }
  if (host.id === "cardHost") { HL.apply(root, HL.card()); HL.count(); }
}


/* ---------------- 🖍️ Destaques (amarelo / verde) ---------------- */
const HL_CSS = `mark.hl{color:#111!important;border-radius:3px;padding:0 1px;box-decoration-break:clone;-webkit-box-decoration-break:clone;cursor:pointer}
mark.hl.y{background:#fde047!important}mark.hl.g{background:#86efac!important}mark.hl *{color:#111!important}`;
const HL = {
  pend: "", sel: null, hideT: 0, from: 0,
  norm: t => String(t || "").replace(/\s+/g, ""),
  card() { if (Study.view != null && Study.undo[Study.view]) return S.byId.get(Study.undo[Study.view].id); return Study.cur; },
  apply(root, c) {
    const box = root.querySelector(".card"); if (!box || !c || !c.hl || !c.hl.length) return;
    const nodes = [], w = document.createTreeWalker(box, NodeFilter.SHOW_TEXT, { acceptNode: n => n.parentNode.closest("style,script,svg") ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT });
    let n, N = "", map = [], off = 0;
    while ((n = w.nextNode())) { const v = n.nodeValue; nodes.push({ n, o: off, L: v.length }); for (let i = 0; i < v.length; i++) if (!/\s/.test(v[i])) { N += v[i]; map.push(off + i); } off += v.length; }
    const rg = [];
    for (const [t, col] of c.hl) {
      const k = this.norm(t); if (k.length < 2) continue;
      let i = N.indexOf(k);
      while (i >= 0) { rg.push([map[i], map[i + k.length - 1] + 1, col === "g" ? "g" : "y", t]); i = N.indexOf(k, i + k.length); }
    }
    if (!rg.length) return;
    rg.sort((a, b) => a[0] - b[0]); const ok = []; let end = -1; for (const r of rg) if (r[0] >= end) { ok.push(r); end = r[1]; }
    for (const { n, o, L } of nodes) {
      const seg = ok.filter(r => r[0] < o + L && r[1] > o); if (!seg.length) continue;
      const v = n.nodeValue, frag = document.createDocumentFragment(); let p = 0;
      for (const [a, b, col, t] of seg) {
        const s0 = Math.max(0, a - o), s1 = Math.min(L, b - o);
        if (s0 > p) frag.appendChild(document.createTextNode(v.slice(p, s0)));
        const m = document.createElement("mark"); m.className = "hl " + col; m.dataset.t = t; m.textContent = v.slice(s0, s1); frag.appendChild(m); p = s1;
      }
      if (p < L) frag.appendChild(document.createTextNode(v.slice(p)));
      n.parentNode.replaceChild(frag, n);
    }
  },
  text() {
    const host = $("#cardHost"), root = host.shadowRoot; if (!root) return "";
    const sel = (root.getSelection && root.getSelection()) || document.getSelection(); if (!sel || sel.isCollapsed) return "";
    const a = sel.anchorNode, inside = a && (root.contains(a) || host.contains(a) || a === host);
    if (!inside && Date.now() - this.from > 15000) return "";
    return sel.toString().replace(/\s+/g, " ").trim().slice(0, 400);
  },
  show(mode, t) {
    const b = $("#hlBar"); clearTimeout(this.hideT);
    this.pend = t; this.sel = mode === "edit" ? t : null;
    $("#hlTxt").textContent = "“" + (t.length > 60 ? t.slice(0, 58) + "…" : t) + "”";
    $("#hlDel").style.display = mode === "edit" ? "" : "none";
    b.classList.add("on");
  },
  hide(ms) { clearTimeout(this.hideT); this.hideT = setTimeout(() => $("#hlBar").classList.remove("on"), ms || 0); },
  async set(col) {
    const c = this.card(), t = this.pend; if (!c || !t) return this.hide();
    if (this.norm(t).length < 2) return toast("Selecione pelo menos 2 letras.");
    const k = this.norm(t);
    c.hl = (c.hl || []).filter(([x]) => this.norm(x) !== k && !(this.sel && this.norm(x) === this.norm(this.sel)));
    if (col) c.hl.push([t, col]);
    await saveProg(c); this.redraw(); this.hide();
    try { (($("#cardHost").shadowRoot.getSelection && $("#cardHost").shadowRoot.getSelection()) || document.getSelection()).removeAllRanges(); } catch (e) {}
    toast(col ? (col === "g" ? "🟩 Destacado em verde" : "🟨 Destacado em amarelo") : "🧽 Destaque removido");
  },
  async clearAll() {
    const c = this.card(); if (!c || !(c.hl && c.hl.length)) return toast("Este card não tem destaques.");
    c.hl = []; await saveProg(c); this.redraw(); toast("🧽 Destaques do card apagados");
  },
  redraw() {
    const c = this.card(); if (!c) return;
    const html = Study.view != null || Study.shown ? c.a : c.q;
    const y = scrollY; renderInto($("#cardHost"), html, c.style, c.deck).then(() => scrollTo(0, y));
    this.count();
  },
  count() { const c = this.card(), n = c && c.hl ? c.hl.length : 0; $("#bHl").textContent = n ? `🧽 Limpar destaques (${n})` : "🖍️ Destacar"; },
  init() {
    const host = $("#cardHost");
    host.addEventListener("pointerdown", () => { this.from = Date.now(); });
    host.addEventListener("touchstart", () => { this.from = Date.now(); }, { passive: true });
    let t0 = 0;
    document.addEventListener("selectionchange", () => {
      clearTimeout(t0); t0 = setTimeout(() => {
        if (location.hash !== "#estudar") return;
        const t = this.text(); if (t && this.norm(t).length >= 2) this.show("new", t); else if (!this.sel) this.hide(450);
      }, 180);
    });
    host.addEventListener("click", e => {
      const m = e.composedPath().find(x => x.tagName === "MARK" && x.classList && x.classList.contains("hl"));
      if (m && !this.text()) { e.stopPropagation(); this.show("edit", m.dataset.t || m.textContent); }
    });
    const bar = $("#hlBar");
    bar.addEventListener("pointerdown", e => { clearTimeout(this.hideT); e.preventDefault(); });
    bar.addEventListener("mousedown", e => e.preventDefault());
    $("#hlY").onclick = () => this.set("y"); $("#hlG").onclick = () => this.set("g");
    $("#hlDel").onclick = () => this.set(null); $("#hlX").onclick = () => { this.sel = null; this.hide(); };
    $("#bHl").onclick = () => { const c = this.card(); if (c && c.hl && c.hl.length) confirmAction(`Apagar os <b>${c.hl.length}</b> destaques deste card?`, () => this.clearAll()); else toast("🖍️ Selecione um trecho do card (arraste ou pressione e segure) e escolha 🟨 ou 🟩."); };
  },
};

/* ---------------- .apkg ---------------- */
let SQLp = null;
function loadSQL() {
  if (SQLp) return SQLp;
  SQLp = new Promise((res, rej) => { const s = document.createElement("script"); s.src = "lib/sql-asm.js"; s.onload = () => initSqlJs().then(res, rej); s.onerror = () => rej(new Error("não carregou sql.js")); document.head.appendChild(s); });
  return SQLp;
}
const isZstd = u8 => u8.length > 4 && u8[0] === 0x28 && u8[1] === 0xb5 && u8[2] === 0x2f && u8[3] === 0xfd;
const unz = u8 => isZstd(u8) ? fzstd.decompress(u8) : u8;
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
    if (v == null || filters.includes("type") || filters.some(f => f.startsWith("tts"))) return "";
    if (filters.includes("cloze")) v = renderCloze(v, ord + 1, answer);
    if (filters.includes("text")) v = esc(strip(v));
    if (filters.includes("hint")) v = `<details><summary>💡 dica</summary>${v}</details>`;
    return v;
  });
  return s.replace(/\[sound:[^\]]+\]/g, "");
}
const fixMediaRefs = html => html.replace(/<img([^>]*?)\ssrc=(["'])([^"']+)\2/gi, (m, pre, q, src) => /^(data:|https?:|blob:)/i.test(src) ? m : `<img${pre} data-m="${esc(decodeURIComponent(src))}"`);
async function importApkg(file, forcedDeck, log) {
  log("📦 Lendo pacote… (motor SQLite ~1,4 MB na 1ª vez)");
  const zip = await JSZip.loadAsync(file); const SQL = await loadSQL();
  const colName = zip.file("collection.anki21b") ? "collection.anki21b" : zip.file("collection.anki21") ? "collection.anki21" : "collection.anki2";
  if (!zip.file(colName)) throw new Error("Arquivo não parece um .apkg do Anki.");
  const db = new SQL.Database(unz(await zip.file(colName).async("uint8array")));
  const q = sql => { const r = db.exec(sql); if (!r.length) return []; const { columns, values } = r[0]; return values.map(v => Object.fromEntries(columns.map((c, i) => [c, v[i]]))); };
  const tables = q("select name from sqlite_master where type='table'").map(r => r.name);
  const models = {}, decks = {};
  if (tables.includes("notetypes")) {
    for (const nt of q("select id,name,config from notetypes")) { const cfg = pb(nt.config); models[nt.id] = { name: nt.name, type: cfg[1] && cfg[1][0] === 1 ? 1 : 0, css: pbStr(cfg, 3), flds: [], tmpls: [] }; }
    for (const f of q("select ntid,ord,name from fields order by ntid,ord")) models[f.ntid] && models[f.ntid].flds.push(f.name);
    for (const t of q("select ntid,ord,config from templates order by ntid,ord")) { const c = pb(t.config); models[t.ntid] && (models[t.ntid].tmpls[t.ord] = { qfmt: pbStr(c, 1), afmt: pbStr(c, 2) }); }
    for (const d of q("select id,name from decks")) decks[d.id] = String(d.name).replace(/\x1f/g, "::");
  } else {
    const col = q("select models,decks from col")[0];
    for (const [id, m] of Object.entries(JSON.parse(col.models))) models[id] = { name: m.name, type: m.type, css: m.css, flds: m.flds.sort((a, b) => a.ord - b.ord).map(f => f.name), tmpls: m.tmpls.sort((a, b) => a.ord - b.ord).map(t => ({ qfmt: t.qfmt, afmt: t.afmt })) };
    for (const [id, d] of Object.entries(JSON.parse(col.decks))) decks[id] = d.name;
  }
  let map = {}; const mediaFile = zip.file("media");
  if (mediaFile) { const raw = await mediaFile.async("uint8array"); if (raw[0] === 0x7b) map = JSON.parse(td.decode(raw)); else (pb(unz(raw))[1] || []).forEach((e, i) => { map[String(i)] = pbStr(pb(e), 1); }); }
  const mItems = [];
  for (const [num, name] of Object.entries(map)) {
    const f = zip.file(num); if (!f || !name) continue;
    const ext = name.split(".").pop().toLowerCase();
    const type = { png: "image/png", jpg: "image/jpeg", jpeg: "image/jpeg", gif: "image/gif", webp: "image/webp", svg: "image/svg+xml" }[ext] || "application/octet-stream";
    mItems.push({ name, blob: new Blob([unz(await f.async("uint8array"))], { type }) });
  }
  await DB.putMany("media", mItems); log(`🖼️ ${mItems.length} imagens/mídias`);
  if (Cloud.assets && mItems.length) { log("☁️ Enviando imagens para a nuvem…"); for (const m of mItems) await Cloud.uploadMedia(m.name, m.blob); }
  const styleRows = Object.entries(models).map(([id, m]) => ({ id: "m:" + id, css: m.css || "" }));
  await DB.putMany("styles", styleRows); styleRows.forEach(s => S.styles.set(s.id, s.css));
  const rows = q("select c.id cid,c.did,c.odid,c.ord,n.mid,n.flds,n.tags,n.guid from cards c join notes n on c.nid=n.id order by c.id");
  log(`🎴 ${rows.length} cards encontrados — montando…`);
  const raw = [];
  for (const r of rows) {
    const m = models[r.mid]; if (!m) continue;
    const vals = String(r.flds).split("\x1f"); const F = {}; m.flds.forEach((n, i) => F[n] = vals[i] || "");
    const deckName = forcedDeck || decks[r.odid || r.did] || decks[r.did] || "Importados";
    const tpl = m.type === 1 ? m.tmpls[0] : m.tmpls[r.ord]; if (!tpl) continue;
    const extra = { Tags: String(r.tags || "").trim(), Deck: deckName, Subdeck: deckName.split("::").pop(), Card: "", Type: m.name };
    const qh = fixMediaRefs(renderTemplate(tpl.qfmt, F, r.ord, false, "", extra));
    const ah = fixMediaRefs(renderTemplate(tpl.afmt, F, r.ord, true, qh, extra));
    raw.push({ id: "a:" + r.guid + ":" + r.ord, deck: deckName, q: qh, a: ah, style: "m:" + r.mid, tags: String(r.tags || "").trim().split(/\s+/).filter(Boolean) });
  }
  db.close();
  return upsertUser(raw);
}
async function importText(text, forcedDeck, log) {
  const t = text.trim();
  if (/^[\[{]|```/.test(t) || t.includes('"cards"') || t.includes('"frente"')) {
    let tot = { novos: 0, atual: 0 };
    for (const o of extractJSON(t)) {
      if (o && /^codice360x-backup/.test(o.formato || "")) { await restoreBackup(o); log("🛟 Backup restaurado."); return { novos: (o.user || o.cards || []).length, atual: 0 }; }
      const nm = await storeMediaMap(o.midia || o.media); if (nm) log(`🖼️ ${nm} imagens`);
      const r = await upsertUser(normalizeCards(o, forcedDeck)); tot.novos += r.novos; tot.atual += r.atual;
    }
    return tot;
  }
  const cards = parseTextLines(t, forcedDeck);
  if (!cards.length) throw new Error("Não reconheci o formato. Cole o JSON da IA ou linhas 'frente ; verso'.");
  return upsertUser(cards);
}
async function importFiles(files, forcedDeck) {
  const box = document.createElement("div"); box.className = "panel"; $("#impLog").prepend(box);
  const log = m => { box.innerHTML += `<div>${m}</div>`; };
  for (const f of files) {
    log(`<b>📄 ${esc(f.name)}</b>`);
    try {
      const r = /\.(apkg|colpkg)$/i.test(f.name) ? await importApkg(f, forcedDeck, log) : await importText(await f.text(), forcedDeck, log);
      log(`✅ <b class="rv">${r.novos} novos</b> · ${r.atual} atualizados (progresso mantido)${Cloud.on ? " · ☁️ sincronizando" : ""}`);
    } catch (e) { console.error(e); log(`❌ <span style="color:var(--red)">${esc(e.message || e)}</span>`); }
  }
  rerender();
}

/* ---------------- Backup ---------------- */
const blobToDataURL = b => new Promise(r => { const fr = new FileReader(); fr.onload = () => r(fr.result); fr.readAsDataURL(b); });
async function exportBackup() {
  toast("⏳ Gerando backup…");
  const media = {}; for (const m of await DB.all("media")) media[m.name] = await blobToDataURL(m.blob);
  const data = { formato: "codice360x-backup-v2", app: APP_VERSION, data: new Date().toISOString(), user: [...S.user.values()], prog: [...S.prog.values()], styles: await DB.all("styles"), settings: S.settings, logs: S.logs, media };
  const json = JSON.stringify(data), name = `codice360x-backup-${today()}.json`;
  if (Cloud.dl) { try { await Cloud.dl.save({ filename: name, data: new Blob([json], { type: "application/json" }) }); toast("✅ Backup salvo"); return; } catch (e) { if (e && e.code === "declined") return toast("Backup cancelado."); } }
  const a = document.createElement("a"); a.href = URL.createObjectURL(new Blob([json], { type: "application/json" })); a.download = name; document.body.appendChild(a); a.click(); a.remove();
  toast(`✅ Backup com ${S.user.size} cards próprios e ${S.prog.size} progressos.`);
}
async function restoreBackup(o) {
  const now = Date.now();
  if (o.formato === "codice360x-backup-v1") { // backup da v1: cards com srs embutido
    for (const c of o.cards || []) { if (c.srs && c.srs.reps) S.prog.set(c.id, { id: c.id, s: c.srs, susp: !!c.susp, mk: !!c.marked, mod: now }); if (c.origin !== "oficial") S.user.set(c.id, { id: c.id, deck: c.deck, q: c.q, a: c.a, style: c.style || "codice", tags: c.tags || [], mod: now, created: c.created || now }); }
  } else {
    for (const u of o.user || []) S.user.set(u.id, Object.assign({}, u, { mod: now }));
    for (const p of o.prog || []) S.prog.set(p.id, Object.assign({}, p, { mod: now }));
    if (o.settings) { S.settings = Object.assign({}, DEFAULTS, o.settings); await saveSettings(); }
    Object.assign(S.logs, o.logs || {});
  }
  await DB.putMany("user", [...S.user.values()]); await DB.putMany("prog", [...S.prog.values()]); await DB.putMany("styles", o.styles || []);
  (o.styles || []).forEach(s => S.styles.set(s.id, s.css));
  const items = []; for (const [name, v] of Object.entries(o.media || {})) items.push({ name, blob: await (await fetch(v)).blob() });
  await DB.putMany("media", items); items.forEach(i => Cloud.uploadMedia(i.name, i.blob));
  await DB.setMeta("logs", S.logs);
  S.user.forEach(u => Cloud.markU(u.id)); S.prog.forEach(p => Cloud.markP(p.id)); Cloud.markSt();
  rebuildCards();
}

/* ---------------- Contagens e fila ---------------- */
const inDeck = (c, prefix) => !prefix || c.deck === prefix || c.deck.startsWith(prefix + "::");
function counts(prefix) {
  const now = Date.now(), eod = endOfDay(), L = L0();
  let n = 0, l = 0, r = 0;
  for (const c of S.cards) {
    if (c.susp || !inDeck(c, prefix)) continue;
    const s = c.srs;
    if (s.st === "new") n++;
    else if (s.st === "learn" || s.st === "relearn") { if (s.due <= now + S.settings.learnAhead * MIN) l++; }
    else if (s.due <= eod) r++;
  }
  return { n: Math.min(n, Math.max(0, limNew(L) - L.nNew)), l, r: Math.min(r, Math.max(0, limRev(L) - L.nRev)), nAll: n, rAll: r };
}
const Study = { prefix: null, ids: null, cur: null, shown: false, undo: [], t0: 0, total: 0, done: 0, seen: new Set() };
function nextCard() {
  const now = Date.now(), eod = endOfDay(), st = S.settings, L = L0();
  const pool = S.cards.filter(c => !c.susp && (Study.ids ? Study.ids.has(c.id) : inDeck(c, Study.prefix)));
  if (Study.sim) { const id = Study.simOrder.find(i => !Study.seen.has(i) && S.byId.get(i)); return id ? S.byId.get(id) : null; }
  if (Study.ids) {
    const nd = pool.filter(c => !Study.seen.has(c.id) || ((c.srs.st === "learn" || c.srs.st === "relearn") && c.srs.due <= now + st.learnAhead * MIN));
    nd.sort((a, b) => (Study.seen.has(a.id) - Study.seen.has(b.id)) || a.srs.due - b.srs.due);
    return nd[0] || null;
  }
  const learnDue = pool.filter(c => (c.srs.st === "learn" || c.srs.st === "relearn") && c.srs.due <= now).sort((a, b) => a.srs.due - b.srs.due);
  if (learnDue.length) return learnDue[0];
  const rev = limRev(L) - L.nRev > 0 ? pool.filter(c => c.srs.st === "review" && c.srs.due <= eod).sort((a, b) => a.srs.due - b.srs.due) : [];
  const nw = limNew(L) - L.nNew > 0 ? pool.filter(c => c.srs.st === "new").sort((a, b) => a.ord - b.ord) : [];
  if (rev.length && (!nw.length || (L.nRev % 5 !== 4))) return rev[0];
  if (nw.length) return nw[0];
  if (rev.length) return rev[0];
  return pool.filter(c => (c.srs.st === "learn" || c.srs.st === "relearn") && c.srs.due <= now + st.learnAhead * MIN).sort((a, b) => a.srs.due - b.srs.due)[0] || null;
}


/* ---------------- Layout celular / desktop ---------------- */
const LAY = { modes: ["auto", "mobile", "desktop"], ic: { auto: "🔄 Auto", mobile: "📱 Celular", desktop: "🖥️ Desktop" },
  apply() { const m = lsGet("layout") || "auto"; document.documentElement.classList.toggle("lay-mobile", m === "mobile"); document.documentElement.classList.toggle("lay-desktop", m === "desktop"); const b = $("#layBtn"); if (b) { const [ic, ...tx] = this.ic[m].split(" "); b.innerHTML = `${ic}<span class="layTx"> ${tx.join(" ")}</span>`; b.title = "Visualização: " + this.ic[m] + " — toque para alternar"; } },
  next() { const m = lsGet("layout") || "auto"; const n = this.modes[(this.modes.indexOf(m) + 1) % 3]; lsSet("layout", n); this.apply(); toast("Visualização: " + this.ic[n]); } };
LAY.apply(); $("#layBtn").onclick = () => LAY.next();
/* ☀️/🌙 Tema claro: classe html.light (CSS em index.html entre LIGHT-START/END; cards via CODICE_LIGHT). Escolha guardada no aparelho. */
const THEME = {
  apply() {
    const L = lsGet("theme") === "light"; document.documentElement.classList.toggle("light", L);
    const m = document.querySelector('meta[name="theme-color"]'); if (m) m.content = L ? "#f4efe2" : "#0b0e13";
    const b = $("#themeBtn"); if (b) { b.textContent = L ? "🌙" : "☀️"; b.title = L ? "Voltar ao tema escuro" : "Versão clara"; }
    for (const el of document.querySelectorAll("*")) if (el.shadowRoot) { const st = el.shadowRoot.getElementById("lt"), c = el.shadowRoot.querySelector(".card"); if (st) st.textContent = L ? CODICE_LIGHT : ""; if (c) { c.classList.toggle("nightMode", !L); c.classList.toggle("night_mode", !L); } }
    if (["", "#inicio"].includes(location.hash)) try { refreshHome(); } catch (e) {}
  },
  toggle() { lsSet("theme", lsGet("theme") === "light" ? "dark" : "light"); this.apply(); }
};
THEME.apply(); $("#themeBtn").onclick = () => THEME.toggle();

/* ---------------- Questões (TEMI / R3) ---------------- */
const DIVS = { temi: "🏛️ TEMI 2028", r3: "🩺 R3 Clínica Médica" };
const QZ = { div: lsGet("qzDiv") || "temi", tema: "", data: null, block: null, i: 0, ok: 0, done: false, pickd: null,
  async load() { if (!this.data) this.data = await fetch("data/questoes.json").then(r => r.json()).catch(() => ({ temi: [], r3: [] })); },
  async open() { await this.load(); this.block ? this.show() : this.home(); },
  list() { return (this.data[this.div] || []).filter(q => !this.tema || q.tema === this.tema); },
  home() {
    this.block = null; const all = this.data[this.div] || [], R = QRES(), feitas = all.filter(q => R[q.id]), certas = feitas.filter(q => R[q.id][0]).length;
    const temas = [...new Set(all.map(q => q.tema))].sort((a, b) => a.localeCompare(b, "pt"));
    const lst = this.list(), pend = lst.filter(q => !R[q.id]).length, err = lst.filter(q => R[q.id] && !R[q.id][0]).length;
    $("#qzHost").innerHTML = `<div class="divTabs">${Object.entries(DIVS).map(([k, v]) => `<button class="btn ${k === this.div ? "gold" : ""}" data-div="${k}">${v}</button>`).join("")}</div>
     <div class="stats" style="margin:12px 0"><div class="stat"><b>${all.length}</b><span>questões</span></div><div class="stat"><b class="n">${feitas.length}</b><span>respondidas</span></div>
      <div class="stat"><b class="rv">${feitas.length ? Math.round(100 * certas / feitas.length) : 0}%</b><span>acerto (última tentativa)</span></div><div class="stat"><b style="color:var(--gold2)">${all.length - feitas.length}</b><span>inéditas</span></div></div>
     <div class="panel"><div class="metaRow"><label>📚 Tema:</label><select id="qzTema"><option value="">Todos os temas (${all.length})</option>${temas.map(t => `<option ${t === this.tema ? "selected" : ""}>${esc(t)}</option>`).join("")}</select></div>
      <div class="metaRow"><button class="btn gold" data-st="10">▶️ Bloco de 10</button><button class="btn" data-st="20">▶️ Bloco de 20</button><button class="btn" data-st="new">🆕 Inéditas (${pend})</button><button class="btn" data-st="err" ${err ? "" : "disabled"}>🔁 Só as erradas (${err})</button><button class="btn" data-st="all">📚 Todas em ordem (${lst.length})</button></div>
      <p class="metaNow">🗺️ Veja onde você acerta e erra em <a href="#jornada" style="color:var(--cy)">Jornada › Mapa de domínio</a>.</p>
      <p class="metaNow">⌨️ Atalhos: <span class="kbd">A</span>–<span class="kbd">E</span> ou <span class="kbd">1</span>–<span class="kbd">5</span> responder · <span class="kbd">Enter</span> próxima · ✨ +15 XP por acerto, +5 por tentativa.</p></div>`;
    $$("#qzHost [data-div]").forEach(b => b.onclick = () => { this.div = b.dataset.div; lsSet("qzDiv", this.div); this.tema = ""; this.home(); });
    $("#qzTema").onchange = e => { this.tema = e.target.value; this.home(); };
    $$("#qzHost [data-st]").forEach(b => b.onclick = () => {
      const R = QRES(), l = this.list(), k = b.dataset.st, sh = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
      const fresh = sh(l.filter(q => !R[q.id])), old = sh(l.filter(q => R[q.id]));
      const pick = k === "all" ? l : k === "new" ? fresh : k === "err" ? sh(l.filter(q => R[q.id] && !R[q.id][0])) : fresh.concat(old).slice(0, +k);
      if (!pick.length) return toast("Nenhuma questão nesse filtro.");
      this.block = pick; this.i = 0; this.ok = 0; this.pickd = null; this.show();
    });
  },
  show() {
    const q = this.block[this.i]; if (!q) return this.end();
    this.pickd = null;
    const QV = (S.logs._qv = S.logs._qv || {}); if (!QV[q.id]) { QV[q.id] = 1; addXP(1, "leitura", "r"); saveLog(); }
    $("#qzHost").innerHTML = `<div id="studyTop"><div class="grow">❓ ${DIVS[this.div]} · <b>${esc(q.tema)}</b></div><div class="cnt">${this.i + 1}/${this.block.length} · ✅ ${this.ok}</div></div>
     <div class="progress"><i style="width:${100 * this.i / this.block.length}%"></i></div>
     <div class="panel qz"><div class="qzEnun">${q.enun}</div><div class="qzAlts">${q.alts.map((a, i) => `<button class="qzAlt" data-a="${i}"><b>${"ABCDE"[i]}</b><span>${a}</span></button>`).join("")}</div><div id="qzCom"></div></div>
     <div class="metaRow" style="justify-content:center"><button class="btn" id="qzQuit">⏹️ Encerrar bloco</button></div>`;
    $$("#qzHost .qzAlt").forEach(b => b.onclick = () => this.pick(+b.dataset.a));
    $("#qzQuit").onclick = () => this.end(); window.scrollTo({ top: 0 });
  },
  pick(i) {
    const q = this.block && this.block[this.i]; if (!q || this.pickd != null || i >= q.alts.length) return; this.pickd = i;
    const ok = i === q.gab, R = QRES(), prev = R[q.id], L = L0();
    R[q.id] = [ok ? 1 : 0, (prev ? prev[1] : 0) + 1, (prev ? prev[2] : 0) + (ok ? 1 : 0), Date.now()]; L.qN = (L.qN || 0) + 1;
    if (ok) this.ok++;
    addXP(ok ? (prev && prev[2] ? 5 : 15) : 5, ok ? "acerto" : "tentativa", "q"); saveLog();
    $$("#qzHost .qzAlt").forEach((b, k) => { b.disabled = true; if (k === q.gab) b.classList.add("ok"); else if (k === i) b.classList.add("bad"); });
    const QC = (S.logs._qc = S.logs._qc || {}), lido = !!QC[q.id];
    const alts = q.porque ? `<div class="qzWhy">${q.alts.map((a, k) => `<div class="${k === q.gab ? "ok" : ""}"><b>${"ABCDE"[k]}</b> ${k === q.gab ? "✅" : "❌"} ${q.porque[k] || ""}</div>`).join("")}</div>` : "";
    $("#qzCom").innerHTML = `<div class="qzRes ${ok ? "ok" : "bad"}">${ok ? "✅ Correto!" : `❌ Gabarito: <b>${"ABCDE"[q.gab]}</b>`}</div>
      <div class="qzExp"><b>💡 Comentário</b><br>${q.com}${alts ? `<div style="margin-top:8px"><b>🔍 Alternativa por alternativa</b></div>${alts}` : ""}${q.pega ? `<div class="qzPega">🎯 <b>Pegadinha de prova:</b> ${q.pega}</div>` : ""}</div>${q.ref ? `<div class="qzRef">📚 ${esc(q.ref)}</div>` : ""}
      <div class="metaRow" style="justify-content:space-between">${lido ? `<span class="chk on">✅ Comentário lido</span>` : `<button class="btn" id="qzChk">☑️ Li o comentário (+3 XP)</button>`}<button class="btn gold" id="qzNext">${this.i + 1 < this.block.length ? "Próxima ▶" : "🏁 Ver resultado"}</button></div>`;
    $("#qzNext").onclick = () => this.next();
    const ck = $("#qzChk"); if (ck) ck.onclick = () => { QC[q.id] = Date.now(); const L = L0(); L.qcN = (L.qcN || 0) + 1; addXP(3, "comentário", "r"); saveLog(); ck.outerHTML = `<span class="chk on">✅ Comentário lido</span>`; };
  },
  next() { if (this.pickd == null) return; this.i++; this.show(); },
  end() {
    const n = this.i + (this.pickd != null && this.block[this.i] ? 1 : 0), pc = n ? Math.round(100 * this.ok / n) : 0;
    if (n) { addSim({ k: "q", deck: `Questões ${this.div === "temi" ? "TEMI" : "R3"}${this.tema ? "::" + this.tema : ""}`, ok: this.ok, n }); saveLog(); }
    this.block = null;
    $("#qzHost").innerHTML = `<div class="empty"><div style="font-size:46px">${pc >= 85 ? "🏆" : pc >= 70 ? "🎯" : "📚"}</div><h2>Bloco concluído</h2><p>Acertos: <b>${this.ok}</b>/${n} · <b>${pc}%</b> ${pc >= 85 ? "🟢" : pc >= 70 ? "🟡" : "🔴"}</p><div class="metaRow" style="justify-content:center"><button class="btn gold" id="qzBack">❓ Voltar às questões</button><a class="btn" href="#inicio">🏠 Início</a></div></div>`;
    $("#qzBack").onclick = () => this.home();
  } };

/* ---------------- Micropartículas (TEMI / R3) ---------------- */
const MC = { div: lsGet("mcDiv") || "temi", tema: "", data: null, i: 0, t0: 0,
  async load() {   // guarda uma cópia no aparelho para abrir sem internet
    if (this.data) return;
    try { const r = await fetch("data/micro.json"); if (!r.ok) throw new Error(r.status); this.data = await r.json(); DB.setMeta("mc:data", this.data).catch(() => {}); }
    catch (e) { this.data = (await DB.meta("mc:data", null).catch(() => null)) || { temi: [], r3: [] }; }
  },
  async open() { await this.load(); this.render(); },
  list() { return (this.data[this.div] || []).filter(m => !this.tema || m.tema === this.tema); },
  render() {
    const all = this.data[this.div] || [], M = MRES(), lidas = all.filter(m => M[m.id]).length, l = this.list();
    if (this.i >= l.length) this.i = Math.max(0, l.length - 1);
    const m = l[this.i], temas = [...new Set(all.map(x => x.tema))].sort((a, b) => a.localeCompare(b, "pt"));
    $("#mcHost").innerHTML = `<div class="divTabs">${Object.entries(DIVS).map(([k, v]) => `<button class="btn ${k === this.div ? "gold" : ""}" data-div="${k}">${v}</button>`).join("")}</div>
     <div class="metaRow"><select id="mcTema"><option value="">Todos os temas (${all.length})</option>${temas.map(t => `<option ${t === this.tema ? "selected" : ""}>${esc(t)}</option>`).join("")}</select><span class="metaNow">📖 Lidas: <b>${lidas}</b>/${all.length}</span><button class="btn sm" id="mcJump">⏭️ Próxima não lida</button></div>
     <div class="progress"><i style="width:${l.length ? 100 * (this.i + 1) / l.length : 0}%"></i></div>
     ${m ? `<div class="mcCard ${M[m.id] ? "lida" : ""}"><div class="mcTop"><span class="pill">${esc(m.tema)}</span><span class="mcN">${this.i + 1}/${l.length}${M[m.id] ? " · ✅ lida" : ""}</span></div>
       <div class="mcEmoji">${m.emoji || "💊"}</div><h2 class="mcTit">${m.titulo}</h2><div class="mcTxt">${m.texto}</div>${m.gancho ? `<div class="mcHook">🧠 ${m.gancho}</div>` : ""}
       ${m.comentario ? `<div class="qzExp mcCom"><b>💬 Comentário</b><br>${m.comentario}</div>` : ""}
       <div class="metaRow" style="justify-content:flex-end">${M[m.id] ? `<span class="chk on">✅ Lida e comentário conferido</span>` : `<button class="btn gold" id="mcChk">☑️ Li a micropartícula${m.comentario ? " e o comentário" : ""} (+${m.comentario ? 3 : 2} XP)</button>`}</div></div>` : `<p class="empty">Nenhuma micropartícula.</p>`}
     <div class="metaRow" style="justify-content:center"><button class="btn" id="mcPrev">◀ Anterior</button><button class="btn gold" id="mcNext">Próxima ▶</button></div>
     <p class="metaNow" style="text-align:center">⌨️ <span class="kbd">←</span> <span class="kbd">→</span> navegar · <span class="kbd">Enter</span> marcar como lida · ✨ XP só com o ☑️ de leitura</p>`;
    $$("#mcHost [data-div]").forEach(b => b.onclick = () => { this.div = b.dataset.div; lsSet("mcDiv", this.div); this.tema = ""; this.i = 0; this.render(); });
    $("#mcTema").onchange = e => { this.tema = e.target.value; this.i = 0; this.render(); };
    $("#mcPrev").onclick = () => this.go(-1); $("#mcNext").onclick = () => this.go(1);
    $("#mcJump").onclick = () => { const k = l.findIndex(x => !MRES()[x.id]); if (k < 0) return toast("🎉 Todas lidas neste filtro!"); this.i = k; this.render(); };
    const ck = $("#mcChk"); if (ck) ck.onclick = () => this.check();
    this.t0 = Date.now();
  },
  check() {
    const m = this.list()[this.i]; if (!m || MRES()[m.id]) return;
    MRES()[m.id] = Date.now(); const L = L0(); L.mN = (L.mN || 0) + 1; addXP(m.comentario ? 3 : 2, "leitura", "m"); saveLog(); this.render();
  },
  go(d) {
    const l = this.list(), m = l[this.i];
    this.i = Math.max(0, Math.min(l.length - 1, this.i + d)); this.render();
  } };


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

/* ---------------- Mnemônicos (TEMI / R3) ----------------
   Progresso em S.logs._n: { id: { n: treinos, ok: acertos, s: acertos seguidos, t: último treino, f: favoritou em, u: desfavoritou em } }
   Dominado = 2 acertos seguidos. Sincroniza junto com os registros (nuvem do Claude, Gist e Ponte). */
const MN = { div: lsGet("mnDiv") || "temi", tema: "", filt: "", q: "", mode: "lista", data: null, lim: 24, cur: null, hint: false, shown: false, sess: { n: 0, ok: 0 },
  nz: s => String(s || "").normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase(),
  async load() {
    if (this.data) return;
    try { const r = await fetch("data/mnemonicos.json"); if (!r.ok) throw new Error(r.status); this.data = await r.json(); DB.setMeta("mn:data", this.data).catch(() => {}); }
    catch (e) { this.data = (await DB.meta("mn:data", null).catch(() => null)) || { temi: [], r3: [] }; }
  },
  async open() { await this.load(); this.render(); },
  st(id) { return NRES()[id] || {}; },
  dom(id) { return (this.st(id).s || 0) >= 2; },
  fav(id) { const e = this.st(id); return (e.f || 0) > (e.u || 0); },
  all() { return this.data[this.div] || []; },
  list() {
    const q = this.nz(this.q).trim(), f = this.filt;
    return this.all().filter(m => (!this.tema || m.tema === this.tema)
      && (!f || (f === "fav" && this.fav(m.id)) || (f === "pend" && !this.dom(m.id)) || (f === "dom" && this.dom(m.id)) || (f === "c" && m.o === "c") || (f === "o" && m.o === "o"))
      && (!q || this.nz(m.t + " " + m.m + " " + m.k.map(k => k.join(" ")).join(" ") + " " + (m.x || "") + " " + (m.c || "")).includes(q)));
  },
  sig(m) { return `<div class="mnSig${m.m.length > 14 ? " long" : ""}">${esc(m.m)}</div>`; },
  body(m) {
    const wide = m.tp !== "a" && m.k.some(k => k[0].length > 6);
    return `<table class="mnTab${wide ? " wide" : ""}">${m.k.map(k => `<tr><td class="l">${esc(k[0])}</td><td>${esc(k[1])}</td></tr>`).join("")}</table>${m.x ? `<div class="mnTip">🎯 ${esc(m.x)}</div>` : ""}${m.c ? `<div class="mnCtx"><b>📖 Contexto</b>${esc(m.c)}</div>` : ""}`;
  },
  orig(m) { return `<span class="mnOrig ${m.o}" title="${m.o === "c" ? "Mnemônico, tríade, regra ou critério consagrado na literatura" : "Sigla criada no CÓDICE 360X para memorizar o conteúdo"}">${m.o === "c" ? "🏛️ Clássico" : "⚒️ 360X"}</span>`; },
  foot(m) { const e = this.st(m.id); return e.n ? `<div class="mnFoot">${this.dom(m.id) ? "✅ Dominado" : "🎯 Em treino"} · ${e.n} treino(s), ${e.ok || 0} acerto(s)</div>` : ""; },
  card(m) {
    return `<div class="mnCard${this.dom(m.id) ? " dom" : ""}"><div class="mcTop"><span class="pill">${esc(m.tema)}</span><span class="mnTools">${this.orig(m)}<button class="mnImg" data-img="${m.id}" title="Gerar cartão-imagem" aria-label="Gerar cartão-imagem">🖼️</button><button class="mnFav" data-fav="${m.id}" title="Favoritar" aria-label="Favoritar">${this.fav(m.id) ? "⭐" : "☆"}</button></span></div>
      <div class="mnTit">${esc(m.t)}</div>${this.sig(m)}${this.body(m)}${this.foot(m)}</div>`;
  },
  head() {
    const all = this.all(), temas = [...new Set(all.map(x => x.tema))], nDom = all.filter(m => this.dom(m.id)).length, nFav = all.filter(m => this.fav(m.id)).length, hoje = (S.logs[today()] || {}).nN || 0;
    const F = [["", "Todos"], ["pend", "🎯 Ainda não dominados"], ["dom", "✅ Dominados"], ["fav", "⭐ Favoritos"], ["c", "🏛️ Clássicos"], ["o", "⚒️ Criados no 360X"]];
    return `<div class="divTabs">${Object.entries(DIVS).map(([k, v]) => `<button class="btn ${k === this.div ? "gold" : ""}" data-div="${k}">${v}</button>`).join("")}</div>
     <div class="metaRow"><button class="btn ${this.mode === "lista" ? "cy" : ""}" data-mode="lista">📖 Consultar</button><button class="btn ${this.mode === "treino" ? "cy" : ""}" data-mode="treino">🎲 Treinar</button>
      <span class="metaNow">🧠 Dominados: <b>${nDom}</b>/${all.length} · ⭐ ${nFav} · hoje: ${hoje} treino(s)</span><button class="btn sm" id="mnFavImg" title="Cartões-imagem dos favoritos desta divisão">🖼️ Cartões dos ⭐</button></div>
     <div class="progress"><i style="width:${all.length ? 100 * nDom / all.length : 0}%"></i></div>
     <div class="mnBar"><select id="mnTema"><option value="">Todos os temas (${all.length})</option>${temas.map(t => `<option ${t === this.tema ? "selected" : ""} value="${esc(t)}">${esc(t)} (${all.filter(x => x.tema === t).length})</option>`).join("")}</select>
      <select id="mnFilt">${F.map(([v, l]) => `<option value="${v}" ${v === this.filt ? "selected" : ""}>${l}</option>`).join("")}</select>
      ${this.mode === "lista" ? `<input type="search" id="mnQ" placeholder="🔎 Buscar sigla, tema ou palavra" value="${esc(this.q)}">` : ""}</div>`;
  },
  render() {
    if (!this.data) return;
    const host = $("#mnHost"); if (!host) return;
    if (this.mode === "treino") { if (!this.cur || !this.list().some(m => m.id === this.cur.id)) this.pick(); host.innerHTML = this.head() + this.train(); }
    else {
      const l = this.list(), show = l.slice(0, this.lim);
      host.innerHTML = this.head() + (l.length ? `<p class="metaNow">${l.length} mnemônico(s) neste filtro · 🏛️ consagrado na literatura · ⚒️ sigla criada aqui</p><div class="mnGrid">${show.map(m => this.card(m)).join("")}</div>
        ${l.length > show.length ? `<div class="metaRow" style="justify-content:center"><button class="btn" id="mnMore">⬇️ Mostrar mais (${l.length - show.length} restantes)</button></div>` : ""}` : `<p class="empty">Nenhum mnemônico neste filtro.</p>`);
    }
    this.bind();
  },
  train() {
    const m = this.cur, l = this.list();
    if (!m) return `<p class="empty">Nenhum mnemônico neste filtro para treinar.</p>`;
    const top = `<div class="mcTop"><span class="pill">${esc(m.tema)}</span><span class="mnTools">${this.orig(m)}<button class="mnFav" data-fav="${m.id}" title="Favoritar" aria-label="Favoritar">${this.fav(m.id) ? "⭐" : "☆"}</button></span></div>`;
    const ses = `<p class="metaNow" style="text-align:center">Sessão: <b>${this.sess.ok}</b> lembrado(s) de ${this.sess.n} · ${l.length} no filtro · ⌨️ <span class="kbd">Espaço</span> revelar · <span class="kbd">1</span> <span class="kbd">2</span> <span class="kbd">3</span> responder</p>`;
    if (!this.shown) return `<div class="mnCard mnTrain">${top}<div class="mnAsk">🧠 Qual é o mnemônico?</div><div class="mnTit">${esc(m.t)}</div>
      ${this.hint ? this.sig(m) + `<p class="metaNow" style="text-align:center">Agora lembre o que cada parte significa.</p>` : ""}
      <div class="mnAns">${this.hint ? "" : `<button class="btn" id="mnHint">💡 Mostrar só a sigla</button>`}<button class="btn gold" id="mnShow">👁️ Revelar</button></div></div>${ses}`;
    return `<div class="mnCard mnTrain">${top}<div class="mnTit">${esc(m.t)}</div>${this.sig(m)}${this.body(m)}
      <div class="mnAns"><button class="btn danger" data-g="0">❌ Não lembrei</button><button class="btn" data-g="1">🟡 Em parte (+1 XP)</button><button class="btn gold" data-g="2">✅ Lembrei (+2 XP)</button></div></div>${ses}`;
  },
  pick() {
    const l = this.list().filter(m => !this.cur || m.id !== this.cur.id), R = NRES();
    if (!l.length) { this.cur = this.list()[0] || null; this.hint = this.shown = false; return; }
    const sc = m => { const e = R[m.id]; return e && e.n ? (e.s || 0) * 1e13 + (e.t || 0) : -1; };
    const ord = l.map(m => [sc(m), Math.random(), m]).sort((a, b) => a[0] - b[0] || a[1] - b[1]);
    const pool = ord[0][0] < 0 ? ord.filter(x => x[0] < 0) : ord.slice(0, Math.min(5, ord.length));
    this.cur = pool[Math.floor(Math.random() * pool.length)][2]; this.hint = this.shown = false;
  },
  answer(g) {
    const m = this.cur; if (!m || !this.shown) return;
    const R = NRES(), e = R[m.id] = Object.assign({}, R[m.id] || {}), L = L0(), was = (e.s || 0) >= 2;
    e.n = (e.n || 0) + 1; e.t = Date.now();
    if (g === 2) { e.ok = (e.ok || 0) + 1; e.s = (e.s || 0) + 1; } else e.s = g === 1 ? Math.min(e.s || 0, 1) : 0;
    L.nN = (L.nN || 0) + 1; this.sess.n++; if (g === 2) this.sess.ok++;
    if (g) addXP(g, "mnemônico", "n");
    if (!was && e.s >= 2) toast("✅ Mnemônico dominado!");
    saveLog(); this.pick(); this.render();
  },
  toggleFav(id, btn) { const R = NRES(), e = R[id] = Object.assign({}, R[id] || {}), on = (e.f || 0) > (e.u || 0); e[on ? "u" : "f"] = Date.now(); if (btn) btn.textContent = on ? "☆" : "⭐"; saveLog(); },
  bind() {
    const host = $("#mnHost");
    $$("[data-div]", host).forEach(b => b.onclick = () => { this.div = b.dataset.div; lsSet("mnDiv", this.div); this.tema = ""; this.lim = 24; this.cur = null; this.render(); });
    $$("[data-mode]", host).forEach(b => b.onclick = () => { this.mode = b.dataset.mode; this.lim = 24; this.cur = null; this.sess = { n: 0, ok: 0 }; this.render(); });
    const t = $("#mnTema"), f = $("#mnFilt"), q = $("#mnQ"), more = $("#mnMore"), hint = $("#mnHint"), show = $("#mnShow");
    if (t) t.onchange = e => { this.tema = e.target.value; this.lim = 24; this.cur = null; this.render(); };
    if (f) f.onchange = e => { this.filt = e.target.value; this.lim = 24; this.cur = null; this.render(); };
    if (q) q.oninput = e => { this.q = e.target.value; this.lim = 24; clearTimeout(this._qt); this._qt = setTimeout(() => { this.render(); const n = $("#mnQ"); if (n) { n.focus(); n.setSelectionRange(n.value.length, n.value.length); } }, 250); };
    if (more) more.onclick = () => { this.lim += 24; this.render(); };
    if (hint) hint.onclick = () => { this.hint = true; this.render(); };
    if (show) show.onclick = () => { this.shown = true; this.render(); };
    $$("[data-g]", host).forEach(b => b.onclick = () => this.answer(+b.dataset.g));
    $$("[data-fav]", host).forEach(b => b.onclick = () => this.toggleFav(b.dataset.fav, b));
    $$("[data-img]", host).forEach(b => b.onclick = () => CARDIMG.show([this.all().find(m => m.id === b.dataset.img)]));
    const fi = $("#mnFavImg", host); if (fi) fi.onclick = () => CARDIMG.show(this.all().filter(m => this.fav(m.id)), "Favoritos " + DIVS[this.div]);
  },
  key(e) {
    if (this.mode !== "treino" || !this.cur) return;
    if (!this.shown) { if (e.code === "Space" || e.key === "Enter") { e.preventDefault(); this.shown = true; this.render(); } else if (e.key === "d" || e.key === "D") { e.preventDefault(); this.hint = true; this.render(); } return; }
    const g = "123".indexOf(e.key); if (g >= 0) { e.preventDefault(); this.answer(g); }
  } };

/* ---------------- 🕊️ Honra: guia espiritual, bússolas de decisão e fluxo ----------------
   Dados em data/honra.json (gerado por tools/ho/build_ho.py). Cópia no aparelho para abrir sem internet.
   Progresso em S.logs._h (mesmo formato de _n: n, ok, s, t, f, u) — sincroniza junto com os registros.
   Registro do dia: hN (treinos), hb (sessões de respiração), hf (filtros), hbu (bússolas), hz1–hz3 (exame da noite), hn (Modo Noite concluído), hg (gratidão/intenção).
   Itens próprios (✍️ Meus) em S.logs._hu: { id: { k: "m"|"b", d: {...}, mod, del } } — vence o mod mais recente. */
const HRES = () => (S.logs._h = S.logs._h || {}), HURES = () => (S.logs._hu = S.logs._hu || {});
const HO = { sub: lsGet("hoSub") || "hoje", data: null, tr: "", tema: "", filt: "", q: "", mode: "lista", lim: 24, cur: null, shown: false, hint: false, sess: { n: 0, ok: 0 },
  bu: null, fa: {}, fDone: false, msg: null, br: null,
  SUBS: [["hoje", "📜 Hoje"], ["noite", "🌙 Noite"], ["cards", "🎴 Cards"], ["mn", "🛡️ Mnemônicos"], ["bussola", "🧭 Bússolas"], ["filtro", "⚖️ Filtro"], ["fluxo", "🌬️ Fluxo"], ["meus", "✍️ Meus"]],
  ed: null, nt: null,
  nz: s => String(s || "").normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase(),
  async load() {
    if (this.data) return;
    try { const r = await fetch("data/honra.json"); if (!r.ok) throw new Error(r.status); this.data = await r.json(); DB.setMeta("ho:data", this.data).catch(() => {}); }
    catch (e) { this.data = (await DB.meta("ho:data", null).catch(() => null)) || { cards: [], mn: [], bu: [], filtro: [], temas: [], trads: {} }; }
  },
  async open() { await this.load(); this.render(); },
  st(id) { return HRES()[id] || {}; },
  dom(id) { return (this.st(id).s || 0) >= 2; },
  fav(id) { const e = this.st(id); return (e.f || 0) > (e.u || 0); },
  T(k) { return (this.data.trads || {})[k] || { n: k, e: "📖", c: "#9aa4b2" }; },
  chip(k) { const t = this.T(k); return `<span class="hoTr" style="border-color:${t.c};color:${t.c}">${t.e} ${esc(t.n)}</span>`; },
  mine(k) { return Object.entries(HURES()).filter(([, e]) => e && e.k === k && !e.del && e.d).map(([id, e]) => Object.assign({}, e.d, { id, o: "u", mod: e.mod })); },
  mnAll() { return this.mine("m").concat(this.data.mn); },
  buAll() { return this.mine("b").concat(this.data.bu); },
  all() { return this.sub === "mn" ? this.mnAll() : this.data.cards; },
  list() {
    const q = this.nz(this.q).trim(), f = this.filt, mnK = this.sub === "mn";
    return this.all().filter(x => (!this.tema || x.tema === this.tema) && (mnK || !this.tr || x.tr === this.tr)
      && (!f || (f === "fav" && this.fav(x.id)) || (f === "pend" && !this.dom(x.id)) || (f === "dom" && this.dom(x.id)) || (f === "c" && x.o === "c") || (f === "o" && x.o === "o") || (f === "u" && x.o === "u"))
      && (!q || this.nz(mnK ? x.t + " " + x.m + " " + x.k.map(k => k.join(" ")).join(" ") + " " + (x.x || "") + " " + (x.c || "") : x.q + " " + x.a + " " + x.r + " " + x.ap + " " + this.T(x.tr).n).includes(q)));
  },
  favBtn(id) { return `<button class="mnFav" data-fav="${id}" title="Favoritar" aria-label="Favoritar">${this.fav(id) ? "⭐" : "☆"}</button>`; },
  foot(id) { const e = this.st(id); return e.n ? `<div class="mnFoot">${this.dom(id) ? "✅ Dominado" : "🎯 Em treino"} · ${e.n} treino(s), ${e.ok || 0} acerto(s)</div>` : ""; },
  back(c) { return `<div class="hoA">${esc(c.a)}</div><div class="hoRef">📍 ${esc(c.r)} <small>· paráfrase 360X</small></div><div class="hoAp"><b>🧭 Faça hoje</b>${esc(c.ap)}</div>`; },
  cardC(c) {
    return `<div class="mnCard hoCard${this.dom(c.id) ? " dom" : ""}"><div class="mcTop">${this.chip(c.tr)}<span class="mnTools"><span class="pill">${esc(c.tema)}</span>${this.favBtn(c.id)}</span></div>
      <div class="mnTit">${esc(c.q)}</div>${this.back(c)}${this.foot(c.id)}</div>`;
  },
  cardM(m) {
    return `<div class="mnCard${this.dom(m.id) ? " dom" : ""}"><div class="mcTop"><span class="pill">${esc(m.tema)}</span><span class="mnTools">${this.orig(m)}<button class="mnImg" data-img="${m.id}" title="Gerar cartão-imagem" aria-label="Gerar cartão-imagem">🖼️</button>${this.favBtn(m.id)}</span></div>
      <div class="mnTit">${esc(m.t)}</div>${MN.sig(m)}${MN.body(m)}${this.foot(m.id)}</div>`;
  },
  orig(m) { return m.o === "u" ? `<span class="mnOrig u" title="Criado por você">✍️ Meu</span>` : MN.orig(m);
  },
  tabs() { return `<div class="hoSubs">${this.SUBS.map(([k, l]) => `<button class="btn ${k === this.sub ? "gold" : ""}" data-sub="${k}">${l}</button>`).join("")}</div>`; },
  head() {
    const D = this.data, mnK = this.sub === "mn", all = this.all(), nDom = all.filter(x => this.dom(x.id)).length, nFav = all.filter(x => this.fav(x.id)).length, hoje = (S.logs[today()] || {}).hN || 0;
    const temas = D.temas.concat(all.map(x => x.tema).filter(t => !D.temas.includes(t))).filter((t, i, a) => a.indexOf(t) === i && all.some(x => x.tema === t));
    const F = [["", "Todos"], ["pend", "🎯 Ainda não dominados"], ["dom", "✅ Dominados"], ["fav", "⭐ Favoritos"]].concat(mnK ? [["c", "🏛️ Clássicos das tradições"], ["o", "⚒️ Criados no 360X"], ["u", "✍️ Meus"]] : []);
    return `<div class="metaRow"><button class="btn ${this.mode === "lista" ? "cy" : ""}" data-mode="lista">📖 Consultar</button><button class="btn ${this.mode === "treino" ? "cy" : ""}" data-mode="treino">🎲 Treinar</button>
      <span class="metaNow">🕊️ Dominados: <b>${nDom}</b>/${all.length} · ⭐ ${nFav} · hoje: ${hoje} treino(s)</span>${mnK ? `<button class="btn sm" id="hoFavImg" title="Cartões-imagem dos mnemônicos favoritos">🖼️ Cartões dos ⭐</button>` : ""}</div>
     <div class="progress"><i style="width:${all.length ? 100 * nDom / all.length : 0}%"></i></div>
     <div class="mnBar">${mnK ? "" : `<select id="hoTr"><option value="">Todas as tradições (${all.length})</option>${Object.entries(D.trads).map(([k, t]) => `<option value="${k}" ${k === this.tr ? "selected" : ""}>${t.e} ${esc(t.n)} (${all.filter(x => x.tr === k).length})</option>`).join("")}</select>`}
      <select id="hoTema"><option value="">Todos os temas</option>${temas.map(t => `<option ${t === this.tema ? "selected" : ""} value="${esc(t)}">${esc(t)} (${all.filter(x => x.tema === t).length})</option>`).join("")}</select>
      <select id="hoFilt">${F.map(([v, l]) => `<option value="${v}" ${v === this.filt ? "selected" : ""}>${l}</option>`).join("")}</select>
      ${this.mode === "lista" ? `<input type="search" id="hoQ" placeholder="🔎 Buscar palavra, livro ou referência" value="${esc(this.q)}">` : ""}</div>`;
  },
  pool() {
    const l = this.list(), show = l.slice(0, this.lim), mnK = this.sub === "mn";
    return l.length ? `<p class="metaNow">${l.length} ${mnK ? "mnemônico(s)" : "card(s)"} neste filtro${mnK ? " · 🏛️ lista clássica da tradição · ⚒️ sigla criada aqui" : " · textos parafraseados, com a referência para conferir no original"}</p>
      <div class="mnGrid">${show.map(x => mnK ? this.cardM(x) : this.cardC(x)).join("")}</div>
      ${l.length > show.length ? `<div class="metaRow" style="justify-content:center"><button class="btn" id="hoMore">⬇️ Mostrar mais (${l.length - show.length} restantes)</button></div>` : ""}` : `<p class="empty">Nada neste filtro.</p>`;
  },
  train() {
    const x = this.cur, l = this.list(), mnK = this.sub === "mn";
    if (!x) return `<p class="empty">Nada neste filtro para treinar.</p>`;
    const top = mnK ? `<div class="mcTop"><span class="pill">${esc(x.tema)}</span><span class="mnTools">${this.orig(x)}${this.favBtn(x.id)}</span></div>`
      : `<div class="mcTop">${this.chip(x.tr)}<span class="mnTools"><span class="pill">${esc(x.tema)}</span>${this.favBtn(x.id)}</span></div>`;
    const ses = `<p class="metaNow" style="text-align:center">Sessão: <b>${this.sess.ok}</b> lembrado(s) de ${this.sess.n} · ${l.length} no filtro · ⌨️ <span class="kbd">Espaço</span> revelar · <span class="kbd">1</span> <span class="kbd">2</span> <span class="kbd">3</span> responder</p>`;
    const q = mnK ? `<div class="mnAsk">🛡️ Qual é o mnemônico?</div><div class="mnTit">${esc(x.t)}</div>` : `<div class="mnAsk">🕊️ O que ensina?</div><div class="mnTit">${esc(x.q)}</div>`;
    if (!this.shown) return `<div class="mnCard mnTrain">${top}${q}
      ${this.hint ? (mnK ? MN.sig(x) : `<div class="hoRef" style="text-align:center">📍 ${esc(x.r)}</div>`) : ""}
      <div class="mnAns">${this.hint ? "" : `<button class="btn" id="hoHint">💡 ${mnK ? "Mostrar só a sigla" : "Mostrar a referência"}</button>`}<button class="btn gold" id="hoShow">👁️ Revelar</button></div></div>${ses}`;
    return `<div class="mnCard mnTrain">${top}${q}${mnK ? MN.sig(x) + MN.body(x) : this.back(x)}
      <div class="mnAns"><button class="btn danger" data-g="0">❌ Não lembrei</button><button class="btn" data-g="1">🟡 Em parte (+1 XP)</button><button class="btn gold" data-g="2">✅ Lembrei (+2 XP)</button></div></div>${ses}`;
  },
  pick() {
    const l = this.list().filter(x => !this.cur || x.id !== this.cur.id), R = HRES();
    if (!l.length) { this.cur = this.list()[0] || null; this.hint = this.shown = false; return; }
    const sc = x => { const e = R[x.id]; return e && e.n ? (e.s || 0) * 1e13 + (e.t || 0) : -1; };
    const ord = l.map(x => [sc(x), Math.random(), x]).sort((a, b) => a[0] - b[0] || a[1] - b[1]);
    const pool = ord[0][0] < 0 ? ord.filter(y => y[0] < 0) : ord.slice(0, Math.min(5, ord.length));
    this.cur = pool[Math.floor(Math.random() * pool.length)][2]; this.hint = this.shown = false;
  },
  answer(g) {
    const x = this.cur; if (!x || !this.shown) return;
    const R = HRES(), e = R[x.id] = Object.assign({}, R[x.id] || {}), L = L0(), was = (e.s || 0) >= 2;
    e.n = (e.n || 0) + 1; e.t = Date.now();
    if (g === 2) { e.ok = (e.ok || 0) + 1; e.s = (e.s || 0) + 1; } else e.s = g === 1 ? Math.min(e.s || 0, 1) : 0;
    L.hN = (L.hN || 0) + 1; this.sess.n++; if (g === 2) this.sess.ok++;
    if (g) addXP(g, "honra", "h");
    if (!was && e.s >= 2) toast("🕊️ Dominado!");
    saveLog(); this.pick(); this.render();
  },
  toggleFav(id, btn) { const R = HRES(), e = R[id] = Object.assign({}, R[id] || {}), on = (e.f || 0) > (e.u || 0); e[on ? "u" : "f"] = Date.now(); if (btn) btn.textContent = on ? "☆" : "⭐"; saveLog(); },
  dayIdx(n) { const d = today(); let h = 0; for (const ch of d) h = (h * 31 + ch.charCodeAt(0)) >>> 0; return h % n; },
  hoje() {
    const D = this.data, L = S.logs[today()] || {}, c = this.msg, nDomC = D.cards.filter(x => this.dom(x.id)).length, nDomM = this.mnAll().filter(x => this.dom(x.id)).length, BU = this.buAll();
    const Z = [["hz1", "🤝 Fui leal ao agir pelos outros?"], ["hz2", "🫱 Fui digno de confiança com quem convivo?"], ["hz3", "📖 Pratiquei o que aprendi?"]];
    return `<div class="hoHero"><div class="hoBrasao">🕊️</div><div><h2 style="margin:0">Honra & Guia Espiritual</h2><p class="metaNow" style="margin:4px 0 0">${D.cards.length} cards de 6 tradições · ${this.mnAll().length} mnemônicos de honra · ${BU.length} bússolas · filtro de decisão · respiração</p></div></div>
     <div class="panel hoPanel hoNtCall"><div><b>🌙 Modo Noite · 5 minutos</b><br><span class="metaNow">Respiração → exame → mensagem → gratidão → bênção. ${L.hn ? "✅ Feito hoje." : ""}</span></div><button class="btn gold" data-sub="noite">▶️ Começar</button></div>
     <div class="panel hoPanel"><h3 style="margin-top:0">🧭 Como você está agora?</h3><p class="metaNow">Toque no que mais se parece com o momento — abre a bússola daquela situação.</p>
      <div class="hoChips">${BU.map(b => `<button class="hoChip" data-bu="${b.id}">${b.e} ${esc(b.t)}</button>`).join("")}</div></div>
     <div class="panel hoPanel"><h3 style="margin-top:0">📜 Mensagem de hoje</h3>
      ${c ? `<div class="mnCard hoCard">${`<div class="mcTop">${this.chip(c.tr)}<span class="pill">${esc(c.tema)}</span></div>`}<div class="mnTit">${esc(c.q)}</div>${this.back(c)}</div>
        <div class="metaRow" style="justify-content:center"><button class="btn" id="hoMsg2">🔄 Outra mensagem</button></div>` : `<div class="metaRow"><button class="btn gold" id="hoMsg">📜 Mostrar a mensagem de hoje</button><span class="metaNow">Aparece só quando você pedir.</span></div>`}</div>
     <div class="grid2">
      <div class="panel hoPanel"><h3 style="margin-top:0">🌙 Exame da noite (Zengzi)</h3><p class="metaNow">Analectos 1:4 — três perguntas antes de dormir. +1 XP cada.</p>
       ${Z.map(([k, l]) => `<label class="hoChk"><input type="checkbox" data-hz="${k}" ${L[k] ? "checked disabled" : ""}> ${l}</label>`).join("")}</div>
      <div class="panel hoPanel"><h3 style="margin-top:0">📊 Seu caminho</h3>
       <div class="hoStat"><b>${nDomC}</b><span>cards dominados de ${D.cards.length}</span></div><div class="hoStat"><b>${nDomM}</b><span>mnemônicos dominados de ${this.mnAll().length}</span></div>
       <div class="hoStat"><b>${L.hb || 0}</b><span>respirações guiadas hoje</span></div><div class="hoStat"><b>${(L.hf || 0) + (L.hbu || 0)}</b><span>bússolas e filtros usados hoje</span></div></div></div>
     <p class="foot">🛡️ Conteúdo de reflexão e formação de caráter, com respeito a cada tradição; os textos são paráfrases com referência para conferir no original. 📖 Numeração: Bíblia e Salmos como na Almeida (hebraica; Bíblias católicas numeram vários Salmos com 1 a menos) · Alcorão na numeração padrão de Kufa (a da tradução de Helmi Nasr) · Analectos: número moderno (ctext) e, entre parênteses, o de James Legge. ✅ <b>352/352 referências conferidas</b> (13/11/2026) contra Almeida ACF, Helmi Nasr, Livro de Mórmon/D&amp;C, Sefaria (Avot, Talmud, Mishná), SuttaCentral e o texto chinês dos Analectos; 3 refs afinadas. Não substitui orientação religiosa, psicológica, médica ou jurídica. Em sofrimento intenso: <b>CVV 188</b> (24 h) · <b>SAMU 192</b>.</p>`;
  },
  bussola() {
    const D = this.data, BU = this.buAll(), b = BU.find(x => x.id === this.bu);
    const chips = `<div class="hoChips">${BU.map(x => `<button class="hoChip${x.id === this.bu ? " on" : ""}" data-bu="${x.id}">${x.e} ${esc(x.t)}</button>`).join("")}</div>`;
    if (!b) return `<div class="panel hoPanel"><h3 style="margin-top:0">🧭 Escolha a situação</h3>${chips}</div>`;
    const mns = (b.mn || []).map(s => this.mnAll().find(m => m.m === s)).filter(Boolean), used = ((S.logs[today()] || {}).hbuL || "").split(",").includes(b.id);
    return `<div class="hoComp"><div class="hoCompT">${b.e} ${esc(b.t)}</div><div class="hoSin">🔎 <b>Sinais:</b> ${esc(b.sin)}</div>
       ${b.al ? `<div class="hoAl">${esc(b.al)}</div>` : ""}
       <div class="hoRose"><div class="hoDir dn"><b>⬆️ Norte · princípio</b>${esc(b.N)}</div><div class="hoDir do"><b>⬅️ Oeste · espere e consulte</b>${esc(b.O)}</div>
        <div class="hoCenter"><span>🧭</span><i>${esc(b.q)}</i></div><div class="hoDir dl"><b>➡️ Leste · faça agora</b>${esc(b.L)}</div><div class="hoDir ds"><b>⬇️ Sul · evite</b>${esc(b.S)}</div></div>
       <div class="hoRefs"><b>📍 Fontes:</b> ${(b.refs || []).map(r => `<button class="hoRefB" data-ref="${esc(r.split(" (")[0])}">${esc(r)}</button>`).join("")}</div>
       <div class="metaRow" style="justify-content:flex-end">${b.o === "u" ? `<span class="mnOrig u">✍️ Minha bússola</span><button class="btn" data-edit="${b.id}">✏️ Editar</button>` : `<a class="btn" href="data/media/honra/${b.id}.jpg" target="_blank" rel="noopener" download="Bussola_360X_${b.id}.jpg">🖼️ Cartão para tela de bloqueio</a>`}${used ? `<span class="chk on">✅ Bússola usada hoje</span>` : `<button class="btn gold" id="hoBuOk">☑️ Usei esta bússola (+2 XP)</button>`}</div></div>
     ${mns.length ? `<h3>🛡️ Mnemônicos desta bússola</h3><div class="mnGrid">${mns.map(m => this.cardM(m)).join("")}</div>` : ""}
     <div class="panel hoPanel"><h3 style="margin-top:0">Outras situações</h3>${chips}</div>`;
  },
  filtro() {
    const F = this.data.filtro, A = this.fa, ans = F.filter((_, i) => A[i] != null).length;
    let good = 0, tot = 0, red = [];
    F.forEach((f, i) => { if (A[i] == null) return; tot += f.w; if (A[i] === f.ok) good += f.w; else if (!f.ok && f.w >= 3) red.push(f.q); });
    const pct = tot ? Math.round(100 * good / tot) : 0;
    let v = "";
    if (ans === F.length) v = red.length ? `<div class="hoVer r">🔴 <b>Pare.</b> Sinal de alerta: ${red.map(esc).join(" · ")}<br>Não decida hoje. Verifique por outro canal e fale com alguém de confiança.</div>`
      : pct >= 85 ? `<div class="hoVer g">🟢 <b>Sinal verde (${pct}%).</b> Decisão bem fundamentada. Registre o porquê e siga em paz.</div>`
      : `<div class="hoVer y">🟡 <b>Espere 24–72 h (${pct}%).</b> Consulte alguém de confiança e responda de novo amanhã.</div>`;
    return `<div class="panel hoPanel"><h3 style="margin-top:0">⚖️ Filtro de Qualidade da Decisão 360X</h3><p class="metaNow">Pense numa decisão concreta e responda com honestidade. ${ans}/${F.length} respondidas.</p>
      ${F.map((f, i) => `<div class="hoFq"><span>${i + 1}. ${esc(f.q)}${f.w >= 3 ? " <b title=\"Peso alto\">⚠️</b>" : ""}</span><span class="hoYN"><button class="btn sm ${A[i] === true ? "cy" : ""}" data-fa="${i}" data-v="1">Sim</button><button class="btn sm ${A[i] === false ? "cy" : ""}" data-fa="${i}" data-v="0">Não</button></span></div>`).join("")}
      ${v}<div class="metaRow" style="justify-content:flex-end"><button class="btn" id="hoFReset">🔄 Novo filtro</button>${v && !this.fDone ? `<button class="btn gold" id="hoFOk">☑️ Registrar (+2 XP)</button>` : this.fDone ? `<span class="chk on">✅ Registrado</span>` : ""}</div></div>
     <p class="foot">Pergunta-mãe: <b>HONRA</b> — Honesto? Outros afetados? Necessário agora? Reversível? Alinhado aos valores? · Dois ⚠️ marcados no lado errado = golpe ou impulso até prova em contrário.</p>`;
  },
  MODES: { caixa: ["🟦 Caixa 4-4-4-4", [["Inspire", 4], ["Segure", 4], ["Expire", 4], ["Segure", 4]]], calma: ["🌊 Calmante 4-6", [["Inspire", 4], ["Expire", 6]]], suspiro: ["😮‍💨 Suspiro duplo", [["Inspire", 2], ["Mais um pouco", 1], ["Expire devagar", 6]]] },
  ANCORAS: ["Aquietai-vos (Salmos 46:10)", "Com a dificuldade vem a facilidade (Alcorão 94:5)", "Inspirando, sei que inspiro (MN 118)", "Paz à tua alma (D&C 121:7)", "O sábio não se angustia (Analectos 9:29)", "O Senhor te dê a paz (Números 6:26)", "Basta a cada dia o seu mal (Mateus 6:34)"],
  fluxo() {
    const m = lsGet("hoBr") || "calma", n = +(lsGet("hoBrN") || 6), b = this.br;
    return `<div class="panel hoPanel"><h3 style="margin-top:0">🌬️ Fluxo & Respiração</h3>
      <p class="metaNow">Aqui, "fluxo" é regular respiração e atenção: expirar mais longo que inspirar ajuda o corpo a sair do modo de alerta. Técnica de relaxamento, não tratamento.</p>
      <div class="metaRow">${Object.entries(this.MODES).map(([k, v]) => `<button class="btn ${k === m ? "cy" : ""}" data-br="${k}" ${b ? "disabled" : ""}>${v[0]}</button>`).join("")}
       <select id="hoBrN" ${b ? "disabled" : ""}>${[3, 6, 10, 15].map(x => `<option ${x === n ? "selected" : ""} value="${x}">${x} ciclos</option>`).join("")}</select></div>
      <div class="hoBreath"><div class="hoOrb" id="hoOrb"><span id="hoPh">${b ? "" : "Pronto"}</span><small id="hoCt"></small></div><div class="hoAnc" id="hoAnc">${esc(this.ANCORAS[this.dayIdx(this.ANCORAS.length)])}</div></div>
      <div class="metaRow" style="justify-content:center">${b ? `<button class="btn danger" id="hoBrStop">⏹️ Parar</button>` : `<button class="btn gold" id="hoBrGo">▶️ Começar (+3 XP ao concluir)</button>`}</div></div>`;
  },
  brStart(m, n, onDone) {
    m = m || lsGet("hoBr") || "calma"; n = n || +(lsGet("hoBrN") || 6); const ph = this.MODES[m][1];
    this.br = { m, n, c: 0, i: 0, t: 0, sub: this.sub, onDone }; this.render(true); this.brStep(ph);
  },
  brStep(ph) {
    const b = this.br; if (!b || location.hash !== "#honra" || this.sub !== b.sub) { this.br = null; return; }
    if (b.i >= ph.length) { b.i = 0; b.c++; if (b.c % 2 === 0) { const a = $("#hoAnc"); if (a) a.textContent = this.ANCORAS[(this.dayIdx(this.ANCORAS.length) + b.c / 2) % this.ANCORAS.length]; } }
    if (b.c >= b.n) { this.br = null; const L = L0(); L.hb = (L.hb || 0) + 1; addXP(3, "respiração", "h"); saveLog(); if (b.onDone) return b.onDone(); toast("🌬️ Respiração concluída. Que a paz te acompanhe."); this.render(); return; }
    const [lab, sec] = ph[b.i], orb = $("#hoOrb"), p = $("#hoPh"), ct = $("#hoCt");
    if (!orb) { this.br = null; return; }
    const sc = /Inspire|Mais/.test(lab) ? (lab === "Mais um pouco" ? 1.18 : 1.1) : /Expire/.test(lab) ? 0.62 : null;
    orb.style.transitionDuration = sec + "s"; if (sc) orb.style.transform = `scale(${sc})`;
    p.textContent = lab; let left = sec; ct.textContent = `${left}s · ciclo ${b.c + 1}/${b.n}`;
    clearInterval(b.iv); b.iv = setInterval(() => { left--; if (left > 0 && ct) ct.textContent = `${left}s · ciclo ${b.c + 1}/${b.n}`; }, 1000);
    b.t = setTimeout(() => { clearInterval(b.iv); b.i++; this.brStep(ph); }, sec * 1000);
  },
  brStop() { const b = this.br; if (b) { clearTimeout(b.t); clearInterval(b.iv); } this.br = null; this.render(); },
  render(force) {
    if (!this.data) return;
    const host = $("#hoHost"); if (!host) return;
    if (this.br && this.sub !== this.br.sub) this.brStop();
    let body = "";
    if (this.sub === "hoje") body = this.hoje();
    else if (this.sub === "bussola") body = this.bussola();
    else if (this.sub === "filtro") body = this.filtro();
    else if (this.sub === "meus") body = this.meus();
    else if (this.sub === "noite") { if (this.br && this.br.sub === "noite" && $("#hoOrb") && !force) return; body = this.noite(); }
    else if (this.sub === "fluxo") { if (this.br && $("#hoOrb") && !force) return; body = this.fluxo(); }
    else { if (this.mode === "treino" && (!this.cur || !this.list().some(x => x.id === this.cur.id))) this.pick(); body = this.head() + (this.mode === "treino" ? this.train() : this.pool()); }
    host.innerHTML = this.tabs() + body;
    this.bind();
  },
  go(sub) { this.sub = sub; lsSet("hoSub", sub); this.lim = 24; this.cur = null; this.sess = { n: 0, ok: 0 }; this.render(); const h = $("#hoHost"); if (h) h.scrollIntoView({ block: "start" }); },
  bind() {
    const host = $("#hoHost"), $h = s => $(s, host);
    $$("[data-sub]", host).forEach(b => b.onclick = () => { if (this.br) this.brStop(); this.go(b.dataset.sub); });
    $$("[data-mode]", host).forEach(b => b.onclick = () => { this.mode = b.dataset.mode; this.lim = 24; this.cur = null; this.sess = { n: 0, ok: 0 }; this.render(); });
    const tr = $h("#hoTr"), t = $h("#hoTema"), f = $h("#hoFilt"), q = $h("#hoQ"), more = $h("#hoMore"), hint = $h("#hoHint"), show = $h("#hoShow");
    if (tr) tr.onchange = e => { this.tr = e.target.value; this.lim = 24; this.cur = null; this.render(); };
    if (t) t.onchange = e => { this.tema = e.target.value; this.lim = 24; this.cur = null; this.render(); };
    if (f) f.onchange = e => { this.filt = e.target.value; this.lim = 24; this.cur = null; this.render(); };
    if (q) q.oninput = e => { this.q = e.target.value; this.lim = 24; clearTimeout(this._qt); this._qt = setTimeout(() => { this.render(); const n = $("#hoQ"); if (n) { n.focus(); n.setSelectionRange(n.value.length, n.value.length); } }, 250); };
    if (more) more.onclick = () => { this.lim += 24; this.render(); };
    if (hint) hint.onclick = () => { this.hint = true; this.render(); };
    if (show) show.onclick = () => { this.shown = true; this.render(); };
    $$("[data-g]", host).forEach(b => b.onclick = () => this.answer(+b.dataset.g));
    $$("[data-fav]", host).forEach(b => b.onclick = () => this.toggleFav(b.dataset.fav, b));
    $$("[data-bu]", host).forEach(b => b.onclick = () => { this.bu = b.dataset.bu; this.go("bussola"); });
    $$("[data-img]", host).forEach(b => b.onclick = () => CARDIMG.show([this.mnAll().find(m => m.id === b.dataset.img)]));
    const fi = $h("#hoFavImg"); if (fi) fi.onclick = () => CARDIMG.show(this.mnAll().filter(m => this.fav(m.id)), "Favoritos da Honra");
    $$("[data-ref]", host).forEach(b => b.onclick = () => { this.q = b.dataset.ref; this.tr = ""; this.tema = ""; this.filt = ""; this.mode = "lista"; this.go("cards"); });
    const bo = $h("#hoBuOk"); if (bo) bo.onclick = () => { const L = L0(), ids = (L.hbuL || "").split(",").filter(Boolean); if (ids.includes(this.bu)) return; ids.push(this.bu); L.hbuL = ids.join(","); L.hbu = ids.length; addXP(2, "bússola", "h"); saveLog(); this.render(); };
    const m1 = $h("#hoMsg"), m2 = $h("#hoMsg2"), C = this.data.cards;
    if (m1) m1.onclick = () => { this.msg = C[this.dayIdx(C.length)]; this.render(); };
    if (m2) m2.onclick = () => { this.msg = C[Math.floor(Math.random() * C.length)]; this.render(); };
    $$("[data-hz]", host).forEach(c => c.onchange = () => { if (!c.checked) return; const L = L0(); if (L[c.dataset.hz]) return; L[c.dataset.hz] = 1; addXP(1, "exame da noite", "h"); saveLog(); c.disabled = true; });
    $$("[data-fa]", host).forEach(b => b.onclick = () => { this.fa[+b.dataset.fa] = b.dataset.v === "1"; this.render(); });
    const fr = $h("#hoFReset"), fo = $h("#hoFOk");
    if (fr) fr.onclick = () => { this.fa = {}; this.fDone = false; this.render(); };
    if (fo) fo.onclick = () => { this.fDone = true; const L = L0(); L.hf = (L.hf || 0) + 1; addXP(2, "filtro de decisão", "h"); saveLog(); this.render(); };
    $$("[data-br]", host).forEach(b => b.onclick = () => { lsSet("hoBr", b.dataset.br); this.render(); });
    const bn = $h("#hoBrN"); if (bn) bn.onchange = e => lsSet("hoBrN", e.target.value);
    const bg = $h("#hoBrGo"), bs = $h("#hoBrStop");
    if (bg) bg.onclick = () => this.brStart();
    this.bindMeus(host); this.bindNoite(host);
    if (bs) bs.onclick = () => this.brStop();
  },
  /* ---- ✍️ Meus: criar e editar mnemônicos e bússolas próprios ---- */
  meus() {
    const E = this.ed || (this.ed = { k: "m" }), mns = this.mine("m"), bus = this.mine("b"), T = this.data.temas.concat(["✍️ Pessoal"]);
    const v = k => esc(E[k] == null ? "" : E[k]), inp = (k, ph, big) => big ? `<textarea id="ed_${k}" rows="${big}" placeholder="${ph}">${v(k)}</textarea>` : `<input id="ed_${k}" placeholder="${ph}" value="${v(k)}">`;
    const temaSel = `<select id="ed_tema">${T.map(t => `<option ${t === (E.tema || "✍️ Pessoal") ? "selected" : ""}>${esc(t)}</option>`).join("")}</select>`;
    const itens = E.k === "m" && Array.isArray(E.k2) ? E.k2 : null;
    if (E.k === "m" && E.itens == null && itens) E.itens = itens.map(x => x[0] + " — " + x[1]).join("\n");
    const form = E.k === "m" ? `<div class="hoForm">
       <label>Tema ${temaSel}</label><label>Título (pergunta) ${inp("t", "Ex.: Antes de responder a uma mensagem difícil")}</label>
       <label>Sigla ou rótulo ${inp("m", "Ex.: CALMA")}</label>
       <label>Itens — um por linha (“C — Conte até 10” ou só o texto; as letras da sigla viram rótulos) ${inp("itens", "Conte até 10 (Enter) Afaste-se (Enter) …", 5)}</label>
       <label>🎯 Dica (opcional) ${inp("x", "Frase curta para lembrar")}</label><label>📖 Contexto / fonte (opcional) ${inp("c", "Ex.: Tiago 1:19 — quando uso", 2)}</label></div>`
      : `<div class="hoForm"><label>Emoji e título <span class="hoRow">${inp("e", "🧭")}${inp("t", "Ex.: Reunião tensa com a chefia")}</span></label>
       <label>🔎 Sinais (como reconhecer) ${inp("sin", "O que sinto ou percebo quando isso acontece", 2)}</label>
       <label>⬆️ Norte · princípio ${inp("N", "O valor que me guia", 2)}</label><label>⬇️ Sul · evitar ${inp("S", "O que eu não quero fazer", 2)}</label>
       <label>➡️ Leste · faça agora ${inp("L", "Ação de até 10 minutos", 2)}</label><label>⬅️ Oeste · espere e consulte ${inp("O", "Quem consultar, quanto esperar", 2)}</label>
       <label>🧭 Pergunta-chave ${inp("q", "A pergunta que me centra")}</label><label>📍 Fontes (separe com ;) ${inp("refs", "Provérbios 15:1; Alcorão 41:34")}</label>
       <label>🛡️ Siglas ligadas (separe com ;) ${inp("mn", "FREIO; PAUSA")}</label><label>⚠️ Alerta (opcional) ${inp("al", "Ex.: telefone de apoio")}</label></div>`;
    const row = (x, lab) => `<div class="hoMine"><span>${lab}</span><button class="btn sm" data-edit="${x.id}">✏️ Editar</button></div>`;
    return `<div class="panel hoPanel"><h3 style="margin-top:0">✍️ ${E.id ? "Editar" : "Criar"} ${E.k === "m" ? "mnemônico" : "bússola"}</h3>
      <div class="metaRow">${E.id ? "" : `<button class="btn ${E.k === "m" ? "cy" : ""}" data-ek="m">🛡️ Mnemônico</button><button class="btn ${E.k === "b" ? "cy" : ""}" data-ek="b">🧭 Bússola</button>`}</div>${form}
      <div class="metaRow" style="justify-content:flex-end">${E.id ? `<button class="btn danger" id="edDel">${E.delAsk ? "⚠️ Toque de novo para apagar" : "🗑️ Apagar"}</button><button class="btn" id="edNew">✖️ Cancelar</button>` : ""}<button class="btn gold" id="edSave">💾 Salvar</button></div>
      <p class="metaNow">Seus itens entram nas abas 🛡️ Mnemônicos (filtro ✍️ Meus), 🧭 Bússolas e no treino, e sincronizam entre aparelhos.</p></div>
     <div class="grid2"><div class="panel hoPanel"><h3 style="margin-top:0">🛡️ Meus mnemônicos (${mns.length})</h3>${mns.length ? mns.map(m => row(m, `<b>${esc(m.m)}</b> · ${esc(m.t)}`)).join("") : `<p class="metaNow">Nenhum ainda.</p>`}</div>
      <div class="panel hoPanel"><h3 style="margin-top:0">🧭 Minhas bússolas (${bus.length})</h3>${bus.length ? bus.map(b => row(b, `${b.e || "🧭"} ${esc(b.t)}`)).join("") : `<p class="metaNow">Nenhuma ainda.</p>`}</div></div>`;
  },
  edRead() { const E = this.ed; $$("#hoHost [id^=ed_]").forEach(el => E[el.id.slice(3)] = el.value); return E; },
  edSave() {
    const E = this.edRead(), t = (E.t || "").trim(), sp = s => String(s || "").split(/[;\n]/).map(x => x.trim()).filter(Boolean);
    let d;
    if (E.k === "m") {
      const sig = (E.m || "").trim(), lines = String(E.itens || "").split("\n").map(x => x.trim()).filter(Boolean);
      if (!t || !sig || !lines.length) return toast("Preencha título, sigla e ao menos um item.");
      const letters = [...sig.normalize("NFD").replace(/[̀-ͯ]/g, "")].filter(c => /[A-Za-z0-9]/.test(c));
      const k = lines.map((l, i) => { const m = l.match(/^(.{1,14}?)\s+[—–-]\s+(.+)$/); return m ? [m[1], m[2]] : [letters.length === lines.length ? letters[i].toUpperCase() : String(i + 1), l]; });
      d = { tema: E.tema || "✍️ Pessoal", t, m: sig, k, x: (E.x || "").trim(), c: (E.c || "").trim(), tp: letters.length === lines.length ? "a" : "l" };
    } else {
      if (!t || !(E.N || E.S || E.L || E.O)) return toast("Preencha o título e ao menos uma direção.");
      d = { e: (E.e || "🧭").trim() || "🧭", t, sin: (E.sin || "").trim(), N: (E.N || "").trim(), S: (E.S || "").trim(), L: (E.L || "").trim(), O: (E.O || "").trim(), q: (E.q || "").trim() || "O que é certo fazer agora?", refs: sp(E.refs), mn: sp(E.mn).map(x => x.toUpperCase()), al: (E.al || "").trim() };
    }
    const id = E.id || "hu" + Date.now().toString(36) + Math.random().toString(36).slice(2, 5);
    HURES()[id] = { k: E.k, d, mod: Date.now() }; saveLog(); addXP(2, "criação própria", "h");
    toast(E.id ? "💾 Atualizado" : "✅ Criado e sincronizando"); this.ed = { k: E.k }; this.render();
  },
  edOpen(id) {
    const e = HURES()[id]; if (!e || !e.d) return;
    this.ed = Object.assign({ id, k: e.k }, e.d);
    if (e.k === "m") { this.ed.itens = e.d.k.map(x => x[0] + " — " + x[1]).join("\n"); }
    else { this.ed.refs = (e.d.refs || []).join("; "); this.ed.mn = (e.d.mn || []).join("; "); }
    this.go("meus");
  },
  bindMeus(host) {
    $$("[data-edit]", host).forEach(b => b.onclick = () => this.edOpen(b.dataset.edit));
    if (this.sub !== "meus") return;
    $$("[data-ek]", host).forEach(b => b.onclick = () => { this.ed = { k: b.dataset.ek }; this.render(); });
    const sv = $("#edSave", host), dl = $("#edDel", host), nw = $("#edNew", host);
    if (sv) sv.onclick = () => this.edSave();
    if (nw) nw.onclick = () => { this.ed = { k: this.ed.k }; this.render(); };
    if (dl) dl.onclick = () => { const E = this.edRead(); if (!E.delAsk) { E.delAsk = 1; return this.render(); } HURES()[E.id] = { k: E.k, del: 1, mod: Date.now() }; saveLog(); toast("🗑️ Apagado"); this.ed = { k: E.k }; this.render(); };
  },
  /* ---- 🌙 Modo Noite: 5 minutos guiados ---- */
  NT: [["🌬️", "Respirar", 90], ["🌙", "Exame da noite", 60], ["📜", "Mensagem", 60], ["🙏", "Gratidão e intenção", 60], ["✨", "Bênção", 30]],
  noite() {
    const N = this.nt, L = S.logs[today()] || {};
    if (!N) return `<div class="panel hoPanel hoNt"><div class="hoNtMoon">🌙</div><h2 style="margin:6px 0">Modo Noite · 5 minutos</h2>
      <p class="metaNow">Uma sequência curta para fechar o dia em paz. Avance no seu ritmo; a barra só sugere o tempo.</p>
      <ol class="hoNtList">${this.NT.map(([e, t, s]) => `<li>${e} <b>${t}</b> <small>· ${s >= 60 ? s / 60 + " min" : s + " s"}</small></li>`).join("")}</ol>
      ${L.hn ? `<p class="chk on">✅ Você já fez o Modo Noite hoje — pode repetir quando quiser.</p>` : ""}
      <button class="btn gold" id="ntGo">▶️ Começar</button>
      <div class="hoRem"><b>🔔 Lembrete diário no Calendário</b><span class="metaNow">Cria um evento que se repete todo dia, com alarme, no app Calendário do celular. Nada roda em segundo plano; para parar, apague o evento.</span>
       <div class="metaRow" style="justify-content:center"><input type="time" id="ntTime" value="${esc(lsGet("ntTime") || "03:30")}" aria-label="Horário do lembrete"><button class="btn" id="ntIcs">📅 Baixar lembrete (.ics)</button></div>
       <span class="metaNow">Se o download não abrir aqui, use no iPhone o <a href="${this.GH}downloads/Lembrete_Modo_Noite_360X_0330.ics" target="_blank" rel="noopener">📎 lembrete pronto (03:30)</a>, no app do GitHub Pages.</span></div></div>`;
    const [e, tit, sec] = this.NT[N.i], dots = this.NT.map((x, i) => `<span class="${i < N.i ? "ok" : i === N.i ? "on" : ""}">${x[0]}</span>`).join("");
    let body = "";
    if (N.i === 0) body = `<div class="hoBreath"><div class="hoOrb" id="hoOrb"><span id="hoPh">${this.br ? "" : "Pronto"}</span><small id="hoCt"></small></div><div class="hoAnc" id="hoAnc">${esc(this.ANCORAS[this.dayIdx(this.ANCORAS.length)])}</div></div>
      <div class="metaRow" style="justify-content:center">${this.br ? `<button class="btn danger" id="hoBrStop">⏹️ Parar</button>` : `<button class="btn gold" id="ntBr">▶️ Respirar 9 ciclos (4-6)</button>`}</div>`;
    else if (N.i === 1) body = [["hz1", "🤝 Fui leal ao agir pelos outros hoje?"], ["hz2", "🫱 Fui digno de confiança com quem convivo?"], ["hz3", "📖 Pratiquei o que aprendi?"]].map(([k, l]) => `<label class="hoChk"><input type="checkbox" data-hz="${k}" ${L[k] ? "checked disabled" : ""}> ${l}</label>`).join("") + `<p class="metaNow">Analectos 1:4 — o exame diário de Zengzi. Sem culpa: só observar e ajustar amanhã.</p>`;
    else if (N.i === 2) { const c = this.msg || (this.msg = this.data.cards[this.dayIdx(this.data.cards.length)]); body = `<div class="mnCard hoCard"><div class="mcTop">${this.chip(c.tr)}<span class="pill">${esc(c.tema)}</span></div><div class="mnTit">${esc(c.q)}</div>${this.back(c)}</div>`; }
    else if (N.i === 3) body = `<div class="hoForm"><label>🙏 Três gratidões de hoje <textarea id="ntG" rows="3" placeholder="1.\n2.\n3.">${esc((L.hg || "").split("||")[0] || "")}</textarea></label>
      <label>🎯 Uma intenção para amanhã <input id="ntI" placeholder="Ex.: falar com calma no plantão" value="${esc((L.hg || "").split("||")[1] || "")}"></label></div><p class="metaNow">Fica guardado só no seu registro do dia.</p>`;
    else body = `<div class="hoBless">“Que o Senhor te abençoe e te guarde;<br>que faça resplandecer o seu rosto sobre ti;<br>que volte para ti o seu olhar e te dê a paz.”<small>Números 6:24-26 · paráfrase</small></div>
      <p class="metaNow" style="text-align:center">Solte o dia. O que ficou pendente espera por amanhã. 🌙</p>`;
    return `<div class="panel hoPanel hoNt"><div class="hoDots">${dots}</div><h2 style="margin:8px 0 4px">${e} ${tit}</h2>
      <div class="hoTimer"><i style="animation-duration:${sec}s" key="${N.i}-${N.k || 0}"></i></div>${body}
      <div class="metaRow" style="justify-content:space-between"><button class="btn" id="ntBack" ${N.i ? "" : "disabled"}>◀ Voltar</button>
      ${N.i < this.NT.length - 1 ? `<button class="btn gold" id="ntNext">Próximo ▶</button>` : `<button class="btn gold" id="ntEnd">✅ Concluir (+5 XP)</button>`}</div></div>`;
  },
  GH: "https://aldenirfilho.github.io/intensivahub/flashcards/",
  ics(hhmm) {
    const [h, mi] = String(hhmm || "03:30").split(":").map(Number), p = n => String(n).padStart(2, "0"), d = new Date(); d.setHours(h || 0, mi || 0, 0, 0); if (d < new Date()) d.setDate(d.getDate() + 1);
    const f = x => `${x.getFullYear()}${p(x.getMonth() + 1)}${p(x.getDate())}T${p(x.getHours())}${p(x.getMinutes())}00`, now = new Date(), e = new Date(d.getTime() + 5 * 60000), url = this.GH + "#honra";
    const z = `${now.getUTCFullYear()}${p(now.getUTCMonth() + 1)}${p(now.getUTCDate())}T${p(now.getUTCHours())}${p(now.getUTCMinutes())}00Z`, q = t => t.replace(/([,;\\])/g, "\\$1");
    return ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//CODICE 360X//Modo Noite//PT-BR", "CALSCALE:GREGORIAN", "METHOD:PUBLISH", "BEGIN:VEVENT", `UID:modo-noite-360x-${p(h)}${p(mi)}@codice360x`, `DTSTAMP:${z}`, `DTSTART:${f(d)}`, `DTEND:${f(e)}`, "RRULE:FREQ=DAILY",
      "SUMMARY:🌙 Modo Noite 360X · 5 min", `DESCRIPTION:${q("Respiração 4-6 → exame da noite → mensagem → gratidão → bênção. Abra: " + url)}`, `URL:${url}`,
      "BEGIN:VALARM", "ACTION:DISPLAY", "DESCRIPTION:🌙 Hora do Modo Noite (5 min)", "TRIGGER:PT0M", "END:VALARM", "END:VEVENT", "END:VCALENDAR"].join("\r\n") + "\r\n";
  },
  ntSave() { const g = $("#ntG"), i = $("#ntI"); if (g || i) { const L = L0(); L.hg = (g ? g.value : "") + "||" + (i ? i.value : ""); saveLog(); } },
  bindNoite(host) {
    if (this.sub !== "noite") return;
    const go = $("#ntGo", host), nx = $("#ntNext", host), bk = $("#ntBack", host), en = $("#ntEnd", host), br = $("#ntBr", host);
    if (go) go.onclick = () => { this.nt = { i: 0, k: Date.now() }; this.render(); };
    const ic = $("#ntIcs", host), tm = $("#ntTime", host);
    if (tm) tm.onchange = () => lsSet("ntTime", tm.value);
    if (ic) ic.onclick = () => { const t = (tm && tm.value) || "03:30"; lsSet("ntTime", t); const a = document.createElement("a"); a.href = URL.createObjectURL(new Blob([this.ics(t)], { type: "text/calendar" })); a.download = `Lembrete_Modo_Noite_360X_${t.replace(":", "")}.ics`; document.body.appendChild(a); a.click(); setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 1500); toast("📅 Abra o arquivo e toque em “Adicionar ao Calendário”."); };
    if (br) br.onclick = () => this.brStart("calma", 9, () => { this.nt.i = 1; this.nt.k = Date.now(); this.render(); });
    if (nx) nx.onclick = () => { if (this.br) this.brStop(); this.ntSave(); this.nt.i++; this.nt.k = Date.now(); this.render(); };
    if (bk) bk.onclick = () => { if (this.br) this.brStop(); this.ntSave(); this.nt.i = Math.max(0, this.nt.i - 1); this.nt.k = Date.now(); this.render(); };
    if (en) en.onclick = () => { const L = L0(), first = !L.hn; L.hn = 1; if (first) addXP(5, "modo noite", "h"); saveLog(); this.nt = null; toast("🌙 Boa noite. Que a paz te acompanhe."); this.render(); };
  },
  key(e) {
    if ((this.sub !== "cards" && this.sub !== "mn") || this.mode !== "treino" || !this.cur) return;
    if (!this.shown) { if (e.code === "Space" || e.key === "Enter") { e.preventDefault(); this.shown = true; this.render(); } else if (e.key === "d" || e.key === "D") { e.preventDefault(); this.hint = true; this.render(); } return; }
    const g = "123".indexOf(e.key); if (g >= 0) { e.preventDefault(); this.answer(g); }
  } };

/* ---------------- Jornada: conquistas, ranking semanal e painéis ---------------- */
const ACH_T = { medalha: "🏅 Medalhas", trofeu: "🏆 Troféus", titulo: "📜 Títulos", brasao: "🛡️ Brasões", honra: "🎖️ Honrarias" };
const ACH_BONUS = { medalha: 20, trofeu: 40, titulo: 50, brasao: 80, honra: 150 };
const XPSRC = { c: ["🎴 Flashcards", "#4dd4ff"], s: ["🧪 Simulados", "#ffc14d"], q: ["❓ Questões", "#5be38a"], r: ["📖 Leitura e comentários", "#b48cff"], m: ["💊 Micropartículas", "#ff8fb1"], n: ["🧠 Mnemônicos", "#7fd1b9"], h: ["🕊️ Honra", "#c9b6ff"], a: ["🏆 Conquistas", "#e8c56a"] };
const isoWeek = t => { const d = new Date(t); d.setHours(0, 0, 0, 0); d.setDate(d.getDate() - ((d.getDay() + 6) % 7)); return d.getTime(); };
function jStats() {
  const days = dayLogs().sort((a, b) => a[0].localeCompare(b[0])), act = l => (l.nAns || 0) + (l.qN || 0) + (l.mN || 0) + (l.nN || 0) + (l.hN || 0) + (l.hb || 0) + (l.hn || 0) + (l.sims || []).length > 0;
  const on = new Set(days.filter(([, l]) => act(l)).map(([d]) => d));
  let cur = 0; for (let i = on.has(today()) ? 0 : 1; on.has(dayKey(Date.now() - i * DAY)); i++) cur++;
  let max = 0, run = 0, prev = null; for (const d of [...on].sort()) { const t = new Date(d + "T12:00").getTime(); run = prev && Math.round((t - prev) / DAY) === 1 ? run + 1 : 1; max = Math.max(max, run); prev = t; }
  const sims = days.flatMap(([, l]) => l.sims || []).filter(x => x.n >= 10).map(x => Math.round(100 * x.ok / x.n));
  const Q = S.logs._q || {}, qv = Object.values(Q), qOk = qv.filter(x => x[0]).length;
  const nNew = S.settings.newPerDay || 0, metaDays = days.filter(([, l]) => nNew && (l.nNew || 0) >= nNew).length;
  const wk = {}; for (const [d, l] of days) { const w = isoWeek(new Date(d + "T12:00").getTime()); wk[w] = (wk[w] || 0) + (l.xp || 0); }
  const xs = {}; for (const [, l] of days) for (const [k, v] of Object.entries(l.xs || {})) xs[k] = (xs[k] || 0) + v;
  return { cur, max: Math.max(max, cur), xp: xpTotal(), lv: levelOf(xpTotal()).lv, sims, qAns: qv.length, qAcc: qv.length ? qOk / qv.length : 0, qc: Object.keys(S.logs._qc || {}).length,
    mic: Object.keys(S.logs._m || {}).length, mn: Object.values(S.logs._n || {}).filter(e => e && (e.s || 0) >= 2).length, hon: Object.values(S.logs._h || {}).filter(e => e && (e.s || 0) >= 2).length,
    hb: days.reduce((a, [, l]) => a + (l.hb || 0), 0), hbu: days.reduce((a, [, l]) => a + (l.hbu || 0) + (l.hf || 0), 0), hn: days.reduce((a, [, l]) => a + (l.hn ? 1 : 0), 0), cards: days.reduce((a, [, l]) => a + (l.nAns || 0), 0), metaDays, wk, xs, days };
}
const ACH = { list: [],
  build() {
    const A = (id, tipo, ic, nome, desc, val, goal) => this.list.push({ id, tipo, ic, nome, desc, val, goal });
    [[3, "medalha", "🔥", "Chama Acesa"], [7, "medalha", "🕯️", "Vigília de 7 Dias"], [14, "trofeu", "⚔️", "Quinzena do Cavaleiro"], [30, "trofeu", "🏰", "Cerco de 30 Dias"], [60, "brasao", "🛡️", "Brasão da Constância"], [100, "brasao", "🐉", "Brasão do Dragão"], [180, "honra", "👑", "Honra da Perseverança"], [365, "honra", "🌟", "Honra ao Mérito Anual"]]
      .forEach(([n, t, ic, nm]) => A("st" + n, t, ic, nm, `Sequência de ${n} dias de estudo seguidos`, s => s.max, n));
    const SIM = [[50, "medalha", "🥉", "Medalha de Bronze"], [60, "medalha", "🥈", "Medalha de Prata"], [70, "medalha", "🥇", "Medalha de Ouro"], [80, "trofeu", "🏆", "Troféu de Excelência"], [90, "brasao", "🛡️", "Brasão de Elite"], [100, "honra", "🎖️", "Honra ao Mérito"]];
    for (const [p, t, ic, nm] of SIM) [[1, "I"], [5, "II"], [20, "III"]].forEach(([k, r]) => A(`sim${p}_${k}`, t, ic, `${nm} ${r}`, `${k} simulado(s) ou bloco(s) de questões (≥ 10 itens) com nota ${p === 100 ? "de 100%" : "≥ " + p + "%"}`, s => s.sims.filter(x => x >= p).length, k));
    [[500, "Iniciado do Códice"], [1000, "Escriba"], [2500, "Bacharel das Runas"], [5000, "Mestre de Armas"], [10000, "Cavaleiro da Ordem"], [25000, "Comendador"], [50000, "Grão-Mestre do Códice"], [100000, "Lenda do TEMI"]]
      .forEach(([n, nm]) => A("xp" + n, "titulo", "📜", nm, `Acumular ${n.toLocaleString("pt-BR")} XP`, s => s.xp, n));
    RANKS.forEach((r, i) => { if (i) A("rk" + i, "titulo", r.split(" ")[0], "Título: " + r.split(" ").slice(1).join(" "), `Alcançar o nível ${i * 5 + 1}`, s => s.lv, i * 5 + 1); });
    [[10, "medalha"], [50, "medalha"], [100, "trofeu"], [200, "trofeu"], [400, "brasao"], [600, "honra"]].forEach(([n, t]) => A("qa" + n, t, "❓", `Questionador ${n}`, `Responder ${n} questões diferentes`, s => s.qAns, n));
    A("acc70", "trofeu", "🎯", "Mira Certeira", "Acerto ≥ 70% com ≥ 50 questões", s => s.qAns >= 50 ? Math.round(100 * s.qAcc) : 0, 70);
    A("acc80", "brasao", "🏹", "Arqueiro de Elite", "Acerto ≥ 80% com ≥ 100 questões", s => s.qAns >= 100 ? Math.round(100 * s.qAcc) : 0, 80);
    A("acc90", "honra", "🦅", "Olho de Águia", "Acerto ≥ 90% com ≥ 200 questões", s => s.qAns >= 200 ? Math.round(100 * s.qAcc) : 0, 90);
    [[10, "medalha"], [50, "medalha"], [100, "trofeu"], [200, "brasao"], [400, "honra"]].forEach(([n, t]) => A("qc" + n, t, "📖", `Leitor de Comentários ${n}`, `Marcar ☑️ ${n} comentários de questões como lidos`, s => s.qc, n));
    [[10, "medalha"], [50, "trofeu"], [100, "brasao"], [200, "honra"], [400, "honra"], [600, "honra"]].forEach(([n, t]) => A("mc" + n, t, "💊", `Alquimista ${n}`, `Ler ${n} micropartículas (☑️)`, s => s.mic, n));
    [[10, "medalha"], [50, "trofeu"], [150, "brasao"], [300, "honra"], [500, "honra"], [800, "honra"]].forEach(([n, t]) => A("mn" + n, t, "🧠", `Mnemonista ${n}`, `Dominar ${n} mnemônicos (2 acertos seguidos no treino)`, s => s.mn, n));
    [[10, "medalha"], [50, "trofeu"], [150, "brasao"], [300, "honra"], [500, "honra"]].forEach(([n, t]) => A("ho" + n, t, "🕊️", `Peregrino da Honra ${n}`, `Dominar ${n} cards ou mnemônicos da aba 🕊️ Honra`, s => s.hon, n));
    [[5, "medalha"], [30, "trofeu"], [100, "brasao"]].forEach(([n, t]) => A("hb" + n, t, "🌬️", `Fôlego Sereno ${n}`, `Concluir ${n} respirações guiadas na aba 🕊️ Honra`, s => s.hb, n));
    [[1, "medalha"], [7, "trofeu"], [30, "brasao"], [100, "honra"]].forEach(([n, t]) => A("hn" + n, t, "🌙", `Vigília Serena ${n}`, `Concluir o Modo Noite em ${n} noite(s)`, s => s.hn, n));
    [[5, "medalha"], [25, "trofeu"], [100, "brasao"]].forEach(([n, t]) => A("hu" + n, t, "🧭", `Bússola de Ouro ${n}`, `Usar ${n} bússolas ou filtros de decisão`, s => s.hbu, n));
    [[100, "medalha"], [500, "medalha"], [1000, "trofeu"], [2500, "trofeu"], [5000, "brasao"], [10000, "honra"]].forEach(([n, t]) => A("cd" + n, t, "🎴", `Guardião de ${n.toLocaleString("pt-BR")} cards`, `Responder ${n.toLocaleString("pt-BR")} flashcards`, s => s.cards, n));
    [[1, "medalha"], [7, "trofeu"], [30, "brasao"], [100, "honra"]].forEach(([n, t]) => A("mt" + n, t, "🎯", `Juramento Cumprido ${n}`, `Cumprir a meta diária de novos em ${n} dia(s)`, s => s.metaDays, n));
    A("wkrec", "trofeu", "📈", "Semana Recorde", "Superar sua melhor semana anterior (≥ 500 XP)", s => { const w = Object.entries(s.wk).sort((a, b) => a[0] - b[0]); if (w.length < 2) return 0; const last = w[w.length - 1][1], best = Math.max(...w.slice(0, -1).map(x => x[1])); return last >= 500 && last > best ? 1 : 0; }, 1);
  },
  got() { return (S.logs._a = S.logs._a || {}); },
  check() {
    if (!this.list.length) this.build();
    const st = jStats(), G = this.got(), novas = [];
    for (const a of this.list) if (!G[a.id] && a.val(st) >= a.goal) { G[a.id] = Date.now(); novas.push(a); }
    if (!novas.length) return;
    saveLog();
    for (const a of novas) addXP(ACH_BONUS[a.tipo], "conquista", "a");
    const a = novas[novas.length - 1];
    toast(`${a.ic} <b>Nova conquista!</b> ${esc(a.nome)}${novas.length > 1 ? ` (+${novas.length - 1})` : ""} · ${ACH_T[a.tipo]}`, 4500);
    if (location.hash === "#jornada") JR.render();
  } };
const JR = {
  async render() { await QZ.load();
    if (!ACH.list.length) ACH.build();
    const st = jStats(), G = ACH.got(), L = levelOf(st.xp), now = Date.now(), wNow = isoWeek(now);
    const d14 = []; for (let i = 13; i >= 0; i--) d14.push(dayKey(now - i * DAY));
    const xp14 = d14.map(d => (S.logs[d] || {}).xp || 0), W = []; for (let i = 11; i >= 0; i--) W.push(isoWeek(now - i * 7 * DAY));
    const wv = W.map(w => st.wk[w] || 0), lab = t => { const d = new Date(+t); return String(d.getDate()).padStart(2, "0") + "/" + String(d.getMonth() + 1).padStart(2, "0"); };
    const rank = Object.entries(st.wk).filter(([, v]) => v > 0).sort((a, b) => b[1] - a[1]), pos = rank.findIndex(([w]) => +w === wNow) + 1;
    const src = Object.entries(XPSRC).map(([k, [n, c]]) => ({ n, c, v: st.xs[k] || 0 })), tot = Object.values(st.xs).reduce((a, b) => a + b, 0) || 1;
    const by = t => ACH.list.filter(a => a.tipo === t), nGot = ACH.list.filter(a => G[a.id]).length;
    const card = a => { const v = Math.min(a.goal, a.val(st)), ok = G[a.id]; return `<div class="ach ${ok ? "on" : ""}" title="${esc(a.desc)}"><div class="achIc">${ok ? a.ic : "🔒"}</div><div class="achTx"><b>${esc(a.nome)}</b><small>${esc(a.desc)}</small>${ok ? `<small class="achD">✅ ${new Date(G[a.id]).toLocaleDateString("pt-BR")} · +${ACH_BONUS[a.tipo]} XP</small>` : `<span class="xpTrack"><i style="width:${Math.round(100 * v / a.goal)}%"></i></span><small>${typeof v === "number" ? v.toLocaleString("pt-BR") : v}/${a.goal.toLocaleString("pt-BR")}</small>`}</div></div>`; };
    $("#jrHost").innerHTML = `
     <div class="panel jrHead"><div class="jrBig">${L.rank.split(" ")[0]}</div><div class="grow"><h2 style="margin:0">${L.rank} · Nível ${L.lv}</h2>
      <span class="xpTrack" style="height:9px;margin:6px 0"><i style="width:${Math.round(100 * L.cur / L.need)}%"></i></span>
      <small style="color:var(--mut)">${st.xp.toLocaleString("pt-BR")} XP · faltam ${L.need - L.cur} para o nível ${L.lv + 1}</small></div></div>
     <div class="stats"><div class="stat"><b style="color:#ff8f5a">🔥 ${st.cur}</b><span>dias seguidos (recorde ${st.max})</span></div><div class="stat"><b class="n">${((S.logs[today()] || {}).xp || 0)}</b><span>XP hoje</span></div>
      <div class="stat"><b class="rv">${(st.wk[wNow] || 0).toLocaleString("pt-BR")}</b><span>XP nesta semana${pos ? ` · ${pos}º lugar` : ""}</span></div><div class="stat"><b style="color:var(--gold2)">${nGot}/${ACH.list.length}</b><span>conquistas</span></div></div>
     <div class="panel"><h2 style="margin-top:0">📊 Painel de produtividade (XP)</h2><div class="charts">
      <div class="chart"><h3>📅 XP por dia (14 dias)</h3>${barSVG(xp14, d14.map(d => d.slice(8) + "/" + d.slice(5, 7)), ["#e8c56a"])}</div>
      <div class="chart"><h3>🗓️ XP por semana (12 semanas)</h3>${barSVG(wv, W.map(lab), W.map(w => w === wNow ? "#4dd4ff" : "#e8c56a"))}</div>
      <div class="chart" style="grid-column:1/-1"><h3>🧭 De onde vem seu XP</h3>${stackSVG(src.map(x => ({ n: x.n, v: x.v, c: x.c })))}
       <div class="legend">${src.map(x => `<span><i style="background:${x.c}"></i>${x.n}: <b>${x.v.toLocaleString("pt-BR")}</b> (${Math.round(100 * x.v / tot)}%)</span>`).join("")}</div></div></div></div>
     ${DOM.html()}
     <div class="panel"><h2 style="margin-top:0">🏟️ Ranking semanal de XP</h2><p class="metaNow">Suas semanas competem entre si: supere seu próprio recorde. 🥇🥈🥉</p>
      <table class="t jrRank"><tr><th>#</th><th>Semana</th><th>XP</th></tr>${rank.slice(0, 10).map(([w, v], i) => `<tr class="${+w === wNow ? "me" : ""}"><td>${["🥇", "🥈", "🥉"][i] || i + 1 + "º"}</td><td>${lab(w)}${+w === wNow ? " · esta semana" : ""}</td><td><b>${v.toLocaleString("pt-BR")}</b></td></tr>`).join("") || `<tr><td colspan=3>Estude para abrir o ranking.</td></tr>`}</table></div>
     <div class="panel"><h2 style="margin-top:0">🏰 Salão de troféus · Temporada I (nov/2026)</h2>
      <div class="achSum">${Object.entries(ACH_T).map(([t, n]) => `<span>${n}: <b>${by(t).filter(a => G[a.id]).length}/${by(t).length}</b></span>`).join("")}</div>
      ${Object.entries(ACH_T).map(([t, n]) => `<h3 class="achH">${n}</h3><div class="achGrid">${by(t).sort((a, b) => (!!G[b.id]) - (!!G[a.id])).map(card).join("")}</div>`).join("")}
      <p class="metaNow">✨ Bônus por conquista: medalha +20, troféu +40, título +50, brasão +80, honraria +150 XP. Novas conquistas chegam a cada atualização do app.</p></div>`;
  } };


/* ---------------- Mapa de domínio (questões + simulados) ---------------- */
const DOM = {
  col: p => p == null ? "#2a3442" : p >= 85 ? "#5be38a" : p >= 70 ? "#ffc14d" : "#ff6b6b",
  rows() {
    const out = [], R = S.logs._q || {}, data = QZ.data || { temi: [], r3: [] };
    for (const div of ["temi", "r3"]) {
      const by = {};
      for (const q of data[div] || []) { const t = by[q.tema] = by[q.tema] || { tot: 0, feitas: 0, ult: 0, at: 0, ok: 0 }; t.tot++; const r = R[q.id]; if (r) { t.feitas++; t.ult += r[0]; t.at += r[1]; t.ok += r[2]; } }
      for (const [tema, t] of Object.entries(by)) out.push({ fonte: div === "temi" ? "❓ TEMI" : "❓ R3", div, tema, n: t.feitas, tot: t.tot, pct: t.feitas ? Math.round(100 * t.ult / t.feitas) : null, hist: t.at ? Math.round(100 * t.ok / t.at) : null });
    }
    const sd = {}; for (const [, l] of dayLogs()) for (const [k, [ok, n]] of Object.entries(l.sd || {})) { const v = sd[k] = sd[k] || [0, 0]; v[0] += ok; v[1] += n; }
    for (const [k, [ok, n]] of Object.entries(sd)) out.push({ fonte: "🧪 Simulado", tema: k.replace("::", " › "), n, tot: null, pct: n ? Math.round(100 * ok / n) : null, hist: null });
    return out;
  },
  html(limit) {
    const rows = this.rows(), done = rows.filter(r => r.n > 0).sort((a, b) => a.pct - b.pct), todo = rows.filter(r => !r.n && r.tot);
    const forte = done.filter(r => r.pct >= 85).length, medio = done.filter(r => r.pct >= 70 && r.pct < 85).length, fraco = done.filter(r => r.pct < 70).length;
    const row = r => `<tr><td>${r.fonte}</td><td><b>${esc(r.tema)}</b></td><td>${r.n}${r.tot ? "/" + r.tot : ""}</td><td><span class="domBar"><i style="width:${r.pct || 0}%;background:${this.col(r.pct)}"></i></span> <b style="color:${this.col(r.pct)}">${r.pct}%</b>${r.hist != null && r.hist !== r.pct ? `<small> · histórico ${r.hist}%</small>` : ""}</td><td>${r.div ? `<button class="btn sm" data-dom="${r.div}|${esc(r.tema)}">🎯 Treinar</button>` : ""}</td></tr>`;
    return `<div class="panel" id="domPanel"><h2 style="margin-top:0">🗺️ Mapa de domínio por tema</h2>
      <p class="metaNow">Ordenado do mais fraco para o mais forte. Questões: acerto na última tentativa de cada questão. Simulados: acerto por baralho. 🟢 ≥ 85% · 🟡 70–84% · 🔴 &lt; 70%.</p>
      <div class="achSum"><span>🔴 A reforçar: <b>${fraco}</b></span><span>🟡 Em consolidação: <b>${medio}</b></span><span>🟢 Dominados: <b>${forte}</b></span><span>⚪ Ainda não testados: <b>${todo.length}</b></span></div>
      ${done.length ? `<table class="t domT"><tr><th>Fonte</th><th>Tema</th><th>Feitas</th><th>Acerto</th><th></th></tr>${(limit ? done.slice(0, limit) : done).map(row).join("")}</table>` : `<p class="metaNow">Responda questões ou faça simulados para montar o mapa.</p>`}
      ${todo.length ? `<details><summary class="metaNow">⚪ Temas ainda não testados (${todo.length})</summary><div class="domTodo">${todo.map(r => `<button class="btn sm" data-dom="${r.div}|${esc(r.tema)}">${r.fonte} · ${esc(r.tema)} (${r.tot})</button>`).join("")}</div></details>` : ""}</div>`;
  } };
document.addEventListener("click", async e => {
  const b = e.target.closest("[data-dom]"); if (!b) return;
  const [div, tema] = b.dataset.dom.split("|"); await QZ.load(); QZ.div = div; lsSet("qzDiv", div); QZ.tema = tema; QZ.block = null; location.hash = "questoes"; setTimeout(() => QZ.home(), 50);
});

/* ---------------- Gráficos (SVG) ---------------- */
function barSVG(vals, labels, colors, h = 120, fmt = v => v) {
  const W = 320, max = Math.max(1, ...vals), bw = W / vals.length;
  return `<svg viewBox="0 -12 ${W} ${h + 38}" role="img">` + vals.map((v, i) => {
    const bh = Math.round((v / max) * h), x = i * bw + 2, y = h - bh;
    return `<rect x="${x}" y="${y}" width="${bw - 4}" height="${Math.max(bh, v ? 2 : 0)}" rx="3" fill="${colors[i] || colors[0]}"><title>${labels[i]}: ${fmt(v)}</title></rect>` +
      (v && vals.length <= 16 ? `<text x="${x + (bw - 4) / 2}" y="${y - 3}" font-size="9" text-anchor="middle" fill="#9aa4b2">${fmt(v)}</text>` : "") +
      (i % Math.ceil(vals.length / 8) === 0 ? `<text x="${x + (bw - 4) / 2}" y="${h + 16}" font-size="9" text-anchor="middle" fill="#9aa4b2">${labels[i]}</text>` : "");
  }).join("") + `</svg>`;
}
function stackSVG(parts) {
  const tot = parts.reduce((s, p) => s + p.v, 0) || 1; let x = 0;
  return `<svg viewBox="0 0 320 22">` + parts.map(p => { const w = 320 * p.v / tot; const r = `<rect x="${x}" y="2" width="${Math.max(0, w - 1)}" height="18" rx="4" fill="${p.c}"><title>${p.n}: ${p.v}</title></rect>`; x += w; return r; }).join("") + `</svg>`;
}
function renderCharts() {
  const now = Date.now(), d0 = new Date(); d0.setHours(0, 0, 0, 0); const base = d0.getTime();
  const fc = Array(14).fill(0); let overdue = 0;
  for (const c of S.cards) { if (c.susp || c.srs.st === "new") continue; const k = Math.floor((c.srs.due - base) / DAY); if (k < 0) overdue++; else if (k < 14) fc[k]++; }
  fc[0] += overdue;
  const fl = fc.map((_, i) => i === 0 ? "hoje" : i === 1 ? "amanhã" : "+" + i);
  const days = [...Array(30)].map((_, i) => dayKey(now - (29 - i) * DAY));
  const ans = days.map(d => (S.logs[d] || {}).nAns || 0);
  const accCol = days.map(d => { const l = S.logs[d]; if (!l || !l.nAns) return "#2a3442"; const a = l.nOk / l.nAns; return a >= .85 ? "#5be38a" : a >= .7 ? "#ffc14d" : "#ff6b6b"; });
  const streak = (() => { let s = 0; for (let i = 0; ; i++) { const l = S.logs[dayKey(now - i * DAY)]; if (l && l.nAns) s++; else if (i > 0) break; else continue; if (i > 999) break; } return s; })();
  const cols = (S.index?.colecoes || []).filter(c => S.settings.cols[c.id] !== false);
  const colHTML = cols.map(col => {
    const cs = S.cards.filter(c => c.col === col.id || (!c.col && false));
    const n = cs.filter(c => c.srs.st === "new").length, l = cs.filter(c => c.srs.st === "learn" || c.srs.st === "relearn").length;
    const y = cs.filter(c => c.srs.st === "review" && c.srs.ivl < 21).length, m = cs.filter(c => c.srs.st === "review" && c.srs.ivl >= 21).length;
    return `<div style="margin-top:6px"><b>${col.icone} ${esc(col.nome)}</b> <span style="color:var(--mut);font-size:12px">${cs.length - n}/${cs.length} vistos</span>${stackSVG([{ n: "novos", v: n, c: "#2a3442" }, { n: "aprendendo", v: l, c: "#ff6b6b" }, { n: "jovens", v: y, c: "#ffc14d" }, { n: "maduros", v: m, c: "#5be38a" }])}</div>`;
  }).join("");
  const own = S.user.size ? `<div style="margin-top:6px"><b>✍️ Meus cards</b> <span style="color:var(--mut);font-size:12px">${S.user.size} cards</span></div>` : "";
  const sims = dayLogs().flatMap(([, l]) => l.sims || []).sort((a, b) => a.t - b.t);
  const wk = t => { const d = new Date(t); d.setHours(0, 0, 0, 0); d.setDate(d.getDate() - ((d.getDay() + 6) % 7)); return d.getTime(); };
  const W = []; for (let i = 11; i >= 0; i--) W.push(wk(Date.now() - i * 7 * DAY));
  const wv = W.map(w => { const xs = sims.filter(x => wk(x.t) === w); const n = xs.reduce((a, x) => a + x.n, 0); return n ? Math.round(100 * xs.reduce((a, x) => a + x.ok, 0) / n) : 0; });
  const pcol = v => v >= 85 ? "#5be38a" : v >= 70 ? "#ffc14d" : v ? "#ff6b6b" : "#2a3442";
  const last = sims.slice(-12);
  const simHTML = sims.length ? `<div class="chart"><h3>🧪 Nota semanal · simulados + questões (12 semanas)</h3>${barSVG(wv, W.map(w => { const d = new Date(w); return String(d.getDate()).padStart(2, "0") + "/" + String(d.getMonth() + 1).padStart(2, "0"); }), wv.map(pcol), 120, v => v + "%")}</div>
    <div class="chart"><h3>📋 Últimas ${last.length} sessões</h3>${barSVG(last.map(x => Math.round(100 * x.ok / x.n)), last.map(x => (x.k === "q" ? "❓" : "🧪") + new Date(x.t).getDate()), last.map(x => pcol(Math.round(100 * x.ok / x.n))), 120, v => v + "%")}
    <div class="legend">${last.slice(-3).reverse().map(x => `<span>${x.k === "q" ? "❓" : "🧪"} ${esc((x.deck || "").split("::").pop())} ${x.ok}/${x.n}</span>`).join("")}</div></div>` :
    `<div class="chart" style="grid-column:1/-1"><h3>🧪 Histórico de simulados</h3><p style="color:var(--mut);margin:0">Faça um 🧪 simulado ou um bloco de ❓ questões para ver sua nota semana a semana.</p></div>`;
  $("#charts").innerHTML = simHTML + `
   <div class="chart"><h3>📅 Previsão de revisões (14 dias)</h3>${barSVG(fc, fl, ["#4dd4ff"])}</div>
   <div class="chart"><h3>🔥 Últimos 30 dias · sequência: ${streak} dia(s)</h3>${barSVG(ans, days.map(d => d.slice(8) + "/" + d.slice(5, 7)), accCol)}
     <div class="legend"><span><i style="background:#5be38a"></i>≥ 85% acerto</span><span><i style="background:#ffc14d"></i>70–84%</span><span><i style="background:#ff6b6b"></i>&lt; 70%</span></div></div>
   <div class="chart" style="grid-column:1/-1"><h3>🏛️ Progresso por coleção</h3>${colHTML}${own}
     <div class="legend"><span><i style="background:#2a3442"></i>novos</span><span><i style="background:#ff6b6b"></i>aprendendo</span><span><i style="background:#ffc14d"></i>jovens (&lt; 21 d)</span><span><i style="background:#5be38a"></i>maduros (≥ 21 d)</span></div></div>`;
}

/* ---------------- UI: Início ---------------- */
function buildTree() {
  const root = { kids: new Map() };
  for (const c of S.cards) { let node = root, path = []; for (const p of c.deck.split("::")) { path.push(p); if (!node.kids.has(p)) node.kids.set(p, { name: p, full: path.join("::"), kids: new Map(), tot: 0, seen: 0 }); node = node.kids.get(p); node.tot++; if (c.srs.st !== "new") node.seen++; } }
  return root;
}
const openDecks = new Set(JSON.parse(lsGet("openDecks") || '["TEMI 2028","R3 Clínica Médica"]'));
function treeHTML(node, depth = 0) {
  const kids = [...node.kids.values()].sort((a, b) => a.name.localeCompare(b.name, "pt", { numeric: true }));
  return kids.map(k => {
    const c = counts(k.full), has = k.kids.size > 0, open = openDecks.has(k.full), acc = depth === 0 ? "#d4af37" : accentFor(k.full);
    const icon = depth === 0 ? (k.name === "TEMI 2028" ? "🏥 " : /cl[ií]nica/i.test(k.name) ? "🩺 " : /outras ias/i.test(k.name) ? "📦 " : "✍️ ") : "";
    const pct = Math.round(100 * k.seen / Math.max(1, k.tot));
    return `<li><div class="dk" data-deck="${esc(k.full)}" style="--acc:${acc}"><span class="tg" data-tg="${esc(k.full)}">${has ? (open ? "▾" : "▸") : "·"}</span><span class="nm">${icon}${esc(k.name)} <small style="color:var(--mut)">${k.tot}</small></span>
      <span class="cnt n">${c.n || ""}</span><span class="cnt l">${c.l || ""}</span><span class="cnt rv">${c.r || ""}</span></div>
      ${depth <= 1 ? `<div class="mini"><i style="width:${pct}%;background:${acc}"></i></div>` : ""}
      ${has ? `<ul class="tree sub ${open ? "open" : ""}">${treeHTML(k, depth + 1)}</ul>` : ""}</li>`;
  }).join("");
}
function refreshHome() {
  const all = counts(null), L = L0(), tot = S.cards.length;
  const ss = S.session; let rb = "";
  if (ss) {
    const pend = ss.ids ? ss.ids.filter(id => { const c = S.byId.get(id); return c && !c.susp && (c.srs.st === "new" || c.srs.due <= endOfDay()); }).length : (() => { const k = counts(ss.prefix); return k.n + k.l + k.r; })();
    const when = new Date(ss.mod).toLocaleString("pt-BR", { day: "2-digit", month: "2-digit", hour: "2-digit", minute: "2-digit" });
    if (pend) rb = `<div class="panel" style="border-color:var(--gold);display:flex;gap:10px;align-items:center;flex-wrap:wrap"><div class="grow">▶️ <b>Continuar de onde parou</b><br><small style="color:var(--mut)">${esc(ss.ids ? "🔎 Estudo filtrado" : (ss.prefix || "Todos os baralhos"))} · ${pend} pendente(s) · ${when}</small></div><button class="btn gold" id="resumeBtn">▶️ Continuar</button></div>`;
  }
  $("#resumeBox").innerHTML = rb; $("#metaHome").innerHTML = metaBarHTML(false);
  if (rb) $("#resumeBtn").onclick = () => startStudy(ss.prefix, ss.ids, true);
  const mature = S.cards.filter(c => c.srs.st === "review" && c.srs.ivl >= 21).length, acc = L.nAns ? Math.round(100 * L.nOk / L.nAns) : 0;
  $("#stats").innerHTML = `<div class="stat"><b class="n">${all.n}</b><span>novos hoje</span></div><div class="stat"><b class="rv">${all.r + all.l}</b><span>revisões pendentes</span></div>
   <div class="stat"><b>${L.nAns}</b><span>respondidos hoje · ${acc}% ✓</span></div><div class="stat"><b style="color:var(--gold2)">${tot}</b><span>cards · ${mature} maduros</span></div>`;
  renderCharts();
  $("#tree").innerHTML = tot ? treeHTML(buildTree()) : `<li class="empty">Nenhum card. Ative uma coleção em ⚙️ Ajustes ou vá em 📥 Importar.</li>`;
  $("#homeFoot").innerHTML = Cloud.on ? "☁️ Progresso salvo na sua conta e sincronizado automaticamente entre aparelhos (abra esta mesma página logado)." : "💾 Progresso salvo neste aparelho. Abra o app pela página do Claude para sincronizar automaticamente; ou use ⚙️ Ajustes → Backup.";
  fillDeckSelects(); setTimeout(() => ACH.check(), 800);
}
function fillDeckSelects() {
  const names = [...new Set(S.cards.flatMap(c => { const p = c.deck.split("::"); return p.map((_, i) => p.slice(0, i + 1).join("::")); }))].sort((a, b) => a.localeCompare(b, "pt", { numeric: true }));
  const opts = names.map(n => `<option value="${esc(n)}">${esc(n.replace(/[^:]+::/g, "· "))}</option>`).join("");
  $("#qDeck").innerHTML = `<option value="">Todos os baralhos</option>` + opts;
  const sd = $("#simDeck"); if (sd) { const keep = sd.value; sd.innerHTML = `<option value="">🎲 Todas as coleções</option>` + names.filter(n => n.split("::").length <= 2).map(n => `<option value="${esc(n)}">${esc(n.replace(/[^:]+::/g, "· "))}</option>`).join(""); sd.value = keep; }
  const own = [...new Set([...S.user.values()].flatMap(u => { const p = u.deck.split("::"); return p.map((_, i) => p.slice(0, i + 1).join("::")); }))].sort();
  $("#delDeck").innerHTML = `<option value="">Escolha um baralho próprio…</option>` + own.map(n => `<option value="${esc(n)}">${esc(n.replace(/[^:]+::/g, "· "))}</option>`).join("");
}
$("#tree").addEventListener("click", e => {
  const tg = e.target.closest("[data-tg]");
  if (tg && tg.textContent !== "·") { const k = tg.dataset.tg; openDecks.has(k) ? openDecks.delete(k) : openDecks.add(k); lsSet("openDecks", JSON.stringify([...openDecks])); refreshHome(); return; }
  const dk = e.target.closest("[data-deck]"); if (dk) startStudy(dk.dataset.deck);
});
$("#studyAll").onclick = () => startStudy(null);
$("#simBtn").onclick = () => startSim(null, $("#simDeck").value || null, +$("#simN").value || 50);
document.addEventListener("click", e => { const a = e.target.closest("[data-medit]"); if (!a) return; e.preventDefault(); location.hash = "ajustes"; setTimeout(() => { const i = $("#sNew"); if (i) { i.focus(); i.scrollIntoView({ block: "center" }); } }, 150); });

/* ---------------- UI: Estudo ---------------- */
function saveSession(prefix, ids) {
  S.session = { prefix: prefix || null, ids: ids ? ids.slice(0, 400) : null, mod: Date.now() };
  DB.setMeta("session", S.session); Cloud.markSt();
}
function startStudy(prefix, ids, resume, sim) {
  if (!resume && !sim) saveSession(prefix, ids);
  Study.sim = sim ? { ok: 0, n: 0, miss: [] } : null; Study.simOrder = sim ? ids.slice() : null;
  Study.prefix = prefix; Study.ids = ids ? new Set(ids) : null; Study.seen = new Set(); Study.undo = []; Study.done = 0; Study.started = true;
  const c = counts(prefix); Study.total = ids ? ids.length : c.n + c.l + c.r;
  if (location.hash !== "#estudar") location.hash = "estudar"; else showCard();
}
function startSim(ids, prefix, n, retry) {
  if (!ids) { const pool = S.cards.filter(c => !c.susp && inDeck(c, prefix || null)); for (let i = pool.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [pool[i], pool[j]] = [pool[j], pool[i]]; } ids = pool.slice(0, n || 50).map(c => c.id); }
  if (!ids.length) return toast("Nenhum card disponível para o simulado.");
  startStudy(null, ids, false, true); Study.sim.deck = prefix || "Todas as coleções"; Study.sim.retry = !!retry;
  toast(`🧪 Simulado com ${ids.length} cards — não altera agenda nem meta.`);
}
async function showCard() {
  Study.view = null; $("#histBanner").style.display = "none";
  const c = nextCard(); Study.cur = c; Study.shown = false;
  $("#studyDeck").textContent = Study.sim ? "🧪 Simulado — sem efeito na agenda" : Study.ids ? "🔎 Estudo filtrado (resultados da busca)" : "📚 " + (Study.prefix || "Todos os baralhos");
  $("#studyMeta").innerHTML = Study.sim ? `<div class="metaBar compact"><div class="mbLbl">🧪 Acertos: <b>${Study.sim.ok}</b>/${Study.sim.n}</div></div>` : metaBarHTML(true);
  const cc = counts(Study.prefix), L = L0();
  $("#studyCounts").innerHTML = Study.ids ? `<span class="cnt">${Study.done}/${Study.total}</span>` : `<span class="cnt n">${cc.n}</span> <span class="cnt l">${cc.l}</span> <span class="cnt rv">${cc.r}</span>`;
  $("#prog").style.width = Study.total ? Math.min(100, 100 * Study.done / Math.max(Study.total, Study.done + 1)) + "%" : "0";
  if (!c && Study.sim) {
    $("#cardHost").style.display = "none"; $("#studyTools").style.display = "none"; $("#studyEmpty").style.display = "block";
    const m = Study.sim, pc = m.n ? Math.round(100 * m.ok / m.n) : 0, miss = m.miss.slice();
    if (!m.saved && m.n && !m.retry) { m.saved = 1; addSim({ k: "sim", deck: m.deck, ok: m.ok, n: m.n }); saveLog(); }
    $("#studyEmpty").innerHTML = `<div style="font-size:46px">🧪</div><h2>Simulado concluído</h2><p>Acertos: <b>${m.ok}</b>/${m.n} · <b>${pc}%</b> ${pc >= 85 ? "🟢" : pc >= 70 ? "🟡" : "🔴"}</p>
      <p style="color:var(--mut)">Nada foi alterado na sua agenda nem na meta de hoje.</p>
      <div class="metaRow" style="justify-content:center">${miss.length ? `<button class="btn" id="simMiss">🔁 Refazer os ${miss.length} errados</button>` : ""}<button class="btn" id="simNew">🎲 Novo simulado</button><a class="btn gold" href="#inicio">🏠 Início</a></div>`;
    const dk = m.deck === "Todas as coleções" ? null : m.deck;
    if (miss.length) $("#simMiss").onclick = () => startSim(miss, dk, null, true);
    $("#simNew").onclick = () => startSim(null, dk, Study.simOrder.length);
    bars(null); return;
  }
  if (!c) {
    $("#cardHost").style.display = "none"; $("#studyTools").style.display = "none"; $("#studyEmpty").style.display = "block";
    const nxt = S.cards.filter(x => !x.susp && x.srs.st !== "new" && inDeck(x, Study.prefix)).map(x => x.srs.due).sort((a, b) => a - b)[0];
    const ca = counts(Study.prefix), ahead = S.cards.filter(x => !x.susp && x.srs.st === "review" && x.srs.due > endOfDay() && inDeck(x, Study.prefix)).length;
    const metaOk = !Study.ids && (ca.nAll > 0 || ca.rAll > 0);
    $("#studyEmpty").innerHTML = `<div style="font-size:46px">🏆</div><h2>Missão cumprida!</h2><p>Hoje: <b>${L.nAns}</b> respostas · <b>${L.nAns ? Math.round(100 * L.nOk / L.nAns) : 0}%</b> de acerto.</p>
      ${nxt ? `<p style="color:var(--mut)">Próximo card vence em <b>${fmtIvl(Math.max(MIN, nxt - Date.now()))}</b>.</p>` : ""}
      <div class="metaBox">
        <h3>🎯 Meta diária</h3>
        <p class="metaNow">🆕 Novos hoje: <b>${L.nNew}</b> / ${limNew(L)} · 🔁 Revisões hoje: <b>${L.nRev}</b> / ${limRev(L)}</p>
        <p class="metaNow">📦 Neste baralho ainda há <b>${ca.nAll}</b> novos e <b>${ca.rAll}</b> revisões vencidas à espera${ahead ? ` · <b>${ahead}</b> revisões futuras` : ""}.</p>
        ${metaOk ? `<div class="metaRow"><span>⏩ Continuar hoje:</span>
          <button class="btn" data-x="10">+10 novos</button><button class="btn" data-x="20">+20 novos</button><button class="btn" data-x="50">+50 novos</button>
          ${ca.rAll ? `<button class="btn" data-xr="100">+100 revisões</button>` : ""}</div>
        <div class="metaRow"><label>✏️ Quantos a mais hoje?</label><input type="number" id="mxNew" min="1" max="999" value="25" style="width:90px"><button class="btn gold" id="mxGo">▶️ Continuar estudando</button></div>` : `<p class="metaNow">✅ Nada pendente aqui além da meta.</p>`}
        ${ahead ? `<div class="metaRow"><button class="btn" id="mAhead">📖 Adiantar as próximas revisões (até 50)</button></div>` : ""}
        <div class="metaRow"><label>💾 Meta fixa (todos os dias):</label>
          <span>🆕 <input type="number" id="mNew" min="0" max="999" value="${S.settings.newPerDay}" style="width:80px"></span>
          <span>🔁 <input type="number" id="mRev" min="0" max="9999" value="${S.settings.revPerDay}" style="width:90px"></span>
          <button class="btn" id="mSave">Salvar meta</button></div>
      </div>
      <a class="btn gold" href="#inicio">🏠 Voltar ao início</a>`;
    const ext = async (xn, xr) => { const L1 = L0(); if (xn) L1.w80n = 0; if (xr) L1.w80r = 0; L1.xNew = (L1.xNew || 0) + xn; L1.xRev = (L1.xRev || 0) + xr; await saveLog(); const c2 = counts(Study.prefix); Study.total = Study.done + c2.n + c2.l + c2.r; toast(`⏩ Meta de hoje ampliada${xn ? ` +${xn} novos` : ""}${xr ? ` +${xr} revisões` : ""}.`); showCard(); };
    $("#studyEmpty").querySelectorAll("[data-x]").forEach(b => b.onclick = () => ext(+b.dataset.x, 0));
    $("#studyEmpty").querySelectorAll("[data-xr]").forEach(b => b.onclick = () => ext(0, +b.dataset.xr));
    const go = $("#mxGo"); if (go) go.onclick = () => { const v = Math.max(1, Math.min(999, +$("#mxNew").value || 0)); ext(v, ca.rAll ? v : 0); };
    const ah = $("#mAhead"); if (ah) ah.onclick = () => { const ids = S.cards.filter(x => !x.susp && x.srs.st === "review" && x.srs.due > endOfDay() && inDeck(x, Study.prefix)).sort((a, b) => a.srs.due - b.srs.due).slice(0, 50).map(x => x.id); startStudy(Study.prefix, ids); };
    $("#mSave").onclick = async () => { S.settings.newPerDay = Math.max(0, +$("#mNew").value || 0); S.settings.revPerDay = Math.max(0, +$("#mRev").value || 0); await saveSettings(); toast("💾 Meta diária salva."); const c2 = counts(Study.prefix); Study.total = Study.done + c2.n + c2.l + c2.r; showCard(); };
    bars(null); return;
  }
  $("#cardHost").style.display = "block"; $("#studyTools").style.display = "flex"; $("#studyEmpty").style.display = "none";
  $("#bMark").textContent = c.marked ? "🚩 Desmarcar" : "🚩 Marcar";
  await renderInto($("#cardHost"), c.q, c.style, c.deck); HL.count(); HL.sel = null; HL.hide();
  Study.t0 = Date.now(); bars("show"); window.scrollTo({ top: 0 });
}
function bars(which) {
  const st = location.hash === "#estudar";
  $("#barShow").classList.toggle("on", which === "show" && st);
  $("#barAns").classList.toggle("on", which === "ans" && st);
  $("#barHist").classList.toggle("on", which === "hist" && st);
}
/* ---------- Voltar / Continuar (histórico da sessão) ---------- */
const GN = { 1: "De novo", 2: "Difícil", 3: "Bom", 4: "Fácil" };
async function histShow() {
  const h = Study.undo[Study.view], c = h && S.byId.get(h.id);
  if (!c) { Study.view = null; return histContinue(); }
  $("#cardHost").style.display = "block"; $("#studyEmpty").style.display = "none"; $("#studyTools").style.display = "flex";
  $("#histBanner").style.display = "block";
  $("#histBanner").innerHTML = `⬅️ <b>Revendo card anterior</b> ${Study.undo.length - Study.view} de ${Study.undo.length} · você respondeu <b>${GN[h.g] || "?"}</b> · próximo em ${c.srs.st === "review" ? fmtIvl(c.srs.ivl * DAY) : fmtIvl(Math.max(MIN, c.srs.due - Date.now()))}`;
  await renderInto($("#cardHost"), c.a, c.style, c.deck);
  $("#hBack").disabled = Study.view <= 0; HL.count(); bars("hist"); window.scrollTo({ top: 0 });
}
function histBack() {
  if (!Study.undo.length) return toast("Ainda não há card anterior nesta sessão.");
  Study.view = Study.view == null ? Study.undo.length - 1 : Math.max(0, Study.view - 1);
  histShow();
}
async function histContinue() {
  Study.view = null; $("#histBanner").style.display = "none";
  const c = Study.cur;
  if (!c) return showCard();
  await renderInto($("#cardHost"), Study.shown ? c.a : c.q, c.style, c.deck);
  bars(Study.shown ? "ans" : "show");
}
async function histRedo() {
  const i = Study.view; const h = Study.undo[i]; if (!h) return;
  const c = S.byId.get(h.id); if (!c) return;
  c.srs = h.srs; // volta ao estado de antes da resposta
  const L = S.logs[h.day]; if (L) { L.nAns = Math.max(0, L.nAns - 1); if (h.g > 1) L.nOk = Math.max(0, L.nOk - 1); if (h.wasNew) L.nNew = Math.max(0, L.nNew - 1); if (h.wasRev) L.nRev = Math.max(0, L.nRev - 1); }
  Study.undo.splice(i, 1); Study.done = Math.max(0, Study.done - 1); Study.seen.delete(c.id);
  await saveProg(c); await saveLog();
  Study.view = null; $("#histBanner").style.display = "none";
  Study.cur = c; Study.shown = false; await renderInto($("#cardHost"), c.q, c.style, c.deck); Study.t0 = Date.now(); bars("show");
  toast("🔁 Responda este card de novo");
}
async function reveal() {
  const c = Study.cur; if (!c || Study.shown) return; Study.shown = true;
  await renderInto($("#cardHost"), c.a, c.style, c.deck);
  const now = Date.now(); for (let g = 1; g <= 4; g++) $("#i" + g).textContent = fmtIvl(schedule(c.srs, g, now).due - now);
  bars("ans");
  const ans = $("#cardHost").shadowRoot.querySelector("#answer"); if (ans && ans.getBoundingClientRect().top > innerHeight * 0.6) ans.scrollIntoView({ behavior: "smooth", block: "start" });
}
async function answer(g) {
  const c = Study.cur; if (!c || !Study.shown) return;
  if (Study.sim) { { const k = c.deck.split("::").slice(0, 2).join("::"), Ls = L0(); Ls.sd = Ls.sd || {}; const v = Ls.sd[k] = Ls.sd[k] || [0, 0]; v[1]++; if (g > 1) v[0]++; } Study.sim.n++; if (g > 1) Study.sim.ok++; else Study.sim.miss.push(c.id); Study.seen.add(c.id); Study.done++; addXP(g > 1 ? 5 : 3, "", "s"); saveLog(); return showCard(); }
  const L = L0();
  const wasNew = c.srs.st === "new", wasRev = c.srs.st === "review";
  Study.undo.push({ id: c.id, srs: Object.assign({}, c.srs), log: Object.assign({}, L), g, wasNew, wasRev, day: today() });
  c.srs = schedule(c.srs, g);
  if (wasNew) L.nNew++; if (wasRev) L.nRev++; L.nAns++; if (g > 1) L.nOk++; L.ms += Math.min(60000, Date.now() - Study.t0);
  Study.seen.add(c.id); if (g > 1 || Study.ids) Study.done++;
  addXP((wasNew ? 10 : 5) + (g > 1 ? 2 : 0), "", "c"); metaWarn(); await saveProg(c); await saveLog(); showCard();
}
async function undo() {
  if (Study.sim) return toast("🧪 No simulado não há desfazer — nada é gravado.");
  const u = Study.undo.pop(); if (!u) return toast("Nada para desfazer.");
  const c = S.byId.get(u.id); c.srs = u.srs; S.logs[u.day || today()] = u.log; Study.view = null; $("#histBanner").style.display = "none"; Study.done = Math.max(0, Study.done - 1);
  await saveProg(c); await saveLog(); Study.cur = c; Study.shown = false;
  await renderInto($("#cardHost"), c.q, c.style, c.deck); bars("show"); toast("↩️ Desfeito");
}
$("#bShow").onclick = reveal;
$$("#barAns [data-g]").forEach(b => b.onclick = () => answer(+b.dataset.g));
$("#bUndo").onclick = undo;
$("#bBack").onclick = histBack; $("#hBack").onclick = histBack; $("#hCont").onclick = histContinue; $("#hRedo").onclick = histRedo;
$("#bEnd").onclick = () => { location.hash = "inicio"; };
$("#bSusp").onclick = async () => { const c = Study.cur; if (!c) return; c.susp = true; await saveProg(c); toast("⏸️ Suspenso (reative em 🔎 Buscar → is:suspenso)"); showCard(); };
$("#bMark").onclick = async () => { const c = Study.cur; if (!c) return; c.marked = !c.marked; await saveProg(c); $("#bMark").textContent = c.marked ? "🚩 Desmarcar" : "🚩 Marcar"; toast(c.marked ? "🚩 Marcado" : "Desmarcado"); };
document.addEventListener("keydown", e => {
  if (/input|textarea|select/i.test(e.target.tagName)) return;
  if (location.hash === "#questoes" && (e.key === "c" || e.key === "C")) { const ck = $("#qzChk"); if (ck) { e.preventDefault(); ck.click(); } return; }
  if (location.hash === "#questoes") { const k = e.key.toUpperCase(), i = "ABCDE".indexOf(k) >= 0 ? "ABCDE".indexOf(k) : "12345".indexOf(e.key); if (i >= 0 && k.length === 1) { e.preventDefault(); QZ.pick(i); } else if (e.key === "Enter" || e.key === "ArrowRight") { e.preventDefault(); QZ.next(); } return; }
  if (location.hash === "#mnemonicos") { MN.key(e); return; }
  if (location.hash === "#honra") { HO.key(e); return; }
  if (location.hash === "#micro") { if (e.key === "ArrowRight" || e.code === "Space") { e.preventDefault(); MC.go(1); } else if (e.key === "ArrowLeft") { e.preventDefault(); MC.go(-1); } else if (e.key === "Enter") { e.preventDefault(); MC.check(); } return; }
  if (location.hash !== "#estudar" || /input|textarea|select/i.test(e.target.tagName)) return;
  if (e.key === "ArrowLeft") { e.preventDefault(); return histBack(); }
  if (e.key === "ArrowRight") { e.preventDefault(); if (Study.view != null) { if (Study.view < Study.undo.length - 1) { Study.view++; histShow(); } else histContinue(); } return; }
  if (Study.view != null) { if (e.code === "Space" || e.key === "Enter") { e.preventDefault(); histContinue(); } return; }
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
  const raw = $("#q").value.trim(), deckSel = $("#qDeck").value, terms = [], filt = { tag: [], deck: [], is: [] };
  (raw.match(/"[^"]+"|'[^']+'|\S+/g) || []).forEach(t => { const m = t.match(/^(tag|deck|is):(.+)$/i); if (m) filt[m[1].toLowerCase()].push(m[2].toLowerCase()); else terms.push(t.replace(/^["']|["']$/g, "").toLowerCase()); });
  const eod = endOfDay(), norm = s => s.normalize("NFD").replace(/[̀-ͯ]/g, ""), nterms = terms.map(norm);
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
      if (i === "meu" && !c.user) return false;
      if (i === "destaque" && !(c.hl && c.hl.length)) return false;
    }
    if (nterms.length) { const t = norm(c.txt || ""); if (!nterms.every(x => t.includes(x))) return false; }
    return true;
  });
  lastResults = res;
  $("#qInfo").textContent = `${res.length} card(s)` + (res.length > 150 ? " — mostrando 150" : "");
  $("#qRes").innerHTML = res.slice(0, 150).map(c => `<div class="res" data-id="${esc(c.id)}" style="border-left:3px solid ${accentFor(c.deck)}"><div class="hd"><div class="q">${esc(strip(c.q).slice(0, 180))}</div>
    <span class="pill">${c.srs.st === "new" ? "novo" : c.srs.st === "review" ? fmtIvl(c.srs.ivl * DAY) : "aprendendo"}</span>${c.marked ? "🚩" : ""}${c.susp ? "⏸️" : ""}</div>
    <div class="bd"><div style="font-size:12px;color:var(--mut);margin-bottom:6px">📚 ${esc(c.deck)}</div><div class="host"></div>
    <div class="row" style="margin-top:8px"><button class="btn sm" data-act="susp">${c.susp ? "▶️ Reativar" : "⏸️ Suspender"}</button><button class="btn sm" data-act="mark">${c.marked ? "Desmarcar" : "🚩 Marcar"}</button>
    <button class="btn sm" data-act="reset">♻️ Reiniciar</button>${c.user ? `<button class="btn sm danger" data-act="del">🗑️ Apagar</button>` : ""}</div></div></div>`).join("");
}
let qT; $("#q").addEventListener("input", () => { clearTimeout(qT); qT = setTimeout(search, 180); });
$("#qDeck").addEventListener("change", search);
$("#qRes").addEventListener("click", async e => {
  const box = e.target.closest(".res"); if (!box) return; const c = S.byId.get(box.dataset.id); const act = e.target.closest("[data-act]")?.dataset.act;
  if (!act) { if (e.target.closest(".hd")) { box.classList.toggle("open"); if (box.classList.contains("open")) renderInto($(".host", box), c.a, c.style, c.deck); } return; }
  if (act === "susp") c.susp = !c.susp;
  if (act === "mark") c.marked = !c.marked;
  if (act === "reset") c.srs = newSRS();
  if (act === "del") { if (box.dataset.confirm !== "1") { box.dataset.confirm = "1"; e.target.textContent = "Confirmar?"; return; } await deleteUserCards([c.id]); box.remove(); toast("🗑️ Apagado"); return; }
  await saveProg(c); search();
});
$("#qStudy").onclick = () => { if (!lastResults.length) return toast("Faça uma busca primeiro."); startStudy(null, lastResults.filter(c => !c.susp).map(c => c.id)); };
async function deleteUserCards(ids) {
  Cloud.tomb = Cloud.tomb || new Map(); const now = Date.now();
  for (const id of ids) { S.user.delete(id); Cloud.tomb.set(id, now); Cloud.markU(id); }
  await DB.delMany("user", ids); await DB.setMeta("tomb", [...Cloud.tomb]); rebuildCards();
}

/* ---------------- UI: Importar ---------------- */
const drop = $("#drop"), fileIn = $("#file");
drop.onclick = () => fileIn.click();
fileIn.onchange = () => { importFiles([...fileIn.files], null); fileIn.value = ""; };
["dragenter", "dragover"].forEach(ev => drop.addEventListener(ev, e => { e.preventDefault(); drop.classList.add("hov"); }));
["dragleave", "drop"].forEach(ev => drop.addEventListener(ev, e => { e.preventDefault(); drop.classList.remove("hov"); }));
drop.addEventListener("drop", e => importFiles([...e.dataTransfer.files], null));
$("#pasteGo").onclick = async () => {
  const t = $("#paste").value; if (!t.trim()) return toast("Cole o texto primeiro.");
  const box = document.createElement("div"); box.className = "panel"; $("#impLog").prepend(box);
  try { const r = await importText(t, $("#pasteDeck").value.trim() || null, m => box.innerHTML += `<div>${m}</div>`); box.innerHTML += `<div>✅ <b class="rv">${r.novos} novos</b> · ${r.atual} atualizados${Cloud.on ? " · ☁️ sincronizando" : ""}</div>`; $("#paste").value = ""; rerender(); }
  catch (e) { box.innerHTML += `<div>❌ <span style="color:var(--red)">${esc(e.message)}</span></div>`; }
};

/* ---------------- UI: Prompt IA ---------------- */
const TEMAS = [
  ...["01 🦠 Sepse e Choque Séptico", "02 🫁 Ventilação Mecânica e SDRA", "03 ❤️ Hemodinâmica e Choque", "04 ⚗️ Distúrbios Ácido-Base", "05 🧂 Eletrólitos", "06 🫘 Rim, LRA e TRS", "07 🧠 Neurointensivismo", "08 😴 Sedação, Analgesia e Delirium", "09 ⚡ Cardiointensivismo e PCR", "10 🧫 Infecção e Antimicrobianos", "11 🩸 Hematologia, Coagulação e Transfusão", "12 🍬 Endocrinologia no Crítico", "13 🫃 Gastro, Fígado e Nutrição", "14 🚑 Trauma, Toxicologia e Ambiental", "15 ⚖️ Ética, Escores, Qualidade e POCUS"].map(t => "TEMI 2028::" + t),
  ...["01 🫀 Cardiologia", "02 🫁 Pneumologia", "03 🫘 Nefrologia", "04 🍬 Endocrinologia", "05 🫃 Gastroenterologia e Hepatologia", "06 🩸 Hematologia", "07 🦠 Infectologia", "08 🦴 Reumatologia", "09 🧠 Neurologia", "10 🎗️ Oncologia Clínica", "11 👴 Geriatria e Cuidados Paliativos", "12 🧘 Psiquiatria na Clínica", "13 🩺 Medicina Preventiva", "14 🧴 Dermatologia e Alergia", "15 💊 Farmacologia, Semiologia e Laboratório"].map(t => "R3 Clínica Médica::" + t),
  "Meus cards::Extras"];
$("#pTema").innerHTML = TEMAS.map(t => `<option value="${esc(t)}">${esc(t.replace("::", " › "))}</option>`).join("");
function buildPrompt() {
  const tema = $("#pTema").value, temaNome = tema.split("::").pop().replace(/^\d+\s*\S+\s*/, ""), sub = $("#pSub").value.trim() || "(subtemas variados dentro do tema)", n = $("#pN").value, nivel = $("#pNivel").value, tipo = $("#pTipo").value, img = $("#pImg").value === "1", mat = $("#pMat").value.trim();
  const prova = tema.startsWith("R3") ? "prova de residência R3 de Clínica Médica" : "prova de título TEMI/AMIB em Medicina Intensiva";
  const estilo = tipo === "cloze" ? "TODOS os cards em formato de lacuna (cloze): em \"frente\" escreva a frase com {{c1::termo}} (pode usar c2, c3 na mesma frase); \"verso\" traz o complemento/explicação." :
    tipo === "basico" ? "Todos os cards no formato pergunta → resposta." : "Maioria pergunta → resposta; cerca de 1 em cada 4 no formato lacuna (cloze) com {{c1::termo}} na \"frente\".";
  return `Você é um gerador de flashcards de alta qualidade para o app CÓDICE 360X (estudo para a ${prova}).

🎯 TAREFA
Crie exatamente ${n} flashcards sobre: ${temaNome} › ${sub}.
Nível: ${nivel}. Idioma: português do Brasil.
${mat ? `\n📄 MATERIAL-BASE (use APENAS este conteúdo como fonte factual; não acrescente dados que não estejam nele):\n"""\n${mat}\n"""\n` : ""}
✅ REGRAS DE CONTEÚDO
1. Um conceito por card. Pergunta direta e específica (critério, corte numérico, dose, conduta, droga de escolha, contraindicação, ensaio clínico marcante, pegadinha de prova).
2. Baseie-se em diretrizes atuais e ensaios clínicos de referência. Preencha "fonte" com a referência curta (ex.: "SSC 2021", "KDIGO 2024", "GOLD 2024"). NUNCA invente referência, dose ou número; na dúvida, não crie o card.
3. ${estilo}
4. "verso": curto e escaneável (≤ 60 palavras OU uma tabela pequena). Comece com 1 emoji. Use <b>negrito</b> nos números-chave e as cores: <b class=r>perigo/erro</b>, <b class=g>alvo/correto</b>, <b class=y>atenção</b>, <b class=c>destaque</b>.
5. Prefira TABELAS para comparações, classificações e doses: <table class=t><tr><th>A</th><th>B</th></tr><tr><td>..</td><td>..</td></tr></table>. Listas: <ul><li>..</li></ul>. Quebra: <br>.
6. "pegadinha": 1 frase com a pegadinha de prova, o erro comum ou uma curiosidade nerd.
7. "subtema": nome curto do subtema (3–5 palavras) para organizar o baralho.
8. "tags": 2–4 palavras-chave sem espaços.
${img ? `9. "imagem": quando um esquema visual ajudar (curva, algoritmo, escala, gráfico de barras, comparação), desenhe um SVG inline: <svg viewBox="0 0 600 300" xmlns="http://www.w3.org/2000/svg">…</svg>, fundo transparente, textos fill="#e8e6df" font-size 16–20, cores #4dd4ff #d4af37 #ff6b6b #5be38a #b48cff, sem <script>, sem imagens externas. Até 1 SVG a cada 4 cards; nos demais "imagem": "".` : `9. "imagem": deixe sempre "".`}

📦 FORMATO DE SAÍDA (obrigatório)
Responda SOMENTE com um único bloco \`\`\`json válido, sem texto antes ou depois:
\`\`\`json
{
  "formato": "codice360x-v1",
  "baralho": "${tema.replace(/"/g, "")}",
  "cards": [
    { "subtema": "…", "frente": "…", "verso": "…", "pegadinha": "…", "fonte": "…", "tags": ["…"], "imagem": "" }
  ]
}
\`\`\`
Aspas duplas, aspas internas escapadas com \\", sem vírgula sobrando. Atributos HTML sem aspas (class=t) e, no SVG, use aspas simples nos atributos.
Se ficar longo, entregue em partes de no máximo 25 cards, cada uma como bloco JSON completo ("Parte 1/2").`;
}
const updPrompt = () => { $("#pOut").textContent = buildPrompt(); };
["#pTema", "#pSub", "#pN", "#pNivel", "#pTipo", "#pImg", "#pMat"].forEach(s => $(s).addEventListener("input", updPrompt));
$("#pCopy").onclick = async () => {
  try { await navigator.clipboard.writeText(buildPrompt()); toast("📋 Prompt copiado! Cole na IA."); }
  catch (e) { const r = document.createRange(); r.selectNodeContents($("#pOut")); const s = getSelection(); s.removeAllRanges(); s.addRange(r); toast("Selecionei o texto — use Copiar do sistema."); }
};

/* ---------------- UI: Ajustes ---------------- */
function fillSettings() {
  const s = S.settings; $("#sNew").value = s.newPerDay; $("#sRev").value = s.revPerDay; $("#sSteps").value = s.steps.join(" "); $("#sGrad").value = s.grad + " " + s.easy;
  $("#colsBox").innerHTML = (S.index?.colecoes || []).map(c => `<label class="btn" style="cursor:pointer"><input type="checkbox" data-col="${c.id}" ${s.cols[c.id] !== false ? "checked" : ""}> ${c.icone} ${esc(c.nome)} (${c.cards})</label>`).join(""); packInfo();
  $$("#colsBox [data-col]").forEach(cb => cb.onchange = async () => { S.settings.cols = Object.assign({}, S.settings.cols, { [cb.dataset.col]: cb.checked }); await saveSettings(); toast("⏳ Carregando coleções…"); await loadOfficial(); rebuildCards(); toast("✅ Coleções atualizadas"); });
  renderSyncUI();
  $("#aboutBox").innerHTML = `CÓDICE 360X v${APP_VERSION} · ${S.cards.length} cards ativos (${S.official.length} oficiais + ${S.user.size} próprios) · SM-2 estilo Anki.<br>Conteúdo educativo — não substitui julgamento clínico nem diretrizes institucionais. Confira editais e versões atuais das diretrizes.`;
}
$("#syncNow").onclick = () => {
  if (Hub.on) { Hub.etag = ""; S.prog.forEach(p => Hub.dirty.p.add(Hub.shP(p.id))); Hub.dirty.st = true; Hub.sync().then(() => { toast(Hub.err ? "⚠️ " + esc(Hub.err) : "☁️ Sincronizado com o GitHub"); renderSyncUI(); }); return; }
  S.prog.forEach(p => Cloud.dirty.p.add(shardP(p.id))); Cloud.dirty.st = true; Cloud.flush().then(() => { toast("☁️ Sincronizado"); fillSettings(); });
};
function renderSyncUI() {
  const info = $("#syncInfo"), box = $("#hubBox"), pb = $("#ponteBox"); if (!info || !box || !pb) return;
  const hm = t => t ? new Date(t).toLocaleString("pt-BR", { day: "2-digit", month: "2-digit", hour: "2-digit", minute: "2-digit" }) : "—";
  if (Hub.inClaude()) {
    info.innerHTML = Cloud.on ? `✅ <b>Nuvem do Claude ativa</b> — progresso, XP, questões e ajustes sincronizam sozinhos em todo aparelho que abrir <b>este link do Claude</b> (navegador do computador ou app Claude no iPhone). Última: <b>${hm(Cloud.lastSync)}</b>.`
      : `💾 Nuvem do Claude indisponível nesta visualização${Cloud.err ? ` (<span style="color:var(--red)">${esc(Cloud.err)}</span>)` : ""} — entre na sua conta do Claude.`;
    box.innerHTML = `<div class="hubNote">🐙 O app do <b>GitHub</b> sincroniza pelo GitHub. Esta página do Claude é isolada por segurança e não acessa o GitHub — para juntar os dois, use a 🌉 <b>Ponte</b> abaixo.</div>`;
    $("#syncNow").style.display = Cloud.on ? "" : "none";
  } else if (Hub.on) {
    const outros = Object.entries(Hub.devs).filter(([k]) => k !== Hub.cfg.dev).map(([, d]) => `<b>${esc(d.n)}</b> (${hm(d.t)})`).join(" · ") || "nenhum ainda — conecte o outro aparelho com a <b>mesma chave</b>";
    info.innerHTML = `✅ <b>Sincronização GitHub ativa</b> — automática: ao abrir o app, a cada 45 s e logo após você estudar.<br>📱 Este aparelho: <b>${esc(Hub.cfg.name || Hub.devName())}</b> · última: <b>${hm(Hub.lastSync)}</b>${Hub.err ? ` · <span style="color:var(--red)">${esc(Hub.err)}</span>` : ""}<br>🔗 Outros aparelhos: ${outros}`;
    box.innerHTML = `<div class="row" style="margin-top:8px"><button class="btn" id="hubCopy">📲 Copiar chave p/ outro aparelho</button><button class="btn danger" id="hubOff">🔌 Desconectar este aparelho</button></div>`;
    $("#syncNow").style.display = "";
    $("#hubCopy").onclick = async () => { try { await navigator.clipboard.writeText(Hub.cfg.token); toast("📋 Chave copiada — cole no outro aparelho em ⚙️ Ajustes"); } catch (e) { toast("Não consegui copiar — crie/cole a chave pelo GitHub."); } };
    $("#hubOff").onclick = () => { Hub.disconnect(); toast("🔌 Desconectado — o progresso continua salvo aqui"); renderSyncUI(); };
  } else {
    info.innerHTML = `💾 <b>Desligada</b> — o que você estuda aqui fica <b>só neste aparelho</b>. Ative uma vez em cada aparelho (iPhone e computador) com a <b>mesma chave</b>:`;
    box.innerHTML = `<ol class="hubSteps"><li>🔑 <a href="https://github.com/settings/tokens/new?scopes=gist&amp;description=CODICE%20360X%20sync" target="_blank" rel="noopener">Criar a chave no GitHub</a> — deixe marcado só <b>gist</b>, validade <b>No expiration</b> → <b>Generate token</b> → copie o código <b>ghp_…</b></li><li>📋 Cole aqui e toque em <b>Conectar</b>. Na 1ª vez, tudo o que você já estudou neste aparelho é <b>enviado (resgate)</b>.</li><li>💻 No outro aparelho, abra o mesmo app, ⚙️ Ajustes → cole a <b>mesma chave</b> → Conectar.</li></ol>
      <div class="row"><input type="password" id="hubTok" class="grow" placeholder="ghp_… (chave do GitHub)" autocomplete="off" autocapitalize="off" spellcheck="false"><input type="text" id="hubName" style="max-width:170px" value="${esc(Hub.devName())}" title="Nome deste aparelho"><button class="btn gold" id="hubGo">🔗 Conectar</button></div><div id="hubMsg" style="margin-top:6px;color:var(--mut)"></div>`;
    $("#syncNow").style.display = "none";
    $("#hubGo").onclick = async () => {
      const t = $("#hubTok").value.trim(), m = $("#hubMsg"); if (!/^(ghp_|github_pat_|gho_)[A-Za-z0-9_]{20,}$/.test(t)) { m.innerHTML = `<span style="color:var(--red)">Cole a chave completa (começa com ghp_).</span>`; return; }
      if (/^github_pat_/.test(t)) { m.innerHTML = `<span style="color:var(--red)">Essa é uma chave “fine-grained”, que não acessa gists. Use o link acima (Tokens <b>classic</b>, escopo gist).</span>`; return; }
      $("#hubGo").disabled = true; m.textContent = "⏳ Conectando e resgatando o progresso deste aparelho…";
      try { const n = await Hub.connect(t, $("#hubName").value.trim() || Hub.devName()); toast(`✅ Sincronização ativa · 🛟 ${n} card(s) com progresso enviados`, 4500); renderSyncUI(); }
      catch (e) { m.innerHTML = `<span style="color:var(--red)">❌ ${esc(e.message || e)}</span>`; $("#hubGo").disabled = false; }
    };
  }
  pb.innerHTML = `<h3 style="margin-top:0">🌉 Ponte Claude ⇄ GitHub</h3><p style="color:var(--mut);margin:4px 0 10px">Junta o progresso do app do GitHub com o da página do Claude (que não acessa o GitHub). 1) Num app: <b>📤 Copiar progresso</b>. 2) No outro: cole abaixo e <b>📥 Mesclar</b>. Nada é apagado — vale sempre a revisão mais recente de cada card.</p>
    <div class="row"><button class="btn cy" id="pnCopy">📤 Copiar progresso</button><small class="muted" id="pnSize"></small></div>
    <textarea id="pnIn" rows="3" placeholder="Cole aqui o código C360X-… copiado no outro app" style="width:100%;margin-top:8px;box-sizing:border-box"></textarea>
    <div class="row" style="margin-top:6px"><button class="btn gold" id="pnGo">📥 Mesclar progresso colado</button><small id="pnMsg" class="muted"></small></div>`;
  $("#pnCopy").onclick = async () => {
    const pr = Ponte.pack();
    try {
      if (window.ClipboardItem && navigator.clipboard && navigator.clipboard.write) await navigator.clipboard.write([new ClipboardItem({ "text/plain": pr.then(t => new Blob([t], { type: "text/plain" })) })]);
      else await navigator.clipboard.writeText(await pr);
      const t = await pr; $("#pnSize").textContent = `${(t.length / 1024).toFixed(0)} KB · ${S.prog.size} cards`; toast("📋 Progresso copiado — cole no outro app (🌉 Ponte)");
    } catch (e) { const t = await pr, ta = $("#pnIn"); ta.value = t; ta.focus(); ta.select(); $("#pnSize").textContent = "Selecionei o código: use Copiar do sistema."; }
  };
  $("#pnGo").onclick = async () => {
    const m = $("#pnMsg"); m.textContent = "⏳ Mesclando…";
    try { const r = await Ponte.importar($("#pnIn").value); renderSyncUI(); $("#pnMsg").innerHTML = `✅ ${r.gotP} card(s) atualizados aqui${Hub.on ? " · enviando ao GitHub" : Cloud.on ? " · enviando à nuvem do Claude" : ""}`; toast("🌉 Progresso mesclado"); }
    catch (e) { $("#pnMsg").innerHTML = `<span style="color:var(--red)">❌ ${esc(e.message || e)}</span>`; }
  };
}
$("#sSave").onclick = async () => {
  const nums = s => s.split(/[\s,;]+/).map(Number).filter(x => x > 0), g = nums($("#sGrad").value);
  Object.assign(S.settings, { newPerDay: Math.max(0, +$("#sNew").value || 0), revPerDay: Math.max(0, +$("#sRev").value || 0), steps: nums($("#sSteps").value).length ? nums($("#sSteps").value) : [1, 10], grad: g[0] || 1, easy: g[1] || 4 });
  await saveSettings(); toast("💾 Ajustes salvos"); rerender();
};
$("#bkExp").onclick = exportBackup;
$("#bkImp").onclick = () => $("#bkFile").click();
$("#bkFile").onchange = async () => { const f = $("#bkFile").files[0]; if (!f) return; try { await restoreBackup(JSON.parse(await f.text())); toast("🛟 Backup restaurado"); rerender(); fillSettings(); } catch (e) { toast("❌ " + esc(e.message)); } };
function confirmAction(msg, fn) {
  $("#confirmBox").innerHTML = `<div class="panel" style="border-color:var(--red)">${msg}<div class="row" style="margin-top:8px"><button class="btn danger" id="cfYes">Sim, confirmar</button><button class="btn" id="cfNo">Cancelar</button></div></div>`;
  $("#cfNo").onclick = () => $("#confirmBox").innerHTML = "";
  $("#cfYes").onclick = async () => { $("#confirmBox").innerHTML = ""; await fn(); rerender(); fillSettings(); };
}
$("#delGo").onclick = () => { const d = $("#delDeck").value; if (!d) return; const ids = [...S.user.values()].filter(u => u.deck === d || u.deck.startsWith(d + "::")).map(u => u.id);
  confirmAction(`Apagar <b>${ids.length}</b> cards próprios de <b>${esc(d)}</b>?`, async () => { await deleteUserCards(ids); toast("🗑️ Baralho apagado"); }); };
$("#resetProg").onclick = () => confirmAction("Zerar o progresso de <b>todos</b> os cards (em todos os aparelhos)?", async () => { const now = Date.now(); S.cards.forEach(c => { c.srs = newSRS(); c.susp = false; c.marked = false; S.prog.set(c.id, { id: c.id, s: c.srs, susp: false, mk: false, hl: c.hl || [], mod: now }); Cloud.markP(c.id); }); await DB.putMany("prog", [...S.prog.values()]); toast("♻️ Progresso zerado"); });
$("#wipe").onclick = () => confirmAction("Apagar <b>todos os seus cards próprios e o progresso</b>? (as coleções oficiais continuam). Faça backup antes.", async () => {
  const ids = [...S.user.keys()]; await deleteUserCards(ids); const now = Date.now();
  S.prog.forEach(p => { p.s = newSRS(); p.susp = false; p.mk = false; p.mod = now; Cloud.markP(p.id); }); await DB.putMany("prog", [...S.prog.values()]); rebuildCards(); toast("💣 Apagado");
});

/* ---------------- Roteamento ---------------- */
function rerender() {
  const v = (location.hash || "#inicio").slice(1);
  if (v === "inicio" || !v) refreshHome(); else if (v === "buscar") search(); else if (v === "ajustes") fillSettings();
}
function route() {
  const v = (location.hash || "#inicio").slice(1), valid = ["inicio", "estudar", "questoes", "micro", "mnemonicos", "honra", "jornada", "buscar", "importar", "prompt", "ajustes"], view = valid.includes(v) ? v : "inicio";
  $$(".view").forEach(s => s.classList.toggle("on", s.id === "v-" + view));
  $$("#nav a").forEach(a => a.classList.toggle("on", a.dataset.v === view));
  { const nav = $("#nav"), on = $("#nav a.on"); if (nav && on && nav.scrollWidth > nav.clientWidth + 1) nav.scrollLeft += on.getBoundingClientRect().left - nav.getBoundingClientRect().left - (nav.clientWidth - on.offsetWidth) / 2; }   // aba ativa sempre visível no celular
  if (view === "inicio") refreshHome();
  if (view === "estudar") { if (!Study.started) { const ss = S.session; startStudy(ss ? ss.prefix : null, ss && ss.ids ? ss.ids : null, true); return; } Study.view != null ? histShow() : (Study.cur && Study.shown ? histContinue() : showCard()); } else bars(null);
  if (view === "buscar") search();
  if (view === "questoes") QZ.open();
  if (view === "micro") MC.open();
  if (view === "mnemonicos") MN.open();
  if (view === "honra") HO.open();
  if (view === "jornada") JR.render();
  xpBadge();
  if (view === "prompt") updPrompt();
  if (view === "ajustes") fillSettings();
}
window.addEventListener("hashchange", route);
document.addEventListener("visibilitychange", () => { if (document.visibilityState === "hidden") { Cloud.flush(); if (Hub.firstMark || Hub.dirty.p.size || Hub.dirty.st) Hub.sync(); } else { Cloud.pull(); Hub.sync(); } });
window.addEventListener("online", () => { Cloud.flush(); Cloud.pull(); Hub.sync(); });
window.addEventListener("pageshow", () => { Cloud.pull(); Hub.sync(); });
setInterval(() => { if (document.visibilityState === "visible") { Cloud.pull(); if (!Hub.busy) Hub.sync(); } }, 45000);
$("#sync").addEventListener("click", () => { location.hash = "#ajustes"; });

(async function init() {
  try {
    await DB.open();
    const st = await DB.meta("settings", null);
    if (st && st.v) { S.settings = Object.assign({}, DEFAULTS, st.v); S.settingsMod = st.mod || 0; } else S.settings = Object.assign({}, DEFAULTS, st || {});
    S.settings.cols = Object.assign({ temi: true, cm: true, ia: true }, S.settings.cols || {});
    S.logs = await DB.meta("logs", {});
    S.session = await DB.meta("session", null);
    const old = await DB.get("meta", "log:" + today()); if (old && !S.logs[today()]) S.logs[today()] = old.v; // migração v1
    S.prog = new Map((await DB.all("prog")).map(p => [p.id, p]));
    S.user = new Map((await DB.all("user")).map(u => [u.id, u]));
    S.styles = new Map((await DB.all("styles")).map(s => [s.id, s.css]));
    Cloud.tomb = new Map(await DB.meta("tomb", []));
  } catch (e) { $("main").innerHTML = `<div class="panel">❌ O navegador bloqueou o armazenamento local (modo privado?).<br><small>${esc(e.message || e)}</small></div>`; return; }
  await loadOfficial(); rebuildCards(); route();
  HL.init();
  Cloud.init();
  Hub.init();
  if (!Hub.on && !Hub.inClaude() && S.prog.size) setTimeout(() => toast("☁️ Seu progresso está <b>só neste aparelho</b> — toque no selo do topo e ative a sincronização em ⚙️ Ajustes.", 6000), 2500);
  if (window.__selftest) window.__selftest();
})();
