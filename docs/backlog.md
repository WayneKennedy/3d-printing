# Backlog

## Open

- **Garage move + recalibration.** The printer lives on the desk today and is destined for the
  garage. On relocation, re-run tram → Z-offset → bed mesh at operating temperature; see
  [calibration.md](calibration.md#after-the-move-to-the-garage). Decide whether Ethernet can
  reach the garage — wired is bulletproof, Wi-Fi is the known weak link.
- **Confirm the Wi-Fi fix holds.** Power-saving is disabled three ways and persistent logging
  is on, but the original 35-minute dropout was never caught in the act, so power-save is the
  strong suspect rather than a proven cause. If it recurs, the journal will now say why.
- **Keep the flashing microSD with the printer.** MCU firmware updates still go via SD; see
  [klipper-setup.md](klipper-setup.md#consequence).
- **Fit a camera.** `crowsnest` is **not broken** — it is configured and waiting. It fails with
  `No usable Devices Found` because `crowsnest.conf` points at `/dev/video0`, which does not
  exist; systemd then gives up after 10 restarts. Confirmed 2026-09-02: nothing on USB
  (only the CH340 and the touchscreen) and `rpicam-hello --list-cameras` reports none. The
  `/dev/video19-28` nodes are the Pi 5's own ISP and codec blocks, not capture devices.
  Wanted so the assistant can pull snapshots of a running print, and for the unattended garage
  printer generally.
  - **Prefer a USB UVC webcam over a Pi Camera Module.** crowsnest is already set to
    `mode: ustreamer`, `device: /dev/video0`, so a UVC camera needs no config at all. The Pi 5's
    CSI connectors are the narrow **22-pin** FPC while Camera Module 3 ships with a 15-pin
    cable, so CSI additionally needs an adapter cable; and the ribbon is short and stiff where
    USB can be placed to actually see the plate.
  - **Two criteria that matter:** (1) **hardware MJPG** — a YUYV-only camera forces the Pi to
    compress in software, adding CPU load during prints, which is the load we avoid for
    Klipper's sake; Logitech C270/C920/C922 all do MJPG in hardware. (2) **close focus** —
    fixed-focus webcams are typically sharp from ~40 cm and will not resolve a first layer from
    15 cm. Resolution matters less than either.
  - **Raise `resolution` above the configured 640x480** once fitted; that is too coarse to spot
    a small feature lifting, which is the failure mode of interest.
  - **Scope of the benefit:** the assistant reads still JPEGs from the snapshot endpoint, on
    demand or on a timer. That is a diagnostic tool, not a safety net — a failure at 03:00 is
    caught at the next snapshot, not as it happens.
  - **Camera chosen: Logitech C920S**, already owned (in the garage). UVC, hardware MJPG,
    autofocus. Its fold-out foot has a **1/4"-20 threaded insert** — mount to that rather than
    clamping the body.
  - **Frame mount, aimed at the nozzle plane.** Decided 2026-09-02. On this frame Z is the bed
    carriage (single `[stepper_z]`, no gantry Z), so **the nozzle never moves vertically**: the
    active layer sits at a constant height and a constant distance from a frame-mounted camera.
    Focus once and it is correct for every print at any height. The cost is that the bed
    descends out of frame on tall prints, which is the right thing to trade away — nothing
    printed here is tall, and the failure mode of interest happens in the first few layers.
  - **Still needed to design the bracket:** the frame extrusion face width where it will mount
    (20 vs 40 mm — the bracket differs completely and this must be measured, not assumed),
    whether M5 T-nuts/hammer nuts are on hand or the bracket should clip over the extrusion,
    and the viewpoint. Print it in **PETG, not PLA** — see the material note below.
  - **Print printer parts in PETG, never PLA.** PLA's glass transition is ~60 °C. With an 80 °C
    bed and a garage that bakes in summer, a PLA bracket creeps slowly enough that it is not
    noticed until the camera is aimed at the floor. Even PETG is marginal close to the heater
    block.
- **`moonraker-timelapse` is installed but not wired up** (installed 2025-12-30, never
  finished). Present and correct: `component/timelapse.py` symlinked into
  `~/moonraker/moonraker/components/`, `klipper_macro/timelapse.cfg` symlinked to
  `~/printer_data/config/timelapse.cfg` and already `[include]`d by `printer.cfg`, and
  `/usr/bin/ffmpeg` for rendering. So `TIMELAPSE_TAKE_FRAME` already exists as a macro.
  Missing, all of it blocked on having a camera first:
  1. `[timelapse]` section in `moonraker.conf` (none present).
  2. `[webcam]` section in `moonraker.conf` (none present) — needed for Mainsail to display the
     feed; the snapshot endpoint works without it.
  3. `[update_manager timelapse]` so it is kept current alongside the other components.
  4. `TIMELAPSE_TAKE_FRAME` appended to `layer_gcode` in `ender5s1_petg.ini`, which is currently
     just `G92 E0`. Without this no frames are captured.
  **Use `hyperlapse` mode** (decided 2026-09-02). The default mode parks the toolhead for every
  frame, which adds time per layer and can leave a witness mark on the part — a setting that
  alters the part to serve the observation is the wrong default for a diagnostic tool.
  Hyperlapse shoots on a timer without parking: no marks, no time cost, slightly less tidy
  footage. Parking mode is a deliberate per-print opt-in for the rare job where the footage
  itself is the deliverable.
  **Do not edit `moonraker.conf` during a print** — restarting Moonraker mid-job is survivable
  (Klipper reads `virtual_sdcard` files from disk itself) but there is no reason to risk it.
- **More filament profiles.** PLA and ABS are still missing and are drop-in files. (Material
  profiles only — the koala-bot profiles added 2026-09-01 are *part* profiles for the same
  PETG; see [workflow](workflow.md#project-specific-profiles).) **PLA is now wanted for a
  specific job** — see the superhero figures below. Any new PLA profile is untested; put a
  Benchy through it before committing a figure to it.
- **Superhero figures for the grandson (raised 2026-09-02).** He asked for "the orange rock
  hero" (The Thing, Fantastic Four) and The Flash. Decisions taken:
  - **Print in white so he can paint them himself** — his dad the painter paints Warhammer miniatures
    and has acrylics and primer. Chosen over printing in character colours: it makes the figure
    something he did rather than something he was given, and one roll of white covers every
    character he asks for next. Orange and red PETG are being ordered anyway for other uses.
  - **No articulated/flexi model exists for either character.** The print-in-place collections
    cover Marvel's A-list only (Spider-Man, Hulk, Iron Man, Wolverine). These will be static
    figures, unlike the dragon and Flexi Rex. Prefer **chibi or Funko style**: chunky limbs
    survive a young child where a scale figure's ankles do not, and the simple shapes mean few
    overhangs. Candidates found (all fan models, personal use): MakerWorld
    [Chibi Flash](https://makerworld.com/en/models/1841533-chibi-flash-speedy-tiny-hero),
    [The Flash Chibi](https://makerworld.com/en/models/2117358-the-flash-chibi),
    [The Thing](https://makerworld.com/en/models/2508127-thing-the-fantastic-four-la-cosa);
    Cults3D [Funko-style The Thing](https://cults3d.com/en/3d-model/game/funko-style-the-thing-fantastic-four).
    **MakerWorld and Printables both block automated fetching** (403 even with a browser UA,
    unlike Thingiverse) and MakerWorld needs a login — the user must download these.
  - **Material: PLA preferred over PETG for anything to be painted.** PETG is stringier, rounds
    off fine detail, has glossier and more visible layer lines under paint, and resists
    sanding. PLA prints crisper, sands easily, and takes primer straight off the bed. If PETG
    is used instead, tell the painter: it needs a good primer key and a light scuff first,
    where PLA does not.
  - **Use a finer layer height, ~0.12-0.16 mm, in a separate figurine profile.** At the
    standing 0.2 mm, layer lines read through paint as banding on curved surfaces such as
    faces. Do not change the standing profile.
  - **Scale to 100-120 mm tall.** the painter is used to 28-32 mm miniatures; a young child's brush
    control is not. Larger details are the difference between painting it and failing to.
  - **Print two of each** — cheap at this size, and it turns a botched first attempt into a
    second go rather than a ruined present.
  - **Supports are a real problem here.** `support_material = 0` in the profile and every print
    so far has been print-in-place or self-supporting. PETG supports weld to the part and take
    surface with them; support scars also show under paint. Prefer models the author designed
    support-free, and if supports are unavoidable build a separate profile with a wider
    `support_material_contact_distance` rather than enabling them on the standing one.
- **No `CANCEL_PRINT` macro in `printer.cfg`.** Moonraker's cancel zeroes the heaters but
  leaves the nozzle parked on the part at temperature — hit on 2026-09-01, needed a manual
  retract/lift/park. `END_PRINT` already has the right body; add
  `[gcode_macro CANCEL_PRINT]` that calls it. Note `M84` there clears the homed flag, so a
  cancel always needs a re-home. Fires exactly when a print is already going wrong.
- **~~First-layer extrusion width~~ — already handled, no action.** `first_layer_extrusion_width
  = 200%` in the profile, which PrusaSlicer computes over layer height: 200 % × 0.24 = **0.48 mm**,
  already wide. This was previously logged as a fix for the adhesion failures; it is not one,
  and that strengthens the case for the plate surface being the cause. (A brim is also the wrong
  tool for open-mesh models — it welds neighbouring features together.)
- **`elefant_foot_compensation = 0`** in `ender5s1_petg.ini` (PrusaSlicer normally defaults to
  0.2 mm). Harmless while every part is sliced with this one profile — bias is consistent, and
  fit coupons measure the real result. It matters only if the profile ever diverges between a
  coupon and the part it validates.
- ~~**`filament_density` missing.**~~ **Done 2026-09-01** — `filament_density = 1.27` added to
  `ender5s1_petg.ini` and both koala profiles; slicer now reports grams.
- ~~**PEI sheet missing.**~~ **Done 2026-09-02** — double-sided textured 235 × 235 mm
  spring-steel plate fitted. Root cause of the 2026-09-01 layer-1 failures; see
  [hardware](hardware.md) and [print-log](print-log.md). Calibration done on fitting: tram
  checked (0.061 mm spread, no adjustment warranted), bed mesh re-probed at 80 °C and saved,
  `z_offset` left at 1.776 with no `PROBE_CALIBRATE`. Magnetic base checked by hand at
  temperature — firm all over, no replacement needed.
  - **`PROBE_CALIBRATE` was correctly skipped, and this reasoning is reusable.** `z_offset` is
    nozzle-to-trigger geometry of the toolhead: the pin protrudes a fixed distance and triggers
    after a fixed travel, so a thicker surface raises probe and nozzle together and the offset
    is unchanged. Two second-order reasons to *check* the first layer anyway and babystep only
    if it looks wrong: **compliance** (1.776 was set against a rubberised magnet that gives
    slightly under probe force; spring steel does not) and **texture** (on textured PEI the
    probe tip and the nozzle's effective datum sit differently against the peaks).
  - **`docs/calibration.md`'s post-garage-move procedure still says to re-run `PROBE_CALIBRATE`**
    on the same flawed basis. Open question, never answered: reword it, or keep as
    belt-and-braces?
- **Deferred prints, now unblocked.** Flexi Rex (sliced at 100 % and 200 %, both on the Pi),
  the remaining koala-bot coupons, and the original ask that is still outstanding — two or
  three fun prints for the grandkids. The Kinetic Hinge Toy is sliced but is a 12 h 53 job.
- **Coupon ladders printed 2026-09-01 but not yet measured.** Three ladders on
  `coupon_ladder`: M3 clearance 3.2/3.4/3.6, insert bores 3.8/4.0/4.2, motor bores
  37.3/37.5/37.7. Smallest that fits wins; test from the top face down, since
  `elefant_foot_compensation = 0` leaves the bottom edge slightly proud. Feeds
  `koala-bot`'s `params.py`. Needs screws and the motor body in hand.
  - **Coupon measurements are specific to the spool they were printed on.** Pigment and brand
    change PETG's flow and shrinkage slightly — typically a few hundredths of a millimetre.
    That is comfortably inside the 0.2 mm steps of the M3 clearance ladder, but it is the same
    order as the margin on a **press-fit** dimension such as the heat-set insert bores
    (3.8/4.0/4.2). Orange and red PETG were ordered 2026-09-02 for robotics parts. Before
    committing a press-fit dimension to `params.py` for parts that will be printed in a
    different spool, re-run a coupon on that spool. Clearance holes do not need this.
- **Every gcode file on the Pi predates the 2026-09-01 18:11 ooze fix.** The `M104` was removed
  from `start_gcode` in the `.ini` profiles at 18:11, but `Kinetic_Toy`, `Flexi-Rex-improved`,
  `Flexi-Rex-200`, `coupon_ladder` and `3DBenchy` were all sliced before that and still carry a
  literal `M104 S<temp>` ahead of the `START_PRINT` call. That line commands the hotend up
  regardless of what the macro does, so the bed-first ordering is defeated for those files.
  Harmless when the bed is already warm from a previous job; on a cold start it restores the
  full ~2 min of oozing. Re-slice before relying on any of them from cold, or strip the `M104`
  line in place. `first_layer_test.gcode` was patched by hand on 2026-09-02 and is correct.
- **No `[idle_timeout]` section in `printer.cfg`** — so Klipper's default 600 s applies, and it
  runs `TURN_OFF_HEATERS` + `M84`. Hit on 2026-09-02: a bed heated to 80 °C for a pre-mesh soak
  was silently switched off at the 10-minute mark, because heaters at temperature do not count
  as activity — only motion and commands do. Any unattended soak, filament-change wait or
  between-jobs hold longer than 10 minutes will do the same. `SET_IDLE_TIMEOUT TIMEOUT=3600`
  fixes it for a session but does **not** survive a restart (`SAVE_CONFIG` included). Decide
  whether to add a persistent `[idle_timeout]` with a longer timeout, or to build the soak into
  a macro that keeps the machine busy. Note a long timeout means heaters stay live longer after
  an abandoned job — that is the trade-off, not a free win.
- **TPU profile wanted.** A 3/4 spool of red TPU is on hand, previously dialled in on an
  Ender-3 for crash-resistant drone parts. Intended here for robot feet and possibly tyres.
  - **The Ender-3 settings are gone and would not have transferred anyway** — that machine was
    **Bowden**. Its retraction values compensate for metres of tube compliance this direct-drive
    machine does not have, and would be badly wrong. Temperatures and speeds would have carried
    over; those are the easier half to re-derive. (This loss is what prompted putting these
    notes under version control.)
  - **Protect the PEI plate.** TPU bonds to PEI aggressively and is one of the few materials
    that can lift coating off a sheet on removal. Textured is more forgiving than smooth, but
    use a glue stick as a release layer rather than find out — the plate was fitted 2026-09-02.
  - **Do not inherit the PETG retraction settings.** `retract_before_travel = 1`, `wipe = 1` and
    40 mm/s retract speed are right for PETG and wrong for a material that buckles under
    compression. TPU wants near-zero retraction at a much lower speed and accepts stringing as
    the price.
  - Direct drive is a real advantage here: the shorter and more constrained the filament path,
    the less TPU can buckle instead of extruding.
- **Lightweight (foaming) PLA profile wanted**, for RC planes. Treat as a separate problem, not
  a PLA variant. Nozzle temperature drives the foaming expansion, so **temperature sets density**
  rather than just flow quality; flow is deliberately run down to roughly 40-50 % to let the
  material expand into the gap, and prints are typically single-perimeter with no infill.
  Tuning means a calibration tower stepping temperature and measuring the resulting density.
  Not something to guess at.
- **PETG temperature tower.** 240 °C is a generic starting point, not this filament's
  measured sweet spot.

## Deferred / parked

- **KlipperScreen display blanking** — cosmetic, tap to wake. Can be disabled if it annoys.
- **OrcaSlicer** — configured on paper but not the routine path; the Pi pipeline replaced it.

## Project ideas raised (not committed)

Printer-adjacent ideas from the commissioning session. The active robotics work lives in
`~/Code/koala-bot`.

- **SpotMicro** (Thingiverse [thing:3445283](https://www.thingiverse.com/thing:3445283)) —
  quadruped, dozens of printed parts, 12 servos, Arduino Mega. PETG suits its structural parts.
- **6-DOF printable arm.** Accuracy depends on drive choice: hobby servos wander by
  millimetres; stepper + gear reduction gets to ~0.2–1 mm. AR4 (Annin Robotics) is the pick
  for repeatability; Thor (AngelLM) is the print-everything option; BCN3D MOVEO is easier but
  only 5-DOF.
- **InMoov revival** — a partially built InMoov torso from ~8 years ago is on the shelf.
  Explicitly parked as inspiration: upstream has had no activity since 2024, and the
  3D-printed auger-thread neck actuators are mechanically compromised by friction.
