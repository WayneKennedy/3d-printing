#!/usr/bin/env python3
"""Watch a running Klipper print via Moonraker; emit one line per notable event.

Written for the Monitor harness: every stdout line becomes a notification, so the
filter lives here rather than in a grep. Exits when the job reaches a terminal
state, so the watch ends on its own.

Talks to Moonraker over the tailnet (trusted_clients covers 100.64.0.0/10, so no
API key and no SSH). Silence means healthy; every terminal state emits.

  tools/print-monitor.py [--host H] [--interval S] [--heartbeat S]
"""
import argparse, json, sys, time, urllib.error, urllib.request

OBJECTS = "print_stats&virtual_sdcard&extruder&heater_bed"
TERMINAL = {"complete": 0, "error": 1, "cancelled": 1}
# Deviation that means something is wrong, not just PID ripple. Nozzle PID
# overshoot on this machine sits inside a couple of degrees.
NOZZLE_TOL, BED_TOL = 10.0, 5.0


def emit(msg):
    print(f"{time.strftime('%H:%M:%S')} {msg}", flush=True)


def get(host, path):
    with urllib.request.urlopen(f"http://{host}{path}", timeout=15) as r:
        return json.load(r)["result"]


def hms(sec):
    return f"{int(sec) // 3600}h{int(sec) % 3600 // 60:02d}m"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--host", default="100.99.147.57:7125")
    p.add_argument("--interval", type=int, default=60)
    p.add_argument("--heartbeat", type=int, default=1800)
    a = p.parse_args()

    state = None
    down = False
    fails = 0
    last_beat = 0.0
    # A heater climbing to target is not a fault; a heater that reached target and
    # then drifted is. Track that per heater, so the heat-soak at the start of every
    # print does not fire a TEMP alert -- which would train the reader to ignore the
    # one alert that actually matters mid-print.
    reached, last_target = {}, {}

    while True:
        try:
            st = get(a.host, f"/printer/objects/query?{OBJECTS}")["status"]
            info = get(a.host, "/printer/info")
        except (urllib.error.URLError, OSError, ValueError, KeyError) as e:
            fails += 1
            # Two misses is a blip; three in a row is the host, the network or Klippy.
            if fails >= 3 and not down:
                down = True
                emit(f"UNREACHABLE Moonraker at {a.host} — {type(e).__name__}: {e}")
            time.sleep(a.interval)
            continue

        if down:
            emit("RECOVERED Moonraker reachable again")
        down, fails = False, 0

        # Klippy itself falling over (lost MCU comms is the documented failure here)
        # does not necessarily show up in print_stats, so check it separately.
        if info.get("state") != "ready":
            emit(f"KLIPPER {info.get('state')} — {info.get('state_message', '').strip()}")
            return 1

        ps, sd = st["print_stats"], st["virtual_sdcard"]
        new = ps["state"]
        pct = sd.get("progress", 0.0) * 100
        dur = ps.get("print_duration", 0.0)

        if new != state:
            if state is not None:
                emit(f"STATE {state} -> {new} at {pct:.1f}% ({ps['filename']})")
            state = new
            if new in TERMINAL:
                emit(f"{new.upper()} {ps['filename']} after {hms(dur)}, "
                     f"{ps.get('filament_used', 0) / 1000:.1f} m filament")
                return TERMINAL[new]
            if new == "paused":
                emit(f"PAUSED {ps['filename']} at {pct:.1f}% — needs a decision")

        for name, obj, tol in (("nozzle", "extruder", NOZZLE_TOL),
                               ("bed", "heater_bed", BED_TOL)):
            tgt, cur = st[obj]["target"], st[obj]["temperature"]
            if tgt != last_target.get(obj):        # new setpoint: warming again
                last_target[obj] = tgt
                reached[obj] = False
            if tgt <= 0:                           # off, or cooling down after the job
                continue
            if not reached.get(obj):
                if cur >= tgt - tol:
                    reached[obj] = True            # arrived; deviation now means something
            elif abs(cur - tgt) > tol:
                emit(f"TEMP {name} {cur:.1f} C vs target {tgt:.0f} C at {pct:.1f}% "
                     f"(had reached target)")

        now = time.monotonic()
        if new == "printing" and now - last_beat >= a.heartbeat:
            last_beat = now
            rate = pct / dur if dur > 0 else 0
            eta = f", ~{hms((100 - pct) / rate)} left" if rate > 0 else ""
            emit(f"OK {pct:.1f}% after {hms(dur)}{eta} — "
                 f"nozzle {st['extruder']['temperature']:.0f}/"
                 f"{st['extruder']['target']:.0f}, "
                 f"bed {st['heater_bed']['temperature']:.0f}/"
                 f"{st['heater_bed']['target']:.0f}")

        time.sleep(a.interval)


if __name__ == "__main__":
    sys.exit(main())
