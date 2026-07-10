# Company archive site design

## Purpose

Create a private working preview that organizes Black Label's verified products, client systems, and reusable engineering work without overstating launch status. The repository name is temporary until the public brand is cleared.

## Audience

- Owners evaluating a custom business system.
- Technical partners evaluating engineering depth.
- Existing clients looking for a plain record of what was built.

## Information architecture

- **Work:** evidence-backed client and product case studies.
- **Products:** verified current surfaces with explicit status labels.
- **Systems:** local-first architecture, automation, release, and operations patterns.
- **Archive:** dated records and sanitized engineering extracts.
- **Contact:** a simple discussion path, with no fake checkout or false-success state.

## Homepage content contract

- Headline: “Software and AI operating systems businesses own.”
- Support: “We build local-first applications, automation, and custom operating infrastructure for real companies.”
- Primary action: “View verified work.”
- Secondary action: “Discuss a system.”
- Status words are limited to `Verified`, `Partial`, and `Building`, as defined in the archive.
- No invented metrics, testimonials, client logos, revenue, or launch claims.
- The preview includes a visible working-name notice and points to Black Label Bots as the current verified public surface.

## Visual direction

- True black and charcoal base with restrained brass/champagne accents.
- Editorial-industrial composition with open horizontal bands, not a dashboard of cards.
- Bold typography, generous space, proof-ledger and archive motifs.
- No neon treatment, hero badge, decorative metric wall, or fake terminal activity.

## Implementation gate

The complete visual concept must be generated and approved before site code is written. Until the public name is decided, every build must set `noindex`, use a preview URL, and avoid attaching `blacklabeltechnologies.com` or implying ownership of that name.

## Technical requirements

- Static-first, responsive, accessible, and deployable from a clean clone.
- One documented setup command and one documented build command.
- No local absolute paths, undeclared services, or hidden bootstrap patches.
- Content comes from versioned structured data.
- Automated checks validate status vocabulary, links, metadata, structured data, and the `noindex` gate.
