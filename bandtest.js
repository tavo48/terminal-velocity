// Proves there are no letterbox bands: samples the canvas corners at several
// viewport shapes. A band shows up as corners that are pure black or identical
// to each other while the centre is not.
const puppeteer = require(process.env.HOME + '/.claude/skills/scroll-film-studio/scripts/node_modules/puppeteer-core');
const fs = require('fs');
const CHROME = ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/Applications/Chromium.app/Contents/MacOS/Chromium'].find(p => fs.existsSync(p));

const SHAPES = [
  ['desktop  1440x900', 1440, 900],
  ['laptop   1280x800', 1280, 800],
  ['tablet L 1024x768', 1024, 768],
  ['tablet P  768x1024', 768, 1024],
  ['near-sq   900x970', 900, 970],
  ['phone     390x844', 390, 844],
  ['ultrawide 2560x1080', 2560, 1080],
];

(async () => {
  const browser = await puppeteer.launch({ executablePath: CHROME, headless: 'new', args: ['--no-sandbox'] });
  for (const [label, w, h] of SHAPES) {
    const page = await browser.newPage();
    await page.setViewport({ width: w, height: h });
    await page.goto('http://localhost:8899/index.html?jump=2600', { waitUntil: 'load' });
    await page.waitForFunction('window.__ready === true', { timeout: 30000 });
    await new Promise(r => setTimeout(r, 900));
    const r = await page.evaluate(() => {
      const c = document.getElementById('frame');
      const g = c.getContext('2d');
      const p = (x, y) => Array.from(g.getImageData(x, y, 1, 1).data.slice(0, 3));
      const inset = 3;
      return {
        film: window.__filmDir ? window.__filmDir() : '?',
        tl: p(inset, inset), tr: p(c.width - inset, inset),
        bl: p(inset, c.height - inset), br: p(c.width - inset, c.height - inset),
      };
    });
    // a corner that is exactly black on every channel is a band, not footage
    const dead = ['tl','tr','bl','br'].filter(k => r[k][0] === 0 && r[k][1] === 0 && r[k][2] === 0);
    console.log(label.padEnd(20), r.film.padEnd(9),
      dead.length ? 'BAND at ' + dead.join(',') : 'covered', '  corners',
      JSON.stringify([r.tl, r.tr, r.bl, r.br]));
    await page.close();
  }
  await browser.close();
})();
