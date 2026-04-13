# neon

`neon` is a real portable MCP plugin in this catalog.
It packages Neon's hosted MCP server once and projects it into `claude`, `codex-package`, `gemini`, `opencode`, and `cursor`.

This plugin uses the canonical `plugin/` layout:

- edit only `plugin/`
- treat the plugin root as generated and target-native output
- use root `AGENTS.md` as the main boundary doc, `CLAUDE.md` as the Claude pointer, and `GENERATED.md` before touching plugin-root files

## What This Plugin Does

This plugin connects agents to Neon's hosted MCP service at `https://mcp.neon.tech/mcp`.
It is the hosted Neon path for database, branch, and project workflows.

Typical use cases:

- inspect Neon projects, databases, branches, and related platform context from the same workflow as active engineering work
- support Postgres and environment reasoning without building a custom local bridge first
- keep hosted Neon context close to schema, migration, and debugging work

## Source Of Truth

Author only these files by hand:

- `plugin/plugin.yaml`
- `plugin/mcp/servers.yaml`
- `plugin/README.md`

Everything else in the plugin root is generated and may be overwritten by `plugin-kit-ai generate`.

## Exact Commands

Run from this repository root:

```bash
cd plugins/neon
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
../plugin-kit-ai/bin/plugin-kit-ai normalize ./plugins/neon
../plugin-kit-ai/bin/plugin-kit-ai generate ./plugins/neon
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

This v1 plugin is intentionally hosted and interactive-first:

- hosted Neon MCP endpoint
- no embedded headers in authored config
- no API-key secret wiring in the portable definition
- no local runtime or launcher path

That keeps the catalog entry clean and portable for hosted Neon workflows.

## Scope Boundary

This plugin intentionally stays small:

- hosted Neon MCP only
- no local or self-hosted Neon variants
- no API-key header presets in the source of truth

If Neon documents preview or evolving behavior on the hosted path, keep that in mind when treating the plugin as a stable automation surface.

## Out Of Scope For V1

These are intentionally not part of this first version:

- embedded API-key headers in authored config
- local or self-hosted Neon MCP variants
- `plugin/skills/**`
- runtime hooks or `launcher.yaml`

Keep the first Neon catalog entry honest, portable, and easy to trust.
