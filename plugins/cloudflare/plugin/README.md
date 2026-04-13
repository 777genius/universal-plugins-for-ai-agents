# cloudflare

`cloudflare` is a real portable MCP plugin in this catalog.
It packages Cloudflare's official API MCP server once and projects it into `claude`, `codex-package`, `gemini`, `opencode`, and `cursor`.

This plugin uses the canonical `plugin/` layout:

- edit only `plugin/`
- treat the plugin root as generated and target-native output
- use root `AGENTS.md` as the main boundary doc, `CLAUDE.md` as the Claude pointer, and `GENERATED.md` before touching plugin-root files

## What This Plugin Does

This plugin connects agents to Cloudflare's hosted API MCP service at `https://mcp.cloudflare.com/mcp`.
It is the official broad Cloudflare API server built on Cloudflare's Code Mode pattern.

Instead of exposing thousands of individual tools, this server gives the model a small token-efficient interface that can search the Cloudflare API surface and execute real API calls against it.

Typical use cases:

- inspect and manage Workers, KV, R2, D1, DNS, Zero Trust, and other Cloudflare products from the same agent workflow
- look up the right Cloudflare API paths without shipping the full OpenAPI schema into model context
- let an authorized agent help with real infrastructure and platform changes while keeping the plugin install story simple

## Source Of Truth

Author only these files by hand:

- `plugin/plugin.yaml`
- `plugin/mcp/servers.yaml`
- `plugin/README.md`

Everything else in the plugin root is generated and may be overwritten by `plugin-kit-ai generate`.

## Exact Commands

Run from this repository root:

```bash
cd plugins/cloudflare
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
../plugin-kit-ai/bin/plugin-kit-ai normalize ./plugins/cloudflare
../plugin-kit-ai/bin/plugin-kit-ai generate ./plugins/cloudflare
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

- hosted Cloudflare API MCP endpoint
- OAuth as the community default
- no bearer-token headers in authored config
- no local runtime or launcher path

That keeps the default install story aligned with Cloudflare's recommended remote setup for interactive MCP clients.

## Why This Uses The API Server

Cloudflare runs many product-specific MCP servers, but this plugin intentionally starts with the flagship API server.

That is the best default catalog entry because it gives broad coverage across Cloudflare products through one stable endpoint:

- `https://mcp.cloudflare.com/mcp`
- one official repository
- one OAuth-first connection story
- one token-efficient interface instead of thousands of endpoint tools

If later the catalog needs narrower product plugins such as observability, bindings, docs, or radar, those should be separate plugin directories rather than hidden modes inside this one.

## Why The Server Alias Is `cloudflare-api`

The plugin directory is named `cloudflare`, but the shared MCP server alias is `cloudflare-api`.
That matches Cloudflare's own configuration examples and makes the generated config easier to compare with upstream docs.

## Advanced Paths Kept Out Of V1

Cloudflare documents several real advanced options:

- bearer-token authentication for CI, automation, or clients without OAuth
- `?codemode=false` to disable Code Mode and expose individual API tools
- product-specific hosted MCP servers for narrower Cloudflare domains
- the separate `cloudflare/skills` bundle for agents that support Agent Skills

These are useful, but they change the token, auth, or product story enough that they should not be silently mixed into the default portable plugin definition.

## Out Of Scope For V1

These are intentionally not part of this first version:

- embedded bearer-token headers in authored config
- `?codemode=false` as the default server URL
- product-specific Cloudflare MCP servers
- `plugin/skills/**`
- runtime hooks or `launcher.yaml`

Keep the first catalog entry small, official, and easy to trust first.
