// Renders output8.html (or output8_dark.html) -> DSA_MASTER_REFERENCE8.pdf
// Runs the same render.js logic but with v8 output paths.
process.env.DSA_HTML_LIGHT = "output8.html";
process.env.DSA_HTML_DARK = "output8_dark.html";
process.env.DSA_PDF_LIGHT = "C:\\Users\\absinghal\\Downloads\\Int\\DSA_MASTER_REFERENCE9.pdf";
process.env.DSA_PDF_DARK = "C:\\Users\\absinghal\\Downloads\\Int\\DSA_MASTER_REFERENCE9_dark.pdf";

const fs = require("fs");
const path = require("path");
let code = fs.readFileSync(path.join(__dirname, "render.js"), "utf-8");

code = code.replace(
    'const htmlPath = path.join(__dirname, dark ? "output_dark.html" : "output.html");',
    'const htmlPath = path.join(__dirname, dark ? (process.env.DSA_HTML_DARK || "output_dark.html") : (process.env.DSA_HTML_LIGHT || "output.html"));'
);
code = code.replace(
    /const outPath = dark[\s\S]*?"C:\\\\Users\\\\absinghal\\\\Downloads\\\\Int\\\\DSA_MASTER_REFERENCE7\.pdf";/,
    'const outPath = dark ? (process.env.DSA_PDF_DARK || "C:\\\\Users\\\\absinghal\\\\Downloads\\\\Int\\\\DSA_MASTER_REFERENCE7_dark.pdf") : (process.env.DSA_PDF_LIGHT || "C:\\\\Users\\\\absinghal\\\\Downloads\\\\Int\\\\DSA_MASTER_REFERENCE7.pdf");'
);

const tmp = path.join(__dirname, ".render8-tmp.js");
fs.writeFileSync(tmp, code);
require(tmp);
