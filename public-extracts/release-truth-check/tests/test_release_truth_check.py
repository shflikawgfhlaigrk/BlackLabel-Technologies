import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from release_truth_check import validate_release  # noqa: E402


MANIFEST = {
    "product": "Example App",
    "version": "1.2.3",
    "build": 42,
    "sha256": "a" * 64,
    "download_url": "https://downloads.example.invalid/example-app-42.zip",
    "team_id": "TEAM123456",
    "architectures": ["arm64", "x86_64"],
}

ARTIFACT = {
    "product": "Example App",
    "version": "1.2.3",
    "build": 42,
    "sha256": "a" * 64,
    "architectures": ["arm64", "x86_64"],
    "external_dependencies": [],
    "signing": {
        "identity": "Developer ID Application: Example Company (TEAM123456)",
        "team_id": "TEAM123456",
        "hardened_runtime": True,
        "notarized": True,
        "stapled": True,
        "gatekeeper": "accepted",
    },
}


class ReleaseTruthCheckTests(unittest.TestCase):
    def test_accepts_matching_portable_trusted_release(self):
        self.assertEqual(validate_release(MANIFEST, ARTIFACT), [])

    def test_rejects_manifest_and_artifact_build_mismatch(self):
        artifact = copy.deepcopy(ARTIFACT)
        artifact["build"] = 41
        self.assertIn("build mismatch: manifest=42 artifact=41", validate_release(MANIFEST, artifact))

    def test_rejects_ad_hoc_or_untrusted_signing(self):
        artifact = copy.deepcopy(ARTIFACT)
        artifact["signing"]["identity"] = "-"
        artifact["signing"]["gatekeeper"] = "rejected"
        issues = validate_release(MANIFEST, artifact)
        self.assertIn("signing identity must be a Developer ID Application identity", issues)
        self.assertIn("Gatekeeper assessment must be accepted", issues)

    def test_rejects_missing_https_download(self):
        manifest = copy.deepcopy(MANIFEST)
        manifest["download_url"] = ""
        self.assertIn("download_url must be an https URL", validate_release(manifest, ARTIFACT))

    def test_rejects_machine_bound_external_dependency(self):
        artifact = copy.deepcopy(ARTIFACT)
        artifact["external_dependencies"] = ["/Users/example/repo/.venv/bin/service"]
        self.assertIn(
            "external_dependencies must be empty for a clean-install release",
            validate_release(MANIFEST, artifact),
        )

    def test_rejects_mixed_architecture_types_without_type_error(self):
        manifest = copy.deepcopy(MANIFEST)
        manifest["architectures"] = ["arm64", 64]
        self.assertIn(
            "manifest architectures must contain only strings",
            validate_release(manifest, ARTIFACT),
        )

    def test_rejects_unhashable_non_string_architecture_without_type_error(self):
        artifact = copy.deepcopy(ARTIFACT)
        artifact["architectures"] = ["arm64", {"name": "x86_64"}]
        self.assertIn(
            "artifact architectures must contain only strings",
            validate_release(MANIFEST, artifact),
        )

    def test_cli_returns_zero_for_good_synthetic_fixture(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            manifest_path = tmp_path / "manifest.json"
            artifact_path = tmp_path / "artifact.json"
            manifest_path.write_text(json.dumps(MANIFEST), encoding="utf-8")
            artifact_path.write_text(json.dumps(ARTIFACT), encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "src" / "release_truth_check.py"),
                    "--manifest",
                    str(manifest_path),
                    "--artifact",
                    str(artifact_path),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("release truth: PASS", result.stdout)


if __name__ == "__main__":
    unittest.main()
