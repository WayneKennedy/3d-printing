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

**Mercury One.1 as a bought full kit (£206.55, owner's quote — seller and contents not yet
recorded here), plus Hydra, plus a new mainboard with ≥ 6 Trinamic drivers.** To be weighed
against **buying a Sovol SV08** before anything is ordered.

**Hydra has a hardware kit, but a partial one:** Fabreeko "Zero G Hydra 3 point conversion for
Ender 5 Pro & Plus", **US$94.99** for the Plus (510 mm extrusion), 3 left in stock when read
2026-09-28 ([Fabreeko](https://www.fabreeko.com/products/zero-g-hydra-3-point-conversion-for-ender-5-pro-plus)).
It contains brackets, couplers, 3 kossel balls + magnets, drag chain, extrusion, **3 × MGN9C
100 mm** rails, inserts, spacers and fasteners. **Not included:** bed plate (MIC-6 aluminium
recommended), bed heater, SSR, TR8 lead screws, **3 × 500 mm Z rails**, extra stepper(s), PEI,
printed parts. US seller: shipping and UK import VAT on top (not priced).

**Mainboard candidates (≥ 6 Trinamic, not yet compared):** BTT Manta M8P V2.0 — 8 driver
slots, £80.00 at 3DJake UK ([3DJake](https://www.3djake.uk/bigtreetech/manta-m8p-v20)), drivers
extra; BTT Octopus / Octopus Pro V1.1 — 8 slots, UK price not found. Either can stay a plain
USB MCU with printhub as host, so the Manta's compute-module socket is optional.

### Contrast: convert 5P vs buy an SV08

| | 5P → Mercury One.1 + Hydra + new board | Sovol SV08 |
|---|---|---|
| Kinematics | CoreXY, fixed gantry, 3-point bed (Hydra) | CoreXY flying gantry (Voron 2.4 derivative, GPL-3.0) |
| Build area | Ender-5 Plus frame, ~350 × 350 (exact post-conversion figure not read) | 350 × 350 × 345 (Sovol spec) |
| Price, known parts | £206.55 kit + US$94.99 Hydra kit (+ shipping/VAT) + ~£80 board + TMC drivers | **£389** sale at sovol.uk (regular £469), 2026-09-28; £486.99 at 3DJake |
| Price, not yet priced | bed plate, heater + SSR, 3 × Z rails, lead screws, 1 motor, printed parts (ABS), toolhead/hotend if the NG does not adapt | none for a working machine |
| Time | many evenings: strip, build, wire, Klipper config written by us, re-commission | unbox, calibrate |
| Firmware | mainline Klipper from day one | Sovol's Klipper fork (0.12, criticised as stale); mainline needs an ST-Link ([issue #28](https://github.com/Sovol3d/SV08/issues/28)) |
| Printers after | 5SI + 5P (CoreXY) + 3KE | 5SI + 5P (Cartesian, noisy) + 3KE + SV08 — a fourth machine and a fourth USB/host question |
| Risk | parts sourcing across UK/US; integration is ours | known machine; reviews note QC issues fixed in later batches (see [Print speed](../open-questions.md#print-speed--how-fast-this-machine-can-go-raised-2026-09-23)) |
| What you get beyond a printer | a machine you built and understand; reuses a frame you own | none |

**Reading (inference):** on price alone the conversion is unlikely to beat the SV08 once the
unpriced Hydra items, drivers and printed parts are added — it plausibly lands above £389. The
case for converting is ownership and learning, reuse of the 5P frame, and mainline Klipper;
the case for the SV08 is time and a known result. **To firm up:** the £206.55 kit's contents
(does it include rails, motors, toolhead?), a priced Hydra remainder list, and the board +
drivers total.

## Open questions (the owner's calls)

1. **Which design** — Mercury One.1 (XY only, keep the stock bed/dual Z) vs Mercury + Hydra
   (also replace the bed/Z with 3-point) vs Tridra.
2. **Which mainboard** — driver count is set by Q1: CoreXY needs 2 (A, B) + extruder; stock Z
   needs 1–2, Hydra needs 3 independent. So **5–6 drivers** with Hydra. UART/SPI Trinamic
   for quiet running. Check wk-inventory first; none recorded as of 2026-09-28.
3. **Toolhead** — Mercury One.1's BOM is built around the **EVA** toolhead (Rapido HF hotend,
   40 mm fan). Does the Micro Swiss NG adapt, or does 5P take EVA? Affects probe mounting and
   every calibration done on 2026-09-28 (probe offsets, `rotation_distance`, `z_offset`).
4. **Printed parts** — which printer and material. ZeroG kit parts are sold in ABS; ABS on
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
