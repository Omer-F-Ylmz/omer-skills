"""BUL-KUR-2 adim 2: repo_link'li kurulmamis kalemler icin gh api (arsiv/404/tur/lisans). Cikti tmp/bk2-repo.tsv"""
import csv, os, re, subprocess, json, sys, time
csv.field_size_limit(10**7)
def oku(p, enc="utf-8-sig"):
    return list(csv.DictReader(open(p, encoding=enc, errors="replace"), delimiter="\t")) if os.path.exists(p) else []
ana = oku('docs/video-tarama/ana-liste.tsv')
KUR = {"KURULMADI-SIRADA", "BULUNAMADI-KESIN", "BULUNDU-ADAY", "BULUNAMADI-ARANIYOR"}
rows = [r for r in ana if r['durum'] in KUR and 'github.com/' in r['repo_link']]
CIK = 'tmp/bk2-repo.tsv'
bit = {r['kalem'] for r in oku(CIK, 'utf-8')}
f = open(CIK, 'a', encoding='utf-8', newline='')
w = csv.writer(f, delimiter='\t')
if not bit: w.writerow(['kalem', 'repo', 'durum', 'tur', 'lisans', 'arsiv', 'yildiz', 'aciklama'])
def tur(d, n, topics):
    t = (d + ' ' + n + ' ' + ' '.join(topics)).lower()
    if re.search(r'skill|claude|mcp|plugin|agent', t): return 'SKILL'
    if re.search(r'model|weights|diffusion|llm', t): return 'MODEL'
    if re.search(r'\bcli\b|command|tool', t): return 'CLI'
    if re.search(r'library|package|sdk|framework', t): return 'PAKET'
    return 'CLI'
n = 0
for r in rows:
    k = r['kalem']
    if k in bit: continue
    m = re.search(r'github\.com/([\w.-]+)/([\w.-]+)', r['repo_link'])
    if not m: continue
    rp = f"{m.group(1)}/{m.group(2)}".removesuffix('.git')
    p = subprocess.run(['gh', 'api', f'repos/{rp}'], capture_output=True, text=True, encoding='utf-8')
    if p.returncode != 0:
        d = '404' if '404' in p.stderr else 'HATA'
        w.writerow([k, rp, d, '', '', '', '', p.stderr[:80].replace('\n', ' ')])
    else:
        j = json.loads(p.stdout)
        lic = (j.get('license') or {}).get('spdx_id') or 'YOK'
        w.writerow([k, rp, 'ARSIV' if j['archived'] else 'ERISILEBILIR', tur(j.get('description') or '', j['name'], j.get('topics', [])), lic, j['archived'], j['stargazers_count'], (j.get('description') or '')[:100].replace('\t', ' ')])
    f.flush(); n += 1
    time.sleep(0.3)
print('BITTI', n, '/', len(rows))
