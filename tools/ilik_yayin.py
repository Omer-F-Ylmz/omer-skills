# ILIK-GECE-YAYIN: kuyrukta uretilen (ve elle verilen) GLB'leri siteye al -> build -> commit -> push -> Vercel READY -> canli URL 200.
# Kullanim: python tools/ilik_yayin.py [--glb N=yol:puan ...] [--dry]
# Kural: puani sitedeki surumden YUKSEK olan urun VitrinCanvas GLB haritasina girer; dusuk olan yalniz public/models/aday/ altina konur.
# Puani olmayan (hakem calismamis) kalem yayinlanmaz. Anahtar yazdirilmaz. Claude kullanmaz.
import os, sys, re, json, shutil, subprocess, argparse, time, urllib.request, urllib.error, datetime as dt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DURUM = os.path.join(ROOT, '.kos', 'kopru', 'ucretsiz', '3d-durum.json')
SITE = os.path.join(os.path.expanduser('~'), 'Desktop', 'Claude ile yapılanlar', 'yaka-cicegi', 'site')
U3D = os.path.join(SITE, '.claude', 'u3d')
CANLI = 'https://ilik-yaka-cicegi.vercel.app'
OZET = os.path.join(ROOT, '.kos', 'kopru', 'arka', 'gece-ozeti.md')
DESKTOP = os.path.join(ROOT, '.kos', 'kopru', 'arka', '_desktop.md')
MAX_KB = 600
# Sitedeki surumun en son olculen hakem4 puani (ilik-v6-ilerleme.md "son en iyi" + faz2k No.2 prosedurel 56,9)
SITE_PUAN = {1: 72.5, 2: 56.9, 3: 57.7, 4: 73.8, 5: 61.8, 6: 64.0, 7: 56.8}

def _env():
    e = dict(os.environ); ek = ['C:/Program Files/nodejs', 'C:/Program Files/Git/cmd', os.path.expandvars('%APPDATA%/npm')]
    e['PATH'] = os.pathsep.join(ek + [e.get('PATH', '')]); return e

def calistir(cmd, **kw):
    return subprocess.run(cmd, cwd=SITE, capture_output=True, text=True, shell=isinstance(cmd, str), encoding='utf-8', errors='replace', env=_env(), timeout=900, **kw)

def adaylar(elle):
    c = {}
    try: k = json.load(open(DURUM, encoding='utf-8')).get('kuyruk') or {}
    except Exception: k = {}
    for n, v in k.items():
        if v.get('puan') is not None and v.get('glb'):
            c[int(n)] = (os.path.join(U3D, 'out', f'q{n}.glb'), float(v['puan']), 'kuyruk')
    for e in elle:  # N=yol:puan
        n, rest = e.split('=', 1); yol, puan = rest.rsplit(':', 1)
        c[int(n)] = (yol, float(puan), 'elle')
    return c

def vlist():
    r = calistir('vercel ls --format=json')
    try: x = json.loads(r.stdout)['deployments'][0]; return 'https://' + x['url'], x['state']
    except Exception: return None

def kod(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, method='HEAD'), timeout=30) as r: return r.status, r.headers.get('Content-Length')
    except urllib.error.HTTPError as e: return e.code, None
    except Exception as e: return 0, str(e)[:60]

def main():
    a = argparse.ArgumentParser(); a.add_argument('--glb', action='append', default=[]); a.add_argument('--dry', action='store_true'); x = a.parse_args()
    c = adaylar(x.glb); log = []
    if not c: print('aday yok (kuyruk bos/puansiz)'); log.append('aday yok'); ozet(log, None, []); return
    vit = os.path.join(SITE, 'src', 'scenes', 'VitrinCanvas.jsx'); kaynak = open(vit, encoding='utf-8').read(); yeni = kaynak
    dosyalar, urller = [], []
    for n, (yol, puan, kay) in sorted(c.items()):
        if not os.path.exists(yol): log.append(f'No.{n}: dosya yok ({yol})'); continue
        kb = os.path.getsize(yol) / 1024
        if kb > MAX_KB: log.append(f'No.{n}: {kb:.0f} KB > {MAX_KB} KB, alinmadi'); continue
        aday = os.path.join(SITE, 'public', 'models', 'aday', f'ucretsiz-{n}-{kay}.glb'); shutil.copy(yol, aday)
        dosyalar.append(os.path.relpath(aday, SITE).replace('\\', '/')); urller.append(f'/models/aday/ucretsiz-{n}-{kay}.glb')
        mevcut = SITE_PUAN.get(n, 0)
        if puan > mevcut:
            ad = f'urun-{n}-ucretsiz.glb'; shutil.copy(yol, os.path.join(SITE, 'public', 'models', ad))
            dosyalar.append(f'public/models/{ad}'); urller.append(f'/models/{ad}')
            ent = f"{n}: ['/models/{ad}', 0]"
            if re.search(rf'\b{n}: \[\'/models/[^\']+\', \d+\]', yeni): yeni = re.sub(rf"\b{n}: \['/models/[^']+', \d+\]", ent, yeni, count=1)
            else: yeni = re.sub(r'const GLB = \{ ', 'const GLB = { ' + ent + ', ', yeni, count=1)
            log.append(f'No.{n}: {puan} > {mevcut} -> SITEYE ALINDI ({ad}, {kb:.0f} KB)')
        else: log.append(f'No.{n}: {puan} <= {mevcut} -> yalniz aday/ (site degismedi, {kb:.0f} KB)')
    if yeni != kaynak: open(vit, 'w', encoding='utf-8', newline='').write(yeni); dosyalar.append('src/scenes/VitrinCanvas.jsx')
    if x.dry: print('\n'.join(log)); return
    b = calistir('npm run build')
    if b.returncode: log.append('BUILD HATA: ' + (b.stdout + b.stderr)[-300:]); ozet(log, None, urller); print('\n'.join(log)); sys.exit(1)
    log.append('build temiz')
    onceki = vlist()
    calistir(['git', 'add', '--'] + dosyalar)
    cm = calistir(['git', 'commit', '-m', 'ILIK-GECE-YAYIN: ucretsiz uretim GLB\n\n' + '\n'.join(log) + '\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>', '--only', '--'] + dosyalar)
    log.append('commit: ' + (cm.stdout.strip().splitlines() or ['?'])[0][:80])
    p = calistir(['git', 'push', 'origin', 'main'])
    if p.returncode: log.append('PUSH HATA: ' + p.stderr[-200:]); ozet(log, None, urller); print('\n'.join(log)); sys.exit(1)
    log.append('push main tamam')
    son = None
    for _ in range(40):  # <=40 x 15 sn
        time.sleep(15); v = vlist()
        if v and (not onceki or v[0] != onceki[0]):
            son = v
            if v[1] in ('READY', 'ERROR', 'CANCELED'): break
    log.append(f'vercel: {son}')
    sonuc = []
    if son and son[1] == 'READY':
        for u in urller:
            for _ in range(6):
                s, l = kod(CANLI + u)
                if s == 200: break
                time.sleep(10)
            sonuc.append(f'{u} {s} {l}B')
    log.append('canli: ' + '; '.join(sonuc))
    ozet(log, son, urller); print('\n'.join(log))

def ozet(log, son, urller):
    t = dt.datetime.now().strftime('%d %b %H:%M')
    satir = f'\n## ILIK-GECE-YAYIN {t}\nCanli: {CANLI}\n' + '\n'.join('- ' + l for l in log) + '\n'
    for f in (OZET, DESKTOP):
        try: open(f, 'a', encoding='utf-8').write(satir)
        except Exception: pass

if __name__ == '__main__': main()
