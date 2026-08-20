#!/usr/bin/env python3
"""Point the site at a real domain.

Until a domain exists the site deliberately ships with no canonical tags, a
root-relative og:image and no sitemap — a canonical pointing at a domain that
does not resolve is worse than having none at all.

Run this once the site has a permanent URL (the Vercel one is fine to start):

    python set-domain.py https://abcoaching.vercel.app
    python set-domain.py https://abcoachingfitness.ie

It is safe to run repeatedly; it replaces whatever was set last time.
"""

import glob
import json
import re
import sys

PAGES = {
    "index.html": "/",
    "about.html": "/about",
    "coaching.html": "/coaching",
    "results.html": "/results",
    "get-started.html": "/get-started",
}
# thanks.html is noindex, so it gets no canonical and stays out of the sitemap.

PRIORITY = {"/": "1.0", "/coaching": "0.9", "/get-started": "0.9",
            "/results": "0.8", "/about": "0.7"}


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: python set-domain.py https://example.com")

    base = sys.argv[1].rstrip("/")
    if not base.startswith(("http://", "https://")):
        sys.exit("Domain must start with https:// (or http://)")

    for page, path in PAGES.items():
        s = open(page, encoding="utf-8").read()
        url = base + path

        # Clear anything a previous run added, so this is idempotent.
        s = re.sub(r'\n<link rel="canonical"[^>]*>', "", s)
        s = re.sub(r'\n<meta property="og:url"[^>]*>', "", s)

        tags = (f'\n<link rel="canonical" href="{url}">'
                f'\n<meta property="og:url" content="{url}">')
        s = s.replace('<meta property="og:type" content="website">',
                      f'{tags.lstrip()}\n<meta property="og:type" content="website">', 1)

        # Social scrapers are unreliable with relative image paths.
        s = re.sub(r'(<meta property="og:image" content=")[^"]*(")',
                   rf'\1{base}/images/social-card.jpg\2', s)

        # Structured data wants absolute URLs too.
        if page == "index.html":
            m = re.search(r'(<script type="application/ld\+json">)([\s\S]*?)(</script>)', s)
            if m:
                data = json.loads(m.group(2))
                data["url"] = base + "/"
                data["image"] = base + "/images/social-card.jpg"
                s = s[:m.start(2)] + "\n" + json.dumps(data, indent=2) + "\n" + s[m.end(2):]

        open(page, "w", encoding="utf-8").write(s)
        print(f"  {page:20} -> {url}")

    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for path, pr in sorted(PRIORITY.items(), key=lambda kv: -float(kv[1])):
            f.write(f"  <url><loc>{base}{path}</loc><priority>{pr}</priority></url>\n")
        f.write("</urlset>\n")
    print("  sitemap.xml          regenerated")

    with open("robots.txt", "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {base}/sitemap.xml\n")
    print("  robots.txt           updated")

    print(f"\nDone. Site now points at {base}")
    print("Commit and push, and Vercel will redeploy automatically.")


if __name__ == "__main__":
    main()
