#!/usr/bin/env python3
"""Toggle the whole site between draft and live.

Draft mode keeps the site out of Google while it is being reviewed. That
matters: a Vercel preview URL is fully public, so without this a half-finished
site carrying a real person's name can start appearing in search results before
they have approved it — and once indexed it competes with the real site later.

    python draft-mode.py on      # noindex everywhere, robots.txt disallows all
    python draft-mode.py off     # ready to be indexed

Check which mode you are in:

    python draft-mode.py status
"""

import glob
import re
import sys

TAG = '<meta name="robots" content="noindex, nofollow">'
MARK = "<!-- DRAFT MODE -->"
BLOCK = f"{MARK}\n{TAG}\n"

# thanks.html carries its own permanent noindex and is left alone.
PAGES = [p for p in sorted(glob.glob("*.html")) if p != "thanks.html"]


def strip(s):
    s = s.replace(BLOCK, "")
    s = re.sub(r'\n?<!-- DRAFT MODE -->\n?<meta name="robots"[^>]*>\n?', "\n", s)
    return s


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ("on", "off", "status"):
        sys.exit("usage: python draft-mode.py on|off|status")
    mode = sys.argv[1]

    if mode == "status":
        on = [p for p in PAGES if MARK in open(p, encoding="utf-8").read()]
        if len(on) == len(PAGES):
            print(f"DRAFT — all {len(PAGES)} pages are noindex. Not visible in search.")
        elif not on:
            print(f"LIVE — all {len(PAGES)} pages are indexable.")
        else:
            print(f"MIXED — {len(on)} of {len(PAGES)} pages are noindex: {', '.join(on)}")
        print("robots.txt:", open("robots.txt", encoding="utf-8").read().strip().replace("\n", " | "))
        return

    for page in PAGES:
        s = strip(open(page, encoding="utf-8").read())
        if mode == "on":
            # Sits directly after the viewport tag, high in <head>.
            s = re.sub(r'(<meta name="viewport"[^>]*>\n)', rf"\1{BLOCK}", s, count=1)
        open(page, "w", encoding="utf-8").write(s)
        print(f"  {page:20} {'noindex' if mode == 'on' else 'indexable'}")

    with open("robots.txt", "w", encoding="utf-8") as f:
        if mode == "on":
            f.write("# Draft. Run: python draft-mode.py off\nUser-agent: *\nDisallow: /\n")
        else:
            f.write("User-agent: *\nAllow: /\n")
    print(f"  robots.txt           {'disallow all' if mode == 'on' else 'allow all'}")

    if mode == "on":
        print("\nDRAFT MODE ON. Safe to share the URL — search engines will skip it.")
    else:
        print("\nLIVE MODE. Run set-domain.py too, so canonical tags and the sitemap exist.")


if __name__ == "__main__":
    main()
