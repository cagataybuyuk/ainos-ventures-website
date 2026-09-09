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
- Founder headshots and LinkedIn links
- Company LinkedIn and canonical website email CTA

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

## Monitoring
Search Console tracking is maintained in Issue #4.

Current state:
- Sitemap submitted to Search Console
- Sitemap is publicly reachable and contains both canonical language URLs
- Search Console initially reported `Couldn't fetch`; monitor for Google-side re-fetch / crawl status
- Both language pages are already indexed and served over HTTPS
- Analytics is intentionally **not enabled for V1**; revisit only if a concrete measurement need emerges

## Next engineering pass — V1.1
The public browser experience is correct, but some V1 presentation/content changes are currently applied through runtime JavaScript or CSS hiding. The next maintainability pass should make the static source itself match the intended public output.

Planned direction:
- Remove deferred Ainos Intelligence markup/navigation from EN/TR source until content is actually published
- Remove internal network-note copy from EN/TR source rather than hiding it with CSS
- Bake `contact@ainosventures.com` and company LinkedIn directly into HTML
- Bake founder photos / profile links and official monogram into static HTML where practical
- Move presentation-only runtime CSS out of `main.js` into stylesheet source
- Keep JavaScript focused on interaction/behavior (mobile navigation, reveal, current year)
- Extend CI to assert that retired/deferred raw-source content cannot reappear
- Re-run production smoke, site quality and responsive visual QA after cleanup

Track this work in the V1.1 GitHub issue/backlog.

## Explicitly deferred
- Social sharing / OG image
- First Ainos Intelligence article or brief
- Analytics
- Privacy / cookie work tied to future analytics or form functionality
- Contact form / backend

## Working method
GitHub is the source of truth for documentation, backlog and code. Website work should be documented in issues before or alongside implementation. Changes are committed to the repository and automatically deployed to Vercel. GitHub Actions protect the release with site-quality, production-smoke and bilingual responsive-visual QA checks.

For future work, keep public website claims conservative and evidence-based; do not reintroduce retired deal figures or unpublished/placeholder content without an explicit content decision.
