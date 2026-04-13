# cloudflare-observability

`cloudflare-observability` is a real portable MCP plugin in this catalog.
It packages Cloudflare's hosted observability MCP server once and projects it into `claude`, `codex-package`, `gemini`, `opencode`, and `cursor`.

This plugin uses the canonical `plugin/` layout:

- edit only `plugin/`
- treat the plugin root as generated and target-native output
- use root `AGENTS.md` as the main boundary doc, `CLAUDE.md` as the Claude pointer, and `GENERATED.md` before touching plugin-root files

## What This Plugin Does

This plugin connects agents to Cloudflare's hosted observability MCP service at `https://observability.mcp.cloudflare.com/mcp`.
It is the focused Cloudflare server for logs, analytics, and debugging insight.

Typical use cases:

- inspect production logs and analytics through the same workflow as incident response and debugging
- separate observability access from the broader Cloudflare API mutation surface
- give agents a focused debugging tool instead of a general infrastructure control plugin

## Source Of Truth

Author only these files by hand:

- `plugin/plugin.yaml`
- `plugin/mcp/servers.yaml`
- `plugin/README.md`

Everything else in the plugin root is generated and may be overwritten by `plugin-kit-ai generate`.

## Exact Commands

Run from this repository root:

```bash
cd plugins/cloudflare-observability
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
../plugin-kit-ai/bin/plugin-kit-ai normalize ./plugins/cloudflare-observability
../plugin-kit-ai/bin/plugin-kit-ai generate ./plugins/cloudflare-observability
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

This v1 plugin is intentionally hosted and OAuth-first:

- hosted Cloudflare observability MCP endpoint
- OAuth as the default connection story
- no bearer-token headers in authored config
- no local runtime or launcher path

That keeps the default install story aligned with Cloudflare's recommended hosted setup for interactive MCP clients.

## Why This Is A Separate Plugin

Cloudflare's observability server is a different product surface from the broader API server:

- it is optimized for logs and analytics workflows
- it keeps debugging access separate from mutation-heavy infrastructure operations
- it gives incident and operations workflows a cleaner, more focused catalog entry

## Out Of Scope For V1

These are intentionally not part of this first version:

- bundled Cloudflare API control actions outside the observability surface
- `plugin/skills/**`
- runtime hooks or `launcher.yaml`

Keep observability and broad infrastructure control as separate plugins first.
