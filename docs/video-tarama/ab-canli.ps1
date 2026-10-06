$py = "$(uv tool dir)\video-cli\Scripts\python.exe"
$OutputEncoding = [Text.UTF8Encoding]::new($false)  # Python'a boru UTF-8 (BOM'suz); 5.1 varsayılanı ASCII
@'
import json, os, sys
from pathlib import Path
from jev import cekirdek as c
from video import hafif, kur, parti as pt, yonlendir as yon
eksik = [k for k in ('AB_VIDEO', 'AB_PAKET', 'AB_MODEL') if not os.environ.get(k)]
if eksik:
    sys.exit('hata: eksik ayar: ' + ', '.join(eksik))
m = os.environ['AB_MODEL']
if m.startswith('~') or '/~' in m or ':free' in m or 'openrouter/free' in m:  # O50: takma ad / ücretsiz kol sabit değil → A/B'ye girmez
    sys.exit('hata: kol sabit değil: ' + m)
v, p, tavan = os.environ['AB_VIDEO'], Path(os.environ['AB_PAKET']), int(os.environ.get('AB_TAVAN', '4'))
if not p.is_file():
    sys.exit('hata: paket yok: ' + str(p))
if os.environ['AB_MODEL'] not in yon.FIYAT:
    sys.exit('hata: fiyat yok: ' + os.environ['AB_MODEL'])
env = dict(os.environ)
kareler = [k for k in pt.paket_oku(p)['kareler'] if Path(k).is_file()] if hafif.GORSEL else []  # parti.py:493 ile aynı kural
if hafif.GORSEL and not kareler:
    sys.exit('hata: kare yok')
h = yon.omni_yokla(os.environ['AB_MODEL'], env, gorsel=bool(kareler))
if h:
    sys.exit('hata: ' + h)
t = c.Tasiyici(env=env, en_fazla=2, istek_tavan=4)
puanla = lambda ms: [x['kalite']['score'] for x in t.yargila(ms, {'kalite': kur.KALITE_Q})]
girdi = [(pt.SISTEM, '=== VIDEO ' + v + ' ===\n' + p.read_text(encoding='utf-8'), pt.sema([v], iz=True), kareler)]
print('kareler', len(kareler))
s = yon.ab({'model': hafif.MODEL}, 'tarama', girdi, {'saglayici': 'omniroute', 'model': os.environ['AB_MODEL']},
           hafif.cagir, env, puanla, tekrar=2, tavan=tavan)
print(json.dumps({k: s.get(k) for k in ('karar', 'yonlendirme')}, ensure_ascii=True))
for k in ('a', 'b'):
    if k in s:
        x = s[k]
        print(k, x['model'], *(['kalite', round(x['kalite'], 3), 'basari', x['basari'], 'usd', round(x['maliyet'], 4)] if 'kalite' in x else []),
              *(['ilk_hata', x['ilk_hata']] if x.get('ilk_hata') else []))
'@ | & $py -
