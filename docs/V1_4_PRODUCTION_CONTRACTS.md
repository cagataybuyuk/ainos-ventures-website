# V1.4 Production contract assertions

Date: 2026-09-09

## Scope
Production verification only. No visual redesign, analytics, content expansion, backend, Ainos Intelligence, Qatar/GCC or mail/DNS work is included.

## Why this pass exists
V1.3 hardened the repository and deployment configuration, but production smoke still checked only for the presence of a CSP header and a generic HTTP 404. V1.4 makes the deployed website prove the stricter behavior directly.

## Implemented production contracts
The production smoke workflow now verifies that:

- The live Content Security Policy contains `style-src 'self'`.
- The live Content Security Policy does not contain `unsafe-inline`.
- A real missing production URL returns HTTP 404.
- The served missing-route body is the branded Ainos Ventures 404 page.
- The live 404 body retains `noindex`.
- The live 404 loads `/assets/css/site-enhancements.css`.
- The live 404 does not contain inline style attributes.
- The existing root/www redirects, EN/TR content checks, robots/sitemap checks, public-asset checks and staging non-indexability checks remain active.

## Implementation
Primary commit: `e66b139b3130117765d42ded938808724c46aacf`

## Validation
- Production smoke: PASS
- Site quality: PASS
- Vercel deployment: SUCCESS

## Result
The release pipeline now checks the actual production contract for the strict CSP and branded 404 behavior. Future repository/configuration drift that does not reach production, or production behavior that diverges from the intended configuration, is more likely to be caught automatically.

## Remaining monitoring
Search Console sitemap re-fetch/crawl status remains tracked separately in Issue #4. Analytics remains intentionally disabled until a concrete measurement need emerges.
