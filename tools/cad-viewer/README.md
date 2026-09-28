# cad-viewer — Mercury One.1 + Hydra (Ender 5 Plus) in the browser

Interactive 3D view of ZeroG's whole-printer STEP for the 5P CoreXY project
([docs/projects/5p-corexy.md](../../docs/projects/5p-corexy.md)). Same pattern as koala-bot's
hardware viewer: a Python build step tessellates the CAD into `scene.json` + binary geometry, and a
single static `viewer.html` renders it with Three.js r128 (vendored, MIT — `vendor/THREE-LICENSE`).

```sh
cd tools/cad-viewer
uv run python build.py            # fetch STEP if missing, build, serve on 0.0.0.0:8018
uv run python build.py --build    # rebuild only;  --serve  serve an existing build
```

Open `http://<host>:8018/` — on the tailnet, e.g. `http://blake:8018/` (verified 2026-09-28).
Needs `uv`; first run installs build123d/OCP (~hundreds of MB) into `.venv/`.

- **Source:** `ZeroGDesign/Hydra` `CAD/Hydra_5Plus.zip` pinned at `a062dbd`, one STEP AP214
  (132 MB, "Hydra 370 Assembly", Autodesk export) of the **whole printer** — frame, Mercury One.1
  gantry, EVA toolhead (Rapido + LGX Lite), Hydra bed/Z, skirts and accessories. CC BY-NC-SA 4.0:
  the STEP (`scratch/cad/`) and the build (`build/cad-viewer/`) are **not committed**.
- **Output:** 1060 parts; `geometry.bin` 23 MB (display mesh 0.8 mm / 0.6 rad), `fasteners.bin`
  13.5 MB (2.0 mm / 1.2 rad — modelled threads dominate) loaded only when Fasteners is switched on.
  **Placement is verified on every build:** each placed solid must match a solid from OCC's
  plain STEP reader (independent of the assembly traversal) within 1 mm — 1153 of 1153 match, or
  the build stops.
- **Trap (found 2026-09-28):** build123d's `import_step` leaves each child in its parent's frame
  (`.wrapped` carries only its own location). The first build used those shapes directly and
  1019 of 1153 solids rendered in local coordinates — "floating parts". An earlier check
  compared meshes with build123d's own bounding boxes, which share the error, so it passed.
  `build.py` now composes every ancestor's location and `verify()` guards it.
- **Printed vs bought** (default colouring): nearest assembly-path segment matching the
  `PRINTED` or `BOUGHT` patterns in `build.py` wins; printed names come from ZeroG's published STL
  lists. 74 printed, 318 bought, 668 fasteners, 0 unclassified. Anything unmatched would be drawn
  in pink as "unclassified" — the build prints them; extend the patterns, don't guess.
- "Hidera_*" is ZeroG's spelling on real parts (right arm, right/rear motor mounts, bed plate),
  not copies. The "stray rail / loose spool / floating inserts" first reported were the placement
  bug above, not ZeroG's model.
- Orientation: Z up; front is −Y (the rear Z motor is +Y).
