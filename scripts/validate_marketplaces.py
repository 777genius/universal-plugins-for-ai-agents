#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
PLUGINS_ROOT = REPO_ROOT / "plugins"
CLAUDE_MARKETPLACE_PATH = REPO_ROOT / ".claude-plugin" / "marketplace.json"
CODEX_MARKETPLACE_PATH = REPO_ROOT / ".agents" / "plugins" / "marketplace.json"

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


def main() -> int:
    errors: list[str] = []

    validate_claude_marketplace(errors)
    validate_codex_marketplace(errors)

    if errors:
        print("Marketplace validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    claude_count = len(discover_plugin_manifests(".claude-plugin"))
    codex_count = len(discover_plugin_manifests(".codex-plugin"))
    print(
        "Marketplace catalogs are in sync "
        f"(Claude: {claude_count} plugins, Codex: {codex_count} plugins)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
