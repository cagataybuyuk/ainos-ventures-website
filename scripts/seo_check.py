from html.parser import HTMLParser
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ERRORS = []

CANONICAL = {
    "en": "https://ainosventures.com/en/",
    "tr": "https://ainosventures.com/tr/",
}
ALTERNATES = {
    "en": "https://ainosventures.com/en/",
    "tr": "https://ainosventures.com/tr/",
    "x-default": "https://ainosventures.com/en/",
}
SITEMAP_URL = "https://ainosventures.com/sitemap.xml"

ARTICLE_ROUTES = {
    "en/intelligence/turkiye-regional-platform": {
        "canonical": "https://ainosventures.com/en/intelligence/turkiye-regional-platform/",
        "alternates": {
            "en": "https://ainosventures.com/en/intelligence/turkiye-regional-platform/",
            "tr": "https://ainosventures.com/tr/intelligence/turkiye-regional-platform/",
            "x-default": "https://ainosventures.com/en/intelligence/turkiye-regional-platform/",
        },
    },
    "tr/intelligence/turkiye-regional-platform": {
        "canonical": "https://ainosventures.com/tr/intelligence/turkiye-regional-platform/",
        "alternates": {
            "en": "https://ainosventures.com/en/intelligence/turkiye-regional-platform/",
            "tr": "https://ainosventures.com/tr/intelligence/turkiye-regional-platform/",
            "x-default": "https://ainosventures.com/en/intelligence/turkiye-regional-platform/",
        },
    },
}



class SeoParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.html_lang = None
        self.canonical = None
        self.alternates = {}
        self.robots = None
        self.og_url = None

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if tag == "html":
            self.html_lang = data.get("lang")
        if tag == "link" and data.get("rel") == "canonical":
            self.canonical = data.get("href")
        if tag == "link" and data.get("rel") == "alternate" and data.get("hreflang"):
            hreflang = data["hreflang"]
            if hreflang in self.alternates:
                ERRORS.append(f"duplicate hreflang annotation: {hreflang}")
            self.alternates[hreflang] = data.get("href")
        if tag == "meta":
            name = (data.get("name") or "").lower()
            prop = (data.get("property") or "").lower()
            if name == "robots":
                self.robots = data.get("content") or ""
            if prop == "og:url":
                self.og_url = data.get("content")


def parse_html(path: Path):
    parser = SeoParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


for lang, expected_canonical in CANONICAL.items():
    path = ROOT / lang / "index.html"
    if not path.exists():
        ERRORS.append(f"missing language page: /{lang}/")
        continue

    text = path.read_text(encoding="utf-8")
    page = parse_html(path)

    if page.html_lang != lang:
        ERRORS.append(f"/{lang}/ html lang must be {lang}")
    if page.canonical != expected_canonical:
        ERRORS.append(f"/{lang}/ canonical must be {expected_canonical}")
    if page.og_url != expected_canonical:
        ERRORS.append(f"/{lang}/ og:url must match canonical")
    if page.alternates != ALTERNATES:
        ERRORS.append(f"/{lang}/ hreflang set must be exactly {ALTERNATES}, found {page.alternates}")
    if page.robots and "noindex" in page.robots.lower():
        ERRORS.append(f"/{lang}/ must remain indexable")
    if "www.ainosventures.com" in text or "ainos-ventures-website.vercel.app" in text:
        ERRORS.append(f"/{lang}/ contains a non-canonical host in public metadata/source")



for route, config in ARTICLE_ROUTES.items():
    path = ROOT / route / "index.html"
    if not path.exists():
        ERRORS.append(f"missing intelligence page: /{route}/")
        continue

    text = path.read_text(encoding="utf-8")
    page = parse_html(path)

    if page.html_lang != route.split("/", 1)[0]:
        ERRORS.append(f"/{route}/ html lang does not match route")
    if page.canonical != config["canonical"]:
        ERRORS.append(f"/{route}/ canonical must be {config['canonical']}")
    if page.og_url != config["canonical"]:
        ERRORS.append(f"/{route}/ og:url must match canonical")
    if page.alternates != config["alternates"]:
        ERRORS.append(f"/{route}/ hreflang set must be exactly {config['alternates']}, found {page.alternates}")
    if page.robots and "noindex" in page.robots.lower():
        ERRORS.append(f"/{route}/ must remain indexable")
    if "www.ainosventures.com" in text or "ainos-ventures-website.vercel.app" in text:
        ERRORS.append(f"/{route}/ contains a non-canonical host in public metadata/source")


sitemap_path = ROOT / "sitemap.xml"
if not sitemap_path.exists():
    ERRORS.append("missing sitemap.xml")
else:
    try:
        tree = ET.parse(sitemap_path)
        root = tree.getroot()
    except ET.ParseError as exc:
        ERRORS.append(f"sitemap.xml is not valid XML: {exc}")
    else:
        sitemap_ns = "http://www.sitemaps.org/schemas/sitemap/0.9"
        xhtml_ns = "http://www.w3.org/1999/xhtml"
        if root.tag != f"{{{sitemap_ns}}}urlset":
            ERRORS.append("sitemap.xml root must be a sitemap urlset")

        seen = set()
        for url_el in root.findall(f"{{{sitemap_ns}}}url"):
            loc_el = url_el.find(f"{{{sitemap_ns}}}loc")
            loc = (loc_el.text or "").strip() if loc_el is not None else ""
            if not loc:
                ERRORS.append("sitemap entry missing <loc>")
                continue
            if loc in seen:
                ERRORS.append(f"duplicate sitemap URL: {loc}")
            seen.add(loc)

            alternates = {}
            for link in url_el.findall(f"{{{xhtml_ns}}}link"):
                if link.attrib.get("rel") != "alternate":
                    continue
                hreflang = link.attrib.get("hreflang")
                href = link.attrib.get("href")
                if not hreflang or not href:
                    ERRORS.append(f"{loc}: malformed hreflang sitemap annotation")
                    continue
                if hreflang in alternates:
                    ERRORS.append(f"{loc}: duplicate sitemap hreflang {hreflang}")
                alternates[hreflang] = href

            expected_alternates = ALTERNATES
            for route_config in ARTICLE_ROUTES.values():
                if loc == route_config["canonical"]:
                    expected_alternates = route_config["alternates"]
                    break
            if alternates != expected_alternates:
                ERRORS.append(f"{loc}: sitemap hreflang set must be exactly {expected_alternates}, found {alternates}")

        expected_urls = set(CANONICAL.values()) | {config["canonical"] for config in ARTICLE_ROUTES.values()}
        if seen != expected_urls:
            ERRORS.append(f"sitemap canonical URL set must be exactly {sorted(expected_urls)}, found {sorted(seen)}")

        raw_sitemap = sitemap_path.read_text(encoding="utf-8")
        for forbidden in ("http://ainosventures.com", "www.ainosventures.com", "vercel.app"):
            if forbidden in raw_sitemap:
                ERRORS.append(f"sitemap.xml contains forbidden/non-canonical host pattern: {forbidden}")


robots_path = ROOT / "robots.txt"
if not robots_path.exists():
    ERRORS.append("missing robots.txt")
else:
    robots_lines = [line.strip() for line in robots_path.read_text(encoding="utf-8").splitlines() if line.strip() and not line.lstrip().startswith("#")]
    required_lines = {
        "User-agent: *",
        "Allow: /",
        f"Sitemap: {SITEMAP_URL}",
    }
    missing = sorted(required_lines.difference(robots_lines))
    if missing:
        ERRORS.append(f"robots.txt missing required directives: {missing}")
    if any(line.lower() == "disallow: /" for line in robots_lines):
        ERRORS.append("robots.txt must not block the full production site")


vercel_path = ROOT / "vercel.json"
if not vercel_path.exists():
    ERRORS.append("missing vercel.json")
else:
    config = json.loads(vercel_path.read_text(encoding="utf-8"))
    root_redirect = next((r for r in config.get("redirects", []) if r.get("source") == "/"), None)
    if not root_redirect:
        ERRORS.append("missing server-side root redirect")
    else:
        if root_redirect.get("destination") != "/en/":
            ERRORS.append("root redirect must point to /en/")
        if root_redirect.get("permanent") is not True:
            ERRORS.append("root redirect must remain permanent")
    if config.get("trailingSlash") is not True:
        ERRORS.append("trailingSlash must remain enabled to match canonical URLs")


root_fallback = ROOT / "index.html"
if root_fallback.exists():
    text = root_fallback.read_text(encoding="utf-8")
    if 'content="0; url=/en/"' not in text:
        ERRORS.append("root fallback page must retain immediate /en/ meta refresh")
    if '<link rel="canonical" href="https://ainosventures.com/en/">' not in text:
        ERRORS.append("root fallback page must canonicalize to /en/")


not_found_path = ROOT / "404.html"
if not_found_path.exists():
    page = parse_html(not_found_path)
    if not page.robots or "noindex" not in page.robots.lower():
        ERRORS.append("404 page must remain noindex")
    if page.canonical:
        ERRORS.append("404 page must not declare a canonical URL")


if ERRORS:
    print("TECHNICAL SEO CHECK FAILED")
    for error in ERRORS:
        print(f"- {error}")
    sys.exit(1)

print("TECHNICAL SEO CHECK PASSED")
print("Verified canonical routes, reciprocal EN/TR/x-default hreflang, exact sitemap coverage, robots discovery, permanent root routing, canonical host hygiene, indexable language pages and noindex 404 behavior.")
