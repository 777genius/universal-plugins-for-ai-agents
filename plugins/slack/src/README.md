# slack

`slack` is a real portable MCP plugin in this catalog.
It packages Slack's hosted MCP server once and projects it into the two targets Slack officially documents today for this flow in our catalog model: `claude` and `cursor`.

This plugin uses the canonical `src/` layout:

- edit only `src/`
- treat the plugin root as generated and target-native output
- use root `AGENTS.md` as the main boundary doc, `CLAUDE.md` as the Claude pointer, and `GENERATED.md` before touching plugin-root files

## What This Plugin Does

This plugin connects agents to Slack's hosted MCP service at `https://mcp.slack.com/mcp`.
It is designed for interactive, user-authorized access to a Slack workspace through OAuth.

Typical use cases:

- search channels, messages, files, and users
- read and draft messages while staying in the agent flow
- bring Slack conversation history and canvases into active work

## Why This Plugin Targets Only Claude And Cursor

This is an intentionally honest subset plugin.

Slack's official MCP overview currently lists select partner-built clients, and its own connection guides in this area are specifically documented for Claude and Cursor.
Slack also requires MCP clients to be backed by a registered Slack app with a fixed app ID, and only internal apps or directory-published apps may use MCP.

Because of that, this plugin bakes in the officially documented client-specific auth shape only for:

- `claude` - `oauth.clientId` plus `callbackPort`
- `cursor` - `auth.CLIENT_ID`

We do not pretend `codex-package`, `gemini`, or `opencode` are first-class supported here without Slack-documented client identities and setup paths.

## Source Of Truth

Author only these files by hand:

- `src/plugin.yaml`
- `src/mcp/servers.yaml`
- `src/README.md`

Everything else in the plugin root is generated and may be overwritten by `plugin-kit-ai generate`.

## Exact Commands

Run from this repository root:

```bash
cd plugins/slack
plugin-kit-ai normalize .
plugin-kit-ai generate .
plugin-kit-ai generate --check .
plugin-kit-ai validate . --platform claude --strict
plugin-kit-ai validate . --platform cursor --strict
```

If you are working from the `plugin-kit-ai` source repo instead of a globally installed CLI, use its built binary against this directory:

```bash
../plugin-kit-ai/bin/plugin-kit-ai normalize ./plugins/slack
../plugin-kit-ai/bin/plugin-kit-ai generate ./plugins/slack
```

## Generated Outputs

`plugin-kit-ai generate .` writes these managed root artifacts:

- `GENERATED.md`
- `README.md`
- `.claude-plugin/plugin.json`
- `.mcp.json`
- `.cursor/mcp.json`

`GENERATED.md` is the generated inventory of managed outputs in the plugin root.
Root `README.md` is a short generated entrypoint that points readers back to this file.

## Auth Model

This v1 plugin is intentionally hosted and remote-only:

- hosted Slack MCP endpoint
- OAuth user authorization
- official Slack-documented client IDs for Claude and Cursor only
- no local runtime or launcher path

That makes `slack` a good fit for interactive workspace access, not for generic headless automation.

## Out Of Scope For V1

These are intentionally not part of this first version:

- `codex-package`, `gemini`, or `opencode` support
- custom Slack app authoring and self-managed client IDs
- local runtime or `launcher.yaml`
- `src/skills/**`

If later we add more targets, that should happen only after Slack publishes a clear official client path or after we intentionally design a separate advanced plugin around custom Slack app identity management.

## Why Hosted Remote MCP

Slack documents a single hosted remote MCP endpoint, does not support SSE for this service, and requires app-backed OAuth identity.
That makes the cleanest community-facing v1:

- one remote endpoint
- one honest target subset
- no fake multi-target parity
