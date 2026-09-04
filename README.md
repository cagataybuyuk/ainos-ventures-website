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
- Automated GitHub Actions site-quality checks

## Milestone status
- [x] Milestone 1 — Production shell
- [x] Milestone 2 — Production Candidate Home
- [x] Baseline technical hardening and CI quality gate
- [ ] Confirm public Selected Work wording / figures
- [ ] Finalise core team bios and roster
- [ ] Replace temporary rendered team cleanup with final EN/TR source markup
- [ ] Final logo / brand assets
- [ ] Social preview image
- [ ] Confirm contact email / contact flow
- [ ] Cross-browser + mobile QA
- [ ] Connect custom domain `ainosventures.com`

## Current staging
`https://ainos-ventures-website.vercel.app/en/`

## Waiting on stakeholder inputs
Brand assets, public case disclosure decisions, team-source material and contact details have been requested from Nidan. These are not blocking technical work.

## Working method
GitHub is the source of truth. Changes are committed to the repository and automatically deployed to Vercel for review. GitHub Actions validates core site structure, language metadata, anchors, local assets, sitemap and 404 indexing rules on each push and pull request.
