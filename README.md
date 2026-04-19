# universal-plugins-for-ai-agents

Universal plugin catalog for AI agents.

This repository holds portable, production-ready plugin directories that already support multiple agents:

- Claude
- Codex
- Gemini
- OpenCode
- Cursor

Current plugins:

| Plugin | Transport | Entry point | Targets |
| --- | --- | --- | --- |
| `atlassian` | remote | `https://mcp.atlassian.com/v1/mcp` | Claude, Codex, Gemini, OpenCode, Cursor |
| `chrome-devtools` | stdio | `npx -y chrome-devtools-mcp@0.21.0` | Claude, Codex, Gemini, OpenCode, Cursor |
| `cloudflare` | remote | `https://mcp.cloudflare.com/mcp` | Claude, Codex, Gemini, OpenCode, Cursor |
| `cloudflare-bindings` | remote | `https://bindings.mcp.cloudflare.com/mcp` | Claude, Codex, Gemini, OpenCode, Cursor |
| `cloudflare-docs` | remote | `https://docs.mcp.cloudflare.com/mcp` | Claude, Codex, Gemini, OpenCode, Cursor |
| `cloudflare-observability` | remote | `https://observability.mcp.cloudflare.com/mcp` | Claude, Codex, Gemini, OpenCode, Cursor |
| `cloudflare-radar` | remote | `https://radar.mcp.cloudflare.com/mcp` | Claude, Codex, Gemini, OpenCode, Cursor |
| `context7` | stdio | `npx -y @upstash/context7-mcp@2.1.6` | Claude, Codex, Gemini, OpenCode, Cursor |
| `docker-hub` | stdio | `docker run -i --rm -e HUB_PAT_TOKEN mcp/dockerhub --transport=stdio --username=${env:HUB_USERNAME}` | Claude, Codex, Gemini, OpenCode, Cursor |
| `firebase` | stdio | `npx -y firebase-tools@latest mcp` | Claude, Codex, Gemini, OpenCode, Cursor |
| `github` | remote | `https://api.githubcopilot.com/mcp/` | Claude, Codex, Gemini, OpenCode, Cursor |
| `gitlab` | remote | `https://gitlab.com/api/v4/mcp` | Claude, Codex, Gemini, OpenCode, Cursor |
| `greptile` | remote | `https://api.greptile.com/mcp` | Claude, Codex, Gemini, OpenCode, Cursor |
| `heroku` | remote | `https://mcp.heroku.com/mcp` | Claude, Codex, Gemini, OpenCode, Cursor |
| `hubspot-crm` | remote | `https://mcp.hubspot.com` | Claude, Codex, Gemini, OpenCode, Cursor |
| `hubspot-developer` | stdio | `npx -y -p @hubspot/cli@8.3.0 hs mcp start` | Claude, Codex, Gemini, OpenCode, Cursor |
| `linear` | remote | `https://mcp.linear.app/mcp` | Claude, Codex, Gemini, OpenCode, Cursor |
| `neon` | remote | `https://mcp.neon.tech/mcp` | Claude, Codex, Gemini, OpenCode, Cursor |
| `notion` | remote | `https://mcp.notion.com/mcp` | Claude, Codex, Gemini, OpenCode, Cursor |
| `sentry` | remote | `https://mcp.sentry.dev` | Claude, Codex, Gemini, OpenCode, Cursor |
| `slack` | remote | `https://mcp.slack.com/mcp` | Claude, Cursor |
| `stripe` | remote | `https://mcp.stripe.com` | Claude, Codex, Gemini, OpenCode, Cursor |
| `supabase` | remote | `https://mcp.supabase.com/mcp?project_ref=${SUPABASE_PROJECT_REF}` | Claude, Codex, Gemini, OpenCode, Cursor |
| `vercel` | remote | `https://mcp.vercel.com` | Claude, Codex, Gemini, OpenCode, Cursor |

`slack` intentionally remains `Claude` and `Cursor` only because Slack's hosted MCP flow is currently documented with client-specific app identity for that path.

## Discovery And Marketplace Use

This repository now ships the root discovery artifacts each ecosystem actually supports:

- Claude Code marketplace catalog: `.claude-plugin/marketplace.json`
- Codex repo marketplace catalog: `.agents/plugins/marketplace.json`
- Cursor marketplace catalog: `.cursor-plugin/marketplace.json`
- Gemini bundled root extension: `gemini-extension.json`

Claude Code can add this repository directly as a marketplace:

```text
/plugin marketplace add 777genius/universal-plugins-for-ai-agents
```

Then install any listed plugin:

```text
/plugin install context7@universal-plugins-for-ai-agents
```

Codex reads repo-local marketplaces from `.agents/plugins/marketplace.json`. Clone this repository, open it as the working repo in Codex, and the marketplace will be available from the local repo catalog.

Cursor now follows the official repo-level marketplace layout used by Cursor plugin repositories and team marketplaces: `.cursor-plugin/marketplace.json` in the root, plus generated `plugins/*/.cursor-plugin/plugin.json` manifests for every installable plugin.

Gemini is different. Official Gemini gallery indexing is repository-rooted and expects a public repository with `gemini-extension.json` at the repository root or archive root plus the `gemini-cli-extension` GitHub topic. This repository now publishes a bundled root Gemini extension for gallery and scanner visibility, while keeping the authored per-plugin `gemini-extension.json` files under `plugins/*/`. The bundled root extension mirrors the 23 Gemini-compatible plugins from this catalog. Prebuilt Gemini archives are published on the GitHub Releases page for tagged versions.

OpenCode still relies on the native `opencode.json` artifacts committed inside each plugin directory.

Marketplace drift is also gated in CI:

- `python3 scripts/validate_marketplaces.py` verifies that the Claude, Codex, Cursor, and Gemini root discovery artifacts stay aligned with the checked-in plugin manifests under `plugins/*`
- `python3 scripts/sync_cursor_marketplace.py` regenerates `.cursor-plugin/marketplace.json` and `plugins/*/.cursor-plugin/plugin.json`
- `python3 scripts/sync_gemini_marketplace.py` regenerates the bundled root `gemini-extension.json`
- `python3 scripts/package_gemini_extensions.py` builds release-ready Gemini archives for the bundled root extension plus every Gemini-compatible plugin
- `.github/workflows/marketplace-visibility.yml` runs `codex-plugin-scanner==2.0.12` across the Claude, Codex, Gemini, and OpenCode ecosystems and uploads JSON scan artifacts for review, while the validate step separately gates Cursor marketplace drift
- `.github/workflows/gemini-gallery-release.yml` packages Gemini archives on version tags and uploads them to GitHub Releases

## Layout

Each plugin lives inside `plugins/`.

Example:

- `plugins/context7/plugin/plugin.yaml`
- `plugins/context7/plugin/mcp/servers.yaml`
- optional `plugins/context7/plugin/targets/...`
- `plugins/context7/plugin/README.md`
- `plugins/context7/CLAUDE.md` and `plugins/context7/AGENTS.md` mark the boundary between authored and generated files
- `plugins/context7/README.md` is a short generated entrypoint that points to `plugins/context7/plugin/README.md`
- generated native artifacts are committed at the plugin root

## Authoring Flow

Each plugin should keep its authored source of truth in:

- `plugin/plugin.yaml`
- optional `plugin/mcp/servers.yaml`
- optional `plugin/targets/<platform>/...`
- edit only `plugin/`; treat plugin-root manifests as generated outputs

Then generate and validate with `plugin-kit-ai`.
