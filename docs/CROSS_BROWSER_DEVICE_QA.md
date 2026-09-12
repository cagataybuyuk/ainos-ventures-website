# Cross-browser & Device QA

## Purpose

The Ainos Ventures website already has strong Chromium-based responsive, interaction, accessibility, performance and production-smoke coverage. This workstream extends that protection to Firefox and WebKit/Safari-like rendering without adding any runtime dependency to the public website.

Search Console Issue #4 remains a separate external-indexing monitor and is not coupled to this workstream.

## Browser matrix

Automated QA covers:

- Chromium
- Firefox
- WebKit

For each engine the workflow exercises the English and Turkish pages at:

- desktop: 1440 × 1000
- mobile/touch: 390 × 844

It also renders the branded 404 recovery page at mobile width.

## Contracts covered

### Core rendering
- EN/TR return a valid local page and preserve the expected `lang` value.
- No horizontal overflow is allowed beyond a 1 px rounding tolerance.
- V2 hero geometry must remain intact.
- The hero headline must retain a desktop-scale typographic hierarchy.
- Four Current Focus items and two founder profiles must remain present.
- The SVG brand mark and both founder images must decode successfully.
- Lazy founder images are verified after the Team section enters the viewport.
- The JavaScript-populated footer year must render.
- Unhandled browser-console and page errors fail the test.

### Keyboard accessibility
- The first desktop Tab stop must be the skip-to-content link.
- The skip link must become visible when focused, allowing for its intentional 160 ms focus transition.
- Section tracking must continue to mark Current Focus as the current navigation location after scrolling.

### Mobile/touch interaction
- The enhanced mobile menu starts closed.
- The toggle opens the menu with the expected `aria-expanded` state.
- Opening the menu moves focus into the navigation.
- Choosing a section closes the menu.
- Escape closes the menu and restores focus to the toggle.
- Mobile rendering must remain free of horizontal overflow.

### Reduced motion
With the OS/browser reduced-motion preference enabled:

- signature hero animation must be disabled;
- navigation transitions must be disabled;
- button transitions must be disabled.

### 404 recovery
Across all engines the 404 fixture must:

- remain `noindex`;
- retain the branded heading;
- avoid horizontal overflow;
- expose both English and Turkish recovery links.

The real HTTP 404 response code remains protected separately by Production Smoke against the deployed Vercel site.

## Validation result

Final branch validation passes all 15 browser/profile contracts:

| Browser | EN desktop | EN mobile/touch | TR desktop | TR mobile/touch | 404 mobile |
| --- | --- | --- | --- | --- | --- |
| Chromium | PASS | PASS | PASS | PASS | PASS |
| Firefox | PASS | PASS | PASS | PASS | PASS |
| WebKit | PASS | PASS | PASS | PASS | PASS |

The release gate requires the final PR head to show:

- Cross-browser Device QA — PASS
- Site Quality — PASS
- Vercel preview deployment — PASS

The cross-browser runner was first stabilized on commit `61c771e8df7c33544b76287d3a177cee6333c3fa`. Its QA artifact contains 12 browser/language/profile screenshots plus the Markdown result summary.

## Audit findings

No reproducible production browser defect was found. The public HTML/CSS/JavaScript/image runtime therefore required no browser-specific change.

Two early test iterations failed for QA-harness reasons and were corrected without changing the website:

1. Founder images use intentional native lazy loading. The first test sampled `naturalWidth` at page load before Team entered the viewport. The runner now scrolls Team into view and waits for successful decode before asserting image health.
2. The skip-to-content link intentionally animates into view over 160 ms on focus. The first test sampled its transformed bounding box on the same frame as the Tab event. The runner now waits for the settled focused state before asserting visibility.

These corrections make the regression suite test actual user-facing contracts rather than implementation timing.

## Visual review

The generated screenshots were reviewed across the three engines. The site retained its intended editorial structure, founder imagery, typography hierarchy, navigation and mobile layout. Expected engine-level font rasterization and timing differences were not treated as defects. No material layout, overflow, content-loss or brand-integrity issue was identified.

## Artifact policy

The workflow uploads:

- a Markdown summary of browser/profile results;
- desktop screenshots for EN/TR in each engine;
- mobile screenshots for EN/TR in each engine;
- failure screenshots when a contract fails.

Artifacts are diagnostic evidence, not pixel-perfect cross-engine golden images. Small font rasterization, anti-aliasing or transition-capture differences are acceptable; usability, accessibility, layout integrity and brand structure are the protected contracts.

## Change policy

A browser-specific code change should only be made when a defect is reproducible and materially affects usability, accessibility, layout integrity or brand presentation. Cosmetic engine differences that do not affect those areas should not trigger production complexity.

## Release gate

Before production merge:

1. Cross-browser Device QA must pass.
2. Site Quality must pass.
3. Vercel preview must succeed.
4. Any actual HTML/CSS/JS/image change must also pass the existing Responsive Visual QA and Performance baseline where their path filters apply.
5. Production merge still requires explicit user approval.
