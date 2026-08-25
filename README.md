# Enthernet Blog

Static technical hub for https://blog.enthernet.com and the permanent archive for `#100DaysOfCloudAndSecurity`.

## Current state

- Day 1 through Day 83 each have a stable generated route and topic-specific engineering record.
- Days 84–100 are shown as planned roadmap entries, not published work.
- The exact Day 1–18 topic map is now populated:
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
- Twelve of those early AWS rows remain marked **archive artifact pending** in the canonical evidence ledger. The topic map is used for the technical blog record, but ledger verification status is not promoted without original screenshots/video/repository evidence.
- Published history is not silently rewritten; corrections are recorded forward.

## Sections

- Home / mission
- 100 Days archive and latest-day carousel
- Per-day engineering pages with architecture, explanation, commands, verification, field gotchas, security notes and lessons learned
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

## Build

```bash
python3 generate.py
```

## GitHub Pages

`.github/workflows/pages.yml` builds the site on every push to `main` and deploys `dist/` with GitHub Pages.

Repository Pages source is configured for **GitHub Actions**. The custom domain is `blog.enthernet.com`, and the generated site includes a matching `CNAME` file.

## Evidence policy

Published artifacts outrank reconstructions. The canonical roadmap/ledger remains the verification record. Where a topic is known but the original historical artifact has not yet been recovered, the blog can carry a clearly labeled technical reconstruction while the ledger remains artifact-pending.

## Visual pass

Pic-of-the-Day assets are intentionally deferred until the written archive is complete and reviewed. No visual should be generated ahead of a day whose technical content is still unsettled.
