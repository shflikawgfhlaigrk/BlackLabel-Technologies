import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCANNER = ROOT / "scripts" / "check-public-boundary.sh"
FIXTURES = ROOT / "tests" / "fixtures" / "public-boundary"


class PublicBoundaryTests(unittest.TestCase):
    def _run_fixture(self, fixture_name: str) -> tuple[subprocess.CompletedProcess[str], str]:
        fixture = json.loads((FIXTURES / fixture_name).read_text(encoding="utf-8"))
        relative_path = "".join(fixture["path_parts"])
        content = "".join(fixture["content_parts"])

        with tempfile.TemporaryDirectory() as tmp:
            scan_root = Path(tmp)
            copied_scanner = scan_root / "scripts" / SCANNER.name
            copied_scanner.parent.mkdir(parents=True)
            shutil.copy2(SCANNER, copied_scanner)

            leak_path = scan_root / relative_path
            leak_path.parent.mkdir(parents=True, exist_ok=True)
            leak_path.write_text(content, encoding="utf-8")

            result = subprocess.run(
                ["bash", str(copied_scanner)],
                check=False,
                capture_output=True,
                text=True,
            )

        return result, content.strip()

    def _assert_rejected_without_echoing(self, fixture_name: str) -> None:
        result, sensitive_content = self._run_fixture(fixture_name)
        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0, output)
        self.assertNotIn(sensitive_content, output)

    def test_rejects_ghp_token_without_echoing_it(self):
        self._assert_rejected_without_echoing("ghp-token.json")

    def test_rejects_xoxb_token_without_echoing_it(self):
        self._assert_rejected_without_echoing("xoxb-token.json")

    def test_rejects_env_production_file(self):
        self._assert_rejected_without_echoing("env-production.json")

    def test_existing_credential_detection_does_not_echo_secret(self):
        self._assert_rejected_without_echoing("gho-token.json")


if __name__ == "__main__":
    unittest.main()
