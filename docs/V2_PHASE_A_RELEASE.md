# V2 Phase A — Art Direction Release

## Purpose
Document the first production-facing V2 visual upgrade and the evidence used to approve it for rollout.

## Scope
Phase A changes presentation and hierarchy while preserving the approved Ainos Ventures content, bilingual information architecture, metadata, contact wiring and lightweight static architecture.

### Visual changes
- Editorial, square hero composition with reduced product/card chrome
- Stronger serif-led hierarchy and more whitespace
- Restrained circle / line geometry as an Ainos signature motif
- Operating model and capabilities expressed through rules and typographic rows rather than repeated cards
- Current Focus converted to a dark institutional typographic sequence
- Markets & Reach converted from pill-like UI to a structured regional / engagement treatment
- Team converted to larger portrait-led editorial profiles
- Contact close given stronger architectural scale

## Implementation
- Production-facing Phase A styles are integrated into `assets/css/team-tuning.css`, which is already loaded by both `/en/` and `/tr/`.
- No production copy, canonical metadata, Organization semantics, social metadata, contact details or founder facts were changed as part of the visual rollout.
- The branded 404 page remains outside the Phase A visual override because it does not load `team-tuning.css`.
- Temporary prototype pages, prototype stylesheet and prototype-only workflow were removed before merge.

## QA evidence
### Prototype review
- EN/TR prototype reviewed at 1440 / 1024 / 768 / 390 / 360 px.
- No horizontal overflow found.
- Direction accepted for hero, Current Focus, Markets & Reach and portrait-led Team.

### Production candidate
Candidate commit: `ac78c2c63d96cc2e15578b81acf6fc1d94814f83`

- Site Quality: PASS
- Bilingual V2 production-candidate visual QA: PASS
- Vercel preview deployment: PASS
- Screenshot artifact included EN/TR Hero, What We Do / Ne Yapıyoruz, Current Focus / Güncel Odak, Markets & Reach / Pazarlar & erişim and Team / Ekip across all five breakpoints.

## Persistent regression protection
`responsive-visual-qa.yml` now retains the existing no-JavaScript and 404 checks and additionally asserts:
- no horizontal overflow on key breakpoints
- editorial zero-radius hero shell
- four Current Focus rows with zero-radius presentation
- two founder profiles
- two Markets & Reach panels with non-pill presentation
- expanded screenshots for Hero, What, Focus, Markets and Team in both languages

## Release gate
Phase A is not considered fully released until the merge commit on `main` passes:
1. Site Quality
2. Responsive Visual QA
3. Production Smoke
4. Vercel deployment

After that gate, Phase B interaction polish can begin.
