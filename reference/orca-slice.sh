#!/bin/bash
# Usage: orca-slice.sh [--printer 5si|5p] <output-name> <profile> <model.stl|.3mf>... [--print] [--no-rotate]
# Slices one or more models onto one plate with OrcaSlicer (flatpak, version-masked) into
# the printer's gcodes dir (5SI ~/printer_data, 5P ~/printer_data_5p; default 5si), then checks the emitted G-code against the traps
# in 3d-printing AGENTS.md and refuses to leave a file that fails them.
#
# <profile> resolves ~/slicer/orca/process_<profile>.json; the filament is the part before the
# first "_" (petg_fast -> filament_petg.json); if machine_<printer>_<filament>.json exists it
# replaces the machine file (tpu: slicer-side z_offset, which Orca keeps in the machine preset).
# Machine: ~/slicer/orca/machine_ender5s1.json
# (5SI) or machine_ender5plus.json (5P), whose printable_area is that bed's MESH (5SI X3-205
# Y28-218, centre 104,123) or, for 5P, the mesh in X and the plate in Y (X15-305 Y-2-348, a
# 350 mm depth centred on Y173: arrange needs ~7 mm more than part + skirt; extrusion is then
# checked against Y1-345; the probe cannot mesh beyond Y336), so Orca's arrange centres parts
# there and refuses anything outside it.
# --no-rotate: keep the STL's orientation. Orca's arrange otherwise turns a part by an arbitrary
# angle (a 186 x 168 plate came out 2.7 deg askew), which a 336 mm plate on 5P has no room for. Several models are arranged by Orca itself.
# Slices while printers print (owner, 2026-09-29): Orca slices up to 6 s were measured harmless
# with both printing - 3d-printing docs/open-questions.md, "Two printers and slicing on one Pi".
set -euo pipefail
APP=com.orcaslicer.OrcaSlicer
DIR="$HOME/slicer/orca"
PRINTER=5si
if [ "${1:-}" = "--printer" ]; then PRINTER="${2:-}"; shift 2; fi
case "$PRINTER" in
  5si) MACHINE="$DIR/machine_ender5s1.json";   GCODES="$HOME/printer_data/gcodes";    PORT=7125; MESH="3 205 28 218" ;;
  5p)  MACHINE="$DIR/machine_ender5plus.json"; GCODES="$HOME/printer_data_5p/gcodes"; PORT=7126; MESH="15 305 1 345" ;;
  *)   echo "Unknown printer: $PRINTER (5si or 5p)" >&2; exit 2 ;;
esac

[ $# -ge 3 ] || { sed -n 2p "$0" | sed 's/^# //' >&2; exit 2; }
NAME="$1"; PROF="$2"; shift 2
DOPRINT=no; ROTATE=(); MODELS=()
for a in "$@"; do
  case "$a" in
    --print) DOPRINT=yes ;;
    --no-rotate) ROTATE=(--allow-rotations=0) ;;
    *) MODELS+=("$(realpath "$a")") ;;
  esac
done

flatpak info --user "$APP" >/dev/null 2>&1 || { echo "OrcaSlicer flatpak ($APP) not installed" >&2; exit 1; }
PROCESS="$DIR/process_${PROF}.json"
FILAMENT="$DIR/filament_${PROF%%_*}.json"
[ -f "${MACHINE%.json}_${PROF%%_*}.json" ] && MACHINE="${MACHINE%.json}_${PROF%%_*}.json"
for f in "$MACHINE" "$PROCESS" "$FILAMENT" "${MODELS[@]}"; do [ -f "$f" ] || { echo "Missing: $f" >&2; exit 1; }; done

VER=$(flatpak info --user "$APP" | awk '/Version:/{print $2}')
echo "Slicer: OrcaSlicer $VER (flatpak) - $PROF for $PRINTER"
TMP=$(mktemp -d "$HOME/.cache/orca-slice.XXXXXX"); trap 'rm -rf "$TMP"' EXIT
set +e
flatpak run --user --command=orca-slicer "$APP" \
  --load-settings "$MACHINE;$PROCESS" --load-filaments "$FILAMENT" \
  --arrange 1 "${ROTATE[@]}" --slice 0 --outputdir "$TMP" "${MODELS[@]}" >"$TMP/log" 2>&1
RC=$?; set -e
if [ $RC -ne 0 ] || [ ! -s "$TMP/plate_1.gcode" ]; then
  echo "Slice failed (exit $RC):" >&2
  python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["error_string"])' "$TMP/result.json" 2>/dev/null >&2 || tail -5 "$TMP/log" >&2
  exit 1
fi
[ -e "$TMP/plate_2.gcode" ] && { echo "Models did not fit one plate (plate_2 produced)" >&2; exit 1; }

# Trap checks on the emitted G-code (AGENTS.md "Traps that have each cost a real print").
G="$TMP/plate_1.gcode"
python3 - "$G" $MESH <<'EOF'
import re, sys
G = sys.argv[1]; X0, X1, Y0, Y1 = map(float, sys.argv[2:6]); fail = []
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
elif min(xs) < X0 or max(xs) > X1 or min(ys) < Y0 or max(ys) > Y1:
    fail.append("footprint X%.1f-%.1f Y%.1f-%.1f outside mesh X%g-%g Y%g-%g" % (min(xs), max(xs), min(ys), max(ys), X0, X1, Y0, Y1))
est = next((l.split("= ")[1] for l in lines if "estimated printing time (normal mode)" in l), "?")
g = next((l.split("= ")[1] for l in lines if l.startswith("; filament used [g]")), "?")
if fail: print("TRAP CHECK FAILED: " + "; ".join(fail)); sys.exit(1)
print("Checks OK - footprint X%.1f-%.1f Y%.1f-%.1f, %s, %s g" % (min(xs), max(xs), min(ys), max(ys), est, g))
EOF
mv "$G" "$GCODES/$NAME.gcode"
echo "Done: $GCODES/$NAME.gcode"
if [ "$DOPRINT" = yes ]; then
  curl -s -X POST "http://localhost:$PORT/printer/print/start?filename=$NAME.gcode"; echo
fi
