import csv, re, os, glob, collections, subprocess, sys
R = r'C:\Projeler\omer-skills'
K = R + r'\.kos\kopru'
RP = K + r'\rapor'
subprocess.run([sys.executable, '-I', K + r'\video_denetim1_izle.py'], capture_output=True)
subprocess.run([sys.executable, '-I', K + r'\video_denetim1_arac.py'], capture_output=True, env={**os.environ, 'PYTHONIOENCODING': 'utf8'})
iz = [l.rstrip('\n').split('\t') for l in open(RP + r'\_izle.txt', encoding='utf8')]
dd = {}
for l in open(K + r'\ig-42-dedupe.tsv', encoding='utf8'):
    p = l.rstrip('\n').split('\t'); dd[p[0]] = p[2:]
atla = {l.strip() for l in open(K + r'\video-atla.txt')}
toplu2 = ''.join(open(f, encoding='utf8').read() for f in glob.glob(K + r'\ig-toplu2*.txt') + glob.glob(K + r'\ig-toplu2*.log'))
ind = [x for x in iz if x[0] == 'INDIRILEMEDI']
hic = [x for x in iz if x[0] == 'HIC']
sil = [x for x in iz if x[0] == 'SILINEN']
h_atla = [x[1] for x in hic if x[1] in atla]
h_toplu2 = [x[1] for x in hic if x[1] not in atla and x[1] in toplu2]
h_hic = [x[1] for x in hic if x[1] not in atla and x[1] not in toplu2]
rows = list(csv.DictReader(open(RP + r'\_arac.tsv', encoding='utf8'), delimiter='\t'))
c = collections.Counter(r['durum'] for r in rows)
yt_env = len(re.findall(r'^\| [\w-]{11} \|', open(R + r'\docs\video-tarama\00-envanter.md', encoding='utf8').read(), re.M))
yt_md = len([f for f in glob.glob(R + r'\docs\video-tarama\*.md') if re.fullmatch(r'[\w-]{11}\.md', os.path.basename(f))])
o = []
o.append('# VIDEO-DENETIM-1 (23 Eki 2026, salt okuma)\n')
o.append('## 1. Izlenme (liste ig-42-linkler.txt = 738 tekil IG baglantisi)\n')
o.append('| durum | sayi |\n|---|---|')
o.append(f'| derin json var (ok) | {738 - len(ind) - len(hic) - len(sil)} |')
o.append(f'| indirilemedi (log) | {len(ind)} |')
o.append(f'| silinmis post (sayilmaz) | {len(sil)} |')
o.append(f'| derin json yok, video degil/atlandi (video-atla.txt; 43 ISLENMIS=video-764 hattinda islendi, 22 YENI=islenmedi) | {len(h_atla)} |')
o.append(f'| derin json yok, ig-toplu2 hattinda izi var | {len(h_toplu2)} |')
o.append(f'| hic denenmedi (hicbir logda/kayitta yok) | {len(h_hic)} |')
o.append(f'\nYouTube: envanter {yt_env} video, docs/video-tarama/<id>.md rapor {yt_md}.\n')
o.append('### Izlenmeyenler\n')
o.append('Indirilemedi:\n')
for x in ind: o.append(f'- {x[1]} — {re.sub(r"\s+", " ", x[2])[:100]}')
o.append('\nvideo-atla (derin yok): ' + ' '.join(h_atla))
o.append('\n  - bunlardan YENI (islenmedi): ' + ' '.join(c for c in h_atla if dd.get(c, [''])[0] == 'YENI'))
o.append('\nig-toplu2 hattinda: ' + ' '.join(h_toplu2))
o.append('\nHic denenmedi: ' + (' '.join(h_hic) or '-'))
o.append('\nSilinmis (sayilmaz): ' + ' '.join(x[1] for x in sil))
o.append('\n## 2-3. Kurulum\n')
o.append('Kapsam: json linkler/komutlar/ekran(OCR)/kare_aciklama alanlarindan github reposu ve kurulum komutu (npx/npm/pip/uv/brew/winget/git clone/plugin) ile gecen adlar. Yalnizca konusmada gecen (linki/komutu olmayan) adlar kapsam disi. OCR gurultusu: yazim hatali kopya adlar ayri satir olabilir. Kurulu = ad claude plugin list / ~/.claude/skills / plugin cache / MCP config / pip / npm -g / uv tool / winget / PATH ciktisinda tam sozcuk olarak bulundu (kanit satiri). Neden = docs/kurulumlar satir-yerel anahtar sozcuk sezgisi, kesin degil.\n')
o.append(f'Toplam {len(rows)} ad: KURULU {c["KURULU"]} · KURULU DEGIL {c["KURULU DEGIL"]} · BELIRSIZ {c["BELIRSIZ"]}\n')
o.append('| durum | ad | video | tur | kanit | neden |\n|---|---|---|---|---|---|')
for r in rows:
    o.append(f'| {r["durum"]} | {r["ad"]} | {r["video_say"]} | {r["tur"]} | {r["kanit"].replace("|", "/")[:80]} | {r["neden"][:70]} |')
open(RP + r'\video-denetim-1.md', 'w', encoding='utf8').write('\n'.join(o) + '\n')
print(len(ind), len(hic), len(sil), len(h_atla), len(h_toplu2), len(h_hic), yt_env, yt_md, dict(c))
print('ILK15', [r['ad'] for r in rows if r['durum'] == 'KURULU DEGIL'][:15])
