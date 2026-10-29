import os,re,sys
sys.path.insert(0,'tools')
K=r'(?:reel|reels|p|tv|shorts)/([\w-]+)|youtu\.be/([\w-]+)|[?&]v=([\w-]+)'
c=[]
for l in open('.kos/kopru/ogren/video-yeni-1-kalan.txt'):
    m=re.search(K,l); c.append(next(g for g in m.groups() if g))
v=[x for x in c if os.path.exists(f'docs/video-tarama/derin/{x}.json')]
print('json',len(v),'/',len(c))
