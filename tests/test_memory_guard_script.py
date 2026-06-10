from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "plugins/pr-in-the-loop/scripts/ensure-memory-gitignore.sh"


class MemoryGuardScriptTest(unittest.TestCase):
    def test_script_creates_and_ignores_open_issue_and_planning_pr_memory(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workdir = Path(tmpdir)
            subprocess.run(["git", "init"], cwd=workdir, check=True, stdout=subprocess.DEVNULL)

            result = subprocess.run(
                ["sh", str(SCRIPT)],
                cwd=workdir,
                check=True,
                text=True,
                capture_output=True,
            )

            self.assertIn("ok: .memory/ is ignored by git", result.stdout)
            self.assertTrue((workdir / ".memory/open-issue").is_dir())
            self.assertTrue((workdir / ".memory/planning-pr").is_dir())

            for memory_file in [
                ".memory/open-issue/work-context.md",
                ".memory/planning-pr/work-context.md",
            ]:
                subprocess.run(
                    ["git", "check-ignore", "-q", memory_file],
                    cwd=workdir,
                    check=True,
                )


if __name__ == "__main__":
    unittest.main()
