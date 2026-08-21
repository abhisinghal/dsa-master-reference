// Render output.html -> DSA_MASTER_REFERENCE.pdf via installed Chrome/Edge.
// High-quality print settings: 3x device scale, wait for fonts, medium hinting.
const puppeteer = require("puppeteer-core");
const path = require("path");
const fs = require("fs");

function findBrowser() {
  const cands = [
    "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
    "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
    "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe",
  ];
  for (const c of cands) if (fs.existsSync(c)) return c;
  throw new Error("No Chrome/Edge found");
}

(async () => {
  const theme = (process.argv[2] || "light").toLowerCase();
  const dark = theme === "dark";
  const htmlPath = path.join(__dirname, dark ? "output_dark.html" : "output.html");
  const outPath = dark
    ? "C:\\Users\\absinghal\\Downloads\\Int\\DSA_MASTER_REFERENCE7_dark.pdf"
    : "C:\\Users\\absinghal\\Downloads\\Int\\DSA_MASTER_REFERENCE7.pdf";
  const browser = await puppeteer.launch({
    executablePath: findBrowser(),
    headless: "new",
    // font-render-hinting=medium is empirically the best for print PDFs on Windows —
    // yields sharper glyph edges than 'none' without the over-hinted look of 'full'.
    // force-color-profile=srgb keeps color reproduction consistent across devices.
    args: [
      "--no-sandbox",
      "--disable-setuid-sandbox",
      "--font-render-hinting=medium",
      "--force-color-profile=srgb",
      "--enable-font-antialiasing",
      "--disable-gpu-driver-bug-workarounds",
    ],
  });
  const page = await browser.newPage();
  // 3x device scale factor — every raster/SVG element is captured at 3x native DPI (≈288 DPI equivalent).
  // Viewport chosen to be A4-ish at 3x so the reflow matches print exactly.
  await page.setViewport({ width: 1240, height: 1754, deviceScaleFactor: 3 });
  await page.emulateMediaType("print");
  await page.goto("file:///" + htmlPath.replace(/\\/g, "/"), { waitUntil: "networkidle0" });
  // Wait for all custom @font-face fonts to be fully loaded — otherwise the printer
  // uses a fallback and the glyphs re-lay-out later, blurring the raster.
  await page.evaluate(async () => {
    if (document.fonts && document.fonts.ready) await document.fonts.ready;
    if (window.mermaid) {
      try { await window.mermaid.run(); } catch (e) { console.error("mermaid:", e.message); }
    }
    // Force the highest-fidelity text rendering path — geometricPrecision on <html>
    // propagates to every descendant that doesn't override it.
    document.documentElement.style.textRendering = "geometricPrecision";
    document.documentElement.style.webkitFontSmoothing = "antialiased";
    document.documentElement.style.mozOsxFontSmoothing = "grayscale";
    // Ensure background colors print exactly (Chrome sometimes strips them).
    document.documentElement.style.webkitPrintColorAdjust = "exact";
    document.documentElement.style.colorAdjust = "exact";
    document.documentElement.style.printColorAdjust = "exact";
  });
  // Longer settle time — lets mermaid finish, fonts finish loading and painting.
  await new Promise(r => setTimeout(r, 1200));
  const pdfOpts = dark
    ? { path: outPath, format: "A4", printBackground: true, displayHeaderFooter: false,
        preferCSSPageSize: false,
        margin: { top: "0", bottom: "0", left: "0", right: "0" } }
    : { path: outPath, format: "A4", printBackground: true, displayHeaderFooter: true,
        preferCSSPageSize: false,
        margin: { top: "16mm", bottom: "15mm", left: "13mm", right: "13mm" },
        headerTemplate: `<div style="font-size:8px;color:#9aa4b2;width:100%;padding:0 13mm;
            font-family:Segoe UI,Arial;display:flex;justify-content:space-between;">
            <span>DSA MASTER REFERENCE</span><span>Senior / Staff Interview Prep</span></div>`,
        footerTemplate: `<div style="font-size:8px;color:#9aa4b2;width:100%;padding:0 13mm;
            font-family:Segoe UI,Arial;display:flex;justify-content:space-between;">
            <span>© DSA Master Reference</span>
            <span>Page <span class="pageNumber"></span> / <span class="totalPages"></span></span></div>` };
  await page.pdf(pdfOpts);
  await browser.close();
  const kb = (fs.statSync(outPath).size / 1024).toFixed(0);
  console.log("PDF written:", outPath, kb + " KB");
})().catch(e => { console.error(e); process.exit(1); });
