# statsig

`statsig` is a real portable MCP plugin in this catalog.
It packages Statsig's hosted MCP server once and projects it into `claude`, `codex-package`, `gemini`, `opencode`, and `cursor`.

This plugin uses the canonical `plugin/` layout:

- edit only `plugin/`
- treat the plugin root as generated and target-native output
- use root `AGENTS.md` as the main boundary doc, `CLAUDE.md` as the Claude pointer, and `GENERATED.md` before touching plugin-root files

## What This Plugin Does

This plugin connects agents to Statsig's hosted MCP service at `https://api.statsig.com/v1/mcp`.
It is designed for interactive, user-authorized access to Statsig experiments, gates, configs, metrics, and audit data through OAuth.

Typical use cases:

- inspect and summarize experiment status
- list stale feature flags and cleanup candidates
- review config and metric definitions
- create or update Statsig entities when the authenticated account has write permissions

## Why This Plugin Targets Five MCP Clients

This is an intentionally broad but still evidence-backed plugin.

Statsig's official MCP docs currently publish setup guides for Codex, Cursor, and Claude Code, and also document manual setup for any MCP-compatible tool.
Because this plugin only uses a standard hosted remote MCP endpoint, it cleanly projects into the full remote package set used by this catalog:

- `claude`
- `codex-package`
- `gemini`
- `opencode`
- `cursor`

We are not claiming first-party marketplace listing inside every vendor client.
We are only claiming that the official Statsig MCP endpoint is standard enough to package honestly for these supported remote targets.

## Source Of Truth

Author only these files by hand:

- `plugin/plugin.yaml`
- `plugin/mcp/servers.yaml`
- `plugin/README.md`

Everything else in the plugin root is generated and may be overwritten by `plugin-kit-ai generate`.

## Exact Commands

Run from this repository root:

```bash
cd plugins/statsig
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
../plugin-kit-ai/bin/plugin-kit-ai normalize ./plugins/statsig
../plugin-kit-ai/bin/plugin-kit-ai generate ./plugins/statsig
```

## Generated Outputs

`plugin-kit-ai generate .` writes these managed root artifacts:

- `GENERATED.md`
- `README.md`
- `.claude-plugin/plugin.json`
- `.codex-plugin/plugin.json`
- `.mcp.json`
- `gemini-extension.json`
- `opencode.json`
- `.cursor/mcp.json`

`GENERATED.md` is the generated inventory of managed outputs in the plugin root.
Root `README.md` is a short generated entrypoint that points readers back to this file.
The shared `.mcp.json` carries the portable remote MCP definition used by multiple targets.

## Auth Model

This v1 plugin is intentionally hosted and remote-only:

- hosted Statsig MCP endpoint
- OAuth user authorization on clients that support it
- no API key headers in authored config
- no local runtime or launcher path

Statsig's docs also show an API-key-based `mcp-remote` fallback for some clients, but this catalog keeps the primary clean hosted endpoint only.

## Out Of Scope For V1

These are intentionally not part of this first version:

- API-key-based `stdio` wrappers
- client-specific auth overrides
- `plugin/skills/**`
- runtime hooks or `launcher.yaml`

If later we need a headless Statsig automation lane, that should be a separate plugin such as `statsig-local`, not a hidden second auth mode inside this one.
