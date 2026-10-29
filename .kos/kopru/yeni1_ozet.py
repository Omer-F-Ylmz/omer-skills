import json,os,re
K=r'(?:reel|reels|p|tv|shorts)/([\w-]+)|youtu\.be/([\w-]+)|[?&]v=([\w-]+)'
kod=[]
for l in open('.kos/kopru/ogren/video-yeni-1-kalan.txt'):
    m=re.search(K,l); kod.append(next(g for g in m.groups() if g))
notlar={}
for l in open('.kos/kopru/ogren/video-yeni-1-notlu.tsv',encoding='utf-8'):
    p=l.rstrip('\n').split('\t'); notlar[p[0]]=p[2]
os.makedirs('.kos/kopru/ogren/yeni1-ozet',exist_ok=True)
ok=[];yok=[]
for c in kod:
    f=f'docs/video-tarama/derin/{c}.json'
    if not os.path.exists(f): yok.append(c); continue
    d=json.load(open(f,encoding='utf-8')); m=d.get('meta') or {}
    tr=' '.join(s['t'] for s in d.get('transkript') or [])[:1800]
    seen=[];S=set()
    for e in d.get('ekran') or []:
        t=e['t'].strip()
        if len(t)>2 and t not in S: S.add(t);seen.append(t)
    ek=' | '.join(seen)[:1800]
    txt=f"# {c}\nNOT: {notlar.get(c,'')}\nurl: {d.get('url')}\nyukleyen: {m.get('yukleyen')} sure: {m.get('sure')}\naciklama: {(m.get('aciklama') or '')[:900]}\nTRANSKRIPT: {tr}\nEKRAN: {ek}\nLINK: {d.get('linkler')}\nKOMUT: {(d.get('komutlar') or [])[:6]}\n"
    open(f'.kos/kopru/ogren/yeni1-ozet/{c}.md','w',encoding='utf-8').write(txt); ok.append(c)
print('ozet',len(ok),'yok',len(yok))
open('.kos/kopru/ogren/video-yeni-1-yok.txt','w').write('\n'.join(yok))
