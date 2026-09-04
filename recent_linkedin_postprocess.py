from pathlib import Path
import re

ROOT = Path(__file__).parent
DIST = ROOT / "dist"

RECENT_LINKEDIN_POSTS = {
    86: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7498654724901146625-w8NZ",
    87: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7499016171250429952-FHWx",
    88: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7499873208951545857-IHM8",
    89: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7500085013867061248-ihTm",
    90: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7500455503269904385-U1Np",
    91: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7500820915140685826-pw35",
    92: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7501178344462327809-u5zM",
}


def artifact_block(day: int, url: str) -> str:
    return (
        '<div class="callout" data-linkedin-artifact="confirmed">'
        '<strong>Original publication recovered.</strong> '
        f'<a class="text-link" href="{url}" target="_blank" rel="noopener noreferrer">'
        f'View the original Day {day} LinkedIn post ↗</a></div>'
    )


def main() -> None:
    day_root = DIST / "100-days"
    for day, url in RECENT_LINKEDIN_POSTS.items():
        matches = list(day_root.glob(f"day-{day:03d}-*/index.html"))
        if len(matches) != 1:
            raise SystemExit(f"Day {day}: expected exactly one generated page, found {len(matches)}")
        page = matches[0]
        html = page.read_text(encoding="utf-8")
        if url not in html:
            marker = '<p class="evidence-note">'
            if marker not in html:
                raise SystemExit(f"Day {day}: evidence-note marker not found")
            html = html.replace(marker, artifact_block(day, url) + marker, 1)
            page.write_text(html, encoding="utf-8")

    archive = day_root / "index.html"
    html = archive.read_text(encoding="utf-8")
    for day in RECENT_LINKEDIN_POSTS:
        pattern = re.compile(rf'(<a class="archive-item" data-search="day {day}\b.*?</a>)', re.DOTALL)
        match = pattern.search(html)
        if not match:
            raise SystemExit(f"Day {day}: archive card not found")
        card = re.sub(r'<span class="status(?: warn)?">.*?</span>', '<span class="status">LinkedIn artifact confirmed</span>', match.group(1), count=1)
        html = html[:match.start()] + card + html[match.end():]
    archive.write_text(html, encoding="utf-8")

    for day, url in RECENT_LINKEDIN_POSTS.items():
        page = next(day_root.glob(f"day-{day:03d}-*/index.html"))
        if url not in page.read_text(encoding="utf-8"):
            raise SystemExit(f"Day {day}: LinkedIn permalink missing after pass")

    print("RECENT LINKEDIN PROVENANCE PASSED")
    print(" - Days 86-92 linked to their original LinkedIn publications")


if __name__ == "__main__":
    main()
