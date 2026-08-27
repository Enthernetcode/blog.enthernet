from pathlib import Path
import re

ROOT = Path(__file__).parent
DIST = ROOT / "dist"

# Canonical LinkedIn permalinks recovered from the original #100DaysOfCloudAndSecurity posts.
# Day 11 and Day 83 intentionally remain absent until their genuine permalinks are recovered.
LINKEDIN_POSTS = {
    1: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7468061484565127170-lKTz",
    2: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-aws-iam-activity-7468315413525921792-1fLH",
    3: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-aws-ec2-activity-7468797486120357888-xXqh",
    4: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7469158161371865088-OlJt",
    5: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7469454463460757504-K3h2",
    6: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7469909605649809408-2Uxu",
    7: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7470177465353707521-SOUw",
    8: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7470272415873441792-lpDW",
    9: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7470862737422843905-1Bdp",
    10: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7471249788257251328-JwC8",
    12: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7471999540921929728-IXrL",
    13: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7472159371838386176-oyTh",
    14: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7472778636039815169-uSaT",
    15: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7473090080639791106-f21B",
    16: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7473394130304339969-4O-C",
    17: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7473787198304235520-Ps4H",
    18: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7474118132454887424-Mh08",
    19: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7474539326991896577-cYXj",
    20: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7474866077856935937-8F0t",
    21: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7475273728415858688-q_zS",
    22: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7475647544837132289-Mt0A",
    23: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7476024475214499840-FFQ_",
    24: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7476296506833043459-oA6C",
    25: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-ansible-automation-activity-7476631602530533376-9W7x",
    26: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_day-26-activity-7477115656342179840-XicV",
    27: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-ansible-automation-activity-7477386582514241536-xaDc",
    28: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7477757662554923008-zKvG",
    29: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7478140509790806016-GMgT",
    30: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_ansible-modules-activity-7478546652799172608-bC5C",
    31: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7478839378220556288-6v4d",
    32: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_ansible-playbook-activity-7478977604885299200-KvRn",
    33: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_variables-in-real-projects-activity-7479318322057048064-HR7G",
    34: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7479881054044971008-HE3P",
    35: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7480371572273340418-USyx",
    36: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7480629280289230850-Id_H",
    37: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7480991556217364480-EBVu",
    38: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7481381038061948930-uB3Q",
    39: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7481640906857611264-aiI-",
    40: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7482275231898796032-8egH",
    41: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7482504796139094017-D_Sm",
    42: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7482731086301671426-YJEK",
    43: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7483103616300417024-bvI7",
    44: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7483411469137702912-6OP0",
    45: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7483794973818142720-yEjx",
    46: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7484293114329825280-I85S",
    47: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7484581526899236865-pBdn",
    48: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7484891818732498944-pOlA",
    49: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-linux-ssh-activity-7485328786117439488-rBHv",
    50: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-linux-bash-activity-7485619640426115072-nJJj",
    51: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-linux-networking-activity-7485955145021730816-Bx0h",
    52: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7486338505439285248-FRAw",
    53: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-cloudsecurity-cybersecurity-activity-7486652416306704384-aWVP",
    54: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-dns-networking-activity-7487120357263437825-osat",
    55: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-cloudsecurity-cybersecurity-activity-7487384876237807616-yFJI",
    56: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-cloudsecurity-cybersecurity-activity-7487754840111042560-eo7B",
    57: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7488136924847763456-8eB4",
    58: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7488499296334589952-uKq-",
    59: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7488872641202823169-Jfww",
    60: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-still-networktroubleshooting-activity-7489257872875315200-Zout",
    61: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7489739946233204736-UyQO",
    62: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7489938556052803584-PRgH",
    63: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7490310231697211392-I-rh",
    64: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7490676498262188032-Xq2v",
    65: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-docker-dockervolumes-activity-7491035300119482368-C339",
    66: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7491412267050266624-6ZA0",
    67: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-docker-dockercompose-activity-7491761405189251073-6zRG",
    68: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-docker-dockerfile-activity-7492442887406743552-ZG_F",
    69: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7492526515235209216-Y19A",
    70: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7492880486206259200--Olo",
    71: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7493342028714508289-fsa4",
    72: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7493896728299970560-bEz3",
    73: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-kubernetes-replicaset-activity-7493975830902149121-GJuV",
    74: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7494381290096599041-susG",
    75: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-kubernetes-cloudsecurity-activity-7494867311128973312-XUCB",
    76: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-kubernetes-cloudsecurity-activity-7495233492012851201-F8dD",
    77: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-kubernetes-configmaps-activity-7495383343727874048-eB8c",
    78: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7495794585990938624-p1A-",
    79: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7496104323513360385-rYs2",
    80: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-kubernetes-k8s-activity-7496426904774873088-M8aM",
    81: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-kubernetes-helm-activity-7496893869754712064-3vGo",
    82: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7497260130955116544-YaaL",
    84: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-100daysofcloudandsecurity-activity-7497947969829249024-F4go",
    85: "https://www.linkedin.com/posts/renuel-roberts-st-enthernet-code-6571a7241_100daysofcloudandsecurity-coreshieldcyberlabs-activity-7498341146872659968-yiLU",
}

PENDING_DAYS = {11, 83}


def _artifact_block(day: int, url: str) -> str:
    return (
        '<div class="callout" data-linkedin-artifact="confirmed">'
        '<strong>Original publication recovered.</strong> '
        f'<a class="text-link" href="{url}" target="_blank" rel="noopener noreferrer">'
        f'View the original Day {day} LinkedIn post ↗</a>'
        '</div>'
    )


def _upgrade_page(path: Path, day: int, url: str) -> None:
    html = path.read_text(encoding="utf-8")

    # Do not duplicate the provenance block if this pass is run more than once.
    if 'data-linkedin-artifact="confirmed"' in html:
        return

    # Promote stale archive-pending badges on days whose original publication is now recovered.
    html = html.replace(
        '<span class="status warn">Topic confirmed · archive artifact pending</span>',
        '<span class="status">LinkedIn artifact confirmed</span>',
    )

    # Remove the old archive-pending warning card. The content generator can keep its historical
    # source wording; this post-process layer reflects the stronger recovered-artifact state.
    html = re.sub(
        r'<div class="status-box warn"><strong>Archive artifact still required\.</strong>.*?</div>',
        '',
        html,
        count=1,
        flags=re.DOTALL,
    )

    confirmed_note = (
        '<p class="evidence-note"><strong>Evidence note:</strong> '
        'The original LinkedIn publication for this day has been recovered and linked above. '
        'This blog entry expands the technical explanation and does not claim every paragraph '
        'is verbatim from the historical social post.</p>'
    )
    html = re.sub(
        r'<p class="evidence-note">.*?</p>',
        confirmed_note,
        html,
        count=1,
        flags=re.DOTALL,
    )

    block = _artifact_block(day, url)
    marker = '<p class="evidence-note">'
    if marker not in html:
        raise RuntimeError(f"Day {day}: evidence-note marker not found in {path}")
    html = html.replace(marker, block + marker, 1)
    path.write_text(html, encoding="utf-8")


def main() -> None:
    day_root = DIST / "100-days"
    if not day_root.exists():
        raise SystemExit("dist/100-days does not exist; run validate.py first")

    upgraded = set()
    for page in sorted(day_root.glob("day-*/index.html")):
        match = re.match(r"day-(\d{3})-", page.parent.name)
        if not match:
            continue
        day = int(match.group(1))
        url = LINKEDIN_POSTS.get(day)
        if not url:
            continue
        _upgrade_page(page, day, url)
        upgraded.add(day)

    missing_pages = sorted(set(LINKEDIN_POSTS) - upgraded)
    if missing_pages:
        raise SystemExit(f"LinkedIn artifact pages not generated: {missing_pages}")

    # Every mapped page must contain its exact permalink after the transformation.
    for day, url in LINKEDIN_POSTS.items():
        matches = list(day_root.glob(f"day-{day:03d}-*/index.html"))
        if len(matches) != 1:
            raise SystemExit(f"Day {day}: expected exactly one generated page, found {len(matches)}")
        rendered = matches[0].read_text(encoding="utf-8")
        if url not in rendered or 'data-linkedin-artifact="confirmed"' not in rendered:
            raise SystemExit(f"Day {day}: LinkedIn provenance was not attached correctly")

    print("LINKEDIN PROVENANCE PASSED")
    print(f" - {len(LINKEDIN_POSTS)} recovered LinkedIn artifacts attached to day pages")
    print(f" - intentionally unresolved days: {sorted(PENDING_DAYS)}")


if __name__ == "__main__":
    main()
