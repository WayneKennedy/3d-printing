#!/usr/bin/env python3
"""Temperature tower: dependency-free STL generator and G-code band patcher.

    tools/temp-tower.py stl   OUT.stl   [--bands 11] [--band-h 5] [--fin 0.86]
    tools/temp-tower.py patch IN.gcode OUT.gcode --start 230 --step -5 [--bands 11] [--band-h 5]

The tower is one prism: a solid 12 x 12 mm core for stability, with a thin fin
along one side as the test specimen - pinch it above and below a layer line in a
band and pull, to find the coolest band whose layers will not split. One prism
means one closed, manifold mesh with no boolean union. No bridges or overhangs:
the TPU parts this was written for (2026-09-21) have none.

The fin defaults to 0.86 mm, which is two 0.45 mm perimeter lines at PrusaSlicer's
spacing (0.45 + 0.45 - 0.2 * (1 - pi/4)), so it prints as two clean lines with no
gap fill. Check the G-code for ';TYPE:Gap fill' anyway.

`patch` inserts M104 at the first layer at or above each band boundary, reading
PrusaSlicer's ';Z:' layer comments. Band 0 runs at --start; slice with first-layer
and other-layer temperatures both set to --start. M104, not M109: a wait would
park the nozzle on the part and ooze a blob; the change settles within a layer
or two, so read each band from its middle, not its edges.
"""
import argparse
import re
import struct
import sys


def prism(poly, h, centre):
    """Triangles of a vertical prism over a CCW polygon, fan-triangulated from
    `centre`, which must see every edge (the polygon is star-shaped about it)."""
    tris, n = [], len(poly)
    cx, cy = centre
    for i in range(n):
        (x0, y0), (x1, y1) = poly[i], poly[(i + 1) % n]
        tris.append(((cx, cy, 0), (x1, y1, 0), (x0, y0, 0)))      # bottom, facing -Z
        tris.append(((cx, cy, h), (x0, y0, h), (x1, y1, h)))      # top, facing +Z
        tris.append(((x0, y0, 0), (x1, y1, 0), (x1, y1, h)))      # side
        tris.append(((x0, y0, 0), (x1, y1, h), (x0, y0, h)))
    return tris


def write_stl(path, tris):
    out = bytearray(80) + struct.pack("<I", len(tris))
    for t in tris:
        out += struct.pack("<3f", 0, 0, 0) + b"".join(struct.pack("<3f", *v) for v in t) + b"\0\0"
    open(path, "wb").write(out)


def cmd_stl(a):
    core, fin_len = 12.0, 15.0
    h = a.bands * a.band_h
    t = a.fin
    # CCW outline: core square with the fin leaving the +X face at mid-height of Y.
    # Centred on the origin in XY, on Z0 (see decisions.md#slicing).
    y0, y1 = -t / 2, t / 2
    c = core / 2
    poly = [(-c, -c), (c, -c), (c, y0), (c + fin_len, y0), (c + fin_len, y1),
            (c, y1), (c, c), (-c, c)]
    xs = [p[0] for p in poly]
    dx = -(min(xs) + max(xs)) / 2
    poly = [(x + dx, y) for x, y in poly]
    # Fan from the core centre, not the vertex average: for this outline the
    # average lands inside the fin, from where the core's far corners are hidden.
    tris = prism(poly, h, (dx, 0.0))
    write_stl(a.out, tris)
    print(f"{a.out}: {len(tris)} triangles, {core + fin_len:.1f} x {core:.1f} x {h:.1f} mm, "
          f"{a.bands} bands of {a.band_h} mm, fin {t} mm")


def cmd_patch(a):
    lines = open(a.inp, errors="ignore").read().splitlines(keepends=True)
    out, band, inserted = [], 0, []
    for line in lines:
        out.append(line)
        m = re.match(r";Z:([\d.]+)", line)
        if m:
            z = float(m.group(1))
            # Clamp: the top layer can sit a hair above bands * band_h (55.04 on a
            # 55 mm tower with a 0.24 first layer) and must not open a band that
            # does not exist - it would print below the tested range.
            want = min(int(z // a.band_h + 1e-6), a.bands - 1)
            if want > band:
                band = want
                temp = a.start + a.step * band
                out.append(f"M104 S{temp:g} ; temp-tower band {band}, Z >= {band * a.band_h:g}\n")
                inserted.append((band, z, temp))
    open(a.out, "w").write("".join(out))
    print(f"band 0: {a.start:g} C from the first layer")
    for b, z, t in inserted:
        print(f"band {b}: {t:g} C from Z {z:g}")
    if not inserted:
        sys.exit("no ';Z:' comments found - not PrusaSlicer G-code?")


ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
sp = ap.add_subparsers(dest="cmd", required=True)
s = sp.add_parser("stl"); s.add_argument("out")
s.add_argument("--bands", type=int, default=11); s.add_argument("--band-h", type=float, default=5.0)
s.add_argument("--fin", type=float, default=0.86)
p = sp.add_parser("patch"); p.add_argument("inp"); p.add_argument("out")
p.add_argument("--start", type=float, required=True); p.add_argument("--step", type=float, required=True)
p.add_argument("--band-h", type=float, default=5.0); p.add_argument("--bands", type=int, default=11)
a = ap.parse_args()
{"stl": cmd_stl, "patch": cmd_patch}[a.cmd](a)
