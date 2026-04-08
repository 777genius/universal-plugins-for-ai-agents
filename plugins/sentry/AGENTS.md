# Plugin Boundary

This plugin uses the canonical `src/` authoring layout.

- Edit only files under `src/`.
- Start with [`src/README.md`](./src/README.md) for the full plugin guide.
- Read [`GENERATED.md`](./GENERATED.md) before touching plugin-root files. It is the required inventory of managed generated outputs.
- Treat plugin-root `README.md`, manifests, and config files as generated outputs.
- `plugin-kit-ai generate` may overwrite every path listed in `GENERATED.md`.

After changing `src/`, run:

```bash
plugin-kit-ai normalize .
plugin-kit-ai generate .
plugin-kit-ai generate --check .
plugin-kit-ai validate . --platform claude --strict
plugin-kit-ai validate . --platform codex-package --strict
plugin-kit-ai validate . --platform gemini --strict
plugin-kit-ai validate . --platform opencode --strict
plugin-kit-ai validate . --platform cursor --strict
```
