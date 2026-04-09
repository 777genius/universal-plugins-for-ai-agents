# cloudflare-docs

`cloudflare-docs` is a real portable MCP plugin in this catalog.
It packages Cloudflare's hosted documentation MCP server once and projects it into `claude`, `codex-package`, `gemini`, `opencode`, and `cursor`.

This plugin uses the canonical `src/` layout:

- edit only `src/`
- treat the plugin root as generated and target-native output
- use root `AGENTS.md` as the main boundary doc, `CLAUDE.md` as the Claude pointer, and `GENERATED.md` before touching plugin-root files

## What This Plugin Does

This plugin connects agents to Cloudflare's hosted documentation MCP service at `https://docs.mcp.cloudflare.com/mcp`.
It is the focused Cloudflare docs server for current product reference information.

Typical use cases:

- pull current Cloudflare product and API reference information into an agent workflow
- answer implementation questions without routing every query through the broader API server
- keep docs lookup separate from operational permissions and mutation-heavy infrastructure tooling

## Source Of Truth

Author only these files by hand:

- `src/plugin.yaml`
- `src/mcp/servers.yaml`
- `src/README.md`

Everything else in the plugin root is generated and may be overwritten by `plugin-kit-ai generate`.

## Exact Commands

Run from this repository root:

```bash
cd plugins/cloudflare-docs
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
../plugin-kit-ai/bin/plugin-kit-ai normalize ./plugins/cloudflare-docs
../plugin-kit-ai/bin/plugin-kit-ai generate ./plugins/cloudflare-docs
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

- hosted Cloudflare documentation MCP endpoint
- OAuth as the default connection story
- no bearer-token headers in authored config
- no local runtime or launcher path

That keeps `cloudflare-docs` clean and easy to compare with Cloudflare's official remote setup.

## Why This Is A Separate Plugin

Cloudflare's documentation server is a different product surface from the broader API server:

- it is narrower and safer for research-heavy workflows
- it keeps docs retrieval separate from infrastructure mutation tools
- it gives the catalog a clearer docs-first entry for users who do not need broad Cloudflare account access

## Out Of Scope For V1

These are intentionally not part of this first version:

- bundled Cloudflare API operations
- `src/skills/**`
- runtime hooks or `launcher.yaml`

Keep docs and operations as separate catalog entries first.
