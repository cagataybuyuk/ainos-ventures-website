# V1.5 — Social Sharing / OG Package

## Objective
Provide a consistent Ainos Ventures corporate preview when the website is shared externally, without altering the approved on-page design.

## Social card
- Canonical asset: `https://ainosventures.com/assets/images/ainos-social-card.png`
- Format: PNG
- Dimensions: 1200 × 630
- Shared by EN/TR because the artwork is intentionally language-neutral and uses the public brand spine `Strategy. Capital. Partnership.`
- Visual system follows the production website: warm ivory, charcoal, official monogram, editorial serif headline and restrained circular geometry.

## Metadata
Both `/en/` and `/tr/` declare `og:image`, explicit PNG type/dimensions/alt metadata, `twitter:card=summary_large_image`, `twitter:image` and `twitter:image:alt`. Canonical URLs, hreflang and Open Graph locale metadata remain unchanged.

## Guardrails
`site_check.py` validates the metadata, PNG signature and exact dimensions. `release_check.py` requires the production social metadata wiring. Production smoke separately verifies the deployed image and page references.

## Explicit non-goals
No analytics, contact form/backend, Ainos Intelligence content, mail/DNS changes or on-page redesign were introduced in V1.5.
