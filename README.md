# AB Coaching Fitness

Marketing site for Augusto Baronio — strength and conditioning for competitive
grapplers, Dublin and online.

Static HTML, CSS and one small JavaScript file. No build step, no framework, no
dependencies. Google Fonts is the only external request.

## Run it locally

```bash
python serve.py
```

Then open <http://localhost:8137>.

Use `serve.py` rather than `python -m http.server`. The site uses clean URLs
(`/about`, not `/about.html`) and the built-in server cannot resolve those, so
links look broken locally even though they work in production. `serve.py` adds
the same fallback Vercel applies.

## Deploy

Push to GitHub, then import the repo at [vercel.com/new](https://vercel.com/new).

No build command and no output directory — it is a static site, so Vercel's
defaults are correct. `vercel.json` handles clean URLs, caching and security
headers. Every push to `main` redeploys automatically.

## Showing it to Augusto

The site is currently in **draft mode**: every page is `noindex, nofollow` and
`robots.txt` disallows everything. A Vercel URL is fully public, so without this
a half-finished site with his name on it could start showing up in Google before
he has approved it — and once indexed, it competes with the real site later.

Deploy and share the URL freely. Check the state any time with:

```bash
python draft-mode.py status
```

**Make the form work for the demo.** Clients test the contact form; it is the
first thing they click. Rather than waiting on Augusto, create the Formspree
form against *your own* email, paste the ID into `get-started.html`, and swap it
to his at launch. Then the demo works end to end and you see the enquiry arrive.

When he approves it:

```bash
python draft-mode.py off
```

## Once there is a permanent URL

The site ships with **no canonical tags and no sitemap** on purpose: pointing
them at a domain that does not resolve is worse than omitting them. Once you
have a URL — the `.vercel.app` one is fine to start with — run:

```bash
python set-domain.py https://your-domain.com
```

That adds canonical and `og:url` tags to every page, makes `og:image` absolute
so social previews work, fills in the structured data, and generates
`sitemap.xml` and `robots.txt`. Safe to run again whenever the domain changes.

## Before it goes public

1. **Turn draft mode off** — `python draft-mode.py off`. Nothing gets indexed
   until you do.
2. **Point it at the domain** — `python set-domain.py https://...`.
3. **The enquiry form must be wired to Augusto's email.** `get-started.html` has
   a `YOUR_FORM_ID` placeholder. Vercel has no built-in form handling, so
   without a Formspree endpoint the site's only call to action silently
   discards submissions.
4. **Confirm the details with him.** The biography on `/about` is drawn from his
   own public Instagram post, and "3 coaching slots open this month" appears
   twice and will go stale.

## Layout

| Path | What it is |
|---|---|
| `*.html` | One file per page. `thanks.html` is the post-submit page and is `noindex` |
| `styles.css` | Every colour, type and spacing token. Shared by all pages |
| `app.js` | Scroll reveals only. Delete it and the site still works |
| `images/` | Photography plus the 1200×630 social share card |
| `videos/` | Empty. `README.md` there explains how to add client video stories |
| `serve.py` | Local dev server with Vercel-style clean URLs |
| `set-domain.py` | Points the site at a real domain |
| `vercel.json` | Clean URLs, cache headers, security headers |
| `HANDOFF.md` | Full build state, decisions and open items |

`.research/` holds the original scraped source material and is git-ignored — it
is reference, not part of the site.
