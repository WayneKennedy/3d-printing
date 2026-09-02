#!/bin/bash
# Usage: slice-print.sh <model.stl|.3mf> [material] [--print]
# materials: petg (default). Slices with the matching Ender-5 S1 profile into Mainsail.
set -e
STL="$1"; MAT="${2:-petg}"
DOPRINT="no"; [ "$3" = "--print" ] && DOPRINT="yes"
CFG="$HOME/slicer/ender5s1_${MAT}.ini"
[ -f "$CFG" ] || { echo "No profile for material: $MAT ($CFG)"; exit 1; }
[ -f "$STL" ] || { echo "Model not found: $STL"; exit 1; }
base=$(basename "$STL"); name="${base%.*}"
OUT="$HOME/printer_data/gcodes/${name}.gcode"
echo "Slicing $base as $MAT -> $OUT"
prusa-slicer --load "$CFG" --export-gcode --output "$OUT" "$STL" 2>&1 | tail -4 \
  || xvfb-run -a prusa-slicer --load "$CFG" --export-gcode --output "$OUT" "$STL" 2>&1 | tail -4
echo "Done: $(ls -l "$OUT" | awk "{print \$5}") bytes"
if [ "$DOPRINT" = "yes" ]; then
  echo "Starting print..."
  curl -s -X POST "http://localhost:7125/printer/print/start?filename=${name}.gcode"; echo
fi
