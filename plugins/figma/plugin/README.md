# figma

`figma` is an official hosted MCP plugin in this catalog.
It packages Figma's remote MCP server once and projects it into the three client lanes Figma explicitly documents today in our target model: `claude`, `codex-package`, and `cursor`.

This plugin uses the canonical `plugin/` layout:

- edit only `plugin/`
- treat the plugin root as generated and target-native output
- use root `AGENTS.md` as the main boundary doc, `CLAUDE.md` as the Claude pointer, and `GENERATED.md` before touching plugin-root files

## What This Plugin Does

This plugin connects agents to Figma's hosted MCP service at `https://mcp.figma.com/mcp`.
It is designed for interactive, user-authorized access to Figma Design, FigJam, and Make through OAuth.

Typical use cases:

- pull exact design context from frames and layers
- inspect variables, components, and layout structure
- help implement designs from shared Figma links
- use code-to-canvas and design-to-code workflows on supported clients

## Why This Plugin Targets Only Claude, Codex, And Cursor

This is an intentionally honest subset plugin.

Figma's current remote-server docs say only clients listed in the Figma MCP Catalog can connect, and the official install guides in this area are published for:

- `claude`
- `codex-package`
- `cursor`

Figma does not currently publish an official hosted MCP connection path here for `gemini` or `opencode`, so this plugin does not pretend that those lanes are first-class supported.

## Source Of Truth

Author only these files by hand:

- `plugin/plugin.yaml`
- `plugin/mcp/servers.yaml`
- `plugin/README.md`

Everything else in the plugin root is generated and may be overwritten by `plugin-kit-ai generate`.

## Exact Commands

Run from this repository root:

```bash
cd plugins/figma
plugin-kit-ai normalize .
plugin-kit-ai generate .
plugin-kit-ai generate --check .
plugin-kit-ai validate . --platform claude --strict
plugin-kit-ai validate . --platform codex-package --strict
plugin-kit-ai validate . --platform cursor --strict
```

If you are working from the `plugin-kit-ai` source repo instead of a globally installed CLI, use its built binary against this directory:

```bash
../plugin-kit-ai/bin/plugin-kit-ai normalize ./plugins/figma
../plugin-kit-ai/bin/plugin-kit-ai generate ./plugins/figma
```

## Generated Outputs

`plugin-kit-ai generate .` writes these managed root artifacts:

- `GENERATED.md`
- `README.md`
- `.claude-plugin/plugin.json`
- `.codex-plugin/plugin.json`
- `.mcp.json`
- `.cursor/mcp.json`

`GENERATED.md` is the generated inventory of managed outputs in the plugin root.
Root `README.md` is a short generated entrypoint that points readers back to this file.
The shared `.mcp.json` carries the portable remote MCP definition used by the supported targets.

## Auth Model

This v1 plugin is intentionally hosted and remote-only:

- hosted Figma MCP endpoint
- OAuth user authorization
- no local desktop-server path in authored config
- no local runtime or launcher path

That makes `figma` a good fit for design-context workflows, not for self-managed local bridging.

## Out Of Scope For V1

These are intentionally not part of this first version:

- the local Figma desktop-server install mode
- `gemini` or `opencode` support without Figma-published connection guides
- `plugin/skills/**`
- runtime hooks or `launcher.yaml`

If later Figma publishes a broader client matrix, we can widen the targets then.
