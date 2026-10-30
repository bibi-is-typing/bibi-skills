#!/usr/bin/env python3
"""Build the self-contained Claude Code variants from the Codex source folders."""
import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ("korean-writing", "pm-frame")


def claude_skill(text, name):
    """Only adapt platform-specific instructions; preserve the shared workflow."""
    replacements = {
        "  adapted_for: Codex": "  adapted_for: Claude Code",
        f"${name}": f"/{name}",
        "## Codex에서 사용": "## Claude Code에서 사용",
        "Codex에 사용자 입력 도구가 있으면 그 도구를 쓰되 모드 제약을 따른다.":
            "Claude Code에서 사용자 질문 도구를 쓸 수 있으면 사용하되 현재 권한과 모드 제약을 따른다.",
        "프로젝트 없는 Codex 채팅은 안내된 outputs 폴더를 사용한다.":
            "프로젝트 문서 위치가 없으면 현재 작업 폴더에 저장한다.",
    }
    for before, after in replacements.items():
        text = text.replace(before, after)
    if "Codex" in text:
        raise ValueError(f"Unmapped Codex instruction in {name}/SKILL.md")
    return text


def expected_files():
    files = {}
    for name in SKILLS:
        source = ROOT / "codex" / name
        for path in sorted(source.rglob("*")):
            if not path.is_file():
                continue
            relative = path.relative_to(source)
            if relative.parts[0] == "agents":
                continue
            data = path.read_bytes()
            if relative == Path("SKILL.md"):
                data = claude_skill(data.decode("utf-8"), name).encode("utf-8")
            files[Path(name) / relative] = data
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check without writing files")
    args = parser.parse_args()
    destination = ROOT / "claude-code"
    expected = expected_files()
    actual = {p.relative_to(destination) for name in SKILLS
              for p in (destination / name).rglob("*") if p.is_file()}
    stale = actual - expected.keys()
    changed = [p for p, data in expected.items()
               if not (destination / p).is_file() or (destination / p).read_bytes() != data]
    if args.check:
        if stale or changed:
            for path in sorted(stale | set(changed)):
                print(f"Out of sync: claude-code/{path}", file=sys.stderr)
            return 1
        print("Claude Code variants are in sync.")
        return 0
    # Unknown extra files are never deleted by the generator.
    if stale:
        parser.error("Unexpected files in claude-code; review them before syncing: "
                     + ", ".join(str(p) for p in sorted(stale)))
    for relative in changed:
        path = destination / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(expected[relative])
    print(f"Synced {len(changed)} files to claude-code/.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
