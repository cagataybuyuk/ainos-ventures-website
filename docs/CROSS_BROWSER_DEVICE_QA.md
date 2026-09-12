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
- The JavaScript-populated footer year must render.
- Unhandled browser-console and page errors fail the test.

### Keyboard accessibility
- The first desktop Tab stop must be the skip-to-content link.
- The skip link must become visible when focused.
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

## Artifact policy

The workflow uploads:

- a Markdown summary of browser/profile results;
- desktop screenshots for EN/TR in each engine;
- mobile screenshots for EN/TR in each engine;
- failure screenshots when a contract fails.

Artifacts are diagnostic evidence, not pixel-perfect cross-engine golden images. Small font rasterization or anti-aliasing differences are acceptable; usability, layout integrity and brand structure are the protected contracts.

## Change policy

A browser-specific code change should only be made when a defect is reproducible and materially affects usability, accessibility, layout integrity or brand presentation. Cosmetic engine differences that do not affect those areas should not trigger production complexity.

## Release gate

Before production merge:

1. Cross-browser Device QA must pass.
2. Site Quality must pass.
3. Vercel preview must succeed.
4. Any actual HTML/CSS/JS/image change must also pass the existing Responsive Visual QA and Performance baseline where their path filters apply.
5. Production merge still requires explicit user approval.
