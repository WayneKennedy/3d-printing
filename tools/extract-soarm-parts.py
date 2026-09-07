#!/usr/bin/env python3
"""Split TheRobotStudio's Ender_Follower_SO101.stl into its 11 individual parts,
preserving the authors' print orientation, and report the overhang that decides
whether each part needs support.

WHY THIS EXISTS: the STLs in STL/SO101/Individual/ are in CAD orientation, NOT
print orientation. Wrist_Roll_Follower is 105.4 mm tall there against 65.2 mm on
the plate; Under_arm flips from 64.4 to 24.0. Only Base matches. Slicing the
Individual/ files discards the authors' support-minimising work, so parts are
extracted from the plate file instead.

Moving_Jaw is two disconnected shells (10878 + 382 triangles) and is written as
one file so the arranger cannot separate the gripper's pieces.

Usage:  extract-soarm-parts.py <Ender_Follower_SO101.stl> <output-dir>
"""
import struct, os, sys, math
from collections import defaultdict

NAMES = {17036:"Wrist_Roll_Pitch", 12056:"Wrist_Roll_Follower", 10508:"Under_arm",
         9558:"Base", 8038:"Upper_arm", 8010:"Motor_holder_Wrist",
         6816:"Base_motor_holder", 6696:"Rotation_Pitch", 5854:"Motor_holder_Base",
         752:"WaveShare_Mounting_Plate"}
JAW = (10878, 382)                       # the two Moving_Jaw shells
THRESH = -math.cos(math.radians(45))     # sub-45deg downward faces need support

def main(src, outdir):
    tris, cur = [], []
    for line in open(src, "r", errors="ignore"):
        s = line.strip()
        if s.startswith("vertex"):
            p = s.split(); cur.append((float(p[1]), float(p[2]), float(p[3])))
            if len(cur) == 3: tris.append(tuple(cur)); cur = []
    print("triangles:", len(tris))

    parent = {}
    def find(x):
        while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]
        return x
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb: parent[ra] = rb
    key = lambda v: (round(v[0],3), round(v[1],3), round(v[2],3))
    for t in tris:
        ks = [key(v) for v in t]
        for k in ks: parent.setdefault(k, k)
        union(ks[0], ks[1]); union(ks[1], ks[2])

    groups = defaultdict(list)
    for i, t in enumerate(tris): groups[find(key(t[0]))].append(i)
    print("connected components:", len(groups), "(11 parts; Moving_Jaw is two shells)")

    out, jaw = {}, []
    for g in groups.values():
        (jaw.extend(g) if len(g) in JAW else out.__setitem__(NAMES[len(g)], g))
    out["Moving_Jaw"] = jaw

    os.makedirs(outdir, exist_ok=True)
    for name, idx in sorted(out.items()):
        with open(os.path.join(outdir, name + ".stl"), "wb") as f:
            f.write(b"\0"*80); f.write(struct.pack("<I", len(idx)))
            for i in idx:
                f.write(struct.pack("<3f", 0, 0, 0))
                for v in tris[i]: f.write(struct.pack("<3f", *v))
                f.write(struct.pack("<H", 0))
        zmin = min(v[2] for i in idx for v in tris[i])
        over = tot = 0.0
        for i in idx:
            (ax,ay,az),(bx,by,bz),(cx,cy,cz) = tris[i]
            ux,uy,uz = bx-ax, by-ay, bz-az
            vx,vy,vz = cx-ax, cy-ay, cz-az
            nx,ny,nz = uy*vz-uz*vy, uz*vx-ux*vz, ux*vy-uy*vx
            mag = math.hypot(nx,ny,nz)
            if mag == 0: continue
            tot += mag/2
            if nz/mag < THRESH and min(az,bz,cz) > zmin+0.3: over += mag/2
        print("  %-26s %6d tri  overhang %6.1f mm2 (%4.1f%%)  %s"
              % (name, len(idx), over, 100*over/tot, "SUPPORTS" if 100*over/tot > 2 else "none"))
    print("\nNOTE: the percentage is a guide, not proof. WaveShare_Mounting_Plate reads 1.7 %")
    print("and still delaminated, because all of it is one cantilevered patch 13 mm up.")
    print("Reprint that part flat with the boss up: 0.0 mm2 overhang. See docs/decisions.md.")

if __name__ == "__main__":
    if len(sys.argv) != 3: print(__doc__); sys.exit(1)
    main(sys.argv[1], sys.argv[2])
