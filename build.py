#!/usr/bin/env python3
"""
Stamp the shared header and footer into every page.

The site is plain static HTML served by GitHub Pages, so this deliberately
writes finished HTML to disk rather than assembling anything in the browser:
the pages stay complete for crawlers and for visitors without JavaScript.

Edit _partials/header.html or _partials/footer.html, run this, commit the
result.

    python build.py            # rewrite the pages
    python build.py --check    # exit 1 if any page is out of date (no writes)

Each page marks where its shared parts go:

    <!-- BUILD:header -->  ...generated...  <!-- /BUILD:header -->

Anything between the markers is generated and will be overwritten. The nav
link matching the page's key (see PAGES) is marked as the current page.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
PARTIALS = ROOT / "_partials"

# page -> which nav item is the current one ("" = no nav item matches)
PAGES = {
    "index.html": "home",
    "about.html": "about",
    "blog.html": "blog",
    "resources.html": "resources",
    "interviews.html": "interviews",
    "contact.html": "contact",
    # the posts live under the Blog section
    "post-1.html": "blog",
    "post-2.html": "blog",
    "post-3.html": "blog",
}


def marker_span(html, name, path):
    """Return (start, end) of the generated region for `name`, or exit loudly.

    A page with a mangled marker pair would otherwise be skipped silently and
    quietly drift away from the partials, so every failure here is fatal.
    """
    open_tag, close_tag = f"<!-- BUILD:{name} -->", f"<!-- /BUILD:{name} -->"
    opens, closes = html.count(open_tag), html.count(close_tag)
    if opens != 1 or closes != 1:
        sys.exit(f"{path.name}: expected exactly one {open_tag} and one "
                 f"{close_tag}, found {opens} and {closes}")
    start, end = html.find(open_tag), html.find(close_tag)
    if end < start:
        sys.exit(f"{path.name}: {close_tag} appears before {open_tag}")
    return start + len(open_tag), end


def mark_current(header_html, key):
    """Add nav-active + aria-current to the link for the current page."""
    if not key:
        return header_html

    def add(match):
        tag = match.group(0)
        if f'data-nav="{key}"' not in tag:
            return tag
        # the Contact item is styled as a pill (header-contact-link), not a nav-link
        tag = re.sub(r'class="((?:nav-link|mobile-nav-link|header-contact-link)\b[^"]*)"',
                     r'class="\1 nav-active"', tag)
        return tag[:-1].rstrip() + ' aria-current="page">'

    return re.sub(r"<a\b[^>]*data-nav=[^>]*>", add, header_html)


def main():
    check = "--check" in sys.argv
    header = (PARTIALS / "header.html").read_text(encoding="utf-8").strip()
    footer = (PARTIALS / "footer.html").read_text(encoding="utf-8").strip()

    changed = []
    for name, key in PAGES.items():
        path = ROOT / name
        if not path.exists():
            sys.exit(f"{name}: listed in PAGES but not found")
        original = path.read_text(encoding="utf-8")

        html = original
        for part, body in (("header", mark_current(header, key)), ("footer", footer)):
            start, end = marker_span(html, part, path)
            html = html[:start] + "\n" + body + "\n" + html[end:]

        if html != original:
            changed.append(name)
            if not check:
                path.write_text(html, encoding="utf-8")

    if check:
        if changed:
            print("Out of date (run: python build.py):")
            for n in changed:
                print("  " + n)
            return 1
        print(f"All {len(PAGES)} pages are up to date.")
        return 0

    if changed:
        print(f"Updated {len(changed)} of {len(PAGES)} pages:")
        for n in changed:
            print("  " + n)
    else:
        print(f"All {len(PAGES)} pages already up to date.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
