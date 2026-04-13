# cloudflare-radar

`cloudflare-radar` is a real portable MCP plugin in this catalog.
It packages Cloudflare's hosted Radar MCP server once and projects it into `claude`, `codex-package`, `gemini`, `opencode`, and `cursor`.

This plugin uses the canonical `plugin/` layout:

- edit only `plugin/`
- treat the plugin root as generated and target-native output
- use root `AGENTS.md` as the main boundary doc, `CLAUDE.md` as the Claude pointer, and `GENERATED.md` before touching plugin-root files

## What This Plugin Does

This plugin connects agents to Cloudflare's hosted Radar MCP service at `https://radar.mcp.cloudflare.com/mcp`.
It is the focused Cloudflare path for internet telemetry, traffic trends, ASN context, and network intelligence.

Typical use cases:

- inspect internet traffic patterns and outage-related context from the same workflow as incident review or planning
- answer network, geography, ASN, and protocol trend questions without starting from the broader Cloudflare API server
- keep telemetry and internet intelligence separate from mutation-heavy infrastructure control

## Source Of Truth

Author only these files by hand:

- `plugin/plugin.yaml`
- `plugin/mcp/servers.yaml`
- `plugin/README.md`

Everything else in the plugin root is generated and may be overwritten by `plugin-kit-ai generate`.

## Exact Commands

Run from this repository root:

```bash
cd plugins/cloudflare-radar
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
../plugin-kit-ai/bin/plugin-kit-ai normalize ./plugins/cloudflare-radar
../plugin-kit-ai/bin/plugin-kit-ai generate ./plugins/cloudflare-radar
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

- hosted Cloudflare Radar MCP endpoint
- OAuth as the community default
- no bearer-token headers in authored config
- no local runtime or launcher path

That keeps `cloudflare-radar` aligned with Cloudflare's hosted remote MCP model for interactive clients.

## Why This Is A Separate Plugin

`cloudflare-radar` is intentionally separate from the broader `cloudflare` API plugin:

- it is focused on internet and network intelligence, not general account operations
- it fits research, incident, and planning workflows better than the wide API server
- it keeps telemetry lookup separate from mutation-heavy infrastructure tooling

## Out Of Scope For V1

These are intentionally not part of this first version:

- bearer-token headers in authored config
- `plugin/skills/**`
- runtime hooks or `launcher.yaml`

Keep the first Radar catalog entry narrow, official, and easy to trust.
