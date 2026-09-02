# Print log

From Moonraker's job history. All in white PETG at 240/80.

| Finished | Job | Duration | Outcome |
|---|---|---|---|
| 2026-08-31 15:43 | `first_layer_test.gcode` | 10.4 min | Complete. Hand-generated (prime line, edge frame, centre square) to validate Z-offset and adhesion before committing to a long print. Clean — validated the whole calibration chain. |
| 2026-08-31 18:09 | `3DBenchy.gcode` | 105 min | Complete. Clean Benchy. First real print; sliced headless on the Pi. |
| 2026-09-01 04:23 | `LittleGrassDragon.gcode` | 504 min (8 h 24) | Complete. Print-in-place articulated flexi, ~160 × 211 mm footprint. Source: Thingiverse [thing:6411173](https://www.thingiverse.com/thing:6411173) (EndK7), "SE" integrated-eyes variant for single-colour. |
| 2026-09-01 15:04 | `Kinetic_Toy.gcode` | 8 min of 774 est. | **Cancelled at layer 1 — first-layer adhesion failure.** (Print in Place) Kinetic Hinge Toy, Thingiverse [thing:6438053](https://www.thingiverse.com/thing:6438053) (OsironGlaw), CC-NC. ~113 × 126 × 21 mm disc of several hundred interlocking hinge segments. See below. |
| 2026-09-01 15:31 | `Flexi-Rex-improved.gcode` | 9.6 min of 169 est. | **Cancelled — same failure as the Kinetic Toy.** A small section did not stick and was dragged into neighbouring pieces. Flexi Rex with stronger links (DrLex), 100 % scale, 81 × 68 × 13 mm. Source: GitHub [`DrLex0/print3D-FlexiRex`](https://github.com/DrLex0/print3D-FlexiRex), `Flexi-Rex-improved.stl` — no Cloudflare, author's settings match `ender5s1_petg.ini` exactly. |
| 2026-09-01 18:10 | `coupon_ladder.gcode` | 135.3 min (2 h 15) | **Complete, clean.** koala-bot fit coupon, 150 × 60 × 6 mm, 22.6 g. Sliced `petg` (0.2 mm, 3 perim, 15 % grid) per koala-bot's `docs/bom.md`. Slicer estimate 135.6 min vs 135.3 actual — accurate to 20 s. No corner lift despite a 150 mm flat footprint on the bare magnetic base. |
| 2026-09-02 18:41 | `first_layer_test.gcode` | 6.3 min | **Complete.** First print on the new textured PEI plate. Ran after tram check and a fresh `BED_MESH_CALIBRATE` at 80 °C. No `PROBE_CALIBRATE`; `z_offset` left at 1.776. |

## Two failures in a row — the pattern (2026-09-01)

Two models, printed hours apart, failed the same way: **the smallest, least-anchored features
let go and were dragged into the rest of the print.** Everything with real bed contact held.

| | Kinetic Hinge Toy | Flexi Rex 100 % |
|---|---|---|
| Layer-1 geometry | single-width rails + short dashes | solid filled regions |
| What held | rails, most dashes | body, head, legs |
| What failed | ~a dozen short dashes | a small section, dragged into other pieces |

The geometries are opposites, so **model geometry is not the common cause** — the earlier
single-model conclusion is superseded. What the two share is that each has a few features with
much less bed contact than the rest, and in both cases those are exactly what released. That is
the signature of a **thin adhesion margin**, where the weakest feature on the plate is the one
that finds it.

Against that: the Benchy (105 min) and the dragon (8 h 24) both completed clean on this same
plate and the same `z_offset = 1.776`. Nothing in the config changed between those successes
and these failures. What *did* change is that the plate has since been used and handled — skin
oils on PEI are the classic cause of exactly this, and IPA alone does not fully remove them.

**Next step before any further printing:** wash the plate with warm soapy water, dry it, then
wipe with IPA. Then run `first_layer_test.gcode` (10.4 min) — it was built for precisely this
check and validated the whole chain once already. Only if it still looks marginal is it worth
touching Z: babystep down 0.02–0.04 mm live and save.

**Observed on the plate (2026-09-01):** adhesion was good across the whole footprint of both
prints; only the smallest features came loose. So this is a *feature-scale* problem, not a
global adhesion problem, and not a tram or mesh low spot.

That rules out lowering Z. Squishing the whole first layer to hold a few small features would
be an over-correction, degrading every dimension on the plate to fix something local.

**ROOT CAUSE, confirmed 2026-09-01: there is no PEI surface on this printer.** The removable
textured-PEI spring-steel plate is missing, mislaid while the machine was stored; every print
to date has gone directly onto the bare rubberised magnetic base. That is not a print surface,
and it explains the pattern exactly — a bare magnet offers no keying, so large footprints hold
by area alone while small isolated features have nothing to grip. Benchy and the dragon
succeeded because they are big and solid; the hinge toy and the Rex failed at their smallest
features. See [hardware](hardware.md) and [backlog](backlog.md).

Corner lift has **not** been observed yet and remains unproven either way; no print so far has
had a large flat footprint to show it. `coupon_ladder` (150 × 60 × 6 mm flat slab) is the right
shape to settle it and is being printed partly for that reason.

Note on flexi prints in PETG: PETG bonds strongly between layers, and the usual expectation is
that print-in-place joints come out stiff or partly fused and need gently cracking free. PLA is
the conventional choice. PETG was used deliberately — it is far tougher for something the
grandkids will handle.

**That expectation did not hold, and the dragon is the evidence** (observed 2026-09-01): every
joint moved freely on removal from the bed, with no cracking-free needed, nothing broken and
nothing seized. DrLex's Flexi Rex notes set the bar as "if you need to use force to free the
hinges, you still have optimization work to do" — this machine clears that bar in PETG. Treat
the fusing risk as a function of joint *clearance*, which is a property of the model, not as an
inherent property of PETG on this printer.

## Kinetic Hinge Toy — why it failed (2026-09-01)

Cancelled 8 minutes in, on layer 1. Diagnosis from a photo of the plate, not from telemetry.

Telemetry exonerates the machine: heat-up 4 min, nozzle 239.9–240.1 °C and bed 80.0–81.4 °C
across the whole layer, first layer laid in ~7 min with no stall.

**Layer 1 geometry.** Not a uniform field of islands, as first assumed. It is a set of long
continuous diagonal rails with short perpendicular dashes (the hinge footprints) between them.
Everything is a *single extrusion width* — nothing on this layer has area.

**What actually failed.** The rails adhered well, and so did the large majority of dashes —
squish and line width look correct. About a dozen dashes lifted at one tip, curled into a hook,
and were then caught by the nozzle on a later pass and dragged loose, ending up as cruft
scattered across the plate. One *long rail* was also dragged and kinked, so this is not purely
a small-feature problem. Fine stringing is visible throughout and is the likely trigger for
some of the catches.

The mechanism is curl-then-drag on single-width extrusions with minimal footprint, not a
failure to adhere in the first place.

**Do not fix this with a brim** — the earlier note here said to, and that was wrong. Brim
material would bridge the gaps between neighbouring dashes and weld the mesh into a solid
plate, destroying the whole point of the model. What to try instead, in order:

1. **Wider first-layer extrusion** (e.g. 0.5–0.6 mm) — more bed contact per line with no added
   connection between features. The single highest-value change.
2. **Bed prep** — clean with IPA; a glue stick on this model is cheap insurance.
3. **Bed 85 °C** for the first layers, and keep the existing fan-off-for-3-layers.
4. **Reduce stringing** (retraction, or 235 °C) so there is less for the nozzle to catch.

Cancelling was correct: a dozen missing hinges means holes in the finished mesh, and loose
cruft on the plate risks further drags over a 13-hour run.

**Do not read this as a PETG flexi failure.** No joint was ever tested; the print never got
past layer 1.

## Lessons banked 2026-09-01

- **Trust the slicer's time estimate, not Moonraker's `progress`.** `virtual_sdcard.progress`
  is byte-position in the file, so it crawls through dense bottom layers and races through
  sparse infill. Extrapolating an ETA from it was wrong twice on the coupon; PrusaSlicer's
  estimate was accurate to 20 seconds.
- **Corner lift is not a problem on this machine.** The coupon is a 150 × 60 mm flat slab —
  the shape most prone to it — and lay flat throughout, on the bare magnetic base at that.
  The bed surface problem is purely small-feature release, not warping.
- **`START_PRINT` heats bed-first as of 18:11** (was parallel). The hotend reached 240 °C
  ~2 min before the bed was ready and oozed while waiting; wipe passes were not clearing it.
  Costs ~1.5 min per print. Side benefit: `G28` now runs with the bed at operating temperature,
  which `calibration.md` wanted anyway.

## Current state

Printer is powered on and `ready`, MCU on `/dev/ttyUSB1`, idle after completing
`coupon_ladder`. Klipper was restarted at 18:11 for the `START_PRINT` change; `START_PRINT`
homes on its own, so the un-homed state needs no action. Machine is still on the desk, not yet
in the garage.

**PEI plate fitted and calibrated 2026-09-02.** The textured spring-steel plate arrived and
is on the machine; the magnetic base was checked by hand at 80 °C and grips firmly all over,
so it needs no replacement. Printing is no longer deferred. See [hardware](hardware.md).

Calibration performed on fitting, at 80 °C throughout:

- **Tram checked, not adjusted.** `SCREWS_TILT_CALCULATE` spread was 0.061 mm corner to corner
  (front-left 1.82975 low, front-right 1.89038 high), calling for CCW 00:03–00:05. Against
  M4's 0.7 mm pitch those are under 0.06 mm of travel — finer than the knobs can be turned, so
  turning them would add error. No corner sat out of family with the others, which is the
  positive result: a plate not seated on the magnet shows as one corner well off.
- **Bed mesh re-probed and saved.** Span 0.254 mm (was 0.246 mm on bare magnet) with the same
  saddle shape — front and back edges high, middle low. The back row landed within 0.02 mm of
  its old values; the front row now sits ~0.1 mm lower relative to the rest. Same bed, uniform
  sheet, as expected.
- **`z_offset` deliberately left at 1.776.** No `PROBE_CALIBRATE` — it is nozzle-to-trigger
  geometry inside the toolhead, so a thicker surface raises probe and nozzle together and the
  number does not move. Verified by first-layer test instead; babystep is the tool if the two
  second-order effects (magnet compliance, textured datum) show up. See [backlog](backlog.md).

Klipper restarted at 18:37 by `SAVE_CONFIG`. Machine is still on the desk, not yet in the
garage.
