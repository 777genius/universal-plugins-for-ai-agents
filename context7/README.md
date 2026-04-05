# context7

`context7` is the first real multi-target MCP-first example in this repo.
It shows how to author one plugin once and generate working outputs for `claude`, `codex-package`, `gemini`, `opencode`, and `cursor`.

This example is intentionally package-only for Claude.
There is no `launcher.yaml`, no runtime binary, and no `hooks/hooks.json`.

## Why This Example Matters

- It uses the same upstream package as the official Claude plugin: `@upstash/context7-mcp@2.1.6`
- It proves that `claude` now supports a package-only mode in `plugin-kit-ai` when you author only package/config surfaces
- It shows the correct lane split for Codex:
  - use `codex-package` for official plugin bundle output
  - do not use `codex-runtime` for a shared MCP package like this

`codex-runtime` is the local notify/runtime lane.
`context7` is a portable MCP package, so `codex-package` is the correct target.

## Authored Source Of Truth

This example is authored from exactly three inputs.

### `plugin.yaml`

```yaml
api_version: v1
name: "context7"
version: "0.1.0"
description: "Upstash Context7 MCP server for up-to-date documentation lookup. Pull version-specific documentation and code examples directly from source repositories into your LLM context."
targets:
  - "claude"
  - "codex-package"
  - "gemini"
  - "opencode"
  - "cursor"
```

### `mcp/servers.yaml`

```yaml
format: plugin-kit-ai/mcp
version: 1

servers:
  context7:
    description: "Up-to-date, version-specific documentation and code examples from source repositories."
    type: stdio
    stdio:
      command: npx
      args:
        - -y
        - "@upstash/context7-mcp@2.1.6"
    targets:
      - claude
      - codex-package
      - gemini
      - opencode
      - cursor
```

### `targets/codex-package/package.yaml`

This file is optional.
Here it is used only to enrich the generated Codex package manifest with first-class metadata.

```yaml
author:
  name: Upstash
homepage: https://context7.com
repository: https://github.com/upstash/context7
license: MIT
keywords:
  - context7
  - mcp
  - documentation
  - ai-agents
```

## Exact Commands

Run the example from this repository:

```bash
cd context7
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
../plugin-kit-ai/bin/plugin-kit-ai normalize ./context7
../plugin-kit-ai/bin/plugin-kit-ai generate ./context7
```

## What `generate` Produces

`plugin-kit-ai generate .` currently writes these 6 managed artifacts:

- `.claude-plugin/plugin.json`
- `.codex-plugin/plugin.json`
- `.mcp.json`
- `gemini-extension.json`
- `opencode.json`
- `.cursor/mcp.json`

The shared `.mcp.json` is consumed by both Claude and Codex package outputs.

Important Claude detail:
- there is no `launcher.yaml`
- there is no `hooks/hooks.json`
- this is valid because the plugin only uses package/config surfaces

## Per-Target Result

### Claude

Generated files:

- `.claude-plugin/plugin.json`
- `.mcp.json`

Claude no longer needs `launcher.yaml` when the repo is package-only and authored from surfaces like:

- `mcp/servers.yaml`
- `skills/`
- `targets/claude/settings.json`
- `targets/claude/lsp.json`
- `targets/claude/user-config.json`
- `targets/claude/manifest.extra.json`
- `targets/claude/commands/**`
- `targets/claude/agents/**`

This example only uses `mcp/servers.yaml`, so Claude gets a clean MCP-only package output.

### Codex

Generated files:

- `.codex-plugin/plugin.json`
- `.mcp.json`

This uses `codex-package` because this plugin is an official-style package bundle, not a local notify runtime integration.

### Gemini

Generated file:

- `gemini-extension.json`

For Gemini the MCP config is projected inline under `mcpServers`.

### OpenCode

Generated file:

- `opencode.json`

For OpenCode the same stdio MCP server is projected as:

- `type: "local"`
- `command: ["npx", "-y", "@upstash/context7-mcp@2.1.6"]`

### Cursor

Generated file:

- `.cursor/mcp.json`

Cursor gets the repo-local MCP config without extra rules or `AGENTS.md`.

## Why Local `stdio`, Not Remote HTTP

This v1 example intentionally uses local `stdio`:

- it matches the official Claude `context7` plugin shape more closely
- it avoids API key and remote auth wiring in the first universal example
- it keeps the example deterministic and easy to copy

## How To Extend Later

Possible next step, but intentionally out of scope for this example:

- switch or add a remote MCP transport
- wire API-key-based auth headers
- add more target-native metadata where it gives real value

Keep v1 small first.
The point of this example is to show the minimum real package that works across all five targets from one authored MCP definition.
