# V1.2 launch checklist

Status: implementation and automated local QA complete. Not yet certified for public launch. Live deployment, browser checks and contact verification remain outstanding.

## Completed

| Area | Result |
|---|---|
| Curation | Sai Swad Dosa selected prominently; Leadership retained in archive; Mad About Markets retained. |
| Content | Earlier names, titles, credits, results and speculative disclosure retained; requested AI tools added. |
| Categories | Experiments hidden from public pages, filters and sitemap. Adidas has one AI record and one homepage gallery. |
| Title clarity | Fixed 14px caption-link override on Print and AI headings. Charcoal on ivory: 12.67:1. Hover/focus: 5.46:1. |
| Design audit | Existing paper palette, type, asymmetry and restrained motion retained. No added gradients, glass, cards, icons, shadows or generic UI patterns. Source review complete; rendered review outstanding. |
| Routes | 18 project routes, 13 films, seven Busy Message screens. All 577 local references resolve across 27 generated HTML files. |
| Preservation | Every retained media asset, source/display field, interaction script, identity data and player/carousel/interlude renderer matches V1.1. |
| Metadata | Unique portfolio/project titles and descriptions; Open Graph/X metadata and image references verified on every generated page. |
| Social image | Portrait-led identity preview added. Project previews use actual posters/artwork. |
| Favicon | Existing identity SVG retained. |
| Crawlability | Sitemap and robots.txt present; removed category absent; public output excludes source/report directories. |
| Images | 70 WebP assets decode; largest is 887,848 bytes. Responsive variants and lazy loading retained; portrait loads eagerly. Artwork not recompressed. |
| Performance | 4,063-byte JavaScript; local system fonts; no dependencies or third-party requests. Videos remain user-played with preload none and posters. No runtime speed score claimed. |
| Accessibility | Existing alt text, image dimensions, keyboard/focus controls, reduced motion, native video controls and manual carousel retained. Metadata contrast strengthened. |
| Secrets | No recognizable keys, credentials or private-key files found in public code or build/content files. No environment files in public output. |
| HTTPS | Public resource paths are relative or HTTPS. No hard-coded HTTP asset request. Actual TLS enforcement is a hosting task. |
| 404 | Matching custom page with Wrong turn. and link back to Selected. |
| Privacy and cookies | No forms, analytics, cookies, third-party embeds, storage or tracking implemented. No cookie banner added. Hosting logs remain outside this source audit. |
| Terms | No transactions, accounts or user submissions. No new standalone Terms page added in this pass. Existing copyright and speculative labels retained. This is a scope decision, not a legal compliance certification. |
| Forms and spam | Not applicable; no form added. |
| Analytics | Intentionally omitted for launch. No credentials required. If introduced later, review data collection and update disclosures first. |
| Closing action | One Say hello link in the closing footer uses the existing main-site destination. Needs destination confirmation below. |
| No dash rule | No em or en dash in public copy or metadata. Original source filenames remain truthful provenance. |

## Required before public launch

1. Publish the complete `dist/` to the intended host, replacing the previous directory instead of merging. Configure directory index routing and `/404.html`, `video/mp4`, and byte-range requests. Do not upload source, reports or repository files as public assets.
2. Add `portfolio.abhinandantejaswi.com` in the host's domain settings. Create the exact DNS record provided there, wait for verification, enable HTTPS, and confirm an HTTP-to-HTTPS redirect. No domain access was available in this task.
3. Confirm the Say hello destination. The existing `https://abhinandantejaswi.com` could not be retrieved or verified. Supply a preferred email or a working contact-page URL, then replace the footer href in `scripts/build.py` and rebuild. Do not assume that the main-site root already provides contact information.
4. Run real browser checks at desktop, tablet, narrow mobile portrait and mobile landscape. Check Print/AI titles at rest, hover, keyboard focus and 200% zoom; navigation wrapping; portrait crop; Index filters; Vodafone arrows, keyboard, swipe, counter and enlargement; Emirates playback; and every film with audio/fullscreen on iOS Safari and Android Chrome. This static build has no compatible managed browser preview here, so these are unverified.
5. Check the published pages return the expected status codes, including a genuine 404 for missing routes. Confirm social-image URLs and all external links on the live domain. No LinkedIn or IMDb URL was supplied or invented.
6. Review the chosen host's request logging and any future integrations before deciding whether a concise privacy disclosure is needed. No analytics account or tracking service has been configured.

## Conditional improvements

- Add approved captions/transcripts for films if available. None were invented in this pass.
- Replace the Hutch watermark-bearing source only if a verified clean master becomes available.

## Verification files

`docs/V1.2-QA.json`, `docs/V1.2-QA.md` and `docs/site-validation.json` record local automated verification. They do not certify live deployment or browser interactions.
