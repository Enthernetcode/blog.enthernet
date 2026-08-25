from pathlib import Path
from html import escape
from datetime import datetime, timezone
import json
import re
import shutil

from content.aws import AWS_DAYS, UNVERIFIED_AWS
from content.ansible import ANSIBLE_DAYS
from content.linux_networking import LINUX_NETWORKING_DAYS
from content.docker import DOCKER_DAYS
from content.kubernetes import KUBERNETES_DAYS
from content.cicd import CICD_DAYS

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
ASSETS = DIST / "assets"
BASE = "https://blog.enthernet.com"

if DIST.exists():
    shutil.rmtree(DIST)
ASSETS.mkdir(parents=True)

SITE = {
    "name": "Enthernet",
    "title": "Enthernet Blog | Cloud, Security, Automation & Systems",
    "description": "Engineering in public: cloud, cybersecurity, automation, Linux, networking, containers, Kubernetes and research backed by real technical work.",
    "github": "https://github.com/Enthernetcode",
    "portfolio": "https://Enthernetcode.github.io",
    "linkedin": "https://www.linkedin.com/in/renuel-roberts-st-enthernet-code-6571a7241",
    "email": "enthernet@enthernetservices.com",
}

DAY_CONTENT = {}
for source in (AWS_DAYS, ANSIBLE_DAYS, LINUX_NETWORKING_DAYS, DOCKER_DAYS, KUBERNETES_DAYS, CICD_DAYS):
    DAY_CONTENT.update(source)

# Titles and phases come from the content modules so one source drives cards, routes and articles.
DAY_TITLES = {day: (data["title"], data["phase"]) for day, data in DAY_CONTENT.items()}

FUTURE = {
    84:"GitHub Actions", 85:"Pipeline Secrets", 86:"Automated Testing & Deploy",
    87:"Prometheus", 88:"Grafana", 89:"Centralized Logging", 90:"Monitoring Dashboard",
    91:"Shared Responsibility", 92:"IAM Best Practices", 93:"Secrets Management",
    94:"GuardDuty & Security Hub", 95:"Incident Response", 96:"Infrastructure Hardening",
    97:"DevSecOps Integration", 98:"Production Three-Tier Infrastructure",
    99:"End-to-End Deploy, Monitoring & Security Review", 100:"Showcase + Lessons Learned"
}

PHASES = [
    ("AWS Networking Foundations", "Days 1–23", "Account, identity, compute, VPC networking, scaling, observability and infrastructure as code."),
    ("Infrastructure Automation", "Days 24–40", "Ansible from first playbooks through variables, roles, failure handling, collections and a LAMP capstone."),
    ("Linux Administration", "Days 41–52", "Filesystem, permissions, identity, processes, services, logs, scheduling, packages and hardening."),
    ("Networking Deep Dive", "Days 53–60", "Transport, DNS, DHCP, HTTP/TLS, reverse proxies, load balancing and layered troubleshooting."),
    ("Docker", "Days 61–70", "Images, containers, storage, networking, Compose, Dockerfiles, security and a multi-container capstone."),
    ("Kubernetes", "Days 71–82", "Control plane, workload controllers, Services, configuration, storage, ingress, Helm and production deployment."),
    ("CI/CD & Observability", "Days 83–90", "Delivery pipelines followed by metrics, dashboards and centralized logging."),
    ("Cloud Security & DevSecOps", "Days 91–97", "Shared responsibility, identity, secrets, detection, incident response and infrastructure hardening."),
    ("Capstone", "Days 98–100", "Integrated infrastructure, delivery, monitoring and security evidence."),
]

PROJECTS = [
    {
        "slug":"core-shield", "name":"Core-Shield Cyber Labs", "kicker":"Cybersecurity Education Platform",
        "summary":"A hands-on cybersecurity learning platform built around Concept over Syntax and Logic over Code.",
        "live":"https://core-shield.enthernetservice.com",
        "details":[
            "Browser-based playground for Python, Node.js, Bash and PHP labs with bounded execution.",
            "Course areas spanning Linux, reverse proxies, Ansible, web scraping and Wi-Fi security.",
            "AI mentor, dashboards and certificate flows designed around understanding rather than button memorization.",
            "Isolation, resource ceilings and untrusted-code execution are product requirements, not optional hardening."
        ]
    },
    {
        "slug":"pinch-ai", "name":"Enthernet Pinch AI", "kicker":"Research Discovery & Evidence",
        "summary":"A research assistant that discovers scholarly sources while preserving metadata and provenance for verification.",
        "live":"https://pinchai.enthernetservice.com",
        "details":[
            "OpenAlex, Crossref and Semantic Scholar integrations.",
            "Normalized source model for DOI, journal, author and open-access metadata.",
            "429/rate-limit handling and polite provider request behavior.",
            "Raw metadata retention and an audit trail so citation-shaped text is not treated as evidence by appearance alone."
        ]
    },
    {
        "slug":"jhc-media", "name":"JHC Media", "kicker":"Live Media Systems Engineering",
        "summary":"A low-strain church production engine concept built around deterministic clocks, GPU paths and explicit backpressure.",
        "live":None,
        "details":[
            "Audio capture clock selected as the Phase 0 master clock.",
            "Preview and Program remain separate operator states.",
            "Zero-copy camera-to-encoder path is a measured Phase 0 requirement, not an assumption.",
            "Backpressure policy must state what gets dropped and who is informed when encoding falls behind."
        ]
    },
    {
        "slug":"automation-systems", "name":"Automation Systems", "kicker":"Queues, Mail & Infrastructure",
        "summary":"Production automation work around mail aggregation, task queues, browser automation and Linux service operations.",
        "live":SITE["github"],
        "details":[
            "Python services with Redis/Celery background workers.",
            "IMAP/SMTP integration, scheduling and failure handling.",
            "Nginx reverse proxy and resource-constrained VPS operations.",
            "Operational focus on retries, idempotence, credentials, queue visibility and recoverability."
        ]
    },
]

RESEARCH = {
    "title":"Full Cell Sufficiency",
    "summary":"An evidence-tracked framework exploring wound healing, cell signaling, mitosis, tissue remodeling, resource sufficiency and controlled regeneration.",
    "live":"https://fcs.enthernet.com",
    "levels":["Established evidence","Supported inference","Hypothesis","Speculation","Open question"],
    "areas":["Wound healing","Cell signaling","Mitosis","Tissue remodeling","Resource sufficiency","Controlled regeneration"]
}

CSS = r'''
:root{--bg:#060b12;--panel:#0d1724;--line:#203149;--text:#f5f8ff;--muted:#94a7bd;--cyan:#6ee7ff;--purple:#a798ff;--green:#65e5aa;--yellow:#ffd56a;--max:1180px;--radius:22px}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:radial-gradient(circle at 85% 5%,rgba(110,231,255,.09),transparent 27%),radial-gradient(circle at 5% 35%,rgba(167,152,255,.07),transparent 24%),var(--bg);color:var(--text);font:16px/1.68 Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}a{color:inherit;text-decoration:none}.shell{width:min(var(--max),calc(100% - 38px));margin:auto}.site-header{position:sticky;top:0;z-index:50;background:rgba(6,11,18,.9);backdrop-filter:blur(15px);border-bottom:1px solid var(--line)}.nav{min-height:70px;display:flex;align-items:center;gap:22px}.brand{font-weight:900;letter-spacing:.13em;margin-right:auto}.nav a:not(.brand){font-size:.92rem;color:#c7d2e2}.nav a:hover,.text-link:hover{color:var(--cyan)}.hero{padding:88px 0 68px}.hero-grid{display:grid;grid-template-columns:minmax(0,1.45fr) minmax(280px,.55fr);gap:36px;align-items:end}.eyebrow,.kicker{color:var(--cyan);text-transform:uppercase;letter-spacing:.1em;font-size:.74rem;font-weight:850}.hero h1,.page-hero h1,.article h1{font-size:clamp(3rem,7.8vw,6.7rem);line-height:.94;letter-spacing:-.055em;margin:.22em 0}.hero-copy,.lead{color:#afbdd0;font-size:1.12rem;max-width:810px}.actions{display:flex;gap:10px;flex-wrap:wrap;margin-top:24px}.btn{display:inline-flex;align-items:center;justify-content:center;padding:12px 17px;border:1px solid #314863;border-radius:12px;font-weight:800}.btn-primary{background:#edf6ff;color:#07101a}.btn-secondary:hover{border-color:var(--cyan)}.stats{display:grid;gap:12px}.stat,.panel,.card,.phase-card,.archive-item,.callout,.status-box{border:1px solid var(--line);background:linear-gradient(145deg,var(--panel),#0a1320);border-radius:var(--radius)}.stat,.card,.phase-card,.archive-item,.panel{padding:22px}.stat strong{display:block;font-size:1.45rem}.stat span,.card p,.phase-card p,.archive-item p,.project-card p,.project-card li{color:var(--muted)}.section{padding:64px 0;border-top:1px solid #122034}.alt{background:rgba(13,23,36,.34)}.section-head{display:flex;justify-content:space-between;align-items:end;gap:22px;margin-bottom:25px}.section-head h2{font-size:clamp(2rem,4.4vw,3.8rem);line-height:1.02;letter-spacing:-.04em;margin:.2em 0}.section-head p{color:var(--muted);max-width:720px}.progress{height:12px;background:#15253a;border-radius:99px;overflow:hidden;margin:14px 0}.progress i{display:block;width:83%;height:100%;background:linear-gradient(90deg,var(--cyan),var(--green))}.grid-2,.grid-3{display:grid;gap:16px}.grid-2{grid-template-columns:repeat(2,minmax(0,1fr))}.grid-3{grid-template-columns:repeat(3,minmax(0,1fr))}.card h3,.phase-card h3,.archive-item h3{margin:.35em 0;font-size:1.35rem}.carousel{display:grid;grid-auto-flow:column;grid-auto-columns:minmax(300px,34%);gap:16px;overflow:auto;padding:4px 0 14px;scroll-snap-type:x mandatory}.carousel .card{scroll-snap-align:start;min-height:290px;display:flex;flex-direction:column}.card .text-link{margin-top:auto}.text-link{color:var(--cyan);font-weight:850}.tag-row{display:flex;flex-wrap:wrap;gap:7px}.tag,.status{display:inline-block;padding:5px 9px;border:1px solid #2d435e;border-radius:999px;color:#b7c6d8;font-size:.76rem}.status{color:var(--green);border-color:rgba(101,229,170,.35)}.status.warn{color:var(--yellow);border-color:rgba(255,213,106,.42)}.page-hero{padding:70px 0 45px}.page-hero h1{max-width:1000px}.search{width:100%;padding:14px 16px;color:white;background:#08111d;border:1px solid #263b56;border-radius:13px;margin:15px 0 24px}.archive-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:13px}.archive-item:hover{border-color:#3b607c;transform:translateY(-1px)}.article-layout{display:grid;grid-template-columns:minmax(0,820px) minmax(220px,1fr);gap:56px;align-items:start}.article{padding:60px 0 80px}.article h1{font-size:clamp(2.8rem,6vw,5.8rem)}.article h2{font-size:1.65rem;margin:44px 0 12px}.article p{color:#c2ccda}.article pre{overflow:auto;background:#03070d;border:1px solid #21334c;border-radius:15px;padding:18px;color:#dcecff;font:14px/1.62 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;white-space:pre-wrap}.callout,.status-box{padding:18px}.callout{border-left:4px solid var(--cyan);color:#d5dfeb}.status-box.warn{border-color:rgba(255,213,106,.45);background:rgba(255,213,106,.05)}.status-box strong{color:var(--yellow)}.toc{position:sticky;top:98px;border-left:1px solid var(--line);padding-left:22px;color:var(--muted);font-size:.88rem}.toc strong{color:white;display:block;margin-bottom:9px}.toc a{display:block;padding:5px 0}.toc a:hover{color:var(--cyan)}.prev-next{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:55px}.prev-next a{border:1px solid var(--line);padding:17px;border-radius:15px}.prev-next a:last-child{text-align:right}.project-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}.project-card{padding:25px;border:1px solid var(--line);background:var(--panel);border-radius:var(--radius)}.project-card h3{font-size:1.55rem;margin:.35em 0}.research-levels{display:flex;flex-wrap:wrap;gap:7px;margin:18px 0}.footer{padding:48px 0;border-top:1px solid var(--line);color:#8193aa}.footer-grid{display:flex;gap:18px;justify-content:space-between;align-items:center}.footer a{color:#aab8c9}.phase-label{color:var(--purple);font-weight:800}.evidence-note{font-size:.9rem;color:#899bb1;border-top:1px solid var(--line);margin-top:36px;padding-top:18px}.empty-art{border:1px dashed #344b65;border-radius:18px;padding:22px;color:#8396ad;margin:24px 0;background:rgba(255,255,255,.015)}
@media(max-width:900px){.hero-grid,.article-layout{grid-template-columns:1fr}.toc{position:static;border-left:0;border-top:1px solid var(--line);padding:20px 0 0}.archive-grid,.grid-3{grid-template-columns:repeat(2,minmax(0,1fr))}.carousel{grid-auto-columns:72%}}
@media(max-width:650px){.shell{width:min(var(--max),calc(100% - 30px))}.nav a:not(.brand){display:none}.hero{padding:55px 0 48px}.grid-2,.grid-3,.archive-grid,.project-grid{grid-template-columns:1fr}.carousel{grid-auto-columns:88%}.section{padding:50px 0}.article{padding-top:38px}.prev-next{grid-template-columns:1fr}.prev-next a:last-child{text-align:left}.footer-grid{align-items:flex-start;flex-direction:column}}
'''

JS = r'''
const q=document.querySelector('[data-search-input]');
if(q){q.addEventListener('input',()=>{const v=q.value.trim().toLowerCase();document.querySelectorAll('[data-search]').forEach(el=>{el.hidden=v && !el.dataset.search.includes(v);});});}
'''

(ASSETS / "styles.css").write_text(CSS, encoding="utf-8")
(ASSETS / "site.js").write_text(JS, encoding="utf-8")


def slugify(value):
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def day_href(day):
    return f"/100-days/day-{day:03d}-{slugify(DAY_TITLES[day][0])}/"


def page_url(path="/"):
    return BASE + ("/" if path == "/" else path)


def nav():
    return f'''<header class="site-header"><nav class="shell nav"><a class="brand" href="/">ENTHERNET</a><a href="/100-days/">100 Days</a><a href="/projects/">Projects</a><a href="/articles/">Notes</a><a href="/research/">Research</a><a href="/about/">About</a><a href="/contact/">Contact</a></nav></header>'''


def footer():
    return f'''<footer class="footer"><div class="shell footer-grid"><span>ENTHERNET · Build it. Verify it. Document the evidence.</span><span><a href="{SITE['github']}">GitHub ↗</a> · <a href="{SITE['linkedin']}">LinkedIn ↗</a></span></div></footer>'''


def layout(title, description, body, canonical="/", article_schema=None):
    schema = f'<script type="application/ld+json">{json.dumps(article_schema)}</script>' if article_schema else ""
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)}</title><meta name="description" content="{escape(description)}"><link rel="canonical" href="{page_url(canonical)}"><meta property="og:title" content="{escape(title)}"><meta property="og:description" content="{escape(description)}"><meta property="og:url" content="{page_url(canonical)}"><meta property="og:type" content="{'article' if article_schema else 'website'}"><meta name="theme-color" content="#060b12"><link rel="stylesheet" href="/assets/styles.css">{schema}</head><body>{nav()}<main>{body}</main>{footer()}<script src="/assets/site.js" defer></script></body></html>'''


def write(relpath, content):
    path = DIST / relpath
    if path.suffix:
        path.parent.mkdir(parents=True, exist_ok=True)
    else:
        path.mkdir(parents=True, exist_ok=True)
        path = path / "index.html"
    path.write_text(content, encoding="utf-8")


def status_label(day):
    data = DAY_CONTENT[day]
    status = data.get("status", "published")
    if day in UNVERIFIED_AWS:
        return '<span class="status warn">Topic confirmed · archive artifact pending</span>'
    labels = {
        "published-artifact":"Published artifact recovered",
        "topic-verified":"Topic verified by artifact",
        "published-after-ledger":"Published after ledger snapshot",
        "published":"Published journey entry",
        "user-confirmed":"Topic confirmed · archive artifact pending",
    }
    return f'<span class="status">{escape(labels.get(status, status))}</span>'


def day_card(day):
    data = DAY_CONTENT[day]
    return f'''<article class="card"><div class="tag-row"><span class="tag">DAY {day:02d}</span><span class="tag">{escape(data['phase'])}</span></div><h3>{escape(data['title'])}</h3><p>{escape(data['summary'])}</p><a class="text-link" href="{day_href(day)}">Read Day {day} →</a></article>'''


# Homepage
latest = "".join(day_card(day) for day in range(83, 73, -1))
project_cards = "".join(
    f'''<article class="project-card"><span class="kicker">{escape(p['kicker'])}</span><h3>{escape(p['name'])}</h3><p>{escape(p['summary'])}</p><div class="actions"><a class="text-link" href="/projects/{p['slug']}/">Case study →</a>{f'<a class="btn btn-secondary" href="{p["live"]}">Live / source ↗</a>' if p['live'] else ''}</div></article>'''
    for p in PROJECTS
)

home = f'''<section class="hero"><div class="shell hero-grid"><div><span class="eyebrow">Day 83 / 100 · Engineering in public</span><h1>Cloud. Security. Automation. Evidence.</h1><p class="hero-copy">A technical notebook, project archive and public engineering record. The short social post tells the story; this site keeps the implementation, failure modes, verification and field knowledge.</p><div class="actions"><a class="btn btn-primary" href="/100-days/">Explore the journey →</a><a class="btn btn-secondary" href="{SITE['github']}">View GitHub ↗</a></div></div><div class="stats"><div class="stat"><strong>83 / 100</strong><span>Journey progress</span></div><div class="stat"><strong>CI/CD</strong><span>Current published phase</span></div><div class="stat"><strong>Evidence first</strong><span>Artifacts outrank reconstruction</span></div></div></div></section>
<section class="section alt"><div class="shell"><div class="section-head"><div><span class="eyebrow">Mission</span><h2>Evidence beats résumé fog.</h2><p>Learn by building, preserve the failures, verify the behavior and leave enough detail for another engineer to reproduce the reasoning.</p></div></div><div class="grid-3"><div class="panel"><h3>Understand the internals</h3><p>Frameworks are useful. Understanding how requests move, how services fail and where trust changes is more durable.</p></div><div class="panel"><h3>Security is architecture</h3><p>Identity, network boundaries, secret handling and privilege are design decisions from the beginning, not a final checkbox.</p></div><div class="panel"><h3>Automation is leverage</h3><p>Repetitive workflows become systems, but only when failure semantics and verification are encoded too.</p></div></div></div></section>
<section class="section"><div class="shell"><div class="section-head"><div><span class="eyebrow">#100DaysOfCloudAndSecurity</span><h2>83 published days in one navigable record.</h2></div><a class="text-link" href="/100-days/">View full archive →</a></div><div class="progress"><i></i></div><p class="lead">Days 1–18 now use the confirmed topic map. The canonical ledger still keeps twelve rows at artifact-pending status until original screenshots, video frames or repository evidence are recovered.</p><div class="carousel">{latest}</div></div></section>
<section class="section alt"><div class="shell"><div class="section-head"><div><span class="eyebrow">Live projects</span><h2>The work should lead somewhere real.</h2><p>Project cards link to case studies and, where deployed, the running systems themselves.</p></div></div><div class="project-grid">{project_cards}</div></div></section>
<section class="section"><div class="shell"><div class="grid-2"><div><span class="eyebrow">Research notebook</span><h2 style="font-size:clamp(2.3rem,5vw,4.4rem);line-height:1.02">Full Cell Sufficiency</h2><p class="hero-copy">{escape(RESEARCH['summary'])}</p><div class="research-levels">{''.join(f'<span class="tag">{escape(x)}</span>' for x in RESEARCH['levels'])}</div><div class="actions"><a class="btn btn-primary" href="/research/full-cell-sufficiency/">Research record</a><a class="btn btn-secondary" href="{RESEARCH['live']}">Live FCS site ↗</a></div></div><div class="panel"><h3>Evidence stays labeled</h3><p>Established biology, supported inference, hypothesis and speculation are deliberately kept separate so an interesting mechanism does not quietly become an established claim.</p><ul>{''.join(f'<li>{escape(x)}</li>' for x in RESEARCH['areas'])}</ul></div></div></div></section>'''
write("index.html", layout(SITE["title"], SITE["description"], home, "/"))


# Journey archive
phase_cards = "".join(f'<article class="phase-card"><span class="phase-label">{escape(days)}</span><h3>{escape(name)}</h3><p>{escape(desc)}</p></article>' for name,days,desc in PHASES)
archive_cards = []
for day in range(83, 0, -1):
    data = DAY_CONTENT[day]
    archive_cards.append(f'''<a class="archive-item" data-search="day {day} {escape(data['title'].lower())} {escape(data['phase'].lower())} {escape(data['summary'].lower())}" href="{day_href(day)}"><div class="tag-row"><span class="tag">DAY {day:02d}</span>{status_label(day)}</div><h3>{escape(data['title'])}</h3><span class="phase-label">{escape(data['phase'])}</span><p>{escape(data['summary'])}</p></a>''')
future_cards = "".join(f'<article class="card"><span class="tag">PLANNED · DAY {day}</span><h3>{escape(title)}</h3><p>Roadmap entry only. It will not be presented as published work until artifact evidence exists.</p></article>' for day,title in FUTURE.items())
archive = f'''<section class="page-hero"><div class="shell"><span class="eyebrow">#100DaysOfCloudAndSecurity</span><h1>100 days. One evidence trail.</h1><p class="lead">Days 1–83 are represented in chronological order. Day topics confirmed by the project artifacts are labeled separately from the early AWS topics confirmed by the user but still awaiting the original archive artifact required by the canonical ledger.</p></div></section><section class="section"><div class="shell"><div class="progress"><i></i></div><p class="lead"><strong>83 of 100 days</strong> · current published phase: CI/CD & Observability.</p></div></section><section class="section alt"><div class="shell"><div class="section-head"><div><span class="eyebrow">Journey phases</span><h2>From cloud foundations to integrated capstones.</h2></div></div><div class="grid-3">{phase_cards}</div></div></section><section class="section"><div class="shell"><div class="section-head"><div><span class="eyebrow">Archive</span><h2>Search the days.</h2><p>Search by day number, phase or technical topic.</p></div></div><input class="search" data-search-input placeholder="Search days, topics, phases…" aria-label="Search journey"><div class="archive-grid">{''.join(archive_cards)}</div></div></section><section class="section alt"><div class="shell"><div class="section-head"><div><span class="eyebrow">Roadmap ahead</span><h2>Days 84–100</h2><p>Planned material is visually separate from published evidence.</p></div></div><div class="grid-3">{future_cards}</div></div></section>'''
write("100-days", layout("100 Days of Cloud & Security | Enthernet", "The permanent evidence-backed archive for #100DaysOfCloudAndSecurity.", archive, "/100-days/"))


# Individual day pages
for day in range(1, 84):
    data = DAY_CONTENT[day]
    title, phase = data["title"], data["phase"]
    prev_link = f'<a href="{day_href(day-1)}">← Day {day-1}<br><strong>{escape(DAY_CONTENT[day-1]["title"])}</strong></a>' if day > 1 else '<a href="/100-days/">← Archive<br><strong>All days</strong></a>'
    next_link = f'<a href="{day_href(day+1)}">Day {day+1} →<br><strong>{escape(DAY_CONTENT[day+1]["title"])}</strong></a>' if day < 83 else '<a href="/100-days/">Roadmap →<br><strong>Days 84–100</strong></a>'

    pending = ""
    if day in UNVERIFIED_AWS:
        pending = f'''<div class="status-box warn"><strong>Archive artifact still required.</strong><p>{escape(UNVERIFIED_AWS[day])}</p><p>The topic is now confirmed by the project owner, so the technical article is populated. The canonical ledger status is not promoted until the original published artifact is recovered.</p></div>'''

    how_html = "".join(f"<p>{escape(p)}</p>" for p in data["how"])
    command_html = f'<h2 id="hands-on">Hands-on reference</h2><pre>{escape(data["commands"])}</pre>' if data.get("commands") else ""
    sections = f'''{pending}<p class="lead">{escape(data['summary'])}</p><h2 id="architecture">Architecture / mental model</h2><pre>{escape(data['architecture'])}</pre><h2 id="how">How it works</h2>{how_html}{command_html}<h2 id="verify">Verification</h2><p>{escape(data['verify'])}</p><h2 id="gotcha">Field note / gotcha</h2><div class="callout">{escape(data['gotcha'])}</div><h2 id="security">Security considerations</h2><p>{escape(data['security'])}</p><h2 id="learned">What I learned</h2><p>{escape(data['lesson'])}</p><div class="empty-art"><strong>Pic of the Day:</strong> queued for the visual pass after the written archive is complete. No image is being generated ahead of the article.</div><p class="evidence-note"><strong>Evidence note:</strong> {escape(data['evidence'])} The blog expands the technical explanation; it does not claim every paragraph is verbatim from the original social post.</p>'''
    description = data["summary"]
    schema = {"@context":"https://schema.org","@type":"Article","headline":title,"description":description,"mainEntityOfPage":page_url(day_href(day)),"author":{"@type":"Person","name":"Enthernet"}}
    body = f'''<section><div class="shell article-layout"><article class="article"><span class="eyebrow">Day {day:02d} of 100 · {escape(phase)}</span><h1>{escape(title)}</h1><div class="tag-row"><span class="tag">#100DaysOfCloudAndSecurity</span><span class="tag">{escape(phase)}</span>{status_label(day)}</div>{sections}<div class="prev-next">{prev_link}{next_link}</div></article><aside class="toc"><strong>On this page</strong><a href="#architecture">Architecture</a><a href="#how">How it works</a><a href="#hands-on">Hands-on</a><a href="#verify">Verification</a><a href="#gotcha">Field note</a><a href="#security">Security</a><a href="#learned">What I learned</a><hr style="border:0;border-top:1px solid var(--line);margin:17px 0"><a href="/100-days/">← Journey archive</a></aside></div></section>'''
    write(day_href(day).strip("/"), layout(f"Day {day}: {title} | Enthernet", description, body, day_href(day), schema))


# Projects
project_index_cards = "".join(f'''<article class="project-card"><span class="kicker">{escape(p['kicker'])}</span><h3>{escape(p['name'])}</h3><p>{escape(p['summary'])}</p><div class="actions"><a class="text-link" href="/projects/{p['slug']}/">Open case study →</a>{f'<a class="btn btn-secondary" href="{p["live"]}">Live / source ↗</a>' if p['live'] else ''}</div></article>''' for p in PROJECTS)
projects_body = f'''<section class="page-hero"><div class="shell"><span class="eyebrow">Projects</span><h1>Systems built to answer real questions.</h1><p class="lead">Each case study records the problem, constraints and engineering decisions, then points to a live system or source when one exists.</p></div></section><section class="section"><div class="shell"><div class="project-grid">{project_index_cards}</div></div></section>'''
write("projects", layout("Projects | Enthernet", "Engineering case studies from Enthernet.", projects_body, "/projects/"))
for p in PROJECTS:
    live = f'<a class="btn btn-primary" href="{p["live"]}">Open live project / source ↗</a>' if p["live"] else ""
    details = "".join(f"<li>{escape(x)}</li>" for x in p["details"])
    body = f'''<section class="page-hero"><div class="shell"><span class="eyebrow">{escape(p['kicker'])}</span><h1>{escape(p['name'])}</h1><p class="lead">{escape(p['summary'])}</p><div class="actions">{live}<a class="btn btn-secondary" href="/projects/">All projects</a></div></div></section><section class="section"><div class="shell grid-2"><div class="panel"><h3>Current engineering record</h3><ul>{details}</ul></div><div class="panel"><h3>Case-study standard</h3><p>Architecture, constraints, failure modes, security decisions and verifiable evidence belong here as the project evolves. A live URL is linked when the system actually exists.</p></div></div></section>'''
    write(f"projects/{p['slug']}", layout(f"{p['name']} | Enthernet", p["summary"], body, f"/projects/{p['slug']}/"))


# Engineering notes
notes = [
    ("ConfigMap subPath mounts do not refresh", "Kubernetes", "Normal projected ConfigMap files can update eventually; a subPath mount does not receive those automatic updates."),
    ("Readiness and liveness answer different questions", "Kubernetes", "Readiness decides traffic eligibility. Liveness decides whether the container should be restarted."),
    ("Container IPs are implementation detail", "Docker", "User-defined Docker networks provide DNS-based names. Hard-coded container IPs turn normal replacement into an outage."),
    ("Every listening port needs an owner", "Linux Security", "Service inventory comes before firewall confidence. Know what is listening and why."),
    ("Troubleshooting needs an order", "Networking", "DNS → route → transport → TLS → proxy → backend → disk is a more useful sequence than random command roulette."),
    ("Rollback can still be failure", "Ansible", "A successful rescue path can leave a play green unless the deployment failure is deliberately re-raised."),
    ("NACLs are stateless", "AWS", "Security Groups track connection state; NACL design must account for both directions and ephemeral return traffic."),
    ("CloudTrail and CloudWatch are different evidence", "AWS", "CloudTrail answers who called what AWS API; CloudWatch answers operational questions from metrics, logs and alarms."),
]
notes_html = "".join(f'<article class="card"><span class="tag">{escape(cat)}</span><h3>{escape(title)}</h3><p>{escape(text)}</p></article>' for title,cat,text in notes)
notes_body = f'''<section class="page-hero"><div class="shell"><span class="eyebrow">Engineering Notes</span><h1>The details documentation summaries usually skip.</h1><p class="lead">Small operational traps worth preserving because they are usually learned after something fails.</p></div></section><section class="section"><div class="shell"><div class="grid-3">{notes_html}</div></div></section>'''
write("articles", layout("Engineering Notes | Enthernet", "Field notes from cloud, Linux, networking, Docker and Kubernetes work.", notes_body, "/articles/"))


# Research
research_body = f'''<section class="page-hero"><div class="shell"><span class="eyebrow">Research</span><h1>Separate the evidence from the interesting idea.</h1><p class="lead">Research notes keep established evidence, inference and speculation visibly distinct.</p></div></section><section class="section"><div class="shell"><article class="project-card"><span class="kicker">Research framework</span><h3>{escape(RESEARCH['title'])}</h3><p>{escape(RESEARCH['summary'])}</p><div class="research-levels">{''.join(f'<span class="tag">{escape(x)}</span>' for x in RESEARCH['levels'])}</div><div class="actions"><a class="text-link" href="/research/full-cell-sufficiency/">Open research record →</a><a class="btn btn-secondary" href="{RESEARCH['live']}">Live FCS site ↗</a></div></article></div></section>'''
write("research", layout("Research | Enthernet", RESEARCH["summary"], research_body, "/research/"))
fcs_body = f'''<section class="page-hero"><div class="shell"><span class="eyebrow">Research framework · Live</span><h1>Full Cell Sufficiency</h1><p class="lead">{escape(RESEARCH['summary'])}</p><div class="actions"><a class="btn btn-primary" href="{RESEARCH['live']}">Open fcs.enthernet.com ↗</a></div></div></section><section class="section"><div class="shell grid-2"><div class="panel"><h3>Research domains</h3><ul>{''.join(f'<li>{escape(x)}</li>' for x in RESEARCH['areas'])}</ul></div><div class="panel"><h3>Evidence discipline</h3><div class="research-levels">{''.join(f'<span class="tag">{escape(x)}</span>' for x in RESEARCH['levels'])}</div><p>The framework is useful only if these categories remain separate. A plausible mechanism is not automatically an established biological result.</p></div></div></section>'''
write("research/full-cell-sufficiency", layout("Full Cell Sufficiency | Enthernet", RESEARCH["summary"], fcs_body, "/research/full-cell-sufficiency/"))


# About + contact
about_body = f'''<section class="page-hero"><div class="shell"><span class="eyebrow">About</span><h1>Infrastructure-first engineering, documented in public.</h1><p class="lead">Software engineer and cybersecurity specialist working across backend systems, Linux infrastructure, cloud, automation, reverse proxies, container networking and defensive architecture.</p></div></section><section class="section"><div class="shell grid-2"><div class="panel"><h3>How I work</h3><p>Build → observe → break → verify → document. The goal is to understand how the layers interact instead of collecting framework names.</p></div><div class="panel"><h3>Why this blog exists</h3><p>Recruiters, collaborators and future me should be able to inspect evidence: architecture, commands, failures, source code and the reasoning behind a decision.</p><div class="actions"><a class="btn btn-secondary" href="{SITE['portfolio']}">Portfolio ↗</a><a class="btn btn-secondary" href="{SITE['linkedin']}">LinkedIn ↗</a></div></div></div></section>'''
write("about", layout("About | Enthernet", "About Enthernet and the engineering-in-public mission.", about_body, "/about/"))
contact_body = f'''<section class="page-hero"><div class="shell"><span class="eyebrow">Contact</span><h1>Find the work where it lives.</h1><p class="lead">For software, infrastructure, cloud, security, automation or research conversations, use the public project channels below.</p><div class="actions"><a class="btn btn-primary" href="mailto:{SITE['email']}">Email</a><a class="btn btn-secondary" href="{SITE['github']}">GitHub ↗</a><a class="btn btn-secondary" href="{SITE['linkedin']}">LinkedIn ↗</a><a class="btn btn-secondary" href="https://core-shield.enthernetservice.com">Core-Shield ↗</a><a class="btn btn-secondary" href="https://pinchai.enthernetservice.com">Pinch AI ↗</a><a class="btn btn-secondary" href="https://fcs.enthernet.com">FCS ↗</a></div></div></section>'''
write("contact", layout("Contact | Enthernet", "Contact Enthernet and browse live engineering projects.", contact_body, "/contact/"))


# Error, metadata and feeds
write("404.html", layout("Not Found | Enthernet", "Page not found.", '<section class="page-hero"><div class="shell"><span class="eyebrow">404</span><h1>That route escaped.</h1><p class="lead">The page does not exist or moved before it learned change management.</p><a class="btn btn-primary" href="/">Back home</a></div></section>', "/404.html"))
(DIST / "CNAME").write_text("blog.enthernet.com", encoding="utf-8")
(DIST / ".nojekyll").write_text("", encoding="utf-8")
(DIST / "robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: https://blog.enthernet.com/sitemap.xml\n", encoding="utf-8")

urls = ["/", "/100-days/", "/projects/", "/articles/", "/research/", "/research/full-cell-sufficiency/", "/about/", "/contact/"]
urls += [f"/projects/{p['slug']}/" for p in PROJECTS]
urls += [day_href(d) for d in range(1,84)]
sitemap = '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{escape(BASE + u)}</loc></url>" for u in urls) + "</urlset>"
(DIST / "sitemap.xml").write_text(sitemap, encoding="utf-8")

items = []
for day in range(83, max(0,83-20), -1):
    data = DAY_CONTENT[day]
    items.append(f'<item><title>Day {day}: {escape(data["title"])}</title><link>{BASE}{day_href(day)}</link><guid>{BASE}{day_href(day)}</guid><description>{escape(data["summary"])}</description></item>')
rss = f'''<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>Enthernet Blog</title><link>{BASE}</link><description>{escape(SITE['description'])}</description>{''.join(items)}</channel></rss>'''
(DIST / "rss.xml").write_text(rss, encoding="utf-8")

snapshot = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "current_day": 83,
    "day_count": 83,
    "artifact_pending_days": sorted(UNVERIFIED_AWS),
    "projects": PROJECTS,
    "research": RESEARCH,
}
(DIST / "site-data.json").write_text(json.dumps(snapshot, indent=2), encoding="utf-8")

print(f"Generated {len(list(DIST.rglob('*.html')))} HTML pages into {DIST}")
print(f"Detailed day records: {len(DAY_CONTENT)}; AWS topics awaiting original archive artifact: {len(UNVERIFIED_AWS)}")
