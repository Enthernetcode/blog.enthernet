"""Tiny dependency-free Markdown subset renderer for blog prose."""
from html import escape
import re
CODE=re.compile(r'`([^`]+)`'); BOLD=re.compile(r'\*\*(.+?)\*'); LINK=re.compile(r'\[([^\]]+)\]\(([^)\s]+)\)')
def inline(text):
    out=[]
    for i,chunk in enumerate(CODE.split(text)):
        if i%2: out.append(f'<code>{escape(chunk)}</code>'); continue
        safe=escape(chunk); safe=LINK.sub(lambda m:f'<a class="text-link" href="{m.group(2)}">{m.group(1)}</a>',safe); safe=BOLD.sub(r'<strong>\1</strong>',safe); out.append(safe)
    return ''.join(out)
def blocks(md):
    out=[]; buf=[]; fence=None; fl=[]
    def flush():
        if buf: out.append(('p','\n'.join(buf).strip())); buf.clear()
    for line in md.splitlines():
        if fence is not None:
            if line.strip().startswith('```'): out.append(('code','\n'.join(fl))); fence=None; fl=[]
            else: fl.append(line)
            continue
        s=line.strip()
        if s.startswith('```'): flush(); fence=s[3:].strip() or 'text'; fl=[]
        elif not s: flush()
        elif s.startswith('### '): flush(); out.append(('h3',s[4:].strip()))
        elif s.startswith('- '):
            if out and out[-1][0]=='ul' and not buf: out[-1][1].append(s[2:].strip())
            else: flush(); out.append(('ul',[s[2:].strip()]))
        else: buf.append(line.rstrip())
    if fence is not None: out.append(('code','\n'.join(fl)))
    flush(); return out
def render(md):
    out=[]
    for kind,p in blocks(md):
        if kind=='p': out.append(f'<p>{inline(p)}</p>')
        elif kind=='code': out.append(f'<pre>{escape(p)}</pre>')
        elif kind=='h3': out.append(f'<h3>{inline(p)}</h3>')
        elif kind=='ul': out.append('<ul>'+''.join(f'<li>{inline(x)}</li>' for x in p)+'</ul>')
    return ''.join(out)
def to_text(md):
    out=[]
    for kind,p in blocks(md):
        if kind=='code': continue
        out.extend(p if kind=='ul' else [p])
    text=' '.join(out); text=CODE.sub(r'\1',text); text=LINK.sub(r'\1',text); return BOLD.sub(r'\1',text).strip()
def word_count(md): return len(to_text(md).split())
def code_lines(md): return sum(len([x for x in p.splitlines() if x.strip()]) for k,p in blocks(md) if k=='code')
