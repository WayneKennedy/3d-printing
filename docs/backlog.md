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
  - ~~**Camera: Logitech C920S**~~ **The camera actually fitted 2026-09-02 is a Sonix/Microdia
    `0c45:6536` "USB Live camera", not the C920S** — Logitech's vendor ID is `046d` and no
    Logitech device enumerated. Verified on the device rather than assumed. It is a better fit
    than the C920S would have been:
    - Hardware **MJPG up to 1920x1080 @ 30 fps** (also H.264 on `/dev/video2`). Measured CPU
      cost of streaming at 1280x720 during a live print: **nil** — load average 0.13, ustreamer
      not in the top six processes.
    - **Its focus controls are fake — the lens is FIXED FOCUS.** It advertises
      `focus_automatic_continuous` and `focus_absolute` (1-1023), but a measured sweep across
      the full range on 2026-09-02 produced no focus curve: sharpness on a static patch of bed
      texture stayed flat at 13.7-14.0 (arbitrary units, stddev of Laplacian), and frames at
      `focus=1` and `focus=1023` are visually identical. The dips at 380/560/850 were the
      toolhead crossing the sample patch, not defocus. **There is nothing to lock.** The
      control was left at its default (`focus_automatic_continuous=1`), which is equally inert.
    - **Consequence: mounting distance is a design constraint, not a free choice.** With a
      fixed lens, sharpness is whatever that lens gives at the chosen distance. The current
      ad-hoc position lands in a usable range — bed speckle resolves clearly, which is the
      detail needed to spot a feature releasing. **Design the bracket to hold roughly the
      current distance**, and test a couple of distances before committing to a geometry.
    - The unit is branded "LOGITUBO 920" — a C920 clone. **If the real C920S surfaces it is
      worth swapping**: genuine autofocus and better optics. Swapping is near-free, since
      crowsnest points at `/dev/video0` rather than at a model.
    - `power_line_frequency` already 50 Hz — no flicker banding, nothing to change.
    - **It does have a 1/4" tripod thread** (confirmed 2026-09-02; it came off a desk arm), so
      the bracket can bolt to that rather than clamping the body.
  - **`crowsnest` is running as of 2026-09-02** — `mode: ustreamer`, `/dev/video0`, raised from
    640x480 to **1280x720**, port 8080. Backup at `crowsnest.conf.bak-0902`. Snapshot endpoint
    `http://localhost:8080/?action=snapshot` returns ~200 KB JPEGs. First snapshot confirmed a
    healthy print and resolved individual Flexi Rex segments and the PEI grain, which is the
    detail level needed to spot a feature releasing. 1080p is available if more is wanted.
  - **Framing note from the first snapshot:** the hotend shroud partly blocks the nozzle tip.
    The part is clearly visible but the moment of extrusion is not. Best view is from the
    front-left, slightly below or level with the nozzle plane, looking slightly up.
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

- **Upgrade policy, set 2026-09-02: the machine stays as-is unless something fails.** Then
  repair or replace is judged on the failure. Assessments made and closed:
  - **CoreXY conversion: no.** The case for CoreXY is removing the inertia of a bed that moves
    in XY. This frame does not have one — the gantry moves in XY and the bed only in Z, so most
    of the benefit is already present. A large amount of work for a small delta, and it would
    discard a validated first layer, a tuned config, a saved mesh and all of these notes.
  - **Carbon-filled filament: the nozzle is the barrier, not the hotend.** CF is abrasive and
    destroys a brass nozzle in hours; a hardened steel nozzle (~GBP 10) is the whole fix for
    CF-PETG or CF-PLA. `max_temp: 305` comes from Klipper's official Ender-5 S1 sample and a
    PTFE-lined hotend cannot be sanctioned to that (the liner degrades near 250 C), so the
    hotend is very likely all-metal — **evidence, not proof; confirm visually**: PTFE tube
    running to the nozzle means lined, bare metal heatbreak means all-metal. A hotend change is
    only needed for high-temp composites (CF-nylon, CF-PC).
    **Caveat worth heeding:** CF makes parts stiffer and more dimensionally stable but usually
    makes layer adhesion and impact resistance *worse* — the fibres are short and interrupt the
    interlayer bond. Right for a bracket that must not flex; wrong for feet and anything taking
    impacts, where plain PETG or TPU is the better material. It is not a straight upgrade.
  - **Dual extrusion: not feasible, and would not deliver what is wanted anyway.** Four drivers
    are configured (X, Y, Z, E) on a compact stock board. Beyond the hardware, soluble or
    breakaway supports need both materials **on the same layers**, so a manual filament swap
    cannot achieve it at any price. Single-nozzle multi-material systems purge at every tool
    change; on a support-heavy print the purge tower routinely outweighs the part, so "cheap
    support material" is not cheap — the cost moves from the support to the waste. The
    realistic answers stay: prefer support-free models, orient to avoid overhangs, and widen
    `support_material_contact_distance` when supports are unavoidable.

- **Second printer: Creality Ender-5 Plus**, in the garage, unused ~2 years. Identified from
  the purchase invoice 2026-09-02. **350 x 350 x 400 mm.** Not committed to commissioning; the
  case for it is that RC plane parts are long and 220 x 220 is the binding constraint.
  - **Klipper ships an official sample**, `printer-creality-ender5plus-2019.cfg` — the same
    thing that made this machine's commissioning safe. Use it; do not guess pins or thermistors.
  - **BLTouch is stock.** Same probe, mesh, tram and `z_offset` reasoning as the S1.
  - **`max_temp: 260` vs the S1's 305 — the signature of a PTFE-lined hotend, not all-metal.**
    This collides with the RC-plane plan: **lightweight PLA foams at 230-260 C**, exactly where
    a PTFE liner degrades and off-gasses. An all-metal hotend is needed before LW-PLA, and is
    cheap. Confirm the liner visually before buying either.
  - **NOT stock: a Micro Swiss NG Direct Drive Extruder is fitted** (noted 2026-09-02). This
    voids several conclusions drawn from the sample config, and means **the official sample is
    no longer safe to use wholesale** — it describes the stock Bowden machine:
    - **`rotation_distance: 33.683` is wrong.** Calibrate it by measurement (extrude 100 mm,
      measure what actually came through). Do not take a figure for the NG's gear ratio from
      the internet.
    - **The BLTouch offsets are wrong.** The NG relocates the probe on its own mount, and a
      toolhead conversion physically moves the nozzle relative to the probe — which is exactly
      what `z_offset` measures. This is the inverse of the bed-surface case: a surface change
      does not move `z_offset`, a toolhead change does. **`PROBE_CALIBRATE` genuinely is
      required here**, along with re-measuring `x_offset` and `y_offset`.
    - **Confirm the thermistor and heater cartridge before powering the hotend.** If the kit
      supplied its own hotend, `sensor_type` may not be the `EPCOS 100K B57560G104F` the sample
      declares. A mismatched sensor does not fail loudly — it reads a plausible wrong
      temperature and the heater compensates in the wrong direction.
    - **It is direct drive now**, so TPU is viable on it and retraction transfers roughly from
      the S1 (~0.8 mm) rather than needing Bowden values. The earlier "TPU stays on the S1"
      reasoning is void — though there is no need to move it.
    - **Open: did the kit include an all-metal hotend, or is the stock lined one still in
      place?** If all-metal, LW-PLA becomes viable, `max_temp` can rise above 260 and the
      RC-plane blocker disappears. If stock, the 260 ceiling stands.
    - The NG uses **hardened steel drive gears**. With an all-metal hotend and a hardened
      nozzle, this machine — not the S1 — may be the better candidate for carbon-filled
      filament.
  - **Flashing will differ.** The sample shows an **FTDI** USB bridge, not the S1's CH340, so
    [klipper-setup.md](klipper-setup.md) does **not** apply to it.
  - **One Pi can host both.** A second Klipper + Moonraker instance against a second MCU is
    established practice — a second set of systemd units and data directories. No second SBC
    needed.
  - **Physical inspection before any config work**, per the lesson from 2026-09-01: build
    surface present and intact, belts not slack, Z lead screw free and not gummed, wheels not
    flat-spotted. The last machine out of that garage was missing its build surface and it cost
    two failed prints and hours of confident wrong diagnosis.
  - Proposed split if commissioned: **S1** = PETG, TPU, detailed figures; **Plus** = large flat
    parts, plain PLA, LW-PLA for planes, and potentially carbon-filled work. The split is now
    driven by bed size and hotend capability rather than by extruder type, since both machines
    are direct drive.

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
