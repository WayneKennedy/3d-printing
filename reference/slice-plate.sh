#!/bin/bash
# Usage: slice-plate.sh <output-name> <material> <model.stl> [model.stl ...]
# Arranges several models onto ONE plate and slices them as a single job.
# Companion to slice-print.sh, which handles a single model. PrusaSlicer's
# --merge arranges the supplied models before merging, so the STLs' own XY
# coordinates do not matter and overlapping source models are fine.
#
# Centres on the MEASURED MESH, not the bed. The bed centre is 110,110 but the
# saved mesh covers X3-205 Y28-218, whose centre is 104,123. Outside the mesh
# Klipper extrapolates, which is exactly where first-layer adhesion turns
# unreliable. It also keeps a plate clear of the START_PRINT purge line at Y8.
# Override with PLATE_CENTER=x,y if a job needs different placement.
set -e
# Slicer resolution (2026-09-09): PrusaSlicer 2.9.6 from Flathub (organic/tree supports,
# buildplate_only honoured by the tree) is preferred; the Debian 2.5.0 binary is the fallback
# and cannot do organic supports. Which one ran is printed. The old xvfb-run fallback was
# dead code: xvfb-run is not installed here.
if flatpak info --user com.prusa3d.PrusaSlicer >/dev/null 2>&1; then
  SLICER="flatpak run --user --command=prusa-slicer com.prusa3d.PrusaSlicer"
  SLICER_NAME="PrusaSlicer 2.9.x (flatpak)"
elif command -v prusa-slicer >/dev/null 2>&1; then
  SLICER="prusa-slicer"
  SLICER_NAME="prusa-slicer $(prusa-slicer --help 2>/dev/null | head -1)"
else
  echo "No slicer found: install PrusaSlicer via flatpak (com.prusa3d.PrusaSlicer) or apt (prusa-slicer)" >&2
  exit 1
fi
echo "Slicer: $SLICER_NAME"
NAME="$1"; shift
MAT="$1"; shift
[ $# -ge 1 ] || { echo "No models given"; exit 1; }
CFG="$HOME/slicer/ender5s1_${MAT}.ini"
[ -f "$CFG" ] || { echo "No profile for material: $MAT ($CFG)"; exit 1; }
for m in "$@"; do [ -f "$m" ] || { echo "Model not found: $m"; exit 1; }; done
CENTER="${PLATE_CENTER:-104,123}"
OUT="$HOME/printer_data/gcodes/${NAME}.gcode"
echo "Slicing $# model(s) as $MAT centred on $CENTER -> $OUT"
$SLICER --load "$CFG" --merge --center "$CENTER" --export-gcode --output "$OUT" "$@" 2>&1 | grep -v "\[trace\]" | tail -5
echo "Done: $(ls -l "$OUT" | awk '{print $5}') bytes"
