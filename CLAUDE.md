# Working on the printer

## Access

`ssh wkenn@printhub` — Tailscale SSH, tailnet-certificate auth, no password. Passwordless
sudo is enabled. A local `id_ed25519` key is also installed as a LAN break-glass path.
Password authentication is disabled on all paths.

Moonraker's HTTP API on `localhost:7125` is the control surface; drive the printer through it
rather than through KlipperScreen. Examples:

```bash
ssh wkenn@printhub 'curl -s localhost:7125/printer/info'
ssh wkenn@printhub 'curl -s -X POST "localhost:7125/printer/gcode/script?script=G28"'
ssh wkenn@printhub 'curl -s "localhost:7125/printer/objects/query?print_stats&extruder&heater_bed"'
```

## Rules learned the hard way

- **Never both drive the nozzle.** During `PROBE_CALIBRATE`, a KlipperScreen tap and an API
  `TESTZ` collided and aborted the manual-probe session with "Move out of range". One
  operator at a time: the assistant sends commands, the user handles paper/filament only.
- **Z cannot go below 0.** `[stepper_z]` declares no `position_min`, so any move under Z0 is
  rejected. Work the paper test in the 0.0–0.3 mm window.
- **Do not edit `printer.cfg` during a print.** Any config change restarts Klipper and aborts
  the job.
- **Never guess hardware config.** Pins, kinematics, thermistor types and endstops came from
  Klipper's official `printer-creality-ender5-s1-2023.cfg` sample. A wrong value on a machine
  with heaters is a safety problem, not a build error.
- **The user is at the machine and can see it.** Ask what the nozzle/first layer actually did
  rather than inferring from telemetry.

## Conventions

- Slicing is plumbing. "Print X in PETG" should mean: fetch model → `slice-print.sh` →
  start. See [docs/workflow.md](docs/workflow.md).
- PETG 240/80 is the standing default and is baked into `START_PRINT`, so a bare `START_PRINT`
  is always safe.
- After any calibration that Klipper persists, `SAVE_CONFIG` restarts Klipper — wait for
  `state: ready` before the next command.
