# docker-hub

`docker-hub` is a real portable MCP plugin in this catalog.
It packages Docker's official Docker Hub MCP server once and projects it into `claude`, `codex-package`, `gemini`, `opencode`, and `cursor`.

This plugin uses the canonical `plugin/` layout:

- edit only `plugin/`
- treat the plugin root as generated and target-native output
- use root `AGENTS.md` as the main boundary doc, `CLAUDE.md` as the Claude pointer, and `GENERATED.md` before touching plugin-root files

## What This Plugin Does

This plugin starts Docker Hub's official MCP server through Docker itself.
It is the Docker Hub path for repository, image, and registry workflows through the `mcp/dockerhub` container image.

Typical use cases:

- inspect Docker Hub repositories and image metadata from the same workflow as active engineering work
- keep registry context close to release, platform, and dependency workflows
- use Docker's official image-backed server instead of rebuilding the same setup by hand per agent

## Source Of Truth

Author only these files by hand:

- `plugin/plugin.yaml`
- `plugin/mcp/servers.yaml`
- `plugin/README.md`

Everything else in the plugin root is generated and may be overwritten by `plugin-kit-ai generate`.

## Exact Commands

Run from this repository root:

```bash
cd plugins/docker-hub
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
../plugin-kit-ai/bin/plugin-kit-ai normalize ./plugins/docker-hub
../plugin-kit-ai/bin/plugin-kit-ai generate ./plugins/docker-hub
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
The shared `.mcp.json` carries the portable stdio definition used by multiple targets.

## Runtime Model

This v1 plugin is intentionally local and auth-first:

- local stdio MCP over `docker run`
- official image `mcp/dockerhub`
- required env vars `HUB_PAT_TOKEN` and `HUB_USERNAME`
- no launcher or separate runtime bundle

The auth-first default is intentional.
It is the useful Docker Hub default for real repository workflows, not the weakest possible setup.

## Required Environment

Set these in the client or shell environment used to launch the MCP server:

- `HUB_PAT_TOKEN`
- `HUB_USERNAME`

You also need a usable local Docker installation because the MCP server runs from Docker's official image.

## Why This Uses Docker-Run Stdio

This catalog plugin follows Docker's official image-backed MCP shape directly:

- one container image
- one stdio transport
- one portable projection across supported agents

That is cleaner than pretending Docker Hub is a hosted remote-only service when Docker's own MCP catalog documents the image-backed path.

## Out Of Scope For V1

These are intentionally not part of this first version:

- public-only unauthenticated defaults in authored config
- alternate install paths outside Docker's official image-backed setup
- `plugin/skills/**`
- runtime hooks or `launcher.yaml`

Keep the first Docker Hub catalog entry useful, official, and reproducible.
