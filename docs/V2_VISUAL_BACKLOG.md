# V2 — Visual & Experience Backlog

Source audit: `docs/V2_VISUAL_EXPERIENCE_AUDIT.md`

## Phase A — Art direction foundation
- [x] Redesign the hero composition without changing approved positioning/copy
- [x] Reduce product-like shell/card chrome
- [x] Define V2 spacing / rhythm / grid tokens
- [x] Define a restrained Ainos signature motif using the monogram / circles / lines
- [x] Reduce repetitive rounded-card and pill patterns across the homepage
- [x] Redesign Current Focus as a stronger editorial module
- [x] Redesign Team as a more senior, portrait-led section
- [x] Redesign Markets & Reach as an institutional geography treatment
- [x] Produce EN/TR desktop and mobile visual references for review
- [x] Release and validate Phase A on production

## Phase B — Interaction polish
- [x] Add compact navigation state on scroll
- [x] Add active-section indication
- [x] Refine navigation / CTA / content hover and focus transitions
- [x] Introduce restrained stagger / line / geometry motion
- [x] Preserve no-JS usability
- [x] Preserve `prefers-reduced-motion`
- [x] Add interaction/accessibility regression checks
- [x] Validate EN/TR desktop, tablet and mobile behavior before production merge
- [x] Release and validate Phase B on production

## Phase C — Editorial extensibility
- [ ] Define a reusable Ainos Intelligence article template
- [ ] Define an Intelligence index/archive pattern for future content
- [ ] Keep Intelligence unpublished until the first real piece is approved
- [ ] Define optional credibility modules for future verified material only

Phase C is intentionally queued rather than active. It should start only when there is real approved editorial material or another concrete credibility-content need.

## Guardrails
- [x] No unsupported metrics, offices, clients, logos or deal claims
- [x] No stock consulting imagery
- [x] No SaaS / generic AI visual language
- [x] No unnecessary framework/runtime dependency
- [x] Maintain EN/TR parity
- [x] Maintain accessibility / CSP / SEO / production smoke checks
- [x] Responsive visual QA at desktop, tablet and mobile breakpoints

## Phase A release evidence
- PR #12 merged to `main`
- Production merge commit: `3a395a9e9a51cd43a94c5bb268839311b8df01ff`
- Site Quality: PASS
- Responsive Visual QA: PASS
- Production Smoke: PASS
- Vercel production deployment: PASS

## Phase B release evidence
- PR #13 merged to `main`
- Production merge commit: `8a2e4491fc92e0233836c2024c3a7a30b1c08364`
- Site Quality run 139: PASS
- Responsive Visual QA run 25: PASS
- Interaction/accessibility contracts: PASS
- Production Smoke run 62: PASS
- Vercel production deployment: PASS
- EN/TR post-merge responsive artifact generated and visually reviewed
