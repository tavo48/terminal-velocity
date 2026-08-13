// Per-tier performance: boot time AND jank, under CPU throttling.
// "Poor mobile performance" is usually boot time, not jank — measure both or you
// will chase the wrong one.
const puppeteer = require(process.env.HOME + '/.claude/skills/scroll-film-studio/scripts/node_modules/puppeteer-core');
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const CASES = [
  ['phone   390x844',  390,  844, 4],
  ['tablet  768x1024', 768, 1024, 2],
  ['desktop 1440x900', 1440, 900, 1],
];

(async () => {
  const b = await puppeteer.launch({ executablePath: CHROME, headless: 'new', args: ['--no-sandbox'] });
  for (const [label, w, h, cpu] of CASES) {
    const p = await b.newPage();
    await p.setViewport({ width: w, height: h, isMobile: cpu > 2, hasTouch: cpu > 2 });
    const c = await p.target().createCDPSession();
    await c.send('Emulation.setCPUThrottlingRate', { rate: cpu });
    const t0 = Date.now();
    await p.goto('http://localhost:8899/index.html', { waitUntil: 'load' });
    await p.waitForFunction('window.__ready===true', { timeout: 60000 });
    const ready = Date.now() - t0;
    await p.evaluate(() => { window.__d = []; let l = 0;
      (function f(t){ if (l) window.__d.push(t - l); l = t; requestAnimationFrame(f); })(performance.now()); });
    const H = await p.evaluate(() => document.documentElement.scrollHeight - innerHeight);
    for (let i = 0; i <= 30; i++){ await p.evaluate(y => scrollTo(0, y), Math.round(H*i/30)); await new Promise(r => setTimeout(r, 80)); }
    for (let i = 30; i >= 0; i--){ await p.evaluate(y => scrollTo(0, y), Math.round(H*i/30)); await new Promise(r => setTimeout(r, 80)); }
    const r = await p.evaluate(() => { const d = window.__d.slice().sort((a,x)=>a-x);
      return { max:+d[d.length-1].toFixed(1), p95:+d[Math.floor(d.length*.95)].toFixed(1),
               over50:d.filter(x=>x>50).length, n:d.length,
               dir: window.__filmDir ? window.__filmDir() : '?' }; });
    console.log(`${label}  cpu${cpu}x  tier ${r.dir.padEnd(9)} ready ${String(ready).padStart(5)}ms  p95 ${String(r.p95).padStart(5)}ms  max ${String(r.max).padStart(5)}ms  >50ms ${r.over50}/${r.n}`);
    await p.close();
  }
  await b.close();
})();
