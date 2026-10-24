"""KAYNAK-KUTUPHANE-1: kartlar + derin json linklerinden tekil site listesi."""
import json, re, glob, os, sys
from urllib.parse import urlparse
siteler = {}
for f in glob.glob('docs/site-inceleme/kart/*.md'):
    t = open(f, encoding='utf8').read(1500)
    m = re.search(r'^site:\s*(\S+)', t, re.M); tur = re.search(r'^tur:\s*(.+)', t, re.M)
    if m:
        h = urlparse(m.group(1)).netloc.lower().removeprefix('www.')
        siteler.setdefault(h, {'tur': tur.group(1).strip() if tur else '', 'kart': os.path.basename(f), 'video': 0})
skip = re.compile(r'(instagram|facebook|youtube|youtu\.be|tiktok|twitter|x\.com|t\.co|linktr|google|apple|wa\.me|whatsapp|bit\.ly)')
for f in glob.glob('docs/video-tarama/derin/*.json'):
    try: d = json.load(open(f, encoding='utf8'))
    except Exception: continue
    metin = json.dumps([d.get('linkler'), d.get('ekran')], ensure_ascii=False)
    for u in set(re.findall(r'https?://[^\s"\)\]>]+', metin)):
        try: h = urlparse(u).netloc.lower().removeprefix('www.')
        except ValueError: continue
        if not h or skip.search(h): continue
        s = siteler.setdefault(h, {'tur': '', 'kart': '', 'video': 0}); s['video'] += 1
with open('docs/kaynak-kutuphane/url-listesi.tsv', 'w', encoding='utf8') as o:
    o.write('host\ttur\tkart\tvideo_anma\n')
    for h, s in sorted(siteler.items(), key=lambda x: (-x[1]['video'], x[0])):
        o.write(f"{h}\t{s['tur']}\t{s['kart']}\t{s['video']}\n")
print(len(siteler), 'tekil host;', sum(1 for s in siteler.values() if s['kart']), 'kartli')
