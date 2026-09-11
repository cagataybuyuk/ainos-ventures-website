from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{path.relative_to(ROOT)}: expected exactly one match, found {count}: {old!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


css = ROOT / "assets" / "css" / "team-tuning.css"
replace_once(
    css,
    "  --v2-quiet:#77766f;",
    "  --v2-quiet:#676760;\n  --muted:#626762;",
)
replace_once(
    css,
    ".eyebrow{margin-bottom:36px;color:#77766f}",
    ".eyebrow{margin-bottom:36px;color:var(--v2-quiet)}",
)

en = ROOT / "en" / "index.html"
replace_once(
    en,
    'aria-label="Türkçeye geç">TR</a>',
    'aria-label="TR — Türkçeye geç">TR</a>',
)
replace_once(
    en,
    ' href="mailto:contact@ainosventures.com" aria-label="Email Ainos Ventures">contact@ainosventures.com</a>',
    ' href="mailto:contact@ainosventures.com">contact@ainosventures.com</a>',
)

tr = ROOT / "tr" / "index.html"
replace_once(
    tr,
    'aria-label="Switch to English">EN</a>',
    'aria-label="EN — Switch to English">EN</a>',
)
replace_once(
    tr,
    ' href="mailto:contact@ainosventures.com" aria-label="Ainos Ventures ile e-posta üzerinden iletişime geç">contact@ainosventures.com</a>',
    ' href="mailto:contact@ainosventures.com">contact@ainosventures.com</a>',
)

print("Accessibility hardening applied successfully.")
