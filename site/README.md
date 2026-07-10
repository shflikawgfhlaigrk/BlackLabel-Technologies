# Company-site working area

Static-first site for the working name **Black Label Technologies**, built per
[the site design spec](../docs/superpowers/specs/2026-07-10-company-archive-site-design.md).
Founder authorized implementation and the `blacklabeltec.com` domain on 2026-07-10
(supersedes the earlier "no production domain approved" note — the approved domain is
blacklabeltec.com; `blacklabeltechnologies.com` remains unattached).

All content renders from versioned structured data (`data/site.json`). Status vocabulary is
limited to `Verified` / `Partial` / `Building`. No invented metrics, testimonials, logos,
revenue, or launch claims — `check.js` enforces this and fails the build otherwise.

**The `noindex` gate is ON** (`meta.noindex` in `data/site.json`): the page ships
`<meta name="robots" content="noindex">` and a disallow-all `robots.txt` until the founder
approves public indexing. Flip `meta.noindex` to `false` to release, then rebuild + redeploy.

## Setup (one command)

No dependencies beyond Node ≥ 18:

    node --version

## Build (one command)

    node build.js && node check.js

Output lands in `dist/` (git-ignored). `check.js` validates status vocabulary, fabrication
patterns, the noindex gate, the working-name notice, machine-local path leaks, links, and metadata.

## Deploy

    npx wrangler pages deploy dist --project-name=blacklabeltec

Custom domains `blacklabeltec.com` and `www.blacklabeltec.com` attach to the Pages project
(Cloudflare manages the DNS records for attached domains automatically).
