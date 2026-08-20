# Video stories — how to add them

Drop the finished `.mp4` files in this folder and their poster images in
`../images/`. The `.vcard` component is already built and styled in
`styles.css`; nothing else needs writing.

## What to ask Augusto for

Ask for the **original files**, not ones re-downloaded from Instagram —
Instagram re-compresses on upload and again on download, so a saved reel looks
noticeably worse than the source.

| | |
|---|---|
| Format | MP4, H.264 video, AAC audio |
| Orientation | Whatever he shot. Vertical 1080×1920 and landscape 1920×1080 both work |
| Length | Under about 45 seconds each. Attention drops off a cliff past that |
| Audio | Must be audible — testimonials are people talking. Check before publishing |
| Naming | `firstname-topic.mp4`, e.g. `suyan-bjjstars.mp4` |

**Get permission in writing.** A client sending Augusto a nice message in a DM
is not the same as agreeing to appear on a public website. One line by text or
email saying they are happy for it to go on the site is enough, and it protects
him.

## Compressing them

Raw phone video is often 50–150MB, which is far too heavy. Install ffmpeg once:

```bash
winget install Gyan.FFmpeg
```

Then, per video — this targets roughly 2–5MB for a 45-second clip:

```bash
ffmpeg -i raw.mp4 -vf "scale=-2:1080" -c:v libx264 -crf 26 -preset slow -movflags +faststart -c:a aac -b:a 96k suyan-bjjstars.mp4
```

Pull a poster frame from two seconds in:

```bash
ffmpeg -i suyan-bjjstars.mp4 -ss 00:00:02 -frames:v 1 -q:v 3 ../images/suyan-bjjstars-poster.jpg
```

`-movflags +faststart` matters: it moves the index to the front of the file so
playback can begin before the whole thing has downloaded.

## The markup

Paste this into `results.html` wherever the section should go. Wrap two or three
of them in `<div class="vgrid"> … </div>`.

```html
<article class="vcard r">
  <video class="vcard__video"
         controls
         preload="none"
         playsinline
         poster="images/suyan-bjjstars-poster.jpg">
    <source src="videos/suyan-bjjstars.mp4" type="video/mp4">
    <track kind="captions" src="videos/suyan-bjjstars.vtt" srclang="en" label="English">
    Your browser cannot play this video.
    <a href="videos/suyan-bjjstars.mp4">Download it instead.</a>
  </video>
  <div class="vcard__body">
    <p class="vcard__quote">
      A short pull quote from what they say in the clip.
    </p>
    <span class="vcard__name">Suyan Queiroz</span>
    <span class="vcard__meta">BJJ Stars superfight winner</span>
  </div>
</article>
```

For a landscape clip add `vcard--wide`: `<article class="vcard vcard--wide r">`.

### Why it is written this way

- `preload="none"` — **no video data downloads until someone presses play.**
  Only the poster JPEG loads. This is what stops videos slowing the page down,
  and it is why the original "no videos, they make sites slow" concern does not
  apply here.
- `poster` — without one the card is a black rectangle until play is pressed.
- `playsinline` — stops iOS hijacking into fullscreen on tap.
- `controls` — gives play, volume and scrub for free, keyboard accessible, no JS.
- The `<a>` fallback inside `<video>` only shows if the browser cannot play it.

### Captions

The `<track>` line is optional but worth doing — most people scroll social video
on mute, and it is the difference between a deaf visitor getting the testimonial
or not. Write a `.vtt` file next to the video:

```
WEBVTT

00:00:00.000 --> 00:00:04.000
Working with Augusto completely changed how I train.
```

If there are no captions yet, delete the `<track>` line rather than pointing at
a file that does not exist.
