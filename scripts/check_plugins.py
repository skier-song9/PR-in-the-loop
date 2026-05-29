#!/usr/bin/env python3
"""Lightweight repository check for Codex plugin marketplace layout."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def load_json(path: Path) -> dict:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except Exception as exc:  # noqa: BLE001
        raise SystemExit(f"invalid JSON: {path}: {exc}") from exc


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def check_skill(skill_path: Path) -> None:
    text = skill_path.read_text(encoding="utf-8")
    require(text.startswith("---\n"), f"missing frontmatter: {skill_path}")
    head = text.split("---", 2)[1]
    require("name:" in head, f"missing skill name: {skill_path}")
    require("description:" in head, f"missing skill description: {skill_path}")


def main() -> int:
    marketplace = load_json(MARKETPLACE)
    require(marketplace.get("name") == "pr-in-the-loop", "marketplace name must be pr-in-the-loop")
    plugins = marketplace.get("plugins")
    require(isinstance(plugins, list) and plugins, "marketplace plugins must be non-empty")

    seen: set[str] = set()
    for entry in plugins:
        name = entry.get("name")
        require(isinstance(name, str) and NAME_RE.match(name) is not None, f"bad plugin name: {name}")
        require(name not in seen, f"duplicate marketplace plugin: {name}")
        seen.add(name)

        source = entry.get("source") or {}
        rel_path = source.get("path")
        require(source.get("source") == "local", f"{name}: source must be local")
        require(isinstance(rel_path, str) and rel_path.startswith("./plugins/"), f"{name}: bad source path")

        plugin_dir = ROOT / rel_path.removeprefix("./")
        manifest_path = plugin_dir / ".codex-plugin" / "plugin.json"
        require(plugin_dir.is_dir(), f"{name}: missing plugin directory")
        manifest = load_json(manifest_path)
        require(manifest.get("name") == name, f"{name}: manifest name mismatch")
        require(manifest.get("skills") == "./skills/", f"{name}: skills path must be ./skills/")

        skills_dir = plugin_dir / "skills"
        require(skills_dir.is_dir(), f"{name}: missing skills directory")
        skill_files = sorted(skills_dir.glob("*/SKILL.md"))
        require(skill_files, f"{name}: no skills found")
        for skill_file in skill_files:
            check_skill(skill_file)

    print(f"OK: {len(seen)} plugins checked")
    return 0


if __name__ == "__main__":
    sys.exit(main())
