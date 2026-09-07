# Decisions

Settled conclusions and the evidence that produced them. **Do not re-litigate these**; if new
evidence contradicts one, correct it here in place rather than arguing it in chat.

**Corrections are kept, not deleted.** Several entries record a conclusion that was reached,
acted on, and found wrong. Keeping the wrong answer alongside why it was wrong is the point —
it stops the next agent re-deriving it. Anything undecided lives in
[open-questions.md](open-questions.md) instead.

## Machine and environment

- **The machine stays as-is unless something fails** (2026-09-02). Then repair-or-replace is
  judged on the failure. Assessments closed under this policy:
  - **CoreXY conversion: no.** The case for CoreXY is removing the inertia of a bed that moves
    in XY. This frame does not have one — the gantry moves in XY and the bed only in Z, so most
    of the benefit is already present. Large work for a small delta, and it would discard a
    validated first layer, a tuned config, a saved mesh and these notes.
  - **Dual extrusion: not feasible, and would not deliver what is wanted.** Four drivers
    (X, Y, Z, E) on a compact stock board. Beyond hardware, soluble or breakaway supports need
    both materials **on the same layers**, so a manual swap cannot achieve it at any price.
    Single-nozzle multi-material purges at every tool change; on a support-heavy print the
    purge tower routinely outweighs the part, so "cheap support material" is not cheap — the
    cost moves from the support to the waste.
  - **Carbon-filled filament: the nozzle is the barrier, not the hotend.** CF destroys a brass
    nozzle in hours; a hardened steel nozzle (~GBP 10) is the whole fix for CF-PETG or CF-PLA.
    `max_temp: 305` in the official sample implies an all-metal hotend, since a PTFE liner
    degrades near 250 °C — **evidence, not proof; confirm visually.** A hotend change is only
    needed for high-temp composites (CF-nylon, CF-PC).
    **Caveat:** CF makes parts stiffer and more dimensionally stable but usually makes layer
    adhesion and impact resistance *worse* — short fibres interrupt the interlayer bond. Right
    for a bracket that must not flex; wrong for feet and anything taking impacts. Not a
    straight upgrade.

- **Garage move and recalibration completed** 2026-09-06. Tram already within tolerance and
  left alone, mesh re-probed and saved (0.246 → 0.281 mm), PID verified rather than re-tuned,
  `z_offset` untouched at 1.776. Values in
  [calibration.md](calibration.md#after-the-move-to-the-garage).
  - **Wi-Fi in the garage is strong — the pre-move worry was unfounded.** −47 dBm at
    433 Mbit/s, MCU link clean (`bytes_retransmit=0`, `bytes_invalid=0`, `srtt=0.003`).
    **Ethernet is not needed**; `eth0` remains `NO-CARRIER`.
  - **The garage behaves as a greenhouse** — clear corrugated PVC roof, hot by day and cold by
    night. A standing condition, not a one-off; see [hardware.md](hardware.md#location) for
    what follows from it.
  - **Enclosure front and top are left OPEN by default**, closed only for genuinely cold
    sessions. This machine prints mostly PETG and PLA, neither of which wants a hot chamber.

- **Ambient must be recorded alongside any future mesh or PID result.** Otherwise "the
  calibration drifted" and "the ambient changed" are indistinguishable after the fact.
  Thermal headroom is ample — bed holds 80 °C on a 34 % duty cycle — so re-tune only if that
  duty approaches saturation.

## Build surface

- **The PEI plate was the root cause of the 2026-09-01 layer-1 failures**, and this is
  confirmed rather than merely likely. `Flexi-Rex-improved.gcode` failed on bare magnet and
  completed intact on PEI — same file, no slicer or Z-offset changes between the two runs. The
  only variable was the surface. Every other hypothesis pursued that day (model geometry, brim,
  first-layer extrusion width, bed contamination, Z-offset) is therefore **ruled out, not
  merely unproven**.
- **Textured, not smooth, is deliberate.** "Gold PEI" describes both; smooth PEI bonds to PETG
  hard enough to tear its own coating off.
- **`PROBE_CALIBRATE` was correctly skipped when the plate was fitted, and the reasoning is
  reusable.** `z_offset` is nozzle-to-trigger geometry inside the toolhead: the pin protrudes a
  fixed distance and triggers after fixed travel, so a thicker surface raises probe and nozzle
  together and the number does not move. **A surface change does not move `z_offset`; a
  toolhead change does.** Two second-order reasons to check the first layer anyway and babystep
  only if it looks wrong: **compliance** (1.776 was set against a rubberised magnet that gives
  slightly under probe force; spring steel does not) and **texture** (probe tip and the
  nozzle's effective datum sit differently against the peaks).
- **`first_layer_extrusion_width = 200%` was already correct** and is not a fix for the
  adhesion failures — 200 % × 0.24 = 0.48 mm, already wide. That it was never the problem
  strengthens the plate diagnosis. A brim is also the wrong tool for open-mesh models; it welds
  neighbouring features together.

## Slicing

- **Bed-first heating, since 2026-09-01.** Parallel heating got the hotend to 240 °C about two
  minutes early and it oozed while waiting for the bed; the wipe passes were not clearing it.
  Costs ~1.5 min per print. Side benefit: `G28` now runs with the bed at operating temperature.
- ~~**Every gcode file predates the 2026-09-01 18:11 ooze fix.**~~ **Wrong diagnosis,
  corrected 2026-09-02.** The real cause: **PrusaSlicer re-injects its own `M104`/`M109` around
  a custom start block unless those tokens appear literally in it.** Removing `M104` from
  `start_gcode` therefore made things *worse* — PrusaSlicer put `M104 S240` ahead of
  everything, so the bed-first fix never took effect for any file, freshly sliced ones
  included. Fixed by restoring `M140`/`M190`/`M104` in the correct order. **Verify by
  inspecting emitted G-code, never by reading the profile.**
- **Retraction stays at 0.8 mm.** The amount was never the problem; four settings were absent
  from the `.ini` so PrusaSlicer's defaults applied silently, and two were wrong for this
  machine. Corrected 2026-09-02: `retract_before_travel` 2 → 1 mm, `retract_layer_change` 0 → 1,
  `wipe` 0 → 1. Longer retracts on PETG pull molten filament into the heatbreak, trading
  stringing for jamming. Raise `retract_length` only if stringing survives those fixes.
- **`elefant_foot_compensation = 0` stays.** Investigated 2026-09-06/07 when an STS3215 servo
  would not seat in a fresh `Motor_holder_Base`, raising the worry that zero compensation
  shrinks a bed-facing pocket from the inside — a bias no fit coupon would catch, since an
  injection-moulded servo shares none of this printer's biases. **The SO-101 gauges settled it:
  the servo is a tight friction fit in `Gauge_0`, which is the intended press fit.** The
  machine is dimensionally correct at 220/215 in PLA+; the tight holder was **support residue
  bonded inside the pocket**, not geometry.
  - **The method is the reusable part.** Two hypotheses predicted the same symptom. The gauges
    print support-free, so a single 1 h 07 print discriminated between them: a good gauge fit
    meant residue, a bad one meant compensation. **Prefer a cheap print that discriminates
    between causes over a long one that merely retries.**
- **`filament_density` added** 2026-09-01 (1.27 for PETG); the slicer now reports grams.
- **PLA+ profile validated** 2026-09-06 on `Motor_holder_Base`, the first PLA of any kind on
  this machine. 220/215 at 60 °C laid down clean with no babystep.
  - **No Benchy was needed.** A real part that is wanted anyway is a better first print than a
    throwaway: a bad result costs nothing extra and a good one is a part in hand.
  - **A `pla60` bed mesh is not needed.** The print ran a 60 °C bed on the 80 °C-probed
    `default` mesh with a clean first layer. The effect is genuinely second-order — **do not
    build `pla60` speculatively.** The parameterisation is written down in
    [workflow.md](workflow.md) if a PLA first layer ever actually misbehaves.
- **`prusa-slicer --merge` is not trusted.** Its headless arrange threw "Objects could not fit
  on the bed" for two small parts on a 220 × 220 bed, and spilled a 7-part plate from X −42 to
  250. Work around it by translating parts into position and writing one merged STL, or keep
  plates to a modest fill and verify the footprint every time.

## Supports

- ~~**Supports are nearly free.**~~ **Wrong — corrected 2026-09-06.** That was measured on
  `Base` alone, the least representative part in the set: it is so large that any support is
  small in relative terms. Measured across the rest, supports everywhere cost **29–75 %**
  (`Wrist_Roll_Pitch` 50.8 g vs 29.1 g, +75 %; `Rotation_Pitch` +38 %;
  `Moving_Jaw` +38 %; `Motor_holder_Base` +29 %). **Never generalise a
  slicing cost from one part.**
- **`support_material_style = snug`, not the default `grid`.** Measured on `Rotation_Pitch`:
  grid 51.3 g, snug 47.0 g, **snug + build-plate-only 42.6 g**, none 37.3 g. PrusaSlicer's own
  help says snug saves material and reduces object scarring.
- **`support_material_buildplate_only = 1` is the answer to "no supports in horizontal screw
  holes"** — previously recorded as impossible headlessly, which was wrong. Support inside a
  bore rests on the part rather than the bed, so the switch drops it.
- **`support_material_contact_distance = 0.25`.** PrusaSlicer's default 0.2 is not an
  improvement; 0.25 is. Widening it further is the right lever when supports are unavoidable
  on a part whose surface matters — but prefer support-free models and better orientation
  first.
- **Tree/organic supports are not available.** PrusaSlicer on printhub is 2.5.0; organic
  supports arrived in 2.6. Upgrading the slicer is the only route to them.
- ~~**Percentage of surface area identifies parts that need support.**~~ **Wrong — corrected
  2026-09-07** by the delaminated WaveShare plate, sliced support-free on the strength of
  "1.7 % overhang". **A percentage hides a small contiguous overhang on a large part.** The
  plate prints *on edge* (51 × 7.6 footprint, 42 mm tall); its section is **4.0 mm** thick
  except between Z 16.8 and 25.2, where the boss protrudes **3.6 mm** horizontally off a
  vertical wall. All **68.6 mm²** of its overhang sits in one patch at Z 12–13, cantilevered
  in mid-air with nothing beneath it.
  - **Contiguous area is not the discriminator either — bridgeability is.**
    `Base_motor_holder` has a *larger* mid-air patch (124.9 mm² at Z 19.7) and printed
    perfectly, because it spans between two walls and bridges. **No cheap geometric metric
    separates these two cases.** Treat a low percentage as "probably fine", not as proof, and
    look at any part whose overhang is concentrated in one patch well above the bed.
  - **`Base` was checked against this same trap and cleared** while it was printing: its
    largest contiguous overhang is **73.4 mm² at Z 0.3–0.7 mm**, effectively at the bed
    rather than cantilevered, so no abort was needed. That is the check to run.
  - **The fix is orientation, not supports.** Measured on that plate: on edge 92.0 mm² of
    overhang, flat boss-down 1764.6 mm², **flat boss-up 0.0 mm²**. Flat is also the stronger
    part for something bolted down carrying a PCB. **The designers were not wrong** — on edge
    costs 388 mm² of bed against 2142 mm² flat, which matters when parts share one plate.
    Printing selectively buys the space to make the better choice.
- **Height drives print time, not volume.** `Base` (122.7 cm³) and `Upper_arm` (117.3 cm³) are
  nearly the same volume, but Base is 87 mm tall against 24.5 mm and takes **twice as long**.
  **Batch by time, never by footprint area.**

## Camera and monitoring

- **A USB UVC webcam, not a Pi Camera Module.** crowsnest is already set to `mode: ustreamer`,
  `device: /dev/video0`, so UVC needs no config. The Pi 5's CSI connectors are 22-pin while
  Camera Module 3 ships a 15-pin cable, and the ribbon is short and stiff where USB can be
  placed to actually see the plate.
- **The fitted camera is a Sonix/Microdia `0c45:6536`, not the C920S it was assumed to be** —
  verified on the device. Hardware MJPG to 1080p30, and measured CPU cost of streaming at
  720p during a live print was **nil**.
  - **Its focus controls are fake — the lens is fixed focus.** A measured sweep across the full
    `focus_absolute` range produced no focus curve; frames at 1 and 1023 are identical. **There
    is nothing to lock.** Consequence: **mounting distance is a design constraint, not a free
    choice.** Design the bracket to hold roughly the current distance.
- **Frame mount, aimed at the nozzle plane.** On this frame Z is the bed carriage, so **the
  nozzle never moves vertically**: the active layer sits at a constant height and distance from
  a frame-mounted camera. Focus once and it is correct at any print height. The cost — the bed
  descends out of frame on tall prints — is the right thing to trade away.
- **Occlusion is driven by toolhead XY, not print height.** The shroud hid much of the model at
  80 % (Z 13.6 mm) and the view was completely clear at 90 % (Z 16.8 mm), taller still. The
  variable is simply where the head is parked when the frame is grabbed. **A single snapshot showing an
  obscured part is not evidence of a problem, and one clear snapshot is not proof the part is
  fine.** Grab two or three seconds apart.
- **Print camera brackets in PETG, never PLA.** PLA's glass transition is ~60 °C; with an 80 °C
  bed and a garage that bakes, a PLA bracket creeps slowly enough that it is not noticed until
  the camera is aimed at the floor.
- **Timelapse should use `hyperlapse` mode** when it is wired up. The default mode parks the
  toolhead for every frame, adding time per layer and risking a witness mark — **a setting that
  alters the part to serve the observation is the wrong default for a diagnostic tool.**
  Parking mode stays a per-print opt-in for jobs where the footage is the deliverable.

## Materials

- **Print printer parts in PETG, never PLA.** See the bracket note above.
- **PLA+ is not PLA.** Same base resin plus impact modifiers: tougher with better layer
  adhesion, but glass transition is unchanged at ~55–60 °C, so **it buys no extra heat
  resistance** — the most common misconception about it, and the one that matters in a
  greenhouse garage. It also runs hotter (eSUN: 210–230 °C nozzle, 45–60 °C bed).
- **Open the enclosure when printing PLA or PLA+.** Enclosures suit ABS/ASA; PLA and PLA+ are
  the materials harmed by them.
- **Coupon measurements are specific to the spool they were printed on.** Pigment and brand
  change PETG's flow and shrinkage by a few hundredths of a millimetre — inside the 0.2 mm
  steps of an M3 clearance ladder, but the same order as the margin on a **press-fit**
  dimension. Re-run a coupon on the new spool before committing a press-fit dimension;
  clearance holes do not need this.

## Project decisions

These belong to projects rather than to the machine and **move out with their projects**; they
are here because the printer repo was the only context store when they were taken.

### SO-ARM101 follower (in progress)

- **Follower only, one to start.** Leader not planned. Upstream `TheRobotStudio/SO-ARM100`;
  SO-101 lives inside it.
- **PLA+, because the arm lives indoors.** Chosen over PETG on stiffness (~3 GPa vs ~2 GPa —
  deflection costs repeatability), clean support release (PETG supports weld to the part), and
  dimensional fidelity for the press-fit STS3215 pockets. **An outdoor arm would be PETG.**
  Do not store a PLA+ arm in the garage over a sunny summer.
- **Do not use `Ender_Follower_SO101.stl`**, despite the README listing it for 220 × 220 beds.
  It measures 216.3 × 215.3 mm, so `START_PRINT`'s purge line runs through the parts with
  nowhere else to put it, and the plate overruns the measured mesh by a **25.7 mm front strip
  and 13.2 mm at the right**. Slice into batches inside
  the meshed area instead — which also halves the loss if a print fails hours in.
- **The `STL/SO101/Individual/` STLs are not in print orientation — extract parts from the plate file.**
  `Wrist_Roll_Follower` is 105.4 mm tall in `Individual/` but 65.2 mm on the Ender plate;
  `Under_arm` flips from 64.4 to 24.0. Only `Base` matches. Split `Ender_Follower_SO101.stl`
  into connected components (`tools/extract-soarm-parts.py`); triangle counts identify each
  part and sum to 96584. **`Moving_Jaw` is two disconnected shells (10878 + 382) that must stay
  in one file**, or the arranger separates the gripper's pieces.
- **Only 6 of the 11 parts need supports** — Moving_Jaw 14.0 %, Rotation_Pitch 11.2 %,
  Wrist_Roll_Pitch 8.3 %, Wrist_Roll_Follower 5.5 %, Under_arm 4.2 %, Upper_arm 3.8 %. The
  other five slice with plain `plaplus`. **Support settings are per-file, so one plate cannot
  mix the two groups** — that constraint, not footprint, decides the plates.
- **Print the gauges first** (`STL/Gauges/`): `Gauge_0` and `Gauge_tight_1` against an STS3215.
  The project's own Step 3, and it mattered more because the profile was untested.
- **Revised total with selective supports: 409 g / 41.9 h**, against 464 g / 47.1 h for
  supports everywhere.

### Superhero figures

- **Print in white so he can paint them himself.** Chosen over character colours: it makes the
  figure something he did rather than something he was given, and one roll covers every
  character asked for next.
- **PLA over PETG for anything to be painted.** PETG is stringier, rounds off fine detail, has
  glossier layer lines under paint and resists sanding. If PETG is used instead, tell the
  painter it needs a primer key and a light scuff first.
- **Chibi or Funko style, 100–120 mm tall.** Chunky limbs survive a young child where a scale
  figure's ankles do not, and larger details are the difference between painting it and failing
  to. **Print two of each** — cheap at this size, and it turns a botched attempt into a second
  go rather than a ruined present.
- **Use a finer layer height (~0.12–0.16 mm) in a separate figurine profile.** At 0.2 mm, layer
  lines read through paint as banding on curved surfaces. Do not change the standing profile.
- **No articulated/flexi model exists for either character** — print-in-place collections cover
  Marvel's A-list only. These will be static figures.

### koala-bot

- **`petg` is the profile, not `petg_koala`.** koala-bot's `docs/bom.md` briefly specified
  4 perimeters / 30 % gyroid and the two `petg_koala*` profiles were built for it; that section
  was rewritten hours later to document the generic `petg` profile instead. Both koala profiles
  are kept but are **not** the spec.
  - **Note the direction of causation:** koala-bot's BOM now documents whatever profile
    happened to be on the Pi as the project standard. It reads as a specification but is an
    observation, and its own text flags 4–5 perimeters for load-bearing parts as untested.
- **`slice_remote.py` is safe but must not run during a print.** It copies STLs to `/tmp` on
  the Pi, slices each for volume and time, deletes the G-code and caches the figures locally —
  it never touches Moonraker and cannot start a print. But it runs PrusaSlicer over ~14 STLs on
  the machine hosting Klippy. Nothing in the script says so.

## Model sourcing

- **No model source can be fetched automatically** (verified 2026-09-02). Thingiverse returns
  the Next.js app shell as a `.zip`; Printables, MakerWorld and MyMiniFactory all 403; Cults3D
  pages fetch but downloads need a login. **The user must download in a browser.**
  - **This is a regression, not a standing limitation** — the browser-User-Agent workaround
    worked on 2026-09-01. Retry it before assuming it is dead, and **always check what you
    got**: the challenge page is HTML wearing a `.zip` name.
  - **GitHub-hosted models need none of this and are worth preferring.**
