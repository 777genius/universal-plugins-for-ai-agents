# universal-plugins-for-ai-agents

Universal plugin catalog for AI agents.

This repository holds portable, production-ready plugin directories that already support multiple agents:

- Claude
- Codex
- Gemini
- OpenCode
- Cursor

Current plugins:

- `plugins/atlassian`: hosted remote-first MCP plugin for Jira, Confluence, and Compass workflows via Atlassian Rovo MCP on `https://mcp.atlassian.com/v1/mcp`
- `plugins/chrome-devtools`: official Chrome DevTools MCP server packaged once for Claude, Codex, Gemini, OpenCode, and Cursor
- `plugins/cloudflare`: hosted OAuth-first MCP plugin for the official Cloudflare API Code Mode server on `https://mcp.cloudflare.com/mcp`
- `plugins/cloudflare-bindings`: hosted OAuth-first MCP plugin for Cloudflare Workers Bindings on `https://bindings.mcp.cloudflare.com/mcp`
- `plugins/cloudflare-docs`: hosted OAuth-first MCP plugin for Cloudflare's documentation server on `https://docs.mcp.cloudflare.com/mcp`
- `plugins/cloudflare-observability`: hosted OAuth-first MCP plugin for Cloudflare's observability server on `https://observability.mcp.cloudflare.com/mcp`
- `plugins/cloudflare-radar`: hosted OAuth-first MCP plugin for Cloudflare Radar internet telemetry and trend workflows on `https://radar.mcp.cloudflare.com/mcp`
- `plugins/context7`: shared MCP-first documentation lookup plugin based on `@upstash/context7-mcp`
- `plugins/docker-hub`: local stdio MCP plugin for Docker Hub repositories and image workflows via Docker's official `mcp/dockerhub` image
- `plugins/gitlab`: remote MCP plugin for the official GitLab MCP server on `gitlab.com` with a note about the current hosted OAuth caveat
- `plugins/github`: remote MCP plugin for official GitHub workflows through `https://api.githubcopilot.com/mcp/` with PAT header projection for all five targets
- `plugins/firebase`: shared MCP plugin for Firebase via `firebase-tools mcp` with shared metadata and five targets (`claude`, `codex-package`, `gemini`, `opencode`, `cursor`)
- `plugins/heroku`: hosted remote-only MCP plugin for Heroku apps, logs, add-ons, and platform operations via `https://mcp.heroku.com/mcp`
- `plugins/hubspot-crm`: hosted remote MCP plugin for HubSpot CRM records, tickets, and reporting on `https://mcp.hubspot.com`
- `plugins/hubspot-developer`: local stdio MCP plugin for HubSpot project, CMS, and build workflows via `@hubspot/cli@8.3.0`
- `plugins/linear`: shared MCP plugin for Linear workspace, issue, and plan workflows via `https://mcp.linear.app/mcp`
- `plugins/neon`: hosted remote MCP plugin for Neon database, branch, and project workflows via `https://mcp.neon.tech/mcp`
- `plugins/notion`: hosted remote-only MCP plugin for interactive OAuth-backed access to Notion docs, pages, and workspace knowledge via `https://mcp.notion.com/mcp`
- `plugins/slack`: hosted remote-only MCP plugin for Slack search, messaging, canvases, and user context via `https://mcp.slack.com/mcp`, intentionally scoped to Claude and Cursor because Slack documents client-specific app identity for that path
- `plugins/stripe`: hosted remote-first MCP plugin for payments, billing, customers, and Stripe knowledge workflows via `https://mcp.stripe.com`
- `plugins/vercel`: hosted remote-only MCP plugin for Vercel docs, projects, deployments, and logs via `https://mcp.vercel.com`
- `plugins/sentry`: hosted remote-only MCP plugin for human-in-the-loop debugging, issues, traces, and incident workflows via `https://mcp.sentry.dev`
- `plugins/supabase`: shared MCP plugin for Supabase project operations via `https://mcp.supabase.com/mcp`
- `plugins/greptile`: shared MCP plugin for Greptile repository intelligence via `https://api.greptile.com/mcp`

## Layout

Each plugin lives inside `plugins/`.

Example:

- `plugins/context7/src/plugin.yaml`
- `plugins/context7/src/mcp/servers.yaml`
- optional `plugins/context7/src/targets/...`
- `plugins/context7/src/README.md`
- `plugins/context7/CLAUDE.md` and `plugins/context7/AGENTS.md` mark the boundary between authored and generated files
- `plugins/context7/README.md` is a short generated entrypoint that points to `plugins/context7/src/README.md`
- generated native artifacts are committed at the plugin root

## Authoring Flow

Each plugin should keep its authored source of truth in:

- `src/plugin.yaml`
- optional `src/mcp/servers.yaml`
- optional `src/targets/<platform>/...`
- edit only `src/`; treat plugin-root manifests as generated outputs

Then generate and validate with `plugin-kit-ai`.
