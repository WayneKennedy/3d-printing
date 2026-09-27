#!/bin/bash
# Usage: orca-slice.sh <output-name> <profile> <model.stl|.3mf>... [--print]
# Slices one or more models onto one plate with OrcaSlicer (flatpak, version-masked) into
# ~/printer_data/gcodes/<output-name>.gcode, then checks the emitted G-code against the traps
# in 3d-printing AGENTS.md and refuses to leave a file that fails them.
#
# <profile> resolves ~/slicer/orca/process_<profile>.json; the filament is the part before the
# first "_" (petg_fast -> filament_petg.json). Machine: ~/slicer/orca/machine_ender5s1.json,
# whose printable_area is the bed MESH (X3-205, Y28-218), so Orca's arrange centres parts on
# 104,123 and refuses anything outside the mesh. Several models are arranged by Orca itself.
set -euo pipefail
APP=com.orcaslicer.OrcaSlicer
DIR="$HOME/slicer/orca"
GCODES="$HOME/printer_data/gcodes"

[ $# -ge 3 ] || { sed -n 2p "$0" | sed 's/^# //' >&2; exit 2; }
NAME="$1"; PROF="$2"; shift 2
DOPRINT=no; MODELS=()
for a in "$@"; do [ "$a" = "--print" ] && DOPRINT=yes || MODELS+=("$(realpath "$a")"); done

flatpak info --user "$APP" >/dev/null 2>&1 || { echo "OrcaSlicer flatpak ($APP) not installed" >&2; exit 1; }
MACHINE="$DIR/machine_ender5s1.json"
PROCESS="$DIR/process_${PROF}.json"
FILAMENT="$DIR/filament_${PROF%%_*}.json"
for f in "$MACHINE" "$PROCESS" "$FILAMENT" "${MODELS[@]}"; do [ -f "$f" ] || { echo "Missing: $f" >&2; exit 1; }; done

STATE=$(curl -s -m10 "http://localhost:7125/printer/objects/query?print_stats" \
  | python3 -c 'import json,sys;print(json.load(sys.stdin)["result"]["status"]["print_stats"]["state"])' 2>/dev/null || echo unknown)
[ "$STATE" = printing ] || [ "$STATE" = paused ] && { echo "Refusing to slice: printer is $STATE (AGENTS.md rule 1)" >&2; exit 1; }

VER=$(flatpak info --user "$APP" | awk '/Version:/{print $2}')
echo "Slicer: OrcaSlicer $VER (flatpak) - $PROF"
TMP=$(mktemp -d "$HOME/.cache/orca-slice.XXXXXX"); trap 'rm -rf "$TMP"' EXIT
set +e
flatpak run --user --command=orca-slicer "$APP" \
  --load-settings "$MACHINE;$PROCESS" --load-filaments "$FILAMENT" \
  --arrange 1 --slice 0 --outputdir "$TMP" "${MODELS[@]}" >"$TMP/log" 2>&1
RC=$?; set -e
if [ $RC -ne 0 ] || [ ! -s "$TMP/plate_1.gcode" ]; then
  echo "Slice failed (exit $RC):" >&2
  python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["error_string"])' "$TMP/result.json" 2>/dev/null >&2 || tail -5 "$TMP/log" >&2
  exit 1
fi
[ -e "$TMP/plate_2.gcode" ] && { echo "Models did not fit one plate (plate_2 produced)" >&2; exit 1; }

# Trap checks on the emitted G-code (AGENTS.md "Traps that have each cost a real print").
G="$TMP/plate_1.gcode"
python3 - "$G" <<'EOF'
import re, sys
G = sys.argv[1]; fail = []
lines = open(G, errors="ignore").read().splitlines()
head = [l for l in lines if l and not l.startswith(";")][:6]
first = lambda tok: next((i for i, l in enumerate(head) if l.split()[0] == tok), 99)
if not first("M140") < first("M190") < first("M104") < first("START_PRINT") < 99:
    fail.append("start block is not M140, M190, M104, START_PRINT: %s" % head)
cfg = dict(re.match(r"; (\w+) = (.*)", l).groups() for l in lines if re.match(r"; \w+ = ", l))
if cfg.get("brim_type") != "no_brim" and cfg.get("brim_width") not in ("0", None): fail.append("brim present")
if cfg.get("gcode_flavor") != "klipper": fail.append("gcode_flavor is %s" % cfg.get("gcode_flavor"))
xs, ys = [], []; x = y = None
for l in lines:
    if not l.startswith(("G1", "G2", "G3")): continue
    mx = re.search(r"X(-?[\d.]+)", l); my = re.search(r"Y(-?[\d.]+)", l)
    if mx: x = float(mx.group(1))
    if my: y = float(my.group(1))
    if re.search(r"E[\d.]", l) and (mx or my): xs.append(x); ys.append(y)
if not xs: fail.append("no extrusion found")
elif min(xs) < 3 or max(xs) > 205 or min(ys) < 28 or max(ys) > 218:
    fail.append("footprint X%.1f-%.1f Y%.1f-%.1f outside mesh X3-205 Y28-218" % (min(xs), max(xs), min(ys), max(ys)))
est = next((l.split("= ")[1] for l in lines if "estimated printing time (normal mode)" in l), "?")
g = next((l.split("= ")[1] for l in lines if l.startswith("; filament used [g]")), "?")
if fail: print("TRAP CHECK FAILED: " + "; ".join(fail)); sys.exit(1)
print("Checks OK - footprint X%.1f-%.1f Y%.1f-%.1f, %s, %s g" % (min(xs), max(xs), min(ys), max(ys), est, g))
EOF
mv "$G" "$GCODES/$NAME.gcode"
echo "Done: $GCODES/$NAME.gcode"
if [ "$DOPRINT" = yes ]; then
  curl -s -X POST "http://localhost:7125/printer/print/start?filename=$NAME.gcode"; echo
fi
