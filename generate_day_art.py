from pathlib import Path
from html import escape
import re
import textwrap

from content import DAY_CONTENT as DAYS, PUBLISHED_DAYS, UNVERIFIED_AWS

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
ART_DIR = DIST / "assets" / "day-art"
BASE = "https://blog.enthernet.com"

PHASE_STYLE = {
    "AWS Networking Foundations": ("#FFB84D", "#33200B"),
    "Infrastructure Automation": ("#A798FF", "#17102E"),
    "Linux Administration": ("#65E5AA", "#0A281D"),
    "Networking Deep Dive": ("#6EE7FF", "#08232A"),
    "Docker": ("#58A6FF", "#0B2038"),
    "Kubernetes": ("#8CA8FF", "#111A3A"),
    "CI/CD & Observability": ("#FF8FD8", "#32142A"),
}


def wrap(text, width, max_lines):
    lines = textwrap.wrap(" ".join(str(text).split()), width=width, break_long_words=False, break_on_hyphens=False)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1].rstrip(" .") + "…"
    return lines


def wrap_architecture(text, width=46, max_lines=7):
    raw = str(text).replace("\t", "  ").splitlines()
    out = []
    for line in raw:
        if not line.strip():
            out.append("")
            continue
        if len(line) <= width:
            out.append(line)
        else:
            indent = len(line) - len(line.lstrip())
            wrapped = textwrap.wrap(line.strip(), width=max(12, width-indent), break_long_words=False, break_on_hyphens=False)
            out.extend((" " * indent + x) for x in wrapped)
        if len(out) >= max_lines:
            break
    if len(out) > max_lines:
        out = out[:max_lines]
    return out


def tspans(lines, x, y, line_height, cls=""):
    attrs = f' class="{cls}"' if cls else ""
    return "".join(f'<text x="{x}" y="{y + i*line_height}"{attrs}>{escape(line)}</text>' for i, line in enumerate(lines))


def slugify(value):
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def svg_for(day, data):
    phase = data["phase"]
    accent, accent_dark = PHASE_STYLE.get(phase, ("#6EE7FF", "#08232A"))
    title_lines = wrap(data["title"], 27, 3)
    summary_lines = wrap(data["summary"], 58, 4)
    lesson_lines = wrap(data["lesson"], 48, 3)
    arch_lines = wrap_architecture(data["architecture"])
    pending = day in UNVERIFIED_AWS
    badge = "TOPIC CONFIRMED · ORIGINAL ARTIFACT PENDING" if pending else "PUBLISHED ENGINEERING RECORD"
    title_y = 232
    summary_y = title_y + len(title_lines)*82 + 28

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900" role="img" aria-labelledby="title desc">
<title id="title">Day {day}: {escape(data['title'])}</title>
<desc id="desc">Pic of the Day for #100DaysOfCloudAndSecurity: {escape(data['summary'])}</desc>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#050A11"/><stop offset="0.58" stop-color="#091522"/><stop offset="1" stop-color="{accent_dark}"/></linearGradient>
  <radialGradient id="glow" cx="78%" cy="16%" r="62%"><stop offset="0" stop-color="{accent}" stop-opacity=".22"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient>
  <filter id="shadow"><feDropShadow dx="0" dy="18" stdDeviation="28" flood-color="#000" flood-opacity=".38"/></filter>
  <style>
    text{{font-family:Inter,Segoe UI,Arial,sans-serif;fill:#F5F8FF}}
    .mono{{font-family:SFMono-Regular,Consolas,Liberation Mono,monospace;fill:#D8E6F6}}
    .muted{{fill:#91A7BD}}
    .accent{{fill:{accent}}}
  </style>
</defs>
<rect width="1600" height="900" fill="url(#bg)"/>
<rect width="1600" height="900" fill="url(#glow)"/>
<path d="M0 724 C260 650 430 782 680 700 S1110 618 1600 690" fill="none" stroke="{accent}" stroke-opacity=".08" stroke-width="2"/>
<path d="M0 770 C310 706 500 830 830 742 S1270 690 1600 742" fill="none" stroke="#6EE7FF" stroke-opacity=".055" stroke-width="2"/>

<g transform="translate(82 66)">
  <text x="0" y="26" font-size="22" font-weight="900" letter-spacing="4">ENTHERNET</text>
  <text x="1420" y="26" text-anchor="end" font-size="18" class="muted" letter-spacing="2">#100DAYSOFCLOUDANDSECURITY</text>
  <line x1="0" y1="58" x2="1436" y2="58" stroke="#263A52"/>
</g>

<g transform="translate(82 150)">
  <rect x="0" y="0" rx="24" width="188" height="54" fill="{accent}" fill-opacity=".13" stroke="{accent}" stroke-opacity=".52"/>
  <text x="94" y="35" text-anchor="middle" font-size="20" font-weight="850" class="accent">DAY {day:02d} / 100</text>
  <text x="218" y="35" font-size="20" font-weight="750" class="muted">{escape(phase.upper())}</text>
</g>

<g transform="translate(82 0)">
  {tspans(title_lines, 0, title_y, 82, 'accent')}
  {tspans(summary_lines, 0, summary_y, 38, 'muted')}
</g>

<g transform="translate(910 164)" filter="url(#shadow)">
  <rect width="606" height="444" rx="28" fill="#09131F" stroke="#28405D"/>
  <text x="34" y="50" font-size="16" font-weight="850" class="accent" letter-spacing="2">ARCHITECTURE / MENTAL MODEL</text>
  <line x1="34" y1="72" x2="572" y2="72" stroke="#243A53"/>
  {tspans(arch_lines, 34, 125, 42, 'mono')}
</g>

<g transform="translate(82 670)">
  <rect width="1434" height="126" rx="24" fill="#0A1522" stroke="#22364D"/>
  <rect width="8" height="126" rx="4" fill="{accent}"/>
  <text x="34" y="36" font-size="15" font-weight="850" class="accent" letter-spacing="2">TAKEAWAY</text>
  {tspans(lesson_lines, 34, 72, 29, '')}
</g>

<g transform="translate(82 832)">
  <text x="0" y="0" font-size="14" class="muted" letter-spacing="1.6">{badge}</text>
  <text x="1434" y="0" text-anchor="end" font-size="14" class="muted">blog.enthernet.com</text>
</g>
</svg>'''


def patch_day_page(day, data):
    slug = f"day-{day:03d}-{slugify(data['title'])}"
    page = DIST / "100-days" / slug / "index.html"
    if not page.exists():
        raise SystemExit(f"Missing generated page for Day {day}: {page}")
    html = page.read_text(encoding="utf-8")
    image_path = f"/assets/day-art/day-{day:03d}.svg"
    image_url = BASE + image_path
    figure = f'''<figure style="margin:34px 0"><img src="{image_path}" alt="Day {day}: {escape(data['title'])} technical visual" width="1600" height="900" loading="lazy" style="display:block;width:100%;height:auto;border:1px solid #203149;border-radius:18px;background:#050A11"><figcaption style="margin-top:10px;color:#8193aa;font-size:.88rem">Pic of the Day · Day {day:02d} · {escape(data['title'])}</figcaption></figure>'''
    old = '<div class="empty-art"><strong>Pic of the Day:</strong> queued for the visual pass after the written archive is complete. No image is being generated ahead of the article.</div>'
    if old not in html:
        raise SystemExit(f"Pic-of-the-Day placeholder not found on Day {day}")
    html = html.replace(old, figure, 1)
    if 'property="og:image"' not in html:
        html = html.replace('</head>', f'<meta property="og:image" content="{image_url}"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{image_url}"></head>', 1)
    page.write_text(html, encoding="utf-8")


def main():
    if set(DAYS) != set(PUBLISHED_DAYS):
        raise SystemExit(f"Day-art generator requires content keys to equal {PUBLISHED_DAYS}")
    ART_DIR.mkdir(parents=True, exist_ok=True)
    for old in ART_DIR.glob("day-*.svg"):
        old.unlink()
    for day in PUBLISHED_DAYS:
        data = DAYS[day]
        (ART_DIR / f"day-{day:03d}.svg").write_text(svg_for(day, data), encoding="utf-8")
        patch_day_page(day, data)
    print(f"Generated and attached {len(PUBLISHED_DAYS)} Pic-of-the-Day SVG assets in {ART_DIR}")


if __name__ == "__main__":
    main()
