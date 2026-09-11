# Print log

From Moonraker's job history. **PETG at 240/80 up to 2026-09-06; PLA+ at 220/215 with a 60 °C
bed from 2026-09-06 onward** — the SO-ARM101 parts are all PLA+. White PETG up to and including
2026-09-03; a new red PETG spool went on 2026-09-06 and needed no temperature or offset change.

The printer moved from the desk to the garage on **2026-09-06** and was recalibrated in place;
see [calibration.md](calibration.md#after-the-move-to-the-garage). Everything below that date
is on the garage machine, whose ambient swings widely — see [hardware.md](hardware.md#location).

| Finished | Job | Duration | Outcome |
|---|---|---|---|
| 2026-08-31 15:43 | `first_layer_test.gcode` | 10.4 min | Complete. Hand-generated (prime line, edge frame, centre square) to validate Z-offset and adhesion before committing to a long print. Clean — validated the whole calibration chain. |
| 2026-08-31 18:09 | `3DBenchy.gcode` | 105 min | Complete. Clean Benchy. First real print; sliced headless on the Pi. |
| 2026-09-01 04:23 | `LittleGrassDragon.gcode` | 504 min (8 h 24) | Complete. Print-in-place articulated flexi, ~160 × 211 mm footprint. Source: Thingiverse [thing:6411173](https://www.thingiverse.com/thing:6411173) (EndK7), "SE" integrated-eyes variant for single-colour. |
| 2026-09-01 15:04 | `Kinetic_Toy.gcode` | 8 min of 774 est. | **Cancelled at layer 1 — first-layer adhesion failure.** (Print in Place) Kinetic Hinge Toy, Thingiverse [thing:6438053](https://www.thingiverse.com/thing:6438053) (OsironGlaw), CC-NC. ~113 × 126 × 21 mm disc of several hundred interlocking hinge segments. See below. |
| 2026-09-01 15:31 | `Flexi-Rex-improved.gcode` | 9.6 min of 169 est. | **Cancelled — same failure as the Kinetic Toy.** A small section did not stick and was dragged into neighbouring pieces. Flexi Rex with stronger links (DrLex), 100 % scale, 81 × 68 × 13 mm. Source: GitHub [`DrLex0/print3D-FlexiRex`](https://github.com/DrLex0/print3D-FlexiRex), `Flexi-Rex-improved.stl` — no Cloudflare, author's settings match `ender5s1_petg.ini` exactly. |
| 2026-09-01 18:10 | `coupon_ladder.gcode` | 135.3 min (2 h 15) | **Complete, clean.** koala-bot fit coupon, 150 × 60 × 6 mm, 22.6 g. Sliced `petg` (0.2 mm, 3 perim, 15 % grid) per koala-bot's `docs/bom.md`. Slicer estimate 135.6 min vs 135.3 actual — accurate to 20 s. No corner lift despite a 150 mm flat footprint on the bare magnetic base. |
| 2026-09-02 18:41 | `first_layer_test.gcode` | 6.3 min | **Complete.** First print on the new textured PEI plate. Ran after tram check and a fresh `BED_MESH_CALIBRATE` at 80 °C. No `PROBE_CALIBRATE`; `z_offset` left at 1.776. |
| 2026-09-02 20:33 | `Flexi-Rex-improved.gcode` | 171.0 min (2 h 51) | **Complete, intact.** The print that failed at layer 1 on 2026-09-01, rerun unchanged on the new textured PEI plate. All segments present, nothing released or dragged. 7.39 m filament (~22.6 g). Slicer estimate 169 min vs 171.0 actual. **This is the confirmation of the plate diagnosis** — same model, same gcode, same settings, different surface. |
| 2026-09-02 22:09 | `Godzilla.gcode` | 237.8 min (3 h 58) | **Complete, all 7 parts intact.** Flexi Godzilla by AndresMF, Thingiverse [thing:3705484](https://www.thingiverse.com/thing:3705484), CC BY-NC. Multi-part: body (138.8 x 89.4 x 10), 2 legs, 2 arms, 2 pins — hand-arranged onto one plate, see below. 12.57 m / 38.4 g. Slicer estimate 241 min vs 237.8 actual. |
| 2026-09-06 10:26 | `LittleGrassDragon.gcode` | 1.0 min of 495 est. | **Aborted immediately — started by accident.** A stray touch on KlipperScreen started the previous job; cancelled 9 s later, then `M112`. Klipper logged `klippy_shutdown` and needed `FIRMWARE_RESTART`. **`filament_used = 0.00` — the bed never reached target and nothing was extruded.** Same clean-abort shape as the `Kinetic_Toy` stop on 09-03. |
| 2026-09-06 19:35 | `LittleGrassDragon.gcode` | 503.2 min (8 h 23) | **Complete, intact.** First print after the garage move, first on the **new red PETG spool**, and the validation of the whole post-move recalibration. Started 11:12 in daylight. 20 244 mm / 61.8 g against a slicer prediction of 20 230 mm; 500.1 min printing vs 495 est (+1 %). **First layer went down clean with no babystep**, which is what confirms `z_offset` 1.776 survived the relocation — see [calibration.md](calibration.md#after-the-move-to-the-garage). Watched throughout on the refitted camera; no lift, warp or released feature at any point, including the small isolated claws that failed on bare magnet on 09-01. Note this file predates the `start_gcode` fix, so the hotend sat at 240 °C oozing through the bed soak. |
| 2026-09-06 22:06 | `soarm_motor_holder_base.gcode` | 131.3 min (2 h 11) | **Complete. First PLA of any kind on this machine**, in white eSUN PLA+ at 220/215, bed 60, supports on. SO-ARM101 follower `Motor_holder_Base` — deliberately printed alone as the first job so it doubles as the STS3215 press-fit gauge on a part that is wanted anyway, rather than a throwaway test. 127.4 min printing vs 130.6 est (-2 %), 20.4 g as sliced. **Validates `ender5s1_plaplus.ini`, and separately proves the 60 °C bed runs fine on the 80 °C-probed `default` mesh** — no babystep, no `pla60` profile needed. Ran in darkness; camera night mode gave gross-failure detection only until a light was switched on. |
| 2026-09-06 23:41 | `so101_servo_gauges.gcode` | 67.0 min (1 h 07) | **Complete.** `Gauge_0` + `Gauge_tight_1` from `STL/Gauges/`, white eSUN PLA+, **no supports**. Printed to settle why an STS3215 would not seat in the `Motor_holder_Base` printed two hours earlier: support residue bonded in the pocket, elephant foot, or general over-extrusion. Gauges print support-free, so they eliminate the first. 62.6 min printing vs 63.8 est (-2 %), 11.9 g. **Result: the servo is a tight friction fit in `Gauge_0` — the intended press fit.** The machine is dimensionally correct; the tight motor holder was support residue. No `elefant_foot_compensation` change. |
| 2026-09-07 07:10 | `soarm_plate1_nosupport.gcode` | 362.9 min (6 h 02) | **Complete, all 4 parts clean.** SO-ARM101 follower plate 1 of 4: `Base_motor_holder`, `Motor_holder_Base` (clean reprint), `Motor_holder_Wrist`, `WaveShare_Mounting_Plate`. White PLA+, **no supports** — all four measure under 2 % overhang area. 358.0 min printing vs 364 est (-1.6 %), 61.8 g against a sliced 61.7 g. Started 01:07 and ran overnight with the camera blind, so watched on telemetry only. **Screw holes came out open and unobstructed with no support scarring** — the direct contrast with the supports-everywhere `Motor_holder_Base` printed hours earlier, which had support welded inside its pockets. **The `WaveShare_Mounting_Plate` from this plate delaminated at its raised boss** (see [decisions.md](decisions.md#supports)); **judged cosmetic on 2026-09-07 and kept** — it and `Base_motor_holder` both mate correctly with a servo fitted, so no reprint. |
| 2026-09-07 19:09 | `soarm_plate2_base.gcode` | 685 min (11 h 25) | **Complete. The best part off this machine so far.** SO-ARM101 follower plate 2 of 4: `Base` alone — 87 mm tall over 435 layers, the tallest thing printed here. White eSUN PLA+, **no supports** (0.5 % overhang). 685 min vs 697 est (−1.7 %). **34.4 m of filament = 82.7 cm³ = 102.6 g at PLA's 1.24 g/cm³, against a sliced 102.5 g** — a near-exact match over 11½ hours, which rules out under-extrusion far more strongly than the completion state does. **The STS3215 (Waveshare ST3215) is a solid press fit in the printed pocket.** That confirms on a production part what `so101_servo_gauges` established on a gauge: the machine is dimensionally correct at 220/215 in PLA+ and `elefant_foot_compensation = 0` is right — see [decisions.md](decisions.md#slicing). **It crossed a full garage hot/cold cycle** — started 08:38 in daytime solar gain, finished 19:09 at dusk — **with no warping or corner lift on an 87 mm part**, which is the first real evidence against the ambient-swing worry rather than an argument about it. The mid-print overhang re-check (largest contiguous overhang 73.4 mm² at Z 0.3–0.7 mm, effectively at the bed) correctly cleared it, so no abort was needed. Finished after dark and `END_PRINT` drops the bed, so **completion could not be confirmed on camera** — verified by the user at the machine. |
| 2026-09-07 20:11 | `soarm_rotation_pitch.gcode` | 11 min of 247 est. | **Aborted deliberately by `M112` — not a printer fault.** First layers went down well; stopped because inspection of the part showed roughly 80 % of it printing over support in the plate-file orientation. 577 mm of filament laid, so unlike the earlier clean aborts there was material on the plate. `CANCEL_PRINT` was not used — it queues behind `M190` — though in the event the job was past the soak and printing, so the heat-soak gotcha did not apply and emergency stop was simply the certain option. Needed `FIRMWARE_RESTART`. See [decisions.md](decisions.md#supports). |
| 2026-09-08 00:01 | `rp_rotx270.gcode` | 213 min (3 h 33) | **Complete, and the part looks great.** SO-ARM101 `Rotation_Pitch`, **rotated 90° about X from the plate-file orientation** — the reprint of the job aborted three hours earlier. White PLA+, `plaplus_soarm`. 213 min vs 217 est (−1.8 %); **12.2 m of filament = 36.39 g against a sliced 36.24 g**, so no under-extrusion. **The rotation cut support material from 5.39 g to 0.12 g (−98 %) and saved 34 min and 6.25 g overall**, and the part is lighter in the rotated pose because the flatter as-extracted orientation spends more on top and bottom solid layers. **This is the print that corrected the recorded assumption that the plate-file orientation is support-minimising** — it is, for four of the six parts, and badly wrong for this one. Ran overnight with the camera blind, watched on telemetry only. |
| 2026-09-08 17:26 | `soarm_plate3.gcode` | 795.6 min (13 h 16) | **Complete; two of three parts good, `Wrist_Roll_Pitch` unusable.** SO-ARM101 follower plate 3 of 4: `Upper_arm`, `Under_arm`, `Wrist_Roll_Pitch` flipped 180°. White PLA+, `plaplus_soarm`. 795.6 min vs 809.7 est (−1.7 %); **45.92 m of filament = 110.4 cm³ = 137.0 g against a sliced 136.9 g**, so no under-extrusion. `Upper_arm` and `Under_arm` clean. **`Wrist_Roll_Pitch` failed at its servo-fork face, the one that mounts to the idler horn** — the face is a downward overhang sitting above the lower tine, not above the bed, so `support_material_buildplate_only = 1` dropped its support and it was extruded into air; the user judged it unusable. The G-code confirms it: support material stops at Z 44.8 mm and the face spans Z 45–50. The flip itself held: **577 mm² of bed contact carried a 62 mm part for 13 h with no brim and no lift**. Started 04:06, and the first daylit hours were watched under the temporary LED lamp (see [open-questions.md](open-questions.md#machine)). Cause and fix in [decisions.md](decisions.md#supports); reprint queued as `wrp_flip_all.gcode`. |
| 2026-09-08 22:00 | `wrp_flip_all.gcode` | 239.6 min (4 h 00) | **Completed, part unusable — support welded to both fork faces.** SO-ARM101 `Wrist_Roll_Pitch`, flipped 180°, reprint of the plate 3 failure with **supports everywhere** (`plaplus_soarm_all`). White PLA+. 239.6 min vs 246.5 est (−2.8 %); **13.40 m = 32.2 cm³ = 40.0 g against a sliced 39.9 g**. The fork face was supported this time — verified in the G-code before starting: support inside the fork footprint from Z 30.2 to 46.8 beneath the face at Z 45.2–47.2, where plate 3 had none above 44.8. Support stands on the lower tine's inner face and in the horizontal bores, as expected for `buildplate_only = 0`. Started 16:45 UTC with the bed heating first; the user chose to watch by ear and Mainsail rather than a monitor. **Inspected 2026-09-09: the support in the fork gap is welded solid to the inner faces of both tines and cannot be removed.** Second time this profile's supports have bonded in PLA+ (`Motor_holder_Base`, 2026-09-06, was the first) — see [decisions.md](decisions.md#supports). Net: the fork faces are the problem in either direction — no support prints them into air, supported they weld. Next attempt is open in [open-questions.md](open-questions.md). |
| 2026-09-09 05:43 | `soarm_plate4.gcode` | 371.1 min (6 h 11) | **Complete; parts not yet inspected.** SO-ARM101 follower plate 4 of 4: `Wrist_Roll_Follower`, `Moving_Jaw`, both as extracted. White PLA+, `plaplus_soarm` plus a **5 mm brim** passed on the command line because `Moving_Jaw` has 30 mm² of flat bed contact. 371.1 min vs 379.0 est (−2.1 %); **19.99 m = 48.1 cm³ = 59.6 g against a sliced 59.6 g**. Started 23:26 and ran overnight unmonitored by choice. With this plate every one of the 11 follower parts has been printed once; only `Wrist_Roll_Pitch` is still without a usable copy. |
| 2026-09-09 16:37 | `wrp_flip_organic.gcode` | 255.3 min (4 h 15) | **Complete; inspected 2026-09-11: usable after craft-knife clean-up.** SO-ARM101 `Wrist_Roll_Pitch`, flipped, third attempt: **organic support from the bed only**, sliced by the new **PrusaSlicer 2.9.6** (first print from it) with `plaplus_soarm` + `--support-material-style organic`. White PLA+. 255.3 min vs 261.3 est (−2.3 %); **12.69 m = 30.5 cm³ = 37.9 g against a sliced 37.8 g**. Support reached the fork face from the bed with nothing standing on the part (verified in G-code before starting). Ran unmonitored by choice, 12:17–16:37. **Inspected 2026-09-11: the part "came out OK with the tree support, after a bit of cleaning up with a craft knife"** — the interface released rather than welding, which is the outcome neither snug profile achieved — **but the large flat fork face it supported was badly scuffed and needed a lot of craft-knife work before it was clean enough to take a servo** (reported 2026-09-11). Contact gap 0.25 mm, the same as the PETG job below, which released clean. **This closes the SO-ARM101 follower printing (all 11 parts usable) and validates PrusaSlicer 2.9.6 on the 2.5-era profiles** — see [decisions.md](decisions.md#supports). |
| 2026-09-09 21:37 | `the_thing_200.gcode` | 290.8 min (4 h 51) | **Complete, "came out OK".** The Thing action figure (Thingiverse 917064, Masterclip, CC BY-SA) at **200 %**, nine pieces in the designer's layout, **orange PETG** on a new spool, **`petg_fig` (0.16 mm layers) — first print on that profile and first PETG since the garage move**, 4 mm brim, no support. 290.8 min vs 294.1 est (−1.1 %); **11.33 m = 27.3 cm³ = 34.6 g at PETG's 1.27 g/cm³ against a sliced 34.6 g.** Nozzle was already at 240 through the bed soak because the spool change needed it hot; harmless, purge line cleaned it. **User's verdict: fine, but probably needs to be bigger** — scale is open again, see [open-questions.md](open-questions.md). |
| 2026-09-10 07:10 | `LittleGrassDragon.gcode` | 537.3 min (8 h 57) | **Complete.** Third run of the flexi dragon, first in **orange PETG** and first from the file **re-sliced on PrusaSlicer 2.9.6** with the canonical `petg` profile (the old 2.5.0 file heated the nozzle through the soak; this one is bed-first, verified). Placement matched the old file within 0.2 mm. **537.3 min vs 536.5 est (+0.1 %)** — the 2.9.6 estimate is accurate where 2.5.0's ran 2 % long; **20.13 m = 48.4 cm³ = 61.5 g against a sliced 61.5 g.** Ran overnight 22:06–07:10, unmonitored by choice. Outcome on the bed not yet reported. |
| 2026-09-11 (time unverified) | `the_thing_320_tree.gcode` | unverified (est. 12 h 33) | **Complete, successful — user's verdict 2026-09-11.** The Thing at **320 %** from the re-packed `The_Thing_320_plate.stl`, **orange PETG**, **first print on `petg_fig_tree`** (0.16 mm layers, organic bed-only support, contact 0.25) — sliced at 111.5 g / 562 layers to Z 90, see [open-questions.md](open-questions.md). **The organic PETG support under the arms released clean: the trees left no marks on the surfaces** (reported 2026-09-11) — the first PETG support on this machine that did not weld, and the case (interface hanging under a face from a bed-rooted tree) `Wrist_Roll_Pitch` had just proven in PLA+. **The orange PETG "strings horribly"** on this nine-piece plate; consequence in [decisions.md](decisions.md#superhero-figures). Duration and filament figures are **pending**: printhub was off the tailnet when this was logged (last seen 13 h earlier), so fill them from Moonraker's job history when it is back. |

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
features. See [hardware](hardware.md) and [decisions](decisions.md).

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

## Godzilla — three changes validated at once (2026-09-02)

This print was the first to exercise three separate fixes, and all three held:

- **Bed-first heating, finally working.** Telemetry caught it directly: bed climbing 37.9 → 80 °C
  over four minutes with the hotend target at **0**, then the hotend commanded only once the bed
  arrived. Every previous print on this machine had the nozzle sat at 240 °C oozing throughout
  that window. See [workflow](workflow.md) — the `M104` tokens in `start_gcode` are load-bearing.
- **The PEI plate on the worst-case geometry.** The two pins are 22.5 × 4.9 mm and 19.7 × 4.9 mm
  — the smallest, most isolated parts printed on this machine, and precisely the feature class
  that failed twice on 2026-09-01. Both adhered at layer 1 and survived to the end.
- **The corrected retraction settings** (`retract_before_travel = 1`, `wipe = 1`,
  `retract_layer_change = 1`), first used here. Seven separate islands means constant travel
  between them; no stringing problem resulted.

**PrusaSlicer 2.5.0's headless `--merge` arrange is broken.** It threw `Objects could not fit on
the bed` for *any* multi-object slice — including two legs and two arms totalling under
120 × 45 mm on a 220 × 220 bed. Single objects slice fine. Worked around by translating each STL
into position with a script and writing one merged binary STL
(`~/models/godzilla/godzilla_plate.stl`), then slicing that as a single object. **Reuse that
approach for any multi-part model**; do not trust `--merge`.

## Current state

Printer is powered on and `ready`, MCU on `/dev/ttyUSB1`, idle after completing
`coupon_ladder`. Klipper was restarted at 18:11 for the `START_PRINT` change; `START_PRINT`
homes on its own, so the un-homed state needs no action. Machine is still on the desk, not yet
in the garage.

**PEI plate fitted and calibrated 2026-09-02.** The textured spring-steel plate arrived and
is on the machine; the magnetic base was checked by hand at 80 °C and grips firmly all over,
so it needs no replacement. Printing is no longer deferred. See [hardware](hardware.md).

**The bed-surface diagnosis is confirmed.** `Flexi-Rex-improved.gcode` failed at layer 1 on
bare magnet on 2026-09-01 and completed intact on the PEI plate on 2026-09-02 — the same file,
unchanged, with no slicer or Z-offset changes between the two runs. The only variable was the
surface. Every other hypothesis pursued on 2026-09-01 (model geometry, brim, first-layer
extrusion width, bed contamination, Z-offset) is therefore ruled out, not merely unproven.

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
  second-order effects (magnet compliance, textured datum) show up. See [decisions](decisions.md).

Klipper restarted at 18:37 by `SAVE_CONFIG`. Machine is still on the desk, not yet in the
garage.
