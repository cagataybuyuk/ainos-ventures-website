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

Machine-readable JSON results are uploaded as the `accessibility-semantic-qa` artifact for 14 days. Reveal elements are audited in their intended resting state so transition opacity cannot create false contrast failures.

## Relationship to existing QA

This workflow does not replace other release gates:

- Lighthouse continues to protect broad accessibility/performance/SEO scoring.
- Cross-browser Device QA continues to protect keyboard, mobile-menu, focus-restoration, reduced-motion and engine-specific behavior.
- Responsive Visual QA continues to protect layout across viewport sizes.
- Production Smoke continues to protect live HTTP/SEO/security/404 contracts.

The semantic audit is intentionally narrower and stricter: it catches DOM/ARIA/WCAG regressions that can remain invisible in screenshots and interaction smoke tests.

## Audit finding and fix

The first deterministic audit found one real WCAG AA contrast problem shared by EN and TR:

- operational-model step numbers (`01`–`04`) used `--stone: #928a7d` on the warm ivory background, producing about 2.97:1 contrast at 10px;
- founder profile numbers used the same stone tone on the team background, producing about 2.76:1 contrast at 10px.

The shared `--stone` token is now overridden to `#6a635b` in `site-enhancements.css`. This preserves the warm stone visual direction while raising contrast to approximately 5.15:1 on the main ivory background and 4.80:1 on the team background, above the 4.5:1 WCAG AA threshold for normal text. The change also improves other small text that intentionally uses the same token without changing copy, layout or production dependencies.

After the fix, the accessibility artifact reports zero semantic errors and zero axe WCAG A/AA violations for EN, TR and the branded 404 document.

## Validation evidence

Validated code head: `936eaa7913ddfbe92c706b4b66831c487eaf0d79`.

- Accessibility Semantic QA run 4 — PASS
- Site Quality run 170 — PASS
- Responsive Visual QA run 36 — PASS
- Cross-browser Device QA run 11 — PASS
- Performance Baseline run 18 — PASS
- Vercel preview deployment — PASS

Accessibility artifact `accessibility-semantic-qa` confirms:

- EN: 0 semantic errors / 0 WCAG violations
- TR: 0 semantic errors / 0 WCAG violations
- 404: 0 semantic errors / 0 WCAG violations

## Change policy

If future audits discover violations, fixes must be evidence-backed and should not change approved Ainos positioning or visual direction unless the accessibility requirement genuinely requires it. Production runtime dependencies must remain unchanged; axe/playwright are CI-only dependencies installed during the workflow.

## Release policy

The branch must pass Accessibility Semantic QA plus all other workflows triggered by any evidence-backed production change. Production merge requires explicit user approval.
