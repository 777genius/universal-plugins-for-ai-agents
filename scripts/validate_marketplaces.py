#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
from pathlib import Path

from sync_cursor_marketplace import (
    CURSOR_MARKETPLACE_PATH,
    build_cursor_marketplace_doc,
    discover_cursor_plugins,
)
from sync_gemini_marketplace import (
    GEMINI_MARKETPLACE_PATH,
    build_gemini_marketplace_doc,
    discover_gemini_plugins,
)


REPO_ROOT = Path(__file__).resolve().parent.parent
PLUGINS_ROOT = REPO_ROOT / "plugins"
CLAUDE_MARKETPLACE_PATH = REPO_ROOT / ".claude-plugin" / "marketplace.json"
CODEX_MARKETPLACE_PATH = REPO_ROOT / ".agents" / "plugins" / "marketplace.json"
MCP_CONFIG_PATH = ".mcp.json"

MARKETPLACE_NAME = "universal-plugins-for-ai-agents"
CLAUDE_OWNER_NAME = "777genius"
CODEX_DISPLAY_NAME = "Universal Plugins For AI Agents"
DEFAULT_CODEX_CATEGORY = "Developer Tools"
DEFAULT_INSTALLATION_POLICY = "AVAILABLE"
DEFAULT_AUTHENTICATION_POLICY = "ON_INSTALL"


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text())
    except FileNotFoundError as exc:
        raise SystemExit(f"Missing required file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc


def discover_plugin_manifests(bundle_dir: str) -> dict[str, dict]:
    discovered: dict[str, dict] = {}

    for manifest_path in sorted(PLUGINS_ROOT.glob(f"*/{bundle_dir}/plugin.json")):
        plugin_root = manifest_path.parent.parent
        manifest = load_json(manifest_path)
        plugin_name = manifest.get("name")

        if not isinstance(plugin_name, str) or not plugin_name:
            raise SystemExit(f"Plugin manifest is missing a valid name: {manifest_path}")
        if plugin_name != plugin_root.name:
            raise SystemExit(
                f"Plugin name drift in {manifest_path}: manifest name {plugin_name!r} "
                f"does not match directory name {plugin_root.name!r}"
            )

        discovered[plugin_name] = {
            "name": plugin_name,
            "description": manifest.get("description"),
            "version": manifest.get("version"),
            "plugin_root": plugin_root,
        }

    return discovered


def discover_transport_signatures() -> dict[str, list[dict[str, str]]]:
    signatures: dict[str, list[dict[str, str]]] = {}

    for mcp_path in sorted(PLUGINS_ROOT.glob(f"*/{MCP_CONFIG_PATH}")):
        plugin_root = mcp_path.parent
        plugin_name = plugin_root.name
        doc = load_json(mcp_path)
        servers = doc.get("mcpServers")
        if not isinstance(servers, dict):
            continue

        for server_name, server in servers.items():
            if not isinstance(server, dict):
                continue

            signature = None
            if isinstance(server.get("url"), str) and server.get("url"):
                signature = f"http::{server['url']}"
            elif isinstance(server.get("command"), str) and server.get("command"):
                args = server.get("args")
                joined_args = ""
                if isinstance(args, list):
                    joined_args = " ".join(str(arg) for arg in args)
                signature = f"stdio::{server['command']} {joined_args}".strip()

            if signature is None:
                continue

            signatures.setdefault(signature, []).append(
                {
                    "plugin": plugin_name,
                    "server": str(server_name),
                    "path": str(mcp_path.relative_to(REPO_ROOT)),
                }
            )

    return signatures


def validate_unique_transport_signatures(errors: list[str]) -> None:
    signatures = discover_transport_signatures()
    for signature, entries in sorted(signatures.items()):
        plugins = sorted({entry["plugin"] for entry in entries})
        if len(plugins) <= 1:
            continue
        rendered_entries = ", ".join(
            f"{entry['plugin']}:{entry['server']} ({entry['path']})" for entry in entries
        )
        errors.append(
            "duplicate MCP transport detected across plugins: "
            f"{signature!r} is used by {rendered_entries}"
        )


def validate_claude_marketplace(errors: list[str]) -> None:
    marketplace = load_json(CLAUDE_MARKETPLACE_PATH)
    expected = discover_plugin_manifests(".claude-plugin")

    if marketplace.get("name") != MARKETPLACE_NAME:
        errors.append(
            f"{CLAUDE_MARKETPLACE_PATH}: expected name {MARKETPLACE_NAME!r}, "
            f"got {marketplace.get('name')!r}"
        )

    owner_name = marketplace.get("owner", {}).get("name")
    if owner_name != CLAUDE_OWNER_NAME:
        errors.append(
            f"{CLAUDE_MARKETPLACE_PATH}: expected owner.name {CLAUDE_OWNER_NAME!r}, "
            f"got {owner_name!r}"
        )

    plugin_root = marketplace.get("metadata", {}).get("pluginRoot")
    if plugin_root != "./plugins":
        errors.append(
            f"{CLAUDE_MARKETPLACE_PATH}: expected metadata.pluginRoot './plugins', "
            f"got {plugin_root!r}"
        )

    actual_plugins = marketplace.get("plugins")
    if not isinstance(actual_plugins, list):
        errors.append(f"{CLAUDE_MARKETPLACE_PATH}: plugins must be an array")
        return

    actual_names = [plugin.get("name") for plugin in actual_plugins]
    expected_names = sorted(expected)

    if actual_names != expected_names:
        errors.append(
            f"{CLAUDE_MARKETPLACE_PATH}: plugin order or membership drift. "
            f"expected {expected_names}, got {actual_names}"
        )

    for plugin in actual_plugins:
        name = plugin.get("name")
        if name not in expected:
            continue

        manifest = expected[name]
        expected_source = f"./plugins/{name}"

        if plugin.get("source") != expected_source:
            errors.append(
                f"{CLAUDE_MARKETPLACE_PATH}: {name} source drift. "
                f"expected {expected_source!r}, got {plugin.get('source')!r}"
            )

        if plugin.get("description") != manifest["description"]:
            errors.append(
                f"{CLAUDE_MARKETPLACE_PATH}: {name} description drift. "
                f"expected {manifest['description']!r}, got {plugin.get('description')!r}"
            )

        if plugin.get("version") != manifest["version"]:
            errors.append(
                f"{CLAUDE_MARKETPLACE_PATH}: {name} version drift. "
                f"expected {manifest['version']!r}, got {plugin.get('version')!r}"
            )


def validate_codex_marketplace(errors: list[str]) -> None:
    marketplace = load_json(CODEX_MARKETPLACE_PATH)
    expected = discover_plugin_manifests(".codex-plugin")

    if marketplace.get("name") != MARKETPLACE_NAME:
        errors.append(
            f"{CODEX_MARKETPLACE_PATH}: expected name {MARKETPLACE_NAME!r}, "
            f"got {marketplace.get('name')!r}"
        )

    display_name = marketplace.get("interface", {}).get("displayName")
    if display_name != CODEX_DISPLAY_NAME:
        errors.append(
            f"{CODEX_MARKETPLACE_PATH}: expected interface.displayName {CODEX_DISPLAY_NAME!r}, "
            f"got {display_name!r}"
        )

    actual_plugins = marketplace.get("plugins")
    if not isinstance(actual_plugins, list):
        errors.append(f"{CODEX_MARKETPLACE_PATH}: plugins must be an array")
        return

    actual_names = [plugin.get("name") for plugin in actual_plugins]
    expected_names = sorted(expected)

    if actual_names != expected_names:
        errors.append(
            f"{CODEX_MARKETPLACE_PATH}: plugin order or membership drift. "
            f"expected {expected_names}, got {actual_names}"
        )

    for plugin in actual_plugins:
        name = plugin.get("name")
        if name not in expected:
            continue

        source = plugin.get("source", {})
        policy = plugin.get("policy", {})
        expected_path = f"./plugins/{name}"

        if source.get("source") != "local":
            errors.append(
                f"{CODEX_MARKETPLACE_PATH}: {name} source.source drift. "
                f"expected 'local', got {source.get('source')!r}"
            )

        if source.get("path") != expected_path:
            errors.append(
                f"{CODEX_MARKETPLACE_PATH}: {name} source.path drift. "
                f"expected {expected_path!r}, got {source.get('path')!r}"
            )

        if policy.get("installation") != DEFAULT_INSTALLATION_POLICY:
            errors.append(
                f"{CODEX_MARKETPLACE_PATH}: {name} installation policy drift. "
                f"expected {DEFAULT_INSTALLATION_POLICY!r}, got {policy.get('installation')!r}"
            )

        if policy.get("authentication") != DEFAULT_AUTHENTICATION_POLICY:
            errors.append(
                f"{CODEX_MARKETPLACE_PATH}: {name} authentication policy drift. "
                f"expected {DEFAULT_AUTHENTICATION_POLICY!r}, got {policy.get('authentication')!r}"
            )

        if plugin.get("category") != DEFAULT_CODEX_CATEGORY:
            errors.append(
                f"{CODEX_MARKETPLACE_PATH}: {name} category drift. "
                f"expected {DEFAULT_CODEX_CATEGORY!r}, got {plugin.get('category')!r}"
            )


def validate_cursor_marketplace(errors: list[str]) -> None:
    marketplace = load_json(CURSOR_MARKETPLACE_PATH)
    expected_plugins = discover_cursor_plugins()
    expected_marketplace = build_cursor_marketplace_doc(expected_plugins)

    if marketplace != expected_marketplace:
        errors.append(
            f"{CURSOR_MARKETPLACE_PATH}: marketplace manifest drift detected. "
            "Run python3 scripts/sync_cursor_marketplace.py to regenerate it."
        )

    expected_names = [plugin["name"] for plugin in expected_plugins]
    actual_plugins = marketplace.get("plugins")
    if not isinstance(actual_plugins, list):
        errors.append(f"{CURSOR_MARKETPLACE_PATH}: plugins must be an array")
        return

    actual_names = [plugin.get("name") for plugin in actual_plugins]
    if actual_names != expected_names:
        errors.append(
            f"{CURSOR_MARKETPLACE_PATH}: plugin order or membership drift. "
            f"expected {expected_names}, got {actual_names}"
        )

    for plugin in expected_plugins:
        manifest_path = plugin["plugin_dir"] / ".cursor-plugin" / "plugin.json"
        try:
            actual_manifest = load_json(manifest_path)
        except SystemExit as exc:
            errors.append(str(exc))
            continue

        if actual_manifest != plugin["cursor_manifest"]:
            errors.append(
                f"{manifest_path}: Cursor plugin manifest drift detected. "
                "Run python3 scripts/sync_cursor_marketplace.py to regenerate it."
            )


def validate_gemini_marketplace(errors: list[str]) -> None:
    marketplace = load_json(GEMINI_MARKETPLACE_PATH)
    expected_plugins = discover_gemini_plugins()
    expected_marketplace = build_gemini_marketplace_doc(expected_plugins)

    if marketplace != expected_marketplace:
        errors.append(
            f"{GEMINI_MARKETPLACE_PATH}: Gemini root extension drift detected. "
            "Run python3 scripts/sync_gemini_marketplace.py to regenerate it."
        )


def main() -> int:
    errors: list[str] = []

    validate_unique_transport_signatures(errors)
    validate_claude_marketplace(errors)
    validate_codex_marketplace(errors)
    validate_cursor_marketplace(errors)
    validate_gemini_marketplace(errors)

    if errors:
        print("Marketplace validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    claude_count = len(discover_plugin_manifests(".claude-plugin"))
    codex_count = len(discover_plugin_manifests(".codex-plugin"))
    cursor_count = len(discover_cursor_plugins())
    gemini_count = len(discover_gemini_plugins())
    print(
        "Marketplace catalogs are in sync "
        f"(Claude: {claude_count} plugins, Codex: {codex_count} plugins, "
        f"Cursor: {cursor_count} plugins, Gemini: {gemini_count} plugins)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
