# universal-plugins-for-ai-agents

Universal plugin catalog for AI agents.

This repository is intended to hold portable, real plugin directories that can be generated for multiple targets such as:

- Claude
- Codex
- Gemini
- OpenCode
- Cursor

Current plugins:

- `context7`: shared MCP-first documentation lookup plugin based on `@upstash/context7-mcp`

## Layout

Each plugin lives in its own top-level directory.

Example:

- `context7/plugin.yaml`
- `context7/mcp/servers.yaml`
- `context7/targets/...`
- generated native artifacts committed next to the authored source

## Authoring Flow

Each plugin should keep its authored source of truth in:

- `plugin.yaml`
- optional `mcp/servers.yaml`
- optional `targets/<platform>/...`

Then generate and validate with `plugin-kit-ai`.
