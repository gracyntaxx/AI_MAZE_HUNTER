"""Use the published BrowserFS CDN asset missing from Pygbag's 0.9.3 path."""

import argparse
from pathlib import Path

BROKEN_URL = "https://pygame-web.github.io/cdn/0.9.3//browserfs.min.js"
FIXED_URL = "https://cdnjs.cloudflare.com/ajax/libs/BrowserFS/2.0.0/browserfs.min.js"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("html_file", type=Path)
    html_file = parser.parse_args().html_file
    content = html_file.read_text(encoding="utf-8")
    if content.count(BROKEN_URL) != 1:
        raise ValueError(f"Expected one Pygbag BrowserFS URL in {html_file}.")
    html_file.write_text(content.replace(BROKEN_URL, FIXED_URL), encoding="utf-8")


if __name__ == "__main__":
    main()
