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
  await p.setViewport({width:920, height:820, deviceScaleFactor:1.5});
  const url = "file:///C:/Users/absinghal/Downloads/Int/DSA_MASTER_REFERENCE_Quiz.html";
  await p.goto(url, {waitUntil:"networkidle0"});
  await p.screenshot({path:__dirname+"/quiz1.png"});
  // click a correct option (find the button whose text matches the answer) — click first option to show feedback
  await p.evaluate(()=>{ const opts=[...document.querySelectorAll('.opt')];
    // click the correct answer for a deterministic 'correct' screenshot
    const ans = document.getElementById('prompt').textContent;
    // just click the option that will be marked correct by clicking the known answer button
    const correctText = window.QUESTIONS ? null : null;
    (opts.find(o=>o.textContent==='Sliding Window')||opts[0]).click();
  });
  await new Promise(r=>setTimeout(r,300));
  await p.screenshot({path:__dirname+"/quiz2.png"});
  // switch to flashcards and flip
  await p.evaluate(()=>setMode('cards'));
  await p.evaluate(()=>flip());
  await new Promise(r=>setTimeout(r,600));
  await p.screenshot({path:__dirname+"/quiz3.png"});
  await b.close();
  console.log("shots written");
})().catch(e=>{console.error(e);process.exit(1);});
