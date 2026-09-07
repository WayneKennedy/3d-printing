#!/usr/bin/env python3
"""Screen a part's print orientations for support cost, before committing to a slice.

Reports, per orientation:
  bed-support cm3  volume of support actually built FROM THE BED, which is what
                   support_material_buildplate_only = 1 will really produce.
  dropped mm2      overhang area whose support buildplate_only REMOVES because it
                   would rest on the part. That support does not exist, so the
                   overhang prints unsupported -- the WaveShare delamination mode.
                   Low support with high dropped area is a trap, not a win.

Screening only: the slicer is the authority. Validated 2026-09-07 against
Rotation_Pitch, where it predicted X270 over as-extracted by 76x and the slicer
measured 45x (0.12 g of support against 5.39 g). An earlier metric that ignored
buildplate_only called the same comparison 1.3x and pointed the wrong way.

Usage: tools/orientation-study.py <part.stl> [part.stl ...]
"""
import struct, math, os, sys
from collections import defaultdict

def load(p):
    f=open(p,'rb'); f.read(80); n=struct.unpack('<I',f.read(4))[0]
    out=[]
    for _ in range(n):
        d=struct.unpack('<12fH',f.read(50))
        out.append((d[3:6],d[6:9],d[9:12]))
    return out

def rot(v,ax,deg):
    x,y,z=v; a=math.radians(deg); c,s=math.cos(a),math.sin(a)
    if ax=='x': return (x, y*c-z*s, y*s+z*c)
    if ax=='y': return (x*c+z*s, y, -x*s+z*c)
    return v

def norm(t):
    (ax,ay,az),(bx,by,bz),(cx,cy,cz)=t
    ux,uy,uz=bx-ax,by-ay,bz-az; vx,vy,vz=cx-ax,cy-ay,cz-az
    nx,ny,nz=uy*vz-uz*vy, uz*vx-ux*vz, ux*vy-uy*vx
    m=math.sqrt(nx*nx+ny*ny+nz*nz)
    if m==0: return (0.0,0.0,1.0), 0.0
    return (nx/m,ny/m,nz/m), m/2.0

def zat(t,px,py):
    (ax,ay,az),(bx,by,bz),(cx,cy,cz)=t
    d=(by-cy)*(ax-cx)+(cx-bx)*(ay-cy)
    if abs(d)<1e-12: return None
    l1=((by-cy)*(px-cx)+(cx-bx)*(py-cy))/d
    l2=((cy-ay)*(px-cx)+(ax-cx)*(py-cy))/d
    l3=1-l1-l2
    if l1<-1e-9 or l2<-1e-9 or l3<-1e-9: return None
    return l1*az+l2*bz+l3*cz

def analyse(tris):
    zs=[v[2] for t in tris for v in t]; z0,z1=min(zs),max(zs)
    xs=[v[0] for t in tris for v in t]; ys=[v[1] for t in tris for v in t]
    bb=(max(xs)-min(xs), max(ys)-min(ys), z1-z0)
    # bucket triangles by XY cell for the downward ray test
    CELL=3.0; grid=defaultdict(list)
    for i,t in enumerate(tris):
        tx=[v[0] for v in t]; ty=[v[1] for v in t]
        for gx in range(int(min(tx)//CELL), int(max(tx)//CELL)+1):
            for gy in range(int(min(ty)//CELL), int(max(ty)//CELL)+1):
                grid[(gx,gy)].append(i)
    total=oh_area=0.0; from_bed=0.0; on_part=0.0
    for t in tris:
        n,area=norm(t)
        if area==0: continue
        total+=area
        if n[2] >= -0.7071: continue
        cz=(t[0][2]+t[1][2]+t[2][2])/3.0
        if cz-z0 <= 0.5: continue           # sitting on the bed already
        oh_area+=area
        px=(t[0][0]+t[1][0]+t[2][0])/3.0; py=(t[0][1]+t[1][1]+t[2][1])/3.0
        blocked=False
        for i in grid.get((int(px//CELL), int(py//CELL)), ()):
            zz=zat(tris[i],px,py)
            if zz is not None and z0+0.2 < zz < cz-0.2:
                blocked=True; break
        proj=area*abs(n[2])
        if blocked: on_part+=proj
        else:       from_bed+=proj*(cz-z0)   # column volume actually built
    return bb, oh_area/total*100 if total else 0, from_bed/1000.0, on_part

parts=sys.argv[1:]
print(f"{'part':22} {'orientation':13} {'bbox (mm)':24} {'oh%':>5} {'bed-support cm3':>16} {'dropped mm2':>12}")
print("-"*98)
for p in parts:
    base=load(p); name=os.path.basename(p).replace('.stl','')
    rows=[]
    for label,ax,d in [('as-extracted',None,0)]+[(f'{a.upper()}{d}',a,d) for a in ('x','y') for d in (90,180,270)]:
        t = base if ax is None else [tuple(rot(v,ax,d) for v in tri) for tri in base]
        bb,ohp,bedv,onpart = analyse(t)
        rows.append((bedv,label,bb,ohp,onpart))
    rows.sort()
    for bedv,label,bb,ohp,onpart in rows:
        flag=''
        if bb[0]>202 or bb[1]>190: flag=' TOO BIG'
        mark=' <= as-sliced' if label=='as-extracted' else ''
        print(f"{name:22} {label:13} {bb[0]:6.1f}x{bb[1]:6.1f}x{bb[2]:6.1f}  {ohp:5.1f} {bedv:16.2f} {onpart:12.0f}{flag}{mark}")
    print()
