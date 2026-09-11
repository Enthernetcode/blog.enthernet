# Enthernet Blog

Static technical hub for https://blog.enthernet.com and the permanent evidence-aware archive for `#100DaysOfCloudAndSecurity`.

## Current state

- **Day 1 through Day 100** have published, topic-specific engineering records and stable generated routes.
- **Day 100** is published as the final showcase: **100 Days Later: From AWS Foundations to Production Security**.
- The completed journey spans AWS foundations, infrastructure as code, Ansible, Linux administration and networking, Docker, Kubernetes, CI/CD, observability, cloud security, DevSecOps automation and production security review.
- Days **86–100** have recovered/confirmed LinkedIn provenance attached during the publication pipeline. Days **93–100** were manually verified against their publication artifacts before mapping their publication links.
- Twelve early AWS rows remain marked **archive artifact pending** in the canonical evidence ledger: Days 1, 3, 5, 6, 7, 8, 9, 10, 14, 15, 17 and 18. Their topics and technical records are populated, but their evidence status is not promoted without original publication evidence.
- Published history is not silently rewritten; corrections and recovered provenance are recorded forward.

## Recent cloud-security sequence

- Day 91 — AWS Shared Responsibility Model
- Day 92 — AWS IAM Best Practices / Least Privilege
- Day 93 — AWS Secrets Management
- Day 94 — Amazon GuardDuty & AWS Security Hub CSPM
- Day 95 — AWS WAF & Shield
- Day 96 — AWS Security Automation with EventBridge & Lambda
- Day 97 — Security Remediation Workflows with Step Functions & Systems Manager
- Day 98 — AWS Organizations & Control Tower
- Day 99 — Production AWS Security Review: Connecting the Controls
- Day 100 — 100 Days Later: From AWS Foundations to Production Security

## What each Day page contains

Every published Day record is expected to include:

- topic summary
- architecture / mental model
- explanatory implementation notes
- hands-on commands, YAML or technical reference
- verification procedure
- field gotcha
- security considerations
- lesson learned
- evidence note
- previous/next navigation
- SEO article metadata
- Pic-of-the-Day asset generated from the registered topic
- LinkedIn provenance where the original publication has been confirmed

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
├── cicd.py
├── observability_security.py
└── day100.py
```

`content/__init__.py` combines the evidence-aware modules and derives `LAST_DAY` from the registered content. `generate.py` renders the deployable site into `dist/`.

## Publication and provenance pipeline

The build separates technical content from recovered social-publication evidence:

1. `validate.py` validates registered day content and generates the deployable archive.
2. `generate_day_art.py` produces topic-linked Pic-of-the-Day SVG assets.
3. `seo_postprocess.py` applies the canonical/entity/SEO layer.
4. LinkedIn provenance post-processors attach confirmed original-publication links and promote archive evidence labels only for mapped artifacts.
5. GitHub Pages uploads the resulting `dist/` artifact only after the validation/deployment workflow succeeds.

This keeps social evidence additive rather than making the technical archive dependent on LinkedIn availability.

## Build and validation

Run the publication gate locally with:

```bash
python3 validate.py
```

The validator derives the expected day count from `PUBLISHED_DAYS`, so it follows the registered journey automatically. It checks:

- every registered Day from 1 through `LAST_DAY` exists exactly once
- required rich-content fields are present and non-empty
- explanatory sections are not thin placeholders
- all expected generated day routes exist
- each published day has its matching Pic-of-the-Day SVG
- old placeholder titles do not leak into rendered HTML
- Core-Shield, Pinch AI and FCS live links are present
- canonical, robots, social and Enthernet entity metadata survive generation
- internal links resolve
- sitemap, RSS, robots.txt, CNAME and other required generated files exist

## GitHub Pages

`.github/workflows/pages.yml` runs the publication pipeline on pushes to `main`. Deployment continues only after validation succeeds, then `dist/` is uploaded through GitHub Pages.

Repository Pages source is configured for **GitHub Actions**. The custom domain is `blog.enthernet.com`, and the generated site includes the matching `CNAME` file.

## Evidence policy

Published artifacts outrank reconstructions. A supplied URL is not assigned to a Day merely because its LinkedIn activity ID appears chronologically correct. Provenance is mapped only when the Day/topic can be confirmed from the publication or its artifact.

Where a historical topic is known but its original artifact has not been recovered, the technical article can remain available while the evidence ledger stays explicitly artifact-pending. This prevents archive completeness from being manufactured by guesswork.

## Day 100

Day 100 completes `#100DaysOfCloudAndSecurity` with the final showcase **100 Days Later: From AWS Foundations to Production Security**. Its successful LinkedIn publication was manually verified from the supplied artifact, and its publication link is attached by the provenance pipeline. The 100-day archive is complete while unresolved historical provenance remains explicitly marked rather than guessed.
