# Reference snapshots

Copied from `printhub` on **2026-09-01**. Read-only reference — the Pi holds the
authoritative copies. To refresh:

```bash
scp wkenn@printhub:printer_data/config/printer.cfg reference/printer.cfg
scp wkenn@printhub:slicer/ender5s1_petg.ini      reference/ender5s1_petg.ini
scp wkenn@printhub:slicer/slice-print.sh         reference/slice-print.sh
```

| File | On the Pi |
|---|---|
| `printer.cfg` | `~/printer_data/config/printer.cfg` |
| `ender5s1_petg.ini` | `~/slicer/ender5s1_petg.ini` |
| `slice-print.sh` | `~/slicer/slice-print.sh` |
