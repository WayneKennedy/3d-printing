# Print workflow

The goal is that slicing is invisible plumbing: hand over a model and a material, get a
print. Mainsail is the UI, not a slicer; the Pi has no slicer GUI.

## Primary path — slice on the Pi

```bash
ssh wkenn@printhub '~/slicer/slice-print.sh <model.stl|.3mf> petg [--print]'
```

It slices with the fixed profile `~/slicer/ender5s1_petg.ini`, writes G-code straight into
`~/printer_data/gcodes/` (where Mainsail lists it), and with `--print` starts the job via
Moonraker. Adding another material is a matter of dropping in `ender5s1_<mat>.ini`; only
`petg` exists today.

Snapshots: [`../reference/slice-print.sh`](../reference/slice-print.sh),
[`../reference/ender5s1_petg.ini`](../reference/ender5s1_petg.ini).

### Profile essentials

PETG 240/80, 0.2 mm layers (0.24 first), 3 perimeters, 15 % grid infill, fan off for 3 layers
then 40–50 %, first layer 20 mm/s. Relative extrusion with a per-layer `G92 E0` — PrusaSlicer
requires that and will produce broken G-code without it.

**Heating order:** bed first, hotend last. `start_gcode` is:

```
M140 S[first_layer_bed_temperature]
M190 S[first_layer_bed_temperature]
M104 S[first_layer_temperature]
START_PRINT EXTRUDER_TEMP=[first_layer_temperature] BED_TEMP=[first_layer_bed_temperature]
```

Bed-first since 2026-09-01: heating in parallel got the hotend to 240 °C about two minutes
early and it oozed while waiting for the bed, and the wipe passes were not clearing it. Costs
~1.5 min per print.

**The literal `M104`/`M190` tokens are load-bearing — do not remove them.** PrusaSlicer emits
its *own* `M104` before the custom start G-code and `M109` after it, and suppresses them only
when it finds those tokens literally in the custom block. A first attempt on 2026-09-01 removed
`M104` from `start_gcode` on the reasoning that `START_PRINT` handles heating — which caused
PrusaSlicer to inject `M104 S240` **ahead of everything**, defeating the fix entirely. That went
unnoticed until 2026-09-02, when slicing Godzilla exposed it. Verified fixed by inspecting the
emitted block, not by reading the profile:

```bash
sed -n '1,25p' out.gcode | grep -E '^M1[0459]|^START_PRINT'
```

Anything sliced between 2026-09-01 18:11 and 2026-09-02 22:06 still heats hotend-first.
**Re-slice rather than trust a file from that window.**

### Aborting during the heat-soak

`CANCEL_PRINT` goes into the same G-code queue as `M190`, so a cancel sent while the bed is
still climbing does not run until the bed reaches target. Moonraker flips the job to `paused`
straight away, which makes it look like the cancel landed when it has not — on 2026-09-03 a
cancel sat behind `M190 S80` with the bed at 68 °C and nothing happened.

The certain fast abort is `M112` (emergency stop). It requires a `FIRMWARE_RESTART` afterwards,
which is no worse than the power cycle you would otherwise reach for.

```bash
ssh wkenn@printhub 'curl -s -X POST "localhost:7125/printer/emergency_stop"'
# then, once you want it back:
ssh wkenn@printhub 'curl -s -X POST "localhost:7125/printer/firmware_restart"'
```

Setting the bed target to 0 first *should* release the `M190` and let a normal cancel through —
Klipper accepts commands from other sources during a temperature wait — but this has **not been
tested on this machine.** Do not reach for it in a hurry.

Cutting mains power to the printer is also safe and leaves no mess: the MCU disappears, Klipper
logs `Lost communication with MCU` and shuts down, and the Pi is unaffected. The give-away in
`dmesg` is `ch341-uart ttyUSB0: converter now disconnected`, which distinguishes a deliberate
power-off from a genuine USB fault.

**Retraction:** 0.8 mm at 40 mm/s with 0.2 mm lift — short, because the extruder is direct
drive, not Bowden. The amount was never the problem; what mattered was that it was not firing.
Four settings were absent from the `.ini`, so PrusaSlicer's defaults applied silently, and two
of them were wrong for this machine. Corrected 2026-09-02:

| Setting | Was (default) | Now | Why |
|---|---|---|---|
| `retract_before_travel` | 2 mm | **1 mm** | Travels under the threshold get no retraction at all. On print-in-place models most hops between adjacent segments are under 2 mm, so the moves most likely to drop ooze on small parts were the ones skipping retraction. |
| `retract_layer_change` | 0 | **1** | Z-hop happened without retracting — a blob at every layer change. |
| `wipe` | 0 | **1** | Nozzle now drags along the last path while retracting, clearing the melt. |
| `only_retract_when_crossing_perimeters` | 0 | 0 | Already correct; 1 would suppress retracts inside the part. |

`retract_length` was deliberately **left at 0.8 mm**. Longer retracts on PETG pull molten
filament up into the heatbreak, trading stringing for jamming, and more retract events at
greater length is how filament grinding starts. Raise it only if stringing survives the fixes
above.

### Model sources

**As of 2026-09-02, no model source can be fetched automatically. The user must download in
a browser and hand the file over.** Verified that day:

| Source | Result |
|---|---|
| Thingiverse `/thing:<id>/zip` | **HTTP 200 but returns the Next.js app shell, not a zip.** Tried with a full browser header set (UA, Accept, Accept-Language, Referer, Sec-Fetch-*). One id also returned 504. |
| Printables | 403 to WebFetch |
| MakerWorld | 403 even with a browser UA from the Pi; also needs a login |
| MyMiniFactory | 403 even with a browser UA from the Pi |
| Cults3D | **Page fetches fine** with a browser UA (useful for checking price and licence), but downloads need a login, and much of its catalogue is paid |

**This is a regression, not a standing limitation.** The browser-User-Agent workaround below did
work on 2026-09-01 — `~/models/hinge.zip` (454 KB) came down that way — so Thingiverse tightened
something in between. Retry it before assuming it is permanently dead:

```bash
curl -sL -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
  (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36" \
  -o model.zip "https://www.thingiverse.com/thing:<id>/zip"
```

**Always check what you got** — the challenge or shell page is HTML wearing a `.zip` name, and
`file model.zip` will say so. A silent HTML download is the failure mode to watch for.

**GitHub-hosted models need none of this and are worth preferring**; DrLex's Flexi Rex is one
such, and is why that print worked first time as a fetch.

## Secondary path — OrcaSlicer on the desktop

Kept for when a print needs actual tuning; not needed for routine work.

| Setting | Value |
|---|---|
| Printer | Creality Ender-5 S1, or Generic Klipper Printer |
| Build volume | 220 × 220 × 280, origin front-left |
| Nozzle / drive | 0.4 mm, direct drive |
| G-code flavour | Klipper |
| Retraction | ~0.8 mm |
| Machine start G-code | `START_PRINT` (replace any inline block entirely) |
| Machine end G-code | `END_PRINT` |
| Host type | Klipper / Moonraker |
| Hostname | `http://100.99.147.57` |
| Port | `7125` |
| API key | blank |
| Device UI | `http://100.99.147.57` |

"Generic Klipper Printer" is a fine choice — it only sets the G-code flavour; Klipper itself
runs on the Pi. Moonraker's `trusted_clients` already includes `100.64.0.0/10`, so the tailnet
address works with no API key, from the desk or the garage. Use the tailnet address rather
than a LAN IP for exactly that reason.

Sanity check after slicing: in preview, the model should sit centred and the first move should
be the prime line along the front edge.

## Project-specific profiles

`slice-print.sh <model> <mat>` resolves `~/slicer/ender5s1_<mat>.ini`, so a project profile is
just another `<mat>` string.

| Profile (`<mat>`) | Layers | Perimeters | Infill | Status |
|---|---|---|---|---|
| `petg` | 0.2 | 3 | 15 % grid | **canonical** — general use *and* koala-bot |
| `petg_koala` | 0.2 | 4 | 30 % gyroid | built 2026-09-01 against a superseded spec; unused |
| `petg_koalacoupon` | 0.15 | 4 | 30 % gyroid | as above; unused |
| `pla` | 0.2 | 3 | 15 % grid | **UNTESTED** — built 2026-09-02, no PLA has been printed yet |

### `pla` — built 2026-09-02, untested

Derived from `ender5s1_petg.ini` by changing **only** material-specific values, so that if a
PLA print misbehaves the material is the only variable: temps 210/205 (first/other), bed 60,
fan 100 % from layer 2 (PETG runs 40-50 % from layer 4), `filament_density = 1.24`. Layer
heights, speeds, perimeters, infill and retraction are byte-identical to the PETG profile.

- **The temperatures are generic starting points, not measured.** Override with the spool's own
  stated range. A temperature tower is the proper answer and is backlogged for both materials.

### `ender5s1_plaplus.ini` — PLA+ is not PLA

Added 2026-09-06 for a white **eSUN PLA+** spool. Derived from `ender5s1_pla.ini` changing
**only** the two temperatures, so the material-is-the-only-variable discipline still holds:

| | plain PLA | PLA+ |
|---|---|---|
| `first_layer_temperature` | 210 | **220** |
| `temperature` | 205 | **215** |

PLA+ is a PLA base resin with impact modifiers. It is **tougher with better layer adhesion**
than plain PLA, but its glass transition is essentially unchanged at ~55-60 °C, so **it buys no
extra heat resistance** — the most common misconception about it, and the one that matters in a
greenhouse garage. It also runs hotter: eSUN's datasheet range is **210-230 °C nozzle, 45-60 °C
bed**. Slicing PLA+ at plain-PLA temperatures under-fuses it and discards exactly the layer
adhesion the "+" is sold for. Most PLA+ brands share that range, but check the label if the
brand changes.

**Open the enclosure when printing PLA+.** The printer is inside a Creality PVC enclosure whose
front and top are left open by default (see [hardware.md](hardware.md#location)). Enclosures are
for ABS/ASA; PLA and PLA+ are the materials harmed by them — a warm chamber causes heat creep in
this direct-drive hotend and undermines the 100 % part cooling the profile specifies. In a
greenhouse garage on a sunny day the chamber can be well above room temperature.

Invoke as `slice-print.sh model.stl plaplus`.

**Validated 2026-09-06** on the SO-ARM101 `Motor_holder_Base`, the first PLA of any kind
printed on this machine. 220/215 at 60 C bed laid down clean with no babystep. No Benchy was
needed in the end: a real part that is wanted anyway is a better first print than a throwaway,
because a bad result costs nothing extra and a good one is a part in hand.
- **No PLA has been printed on this machine.** Put a Benchy through this profile before
  committing anything that matters to it.
- **The saved bed mesh was probed at 80 C and `START_PRINT` hardcodes `BED_MESH_PROFILE
  LOAD=default`.** A 60 C PLA print therefore loads the 80 C bed shape. The difference is
  second-order (bed bowing between 60 and 80 C is typically a few hundredths of a millimetre,
  comparable to the mesh's own spread) but it is cheap to fix properly: probe a second profile
  at 60 C with `BED_MESH_CALIBRATE PROFILE=pla60`, parameterise `START_PRINT` as
  `BED_MESH_PROFILE LOAD={params.MESH|default('default')}`, and add `MESH=pla60` to the PLA
  profile's `start_gcode`. A bare `START_PRINT` then still means PETG 240/80 on the default
  mesh, so it stays safe. **Requires editing `printer.cfg`, so not during a print.**

  **Measured 2026-09-06: not needed.** The first PLA+ print ran a 60 C bed on the 80 C-probed
  `default` mesh and the first layer was clean with no babystep. The effect really is
  second-order, so **do not build `pla60` speculatively** - the parameterisation above is
  written down and stays available if a PLA first layer ever actually misbehaves.

**Check a project's own spec before slicing, and check it is current.** koala-bot's
`docs/bom.md` briefly specified 4 perimeters / 30 % gyroid, and the two `petg_koala*` profiles
were built for it; that section was rewritten hours later to document the generic `petg`
profile instead. Both koala profiles are kept but are **not** the spec — do not use them
without checking `docs/bom.md` again.

Note the direction of causation there: koala-bot's BOM now documents whatever profile happened
to be on the Pi as the project standard. It reads as a specification but is an observation, and
its own text flags 4–5 perimeters for load-bearing parts as an untested open point.

### koala-bot's `slice_remote.py` — safe, with one caveat

`hardware/src/koala_hardware/slice_remote.py` copies every STL to `/tmp/koala-slice` on the Pi,
slices each for volume and time, deletes the G-code, and caches the figures locally. It does
**not** touch Moonraker, does not write to `~/printer_data/gcodes/`, and cannot start a print.

**Do not run it during a print.** It runs PrusaSlicer over ~14 STLs on the machine hosting
Klippy; sustained CPU load on the print host is a real risk to a running job. Nothing in the
script says so.

## Inspect layer 1 before printing

Cheap, headless, and it would have caught the 2026-09-01 Kinetic Hinge Toy failure in a minute.
Parse the first extruding layer out of the G-code and render it — what you are looking for is
whether layer 1 has *area*. Solid filled regions adhere; a field of single-width lines and
small isolated dashes is the shape that fails.

Extract the layer-1 segments on the Pi, then render locally with ImageMagick:

```bash
# on the Pi: emit "x1 y1 x2 y2" per extruding move of the first layer
python3 - <<'EOF' > layer1.txt
import re
G="/home/wkenn/printer_data/gcodes/<job>.gcode"
z=None; px=py=None; first=None
for line in open(G, errors="ignore"):
    if not line.startswith(("G1","G0")): continue
    mz=re.search(r"\bZ(-?[\d.]+)", line)
    if mz: z=float(mz.group(1))
    mx=re.search(r"\bX(-?[\d.]+)", line); my=re.search(r"\bY(-?[\d.]+)", line)
    if mx and my:
        x,y=float(mx.group(1)),float(my.group(1))
        if " E" in line:
            if first is None: first=z
            if z==first and px is not None: print("%.3f %.3f %.3f %.3f"%(px,py,x,y))
        px,py=x,y
EOF
```

Draw those as SVG lines on a 220 × 220 grid (flip Y — G-code origin is front-left, SVG's is
top-left) and `convert` to PNG. Also worth checking the same way: that the extruding X/Y bounds
sit inside the bed, since PrusaSlicer centres the object and a model may arrive far off-origin.

## Viewing photos of prints

Phone photos of the plate are the only way to diagnose an adhesion failure — telemetry cannot
see it. iPhone `.HEIC` needs decoding first; `libheif-examples` and `imagemagick` are installed
locally for this:

```bash
heif-convert -q 90 IMG_1234.HEIC out.jpg
convert out.jpg -crop 1100x900+1750+2300 +repage -resize 1300x detail.jpg   # zoom a region
```

WSL paths given as `\\wsl.localhost\Ubuntu-24.04\home\wkenn\...` map to `/home/wkenn/...`.
