// Measures what actually crashed the tab: the RENDERER PROCESS memory (RSS of the
// whole Chrome tree), not the JS heap — decoded images live outside the JS heap,
// which is why the first version of this test showed 1MB while the tab died.
// Runs several full round trips, the exact path the user reported.
const puppeteer = require(process.env.HOME + '/.claude/skills/scroll-film-studio/scripts/node_modules/puppeteer-core');
const { execSync } = require('child_process');
const fs = require('fs');

const CHROME = ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/Applications/Chromium.app/Contents/MacOS/Chromium'].find(p => fs.existsSync(p));

function treeRssMB(pid){
  try {
    const out = execSync(`ps -Ao pid,ppid,rss | awk 'NR>1'`).toString().trim().split('\n')
      .map(l => l.trim().split(/\s+/).map(Number));
    const kids = new Map();
    for (const [p, pp, rss] of out){
      if (!kids.has(pp)) kids.set(pp, []);
      kids.get(pp).push([p, rss]);
    }
    let total = 0; const stack = [pid];
    const rssOf = new Map(out.map(([p, , rss]) => [p, rss]));
    const seen = new Set();
    while (stack.length){
      const p = stack.pop();
      if (seen.has(p)) continue; seen.add(p);
      total += rssOf.get(p) || 0;
      for (const [c] of (kids.get(p) || [])) stack.push(c);
    }
    return Math.round(total / 1024);
  } catch { return -1; }
}

(async () => {
  const browser = await puppeteer.launch({ executablePath: CHROME, headless: 'new', args: ['--no-sandbox'] });
  const pid = browser.process().pid;
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 800 });
  await page.goto('http://localhost:8899/index.html', { waitUntil: 'load' });
  await page.waitForFunction('window.__ready === true', { timeout: 30000 });

  const probe = async () => {
    const c = await page.evaluate(() => ({
      bmp: window.__bmpCount ? window.__bmpCount() : -1,
      img: window.__imgCount ? window.__imgCount() : -1,
    }));
    return { ...c, rss: treeRssMB(pid) };
  };

  const H = await page.evaluate(() => document.documentElement.scrollHeight - innerHeight);
  console.log('start        ', JSON.stringify(await probe()));

  const peak = { rss: 0, bmp: 0, img: 0 };
  for (let trip = 1; trip <= 3; trip++){
    for (const dir of ['down', 'up']){
      for (let i = 0; i <= 16; i++){
        const f = dir === 'down' ? i / 16 : 1 - i / 16;
        await page.evaluate(y => scrollTo(0, y), Math.round(H * f));
        await new Promise(r => setTimeout(r, 130));
      }
      const p = await probe();
      peak.rss = Math.max(peak.rss, p.rss);
      peak.bmp = Math.max(peak.bmp, p.bmp);
      peak.img = Math.max(peak.img, p.img);
      console.log(`trip ${trip} ${dir.padEnd(5)}`, `rss ${String(p.rss).padStart(5)}MB`,
                  ` bitmaps ${String(p.bmp).padStart(3)}`, ` imgs ${String(p.img).padStart(4)}`);
    }
  }
  const alive = await page.evaluate(() => !!document.getElementById('frame'));
  console.log(`PEAK rss ${peak.rss}MB · bitmaps ${peak.bmp} · imgs ${peak.img} · tab ${alive ? 'ALIVE' : 'DEAD'}`);
  await browser.close();
})();
