#!/usr/bin/env python3
"""Check package structure, required fields, self-contained links, and platform sync."""
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ("korean-writing", "pm-frame")


def local_links(path, boundary):
    errors = []
    text = path.read_text(encoding="utf-8")
    for target in re.findall(r"\[[^\]\n]*\]\(([^)\s]+)\)", text):
        if re.match(r"^[a-z]+:", target) or target.startswith("#"):
            continue
        resolved = (path.parent / target.split("#")[0]).resolve()
        if not resolved.is_relative_to(boundary.resolve()) or not resolved.is_file():
            errors.append(f"Broken or escaping link: {path.relative_to(ROOT)} -> {target}")
    return errors


def main():
    errors = []
    count = 0
    for target in ("codex", "claude-code"):
        for name in SKILLS:
            folder = ROOT / target / name
            skill = folder / "SKILL.md"
            if not skill.is_file():
                errors.append(f"Missing SKILL.md: {target}/{name}")
                continue
            text = skill.read_text(encoding="utf-8")
            frontmatter = re.match(r"^---\n(.*?)\n---\n", text, re.S)
            if not frontmatter:
                errors.append(f"Missing frontmatter: {target}/{name}")
                continue
            fields = dict(re.findall(r"^(name|description):\s*(.+)$", frontmatter[1], re.M))
            if fields.get("name") != name or not 1 <= len(fields.get("description", "")) <= 1024:
                errors.append(f"Invalid name/description: {target}/{name}")
            if target == "codex" and not (folder / "agents/openai.yaml").is_file():
                errors.append(f"Missing Codex metadata: {name}")
            if target == "claude-code" and (folder / "agents").exists():
                errors.append(f"Codex metadata in Claude Code package: {name}")
            for path in folder.rglob("*"):
                if path.is_symlink():
                    errors.append(f"Package must be self-contained, found symlink: {path}")
                if path.is_file() and path.suffix == ".md":
                    errors.extend(local_links(path, folder))
            count += 1
    for path in (ROOT / "README.md", ROOT / "LICENSES.md",
                 ROOT / "codex/README.md", ROOT / "claude-code/README.md"):
        errors.extend(local_links(path, ROOT))
    result = subprocess.run([sys.executable, str(ROOT / "scripts/sync_claude.py"), "--check"])
    if result.returncode:
        errors.append("Claude Code generation check failed")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"Validated {count} skill packages and README links.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
