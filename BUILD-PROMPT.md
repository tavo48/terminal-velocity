Build a single self-contained `index.html` — a **scroll-film website**. The entire hero is
one continuous 25-second cinematic shot that scrubs frame-by-frame as the visitor scrolls,
then resolves into product content. No `<video>` element anywhere: the film is a sequence
of JPEG frames painted to a `<canvas>`, and scroll position is the playhead.

Brand: **GEAR — Neural Visor XV**. A sealed helmet rated for atmospheric re-entry.
The shot: an armoured figure falls from the edge of space to a wet city street, straight
down, unbroken. The altimeter runs 98,000 m to 0.

---

## 1. THE FILM (frames — read this first)

You need 601 JPEG frames at 24fps named `f_0001.jpg` … `f_0601.jpg`. Pick one source:

- **A (easiest — the real film is already public)** — fetch it straight from the live
  deployment. Every frame is served with `access-control-allow-origin: *`, so cross-origin
  `fetch` + `createImageBitmap` works with no proxy and no credentials:

  ```
  https://terminal-velocity.pages.dev/<cut>/f_0001.jpg?v=2   …through f_0601.jpg
  cuts: frames (16:9 1440w) · frames-v (9:16 720w) · frames-m (480w) · frames-s (360w)
  ```

  Use this to build and verify against the genuine film. For production, copy the folders
  locally rather than hot-linking someone else's origin.
- **B** — generate the film yourself with an image-to-video model that pins **both** the
  first and last frame of each clip. Six keyframes, five 5s clips chained so that clip N's
  start image is the **ffmpeg-extracted literal last frame** of clip N−1 (not the keyframe).
  Then `ffmpeg -i master.mp4 -vf "fps=24,scale=1440:-1" -q:v 6 frames/f_%04d.jpg`.
- **C** — stub it: any 601 sequential images. The engine is the deliverable; the film is
  swappable.

The four cuts exist because **portrait must never letterbox**. Same frame count in every
cut so the playhead maps 1:1 when the tier swaps.

---

## 2. THE ENGINE — these are laws, not preferences. Each one is a bug I already paid for.

**2.1 Never use `HTMLImageElement` as the frame store.** Chrome keeps a decoded copy of
every image it paints in an internal cache that survives dropping the element *and* setting
`src=''`. Scrubbing 600 frames walks all of them: +90MB per round trip, unbounded, until the
renderer dies with "Aw, Snap!". Fetch bytes → `createImageBitmap` → `Map`. That way `close()`
genuinely frees. This also means **no `drawImage(imgElement)` fallback** — that "robust"
branch reintroduces the exact leak wearing a disguise.

```js
var bitmaps = new Map();     // idx -> ImageBitmap — the ONLY pixel store
var pending = new Map();
var BITMAP_BUDGET = TIER.budget * 1024 * 1024;
var frameW = 0, frameH = 0, displayed = -1;
var winLo = 0, winHi = 0, winCenter = -9999;
```

**2.2 Budget in BYTES, and make the window direction-aware.** Keep a window around the
playhead sized by `frameW*frameH*4`, weighted toward the scroll direction; evict the far
edge with `close()`. Never a fixed frame count — a 1440w frame and a 360w frame differ 16×.

**2.3 Decode in a Worker.** Safari does not decode `createImageBitmap` off the main thread
the way Chrome does, so every frame lands on the thread running the scroll. Trap: a Worker
built from a Blob URL has a `blob:` base, so **relative paths silently resolve to nothing** —
no error, black canvas. Absolutise before posting.

```js
var src = "self.onmessage=function(e){var d=e.data;" +
  "fetch(d.url,{cache:'force-cache'}).then(function(r){return r.blob()})" +
  ".then(createImageBitmap)" +
  ".then(function(b){self.postMessage({idx:d.idx,bm:b},[b])})" +
  ".catch(function(){self.postMessage({idx:d.idx,err:1})})};";
var decoder = new Worker(URL.createObjectURL(new Blob([src], {type:'text/javascript'})));
decoder.postMessage({ idx: i, url: new URL(FRAME_PATH(i), location.href).href });
```

**2.4 Pick the cut by ASPECT RATIO, not width.** A tablet is wide in pixels and portrait in
shape; choosing by width letterboxes it.

```js
var MQ_PORTRAIT = matchMedia('(max-aspect-ratio: 1/1)');
var IS_IOS = /iP(hone|ad|od)/.test(navigator.platform) ||
             (navigator.maxTouchPoints > 1 && /Mac/.test(navigator.platform)) ||
             /iPhone|iPad|iPod/.test(navigator.userAgent);
function pickTier(){
  if (!MQ_PORTRAIT.matches) return { dir:'frames',   budget:120, conc:8, lerp:0.14 };
  if (IS_IOS || Math.min(innerWidth, innerHeight) <= 430)
    return { dir:'frames-s', budget:34,  conc:4, lerp:0.30 };
  if (Math.min(innerWidth, innerHeight) <= 700 || (navigator.deviceMemory || 8) <= 4)
    return { dir:'frames-m', budget:52,  conc:5, lerp:0.20 };
  return { dir:'frames-v', budget:100, conc:7, lerp:0.16 };
}
```
On a tier swap, `close()` every bitmap from the old cut before refilling or it leaks on
every rotation. Note the phone `lerp` is **higher**: a long smoothing tail reads as *stuck*
when the browser is already dropping frames.

**2.5 Always cover, never letterbox.**
```js
function paint(src){
  var cw=canvas.width, ch=canvas.height, iw=src.width, ih=src.height;
  var s=Math.max(cw/iw, ch/ih), w=iw*s, h=ih*s;
  ctx.drawImage(src, (cw-w)/2, (ch-h)/2, w, h);
}
```
Cap DPR at 1.0 and match source width to canvas width instead. Upscaling a frame reads as
"pixelated", which tempts you to raise DPR and makes it worse.

**2.6 `100svh`, never `100dvh`, on the sticky stage.** iOS resizes `dvh` *continuously*
while the URL bar collapses during a drag, so every scroll fires resize and every resize
reallocates `canvas.width` mid-gesture. That is the iPhone stutter.

```css
#stage{position:sticky;top:0;height:100vh;height:100svh;overflow:hidden;background:#000}
```
```js
function sizeCanvas(){                    // idempotent — returns false when unchanged
  var w=Math.round(stage.clientWidth), h=Math.round(stage.clientHeight);
  if (w===canvas.width && h===canvas.height) return false;
  canvas.width=w; canvas.height=h; return true;
}
```
**One** debounced (~120ms) resize handler. Several handlers each doing part of the job will
fight each other invisibly.

**2.7 Open the window before you wait on it.** Compute the prefetch window from *guessed*
frame dimensions and it comes out smaller than the boot target, so boot always falls through
to the emergency timeout — a 10-second blank load that profiles as "slow network". Re-open
the window once real dimensions are known, and clamp: `need = Math.min(BOOT_TARGET, winHi-winLo+1)`.
`BOOT_TARGET = 24`.

**2.8 Version the frame URLs.** Frames are served `immutable` for a year, so a re-cut that
reuses filenames pins every returning visitor to the old film forever — it presents as "the
deploy did nothing".

```js
var FILM_V = '2';   // bump on every re-cut
var FRAME_PATH = function(i){ return TIER.dir+'/f_'+String(i+1).padStart(4,'0')+'.jpg?v='+FILM_V; };
```

**2.9 Dev hooks, required:** `?jump=<scrollY>` lands pre-scrolled with all scroll state
force-settled; `window.__ready = true` only once the target frame is decoded; expose
`window.__frameIdx = () => displayed` and `window.__filmDir = () => TIER.dir`. A windowed
loader breaks `?jump` silently — a deep jump has nothing decoded in its window and
photographs black while `__ready` fires anyway. The jump path must fetch its own window.

**2.10 Respect `prefers-reduced-motion`** — hold a single representative frame.

---

## 3. THE WORLD (exact)

```css
--ink:#000000;  --paper:#0a0a0a;  --accent:#f5e100;  --ember:#d2500f;
--hot:#ff7a1a;  --steel:#8f9296;  --text:#f2f2f2;    --dim:#9a9a9a;
--seam:#010101; --edge:rgba(255,255,255,.12);
```
Fonts (Google): **Zen Dots** for display, **Chakra Petch** for UI/body.
`border-radius: 0` everywhere. **No box-shadows** — depth comes from gradients and light only.
Wordmark `GEAR` as inline SVG, never an image.

`FRAME_COUNT = 601`. Chapters, driven by scroll progress:
`EXOSPHERE · ENTRY · CLOUD DECK · APPROACH · TERMINAL`

---

## 4. THE PAGE

Fixed chrome over the film: `GEAR` wordmark top-left; nav `SYSTEM / SPEC / ISSUE` top-right;
bottom-left a live **altimeter** counting 98,000 → 0 (large numerals, `M AGL` label);
bottom-right the current chapter name with a thin progress rule. The chrome must invert or
soften as the film brightens — it sits over changing footage.

**Beats** — copy pinned to scroll fractions, fading in/peaking/out. Left-aligned:

| in | peak | out | text |
|---|---|---|---|
| −0.10 | 0.000 | 0.12 | **RATED FOR THE WHOLE WAY DOWN** (h1, eyebrow `NEURAL VISOR XV`) |
| 0.16 | 0.235 | 0.32 | "1,600° on the shell. Twenty-one behind the glass." |
| 0.38 | 0.460 | 0.55 | "Blink and you miss another thousand metres." |
| 0.62 | 0.700 | 0.79 | "It reads the ground from four kilometres out." |
| 0.88 | 0.955 | 2.00 | **BUILT TO ARRIVE** + CTA `REQUEST ISSUE` |

Beat scrims must be painted on the block itself, **not** a `::before` with `z-index:-1` — a
negative-z pseudo-element cannot escape its parent's stacking context and lands over the
text. Absolutely-positioned beats need `right:0` or the scrim shrinks to the text and reads
as a visible rectangle. Drive vertical offsets with a CSS custom property (`--beat-y`), never
an inline `transform`, or JS will override the mobile stylesheet.

### The helmet turntable (`#product`) — full-bleed and draggable

The hero helmet is **not a static `<img>`**. It spans the full frame width and the visitor
rotates it by dragging. Build it with the *same engine as the film* — a frame scrub on a
canvas, driven by pointer delta instead of scroll. No WebGL, no 3D model, no new dependency:

- `product/turn/t_0001.jpg` … `t_0048.jpg` — one 360° orbit of the helmet on pure black.
- Reuse the bitmap store, the byte budget and the windowed prefetch verbatim. The frame
  index wraps (`(i % N + N) % N`) so the spin is endless in both directions.
- `pointerdown/move/up` + `touch-action: none` on the canvas; ~`N / 600px` of drag per full
  revolution. Add inertia on release and a slow idle auto-rotate that stops on first
  interaction. Arrow keys step one frame — it must be operable without a mouse.
- Preload only ~8 frames around the current index; this section is below the fold and must
  not compete with the film for bandwidth.
- Cursor `grab` / `grabbing`, and a one-time hint that disappears after the first drag.
  Never label it "drag to rotate" in body copy — the cursor and the idle spin say it.
- `prefers-reduced-motion`: no idle spin, drag still works.

**Generating the orbit:** pin the clip's first and last frame to the *same* image so the
loop is forced to close — otherwise the object drifts a few degrees per second and the
helmet subtly changes shape as it turns. Black background, one continuous orbit, camera
moves and the object stays put. If a full 360° will not hold, a 120° arc scrubbed back and
forth still reads as interactive and is far more reliable.

Below the film: `#product` (helmet, 3 detail shots), `#system`, `#spec` (a numbered spec
table — thermal shell 1,600°, sealed optics 240°, terrain lock 4.2 km, charge cell 31 h,
cowl 0.9 kg), `#issue`, and a closing band.

**The seam:** sample the last frame's bottom 12% and start the first content section on
exactly that colour, then gradient away. A visible line between film and page kills the
illusion. Same discipline for image assets: level their black point to the page black or the
asset reads as a pasted rectangle.

**Never let the page narrate its own mechanic.** No "scroll to explore", no "as you scroll
the frame narrows". The page performs the idea; it does not describe it.

---

## 5. VERIFY BEFORE CALLING IT DONE

Boot it in a real browser at 1440×900, 768×1024 and 390×844. Assert: zero console errors,
zero 4xx, `__ready` true, the correct tier per shape, and that frames actually **change**
across scroll stations. Memory must be **flat** across three full scroll round-trips —
measure the browser process RSS, not `performance.memory`, which only sees the JS heap and
will read 1MB while the tab is dying. Judge jank by p95/max rAF delta, never average fps.

Deliver one `index.html`, self-contained apart from the frame folders and the Google Fonts
link.
