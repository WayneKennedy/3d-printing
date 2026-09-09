#!/bin/bash
# Usage: slice-print.sh <model.stl|.3mf> [material] [--print]
# materials: petg (default). Slices with the matching Ender-5 S1 profile into Mainsail.
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
STL="$1"; MAT="${2:-petg}"
DOPRINT="no"; [ "$3" = "--print" ] && DOPRINT="yes"
CFG="$HOME/slicer/ender5s1_${MAT}.ini"
[ -f "$CFG" ] || { echo "No profile for material: $MAT ($CFG)"; exit 1; }
[ -f "$STL" ] || { echo "Model not found: $STL"; exit 1; }
base=$(basename "$STL"); name="${base%.*}"
OUT="$HOME/printer_data/gcodes/${name}.gcode"
echo "Slicing $base as $MAT -> $OUT"
$SLICER --load "$CFG" --export-gcode --output "$OUT" "$STL" 2>&1 | grep -v "\[trace\]" | tail -4
echo "Done: $(ls -l "$OUT" | awk "{print \$5}") bytes"
if [ "$DOPRINT" = "yes" ]; then
  echo "Starting print..."
  curl -s -X POST "http://localhost:7125/printer/print/start?filename=${name}.gcode"; echo
fi
