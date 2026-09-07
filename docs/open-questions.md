# Open questions

Genuinely undecided, plus work in progress. **Never state anything here as settled.** Once one
is resolved, move it to [decisions.md](decisions.md) with the evidence that resolved it.

**Live machine state is not recorded here.** It is stale the moment it is written; Moonraker
holds it authoritatively. Query it, or run `tools/print-monitor.py` — see
[AGENTS.md](../AGENTS.md).

## Active work

### SO-ARM101 follower — 5 of 11 parts done

Sliced figures are measured, not estimated. Slice with `slice-plate.sh`, which centres on the
measured mesh; **verify the emitted footprint against the mesh bounds before printing**, and
**never slice while a print is running**. Parts live in `~/models/so-arm101/` on the Pi.

**The parts are reproducible from upstream, verified 2026-09-07.** Do not record which machine
holds a clone — clone it where you need it:

```bash
git clone https://github.com/TheRobotStudio/SO-ARM100.git      # ~450 MB checked out
tools/extract-soarm-parts.py \
  SO-ARM100/STL/SO101/Follower/Ender_Follower_SO101.stl  <outdir>
```

All 11 parts came out **byte-identical (md5) to the copies on the Pi** that are being printed,
from a fresh clone on a bare machine. So upstream geometry has not moved since the 2026-09-06
measurements, the extractor is deterministic, and the Pi's models are trustworthy rather than
merely old. Re-run this check rather than assuming it still holds after an upstream change.

| Plate | Parts | Profile | Time | g |
|---|---|---|---|---|
| 3 | Upper_arm, Under_arm, Wrist_Roll_Pitch | `plaplus_soarm` | 13 h 49 | 143 |
| 4 | Rotation_Pitch, Wrist_Roll_Follower, Moving_Jaw | `plaplus_soarm` | 10 h 24 | 102 |

Per-part figures, sliced and measured 2026-09-06 with **supports everywhere**, so these are
**upper bounds** — the `plaplus_soarm` profile (snug + build-plate-only) comes in under them,
e.g. `Rotation_Pitch` 51.3 g grid-everywhere against 42.6 g as actually sliced:

| Remaining part | g | Time | Overhang |
|---|---|---|---|
| `Upper_arm` | 61.6 | 5 h 51 | 3.8 % |
| `Rotation_Pitch` | 51.5 | 4 h 53 | 11.2 % |
| `Wrist_Roll_Pitch` | 50.8 | 4 h 47 | 8.3 % |
| `Under_arm` | 49.4 | 4 h 39 | 4.2 % |
| `Wrist_Roll_Follower` | 46.9 | 4 h 48 | 5.5 % |
| `Moving_Jaw` | 22.2 | 2 h 26 | 14.0 % |

**Orientation is settled for five of six; one slice test outstanding.** Screened 2026-09-07
with [`tools/orientation-study.py`](../tools/orientation-study.py) — see
[decisions.md](decisions.md#supports). `Rotation_Pitch` is re-sliced rotated and printing.
`Upper_arm`, `Under_arm`, `Wrist_Roll_Follower` and `Moving_Jaw` stay as extracted.
**`Wrist_Roll_Pitch` should be flipped 180°, and the pending slice test now confirms rather
than decides.** It is the awkward part of the set — no good flat face in any orientation. The
flip wins on three axes and loses on one:

| | as-extracted | **X180 (flip)** |
|---|---|---|
| bed support | 7.53 cm³ | **4.83 cm³** (−36 %) |
| **bed contact** | **251 mm² / 9 %** | **577 mm² / 21 %** (+130 %) |
| aspect (h/√contact) | 3.93 | **2.59** |
| unsupported overhang | 754 mm² | 858 mm² (+14 %, against) |

**Bed contact is what decides it.** At 251 mm² on a 62 mm-tall part it is the worst in the set
and outside anything printed successfully here; flipped it lands in the same class as `Base`
(1692 mm², aspect 2.11), which ran 11 h 25 clean. A tall part with a poor grip is how a job
lets go hours in.

**Add a brim.** The standing objection — that a brim welds neighbouring features on open-mesh
models — does not apply to a solid part, and 577 mm² under 62 mm of part is worth the
insurance. `brim_width` is not in the profiles today, so this means a per-job override or a
one-line profile variant; decide which before slicing plate 3.

**Open: plate order does not match assembly order.** Building and testing from the base
upward, the next part needed is **`Rotation_Pitch`** — which sits on plate 4, behind all of
plate 3. Two facts make this cheap to fix rather than a constraint to live with:

- **The support-grouping rule does not bind among the remaining six.** All six need supports,
  so all six slice with `plaplus_soarm`. "One plate cannot mix the two groups" is satisfied by
  *any* grouping of them — plates 3 and 4 were split on bed space and time alone, so they can
  be re-grouped freely by assembly order at no cost.
- **`Rotation_Pitch` alone is ~4 h 53 at worst, and less as actually sliced.** That fits a
  daylight window, which means **it sidesteps the LED-strip decision entirely** rather than
  waiting on it, and it gets the base joint assembled and test-fitted before another ~24 h is
  committed to the rest. That is the same "prefer a cheap print that discriminates" reasoning
  that the gauges settled the elephant-foot question with — see
  [decisions.md](decisions.md#slicing).

  Assembly order from the base up is `Rotation_Pitch` → `Upper_arm` → `Under_arm` →
  `Wrist_Roll_Pitch` → `Wrist_Roll_Follower` → `Moving_Jaw`. **Re-plate before slicing 3 or 4.**

Open within it:

- **Fit the LED strip before plates 3 and 4?** Neither fits in a daylight window, and the
  camera is blind in the dark. See the night-monitoring item below.

### `Kinetic_Toy.gcode` is sliced, correct and waiting

Re-sliced 2026-09-03 with bed-first heating and corrected retraction — 13 h 41, 87.4 g,
verified in the emitted G-code. Started and aborted within three minutes for the garage move;
the bed reached 68 °C and the hotend never left ambient, so no filament was laid. **Do not
re-slice it.**

The recalibration it was waiting on is done and the camera is back, so **the remaining blocker
is light, not hardware.** At 13 h it runs unattended into the night. Either start it early
enough to finish the critical first hours in daylight, or fit the LED strip first. The white
spool it was queued against was swapped for **red PETG** on 2026-09-06, so it comes out red
unless white is reloaded; 87.4 g is not a constraint either way.

### Coupon ladders printed 2026-09-01, not yet measured

Three ladders on `coupon_ladder`: M3 clearance 3.2/3.4/3.6, insert bores 3.8/4.0/4.2, motor
bores 37.3/37.5/37.7. Smallest that fits wins; **test from the top face down**, since
`elefant_foot_compensation = 0` leaves the bottom edge slightly proud. Feeds koala-bot's
`params.py`. Needs screws and the motor body in hand.

### Four sliced files still heat the nozzle during the bed soak

Audited 2026-09-06. Still emitting `M104` before `M190`: **`LittleGrassDragon`,
`Flexi-Rex-200`, `Flexi-Rex-improved`, `coupon_ladder`**. Correct already: `3DBenchy`,
`Godzilla`, `Kinetic_Toy`, `first_layer_test`. **Not chronological** — `3DBenchy` predates the
fix but was sliced correctly, so **check the file, not its date**:
`grep -avE '^;|^$' FILE | head -6`. Consequence is a blob of ooze and a dirty nozzle exactly as
the first layer starts, which is self-limiting (the purge line cleans the tip). **Re-slice when
next wanted rather than pre-emptively**; the files are otherwise correct.

## Machine

- **Night monitoring needs a light.** With the room dark, an auto-exposure snapshot is
  essentially black (mean 0–2/255) and auto mode caps its own shutter. Forced manual exposure
  rescues it to **gross failure detection only** — enough to confirm nothing has come loose,
  not enough for detail, and at ~0.5 s shutter anything moving smears. The v4l2 settings are in
  [hardware.md](hardware.md). **A cheap USB LED strip on the frame is the real fix** and is a
  prerequisite for treating the camera as useful on any overnight print.
- **The camera bracket is still to be designed.** Three things must be measured, not assumed:
  the frame extrusion face width where it mounts (**20 vs 40 mm — the bracket differs
  completely**), whether M5 T-nuts are on hand or the bracket should clip over the extrusion,
  and the viewpoint. Best view found so far is front-left, slightly below or level with the
  nozzle plane, looking slightly up. The camera has a 1/4" tripod thread, so the bracket can
  bolt to that rather than clamping the body. **Hold roughly the current distance** — the lens
  is fixed focus. Print it in PETG.
- **`moonraker-timelapse` is installed on `printhub` but not wired up** (installed 2025-12-30). Present and
  correct: `component/timelapse.py` symlinked into `~/moonraker/moonraker/components/`,
  `klipper_macro/timelapse.cfg` symlinked to `~/printer_data/config/timelapse.cfg` and
  already `[include]`d by `printer.cfg`, `/usr/bin/ffmpeg` for rendering, so
  `TIMELAPSE_TAKE_FRAME` already exists as a macro. **This was blocked on having a camera; the
  camera was fitted 2026-09-02, so it is now unblocked.** Still missing:
  1. `[timelapse]` section in `moonraker.conf`.
  2. `[webcam]` section in `moonraker.conf` — needed for Mainsail to display the feed; the
     snapshot endpoint works without it.
  3. `[update_manager timelapse]` so it is kept current.
  4. `TIMELAPSE_TAKE_FRAME` appended to `layer_gcode` in the profiles, currently just `G92 E0`.
     **Without this no frames are captured.**

  Use `hyperlapse` mode — see [decisions.md](decisions.md#camera-and-monitoring). **Do not edit
  `moonraker.conf` during a print.**
- **No `[idle_timeout]` section in `printer.cfg`**, so Klipper's default 600 s applies and runs
  `TURN_OFF_HEATERS` + `M84`. A bed heated to 80 °C for a pre-mesh soak was silently switched
  off at the 10-minute mark, because **heaters at temperature do not count as activity** — only
  motion and commands do. `SET_IDLE_TIMEOUT TIMEOUT=3600` fixes it for a session but does not
  survive a restart. **Decide:** a persistent `[idle_timeout]` with a longer timeout, or a soak
  macro that keeps the machine busy. Note the trade-off — a long timeout means heaters stay
  live longer after an abandoned job.
- **No `CANCEL_PRINT` macro in `printer.cfg`.** Moonraker's cancel zeroes the heaters but
  leaves the nozzle parked on the part at temperature — hit 2026-09-01, needed a manual
  retract/lift/park. `END_PRINT` already has the right body; add a `[gcode_macro CANCEL_PRINT]`
  that calls it. Note `M84` there clears the homed flag, so a cancel always needs a re-home.
  **Fires exactly when a print is already going wrong**, which is the argument for doing it.
- **[calibration.md](calibration.md)'s post-move procedure still says to re-run
  `PROBE_CALIBRATE`** on a basis that [decisions.md](decisions.md#build-surface) shows is
  flawed for a surface change. **Never answered: reword it, or keep it as belt-and-braces?**
- **Confirm the Wi-Fi fix holds.** Power-saving is disabled three ways and persistent logging
  is on, but the original 35-minute dropout was never caught in the act, so power-save is the
  **strong suspect rather than a proven cause**. If it recurs, the journal will now say why.
- **Move the PETG spool indoors or into a dry box.** Now a heat and UV problem as well as a
  damp one — PETG is hygroscopic and a sunlit greenhouse is a poor filament store.
- **A slicer off the print host would remove the "never slice during a print" constraint.**
  It bit tonight: comparing `Wrist_Roll_Pitch` orientations had to be deferred ~3.5 h because
  `printhub` is the only machine with PrusaSlicer, and it was busy printing. Neither `blake`
  (12 cores) nor `ivory` (12 cores) has one, and both are far faster than the Pi's 4 cores.
  **Put it on `ivory`, not `blake`** — blake gets wiped. **Pin the version to 2.5.0**, or
  figures stop being comparable with everything already measured, and note that a newer
  PrusaSlicer would also change support behaviour (organic supports arrive in 2.6). This is the
  same conclusion the multi-printer section reaches from a different direction.
- **Keep the flashing microSD with the printer.** MCU firmware updates still go via SD; see
  [klipper-setup.md](klipper-setup.md#consequence).

## Materials wanted

- **ABS profile** — missing, and a drop-in file.
- **TPU profile.** A 3/4 spool of red TPU is on hand, previously dialled in on an Ender-3 for
  drone parts. **Those settings are gone and would not have transferred anyway** — that machine
  was Bowden, and its retraction compensates for tube compliance this direct-drive machine does
  not have. Temperatures and speeds would have carried; those are the easier half to re-derive.
  (This loss is what prompted putting these notes under version control.)
  - **Do not inherit the PETG retraction settings.** `retract_before_travel = 1`, `wipe = 1`
    and 40 mm/s are right for PETG and wrong for a material that buckles under compression.
    TPU wants near-zero retraction at much lower speed and accepts stringing as the price.
  - **Protect the PEI plate.** TPU bonds to PEI aggressively and is one of the few materials
    that can lift coating off a sheet on removal. Use a glue stick as a release layer rather
    than find out.
- **Lightweight (foaming) PLA profile**, for RC planes. **Treat as a separate problem, not a
  PLA variant** — nozzle temperature drives foaming expansion, so **temperature sets density**
  rather than just flow quality. Flow runs down to ~40–50 % to let the material expand, and
  prints are typically single-perimeter with no infill. Tuning means a tower stepping
  temperature and measuring density. Not something to guess at.
- **Temperature towers for PETG and PLA.** 240 °C and the PLA/PLA+ figures are generic starting
  points from datasheets, not this machine's or this filament's measured sweet spot.

## More than one printer

Two candidate second machines are on hand. **The Ender-3 V3 KE is likely to be commissioned
first, on desk space** rather than on capability.

### How a printer attaches decides almost everything

**This is the fork that reorders the whole question**, because the two candidates attach
differently:

- The **Ender-5 S1 and Ender-5 Plus are dumb MCUs on USB.** Klipper's host process runs on
  printhub, so each one consumes a USB port, a `klippy` process and real host CPU.
- The **Ender-3 V3 KE ships with its own Klipper host — the Nebula Pad**, a separate Linux
  module. Left stock it attaches over the network and consumes no printhub USB port and no host
  CPU. **But the Nebula Pad can be bypassed entirely**, driving the KE's mainboard MCU from
  printhub over USB exactly like the S1 — in which case it consumes both.

So "how many printers can the Pi drive?" is not a property of the printer. **It is a
consequence of a choice**, and for the KE that choice is still open.

### The USB constraint — verified on printhub 2026-09-07

**A USB hub is fine and port count is not the limit.** The MCU link is low-rate serial; the
CH340 negotiates at **12 Mbit/s** and Klipper uses a fraction of it. Bandwidth is a non-issue.
Four physical connectors, three in use (CH340, touchscreen, camera).

**The real constraint is device naming, and the standard Klipper advice breaks here.**

```
/dev/serial/by-id/usb-1a86_USB_Serial-if00-port0        -> ttyUSB0
/dev/serial/by-path/platform-xhci-hcd.0-usb-0:1:1.0-port0 -> ttyUSB0
```

**The `by-id` path carries no serial number** — just vendor and product — because the CH340
(`1a86:7523`) does not report one. **A second identical Creality board produces the identical
`by-id` path**, so "always use `by-id`, never `ttyUSB0`" fails exactly when there is more than
one printer. Which machine is which becomes a coin flip at every boot, and the config that
lands on the wrong one carries heater and kinematics settings.

**Use `by-path` for any USB-attached second machine.** It encodes physical topology — which
socket on which hub — and is stable and unique per socket; through a hub it simply gains path
segments. **Label the hub sockets physically and never move a cable between ports.** Boards
with native USB (STM32 CDC-ACM, `ttyACM*`) usually *do* carry unique serials, so a mixed farm
may have some printers safely on `by-id` and others not — check each rather than assume.

**Host CPU, not USB, is the ceiling.** printhub sits at load 0.35 across 4 cores with a print
running and the camera streaming, so there is headroom — **but the cost of a second `klippy`
instance has not been measured here, and should be before committing to a third.** The known
collision matters more as the count rises: PrusaSlicer saturating the Pi degrades *every*
running print, not just the one being sliced for. **A farm probably wants slicing off the print
host entirely.**

Two farm concerns known to matter generally but **not verified here**: use a self-powered hub
rather than bus-powered, and expect ground-loop and switching noise from multiple heated beds
sharing a USB ground tree. The latter would present as `ch341-uart: converter now disconnected`
— indistinguishable in `dmesg` from a deliberate power-off, per [hardware.md](hardware.md).

### Creality Ender-3 V3 KE — acquired 2026-09-07, unopened

**Likely commissioned before the Ender-5 Plus, on desk space.** 220 × 220 × 240.

**Nothing below is verified on the machine — the box is unopened.** These are vendor and
community facts that shape the plan; confirm each on the hardware before acting, per the
never-guess-hardware rule in [AGENTS.md](../AGENTS.md).

- **It ships with real Klipper, in the proper two-part architecture** — not Marlin with
  "Klipper" on the box, and not a Marlin conversion like the Ender-5 S1 was. So
  [klipper-setup.md](klipper-setup.md) does not apply: no flashing, no microSD.

  | Part | Role |
  |---|---|
  | Mainboard **GD32F303RET6** (treat as STM32F103, Cortex-M3) | runs Klipper **MCU firmware** |
  | **Nebula Pad**, a separate Linux module | runs the Klipper **host** (klippy), Creality's UI and the network stack |

- **It is Creality's fork, not mainline.** Their changes were never merged upstream, and the
  version on the printer is reported as **outdated and not directly updateable**. That is the
  substantive argument against leaving it stock — it is a Klipper that cannot follow Klipper.
- **Stock firmware is Creality's walled garden.** The community route to a normal Klipper stack
  is the **Guilouz `Creality-Helper-Script`** (written for the K1/K1 Max, reported working on
  the KE), installed over root SSH to the printer itself. It brings up **Moonraker on 7125**,
  with **Fluidd on 4408 and Mainsail on 4409**.
- **Open: does it join the tailnet?** It is a Linux host, so plausibly yes, which would make it
  reachable the same way printhub is. Unverified, and it decides whether it is addressable from
  the workstation directly or only via printhub.
- **Open: what does printhub's role become?** Under stock or helper-script, the KE hosts its
  own Klipper and Moonraker and printhub is only a *client* — slicing and orchestration. Under
  the bypass, printhub is its host as well. **The repo's
  convention that "Moonraker is `100.99.147.57:7125`" stops being unambiguous** the moment a
  second Moonraker exists on 7125 on another host. Decide the addressing convention before
  writing any KE automation.
- **The real decision is three-way, not two.** All three are reversible; none is committed.

  | | What it means | Cost |
  |---|---|---|
  | **Stock** | Creality Print and their cloud | Walled garden; a Klipper that cannot be updated |
  | **Helper script** | Keep the Nebula Pad, add Moonraker/Fluidd/Mainsail on it | Same Moonraker API this repo already drives, so `slice-print.sh` works against it; still Creality's fork underneath |
  | **Bypass the Pad** | Drive the mainboard MCU from printhub over USB with **mainline** Klipper | One host, one Moonraker, no addressing ambiguity, uniform with the S1 — but **consumes a printhub USB port and host CPU, so the USB constraint above applies** |

  **The bypass is the one that fits this setup best on paper** — it collapses the addressing
  question, keeps a single Moonraker, and puts the KE on mainline rather than a frozen fork.
  It is also the most work and abandons the Nebula Pad's touchscreen. Community configs exist
  for exactly this (`lividhen/Klipper-Ender-3-V3-KE`), driving the board through **Creality's
  serial-to-USB adapter** — **check whether that adapter is another CH340**, because if it is,
  the `by-path` requirement above applies to this machine on day one.
- **Physical inspection still applies**, even unopened — the 2026-09-01 lesson was a missing
  build surface, and a sealed box only rules out *later* loss, not a shipping fault.

### Creality Ender-5 Plus — not committed

In the garage, unused ~2 years, identified from the purchase invoice 2026-09-02.
**350 × 350 × 400 mm.** The case for it is that RC plane parts are long and 220 × 220 is the
binding constraint — a reason the KE does not address, since it is 220 × 220 too. **Now
likely the third machine rather than the second.** It is USB-attached, so everything in the
USB constraint above applies to it and not to the KE.

- **Klipper ships an official sample**, `printer-creality-ender5plus-2019.cfg` — the same thing
  that made this machine's commissioning safe. Use it; do not guess pins or thermistors.
- **NOT stock: a Micro Swiss NG Direct Drive Extruder is fitted.** This **voids the sample
  config as a wholesale source** — it describes the stock Bowden machine:
  - **`rotation_distance: 33.683` is wrong.** Calibrate by measurement (extrude 100 mm, measure
    what came through). Do not take the NG's gear ratio from the internet.
  - **The BLTouch offsets are wrong.** The NG relocates the probe and moves the nozzle relative
    to it. **This is the inverse of the bed-surface case: a surface change does not move
    `z_offset`, a toolhead change does.** `PROBE_CALIBRATE` genuinely is required here, plus
    re-measuring `x_offset` and `y_offset`.
  - **Confirm the thermistor and heater cartridge before powering the hotend.** If the kit
    supplied its own hotend, `sensor_type` may not be what the sample declares. **A mismatched
    sensor does not fail loudly** — it reads a plausible wrong temperature and the heater
    compensates in the wrong direction.
  - It is direct drive now, so TPU is viable on it and retraction transfers roughly from the S1.
    The earlier "TPU stays on the S1" reasoning is void.
- **Open: did the kit include an all-metal hotend, or is the stock lined one still in place?**
  `max_temp: 260` in the sample is the signature of a PTFE liner. This collides with the
  RC-plane plan — **lightweight PLA foams at 230–260 °C, exactly where a PTFE liner degrades
  and off-gasses.** If all-metal, LW-PLA becomes viable and the blocker disappears; if stock,
  the 260 ceiling stands. **Confirm visually before buying either.**
- **Flashing will differ** — the sample shows an FTDI USB bridge, not the S1's CH340, so
  [klipper-setup.md](klipper-setup.md) does not apply.
- **One Pi can host both S1 and Plus** — a second Klipper + Moonraker instance against a
  second MCU is established practice, and no second SBC is needed. But see the USB
  constraint above: address it by `by-path`, and **measure the cost of the second `klippy`
  instance** rather than assuming the headroom is free.
- **Physical inspection before any config work**, per the lesson from 2026-09-01: build surface
  present and intact, belts not slack, Z lead screw free, wheels not flat-spotted. The last
  machine out of that garage was missing its build surface, and it cost two failed prints and
  hours of confident wrong diagnosis.
- **Proposed split if commissioned:** S1 = PETG, TPU, detailed figures; Plus = large flat
  parts, plain PLA, LW-PLA, potentially carbon-filled. Driven by bed size and hotend
  capability, not extruder type, since both are direct drive.

## This repo's shape

- **Nothing arbitrates concurrent access to the printer.** "Never slice while a print runs" is
  enforced today by a single operator's attention. **If a second consumer (koala-bot's own
  session, say) starts driving its own prints, two agents can slice concurrently and nothing
  stops them.** Moonraker refuses a second *print*; nothing refuses a concurrent *slice*, which
  is the documented hazard. **Decide before the second consumer arrives, not after.** Cheapest
  workable answer is a lock file on the Pi that `slice-print.sh` and `slice-plate.sh` check,
  plus an explicit precondition in [AGENTS.md](../AGENTS.md).
- **Project knowledge should move out with its project.** The SO-ARM101 material in
  [decisions.md](decisions.md#project-decisions) and above is project work living in the device
  repo because this was the only context store when it was written. **Move it when the arm is
  finished, not mid-build.** What stays behind is only what generalises: batch by print time
  not footprint, bridgeability rather than overhang percentage, `buildplate_only` for bores.

## Deferred / parked

- **Deferred prints, now unblocked.** Flexi Rex (sliced at 100 % and 200 %), the remaining
  koala-bot coupons, and the original outstanding ask — two or three fun prints for the
  grandkids.
- **KlipperScreen display blanking** — cosmetic, tap to wake. Can be disabled if it annoys.
- **OrcaSlicer** — configured on paper but not the routine path; the Pi pipeline replaced it.
  Settings kept in [workflow.md](workflow.md) for when a print needs actual tuning.

## Project ideas raised, not committed

Printer-adjacent ideas from commissioning. Active robotics work lives in `~/Code/koala-bot`.

- **SpotMicro** ([thing:3445283](https://www.thingiverse.com/thing:3445283)) — quadruped,
  dozens of printed parts, 12 servos, Arduino Mega. PETG suits its structural parts.
- **6-DOF printable arm.** Accuracy depends on drive choice: hobby servos wander by
  millimetres; stepper + gear reduction reaches ~0.2–1 mm. AR4 (Annin Robotics) is the pick for
  repeatability; Thor (AngelLM) is the print-everything option; BCN3D MOVEO is easier but only
  5-DOF.
- **InMoov revival** — a partially built torso from ~8 years ago is on the shelf. **Parked as
  inspiration only:** upstream has had no activity since 2024, and the 3D-printed auger-thread
  neck actuators are mechanically compromised by friction.
