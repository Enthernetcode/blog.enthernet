from pathlib import Path
import re

from linkedin_postprocess import LINKEDIN_POSTS, PENDING_DAYS

ROOT = Path(__file__).parent
ARCHIVE = ROOT / "dist" / "100-days" / "index.html"


def _replace_card_status(html: str, day: int, confirmed: bool) -> str:
    # Each archive card begins with an anchor whose data-search starts with "day N ...".
    # Limit the substitution to that card so we never promote another day's badge by accident.
    card_pattern = re.compile(
        rf'(<a class="archive-item" data-search="day {day}\b.*?</a>)',
        re.DOTALL,
    )
    match = card_pattern.search(html)
    if not match:
        raise RuntimeError(f"Day {day}: archive card not found")

    card = match.group(1)
    if confirmed:
        card = re.sub(
            r'<span class="status(?: warn)?">(?:Topic confirmed · archive artifact pending|Published journey entry|Published artifact recovered|LinkedIn artifact confirmed)</span>',
            '<span class="status">LinkedIn artifact confirmed</span>',
            card,
            count=1,
        )
    else:
        card = re.sub(
            r'<span class="status(?: warn)?">.*?</span>',
            '<span class="status warn">LinkedIn artifact pending</span>',
            card,
            count=1,
        )

    return html[:match.start()] + card + html[match.end():]


def main() -> None:
    if not ARCHIVE.exists():
        raise SystemExit("dist/100-days/index.html not found")

    html = ARCHIVE.read_text(encoding="utf-8")

    # The archive introduction used to describe recovered early AWS posts as still pending.
    html = re.sub(
        r'<p class="lead">Days 1–\d+ are represented in chronological order\..*?</p>',
        '<p class="lead">Published days are represented in chronological order. Recovered original LinkedIn posts are marked as confirmed provenance; only days whose genuine permalink is still missing remain explicitly pending.</p>',
        html,
        count=1,
        flags=re.DOTALL,
    )

    for day in sorted(LINKEDIN_POSTS):
        # Only touch cards that are actually present in the current generated archive.
        if re.search(rf'data-search="day {day}\b', html):
            html = _replace_card_status(html, day, confirmed=True)

    for day in sorted(PENDING_DAYS):
        if re.search(rf'data-search="day {day}\b', html):
            html = _replace_card_status(html, day, confirmed=False)

    ARCHIVE.write_text(html, encoding="utf-8")

    # Tripwires for the stale AWS badges that triggered this repair.
    stale_days = {1, 3, 5, 6, 7, 8, 9, 10, 14, 15, 17, 18}
    rendered = ARCHIVE.read_text(encoding="utf-8")
    for day in stale_days:
        card = re.search(rf'<a class="archive-item" data-search="day {day}\b.*?</a>', rendered, re.DOTALL)
        if not card:
            raise SystemExit(f"Day {day}: archive card missing after provenance pass")
        if 'LinkedIn artifact confirmed' not in card.group(0):
            raise SystemExit(f"Day {day}: stale/pending archive badge survived")

    # Day 11 must remain pending until a genuine original permalink is recovered.
    day11 = re.search(r'<a class="archive-item" data-search="day 11\b.*?</a>', rendered, re.DOTALL)
    if day11 and 'LinkedIn artifact pending' not in day11.group(0):
        raise SystemExit("Day 11 must remain LinkedIn artifact pending")

    print("ARCHIVE PROVENANCE PASSED")
    print(" - recovered LinkedIn artifacts promoted on archive cards")
    print(" - stale pending badges removed from Days 1,3,5-10,14,15,17,18")
    print(" - unresolved permalink days remain pending")


if __name__ == "__main__":
    main()
