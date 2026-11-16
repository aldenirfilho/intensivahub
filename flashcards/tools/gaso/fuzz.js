const E = require("./gaso_engine.js"), fs = require("fs");
const d = JSON.parse(fs.readFileSync("/tmp/fuzz.json", "utf8")); let bad = 0, num = 0;
for (const c of d.casos) { const r = E.analyze(c.lab);
  if (r.codes.join("+") !== c.codes.join("+")) { bad++; if (bad < 6) console.log("❌", JSON.stringify(c.lab), r.codes, c.codes); }
  for (const k of ["dd", "aa", "ogap"]) if (c[k] != null && Math.abs(c[k] - r[k]) > 1e-6) num++; }
console.log("fuzz", d.casos.length, "códigos divergentes", bad, "números divergentes", num);
