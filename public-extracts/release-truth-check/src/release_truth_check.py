#!/usr/bin/env python3
"""Validate that a release manifest and inspected artifact tell the same truth."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List
from urllib.parse import urlparse


SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def validate_release(manifest: Dict[str, Any], artifact: Dict[str, Any]) -> List[str]:
    issues: List[str] = []

    for key in ("product", "version", "build", "sha256", "download_url", "team_id", "architectures"):
        if key not in manifest:
            issues.append(f"manifest missing required field: {key}")
    for key in ("product", "version", "build", "sha256", "architectures", "external_dependencies", "signing"):
        if key not in artifact:
            issues.append(f"artifact missing required field: {key}")

    for key in ("product", "version", "build", "sha256"):
        if key in manifest and key in artifact and manifest[key] != artifact[key]:
            issues.append(f"{key} mismatch: manifest={manifest[key]} artifact={artifact[key]}")

    manifest_hash = str(manifest.get("sha256", ""))
    artifact_hash = str(artifact.get("sha256", ""))
    if manifest_hash and not SHA256_RE.fullmatch(manifest_hash):
        issues.append("manifest sha256 must be 64 lowercase hexadecimal characters")
    if artifact_hash and not SHA256_RE.fullmatch(artifact_hash):
        issues.append("artifact sha256 must be 64 lowercase hexadecimal characters")

    download_url = str(manifest.get("download_url", ""))
    parsed_download = urlparse(download_url)
    if parsed_download.scheme != "https" or not parsed_download.netloc:
        issues.append("download_url must be an https URL")

    manifest_architectures = manifest.get("architectures")
    artifact_architectures = artifact.get("architectures")
    if not isinstance(manifest_architectures, list) or not manifest_architectures:
        issues.append("manifest architectures must be a non-empty list")
    if not isinstance(artifact_architectures, list) or not artifact_architectures:
        issues.append("artifact architectures must be a non-empty list")
    if isinstance(manifest_architectures, list) and isinstance(artifact_architectures, list):
        if set(manifest_architectures) != set(artifact_architectures):
            issues.append(
                "architecture mismatch: "
                f"manifest={sorted(manifest_architectures)} artifact={sorted(artifact_architectures)}"
            )

    dependencies = artifact.get("external_dependencies")
    if dependencies != []:
        issues.append("external_dependencies must be empty for a clean-install release")

    signing = artifact.get("signing")
    if not isinstance(signing, dict):
        issues.append("artifact signing must be an object")
        signing = {}

    identity = str(signing.get("identity", ""))
    if not identity.startswith("Developer ID Application:"):
        issues.append("signing identity must be a Developer ID Application identity")

    manifest_team = str(manifest.get("team_id", ""))
    signing_team = str(signing.get("team_id", ""))
    if not manifest_team or manifest_team != signing_team:
        issues.append(f"team_id mismatch: manifest={manifest_team} artifact={signing_team}")

    for key, label in (
        ("hardened_runtime", "hardened runtime must be enabled"),
        ("notarized", "artifact must be notarized"),
        ("stapled", "notarization ticket must be stapled"),
    ):
        if signing.get(key) is not True:
            issues.append(label)

    if signing.get("gatekeeper") != "accepted":
        issues.append("Gatekeeper assessment must be accepted")

    return issues


def _read_json(path: Path) -> Dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--artifact", type=Path, required=True)
    args = parser.parse_args()

    try:
        issues = validate_release(_read_json(args.manifest), _read_json(args.artifact))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"release truth: ERROR\n- {exc}", file=sys.stderr)
        return 2

    if issues:
        print("release truth: FAIL")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print("release truth: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
