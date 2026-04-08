# sentry

`sentry` is a real portable MCP plugin in this catalog.
It packages Sentry's official hosted MCP service once and projects it into `claude`, `codex-package`, `gemini`, `opencode`, and `cursor`.

This plugin uses the canonical `src/` layout:

- edit only `src/`
- treat the plugin root as generated and target-native output
- use root `AGENTS.md` as the main boundary doc, `CLAUDE.md` as the Claude pointer, and `GENERATED.md` before touching plugin-root files

## What This Plugin Does

This plugin connects agents to Sentry's hosted MCP service at `https://mcp.sentry.dev`.
It is designed for human-in-the-loop debugging workflows, not as a generic wrapper around every Sentry API surface.

Typical use cases:

- inspect issues, traces, and debugging context
- triage incidents while keeping engineering context close
- help coding agents reason about real production failures

## Source Of Truth

Author only these files by hand:

- `src/plugin.yaml`
- `src/mcp/servers.yaml`
- `src/README.md`

Everything else in the plugin root is generated and may be overwritten by `plugin-kit-ai generate`.

## Exact Commands

Run from this repository root:

```bash
cd plugins/sentry
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
../plugin-kit-ai/bin/plugin-kit-ai normalize ./plugins/sentry
../plugin-kit-ai/bin/plugin-kit-ai generate ./plugins/sentry
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

This v1 plugin is intentionally hosted and remote-only:

- hosted Sentry MCP endpoint
- OAuth user authorization
- no bearer-token headers in authored config
- no local runtime or launcher path

That keeps the plugin aligned with the hosted SaaS path Sentry exposes for interactive coding agents.

## Product Boundary

This plugin is for human-in-the-loop debugging and incident workflows.
It does not promise every self-hosted or local Sentry transport story in the same package.

In particular, these are intentionally out of scope for this v1:

- stdio `@sentry/mcp-server` setup
- self-hosted Sentry transport and token wiring
- embedded search-provider configuration
- `src/skills/**`
- runtime hooks or `launcher.yaml`

If you later need self-hosted or stdio operation, that should become a separate variant rather than a second mode hidden inside this plugin.
