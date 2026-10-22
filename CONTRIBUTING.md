# Contributing

Contributions are welcome: clearer instructions, better packing or validation,
new original examples, and compatibility fixes.

## Before a pull request

- Describe the problem and how to reproduce it.
- Keep Nexirum's supplied animation contract intact unless proposing an explicit format change.
- Run `python skills/create-nexirum-avatar/scripts/test_avatar_tool.py`.
- Check any changed avatar with `avatar_tool.py check` and inspect all frames.
- Report file validation, visual review and app testing separately.
- Keep generated outputs, credentials, user paths and caches out of commits.

Use Python for local tooling and browser JavaScript for previews. Do not add
Node.js, hidden API calls, credential discovery, or automatic changes to the
Nexirum application. New artwork should use an image-generation tool rather than
duplicate a static pose to imitate an animation.

For example assets, provide the generation prompts, relevant edits and a concise
verification record. Contribute only material you can share under this
repository's MIT license. Do not submit private user images or conversations.

AI-assisted contributions are welcome. Review generated code and assets before
submitting them.

