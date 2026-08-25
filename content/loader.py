"""Load one Markdown source file per #100DaysOfCloudAndSecurity day."""
from pathlib import Path
import re
from content.render import render, to_text, word_count, code_lines
DAYS_DIR=Path(__file__).parent/'days'
FILENAME=re.compile(r'^(\d{3})-([a-z0-9-]+)\.md$')
TEXT={'summary':'Summary','evidence':'Evidence'}
CODE={'architecture':'Architecture','commands':'Commands'}
RICH={'how':'How it works','verify':'Verification','gotcha':'Gotcha','security':'Security','lesson':'Lesson','failure':'Failure','pending':'Artifact pending','references':'References'}
REQUIRED=('Summary','Architecture','How it works','Verification','Gotcha','Security','Lesson','Evidence')
VALID={'published-artifact','topic-verified','published-after-ledger','published','user-confirmed'}
class ContentError(Exception): pass
def frontmatter(raw,source):
    if not raw.startswith('---\n'): raise ContentError(f'{source}: missing frontmatter')
    end=raw.find('\n---\n',3)
    if end<0: raise ContentError(f'{source}: unterminated frontmatter')
    meta={}
    for line in raw[4:end].splitlines():
        if line.strip() and not line.lstrip().startswith('#'):
            if ':' not in line: raise ContentError(f'{source}: bad frontmatter line {line!r}')
            k,v=line.split(':',1); meta[k.strip()]=v.strip().strip('"')
    return meta,raw[end+5:]
def sections(body,source):
    out={}; current=None; buf=[]
    for line in body.splitlines():
        if line.startswith('## '):
            if current: out[current]='\n'.join(buf).strip()
            current=line[3:].strip(); buf=[]
        elif current: buf.append(line)
        elif line.strip(): raise ContentError(f"{source}: text before first '## '")
    if current: out[current]='\n'.join(buf).strip()
    return out
def one_fence(md,source,heading):
    m=re.match(r'^```[a-z]*\n(.*?)\n?```$',md.strip(),re.S)
    if not m: raise ContentError(f"{source}: '## {heading}' must contain one fenced block")
    return m.group(1)
def load_day(path):
    m=FILENAME.match(path.name)
    if not m: raise ContentError(f'{path.name}: filename must be NNN-slug.md')
    meta,body=frontmatter(path.read_text(encoding='utf-8'),path.name); sec=sections(body,path.name)
    for key in ('day','title','phase','status'):
        if not meta.get(key): raise ContentError(f'{path.name}: missing {key}')
    missing=[x for x in REQUIRED if not sec.get(x)]
    if missing: raise ContentError(f'{path.name}: missing sections {missing}')
    if meta['status'] not in VALID: raise ContentError(f"{path.name}: bad status {meta['status']}")
    day=int(meta['day'])
    if day!=int(m.group(1)): raise ContentError(f'{path.name}: day mismatch')
    r={'day':day,'slug':m.group(2),'source':path.name,'title':meta['title'],'phase':meta['phase'],'status':meta['status'],'artifact_url':meta.get('artifact_url',''),'date_published':meta.get('date_published','')}
    for k,h in TEXT.items(): r[k]=to_text(sec[h])
    for k,h in CODE.items(): r[k]=one_fence(sec.get(h,''),path.name,h) if sec.get(h) else ''
    for k,h in RICH.items(): r[k]=sec.get(h,''); r[k+'_html']=render(r[k]) if r[k] else ''
    r['body_words']=sum(word_count(sec.get(h,'')) for h in list(TEXT.values())+list(RICH.values()))
    r['code_lines']=code_lines(sec.get('Commands',''))+code_lines(sec.get('How it works',''))
    r['reference_count']=r['references'].count('- ')
    known=set(TEXT.values())|set(CODE.values())|set(RICH.values()); unknown=set(sec)-known
    if unknown: raise ContentError(f'{path.name}: unknown sections {sorted(unknown)}')
    return r
def load_days(directory=DAYS_DIR):
    days={}
    for path in sorted(Path(directory).glob('*.md')):
        r=load_day(path)
        if r['day'] in days: raise ContentError(f"duplicate Day {r['day']}")
        days[r['day']]=r
    if not days: raise ContentError('no day files found')
    gaps=sorted(set(range(1,max(days)+1))-set(days))
    if gaps: raise ContentError(f'gaps in day sequence: {gaps}')
    return days
