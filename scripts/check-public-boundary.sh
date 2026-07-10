#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if find . -path './.git' -prune -o -type f \( \
  -name '*.p12' -o \
  -name '*.mobileprovision' -o \
  -name '*.provisionprofile' -o \
  -name '*.sqlite' -o \
  -name '*.sqlite3' -o \
  -name '*.db' -o \
  -name '.env' -o \
  \( -name '.env.*' ! -name '.env.example' \) -o \
  -name '*.key' -o \
  -name '*.pem' \
\) -print -quit | grep -q .; then
  echo 'Blocked private or signing artifact detected.' >&2
  exit 1
fi

set +e
grep -rEIq \
  --exclude-dir='.git' \
  --exclude='check-public-boundary.sh' \
  '(gho_|ghp_[A-Za-z0-9]{20,}|github_pat_|xoxb-[A-Za-z0-9-]{20,}|sk_live_|sk_test_|AKIA[0-9A-Z]{16}|-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----)' \
  .
credential_scan_status=$?
set -e

case "$credential_scan_status" in
  0)
    echo 'Potential credential detected.' >&2
    exit 1
    ;;
  1) ;;
  *)
    echo 'Credential scan could not complete.' >&2
    exit 2
    ;;
esac

echo 'Public boundary checks passed.'
