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
- Minimal favicon
- Accessible mobile navigation
- Automated GitHub Actions site-quality checks

## Milestone status
- [x] Milestone 1 — Production shell
- [x] Milestone 2 — Production Candidate Home
- [x] Baseline technical hardening and CI quality gate
- [x] Remove Mert Özel from EN/TR source and rebalance the core-team layout
- [ ] Cross-browser + mobile QA
- [ ] Final launch QA
- [ ] Connect custom domain `ainosventures.com`

## Waiting on stakeholder inputs
The following items are intentionally waiting until materials arrive from Nidan:
- [ ] Confirm public Selected Work wording / figures
- [ ] Finalise core team bios and public roster details
- [ ] Final logo / brand assets
- [ ] Social preview image based on final brand assets
- [ ] Confirm contact email / contact flow

These items do not block technical hardening or QA work.

## Current staging
`https://ainos-ventures-website.vercel.app/en/`

## Working method
GitHub is the source of truth. Changes are committed to the repository and automatically deployed to Vercel for review. GitHub Actions validates core site structure, language metadata, anchors, local assets, sitemap and 404 indexing rules on each push and pull request.
