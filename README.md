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

## Approved positioning / brand direction
- Tagline: `Strategy · Capital · Partnership.`
- Warm ivory / off-white background
- Charcoal typography
- Minimal editorial visual language
- Business card visual will be used as the primary final brand reference once received

## Milestone status
- [x] Milestone 1 — Production shell
- [x] Milestone 2 — Production Candidate Home
- [x] Baseline technical hardening and CI quality gate
- [x] Final core-team roster confirmed: Tunca Cingöz — Co-Founder; Nidan Akmanoğlu — Co-Founder
- [x] Mert Özel removed from EN/TR source and core-team layout rebalanced
- [x] Replace Selected Work / deal figures with Current Focus
- [x] Current Focus approved categories: Energy & Infrastructure; Industrial & Technology; Consumer & Hospitality; Digital Assets & Technology
- [ ] Cross-browser + mobile QA
- [ ] Final launch QA
- [ ] Connect custom domain `ainosventures.com`

## Waiting on stakeholder inputs
The following items remain parked until materials arrive from Nidan:
- [ ] Final logo / business-card visual / source brand assets
- [ ] Factual source material for final Tunca and Nidan bios
- [ ] Confirm team photography approach / provide headshots if used
- [ ] Confirm public contact email / contact flow
- [ ] Official Ainos Ventures LinkedIn URL
- [ ] Social preview image after final brand assets

These items do not block technical hardening or QA work.

## Current staging
`https://ainos-ventures-website.vercel.app/en/`

## Working method
GitHub is the source of truth. Changes are committed to the repository and automatically deployed to Vercel for review. GitHub Actions validates core site structure, language metadata, anchors, local assets, sitemap, JavaScript syntax, Vercel configuration and 404 indexing rules on each push and pull request.
