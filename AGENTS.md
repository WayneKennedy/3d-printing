# Driving the printer

Onboarding for any AI harness working this machine. **If you read one file before touching the
printer, read this one.** It is the contract other repos consume; everything here is either a
safety rule or the minimum needed to slice and start a job correctly. Detail lives in `docs/`
and is linked rather than repeated.

The machine is a **Creality Ender-5 S1**, stock, running **Klipper** on `printhub` (Raspberry
Pi 5, MainsailOS). Full identifiers: [docs/hardware.md](docs/hardware.md).

## Access — no SSH needed

Moonraker's HTTP API is the control surface. `trusted_clients` covers the tailnet
(`100.64.0.0/10`), so **the workstation reaches it directly, with no API key and no SSH hop**:

```bash
curl -s "http://100.99.147.57:7125/printer/info"
curl -s "http://100.99.147.57:7125/printer/objects/query?print_stats&virtual_sdcard&extruder&heater_bed"
curl -s -X POST "http://100.99.147.57:7125/printer/gcode/script?script=G28"
curl -s "http://100.99.147.57/webcam/?action=snapshot" > snap.jpg
```

Shell access, when you genuinely need the Pi itself (slicing, file inspection):

```bash
tailscale ssh wkenn@printhub '<command>'
```

**Prefer `tailscale ssh` over plain `ssh`.** Tailscale SSH verifies the host key through the
tailnet CA; plain `ssh` fails with `Host key verification failed` on a workstation that has no
`known_hosts` entry, and there is no TTY to accept one. Passwordless sudo is enabled.

**The camera is on port 80 via nginx, not 8080.** 8080 is bound to localhost on the Pi and does
not answer over the tailnet. The trailing slash is load-bearing — `/webcam?action=snapshot`
301s and drops the query string.

## Rules that will cost you a print if broken

1. **Never slice while a print is running.** PrusaSlicer saturates the Pi's cores and Klipper's
   timing is what suffers. This is not currently enforced by anything but attention — check
   `print_stats.state` before invoking any slicer on the Pi.
2. **Never edit `printer.cfg` during a print.** Any config change restarts Klipper and aborts
   the job. `SAVE_CONFIG` also restarts it — wait for `state: ready` before the next command.
3. **Never guess hardware config.** Pins, kinematics, thermistors and endstops came from
   Klipper's official `printer-creality-ender5-s1-2023.cfg` sample. A wrong value on a machine
   with heaters is a safety problem, not a build error.
4. **One operator at a time.** During `PROBE_CALIBRATE`, a KlipperScreen tap and an API `TESTZ`
   collided and killed the manual-probe session with "Move out of range". The assistant sends
   commands; the user handles paper and filament only.
5. **Z cannot go below 0.** `[stepper_z]` declares no `position_min`, so any move under Z0 is
   rejected. Work the paper test in the 0.0–0.3 mm window.
6. **The user is at the machine and can see it.** Ask what the nozzle or first layer actually
   did rather than inferring it from telemetry.

## Slicing and printing

Slicing is plumbing: "print X in PETG" should mean fetch model → slice → start.

```bash
tailscale ssh wkenn@printhub '~/slicer/slice-print.sh <model.stl|.3mf> [material] [--print]'
tailscale ssh wkenn@printhub '~/slicer/slice-plate.sh <output-name> <material> <model.stl>...'
```

`slice-print.sh` handles one model; `slice-plate.sh` arranges several onto one plate. Both
write G-code into `~/printer_data/gcodes/`, where Mainsail lists it. `<material>` resolves
`~/slicer/ender5s1_<material>.ini`.

| Material | Profile | Status |
|---|---|---|
| `petg` | 240/80, 0.2 mm, 3 perim, 15 % grid | **canonical**, general use |
| `plaplus` | 220/215, bed 60, 100 % fan | **validated** 2026-09-06 |
| `plaplus_soarm` | `plaplus` + snug build-plate-only supports | validated, support-needing parts |
| `pla` | 210/205, bed 60 | **untested — no plain PLA has been printed** |
| `petg_koala`, `petg_koalacoupon` | 4 perim, 30 % gyroid | built for a superseded spec; **not** the koala-bot standard |

**A bare `START_PRINT` is always safe** — it defaults to PETG 240/80. It homes on its own, so an
un-homed machine needs no action first.

### Traps that have each cost a real print

- **The literal `M104`/`M190` tokens in `start_gcode` are load-bearing.** PrusaSlicer injects
  its own `M104` *ahead of the custom block* unless it finds those tokens literally inside it.
  Removing `M104` on the reasoning that `START_PRINT` handles heating defeated the bed-first
  fix entirely and went unnoticed for a day. **Verify by inspecting emitted G-code, never by
  reading the profile**: `grep -avE '^;|^$' FILE | head -6`.
- **The usable area is the mesh, not the bed.** Bed is 220 × 220, but the saved mesh covers
  **X3–205, Y28–218** and outside it Klipper extrapolates, which is where first-layer adhesion
  turns unreliable. `slice-plate.sh` centres on `104,123` for this reason. **Verify the emitted
  footprint against the mesh bounds before printing.**
- **`START_PRINT`'s purge line runs at Y8, X15→X205.** Anything placed there gets a prime line
  drawn through it.
- **`prusa-slicer --merge` is unreliable** — it has thrown "Objects could not fit on the bed"
  for two small parts, and spilled a 7-part plate from X −42 to 250. Translate parts into
  position and merge to one STL, or keep plates to a modest fill and check the footprint.
- **PLA+ is not PLA.** Same base resin plus impact modifiers: tougher, better layer adhesion,
  but glass transition is unchanged at ~55–60 °C, so it buys **no extra heat resistance**.
  It runs hotter (210–230 °C). Slicing it at plain-PLA temperatures under-fuses it.
- **Open the enclosure for PLA and PLA+.** Enclosures are for ABS/ASA; a warm chamber causes
  heat creep in this direct-drive hotend and undermines the 100 % part cooling these profiles
  specify. Front and top are left open by default.
- **PrusaSlicer on the Pi is 2.5.0** — no tree/organic supports (those arrived in 2.6). `snug`
  is the closest this version offers.

Full detail, with the measurements behind each: [docs/workflow.md](docs/workflow.md).

## Watching a running print

```bash
tools/print-monitor.py            # polls Moonraker; emits on every terminal state
```

It emits on `complete`/`error`/`cancelled`/`paused`, on Klippy leaving `ready`, on temperature
drift and on the API going unreachable, then exits. **A monitor that greps only for success is
silent through a crash, which is indistinguishable from "still running"** — hence the explicit
failure coverage.

The camera is **blind after dark**; night-mode exposure gets gross failure detection only. See
[docs/hardware.md](docs/hardware.md) for the v4l2 settings and the fixed-focus constraint.

## Aborting

**`CANCEL_PRINT` does not work during the heat-soak.** It queues behind `M190`, so a cancel
sent while the bed is climbing does not run until the bed reaches target — and Moonraker flips
the job to `paused` immediately, which makes it look like the cancel landed when it has not.

The certain fast abort is emergency stop:

```bash
curl -s -X POST "http://100.99.147.57:7125/printer/emergency_stop"
curl -s -X POST "http://100.99.147.57:7125/printer/firmware_restart"   # when you want it back
```

Cutting mains power to the printer is also safe and leaves no mess — the MCU disappears and
Klipper shuts down cleanly; the Pi is unaffected.

**There is no `CANCEL_PRINT` macro in `printer.cfg`.** Moonraker's cancel zeroes the heaters but
leaves the nozzle parked on the part at temperature. See
[docs/open-questions.md](docs/open-questions.md).

## Where things live

| File | Contents |
|---|---|
| [docs/hardware.md](docs/hardware.md) | Printer, Pi, camera, network — verified identifiers |
| [docs/calibration.md](docs/calibration.md) | Current calibration values and how to redo them |
| [docs/workflow.md](docs/workflow.md) | Model → G-code → print, in full |
| [docs/klipper-setup.md](docs/klipper-setup.md) | How Klipper was flashed; the flashing gotchas |
| [docs/print-log.md](docs/print-log.md) | What has been printed, with outcomes |
| [docs/decisions.md](docs/decisions.md) | Settled decisions and why — **do not re-litigate** |
| [docs/open-questions.md](docs/open-questions.md) | Genuinely undecided, and active work |
| `reference/` | Snapshots of the live files on the Pi |
| `tools/` | `print-monitor.py`, `sync-reference.sh`, `extract-soarm-parts.py` |

**The Pi holds the authoritative copies; `reference/` is a version-controlled cache.** Refresh
with `./tools/sync-reference.sh` before trusting anything in it, and after any change made on
the Pi. A stale snapshot is worse than none, because it will be trusted.

**Distinguish decided from open.** `decisions.md` records conclusions with the evidence that
produced them, including conclusions that were reached, tested and found wrong — those
corrections are kept deliberately so the next agent does not re-derive a known-wrong answer.
Never state an open question as settled.
