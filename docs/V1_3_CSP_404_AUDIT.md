# V1.3 CSP & 404 hardening audit

Date: 2026-09-09

## Scope
Website security and error-page resilience only. No redesign, analytics, form/backend, Ainos Intelligence, Qatar/GCC or mail/DNS work is included.

## Baseline finding
The public EN/TR pages were already static, self-hosted and protected by CSP, but `404.html` still contained inline `style` attributes. Because of that, production CSP still allowed `style-src 'unsafe-inline'`.

The same inline 404 rules also overrode the responsive `.hero-grid` media rule, making the error page less consistent with the rest of the site on small screens.

## Implementation
- Removed all inline styles from `404.html`.
- Moved 404 layout/typography into `assets/css/site-enhancements.css`.
- Added shared enhancement CSS to the 404 page.
- Added explicit EN/TR `hreflang` and `lang` metadata to 404 home links.
- Kept the 404 page `noindex`.
- Tightened production CSP from `style-src 'self' 'unsafe-inline'` to `style-src 'self'`.
- Extended site/release CI to reject inline production styles and any future `unsafe-inline` CSP regression.
- Extended responsive visual QA to capture the 404 page at 1440px and 360px.

## Validation
Implementation head: `c6c8ac53b85227515468ca15b6e238b5c573aa16`

- Site quality: PASS
- Production smoke: PASS
- Responsive visual QA: PASS
- Vercel deployment: SUCCESS
- 404 desktop screenshot reviewed: PASS
- 404 mobile screenshot reviewed: PASS

## Result
The site now has a stricter self-hosted style CSP with no inline-style exception, and the branded 404 page follows the same responsive system as the rest of the site.

## Deferred / unchanged
- Analytics remains disabled.
- No contact form/backend.
- No OG/social image yet.
- No Ainos Intelligence article yet.
- No mail/DNS changes.
- Search Console sitemap re-fetch remains tracked separately in Issue #4.
