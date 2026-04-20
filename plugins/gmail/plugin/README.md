# gmail

`gmail` is an Anthropic-hosted connector plugin in this catalog.
It packages Claude's Gmail connector and projects it into the only officially documented lane we can honestly support here today: `claude`.

This plugin uses the canonical `plugin/` layout:

- edit only `plugin/`
- treat the plugin root as generated and target-native output
- use root `AGENTS.md` as the main boundary doc, `CLAUDE.md` as the Claude pointer, and `GENERATED.md` before touching plugin-root files

## What This Plugin Does

This plugin connects Claude to Anthropic's hosted Gmail connector at `https://gmail.mcp.claude.com/mcp`.
It is designed for interactive, user-authorized access to Gmail inside Claude.

Typical use cases:

- search and read emails using natural language
- inspect message and attachment metadata
- review threads and labels
- draft emails in Gmail with explicit user approval

## Why This Plugin Targets Only Claude

This is an intentionally honest single-target plugin.

Anthropic documents Gmail as a Claude-hosted Google Workspace connector, and the official Anthropic plugin examples use this connector only inside Claude plugin `.mcp.json` configs.
We do not have official hosted MCP connection docs for this Gmail flow in `codex-package`, `gemini`, `opencode`, or `cursor`, so this plugin stays `claude` only.

## Source Of Truth

Author only these files by hand:

- `plugin/plugin.yaml`
- `plugin/mcp/servers.yaml`
- `plugin/README.md`

Everything else in the plugin root is generated and may be overwritten by `plugin-kit-ai generate`.

## Exact Commands

Run from this repository root:

```bash
cd plugins/gmail
plugin-kit-ai normalize .
plugin-kit-ai generate .
plugin-kit-ai generate --check .
plugin-kit-ai validate . --platform claude --strict
```

If you are working from the `plugin-kit-ai` source repo instead of a globally installed CLI, use its built binary against this directory:

```bash
../plugin-kit-ai/bin/plugin-kit-ai normalize ./plugins/gmail
../plugin-kit-ai/bin/plugin-kit-ai generate ./plugins/gmail
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

- Anthropic-hosted Gmail connector
- Google account authentication through Claude
- explicit user approval for actions
- no local runtime or launcher path

## Limitations

Current Gmail limitations in Claude docs are important:

- Claude drafts email, but does not send it automatically
- attachment content is not directly available through Gmail here
- this plugin is tied to the Google account the user authenticated in Claude

This plugin is for Claude-hosted Gmail workflows, not for generic cross-client Gmail MCP portability.
