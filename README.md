# Enthernet Blog

Static technical hub for https://blog.enthernet.com and the permanent archive for `#100DaysOfCloudAndSecurity`.

## Current state

- Day 1 through Day 83 each have a stable generated route.
- Days 84–100 are shown as planned roadmap entries, not published work.
- Twelve early AWS rows remain explicitly marked `Topic pending archive verification` because the canonical ledger does not yet have artifact evidence for their exact topics.
- Published history is not silently rewritten; corrections are recorded forward.

## Sections

- Home / mission
- 100 Days archive and latest-day carousel
- Per-day pages
- Projects
- Engineering notes
- Research, including Full Cell Sufficiency
- About
- Contact
- Sitemap, robots.txt, CNAME and `.nojekyll`

## Build

```bash
python3 generate.py
```

The generator writes the deployable static site to `dist/`.

## GitHub Pages

`.github/workflows/pages.yml` builds the site on every push to `main` and deploys `dist/` with GitHub Pages.

Repository Pages source is configured for **GitHub Actions**. The custom domain is `blog.enthernet.com`, and the generated site includes a matching `CNAME` file.

## Evidence policy

The canonical roadmap/ledger outranks AI reconstructions. Missing historical text can be backfilled later without changing stable URLs or pretending uncertain topics were verified.
