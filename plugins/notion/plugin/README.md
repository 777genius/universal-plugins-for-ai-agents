# notion

`notion` is a real portable MCP plugin in this catalog.
It packages Notion's hosted MCP server once and projects it into `claude`, `codex-package`, `gemini`, `opencode`, and `cursor`.

This plugin uses the canonical `plugin/` layout:

- edit only `plugin/`
- treat the plugin root as generated and target-native output
- use root `AGENTS.md` as the main boundary doc, `CLAUDE.md` as the Claude pointer, and `GENERATED.md` before touching plugin-root files

## What This Plugin Does

This plugin connects agents to Notion's hosted MCP service at `https://mcp.notion.com/mcp`.
It is designed for interactive, user-authorized access to a real Notion workspace through OAuth.

Typical use cases:

- search internal docs and project pages
- read and update knowledge-base content
- work with planning and workspace information without leaving the agent flow

## Source Of Truth

Author only these files by hand:

- `plugin/plugin.yaml`
- `plugin/mcp/servers.yaml`
- `plugin/README.md`

Everything else in the plugin root is generated and may be overwritten by `plugin-kit-ai generate`.

## Exact Commands

Run from this repository root:

```bash
cd plugins/notion
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
../plugin-kit-ai/bin/plugin-kit-ai normalize ./plugins/notion
../plugin-kit-ai/bin/plugin-kit-ai generate ./plugins/notion
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

- hosted Notion MCP endpoint
- OAuth user authorization
- no bearer-token headers in authored config
- no local runtime or launcher path

That makes `notion` a good fit for interactive workspace access, not for headless automation.

## Out Of Scope For V1

These are intentionally not part of this first version:

- self-hosted or local Notion MCP mode
- headless automation with manual token wiring
- `plugin/skills/**`
- runtime hooks or `launcher.yaml`
- file upload workflows, because current Notion MCP does not support file uploads

If later you need unattended automation or a local token-driven setup, that should become a separate plugin such as `notion-local`, not a second mode hidden inside this one.

## Why Hosted Remote MCP

Notion currently recommends the hosted MCP flow for end-user connection, and its open-source local MCP server is no longer the primary actively maintained path.
This keeps the plugin simpler and closer to the official user-facing setup:

- one remote endpoint
- one auth story
- no extra local bridge process in authored config

Keep v1 narrow and reliable first.
