# heroku

`heroku` is a real portable MCP plugin in this catalog.
It packages Heroku's hosted MCP server once and projects it into `claude`, `codex-package`, `gemini`, `opencode`, and `cursor`.

This plugin uses the canonical `src/` layout:

- edit only `src/`
- treat the plugin root as generated and target-native output
- use root `AGENTS.md` as the main boundary doc, `CLAUDE.md` as the Claude pointer, and `GENERATED.md` before touching plugin-root files

## What This Plugin Does

This plugin connects agents to Heroku's hosted MCP service at `https://mcp.heroku.com/mcp`.
It is designed for interactive, user-authorized access to Heroku apps, logs, add-ons, databases, and platform operations through OAuth.

Typical use cases:

- inspect apps, dynos, config vars, releases, and pipelines from the same workflow as active engineering work
- review logs, operational state, and Postgres-related context without leaving the agent session
- help with routine platform operations without introducing a local bridge process

## Source Of Truth

Author only these files by hand:

- `src/plugin.yaml`
- `src/mcp/servers.yaml`
- `src/README.md`

Everything else in the plugin root is generated and may be overwritten by `plugin-kit-ai generate`.

## Exact Commands

Run from this repository root:

```bash
cd plugins/heroku
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
../plugin-kit-ai/bin/plugin-kit-ai normalize ./plugins/heroku
../plugin-kit-ai/bin/plugin-kit-ai generate ./plugins/heroku
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

- hosted Heroku MCP endpoint
- OAuth user authorization
- no bearer-token headers in authored config
- no local runtime or launcher path

That keeps the default install story aligned with Heroku's recommended remote setup for interactive MCP clients.

Heroku also documents an official stdio path through `heroku mcp:start`.
This catalog plugin intentionally keeps the hosted remote variant as the default package because it is easier to project consistently across all current targets without depending on a globally installed Heroku CLI.

## Out Of Scope For V1

These are intentionally not part of this first version:

- embedded API key or bearer-token headers in authored config
- the official local stdio path through `heroku mcp:start`
- `src/skills/**`
- runtime hooks or `launcher.yaml`

Keep the default catalog entry small, official, and easy to trust first.
