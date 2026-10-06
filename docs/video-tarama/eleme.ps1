$py = "$(uv tool dir)\video-cli\Scripts\python.exe"
@'
import os, sys
from pathlib import Path
from jev import cekirdek as c
from video import hafif, ikinci_goz as ig, kur, parti as pt, yonlendir as yon
eksik = [k for k in ('AB_PAKET', 'ELEME_ADAYLAR') if not os.environ.get(k)]
if eksik:
    sys.exit('hata: eksik ayar: ' + ', '.join(eksik))
p = Path(os.environ['AB_PAKET'])
if not p.is_file():
    sys.exit('hata: paket yok: ' + str(p))
v, adaylar, env = p.parent.name, [m.strip() for m in os.environ['ELEME_ADAYLAR'].split(',') if m.strip()], dict(os.environ)
kareler = [k for k in pt.paket_oku(p)['kareler'] if Path(k).is_file()] if hafif.GORSEL else []  # parti.py:493 ile aynı kural
if hafif.GORSEL and not kareler:
    sys.exit('hata: kare yok')
# supported_parameters: OpenRouter katalog GET (ücretsiz, anahtarsız; model çağrısı değil)
liste = ig._post('https://openrouter.ai/api/v1/models', None, {})[1].get('data') or []
destek = {'openrouter/' + x['id']: x.get('supported_parameters') or [] for x in liste if 'openrouter/' + x.get('id', '') in adaylar}
t = c.Tasiyici(env=env, en_fazla=2, istek_tavan=4)  # tek kör Jev partisi, ≤ 4 istek
puanla = lambda ms: [x['kalite']['score'] for x in t.yargila(ms, {'kalite': kur.KALITE_Q})]
g = (pt.SISTEM, '=== VIDEO ' + v + ' ===\n' + p.read_text(encoding='utf-8'), pt.sema([v], iz=True), kareler)
print('kareler', len(kareler), '· adaylar', len(adaylar))
s = yon.eleme(g, adaylar, hafif.cagir, hafif.MODEL, env, puanla, onbellek=p.parent.parent / 'ab', destek=destek)
for r in s['satirlar']:
    print(r)
print(s['oneri'])
print(f"toplam: A ${s['a_usd']:.4f} · B ${s['b_usd']:.4f} · Jev ≤4 istek (usd ölçülmüyor)")
'@ | & $py -
