# chrome-devtools

`chrome-devtools` is a real portable MCP plugin in this catalog.
It packages the official `chrome-devtools-mcp` server once and projects working outputs for `claude`, `codex-package`, `gemini`, `opencode`, and `cursor`.

This plugin uses the canonical `src/` layout:

- edit only `src/`
- treat the plugin root as generated/native output
- use root `CLAUDE.md` and `AGENTS.md` as boundary docs for humans and agents, and read root `GENERATED.md` before touching generated outputs

## What This Plugin Does

It launches the official `chrome-devtools-mcp@0.21.0` server through local `stdio`.
That lets supported agent clients open or connect to Chrome, inspect pages, automate browser flows, capture screenshots and snapshots, and analyze performance through the official Chrome DevTools MCP toolset.

## Source Of Truth

Author only these files by hand:

- `src/plugin.yaml`
- `src/mcp/servers.yaml`
- `src/README.md`

Everything else in the plugin root is generated and may be overwritten by `plugin-kit-ai generate`.

The MCP source file uses `api_version: v1` as the canonical schema marker.

## Exact Commands

Run from this repository root:

```bash
cd plugins/chrome-devtools
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
../plugin-kit-ai/bin/plugin-kit-ai normalize ./plugins/chrome-devtools
../plugin-kit-ai/bin/plugin-kit-ai generate ./plugins/chrome-devtools
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
`README.md` is the generated mirror of this file.
The shared `.mcp.json` is consumed by both Claude and Codex package outputs.

## Why This Uses Local `stdio`

This plugin follows the official baseline install shape from the upstream repo:

- `npx -y chrome-devtools-mcp@...`
- no wrapper service
- no custom proxy layer

That keeps the plugin close to the official server behavior across clients.

## Why This Pins `0.21.0`

The official docs often show `chrome-devtools-mcp@latest`.
This catalog plugin pins `0.21.0` instead so the generated plugin stays reproducible and reviewable.

If you intentionally want rolling upstream updates, change the package in `src/mcp/servers.yaml` from:

- `chrome-devtools-mcp@0.21.0`

to:

- `chrome-devtools-mcp@latest`

and regenerate.

## Official Requirements

The upstream server currently requires:

- Node.js `^20.19.0 || ^22.12.0 || >=23`
- npm
- Chrome stable or newer

## Useful Upstream Flags

If you want different runtime behavior later, add official upstream flags in `src/mcp/servers.yaml`, then regenerate.
Useful examples from the official docs:

- `--headless`
- `--slim`
- `--isolated=true`
- `--browser-url=http://127.0.0.1:9222`
- `--autoConnect`
- `--no-usage-statistics`

## Comparison With The Referenced Codex Wrapper

The referenced `chrome-devtools-codex-plugin` is directionally right, but it is not complete as checked in:

- it claims a plugin-local `.mcp.json`, but that file is missing
- it claims `agents/openai.yaml`, but that file is also missing
- so as committed, it does not fully match its own README or a complete Codex package layout

This catalog plugin fixes that by using one canonical authored source and committing the generated native artifacts explicitly.

## How To Extend Later

Possible next steps, but intentionally out of scope for this v1 example:

- add a second plugin variant tuned for `--slim --headless`
- add a variant preconfigured for `--browser-url=http://127.0.0.1:9222`
- add portable skills only if they bring clear value across targets

Keep v1 small first.
