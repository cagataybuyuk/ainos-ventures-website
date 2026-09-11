# Technical SEO & Crawl/Indexing Audit

Date: 2026-09-11

Issue: #16

## Objective

Audit the released bilingual Ainos Ventures website for technical SEO, crawlability, indexability and metadata consistency while Search Console Issue #4 continues independently as an external Google-side monitoring item.

This audit deliberately avoids speculative SEO content changes. The site is small, static and already indexed in EN/TR, so the focus is keeping canonical signals simple, consistent and machine-verifiable.

## Current production model

- Canonical host: `https://ainosventures.com`
- Canonical pages: `/en/` and `/tr/`
- Root `/` permanently redirects to `/en/`
- `www` redirects to the apex domain
- EN/TR use self-referencing canonicals
- EN/TR each publish reciprocal `hreflang` annotations for `en`, `tr` and `x-default`
- `x-default` resolves to the English canonical page
- Root-level `robots.txt` exposes the production sitemap
- Root-level XML sitemap lists the two indexable language pages
- Unknown routes return a real HTTP 404 and the branded 404 document is `noindex`
- The legacy Vercel host is protected from indexing
- Organization microdata uses public company facts only

## External standards reviewed

The audit was cross-checked against current Google Search Central guidance:

- Canonicalization: redirects and `rel="canonical"` are strong signals; sitemap inclusion is a weaker supporting signal. Self-referencing canonicals are recommended.
  - https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls
- Permanent HTTP redirects are the preferred redirect mechanism when a URL should resolve permanently to a canonical destination.
  - https://developers.google.com/search/docs/crawling-indexing/301-redirects
- Localized pages should use reciprocal annotations and each localized version should include itself in the alternate set. `x-default` is recommended as a fallback for unmatched languages.
  - https://developers.google.com/search/docs/specialty/international/localized-versions
- XML sitemaps may carry localized-version annotations; sitemap URLs should be fully-qualified canonical URLs.
  - https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap
- `lastmod` is useful only when it truthfully reflects significant page changes. It should not be added as decorative freshness metadata.
  - https://developers.google.com/search/blog/2023/06/sitemaps-lastmod-ping

## Findings

### 1. Canonical routing is already strong — PASS

The root route is handled by a permanent server-side redirect to `/en/`. EN/TR each have self-referencing canonical tags and matching `og:url` values. The production `www` host redirects to the apex domain. These signals point in the same direction rather than competing.

Decision: no routing redesign.

### 2. HTML hreflang is correct and reciprocal — PASS

Both language pages expose the same alternate set:

- `en` → `https://ainosventures.com/en/`
- `tr` → `https://ainosventures.com/tr/`
- `x-default` → `https://ainosventures.com/en/`

This is the intended bilingual fallback model.

Decision: preserve this contract exactly until a new real language version is introduced.

### 3. Sitemap alternates were valid but not fully aligned with the HTML contract — IMPROVED

The sitemap contained reciprocal EN/TR alternates but omitted the already-approved `x-default` fallback used by the page heads.

This was not an indexing blocker, but keeping the sitemap and HTML alternate sets identical removes an avoidable source of drift and makes the default-language policy explicit in both representations.

Change: add `x-default` to both sitemap entries and normalize alternate ordering.

### 4. Static CI validated presence, not the full SEO graph — IMPROVED

Before this audit, `site_check.py` confirmed that canonical URLs and sitemap URLs existed, but the sitemap itself was only checked with string presence. That would not catch several regressions, such as:

- duplicate sitemap URLs
- a rogue `www` or staging URL
- a missing reciprocal alternate
- an incomplete `x-default` set
- a malformed sitemap URL entry
- accidental full-site `Disallow: /`

Change: add `scripts/seo_check.py` and run it inside Site Quality CI. The new contract parses the sitemap XML and verifies the canonical/hreflang/robots/root-routing relationships as a single system.

### 5. Production smoke checked pages but not exact canonical/hreflang semantics — IMPROVED

The production smoke previously confirmed that canonical URLs appeared somewhere in the rendered source. It did not assert the exact `rel="canonical"`, full EN/TR/x-default alternate set, matching `og:url`, or exact sitemap alternate graph.

Change: production smoke now verifies those contracts on the deployed site and parses the deployed sitemap XML instead of relying only on URL greps.

### 6. Robots discovery policy is intentionally simple — PASS

`robots.txt` allows the site and points to the canonical sitemap. No crawler-specific optimization or blocking rule is justified for the current public site.

Decision: retain the simple allow-all production policy and guard against accidental `Disallow: /`.

### 7. 404 indexing behavior is correct — PASS / HARDENED

The branded error page is `noindex`, and production smoke verifies that missing routes return HTTP 404.

Change: the SEO contracts also ensure that the 404 document does not acquire a canonical URL, avoiding a future signal that could incorrectly canonicalize missing pages to a real page.

### 8. `lastmod` is intentionally not added — NO CHANGE

Google can use accurate `lastmod` values for crawl scheduling, but inaccurate or automatically refreshed dates are counterproductive. This repository does not yet have a durable mechanism that distinguishes significant content updates from operational commits.

Decision: omit `lastmod` until it can be maintained truthfully. If content publishing becomes more frequent, generate it from an explicit content-release date rather than every deploy timestamp.

### 9. Explicit `index,follow` metadata is unnecessary — NO CHANGE

The EN/TR pages are indexable by default and already protected by CI from accidental `noindex`.

Decision: do not add redundant `meta robots="index,follow"` markup.

### 10. No SEO-driven copy expansion — NO CHANGE

The site already has clear public positioning and structured bilingual content. There is no evidence that adding keyword-heavy blocks, hidden text, unsupported claims or placeholder editorial content would improve the site.

Decision: preserve concise public copy. Future content expansion belongs to real approved Ainos Intelligence or credibility material, not this technical workstream.

## Changes in this workstream

1. `sitemap.xml`
   - add `x-default` to both canonical language entries
   - keep the EN/TR alternate set identical for each entry

2. `scripts/seo_check.py`
   - verify canonical and `og:url` alignment
   - verify exact reciprocal EN/TR/x-default hreflang set
   - parse sitemap XML and enforce exact canonical coverage
   - reject duplicate/rogue/non-canonical sitemap URLs
   - verify robots discovery directives and reject full-site blocking
   - verify permanent root routing and trailing-slash policy
   - verify root fallback canonical/refresh policy
   - verify language pages remain indexable
   - verify the 404 remains noindex and has no canonical

3. `.github/workflows/site-quality.yml`
   - add the dedicated technical SEO contract check

4. `.github/workflows/production-smoke.yml`
   - assert exact live canonical/hreflang/og:url tags
   - reject non-canonical hosts in production page source
   - parse the live sitemap XML and verify exact alternate relationships
   - verify the live robots discovery contract
   - reject a canonical URL on the served 404 document

## Non-goals

- No Search Console API/settings changes
- No manual indexing requests
- No analytics
- No keyword-stuffing or new unsupported claims
- No JSON-LD migration solely for format preference
- No `lastmod` until a truthful maintenance model exists
- No MX/SPF/DKIM/DMARC changes
- No redesign or content architecture change

## Release gate

Before production merge:

- Site Quality must pass, including `scripts/seo_check.py`
- Responsive Visual QA should remain green even though this work does not alter layout
- Performance baseline should remain green
- Vercel preview should deploy successfully

After merge:

- Production Smoke must pass against the live canonical domain
- Vercel production deployment must succeed
- Search Console Issue #4 remains open independently until Google-side sitemap/crawl status is resolved

## Expected outcome

The website does not need a broad SEO rebuild. The useful improvement is stronger consistency and regression protection around the small set of canonical URLs that matter. The resulting configuration remains intentionally simple: two canonical language pages, one fallback language policy, one sitemap, one robots file and explicit production checks that all of those signals agree.
