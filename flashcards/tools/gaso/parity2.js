const E = require("./gaso_engine.js"), fs = require("fs");
const d = JSON.parse(fs.readFileSync("/tmp/parity2.json", "utf8")); let bc = 0, bn = 0, bs = 0, bp = 0;
for (const c of d) { const r = E.analyze(c.lab);
  if (r.codes.join("+") !== c.codes.join("+")) bc++;
  for (const k of Object.keys(c.x)) if (Math.abs(c.x[k] - r.x[k]) > 1e-6) bn++;
  if (Object.keys(c.x).length !== Object.keys(r.x).length) bn++;
  if (JSON.stringify(c.xsteps) !== JSON.stringify(r.xsteps)) { bs++; if (bs < 4) console.log("PY:", c.xsteps, "\nJS:", r.xsteps); }
  if (E.panel(c.lab) !== c.panel) { bp++; if (bp < 3) console.log("PANEL PY:", c.panel.slice(-400), "\nJS:", E.panel(c.lab).slice(-400)); } }
console.log("extras", d.length, "códigos≠", bc, "números≠", bn, "textos≠", bs, "painéis≠", bp);
