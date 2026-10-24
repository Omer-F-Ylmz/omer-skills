"""KAYNAK-KUTUPHANE-1: tara-parca1.json + secili tablo -> site md, envanter.tsv, kutuphane-haritasi.tsv, icerik tsv; AL repolarini klonlar."""
import json, os, re, subprocess, datetime, collections, sys
R = 'docs/kaynak-kutuphane'; LIB = r'C:/Users/pc/Desktop/Claude ile yapılanlar/kaynak-kutuphane'
P = sys.argv[1] if len(sys.argv) > 1 else '1'; S = '' if P == '1' else f'-parca{P}'  # parça 3: python tools/kk1_yaz.py 3
out = json.load(open(f'{R}/tara-parca{P}.json', encoding='utf8')); BUGUN = datetime.date.today().isoformat()
# host: (tur, own_repo, lisans, sart, karar, indirme)
T = {
'reactbits.dev': ('UI bileşen/animasyon', 'DavidHDev/react-bits', 'MIT+Commons Clause', 'satış/yeniden dağıtım yasak; site/üründe kullanım serbest', 'AL-ŞARTLI', 'GitHub+shadcn registry'),
'21st.dev': ('UI bileşen (topluluk)', 'serafimcloud/21st', 'MIT (platform); bileşen lisansı yazara bağlı', 'her bileşende yazar lisansı ayrı bakılır', 'AL-ŞARTLI', 'registry/MCP'),
'fancycomponents.dev': ('UI bileşen/animasyon', 'danielpetho/fancy', 'MIT', '', 'AL', 'GitHub+shadcn registry'),
'kokonutui.com': ('UI bileşen', 'kokonut-labs/kokonutui', 'MIT', '', 'AL', 'GitHub+shadcn registry'),
'cult-ui.com': ('UI bileşen', 'nolly-studio/cult-ui', 'MIT', '', 'AL', 'GitHub+shadcn registry'),
'shadcn.io': ('UI bileşen dizini', '', 'belirsiz (sahip repo yok)', 'lisans doğrulanamadı', 'ATLANDI', '-'),
'componentry.dev': ('UI bileşen/animasyon', 'harshjdhv/componentry', 'MIT', '', 'AL', 'GitHub+registry'),
'canvasui.dev': ('UI bileşen (canvas)', 'DavidHDev/canvas-ui', 'MIT+Commons Clause', 'satış/yeniden dağıtım yasak', 'AL-ŞARTLI', 'GitHub'),
'originkit.dev': ('UI bileşen', '', 'erişilemedi (zaman aşımı)', 'tarama başarısız', 'ATLANDI', '-'),
'uiarc.dev': ('UI bileşen', 'kuratlielia/arc-library', 'MIT', '', 'AL', 'GitHub'),
'vengenceui.com': ('UI bileşen', 'ashutoshx7/vengenceui', 'MIT', '', 'AL', 'GitHub'),
'skecher-ui.com': ('UI bileşen', 'codesign-spa27/skecher-ui', 'LİSANS DOSYASI YOK', 'lisanssız = tüm haklar saklı', 'ATLANDI', 'GitHub (alınmadı)'),
'balsa-ui.com': ('UI bileşen', '', 'belirsiz', 'sahip repo bulunamadı', 'ATLANDI', '-'),
'threeui.com': ('3D/UI bileşen', '', 'belirsiz', 'sahip repo bulunamadı', 'ATLANDI', '-'),
'threlte.xyz': ('3D kütüphane (Svelte+three)', 'threlte/threlte', 'MIT', '', 'AL', 'npm @threlte/core'),
'vantajs.com': ('WebGL arka plan efekti', 'tengbao/vanta', 'MIT', '', 'AL', 'GitHub+npm vanta'),
'base-ui.21st.dev': ('UI bileşen (Base UI)', 'mui/base-ui', 'MIT', '', 'AL', 'npm @base-ui-components/react'),
'motion.dev': ('animasyon kütüphanesi', 'motiondivision/motion', 'MIT', '', 'AL', 'npm motion'),
'gsap.com': ('animasyon kütüphanesi', 'greensock/GSAP', 'GSAP Standard License (ücretsiz, ticari dahil)', 'GSAP ile GSAP rakibi görsel animasyon aracı yapılamaz', 'AL-ŞARTLI', 'npm gsap'),
'lenis.dev': ('smooth scroll kütüphanesi', 'darkroomengineering/lenis', 'MIT', '', 'AL', 'GitHub+npm lenis'),
'react-spring.dev': ('animasyon kütüphanesi', 'pmndrs/react-spring', 'MIT', '', 'AL', 'npm @react-spring/web'),
'rive.app': ('animasyon çalışma zamanı', 'rive-app/rive-wasm', 'MIT (runtime); .riv dosyaları yazara bağlı', 'topluluk .riv lisansı tek tek', 'AL-ŞARTLI', 'npm @rive-app/canvas'),
'lottielab.com': ('animasyon editörü (SaaS)', '', 'ücretli editör/ücretsiz katman sınırlı', 'repo yok', 'ATLANDI', '-'),
'madewithgsap.com': ('ilham galerisi', '', 'galeri; içerik sahiplerine ait', 'kod indirme yok', 'ATLANDI', '-'),
'ripplix.com': ('animasyon ilham galerisi', '', 'galeri; içerik sahiplerine ait', 'kod indirme yok', 'ATLANDI', '-'),
'gradients.sh': ('gradyan CSS', '', 'belirsiz', 'lisans metni bulunamadı', 'ATLANDI', '-'),
'unicorn.studio': ('WebGL efekt editörü (SaaS)', '', 'ücretsiz katman+ücretli', 'kapalı kaynak', 'ATLANDI', '-'),
'springs.studio': ('spring animasyon aracı', '', 'belirsiz', 'sahip repo yok', 'ATLANDI', '-'),
'animos.app': ('şablon', '', 'belirsiz', 'sahip repo yok', 'ATLANDI', '-'),
'component.gallery': ('UI bileşen referans dizini', '', 'içerik referans; kod yok', 'kod indirme yok', 'ATLANDI', '-'),
'remotion.dev': ('video/animasyon kütüphanesi', 'remotion-dev/remotion', 'Remotion License (özel)', 'bireysel/≤3 kişilik şirket ücretsiz; büyük şirkete lisans gerekir', 'AL-ŞARTLI', 'npm remotion'),
'motion-canvas.io': ('animasyon kütüphanesi', 'motion-canvas/motion-canvas', 'MIT', '', 'AL', 'npm @motion-canvas/core'),
'lucide.dev': ('ikon seti', 'lucide-icons/lucide', 'ISC (+MIT Feather)', 'telif notu korunur', 'AL', 'GitHub SVG+npm lucide-static'),
'game-icons.net': ('ikon seti (oyun)', 'game-icons/icons', 'CC BY 3.0 (bazıları CC0)', 'atıf zorunlu (yazar adı)', 'AL-ŞARTLI', 'GitHub SVG'),
'3dicons.co': ('3D ikon', '', 'site: açık kaynak ikonlar; sürüm başına lisans doğrulanmadı', 'lisans sayfası okunmadı', 'ATLANDI', 'Figma/ZIP'),
'fontshare.com': ('font', '', 'ITF Free Font License (ticari serbest)', 'indirme site üzerinden; otomatik alınmadı', 'ATLANDI', 'site indirme'),
'googlefonts.github.io': ('font dizini', 'googlefonts/googlefonts.github.io', 'Apache-2.0 (site); fontlar OFL', 'fontlar tek tek OFL', 'AL', '@fontsource npm'),
'lordicon.com': ('animasyonlu ikon', '', 'ücretsiz katman atıf+kısıtlı', 'ücretli kısmı alınmaz', 'ATLANDI', '-'),
'thiings.co': ('3D ikon', '', 'belirsiz', 'lisans metni bulunamadı', 'ATLANDI', '-'),
'unblast.com': ('ücretsiz grafik/şablon', '', 'varlık başına değişir', 'toplu doğrulanamadı', 'ATLANDI', '-'),
'fontjoy.com': ('font eşleştirme aracı', 'jack000/fontjoy', 'MIT (2017, bakımsız)', '', 'AL', 'GitHub'),
'sketchfab.com': ('3D model', '', 'model başına CC; indirme giriş ister', 'giriş duvarı: alınmaz', 'ATLANDI', '-'),
'spline.design': ('3D editör (SaaS)', '', 'kapalı kaynak; dışa aktarım hesapla', 'giriş gerekir', 'ATLANDI', '-'),
'textures.com': ('doku', '', 'ücretsiz kota+kısıtlı lisans', 'giriş+kota', 'ATLANDI', '-'),
'zoetrope.furkankly.dev': ('animasyon kütüphanesi', 'furkankly/zoetrope', 'MIT', '', 'AL', 'GitHub'),
'webild.io': ('şablon', '', 'belirsiz', 'sahip repo yok', 'ATLANDI', '-'),
'clbthemes.com': ('şablon (WP tema)', '', 'ücretli temalar', 'ücretli', 'ATLANDI', '-'),
'collectivekit.co': ('şablon', '', 'belirsiz', 'sahip repo yok', 'ATLANDI', '-'),
'temlis.com': ('şablon dizini', '', 'şablon başına değişir', 'toplu doğrulanamadı', 'ATLANDI', '-'),
'coloniazacamil.com': ('UI sitesi (ilham)', '', 'sahip repo yok', 'site kodu bulunamadı; fflate üçüncü taraf bağımlılık', 'ATLANDI', '-'),
'namethatui.com': ('UI galerisi', '', 'sahip repo yok', 'kaynak kod yok', 'ATLANDI', '-'),
'prompt-motion.com': ('prompt/şablon galerisi', '', 'sahip repo yok', 'kaynak kod yok', 'ATLANDI', '-'),
'self.to': ('site/şablon', '', 'sahip repo yok', 'kaynak kod yok', 'ATLANDI', '-'),
'uizze.com': ('UI tasarım becerileri', 'uizze/uizze', 'MIT', 'telif notu korunur', 'AL', 'GitHub'),
'wallhang.com': ('3D/duvar kağıdı sitesi', '', 'belirsiz', 'tarama başarısız (SSL sertifika doğrulaması)', 'ATLANDI', '-'),
'whatships.com': ('gemi/görsel sitesi', '', 'sahip repo yok', 'kaynak kod yok', 'ATLANDI', '-'),
'app.spline.design': ('3D editör (SaaS)', '', 'kapalı kaynak', 'giriş gerekir', 'ATLANDI', '-'),
'aptransit.co': ('UI sitesi (ilham)', '', 'sahip repo yok', 'kaynak kod yok', 'ATLANDI', '-'),
'draftly.space': ('doküman/çizim aracı', '', 'lisans doğrulanamadı (repo adı .git içeriyor)', 'elle doğrulanacak', 'ATLANDI', '-'),
'kombai.com': ('UI üretici (SaaS)', '', 'kapalı kaynak', 'kaynak kod yok', 'ATLANDI', '-'),
'posemy.art': ('poz/3D referans', '', 'sahip repo yok', 'giriş/kota; kaynak yok', 'ATLANDI', '-'),
'reallusion.com': ('3D karakter (SaaS)', '', 'kapalı kaynak', 'ürün lisansı ücretli', 'ATLANDI', '-'),
'shotblock.vercel.app': ('WebGL demo', '', 'sahip repo yok', 'kaynak kod yok', 'ATLANDI', '-'),
'skills.wheresryan.sh': ('agent skill (izometrik çizim)', 'wheresryan22/anatomy', 'MIT', 'telif notu korunur', 'AL', 'GitHub'),
'top3d.ai': ('3D üretim (SaaS)', '', 'kapalı kaynak', 'kaynak kod yok', 'ATLANDI', '-'),
'getlayers.ai': ('web şablon/prompt kütüphanesi', 'textura-agency/next16-claude-starter', 'Unlicense (kamu malı)', 'sahip eşleşmesi (textura-agency) elle doğrulanacak', 'AL-ŞARTLI', 'GitHub'),
'jiro.build': ('site oluşturucu (SaaS)', '', 'kapalı kaynak', 'kaynak kod yok', 'ATLANDI', '-'),
'scrolltide.co': ('scroll animasyon sitesi', '', 'sahip repo yok', 'kaynak kod yok', 'ATLANDI', '-'),
}
os.makedirs(f'{R}/site', exist_ok=True)
env = dict(os.environ); env['GIT_TERMINAL_PROMPT'] = '0'
info = {i['repo'].lower(): i for o in out.values() for i in o['repo_bilgi']}
def sz(p):
    return sum(os.path.getsize(os.path.join(d, f)) for d, _, fs in os.walk(p) for f in fs) // 1024
env_rows, lib_rows, alinan, atlanan = [], collections.defaultdict(lambda: [set(), '', '']), [], []
for h, (tur, repo, lis, sart, karar, ind) in T.items():
    if h not in out: continue
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
status: parca1
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
with open(f'{R}/envanter{S}.tsv', 'w', encoding='utf8', newline='\n') as f:
    f.write('site\ttur\tucretsiz\tlisans\tsart_atif\tindirme\tkarar\tyer\n')
    for r in env_rows: f.write('\t'.join(r) + '\n')
LNOT = {'three.js': ('3D render', 'MIT', 'mrdoob/three.js'), 'gsap': ('timeline/scroll animasyon', 'GSAP Standard', 'greensock/GSAP'), 'lenis': ('smooth scroll', 'MIT', 'darkroomengineering/lenis'),
 'framer-motion/motion': ('React/JS animasyon', 'MIT', 'motiondivision/motion'), 'react-spring': ('spring fiziği', 'MIT', 'pmndrs/react-spring'), 'lottie': ('vektör animasyon oynatma', 'MIT', 'airbnb/lottie-web'),
 'rive': ('etkileşimli animasyon', 'MIT', 'rive-app/rive-wasm'), 'spline': ('3D sahne gömme', 'ticari runtime', 'splinetool/runtime'), 'r3f': ('React three.js', 'MIT', 'pmndrs/react-three-fiber'),
 'tailwind': ('utility CSS', 'MIT', 'tailwindlabs/tailwindcss'), 'radix': ('erişilebilir primitive', 'MIT', 'radix-ui/primitives'), 'shadcn': ('bileşen dağıtım modeli', 'MIT', 'shadcn-ui/ui'),
 'next.js': ('React framework', 'MIT', 'vercel/next.js'), 'ogl': ('mini WebGL', 'Unlicense', 'oframe/ogl'), 'matter-js': ('2D fizik', 'MIT', 'liabru/matter-js'), 'lucide': ('ikon', 'ISC', 'lucide-icons/lucide'),
 'webgl-shader': ('GLSL shader', '-', '-'), 'svelte': ('UI framework', 'MIT', 'sveltejs/svelte'), 'nuxt/vue': ('Vue framework', 'MIT', 'nuxt/nuxt'), 'tsl/webgpu': ('WebGPU/TSL', 'MIT', 'mrdoob/three.js'),
 'codemirror/monaco': ('kod editörü', 'MIT', 'microsoft/monaco-editor')}
with open(f'{R}/kutuphane-haritasi{S}.tsv', 'w', encoding='utf8', newline='\n') as f:
    f.write('kutuphane\tsiteler\tne_icin\tlisans\trepo\n')
    for l, (s, _, _) in sorted(lib_rows.items(), key=lambda x: -len(x[1][0])):
        n = LNOT.get(l, ('', '', '')); f.write(f"{l}\t{','.join(sorted(s))}\t{n[0]}\t{n[1]}\t{n[2]}\n")
json.dump({'alinan': alinan, 'atlanan': atlanan}, open(f'{R}/_ozet-parca{P}.json', 'w', encoding='utf8'), ensure_ascii=False)
print(len(T), 'site;', len(alinan), 'klon;', len(atlanan), 'atlandi;', len(lib_rows), 'kutuphane;', sum(a[3] for a in alinan) // 1024, 'MB')
