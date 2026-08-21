const puppeteer = require("puppeteer-core");
const fs = require("fs");
function findBrowser(){
  for (const c of ["C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
    "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe"]) if (fs.existsSync(c)) return c;
  throw new Error("no browser");
}
(async()=>{
  const b = await puppeteer.launch({executablePath:findBrowser(), headless:"new", args:["--no-sandbox"]});
  const p = await b.newPage();
  await p.setViewport({width:760, height:230, deviceScaleFactor:2});
  await p.goto("file:///"+__dirname.replace(/\\/g,"/")+"/poc.html", {waitUntil:"networkidle0"});
  const el = await p.$("#cap-target");
  await el.screenshot({path:__dirname+"/poc.png"});
  await b.close();
  console.log("shot written");
})().catch(e=>{console.error(e);process.exit(1);});
