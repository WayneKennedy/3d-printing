# Calibration

All values below are live in the `SAVE_CONFIG` block of `printer.cfg`. PID and Z-offset date
from 2026-09-01 and were validated by a clean first-layer test square, a clean Benchy and an
8 h dragon print; the mesh and tram figures were re-measured after the garage move on
2026-09-06.

| Item | Value | Notes |
|---|---|---|
| Hotend PID | `Kp=20.623 Ki=1.136 Kd=93.577` | tuned at 210 °C; **re-verified in the garage 2026-09-06** — see below |
| Bed PID | `Kp=51.668 Ki=0.398 Kd=1677.907` | tuned at 60 °C; very long period (`Tu≈260 s`), the tune takes 15+ min — it is slow, not stuck |
| Probe Z-offset | `1.776` | set at 240 °C with white PETG loaded; chosen between "smoosh" (0.183) and free (0.233) |
| Bed mesh `default` | 4 × 4, range **0.281 mm** | re-probed at 80 °C after the garage move, 2026-09-06; same gentle bowl, no tilt |
| Bed tram | FL base / FR 0.059 / RL 0.036 / RR 0.014 mm | 2026-09-06, all four within `00:05`; chasing the last corner just rocks the others |
| Probe repeatability | **≤ 0.0025 mm** | 2026-09-06, quantisation-limited — see below |

## Procedure

Run in this order; each of PID, Z-offset and mesh needs `SAVE_CONFIG` after, which restarts
Klipper.

```
PID_CALIBRATE HEATER=extruder TARGET=210      → SAVE_CONFIG
PID_CALIBRATE HEATER=heater_bed TARGET=60     → SAVE_CONFIG
SCREWS_TILT_CALCULATE                          → adjust knobs → repeat until all ≤ 00:05
PROBE_CALIBRATE                                → paper drag → ACCEPT → SAVE_CONFIG
BED_MESH_CALIBRATE                             → SAVE_CONFIG
```

### Reading `SCREWS_TILT_CALCULATE`

Clock notation out of one full turn: `00:26` ≈ 26/60 of a turn, `01:20` = one turn plus 20
minutes. **CW as viewed from above raises that corner** (verified empirically — every screw's
number shrank toward `00:00`). If a re-probe shows a number *grew*, that screw went the wrong
way. Within `00:05` is dialled in.

The four screws interact: adjusting one pivots the plate and can push another out. Stop once
all four are close rather than chasing perfection.

### Z-offset by paper drag

`PROBE_CALIBRATE` opens a manual-adjust panel. One operator only — the assistant drives
`TESTZ`, the user handles the paper. Z cannot go below 0, so work in the 0.0–0.3 mm window.
Target is light, consistent drag: the paper slides with resistance and goes back in without a
fight. Doing it hot (240 °C, filament loaded, nozzle wiped clean) is the accurate way.

If the CR-Touch throws `BLTouch failed to deploy`, run `BLTOUCH_DEBUG COMMAND=reset` then
`BLTOUCH_DEBUG COMMAND=self_test`; `QUERY_PROBE` should then report `probe: open`.

Small first-layer corrections do not need this whole dance — babystep Z live during a print
and save the offset.

## After the move to the garage

The printer moved to the garage on **2026-09-06**. The procedure, for this move and any future
one:

1. `SCREWS_TILT_CALCULATE` → adjust → repeat
2. `BED_MESH_CALIBRATE` → `SAVE_CONFIG`
3. Print `first_layer_test.gcode` and look at it. Babystep only if it actually looks wrong.

Do it **at operating temperature**, in place. PID values carry over fine; the mesh and tram are
location- and temperature-sensitive, and moving the machine shifts bed geometry.

### What the 2026-09-06 move actually changed: almost nothing

**Ambient at the time: ~25 °C** (bed at rest read 25.2 °C and drifting down before anything was
heated, on a September morning). Every figure below belongs to those conditions — the garage
swings widely, so record this alongside any future re-measurement.

The machine travelled far better than the procedure assumes. Only the mesh needed rewriting.

- **Tram survived untouched.** `SCREWS_TILT_CALCULATE` came back FR `00:05`, RL `00:03`,
  RR `00:01` — all already inside the `00:05` threshold, spanning 0.059 mm corner to corner,
  and within a few hundredths of the pre-move figures. **No knob was turned.** Turning FR for a
  20 µm gain would only have rocked the other three.
- **Mesh shifted slightly and was re-saved.** Range 0.246 → 0.281 mm, same bowl, same high
  rear-left corner; the largest single point moved 0.054 mm. Worth re-probing, but the bed was
  neither warped nor tilted by the move.
- **`z_offset` was not touched**, per the reasoning below. It remains 1.776, and the first
  layer after the move went down clean with **no babystep needed** — so leaving it alone was
  right, and the toolhead-geometry argument now has a relocation to its name.
- **A brand-new red PETG spool went on at the same time** and printed clean at the standing
  240/80 with no adjustment. Changing filament colour and spool did not require a temperature
  or offset change.

### Verify PID rather than re-tuning it (2026-09-06)

The claim that "PID values carry over" was a prediction until this move. It is now measured, and
the check is nearly free because the machine has to sit at operating temperature for the tram
and mesh anyway. Hold 240/80 and log temperature and duty cycle for ~10 min:

| | Overshoot | Settled | Duty at hold |
|---|---|---|---|
| Hotend | +0.90 °C | 240.0 ± 0.12 °C | 0.48 |
| Bed | +1.24 °C | 80.0 ± 0.02 °C | **0.34** |

Both settled monotonically with no oscillation. **Distinguishing a settling transient from slow
hunting needs about two full periods** — the bed's `Tu≈260 s` means a 10 min window, and
counting mean-crossings is the test: 2 crossings is one overshoot-and-settle, whereas real
hunting would have given ~9 regular ones.

**The duty cycle is the number that answers the cold-garage question.** The bed holds 80 °C on
34 % power, so two-thirds of the heater is in reserve — a cold night has a lot of margin to eat
before the bed cannot hold target. Re-tune only if that duty climbs near saturation or the
trace starts oscillating; a re-tune costs 20+ min and the bed tune alone is 15+.

### Check the probe before trusting a mesh

A relocation is exactly the event that could knock the probe, so verify it before it is used for
16 mesh points. `BLTOUCH_DEBUG COMMAND=self_test` then `QUERY_PROBE` should give `probe: open`.

`PROBE_ACCURACY` is the sharper test, with one trap: on 2026-09-06 it returned **range
0.000000, stdev 0.000000** over 12 samples, which looks like a stuck reading rather than a good
one. It is not. Z resolution here is `rotation_distance 8 / (200 × 16 microsteps)` =
**0.0025 mm/step**, and a second run at a different point alternated between two values exactly
one step apart. **The probe repeats to better than one Z microstep, so quantisation, not the
probe, sets the noise floor.** If a single point ever reads a perfect zero range again, confirm
it by probing a *second* location rather than assuming a fault.

**`PROBE_CALIBRATE` is deliberately not on that list.** `z_offset` is nozzle-to-trigger geometry
*inside the toolhead*: the probe pin protrudes a fixed distance and triggers after a fixed
travel, so anything that raises or lowers the bed surface raises or lowers probe and nozzle
together and the offset is unchanged. Moving the machine does not reach inside the toolhead.
Confirmed empirically twice. On 2026-09-02, fitting the PEI plate added ~0.6 mm of surface and
1.776 was still correct, verified by first-layer test. **Confirmed again on 2026-09-06 across
the garage move itself** — the machine was relocated, re-trammed and re-meshed, `z_offset` was
deliberately left alone, and the first layer of the dragon laid down clean with no babystep.
That second case is the stronger one, because relocation is precisely the event the argument
claims is harmless. Re-run `PROBE_CALIBRATE` only if something
actually changed that geometry: the probe was removed or knocked, the hotend or nozzle was
swapped, or the first-layer test looks wrong in a way babystep cannot explain.
