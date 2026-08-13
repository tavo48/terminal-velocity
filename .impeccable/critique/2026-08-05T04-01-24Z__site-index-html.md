---
target: site/index.html
total_score: 23
max_score: 36
na_heuristics: 10
p0_count: 3
p1_count: 3
timestamp: 2026-08-05T04-01-24Z
slug: site-index-html
---
Method: dual-agent (A: design review, isolated · B: detector + measured browser evidence, isolated)

## Design Health Score

| # | Heuristic | Score | Key issue |
|---|---|---|---|
| 1 | Visibility of System Status | 2 | Film chrome fades at p>0.92 leaving 5,300px with no position indicator; and the status readouts themselves drop under AA over bright film (altimeter p05 2.87, chapter label 1.57) |
| 2 | Match System / Real World | 3 | Altimeter reads `144 M AGL` over a frame where the figure is kneeling on asphalt |
| 3 | User Control and Freedom | 2 | Finale CTA jumps 5,544px past every remaining artifact, no way back but manual scroll |
| 4 | Consistency and Standards | 3 | Three identical yellow CTAs do three different classes of thing; 3 footer links styled live, all `href="#"` |
| 5 | Error Prevention | 2 | `START A FITTING` opens mail to `issue@gear.systems`, a domain that does not resolve |
| 6 | Recognition Rather Than Recall | 3 | "TURN IT" hint removed permanently on any pointerdown incl. accidental |
| 7 | Flexibility and Efficiency | 2 | Not n/a — page ships nav, ?jump=, arrow-key turntable. The accelerators it ships let a cold visitor skip the entire film in one click |
| 8 | Aesthetic and Minimalist Design | 4 | Exemplary in the film; one idea per viewport, one scrim per beat |
| 9 | Error Recovery | 2 | Frame 404s leave a black canvas behind a loader already force-dismissed at 9s; turntable failure leaves "TURN IT" as a lie |
| 10 | Help and Documentation | n/a | One linear scroll surface, one gesture; genuine gaps are affordance problems scored under #1/#6 |
| **Total** | | **23/36** | **Acceptable (64%)** |

## Design Specificity Verdict

Split, and the split is the story. The film (0-850vh) is unambiguously authored: beats keyed to specific frames, altimeter and chapter labels matching what is on screen, a genuinely different 9:16 phone film with beats re-composed to the bottom. No unrelated product could wear it.

Everything below the film is the opposite. Strip the turntable and two macro plates and `#system`/`#spec`/`#issue`/`#close` is a generic dark-mode product page that would serve a watch, a bike frame or an EV unchanged. `#spec` holds 181px of content in an 828px band at 1440x900 — 77% empty black.

Deterministic scan: 3 findings, exit 2. `layout-transition` (loader bar, real but negligible), `dark-glow` (CTA hover halo, true positive by the rule), `broken-image` (FALSE POSITIVE — matched the word `<img>` inside a JS block comment at line 623).

The deeper failure neither the detector nor category convention would flag: the page is authored for someone shopping for a helmet, who does not exist. The intended visitor is a hiring decision-maker, and nothing on the page serves them.

## Priority Issues

### P0 — No path from the page to its author, and every path that exists is dead
Three footer social links are `href="#"` (verified). `START A FITTING` is `mailto:issue@gear.systems`, non-resolving. `REQUEST ISSUE` is an in-page anchor. The author's name appears ZERO times in the DOM — not in title, meta, author tag or footer. Peak-end: peak 9, end 2. The visitor has just been convinced someone very good made this and has no way to find out who.
Suggested command: /impeccable shape

### P0 — The primary CTA is an invisible keyboard focus trap
Tab #5 on desktop (#2 on phone) lands on `a.cta "Request issue"` inside the finale beat at `opacity:0`. Its rect is already in viewport so the browser does not scroll — scrollY stays 0. Measured focus-ring pixel diff: 0.00%. A keyboard user tabs onto the page's primary conversion control and it is completely invisible, at the top of the page, before the film has played.
Suggested command: /impeccable harden

### P0 — `touch-action:none` traps vertical scroll across 39% of the phone viewport
`.turn-stage` is 354x329 CSS px on an 844px viewport. Swipe up starting on the helmet moves the page 0px; identical swipe over the film moves 285px. Fix: `touch-action: pan-y` plus an axis gate on first pointermove (`|dy| > |dx|` → release the drag).
Suggested command: /impeccable adapt

### P1 — The film's own CTA fires the visitor past every remaining piece of evidence
`.beat.b-finale .cta` is `href="#issue"`, measured 6,446 → 11,990 = 5,544px, 6.2 viewports. Bypasses the turntable, both macro plates, the spec sheet. It is also the brightest object on the page at the emotional peak, so it is the most likely thing clicked. The page is built to skip its own best evidence.
Suggested command: /impeccable shape

### P1 — Fixed chrome drops under AA over the bright stretch of the film
Measured per-glyph-pixel contrast across 21 scroll positions. Nav links p05 2.30 (fails 13 of 63 samples, p≈0.35-0.55, the cloud deck); chapter label 1.57 (fails 6 of 15); `M AGL` 2.48; altimeter 2.87 against a 3.0 threshold. The beats are fine — their per-beat scrims work. The chrome has no scrim and the `on-light` luma sampler only reads the film canvas.
Suggested command: /impeccable audit

### P1 — No scroll affordance, and scrolling is the entire argument
At scrollY 0 on all three viewports there is no cue: no chevron, no label, no motion. The first viewport is compositionally complete and reads as a finished static hero. Lowest-cost fix protecting the highest-cost asset on the site.
Suggested command: /impeccable delight

### P2 — Desktop copy column in `01 / The object` breaks at ~24 characters
`.turn-row{grid-template-columns:minmax(210px,19%) 1fr}` resolves the copy column to ~258px at both 1440 and 1920, so `.lede` (which declares `max-width:56ch`) wraps at ~24 chars across nine ragged lines. Below 820px it stacks and reads correctly — the broken case is desktop only, which is where a client reviews deliberately.
Suggested command: /impeccable layout

### P2 — `swapFilm()` throws on every orientation change
Line 901 `bitmaps.clear(); decoding.clear();` — `decoding` is declared nowhere in the file (verified: 0 declarations, 1 use). Throws `ReferenceError` after `FRAME_DIR` is reassigned and `bitmaps` cleared but before `pending.forEach(abort)` and the `frameW/frameH` reset, so stale fetches survive and the memory budget is sized against the old cut's dimensions.
Suggested command: /impeccable harden

## Persona Red Flags

**Jordan (first-timer, cold arrival):** no scroll cue at scrollY 0; nav offers three jump links out of the only thing that makes the page persuasive; the brightest object at the peak teleports him past all remaining evidence; nothing anywhere tells him this is a portfolio or who made it.

**Riley (stress tester):** swipe up over the helmet = 0px; every rotation throws `ReferenceError`; all three social links land at the top; the mailto domain does not resolve; tab #5 is an invisible focus stop; tab #6 teleports 7,849px past the film; focus rings are Chrome default blue `#005FCC` on a black/yellow page; reduced-motion still scrubs 601 frames across 8.5 viewports.

**Casey (distracted mobile):** the 39% scroll trap immediately after the film; ~460px of pure black between the CTA and the footer; three 38x38 dead social targets; 73x23 wordmark target; no `env(safe-area-inset-bottom)` despite `viewport-fit=cover`, so the altimeter sits in the home-indicator zone; nav removed at ≤640px with no replacement.

## Minor Observations

- Fixed `GEAR` wordmark overlaps running body copy below the film; `#chrome` has no backdrop and the luma sampler only reads the film canvas, so header colour freezes at the last film frame.
- Document outline: `h1,h2,h2,h2,h1,h2,h3,h3,h3` — two h1s and a jump back up mid-document. `#spec` and `#close` contain no heading at all.
- `canvas#frame` (the entire narrative) and the runtime `canvas.turn-obj` both have no accessible name, no role, no fallback content. The turntable's `<img alt>` is destroyed by `replaceWith`.
- `figure#turnStage` gets `tabIndex=0` and arrow-key handling with no `role` and no accessible name.
- No `<noscript>`: with JS disabled the page is the loader, forever, over a 12,926px document.
- Debug logger ships to production — `jank max Xms` every 2s, 32 lines during a full scroll.
- 37.43 MB downloaded in one desktop scroll pass, 12.33 MB on phone. `_headers` covers `/frames*/` but has NO rule for `/product/*`, including the 4.5 MB turntable set.
- The two 1000x1000 macro stills (253 KB combined) are served identically to phones, un-resized.
- `#turnStill` declares `960x892` but the served file is `835x776`.
- No Open Graph tags; the meta description sells a fictional helmet. A link pasted in Slack or LinkedIn previews as an ad for a product that does not exist, with no image, on a page made of 601 beautiful frames.
- Beat at p=0.235 wraps to four ragged lines at 1440px, not the two its `<br>` intends; `"shell."` is a widow. It is the first beat the visitor reads.
- `.beat h1{white-space:nowrap}` with `clamp(38px,6.2vw,86px)` is a live overflow risk for any copy change.

## Questions to Consider

1. `BRIEF.md` is named in PRODUCT.md as the strongest proof of method this project has — and it is not on the page. What if the real second act, replacing `#spec` and `#issue`, were the build record styled in this exact visual language? It is the only content here a neighbouring portfolio could not copy.
2. Does the GEAR fiction pay for itself past the film? Inside it, it is load-bearing. Below it, it costs a CTA that must be fake, a footer that must be fake, and an email that must bounce.
3. The page is 14.3 viewports and the last 5 are the weakest. What breaks if `#spec` is deleted entirely and the film's own altimeter payoff carries `98,000`?
4. The phone layout of `01 / The object` is better composed than the desktop layout of the same section. What else here was composed for portrait first and bolted to landscape?
