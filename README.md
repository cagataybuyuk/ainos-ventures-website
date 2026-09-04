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
- Accessible mobile navigation with keyboard focus management
- Skip-to-content support and reduced-motion handling
- Automated GitHub Actions site-quality checks
- Automated bilingual responsive visual QA at 1440 / 1024 / 768 / 390 / 360 px

## Approved positioning / brand direction
- Tagline: `Strategy · Capital · Partnership.`
- Warm ivory / off-white background
- Charcoal typography (`#1C1C1C` reference)
- Minimal editorial visual language
- Official vector logo package received

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
- [x] Official Ainos Ventures company LinkedIn linked from Contact
- [x] Official monogram applied to navigation and favicon
- [x] Headshot mapping confirmed: Nidan = photo 1; Tunca = photo 2
- [x] Founder headshots uploaded and published in centered responsive team cards
- [x] Founder role summaries aligned to responsibilities at Ainos Ventures
- [x] Accessibility / keyboard-navigation code pass
- [x] Custom domain connected: `ainosventures.com`; `www` redirects to apex
- [x] Visual responsive QA — EN/TR hero, Current Focus and Team reviewed at 1440 / 1024 / 768 / 390 / 360 px
- [ ] Production launch QA
- [ ] Final technical release checklist

## Remaining stakeholder inputs / decisions
- [ ] Final factual bio copy approval after LinkedIn/background review

## Explicitly deferred
- Social sharing / OG image
- First Ainos Intelligence article or brief
- Privacy / cookie setup until analytics and form setup are finalised

`info@ainosventures.com` is also available as a secondary company inbox.

## Current production / staging
Production: `https://ainosventures.com/`
Staging: `https://ainos-ventures-website.vercel.app/en/`

## Working method
GitHub is the source of truth. Changes are committed to the repository and automatically deployed to Vercel for review. GitHub Actions validates core site structure, language metadata, anchors, local assets, sitemap, JavaScript syntax, Vercel configuration, approved focus content, accessibility wiring, brand/contact/team wiring and 404 indexing rules on each push and pull request. A separate responsive visual workflow uses headless Chrome to capture EN and TR hero, Current Focus and Team views at five target viewport widths for visual regression review.
