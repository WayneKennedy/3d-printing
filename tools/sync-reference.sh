#!/bin/bash
# Refresh reference/ from the live files on printhub, then show what drifted.
# The Pi holds the authoritative copies; reference/ is a version-controlled cache.
# Run this after ANY change on the Pi, and before trusting reference/ for anything.
#
# Assumes nothing about the machine it runs on. A fresh clone on a freshly
# reformatted box either works or says exactly what is missing. In particular it
# never reports a broken connection as though the Pi had lost its config -- the
# previous version swallowed transport errors per file and printed "MISSING on Pi"
# for every one of them when plain ssh could not verify the host key.

set -euo pipefail
cd "$(dirname "$0")/.."

HOST="${PRINTHUB_HOST:-wkenn@printhub}"
FAILED=0

# --- transport ---------------------------------------------------------------
# Plain ssh needs a known_hosts entry and a TTY to accept one, so it fails on a
# machine that has never talked to the Pi. tailscale ssh verifies through the
# tailnet CA and needs neither. Prefer it, fall back to ssh, and if neither works
# say so once, up front, rather than failing eleven times in a row.

probe() {
  case "$1" in
    tailscale) command -v tailscale >/dev/null 2>&1 &&
               timeout 20 tailscale ssh "$HOST" true >/dev/null 2>&1 ;;
    ssh)       timeout 20 ssh -o BatchMode=yes -o ConnectTimeout=10 "$HOST" true \
                 >/dev/null 2>&1 ;;
  esac
}

remote() {  # run one command string on the Pi over whichever transport works
  # stdin is closed deliberately. ssh and tailscale ssh both read stdin and will
  # swallow the rest of a `while read` loop's input, which silently synced only
  # the FIRST discovered profile and left the others looking absent.
  case "$TRANSPORT" in
    tailscale) timeout 60 tailscale ssh "$HOST" "$1" </dev/null ;;
    ssh)       timeout 60 ssh -n -o BatchMode=yes "$HOST" "$1" </dev/null ;;
    *)         return 1 ;;
  esac
}

TRANSPORT=""
for t in tailscale ssh; do
  if probe "$t"; then TRANSPORT="$t"; break; fi
done

if [ -z "$TRANSPORT" ]; then
  {
    echo "sync-reference.sh: cannot reach $HOST. Nothing was written."
    echo
    echo "Tried, in order:"
    if command -v tailscale >/dev/null 2>&1; then
      echo "  tailscale ssh $HOST  - installed, but the connection failed"
    else
      echo "  tailscale ssh $HOST  - 'tailscale' is not installed on this machine"
    fi
    echo "  ssh $HOST            - failed (BatchMode: no password or host-key prompt possible)"
    echo
    echo "Likely causes:"
    echo "  * not on the tailnet, or the Pi is off  - check 'tailscale status'"
    echo "  * no known_hosts entry and no TTY to accept one. Either use tailscale,"
    echo "    which verifies via the tailnet CA, or seed the key once:"
    echo "      ssh-keyscan -t ed25519 ${HOST#*@} >> ~/.ssh/known_hosts"
    echo
    echo "Target another machine with:  PRINTHUB_HOST=user@host $0"
  } >&2
  exit 1
fi

echo "Syncing reference/ from $HOST over $TRANSPORT"

# --- one file ----------------------------------------------------------------
sync() {  # <remote path, absolute or relative to ~> <local path>
  local rp="$1" lp="$2" tmp size got
  tmp=$(mktemp)

  # Ask for the size first. The connection is already known good, so "no size"
  # genuinely means the file is absent rather than the link being down.
  size=$(remote "stat -c %s '$rp' 2>/dev/null || echo missing" | tr -d '\r\n') || size=missing
  if [ "$size" = "missing" ] || [ -z "$size" ]; then
    echo "  MISSING on Pi: $rp"
    rm -f "$tmp"; FAILED=1; return
  fi

  remote "cat '$rp'" > "$tmp" 2>/dev/null || true
  got=$(wc -c < "$tmp")
  if [ "$got" != "$size" ]; then
    # A short read must never overwrite a good snapshot with a truncated one.
    echo "  TRUNCATED:  $rp - got $got of $size bytes, not written"
    rm -f "$tmp"; FAILED=1; return
  fi

  if [ -f "$lp" ] && cmp -s "$lp" "$tmp"; then
    echo "  unchanged:  $lp"
    rm -f "$tmp"
  else
    mkdir -p "$(dirname "$lp")"
    mv "$tmp" "$lp"
    echo "  UPDATED:    $lp"
  fi
}

sync "printer_data/config/printer.cfg"   "reference/printer.cfg"
sync "printer_data/config/crowsnest.conf" "reference/crowsnest.conf"

# Slicer scripts and profiles are DISCOVERED on the Pi, not hardcoded. A hardcoded
# list silently left ender5s1_petg_koala.ini, ender5s1_petg_koalacoupon.ini and
# slice-plate.sh out of version control entirely - the exact "a dialled-in profile
# gets lost" failure this directory exists to prevent. Backups (*.bak*) are skipped.
found=0
while read -r rp; do
  [ -n "$rp" ] || continue
  sync "$rp" "reference/$(basename "$rp")"
  found=$((found + 1))
done < <(remote 'ls ~/slicer/*.sh ~/slicer/ender5s1_*.ini 2>/dev/null' \
         | tr -d '\r' | grep -v '\.bak' || true)

if [ "$found" -eq 0 ]; then
  echo "  WARNING: discovered no slicer scripts or profiles in ~/slicer on the Pi." >&2
  echo "           That is not normal - check the path before trusting reference/." >&2
  FAILED=1
fi

echo
if ! git rev-parse --git-dir >/dev/null 2>&1; then
  echo "Not a git checkout, so no drift summary."
elif git diff --quiet -- reference/ && git diff --cached --quiet -- reference/; then
  echo "reference/ is in sync with the Pi; nothing to commit."
else
  echo "reference/ drifted. Changes:"
  git --no-pager diff --stat -- reference/
fi

[ "$FAILED" -eq 0 ] || { echo; echo "Completed with problems (see above)." >&2; exit 2; }
