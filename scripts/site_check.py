from html.parser import HTMLParser
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PAGES = {
    ROOT / "en" / "index.html": "en",
    ROOT / "tr" / "index.html": "tr",
}
ERRORS = []
WARNINGS = []


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.hrefs = []
        self.assets = []
        self.html_lang = None
        self.canonical = None
        self.alternates = {}
        self.robots = None
        self.meta = {}
        self.og = {}
        self.h1_count = 0
        self.title_count = 0
        self._in_title = False
        self.title_text = ""

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if tag == "html":
            self.html_lang = data.get("lang")
        if tag == "h1":
            self.h1_count += 1
        if tag == "title":
            self.title_count += 1
            self._in_title = True
        if "id" in data:
            self.ids.append(data["id"])
        if "href" in data:
            href = data["href"]
            self.hrefs.append(href)
            if href.startswith("/assets/"):
                self.assets.append(href)
        if "src" in data:
            src = data["src"]
            if src.startswith("/assets/"):
                self.assets.append(src)
        if tag == "link" and data.get("rel") == "canonical":
            self.canonical = data.get("href")
        if tag == "link" and data.get("rel") == "alternate" and data.get("hreflang"):
            self.alternates[data["hreflang"]] = data.get("href")
        if tag == "meta":
            name = data.get("name")
            prop = data.get("property")
            content = data.get("content")
            if name:
                self.meta[name.lower()] = content
            if prop:
                self.og[prop.lower()] = content
            if name == "robots":
                self.robots = content

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title_text += data


def parse(path: Path):
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


for path, lang in PAGES.items():
    rel = path.relative_to(ROOT)
    if not path.exists():
        ERRORS.append(f"Missing required page: {rel}")
        continue

    text = path.read_text(encoding="utf-8")
    page = parse(path)

    if page.html_lang != lang:
        ERRORS.append(f"{rel}: expected html lang={lang!r}, found {page.html_lang!r}")

    if page.title_count != 1 or not page.title_text.strip():
        ERRORS.append(f"{rel}: must contain exactly one non-empty <title>")

    if page.h1_count != 1:
        ERRORS.append(f"{rel}: expected exactly one h1, found {page.h1_count}")

    for required_meta in ("description", "viewport"):
        if not page.meta.get(required_meta):
            ERRORS.append(f"{rel}: missing meta {required_meta}")

    expected_canonical = f"https://ainosventures.com/{lang}/"
    if page.canonical != expected_canonical:
        ERRORS.append(f"{rel}: canonical should be {expected_canonical}")
    if page.canonical and "vercel.app" in page.canonical:
        ERRORS.append(f"{rel}: staging URL must never be canonical")

    expected_alternates = {
        "en": "https://ainosventures.com/en/",
        "tr": "https://ainosventures.com/tr/",
        "x-default": "https://ainosventures.com/en/",
    }
    for hreflang, expected_url in expected_alternates.items():
        if page.alternates.get(hreflang) != expected_url:
            ERRORS.append(f"{rel}: hreflang {hreflang} should be {expected_url}")

    for required_og in ("og:title", "og:description", "og:type", "og:url", "og:site_name"):
        if not page.og.get(required_og):
            ERRORS.append(f"{rel}: missing {required_og}")

    if page.og.get("og:url") != expected_canonical:
        ERRORS.append(f"{rel}: og:url should match canonical")

    if not page.meta.get("twitter:card"):
        ERRORS.append(f"{rel}: missing twitter:card")

    if page.robots and "noindex" in page.robots.lower():
        ERRORS.append(f"{rel}: production language pages must be indexable")

    duplicates = sorted({x for x in page.ids if page.ids.count(x) > 1})
    if duplicates:
        ERRORS.append(f"{rel}: duplicate ids: {', '.join(duplicates)}")

    ids = set(page.ids)
    for href in page.hrefs:
        if href.startswith("#") and len(href) > 1 and href[1:] not in ids:
            ERRORS.append(f"{rel}: anchor {href} has no target id")

    for asset in page.assets:
        asset_path = ROOT / asset.lstrip("/")
        if not asset_path.exists():
            ERRORS.append(f"{rel}: missing asset {asset}")

    if "/assets/css/team-tuning.css" not in page.hrefs:
        ERRORS.append(f"{rel}: missing responsive team tuning stylesheet")

    other_lang = "tr" if lang == "en" else "en"
    if f"/{other_lang}/" not in page.hrefs:
        ERRORS.append(f"{rel}: missing visible language switch to /{other_lang}/")

    if "Mert Özel" in text:
        ERRORS.append(f"{rel}: retired team entry Mert Özel must not remain in source")

    if 'id="focus"' not in text:
        ERRORS.append(f"{rel}: approved Current Focus section is missing")

    if "Selected Work" in text or "Seçilmiş Çalışmalar" in text:
        ERRORS.append(f"{rel}: retired Selected Work wording must not remain")

    for retired_figure in ("~$50m", "~€100m"):
        if retired_figure in text:
            ERRORS.append(f"{rel}: retired deal figure {retired_figure} must not remain")

    expected_focus = (
        ("Energy & Infrastructure", "Industrial & Technology", "Consumer & Hospitality", "Digital Assets & Technology")
        if lang == "en"
        else ("Enerji & Altyapı", "Sanayi & Teknoloji", "Tüketici & Konaklama", "Dijital Varlıklar & Teknoloji")
    )
    for focus_name in expected_focus:
        if focus_name not in text:
            ERRORS.append(f"{rel}: missing approved focus area {focus_name}")

for required in [
    "robots.txt",
    "sitemap.xml",
    "vercel.json",
    "404.html",
    "assets/css/styles.css",
    "assets/css/team-tuning.css",
    "assets/js/main.js",
    "assets/images/favicon.svg",
    "assets/images/ainos-monogram.svg",
    "assets/images/nidan-web.jpg",
    "assets/images/tunca-web.jpg",
]:
    if not (ROOT / required).exists():
        ERRORS.append(f"Missing required file: {required}")

sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8") if (ROOT / "sitemap.xml").exists() else ""
for url in ("https://ainosventures.com/en/", "https://ainosventures.com/tr/"):
    if url not in sitemap:
        ERRORS.append(f"sitemap.xml missing {url}")

robots = (ROOT / "robots.txt").read_text(encoding="utf-8") if (ROOT / "robots.txt").exists() else ""
if "https://ainosventures.com/sitemap.xml" not in robots:
    ERRORS.append("robots.txt does not reference the production sitemap")

if (ROOT / "404.html").exists():
    p404 = parse(ROOT / "404.html")
    if not p404.robots or "noindex" not in p404.robots.lower():
        ERRORS.append("404.html must be noindex")

main_js = (ROOT / "assets/js/main.js").read_text(encoding="utf-8") if (ROOT / "assets/js/main.js").exists() else ""
for required_js in (
    "contact@ainosventures.com",
    "ainos-monogram.svg",
    "nidan-web.jpg",
    "tunca-web.jpg",
    "Skip to main content",
    "Ana içeriğe geç",
    "prefers-reduced-motion",
    "aria-expanded",
    "https://www.linkedin.com/company/ainos-ventures/",
):
    if required_js not in main_js:
        ERRORS.append(f"main.js missing required production/accessibility/team wiring: {required_js}")

for profile in (
    "https://www.linkedin.com/in/tunca-cingöz-429592a/",
    "https://www.linkedin.com/in/nidan-akmanoglu-163b6918/",
):
    if profile not in main_js:
        ERRORS.append(f"main.js missing approved LinkedIn profile: {profile}")

for warning in WARNINGS:
    print(f"WARNING: {warning}")

if ERRORS:
    print("\nSITE CHECK FAILED")
    for error in ERRORS:
        print(f"- {error}")
    sys.exit(1)

print("SITE CHECK PASSED")
print(f"Checked {len(PAGES)} language pages plus approved focus content, metadata, navigation, deployment, accessibility, brand/contact/team wiring, responsive tuning, SEO and asset requirements.")
