# hubspot-developer

`hubspot-developer` is a real portable MCP plugin in this catalog.
It packages HubSpot's local Developer MCP server once and projects it into `claude`, `codex-package`, `gemini`, `opencode`, and `cursor`.

This plugin uses the canonical `src/` layout:

- edit only `src/`
- treat the plugin root as generated and target-native output
- use root `AGENTS.md` as the main boundary doc, `CLAUDE.md` as the Claude pointer, and `GENERATED.md` before touching plugin-root files

## What This Plugin Does

This plugin starts HubSpot's local Developer MCP server through the HubSpot CLI.
It is the developer-facing HubSpot path for project scaffolding, CMS work, builds, logs, and app workflows.

Typical use cases:

- create and manage HubSpot developer projects from the same workflow as active coding work
- inspect project state, builds, logs, and local developer context without leaving the agent session
- use HubSpot's CLI-backed development tools through one portable stdio definition

## Source Of Truth

Author only these files by hand:

- `src/plugin.yaml`
- `src/mcp/servers.yaml`
- `src/README.md`

Everything else in the plugin root is generated and may be overwritten by `plugin-kit-ai generate`.

## Exact Commands

Run from this repository root:

```bash
cd plugins/hubspot-developer
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
../plugin-kit-ai/bin/plugin-kit-ai normalize ./plugins/hubspot-developer
../plugin-kit-ai/bin/plugin-kit-ai generate ./plugins/hubspot-developer
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
The shared `.mcp.json` carries the portable stdio definition used by multiple targets.

## Runtime Model

This v1 plugin is intentionally local and CLI-backed:

- local stdio MCP over `hs mcp start`
- pinned to `@hubspot/cli@8.3.0`
- uses `HUBSPOT_MCP_STANDALONE=true` so the running MCP server can keep resolving HubSpot CLI subcommands through the same pinned package
- no launcher or separate runtime bundle

The `npx -p @hubspot/cli@8.3.0 hs mcp start` path avoids requiring a globally preinstalled `hs` binary.

HubSpot's official docs describe the Developer MCP server as GA and generally onboard users through `hs mcp setup`.
This catalog plugin intentionally packages the same local MCP server as a portable, reproducible stdio definition instead of relying on an interactive setup step.

## Why This Is Separate From `hubspot-crm`

HubSpot exposes two very different MCP shapes:

- remote CRM/account access
- local developer tooling via the CLI

They should stay separate because the transport, auth, and user expectations differ too much.

Use `hubspot-developer` for local project and CMS development.
Use `hubspot-crm` for hosted CRM workflows.

## Out Of Scope For V1

These are intentionally not part of this first version:

- target-specific command overrides
- `src/skills/**`
- runtime hooks or `launcher.yaml`

Keep the default developer plugin simple, pinned, and reproducible.
