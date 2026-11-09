/* CÓDICE 360X · Flashcards v2
   - Coleções oficiais (TEMI 2028 + R3 Clínica Médica) carregadas dos arquivos do app
   - Cards do usuário + progresso em IndexedDB (cache local) e, numa página do Claude, sincronizados
     automaticamente na nuvem do artifact (db por usuário) — mesmo login = mesmo progresso em todos os aparelhos.
   - Importa .apkg (Anki legado e 2.1.50+), JSON de qualquer IA e TXT/CSV. */
"use strict";
const APP_VERSION = "4.2.1";
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
const act = l => !l ? 0 : (l.nAns === undefined && !l.xp ? Object.keys(l).length : (l.nAns || 0) + (l.qN || 0) + (l.mN || 0) + (l.sims || []).length + (l.xp || 0) / 1000);
const dayLogs = () => Object.entries(S.logs).filter(([k]) => /^\d/.test(k));
const QRES = () => (S.logs._q = S.logs._q || {}), MRES = () => (S.logs._m = S.logs._m || {});
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
      for (const [d, l] of Object.entries(data.logs || {})) { const cur = S.logs[d]; if (!cur || act(l) > act(cur)) { S.logs[d] = l; changed = true; } }
      if (data.session && (!S.session || data.session.mod > S.session.mod)) { S.session = data.session; DB.setMeta("session", S.session); changed = true; }
      if (S.session && (!data.session || S.session.mod > data.session.mod)) this.dirty.st = true;
      if (changed) DB.setMeta("logs", S.logs);
      // se meu log local de algum dia é maior, preciso enviar
      for (const [d, l] of Object.entries(S.logs)) if (!data.logs || !data.logs[d] || act(data.logs[d]) < act(l)) this.dirty.st = true;
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
  markP(id) { this.dirty.p.add(shardP(id)); this.schedule(); },
  markU(id) { this.dirty.u.add(shardU(id)); this.schedule(); },
  markSt() { this.dirty.st = true; this.schedule(); },
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
        const keep = Object.keys(S.logs).sort().slice(-120); const logs = {}; keep.forEach(k => logs[k] = S.logs[k]);
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
  async function worker() {
    while (next < decks.length) {
      const i = next++, d = decks[i]; let j = null;
      if (!offline) {
        try { j = await fetchJSON(d.arquivo); if (needCache) DB.setMeta("deck:" + d.arquivo, j).catch(() => {}); }
        catch (e) { console.warn("baralho falhou", d.arquivo, e); }
      }
      if (!j) { j = await DB.meta("deck:" + d.arquivo, null).catch(() => null); if (j) fromCache++; else failed.push(d.arquivo); }
      res[i] = j;
    }
  }
  await Promise.all(Array.from({ length: Math.min(6, decks.length) }, worker));
  if (!failed.length && !offline && needCache) DB.setMeta("offCacheVer", idx.versao).catch(() => {});
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
  else if (offline || fromCache) toast(`📦 Sem internet estável: usando a cópia salva no aparelho (${fromCache || decks.length} baralhos).`);
  if (!failed.length) officialRetry = 0;
}
document.addEventListener("click", async e => {
  if (!e.target.closest || !e.target.closest("#reloadCols")) return;
  toast("⏳ Baixando as coleções de novo…"); await DB.setMeta("offCacheVer", "").catch(() => {});
  officialRetry = 0; await loadOfficial(); rebuildCards(); try { rerender(); } catch (er) { route(); }
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
  root.innerHTML = `<style>:host{display:block}${extra}${css}${HL_CSS}</style><div class="card nightMode night_mode" style="--acc:${accentFor(deck)}">${sanitize(html)}</div>`;
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
  async load() { if (!this.data) this.data = await fetch("data/micro.json").then(r => r.json()).catch(() => ({ temi: [], r3: [] })); },
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


/* ---------------- Jornada: conquistas, ranking semanal e painéis ---------------- */
const ACH_T = { medalha: "🏅 Medalhas", trofeu: "🏆 Troféus", titulo: "📜 Títulos", brasao: "🛡️ Brasões", honra: "🎖️ Honrarias" };
const ACH_BONUS = { medalha: 20, trofeu: 40, titulo: 50, brasao: 80, honra: 150 };
const XPSRC = { c: ["🎴 Flashcards", "#4dd4ff"], s: ["🧪 Simulados", "#ffc14d"], q: ["❓ Questões", "#5be38a"], r: ["📖 Leitura e comentários", "#b48cff"], m: ["💊 Micropartículas", "#ff8fb1"], a: ["🏆 Conquistas", "#e8c56a"] };
const isoWeek = t => { const d = new Date(t); d.setHours(0, 0, 0, 0); d.setDate(d.getDate() - ((d.getDay() + 6) % 7)); return d.getTime(); };
function jStats() {
  const days = dayLogs().sort((a, b) => a[0].localeCompare(b[0])), act = l => (l.nAns || 0) + (l.qN || 0) + (l.mN || 0) + (l.sims || []).length > 0;
  const on = new Set(days.filter(([, l]) => act(l)).map(([d]) => d));
  let cur = 0; for (let i = on.has(today()) ? 0 : 1; on.has(dayKey(Date.now() - i * DAY)); i++) cur++;
  let max = 0, run = 0, prev = null; for (const d of [...on].sort()) { const t = new Date(d + "T12:00").getTime(); run = prev && Math.round((t - prev) / DAY) === 1 ? run + 1 : 1; max = Math.max(max, run); prev = t; }
  const sims = days.flatMap(([, l]) => l.sims || []).filter(x => x.n >= 10).map(x => Math.round(100 * x.ok / x.n));
  const Q = S.logs._q || {}, qv = Object.values(Q), qOk = qv.filter(x => x[0]).length;
  const nNew = S.settings.newPerDay || 0, metaDays = days.filter(([, l]) => nNew && (l.nNew || 0) >= nNew).length;
  const wk = {}; for (const [d, l] of days) { const w = isoWeek(new Date(d + "T12:00").getTime()); wk[w] = (wk[w] || 0) + (l.xp || 0); }
  const xs = {}; for (const [, l] of days) for (const [k, v] of Object.entries(l.xs || {})) xs[k] = (xs[k] || 0) + v;
  return { cur, max: Math.max(max, cur), xp: xpTotal(), lv: levelOf(xpTotal()).lv, sims, qAns: qv.length, qAcc: qv.length ? qOk / qv.length : 0, qc: Object.keys(S.logs._qc || {}).length,
    mic: Object.keys(S.logs._m || {}).length, cards: days.reduce((a, [, l]) => a + (l.nAns || 0), 0), metaDays, wk, xs, days };
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
    [[10, "medalha"], [50, "trofeu"], [100, "brasao"], [200, "honra"]].forEach(([n, t]) => A("mc" + n, t, "💊", `Alquimista ${n}`, `Ler ${n} micropartículas (☑️)`, s => s.mic, n));
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
  $("#colsBox").innerHTML = (S.index?.colecoes || []).map(c => `<label class="btn" style="cursor:pointer"><input type="checkbox" data-col="${c.id}" ${s.cols[c.id] !== false ? "checked" : ""}> ${c.icone} ${esc(c.nome)} (${c.cards})</label>`).join("");
  $$("#colsBox [data-col]").forEach(cb => cb.onchange = async () => { S.settings.cols = Object.assign({}, S.settings.cols, { [cb.dataset.col]: cb.checked }); await saveSettings(); toast("⏳ Carregando coleções…"); await loadOfficial(); rebuildCards(); toast("✅ Coleções atualizadas"); });
  $("#syncInfo").innerHTML = Cloud.on ? `☁️ Ativa — progresso, ajustes e cards próprios vão para sua conta. Última sincronização: <b>${new Date(Cloud.lastSync).toLocaleTimeString("pt-BR")}</b>.` :
    `💾 Desativada nesta visualização${Cloud.err ? ` (<span style="color:var(--red)">${esc(Cloud.err)}</span>)` : ""}. A sincronização automática funciona quando o app é aberto pela página do Claude, logado.`;
  $("#syncNow").style.display = Cloud.on ? "" : "none";
  $("#aboutBox").innerHTML = `CÓDICE 360X v${APP_VERSION} · ${S.cards.length} cards ativos (${S.official.length} oficiais + ${S.user.size} próprios) · SM-2 estilo Anki.<br>Conteúdo educativo — não substitui julgamento clínico nem diretrizes institucionais. Confira editais e versões atuais das diretrizes.`;
}
$("#syncNow").onclick = () => { S.prog.forEach(p => Cloud.dirty.p.add(shardP(p.id))); Cloud.dirty.st = true; Cloud.flush().then(() => { toast("☁️ Sincronizado"); fillSettings(); }); };
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
  const v = (location.hash || "#inicio").slice(1), valid = ["inicio", "estudar", "questoes", "micro", "jornada", "buscar", "importar", "prompt", "ajustes"], view = valid.includes(v) ? v : "inicio";
  $$(".view").forEach(s => s.classList.toggle("on", s.id === "v-" + view));
  $$("#nav a").forEach(a => a.classList.toggle("on", a.dataset.v === view));
  if (view === "inicio") refreshHome();
  if (view === "estudar") { if (!Study.started) { const ss = S.session; startStudy(ss ? ss.prefix : null, ss && ss.ids ? ss.ids : null, true); return; } Study.view != null ? histShow() : (Study.cur && Study.shown ? histContinue() : showCard()); } else bars(null);
  if (view === "buscar") search();
  if (view === "questoes") QZ.open();
  if (view === "micro") MC.open();
  if (view === "jornada") JR.render();
  xpBadge();
  if (view === "prompt") updPrompt();
  if (view === "ajustes") fillSettings();
}
window.addEventListener("hashchange", route);
document.addEventListener("visibilitychange", () => { if (document.visibilityState === "hidden") Cloud.flush(); else Cloud.pull(); });
window.addEventListener("online", () => { Cloud.flush(); Cloud.pull(); });
window.addEventListener("pageshow", () => Cloud.pull());
setInterval(() => { if (document.visibilityState === "visible") Cloud.pull(); }, 45000);

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
  if (window.__selftest) window.__selftest();
})();
