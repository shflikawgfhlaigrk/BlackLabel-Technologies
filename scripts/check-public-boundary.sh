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
  -name '*.key' -o \
  -name '*.pem' \
\) -print | grep -q .; then
  echo 'Blocked private or signing artifact detected.' >&2
  exit 1
fi

if rg --hidden --glob '!.git/**' --glob '!scripts/check-public-boundary.sh' \
  '(gho_|github_pat_|sk_live_|sk_test_|AKIA[0-9A-Z]{16}|-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----)' .; then
  echo 'Potential credential detected.' >&2
  exit 1
fi

echo 'Public boundary checks passed.'
