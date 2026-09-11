# Performance & Core Web Vitals Baseline

Date: 2026-09-11
Workstream: Issue #14 / PR #15
Baseline source: released V2 Phase B code on `main`, measured and hardened on `performance-cwv-baseline`.

## Scope and method

The audit uses Lighthouse 13.4.1 in GitHub Actions with Chrome 152 against a local static HTTP server. EN and TR are tested in mobile and desktop profiles. The stabilized workflow runs three samples per profile and reports the median, with raw Lighthouse JSON and a generated summary retained as an artifact.

This is a **lab performance baseline**, not field Core Web Vitals data. It is suitable for frontend execution, layout stability, accessibility and regression detection. Cache-lifetime and document-latency opportunities reported against Python's development HTTP server are not treated as production-authoritative because that server does not reproduce Vercel CDN caching/compression behavior.

## Initial single-sample signal

| Profile | Performance | Accessibility | Best Practices | SEO | FCP | LCP | TBT | CLS | Speed Index | Transfer |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| EN desktop | 100 | 95 | 100 | 100 | 0.3 s | 0.4 s | 0 ms | 0 | 0.3 s | 56.4 KiB |
| EN mobile | 82 | 95 | 100 | 100 | 1.3 s | 1.6 s | 700 ms | 0 | 1.5 s | 56.4 KiB |
| TR desktop | 100 | 95 | 100 | 100 | 0.3 s | 0.4 s | 0 ms | 0 | 0.3 s | 56.9 KiB |
| TR mobile | 100 | 95 | 100 | 100 | 1.4 s | 1.4 s | 0 ms | 0 | 1.4 s | 56.9 KiB |

The isolated EN-mobile TBT result was correctly treated as lab noise rather than a JavaScript regression. Repeated sampling later produced 0 ms median TBT on every profile.

## Confirmed findings and fixes

### 1. Small muted-text contrast

Lighthouse consistently scored accessibility at 95 because small hero/section labels were slightly below the required contrast ratio on the warm ivory backgrounds.

Applied fix:
- `--muted` hardened to `#626762`
- `--v2-quiet` hardened to `#676760`
- the V2 eyebrow now uses the shared quiet token

The visual direction remains unchanged while the affected text moves safely above the contrast threshold.

### 2. Visible label / accessible name mismatch

The language switch and visible email CTA had explicit accessible labels that did not contain the visible label text.

Applied fix:
- language-switch accessible labels now include visible `TR` / `EN`
- redundant email `aria-label` values were removed so the visible email address is the accessible name

### 3. Intermittent mobile layout shift during progressive enhancement

Repeated PR sampling surfaced an intermittent TR-mobile CLS of approximately `0.055`. Lighthouse attributed the shift to the full `main` region moving when the no-JavaScript fallback navigation collapsed into the JavaScript-enhanced mobile header after script boot.

Applied fix:
- modern scripting-enabled browsers now reserve the enhanced one-row mobile navigation layout at CSS evaluation time via the `scripting: enabled` media feature
- the existing `html.js` selectors remain as a compatibility fallback
- true no-JavaScript users continue to receive the visible fallback navigation

This removes the paint-timing race without adding a render-blocking bootstrap script or changing the mobile visual design.

## Stabilized median result after hardening

PR-run median of three samples per profile:

| Profile | Performance | Accessibility | Best Practices | SEO | FCP | LCP | TBT | CLS | Speed Index | Transfer |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| EN desktop | 100 | 100 | 100 | 100 | 0.32 s | 0.36 s | 0 ms | 0 | 0.32 s | 56.5 KiB |
| EN mobile | 100 | 100 | 100 | 100 | 1.20 s | 1.35 s | 0 ms | 0 | 1.20 s | 56.5 KiB |
| TR desktop | 100 | 100 | 100 | 100 | 0.32 s | 0.36 s | 0 ms | 0 | 0.32 s | 57.0 KiB |
| TR mobile | 100 | 100 | 100 | 100 | 1.35 s | 1.35 s | 0 ms | 0 | 1.35 s | 57.0 KiB |

The performance workflow enforces a stable lab quality floor of Accessibility / Best Practices / SEO = 100 and median CLS <= 0.01. Performance score itself is reported but not used as a hard pass/fail gate because synthetic timing is inherently variable.

## Delivery / asset observations

- Normal first-load transfer in the local audit is approximately 57 KiB.
- Founder JPGs are approximately 31 KiB each and already use explicit dimensions, lazy loading and async decoding.
- Shared CSS source is approximately 33 KiB before transfer compression.
- Main JavaScript source is approximately 5.3 KiB.
- The social-sharing PNG is not part of normal page rendering and is approximately 7.5 KiB.
- No framework/runtime bundle exists.
- `vercel.json` intentionally uses revalidation for CSS/JS because asset filenames are stable rather than content-hashed; long immutable caching would risk stale releases.

## Conclusion

No broad CSS/JS refactor, framework change, image-conversion project or speculative dead-code cleanup is justified by the measurements. The useful work was targeted: accessibility hardening plus elimination of an intermittent progressive-enhancement CLS race.

The permanent Lighthouse workflow provides a repeatable regression baseline for future visual/content changes. Any later performance work should be driven by measured production/field evidence rather than cleanup for its own sake.