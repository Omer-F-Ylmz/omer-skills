import json,re
from pathlib import Path
T=json.load(open('.kos/kopru/ara/dy1_tum.json'))
tum=T['tum']
notlar={}
for l in Path('.kos/kopru/linkler-2026-10-23-omer.tsv').read_text(encoding='utf-8').splitlines()[1:]:
    p=l.split('\t')
    if len(p)>2 and p[2].strip(): notlar[p[0]]=p[2].strip()
CAM=re.compile(r'\b([A-Z][a-z]+[A-Z][A-Za-z0-9]*|[A-Za-z0-9]+(?:-[A-Za-z0-9]+)+|[A-Z][A-Za-z0-9]{2,}(?:\.[a-z]{2,3})?)\b')
STOP=set('The This That What When With From Your Here Just Comment Video Link Follow Share Save Like Instagram YouTube DM AI Claude Code Never Number Step Stop Now And But You'.split())
def isimler(d):
    m=d.get('meta') or {}
    out={}
    for u in d.get('linkler') or []:
        out[re.sub(r'https?://(www\.)?','',str(u))[:50]]='linkler'
    for c in d.get('komutlar') or []:
        out[str(c)[:50]]='komutlar'
    cap=m.get('aciklama') or ''
    for g in re.findall(r'github\.com/[\w.-]+/[\w.-]+',cap): out[g]='meta.aciklama'
    for src,txt in (('meta.aciklama',cap),('ekran',' '.join(x.get('t','') for x in d.get('ekran') or [])),('transkript',' '.join(x.get('t','') for x in d.get('transkript') or []))):
        from collections import Counter
        c=Counter(w for w in CAM.findall(txt) if w not in STOP and len(w)>3 and not w.isdigit() and re.search('[A-Za-z]{4}',w) and src!='transkript')
        for w,n in c.items():
            if w not in out and n>=(1 if src=='meta.aciklama' else 3): out[w]=src
    return out
sat=[];toplam=0;ok=0;ad=set();hata=[]
sil=set(T['sil'])
for k,u in tum.items():
    toplam+=1
    f=Path(f'docs/video-tarama/derin/{k}.json')
    if not f.exists(): hata.append(k); sat.append(f'- {k} {u}\n  HATA/yok: derin json yok\n'); continue
    d=json.loads(f.read_text(encoding='utf-8')); ok+=1
    m=d.get('meta') or {}
    tr=' '.join(x.get('t','') for x in d.get('transkript') or [])
    cap=(m.get('aciklama') or '').replace('\n',' ')
    ozet=(tr[:230] or cap[:230] or ' '.join(x.get('t','') for x in (d.get('ekran') or [])[:25])[:230]).strip()
    nm=isimler(d); ad.update(nm)
    nl=', '.join(f'{a} ({b})' for a,b in list(nm.items())[:8]) or 'çıkmadı'
    n=f'  NOT: {notlar[k]}\n' if k in notlar else ''
    sat.append(f'- {k} [{m.get("yukleyen","?")}, {int(m.get("sure") or 0)}sn, kare {d.get("kare_sayisi")}] {u}\n{n}  Gösteriyor: {ozet}\n  Araç/repo: {nl}\n')
bas=f'# DERİN-YENİ-1 (23 Eki)\ntoplam {toplam} · ok {ok} · silinmiş {len(sil)} · hata {len(hata)} · ad {len(ad)}\nAPKLAB-SS = github.com/APKLab/APKLab (VS Code APK eklentisi; video değil, kurulum listesine).\nAd çıkarımı sezgisel (başlık/OCR/komut/link alanları); kanıt alanı parantezde.\n\n'
Path('.kos/kopru/rapor/derin-yeni-1.md').write_text(bas+'\n'.join(sat),encoding='utf-8')
print(toplam,ok,len(sil),len(hata),len(ad))
