# firebase

`firebase` is a real multi-target MCP plugin in this catalog, modeled after Anthropic's Firebase reference plugin.
It is authored once and generated for `claude`, `codex-package`, `gemini`, `opencode`, and `cursor`.

This plugin uses the canonical `plugin/` layout:

- edit only `plugin/`
- treat the plugin root as generated/native output
- use root `AGENTS.md` as the main boundary doc and `CLAUDE.md` as the Claude-specific pointer
- read `GENERATED.md` before editing root manifest files

## What this plugin does

It registers Firebase via the official `firebase-tools` MCP server command and exposes Firebase project management actions through MCP:

- Firestore operations
- Authentication workflows
- Cloud Functions operations
- Hosting management
- Storage operations

The server is invoked as:

`npx -y firebase-tools@latest mcp`

## Why remote HTTP is not used

This v1 example is intentionally `stdio`-based, matching the published Firebase plugin config and avoiding extra authentication transport wiring for this first-party example.

## Source of truth

Edit only these files by hand:

- `plugin/plugin.yaml`
- `plugin/mcp/servers.yaml`
- `plugin/README.md`

Everything else in plugin root is generated and may be overwritten by `plugin-kit-ai generate`.

## Exact generation flow

From `plugins/firebase`:

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

If you are in the `plugin-kit-ai` source tree, use:

```bash
../plugin-kit-ai/bin/plugin-kit-ai normalize ./plugins/firebase
../plugin-kit-ai/bin/plugin-kit-ai generate ./plugins/firebase
../plugin-kit-ai/bin/plugin-kit-ai generate --check ./plugins/firebase
../plugin-kit-ai/bin/plugin-kit-ai validate ./plugins/firebase --platform claude --strict
../plugin-kit-ai/bin/plugin-kit-ai validate ./plugins/firebase --platform codex-package --strict
../plugin-kit-ai/bin/plugin-kit-ai validate ./plugins/firebase --platform gemini --strict
../plugin-kit-ai/bin/plugin-kit-ai validate ./plugins/firebase --platform opencode --strict
../plugin-kit-ai/bin/plugin-kit-ai validate ./plugins/firebase --platform cursor --strict
```

## Why `codex-package`, not `codex-runtime`

`codex-runtime` is for local runtime-style plugin wiring.
`firebase` is portable MCP, so `codex-package` is the correct target.
