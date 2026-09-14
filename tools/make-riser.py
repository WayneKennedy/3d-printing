#!/usr/bin/env python3
"""Generate desk-riser STL: truncated cones (frustums), pure Python, no dependencies.

Usage: make-riser.py OUT.stl [--base D] [--top D] [--height H] [--count N] [--gap G]
Defaults: base 80 mm, top 75 mm, height 12 mm, count 2, gap 10 mm. Multiple risers are
placed side by side along X in ONE STL so the slicer never has to --merge (see AGENTS.md:
`prusa-slicer --merge` is unreliable). slice-plate.sh --center then puts the bbox on the mesh.
"""
import argparse, math, struct, sys

def frustum(cx, cy, r_base, r_top, h, n=180):
    tris = []
    for i in range(n):
        a0, a1 = 2*math.pi*i/n, 2*math.pi*(i+1)/n
        b0 = (cx+r_base*math.cos(a0), cy+r_base*math.sin(a0), 0.0)
        b1 = (cx+r_base*math.cos(a1), cy+r_base*math.sin(a1), 0.0)
        t0 = (cx+r_top*math.cos(a0),  cy+r_top*math.sin(a0),  h)
        t1 = (cx+r_top*math.cos(a1),  cy+r_top*math.sin(a1),  h)
        tris.append((b0, b1, t1)); tris.append((b0, t1, t0))          # wall, outward CCW
        tris.append(((cx, cy, 0.0), b1, b0))                          # bottom, normal -Z
        tris.append(((cx, cy, h), t0, t1))                            # top, normal +Z
    return tris

def normal(a, b, c):
    u = [b[i]-a[i] for i in range(3)]; v = [c[i]-a[i] for i in range(3)]
    n = [u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0]]
    l = math.sqrt(sum(x*x for x in n)) or 1.0
    return [x/l for x in n]

def write_stl(path, tris):
    with open(path, "wb") as f:
        f.write(b"riser frustum".ljust(80, b"\0")); f.write(struct.pack("<I", len(tris)))
        for a, b, c in tris:
            f.write(struct.pack("<3f", *normal(a, b, c)))
            for p in (a, b, c): f.write(struct.pack("<3f", *p))
            f.write(b"\0\0")

p = argparse.ArgumentParser()
p.add_argument("out"); p.add_argument("--base", type=float, default=80)
p.add_argument("--top", type=float, default=75); p.add_argument("--height", type=float, default=12)
p.add_argument("--count", type=int, default=2); p.add_argument("--gap", type=float, default=10)
a = p.parse_args()
pitch = a.base + a.gap
tris = []
for k in range(a.count):
    cx = (k - (a.count-1)/2) * pitch
    tris += frustum(cx, 0.0, a.base/2, a.top/2, a.height)
write_stl(a.out, tris)
w = (a.count-1)*pitch + a.base
print(f"{a.out}: {a.count} x frustum base {a.base} top {a.top} h {a.height}; footprint {w:.1f} x {a.base:.1f} mm, {len(tris)} triangles")
