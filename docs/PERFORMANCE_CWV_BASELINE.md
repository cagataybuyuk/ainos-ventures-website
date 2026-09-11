# Performance & Core Web Vitals Baseline

Date: 2026-09-11
Workstream: Issue #14 / PR #15
Baseline source: released V2 Phase B code on `main`, measured from the `performance-cwv-baseline` branch before optimization changes.

## Method

The first pass uses Lighthouse 13.4.1 in GitHub Actions with Chrome 152 against a local static HTTP server. EN and TR are audited in mobile and desktop profiles. Raw Lighthouse JSON and a generated summary are stored as a workflow artifact.

This local-server pass is appropriate for frontend execution, layout stability, accessibility and relative regression testing. Cache-lifetime and document-latency opportunities from this run are **not production-authoritative**, because Python's development HTTP server does not reproduce Vercel CDN caching/compression behavior.

## Initial scores

| Profile | Performance | Accessibility | Best Practices | SEO | FCP | LCP | TBT | CLS | Speed Index | Transfer |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| EN desktop | 100 | 95 | 100 | 100 | 0.3 s | 0.4 s | 0 ms | 0 | 0.3 s | 56.4 KiB |
| EN mobile | 82 | 95 | 100 | 100 | 1.3 s | 1.6 s | 700 ms | 0 | 1.5 s | 56.4 KiB |
| TR desktop | 100 | 95 | 100 | 100 | 0.3 s | 0.4 s | 0 ms | 0 | 0.3 s | 56.9 KiB |
| TR mobile | 100 | 95 | 100 | 100 | 1.4 s | 1.4 s | 0 ms | 0 | 1.4 s | 56.9 KiB |

## Interpretation

The website is already very light: first-load transfer in the local audit is roughly 57 KiB, CLS is zero, desktop performance is 100, and Best Practices / SEO are 100 in all four profiles.

The isolated EN-mobile TBT result is not treated as a confirmed regression. The same shared JavaScript produced 0 ms TBT in TR mobile and both desktop runs. The EN trace contains a one-off ~966 ms page task plus unusually inflated main-thread time, so the next measurement step is repeated sampling and median comparison rather than speculative JavaScript refactoring.

## Confirmed accessibility findings

The 95 accessibility score is reproducible across EN/TR and desktop/mobile. Lighthouse identified two concrete classes of issue:

1. **Small muted text contrast** — hero topline, eyebrow and section-kicker text are slightly below the 4.5:1 requirement on warm ivory / soft-ivory backgrounds. Current measured ratios are approximately 3.97–4.27:1 depending on the token/background.
2. **Visible-label / accessible-name mismatch** — the language switch and email CTA use `aria-label` values that do not include their visible label text. The email address itself is already a clear accessible name; language switches should include `TR` / `EN` in any explicit accessible label.

These are high-confidence, low-risk fixes and do not require a visual redesign.

## Delivery / asset observations

- Founder JPGs are approximately 31 KiB each and already use explicit dimensions, lazy loading and async decoding.
- Shared CSS source is approximately 33 KiB total before transfer compression.
- Main JavaScript source is approximately 5.3 KiB.
- The social-sharing PNG is not part of normal page rendering and is approximately 7.5 KiB.
- No framework/runtime bundle exists.

## Next actions

1. Re-run Lighthouse with repeated mobile/desktop sampling and use median values to remove one-run noise.
2. Apply the two confirmed accessibility fixes on the branch.
3. Re-measure accessibility and performance.
4. Inspect production delivery separately before acting on cache/document-latency suggestions.
5. Merge only if the measured result improves or preserves the released V2 experience.

No CSS/JS dead-code cleanup is justified by the current performance evidence alone.