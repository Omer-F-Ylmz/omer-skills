import json, re, glob, os, collections
R = r'C:\Projeler\omer-skills'
K = R + r'\.kos\kopru'
liste = [l.strip() for l in open(K + r'\ig-42-linkler.txt', encoding='utf8') if l.strip()]
code = lambda u: re.search(r'/(?:p|reel|reels|tv)/([\w-]+)', u).group(1) if re.search(r'/(?:p|reel|reels|tv)/([\w-]+)', u) else u
codes = [code(u) for u in liste]
uniq = list(dict.fromkeys(codes))
sil = set(re.findall(r'\bD[\w-]{10}\b', open(K + r'\ig-silinen.txt', encoding='utf8').read().split('\n', 1)[1]))
derin = {os.path.basename(f)[:-5] for f in glob.glob(R + r'\docs\video-tarama\derin\*.json')}
# log nedenleri
neden = {}
for f in glob.glob(K + r'\derin-toplu*.log'):
    for l in open(f, encoding='utf8', errors='replace'):
        m = re.match(r'^([\w-]{6,})\t(.*)', l)
        if m and 'indirilemedi' in m.group(2):
            neden[m.group(1)] = m.group(2)[:110]
ok = [c for c in uniq if c in derin]
sl = [c for c in uniq if c in sil and c not in derin]
diger = [c for c in uniq if c not in derin and c not in sil]
ind = [c for c in diger if c in neden]
hic = [c for c in diger if c not in neden]
print('liste', len(liste), 'tekil', len(uniq), 'silinen(sayilmaz)', len(sl), 'derin json toplam', len(derin))
print('ok', len(ok), 'indirilemedi', len(ind), 'hic denenmedi', len(hic))
with open(R + r'\.kos\kopru\rapor\_izle.txt', 'w', encoding='utf8') as w:
    for c in ind: w.write(f'INDIRILEMEDI\t{c}\t{neden[c]}\n')
    for c in hic: w.write(f'HIC\t{c}\n')
    for c in sl: w.write(f'SILINEN\t{c}\n')
cnt = collections.Counter(re.sub(r'[\w-]{8,}', '', neden[c])[:60] for c in ind)
for k, v in cnt.most_common(6): print(v, k)
