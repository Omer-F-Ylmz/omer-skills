"""KAYNAK-KUTUPHANE-1 parca 2: tara-parca2.json + secili tablo -> site md, envanter-parca2.tsv, kutuphane-haritasi-parca2.tsv, icerik tsv; AL repolarini klonlar. Parca 1 ciktilarina dokunmaz."""
import json, os, re, subprocess, datetime, collections
R = 'docs/kaynak-kutuphane'; LIB = r'C:/Users/pc/Desktop/Claude ile yapılanlar/kaynak-kutuphane'
out = json.load(open(f'{R}/tara-parca2.json', encoding='utf8')); BUGUN = datetime.date.today().isoformat()
# host: (tur, own_repo, lisans, sart, karar, indirme)
T = {
'ace.c9.io': ('kod editörü (Ace)', 'ajaxorg/ace', 'BSD-3-Clause', 'telif notu korunur', 'AL', 'GitHub+npm ace-builds'),
'adele.uxpin.com': ('UI şablon/tasarım sistemi', '', 'belirsiz', 'sahip repo yok', 'ATLANDI', '-'),
'arxivisual.org': ('görselleştirme sitesi', '', 'belirsiz', 'sahip repo yok', 'ATLANDI', '-'),
'cadence.rubenstom.com': ('animasyon ilham/şablon', '', 'belirsiz', 'sahip repo yok', 'ATLANDI', '-'),
'catalog.ngc.nvidia.com': ('AI model/konteyner kataloğu', '', 'NVIDIA koşulları', 'kurumsal katalog; UI kaynağı değil', 'ATLANDI', '-'),
'codebase.build': ('site (kod tabanı)', '', 'belirsiz', 'sahip repo yok; bileşen kodu tespit edilmedi', 'ATLANDI', '-'),
'components.build': ('UI bileşen dizini', 'vercel/components.build', 'Apache-2.0', 'lisans ve NOTICE korunur', 'AL', 'GitHub'),
'craftwork.design': ('UI şablon/tasarım', '', 'belirsiz', 'sahip repo yok', 'ATLANDI', '-'),
'cultofclaude.com': ('topluluk dizini (Claude)', '', 'bağlı repolar ayrı lisanslı', 'site kendi kodu yok; bağlantılı repolar ayrı satır', 'ATLANDI', '-'),
'delta.dev': ('site (astro)', '', 'belirsiz', 'sahip repo yok', 'ATLANDI', '-'),
'design.cash.app': ('tasarım sitesi', '', 'belirsiz', 'robots alt sayfayı yasaklıyor; alt sayfa taranmadı', 'ATLANDI', '-'),
'designskills.dev': ('tasarım skill dizini', '', 'belirsiz', 'sahip repo bulunamadı (sayfadaki repo ayrı satır)', 'ATLANDI', '-'),
'designsystemlabs.co': ('tasarım sistemi (Radix/Lucide)', '', 'belirsiz', 'sahip repo yok', 'ATLANDI', '-'),
'dsc.gg': ('site (Lucide)', '', 'belirsiz', 'sahip repo yok', 'ATLANDI', '-'),
'excalidraw.com': ('el çizimi çizim bileşeni', 'excalidraw/excalidraw', 'MIT', 'telif notu korunur', 'AL', 'GitHub+npm @excalidraw/excalidraw'),
'getbootstrap.com': ('CSS/UI framework', 'twbs/bootstrap', 'MIT', 'telif notu korunur', 'AL', 'GitHub+npm bootstrap'),
'getrubric.app': ('WebGL shader efekti', '', 'belirsiz', 'sahip repo yok', 'ATLANDI', '-'),
'ghcr.io': ('altyapı (konteyner kayıt)', '', 'GitHub hizmeti', 'UI kaynağı değil', 'ATLANDI', '-'),
'gpui.rs': ('GPU UI framework (Zed)', 'zed-industries/zed', 'Apache-2.0 (GPUI crate; depo geneli ayrı)', 'tam zed deposu büyük; crate ayrı alınacak', 'ATLANDI', '-'),
'hairline.lucasmarkes.com': ('UI bileşen/tasarım sistemi', 'lucasmarkes/hairline', 'MIT', '', 'AL', 'GitHub'),
'highlightjs.org': ('kod vurgulama', 'highlightjs/highlight.js', 'BSD-3-Clause', 'telif notu korunur', 'AL', 'GitHub+npm highlight.js'),
'horizonx.so': ('site (gsap/lenis)', '', 'belirsiz', 'sahip repo yok', 'ATLANDI', '-'),
'img.shields.io': ('rozet servisi', 'badges/shields', 'Apache-2.0', 'UI kaynağı değil', 'ATLANDI', '-'),
'jquery.com': ('JS kütüphanesi', 'jquery/jquery', 'MIT', 'telif notu korunur', 'AL', 'GitHub+npm jquery'),
'kit.dev': ('UI kiti (shadcn/radix)', '', 'belirsiz', 'sahip repo yok', 'ATLANDI', '-'),
'kolekti.com': ('site (Next.js)', '', 'belirsiz', 'sahip repo yok', 'ATLANDI', '-'),
'libraries.dev': ('kütüphane dizini', 'jakubantalik/libraries.dev', 'MIT', '', 'AL', 'GitHub'),
'macos.telegram.org': ('ürün sitesi (Telegram)', '', 'Telegram koşulları', 'ürün sitesi; kod alınmaz', 'ATLANDI', '-'),
'n8n-skills.com': ('otomasyon skill dizini', 'czlonkowski/n8n-skills', 'MIT', 'UI değil (kapsam dışı)', 'ATLANDI', '-'),
'open-design.ai': ('tasarım aracı', 'nexu-io/open-design', 'Apache-2.0', 'telif notu korunur', 'AL', 'GitHub'),
'paperanimator.com': ('animasyon (site)', '', 'belirsiz', 'sahip repo yok', 'ATLANDI', '-'),
'polycasts.com': ('eğitim sitesi', '', 'belirsiz', 'sahip repo yok', 'ATLANDI', '-'),
'pptr.dev': ('tarayıcı otomasyonu', 'puppeteer/puppeteer', 'Apache-2.0', 'UI kaynağı değil (kapsam dışı)', 'ATLANDI', '-'),
'raw.githubusercontent.com': ('altyapı (dosya sunucusu)', '', 'GitHub hizmeti', 'UI kaynağı değil', 'ATLANDI', '-'),
'readymag.com': ('site oluşturucu (SaaS)', '', 'kapalı kaynak', 'SaaS; kod alınmaz', 'ATLANDI', '-'),
'scrollhaus.ai': ('scroll 3D şablon', 'amj1994/scrollhaus-free', 'YOK (lisans dosyası yok)', 'lisanssız = tüm haklar saklı', 'ATLANDI', '-'),
'shadcnblocks.com': ('UI blok kütüphanesi', 'shadcnblocks/shadcn-ui-blocks', 'MIT + Commons Clause', 'satış/ürün olarak yeniden dağıtım yasak', 'AL-ŞARTLI', 'GitHub'),
'shots.so': ('ekran görüntüsü aracı', '', 'belirsiz', 'sahip repo yok', 'ATLANDI', '-'),
'shields.io': ('rozet servisi', 'badges/shields', 'Apache-2.0', 'UI kaynağı değil', 'ATLANDI', '-'),
'socket.io': ('gerçek zamanlı ağ kütüphanesi', 'socketio/socket.io', 'MIT', 'UI kaynağı değil (kapsam dışı)', 'ATLANDI', '-'),
'stably.ai': ('QA platformu', 'stablyai/orca', 'MIT', 'UI kaynağı değil (kapsam dışı)', 'ATLANDI', '-'),
'stagehand.dev': ('AI tarayıcı otomasyonu', 'browserbase/stagehand', 'MIT', 'UI kaynağı değil (kapsam dışı)', 'ATLANDI', '-'),
'stitch.build': ('tasarım sitesi', '', 'belirsiz', 'tarama zaman aşımı (2 deneme); sahip repo yok', 'ATLANDI', '-'),
'superdesign.dev': ('tasarım aracı (site)', '', 'belirsiz', 'sahip repo yok', 'ATLANDI', '-'),
'swarms.xyz': ('AI ajan çatısı', 'kyegomez/swarms', 'Apache-2.0', 'UI kaynağı değil (kapsam dışı)', 'ATLANDI', '-'),
'tmux.sh': ('terminal aracı (site)', '', 'belirsiz', 'tarama zaman aşımı (2 deneme); sahip repo yok', 'ATLANDI', '-'),
'usehallmark.com': ('AI kart üretici', 'nutlope/hallmark', 'MIT', 'UI kaynağı değil (kapsam dışı)', 'ATLANDI', '-'),
'useplanes.com': ('site (tailwind/shadcn)', '', 'belirsiz', 'sahip repo yok', 'ATLANDI', '-'),
'visx.21st.dev': ('React grafik/görselleştirme bileşenleri', 'airbnb/visx', 'MIT', 'telif notu korunur', 'AL', 'GitHub+npm @visx/*'),
}
os.makedirs(f'{R}/site', exist_ok=True)
env = dict(os.environ); env['GIT_TERMINAL_PROMPT'] = '0'
info = {i['repo'].lower(): i for o in out.values() for i in o['repo_bilgi']}
def sz(p):
    return sum(os.path.getsize(os.path.join(d, f)) for d, _, fs in os.walk(p) for f in fs) // 1024
env_rows, lib_rows, alinan, atlanan = [], collections.defaultdict(lambda: [set(), '', '']), [], []
for h, (tur, repo, lis, sart, karar, ind) in T.items():
    o = out.get(h, {}); libs = o.get('libs', {}); ri = info.get(repo.lower(), {})
    ytl = f"{ri.get('yildiz','')}★ son {ri.get('son','')}" if ri else ''
    yol = ''
    if karar.startswith('AL') and repo and ind.startswith('GitHub'):
        slug = re.sub(r'[^\w.-]', '_', h)
        yol = f'{LIB}/{tur.split()[0].lower().replace("/", "-")}/{slug}/{repo.split("/")[1]}'
        if not os.path.isdir(yol):
            os.makedirs(os.path.dirname(yol), exist_ok=True)
            r = subprocess.run(['git', 'clone', '--depth', '1', '-q', f'https://github.com/{repo}.git', yol], capture_output=True, text=True, encoding='utf8', timeout=240, env=env)
            if r.returncode: yol = ''; karar += '(klon-hata)'
        if yol:
            open(f'{yol}/KAYNAK.md', 'w', encoding='utf8', newline='\n').write(f'# KAYNAK\n- site: https://{h}\n- repo: https://github.com/{repo}\n- lisans: {lis}\n- şart/atıf: {sart or "telif notu korunur"}\n- alınma tarihi: {BUGUN}\n- boyut: {sz(yol)} KB (.git dahil)\n')
            alinan.append((h, repo, lis, sz(yol)))
    if karar.startswith('ATLANDI'): atlanan.append((h, sart or lis))
    env_rows.append([h, tur, 'evet' if not karar.startswith('ATLANDI') else 'belirsiz/kısıtlı', lis, sart, ind, karar, yol.replace(LIB, '<lib>')])
    for l, n in libs.items():
        if n >= 2: lib_rows[l][0].add(h)
    sm = o.get('sitemap_ornek', [])
    open(f'{R}/site/{h}.md', 'w', encoding='utf8', newline='\n').write(f"""---
type: kaynak-site
status: parca2
tags: [kaynak-kutuphane]
relatedTo: [kaynak-kutuphane-1]
---
# {h}
- tür: {tur} · karar: **{karar}** · lisans: {lis} {('· şart: ' + sart) if sart else ''}
- başlık: {o.get('baslik','')} — {o.get('aciklama','')[:160]}
- tarama: {o.get('durum','?')} · robots: {o.get('robots','?')} · sitemap URL sayısı: {o.get('sitemap_url',0)}
- 0a repo: {('https://github.com/' + repo + ' · ' + ytl) if repo else 'sahip repo bulunamadı'}; sayfada geçen GitHub bağlantıları: {', '.join(o.get('github',[])[:5]) or '-'}; npm: {', '.join(o.get('npm',[])) or '-'}
- 0b yığın (HTML+ilk 6 JS paketi, anma sayısı): {', '.join(f'{k}×{v}' for k, v in sorted(libs.items(), key=lambda x: -x[1])) or 'tespit edilemedi (istemci-render/JS paketi okunamadı)'}
- indirme yolu: {ind}
- sitemap örnekleri: {', '.join(sm[:4]) or '-'}
- not: derin tarama HTTP+robots/sitemap ile yapıldı (≥1 sn aralık, giriş yok); REA/headless yalnız seçili sitelerde (rapora bak).
""")
    with open(f'{R}/site/{h}-icerik.tsv', 'w', encoding='utf8', newline='\n') as tsv:
        tsv.write('url\tkaynak\n')
        for u in sm: tsv.write(f'{u}\tsitemap(ilk 8; toplam {o.get("sitemap_url",0)})\n')
with open(f'{R}/envanter-parca2.tsv', 'w', encoding='utf8', newline='\n') as f:
    f.write('site\ttur\tucretsiz\tlisans\tsart_atif\tindirme\tkarar\tyer\n')
    for r in env_rows: f.write('\t'.join(r) + '\n')
LNOT = {'three.js': ('3D render', 'MIT', 'mrdoob/three.js'), 'gsap': ('timeline/scroll animasyon', 'GSAP Standard', 'greensock/GSAP'), 'lenis': ('smooth scroll', 'MIT', 'darkroomengineering/lenis'),
 'framer-motion/motion': ('React/JS animasyon', 'MIT', 'motiondivision/motion'), 'react-spring': ('spring fiziği', 'MIT', 'pmndrs/react-spring'), 'lottie': ('vektör animasyon oynatma', 'MIT', 'airbnb/lottie-web'),
 'rive': ('etkileşimli animasyon', 'MIT', 'rive-app/rive-wasm'), 'spline': ('3D sahne gömme', 'ticari runtime', 'splinetool/runtime'), 'r3f': ('React three.js', 'MIT', 'pmndrs/react-three-fiber'),
 'tailwind': ('utility CSS', 'MIT', 'tailwindlabs/tailwindcss'), 'radix': ('erişilebilir primitive', 'MIT', 'radix-ui/primitives'), 'shadcn': ('bileşen dağıtım modeli', 'MIT', 'shadcn-ui/ui'),
 'next.js': ('React framework', 'MIT', 'vercel/next.js'), 'ogl': ('mini WebGL', 'Unlicense', 'oframe/ogl'), 'matter-js': ('2D fizik', 'MIT', 'liabru/matter-js'), 'lucide': ('ikon', 'ISC', 'lucide-icons/lucide'),
 'webgl-shader': ('GLSL shader', '-', '-'), 'svelte': ('UI framework', 'MIT', 'sveltejs/svelte'), 'nuxt/vue': ('Vue framework', 'MIT', 'nuxt/nuxt'), 'tsl/webgpu': ('WebGPU/TSL', 'MIT', 'mrdoob/three.js'),
 'codemirror/monaco': ('kod editörü', 'MIT', 'microsoft/monaco-editor'), 'astro': ('site framework', 'MIT', 'withastro/astro')}
with open(f'{R}/kutuphane-haritasi-parca2.tsv', 'w', encoding='utf8', newline='\n') as f:
    f.write('kutuphane\tsiteler\tne_icin\tlisans\trepo\n')
    for l, (s, _, _) in sorted(lib_rows.items(), key=lambda x: -len(x[1][0])):
        n = LNOT.get(l, ('', '', '')); f.write(f"{l}\t{','.join(sorted(s))}\t{n[0]}\t{n[1]}\t{n[2]}\n")
json.dump({'alinan': alinan, 'atlanan': atlanan}, open(f'{R}/_ozet-parca2.json', 'w', encoding='utf8'), ensure_ascii=False)
print(len(T), 'site;', len(alinan), 'klon;', len(atlanan), 'atlandi;', len(lib_rows), 'kutuphane;', sum(a[3] for a in alinan) // 1024, 'MB')
