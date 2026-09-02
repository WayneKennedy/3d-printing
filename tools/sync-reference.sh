#!/bin/bash
# Refresh reference/ from the live files on printhub, then show what drifted.
# The Pi holds the authoritative copies; reference/ is a snapshot for version control.
# Run this after ANY change on the Pi, and before trusting reference/ for anything.
set -euo pipefail
cd "$(dirname "$0")/.."
HOST="${PRINTHUB_HOST:-wkenn@printhub}"

sync() {  # <remote path> <local path>
  local tmp; tmp=$(mktemp)
  if ! scp -q "$HOST:$1" "$tmp" 2>/dev/null; then
    echo "  MISSING on Pi: $1"; rm -f "$tmp"; return
  fi
  if [ -f "$2" ] && diff -q "$2" "$tmp" >/dev/null; then
    echo "  unchanged: $2"
  else
    mv "$tmp" "$2"; echo "  UPDATED:   $2"
  fi
  rm -f "$tmp" 2>/dev/null || true
}

echo "Syncing reference/ from $HOST"
sync "printer_data/config/printer.cfg" "reference/printer.cfg"
sync "slicer/slice-print.sh"           "reference/slice-print.sh"
sync "printer_data/config/crowsnest.conf" "reference/crowsnest.conf"
for ini in petg pla; do
  sync "slicer/ender5s1_${ini}.ini" "reference/ender5s1_${ini}.ini"
done

echo
if git diff --quiet -- reference/; then
  echo "reference/ is in sync with the Pi; nothing to commit."
else
  echo "reference/ drifted. Changes:"
  git --no-pager diff --stat -- reference/
fi
