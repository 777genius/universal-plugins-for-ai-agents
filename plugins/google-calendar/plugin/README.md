# google-calendar

`google-calendar` is an Anthropic-hosted connector plugin in this catalog.
It packages Claude's Google Calendar connector and projects it into the only officially documented lane we can honestly support here today: `claude`.

This plugin uses the canonical `plugin/` layout:

- edit only `plugin/`
- treat the plugin root as generated and target-native output
- use root `AGENTS.md` as the main boundary doc, `CLAUDE.md` as the Claude pointer, and `GENERATED.md` before touching plugin-root files

## What This Plugin Does

This plugin connects Claude to Anthropic's hosted Google Calendar connector at `https://gcal.mcp.claude.com/mcp`.
It is designed for interactive, user-authorized access to Google Calendar inside Claude.

Typical use cases:

- inspect calendars and upcoming events
- create, update, and delete calendar events with approval
- find mutual availability across attendees
- respond to invitations and manage recurring meetings

## Why This Plugin Targets Only Claude

This is an intentionally honest single-target plugin.

Anthropic documents Google Calendar as a Claude-hosted Google Workspace connector, and the official Anthropic plugin examples use this connector only inside Claude plugin `.mcp.json` configs.
We do not have official hosted MCP connection docs for this calendar flow in `codex-package`, `gemini`, `opencode`, or `cursor`, so this plugin stays `claude` only.

## Source Of Truth

Author only these files by hand:

- `plugin/plugin.yaml`
- `plugin/mcp/servers.yaml`
- `plugin/README.md`

Everything else in the plugin root is generated and may be overwritten by `plugin-kit-ai generate`.

## Exact Commands

Run from this repository root:

```bash
cd plugins/google-calendar
plugin-kit-ai normalize .
plugin-kit-ai generate .
plugin-kit-ai generate --check .
plugin-kit-ai validate . --platform claude --strict
```

If you are working from the `plugin-kit-ai` source repo instead of a globally installed CLI, use its built binary against this directory:

```bash
../plugin-kit-ai/bin/plugin-kit-ai normalize ./plugins/google-calendar
../plugin-kit-ai/bin/plugin-kit-ai generate ./plugins/google-calendar
```

## Generated Outputs

`plugin-kit-ai generate .` writes these managed root artifacts:

- `GENERATED.md`
- `README.md`
- `.claude-plugin/plugin.json`
- `.mcp.json`

`GENERATED.md` is the generated inventory of managed outputs in the plugin root.
Root `README.md` is a short generated entrypoint that points readers back to this file.

## Auth Model

This v1 plugin is intentionally hosted and remote-only:

- Anthropic-hosted Google Calendar connector
- Google account authentication through Claude
- explicit user approval for actions
- no local runtime or launcher path

This plugin is for Claude-hosted calendar workflows, not for generic cross-client Google Calendar MCP portability.
