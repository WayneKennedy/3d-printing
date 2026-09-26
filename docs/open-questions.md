# Open questions

Genuinely undecided, plus work in progress. **Never state anything here as settled.** Once one
is resolved, move it to [decisions.md](decisions.md) with the evidence that resolved it.

**Live machine state is not recorded here.** It is stale the moment it is written; Moonraker
holds it authoritatively. Query it, or run `tools/print-monitor.py` — see
[AGENTS.md](../AGENTS.md).

## Active work

### Desk Gridfinity and openGrid — all 12 plates printed 2026-09-25

Decided so far: [decisions.md](decisions.md#desk-gridfinity). STLs come from
[`tools/gridfinity.sh`](../tools/gridfinity.sh) (Gridfinity Rebuilt pinned at `910e22d`).

- **Grid decided: twelve 4 × 4 plates, 504 × 672 mm** — [decisions.md](decisions.md#desk-gridfinity).
  **All 12 printed by 2026-09-25 16:02 BST** ([print-log.md](print-log.md)); fixing by
  double-sided tape is the owner's next step. Test bins: 4 × 2 × 3 (fit "perfect"), 4 × 2 × 9
  divided (overnight, not yet judged); 2 × 2 × 9 sliced, not printed. **4 × 4 × 3 with 16 × 1 × 1
  bays, no tabs, no lip** (`divx=4 divy=4 style_tab=5`) printing 2026-09-26 from 20:17 BST —
  6 h 58 m est., 135 g: the 24 divider walls dominate.
- **Sliced in `petg`, centred `104,123`, on the Debian 2.5.0 binary.** Footprints include the skirt
  and stay inside the mesh:

  | Part | Time | PETG | Footprint X / Y |
  |---|---|---|---|
  | `bp_4x4` | 2 h 17 m | 25.6 g | 16–192 / 35–211 |
  | `bp_3x4` | 1 h 43 m | 19.1 g | 37–171 / 35–211 |
  | `bin_1x1x3` | 1 h 11 m | 13.7 g | 82–126 / 101–145 |
  | `bin_2x1x3` | 2 h 01 m | 23.2 g | 61–147 / 101–145 |

  All 12 baseplates: about **25 h and 281 g**, before any bins.
- **Skeletonized 4 × 4 with screw holes, sliced 2026-09-23 — rejected, files deleted** (owner): **6 h 36 m on `petg`, 4 h 13 m on `petg_fast`, 64.7 g
  either way** — 2.5× the thin plate's filament. Footprint X 16–192 Y 35–211, bed-first
  header, no brim. Twelve plates at this rate: ~45 h and ~700 g (8 × 4 × 4 + 4 × 3 × 4, the
  3 × 4 not yet sliced). White spool: nearly a full 1 kg (owner, 2026-09-23), enough either way.
  **Owner rejected the time** ("6.5 hours per grid… absurd"). Printables pages quote ~40–56 min
  for a thin 4 × 4 and 5 h 04 m for a floored one with mounting holes, printer unstated.
  **Thin on `petg_fast`: 1 h 26 m, 25.6 g** (`gf_bp_4x4_petg_fast.gcode`) — ~16 h for all 12.
  Thin plates are back in play; how to fix them down is open: mounting tape, screw tabs into
  the 19/14 mm margin on perimeter plates, or M2 at interior nodes (solid Ø~9 at z0 but only
  Ø3.5 at the top face, so an M2 head (~Ø3.8) sits proud — bin-corner clearance ~1.8 mm).
- **Test bin 4 × 2 × 3 printing 2026-09-23 on `petg_fast`: standard style** (owner: "bare box,
  no dividers, auto label"), stock tab, scoop, stacking lip — 3 h 09 m est., 70.3 g. Lite was
  2 h 12 m / 41.2 g for comparison.
- **First `bp_4x4` (thin) printed 2026-09-23 17:34, white PETG.** Check how a bin seats and how the
  plate lies flat on the desk before committing the other 11 plates.
- **Next: print the ten remaining plates plain (thin, no tabs), then test the layout on the
  desk** (owner, 2026-09-23); the row/side joins and tab plan are settled after that. File:
  `gf_bp_4x4_petg_fast.gcode`, one plate per run. **Tabs added later to plain plates must be
  glued to the outer face or come with reprinted plates** — a separate piece clamped over the
  rim collides with edge bins (rim top is at 5 mm at the very edge; a bin wall stands 0.25 mm
  inside it).
- **Planned extension (owner, 2026-09-23, "probably"): a straight row of 4 × 4 plates across the
  back of the keyboard / soldering-mat area, lined up from the right-hand grid, joining a single
  column down the left side of the mat** — a U round the mat. Unknown: row length, column
  length, and whether 168 mm of depth is clear between keyboard and the monitor stand / MDF
  back panel. It turns some grid edges into plate-to-plate joints, so **the tab variants wait
  on the full outline.**
  The U adds **inner-corner tabs** (owner, 2026-09-23) at its two concave corners: a lap tab
  whose halves meet at 90°, pointing into the mat area. Tab types then: outer corner (1 plate),
  straight edge joint (2, lap), inner corner (2, lap at 90°). Proposed build: generate every
  plate from one layout list of plate positions, deriving outer edges, joints and corner types.
- ~~**Fixing: screw-down tabs**~~ **Dropped 2026-09-25 for double-sided tape** ([decisions.md](decisions.md#desk-gridfinity)). Was: tabs at the grid's corners and perimeter edge joints (owner leaning,
  2026-09-23; plan-view draft sent, not approved). 14 screws: 4 corner tabs, 10 lap-joint tabs
  (half from each neighbouring plate, one screw through both, so the joint is tied too). Tabs
  sit in the 14 mm front/back margin and **2 mm beyond the 500 mm area at the sides** (the grid
  is 504 wide), below the 5 mm plate top; the two thin middle plates carry none
  and are trapped by the ring. Screws unknown — none in wk-inventory `stock.md` or `purchases/`
  (searched 2026-09-23). Supersedes the frame idea below if approved.
- ~~**Frame: printed corners around the grid (owner).**~~ **Dropped 2026-09-25.** The spare margin fits a border exactly:
  19 mm each side and 14 mm front and back brings 462 × 672 out to 500 × 700. Open: corners only,
  or corners plus straight edge pieces (with corners alone, the middle plates along an edge can
  still slide outward); the frame's height and how it holds the plates' edge.
  **Deferred by the owner until two plates are printed and their alignment is seen.**
- **openGrid panel:** waiting for the back panel to arrive. Its dimensions, tile size (28 mm
  grid) and Full vs Lite are all open.

### Drawer Gridfinity — 7-drawer unit, waiting for the Ender-5 Plus

**Owner's decision, 2026-09-24: wait for the Plus** — partly as the push to commission it.
Symmetric layout wanted (18 mm fill at each side). **Preferred: two prints per drawer**, a 4 × 8
padded left (186 × 336 mm) and a 5 × 8 padded right (228 × 336), **if the Plus's usable area
takes 336 mm plus skirt** — unknown until its mesh is probed. **Fallback: 18 | 4×4 | 1×4 | 4×4 |
18 in two rows** (2 left-padded + 2 right-padded 4 × 4 at 186 × 168, 2 plain 1 × 4 strips),
all within the S1. 5 × 4 is not printable on the S1 (210 mm > ~194 usable).


Owner, 2026-09-24: a 7-drawer unit (Amazon), **internal 414 W × 335 D mm, 70 mm deep**
(re-measured; the first figures, 410 × 330, were wrong). **Two `bp_4x4` fit front to back
"perfectly snugly"** (owner, test-fitted plates 1–2): 8 units deep, no padding, and the snug fit
holds them. Across, 9 units = 378 mm leaves **36 mm**. Earlier S1-only proposal, superseded by the decision above:
- Per drawer: 4 × `bp_4x4` (8 × 8 units) + a 1-unit column padded to fill the 36 mm,
  printed as two 1 × 4 strips ≈ 78 × 168 mm (Gridfinity Rebuilt `distancex`, or split 18 mm
  each side). All within the S1's 4 × 4 limit. (The Plus
  may not manage a 336 mm-deep plate; its mesh is unmeasured.)
- 7 drawers: 28 × `bp_4x4` (1 h 31 m, 25.6 g each) + 14 strips (unsliced) ≈ 45 h, ~800 g —
  more than the white spool holds. Check wk-inventory filament before buying.
- **Bins: 9 U** (decided — [decisions.md](decisions.md#desk-gridfinity)); 63 mm in a 70 mm drawer,
  clearance under the drawer above still to confirm.
- Location codes `DRW1`–`DRW7` (wk-inventory `AGENTS.md`); proposed top = `DRW1`, unconfirmed.

### Print speed — how fast this machine can go (raised 2026-09-23)

**Owner's aim:** print the second desk `bp_4x4` at the fastest this printer can manage, "for science",
and learn what would speed it up generally. Plan, **nothing run yet**:
1. **Measure the hotend's max volumetric flow in PETG** (air extrusion, 100 mm at rising
   mm³/s, owner measures the mark). **No measured Sprite figure exists anywhere** — a forum
   thread asking exactly this is unanswered
   ([3dprintingspace](https://3dprintingspace.com/t/sprite-extruder-maximum-flow/7659)).
   Creality's "50 mm³" is a melt-chamber volume, not a rate.
2. **`petg_max` profile:** `max_volumetric_speed` ≈ 85 % of measured, all feature speeds at the
   300 mm/s Klipper cap so flow decides, slicer accelerations 5000, first layer unchanged. No
   `printer.cfg` change, so this is the ceiling **as currently configured**.
   **Owner clarified 2026-09-23: fidelity is paramount — the fastest settings that do not
   distort the part, not the absolute maximum.**
3. Slice `bp_4x4` with it and compare to 2 h 17 m. **Where plate 1's time goes** (G-code
   parse, trapezoid model: 135 min vs slicer 137): perimeters 50 min (45 mm/s), external
   perimeters 42 min (30), **solid infill 27 min at 20 mm/s on every layer**, the rest 16. Modelled,
   not sliced: 80/50/80/120 mm/s (perim/ext/solid/infill), travel 250 → ~89 min; 100/60/100/150 →
   ~81 min, peak flow 9 mm³/s. Accel 20 000 (CoreXY-class) at today's speeds saves only 7 min;
   at 100/60/100/150 it gives ~68 min — acceleration pays only once speeds are up. Then tune
   pressure advance and keep external-perimeter acceleration lower for ringing. A speed-induced dimensional error would
   confound the two-plate alignment check the frame design waits on.

**Where this printer stands** (live via Moonraker 2026-09-23; `reference/printer.cfg` agrees):
`kinematics: cartesian`, `max_velocity 300`, `max_accel 5000`, `square_corner_velocity 5`,
**`pressure_advance 0` (never tuned), no `[input_shaper]`, no `[adxl345]`.** The `petg` profile
runs perimeters 45, external 30, infill 60, travel 150 mm/s and emits no `M204`, so every move
gets Klipper's 5000. At 60 mm/s × 0.45 × 0.2 infill needs only ~5.4 mm³/s — **the profile, not
the machine, is the limit today.** Estimates land within 1–2 % of actual, consistent with
speeds low enough that acceleration barely matters.

**Why the Sovol SV08 is fast — checked 2026-09-23.** A GPL-3.0 derivative of the Voron 2.4
([Sovol3d/SV08](https://github.com/Sovol3d/SV08)): flying-gantry CoreXY on linear rails, so
the bed moves only in Z and both XY motors are frame-mounted — low moving mass. Stock config
has an `[adxl345]` on the toolhead, input shaper (mzv 35 Hz), `pressure_advance 0.025`,
`max_accel 40000`, `max_velocity 700`. Hotend flow ≤ 30 mm³/s is **manufacturer-only**.
**Independent:** ~12–13½ min speed Benchy ([Tom's Hardware](https://www.tomshardware.com/3d-printing/sovol-sv08-review)),
which recommends 200–300 mm/s for quality prints; adhesion at speed and default over-extrusion
needed fixing. "Open source" holds but is a **Sovol fork of Klipper 0.12**, criticised as stale
([issue #28](https://github.com/Sovol3d/SV08/issues/28)); going mainline needs an ST-Link.
£389 at sovol.uk on 2026-09-23 (out of stock). **The Ender-5 S1 is a Cartesian cube with its
X motor on the moving gantry** ([Creality](https://www.creality.com/products/ender-5-s1-3d-printer);
reviews put it at ~90–120 mm/s before ringing, [3DPrintBeginner](https://3dprintbeginner.com/creality-ender-5-s1-review/)).
It cannot reach SV08 accelerations; its headroom is in flow, pressure advance and input shaping.

**Speed levers here, cheapest first** (none tried):
- **Profile speeds up to the measured flow** — free; step 1–2 above.
- **Tune pressure advance** (Klipper tuning tower) — free; keeps corners clean at speed.
- **Input shaper** — needs an ADXL345 (**check wk-inventory before buying**) or Klipper's
  manual ringing-tower method, which needs nothing. Then accel can be raised with less ringing.
  Needs a `printer.cfg` change — never during a print (AGENTS.md rule 2).
- **Fewer, thicker layers for functional parts** (0.28 mm; a 0.6 mm nozzle) — the Gridfinity
  plates are the obvious case.
- **Hotend hardware** (high-flow nozzle) — only if the flow test shows the hotend is the limit.

### bam-rig (wk-robotics) — moved to the Ender-3 V3 KE, other filament

**Owner, 2026-09-24 23:10 BST: the white PETG spool is reserved for Gridfinity; bam-rig will print
on the Ender-3 V3 KE in another filament.** The S1 G-codes below are therefore not used as they
stand — the KE needs its own slice, and a different material may need its own profile.

Staged 2026-09-24 in `~/bam-rig` on printhub (outside Mainsail) by a wk-robotics session;
parts and requirements are that repo's. **Owner chose two plates** (2026-09-24), overnight,
possibly split between this printer and the Ender-3 V3 KE if it is commissioned in time:
`bam-rig-plate1-bracket-arms-100pc.gcode` (6 h 15 m, 125.6 g, 100 % rectilinear) and
`bam-rig-plate2-pots-lids.gcode` (4 h 54 m, 107.7 g) — both verified 2026-09-24 against this
repo's rules (no brim/support, `M204 S`, bed-first header, footprint in mesh). Both are S1
G-code; the KE needs its own slice. A one-plate 3MF (`bam-rig-oneplate.gcode`, 11 h 07 m) was
built and verified but not chosen: it saves ~15 min and risks every part on one run.

### koala-bot brims contradict the no-brim rule

The [house rule](decisions.md#slicing) (2026-09-23) says no brim without a recorded failure.
koala-bot still adds them: `hardware/print/manufacturing-petg.ini` and
`manufacturing-petg-tree.ini` set `brim_width = 4`, `manufacturing-tpu.ini` sets 3, and
`hardware/src/koala_hardware/export.py` flags "brim" for tall or small-footprint parts
(`tray_spacer` in `docs/bom.md`). koala-bot's DEC-39 permits declared brims. **Not changed
yet:** on 2026-09-23 koala-bot had 42 uncommitted files, `export.py` among them, so it was
left for whoever owns that work. Until it is changed, override on the command line with
`--brim-width 0` when slicing koala-bot parts here.

### TPU 95A — profile and calibration

**Spool loaded 2026-09-21** (owner): Reprapper **Silk** TPU, yellow, 1.75 mm, 250 g, batch
20260407S01. 95A (owner; product listing). **Temperature: label 205–230 °C, listing 180–220 °C** —
they disagree, so the tower spans both. For two wk-drones parts
([wk-drones](https://github.com/WayneKennedy/wk-drones)):
- **Holybro 10" FC deck, rev C** — **printing 2026-09-21 at the owner's request** (rev B is
  superseded). Modelled in CadQuery from the 2D drawing, with the coupon's corrections (arms drawn
  1.9, hex 4.85 AF untested): wk-drones `aircraft/holybro-10/print/src/h743-deck-revc.py`, commit
  `1b11e03`. `h743_deck_revc.gcode`: upside down (`--rotate-x 180`), no support, 3 h 00, 17.1 g.
  **Printed 2026-09-22 00:45**, 176 min, full filament delivered. **Owner: "perfect"; the 4.85 AF
  hex takes a standoff by hand and needs pliers to remove** — press-fit answered, allowances
  moved to [decisions.md](decisions.md#materials). The pillars-only coupon is no longer needed. A 38 × 56 × 5 mm platform carrying the FC hangs on four Z-shaped flexure arms
  between two anchor blocks; 20 mm brass hex standoffs (4.55 AF) are pressed through Ø11 ×
  19.8 mm TPU pillars. Prints **upside down, FC face on the bed**; no bridges or overhangs.
  Per the wk-drones session, 2026-09-21, in priority order: (1) the **hex press-fit** — drawn
  at nominal 4.55 AF on the untested assumption that TPU holes print undersize and grip;
  (2) **arm width** — the arms are 2.0 wide × 5.0 tall, solid perimeters, and are the
  isolator's spring: stiffness goes with width³, so a 10 % width error is ~30 % in stiffness;
  (3) **first-layer flatness and release** — the FC seats on the first-layer face. Target
  natural frequency 25–40 Hz is tuned from flight logs, so **batch consistency matters more
  than the absolute hardness** — keep the batch number with the part.
- **Bee35: a mount for the Matek M10Q-5883 GPS** (owner, 2026-09-21), whose widest element is
  its 20 × 20 mm PCB. Candidate `220.stl` (pocket 20.4 × 22.4) per wk-drones'
  `aircraft/bee35/print/sources.md`; the choice of model is wk-drones'.

**What those parts need decides what gets calibrated: press-fit, thin-wall width and the first
layer — not bridging, overhangs or surface finish.**

**Profile `tpu` — created 2026-09-21, untested.** `~/slicer/ender5s1_tpu.ini`, `petg` with:
215 °C (220 first layer), inside the overlap of both ranges; bed 50 °C; retraction 0.4 mm at
20 mm/s, no wipe, no lift, not on layer change, only on travels over 2 mm; fan 30–50 %, off
for layer 1 only; speeds 15–25 mm/s; `max_volumetric_speed = 2.5`; `avoid_crossing_perimeters`.
**Do not copy PETG's retraction** (`retract_before_travel = 1`, `wipe = 1`, 40 mm/s): TPU
buckles under compression, so it wants little retraction, slowly, and accepts stringing as the
price. Every value is a starting point, not a measurement. Verified by slicing koala-bot's
`front_contact_pad` on both binaries: bed-first header intact, 220 → 215 after layer 1, peak
extrusion 2.50 mm³/s (2.9.6) / 2.04 (2.5.0), ~6 g, ~53 min. **`START_PRINT` needs no change**
for TPU: its purge runs ≈1.6 mm³/s and its retractions are 0.5 mm and 2 mm at 30 mm/s.

**Before the first TPU print:**
- **No glue-stick release layer — owner's decision, 2026-09-21.** None is owned. TPU bonds to
  PEI aggressively and can lift coating on removal; the owner accepted that on the grounds
  that the plate is double-sided and they have printed TPU on PEI before without damage (on
  another machine; not recorded here). **If a part will not release, let the plate cool fully
  and flex it; do not lever the part off.**
- **The spool is dry**: new, vacuum bag opened the morning of 2026-09-21 (owner). If it sits
  out for weeks, that no longer holds — TPU is hygroscopic and wet TPU pops, strings and bonds
  badly.
- **The owner watches the first layer** (AGENTS.md rule 7); babystep if it is over-squished —
  TPU tolerates a slightly high first layer better than a crushed one.

**Calibration prints, in order.** Grams and times are estimates until sliced; the whole plan
should cost ~20 g of the 250 g spool.
The tower needs no bridge or overhang features: nothing it serves has them. The spool is small, so do not print a calibration step
that no consumer part depends on.

| # | Print | Settles | Read it by | Est. |
|---|---|---|---|---|
| 1 | **Temperature tower, 230 → 180 °C in 5 °C bands** (11 bands, spans both ranges). **Sliced 2026-09-21: `tpu_temp_tower.gcode`**, 2.9.6, 60 min, 5.9 g, footprint X 87–121 Y 113–133, no gap fill; STL `~/models/calibration/tpu_tower.stl` from [`tools/temp-tower.py`](../tools/temp-tower.py). Band *n* (0 = bottom) is Z 5n–5n+5 at 230 − 5n °C. **Printed 2026-09-21: under-extrudes from 190 °C (band 8), no extrusion at 180, stopped by `M112`** ([print log](print-log.md)); 195 is the coolest clean band. **Profile floor ~205 °C** (reasoning, not measurement: 15 °C over the 190 onset, because under-extrusion thins the arms and arm width is what sets their stiffness). **Tear test (owner): no layer tears by fingertip and nail anywhere 0–40 mm (230–195 °C); tears easily above 40.** Sheen best and uniform 20–35 mm (210–200 °C). Released from bare PEI very easily, plate unmarked by report. **Tower peaked at 2.04 mm³/s (mean 1.44)**, so the onset holds only up to ~2.0. **→ Profile set 2026-09-21: 210 °C (215 first layer), `max_volumetric_speed` 2.0, slicer `z_offset` −0.02** (TPU G-code only; `printer.cfg` untouched) | nozzle temperature | bend and try to tear each band by hand: lowest band that will not split between layers, then the silk sheen and stringing among those that pass. Owner reports; nothing inferred from telemetry | ~8 g, ~2 h |
| 2 | **Single-wall 20 mm cube** (spiral vase), at the #1 temperature | `extrusion_multiplier` | calipers on the wall at 8 points against the 0.45 mm extrusion width | **Printed 2026-09-21**, 16 min, job state `complete`. The wall is intact about a third of the way up, then loops of strands. **Cause unknown**: first read as a floppy one-line wall, but the next job extruded nothing at all, so **feeding may already have been failing here** (`filament_used` is commanded E, not measured, so it cannot tell). Lower wall: 8 readings 0.40–0.42 mm against 0.45. **Void: the spool was found tangled** (owner, 2026-09-21; how is not known), so drag was building during this cube — the likelier cause of the loops — and the reading cannot be separated from it. The 1.10 multiplier set from it is **reverted to 1.0**. **Re-measured 2026-09-21 on `tpu_flow_cube_8.gcode`** (8 mm, flow 1.0) after untangling and hand-feeding 50 mm cleanly: **8 readings all 0.44 mm against 0.45 → `extrusion_multiplier` stays 1.0** — 2 % is inside caliper resolution (0.01 mm ≈ 2 % here) and TPU compresses under the jaws. The coupon's 2.0 mm arm checks it at a larger width. **Release: a sticky tug when pulled warm** (owner, deliberately not cooled — "feels like a plus"); easy with light pressure when cool. `z_offset` −0.02 stays. **The tower's onset is not affected**: a tangle only tightens, and the cube's lower wall printed cleanly after the tower's cold bands failed. **Released easily, light pressure only, at `z_offset` −0.02** (owner) — offset unchanged pending the coupon's thin arms. Next TPU cube: `--height 8` |
| 3 | **Deck coupon** — **failed 2026-09-21: nothing extruded from the start** (no purge line, no skirt; owner), ran 73 min on air, stopped by `M112` at Z 5.4 at 210 °C. **Cause: the spool was tangled** (owner) — the extruder pushed against a locked spool throughout. **Re-sliced at flow 1.0: `tpu_deck_coupon.gcode`**, 2 h 04, 11.6 g, first layer Z 0.22, no gap fill. **Results from the partial print (owner, 2026-09-21)** — plate 4.1 and arms 4.85 tall, both complete; pillars stopped at 5.15:
  - **Arms print ~0.1 mm wide**: drawn 1.8 / 2.0 / 2.08 / 2.2 → **1.98 / 2.10 / 2.20 / 2.30**. Flow is right (cube), so this is edge spread; consistent +0.10–0.12 over 2.0–2.2, +0.18 at 1.8 (fewer loops, widened lines). **Draw ~1.9 to print 2.0**; 2.1 vs 2.0 is ~16 % stiffer (width³).
  - **Windows**: +0.2 snug, +0.4 and +0.6 loose → **a 20.0 mm board wants a 20.2 pocket.** `220.stl`'s 20.4 × 22.4 would be loose on both axes.
  - **Hex holes too tight at every size**: across flats 4.34 / 4.36 / 4.70 (inside jaws, drawn 4.45 / 4.55 / 4.65 — inconsistent, treat as rough). Owner: the 4.65 takes a 4.55 AF standoff only with a press, and **20 mm of it would need a press and silicone**; the smaller two tighter. **Rev C's 4.55 AF will not press through.** Likely cause (reasoning, not measured): **rounded printed corners bind the brass hex's sharp corners** (5.25 across corners) before the flats matter. Next: a pillars-only coupon, full 19.8 mm, 4.75 / 4.85 / 4.95 AF, optionally a corner-relieved hex.
  - **Plate flatness: perfectly flat** (owner) — the first-layer face the FC seats on is sound.

**Second attempt lost at 71 min to a USB over-current that dropped the MCU** ([below](#usb-over-current-dropped-the-mcu-mid-print-2026-09-21--cause-found)); purge, skirt and first layer had been good. Reprint unchanged. **Watch for the purge line and skirt** — telemetry cannot see a feed failure. Original plan: on a flat base printed like rev C's first-layer face: three **Ø11 × 19.8 mm pillars with hex holes at 4.45 / 4.55 / 4.65 AF** (the real pillar, so hoop stiffness and grip length match); three **arms 5.0 mm tall × 30 mm at 1.8 / 2.0 / 2.2 mm wide**, solid perimeters, no infill; **20 × 20 mm square pockets at +0.2 / +0.4 / +0.6** for the M10Q-5883 PCB | the hex size rev C should draw; whether 2.0 mm prints at 2.0; the clearance a 20 mm board needs | a brass standoff pressed into each pillar (goes in by hand? holds? splits?); the GPS board tried in each pocket; arm widths by calipers at 5 points; the base checked flat on glass. **Before printing, check the arm G-code for gap fill** — a width that is not a whole number of perimeter lines prints a gap-fill seam down the spring, and the fix is a CAD width, not a setting | ~8 g, ~1.5 h |
| 4 | **Bee35 GPS mount, SpeedyBee `220.stl` as-is** (owner's choice over a scaled or redrawn version) | the profile on a real part; the frame interface; whether the corner clips hold a board that the coupon says is loose in a 20.4 × 22.4 pocket; whether the JST-GH connector clears | fit on the frame and of the M10Q-5883 | **Started 2026-09-21**, `bee35_gps_220.gcode`, 47 min, 4.2 g. Downloaded from SpeedyBee's Bee35 print-files page (SHA-256 `1e53d298…`, Shapr3D export, closed mesh, 3.39 cm³), kept at `printhub:~/models/bee35/` and not committed (licence TBC, per wk-drones `sources.md`). **Printed standing on its original +Y face, no supports** — the only orientation with no large unsupported ceiling: as-authored makes the pocket roof a 20 × 22 mm bridge; this leaves a 6.2 mm bridge, two 1 mm hole roofs, and one 2 mm-deep ledge under the middle clip (~25 mm², 19–21° from horizontal) printed into air. Supporting that ledge would mean TPU support on a TPU face. 2.9.6 warns of floating bridge anchors and loose extrusions — that ledge. **Why not scale it:** a 10 % Y squeeze to reach 20.2 distorts the frame interface too, and the 22.4 axis may be deliberate connector room. **Result (owner): usable.** The M10Q-5883 seats and three of the four lugs hold it; **the top lug (connector edge, top in print orientation) printed into air** and is strings — owner judges the JST-GH plug will hold that edge. The 2 mm ledge printed fine. **Prediction error:** the straight-down ray check put that lug's underside in "support would stand on the part" and it was then dismissed as small; an **organic tree from the bed can curve round the part to reach it**, which a vertical ray cannot see. **Reprint, if wanted: organic, bed-only support** (as `petg_fig_tree`), checked in the slice to touch only that lug |

Skipped unless something forces them: a **retraction test** (stringing is cosmetic on these
parts, and TPU trades it for reliable feeding) and a **volumetric ceiling test** (2.5 mm³/s
only matters if jobs are too slow, and these parts are small). **Pressure advance stays off**,
as for every other material here — `printer.cfg` sets none.

**Flow cube and deck coupon sliced 2026-09-21 at the tower's settings**, both in Mainsail, first
layer at Z 0.22, footprints in the mesh: `tpu_flow_cube.gcode` (spiral vase, 1 perimeter,
3 bottom layers, 16 min, 1.1 g) and `tpu_deck_coupon.gcode` (2 h 05; **re-sliced with `extrusion_multiplier` 1.10**, 12.7 g — above the ~8 g
estimate). STLs `~/models/calibration/` from
[`tools/calibration-parts.py`](../tools/calibration-parts.py), whose docstring gives the
coupon's layout; both verified closed and outward-facing, volumes matching hand calculation.
**No arm has gap fill, 2.0 mm included** — 2.9.6's variable-width perimeters print 2.0, 2.08 and
2.2 as the same loops (1.8 one loop fewer), so the extra 2.08 arm, added on fixed-width
arithmetic, was unnecessary: **rev C can keep 2.0**, and its accuracy is a flow question. 2.9.6
warns "Low bed adhesion — consider brim" for the coupon; **not acted on**: the 55 mm tower on a
12 mm core stood without a brim, and a brim would distort the bottom of the arms and pillars
being measured. **Before either: check the filament for a gear notch** from the 185/180 bands. **The three pillars come off as loose parts: mark each (left → right = 4.45 / 4.55 /
4.65 AF) before lifting it off.** `220.stl` is
on neither host — wk-drones records its source (SpeedyBee's Bee35 download) but not the file;
it matters only if the owner names the GPS mount as the Bee35 part. When `tpu` is validated,
koala-bot's provisional `hardware/print/manufacturing-tpu.ini` (230/50) should layer on it
rather than on `petg`.

### SO-ARM101 follower — all 11 parts usable; next is assembly

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

| Plate | Parts | Profile | Time | g | Status |
|---|---|---|---|---|---|
| 3 | `Upper_arm`, `Under_arm`, `Wrist_Roll_Pitch` flipped | `plaplus_soarm` | 13 h 30 | 136.9 | **Done 2026-09-08 17:26.** Two good; `Wrist_Roll_Pitch` fork face printed into air, unusable — [print-log](print-log.md), [decisions](decisions.md#supports) |
| 3b | `Wrist_Roll_Pitch` flipped, **supports everywhere** | `plaplus_soarm_all` | 4 h 06 | 39.9 | **Failed 2026-09-08**: support welded to both fork faces — [print-log](print-log.md), [decisions](decisions.md#supports) |
| 4 | `Wrist_Roll_Follower`, `Moving_Jaw` | `plaplus_soarm` + **5 mm brim** | 6 h 19 | 59.6 | **Done 2026-09-09 05:43**, parts not yet inspected. Both pass `--bands` as extracted (61 and 2 mm² dropped, scattered). Brim because `Moving_Jaw` has only 30 mm² of flat bed contact (aspect 4.09); passed as `--brim-width 5` on the command line, not a profile change. Footprint X 41–167 / Y 67–173 verified inside the mesh |

**Printing is closed as of 2026-09-11**: the organic `Wrist_Roll_Pitch` is usable after
craft-knife clean-up ([print-log](print-log.md)), so every one of the 11 follower parts has a
usable copy — though its supported flat fork face was badly scuffed and needed a lot of
craft-knife work to take a servo ([decisions](decisions.md#supports)). The plate-4 parts
(`Wrist_Roll_Follower`, `Moving_Jaw`) have not been reported as inspected. **Next: assembly, base up, with
every support-cleaned face's fit reported into [print-log.md](print-log.md)** — the fork faces
of `Wrist_Roll_Pitch` against the idler horn in particular, since that is the knife-cleaned
interface.

| `Wrist_Roll_Pitch` flipped | g | Time | Outcome |
|---|---|---|---|
| snug, bed-only (plate 3) | 31.9 | 3 h 30 | fork face in air |
| snug, everywhere (3b) | 39.9 | 4 h 06 | welded |
| **organic, bed-only** | **37.8** | **4 h 21** | **printed 2026-09-09, 4 h 15; usable after craft-knife clean-up** (inspected 2026-09-11) — [print-log](print-log.md), [decisions](decisions.md#supports) |

Per-part figures for what remains, sliced and measured 2026-09-06 with **supports everywhere**,
so these are **upper bounds** for anything sliced `plaplus_soarm`:

| Remaining part | g | Time | Overhang |
|---|---|---|---|
| `Wrist_Roll_Follower` | 46.9 | 4 h 48 | 5.5 % |
| `Moving_Jaw` | 22.2 | 2 h 26 | 14.0 % |

Orientation for both plate-4 parts was screened 2026-09-07 and both stay as extracted — see
[decisions.md](decisions.md#supports). **Before slicing plate 4, run
`tools/orientation-study.py --bands` on both and judge every dropped patch by where it is**, the
check that would have caught `Wrist_Roll_Pitch`. Assembly order from the base up is
`Rotation_Pitch` → `Upper_arm` → `Under_arm` → `Wrist_Roll_Pitch` → `Wrist_Roll_Follower` →
`Moving_Jaw`, which the queue now matches.

Open within it:

- **PLA+ support interface scuffs a flat mating face at a 0.25 mm gap; PETG releases clean at
  the same gap** (2026-09-11, [decisions](decisions.md#supports)). If another PLA+ part needs a
  supported flat face, the untested options are a larger contact gap (0.3–0.35 mm, at the cost
  of a rougher underside) or lowering the interface temperature. Not worth a test print until
  a part needs it.
- **Permanent LED strip before plate 4?** The temporary lamp made overnight camera frames fully
  diagnostic on 2026-09-08 (see [Machine](#machine)), so a night start is watchable with the lamp
  in place; the strip is still the proper fitting.

### The Thing action figure (Thingiverse 917064) — 320 % printed successfully 2026-09-11

Fetched 2026-09-09. Thingiverse blocks unauthenticated downloads (JS shell, API 401, zip link
redirects), so the user downloaded it in a browser; pulled from `ivory` (WSL2 on the Windows
machine) at `/mnt/d/Users/wkenn/Downloads/FANTASTIC 4 THE THING ACTION FIGURE - 917064/`.
**"Fantastic 4 The Thing action figure" by Masterclip, CC BY-SA.** Staged on the Pi as
`~/models/the-thing/The_Thing_001.stl` (md5 `77343ecd…`, binary, 274 386 triangles) with the
README and licence beside it. One STL holding **9 shells already arranged flat on the bed**,
63 × 45 × 28 mm as a plate: legs (28 mm tall), torso (23), two arms, head, a second face, two
3.6 mm pegs and a 5.2 mm ball. Screened with `orientation-study.py`: overhang 2–15 %, dropped
area ≤ 14 mm², bed support ≤ 0.55 cm³ — **support-free as arranged; keep the designer's layout.**

- **Decided 2026-09-09: 200 %, orange PETG, unpainted, `petg_fig`** — see
  [decisions.md](decisions.md#superhero-figures). At 200 % the plate is 127 × 90 mm, so **two
  copies do not fit side by side in the 202 mm mesh**; they would stack in Y with 5 mm to spare,
  which is too tight — **one figure per job**, and the first job validates the profile. Bed contact
  per piece at 100 % is 9–104 mm², ×4 at 200 %; slice with a **4 mm brim** for the heads, pegs
  and ball (5 mm risks neighbouring brims fusing across the gaps between pieces).
- Profiles created 2026-09-09, both untested: `ender5s1_petg_fig.ini` (this print) and
  `ender5s1_plaplus_fig.ini` (for a figure that will be painted). Each is its base profile with
  `layer_height = 0.16` and nothing else.
- **The spool changes to orange PETG for this print.** PETG runs 240/80 with the enclosure as
  it was for PETG before; the PLA+ "open the enclosure" rule does not apply.
- **Sliced 2026-09-09 as `the_thing_200.gcode`** (2.9.6, `petg_fig`, `--scale 200% --brim-width 4
  --center 104,123`, single STL so the designer's layout is kept): **34.6 g, 4 h 54, 351 layers to
  Z 56.2, no support.** Verified in the G-code: `M140`/`M190 S80` before `M104 S240`; layers
  0.24 then 0.16; footprint X 33–173 / Y 71–171 inside the mesh and clear of the purge line.
  **Printed 2026-09-09, came out OK** — [print-log](print-log.md). `petg_fig` has now run once.
- **Decided 2026-09-09: 320 %, with organic support for the arms** ("let's max it out"). The
  designer's layout is 202.6 mm wide at 320 %, fractionally over the mesh and with no room for
  trees, so the nine shells were **re-packed by translation only, every piece in its original
  upright pose**, into `~/models/the-thing/The_Thing_320_plate.stl` (md5 `31a3dad9…`, scaled in
  the file, so slice at 100 %): legs, torso and both arms on one row, head, face, pegs and ball on
  a second, 8 mm gaps. **Plate 168 × 122 mm → X 20–188 / Y 62–184 centred on 104,123.** Pieces at
  320 %: legs 40 × 84 × 90 tall, torso 73 tall, arms 68 long, pegs 11.5, ball 16.8 — big enough
  that no brim is planned. Assembled height ~170–185 mm.
- **Profile `petg_fig_tree`**: `petg_fig` plus the `plaplus_soarm` support block with
  `style = organic`, `buildplate_only = 1`, contact 0.25. **PETG support release at that gap is
  unverified here and PETG supports have welded before** — the arms are the test; the interface
  hangs under the arm from a bed-rooted tree, the case the user expects to release.
- **Sliced 2026-09-10 06:11 UTC: 111.5 g, 12 h 33, 562 layers to Z 90.** Far under the
  volume extrapolation (~140 g / ~20 h) — the 200 % print's brim and fixed overheads do not
  scale. Verified in the G-code: `M140`/`M190 S80` before `M104 S240`; footprint X 12–191 /
  Y 54–190 including skirt and tree bases, inside the mesh; organic support under both arms
  (Z 0–30), under the legs, torso, head and face, all bed-rooted (`buildplate_only = 1`).
- **Printed, successful (user's verdict 2026-09-11)** — first print on `petg_fig_tree`, now
  validated; the PETG organic support under the arms came off clean with no marks. **The orange PETG strung badly
  across the nine pieces**, which is why that spool is now for single-piece plates — see
  [decisions.md](decisions.md#superhero-figures). 12 h 15, 111.5 g — [print-log](print-log.md).
  Open: is 320 % the final scale, and does the figure assemble cleanly (pegs, ball joint)?

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

### Three sliced files still heat the nozzle during the bed soak

Audited 2026-09-06. Still emitting `M104` before `M190`: **`Flexi-Rex-200`,
`Flexi-Rex-improved`, `coupon_ladder`** (`LittleGrassDragon` re-sliced correctly 2026-09-09). Correct already: `3DBenchy`,
`Godzilla`, `Kinetic_Toy`, `first_layer_test`. **Not chronological** — `3DBenchy` predates the
fix but was sliced correctly, so **check the file, not its date**:
`grep -avE '^;|^$' FILE | head -6`. Consequence is a blob of ooze and a dirty nozzle exactly as
the first layer starts, which is self-limiting (the purge line cleans the tip). **Re-slice when
next wanted rather than pre-emptively**; the files are otherwise correct.

### `slice-plate.sh` cannot make a plate — how to fix it

Raised 2026-09-21 by the `--merge` A/B ([decisions.md](decisions.md#slicing)). The script
prefers the flatpak 2.9.6, whose `--merge` always segfaults, and its `| tail -5` pipeline hides
the exit code, so it prints `Done:` with no file. The Debian 2.5.0 `--merge` works, but only if
every STL sits on Z0; the script's header says source coordinates "do not matter", which holds
for XY and is wrong for Z. Undecided between:

- **Force the Debian binary for `--merge`** and drop each input to Z0 first. Keeps one-command
  plates; loses organic support on plates, which only the flatpak has.
- **Drop `--merge`**: pre-merge into one Z0 STL (as `make-riser.py` and the Godzilla plate did)
  and slice with either binary. Keeps organic support; needs an arranging step.

Either way it should fail on a non-zero exit instead of printing `Done:`. Until decided, slice
plates by hand with `/usr/bin/prusa-slicer --merge` on Z0 inputs, as in [AGENTS.md](../AGENTS.md).

## Machine

- **Moonraker briefly stops answering, twice now** — 2026-09-23 ~20:50 BST (just after plate 2
  completed: Moonraker and SSH both hung ~2 min while `tailscale ping` answered) and 2026-09-24
  19:39 BST (an empty reply to a status query ~11 min after plate 7 completed; answered in
  0.24 s moments later). Both recovered unaided, no reboot, low load, no wlan/OOM journal lines
  on the first. Cause unknown. **Consequence for tooling: a start command gated on a status
  query can silently not start** — check for an empty reply and say so rather than `&&`-chain.

- **The camera is off the printer, lent out for SO-ARM101 observations.** It was absent when
  the Pi booted on 2026-09-13 16:28, so crowsnest stopped on "No usable Devices Found" and the
  snapshot URL returns nginx 502. The user plans to refit it on **2026-09-15**. **Until then
  every print is telemetry-only, and the 502 is expected, not a fault to debug.** After it is
  plugged back in, run the reset-and-restart in [hardware.md](hardware.md#host-printhub) and
  confirm a ~200 KB frame, then delete this bullet and restore "active" in hardware.md.
- **Night monitoring needs a light.** With the room dark, an auto-exposure snapshot is
  essentially black (mean 0–2/255) and auto mode caps its own shutter. Forced manual exposure
  rescues it to **gross failure detection only** — enough to confirm nothing has come loose,
  not enough for detail, and at ~0.5 s shutter anything moving smears. The v4l2 settings are in
  [hardware.md](hardware.md). **A cheap USB LED strip on the frame is the real fix** and is a
  prerequisite for treating the camera as useful on any overnight print.
  - **Confirmed by trial, 2026-09-08.** A temporary LED lamp was set up during the plate 3
    print at 05:40, well before sunrise. Snapshots went from the essentially-black frames of
    the night before to **fully diagnostic**: PEI speckle resolves, the bed's "Warning hot
    surface" text is legible, part outlines and corner adhesion are clearly readable — the same
    quality as a daylight frame, with **no night-mode v4l2 settings needed at all**. So the
    fix is genuinely just light; the camera and its auto-exposure are fine.
  - **No flicker banding across two frames three seconds apart**, which is the specific failure
    mode a PWM-dimmed strip would cause against a rolling shutter. One pair is not proof —
    check again on any permanent fitting, and prefer a strip run at constant full output over
    one with an inline dimmer.
  - **This makes overnight prints properly watchable and unblocks the 13 h jobs** that were
    previously "start in daylight or fit the strip first". A permanent frame-mounted strip is
    still the answer; the trial says it will work.
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
  - **Containerising the slicer on printhub — raised 2026-09-23, parked by the owner ("leave
    printhub alone for now").** A container alone does not isolate CPU; only cgroup limits do
    (Docker `--cpuset-cpus`, LXD `limits.cpu`, or with nothing installed
    `systemd-run --scope -p AllowedCPUs=1-3 -p CPUWeight=10 nice -n 19 …` in the slice scripts).
    printhub is Debian 12 arm64 (MainsailOS), cgroup v2 with `cpuset`/`cpu`, no Docker or snap.
    Ubuntu Workshop (Canonical, May 2026; snap on LXD) targets Ubuntu dev workstations — a
    candidate for a pinned-version slicer on `ivory` if that runs Ubuntu (unverified), not for
    printhub. **Rule 1's harm has never been measured**: no print in the log was damaged by
    slicing. The test, if revisited: slice during a print and compare `buffer_time`/`sysload`
    in `klippy.log`'s `Stats` lines against a quiet stretch.
- **Keep the flashing microSD with the printer.** MCU firmware updates still go via SD; see
  [klipper-setup.md](klipper-setup.md#consequence).

## Materials wanted

- **ABS profile** — missing, and a drop-in file.
- **TPU profile** — in progress; see [TPU 95A — profile and calibration](#tpu-95a--profile-and-calibration).
  The 3/4 spool of **red TPU** (hardness unrecorded) was dialled in on a Bowden Ender-3 for
  drone parts; **those settings are gone and would not have transferred anyway** — Bowden
  retraction compensates for tube compliance this direct-drive machine does not have. (This
  loss is what prompted putting these notes under version control.) Re-run the temperature
  tower for it when it is next wanted; the rest of the yellow spool's calibration should carry.
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

### USB over-current dropped the MCU mid-print (2026-09-21) — cause found

**What happened (facts, from `dmesg` and `klippy.log`):** at 20:06:11 and again at 20:06:25
(printhub clock, BST; 19:06 UTC) **every USB port on both xHCI controllers** (`usb1`–`usb4`,
port1 and port2) logged `over-current change` simultaneously. Both attached devices — the CH340
MCU link and the QDtech MPI1001 touchscreen — disconnected and re-enumerated; Klipper logged
`Timeout with MCU 'mcu'` → `Lost communication with MCU 'mcu'` and shut down, killing
`tpu_deck_coupon.gcode` at 71 min. **The first over-current since boot** (2026-09-17 22:48).
`vcgencmd get_throttled` = `0x0`: no undervoltage since boot. `usb_max_current_enable=1`.
Only those two devices were attached; the camera is not connected.

**Cause: the owner plugged a USB LED light into printhub at that moment** to see the print
(owner, 2026-09-21); it has been removed. Its inrush tripped the shared over-current protection
on all ports. **Resolved as a rule** — AGENTS.md rule 6: nothing goes into printhub's USB during a
print. Left here because the signature is worth recognising: every port flagging over-current
simultaneously means one event on the shared supply, not one device's draw. A self-powered hub
between Pi and printer would isolate the MCU from such events; still unverified, under
[The USB constraint](#the-usb-constraint--verified-on-printhub-2026-09-07).

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

**Commissioning 2026-09-24 (owner), for throughput** — "we need throughput!": a second printer
for the ten remaining desk Gridfinity plates. That settles the order: **stock first** (prove
the hardware, print plates on day one, Creality Print as slicer), **helper script next**
(same Moonraker API as the S1, so this repo's tools drive it), **bypass only later if ever**
(printhub USB cabling is barred during S1 prints by AGENTS.md rule 6, plus a from-scratch
config). Day-one checklist:
1. Confirm the model on the box (V3 KE) and the contents against the manual; physical
   inspection before power — build surface present and intact, belts, frame, no shipping damage.
2. Stock first power-up: Creality's self-test / auto-calibration, then its own test print.
3. First plate: `gf_bp_4x4` (Gridfinity Rebuilt thin 4 × 4, no magnets, see
   [decisions.md](decisions.md#desk-gridfinity)) sliced for the KE — **check the footprint
   against its bed mesh** before printing; S1's G-code is not portable (different start macros).
4. Record what was verified here, and move settled facts to decisions.md.
Before any automation: decide the addressing convention (a second Moonraker on 7125).

**Owner, 2026-09-24: assembled, not powered; wants no Creality Cloud, and to drop the Nebula
Pad (bypass route).** Researched the same day — community sources, **nothing verified on this
machine**:
- **Mainboard CR4NS200320C13, GD32F303RET6** (Klipper builds it as STM32F103), **no USB port
  and no SD slot**; the visible USB ports are the Pad's. The Pad talks to it over **UART
  (USART2 PA2/PA3) at 230400 baud** through a **10-pin box header** — pinout per
  [salami738](https://github.com/salami738/ender3-v3-ke-klipper-mainline/blob/main/pinout/creality-mainboard-pinout.md):
  1, 5 GND · 4 PA2 (MCU TX) · 9 PA3 (MCU RX) · **6 +5 V out from the mainboard** · 8, 10 NC ·
  2, 3, 7 uncertain. Logic level 3.3 V implied, unverified. **Wire TX/RX/GND only.**
- **Pi link:** most common is Creality's "Sonic Pad Serial Cable" (USB ID `1a86`, WCH — the
  CH340 family, so **printhub's `by-path` rule applies**), as used by
  [lividhen/Klipper-Ender-3-V3-KE](https://github.com/lividhen/Klipper-Ender-3-V3-KE) (Pi 4,
  MainsailOS). A generic 3.3 V USB-TTL adapter on pins 4/9/GND should work; no KE report found.
  **wk-inventory lists no USB-serial adapter or SWD probe** (stock + purchases, 2026-09-24).
- **Flashing may be unnecessary:** stock MCU firmware was "protocol compatible with the most
  recent build of klipper" as of 2025-01-11 (lividhen) — unverified against today's Klipper;
  a mismatch makes Klipper refuse to connect, which harms nothing. Flashing mainline needs an
  **SWD probe soldered to pads** by the ribbon connector (no SD, no USB), Katapult at 8 KiB
  offset, 8 MHz crystal, USART2, 230400 (**250000 fails**). Katapult overwrites Creality's
  bootloader: **dump the full 512 KB flash first** — the only way back.
- **Config:** none in mainline `config/`. Community: lividhen (Pi host, Kalico fork, 5 stars),
  [salami738](https://github.com/salami738/ender3-v3-ke-klipper-mainline) (mainline on the Pad,
  updated 2026-09). CR Touch = plain `[bltouch]` (PC13/PC14); the "PR-touch" load cell (HX711)
  has partial mainline support. **Accelerometer is read by the Pad**, so dropping it loses input
  shaping calibration unless another accelerometer is added. No toolhead MCU (inferred).
- **Lost with the Pad:** touchscreen, Creality UI, Pad accelerometer, PR-touch Z-offset UX.
  Camera is sold as USB (UVC → Crowsnest); unverified on a Pi.
- **Seen on the machine (owner photo, 2026-09-24):** the Pad carries a keyed, shrouded **10-pin
  (2 × 5) box header** plus a **USB-C port** (purpose unknown); the ribbon to the mainboard has
  an IDC plug with a pin-1 stripe. **The pinout above is the mainboard end** — before wiring
  anything, power on with the Pad unplugged and meter the cable end: pin 6–1 ≈ 5 V, pins 4 and 9
  idle ≈ 3.3 V to GND. That confirms orientation, the 5 V pin and the logic level in one go.
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
- **Gridfinity baseplates are a second case for it** (owner, 2026-09-23). On the nominal
  350 × 350 bed a 7 × 7 plate (294 mm) should fit — **unverified until its mesh bounds are
  known**. The desk's proposed 11 × 16 grid ([Desk Gridfinity](#desk-gridfinity-and-opengrid--all-12-plates-printed-2026-09-25))
  would drop from 12 plates on the S1 to 4 (6+5 × 8+8). Not being commissioned yet.
- **Owner's original plan: convert it to CoreXY** (stated 2026-09-23) — to take the X motor
  off the moving gantry, the same reason the Sovol SV08 is fast
  ([Print speed](#print-speed--how-fast-this-machine-can-go-raised-2026-09-23)). The bed already
  moves only in Z, so the conversion is the belt path and motor mounts, plus `kinematics:
  corexy` in Klipper. **Not scoped:** no kit or design chosen, and the conversion would
  invalidate the stock sample config's XY stepper sections as well as the NG-extruder items
  above. Its gain is acceleration headroom, which pays only once profile speeds are up.
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
