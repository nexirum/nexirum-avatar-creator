# Clay Dog verification

Date: **22 October 2026**

## Technical checks

- 14 states and 140 frames.
- Static WebP atlases, each 2560 × 256 pixels.
- Transparent backgrounds; no empty frames.
- Largest atlas: 195,934 bytes, below 229,376 bytes.
- Catalog references, preset timings, loops and transitions validated.
- All 140 frames visually inspected on light, dark and yellow backgrounds.
- No obvious clipping or unintended transparent areas in the dog.

## App confirmation

After receiving the original dog package, the project owner confirmed that it
works in the Nexirum app. This is a user-reported confirmation, not an automated
integration test or a guarantee for every app version.

The English distribution uses the same 14 atlas files byte for byte. The folder
and display name are changed to `clay-dog` and **Clay Dog**, and the preview and
instructions are in English. These text-only changes were not separately tested
inside the app.

The automatic `validation.json` keeps `app_runtime_tested: false`: the validator
does not run Nexirum. This record provides the separate human confirmation.

## Generation

Three built-in image-generation calls produced one identity reference and two
seven-row sprite sheets. The prompts are in `creation.json`.

Packing used the inspected row boundaries and character anchors in `plan.json`.
Alpha endpoints were normalized from 8% to 98% after inspecting the generated
haze. All 140 poses and the 256-pixel frame dimensions were preserved.

