import re,glob,os
K=r'(?:reel|reels|p|tv)/([\w-]+)|youtu\.be/([\w-]{11})|v=([\w-]{11})|shorts/([\w-]{11})'
def kod(s):
    m=re.search(K,s)
    return next((g for g in m.groups() if g),None) if m else None
def kodlar(path):
    out=set()
    for l in open(path,encoding='utf-8',errors='ignore'):
        for u in re.findall(r'https?://\S+',l):
            c=kod(u)
            if c:out.add(c)
    return out
d='.kos/kopru/'
yeni={}
for f in ['linkler-2026-10-29-omer.txt','linkler-2026-10-29-notlu.txt']:
    notu=None
    for l in open(d+f,encoding='utf-8'):
        u=re.search(r'https?://\S+',l)
        if u:
            c=kod(u.group()); 
            if c: yeni.setdefault(c,[u.group(),''])
        elif 'NOT:' in l and c: yeni[c][1]=l.split('NOT:',1)[1].strip()
eski=set()
for f in glob.glob('docs/video-tarama/derin*/*.json'): eski.add(os.path.basename(f)[:-5])
for f in glob.glob('docs/video-tarama/*.md'): eski.add(os.path.basename(f)[:-3])
for f in glob.glob(d+'ogren/video-764*.tsv'): eski|=kodlar(f)
eski|=set(open(d+'video-atla.txt').read().split())
print('tekil',len(yeni),'zaten var',len([c for c in yeni if c in eski]))
kal=[c for c in yeni if c not in eski]
os.makedirs(d+'ogren',exist_ok=True)
open(d+'ogren/video-yeni-1-kalan.txt','w').write('\n'.join(yeni[c][0] for c in kal)+'\n')
open(d+'ogren/video-yeni-1-notlu.tsv','w',encoding='utf-8').write('\n'.join(f"{c}\t{yeni[c][0]}\t{yeni[c][1]}\t{'KALAN' if c in kal else 'ESKI'}" for c in yeni if yeni[c][1])+'\n')
print('kalan',len(kal),'notlu',sum(1 for c in yeni if yeni[c][1]),'notlu kalan',sum(1 for c in kal if yeni[c][1]))
