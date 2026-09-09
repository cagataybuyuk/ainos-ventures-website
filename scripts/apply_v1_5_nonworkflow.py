from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parents[1]
SOCIAL_URL = "https://ainosventures.com/assets/images/ainos-social-card.png"
SOCIAL_PATH = ROOT / "assets/images/ainos-social-card.png"
ALT = "Ainos Ventures — Strategy. Capital. Partnership."


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise SystemExit(f"Missing expected source for {label}")
    if text.count(old) != 1:
        raise SystemExit(f"Expected exactly one source for {label}, found {text.count(old)}")
    return text.replace(old, new, 1)


def patch_page(path: Path):
    text = path.read_text(encoding="utf-8")
    if SOCIAL_URL in text:
        return
    old = '  <meta name="twitter:card" content="summary">'
    block = f'''  <meta property="og:image" content="{SOCIAL_URL}">\n  <meta property="og:image:type" content="image/png">\n  <meta property="og:image:width" content="1200">\n  <meta property="og:image:height" content="630">\n  <meta property="og:image:alt" content="{ALT}">\n  <meta name="twitter:card" content="summary_large_image">\n  <meta name="twitter:image" content="{SOCIAL_URL}">\n  <meta name="twitter:image:alt" content="{ALT}">'''
    text = replace_once(text, old, block, str(path.relative_to(ROOT)))
    path.write_text(text, encoding="utf-8")


for rel in ("en/index.html", "tr/index.html"):
    patch_page(ROOT / rel)

raw = SOCIAL_PATH.read_bytes()
if raw[:8] != b"\x89PNG\r\n\x1a\n":
    raise SystemExit("Social card is not a PNG")
width, height = struct.unpack(">II", raw[16:24])
if (width, height) != (1200, 630):
    raise SystemExit(f"Unexpected social card dimensions: {width}x{height}")

path = ROOT / "scripts/site_check.py"
text = path.read_text(encoding="utf-8")
text = replace_once(text, '    for required_og in ("og:title", "og:description", "og:type", "og:url", "og:site_name"):\n', '    for required_og in ("og:title", "og:description", "og:type", "og:url", "og:site_name", "og:image", "og:image:type", "og:image:width", "og:image:height", "og:image:alt"):\n', "site_check required OG fields")
text = replace_once(text, '    if not page.meta.get("twitter:card"):\n        ERRORS.append(f"{rel}: missing twitter:card")\n', f'''    if page.og.get("og:image") != "{SOCIAL_URL}":\n        ERRORS.append(f"{{rel}}: og:image should use canonical social card")\n    if page.og.get("og:image:type") != "image/png":\n        ERRORS.append(f"{{rel}}: og:image:type should be image/png")\n    if page.og.get("og:image:width") != "1200" or page.og.get("og:image:height") != "630":\n        ERRORS.append(f"{{rel}}: social image dimensions must be 1200x630")\n    if page.meta.get("twitter:card") != "summary_large_image":\n        ERRORS.append(f"{{rel}}: twitter:card should be summary_large_image")\n    if page.meta.get("twitter:image") != "{SOCIAL_URL}":\n        ERRORS.append(f"{{rel}}: twitter:image should use canonical social card")\n    if not page.meta.get("twitter:image:alt"):\n        ERRORS.append(f"{{rel}}: missing twitter:image:alt")\n''', "site_check twitter/social assertions")
text = replace_once(text, '    "assets/images/tunca-web.jpg",\n]:\n', '    "assets/images/tunca-web.jpg",\n    "assets/images/ainos-social-card.png",\n]:\n', "site_check required social asset")
insert_anchor = 'robots = (ROOT / "robots.txt").read_text(encoding="utf-8") if (ROOT / "robots.txt").exists() else ""\n'
insert = '''social_path = ROOT / "assets/images/ainos-social-card.png"\nif social_path.exists():\n    social_raw = social_path.read_bytes()\n    if social_raw[:8] != b"\\x89PNG\\r\\n\\x1a\\n":\n        ERRORS.append("Social card must be a PNG")\n    elif len(social_raw) < 24:\n        ERRORS.append("Social card PNG is truncated")\n    else:\n        social_width, social_height = struct.unpack(">II", social_raw[16:24])\n        if (social_width, social_height) != (1200, 630):\n            ERRORS.append(f"Social card must be 1200x630, found {social_width}x{social_height}")\n\n'''
if 'import struct\n' not in text:
    text = replace_once(text, 'from pathlib import Path\n', 'from pathlib import Path\nimport struct\n', 'site_check struct import')
text = replace_once(text, insert_anchor, insert + insert_anchor, "site_check PNG validation")
path.write_text(text, encoding="utf-8")

path = ROOT / "scripts/release_check.py"
text = path.read_text(encoding="utf-8")
needle = '        \'itemprop="sameAs"\',\n'
replacement = needle + f'''        '<meta property="og:image" content="{SOCIAL_URL}">',\n        '<meta property="og:image:type" content="image/png">',\n        '<meta property="og:image:width" content="1200">',\n        '<meta property="og:image:height" content="630">',\n        '<meta name="twitter:card" content="summary_large_image">',\n        '<meta name="twitter:image" content="{SOCIAL_URL}">',\n'''
text = replace_once(text, needle, replacement, "release_check social metadata")
path.write_text(text, encoding="utf-8")

path = ROOT / "README.md"
text = path.read_text(encoding="utf-8")
anchor = 'Detailed V1.4 notes: `docs/V1_4_PRODUCTION_CONTRACTS.md`\n\n'
v15 = '''Detailed V1.4 notes: `docs/V1_4_PRODUCTION_CONTRACTS.md`\n\n### V1.5 — social sharing / OG package\n- [x] Added one shared 1200×630 Ainos Ventures social card\n- [x] Added canonical `og:image` metadata to EN/TR\n- [x] Added explicit Open Graph image type/dimensions/alt metadata\n- [x] Upgraded Twitter card metadata to `summary_large_image`\n- [x] Added CI and production-smoke contracts for the image and metadata\n\nDetailed V1.5 notes: `docs/V1_5_SOCIAL_SHARING.md`\n\n'''
text = replace_once(text, anchor, v15, "README V1.5 section")
text = text.replace('- Social sharing / OG image\n', '')
path.write_text(text, encoding="utf-8")

(ROOT / "docs/V1_5_SOCIAL_SHARING.md").write_text('''# V1.5 — Social Sharing / OG Package\n\n## Objective\nProvide a consistent Ainos Ventures corporate preview when the website is shared externally, without altering the approved on-page design.\n\n## Social card\n- Canonical asset: `https://ainosventures.com/assets/images/ainos-social-card.png`\n- Format: PNG\n- Dimensions: 1200 × 630\n- Shared by EN/TR because the artwork is intentionally language-neutral and uses the public brand spine `Strategy. Capital. Partnership.`\n- Visual system follows the production website: warm ivory, charcoal, official monogram, editorial serif headline and restrained circular geometry.\n\n## Metadata\nBoth `/en/` and `/tr/` declare `og:image`, explicit PNG type/dimensions/alt metadata, `twitter:card=summary_large_image`, `twitter:image` and `twitter:image:alt`. Canonical URLs, hreflang and Open Graph locale metadata remain unchanged.\n\n## Guardrails\n`site_check.py` validates the metadata, PNG signature and exact dimensions. `release_check.py` requires the production social metadata wiring. Production smoke separately verifies the deployed image and page references.\n\n## Explicit non-goals\nNo analytics, contact form/backend, Ainos Intelligence content, mail/DNS changes or on-page redesign were introduced in V1.5.\n''', encoding="utf-8")

print("V1.5 non-workflow migration applied")
