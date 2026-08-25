from pathlib import Path
from html import escape
import json
import re

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
BASE = "https://blog.enthernet.com"
LINKEDIN = "https://www.linkedin.com/in/renuel-roberts-st-enthernet-code-6571a7241"
GITHUB = "https://github.com/Enthernetcode"
PORTFOLIO = "https://Enthernetcode.github.io"
CORE_SHIELD = "https://core-shield.enthernetservice.com"
PINCH_AI = "https://pinchai.enthernetservice.com"
FCS = "https://fcs.enthernet.com"


def url_for(path: Path) -> str:
    rel = path.relative_to(DIST).as_posix()
    if rel == "index.html":
        return BASE + "/"
    if rel.endswith("/index.html"):
        return BASE + "/" + rel[:-10]
    return BASE + "/" + rel


def jsonld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "</script>"


def title_of(html):
    m = re.search(r"<title>(.*?)</title>", html, re.I | re.S)
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else "Enthernet"


def description_of(html):
    m = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', html, re.I)
    return m.group(1).strip() if m else "Enthernet engineering, cloud, cybersecurity, automation and technical research."


def replace_meta(html, name, value, prop=False):
    attr = "property" if prop else "name"
    pattern = rf'<meta\s+{attr}="{re.escape(name)}"\s+content="[^"]*"\s*/?>'
    tag = f'<meta {attr}="{name}" content="{escape(value, quote=True)}">'
    if re.search(pattern, html, re.I):
        return re.sub(pattern, tag, html, count=1, flags=re.I)
    return html.replace("</head>", tag + "</head>", 1)


def ensure_canonical(html, url):
    tag = f'<link rel="canonical" href="{url}">'
    pattern = r'<link\s+rel="canonical"\s+href="[^"]*"\s*/?>'
    if re.search(pattern, html, re.I):
        return re.sub(pattern, tag, html, count=1, flags=re.I)
    return html.replace("</head>", tag + "</head>", 1)


person = {
    "@type": "Person",
    "@id": BASE + "/#renuel-roberts",
    "name": "Renuel Roberts",
    "alternateName": ["Enthernet Code", "Renuel Roberts ST Enthernet Code"],
    "url": BASE + "/about/",
    "sameAs": [LINKEDIN, GITHUB, PORTFOLIO],
    "knowsAbout": ["Cloud computing", "Cybersecurity", "Software engineering", "Automation", "Linux", "Networking", "Docker", "Kubernetes", "CI/CD"]
}
organization = {
    "@type": "Organization",
    "@id": BASE + "/#organization",
    "name": "Enthernet",
    "alternateName": ["Enthernet Code"],
    "url": BASE + "/",
    "description": "Independent software engineering, cloud and cybersecurity initiative documenting technical projects, research and #100DaysOfCloudAndSecurity.",
    "founder": {"@id": BASE + "/#renuel-roberts"},
    "sameAs": [GITHUB, LINKEDIN, CORE_SHIELD, PINCH_AI, FCS]
}
website = {
    "@type": "WebSite",
    "@id": BASE + "/#website",
    "url": BASE + "/",
    "name": "Enthernet",
    "alternateName": "Enthernet Blog",
    "description": "Cloud, cybersecurity, automation, software engineering and technical research by Enthernet.",
    "publisher": {"@id": BASE + "/#organization"},
    "inLanguage": "en"
}

for path in DIST.rglob("*.html"):
    html = path.read_text(encoding="utf-8")
    url = url_for(path)
    title = title_of(html)
    desc = description_of(html)

    # Make the homepage especially explicit while keeping article titles intact.
    if path == DIST / "index.html":
        title = "Enthernet | Cloud, Cybersecurity & Engineering by Renuel Roberts"
        desc = "Enthernet is the engineering and cybersecurity platform of Renuel Roberts, documenting #100DaysOfCloudAndSecurity, cloud infrastructure, DevSecOps, software projects and technical research."
        html = re.sub(r"<title>.*?</title>", f"<title>{escape(title)}</title>", html, count=1, flags=re.I | re.S)
        html = replace_meta(html, "description", desc)

        identity = '''<section class="section"><div class="shell"><div class="section-head"><div><span class="eyebrow">About Enthernet</span><h2>Engineering, security and research built in public.</h2><p>Enthernet is an independent software engineering, cloud and cybersecurity initiative by Renuel Roberts. It connects the #100DaysOfCloudAndSecurity technical archive with deployed projects including Core-Shield Cyber Labs and Enthernet Pinch AI, plus the Full Cell Sufficiency research record.</p></div></div><div class="actions"><a class="btn btn-secondary" href="/about/">About Renuel &amp; Enthernet →</a><a class="btn btn-secondary" href="/projects/">Explore projects →</a><a class="btn btn-secondary" href="/research/">Research →</a></div></div></section>'''
        if "About Enthernet" not in html:
            html = html.replace("</main>", identity + "</main>", 1)

    html = ensure_canonical(html, url)
    html = replace_meta(html, "og:title", title, prop=True)
    html = replace_meta(html, "og:description", desc, prop=True)
    html = replace_meta(html, "og:url", url, prop=True)
    html = replace_meta(html, "og:site_name", "Enthernet", prop=True)
    html = replace_meta(html, "twitter:title", title)
    html = replace_meta(html, "twitter:description", desc)
    html = replace_meta(html, "twitter:card", "summary_large_image")
    html = replace_meta(html, "robots", "index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1")

    graph = [website, organization, person]
    breadcrumb = {
        "@type": "BreadcrumbList",
        "@id": url + "#breadcrumb",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Enthernet", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": title, "item": url},
        ]
    }
    if url != BASE + "/":
        graph.append(breadcrumb)
    if "/100-days/day-" in url:
        graph.append({
            "@type": "TechArticle",
            "@id": url + "#article",
            "headline": title.replace(" | Enthernet", ""),
            "description": desc,
            "url": url,
            "mainEntityOfPage": url,
            "author": {"@id": BASE + "/#renuel-roberts"},
            "publisher": {"@id": BASE + "/#organization"},
            "isPartOf": {"@id": BASE + "/#website"},
            "inLanguage": "en",
            "about": ["Cloud computing", "Cybersecurity", "Software engineering"]
        })
    graph_tag = jsonld({"@context": "https://schema.org", "@graph": graph})
    if 'id="enthernet-entity-graph"' not in html:
        graph_tag = graph_tag.replace("<script ", '<script id="enthernet-entity-graph" ', 1)
        html = html.replace("</head>", graph_tag + "</head>", 1)

    path.write_text(html, encoding="utf-8")

print("Applied Enthernet entity SEO, self-canonicals, social metadata and structured data to generated HTML")
