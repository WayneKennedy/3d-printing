# Calibration

All values below are live in the `SAVE_CONFIG` block of `printer.cfg` as of 2026-09-01, and
were validated by a clean first-layer test square, a clean Benchy, and an 8 h dragon print.

| Item | Value | Notes |
|---|---|---|
| Hotend PID | `Kp=20.623 Ki=1.136 Kd=93.577` | tuned at 210 °C |
| Bed PID | `Kp=51.668 Ki=0.398 Kd=1677.907` | tuned at 60 °C; very long period (`Tu≈260 s`), the tune takes 15+ min — it is slow, not stuck |
| Probe Z-offset | `1.776` | set at 240 °C with white PETG loaded; chosen between "smoosh" (0.183) and free (0.233) |
| Bed mesh `default` | 4 × 4, range **0.246 mm** | after tramming; gentle bowl/curvature, no tilt |
| Bed tram | FL base / FR ≈0.07 / RR ≈0.01 / RL 0.00 mm | good enough — chasing the last corner just rocks the others |

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

The printer is destined for the garage. When it relocates:

1. `SCREWS_TILT_CALCULATE` → adjust → repeat
2. `BED_MESH_CALIBRATE` → `SAVE_CONFIG`
3. Print `first_layer_test.gcode` and look at it. Babystep only if it actually looks wrong.

Do it **at operating temperature**, in place. PID values carry over fine; the mesh and tram are
location- and temperature-sensitive, and moving the machine shifts bed geometry.

**`PROBE_CALIBRATE` is deliberately not on that list.** `z_offset` is nozzle-to-trigger geometry
*inside the toolhead*: the probe pin protrudes a fixed distance and triggers after a fixed
travel, so anything that raises or lowers the bed surface raises or lowers probe and nozzle
together and the offset is unchanged. Moving the machine does not reach inside the toolhead.
Confirmed empirically on 2026-09-02 — fitting the PEI plate added ~0.6 mm of surface and 1.776
was still correct, verified by first-layer test. Re-run `PROBE_CALIBRATE` only if something
actually changed that geometry: the probe was removed or knocked, the hotend or nozzle was
swapped, or the first-layer test looks wrong in a way babystep cannot explain.
