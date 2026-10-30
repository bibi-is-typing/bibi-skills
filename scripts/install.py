#!/usr/bin/env python3
"""Install the selected local skill folders. No network or third-party packages."""
import argparse
from datetime import datetime, timezone
import os
from pathlib import Path
import shutil
import sys
import tempfile
import uuid
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ("korean-writing", "pm-frame")


def default_destination(target):
    return Path.home() / (".agents" if target == "codex" else ".claude") / "skills"


def install_one(source, destination, replace=False):
    """Stage first; back up a replaced skill as ZIP; restore it if swapping fails."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    backup = None
    with tempfile.TemporaryDirectory(prefix=".bibi-skills-", dir=destination.parent) as temporary:
        staging = Path(temporary) / "new"
        previous = Path(temporary) / "previous"
        shutil.copytree(source, staging)
        # Recheck after staging in case the destination changed since preflight.
        if destination.is_symlink() or (destination.exists() and not destination.is_dir()):
            raise ValueError(f"Not an ordinary skill directory: {destination}")
        if destination.exists():
            if not replace:
                raise ValueError(f"Already installed: {destination}")
            backup_dir = destination.parent / ".bibi-skills-backups"
            backup_dir.mkdir(exist_ok=True)
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            backup = backup_dir / f"{destination.name}-{stamp}-{uuid.uuid4().hex[:8]}.zip"
            with zipfile.ZipFile(backup, "x", zipfile.ZIP_DEFLATED) as archive:
                for path in sorted(destination.rglob("*")):
                    if path.is_symlink():
                        raise ValueError(f"Review symlink before replacing: {path}")
                    if path.is_file():
                        archive.write(path, Path(destination.name) / path.relative_to(destination))
                if archive.testzip() is not None:
                    raise ValueError(f"Backup verification failed: {backup}")
            destination.rename(previous)
        try:
            staging.rename(destination)
        except OSError:
            if previous.exists():
                previous.rename(destination)
            raise
    return backup


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True, choices=("codex", "claude-code", "both"))
    parser.add_argument("--skill", nargs="+", choices=SKILLS, default=list(SKILLS))
    parser.add_argument("--dest", type=Path, help="Custom skills directory; single target only")
    parser.add_argument("--replace", action="store_true", help="Back up and replace existing skills")
    parser.add_argument("--dry-run", action="store_true", help="Show the plan without writing files")
    args = parser.parse_args()
    if args.target == "both" and args.dest:
        parser.error("--dest requires a single --target")
    targets = ("codex", "claude-code") if args.target == "both" else (args.target,)
    plan = []
    errors = []
    for target in targets:
        folder = (args.dest or default_destination(target)).expanduser().absolute()
        for name in dict.fromkeys(args.skill):
            source = ROOT / target / name
            destination = folder / name
            if not (source / "SKILL.md").is_file():
                errors.append(f"Missing source: {source}")
            if destination.resolve().is_relative_to(ROOT.resolve()):
                errors.append(f"Installation destination must be outside this repository: {destination}")
            if destination.is_symlink() or (destination.exists() and not destination.is_dir()):
                errors.append(f"Review existing non-directory/symlink: {destination}")
            elif destination.exists() and not args.replace:
                errors.append(f"Already installed: {destination}; use --replace to back it up and update")
            if target == "codex" and args.dest is None:
                legacy = Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex") / "skills" / name
                if legacy.exists() and legacy.resolve() != destination.resolve():
                    errors.append(f"Existing Codex skill: {legacy}; use --dest '{legacy.parent}' to update it without creating duplicates")
            plan.append((source, destination))
    if errors:
        parser.exit(1, "\n".join(errors) + "\n")
    for source, destination in plan:
        print(f"{'Would install' if args.dry_run else 'Installing'} {source.parent.name}/{source.name} -> {destination}")
        if not args.dry_run:
            backup = install_one(source, destination, args.replace)
            if backup:
                print(f"Backup: {backup}")
    if not args.dry_run:
        print("Installed. Use $skill-name in Codex or /skill-name in Claude Code.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError) as error:
        print(f"Install failed: {error}", file=sys.stderr)
        sys.exit(1)
