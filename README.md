# Abhinandan Tejaswi: Creative Folio V1.2

A static-first creative portfolio for portfolio.abhinandantejaswi.com. This project contains creative work only. It does not contain acting or voice reels, products, agents or passion-project sites.

## Run locally

Requires Python 3.10 or newer. No JavaScript packages or installation are needed to run the site.

```sh
cd abhinandan-folio
python3 -m http.server 8000 --directory dist
```

Open http://localhost:8000. This command also works from Windows PowerShell when Python is installed. Do not double-click index.html: root-relative asset paths require a web server.

## Edit and build

Project records live in `content/projects.json`. Identity and landscape records live in `content/identity.json`. Change content, then run:

```sh
python3 scripts/build.py
```

The output is `dist/`, with individually addressable static routes. Styles and progressively enhanced interactions are authored directly in `dist/style.css` and `dist/app.js`; the builder preserves them and the media folder. Commit the complete `dist/` tree. No runtime Python, database, API key or application server is needed.

## Add work

1. Add an image or browser-compatible MP4 to `dist/assets/`. Use H.264 video with AAC audio and fast-start metadata. Keep originals separately.
2. Create a project record in `content/projects.json`, following a matching film, carousel, images or banners record. Keep `slug` unique.
3. Set the actual dimensions and a sensible `recommendedDisplaySize`; do not infer native capture quality from a filename.
4. Add reliable credits to `role`. Set missing years to null. Unknown credits are deliberately omitted from the public page.
5. Add `ai` to `tags` for AI-assisted work. Set `commissionStatus` to `speculative` for self-initiated brand concepts, with an explicit note.
6. Run the builder and validate the new route.

`prepare_assets.py SOURCE_DIR` is an optional reproducible preparation step for the original supplied filenames. It requires Pillow, ffmpeg and ffprobe. It copies/remuxes selected videos, creates WebP presentation images, using the current content records. It never edits originals. It preserves editorial changes, ordering and curated poster frames. Banner captures already packaged in dist are retained.

## Project fields

Records support title, client, year, category, subCategory, role, description, headline, note, heroAsset, assets, video, videoSources, preferredSource, nativeResolution, aspectRatio, poster, featured, priority, projectType, commissionStatus, tags and recommendedDisplaySize. `videoSources` records comparisons without shipping rejected masters. The metadata file documents bitrate, duration, dimensions and hashes for inspected files.

## Deployment

Upload the contents of `dist/` to a static host. Routes have real directories and index.html files, so no SPA catch-all is required. Configure the 404 page as `/404.html` and serve MP4 files with byte-range support and `video/mp4` content type. Keep each asset under the host's file-size limit. The largest current video is below 25 MiB.

The existing Sites identity is in `.openai/hosting.json`. Use that same site for future Sites updates. Do not create a replacement site for ordinary edits.

For the target custom hostname, add `portfolio.abhinandantejaswi.com` through the host's custom-domain settings, then create the exact DNS record supplied by the host. Wait for DNS and TLS verification before announcing the domain as live. The main site and other subdomains are outside this deployment. Metadata and sitemap already use the requested target hostname.

## Before a public launch

- The supplied Prime launch, History TV18 and print roles are included. Other unspecified role credits and years remain omitted.
- Supply the exact preferred email and LinkedIn URL if you want them published. No guessed contact details are included.
- Replace the Hutch source with a clean master if available. Its surviving watermark is disclosed.
- Add any further AI films as separate records. The current AI view presents the supplied AI-assisted Adidas concept.
- Compare any additional files from your Windows folders. That filesystem was not accessible in this workspace; this V1 uses uploaded assets.
- Captions are not newly transcribed. Some source films contain their own on-screen subtitles.
- Verify the site on actual mobile Safari and Android Chrome before broad distribution, including sound and fullscreen.

## Architecture

`build.py` contains reusable rendering functions for navigation, identity hero, film players, archival presentation, editorial cards, screenshot carousel, print/art display, banner sets, landscape interludes, work index, metadata, project notes and About. The output is semantic HTML. `app.js` adds manual carousel navigation, enlargement, filters and exclusive video playback. All project routes and native video controls work without JavaScript; the screenshot rail remains touch-scrollable. Artwork is directly present in HTML.

See `DESIGN-NOTES.md`, `docs/CONTENT-INVENTORY.md`, and `docs/SOURCE-COMPARISON.md` for the decisions behind the presentation.

## V1.1

See `CHANGELOG.md` for the focused content pass and `docs/V1.1-QA.md` for verification. The original appearance, CSS, interaction script, media bytes and display sizing are preserved. The removed print campaign has no route or asset in dist.

## V1.2 launch candidate

See `LAUNCH-CHECKLIST.md` and `docs/V1.2-QA.md` for verified checks and outstanding launch actions. Run:

```sh
python3 scripts/build.py
python3 scripts/validate.py
node --check dist/app.js
python3 scripts/qa_v12.py
```

For media-preservation checks, pass the original V1.1 ZIP as the optional argument to `qa_v12.py`.

Replace the old `dist/` directory on deployment, rather than merging files. This removes the retired category and campaign routes. Source data still accepts future experimental work; public categories are controlled by `PUBLIC_CATEGORIES` in `build.py`. Adidas currently uses category `ai`.

AI production tools live in the optional `aiTools` array and appear only on detail pages. `selectedNote` supports a short contribution/result line. Social metadata uses `dist/og.png` for collection pages and existing artwork/posters for individual projects. The social preview never replaces the actual portrait on the site.

There are no analytics, forms, cookies, third-party player embeds or external font requests in this build. No account integration or cookie banner was added. Hosting request logs and any future tracking need a separate privacy review when the hosting setup is confirmed.

Enforce HTTPS and redirect HTTP at the chosen host. Publish only `dist/`, never content records, scripts, reports or repository files. Keep byte-range support for videos and configure `/404.html`. Verify the existing main-site destination before using it as the live Say hello route, or replace it with your confirmed contact URL/email.
