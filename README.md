# Ainos Ventures Website

Production repository for the bilingual Ainos Ventures corporate website.

## Current architecture
- Static HTML / CSS / vanilla JavaScript
- English route: `/en/`
- Turkish route: `/tr/`
- Shared visual system and responsive layout
- Canonical + hreflang metadata
- `robots.txt` + bilingual `sitemap.xml`
- Vercel deployment config
- Baseline security headers
- Branded 404 page
- Official Ainos monogram favicon / navigation mark
- Accessible mobile navigation
- Automated GitHub Actions site-quality checks

## Approved positioning / brand direction
- Tagline: `Strategy · Capital · Partnership.`
- Warm ivory / off-white background
- Charcoal typography (`#1C1C1C` reference)
- Minimal editorial visual language
- Official vector logo package received
- Business-card visual can remain an optional reference if exact print-layout matching is needed

## Milestone status
- [x] Milestone 1 — Production shell
- [x] Milestone 2 — Production Candidate Home
- [x] Baseline technical hardening and CI quality gate
- [x] Final core-team roster confirmed: Tunca Cingöz — Co-Founder; Nidan Akmanoğlu — Co-Founder
- [x] Mert Özel removed from EN/TR source and core-team layout rebalanced
- [x] Replace Selected Work / deal figures with Current Focus
- [x] Current Focus approved categories: Energy & Infrastructure; Industrial & Technology; Consumer & Hospitality; Digital Assets & Technology
- [x] Public contact route confirmed; website uses `contact@ainosventures.com`
- [x] Personal LinkedIn profiles received for both co-founders
- [x] Official monogram applied to navigation and favicon
- [ ] Cross-browser + mobile QA
- [ ] Final launch QA
- [ ] Connect custom domain `ainosventures.com`

## Waiting on stakeholder inputs / decisions
- [ ] Explicit mapping of the two supplied headshots to Tunca / Nidan before publishing them
- [ ] Final factual bio copy approval after LinkedIn/background review
- [ ] Official Ainos Ventures company LinkedIn URL, if/when created
- [ ] Social preview image based on final brand assets

`info@ainosventures.com` is also available as a secondary company inbox.

These items do not block technical hardening or QA work.

## Current staging
`https://ainos-ventures-website.vercel.app/en/`

## Working method
GitHub is the source of truth. Changes are committed to the repository and automatically deployed to Vercel for review. GitHub Actions validates core site structure, language metadata, anchors, local assets, sitemap, JavaScript syntax, Vercel configuration and 404 indexing rules on each push and pull request.
