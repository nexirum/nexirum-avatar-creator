# Generation and visual review

## Reference

When starting from text alone, turn the brief into a compact character design:
species/object, body arrangement, face, distinctive features, material and palette.
Choose reasonable defaults for unspecified details and generate the reference.
This reference is an output of the workflow, not an input the user must provide.
Use a supplied image when there is one; avoid searching previous avatars or chats
to fill a requirement the installed skill already defines.

Define the requested species/object, personality, proportions, silhouette, style,
materials, and palette. A show's visual style does not by itself specify its
animal species. Preserve user-approved clothing and accessories; avoid adding
unrelated ones. Generate one full-body
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

For a new character, first inspect one ten-frame pilot row. Adapt dimensions and
group count to the tool and body proportions. The seven-row scaffold is a layout
option, not a requirement. Include visible transparent margins at all four outer
edges as well as between poses. Requested layout is not proof of actual layout.
Reject cropped feet, hands, ears or heads; smaller groups or another canvas shape
may be needed. Preserve accepted artwork when repairing only a failed state.

Use these behaviours without needing an example image. Choose the suggested cue
when useful, or an equally legible alternative suited to the character. Symbols
are not mandatory when the action already reads clearly. Keep one visual style
for the chosen cues and leave room for them in every affected frame.

| Sheet | State | Baseline action | Suggested distinguishing cue |
|---|---|---|---|
| 1 | idle | Calm breathing and a brief blink, closed loop. | Neutral pose; no status symbol. |
| 1 | thinking | Gaze shifts up; head tilts; hand/paw to chin if appropriate. | Small thought dots or a thoughtful ear pose. |
| 1 | listening | Alert ears/gaze; lean or turn toward a sound. | Blue sound arcs beside an ear/headset. |
| 1 | talking | Clearly changing mouth/beak shapes and a conversational gesture. | Speech strokes beside the mouth. |
| 1 | happy | Smile and joyful hand, ear, wing or tail motion. | Thumbs-up or a small celebratory sparkle. |
| 1 | warning | Attentive caution gesture or upright alert posture. | Amber caution symbol. |
| 1 | sleep | Closed eyes, relaxed posture, slow breathing. | Gently drifting Zzz. |
| 2 | error | Concern, pause or shrug, distinct from warning. | Red error symbol; avoid despair. |
| 2 | success | Show an affirmative gesture, then return to neutral. | Green check mark. |
| 2 | wake | Closed to open eyes; stretch; settle awake. | Brief waking rays that disappear at the end. |
| 2 | hello | Wave a hand/paw/wing or give a friendly bow, then settle. | Greeting gesture remains the main cue. |
| 2 | confused | Curious head tilt and questioning gaze or open palm. | Question mark. |
| 2 | searching | Scan left and right with gaze/head and a searching action. | Magnifier, floating if anatomy needs it. |
| 2 | working | Visible repeated typing, tool use or another focused task. | Small laptop, tool or progress indicator. |

For each row, describe the ordered motion: initial pose, anticipation, main action,
recovery and ending. Vary the action across the ten frames, rather than relying on
texture changes or moving only the whole sprite. Looping rows should close smoothly;
success, wake and hello end in a pose compatible with idle. Their transition rules
and timings come from assets/animations.json, not from this artistic cue table.

Adapt anatomy: dogs can use ears/tail/body; cats can use gaze/ears/posture. Do not
force hands or humanoid stances. Review large pose changes and sleep/wake anchors.

## Review

Before expanding a pilot into all states, define the visible cue for each state.
Preserve symbols and props from a user-approved reference when they explain the
state: for example sound arcs, an alert, a check mark, a question mark, a magnifier
or a laptop. Match the requested style and reserve space for them inside each
frame. Do not erase this vocabulary merely to simplify packing. Restrained motion
does not mean indistinguishable states: review representative frames side by side
at actual display size and ensure they communicate different behaviours.

Count rows/poses; inspect identity, scale, lighting, accessories, and camera across
sheets. View light/dark/coloured backgrounds and verify white/black surfaces remain
solid. Watch loops and one-shot endings; static checks cannot prove smoothness.
Inspect detached symbols separately. Component assignment is geometric assistance,
not proof of ownership. Override ambiguous crops or repair with the image tool.
Make targeted repairs and preserve previously accepted states.
