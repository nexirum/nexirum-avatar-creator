# Local helper

Run `python3 scripts/avatar_tool.py --help` from the skill directory, or use the
script's absolute path. Use explicit paths; no environment variables or API keys.

Python dependencies are listed in `scripts/requirements.txt`; ImageMagick is a
separate system dependency. Install missing dependencies only in the intended
skill/tooling environment, not in the client's Nexirum service. Validation alone
does not need NumPy, SciPy, or ImageMagick.

## Fresh installation, starting from a text idea

Use only the installed skill folder and a new working/output directory. Read the
bundled format and catalog, then check image generation and local dependencies
before spending time on all states. A missing tool is an environment limitation;
an existing avatar or sample JSON cannot replace that tool.

1. Generate the character reference from the brief, then a ten-frame pilot and
   the remaining state sheets following generation.md. No example files are needed.
2. Run `plan` on those newly generated sheets using the command pattern below.
   The paths are the new files you just created; the owl name and sample crop
   coordinates below are illustrative, not required assets or reusable geometry.
3. Inspect the actual image geometry, adjust anchors/scale and mark the plan reviewed.
4. Run `pack`. It creates animations.json from the bundled preset, WebP atlases,
   preview.html from the bundled template, contact sheets, instructions and ZIP.
   You do not need to create a starter animations.json or obtain one from the user.
5. Inspect the produced contact sheets and playback; deliver the actual output files
   with the checks and any remaining limitations recorded.

Keep prompts and relevant edits in a creation record using only `tool`, `prompts`
and `notes`. Record decisions from this run rather than relying on earlier chats.

## Existing assets

```bash
python3 scripts/avatar_tool.py check /path/to/avatar
python3 scripts/avatar_tool.py package /path/to/avatar --id owl --out /path/to/new-delivery
```

Check prints JSON, with nonzero exit on incompatibility. Package creates a new
directory with `owl/`, `owl.zip`, `preview.html`, `validation.json`, installation
instructions and contact sheets. ZIP excludes input sheets and private paths.

## New sheets

```bash
python3 scripts/avatar_tool.py plan --id owl --name 'Nexirum Owl' \
  --sheet /path/to/sheet-one.png \
  --rows idle,thinking,listening,talking,happy,warning,sleep \
  --sheet /path/to/sheet-two.png \
  --rows error,success,wake,hello,confused,searching,working \
  --out /path/to/plan.json
```

Inspect and edit the proposed grid. `x_centers` contains ten body anchors;
`y_edges` contains row boundaries including the outer edges. Measure empty gaps
instead of trusting equal spacing. Paths are absolute or relative to the plan.

```json
{
  "avatar_id": "owl",
  "name": "Nexirum Owl",
  "reviewed": true,
  "sheets": [{
    "source": "sheet-one.png",
    "states": ["idle", "thinking", "listening", "talking", "happy", "warning", "sleep"],
    "x_centers": [80,230,380,530,680,830,980,1130,1280,1430],
    "y_edges": [0,150,297,445,595,742,884,1024],
    "scale": 1.0,
    "alpha_levels": null
  }],
  "overrides": {}
}
```

This only illustrates one sheet. Complete plans cover every preset state exactly
once. Coordinates are examples, not a crop map for arbitrary generations.

Use `overrides` when grouping or anchoring needs correction:

```json
"warning:0": {
  "regions": [[30,755,101,123], [137,759,30,33]],
  "anchor_x": 81,
  "baseline_y": 875
}
```

Key: state and zero-based frame. Regions are `[x,y,width,height]` in sheet pixels.
Keep all body parts and symbols; rectangles must exclude neighbouring sprites.
Anchor-only overrides are allowed. Set `reviewed: true` after geometry inspection,
without requiring an additional user confirmation.

Keep `alpha_levels` null normally. For an inspected hazy alpha export, e.g.
`[0.20,0.94]` maps normalized alpha endpoints to zero/full opacity. This cannot
remove a baked background or repair missing surfaces. Scale is uniform per sheet.

```bash
python3 scripts/avatar_tool.py pack /path/to/plan.json --out /path/to/new-delivery \
  --record /path/to/creation.json
```

Optional creation JSON accepts only `tool`, `prompts`, `notes`. Exclude secrets and
local source paths. Output directories must be new. Staging completes validation
before publication. Oversize fails without automatic lossy conversion/frame removal.

Static verification checks format, dimensions, nonempty cells, transparency,
references, timings, transitions, and size. Visual/animation review and real app
testing remain separate. Edge-touch warnings require inspection.

## Maintainer check without example assets

Run `python3 scripts/test_avatar_tool.py` for fast regression checks. With all
packing dependencies available, also run `python3 scripts/test_standalone.py`.
The latter copies only the skill into an isolated folder, makes synthetic test
inputs, and runs the real `plan`, `pack` and `check` commands from a new workspace.
It verifies generated catalog, 14 states of ten distinct frames, alpha, preview and
ZIP without repository examples or an existing animations.json. This is a tooling
integration test, not an image-generation or visual-quality evaluation.
