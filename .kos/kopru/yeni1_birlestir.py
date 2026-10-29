import glob,re,os,collections
d='.kos/kopru/ogren/yeni1-cikti/'; R='.kos/kopru/rapor/'
kur=open('docs/katalog/yetenek.tsv',encoding='utf-8',errors='ignore').read().lower()+open('docs/envanter/envanter.tsv',encoding='utf-8',errors='ignore').read().lower()
rows=[];S=set()
for f in sorted(glob.glob(d+'env*.tsv')):
    for l in open(f,encoding='utf-8'):
        p=l.rstrip('\n').split('\t')
        if len(p)<3: continue
        p+=['']*(5-len(p)); a=p[1].lower().replace(' (?)','').strip()
        key=(a,p[2])
        if key in S: continue
        S.add(key)
        durum='KURULU' if len(a)>3 and a in kur else 'KURULACAK'
        rows.append([durum]+p[:5])
site=[r for r in rows if r[3].upper().startswith(('SİTE','SITE'))]
h='durum\tkod\tad\ttür\turl/komut\tne işe yarar\n'
open(R+'video-yeni-1-kurulacaklar.tsv','w',encoding='utf-8').write(h+'\n'.join('\t'.join(r) for r in rows if r[0]=='KURULACAK')+'\n')
open(R+'video-yeni-1-siteler.tsv','w',encoding='utf-8').write(h+'\n'.join('\t'.join(r) for r in site)+'\n')
n=''.join(open(f,encoding='utf-8').read()+'\n' for f in sorted(glob.glob(d+'not*.md')))
open(R+'video-yeni-1-notlu.md','w',encoding='utf-8').write('# VIDEO-YENI-1 notlu linkler (Ömer notu → cevap → karar)\n\n'+n)
c=collections.Counter(r[0] for r in rows)
print(len(rows),dict(c),'site',len(site),'notblok',n.count('\n## '),len(glob.glob(d+'env*.tsv')),'env dosyasi')
