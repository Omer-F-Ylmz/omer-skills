import glob,re,collections
d='.kos/kopru/ogren/yeni1-cikti/'
rows=[];S=set()
for f in sorted(glob.glob(d+'env*.tsv')):
    for l in open(f,encoding='utf-8'):
        p=l.rstrip('\n').split('\t')
        if len(p)<3: continue
        p+=['']*(5-len(p)); key=(p[1].lower().replace(' (?)','').strip(),p[2])
        if key in S: continue
        S.add(key); rows.append(p[:5])
print(len(rows))
