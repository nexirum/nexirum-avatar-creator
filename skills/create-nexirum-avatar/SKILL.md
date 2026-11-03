---
name: create-nexirum-avatar
description: Create animated desktop mascots for Nexirum from an idea, character reference, or sprite sheets. Generate a consistent character and 14 states, pack transparent 256-pixel frames into static WebP atlases, validate the 224 KiB limit, and deliver a preview and installable avatar folder. Also inspect or repackage existing Nexirum avatars. Use for mascot, avatar, robot, dog, cat, or sprite animation requests for Nexirum or its Companion app. Exclude ChatGPT Pets and physical robot firmware.
---

# Nexirum Avatar Creator

Produce a character package for the existing Companion format. Keep the app,
microphones, wake-word models, and user settings outside this workflow. Use the
user's language for names, explanations, and delivery instructions.

## Start

- A short text idea is sufficient to create a new avatar. The installed skill
  contains its format, state definitions, catalog and preview templates, and
  packing tools. No previous avatar, sample JSON, repository example, app source,
  or earlier chat is required. Resolve bundled paths relative to this SKILL.md.
- Use the supplied idea/reference and visible preferences. Ask only when a missing
  choice materially blocks creation; otherwise choose reasonable defaults.
- Complete reference, states, packing, and verification for full-avatar requests.
  Stop at the requested concept for concept-only requests.
- Inspect local reference images before using them. Preserve existing avatars;
  write a new output directory and unique folder ID.
- Do not substitute this workflow for ChatGPT Pets tooling.

Use the host's image-generation tool and applicable image skill for artwork and
semantic edits. Prefer the built-in tool. If unavailable, explain the limitation
and offer prompt preparation or processing existing artwork. Do not silently call
a paid API, request credentials, or create environment variables. This skill has
no model client or network calls.

Local tools require Python 3.10+, Pillow, and ImageMagick (`magick` or `convert`
plus `montage`). Packing sheets also requires NumPy and SciPy. Validation alone
requires Python and Pillow. No Node.js is used. Keep dependency installation
separate from Nexirum production. Use explicit paths and command arguments.

Read [the format](references/nexirum-format.md) and load
[the complete catalog](assets/animations.json) before planning states. This bundled
file is the source of truth: 14 states, 10 frames each, preserved timings, loops,
and transitions. The user need not restate these rules or supply animations.json.
The packer creates it from this preset and the new avatar's display name.

## Generate artwork

Keep image-generation prompts limited to artwork. Build the preview, catalog and
ZIP with the local tools: never ask the image model to draw a delivery package,
file tree, specification poster or mock preview. Text depicting a file is not a
file, and claims printed in an image do not establish transparency or compatibility.

1. If no image was supplied, design the character from the text idea and generate
   its identity reference yourself. Choose unspecified visual details that suit
   the brief; no sample avatar is needed. Create one full-body reference with
   genuine transparency, a readable silhouette,
   and detail appropriate to small size. Respect the style; animals need not be
   robotic, humanoid, or dressed.
2. Reuse this image as the identity reference for every state sheet.
3. Read [generation guidance](references/generation.md) and assign a distinct
   action and visual cue to each preset state, using its baseline behaviours
   even when no reference exists. For a new character or a
   failed attempt, inspect a single ten-frame pilot before generating the remaining
   states. Use the two seven-row layout only when the anatomy and spacing fit it;
   smaller groups are valid. Each row contains ten ordered
   poses for one state. Keep camera, scale, lighting, anatomy, and placement stable.
4. Request real alpha and opaque character surfaces, including dark faces and light
   fur. Exclude printed grids, labels, cast shadows, and baked checkerboards.
   Keep body parts and detached symbols clear of neighbouring poses.
5. Inspect the output before packing. A prompt does not prove valid layout, true
   transparency, motion, or identity consistency. Repair only demonstrated defects.
   Never duplicate a single pose to manufacture ten frames or replace a failed
   state with idle without disclosure.

Preserve the approved character's face, proportions, clothing and accessories.
A style reference does not choose the species. If the user supplies a presentation
board, use its chosen character as an identity reference, not its cropped tiles as
animation frames. Every frame must retain the requested full-body anatomy. Inspect
hands, legs and feet explicitly before continuing; reject source-edge truncation.

Honour explicit reference-approval requests before generating sequences. Otherwise
inspect the reference and continue without an unnecessary confirmation round.
Follow the image tool's display and saving rules; retain the final prompt set.

## Pack and validate

Read [tool usage](references/tool-usage.md). Reuse `scripts/avatar_tool.py` rather
than rewriting the pipeline for each character.

1. Run `plan`. Inspect source sheets and adjust actual row gaps and body centres.
   Generated grids often drift; uniform arithmetic is only a starting proposal.
   Also set a uniform scale per sheet that fits complete poses in 256-pixel cells.
   The proposed scale of 1.0 is not a fit calculation. The pilot is an intermediate
   image review; final `plan` and `pack` require all 14 states.
2. Set `reviewed: true` after that inspection. This is the agent's geometry check,
   not a new user-approval requirement.
3. Run `pack`. It groups disconnected pieces by supplied centres, aligns anchors,
   preserves alpha, and creates lossless WebP. Inspect symbol ownership. Use frame
   overrides where geometry alone cannot assign a symbol or a pose needs a new
   anchor. Do not treat component grouping as semantic proof.
4. Preserve alpha by default. Set `alpha_levels` only for an inspected hazy alpha
   export. It cannot repair missing faces or opaque backgrounds. Use the image tool
   for those defects; never key out black/white parts of a character.
5. Run `check`. Inspect all contact-sheet frames and play every state on light,
   dark, and coloured backgrounds. Check complete silhouettes, symbols, identity,
   unwanted holes, flicker, alignment, loop seams, and one-shot endings.
6. Keep each atlas at or below 229,376 bytes. The packer fails if too large. Do not
   silently remove states, reduce frames or dimensions, or switch to lossy output.
   Simplify the artwork with the image tool or disclose the remaining limitation.

Automatic checks establish file compatibility, not visual or runtime correctness.
Treat `compatible: true` together with `visual_review_required: true` as awaiting
visual review. Record which states and backgrounds were actually inspected, and
any rejected or regenerated sheets. Do not claim missing limbs, interior holes or
animation quality were automatically verified. On a failure, retain accepted
artwork, identify the failing stage and repair that stage without redesigning the
character. Preserve the tool's error if recovery remains blocked.
For existing valid assets, use `check` and `package`; no generation is needed.

## Deliver

Deliver the avatar ZIP and standalone HTML preview. Include a creation record
(tool, prompts, relevant edits) for generated artwork, without private history,
credentials, or local source paths. The preview uses no server, microphone, or AI.

Explain copying `<avatar-id>` into `resources/avatars/` beside the executable and
selecting it in Personal preferences → Appearance. Keep wake-name/Vosk setup
separate. Report actual checks and any visual or runtime limitation.

Use the host's durable artifact-saving mechanism; in ChatGPT Work, save generated
deliverables through Library. Image display alone does not deliver the complete
package. Do not alter the app or publish the skill publicly as a side effect.
