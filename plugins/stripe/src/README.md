# stripe

`stripe` is a real portable MCP plugin in this catalog.
It packages Stripe's official hosted MCP server once and projects it into `claude`, `codex-package`, `gemini`, `opencode`, and `cursor`.

This plugin uses the canonical `src/` layout:

- edit only `src/`
- treat the plugin root as generated and target-native output
- use root `AGENTS.md` as the main boundary doc, `CLAUDE.md` as the Claude pointer, and `GENERATED.md` before touching plugin-root files

## What This Plugin Does

This plugin connects agents to Stripe's hosted MCP service at `https://mcp.stripe.com`.
It is an official remote MCP integration for Stripe API workflows plus Stripe knowledge search.

Typical use cases:

- inspect customers, products, prices, subscriptions, invoices, refunds, and balance data
- search Stripe documentation and support knowledge from the same agent workflow
- let an authorized agent help with common billing and payments operations without leaving the workspace

Stripe's MCP surface includes real write-capable commerce tools, so this plugin keeps the setup explicit and conservative.

## Source Of Truth

Author only these files by hand:

- `src/plugin.yaml`
- `src/mcp/servers.yaml`
- `src/README.md`

Everything else in the plugin root is generated and may be overwritten by `plugin-kit-ai generate`.

## Exact Commands

Run from this repository root:

```bash
cd plugins/stripe
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
../plugin-kit-ai/bin/plugin-kit-ai normalize ./plugins/stripe
../plugin-kit-ai/bin/plugin-kit-ai generate ./plugins/stripe
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

This v1 plugin is intentionally hosted and remote-first:

- hosted Stripe MCP endpoint
- OAuth user authorization as the preferred path
- no bearer-token headers in authored config
- no local runtime or launcher path

That keeps the default install story aligned with Stripe's official guidance for interactive MCP clients.

## Why OAuth-First

Stripe documents two additional advanced paths:

- a bearer-token `Authorization` header for autonomous agents or MCP clients that do not support OAuth
- a local Stripe MCP server via `@stripe/mcp`

Those are real and useful, but they change the trust, secret-management, and operational story enough that they should not be hidden inside the default portable plugin definition.

For a shared community catalog, the cleanest default is:

- one hosted endpoint
- one preferred auth story
- no secrets baked into generated files

## Safety Note

Stripe explicitly recommends human confirmation and caution when using its MCP with other servers because commerce actions can be write-capable.

Treat this plugin as a privileged integration:

- prefer human approval for write actions
- keep OAuth sessions scoped to the right Stripe account
- if you later use restricted API keys for autonomous agents, do that in a separate variant with a much tighter safety story

## Out Of Scope For V1

These are intentionally not part of this first version:

- embedded bearer-token headers in authored config
- `src/skills/**`
- runtime hooks or `launcher.yaml`
- the local `@stripe/mcp` server path
- an autonomous token-driven variant

If later you need fully headless automation or a local Stripe CLI-style setup, those should become separate variants such as `stripe-autonomous` or `stripe-local`, not extra hidden modes inside this plugin.
