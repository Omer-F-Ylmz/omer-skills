$py = "$(uv tool dir)\video-cli\Scripts\python.exe"
@'
import json, os, sys
from pathlib import Path
from jev import cekirdek as c
from video import hafif, kur, parti as pt, yonlendir as yon
eksik = [k for k in ('AB_VIDEO', 'AB_PAKET', 'AB_MODEL') if not os.environ.get(k)]
if eksik:
    sys.exit('hata: eksik ayar: ' + ', '.join(eksik))
v, p, tavan = os.environ['AB_VIDEO'], Path(os.environ['AB_PAKET']), int(os.environ.get('AB_TAVAN', '4'))
if not p.is_file():
    sys.exit('hata: paket yok: ' + str(p))
env = dict(os.environ)
h = yon.omni_yokla(os.environ['AB_MODEL'], env, gorsel=True)
if h:
    sys.exit('hata: ' + h)
kareler = [k for k in pt.paket_oku(p)['kareler'] if Path(k).is_file()] if hafif.GORSEL else []  # parti.py:493 ile aynı kural
t = c.Tasiyici(env=env, en_fazla=2, istek_tavan=4)
puanla = lambda ms: [x['kalite']['score'] for x in t.yargila(ms, {'kalite': kur.KALITE_Q})]
girdi = [(pt.SISTEM, '=== VIDEO ' + v + ' ===\n' + p.read_text(encoding='utf-8'), pt.sema([v], iz=True), kareler)]
print('kareler', len(kareler))
s = yon.ab({'model': hafif.MODEL}, 'tarama', girdi, {'saglayici': 'omniroute', 'model': os.environ['AB_MODEL']},
           hafif.cagir, env, puanla, tekrar=2, tavan=tavan)
print(json.dumps({k: s.get(k) for k in ('karar', 'yonlendirme')}, ensure_ascii=True))
for k in ('a', 'b'):
    if k in s:
        print(k, s[k]['model'], 'kalite', round(s[k]['kalite'], 3), 'basari', s[k]['basari'], 'usd', round(s[k]['maliyet'], 4))
'@ | & $py -
