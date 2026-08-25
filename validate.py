from pathlib import Path
from html import escape as html_escape
from html.parser import HTMLParser
import subprocess
import sys

from content.aws import AWS_DAYS, UNVERIFIED_AWS
from content.ansible import ANSIBLE_DAYS
from content.linux_networking import LINUX_NETWORKING_DAYS
from content.docker import DOCKER_DAYS
from content.kubernetes import KUBERNETES_DAYS
from content.cicd import CICD_DAYS

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
ART_DIR = DIST / "assets" / "day-art"

SOURCES = (AWS_DAYS, ANSIBLE_DAYS, LINUX_NETWORKING_DAYS, DOCKER_DAYS, KUBERNETES_DAYS, CICD_DAYS)
DAYS = {}
for source in SOURCES:
    overlap = set(DAYS).intersection(source)
    if overlap:
        raise SystemExit(f"Duplicate day definitions: {sorted(overlap)}")
    DAYS.update(source)

EXPECTED = set(range(1, 84))
actual = set(DAYS)
if actual != EXPECTED:
    missing = sorted(EXPECTED - actual)
    extra = sorted(actual - EXPECTED)
    raise SystemExit(f"Day coverage mismatch. missing={missing} extra={extra}")

REQUIRED = {
    "title", "phase", "status", "summary", "architecture", "how",
    "commands", "verify", "gotcha", "security", "lesson", "evidence"
}
PLACEHOLDER_PATTERNS = (
    "topic pending archive verification",
    "todo",
    "tbd",
    "lorem ipsum",
    "this day focused on",
)

errors = []
seen_titles = set()
for day in range(1, 84):
    data = DAYS[day]
    missing = REQUIRED - set(data)
    if missing:
        errors.append(f"Day {day}: missing fields {sorted(missing)}")
        continue

    title = str(data["title"]).strip()
    if not title:
        errors.append(f"Day {day}: blank title")
    if title in seen_titles:
        errors.append(f"Day {day}: duplicate title {title!r}")
    seen_titles.add(title)

    if not isinstance(data["how"], list) or len(data["how"]) < 3:
        errors.append(f"Day {day}: 'how' must contain at least 3 explanatory paragraphs")

    for key in ("summary", "architecture", "commands", "verify", "gotcha", "security", "lesson", "evidence"):
        value = str(data[key]).strip()
        if not value:
            errors.append(f"Day {day}: blank {key}")
        low = value.lower()
        for marker in PLACEHOLDER_PATTERNS:
            if marker in low:
                errors.append(f"Day {day}: placeholder-like text in {key}: {marker!r}")

    if len(str(data["summary"]).strip()) < 70:
        errors.append(f"Day {day}: summary is too thin")
    if len(str(data["gotcha"]).strip()) < 45:
        errors.append(f"Day {day}: gotcha is too thin")

if set(UNVERIFIED_AWS) != {1, 3, 5, 6, 7, 8, 9, 10, 14, 15, 17, 18}:
    errors.append("AWS archive-pending register changed unexpectedly")

if errors:
    print("CONTENT VALIDATION FAILED")
    for err in errors:
        print(" -", err)
    raise SystemExit(1)

# Build the deployable artifact, then generate/attach the 83 repo-native visual assets.
subprocess.run([sys.executable, str(ROOT / "generate.py")], check=True)
subprocess.run([sys.executable, str(ROOT / "generate_day_art.py")], check=True)

if not DIST.exists():
    raise SystemExit("Generator did not create dist/")

pages = sorted((DIST / "100-days").glob("day-*/index.html"))
if len(pages) != 83:
    raise SystemExit(f"Expected 83 generated day pages, found {len(pages)}")

art = sorted(ART_DIR.glob("day-*.svg"))
if len(art) != 83:
    raise SystemExit(f"Expected 83 Pic-of-the-Day SVGs, found {len(art)}")

for day in range(1, 84):
    expected_art = ART_DIR / f"day-{day:03d}.svg"
    if not expected_art.exists():
        raise SystemExit(f"Missing Pic-of-the-Day asset for Day {day}")
    svg = expected_art.read_text(encoding="utf-8")
    expected_title = f'<title id="title">Day {day}: {html_escape(DAYS[day]["title"])}</title>'
    if expected_title not in svg:
        raise SystemExit(f"Day {day} visual is not tied to the correct topic")

all_html = "\n".join(p.read_text(encoding="utf-8") for p in DIST.rglob("*.html"))
if "Topic pending archive verification" in all_html:
    raise SystemExit("Old placeholder title leaked into generated HTML")
if "queued for the visual pass" in all_html:
    raise SystemExit("Old Pic-of-the-Day placeholder leaked into generated HTML")

for day in range(1, 84):
    marker = f"/assets/day-art/day-{day:03d}.svg"
    if marker not in all_html:
        raise SystemExit(f"Rendered HTML does not reference Day {day} visual")

for required_link in (
    "https://core-shield.enthernetservice.com",
    "https://pinchai.enthernetservice.com",
    "https://fcs.enthernet.com",
):
    if required_link not in all_html:
        raise SystemExit(f"Required live project link missing: {required_link}")

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key == "href" and value:
                self.links.append(value)


def internal_target(href: str):
    href = href.split("#", 1)[0].split("?", 1)[0]
    if not href or not href.startswith("/") or href.startswith("//"):
        return None
    if href == "/":
        return DIST / "index.html"
    path = DIST / href.lstrip("/")
    if href.endswith("/"):
        return path / "index.html"
    return path

broken = []
for html_file in DIST.rglob("*.html"):
    parser = LinkParser()
    parser.feed(html_file.read_text(encoding="utf-8"))
    for href in parser.links:
        target = internal_target(href)
        if target is not None and not target.exists():
            broken.append((html_file.relative_to(DIST).as_posix(), href))

if broken:
    print("BROKEN INTERNAL LINKS")
    for source, href in broken[:50]:
        print(f" - {source} -> {href}")
    raise SystemExit(1)

required_files = [
    DIST / "index.html", DIST / "100-days" / "index.html",
    DIST / "projects" / "index.html", DIST / "articles" / "index.html",
    DIST / "research" / "index.html", DIST / "about" / "index.html",
    DIST / "contact" / "index.html", DIST / "sitemap.xml", DIST / "rss.xml",
    DIST / "robots.txt", DIST / "CNAME", DIST / ".nojekyll"
]
missing = [p.relative_to(DIST).as_posix() for p in required_files if not p.exists()]
if missing:
    raise SystemExit(f"Required generated files missing: {missing}")

print("VALIDATION PASSED")
print(" - 83/83 day records contain required rich-content fields")
print(" - 83/83 day routes generated")
print(" - 83/83 Pic-of-the-Day SVG assets generated and attached")
print(" - no old content or visual placeholders in rendered HTML")
print(" - live project/research links present")
print(" - internal-link check passed")
