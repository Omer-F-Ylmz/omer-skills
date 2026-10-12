"""IG-18 birlesik.tsv × IG-40 kararları (d4 + P2 + P3) → devir40.tsv (DEVİR-IG40) + kalan.tsv."""
import csv, re
from pathlib import Path

BU = Path(__file__).parent
WT = Path('C:/Projeler/omer-skills-wt')
oku = lambda p: list(csv.DictReader(open(p, encoding='utf-8'), delimiter='\t'))

karar = {}
for p in ['igkur/.claude/igkur/karar.tsv', 'igkur-p2/.claude/igkur/p2/karar.tsv', 'igkur-p3/.claude/igkur/p3/karar.tsv']:
    for s in oku(WT / p):
        karar[s['sira']] = s
anahtar, repo = {}, {}
for s in oku(WT / 'igkur/.claude/igkur/sirali.tsv'):
    k = karar.get(s['sira'])
    if not k:
        continue
    anahtar.setdefault(s['anahtar'], k)
    if '/' in s['repo']:
        repo.setdefault(s['repo'].lower(), k)


def repo_of(link):
    m = re.search(r'github\.com/([^/\s]+/[^/\s#?]+)', link or '')
    return m.group(1).lower().removesuffix('.git') if m else ''


devir, kalan = [], []
for s in oku(BU / 'birlesik.tsv'):
    k = anahtar.get(s['anahtar']) or repo.get(repo_of(s['link']))
    if k:
        devir.append({**s, 'sira40': k['sira'], 'karar40': k['karar'], 'gerekce40': k['gerekce']})
    else:
        kalan.append({**s, 'repo': repo_of(s['link'])})

for ad, satir in [('devir40.tsv', devir), ('kalan.tsv', kalan)]:
    with open(BU / ad, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(satir[0]), delimiter='\t')
        w.writeheader()
        w.writerows(satir)
print('devir40', len(devir), 'kalan', len(kalan), 'kalan-repo', sum(1 for s in kalan if s['repo']))
