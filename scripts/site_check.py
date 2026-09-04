from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
import re
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

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if tag == "html":
            self.html_lang = data.get("lang")
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
        if tag == "meta" and data.get("name") == "robots":
            self.robots = data.get("content")


def parse(path: Path):
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser

for path, lang in PAGES.items():
    if not path.exists():
        ERRORS.append(f"Missing required page: {path.relative_to(ROOT)}")
        continue

    text = path.read_text(encoding="utf-8")
    page = parse(path)

    if page.html_lang != lang:
        ERRORS.append(f"{path.relative_to(ROOT)}: expected html lang={lang!r}, found {page.html_lang!r}")

    expected_canonical = f"https://ainosventures.com/{lang}/"
    if page.canonical != expected_canonical:
        ERRORS.append(f"{path.relative_to(ROOT)}: canonical should be {expected_canonical}")

    for required_lang in ("en", "tr", "x-default"):
        if required_lang not in page.alternates:
            ERRORS.append(f"{path.relative_to(ROOT)}: missing hreflang {required_lang}")

    duplicates = sorted({x for x in page.ids if page.ids.count(x) > 1})
    if duplicates:
        ERRORS.append(f"{path.relative_to(ROOT)}: duplicate ids: {', '.join(duplicates)}")

    ids = set(page.ids)
    for href in page.hrefs:
        if href.startswith("#") and len(href) > 1 and href[1:] not in ids:
            ERRORS.append(f"{path.relative_to(ROOT)}: anchor {href} has no target id")

    for asset in page.assets:
        asset_path = ROOT / asset.lstrip("/")
        if not asset_path.exists():
            ERRORS.append(f"{path.relative_to(ROOT)}: missing asset {asset}")

    if "Mert Özel" in text:
        WARNINGS.append(f"{path.relative_to(ROOT)} still contains the retired staging team entry in source; rendered JS removes it. Clean this when final bios are merged.")

for required in ["robots.txt", "sitemap.xml", "vercel.json", "404.html", "assets/css/styles.css", "assets/js/main.js", "assets/images/favicon.svg"]:
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

for warning in WARNINGS:
    print(f"WARNING: {warning}")

if ERRORS:
    print("\nSITE CHECK FAILED")
    for error in ERRORS:
        print(f"- {error}")
    sys.exit(1)

print("SITE CHECK PASSED")
print(f"Checked {len(PAGES)} language pages plus deployment, SEO and asset requirements.")
