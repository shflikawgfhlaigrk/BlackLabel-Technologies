# Public extracts policy

## Decision

Release curated, newly packaged examples—not slices copied directly from production repositories.

The first public material should explain engineering judgment and demonstrate narrow reusable patterns. It should not reveal the product moat, client implementation, operating data, deployment credentials, or machine-specific recovery shortcuts.

## Allowed candidates

- Small generic utilities with independent tests and no product-specific identifiers.
- Synthetic examples of updater validation, health checks, local-first storage, or release verification.
- Architecture diagrams and case studies that use verified claims and approved screenshots.
- Setup documentation that succeeds on a clean machine from declared prerequisites.

## Blocked material

- Full product, agent, model, automation, lead, trading, property, or client repositories.
- Real customer, order, lead, message, analytics, or financial data.
- Prompt libraries, scoring logic, proprietary orchestration, or production infrastructure maps.
- Secrets, internal URLs, signing assets, device identifiers, entitlement material, or account IDs.
- Code that depends on `/Users/...`, Homebrew-only absolute paths, an existing virtual environment, a hand-installed LaunchAgent, or undeclared local state.
- Any file with unclear third-party licensing or unclear client ownership.

## Required release gate

Every candidate must have all of the following:

1. A named owner and a one-sentence public purpose.
2. A clean-room directory created outside the production repository.
3. Synthetic fixtures only.
4. Secret and private-data scans with zero findings.
5. A clean-clone setup test on a fresh user environment.
6. Tests that exercise the advertised behavior.
7. A dependency and license review.
8. An explicit license chosen for that extract.
9. A statement of what was deliberately omitted.
10. Final human approval before the repository changes from private to public.

## First recommended extracts

1. `release-truth-check`: a synthetic macOS bundle/manifest verifier.
2. `local-service-readiness`: a generic sidecar readiness and stale-process example.
3. `proof-ledger-schema`: a generic evidence ledger with synthetic records.

These are recommendations, not approval to publish. Build and verify them privately first.
