$py = "$(uv tool dir)\video-cli\Scripts\python.exe"
$OutputEncoding = [Text.UTF8Encoding]::new($false)  # Python'a boru UTF-8 (BOM'suz); 5.1 varsayılanı ASCII
$env:ELEME_DOC = $PSScriptRoot
if (-not $env:ELEME_ORNEK) { $env:ELEME_ORNEK = "$PSScriptRoot\..\..\.kos\2026-09-30-uzun\form\V0XbuApxlhg.json" }  # V1 örneği (Claude formu)
if (-not $env:ELEME_ORNEK21) { $env:ELEME_ORNEK21 = "$PSScriptRoot\..\..\.kos\2026-10-03-short\form\vfLtsYbtJf0.json" }  # F3-V2 V21 örneği (yon.ornek_sec)
if (-not $env:ELEME_ORNEK6) { $env:ELEME_ORNEK6 = "$PSScriptRoot\..\..\.kos\2026-09-30-uzun-2\form\Pj2FnVE-W3c.json" }  # F3-V6 V6/V63 örneği (yon.ornek_sec6; 6 liste dolu, doğrulamada kullanılmaz)
@'
import os, sys, time
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
destek = {'openrouter/' + x['id']: x.get('supported_parameters') or [] for x in liste if 'openrouter/' + x.get('id', '') in {a.split('@')[0] for a in adaylar}}
# tek kör Jev partisi; istek tavanı = puanlanacak yanıt sayısı (eleme B'den önce ≤ yon.JEV_TAVAN olduğunu denetler)
puanla = lambda ms: [x['kalite'] for x in c.Tasiyici(env=env, en_fazla=2, istek_tavan=len(ms)).yargila(ms, {'kalite': kur.KALITE_Q})]
# F3-V8 teşhis: ELEME_BOYUT=1 → 5 boyut sorusu ayrı parti (karar yalnız kalite); kayıtta olan boyut yeniden sorulmaz
boyut = (lambda ms: [{k: x[k] for k in kur.BOYUT_Q} for x in c.Tasiyici(env=env, en_fazla=2, istek_tavan=len(ms)).yargila(ms, kur.BOYUT_Q)]) \
    if os.environ.get('ELEME_BOYUT') == '1' else None
g = (pt.SISTEM, '=== VIDEO ' + v + ' ===\n' + p.read_text(encoding='utf-8'), pt.sema([v], iz=True), kareler)
print('kareler', len(kareler), '· adaylar', len(adaylar))
ts, ornek = time.strftime('%Y%m%d-%H%M%S'), Path(os.environ['ELEME_ORNEK']) if os.environ.get('ELEME_ORNEK') else None
# F3-V2 V21 örneği (yon.ornek_sec: OLCUM listeleri dolu en kısa Claude formu, b2QkhmQ0sT0 hariç; doğrulamada kullanılmaz)
ornek21 = Path(os.environ['ELEME_ORNEK21']) if os.environ.get('ELEME_ORNEK21') else None
ornek6 = Path(os.environ['ELEME_ORNEK6']) if os.environ.get('ELEME_ORNEK6') else None
print('varyantlar:', ' · '.join(f'{k} {d}' for k, d in yon.VARYANT.items()), '· V1 örneği', ornek, '· V21 örneği', ornek21)
s = yon.eleme(g, adaylar, hafif.cagir, hafif.MODEL, env, puanla, onbellek=p.parent.parent / 'ab', destek=destek, ornek=ornek, ornek21=ornek21, ornek6=ornek6, boyut=boyut,
             kayit=Path(os.environ['ELEME_YENIDEN']) if os.environ.get('ELEME_YENIDEN') else p.parent.parent / 'eleme' / ts,
             yeniden=Path(os.environ['ELEME_YENIDEN']) if os.environ.get('ELEME_YENIDEN') else None)  # yeniden: B çağrısı 0, kayıttan puanla
for r in (s.get('rapor') or {}).values():  # F3-V8: dolu alan + boyut satırı rapora (konsol + md)
    r['olcum'] = [*(r.get('olcum') or ()), *[x for x in (r.get('dolu'), (r.get('boyut') or {}).get('satir')) if x]]
for r in s['satirlar']:
    print(r)
print(s['oneri'])
print(f"toplam: A ${s['a_usd']:.4f} · B ${s['b_usd']:.4f} · Jev ≤{s.get('jev_istek', 4)} istek (usd ölçülmüyor)")
for ad, r in (s.get('rapor') or {}).items():
    print(ad, '·', r['ozet'])
    for x in r.get('olcum', ()):
        print('  ', x)
if s.get('rapor') and os.environ.get('ELEME_DOC'):
    md = Path(os.environ['ELEME_DOC']) / f'eleme-{ts}.md'
    md.write_text(f'# eleme {ts} · {v}\n\nvaryantlar: ' + ' · '.join(f'{k} {d}' for k, d in yon.VARYANT.items()) + f' · V1 örneği {ornek}\n\n' + '\n'.join(s['satirlar']) + '\n\n' + s['oneri'] + '\n' + ''.join(f"\n## {ad}\n\n{r['ozet']}\n\n" + ''.join(f'- {x}\n' for x in r.get('olcum', ())) + "\n| alan | A | B | fark % |\n|---|---|---|---|\n" + '\n'.join(r['satirlar']) + '\n' for ad, r in s['rapor'].items()), encoding='utf-8')
    print('rapor:', md)
'@ | & $py -
