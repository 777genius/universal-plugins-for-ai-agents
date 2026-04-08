# gitlab

`gitlab` is a real portable MCP plugin in this catalog.
It shows the clean remote-MCP path for authoring one plugin once and generating working outputs for `claude`, `codex-package`, `gemini`, `opencode`, and `cursor`.

This plugin uses the canonical `src/` layout:

- edit only `src/`
- treat the plugin root as generated/native output
- use root `AGENTS.md` as the main boundary doc, `CLAUDE.md` as the Claude-specific pointer, and `GENERATED.md` before touching generated outputs

## What This Plugin Does

It connects agents to the official GitLab MCP server over HTTP at `https://gitlab.com/api/v4/mcp`.
That lets MCP-compatible clients authenticate with GitLab OAuth and then work with GitLab projects, issues, merge requests, and related DevOps workflows.

## Current GitLab.com Caveat

⚠️ As of April 5, 2026, GitLab documents this MCP endpoint publicly, but there is also an open GitLab.com issue reporting broken OAuth scope handling for the hosted `https://gitlab.com/api/v4/mcp` flow.

That means this plugin is structurally correct and matches the official HTTP MCP design, but real `gitlab.com` authentication may depend on GitLab fixing their hosted OAuth configuration.
If you run self-managed GitLab with MCP enabled, that path may be more reliable until the GitLab.com issue is resolved.

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
cd plugins/gitlab
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
../plugin-kit-ai/bin/plugin-kit-ai normalize ./plugins/gitlab
../plugin-kit-ai/bin/plugin-kit-ai generate ./plugins/gitlab
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
The shared `.mcp.json` is consumed by both Claude and Codex package outputs.

## Why This Uses Remote HTTP

This plugin intentionally uses remote MCP instead of local `stdio`:

- GitLab documents HTTP transport as the recommended connection path
- Claude Code, Gemini CLI, Cursor, and Codex all support direct HTTP for the GitLab MCP server
- it avoids adding a local `mcp-remote` dependency when the server already exposes a native MCP endpoint

## GitLab.com vs Self-Managed

This catalog plugin targets `gitlab.com` by default:

- `https://gitlab.com/api/v4/mcp`

For a self-managed GitLab instance, copy this plugin and change the URL in `src/mcp/servers.yaml` to your own instance:

- `https://<your-gitlab-host>/api/v4/mcp`

## How To Extend Later

Possible next steps, but intentionally out of scope for this v1 example:

- add a self-managed variant plugin with a different default URL
- add target-native metadata only if it gives real user value
- add extra documentation for enterprise OAuth rollout flows

Keep v1 small first.
