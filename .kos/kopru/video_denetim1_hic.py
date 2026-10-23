import glob, os, collections
R = r'C:\Projeler\omer-skills'
hic = [l.split('\t')[1].strip() for l in open(R + r'\.kos\kopru\rapor\_izle.txt', encoding='utf8') if l.startswith('HIC')]
txt = {}
pats = ['.kos/kopru/*.log', '.kos/kopru/*.tsv', '.kos/kopru/*.txt', '.kos/kopru/*.json', 'docs/video-tarama/*.md', 'docs/video-tarama/raw/**/*', 'docs/video-tarama/altin/**/*', 'docs/kurulumlar/**/*.md', 'docs/**/*.tsv']
for p in pats:
    for f in glob.glob(os.path.join(R, p), recursive=True):
        if os.path.isfile(f) and 'ig-42-linkler' not in f and 'ig-42-kalan' not in f and '_izle' not in f:
            try: txt[f] = open(f, encoding='utf8', errors='replace').read()
            except Exception: pass
found = {c: [f for f, t in txt.items() if c in t] for c in hic}
print(len(hic), 'izi olan', sum(1 for v in found.values() if v))
print(collections.Counter(os.path.basename(f) for v in found.values() for f in v).most_common(8))
for c in hic[:5]: print(c, [os.path.basename(f) for f in found[c]][:3])
