#!/usr/bin/env python3
"""Builds the God-Mode SEO pack from src/ into three installable shapes:

  skills/<name>/SKILL.md                 21 standalone skills (Claude Code, npx skills add, any Agent Skills client)
  .claude-plugin/{plugin,marketplace}.json   the same 21 skills as a Claude Code plugin
  dist/god-mode-seo.zip                  ONE skill for Claude.ai (a router + 21 playbooks), uploaded once

Run: python3 build.py   (no dependencies)
"""
import json, re, shutil, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / 'src'
RULES = (SRC / 'rules.md').read_text().strip()
DEPTS = ['Analysis', 'Optimization', 'Content', 'Diagnostics', 'Strategy']


def parse():
    text = (SRC / 'skills.md').read_text()
    out = []
    for block in re.split(r'^=== ', text, flags=re.M)[1:]:
        head, rest = block.split('\n', 1)
        name, dept, job = [p.strip() for p in head.split('|')]
        m = re.match(r'description:\s*(.+?)\n---\n', rest, flags=re.S)
        assert m, name
        desc = m.group(1).strip()
        body = rest[m.end():].strip()
        assert len(desc) <= 1024, (name, len(desc))
        assert dept in DEPTS, (name, dept)
        assert '—' not in body + desc, f'em dash in {name}'
        out.append({'name': name, 'dept': dept, 'job': job, 'desc': desc, 'body': body})
    assert len(out) == 21, len(out)
    return out


def fm(name, desc):
    return f'---\nname: {name}\ndescription: {json.dumps(desc)}\n---\n\n'


def menu(skills, link=None):
    rows = ['| # | Skill | Department | What it does |', '|---|---|---|---|']
    for i, s in enumerate(skills, 1):
        nm = f'[`{s["name"]}`]({link.format(**s)})' if link else f'`{s["name"]}`'
        rows.append(f'| {i:02d} | {nm} | {s["dept"]} | {s["job"]} |')
    return '\n'.join(rows)


def build():
    skills = parse()
    # 1. standalone skills
    sk = ROOT / 'skills'
    if sk.exists():
        shutil.rmtree(sk)
    for s in skills:
        d = sk / s['name']
        d.mkdir(parents=True)
        (d / 'SKILL.md').write_text(fm(s['name'], s['desc']) + s['body'] + '\n\n' + RULES + '\n')
    # 2. Claude Code plugin manifests (skills/ is discovered automatically)
    cp = ROOT / '.claude-plugin'
    cp.mkdir(exist_ok=True)
    meta = {'name': 'god-mode-seo', 'version': '1.0.0',
            'description': '21 SEO skills in 5 departments, all reading the same live data through the Distribb SEO connector: Search Console, keyword volumes, backlinks and AI citations.',
            'author': {'name': 'Distribb', 'url': 'https://distribb.io'}, 'homepage': 'https://distribb.io', 
            'keywords': ['seo', 'search-console', 'claude-skills', 'distribb'], 'icon': '.claude-plugin/icon.png'}
    (cp / 'plugin.json').write_text(json.dumps(meta, indent=2) + '\n')
    (cp / 'marketplace.json').write_text(json.dumps({
        'name': 'god-mode-seo', 'description': 'God-Mode SEO by Distribb: 21 Claude SEO skills that run on the Distribb SEO connector.', 'owner': {'name': 'Distribb', 'url': 'https://distribb.io'},
        'plugins': [{'name': 'god-mode-seo', 'source': './', 'description': meta['description'], 'version': meta['version']}],
    }, indent=2) + '\n')
    # 3. one Claude.ai skill: a router + the 21 playbooks as references
    names = ', '.join(s['name'] for s in skills)
    rdesc = ('God-Mode SEO: 21 SEO skills in 5 departments (Analysis, Optimization, Content, Diagnostics, Strategy) that all read '
             'the same live data through the Distribb SEO connector. Use when the user types god-mode, or any of these skill names '
             f'with or without a slash: {names}; or asks for one of those jobs (why clicks dropped, keyword ideas, title rewrites, '
             'internal links, schema, content gaps, cannibalization, robots.txt, indexing, AI citations, an SEO roadmap, a weekly SEO report).')
    assert len(rdesc) <= 1024, len(rdesc)
    router = fm('god-mode-seo', rdesc) + f"""# God-Mode SEO

21 skills, one job each, all reading the same live data through the Distribb SEO connector.

## How to run a skill
When the user types a skill name below (with or without a slash), or asks for its job, read `references/<name>.md`
and follow it step by step. When they type "god-mode" or ask what you can do, show this menu and ask which to run.
If a request spans several skills, run them in the order a strategist would (diagnose before you fix) and say which you are running.

{menu(skills)}

{RULES}
"""
    stage = ROOT / 'build' / 'god-mode-seo'
    if stage.parent.exists():
        shutil.rmtree(stage.parent)
    (stage / 'references').mkdir(parents=True)
    (stage / 'SKILL.md').write_text(router)
    for s in skills:
        (stage / 'references' / f'{s["name"]}.md').write_text(s['body'] + '\n')
    dist = ROOT / 'dist'
    dist.mkdir(exist_ok=True)
    zp = dist / 'god-mode-seo.zip'
    if zp.exists():
        zp.unlink()
    with zipfile.ZipFile(zp, 'w', zipfile.ZIP_DEFLATED) as z:
        for f in sorted(stage.rglob('*')):
            if f.is_file():
                z.write(f, f.relative_to(stage.parent))
    # README menu
    rd = ROOT / 'README.md'
    txt = rd.read_text()
    txt = re.sub(r'<!-- MENU -->.*<!-- /MENU -->', '<!-- MENU -->\n' + menu(skills, 'skills/{name}/SKILL.md') + '\n<!-- /MENU -->', txt, flags=re.S)
    rd.write_text(txt)
    print(f'{len(skills)} skills -> skills/, plugin manifests, {zp.relative_to(ROOT)} ({zp.stat().st_size // 1024} KB)')


if __name__ == '__main__':
    build()
