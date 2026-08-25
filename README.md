# Enthernet Blog

Static technical hub for https://blog.enthernet.com and the permanent archive for `#100DaysOfCloudAndSecurity`.

## Current state

- Day 1 through Day 83 each have a stable generated route and topic-specific engineering record.
- Days 84–100 are shown as planned roadmap entries, not published work.
- The exact Day 1–18 topic map is populated:
  1. AWS Free Tier & AWS Console
  2. IAM & Least Privilege
  3. EC2
  4. Security Groups
  5. Network ACLs
  6. Amazon VPC
  7. Subnets
  8. Route Tables
  9. Internet Gateway
  10. NAT Gateway
  11. VPC Endpoints
  12. VPC Peering
  13. Transit Gateway
  14. Review + Practical Lab
  15. Elastic Load Balancer
  16. Auto Scaling
  17. CloudWatch
  18. CloudTrail
- Twelve early AWS rows remain marked **archive artifact pending** in the canonical evidence ledger. Their exact topics are confirmed and their blog articles are populated, but ledger verification status is not promoted without original screenshots/video/repository evidence.
- Published history is not silently rewritten; corrections are recorded forward.

## What each Day page contains

Every Day 1–83 record is expected to include:

- topic summary
- architecture / mental model
- at least three explanatory paragraphs
- hands-on commands, YAML or technical reference
- verification procedure
- field gotcha
- security considerations
- lesson learned
- evidence note
- previous/next navigation
- SEO article metadata

## Sections

- Home / mission
- 100 Days archive and latest-day carousel
- Per-day engineering pages
- Projects with live links to Core-Shield Cyber Labs and Enthernet Pinch AI
- Engineering notes
- Research, including Full Cell Sufficiency and the live FCS site
- About
- Contact
- Sitemap, RSS, robots.txt, CNAME and `.nojekyll`

## Content structure

```text
content/
├── aws.py
├── ansible.py
├── linux_networking.py
├── docker.py
├── kubernetes.py
└── cicd.py
```

`generate.py` renders the site from these evidence-aware content modules into `dist/`.

## Build and validation

Run the full publication gate locally with:

```bash
python3 validate.py
```

The validator checks:

- all 83 day records exist exactly once
- required rich-content fields exist and are non-empty
- explanatory sections are not thin placeholders
- all 83 generated day routes exist
- old placeholder titles do not leak into rendered HTML
- Core-Shield, Pinch AI and FCS live links are present
- internal links resolve
- required generated metadata/files exist

`validate.py` runs `generate.py` itself after the content checks, so the artifact it validates is the same `dist/` directory GitHub Pages uploads.

## GitHub Pages

`.github/workflows/pages.yml` runs `python3 validate.py` on every push to `main`. Deployment only continues if the validation gate passes, then `dist/` is uploaded with GitHub Pages.

Repository Pages source is configured for **GitHub Actions**. The custom domain is `blog.enthernet.com`, and the generated site includes a matching `CNAME` file.

## Evidence policy

Published artifacts outrank reconstructions. The canonical roadmap/ledger remains the verification record. Where a topic is known but the original historical artifact has not yet been recovered, the blog carries a clearly labeled technical reconstruction while the ledger remains artifact-pending.

## Visual pass

Pic-of-the-Day assets remain intentionally separate from the written archive. They should be generated only after the technical content for a day is settled, then linked to that day's page and social/carousel workflow.
