"""Scaffold the next Markdown day. Counts/routes/navigation derive automatically."""
import argparse,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent; sys.path.insert(0,str(ROOT))
from content.loader import load_days
T='''---\nday: {day}\ntitle: {title}\nphase: {phase}\nstatus: {status}\nartifact_url:\ndate_published:\n---\n\n## Summary\n\nWrite the concise summary.\n\n## Architecture\n\n```text\ncomponent -> component\n```\n\n## How it works\n\nExplain the mechanism, failure mode, and surrounding layer.\n\n## Commands\n\n```bash\n# real commands\n```\n\n## Verification\n\nHow it was proved.\n\n## Gotcha\n\nThe field detail that bites.\n\n## Security\n\nIdentity, exposure, secrets, blast radius.\n\n## Lesson\n\nThe takeaway.\n\n## Evidence\n\nPublished post, repository, screenshot or lab run.\n\n## References\n\n- https://\n'''
def slug(s): return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')
def main():
    p=argparse.ArgumentParser(); p.add_argument('title'); p.add_argument('--phase',required=True); p.add_argument('--day',type=int); p.add_argument('--status',default='published'); a=p.parse_args()
    day=a.day or max(load_days())+1; path=ROOT/'content'/'days'/f'{day:03d}-{slug(a.title)}.md'
    if path.exists(): raise SystemExit(f'already exists: {path}')
    path.write_text(T.format(day=day,title=a.title,phase=a.phase,status=a.status),encoding='utf-8'); print(f'Created {path.relative_to(ROOT)}')
if __name__=='__main__': main()
