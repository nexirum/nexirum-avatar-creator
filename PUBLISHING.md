# Publish on GitHub

Suggested repository name: **nexirum-avatar-creator**

Suggested description:

> AI-assisted creation and validation of animated desktop mascots for Nexirum Companion.

Suggested topics: `nexirum`, `agent-skills`, `avatars`, `sprite-animation`, `python`, `webp`.

## From the ZIP

1. Extract the distribution ZIP on your computer.
2. Open its `nexirum-avatar-creator` folder.
3. Create an empty public repository in your GitHub account or the Nexirum organization.
4. Upload the **contents** of this folder, so `README.md`, `LICENSE`, `skills/` and `examples/` appear at the repository root.
5. Include the hidden `.gitignore` and `.gitattributes` files.
6. Check that the README's image and relative links open correctly.

Uploading only the ZIP will not expose the skill files and README as a normal
repository. You may add the ZIP separately as a release download afterwards.

This distribution contains no Git history, remote configuration, credentials
or private workspace paths. No repository has been created or published by
preparing this package.

## Optional local Git commands

Run inside the extracted folder:

```sh
git init
git add .
git commit -m "Initial release of Nexirum Avatar Creator"
git branch -M main
```

Then use the remote URL shown by your new GitHub repository and follow GitHub's
instructions to connect and push. Do not overwrite a repository that already
contains unrelated work.

