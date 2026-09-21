#!/usr/bin/env python3
"""Dependency-free calibration STLs, each a set of closed prisms (no booleans).

    tools/calibration-parts.py flow-cube   OUT.stl [--size 20] [--height H]
    tools/calibration-parts.py deck-coupon OUT.stl

flow-cube: a plain box, to slice in spiral-vase mode (one perimeter, no top) and
measure the wall against the extrusion width -> extrusion_multiplier. For TPU use
--height 8 or so: a one-line TPU wall went floppy about a third of the way up a
20 mm cube and was dragged into loops (2026-09-21); only the lower wall was usable.

deck-coupon: the wk-drones Holybro 10" FC deck rev C's risky features at real size,
plus the Bee35 GPS pocket (3d-printing open-questions.md, "TPU 95A"). Every body
stands on Z0; the set is centred on the origin, so slice it as one STL with
--center and no --merge (decisions.md#slicing). Layout, +X to the right as it
sits on the bed:
  back row   window plate 76 x 30 x 4 mm, 20 mm square windows at +0.2 / +0.4 /
             +0.6 mm clearance, left to right; the plate is also the flatness check
  middle row three Ø11 x 19.8 mm pillars, hex holes 4.45 / 4.55 / 4.65 AF, left to
             right. They come off the bed as loose parts: MARK EACH BEFORE LIFTING
  front row  four arms 30 mm long x 5 mm tall, 1.8 / 2.0 / 2.08 / 2.2 mm wide, back
             to front. 2.08 was added as the nearest whole number of fixed-width
             lines to 2.0; in the event PrusaSlicer 2.9.6's variable-width perimeters
             print 2.0, 2.08 and 2.2 all as the same loops with no gap fill, so 2.08
             is only an extra data point (sliced 2026-09-21).
"""
import argparse
import math
import struct


def write_stl(path, tris):
    out = bytearray(80) + struct.pack("<I", len(tris))
    for t in tris:
        out += struct.pack("<3f", 0, 0, 0) + b"".join(struct.pack("<3f", *v) for v in t) + b"\0\0"
    open(path, "wb").write(out)


def wall(a, b, h):
    """Side quad on edge a->b of a CCW outline (material on the left), facing out."""
    (x0, y0), (x1, y1) = a, b
    return [((x0, y0, 0), (x1, y1, 0), (x1, y1, h)), ((x0, y0, 0), (x1, y1, h), (x0, y0, h))]


def caps(poly, h):
    """Bottom and top of a convex CCW polygon, fanned from its first vertex."""
    tris = []
    for i in range(1, len(poly) - 1):
        (ax, ay), (bx, by), (cx, cy) = poly[0], poly[i], poly[i + 1]
        tris.append(((ax, ay, 0), (cx, cy, 0), (bx, by, 0)))
        tris.append(((ax, ay, h), (bx, by, h), (cx, cy, h)))
    return tris


def grid_body(xs, ys, solid, h):
    """Prism over the solid cells of a rectilinear grid. Cells share grid lines, so
    there are no T-junctions; walls only where solid meets empty."""
    tris = []
    nx, ny = len(xs) - 1, len(ys) - 1
    filled = lambda i, j: 0 <= i < nx and 0 <= j < ny and solid(i, j)
    for i in range(nx):
        for j in range(ny):
            if not solid(i, j):
                continue
            a, b, c, d = (xs[i], ys[j]), (xs[i + 1], ys[j]), (xs[i + 1], ys[j + 1]), (xs[i], ys[j + 1])
            tris += caps([a, b, c, d], h)
            for (p, q), (di, dj) in (((a, b), (0, -1)), ((b, c), (1, 0)), ((c, d), (0, 1)), ((d, a), (-1, 0))):
                if not filled(i + di, j + dj):
                    tris += wall(p, q, h)
    return tris


def box(x0, y0, x1, y1, h):
    return grid_body([x0, x1], [y0, y1], lambda i, j: True, h)


def hex_pillar(cx, cy, dia, af, h, per_side=8):
    """Round pillar with a through hex hole: six convex annular sectors, each from
    one hex edge to the matching arc of a 6*per_side-gon on the pillar diameter."""
    rh, ro, n = af / math.sqrt(3), dia / 2, 6 * per_side
    hexv = [(cx + rh * math.cos(math.radians(60 * i)), cy + rh * math.sin(math.radians(60 * i))) for i in range(6)]
    outv = [(cx + ro * math.cos(2 * math.pi * k / n), cy + ro * math.sin(2 * math.pi * k / n)) for k in range(n)]
    tris = []
    for i in range(6):
        arc = [outv[(i * per_side + k) % n] for k in range(per_side + 1)]
        poly = [hexv[i]] + arc + [hexv[(i + 1) % 6]]              # CCW
        tris += caps(poly, h)
        for k in range(per_side):                                  # outer arc
            tris += wall(arc[k], arc[k + 1], h)
        tris += wall(hexv[(i + 1) % 6], hexv[i], h)                # hex edge, facing into the hole
    return tris


def centred(tris):
    xs = [v[0] for t in tris for v in t]
    ys = [v[1] for t in tris for v in t]
    dx, dy = -(min(xs) + max(xs)) / 2, -(min(ys) + max(ys)) / 2
    return [tuple((x + dx, y + dy, z) for x, y, z in t) for t in tris], (max(xs) - min(xs), max(ys) - min(ys))


def deck_coupon():
    tris = []
    # Window plate: grid lines at every window edge; three windows centred 25 mm apart.
    w, depth, t = 76.0, 30.0, 4.0
    wins = [(-25.0, 20.2), (0.0, 20.4), (25.0, 20.6)]
    xs = sorted({-w / 2, w / 2} | {c + s * sz / 2 for c, sz in wins for s in (-1, 1)})
    edges_y = {}
    for c, sz in wins:
        edges_y[c] = (depth / 2 - sz / 2, depth / 2 + sz / 2)
    ys = sorted({0.0, depth} | {v for lo_hi in edges_y.values() for v in lo_hi})
    def solid(i, j):
        mx, my = (xs[i] + xs[i + 1]) / 2, (ys[j] + ys[j + 1]) / 2
        return not any(abs(mx - c) < sz / 2 and abs(my - depth / 2) < sz / 2 for c, sz in wins)
    tris += grid_body(xs, ys, solid, t)
    # Pillars, 8 mm clear of the plate, 16 mm on centres.
    for k, af in enumerate((4.45, 4.55, 4.65)):
        tris += hex_pillar(-16.0 + 16.0 * k, -13.5, 11.0, af, 19.8)
    # Arms, front row, back to front; 6 mm on centres.
    for k, aw in enumerate((1.8, 2.0, 2.08, 2.2)):
        y = -26.0 - 6.0 * k
        tris += box(-15.0, y - aw / 2, 15.0, y + aw / 2, 5.0)
    return tris


ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
sp = ap.add_subparsers(dest="cmd", required=True)
c = sp.add_parser("flow-cube"); c.add_argument("out"); c.add_argument("--size", type=float, default=20.0)
c.add_argument("--height", type=float, help="default: same as --size")
d = sp.add_parser("deck-coupon"); d.add_argument("out")
a = ap.parse_args()
if a.cmd == "flow-cube":
    s = a.size / 2
    tris = box(-s, -s, s, s, a.height or a.size)
else:
    tris = deck_coupon()
tris, (bx, by) = centred(tris)
write_stl(a.out, tris)
print(f"{a.out}: {len(tris)} triangles, footprint {bx:.1f} x {by:.1f} mm")
