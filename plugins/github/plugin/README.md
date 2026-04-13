# github

`github` is a real multi-target MCP plugin in this catalog and mirrors the official reference from Anthropic's external GitHub plugin.
It is authored once and generated for `claude`, `codex-package`, `gemini`, `opencode`, and `cursor`.

This plugin uses the canonical `plugin/` authoring layout:

- edit only `plugin/`
- treat the plugin root as generated/native output
- use root `AGENTS.md` as the main boundary doc, `CLAUDE.md` as the Claude-specific pointer, and `GENERATED.md` before touching generated artifacts
- read `GENERATED.md` before editing plugin-root files

## What this plugin does

It connects agents to GitHub through the official `github` MCP endpoint:

- search and inspect repositories
- manage issues and pull requests
- review files and code
- use GitHub API capabilities from agent tools

## Source of truth

Edit only these files by hand:

- `plugin/plugin.yaml`
- `plugin/mcp/servers.yaml`
- `plugin/README.md`

Everything else at plugin root is generated and may be overwritten by `plugin-kit-ai generate`.

## Exact authored files

```bash
cat plugin/plugin.yaml
cat plugin/mcp/servers.yaml
```

`plugin/plugin.yaml` defines shared metadata and target list.
`plugin/mcp/servers.yaml` defines remote MCP transport and GitHub auth header placeholder.

## Exact generation flow

Run from `plugins/github`:

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
../plugin-kit-ai/bin/plugin-kit-ai normalize ./plugins/github
../plugin-kit-ai/bin/plugin-kit-ai generate ./plugins/github
../plugin-kit-ai/bin/plugin-kit-ai generate --check ./plugins/github
../plugin-kit-ai/bin/plugin-kit-ai validate ./plugins/github --platform claude --strict
../plugin-kit-ai/bin/plugin-kit-ai validate ./plugins/github --platform codex-package --strict
../plugin-kit-ai/bin/plugin-kit-ai validate ./plugins/github --platform gemini --strict
../plugin-kit-ai/bin/plugin-kit-ai validate ./plugins/github --platform opencode --strict
../plugin-kit-ai/bin/plugin-kit-ai validate ./plugins/github --platform cursor --strict
```

## Expected generated outputs

After `plugin-kit-ai generate .`, the plugin root should contain:

- `GENERATED.md`
- `README.md`
- `.claude-plugin/plugin.json`
- `.codex-plugin/plugin.json`
- `.mcp.json`
- `gemini-extension.json`
- `opencode.json`
- `.cursor/mcp.json`

`GENERATED.md` is the generated inventory of all root-managed outputs.

## Why remote HTTP for v1

GitHub MCP in the official plugin is remote and auth-driven; this first-class example shows how to project streamable HTTP with headers for all five targets.

## Why local stdio / remote in this step

`context7` uses local stdio because no auth header is required.
`github` uses remote HTTP because the official endpoint expects a tokened remote transport.

For now, this plugin is intentionally v1 and only includes the shared remote baseline.

To extend later, add target overrides for custom headers/model hints in `mcp/servers.yaml` overrides, keeping this base path as the default.
