# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

The primary visitor is a **prospective client or hiring decision-maker evaluating Victor
Ortega** (senior UX/Content Designer). They arrive cold, usually from a link Victor sent,
with no prior context on GEAR and no intent to buy a helmet. They are deciding one thing:
*can this person build something I want built?*

They open it on whatever device is in hand — desktop when reviewing deliberately, phone
when the link arrives in a message. Both are first impressions of equal weight.

## Product Purpose

A **portfolio piece**. GEAR / Neural Visor XV is a fictional brand invented as a vehicle;
the real subject of the page is the standard of work.

Success is not a conversion on the page's in-world CTA. Success is the visitor finishing
the scroll and wanting to hire Victor.

## Positioning

The page **is** one continuous cinematic shot — 25 seconds of unbroken descent from the
edge of space to a wet city street — scrubbed frame by frame against scroll position, then
resolving into product content. Not a video embed, not a hero with parallax.

What a neighbouring portfolio could not truthfully copy is the production pipeline behind
it: generated footage chained shot-to-shot with both ends pinned, measured junction
continuity, four frame cuts selected by device shape and memory capacity, and a canvas
engine built to keep a 600-frame film scrubbing without leaking a phone's memory. The
artifact demonstrates the method; the method is the differentiator.

## Operating Context

- Visitor arrives cold via a direct link. There is no surrounding portfolio index, no
  navigation into this page from anywhere, and no explanation preceding it.
- The whole experience is one page, scrolled top to bottom, roughly 850vh of film followed
  by product sections.
- Deployed as a static site on Cloudflare Pages at `terminal-velocity.pages.dev`.
- The build record lives in `BRIEF.md`; a portable reconstruction spec lives in
  `BUILD-PROMPT.md`.

## Capabilities and Constraints

**Immovable — confirmed by the owner:**

- **The film.** 601 frames, 25s, five chained clips. It cost a full re-shoot to get the
  subject moving organically; regenerating it is expensive and is not a casual option.
- **The scroll-film mechanic.** The page being one continuous shot driven by scroll is the
  entire idea, not a treatment applied to it.

**Explicitly NOT immovable — the owner did not protect these:**

- The GEAR / Neural Visor XV brand fiction.
- The current copy, including the `RATED FOR THE WHOLE WAY DOWN` →
  `AWAKE THE WHOLE WAY DOWN` arc.

**Technical:**

- Static HTML/CSS/JS, single self-contained `site/index.html`, no framework, no build step.
- Film frames: four cuts (`frames/` 16:9 1440w · `frames-v/` 9:16 720w · `frames-m/` 480w ·
  `frames-s/` 360w), identical 601-frame counts so the playhead maps 1:1 across a swap.
- Helmet turntable: three cuts (`turn/` 60f 960px · `turn-m/` 30f 640px · `turn-s/` 30f
  420px), chosen by viewport and `deviceMemory`.
- Total payload ~102 MB, of which the film is the overwhelming majority. Frames are served
  `immutable` and versioned via `?v=FILM_V`; a re-cut without bumping that version leaves
  returning visitors on the old film.
- Decoded-bitmap memory is the binding runtime constraint, not file size: the desktop
  turntable holds 196 MB resident and the film budgets 120 MB. Phones get 18.7 MB.

**Undecided:**

- **There is currently no path from this page to Victor.** The only call to action is the
  in-world `REQUEST ISSUE`, which does nothing and belongs to the fiction. Given that the
  intended visitor is evaluating Victor, this is an open product gap, not a styling choice.
  How he wants to be identified and contacted has not been decided.
- Whether this page stands alone or eventually sits inside a wider portfolio.

## Brand Commitments

GEAR / Neural Visor XV is **fiction and not binding**. It is a vehicle, and the owner has
explicitly left it open to change.

The identity that actually needs protecting is Victor's own, and how he wants to be
presented on this page has not yet been established. Do not invent it.

Locked world details currently implemented (as incumbent evidence, not as commitments):
ground `#000000`, accent `#f5e100`, ember `#d2500f`; Zen Dots display and Chakra Petch UI;
radius 0 everywhere; no box-shadows — depth comes from gradients and light only.

## Evidence on Hand

Real and usable:

- The 25s film, five chained clips, in four frame cuts (`site/frames*`).
- A 360° helmet turntable in three cuts (`site/product/turn*`), generated and stabilised.
- Three product plates: helmet hero, visor macro, collar-seal macro (`site/product/`).
- `BRIEF.md` — the full build record: job ids, costs, gate results, and every failure and
  fix. This is genuine process evidence and the strongest proof of method the project has.
- `BUILD-PROMPT.md` — a portable spec that reconstructs the engine elsewhere.

Absent — must never be fabricated:

- No real customers, testimonials, press, case studies, pricing, or benchmarks. GEAR has
  never sold anything. Every number on the spec sheet is invented product fiction.
- No client work, employer, or credential is stated anywhere on the page.

## Product Principles

1. **The film is the argument.** Anything that competes with it for attention in the first
   viewport is working against the only thing that makes this page persuasive.
2. **The visitor is judging the maker, not the helmet.** Every decision should be legible
   as craft. Fiction that reads as an unfinished placeholder undercuts the point.
3. **Phone is a first impression, not a fallback.** The link arrives in a message as often
   as it arrives on a desktop.
4. **Never fabricate proof.** The brand is openly fictional; invented customers or
   credentials would make the whole page dishonest rather than stylised.
5. **Runtime memory is a design constraint.** Ambition that a phone cannot hold is not
   ambition, it is a crash.

## Accessibility & Inclusion

No product-specific standard has been established with the owner. The build currently
respects `prefers-reduced-motion` and keeps beat copy above 4.5:1 against unpredictable
footage via per-beat scrims.
