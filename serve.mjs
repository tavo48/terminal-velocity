// Minimal static server for local preview.
//
// Python's http.server is not usable here: it evaluates os.getcwd() at import time to build
// its --directory default, and the sandbox denies that call, so the module dies before main()
// ever runs. Nothing about the arguments can avoid it. Node has no equivalent trip-wire.
//
// Root is resolved from this file's own location, so the server never depends on the working
// directory it happens to be launched from.
import { createServer } from 'node:http';
import { createReadStream, promises as fs } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join, normalize, extname, sep } from 'node:path';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), 'site');
const PORT = Number(process.env.PORT || 8811);

const TYPES = {
  '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8', '.json': 'application/json',
  '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png',
  '.webp': 'image/webp', '.avif': 'image/avif', '.svg': 'image/svg+xml',
  '.mp4': 'video/mp4', '.woff2': 'font/woff2', '.ico': 'image/x-icon',
};

createServer(async (req, res) => {
  try {
    let p = decodeURIComponent(new URL(req.url, 'http://x').pathname);
    if (p.endsWith('/')) p += 'index.html';
    // normalize first, then require the result to stay under ROOT — ".." can never escape
    const file = normalize(join(ROOT, p));
    if (file !== ROOT && !file.startsWith(ROOT + sep)) {
      res.writeHead(403).end('forbidden');
      return;
    }
    const stat = await fs.stat(file);
    if (stat.isDirectory()) {
      res.writeHead(301, { Location: p + '/' }).end();
      return;
    }
    res.writeHead(200, {
      'Content-Type': TYPES[extname(file).toLowerCase()] || 'application/octet-stream',
      'Content-Length': stat.size,
      // never cache locally: the whole point of the preview is seeing the edit you just made
      'Cache-Control': 'no-store',
    });
    createReadStream(file).pipe(res);
  } catch {
    res.writeHead(404, { 'Content-Type': 'text/plain' }).end('not found');
  }
}).listen(PORT, () => console.log(`serving ${ROOT} on http://localhost:${PORT}`));
