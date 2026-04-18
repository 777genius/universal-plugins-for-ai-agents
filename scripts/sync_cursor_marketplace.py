#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
PLUGINS_ROOT = REPO_ROOT / "plugins"
CURSOR_MARKETPLACE_PATH = REPO_ROOT / ".cursor-plugin" / "marketplace.json"

MARKETPLACE_NAME = "universal-plugins-for-ai-agents"
OWNER_NAME = "777genius"
MARKETPLACE_DESCRIPTION = (
    "Portable Cursor plugin marketplace for the universal-plugins-for-ai-agents repository."
)
MARKETPLACE_VERSION = "1.0.0"
PLUGIN_ROOT = "plugins"
MCP_REF = "./.mcp.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def write_json(path: Path, doc: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, indent=2, sort_keys=False) + "\n")


def discover_cursor_plugins() -> list[dict]:
    discovered: list[dict] = []

    for plugin_dir in sorted(p for p in PLUGINS_ROOT.iterdir() if p.is_dir()):
        source_manifest_path = plugin_dir / ".codex-plugin" / "plugin.json"
        if not source_manifest_path.exists():
            source_manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
        if not source_manifest_path.exists():
            continue
        if not (plugin_dir / ".mcp.json").exists():
            continue

        source_manifest = load_json(source_manifest_path)
        name = source_manifest.get("name")
        if not isinstance(name, str) or not name:
            raise SystemExit(f"Cursor source manifest is missing a valid name: {source_manifest_path}")
        if name != plugin_dir.name:
            raise SystemExit(
                f"Cursor source manifest drift in {source_manifest_path}: "
                f"manifest name {name!r} does not match directory {plugin_dir.name!r}"
            )

        cursor_manifest = {
            "name": name,
            "displayName": source_manifest.get("displayName") or name,
            "version": source_manifest.get("version"),
            "description": source_manifest.get("description"),
            "mcpServers": MCP_REF,
        }
        for key in ("author", "homepage", "repository", "license", "keywords"):
            if key in source_manifest:
                cursor_manifest[key] = source_manifest[key]

        discovered.append(
            {
                "name": name,
                "version": source_manifest.get("version"),
                "description": source_manifest.get("description"),
                "plugin_dir": plugin_dir,
                "cursor_manifest": cursor_manifest,
                "marketplace_entry": {
                    "name": name,
                    "source": name,
                    "description": source_manifest.get("description"),
                    "version": source_manifest.get("version"),
                },
            }
        )

    return discovered


def build_cursor_marketplace_doc(plugins: list[dict]) -> dict:
    return {
        "name": MARKETPLACE_NAME,
        "owner": {
            "name": OWNER_NAME,
        },
        "metadata": {
            "description": MARKETPLACE_DESCRIPTION,
            "version": MARKETPLACE_VERSION,
            "pluginRoot": PLUGIN_ROOT,
        },
        "plugins": [plugin["marketplace_entry"] for plugin in plugins],
    }


def sync_cursor_marketplace() -> int:
    plugins = discover_cursor_plugins()

    for plugin in plugins:
        write_json(plugin["plugin_dir"] / ".cursor-plugin" / "plugin.json", plugin["cursor_manifest"])

    write_json(CURSOR_MARKETPLACE_PATH, build_cursor_marketplace_doc(plugins))
    print(f"Synced Cursor marketplace artifacts for {len(plugins)} plugins.")
    return 0


if __name__ == "__main__":
    raise SystemExit(sync_cursor_marketplace())
