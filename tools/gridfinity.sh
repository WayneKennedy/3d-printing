#!/bin/bash
# Generate Gridfinity STLs from Gridfinity Rebuilt (OpenSCAD) at a pinned commit.
#
#   tools/gridfinity.sh baseplate <gridx> <gridy>          -> scratch/gridfinity/bp_<x>x<y>.stl
#   tools/gridfinity.sh bin <gridx> <gridy> <gridz>        -> scratch/gridfinity/bin_<x>x<y>x<z>.stl
#
# Settled parameters (docs/decisions.md#desk-gridfinity): thin baseplate, no magnet or screw
# holes in plates or bins. Anything else, pass extra OpenSCAD args after the sizes, e.g.
#   tools/gridfinity.sh bin 2 1 3 -D divx=2
#
# Needs an OpenSCAD newer than 2021.01: Ubuntu's 2021.01 renders baseplates but fails to
# parse gridfinity-rebuilt-bins.scad (syntax error, line 125). A development snapshot from
# https://files.openscad.org/snapshots/ works (2026.09.22 tested); point $OPENSCAD at it.
# Largest printable baseplate here is 4x4 (168 mm) -- the mesh is ~202 x 190 mm.

set -euo pipefail
cd "$(dirname "$0")/.."

REPO=https://github.com/kennetek/gridfinity-rebuilt-openscad.git
COMMIT=910e22d8607fd7f5f51ad5e5cbc5287a76810bfd   # 2025-08-31
SRC=scratch/gridfinity-rebuilt-openscad
OUT=scratch/gridfinity
OPENSCAD="${OPENSCAD:-openscad}"

usage() { sed -n 4,5p "$0" | sed 's/^# *//' >&2; exit 2; }

command -v "$OPENSCAD" >/dev/null || { echo "OpenSCAD not found: set \$OPENSCAD to a snapshot build (see header)" >&2; exit 1; }
command -v git >/dev/null || { echo "git not found" >&2; exit 1; }
VER=$("$OPENSCAD" --version 2>&1 | grep -oE '[0-9]{4}\.[0-9.]+' | head -1)
[ "${VER%%.*}" -gt 2021 ] 2>/dev/null || { echo "OpenSCAD $VER is too old for the bin script; need a snapshot build (see header)" >&2; exit 1; }

if [ ! -d "$SRC/.git" ]; then
  git init -q "$SRC"
  git -C "$SRC" fetch -q --depth 1 "$REPO" "$COMMIT"
  git -C "$SRC" checkout -q FETCH_HEAD
fi
[ "$(git -C "$SRC" rev-parse HEAD)" = "$COMMIT" ] || { echo "$SRC is not at pinned $COMMIT" >&2; exit 1; }
mkdir -p "$OUT"
OUT=$(realpath "$OUT")

BACKEND=()
"$OPENSCAD" --help 2>&1 | grep -q -- '--backend' && BACKEND=(--backend=manifold)

kind="${1:-}"; shift || true
case "$kind" in
  baseplate)
    [ $# -ge 2 ] || usage
    x=$1 y=$2; shift 2
    f="$OUT/bp_${x}x${y}.stl"
    (cd "$SRC" && "$OPENSCAD" "${BACKEND[@]}" -q -o "$f" -D gridx="$x" -D gridy="$y" \
      -D style_plate=0 -D enable_magnet=false "$@" gridfinity-rebuilt-baseplate.scad) ;;
  bin)
    [ $# -ge 3 ] || usage
    x=$1 y=$2 z=$3; shift 3
    f="$OUT/bin_${x}x${y}x${z}.stl"
    (cd "$SRC" && "$OPENSCAD" "${BACKEND[@]}" -q -o "$f" -D gridx="$x" -D gridy="$y" -D gridz="$z" \
      -D refined_holes=false -D magnet_holes=false -D screw_holes=false "$@" gridfinity-rebuilt-bins.scad) ;;
  *) usage ;;
esac
[ -s "$f" ] || { echo "OpenSCAD produced no output for $f" >&2; exit 1; }
echo "$f"
