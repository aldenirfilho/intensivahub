const E = require("./gaso_engine.js"), fs = require("fs");
const d = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
let bad = 0;
for (const c of d.casos) { const r = E.analyze(c.lab); if (r.codes.join("+") !== c.codes.join("+")) { bad++; console.log("❌", c.n, r.codes, c.codes); } }
console.log("casos", d.casos.length, "divergentes", bad);
