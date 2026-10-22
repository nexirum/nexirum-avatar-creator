# Nexirum Companion format

Contract supplied by the app owner on 22 October 2026. Recheck against the app if
its loader changes; these are not universal sprite rules.

Copy one folder beneath `resources/avatars/` beside `NexirumCompanion.exe`, e.g.
`resources/avatars/owl/animations.json` and the referenced WebPs. Discovery is
automatic; external avatar folders do not require recompilation. Select one in
Personal preferences → Appearance. JSON `name` supplies the display name; the
spoken wake name is configured separately.

Use a simple ASCII folder ID without spaces/accents. The helper conservatively
allows lowercase letters, digits, and single hyphens, up to 64 characters, excluding
Windows device names. This extra restriction belongs to the helper.

- Static WebP, one horizontal row of frames per atlas, with alpha.
- Cells exactly 256 × 256 pixels; supplied preset has 10, so atlas is 2560 × 256.
- Maximum 224 KiB = 229,376 bytes per atlas, measured on the actual file.
- Include every referenced WebP; local basenames only.
- Preserve preset states, timings, loops, and nextState unless the app contract changes.
- Exclude executable code, Vosk models, credentials, and microphone logic.

The helper validates the complete supplied preset; it does not claim the app
rejects every other possible configuration.

| State | ms per frame | Loop | Next |
|---|---:|---|---|
| idle | 1200 | yes | — |
| thinking | 800 | yes | — |
| listening | 700 | yes | — |
| talking | 450 | yes | — |
| happy | 650 | yes | — |
| warning | 650 | yes | — |
| sleep | 1200 | yes | — |
| error | 700 | yes | — |
| success | 650 | no | idle |
| wake | 750 | no | idle |
| hello | 650 | no | idle |
| confused | 800 | yes | — |
| searching | 650 | yes | — |
| working | 550 | yes | — |

Preview speed does not edit the preset. Packing uses baseline y=239 and horizontal
anchor x=128, matching the rabbit/owl. Review anchors for floating/lying poses;
do not resize each individual pose to fill the cell.
