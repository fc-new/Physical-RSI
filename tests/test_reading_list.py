from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ReadingListChecks(unittest.TestCase):
    def run_script(self, name: str, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(ROOT / "scripts" / name), *args],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )

    def test_schema_is_valid(self) -> None:
        result = self.run_script("validate_reading_list.py")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_readme_is_rendered(self) -> None:
        result = self.run_script("render_readme.py", "--check")
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
