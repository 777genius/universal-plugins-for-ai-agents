# atlassian

`atlassian` is a real portable MCP plugin in this catalog.
It packages Atlassian's hosted Rovo MCP server once and projects it into `claude`, `codex-package`, `gemini`, `opencode`, and `cursor`.

This plugin uses the canonical `src/` layout:

- edit only `src/`
- treat the plugin root as generated and target-native output
- use root `AGENTS.md` as the main boundary doc, `CLAUDE.md` as the Claude pointer, and `GENERATED.md` before touching plugin-root files

## What This Plugin Does

This plugin connects agents to Atlassian's hosted Rovo MCP service at `https://mcp.atlassian.com/v1/mcp`.
It is an official remote MCP integration for Jira, Confluence, and Compass workflows with interactive user authorization through OAuth 2.1.

Typical use cases:

- search Jira issues and recent project work without leaving the agent flow
- read and summarize Confluence pages as planning or implementation context
- pull Compass service context into debugging, review, and delivery workflows
- create or update Atlassian content with the same permissions the authorized user already has

## Source Of Truth

Author only these files by hand:

- `src/plugin.yaml`
- `src/mcp/servers.yaml`
- `src/README.md`

Everything else in the plugin root is generated and may be overwritten by `plugin-kit-ai generate`.

## Exact Commands

Run from this repository root:

```bash
cd plugins/atlassian
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
../plugin-kit-ai/bin/plugin-kit-ai normalize ./plugins/atlassian
../plugin-kit-ai/bin/plugin-kit-ai generate ./plugins/atlassian
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

This v1 plugin is intentionally hosted and remote-first:

- hosted Atlassian Rovo MCP endpoint
- OAuth 2.1 user authorization as the default path
- no bearer-token or basic-auth headers in authored config
- no local runtime or launcher path

That keeps the plugin aligned with Atlassian's primary interactive setup model for Jira, Confluence, and Compass access.

## Why This Uses `/v1/mcp`

Atlassian documents `https://mcp.atlassian.com/v1/mcp` as the current endpoint for custom clients and states that `/v1/sse` is no longer supported after June 30, 2026.
This plugin therefore keeps the remote streamable HTTP endpoint as the only source of truth and does not carry legacy SSE wiring.

## API Token Note

Atlassian also documents API-token-based authentication for advanced scenarios if an organization admin has explicitly enabled it.
This first plugin version does not bake that path into authored config because it changes the security story and may expose a smaller tool set than OAuth.

Treat API-token or service-account auth as an advanced follow-up path, not as the community default for this catalog entry.

## IDE Bridge Note

Atlassian still documents `mcp-remote` for some local IDE and custom-client setups.
This plugin intentionally keeps the canonical server definition as the hosted remote MCP endpoint itself instead of baking a bridge process into the authored config.

If a specific client version still needs a bridge, treat that as a client-side compatibility detail rather than as the plugin's shared source of truth.

## Out Of Scope For V1

These are intentionally not part of this first version:

- API-token or service-account header wiring in generated config
- local `mcp-remote` bridge processes in authored config
- `src/skills/**`
- runtime hooks or `launcher.yaml`

Keep v1 small, official, and easy to trust first.
