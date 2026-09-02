# Reference snapshots

The Pi holds the **authoritative** copies. These are version-controlled snapshots so that a
configuration is never lost the way an earlier machine's dialled-in TPU profile was.

**A stale snapshot is worse than none**, because it will be trusted. On 2026-09-02 this
directory was found to be carrying a `printer.cfg` from before the previous day's `START_PRINT`
change and before the new bed mesh. Refresh before relying on anything here:

```bash
./tools/sync-reference.sh
```

It copies each file down, reports which ones drifted, and leaves the changes staged for review
rather than committing them. Run it after **any** change made on the Pi.

| File | On the Pi |
|---|---|
| `printer.cfg` | `~/printer_data/config/printer.cfg` |
| `ender5s1_petg.ini` | `~/slicer/ender5s1_petg.ini` |
| `ender5s1_pla.ini` | `~/slicer/ender5s1_pla.ini` — untested, see [workflow](../docs/workflow.md) |
| `slice-print.sh` | `~/slicer/slice-print.sh` |
| `crowsnest.conf` | `~/printer_data/config/crowsnest.conf` |

`printer.cfg` includes Klipper's `SAVE_CONFIG` block at the end — PID values, probe `z_offset`
and the saved bed mesh — so a refresh captures calibration state as well as configuration.
