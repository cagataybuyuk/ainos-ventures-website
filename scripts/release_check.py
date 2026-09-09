import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ERRORS = []

vercel_path = ROOT / "vercel.json"
if not vercel_path.exists():
    ERRORS.append("Missing vercel.json")
else:
    config = json.loads(vercel_path.read_text(encoding="utf-8"))

    redirects = config.get("redirects", [])
    root_redirect = next((r for r in redirects if r.get("source") == "/"), None)
    if not root_redirect:
        ERRORS.append("Missing root redirect")
    else:
        if root_redirect.get("destination") != "/en/":
            ERRORS.append("Root redirect must point to /en/")
        if root_redirect.get("permanent") is not True:
            ERRORS.append("Root redirect must be permanent")

    headers = config.get("headers", [])
    global_headers = next((h for h in headers if h.get("source") == "/(.*)" and not h.get("has")), None)
    global_map = {x.get("key"): x.get("value") for x in (global_headers or {}).get("headers", [])}
    for required in (
        "X-Content-Type-Options",
        "Referrer-Policy",
        "Permissions-Policy",
        "Strict-Transport-Security",
        "Content-Security-Policy",
    ):
        if not global_map.get(required):
            ERRORS.append(f"Missing production security header: {required}")

    csp = global_map.get("Content-Security-Policy") or ""
    if "style-src 'self'" not in csp:
        ERRORS.append("Production CSP must restrict styles to self-hosted sources")
    if "'unsafe-inline'" in csp:
        ERRORS.append("Production CSP must not allow unsafe-inline")

    staging_rule = next((
        h for h in headers
        if any(rule.get("type") == "host" and rule.get("value") == "ainos-ventures-website.vercel.app" for rule in h.get("has", []))
    ), None)
    staging_map = {x.get("key"): x.get("value") for x in (staging_rule or {}).get("headers", [])}
    if "noindex" not in (staging_map.get("X-Robots-Tag") or "").lower():
        ERRORS.append("Staging host must send X-Robots-Tag noindex")

    cache_rules = [h for h in headers if h.get("source", "").startswith("/assets/")]
    if not cache_rules:
        ERRORS.append("Static assets must have explicit cache policies")
    else:
        for rule in cache_rules:
            cache_map = {x.get("key"): x.get("value") for x in rule.get("headers", [])}
            if "max-age" not in (cache_map.get("Cache-Control") or ""):
                ERRORS.append(f"Static asset rule {rule.get('source')} must have an explicit cache policy")

for lang in ("en", "tr"):
    page = ROOT / lang / "index.html"
    if not page.exists():
        ERRORS.append(f"Missing /{lang}/ page")
        continue
    text = page.read_text(encoding="utf-8")
    canonical = f'https://ainosventures.com/{lang}/'
    if canonical not in text:
        ERRORS.append(f"/{lang}/ does not reference canonical production URL")
    if "www.ainosventures.com" in text:
        ERRORS.append(f"/{lang}/ must not use www in canonical page metadata")
    for stylesheet in ("/assets/css/site-enhancements.css", "/assets/css/team-tuning.css"):
        if stylesheet not in text:
            ERRORS.append(f"/{lang}/ must load required stylesheet {stylesheet}")
    for required in (
        "mailto:contact@ainosventures.com",
        "https://www.linkedin.com/company/ainos-ventures/",
        'itemtype="https://schema.org/Organization"',
        'itemid="https://ainosventures.com/#organization"',
        'itemprop="logo"',
        'itemprop="legalName"',
        'itemprop="email"',
        'itemprop="sameAs"',
    ):
        if required not in text:
            ERRORS.append(f"/{lang}/ missing static production/Organization wiring: {required}")

    expected_locale = 'en_US' if lang == 'en' else 'tr_TR'
    expected_alternate = 'tr_TR' if lang == 'en' else 'en_US'
    if f'<meta property="og:locale" content="{expected_locale}">' not in text:
        ERRORS.append(f"/{lang}/ missing expected og:locale {expected_locale}")
    if f'<meta property="og:locale:alternate" content="{expected_alternate}">' not in text:
        ERRORS.append(f"/{lang}/ missing expected alternate locale {expected_alternate}")

root_html = (ROOT / "index.html").read_text(encoding="utf-8") if (ROOT / "index.html").exists() else ""
if "/en/" not in root_html:
    ERRORS.append("Root fallback page does not point to /en/")

not_found = (ROOT / "404.html").read_text(encoding="utf-8") if (ROOT / "404.html").exists() else ""
if "noindex" not in not_found.lower():
    ERRORS.append("404 page must remain noindex")
for required in (
    "/assets/css/site-enhancements.css",
    'class="hero-grid not-found-grid"',
    'class="serif not-found-title"',
    'hreflang="en"',
    'hreflang="tr"',
):
    if required not in not_found:
        ERRORS.append(f"404 page missing responsive/language release wiring: {required}")
if " style=" in not_found.lower() or "<style" in not_found.lower():
    ERRORS.append("404 page must not use inline styles under the strict CSP")

main_js = (ROOT / "assets/js/main.js").read_text(encoding="utf-8") if (ROOT / "assets/js/main.js").exists() else ""
if "document.documentElement.classList.add('js')" not in main_js:
    ERRORS.append("main.js must opt the document into JavaScript-enhanced presentation")

enhancements_css = (ROOT / "assets/css/site-enhancements.css").read_text(encoding="utf-8") if (ROOT / "assets/css/site-enhancements.css").exists() else ""
for required in (
    ".reveal{opacity:1;transform:none}",
    "html.js .reveal{opacity:0;transform:translateY(12px)}",
    "html.js .nav-links{display:none}",
    ".not-found-grid{min-height:620px;grid-template-columns:1fr .55fr}",
):
    if required not in enhancements_css:
        ERRORS.append(f"Missing progressive/404 release wiring: {required}")

if ERRORS:
    print("RELEASE CHECK FAILED")
    for error in ERRORS:
        print(f"- {error}")
    sys.exit(1)

print("RELEASE CHECK PASSED")
print("Verified production redirect, canonical host, staging noindex, strict self-hosted CSP, progressive enhancement, Organization semantics, bilingual social locales, responsive stylesheets, static contact wiring, asset caching and responsive/noindex 404 policy.")
