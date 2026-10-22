# Generation and visual review

## Reference

Define the requested species/object, personality, proportions, silhouette, style,
materials, and palette. Avoid unrelated accessories. Generate one full-body
reference and reuse it explicitly as identity input for all sequences.
Retain the tool and prompt set in the creation record.

## Sheet scaffold

```text
Use case: stylized-concept
Asset type: animation sprite sheet for a desktop companion
Identity: preserve the supplied reference's face, proportions, materials,
colours, anatomy, and accessories in every pose.
Canvas: 1536×1024, exactly 10 columns and 7 rows, one state per row.
Camera: fixed full-body view, same scale and placement throughout.
Background: genuinely transparent; opaque interiors including dark faces and
light fur; no grid, labels, floor, cast shadow, or checkerboard.
Layout: invisible cells with clear gaps; every body part and optional symbol
inside its own cell. Prefer modest gestures and readable, simple detail.
Motion: ten ordered poses per row, common ground line, smooth loop closure.
Do not draw ten unrelated poses. One-shot states end compatible with idle.
Rows in this exact order: [insert seven behaviours below].
```

Adapt dimensions and group count to the tool. Requested layout is not proof of
actual layout. Use smaller groups when count or identity repeatedly drifts.

| Sheet | State | Behaviour |
|---|---|---|
| 1 | idle | Calm breathing, brief blink, closed loop. |
| 1 | thinking | Thoughtful head/ear movement or gaze. |
| 1 | listening | Attentive gaze, gentle tilt, optional sound arcs. |
| 1 | talking | Subtle mouth/beak motion and conversational gesture. |
| 1 | happy | Joyful but restrained expression/body language. |
| 1 | warning | Calm alert, optional amber symbol. |
| 1 | sleep | Relaxed posture and closed eyes. |
| 2 | error | Technical concern distinct from warning; avoid despair. |
| 2 | success | Brief affirmative gesture, ending compatible with idle. |
| 2 | wake | Sleep to awake, ending compatible with idle. |
| 2 | hello | Brief greeting, ending compatible with idle. |
| 2 | confused | Curious uncertainty, not anger. |
| 2 | searching | Small scanning gaze/head movement. |
| 2 | working | Concentrated activity, not irritation. |

Adapt anatomy: dogs can use ears/tail/body; cats can use gaze/ears/posture. Do not
force hands or humanoid stances. Review large pose changes and sleep/wake anchors.

## Review

Count rows/poses; inspect identity, scale, lighting, accessories, and camera across
sheets. View light/dark/coloured backgrounds and verify white/black surfaces remain
solid. Watch loops and one-shot endings; static checks cannot prove smoothness.
Inspect detached symbols separately. Component assignment is geometric assistance,
not proof of ownership. Override ambiguous crops or repair with the image tool.
Make targeted repairs and preserve previously accepted states.
