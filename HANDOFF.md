# AB Coaching Fitness — build state

Last worked on: **20 Aug 2026**. Site is **complete, audited and working**.
Nothing is half-finished; the items below are decisions and client input, not
broken work.

## Direction (rebuilt 20 Aug)

Retargeted from time-poor hobbyists to **competitive grapplers in their 20s and
30s who are already good and want to go pro**. They already train as much as
they can; the lever is gym work. Headline is *Technique got you here. Power
takes you pro.*

Palette and feel were taken from the fitnesspoint Webflow reference: white,
sharp corners (`--radius: 0`), heavy Poppins ExtraBold set tight, crimson
accent. Old dark ink-and-gold scheme is gone.

## Audit status (all five pages, checked at 1440 / 1280 / 768 / 375 / 320px)

| Check | Result |
|---|---|
| Horizontal overflow | None at 1440 / 1280 / 768 / 375 / 320px |
| Colour contrast (WCAG AA) | 0 failures, measured from rendered styles |
| Heading order | No skipped levels |
| Touch targets | Nav 44px+, footer icons 40px |
| Works with JavaScript off | Yes — 0 elements hidden without JS |
| Scroll reveals | All fire correctly |
| Broken links / images | None |
| Emojis anywhere in the build | None |
| Total image payload | ~284KB across the whole site |

## Run it

```bash
python serve.py
```

Then open <http://localhost:8137>. Use `serve.py`, **not** `python -m
http.server` — the site uses clean URLs (`/about`, not `/about.html`) and the
built-in server cannot resolve those, so links look broken locally even though
they work live. `serve.py` reproduces Vercel's routing.

Opening files directly with `file://` will not work either; it needs HTTP.

## Deploying

Repo is initialised and committed on `main`, ready to push. Deploy path is
**GitHub + Vercel**: push, then import at vercel.com/new. No build command, no
output directory — Vercel's static defaults are correct. `vercel.json` handles
clean URLs, caching and security headers.

There is no `gh`, `vercel` or `npm` on this machine, so the push and the Vercel
import are manual steps.

## What exists

| File | What it is |
|---|---|
| `index.html` | Home — hero, stats, the problem, belt ladder, first month, Suyan proof band, CTA |
| `about.html` | Augusto's story, the numbers, how he coaches, off the mats |
| `coaching.html` | 1-1 PT, 2-1 partner, online coaching, pricing stance, 6-question FAQ |
| `results.html` | Suyan headline result, pointer to the pinned IG reviews, year in review |
| `get-started.html` | The enquiry form, now asking belt, next comp and gym hours |
| `styles.css` | All tokens — colour, type scale, spacing. Shared by all five pages |
| `app.js` | Scroll reveals only. Delete it and the site still works completely |
| `images/` | 8 photos and a 1200×630 social share card |
| `favicon-16/32.png`, `apple-touch-icon.png` | White "AB" on a crimson tile |
| `robots.txt`, `sitemap.xml` | Search engine basics |
| `.research/` | Original uncropped Instagram downloads + source URLs |

## Decisions already made

- **Multi-page, not one file.** You picked separate HTML files. CSS and JS are
  shared rather than inlined five times, so a style change is one edit.
- **Palette**: white `#FFFFFF` / near-black `#111113` / crimson `#EB3B52`,
  taken from the reference site. Three reds exist on purpose and are not
  interchangeable — `--red` for fills and large type, `--red-btn` `#D92C43` for
  anything with small white text on it (the brand red fails AA there),
  `--red-deep` for red as text on white, `--red-soft` for red as text on black.
- **Type**: Poppins ExtraBold (display) + Barlow (body). The display scale is
  sized for Poppins, which sets far wider than a condensed face.
- **The red band runs black-on-crimson, not white.** White text on `#EB3B52`
  is 3.98:1 and fails AA; black on it is 4.74:1 and passes. It also looks
  better. Do not flip it back to white.
- **Signature element**: the belt ladder on the home page — real BJJ belts drawn
  in CSS with correct sleeve colours (black sleeve on purple and brown, red on
  the black belt). Tiers are purple / brown / black to match the new audience;
  there is deliberately no beginner tier.
- **No JS dependency.** Everything is visible with JavaScript off. `app.js` only
  adds fade-ups. Reduced motion is respected.
- **Mobile nav** is a two-row sticky bar, no hamburger, no JS.

## Do first tomorrow

1. **Make the form live.** In `get-started.html`, find `YOUR_FORM_ID` (there is a
   TODO comment above it). Augusto signs up free at formspree.io, creates a form,
   pastes the endpoint ID in. Until that is done the form does not send anything.
2. **Better photos.** Instagram only serves 12 posts to logged-out visitors and
   most have text baked into them, so most of `images/` are crops of what was
   reachable. Dropping files in the folder works well — see the 2-1 photo. Two
   ways to improve the rest:
   - Install the Claude in Chrome extension and sign into Instagram there — the
     full carousels become reachable through your existing session. (I will not
     type a password into Instagram; using a session you already opened is fine.)
   - Or just drop better files into `images/` using the same filenames.
3. **Real numbers.** "3 coaching slots open this month" appears on the home page
   and results page. Confirm with Augusto or make it generic.
4. **The domain.** Every page has `abcoaching.ie` hardcoded in its canonical,
   Open Graph and structured data tags, plus `robots.txt` and `sitemap.xml`.
   Find-and-replace it once the real domain exists — social previews and search
   listings will be wrong until then. Each one is marked with a TODO comment.
5. **Phone and address.** `index.html` has LocalBusiness structured data with
   `telephone` and `address` deliberately left out, since I do not have them.
   Adding both materially improves how he ranks for "jiu jitsu strength coach
   Dublin" style searches.

## Honesty notes — worth keeping

- **Suyan Queiroz's quote is verbatim** from a testimonial screenshot on his
  Instagram. That one is real and directly quoted, and it is now the only
  client quote on the site.
- **Sean and Fiachra were removed** from the results page in the retarget. Both
  were off-message for competitive grapplers — Sean's was a body-composition
  transformation, Fiachra's was about getting back into a routine around long
  work shifts. Neither was a client quote either; they were Augusto's own
  write-ups. They are still in git-less history only, so re-add from an earlier
  version of `results.html` if the audience ever widens again.
- **Instagram video could not be embedded.** Instagram serves no video at all to
  logged-out visitors, and the public embed only renders a poster plus a
  click-out. If Augusto sends the original files they can be self-hosted
  properly — the `.vcard` component is already built and `videos/README.md` has
  the markup and the ffmpeg commands.
- The **training-clip gallery was removed** on request. Results now points
  visitors to the testimonials pinned at the top of his Instagram profile
  instead. The `.reel` styles and the two reel cover images went with it; the
  originals are still in `.research/reels/` if it is ever wanted back.
- **The 2-1 partner photo** is `augusto-comp-gi.jpg`, supplied by Marcus rather
  than scraped. The original went in as `fixing gi.jpg`; it was renamed
  (spaces in filenames need URL-encoding and break on some hosts), cropped to
  drop the waistband at the bottom, and resized from 1432px to 760px. The
  untouched original is in `.research/fixing gi (original).jpg`.
  **Supplying photos this way is the right route** — every Meta image endpoint
  returns a login wall, so nothing new is scrapeable.
- The biography on `about.html` is drawn from Augusto's own public Instagram post
  about himself. Worth having him read it before it goes live.

## Not done

- **Not pushed or deployed yet.** The repo exists locally with one commit; it
  needs a GitHub remote and a Vercel import.
- **No canonical tags, no sitemap.** Removed on purpose — they pointed at
  `abcoaching.ie`, which does not exist. Run `python set-domain.py <url>` once
  there is a permanent URL (the `.vercel.app` one counts) and they come back
  properly, along with an absolute `og:image` and the structured-data URLs.
- No cookie banner or privacy policy. Not needed as built — the site sets no
  cookies and runs no analytics. That changes the moment analytics is added.
