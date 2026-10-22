# Installation

## A. Use the included dog in Nexirum

No Python or AI service is needed to install an already-created avatar.

1. Extract the repository ZIP.
2. Find `examples/clay-dog/clay-dog/`.
3. Locate the folder containing `NexirumCompanion.exe` on your Windows computer.
4. Create `resources/avatars/` there if it does not exist.
5. Copy the entire `clay-dog` folder into `resources/avatars/`.

The final catalog location must be:

```text
resources/avatars/clay-dog/animations.json
```

All 14 WebP files must sit beside that JSON file. Avoid an extra nested
`clay-dog/clay-dog/` folder.

6. Open **Personal preferences → Appearance** in Nexirum and select **Clay Dog**.
7. Configure the spoken wake name separately, if you use voice activation.

Keep existing avatars intact. If the new avatar is not listed, check the folder
location and catalog first, then quit and reopen the app.

To preview without installing, open `examples/clay-dog/preview.html` in a browser
after downloading the files. It works offline.

## B. Install the creation skill in your AI agent

1. Find `skills/create-nexirum-avatar/`.
2. Import or copy that **complete folder** into your agent's skills location.
   Do not copy only `SKILL.md`.
3. For a Codex setup using its default local directory, place it under
   `.codex/skills/` inside your user profile. On Windows, browse to your user
   folder and open or create that path.
4. Start a new agent turn/session so it can discover the skill.
5. Ask:

> Use $create-nexirum-avatar to create a friendly clay-style cat. Prepare all 14 states, a preview and the Nexirum avatar package.

If the host does not discover the skill, point it directly at
`skills/create-nexirum-avatar/SKILL.md`.

The agent needs image generation to create new artwork and local Python/file
tools to prepare the package. A text-only agent cannot generate the images.
The skill does not include an image model or API credentials.

## C. Prepare local packing tools

Only needed on the computer or agent environment that builds avatar packages;
these tools do not need to be installed on the Nexirum client just to use a mascot.

- Python 3.10 or newer.
- Pillow, NumPy and SciPy from the supplied `scripts/requirements.txt`.
- ImageMagick with WebP support: `magick`, or `convert` plus `montage`.

Follow the Windows or Linux/macOS commands in [README.md](README.md#local-tools).
Install dependencies in a separate virtual environment; do not change Nexirum's
server dependencies.

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


