import json, glob, re, os, collections, shutil
R = r'C:\Projeler\omer-skills'
RP = R + r'\.kos\kopru\rapor'
home = os.path.expanduser('~')
# ---- 1. araç adayları (json: linkler, komutlar, ekran, kare_aciklama)
GH = re.compile(r'github\.com/([A-Za-z0-9][\w.-]{0,38})/([A-Za-z0-9][\w.-]{1,60})', re.I)
INS = re.compile(r'(?:npx|npm\s+(?:i|install)(?:\s+-g)?|pnpm\s+(?:add|dlx)|pip3?\s+install(?:\s+-U)?|uv\s+(?:tool\s+install|pip\s+install)|uvx|brew\s+install|winget\s+install|git\s+clone|claude\s+plugin\s+install|/plugin\s+(?:install|marketplace\s+add))\s+(?:-\S+\s+)*([@\w][\w@./:-]{2,70})', re.I)
cand = collections.defaultdict(lambda: {'vid': set(), 'ham': set(), 'tur': set()})
for f in glob.glob(R + r'\docs\video-tarama\derin\*.json'):
    d = json.load(open(f, encoding='utf8'))
    kod = d.get('kod', os.path.basename(f)[:-5])
    parts = [str(x) for x in d.get('linkler', [])] + [str(x) for x in d.get('komutlar', [])]
    parts += [str(x.get('t', '')) for x in d.get('ekran', []) if isinstance(x, dict)]
    parts.append(str(d.get('kare_aciklama', '')))
    txt = '\n'.join(parts)
    for o, r in GH.findall(txt):
        r = re.sub(r'(\.git)?[.,;:)]*$', '', r)
        if o.lower() in ('github', 'issues', 'topics', 'features', 'sponsors', 'settings', 'orgs', 'marketplace'): continue
        k = r.lower()
        cand[k]['vid'].add(kod); cand[k]['ham'].add(f'{o}/{r}'); cand[k]['tur'].add('repo')
    for m in INS.findall(txt):
        m = re.sub(r'(--\S*|@latest|@lat)$', '', m.strip('.,;:)"\''))
        if m.endswith(('.txt', '.json', '.py', '.md')) or m.startswith('http') or m.startswith('1http'): continue
        if m.lower() in ('install', 'the', 'it', 'and', 'with', 'for', 'to', 'a', 'in', 'on') or m.startswith('http') and 'github' in m: continue
        k = re.sub(r'^.*/', '', m).lower() if m.count('/') == 1 and not m.startswith('@') else m.lower()
        cand[k]['vid'].add(kod); cand[k]['ham'].add(m); cand[k]['tur'].add('komut')
# ---- 2. kurulu saman
hay = []
for g in glob.glob(RP + r'\_inv_*.txt'):
    for l in open(g, encoding='utf8', errors='replace'):
        hay.append((os.path.basename(g), l.strip().lower()))
for base in [home + r'\.claude\skills', home + r'\.claude\agents', R + r'\skills', R + r'\.claude\skills']:
    if os.path.isdir(base):
        for n in os.listdir(base): hay.append((base.replace(home, '~'), n.lower()))
for base in glob.glob(home + r'\.claude\plugins\cache\*\*'):
    hay.append(('plugins/cache', os.path.basename(base).lower()))
    for sub in glob.glob(base + r'\*\skills\*'): hay.append(('plugins/cache skill', os.path.basename(sub).lower()))
for sub in glob.glob(home + r'\.claude\plugins\marketplaces\*'): hay.append(('marketplaces', os.path.basename(sub).lower()))
GEN = {'skills', 'skill', 'claude', 'claude-code', 'code', 'awesome', 'agents', 'mcp', 'plugins', 'tools', 'cli', 'app', 'docs', 'main', 'readme', 'repo', 'project', 'your-repo', 'example', 'my-project', 'ai', 'demo', 'test', 'tree', 'blob', 'issues', 'releases', 'npm', 'pip'}
kdocs = []
for g in glob.glob(R + r'\docs\kurulumlar\**\*.md', recursive=True):
    kdocs.append((g, open(g, encoding='utf8', errors='replace').read().lower()))
def neden(ad):
    t = [(g, x) for g, x in kdocs if ad in x]
    if not t: return 'bilinmiyor (kurulum kaydi yok)'
    x = ' '.join(l for _, b in t for l in b.splitlines() if ad in l)
    if re.search(r'skillspector[^.\n]{0,40}(red|risk|high|critical|fail)|g[uü]vensiz|malicious|zararl', x): return 'guvenlik (docs/kurulumlar: ' + os.path.basename(t[0][0]) + ')'
    if re.search(r'lisans[^.\n]{0,30}(yok|no license|gpl|nc|agpl)|no license|polyform|non-?commercial', x): return 'lisans (docs/kurulumlar: ' + os.path.basename(t[0][0]) + ')'
    if re.search(r'[uü]cretli|paid|abonelik|api key|hesap', x): return 'ucretli/hesap (docs/kurulumlar: ' + os.path.basename(t[0][0]) + ')'
    return 'bilinmiyor (kayit var, red nedeni yok: ' + os.path.basename(t[0][0]) + ')'
rows = []
for k, v in cand.items():
    ad = k.strip('@').split('--')[0].replace('.git', '')
    if len(ad) < 3 or not re.search(r'[a-z]', ad): continue
    rx = re.compile(r'(?<![a-z0-9_-])' + re.escape(ad) + r'(?![a-z0-9_-])')
    ev = next((f'{s}: {l[:90]}' for s, l in hay if rx.search(l)), '')
    which = shutil.which(ad) if v['tur'] == {'komut'} and re.fullmatch(r'[\w.-]+', ad) else None
    if which: ev = ev or f'PATH: {which}'
    if ad in GEN: dur = 'BELIRSIZ'
    elif ev: dur = 'KURULU'
    else: dur = 'KURULU DEGIL'
    rows.append((dur, ad, len(v['vid']), ','.join(sorted(v['tur'])), '|'.join(sorted(v['ham']))[:60], ev, sorted(v['vid'])[:3], neden(ad) if dur == 'KURULU DEGIL' else ''))
rows.sort(key=lambda r: (-r[2], r[1]))
with open(RP + r'\_arac.tsv', 'w', encoding='utf8') as w:
    w.write('durum\tad\tvideo_say\ttur\tham\tkanit\tornek_video\tneden\n')
    for r in rows: w.write('\t'.join(map(str, r)) + '\n')
print(len(rows), collections.Counter(r[0] for r in rows))
