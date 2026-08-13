# TERMINAL VELOCITY — build brief (survives context compaction)

Scroll-film site for **GEAR / Neural Visor XV**. The page is one continuous 25s shot
that scrubs on scroll, then hands off into content sections.

## The film
- **Vector (never violate):** the camera only ever falls straight down. One unbroken
  descent from the edge of space to the ground. No rises, no pull-backs.
- **Shape:** 5 clips × 5s = 25s. 6 keyframes. Chained.
- **Subject law:** the armored figure stays centered at roughly constant scale for the
  whole film; the WORLD transforms around him. He is never off screen.
- **Arc:** exosphere → atmosphere entry (visor ignites) → cloud break → city grid →
  landing crouch. Ends on the composition of the existing GEAR hero.
- Storyboard + prompts: `storyboard.json` (passed `vector-check.py`).

## Engine
- Higgsfield **via MCP** (no CLI on this machine). Same chain contract, different calls.
- Model: `seedance_2_0` (full — NOT mini for finals). Exposes `start_image` + `end_image`.
- **Chain law:** clip N's `start_image` = clip N−1's ffmpeg-extracted LITERAL last frame
  (the real pixels, via a fresh media_upload), NOT the keyframe. `end_image` = kf(N+1).
  Only kf1 starts clip 1. Sequential — never fan out in parallel.
- Audio OFF always. Draft tier = `seedance_2_0_mini` 480p (5 cr). Final = `seedance_2_0`
  720p (22.5 cr/clip).

## Assets / IDs
- Source character (leveled full-body, pure-black bg): media_id
  `cd89c040-2308-415f-9850-45121b190512`
- **Keyframe job ids** (use directly as `medias` values):
  - kf1 exosphere      `8a9a6aab-67b0-431c-b2d1-a53e18d58b74`
  - kf2 entry          `4dcd6948-bd37-4155-8913-9dedd39feb5e`
  - kf3 cloud          `ecdf5a51-75e9-4bc8-81c5-7402b1182642`
  - kf4 below-cloud    `0050d109-15b4-433f-9914-0974ab9714c8`
  - kf5 braced         `ed48fae3-1f45-4623-8127-fa1d9889aaab`
  - kf6 landed         `d28db0d7-dd02-446d-b11a-cd15da8d1558`
  - PNGs also on disk in `assets/kf1..kf6.png`
- **kf6 REPLACED** — the original landed on pure black, which contradicts the city he
  had just been falling toward. New kf6 = landing in a crouch on wet asphalt in that
  city street: `8d987513-537d-4276-a36f-8ca513e80f81`. Desktop clip 5 must be
  regenerated against it.
- **9:16 mobile pass** (each recomposed from its 16:9 counterpart so both films are the
  same shot; kf6v comes from the new city-street kf6):
  - v1 `9ce27dcb-0416-47e8-8ecd-ecb09601c6b5`
  - v2 `c810ed26-b6ef-44c7-9f97-863688eee238`
  - v3 `1b72a82b-792f-4023-ac8f-48be67f3aad1`
  - v4 `0a91fd60-4402-4b96-9c6d-9d29524367d6`
  - v5 `9a360edf-e0e3-4513-ad22-043dc0457231`
  - v6 — pending, generate from the new kf6

## Mobile law (skill: "Mobile is a different film, not a narrower one")
Two frame sets of IDENTICAL length so the playhead maps 1:1. Swap on
`matchMedia('(max-width: 768px)')`, and on switch CLOSE every decoded ImageBitmap from
the old set before refilling or it leaks GPU memory on every rotation.
`frames/` = desktop 16:9 · `frames-v/` = mobile 9:16.
- Existing hero project (do not disturb): `/Users/octavioortega/Desktop/borra/gear-hero`
- This build: `/Users/octavioortega/Desktop/borra/terminal-velocity`
  (`assets/` keyframes+clips, `frames/` extracted JPEGs, `site/` the page)

## World (locked)
- Ground `#000000`. Accent `#f5e100`. Scarf burnt orange. Graphite/carbon grays.
- Display **Zen Dots**, UI **Chakra Petch** (Google Fonts).
- Radius 0 everywhere. No shadows — depth from gradients and light only.

## Do-nots
- No dissolves over bad junctions — fix the join.
- Never decimate frames to lighten payload — drop width/quality instead. Extract at
  native 24fps (25s ≈ 601 frames) at 1024px `-q:v 6`.
- Never run a preview server in the foreground — `nohup … &`, poll, `pkill`.
- Don't reskin the gear-hero page; this is its own world.
- `copy-gate.js` must exit 0 before shipping. Never let the page narrate its own mechanic.

## Budget — SPENT
Approved ~150 cr. Actual: **137** (757 → 620).
- 6 keyframes (nano_banana_pro 2k, chained): 12
- 1 draft clip (mini 480p) to prove the pins: 5
- 5 master clips (seedance_2_0 720p): 112.5
Skipped the other 4 draft clips (−20 cr) once clip 1 proved both pins were honoured.

## STATUS: shipped locally
- Film: 601 frames @ 24fps = 25.04s, 1280×720 master, frames at 1440w (38 MB).
- Gates: vector-check PASS · continuity-gate PASS (median .805) · copy-gate PASS.
- Junctions (visual verdict beats the number — stochastic texture under-reads):
  1→2 .832 ok · 2→3 .841 ok · 3→4 .615 ok (city lights) · 4→5 .630 ok.
- Serve: `cd site && nohup python3 -m http.server 8899 &` → http://localhost:8899
- Verify: `node ~/.claude/skills/scroll-film-studio/scripts/verify.js shot "http://localhost:8899/index.html?jump=<y>" out.png 1440 900`
- NOTE: the in-app Browser pane renders this black (throttled hidden tab, rAF frozen).
  That is a known harness artefact — use verify.js with real Chrome, which is correct.

## Not done yet
- Deploy to Vercel (opt-in, never done without asking).
- A true 9:16 mobile film. Portrait currently centre-crops the 16:9 master to a
  tall band, which works only because the subject is centred in every frame.

## Pendiente: el corte de mitad-de-clip a 331 m (p≈0.90, frame ~538)
Clip 5 cruza altura + locación + luz de una vez, así que corta en vez de viajar.
Fix = partirlo en dos con un keyframe intermedio a nivel de azotea.
- kf5b (16:9) YA GENERADO: job `6bf6af42-a315-4a16-9107-566ccf57c217`, en assets/kf5b.png
- Falta: v5b (9:16) + 4 clips de 4s (2 por versión) ≈ 74 cr restantes

## EN CURSO: re-filmado de clips 1–3 por movimiento orgánico (135 cr aprobados)
**Causa raíz:** mis prompts decían "Figure held centered at constant scale" — el modelo
obedeció y congeló al personaje. Probado con 5 cr: quitarlo lo desacartona por completo.

**Lenguaje que SÍ funciona** (usar en los 6 clips): brazos barriendo y corrigiendo contra
el flujo de aire, dedos enguantados abriéndose, cabeza girando a mirar el suelo y luego a
un lado, torso rolando y cabeceando con la turbulencia, scarf latigueando caótico, glifos
del visor parpadeando/actualizándose. Cerrar con "Organic, physical, weighty freefall
motion." NUNCA volver a escribir "held centered" ni "constant scale".

**Cadenas (independientes entre sí, correr en paralelo):**
- 16:9 → m1' (kf1→kf2) `7da24799-0e97-4863-a710-47b4fb8fd73f` · m2' (m1'-last→kf3) · m3' (m2'-last→kf4)
- 9:16 → w1' (v1→v2) `e765eabb-6142-4332-87da-052af96f35a2` · w2' (w1'-last→v3) · w3' (w2'-last→v4)
- Clips 4 y 5 NO se re-filman. Medir la unión 3→4 en ambas versiones; si pasa (≥0.80 o
  veredicto visual), reensamblar con los clips 4–5 existentes.
- Después: re-extraer los TRES sets (frames/ frames-v/ frames-m/), mismo conteo, y
  re-desplegar a Cloudflare Pages (proyecto `terminal-velocity`).

**Higgsfield degradado hoy:** jobs de 8–12 min en vez de 45 s. No es un cuelgue.

### Progreso del re-filmado (actualizado)
- ✅ n1 (16:9 clip1) `7da24799` → assets/n1.mp4 · last frame subido `aa14e28d-9966-4b3a-9f15-00aee56fc0f7`
- ✅ x1 (9:16 clip1) `e765eabb` → assets/x1.mp4 · last frame subido `00f4509d-b1c3-4787-b356-5fc947118576`
- ⏳ n2 (16:9 clip2) `6dece553-dd55-4c2c-92aa-af7daf6590e0`
- ⏳ x2 (9:16 clip2) `887c01d2-955f-4615-b7c3-1def094b7137`
- Falta: n3 (n2-last→kf4) y x3 (x2-last→v4), luego medir unión 3→4.
- Nota de dirección: clip 1 se dejó con movimiento SUAVE a propósito (vacío, poco aire).
  La brusquedad escala al entrar a la atmósfera. El usuario se quejó de "entrada a la
  atmósfera" = clip 2, que sí lleva el lenguaje violento probado.

### iOS: cuarto corte (frames-s @360px) — desplegado
Safari en iOS estrangula rAF durante el scroll por inercia; el arnés (Chrome headless
+ CPU throttle) NO lo reproduce. Mitigación desplegada: corte de 360px (10MB, bitmap
0.88MB), budget 34MB, conc 4, y lerp 0.30 (un lerp alto se ve "atorado" cuando el
navegador no entrega cuadros). PENDIENTE: confirmación del usuario en dispositivo real.
- ✅ n2 (16:9 clip2) → assets/n2.mp4 · last subido `b6921ecd-76ab-4d4f-9748-951e5f458278`
- ✅ x2 (9:16 clip2) → assets/x2.mp4 · last subido `866cdc0a-fb6f-4518-a58e-16ee9cd076c9`
- ⏳ n3 (16:9 clip3) `e0f823e0-e9c5-4487-97e3-fb651f521214` (n2-last→kf4)
- ⏳ x3 (9:16 clip3) `6271db1a-ae79-4cce-a9ca-023f9058ffea` (x2-last→v4)
VERIFICADO: clip 2 re-filmado tiene movimiento orgánico real (cuerpo rola, brazos
independientes, cabeza busca el suelo). El cambio de prompt funcionó.

## DESPLEGADO Y VERIFICADO — 2026-08-03
URL: https://terminal-velocity.pages.dev (deploy `65c02d5a`)

**Causa raíz del "se ve igual / sigue sin funcionar":** NO era el caché. `site/` tenía
2095 archivos huérfanos del film viejo, nombrados `f_0001 2.jpg` (copia con espacio que
deja macOS al colisionar un `cp`). Un espacio en el nombre **cuelga a wrangler pages
deploy** justo después de pedir el upload-token: 0% CPU, socket TCP abierto sin tráfico,
sin error, para siempre. Tres deploys de ~50 min murieron ahí. Borrados los 2095 →
el deploy corrió en **1.67 s**.

**Cache-busting (ya en producción):** `FILM_V = '2'` + `?v=` en FRAME_PATH. Sin esto,
`immutable` clava a los visitantes al film viejo un año. Bump FILM_V en cada re-corte.
`_headers` ahora cubre los CUATRO cortes (antes faltaban frames-m y frames-s).

**Verificación en vivo (Chrome real, 3 viewports):**
- desktop 1440x900 → tier `frames`   boot 1721 ms · 0 errs · 0 http4xx
- tablet  768x1024 → tier `frames-v` boot  713 ms · 0 errs · 0 http4xx
- phone   390x844  → tier `frames-s` boot  786 ms · 0 errs · 0 http4xx
- Tira de contacto de 9 estaciones: arco completo OK (exosfera → ignición del visor →
  nube → rejilla urbana → aterrizaje en calle mojada). Movimiento orgánico confirmado.
- El film termina al ~72% del scroll; de ahí en adelante son las secciones de producto.
- HTML vivo = local byte por byte (40757 B).

**Trampas de verificación (me engañaron, documentadas en el skill):**
- `/index.html` da **308 → `/`**. Sin `curl -L` lees un body vacío y crees que no subió.
- HTTP/2 Early Hints hace que `curl` sin `--compressed` regrese 0 bytes.
- Medir CPU/red solo del PID padre miente: hay que ver el árbol de procesos.

Aprendizajes integrados en `~/.claude/skills/scroll-film-studio/references/engine.md`
(sección nueva "Shipping the film").

### Sigue pendiente
- Corte de mitad-de-clip a 331 m (~74 cr). kf5b ya generado.
- Confirmación del usuario del performance en iPhone real tras el fix de `100svh`.
- Actualizar los artboards "WEB v2" de Paper (aún muestran el movimiento viejo).

## Turntable del casco (en curso)
- Sección rediseñada: copy angosto a la izquierda (25%), casco a la derecha (75%).
  Copy = callback del hero: "RATED FOR THE WHOLE WAY DOWN" → "AWAKE THE WHOLE WAY DOWN".
- **NO HUD sintético.** Se intentó una capa de bloques de color simulando texto sobre el
  visor y se veía a imitación barata sobre un render real. El usuario la rechazó de
  inmediato. La telemetría buena es la que YA viene horneada en la placa.
- Placa placeholder: `product/hero-wide.jpg` = crop 1200x1080 de hero.jpg (más apaisado,
  el casco llena la columna; la vertical original dejaba medio cuadro vacío).
- Sombra = pool de luz rebotada con mix-blend screen DENTRO de la placa. Detrás de un
  render negro opaco es invisible; en negro puro una sombra oscura no existe.
- Bug corregido: posicionar overlays con `offsetLeft` en JS los manda fuera del objeto.
  CSS con porcentajes sobre un wrapper `position:relative` es lo correcto.
- Motor del giro YA escrito en index.html: busca `product/turn/t_0001.jpg`; si no existe
  cae a la placa estática sin error. Al generar los frames, no hay que tocar código.
- **Draft orbit lanzado** (5 cr, mini 1:1): job `ef9edb23-2af1-40cd-a86e-e8619861ff0d`
  start_image = end_image = `ab205e40-f65e-4d8f-9d00-dcf5c569c22c` para forzar cierre.
- PENDIENTE DE DECISIÓN: 720p (22.5 cr) probablemente da un casco MÁS SUAVE que la placa
  estática actual — codec + negro mate + fibra de carbono es el peor caso. 1080p cuesta 45
  y el saldo es 43.5. Si el carbono no aguanta, quedarse con el casco filoso sin giro.
- Saldo: 43.5 antes del draft. Los 135 cr que faltaban fueron 3 clips de 1080p entre
  20:58 y 21:13 de OTRA sesión del usuario, no de este proyecto.

### Turntable RESUELTO — 10 créditos en total
- Draft 1 `ef9edb23` (5 cr): objeto coherente y loop cerrado, pero la cámara vagabundeaba.
- Draft 2 `bb5d8805` (5 cr): cambió el modelo mental a **"casco sobre tornamesa, cámara
  atornillada al tripié"**. Una cámara FIJA es mucho más estable de generar que una
  orbitando, y el resultado en pantalla es idéntico. Éste es el que se usó.
- `stabilize-turn.py` normaliza cada cuadro a la MISMA ALTURA de silueta y mismo centro.
  Altura, nunca ancho: un casco de frente es legítimamente más angosto que de perfil, y
  normalizar el ancho pelearía contra el giro mismo. Resultado: altura 0.0%, centro-Y 0.0%.
- Salida final: 60 cuadros (6° c/u) a 760px, recortados 8.5% abajo para matar un piso
  reflejante que el modelo metió pese al prompt. 2.6 MB en `site/product/turn/`.
- Verificado en Chrome real: idle una vuelta cada ~22 s, arrastre 1/3 de vuelta por 300 px,
  inercia con retorno al idle, 0 errores de página.

**DOS VECES ME ENGAÑÓ MI PROPIO INSTRUMENTO, no el material:**
1. `turnstab.py` medía el CENTROIDE de masa, que se mueve legítimamente en un objeto
   asimétrico girando → reportaba 22.8% de deriva sobre material que estaba bien. Casi
   gasto créditos re-prompteando. Corregido a caja delimitadora (la altura es el invariante).
2. Medir el arrastre con `mouse.move` sin pausa: Chrome fusiona los eventos y parecía que
   el arrastre no giraba. Con 16 ms entre movimientos: 13 eventos, funciona perfecto.
3. El panel del navegador in-app estrangula rAF → el giro corría a 0.2 fps y parecía muerto.
   Verificar SIEMPRE con Chrome real (puppeteer), como ya dice el BRIEF para el film.

Hook de depuración añadido: `window.__turn()` → {idx, vel, loaded, ctx, dragging, touched}.

### v3 del turntable — la luz era el problema, no la resolución
Job `9011e814` (12.5 cr). El usuario notó que el carbono no se apreciaba en el giro.
Medición (micro-contraste / brillo del casco, región normalizada por bbox):
  placa original  25.4 / 55.3    v2  20.4 / 51.8    v3  22.5 / 45.5
El fix fue LUZ: clave dura RASANTE en ángulo bajo que resbala sobre la superficie en vez
de bañarla — es lo que revela un tejido. Micro-contraste +10% y el tejido diagonal se lee.
De paso apareció el especular del anillo del cuello, que también se pidió explícitamente.
- v3 salió **LOCKED de fábrica** (0.0/1.4/0.0) — NO se estabilizó: cada resample cuesta
  nitidez, y la nitidez era justo el objetivo. Solo crop del 7% inferior (piso reflejante).
- 60 cuadros @ 960x892, 4.3 MB, FILM_V del turntable subido a v:'2'.
- El ring seal NO se va a ver en el giro a ninguna resolución: ocupa ~40px de 850. Es
  problema de ESCALA, no de calidad. Para eso existe el macro de abajo.
- 4K nativo cotizado: **110 cr** (seedance_2_0, 1:1, 5s, std, bitrate high). 1080p = 45 cr
  y es mal negocio: solo 12% más resolución lineal que los 960 actuales.

## ERROR ABIERTO: el casco del producto NO es el casco del personaje
Confirmado visualmente. Película: anguloso, facetado, barbilla en punta, filo de luz fría
en toda la silueta, visor OPACO — casco sellado tipo traje espacial. Producto: integral de
moto, redondo, visor ovalado ancho con telemetría ámbar encendida, tejido de carbono.
Dos objetos distintos, de géneros distintos.

**Causa raíz:** nunca se encadenaron. El personaje viene de la imagen fuente
`cd89c040-2308-415f-9850-45121b190512`; `product/hero.jpg`, `visor.jpg` y `seal.jpg` se
generaron por separado, cada una interpretando "un casco" por su cuenta. Es la MISMA ley
que ya teníamos para los pines intermedios — se extrae del material real, no se genera —
que nunca se aplicó a los assets de producto.

**Por qué importa:** la sección se llama "The object" y afirma ser el casco de la caída.
Un visitante que mire con atención ve que la página se contradice a sí misma.

**Opciones (saldo: 6 créditos, ninguna alcanza hoy):**
1. Regenerar las placas de producto PARTIENDO de un frame extraído de la película donde el
   casco se lee bien, como referencia pineada. Luego re-hacer el turntable desde esa placa.
   ~12.5 cr el draft del giro + costo de las placas. La correcta.
2. Extraer las placas directamente de la película. Gratis, pero el máster es 1280x720 y el
   casco ocupa poco cuadro: no da para una placa héroe ni existe giro.
3. Dejarlo y documentarlo.

**Lección para el skill:** todo asset de producto que la página afirme que es el mismo
objeto del film DEBE derivarse de un frame extraído del film, con la misma jerarquía que
ya usamos para los pines: extraer > editar mínimo > doble referencia > generación libre.

### Casco canónico RECUPERADO — 2026-08-05
La referencia verdadera del proyecto es `design_handoff_gear_hero/reference.png` (1878x1350),
la primerísima imagen del proyecto. De ahí salió todo. El casco canónico tiene:
corona pálida muy castigada con ranuras · casco inferior negro brillante con micro-grabado
punteado · **puerto circular en la sien con anillo cromado** · placa gris angular con
remaches · mentonera angular con ranuras horizontales · estarcido "818" · marcas naranjas
en el borde de la corona · bufanda naranja.
El casco de `product/hero.jpg` NO tiene NINGUNA de esas características. Eran objetos
distintos, y el de la película es un tercer objeto intermedio.

- Recorte canónico subido: media_id `c0572057-5e1c-4a11-9a7b-0b36e302da24`
- Placa nueva (GPT Image 2, 2k/medium, 3 cr): job `341bb140-fc64-4186-87cb-ed9d9ca13487`
  → `assets/plate-v1.png` 2048x2048. Fidelidad alta, todas las características presentes.
- **Decisión del usuario: el visor va con el ámbar ENCENDIDO**, aunque el canónico lo tiene
  negro reflectante. El ámbar ya es parte del lenguaje del sitio.

**Precios verificados de GPT Image 2** (llamada exacta, no de memoria):
1k/medium 2 cr · 2k/medium 3 cr · 2k/high 7 cr.

**Plan pendiente, en este orden — no se puede invertir:**
1. Editar plate-v1 para encender el ámbar del visor (3 cr)
2. Aprobar la placa
3. Generar el turntable DESDE esa placa, mini 1:1 5s, ambos extremos pineados (12.5 cr)
4. `stabilize-turn.py` + crop del piso + 3 cortes (turn/ turn-m/ turn-s/) — gratis
5. Bump de `TURN.v` en index.html o el caché inmutable sirve el casco viejo
Faltan 15.5 cr. Saldo tras la placa: 3.

Las dos macros (`visor.jpg`, `seal.jpg`) siguen siendo del casco equivocado. El canónico no
tiene "anillo de sello de cuello" — esa macro hay que replantearla, no solo regenerarla.

### Placa final LISTA — pin del turntable
- `assets/plate-final.png` (2048²) — job `d761e5e3-049a-4ede-a511-37fd47450487`, 3 cr.
  Edición mínima sobre plate-v1: bufanda FUERA + ámbar ENCENDIDO. Las 8 características
  canónicas intactas. El ámbar salió con contenido real (`SYS LOG`, `UPLINK`, `A18`,
  `P 02`) y quedó dentro del cristal, no como pantalla brillante.
- `assets/plate-pin.png` (2048²) — **ESTE es el que se pinea**, no plate-final.
  plate-final traía el objeto al 97% del alto (margen 27px arriba, 32 abajo). Un turntable
  con eso se sale del cuadro al girar a perfil, Y rompe `stabilize-turn.py`, que normaliza
  por altura de silueta y necesita el objeto completo. Recompuesto localmente al 66%,
  centrado. Gratis, sin regenerar.

**Lo que sigue mañana, exacto:**
1. Recargar créditos (~30 para tener colchón).
2. `generate_video` mini, 1:1, 5s, start_image = end_image = plate-pin (subir primero).
   Prompt: el de tornamesa que ya funcionó — "cámara atornillada al tripié, el casco gira
   sobre su eje" — NO "cámara orbitando". 12.5 cr.
3. `turnstab.py` para verificar (caja delimitadora, NO centroide).
4. `stabilize-turn.py` solo si sale WANDERING; si sale LOCKED no estabilizar — cada
   resample cuesta nitidez.
5. Recortar el piso reflejante si aparece, 3 cortes (turn/ 60f 960 · turn-m/ 30f 640 ·
   turn-s/ 30f 420), bump de `TURN.v`, ship-gate, deploy.
6. Encontrar el frame frontal nuevo para `TURN.start` (el script de ámbar+ancho ya existe).

Saldo: 0. Gastado hoy en el casco: 6 cr (3 placa + 3 edición).

## Secciones de abajo — rediseñadas 2026-08-05 (sin créditos)
Arranque medido: `#system` 32% vacío · `#spec` **77–82%** · `#issue` **82%**.

- **`#spec` BORRADA.** Dos cifras inventadas en la composición más vacía del sitio,
  repitiendo el pago que la película ya entregó — el visitante acababa de ver el altímetro
  correr de 98,000 a cero. Sus números bajaron a `.verdict`, una línea bajo la tabla de
  `#system`: son el veredicto de esa tabla, no una sección.
- **`#issue` recompuesta**: de 828px al 82% vacío → 434px al 52%. Tres términos reales
  (fitting / lead time / lote) como `<dl>`. Fuera el CTA a `issue@gear.systems`, que no
  resolvía.
- **Los 5 eyebrows numerados, fuera.** El piso de calidad de impeccable los prohíbe sin
  excepción, y estaban rotos entre sí (`03 / Qualification` numerado junto a `Tested to`
  sin numerar, mismo peso visual).
- **Nav**: apuntaba a `#spec` (ya inexistente) y era una escotilla para saltarse la
  película, ofrecida en scroll 0. Ahora `Object / System / Issue` y solo aparece con
  `#chrome.past-film`.

Página: 12,926px → **12,451px**. Cero errores, cero links muertos, sin overflow horizontal,
detector exit 0 en los tres viewports.

### PENDIENTE con créditos — las dos macros
`product/visor.jpg` y `product/seal.jpg` son close-ups del casco EQUIVOCADO. Hay que
regenerarlas desde `assets/plate-pin.png` (el canónico) con GPT Image 2, edición mínima,
2k/medium = 3 cr c/u. Ojo: el canónico NO tiene anillo de sello de cuello — esa segunda
macro hay que replantear qué detalle muestra (candidatos: el puerto circular de la sien con
su anillo cromado, o la mentonera con ranuras). Prioridad después del turntable.

### Macro del puerto de la sien — LISTA, sin créditos
Generada por el usuario en ChatGPT con el prompt de edición mínima, partiendo de
`plate-pin.png`. Guardada en `assets/macro-port.png` (1254²).
- Reemplaza `product/seal.jpg` + `seal-s.jpg` (1000 y 560, q84 = 138 y 54 KB).
  El casco canónico NO tiene anillo de sello de cuello, así que esa placa nunca era
  regenerable — había que decidir qué detalle mostrar. El puerto es la firma más
  reconocible del diseño y es el tipo de detalle que justifica un macro.
- Copy reescrito: la leyenda describía un anillo de cuello que ya no está en la foto.
  Nuevo texto ata el puerto al argumento de "una sola unidad sellada" de #system.
- Calidad q84 elegida midiendo: la curva de fidelidad se aplana después de 84
  (q88 = 160 KB, q84 = 138 KB, diferencia 0.12). Arriba de eso son bytes que el ojo
  no recoge, y B ya había marcado las macros como los assets más pesados.
- El archivo llegó nombrado `ChatGPT Image Aug 5... .png` — CON ESPACIOS, justo lo que
  cuelga a wrangler. Renombrado. El ship-gate lo habría atrapado igual.

**PENDIENTE:** `product/visor.jpg` sigue siendo el macro del casco VIEJO. Falta que el
usuario corra el primer prompt (telemetría del visor) en ChatGPT. Gratis.

### Bug de caché en las imágenes de producto — 2026-08-05
Agregué `/product/*  immutable, max-age=31536000` al `_headers` y **dos horas después
reemplacé `seal.jpg` con el mismo nombre de archivo**. El deploy funcionó, el archivo en
el servidor era nuevo, y el usuario siguió viendo el macro viejo. Es exactamente el mismo
fallo que ya habíamos arreglado para los frames con `FILM_V`, en una carpeta que yo mismo
acababa de volver inmutable.
Por qué el casco SÍ cambió y la oreja no: `hero-canon*` son nombres de archivo nuevos.

**Arreglo:** todas las referencias bajo `product/` llevan `?v=2`. Súbelo al reemplazar
cualquier plate o macro.
**Gate nuevo en `ship-gate.sh` (3b):** para CADA carpeta con regla immutable en `_headers`
—no solo `frames*`— exige que sus referencias en el HTML lleven `?v=`. Probado en ambas
direcciones: falla con `product/seal.jpg` desnudo, pasa con `?v=2`.

### Turntable RESUELTO vía Fal.ai / Kling v3 pro — 2026-08-05
Higgsfield quedó en 0 créditos; el usuario conectó Fal.ai con la skill `media-gen`.
Llave en `~/.zshenv` (NO en `.zshrc`, que los shells no interactivos no leen). Hay que
hacer `source ~/.zshenv` antes de cada llamada en esta sesión.

**Modelo: `kling-v3-pro`** (`fal-ai/kling-video/v3/pro/image-to-video`), $0.168/s con audio.
Razón: expone `start_image_url` Y `end_image_url`, que es lo que fuerza el cierre del loop.
CORRECCIÓN a lo que dije antes: `seedance-2-pro` también los expone ($0.3024/s); el que
tiene el end-frame "unverified" es `seedance-2-fast`. Kling gana por precio, no por ser el
único.

**ERROR QUE COSTÓ DINERO:** lancé la primera generación en primer plano. El timeout de la
herramienta mató mi shell a los 2 min, el trabajo siguió vivo en Fal, y relancé creyéndolo
muerto. Dos cargos, $1.68 en vez de $0.84. **Toda generación va en background desde el
arranque.** El primer clip apareció después vía un share link del usuario y resultó ser el
BUENO — sin plataforma.

**Los dos clips:**
- `assets/turn-k1.mp4` — el primero. SIN base. Es el que se usó.
- `assets/turn-kling.mp4` — el segundo. Le salió un disco de tornamesa literal porque mi
  prompt decía "sits on a motorised turntable": describí el rig y el modelo lo renderizó.
  **Nunca nombrar el aparato; describir solo cámara y objeto.**

**Falso positivo mío:** leí el contact sheet y afirmé que el casco "cambiaba de diseño al
girar". El usuario lo cuestionó y tenía razón — era la rotación. Desde atrás solo se ve la
corona pálida, así que el blanco domina. Comparando cuadros al mismo ángulo el objeto es
idéntico. Casi le hago gastar $1.51 de más por un problema inexistente.

**Salida:** 1440x1440, 121 cuadros. Estabilizado con `stabilize-turn.py` (deriva 10.6% →
5.3%). Tres cortes: `turn/` 36f@1000 (137 MB) · `turn-m/` 30f@640 (47 MB) · `turn-s/`
30f@440 (22 MB). **36 cuadros y no 60**: el corte anterior pedía 196 MB y trabó el
navegador del usuario; 10° por paso en vez de 6° no lo ve una mano arrastrando.
`TURN.v='3'`, frente en índice 11 (`t_0012.jpg`).
Medido: carga 76ms, jank p95 17.6ms, CERO cuadros >50ms, 0 errores.

### Turntable IMPECABLE — cero blur, 2026-08-06
El usuario rechazó el giro anterior: "se ve raspado y viejo, debería verse impecable,
nuevo, con iluminación de estudio" y "no quiero nada borroso".

**Tenía razón en el blur y mi medición no lo probaba.** Yo había medido VARIACIÓN entre
ángulos (plana) y concluí que no había blur. Pero si el motion blur es uniforme en todos
los cuadros, esa prueba lo pasa por alto. La prueba correcta es contra algo SIN movimiento:
mismo casco, mismo tamaño en píxeles, placa fija 35.4 vs cuadro de video 30.7 = **13% de
pérdida**. Blur real.

**Pipeline que lo resolvió ($2.63 total):**
1. `nano-banana-pro-edit` desde `plate-final.png` → `assets/plate-new.png` ($0.15).
   Prompt con identidad y condición SEPARADAS: bloque "mantener idéntico" con las 7
   características del diseño, bloque "cambiar solo la condición" con el acabado. Pedir
   "un casco nuevo" sin esa separación rediseña el objeto.
2. Reencuadre local al 66% → `assets/pin-new.png` (gratis).
3. `kling-v3-pro` **10 segundos, no 5** ($1.68). 360° en 10s son 36°/s en vez de 72°/s:
   la mitad de velocidad angular, dos tercios menos de blur. Prompt de "fotografía de
   revista, no cine": obturador rápido, cada cuadro congelado, sin bokeh. NUNCA nombrar
   el rig — el intento anterior renderizó un disco de tornamesa porque dije "sits on a
   motorised turntable".
4. **Topaz Video** ($0.80). Pérdida vs placa: crudo +4% → Topaz **−2%**, o sea los cuadros
   quedaron MÁS nítidos que la fotografía de referencia.

**NO se estabilizó, a propósito.** `stabilize-turn.py` empeoró la deriva (6.4% → 7.1%)
porque este casco NO tiene altura invariante: la mentonera sobresale, así que de perfil la
silueta es más alta que de frente. La suposición del script (altura = invariante del giro
vertical) es falsa para esta geometría, y normalizarla mete bamboleo en vez de quitarlo.
Además cada resample gasta la nitidez que Topaz acababa de comprar.

Cortes: `turn/` 36f@1000 (137 MB) · `turn-m/` 30f@640 (47 MB) · `turn-s/` 30f@440 (22 MB).
`TURN.v='4'`, frente en índice 32 (`t_0033.jpg`).
Medido: carga 75ms, jank p95 18.6ms, cero cuadros >50ms, 0 errores.

**PENDIENTE:** las dos macros (`visor.jpg`, `seal.jpg`) siguen siendo del casco CASTIGADO.
Junto a un giro impecable se va a notar. Regenerar desde `plate-new.png`, $0.15 c/u.

### Giro completo de 360° — el turntable definitivo, 2026-08-06
El usuario: "no gira completo y el giro que hace es errático, se devuelve solo".
**Tenía razón, cuarta vez en el día.**

**El diagnóstico y la trampa:** el cuadro de "media vuelta" era un PERFIL, no la nuca — el
puerto de la sien al centro y el visor de canto. El clip cubría ~180° y regresaba.
**Pinear los dos extremos a la misma imagen INVITA a la oscilación**: ir y volver satisface
"inicio = final" de la forma más barata posible. Una vuelta real también lo satisface, pero
es más trabajo, y el modelo elige lo fácil.

Y mi prueba del ámbar me engañó: cayó a 2 a media vuelta y lo leí como "vimos la nuca".
No — era el visor de canto en perfil.

**El arreglo: un punto intermedio nombrado.** La misma ley que ya teníamos escrita por el
corte de los 331 m y que no había aplicado aquí. El prompt ahora describe explícitamente
qué debe verse a mitad de la toma: *"the camera is looking at the BACK of the helmet, the
visor faces directly away and is completely out of sight, no amber telemetry is visible at
all"*. Un destino nombrado no se puede saltar. Más prohibición explícita del retroceso:
"one direction only, never reversing, never rocking back".

**Prueba que lo verifica** (y que cachó el fallo): el ANCHO de silueta debe hacer DOS
montículos en una vuelta real (frente-perfil-nuca-perfil-frente). Una oscilación hace uno.
El clip malo: un montículo. El bueno: dos.

**Pipeline final:** `pin-new.png` → kling-v3-pro 10s ($1.68) → Topaz ($0.80).
Blur: crudo +6% vs la placa → tras Topaz **−3%**, o sea más nítido que la referencia.
Sin estabilizar (misma razón: la mentonera rompe la invarianza de altura).
Cortes: turn 36f@1000 · turn-m 30f@640 · turn-s 30f@440. `TURN.v='5'`.
Frente derivado POR PROPORCIÓN (0.917 del máster), no por detección de ámbar — a 640px la
detección eligió mal y descuadró un corte.

**Inercia de volante (gratis):** decaimiento 0.90 → 0.978, y el momento ahora acumula el
flick (`mom*0.5 + step*0.7`) con tope de ~2.5 vueltas/s en vez de tomar solo el último
delta. Un flick da ~vuelta y media y baja suave en ~5 s.

**El ship-gate salvó un deploy:** cachó 94 archivos `t_0017 2.jpg` con espacios — el mismo
defecto que colgó a wrangler 50 minutos. El gate que escribí para eso funcionó.

**Gasto del día en Fal: $6.79.** De ese, $1.68 fue mi error de lanzar en primer plano y
$2.48 el giro que oscilaba.

## Turntable v6 — el giro que "se trababa" (resuelto, $0)

Síntoma: "no gira completo y se traba". Real y medible, no percepción.

Diagnóstico: comparé cada par consecutivo de los 36 cuadros desplegados (200x200, gris).
Ocho eran casi idénticos — dos zonas muertas: cuadros 1-4 y 19-23. El paso más lento
era **1% del más rápido**. Arrastras y no pasa nada, luego brinca.

Causa raíz, y esta es la lección: **un modelo de video cumple una restricción quedándose
quieto.** Le pinné start=end (misma imagen) y le puse un waypoint "la nuca al medio".
Kling satisfizo las tres condiciones *deteniéndose* en cada una. 33 de 241 cuadros del
máster tienen movimiento ~0. El prompt decía "constant speed, never pausing" y aun así
pausó — la restricción geométrica gana sobre el adverbio.

Arreglo (gratis, sin regenerar): **muestrear por movimiento acumulado, no por tiempo.**
Se recorre el máster sumando la diferencia cuadro a cuadro, y se eligen los N de salida
en pasos iguales de esa suma. Las pausas aportan ~0 movimiento, así que colapsan a un
cuadro; el resto se redistribuye donde el objeto sí gira.

    paso entre cuadros   antes: min 0.08  max 14.17   (8/36 congelados)
                        después: min 7.01  max 10.55   (0/36 congelados)
    el paso más lento pasó de 1% a 66% del más rápido

Verificado en vivo con ángulo **desenrollado** (el índice envuelto esconde un retroceso
como si fuera un salto): un solo flick da **1268° = 3.5 vueltas**, retroceso 0.0°,
5.2s de inercia, se detiene solo. EASE 0.22 -> 0.15 para que entre suave.
TURN.v 5 -> 6. El frente se movió a t_0002 en los tres cortes (re-medido por área ámbar,
no asumido — el re-muestreo cambia TODOS los índices).

## Turntable v7 — el vaivén de 180°, la causa real (2026-08-06)

v6 no arregló nada de fondo. El defecto no eran los cuadros congelados sino la **geometría
del clip**: nunca dio la vuelta. Prueba decisiva, y hay que hacerla siempre:

    para cada cuadro, busca su gemelo más parecido en el resto de la tira
    una vuelta real -> CERO gemelos
    un vaivén      -> muchos, simétricos alrededor del punto de retorno

v6 daba 16 gemelos de 36, doblados exactamente en el 19: 17~21, 16~22, 15~23, 14~24.
Palíndromo perfecto. El casco iba del frente a la nuca y **se regresaba por el mismo lado**;
nunca se veía el otro costado. Eso es "no gira completo" y también "da tumbos": con inercia,
en el cuadro 19 la imagen invierte dirección aunque el índice siga avanzando.

**Causa: pinnear `end_image` = `start_image`.** Salir y volver es la forma más barata de
cumplir "termina donde empezaste". Ya estaba escrito en este archivo como ley y aun así lo
hice, confiando en que un waypoint intermedio forzaría la vuelta. No la forzó: solo definió
el punto de retorno.

**Arreglo:** generar SIN pin final, pedir que se pase de una vuelta, y encontrar el punto de
ciclo después comparando cada cuadro tardío contra el cuadro 0. Resultado: 0 gemelos en 241.
Cubrió 350° de 360 — quedan 10.1° y un brinco de 2x un paso normal una vez por vuelta.
Interpolar ese hueco con flujo óptico se probó y se **rechazó**: 18.4% de pérdida de nitidez,
fantasmea sobre el visor negro. Cerrarlo bien = otra corrida de $1.12 pidiendo 1.25 vueltas.

**Memoria (la queja de "se lagea"), resuelta aparte.** 48 cuadros a 1000px son 192 MB, peor
que los 137 que ya trababan. Bajar a 36 cuadros era el trade equivocado: pasos angulares
gruesos SON el tumbo. Solución de dos capas, solo en desktop:
- las 48 en 300px, permanentes (16 MB) -> arrastrable a los 0.4s
- ventana de ~12 en 1000px siguiendo la mano, sesgada hacia adelante
- girando rápido deja de pedir alta y pinta la baja; el movimiento la tapa
- `ImageBitmap.close()` es lo que libera de verdad; soltar la referencia no basta

62 MB con 48 ángulos y nitidez completa en reposo. Verificado: 1269° de un flick, retroceso
0.0°, 5.5s de inercia, p95 18.6ms, 0 cuadros >50ms, 0 errores, 0 404 en los tres tiers.

**Macros nuevos** (`visor.jpg`, `seal.jpg` -> `?v=3`) con `nano-banana-pro-edit` desde
`plate-new.png`, $0.15 c/u, para que coincidan con el casco impecable del giro.

**Gasto:** clip $1.12 + macros $0.30. Más ~$1.12 de un clip huérfano: usé `subscribe()`,
mataron el proceso, y el `request_id` se fue con él. Regla nueva en media-gen/SKILL.md.

## Turntable v9 — la respiración de escala (2026-08-06)

Tres defectos reales que reportó Victor y que mis métricas no veían: giro invertido,
el casco crece y encoge, y un corte duro.

1. **Invertido.** Signo. `step = -dx * ...` y la flecha derecha con el mismo sentido.
2. **Corte duro.** El clip de 350° dejaba un hueco de 10.1°, comparable a un paso de 7.5°,
   así que no se podía absorber. Regenerado pidiendo **vuelta y cuarto**: hueco de 3.4°,
   menor que un paso de 10°, y muestreando sobre el ciclo cerrado (arco + hueco) la costura
   sale en 0.91x de un paso. Sin corte.
3. **Escala.** Aquí me equivoqué tres veces seguidas, todas por medir mal:
   - Normalizar contra la altura de silueta **cruda** inyectó saltos de 2.7x. El reflejo del
     piso entra y sale del umbral y movió la lectura 198px entre cuadros vecinos.
   - Filtrar con mediana quitó los saltos pero dejó 21% de variación.
   - Componente conexa mayor lo empeoró (45%): con umbral 18 el visor negro parte el casco
     en varios blobs y "el mayor" agarra pedazos distintos en cada cuadro.
   - La carcasa blanca tampoco sirve: su extensión varía 44.7% por geometría real.

   **Lo que sí funciona: registrar cuadros vecinos.** Entre dos cuadros contiguos la
   geometría casi no cambia, así que cualquier cambio de escala ES la cámara. Búsqueda de
   escala por SSD sobre pares, acumulada y destendenciada porque la cámara debe cerrar donde
   abrió. Resultado: 21.1% de zoom real, con brincos vecinos de 1.51% en vez de 20%.

   **La traslación NO es separable así.** Para un objeto que gira, los rasgos deslizándose de
   lado leen como desplazamiento: la correlación de fase devolvió 317px de "deriva" que era
   la rotación misma. Así que se corrige solo escala, centrada en el centro del cuadro.

   **Y todas las escalas >= 1, siempre.** Encoger o recentrar mete el borde del cuadro
   original en pantalla como un rectángulo gris. Se subió una vez así.

Verificado: 1275° de un flick, retroceso 0.0°, 5.4s de inercia, sigue la mano, costura 0.91x,
0 saltos, 0 congelados, 58 MB, p95 18.7ms, 0 errores y 0 404 en los tres tiers.

**Gasto del turntable hoy: $3.66** — $1.12 el clip de 350°, $1.12 el de vuelta y cuarto,
$0.30 los macros, y $1.12 de un clip huérfano por usar `subscribe()`.

## Turntable v10 — arco de 180°, no vuelta completa (2026-08-06)

Decisión de Victor tras cinco intentos míos de arreglar la vuelta completa: **no girar 360,
mostrar solo frente y ambos costados.** Es la decisión correcta y debí proponerla yo.

Por qué funciona: el tercio trasero del clip trae un panel de fondo más claro que se lee como
el borde del cuadro (desbalance de esquinas hasta 53 contra 1.0 en el arco bueno) y es donde
vive el reflejo del piso. Cortando ahí, los dos defectos dejan de existir en vez de que yo
los persiga con transformaciones que sólo los empeoraban.

**Arco:** ±90° del frente = 180°, 36 cuadros, **5.1° por paso** (antes 10°). Esquinas máx 1.0,
cero saltos, cero congelados. El frente cae en t_19, que es el cuadro inicial.

**Interacción:** ya no envuelve. `clampi` en vez de `wrap`, sin atajo por el camino corto, y
la inercia se amortigua en los últimos 3 cuadros (`mom *= 0.55 + 0.15*room`) para entrar
deslizándose al tope en vez de estrellarse. ~3.7s de deslizamiento antes de detenerse.

**Bug que salió de paso:** los manejadores estaban en el `<figure>` completo pero
`touch-action:pan-y`, `cursor:grab` y la regla `.turn-plate.dragging` viven en la placa. O sea
el cursor de "agarrando" nunca aparecía y arrastrar sobre el párrafo giraba el casco. La
interacción, el foco y el aria-label se movieron a la placa; el IntersectionObserver se queda
en el figure porque ahí sí conviene el margen de carga.

**Y la lección de método:** encontrar "el frente" automáticamente falló tres veces. El ámbar
del visor marca un 3/4, no el frente. La simetría especular se equivocó por 35 cuadros. Lo
resolví mirando la tira de contactos y fijando el índice a mano. Para 240 cuadros, mirar es
más barato y más confiable que otra métrica.

Verificado en desktop, tablet y móvil: arranca en el frente, topa en 0 y 35, no envuelve,
p95 17.6ms, 0 errores, 0 404. En móvil hay que probar con TOUCH — `p.mouse` no dispara nada
bajo emulación táctil y me hizo creer dos veces que el móvil estaba roto.
