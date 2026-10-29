# ucretsiz_3d.py: ucretsiz 3D uretimi icin kalici yonlendirici (metin havuzu ucretsiz_havuz.py'nin 3D karsiligi).
#   --yokla                : saglayicilari canli olc -> .kos/kopru/ucretsiz/3d-durum.json (anahtar degeri ASLA yazilmaz)
#   --uret <foto> --ad No7 : kalan krediye/maliyete gore en kaliteliyi sec; 402 -> siradaki, 429 -> yenilenme saatini kaydet + siradaki
#   --kuyruk               : bekleyen kalemleri (2,3,5,6,7) sirayla uret + kalite hatti (zamanlayicidan cagrilir)
#   --planla               : kotasi dolan saglayicinin yenilenmesinden 5 dk sonrasina tek seferlik gorev kurar
# Kural: para harcanmaz (yalniz ucretsiz kredi/kota), HTTP'de HER ZAMAN User-Agent (Higgsfield/Cloudflare 1010 dersi), silme yok.
import os, sys, re, json, time, shutil, subprocess, threading, argparse, urllib.request, urllib.error, datetime as dt
try: import winreg
except ImportError: winreg = None
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DURUM = os.path.join(ROOT, '.kos', 'kopru', 'ucretsiz', '3d-durum.json')
U3D = os.path.join(os.path.expanduser('~'), 'Desktop', 'Claude ile yapılanlar', 'yaka-cicegi', 'site', '.claude', 'u3d')
UA = {'User-Agent': 'curl/8.9.1'}

def env(k):
    v = os.environ.get(k)
    if v or not winreg: return v
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Environment') as h: return winreg.QueryValueEx(h, k)[0]
    except OSError: return None

def http(url, hd=None, body=None, method=None, t=40):
    r = urllib.request.Request(url, json.dumps(body).encode() if body is not None else None, {**UA, **(hd or {})}, method=method)
    if body is not None: r.add_header('Content-Type', 'application/json')
    try:
        with urllib.request.urlopen(r, timeout=t) as x: return x.status, x.read().decode('utf8', 'ignore')
    except urllib.error.HTTPError as e: return e.code, e.read().decode('utf8', 'ignore')
    except Exception as e: return 0, str(e)[:120]

def yukle():
    try: return json.load(open(DURUM, encoding='utf8'))
    except (OSError, ValueError): return {'saglayici': {}}

def yaz(d):
    os.makedirs(os.path.dirname(DURUM), exist_ok=True)
    d['guncel'] = dt.datetime.now().isoformat(timespec='seconds')
    with open(DURUM, 'w', encoding='utf8', newline='\n') as f: json.dump(d, f, ensure_ascii=False, indent=1)

def kayit(d, ad, **kw):
    d['saglayici'].setdefault(ad, {}).update(kw, olcum=dt.datetime.now().isoformat(timespec='seconds'))

# kalite sirasi (yuksek -> dusuk); maliyet = bir dokulu GLB icin kredi; kredi=None -> kredi tipi degil (kota)
SIRA = [('higgsfield', 9), ('hf-zerogpu', 0), ('sorceress', 40), ('3daistudio', 60), ('tripo-api', 40)]

# ---------- yoklama ----------
def yokla_hf_space(d):
    """Gercek is dener (ZeroGPU ucretsiz): kota bitmisse hata govdesinden yenilenme saati okunur."""
    r = uret_hf(os.path.join(U3D, 'in', '7-white.png'), '_yokla', sure=150)
    if r.get('glb'): kayit(d, 'hf-zerogpu', durum='kota var', son_hata=None, yenilenme=None, uretilen=r['glb'])
    elif r.get('kota'): kayit(d, 'hf-zerogpu', durum='kota dolu', yenilenme=r['yenilenme'], son_hata=r['hata'][:200])
    else: kayit(d, 'hf-zerogpu', durum='belirsiz', son_hata=r.get('hata', '')[:200])

def yokla():
    d = yukle()
    H = env('HIGGSFIELD_API_KEY')
    s, b = http('https://platform.higgsfield.ai/requests/00000000-0000-0000-0000-000000000000/status', {'Authorization': 'Key ' + (H or '')})
    kayit(d, 'higgsfield', anahtar_var=bool(H), http_durum=s, kalan_kredi=d['saglayici'].get('higgsfield', {}).get('kalan_kredi', 1), is_basi={'tripo_h3_1_std': 9, 'tripo_h3_1_detailed': 18, 'hunyuan3d_v3': 11, 'tripo_p2': 34},
          not_='REST bakiye ucu yok; kalan_kredi Desktop MCP olcumu (29 Eki 17:15). Yenilenme kurali belgeden/Desktop ile dogrulanmali. Uretim Desktop MCP ile (UA sart).')
    s, b = http('https://api.tripo3d.ai/v2/openapi/user/balance', {'Authorization': 'Bearer ' + (env('TRIPO_API_KEY') or '')})
    try: bal = json.loads(b)['data']['balance']
    except Exception: bal = None
    kayit(d, 'tripo-api', http_durum=s, kalan_kredi=bal, is_basi=40)
    s, b = http('https://api.3daistudio.com/account/user/wallet/', {'Authorization': 'Bearer ' + (env('THREEDAI_API_KEY') or '')})
    try: bal = float(json.loads(b)['balance'])
    except Exception: bal = None
    kayit(d, '3daistudio', http_durum=s, kalan_kredi=bal, is_basi=60, not_='dokulu en ucuz 60 kr')
    old = d['saglayici'].get('sorceress', {})
    kayit(d, 'sorceress', anahtar_var=bool(env('SORCERESS_API_KEY')), kalan_kredi=old.get('kalan_kredi', 20), is_basi={'tripo-v3.1 std': 40, 'hunyuan3d-3.1': 30},
          not_='bakiye ucu yok; deger son 402 yanitindan (sorc-kuyruk.log), --uret 402 alinca guncellenir')
    s, b = http('https://integrate.api.nvidia.com/v1/models', {'Authorization': 'Bearer ' + (env('NVIDIA_API_KEY') or '')})
    kayit(d, 'nvidia-nim-trellis', http_durum=s, kullanilamaz='trellis yalniz metin kabul ediyor (422 example_id) -> foto girdisi yok')
    F = env('FAL_KEY'); s, b = http('https://queue.fal.run/fal-ai/trellis', {'Authorization': 'Key ' + (F or '')}, body={})
    kayit(d, 'fal', http_durum=s, yanit=b[:160].replace(F or '\0', '***'), not_='bos govdeyle sinama (para harcamaz); 403 ise bakiye bitik, 422 ise kimlik+bakiye gecti')
    C = env('CLOUDFLARE_API_KEY'); s, b = http('https://api.cloudflare.com/client/v4/user/tokens/verify', {'Authorization': 'Bearer ' + (C or '')})
    kayit(d, 'cloudflare', anahtar_var=bool(C), hesap_id_var=bool(env('CLOUDFLARE_ACCOUNT_ID')), http_durum=s, yanit=b[:120],
          not_='CLOUDFLARE_API_KEY Bearer olarak gecersiz (Global API Key biciminde; X-Auth-Email gerekir). Workers AI katalogunda image-to-3D modeli yok -> 3D icin kullanilamaz')
    kayit(d, 'modal', durum='Omer karari', not_='GPU icin odeme yontemi sart (T4/A10G/L40S InvalidError); CAGRILMAZ')
    kayit(d, 'meshy-web+tripo-web', durum='Desktop Chrome gerekir', not_='Desktop listesine; girisli oturum')
    yokla_hf_space(d)
    yaz(d); print(json.dumps({k: {x: v.get(x) for x in ('kalan_kredi', 'durum', 'http_durum', 'yenilenme') if x in v} for k, v in d['saglayici'].items()}, ensure_ascii=False))

# ---------- uretim ----------
def kota_oku(msg):
    """'Try again in 0:12:34' ya da 'in 12h' -> yenilenme zamani."""
    m = re.search(r'again in\s+(\d+):(\d+):(\d+)', msg)
    if m: return (dt.datetime.now() + dt.timedelta(hours=int(m[1]), minutes=int(m[2]), seconds=int(m[3]))).isoformat(timespec='seconds')
    return None

def uret_hf(foto, ad, sure=900):
    out = {}
    def is_():
        try:
            from gradio_client import Client, handle_file
            for sp, ep in (('tencent/Hunyuan3D-2.1', 'hy'), ('microsoft/TRELLIS.2', 'tr')):
                try:
                    c = Client(sp, token=env('HF_TOKEN'), verbose=False)
                    if ep == 'hy':
                        r = c.predict(image=handle_file(foto), steps=30, guidance_scale=5.0, seed=1234, octree_resolution=256, check_box_rembg=True, num_chunks=8000, randomize_seed=False, api_name='/generation_all')
                    else:
                        c.predict(api_name='/start_session'); p = c.predict(input=handle_file(foto), api_name='/preprocess_image')
                        c.predict(image=handle_file(p), seed=0, resolution='1024', api_name='/image_to_3d')
                        r = c.predict(decimation_target=300000, texture_size=2048, api_name='/extract_glb')
                    g = [x for x in _yollar(r) if x.endswith('.glb')]
                    if g:
                        dst = os.path.join(U3D, 'out', f'hfz-{ad}.glb'); shutil.copy(g[-1], dst); out['glb'] = dst; out['saglayici'] = sp; return
                except Exception as e:
                    m = str(e); out['hata'] = (out.get('hata', '') + f' | {sp}: {m}')[:600]
                    if re.search(r'quota|ZeroGPU|429|exceeded', m, re.I): out['kota'] = True; out['yenilenme'] = out.get('yenilenme') or kota_oku(m)
        except Exception as e: out['hata'] = str(e)[:300]
    t = threading.Thread(target=is_, daemon=True); t.start(); t.join(sure)
    if t.is_alive() and not out: out['hata'] = f'{sure}s icinde bitmedi (kota var, is surdu)'
    return out

def _yollar(o):
    if isinstance(o, str): return [o]
    if isinstance(o, dict): return sum([_yollar(v) for v in o.values()], [])
    if isinstance(o, (list, tuple)): return sum([_yollar(v) for v in o], [])
    return []

def uret_sorc(foto, ad):
    sys.path.insert(0, U3D); import sorc  # sorc.req: UA'li istek
    n = re.sub(r'\D', '', ad) or '0'
    u = sorc.req('/tools/file_upload', {'filename': f'urun-{n}.png', 'contentType': 'image/png'})['data']
    urllib.request.urlopen(urllib.request.Request(u['uploadUrl'], open(foto, 'rb').read(), {'Content-Type': 'image/png', **UA}, method='PUT'), timeout=120)
    r = sorc.req('/tools/model_generate', {'model': 'tripo-v3.1', 'imageUrl': u['publicUrl'], 'params': {'texture': 'standard'}})
    if r.get('HTTP') == 402:
        try: return {'odeme': True, 'kalan': json.loads(r['body']).get('balance')}
        except Exception: return {'odeme': True}
    jid = (r.get('data') or {}).get('jobId')
    if not jid: return {'hata': str(r)[:200]}
    t0 = time.time()
    while time.time() - t0 < 1200:
        time.sleep(15); s = sorc.req(f'/jobs/{jid}'); dd = s.get('data', s)
        if dd.get('status') in ('succeeded', 'failed', 'error'): break
    url = (dd.get('mesh') or {}).get('url') if isinstance(dd.get('mesh'), dict) else None
    if not url: return {'hata': json.dumps(dd)[:200]}
    dst = os.path.join(U3D, 'out', f'sorc-{ad}.glb'); urllib.request.urlretrieve(url, dst); return {'glb': dst}

def uret_3dai(foto, ad):
    import base64
    key = env('THREEDAI_API_KEY'); hd = {'Authorization': 'Bearer ' + key}
    img = 'data:image/png;base64,' + base64.b64encode(open(foto, 'rb').read()).decode()
    s, b = http('https://api.3daistudio.com/v1/3d-models/tripo/image-to-3d/3.2/', hd, {'image': img}, t=120)
    if s in (402, 403): return {'odeme': True, 'hata': b[:150]}
    try: tid = json.loads(b)['task_id']
    except Exception: return {'hata': f'{s} {b[:150]}'}
    t0 = time.time()
    while time.time() - t0 < 900:
        time.sleep(15); s, b = http(f'https://api.3daistudio.com/v1/generation-request/{tid}/status/', hd); j = json.loads(b)
        if j['status'] in ('FINISHED', 'FAILED'): break
    if j['status'] != 'FINISHED': return {'hata': str(j)[:200]}
    dst = os.path.join(U3D, 'out', f'3dai-{ad}.glb'); urllib.request.urlretrieve(j['results'][0]['asset'], dst); return {'glb': dst}

def uret(foto, ad):
    d = yukle(); S = d['saglayici']
    for ad_s, maliyet in SIRA:
        k = S.get(ad_s, {}); kalan = k.get('kalan_kredi')
        if ad_s == 'higgsfield': print('atla higgsfield: yalniz Desktop MCP ile uretilir (kalan', kalan, ', is 9)'); continue
        if ad_s == 'tripo-api': continue
        if kalan is not None and kalan < maliyet: print(f'atla {ad_s}: kalan {kalan} < {maliyet}'); continue
        yen = k.get('yenilenme')
        if ad_s == 'hf-zerogpu' and yen and dt.datetime.fromisoformat(yen) > dt.datetime.now(): print(f'atla {ad_s}: yenilenme {yen}'); continue
        print('dene', ad_s)
        r = uret_hf(foto, ad) if ad_s == 'hf-zerogpu' else uret_sorc(foto, ad) if ad_s == 'sorceress' else uret_3dai(foto, ad)
        if r.get('glb'): kayit(d, ad_s, son_hata=None); yaz(d); print('GLB', r['glb']); return r['glb']
        if r.get('kota'): kayit(d, ad_s, durum='kota dolu', yenilenme=r.get('yenilenme'), son_hata=r['hata'][:200])
        elif r.get('odeme'):
            if r.get('kalan') is not None: kayit(d, ad_s, kalan_kredi=r['kalan'])
            kayit(d, ad_s, son_hata='402 kredi yok')
        else: kayit(d, ad_s, son_hata=str(r.get('hata'))[:200])
        yaz(d)
    print('hicbir saglayici uretemedi'); return None

# ---------- kalite hatti + kuyruk + zamanlayici ----------
def kalite(glb, n, ad):
    """isle.sh (renk esle, meshopt, <=600KB, render) + hakem4 (4 kosu x 2 hakem) -> ortalama puan."""
    bash = shutil.which('bash') or r'C:\Program Files\Git\bin\bash.exe'
    subprocess.run([bash, 'isle.sh', os.path.relpath(glb, U3D).replace('\\', '/'), f'in/{n}-rgba.png', ad], cwd=U3D, check=True)
    subprocess.run([sys.executable, 'hakem4.py', str(n), ad], cwd=U3D, check=True)
    return json.load(open(os.path.join(U3D, 'r', f'{ad}-h4.json')))['ort']

def kuyruk():
    d = yukle(); d.setdefault('kuyruk', {})
    for n in (2, 3, 5, 6, 7):
        if d['kuyruk'].get(str(n), {}).get('puan'): continue
        foto = os.path.join(U3D, 'in', f'{n}-white.png'); glb = uret(foto, f'q{n}')
        d = yukle(); d.setdefault('kuyruk', {})
        if not glb: d['kuyruk'][str(n)] = {'durum': 'uretilemedi'}; yaz(d); break  # kota/kredi yoksa siradakini bosa denemez
        d['kuyruk'][str(n)] = {'glb': glb, 'puan': kalite(glb, n, f'q{n}')}; yaz(d)

def planla():
    d = yukle(); yens = [(k, v['yenilenme']) for k, v in d['saglayici'].items() if v.get('yenilenme')]
    if not yens:  # gövdede saat yoksa (runs limit): hy21.log'dan olculen ~00:30 gunluk yenilenme
        n = dt.datetime.now(); t0 = n.replace(hour=0, minute=30, second=0, microsecond=0)
        yens = [('hf-zerogpu(olculen 00:30)', (t0 if t0 > n else t0 + dt.timedelta(days=1)).isoformat(timespec='seconds'))]
    ad, y = min(yens, key=lambda x: x[1]); t = dt.datetime.fromisoformat(y) + dt.timedelta(minutes=5)
    py = shutil.which('pythonw') or sys.executable  # pencere acmaz
    cmd = f'"{py}" "{os.path.abspath(__file__)}" --kuyruk'
    subprocess.run(['schtasks', '/create', '/f', '/tn', 'ucretsiz3d-kuyruk', '/sc', 'once', '/sd', t.strftime('%d/%m/%Y'), '/st', t.strftime('%H:%M'), '/tr', cmd], check=True)
    print(f'gorev kuruldu: {t:%Y-%m-%d %H:%M} ({ad} yenilenmesi +5 dk)')

if __name__ == '__main__':
    a = argparse.ArgumentParser(); a.add_argument('--yokla', action='store_true'); a.add_argument('--uret'); a.add_argument('--ad', default='x')
    a.add_argument('--kuyruk', action='store_true'); a.add_argument('--planla', action='store_true'); x = a.parse_args()
    if x.yokla: yokla()
    elif x.uret: uret(x.uret, x.ad)
    elif x.kuyruk: kuyruk()
    elif x.planla: planla()
    else: a.print_help()
