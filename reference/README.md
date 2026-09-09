# Reference snapshots

The Pi holds the **authoritative** copies. These are version-controlled snapshots so that a
configuration is never lost the way an earlier machine's dialled-in TPU profile was.

**A stale snapshot is worse than none**, because it will be trusted. On 2026-09-02 this
directory was found to be carrying a `printer.cfg` from before the previous day's `START_PRINT`
change and before the new bed mesh. Refresh before relying on anything here:

```bash
./tools/sync-reference.sh
```

It copies each file down, reports which ones drifted, and leaves the changes for review
rather than committing them. Run it after **any** change made on the Pi.

**It probes its own transport** (`tailscale ssh`, then plain `ssh`) and, if neither answers,
fails once saying what is missing and writes nothing — rather than reporting every file as
`MISSING on Pi`, which is what the previous version did when `ssh` could not verify the host
key. It also checks each file's byte count, so a short read can never overwrite a good
snapshot with a truncated one.

**Verified in sync with the Pi on 2026-09-07** — all 10 files unchanged.

**Slicer profiles are discovered, not listed** (changed 2026-09-06). The script used to loop
over a hardcoded `petg pla`, which meant `ender5s1_petg_koala.ini` and
`ender5s1_petg_koalacoupon.ini` had never been version-controlled at all — the precise failure
this directory exists to prevent, and worse than the stale-snapshot problem below because there
was nothing to be stale. It now globs `~/slicer/ender5s1_*.ini` on the Pi and skips `*.bak*`, so
a new profile cannot be silently left out.

| File | On the Pi |
|---|---|
| `printer.cfg` | `~/printer_data/config/printer.cfg` |
| `ender5s1_petg.ini` | `~/slicer/ender5s1_petg.ini` |
| `ender5s1_pla.ini` | `~/slicer/ender5s1_pla.ini` — plain PLA, untested, see [workflow](../docs/workflow.md) |
| `ender5s1_plaplus.ini` | `~/slicer/ender5s1_plaplus.ini` — **PLA+ is not PLA**: same profile, 220/215 not 210/205. **Validated 2026-09-06** on `Motor_holder_Base` |
| `ender5s1_plaplus_soarm.ini` | `~/slicer/ender5s1_plaplus_soarm.ini` — plain `plaplus` plus supports (`snug`, `buildplate_only`, contact 0.25). For the **6 SO-ARM101 parts that need support**; the other 5 use plain `plaplus` |
| `ender5s1_plaplus_soarm_all.ini` | `~/slicer/ender5s1_plaplus_soarm_all.ini` — `plaplus_soarm` with `buildplate_only = 0`, nothing else changed. For a part whose overhang sits **above the part**, which `buildplate_only` drops so the face prints into air (`Wrist_Roll_Pitch`, 2026-09-08). Brings support back inside horizontal bores, so not the default. See [decisions](../docs/decisions.md#supports) |
| `ender5s1_plaplus_fig.ini` | `~/slicer/ender5s1_plaplus_fig.ini` — `plaplus` with `layer_height = 0.16`, nothing else. Figurines to be painted; **untested** |
| `ender5s1_petg_fig.ini` | `~/slicer/ender5s1_petg_fig.ini` — `petg` with `layer_height = 0.16`, nothing else. Figurines in their final colour, unpainted; **untested** |
| `ender5s1_petg_fig_tree.ini` | `~/slicer/ender5s1_petg_fig_tree.ini` — `petg_fig` plus the `plaplus_soarm` support block with `style = organic` (needs PrusaSlicer ≥ 2.6). **Untested** |
| `ender5s1_petg_koala.ini` | `~/slicer/ender5s1_petg_koala.ini` — project profile, not the koala-bot spec |
| `ender5s1_petg_koalacoupon.ini` | `~/slicer/ender5s1_petg_koalacoupon.ini` — as above |
| `slice-print.sh` | `~/slicer/slice-print.sh` — one model |
| `slice-plate.sh` | `~/slicer/slice-plate.sh` — several models on one plate, centred on the measured mesh rather than the bed |
| `crowsnest.conf` | `~/printer_data/config/crowsnest.conf` |

`printer.cfg` includes Klipper's `SAVE_CONFIG` block at the end — PID values, probe `z_offset`
and the saved bed mesh — so a refresh captures calibration state as well as configuration.
