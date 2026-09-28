# 5P CoreXY conversion (Ender-5 Plus)

**Status: planning — owner leans Mercury One.1 kit + Hydra + new board; to be contrasted with an SV08. Nothing bought.** Started 2026-09-28 at the owner's request.
Decided facts go to [decisions.md](../decisions.md) when they are decided; this file is the
working brief and the prior-art survey. Machine state today:
[open-questions.md → Creality Ender-5 Plus](../open-questions.md#creality-ender-5-plus--not-committed).

## Goal and givens

- **Goal (owner, 2026-09-23 and 2026-09-28):** convert 5P from Cartesian to CoreXY — "my
  original plan for the Ender 5 Plus", to take the X motor off the moving gantry, the same
  reason the Sovol SV08 is fast
  ([Print speed](../open-questions.md#print-speed--how-fast-this-machine-can-go-raised-2026-09-23)).
- **Full mainboard replacement is assumed** (owner, 2026-09-28). The stock Creality V2.2
  (ATmega2560, soldered trim-pot drivers) goes. This also answers the 5P noise complaint
  (stepper "singing" from those drivers) and allows **independent Z drivers**, so Klipper can
  level the bed itself (`Z_TILT_ADJUST`) instead of the manual lead-screw sync done on
  2026-09-28.
- **Keep:** the frame (Ender-5 Plus 2020/2040 box, 350 × 350 × 400 build), the Micro Swiss NG
  extruder + all-metal hotend and the ANTCLABS BLTouch **unless** the chosen design dictates
  its own toolhead (see open question 3).
- **5P stays usable until the conversion starts.** Connor's belt-guide rails are printing on it
  now; the move from the Workmate to a permanent garage table comes after those
  ([open-questions](../open-questions.md#creality-ender-5-plus--not-committed)).

## Prior art (surveyed 2026-09-28; not yet evaluated in depth)

| Project | What it is | Plus support | Licence | Activity |
|---|---|---|---|---|
| **ZeroG Mercury One.1** ([docs](http://docs.zerog.one/manual/build/mercury_eva), [GitHub `ZeroGDesign/MercuryOne`](https://github.com/ZeroGDesign/MercuryOne)) | CoreXY XY motion system that replaces the Ender 5's XY, reusing the frame. Community project; commercial kits sold (e.g. [Fabreeko](https://www.fabreeko.com/products/mercury-one-kit)) | **Yes** — "Ender 5, Ender 5 Pro, and Ender 5 Plus frames". Plus BOM: **1 × 2020 extrusion 500 mm, 3 × MGN12H rails 450 mm** ([BOM](https://docs.zerog.one/manual/build/mercury_eva/bill_of_material)); 2 × NEMA17 for XY; Gates 2GT belt; F695 flanged-bearing idlers | CC BY-NC-SA 4.0 | repo pushed 2025-07-25; 52★ (predecessor `Mercury-OUTDATED` 249★) |
| **ZeroG Hydra** ([docs](http://docs.zerog.one/manual/build/hydra), [BOM](https://docs.zerog.one/manual/build/hydra/bill_of_material), [GitHub](https://github.com/ZeroGDesign/Hydra)) | Bed/Z system: 3-point bed with **3 Z motors** — pairs with Mercury | Yes (`Hydra_5Plus`): 3 × MGN12 rails 500 mm, 3 × TR8 lead screws 450/470 mm, 377 mm aluminium bed + heater | CC BY-NC-SA 4.0 (ZeroG) | pushed 2025-05-15; 20★ |
| **Tridra** ([GitHub `MacBoyPro98/Tridra`](https://github.com/MacBoyPro98/Tridra)) | Ender 5 Plus CoreXY using the **Hydra bed + Voron Trident gantry** | Yes — built for it | GPL-3.0 | 5 commits, pushed 2024-10-19; 6★ — a single builder's project |
| boothyboothy **Ender 5 Core XY with Linear Rails** MK1–MK3 ([MK3 on Printables](https://printables.com/model/169131-ender-5-core-xy-with-linear-rails-mk3)) | Printed CoreXY conversion with linear rails | Ender 5 — **Plus fit not confirmed** | Printables listing licence not read | — |
| CritterNinja **Ender 5 Plus Linear Rail Kit** ([Printables](https://www.printables.com/model/886756-ender-5-plus-linear-rail-kit)) | Linear rails on the **stock Cartesian** belt path — **not CoreXY** | Yes | not read | — |

Other items seen, not assessed: EVA 3.0 front for 5 Plus, a Mercury One.1 5 Plus enclosure
top-hat, an Ender-5 triple-Z mod, and "EnVo" (Ender 5 → Voron) — all on Printables.

**Reading of the field (inference, not yet verified by a build):** Mercury One.1 is the
mainstream route with an explicit 5 Plus BOM, published docs and a kit supply; Hydra is its
optional bed/Z companion and is what makes the new board's independent Z drivers pay off.
Tridra is the same idea with a Voron gantry, but is one person's repo. **ZeroG's docs say "we
haven't written any configuration for Klipper"** for Mercury One.1 — the Klipper config would
be ours, which is normal (`kinematics: corexy` + the new board's pins from its official
sample).

## Owner's lean (2026-09-28) — not yet decided

**Mercury One.1 as a bought full kit, plus Hydra, plus a new mainboard with ≥ 6 Trinamic
drivers.** To be weighed against **buying a Sovol SV08** before anything is ordered.

**Mercury kit (owner's link, read 2026-09-28):** Fabreeko "HoneyBadger Zero G Mercury One Ender
5 CoreXY Conversion Kit", **Ender 5 Plus – Full Kit (Rails + Fans), US$269.99** (the owner saw
**£206.55** — Fabreeko's currency display; whether UK import VAT/handling comes on top was not
read), **pre-order, ships late Sept – early Oct** ([Fabreeko](https://www.fabreeko.com/collections/zero-g/products/mercury-one-kit)).
- **Base kit:** 2 × HoneyBadger NEMA17 1.8° 48 mm motors, 1 × extrusion (500 mm for Plus),
  100 × M3 heat inserts, Mercury 1.1 fastener BOM incl. EVA screws (+20 %), 2 × Omron D2F-5L
  microswitches (endstops), **1 × 50 W 24 V heater + 1 × 104-GT2 thermistor** (hotend), motion
  kit with 6 mm Gates belts and 8.5 mm idlers.
- **Full kit adds:** 3 × MGN12H stainless rails **450 mm** (Plus), 1 × 5015 fan, 1 × 4010 fan.
- **Not included:** **printed parts** (must suit the 8.5 mm toothed idlers), **toolhead
  assembly, hotend**, control board, the printer itself.

**Hydra has a hardware kit, but a partial one — and it is sold out:** Fabreeko "Zero G Hydra 3
point conversion for Ender 5 Pro & Plus", Plus variant (510 mm extrusion) **US$99.99 sale,
Sold Out** on the owner's link (an earlier read the same day showed US$94.99 / "3 left" — which
variant that was is unclear; the owner's check says the Plus is out of stock) ([Fabreeko](https://www.fabreeko.com/products/zero-g-hydra-3-point-conversion-for-ender-5-pro-plus)).
It contains brackets, couplers, 3 kossel balls + magnets, drag chain, extrusion, **3 × MGN9C
100 mm** rails, inserts, spacers and fasteners. **Not included:** bed plate (MIC-6 aluminium
recommended), bed heater, SSR, TR8 lead screws, **3 × 500 mm Z rails**, extra stepper(s), PEI,
printed parts. US seller: shipping and UK import VAT on top (not priced).

**Mainboard candidates (≥ 6 Trinamic, not yet compared):** BTT Manta M8P V2.0 — 8 driver
slots, £80.00 at 3DJake UK ([3DJake](https://www.3djake.uk/bigtreetech/manta-m8p-v20)), drivers
extra; BTT Octopus / Octopus Pro V1.1 — 8 slots, UK price not found. Either can stay a plain
USB MCU with printhub as host, so the Manta's compute-module socket is optional.

### Reuse first (owner, 2026-09-28)

**Owner leans to building Mercury even if it costs more than an SV08:** "I hate consigning things
to landfill or obsolete dust gathering, if I can reuse instead." So each part below is judged
**reuse before buy**.

**Toolhead — the Micro Swiss NG can stay (evidence, not yet proven here):**
- Micro Swiss sells an **NG adaptation plate for Ender 5 / 5 Pro / 5 Plus on an MGN12 rail with
  an MGN12H carriage**, **US$16.00**, NG and NG REVO
  ([Micro Swiss](https://store.micro-swiss.com/products/micro-swiss-ng-direct-drive-extruder-adaptation-plate-for-creality-ender-5-5-pro-5-plus-linear-rail-edition)).
  Mercury One.1's X axis is an MGN12H carriage. The description does not mention Mercury; **one
  customer review does:** "Perfect upgrade to add my Microswiss my Mercury One.1 printer".
- Community parts exist: "MicroSwiss NG for Mercury One with Cable Chain" (GupperKay,
  [Thingiverse 7050319](https://www.thingiverse.com/thing:7050319) — contents not readable by
  fetch) and a "Microswiss ng linear rail adapter Core_XY"
  ([Thingiverse 7210368](https://www.thingiverse.com/thing:7210368)). A search summary said a
  Mercury NG REVO adapter "requires a new fan shroud to clear the belt clamp" — **source not
  pinned down; treat as a warning to check.**
- EVA 3 (Mercury's default toolhead) lists V6/Mosquito/Copperhead/Dragon/Volcano hotends and
  Titan/BMG/LGX/Orbiter drives — **no Micro Swiss** — so keeping the NG means **not using EVA**.
- Consequences: the kit's 50 W heater + 104-GT2 thermistor become spares; probe offsets change
  with the new mount (re-measure, as on 2026-09-28); `rotation_distance: 7.670` stays (same
  extruder). The BLTouch needs a mount on the new carriage — unchecked.

**Hydra — buyable from the UK/EU:**
- Hardware kit **in stock at 3DO (Denmark), kr 816** for the Plus 510 mm variant (same contents
  as Fabreeko's) ([3DO](https://3do.dk/en/frame-kits/2526-zero-g-hydra-3-point-conversion-kit-for-ender-5-pro-plus.html));
  UK shipping not shown on the page.
- Printed parts: **JB3D (UK)** sells ABS kits — **Mercury £40–70** (Standard or **Plus**, EVA /
  Stealthburner / **"None"** toolhead option, idler 8.5/9/10 mm), **Hydra bed mounts £30**
  ([Mercury](https://jb3d.uk/product/zero-g-mercury-one-ender-5-conversion/),
  [Hydra](https://jb3d.uk/product/zero-g-hydra-bed-conversion-printed-parts-kits-in-abs/)).
  That answers "who prints the ABS"; the "None" toolhead option fits keeping the NG.
- Bed: Fabreeko ATP5 plate for 5 Plus, **US$79.99, 9.53 mm**, has **both the stock and the
  Hydra bolt patterns**, pre-order 10–15 days; edge-to-edge heater extra US$79.99
  ([Fabreeko](https://www.fabreeko.com/products/zero-g-atp5-aluminum-beds-for-ender-5-pro-plus-hydra-conversion)).
- **The bed is not a Hydra requirement** (owner's challenge, 2026-09-28 — correct): Hydra's BOM
  lists a bed because it is a full build list. The **heater pad and PEI are generic** and stay if
  they work. Only the **aluminium plate** is in question, for two reasons: it needs the **three
  Hydra mounting points** (drill and tap the stock plate — Fabreeko's ATP5 is sold with both
  patterns precisely to save that), and it must stay flat **supported at three points** when hot
  (ZeroG recommend 9.53 mm MIC-6 cast plate; the stock plate is probably thinner — **not
  measured**). Plan: fit Hydra with the stock plate, mesh it hot, buy a thick plate only if the
  mesh shows sag.
- **Stock bed is 377 mm square, 4 mm aluminium, heater bonded underneath and insulated**
  (owner, 2026-09-28) — 377 mm is **exactly Hydra's BOM size**; heater + insulation reusable as
  is. The plate sits on a **20 × 10 extrusion frame** carried by the two Z lead-screw nuts and
  holding the **4 corner adjusters**. Stiffness vs ZeroG's 9.53 mm MIC-6: (4/9.53)³ ≈ **1/13**
  the bending stiffness at ~0.42× the mass. **Estimate, not measured:** self-weight sag on 3
  points of order 0.1–0.3 mm — static and mesh-compensable; thermal bowing is the unknown
  (today's 4-point-supported mesh at 80 °C is a 0.30 mm dome). Options: **A** plate direct on
  Hydra's 3 points (drill/tap 3 mounts, retire the 20 × 10 frame) — standard layout, test with a
  hot mesh; **B** keep the 20 × 10 frame + corner screws and put the *frame* on Hydra's 3 points
  — maximum reuse, but a custom adaptation that defeats Hydra's free-expansion kinematic mount;
  **C** buy the ATP5 9.53 mm plate (US$79.99). ~~Lean: A, falling back to C~~ — **owner now
  favours C, the 9.5 mm plate** (2026-09-28), accepting that the bonded heater likely does not
  transfer (peeling a bonded silicone pad often tears it or ruins the bond) → **plan a new
  heater**: Fabreeko edge-to-edge US$79.99, or a generic 370 mm pad. **Read the stock pad's label
  first (24 V DC or mains AC, watts)** — it decides whether 5P's bed wiring can drive it or
  Hydra's SSR is needed. The old plate + heater stay a working bed (spare / pass on).
- **Hydra's three bed mounts, from ZeroG's `377x370.dxf`** (downloaded 2026-09-28 from
  `docs.zerog.one/assets/dxf/hydra/`; scaled from the 377 × 370 mm outline, 1 drawing unit =
  63.5 mm): two on one **377 mm edge, 13.5 mm in from each corner and 10 mm from the edge**; one
  **centred on the opposite edge** (188.5 mm along), 10 mm in. Holes **Ø4.3 through, Ø8
  counterbore 4.5 deep**. The drawing recommends **8–10 mm** plate "for thermal stability and
  proper bolt engagement". Arms are named left / right / rear, which suggests **front-left,
  front-right and rear-centre** (Trident-style) — inference; the drawing does not label front.
  A `410x410` bed variant also exists. Z motor positions: not yet read (arm build pages).
- **Reuse candidates, remaining unverified:** the stock bed's thickness/heater (above), the **two stock Z
  motors and TR8 lead screws** (Hydra needs 3 motors and 3 × 450/470 mm screws — measure the
  stock screws), the **PSU**, the **filament sensor**. Measure before buying any of them.
- Hydra BOM (5 Plus): 510 mm 2020 extrusion, 3 × MGN9C 100 mm, **3 × MGN12C/H 500 mm**, 3 ×
  TR8 450/470 mm + nuts, 3 × 5–8 mm couplers, 3 × NEMA17, 377 mm bed + heater, SSR, drag chain,
  3 × 10 mm M4 kossel balls, 3 × 12 × 5 mm countersunk magnets, fasteners
  ([BOM](https://docs.zerog.one/manual/build/hydra/bill_of_material)).

### Contrast: convert 5P vs buy an SV08

| | 5P → Mercury One.1 + Hydra + new board | Sovol SV08 |
|---|---|---|
| Kinematics | CoreXY, fixed gantry, 3-point bed (Hydra) | CoreXY flying gantry (Voron 2.4 derivative, GPL-3.0) |
| Build area | Ender-5 Plus frame, ~350 × 350 (exact post-conversion figure not read) | 350 × 350 × 345 (Sovol spec) |
| Price, known parts | Mercury full kit US$269.99 (≈ £206.55 shown) + Hydra kit US$99.99 (**sold out**) + US shipping/VAT + ~£80 board + TMC drivers | **£389** sale at sovol.uk (regular £469), 2026-09-28; £486.99 at 3DJake |
| Price, not yet priced | **printed parts** (Mercury + EVA + Hydra), **hotend** (Mercury BOM names Rapido HF), bed plate, bed heater + SSR, 3 × Z rails, lead screws, 1 Z motor | none for a working machine |
| Time | many evenings: strip, build, wire, Klipper config written by us, re-commission | unbox, calibrate |
| Firmware | mainline Klipper from day one | Sovol's Klipper fork (0.12, criticised as stale); mainline needs an ST-Link ([issue #28](https://github.com/Sovol3d/SV08/issues/28)) |
| Printers after | 5SI + 5P (CoreXY) + 3KE | 5SI + 5P (Cartesian, noisy) + 3KE + SV08 — a fourth machine and a fourth USB/host question |
| Risk | parts sourcing across UK/US; integration is ours | known machine; reviews note QC issues fixed in later batches (see [Print speed](../open-questions.md#print-speed--how-fast-this-machine-can-go-raised-2026-09-23)) |
| What you get beyond a printer | a machine you built and understand; reuses a frame you own | none |

**Reading (inference):** on price alone the conversion is unlikely to beat the SV08 once the
unpriced Hydra items, drivers and printed parts are added — it plausibly lands above £389. The
case for converting is ownership and learning, reuse of the 5P frame, and mainline Klipper;
the case for the SV08 is time and a known result. The kit settles the XY side (rails, motors,
belts, idlers, endstops, fans, fasteners) but **not the toolhead or hotend**. **To firm up:**
whether the Micro Swiss NG hotend can sit in EVA (if not, a hotend purchase), a UK source or
restock date for Hydra, a priced Hydra remainder list, the board + drivers total, and who prints
the ABS parts.

## Open questions (the owner's calls)

1. **Which design** — Mercury One.1 (XY only, keep the stock bed/dual Z) vs Mercury + Hydra
   (also replace the bed/Z with 3-point) vs Tridra.
2. **Which mainboard** — driver count is set by Q1: CoreXY needs 2 (A, B) + extruder; stock Z
   needs 1–2, Hydra needs 3 independent. So **5–6 drivers** with Hydra. UART/SPI Trinamic
   for quiet running. Check wk-inventory first; none recorded as of 2026-09-28.
3. **Toolhead** — *leaning NG via the Micro Swiss MGN12H plate (see Reuse first).* Mercury One.1's BOM is built around the **EVA** toolhead (Rapido HF hotend,
   40 mm fan). Does the Micro Swiss NG adapt, or does 5P take EVA? Affects probe mounting and
   every calibration done on 2026-09-28 (probe offsets, `rotation_distance`, `z_offset`).
4. **Printed parts — decided in principle (owner, 2026-09-28): print them here, in ABS, from
   the owner's unopened grey ABS spool.** ABS over PETG because the gantry sits over an
   80–100 °C bed and the idler/tensioner parts carry constant belt load — PETG softens near
   80 °C and creeps; ZeroG and JB3D use ABS. **Print on 5SI** (enclosed; hotend `max_temp` 305,
   bed 110) — 5P is open-frame and is the machine being converted. Needed first: an **ABS
   profile** (none exists; ABS never printed here) proven on a temperature check and a small
   warp test; **enclosure closed** (the "closed when needed" case in
   [hardware.md](../hardware.md)); ventilation for styrene/UFP; no brim unless a part lifts
   (house rule). Check each Plus-specific part against 5SI's mesh (X3–205, Y28–218) once the
   STLs are downloaded. JB3D's ABS kits (£40–70 + £30) remain the fallback. ZeroG kit parts are sold in ABS; ABS on
   5SI (open enclosure) is untested here and the long parts may warp. PETG vs ABS for a
   gantry near a hot bed is a real question.
5. **Build or buy the kit** — printed parts + sourced hardware vs a commercial kit.
6. **Licence** — ZeroG is CC BY-NC-SA 4.0: fine for personal use; derivatives must stay
   non-commercial and share-alike. Tridra is GPL-3.0.

## Next steps

- Read the Mercury One.1 build manual end to end and list which stock 5P parts are reused vs
  replaced.
- Confirm Mercury One.1 5 Plus supports a non-EVA toolhead, or price the EVA route.
- Shortlist boards against Q2 and check stock.
