# 3D Printing

Context store for the Creality Ender-5 S1 running Klipper on the `printhub` Raspberry Pi.

The printer was commissioned 2026-08-28 → 2026-08-31 (stock Marlin → Klipper, full
calibration, first prints). That work happened in a session under `~/Code/codename-talis`;
this folder is its permanent home.

## Quick reference

| Thing | Value |
|---|---|
| Printer | Creality Ender-5 S1, stock (no mods) |
| Host | `printhub` — Raspberry Pi 5 (8 GB, NVMe), Debian 12, MainsailOS stack |
| Mainsail UI | http://100.99.147.57 (tailnet) · http://printhub |
| Moonraker API | port `7125` |
| SSH | `tailscale ssh wkenn@printhub` (Tailscale SSH; password auth disabled) |
| Default filament | White PETG — 240 °C nozzle / 80 °C bed |
| Slice + print | `tailscale ssh wkenn@printhub '~/slicer/slice-print.sh <model> petg [--print]'` |

## Documents

| File | Contents |
|---|---|
| [AGENTS.md](AGENTS.md) | **Start here.** How to drive the machine safely — access, rules, slicing, monitoring |
| [CLAUDE.md](CLAUDE.md) | Imports `AGENTS.md`; Claude-specific notes only |
| [docs/hardware.md](docs/hardware.md) | Printer, mainboard, Pi, network — verified identifiers |
| [docs/klipper-setup.md](docs/klipper-setup.md) | How Klipper was flashed and configured; the flashing gotchas |
| [docs/calibration.md](docs/calibration.md) | Current calibration values and how to redo them |
| [docs/workflow.md](docs/workflow.md) | Model → G-code → print, on the Pi and in OrcaSlicer |
| [docs/print-log.md](docs/print-log.md) | What has been printed, with outcomes |
| [docs/decisions.md](docs/decisions.md) | Settled decisions and why — do not re-litigate |
| [docs/open-questions.md](docs/open-questions.md) | Genuinely undecided, and work in progress |
| `reference/` | Snapshots of the live files on the Pi — refresh with `tools/sync-reference.sh` |

`reference/` is a snapshot for reading, not a deployment source. The Pi holds the
authoritative copies; re-snapshot rather than push.
