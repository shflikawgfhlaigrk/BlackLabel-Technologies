# Release truth check

Private clean-room candidate for a future public extract. It compares a release manifest with independently collected artifact metadata and fails when product identity, version, build, hash, architecture, signing, notarization, Gatekeeper status, download transport, or clean-install portability diverge.

This is a synthetic teaching example. It contains no Black Label product logic, client code, production identifiers, credentials, or operating data.

## Run

```bash
python3 src/release_truth_check.py \
  --manifest tests/fixtures/manifest-good.json \
  --artifact tests/fixtures/artifact-good.json
```

Expected output:

```text
release truth: PASS
```

Run tests:

```bash
python3 -m unittest discover -s tests -v
```

## Deliberate omissions

- It does not call `codesign`, `spctl`, `stapler`, or a release API. A production pipeline should collect those results independently and serialize them as artifact metadata.
- It does not install or launch an application.
- It does not authenticate a download URL.
- It does not implement product-specific updater logic.

The extract stays private until an explicit license is approved and the disclosure review is complete.
