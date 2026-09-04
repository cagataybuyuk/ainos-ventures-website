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

    staging_rule = next((
        h for h in headers
        if any(rule.get("type") == "host" and rule.get("value") == "ainos-ventures-website.vercel.app" for rule in h.get("has", []))
    ), None)
    staging_map = {x.get("key"): x.get("value") for x in (staging_rule or {}).get("headers", [])}
    if "noindex" not in (staging_map.get("X-Robots-Tag") or "").lower():
        ERRORS.append("Staging host must send X-Robots-Tag noindex")

    cache_sources = ("/assets/js/(.*)", "/assets/css/(.*)", "/assets/images/(.*)")
    for source in cache_sources:
        rule = next((h for h in headers if h.get("source") == source), None)
        rule_map = {x.get("key"): x.get("value") for x in (rule or {}).get("headers", [])}
        cache_control = rule_map.get("Cache-Control") or ""
        if "max-age" not in cache_control:
            ERRORS.append(f"{source} must have an explicit cache policy")

    for source in ("/assets/js/(.*)", "/assets/css/(.*)"):
        rule = next((h for h in headers if h.get("source") == source), None)
        rule_map = {x.get("key"): x.get("value") for x in (rule or {}).get("headers", [])}
        cache_control = (rule_map.get("Cache-Control") or "").lower()
        if "max-age=0" not in cache_control or "must-revalidate" not in cache_control:
            ERRORS.append(f"{source} should revalidate during active launch to avoid stale releases")

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

root_html = (ROOT / "index.html").read_text(encoding="utf-8") if (ROOT / "index.html").exists() else ""
if "/en/" not in root_html:
    ERRORS.append("Root fallback page does not point to /en/")

not_found = (ROOT / "404.html").read_text(encoding="utf-8") if (ROOT / "404.html").exists() else ""
if "noindex" not in not_found.lower():
    ERRORS.append("404 page must remain noindex")

if ERRORS:
    print("RELEASE CHECK FAILED")
    for error in ERRORS:
        print(f"- {error}")
    sys.exit(1)

print("RELEASE CHECK PASSED")
print("Verified production redirect, canonical host, staging noindex, security headers, split asset caching and 404 indexing policy.")
