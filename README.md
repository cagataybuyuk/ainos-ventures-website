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
- Bilingual Open Graph locale metadata
- `robots.txt` + bilingual `sitemap.xml`
- Vercel routing, caching and security headers
- Strict self-hosted Content Security Policy; production HTML does not require inline styles
- Branded responsive 404 page with `noindex`
- Official Ainos monogram favicon / navigation mark
- Accessible mobile navigation with keyboard focus management
- Skip-to-content support and reduced-motion handling
- Progressive enhancement: public content/navigation remain usable without JavaScript
- Schema.org `Organization` microdata using current public company facts
- Founder headshots and LinkedIn links
- Company LinkedIn and canonical website email CTA
- Production smoke asserts deployed CSP and branded 404 behavior, not only repository configuration

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

## Release status
### V1 — production launch
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

### V1.1 — source cleanup / maintainability
- [x] Removed unpublished Insights/internal release-note markup from raw source
- [x] Baked brand/contact/team wiring directly into static HTML
- [x] Moved presentation CSS out of runtime JavaScript
- [x] Added raw-source CI guardrails

### V1.2 — post-launch resilience / search semantics
- [x] Added no-JavaScript resilience for reveal content and mobile navigation
- [x] Added explicit browser QA with JavaScript disabled at mobile width
- [x] Added schema.org `Organization` microdata using public facts only
- [x] Added EN/TR Open Graph locale metadata
- [x] Extended site/release CI guardrails
- [x] Site quality / production smoke / responsive visual QA PASS

Detailed V1.2 audit: `docs/V1_2_POST_LAUNCH_AUDIT.md`

### V1.3 — CSP hardening / 404 resilience
- [x] Removed inline styles from the branded 404 page
- [x] Moved 404 layout into shared responsive CSS
- [x] Tightened CSP to `style-src 'self'` with no `unsafe-inline`
- [x] Added CI guardrails against inline production styles / CSP regression
- [x] Added 404 desktop/mobile responsive visual QA
- [x] Site quality / production smoke / responsive visual QA PASS
- [x] Vercel deployment success

Detailed V1.3 audit: `docs/V1_3_CSP_404_AUDIT.md`

### V1.4 — production contract assertions
- [x] Assert the live CSP contains `style-src 'self'`
- [x] Assert the live CSP does not contain `unsafe-inline`
- [x] Assert a real missing route returns the branded Ainos 404 body
- [x] Assert the served 404 remains `noindex`, uses shared CSS and contains no inline styles
- [x] Preserve root/www redirects, EN/TR, sitemap/assets and staging checks
- [x] Site quality / production smoke PASS
- [x] Vercel deployment success

Detailed V1.4 notes: `docs/V1_4_PRODUCTION_CONTRACTS.md`

### V1.5 — social sharing / OG package
- [x] Added one shared 1200×630 Ainos Ventures social card
- [x] Added canonical `og:image` metadata to EN/TR
- [x] Added explicit Open Graph image type/dimensions/alt metadata
- [x] Upgraded Twitter card metadata to `summary_large_image`
- [x] Added CI and production-smoke contracts for the image and metadata

Detailed V1.5 notes: `docs/V1_5_SOCIAL_SHARING.md`

## Monitoring
Search Console tracking is maintained in Issue #4.

Current state:
- Sitemap submitted to Search Console
- Sitemap is publicly reachable and contains both canonical language URLs
- Search Console initially reported `Couldn't fetch`; monitor for Google-side re-fetch / crawl status
- Both language pages are already indexed and served over HTTPS
- Analytics is intentionally **not enabled**; revisit only if a concrete measurement need emerges

## Explicitly deferred
- First Ainos Intelligence article or brief
- Analytics
- Privacy / cookie work tied to future analytics or form functionality
- Contact form / backend

## Working method
GitHub is the source of truth for documentation, backlog and code. Website work should be documented in issues before or alongside implementation. Changes are committed to the repository and automatically deployed to Vercel. GitHub Actions protect the release with site-quality, production-smoke and bilingual responsive-visual QA checks.

For future work, keep public website claims conservative and evidence-based; do not reintroduce retired deal figures or unpublished/placeholder content without an explicit content decision.
