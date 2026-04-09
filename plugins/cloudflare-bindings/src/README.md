# cloudflare-bindings

`cloudflare-bindings` is a real portable MCP plugin in this catalog.
It packages Cloudflare's hosted Workers Bindings MCP server once and projects it into `claude`, `codex-package`, `gemini`, `opencode`, and `cursor`.

This plugin uses the canonical `src/` layout:

- edit only `src/`
- treat the plugin root as generated and target-native output
- use root `AGENTS.md` as the main boundary doc, `CLAUDE.md` as the Claude pointer, and `GENERATED.md` before touching plugin-root files

## What This Plugin Does

This plugin connects agents to Cloudflare's Workers Bindings MCP service at `https://bindings.mcp.cloudflare.com/mcp`.
It is the focused Cloudflare path for storage, AI, and compute primitives in Workers applications.

Typical use cases:

- work with Workers bindings and platform primitives without exposing the full Cloudflare API server
- help agents reason about storage, compute, and AI building blocks while implementing Workers apps
- keep Cloudflare platform guidance narrow and task-shaped instead of always starting from the broad API plugin

## Source Of Truth

Author only these files by hand:

- `src/plugin.yaml`
- `src/mcp/servers.yaml`
- `src/README.md`

Everything else in the plugin root is generated and may be overwritten by `plugin-kit-ai generate`.

## Exact Commands

Run from this repository root:

```bash
cd plugins/cloudflare-bindings
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
../plugin-kit-ai/bin/plugin-kit-ai normalize ./plugins/cloudflare-bindings
../plugin-kit-ai/bin/plugin-kit-ai generate ./plugins/cloudflare-bindings
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

- hosted Cloudflare Workers Bindings MCP endpoint
- OAuth as the default auth story
- no bearer-token headers in authored config
- no local runtime or launcher path

That keeps the default install path aligned with Cloudflare's hosted remote MCP model.

## Why This Is Separate From `cloudflare`

The main `cloudflare` plugin is the broad API server.
`cloudflare-bindings` is narrower and more task-shaped for Workers applications.

That split is better for the catalog because it keeps:

- the wide API surface in one plugin
- product-specific Workers binding workflows in another

## Out Of Scope For V1

These are intentionally not part of this first version:

- bearer-token headers in authored config
- `src/skills/**`
- runtime hooks or `launcher.yaml`

Keep the first family plugin narrow, official, and easy to understand.
