#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
PLUGINS_ROOT = REPO_ROOT / "plugins"
GEMINI_MARKETPLACE_PATH = REPO_ROOT / "gemini-extension.json"

MARKETPLACE_NAME = "universal-plugins-for-ai-agents"
MARKETPLACE_VERSION = "0.1.0"
MARKETPLACE_DESCRIPTION = (
    "Bundled Gemini CLI extension that exposes the Gemini-compatible plugins "
    "from the universal-plugins-for-ai-agents catalog."
)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def write_json(path: Path, doc: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, indent=2, sort_keys=False) + "\n")


def discover_gemini_plugins() -> list[dict]:
    discovered: list[dict] = []

    for plugin_dir in sorted(p for p in PLUGINS_ROOT.iterdir() if p.is_dir()):
        manifest_path = plugin_dir / "gemini-extension.json"
        if not manifest_path.exists():
            continue

        manifest = load_json(manifest_path)
        name = manifest.get("name")
        if not isinstance(name, str) or not name:
            raise SystemExit(f"Gemini manifest is missing a valid name: {manifest_path}")
        if name != plugin_dir.name:
            raise SystemExit(
                f"Gemini manifest drift in {manifest_path}: "
                f"manifest name {name!r} does not match directory {plugin_dir.name!r}"
            )

        mcp_servers = manifest.get("mcpServers")
        if not isinstance(mcp_servers, dict) or not mcp_servers:
            raise SystemExit(f"Gemini manifest is missing mcpServers: {manifest_path}")

        discovered.append(
            {
                "name": name,
                "version": manifest.get("version"),
                "description": manifest.get("description"),
                "plugin_dir": plugin_dir,
                "manifest": manifest,
                "mcp_servers": mcp_servers,
            }
        )

    return discovered


def build_gemini_marketplace_doc(plugins: list[dict]) -> dict:
    merged_servers: dict = {}
    for plugin in plugins:
        for server_name, server_config in plugin["mcp_servers"].items():
            if server_name in merged_servers:
                raise SystemExit(
                    f"Gemini marketplace server name collision: {server_name!r} "
                    f"from plugin {plugin['name']!r}"
                )
            merged_servers[server_name] = server_config

    return {
        "name": MARKETPLACE_NAME,
        "version": MARKETPLACE_VERSION,
        "description": MARKETPLACE_DESCRIPTION,
        "mcpServers": merged_servers,
    }


def sync_gemini_marketplace() -> int:
    plugins = discover_gemini_plugins()
    write_json(GEMINI_MARKETPLACE_PATH, build_gemini_marketplace_doc(plugins))
    print(f"Synced Gemini root extension for {len(plugins)} plugins.")
    return 0


if __name__ == "__main__":
    raise SystemExit(sync_gemini_marketplace())
