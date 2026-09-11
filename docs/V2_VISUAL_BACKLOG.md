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

## Phase B — Interaction polish
- [ ] Add compact navigation state on scroll
- [ ] Add active-section indication
- [ ] Refine navigation / CTA / card hover and focus transitions
- [ ] Introduce restrained stagger / line / geometry motion
- [ ] Preserve no-JS usability
- [ ] Preserve `prefers-reduced-motion`

## Phase C — Editorial extensibility
- [ ] Define a reusable Ainos Intelligence article template
- [ ] Define an Intelligence index/archive pattern for future content
- [ ] Keep Intelligence unpublished until the first real piece is approved
- [ ] Define optional credibility modules for future verified material only

## Guardrails
- [x] No unsupported metrics, offices, clients, logos or deal claims
- [x] No stock consulting imagery
- [x] No SaaS / generic AI visual language
- [x] No unnecessary framework/runtime dependency
- [x] Maintain EN/TR parity
- [x] Maintain accessibility / CSP / SEO / production smoke checks in the Phase A candidate
- [x] Responsive visual QA at desktop, tablet and mobile breakpoints

## Phase A evidence
- Review branch: `v2-phase-a-prototype`
- Draft review PR: #12
- Production-candidate visual QA covers EN/TR at 1440 / 1024 / 768 / 390 / 360 px
- Site Quality: PASS
- V2 bilingual visual contracts: PASS
- Vercel preview deployment: PASS

Phase A should be considered complete only after the merged `main` commit passes the persistent Site Quality, Responsive Visual QA, Production Smoke and Vercel checks.
