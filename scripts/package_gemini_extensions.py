#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import shutil
import tarfile
import tempfile
from pathlib import Path

from sync_gemini_marketplace import build_gemini_marketplace_doc, discover_gemini_plugins


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DEST = REPO_ROOT / "artifacts" / "gemini-release-archives"
GEMINI_INCLUDE_PATHS = (
    "gemini-extension.json",
    "GEMINI.md",
    "README.md",
    "agents",
    "assets",
    "commands",
    "contexts",
    "hooks",
    "policies",
    "skills",
    "themes",
)
ROOT_GEMINI_INCLUDE_PATHS = ("README.md",)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def stage_gemini_extension(plugin_dir: Path, staging_dir: Path) -> None:
    for relative in GEMINI_INCLUDE_PATHS:
        source = plugin_dir / relative
        if not source.exists():
            continue
        target = staging_dir / relative
        if source.is_dir():
            shutil.copytree(source, target, dirs_exist_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)


def stage_root_gemini_bundle(staging_dir: Path, marketplace_doc: dict) -> None:
    manifest_path = staging_dir / "gemini-extension.json"
    manifest_path.write_text(json.dumps(marketplace_doc, indent=2, sort_keys=False) + "\n")

    for relative in ROOT_GEMINI_INCLUDE_PATHS:
        source = REPO_ROOT / relative
        if not source.exists():
            continue
        target = staging_dir / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def package_gemini_extensions(dest: Path) -> int:
    shutil.rmtree(dest, ignore_errors=True)
    dest.mkdir(parents=True, exist_ok=True)

    plugins = discover_gemini_plugins()
    for plugin in plugins:
        name = plugin["name"]
        plugin_dir = plugin["plugin_dir"]
        manifest = plugin["manifest"]
        if name != plugin_dir.name:
            raise SystemExit(
                f"Gemini manifest drift in {plugin_dir / 'gemini-extension.json'}: "
                f"manifest name {name!r} does not match directory {plugin_dir.name!r}"
            )

        archive_path = dest / f"{name}.tar.gz"
        with tempfile.TemporaryDirectory(prefix=f"gemini-{name}-") as tmp:
            staging_dir = Path(tmp)
            stage_gemini_extension(plugin_dir, staging_dir)

            staged_manifest_path = staging_dir / "gemini-extension.json"
            if not staged_manifest_path.exists():
                raise SystemExit(f"Packaged Gemini archive is missing gemini-extension.json: {archive_path}")

            staged_manifest = load_json(staged_manifest_path)
            if staged_manifest.get("name") != name:
                raise SystemExit(
                    f"Packaged Gemini archive manifest drift for {name}: "
                    f"expected {name!r}, got {staged_manifest.get('name')!r}"
                )
            if not staged_manifest.get("version"):
                raise SystemExit(f"Packaged Gemini archive manifest is missing version for {name}")

            with tarfile.open(archive_path, "w:gz") as tar:
                for staged_path in sorted(staging_dir.rglob("*")):
                    tar.add(staged_path, arcname=staged_path.relative_to(staging_dir))

    marketplace_doc = build_gemini_marketplace_doc(plugins)
    marketplace_name = marketplace_doc["name"]
    marketplace_archive_path = dest / f"{marketplace_name}.tar.gz"
    with tempfile.TemporaryDirectory(prefix="gemini-marketplace-") as tmp:
        staging_dir = Path(tmp)
        stage_root_gemini_bundle(staging_dir, marketplace_doc)

        staged_manifest_path = staging_dir / "gemini-extension.json"
        staged_manifest = load_json(staged_manifest_path)
        if staged_manifest.get("name") != marketplace_name:
            raise SystemExit(
                f"Packaged Gemini marketplace archive manifest drift: "
                f"expected {marketplace_name!r}, got {staged_manifest.get('name')!r}"
            )
        if not staged_manifest.get("version"):
            raise SystemExit("Packaged Gemini marketplace archive manifest is missing version")

        with tarfile.open(marketplace_archive_path, "w:gz") as tar:
            for staged_path in sorted(staging_dir.rglob("*")):
                tar.add(staged_path, arcname=staged_path.relative_to(staging_dir))

    print(f"Packaged {len(plugins) + 1} Gemini release archives into {dest}.")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Package release-ready Gemini extension archives from plugins/*."
    )
    parser.add_argument(
        "--dest",
        type=Path,
        default=DEFAULT_DEST,
        help=f"Destination directory for packaged archives (default: {DEFAULT_DEST})",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    raise SystemExit(package_gemini_extensions(args.dest.resolve()))
