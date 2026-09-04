from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
PLACEHOLDERS = (
    "EDEN_STRIPE_CHECKOUT_URL",
    "will be connected before public launch",
    "Billing management will open here once",
    "Closed beta access is currently invite-only",
)


class AssetParser(HTMLParser):
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        self.references = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        for name in ("href", "src"):
            value = attributes.get(name)
            if value:
                self.references.append(value)


def main():
    failures = []
    html_files = sorted(ROOT.glob("*.html"))
    assert html_files, "No HTML pages found."

    for page in html_files:
        text = page.read_text(encoding="utf-8")
        parser = AssetParser(page)
        parser.feed(text)
        for reference in parser.references:
            parsed = urlsplit(reference)
            if parsed.scheme or reference.startswith(("#", "mailto:")):
                continue
            local_path = ROOT / parsed.path
            if parsed.path and not local_path.exists():
                failures.append(f"{page.name}: missing {reference}")

    source_files = list(ROOT.glob("*.html")) + list(ROOT.glob("*.js"))
    for source in source_files:
        text = source.read_text(encoding="utf-8")
        for placeholder in PLACEHOLDERS:
            if placeholder in text:
                failures.append(f"{source.name}: launch placeholder: {placeholder}")

    if failures:
        raise SystemExit("\n".join(failures))
    print(f"Validated {len(html_files)} pages: local links and launch copy OK.")


if __name__ == "__main__":
    main()
