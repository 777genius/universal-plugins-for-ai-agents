# universal-plugins-for-ai-agents

Universal plugin catalog for AI agents.

This repository is intended to hold portable, real plugin directories that can be generated for multiple targets such as:

- Claude
- Codex
- Gemini
- OpenCode
- Cursor

Current plugins:

- `plugins/chrome-devtools`: official Chrome DevTools MCP server packaged once for Claude, Codex, Gemini, OpenCode, and Cursor
- `plugins/context7`: shared MCP-first documentation lookup plugin based on `@upstash/context7-mcp`
- `plugins/gitlab`: remote MCP plugin for the official GitLab MCP server on `gitlab.com` with a note about the current hosted OAuth caveat

## Layout

Each plugin lives inside `plugins/`.

Example:

- `plugins/context7/src/plugin.yaml`
- `plugins/context7/src/mcp/servers.yaml`
- optional `plugins/context7/src/targets/...`
- `plugins/context7/src/README.md`
- `plugins/context7/CLAUDE.md` and `plugins/context7/AGENTS.md` mark the boundary between authored and generated files
- `plugins/context7/README.md` is generated from `plugins/context7/src/README.md`
- generated native artifacts are committed at the plugin root

## Authoring Flow

Each plugin should keep its authored source of truth in:

- `src/plugin.yaml`
- optional `src/mcp/servers.yaml`
- optional `src/targets/<platform>/...`
- edit only `src/`; treat plugin-root manifests as generated outputs

Then generate and validate with `plugin-kit-ai`.
