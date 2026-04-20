# microsoft365

`microsoft365` is an Anthropic-hosted connector plugin in this catalog.
It packages Claude's Microsoft 365 connector and projects it into the only officially documented lane we can honestly support here today: `claude`.

This plugin uses the canonical `plugin/` layout:

- edit only `plugin/`
- treat the plugin root as generated and target-native output
- use root `AGENTS.md` as the main boundary doc, `CLAUDE.md` as the Claude pointer, and `GENERATED.md` before touching plugin-root files

## What This Plugin Does

This plugin connects Claude to Anthropic's hosted Microsoft 365 connector at `https://microsoft365.mcp.claude.com/mcp`.
It is designed for interactive, user-authorized access to Microsoft 365 data inside Claude.

This single connector covers the Microsoft-family cards from the screenshot:

- Teams
- SharePoint
- Outlook Email
- Outlook Calendar

Typical use cases:

- search SharePoint and OneDrive documents
- summarize Outlook email threads
- inspect Outlook calendar and meeting context
- review Teams chats and channel discussions

## Why This Plugin Targets Only Claude

This is an intentionally honest single-target plugin.

Anthropic documents Microsoft 365 as one pre-built Claude-hosted connector spanning Outlook, SharePoint, OneDrive, and Teams.
We do not have official hosted MCP connection docs for this Microsoft 365 flow in `codex-package`, `gemini`, `opencode`, or `cursor`, so this plugin stays `claude` only.

## Why There Is One `microsoft365` Plugin Instead Of Four Aliases

The official Anthropic docs describe one Microsoft 365 connector, not four separate hosted MCP servers.
Shipping separate `teams`, `sharepoint`, `outlook-email`, and `outlook-calendar` plugin directories here would just duplicate the same backend endpoint and create install drift.

This catalog keeps the canonical service boundary:

- one hosted Microsoft 365 endpoint
- one Claude-only plugin
- clear coverage of the four UI cards it actually spans

## Source Of Truth

Author only these files by hand:

- `plugin/plugin.yaml`
- `plugin/mcp/servers.yaml`
- `plugin/README.md`

Everything else in the plugin root is generated and may be overwritten by `plugin-kit-ai generate`.

## Exact Commands

Run from this repository root:

```bash
cd plugins/microsoft365
plugin-kit-ai normalize .
plugin-kit-ai generate .
plugin-kit-ai generate --check .
plugin-kit-ai validate . --platform claude --strict
```

If you are working from the `plugin-kit-ai` source repo instead of a globally installed CLI, use its built binary against this directory:

```bash
../plugin-kit-ai/bin/plugin-kit-ai normalize ./plugins/microsoft365
../plugin-kit-ai/bin/plugin-kit-ai generate ./plugins/microsoft365
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

- Anthropic-hosted Microsoft 365 connector
- Microsoft Entra and Microsoft 365 authentication through Claude
- delegated read-only access
- no local runtime or launcher path

Important scope notes from Anthropic's docs:

- this connector requires a Microsoft business account tied to a Microsoft Entra tenant
- personal `@outlook.com` and similar accounts are not supported
- the current connector is read-only

This plugin is for Claude-hosted Microsoft 365 workflows, not for generic cross-client Microsoft Graph portability.
