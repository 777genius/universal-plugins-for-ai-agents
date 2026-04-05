# context7

`context7` is a real portable MCP plugin in this catalog.
It shows the fastest clean path for authoring one plugin once and generating working outputs for `claude`, `codex-package`, `gemini`, `opencode`, and `cursor`.

This plugin uses the canonical `src/` layout:

- edit only `src/`
- treat the plugin root as generated/native output
- use root `CLAUDE.md` and `AGENTS.md` as boundary docs for humans and agents

## What This Plugin Does

It installs the official `@upstash/context7-mcp@2.1.6` server through local `stdio` and projects it into five targets from one authored source.

## Source Of Truth

Author only these files by hand:

- `src/plugin.yaml`
- `src/mcp/servers.yaml`
- `src/README.md`

For this plugin there is no `src/targets/codex-package/package.yaml`, because shared package metadata now lives in `src/plugin.yaml`.

Everything else in the plugin root is generated and may be overwritten by `plugin-kit-ai generate`.

## Exact Commands

Run from this repository root:

```bash
cd plugins/context7
plugin-kit-ai normalize .
plugin-kit-ai generate .
plugin-kit-ai generate --check .
plugin-kit-ai validate . --platform claude --strict
plugin-kit-ai validate . --platform codex-package --strict
plugin-kit-ai validate . --platform gemini --strict
plugin-kit-ai validate . --platform opencode --strict
plugin-kit-ai validate . --platform cursor --strict
```

If you are working from the `plugin-kit-ai` source repo instead of a globally installed CLI, use its built binary against this directory:

```bash
../plugin-kit-ai/bin/plugin-kit-ai normalize ./plugins/context7
../plugin-kit-ai/bin/plugin-kit-ai generate ./plugins/context7
```

## Generated Outputs

`plugin-kit-ai generate .` writes these managed root artifacts:

- `README.md`
- `.claude-plugin/plugin.json`
- `.codex-plugin/plugin.json`
- `.mcp.json`
- `gemini-extension.json`
- `opencode.json`
- `.cursor/mcp.json`

`README.md` is the generated mirror of this file.
The shared `.mcp.json` is consumed by both Claude and Codex package outputs.

## Why `claude` Works Without `launcher.yaml`

This plugin intentionally has:

- no `src/launcher.yaml`
- no `hooks/hooks.json`

That is valid because the Claude target now supports package-only mode when the plugin only uses package/config surfaces such as portable MCP and optional package metadata.

## Why `codex-package`, Not `codex-runtime`

`codex-runtime` is the repo-local notify/runtime lane.
`context7` is a portable MCP package, so `codex-package` is the correct target.

## Why Local `stdio`, Not Remote HTTP

This v1 example intentionally uses local `stdio`:

- it matches the official Claude `context7` plugin shape more closely
- it avoids API key and remote auth wiring in the first universal example
- it keeps the example deterministic and easy to copy

## How To Extend Later

Possible next steps, but intentionally out of scope for this v1 example:

- switch or add a remote MCP transport
- wire API-key-based auth headers
- add more target-native metadata where it gives real value

Keep v1 small first.
