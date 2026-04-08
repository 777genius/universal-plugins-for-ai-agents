# vercel

`vercel` is a real portable MCP plugin in this catalog.
It packages Vercel's official hosted MCP service once and projects it into `claude`, `codex-package`, `gemini`, `opencode`, and `cursor`.

This plugin uses the canonical `src/` layout:

- edit only `src/`
- treat the plugin root as generated and target-native output
- use root `AGENTS.md` as the main boundary doc, `CLAUDE.md` as the Claude pointer, and `GENERATED.md` before touching plugin-root files

## What This Plugin Does

This plugin connects agents to Vercel's hosted MCP service at `https://mcp.vercel.com`.
It is an official remote MCP integration for documentation lookup plus authenticated project, deployment, and log workflows.

Typical use cases:

- search Vercel docs without leaving the agent flow
- inspect projects and deployments
- analyze deployment logs and operational context

Vercel currently describes its MCP offering as beta upstream, so this plugin keeps the integration honest and narrow.

## Source Of Truth

Author only these files by hand:

- `src/plugin.yaml`
- `src/mcp/servers.yaml`
- `src/README.md`

Everything else in the plugin root is generated and may be overwritten by `plugin-kit-ai generate`.

## Exact Commands

Run from this repository root:

```bash
cd plugins/vercel
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
../plugin-kit-ai/bin/plugin-kit-ai normalize ./plugins/vercel
../plugin-kit-ai/bin/plugin-kit-ai generate ./plugins/vercel
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

- hosted Vercel MCP endpoint
- OAuth user authorization
- no bearer-token headers in authored config
- no local runtime or launcher path

That keeps the plugin aligned with the official client-facing flow for Vercel project access.

## Gemini Note

Some Vercel setup docs for Gemini still show an `mcp-remote` bridge process.
This plugin intentionally keeps `https://mcp.vercel.com` as the canonical universal source of truth instead of baking a Gemini-only bridge into authored config.

If a specific Gemini client version still needs that bridge, treat it as a client-side compatibility note rather than as the plugin's authored MCP definition.

## Out Of Scope For V1

These are intentionally not part of this first version:

- local or self-hosted Vercel MCP variants
- `src/skills/**`
- runtime hooks or `launcher.yaml`
- target-specific authored special-casing for Gemini

Keep v1 small and clean first.
