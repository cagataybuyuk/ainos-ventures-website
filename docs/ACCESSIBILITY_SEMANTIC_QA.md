# Accessibility & Semantic QA

## Objective

Add a dedicated WCAG-oriented regression layer that complements Lighthouse, responsive visual QA and cross-browser interaction checks.

## Coverage

The workflow validates the English homepage, Turkish homepage and branded 404 document with Chromium plus axe-core. It enforces WCAG 2.0/2.1 A and AA rules and adds explicit semantic contracts for:

- document language and non-empty title
- exactly one `main` landmark
- exactly one `h1`
- expected primary heading content
- labelled navigation landmarks where present
- `noindex` on the branded 404 document

Machine-readable JSON results are uploaded as the `accessibility-semantic-qa` artifact for 14 days.

## Relationship to existing QA

This workflow does not replace other release gates:

- Lighthouse continues to protect broad accessibility/performance/SEO scoring.
- Cross-browser Device QA continues to protect keyboard, mobile-menu, focus-restoration, reduced-motion and engine-specific behavior.
- Responsive Visual QA continues to protect layout across viewport sizes.
- Production Smoke continues to protect live HTTP/SEO/security/404 contracts.

The semantic audit is intentionally narrower and stricter: it catches DOM/ARIA/WCAG regressions that can remain invisible in screenshots and interaction smoke tests.

## Change policy

If the audit discovers violations, fixes must be evidence-backed and should not change approved Ainos positioning or visual direction unless the accessibility requirement genuinely requires it. Production runtime dependencies must remain unchanged; axe/playwright are CI-only dependencies installed during the workflow.

## Release policy

The branch must pass Accessibility Semantic QA plus all other workflows triggered by any evidence-backed production change. Production merge requires explicit user approval.
