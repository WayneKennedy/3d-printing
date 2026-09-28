"""Tessellate ZeroG's Mercury One.1 + Hydra (Ender 5 Plus) STEP into a browser 3D viewer.

    uv run python build.py            # fetch (if needed), build, serve on :8018 (0.0.0.0)
    uv run python build.py --build    # build only
    uv run python build.py --serve    # serve an existing build

Source: ZeroGDesign/Hydra `CAD/Hydra_5Plus.zip` at a pinned commit — one STEP of the whole
printer (Ender 5 Plus frame, Mercury One.1 gantry, EVA toolhead, Hydra bed/Z). CC BY-NC-SA 4.0;
the STEP and the generated geometry are NOT committed (build/ and scratch/ are ignored).
Output: build/cad-viewer/{index.html, three-r128.min.js, scene.json, geometry.bin}.
Viewer pattern follows koala-bot's hardware viewer (Three.js r128, vendored, Z up).
"""
import argparse
import http.server
import io
import json
import pathlib
import re
import shutil
import sys
import time
import urllib.request
import zipfile

import numpy as np
from build123d import import_step
from OCP.BRep import BRep_Tool
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.BRepTools import BRepTools
from OCP.TopAbs import TopAbs_FACE, TopAbs_REVERSED
from OCP.TopExp import TopExp_Explorer
from OCP.TopLoc import TopLoc_Location
from OCP.TopoDS import TopoDS

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
CACHE = REPO / "scratch" / "cad"
OUT = REPO / "build" / "cad-viewer"

HYDRA_COMMIT = "a062dbd6c4fc725d48c27dabbcf4aa78a7b9b8d5"   # ZeroGDesign/Hydra, 2025-05-15
ZIP_URL = f"https://github.com/ZeroGDesign/Hydra/raw/{HYDRA_COMMIT}/CAD/Hydra_5Plus.zip"
LINEAR, ANGULAR = 0.8, 0.6          # mm, rad — display tessellation, not a manufacturing mesh
FAST_LINEAR, FAST_ANGULAR = 2.0, 1.2   # fasteners: modelled threads dominate the triangle count

FASTENER = re.compile(r"screw|shcs|schc|bhcs|fhcs|tnut|t-nut|washer|heatset|heat_set|nut\b|_nut|"
                      r"dowel|m[2-5][-_x]|din_912|iso_|rivet|zip", re.I)
CATEGORIES = {   # colour per category; a group's category is decided in categorise()
    "Hydra": "#e05a5a", "Mercury": "#4fb3a0", "Toolhead": "#b36bd6",   # none orange/steel: those mean printed/bought
    "Frame": "#8a939d", "Electrics": "#d6c34f", "Accessories": "#7fbf7f",
}
FASTENER_COLOUR = "#5d6670"

# Printed vs bought (owner, 2026-09-28: "colour the parts we'd print separately from the parts we
# buy"). Walk from the leaf up its assembly path; the NEAREST segment matching either list wins,
# so an MGN9C carriage inside a printed Hydra arm is bought and the arm body is printed. Printed
# names come from ZeroG's published STLs (MercuryOne@8030dc6 STLs/, Hydra STLs/) as they appear
# in this CAD. Anything matching neither is "unclassified" and drawn in a warning colour — the
# viewer never guesses. Fasteners are bought.
PRINTED = re.compile(r"xjoint_[lr]_(top|bottom)|flangestack_sapcer|front_tower_(left|right)|"
                     r"tension_plate|stepper_bottom|stepper_towers|y_endstop_v|x_endstop_block|"
                     r"rear_?cable_?arm|belt_clamp|bl_touch_mount|^face_rapido$|trihorn|eva2-4|"
                     r"eva_backplate|eva_frontplate|(hydra|hidera)_(left|right|rear)_arm|n17mount|"
                     r"^mt_12x|^mini_tank$|chainend|clip_top|zerog_callibration|"
                     r"^sk_(438|455|centerlogo|ft_)|^component1$|din_dropbracket|cable_tie|"
                     r"idler_spacers|xjoint_stop", re.I)
BOUGHT = re.compile(r"nema|motor_coupler|^assembly_1_<3>$|mgn|^rail$|gt2_|idler|xyjoint_20t|"
                    r"flange_stack|f695|shim|pin_5|_pin|dowel|magnet(?!_clip)|kossel|tr8|leadscrew|"
                    r"heater|^pei$|belt_5plus|d2f|^switch$|bl-touch|5015|_fan|capricorn|ptfe|"
                    r"push-to-connect|^spool$|wire|rapdio|^\[assembly\]_face_rapido|lgx|drag_chain|"
                    r"^segment|male_end|2020|2040|vslot|t-slot|extrusion|_bed_3|toppanel|bottompanel|"
                    r"^500_v|wago|hydra_frame|pulley|rubber_foot|iec_fused", re.I)
CLASS_COLOURS = {"printed": "#e89a3c", "bought": "#7f9bb3", "fastener": FASTENER_COLOUR,
                 "unclassified": "#e0457b"}


def source_of(path: list[str], fastener: bool) -> str:
    if fastener:
        return "fastener"
    for seg in reversed(path):
        if PRINTED.search(seg):
            return "printed"
        if BOUGHT.search(seg):
            return "bought"
    return "unclassified"


def fetch_step() -> pathlib.Path:
    step = CACHE / "Hydra_5Plus.stp"
    if step.exists():
        return step
    CACHE.mkdir(parents=True, exist_ok=True)
    print(f"fetching {ZIP_URL}", file=sys.stderr)
    data = urllib.request.urlopen(ZIP_URL, timeout=300).read()
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        z.extract("Hydra_5Plus.stp", CACHE)
    return step


def categorise(path: list[str]) -> str:
    top = path[0]
    if top.startswith("Ender_5_Plus_Hydra_Frame"):
        sub = path[2] if len(path) > 2 else ""
        if re.match(r"Hydra_Frame|5Plus_Hydra_TopPanel|5_plus_v", sub):
            return "Frame"
        if sub.startswith("Wago"):
            return "Electrics"
        return "Hydra"
    if top == "X_Gantry" and len(path) > 1 and path[1].startswith("ToolHead"):
        return "Toolhead"
    if re.match(r"Spool|ptfe|5plus_Skirt|DIN_|500_v|Cable_Tie", top):
        return "Accessories"
    return "Mercury"


def group_name(path: list[str]) -> str:
    top = path[0]
    if top.startswith("Ender_5_Plus_Hydra_Frame") and len(path) > 2:
        return path[2]
    if top == "X_Gantry" and len(path) > 1 and path[1].startswith("ToolHead"):
        return "ToolHead (EVA)"
    return top


def mesh(shape, lin=LINEAR, ang=ANGULAR) -> tuple[np.ndarray, np.ndarray]:
    """Triangulate one located leaf; faces OCC cannot mesh are skipped, not the whole part."""
    w = shape.wrapped
    BRepTools.Clean_s(w)             # drop any finer triangulation carried in from the import
    BRepMesh_IncrementalMesh(w, lin, False, ang, True)
    pos, idx, base = [], [], 0
    exp = TopExp_Explorer(w, TopAbs_FACE)
    while exp.More():
        face = TopoDS.Face(exp.Current())
        loc = TopLoc_Location()
        tri = BRep_Tool.Triangulation_s(face, loc)
        exp.Next()
        if tri is None:
            continue
        trsf = loc.Transformation()
        nodes = [tri.Node(i).Transformed(trsf) for i in range(1, tri.NbNodes() + 1)]
        pos.extend((p.X(), p.Y(), p.Z()) for p in nodes)
        rev = face.Orientation() == TopAbs_REVERSED
        for i in range(1, tri.NbTriangles() + 1):
            a, b, c = tri.Triangle(i).Get()
            idx.append((base + a - 1, base + c - 1, base + b - 1) if rev
                       else (base + a - 1, base + b - 1, base + c - 1))
        base += len(nodes)
    return np.asarray(pos, np.float32).reshape(-1, 3), np.asarray(idx, np.uint32).reshape(-1, 3)


def build() -> None:
    step = fetch_step()
    t = time.time()
    root = import_step(str(step))
    print(f"read {step.name} in {time.time() - t:.0f}s", file=sys.stderr)

    leaves = []
    def walk(s, path):
        kids = list(s.children)
        if not kids:
            leaves.append((s, path))
        for k in kids:
            walk(k, path + [k.label])
    walk(root, [])

    OUT.mkdir(parents=True, exist_ok=True)
    blobs = {"geometry.bin": io.BytesIO(), "fasteners.bin": io.BytesIO()}
    items, groups, skipped = [], {}, 0
    t = time.time()
    for shape, path in leaves:
        name = path[-1]
        fastener = bool(FASTENER.search(name)) or any(FASTENER.search(p) for p in path[1:-1])
        try:
            v, f = mesh(shape, *((FAST_LINEAR, FAST_ANGULAR) if fastener else (LINEAR, ANGULAR)))
        except Exception as exc:          # a malformed body: report, do not invent geometry
            print(f"skip {'/'.join(path)}: {exc}", file=sys.stderr)
            skipped += 1
            continue
        if not len(f):
            skipped += 1
            continue
        cat = categorise(path)
        grp = group_name(path)
        src = source_of(path, fastener)
        g = groups.setdefault(grp, {"name": grp, "category": cat, "parts": 0, "tris": 0})
        g["parts"] += 1
        g["tris"] += int(len(f))
        lo, hi = v.min(0), v.max(0)
        fname = "fasteners.bin" if fastener else "geometry.bin"
        blob = blobs[fname]
        pos_off = blob.tell(); blob.write(v.tobytes())
        idx_off = blob.tell(); blob.write(f.tobytes())
        items.append({
            "name": name, "group": grp, "category": cat, "fastener": fastener, "source": src,
            "path": "/".join(path[:-1]),
            "colour": FASTENER_COLOUR if fastener else CATEGORIES[cat],
            "source_colour": CLASS_COLOURS[src],
            "file": fname, "pos": [pos_off, int(len(v))], "idx": [idx_off, int(len(f))],
            "size": [round(float(x), 1) for x in (hi - lo)],
            "min": [round(float(x), 1) for x in lo], "max": [round(float(x), 1) for x in hi],
        })
    for fname, b in blobs.items():
        (OUT / fname).write_bytes(b.getvalue())
    scene = {
        "title": "Mercury One.1 + Hydra — Ender 5 Plus",
        "source": f"ZeroGDesign/Hydra@{HYDRA_COMMIT[:7]} CAD/Hydra_5Plus.zip (CC BY-NC-SA 4.0)",
        "tessellation": {"linear_mm": LINEAR, "angular_rad": ANGULAR},
        "categories": CATEGORIES, "fastener_colour": FASTENER_COLOUR, "class_colours": CLASS_COLOURS,
        "groups": sorted(groups.values(), key=lambda g: (list(CATEGORIES).index(g["category"]), g["name"])),
        "items": items, "skipped": skipped,
    }
    (OUT / "scene.json").write_text(json.dumps(scene))
    shutil.copy(HERE / "viewer.html", OUT / "index.html")
    shutil.copy(HERE / "vendor" / "three-r128.min.js", OUT / "three-r128.min.js")
    tris = sum(i["idx"][1] for i in items)
    from collections import Counter
    print("source:", dict(Counter(i["source"] for i in items)), file=sys.stderr)
    tr = Counter()
    for i in items: tr[i["source"]] += i["idx"][1]
    print("triangles by source:", dict(tr), file=sys.stderr)
    for i in items:
        if i["source"] == "unclassified":
            print(f"  unclassified: {i['path']}/{i['name']}", file=sys.stderr)
    print(f"{len(items)} parts, {tris} triangles, {skipped} skipped, "
          + ", ".join(f"{k} {len(b.getvalue()) / 1e6:.1f} MB" for k, b in blobs.items())
          + f", {time.time() - t:.0f}s", file=sys.stderr)


def serve(port: int) -> None:
    handler = lambda *a, **k: http.server.SimpleHTTPRequestHandler(*a, directory=str(OUT), **k)
    print(f"serving {OUT} on http://0.0.0.0:{port}/", file=sys.stderr)
    http.server.ThreadingHTTPServer(("0.0.0.0", port), handler).serve_forever()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--build", action="store_true", help="build only")
    ap.add_argument("--serve", action="store_true", help="serve an existing build only")
    ap.add_argument("--port", type=int, default=8018)
    a = ap.parse_args()
    if not a.serve:
        build()
    if not a.build:
        serve(a.port)
