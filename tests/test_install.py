"""Exercise real installation and update outcomes in temporary directories."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/install.py"
spec = importlib.util.spec_from_file_location("install", SCRIPT)
install = importlib.util.module_from_spec(spec)
spec.loader.exec_module(install)


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.destination = self.root / "skills"

    def run_installer(self, *arguments, target="codex"):
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--target", target,
             "--dest", str(self.destination), *arguments],
            text=True, capture_output=True,
        )

    def test_fresh_installs_match_complete_platform_payload(self):
        for target in ("codex", "claude-code"):
            self.destination = self.root / target
            result = self.run_installer(target=target)
            self.assertEqual(result.returncode, 0, result.stderr)
            for name in install.SKILLS:
                source = ROOT / target / name
                for file in source.rglob("*"):
                    if file.is_file():
                        installed = self.destination / name / file.relative_to(source)
                        self.assertEqual(installed.read_bytes(), file.read_bytes())

    def test_collision_preflight_does_not_partially_install(self):
        existing = self.destination / "pm-frame"
        existing.mkdir(parents=True)
        (existing / "SKILL.md").write_text("my custom skill")
        result = self.run_installer()
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.destination / "korean-writing").exists())
        self.assertEqual((existing / "SKILL.md").read_text(), "my custom skill")

    def test_replace_preserves_custom_files_in_valid_backup(self):
        existing = self.destination / "korean-writing"
        (existing / "references").mkdir(parents=True)
        (existing / "SKILL.md").write_text("old skill")
        (existing / "references/custom.md").write_text("my notes")
        result = self.run_installer("--skill", "korean-writing", "--replace")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((existing / "SKILL.md").read_bytes(),
                         (ROOT / "codex/korean-writing/SKILL.md").read_bytes())
        self.assertFalse((existing / "references/custom.md").exists())
        archives = list((self.destination / ".bibi-skills-backups").glob("*.zip"))
        self.assertEqual(len(archives), 1)
        with zipfile.ZipFile(archives[0]) as archive:
            self.assertIsNone(archive.testzip())
            self.assertEqual(archive.read("korean-writing/SKILL.md"), b"old skill")
            self.assertEqual(archive.read("korean-writing/references/custom.md"), b"my notes")

    def test_dry_run_makes_no_directories(self):
        result = self.run_installer("--dry-run")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(self.destination.exists())

    def test_single_skill_does_not_install_other_skill(self):
        result = self.run_installer("--skill", "pm-frame", target="claude-code")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.destination / "pm-frame/SKILL.md").is_file())
        self.assertFalse((self.destination / "korean-writing").exists())

    def test_leaf_symlink_is_preserved_even_with_replace(self):
        original = self.root / "linked-skill"
        original.mkdir()
        (original / "SKILL.md").write_text("linked content")
        self.destination.mkdir()
        (self.destination / "pm-frame").symlink_to(original, target_is_directory=True)
        result = self.run_installer("--skill", "pm-frame", "--replace")
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue((self.destination / "pm-frame").is_symlink())
        self.assertEqual((original / "SKILL.md").read_text(), "linked content")

    def test_failed_swap_restores_existing_skill(self):
        existing = self.destination / "pm-frame"
        existing.mkdir(parents=True)
        (existing / "SKILL.md").write_text("restore me")
        real_rename = Path.rename

        def fail_new_swap(path, target):
            if path.name == "new":
                raise OSError("simulated write failure")
            return real_rename(path, target)

        with patch.object(Path, "rename", fail_new_swap):
            with self.assertRaises(OSError):
                install.install_one(ROOT / "codex/pm-frame", existing, replace=True)
        self.assertEqual((existing / "SKILL.md").read_text(), "restore me")


if __name__ == "__main__":
    unittest.main()
