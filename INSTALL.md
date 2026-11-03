# Installation

## A. Install the creation skill in your AI agent

Install only the complete skill folder. The repository's example avatar is
optional: a short character description is enough to start a new creation.

1. Find `skills/create-nexirum-avatar/`.
2. Import or copy that **complete folder** into your agent's skills location.
   Do not copy only `SKILL.md`.
3. For a current Codex setup, place it under `.agents/skills/` inside your user
   profile. On Windows, paste `%USERPROFILE%\.agents\skills\` into File Explorer
   and create that path if it does not exist. The final entrypoint must be
   `%USERPROFILE%\.agents\skills\create-nexirum-avatar\SKILL.md`, with `assets`,
   `references` and `scripts` beside it.
4. Codex detects installed skills automatically. If it does not appear on the
   next turn, restart Codex. See the [official skill documentation](https://learn.chatgpt.com/docs/build-skills).
5. Ask:

> Use $create-nexirum-avatar to create a friendly clay-style cat, with a preview and an installable Nexirum package.

If the host does not discover the skill, point it directly at
`skills/create-nexirum-avatar/SKILL.md`.

The agent needs image generation to create new artwork and local Python/file
tools to prepare the package. A text-only agent cannot generate the images.
The skill does not include an image model or API credentials.

The skill creates its own character reference, state sheets, animations.json,
preview and package. You do not need an existing avatar, sample images, JSON
files, app source code or a previous chat. The bundled catalog specifies all
14 states, frame counts, timings and transitions.

For future updates, replace the contents of this same installed skill folder with
the complete new version. Updating GitHub alone does not update a downloaded copy.

## B. Prepare local packing tools

Only needed on the computer or agent environment that builds avatar packages;
these tools do not need to be installed on the Nexirum client just to use a mascot.

- Python 3.10 or newer.
- Pillow, NumPy and SciPy from the supplied `scripts/requirements.txt`.
- ImageMagick with WebP support: `magick`, or `convert` plus `montage`.

Follow the Windows or Linux/macOS commands in [README.md](README.md#local-tools).
Install dependencies in a separate virtual environment; do not change Nexirum's
server dependencies.

## C. Install a completed avatar in Nexirum

No Python or AI service is needed on the computer that only uses the finished avatar.

1. Extract the delivered avatar ZIP and find the avatar folder containing
   `animations.json` and its 14 WebP files.
2. Copy that entire folder into `resources/avatars/` beside `NexirumCompanion.exe`.
   Keep the JSON and WebPs together, without adding an extra nested avatar folder.
3. Select the avatar in **Personal preferences → Appearance**.

Open the delivered `preview.html` in a browser to inspect it without installing
the app; it works offline. Keep existing avatars intact. If the new avatar is not
listed, check its location and catalog before restarting the app. Configure the
spoken wake name separately if you use voice activation.

The repository's optional demonstration can be installed the same way: copy
`examples/clay-dog/clay-dog/` into `resources/avatars/` and select **Clay Dog**.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Skill is not discovered | Folder contains `SKILL.md`, scripts, assets and references; open a new agent session. |
| Image generation unavailable | Use an image-capable host or supply existing sprite sheets. |
| Python module missing | Install the requirements with the same Python executable used to run the script. |
| ImageMagick unavailable | Install it separately; pip does not install it. |
| Atlas exceeds 224 KiB | Review/simplify the artwork; do not remove required states or frames silently. |
| Face or body looks transparent | Inspect the generated source. Do not remove white or black by colour to create transparency. |
| Avatar does not appear in Nexirum | Verify the folder beside the executable and every atlas filename referenced by `animations.json`. |


