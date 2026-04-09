# hubspot-crm

`hubspot-crm` is a real portable MCP plugin in this catalog.
It packages HubSpot's hosted remote MCP server once and projects it into `claude`, `codex-package`, `gemini`, `opencode`, and `cursor`.

This plugin uses the canonical `src/` layout:

- edit only `src/`
- treat the plugin root as generated and target-native output
- use root `AGENTS.md` as the main boundary doc, `CLAUDE.md` as the Claude pointer, and `GENERATED.md` before touching plugin-root files

## What This Plugin Does

This plugin connects agents to HubSpot's remote MCP service at `https://mcp.hubspot.com`.
It is the CRM-facing HubSpot path for beta, read-only access to CRM objects and account context.

Typical use cases:

- inspect contacts, companies, deals, tickets, invoices, and related CRM context from the same workflow as active implementation or support work
- search and retrieve HubSpot CRM records without building a custom bridge first
- pull business context into an agent session before changing product, support, or growth flows

## Source Of Truth

Author only these files by hand:

- `src/plugin.yaml`
- `src/mcp/servers.yaml`
- `src/README.md`

Everything else in the plugin root is generated and may be overwritten by `plugin-kit-ai generate`.

## Exact Commands

Run from this repository root:

```bash
cd plugins/hubspot-crm
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
../plugin-kit-ai/bin/plugin-kit-ai normalize ./plugins/hubspot-crm
../plugin-kit-ai/bin/plugin-kit-ai generate ./plugins/hubspot-crm
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

- hosted HubSpot MCP endpoint
- no embedded credentials in authored config
- no bearer-token headers in authored config
- no local runtime or launcher path

Important:

- HubSpot documents the remote MCP server as **BETA**
- the current server surface is **read-only** for supported CRM objects
- HubSpot's remote MCP flow expects a user-owned MCP auth app and PKCE-based login

That means this catalog plugin gives you the correct portable server definition, but you still need to complete the client-specific auth setup in the tool you are using.

## Why This Is Separate From `hubspot-developer`

HubSpot exposes two different MCP stories:

- remote CRM/account workflows
- local developer tooling through the HubSpot CLI

Those should not be mixed into one plugin because the auth, runtime, and user expectations are different.

Use `hubspot-crm` when you need hosted CRM access.
Use `hubspot-developer` when you need local developer tooling for HubSpot projects.

## Out Of Scope For V1

These are intentionally not part of this first version:

- embedded MCP auth app credentials
- custom target-specific secret wiring
- `src/skills/**`
- runtime hooks or `launcher.yaml`

Keep the first catalog entry honest, portable, and easy to trust.
