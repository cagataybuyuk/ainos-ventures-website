# Ainos Ventures Website

Production repository for the bilingual Ainos Ventures corporate website.

> **Project scope:** this repository tracks website work only — product/content changes, GitHub/Vercel delivery, domain/SEO, QA and website-specific brand implementation. Corporate decks, Qatar/GCC business development and other Ainos Ventures workstreams are out of scope here.

## Production
- Canonical domain: `https://ainosventures.com/`
- English: `https://ainosventures.com/en/`
- Turkish: `https://ainosventures.com/tr/`
- `www.ainosventures.com` redirects to the apex domain
- GitHub `main` is the source of truth; Vercel deploys from the repository

## Current architecture
- Static HTML / CSS / vanilla JavaScript
- Root `/` permanently redirects to `/en/`
- Shared bilingual visual system
- Canonical + `hreflang` metadata
- `robots.txt` + bilingual `sitemap.xml`
- Vercel routing, caching and security headers
- Branded 404 page with `noindex`
- Official Ainos monogram favicon / navigation mark
- Accessible mobile navigation with keyboard focus management
- Skip-to-content support and reduced-motion handling
- Founder headshots and LinkedIn links are present directly in static HTML
- Company LinkedIn and canonical website email CTA are present directly in static HTML
- Presentation/responsive enhancement rules live in CSS; `main.js` is limited to interaction/behavior

## Brand / positioning
- Tagline: `Strategy · Capital · Partnership.`
- Warm ivory / off-white background
- Charcoal typography (`#1C1C1C` production reference)
- Minimal, editorial, senior visual language
- Positioning: strategy + finance + capital + partnerships + execution
- Public founders:
  - Tunca Cingöz — Co-Founder
  - Nidan Akmanoğlu — Co-Founder
- Public Current Focus:
  - Energy & Infrastructure
  - Industrial & Technology
  - Consumer & Hospitality
  - Digital Assets & Technology
- Primary website contact: `contact@ainosventures.com`

## Release status — V1
- [x] Production shell and bilingual routes
- [x] Final core-team roster and founder bios
- [x] Founder headshots and LinkedIn links
- [x] Official monogram / favicon
- [x] Current Focus replaced retired Selected Work / public deal figures
- [x] Responsive QA at 1440 / 1024 / 768 / 390 / 360 px for EN/TR
- [x] Accessibility / keyboard-navigation pass
- [x] Canonical domain and `www` redirect
- [x] SEO canonical / hreflang / robots / sitemap checks
- [x] Security-header and caching pass
- [x] Unknown-route 404 behavior
- [x] Production smoke QA
- [x] Site-quality CI
- [x] Responsive visual QA
- [x] Google Search Console Domain property verified
- [x] `/en/` confirmed indexed by Google
- [x] `/tr/` confirmed indexed by Google

## V1.1 maintainability — completed
The static source now matches the intended public output rather than relying on runtime JavaScript injection or CSS-only hiding for core content.

Completed:
- [x] Removed unpublished Ainos Intelligence navigation and section markup from EN/TR source
- [x] Removed internal network-note/release-note copy from EN/TR source
- [x] Baked `contact@ainosventures.com` and company LinkedIn directly into EN/TR HTML
- [x] Baked founder photos, founder LinkedIn links and official monogram directly into EN/TR HTML
- [x] Moved presentation/responsive runtime styles from `main.js` into `assets/css/site-enhancements.css`
- [x] Removed V1 hide rules from `assets/css/team-tuning.css`
- [x] Reduced `main.js` to mobile navigation, accessibility interaction, reveal animation and current-year behavior
- [x] Extended `scripts/site_check.py` and `scripts/release_check.py` to protect raw-source/static wiring
- [x] Site quality PASS
- [x] Production smoke PASS
- [x] Responsive visual QA PASS after the visual/source refactor
- [x] Desktop and mobile EN/TR screenshots reviewed with no visible regression

Primary implementation commits:
- `7c284d57a0df841cf86852542fddbe70f1a047e2` — static source / CSS / JS refactor
- `1ad01f2647afe8400bec610665ce223c15f2a563` — release-check alignment for static contact wiring

## Monitoring
Search Console tracking is maintained in Issue #4.

Current state:
- Sitemap submitted to Search Console
- Sitemap is publicly reachable and contains both canonical language URLs
- Search Console initially reported `Couldn't fetch`; monitor for Google-side re-fetch / crawl status
- Both language pages are already indexed and served over HTTPS
- Analytics is intentionally **not enabled for V1**; revisit only if a concrete measurement need emerges

## Explicitly deferred
- Social sharing / OG image
- First Ainos Intelligence article or brief
- Analytics
- Privacy / cookie work tied to future analytics or form functionality
- Contact form / backend

## Working method
GitHub is the source of truth for documentation, backlog and code. Website work should be documented in issues before or alongside implementation. Changes are committed to the repository and automatically deployed to Vercel. GitHub Actions protect the release with site-quality, production-smoke and bilingual responsive-visual QA checks.

For future work, keep public website claims conservative and evidence-based; do not reintroduce retired deal figures or unpublished/placeholder content without an explicit content decision.
