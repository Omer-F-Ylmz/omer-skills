"""IG-18-KUR toplu karar: devir40.tsv (DEVİR-IG40) + kalan.tsv (OZEL) → karar18.tsv; devir/*.tsv sonuna ek (--devir)."""
import csv, sys
from pathlib import Path

BU = Path(__file__).parent
DEVIR = Path('C:/Projeler/omer-skills/.kos/kopru/devir')
WT = Path('C:/Projeler/omer-skills-wt')
oku = lambda p: list(csv.DictReader(open(p, encoding='utf-8'), delimiter='\t'))
K40 = {}
for p in ['igkur/.claude/igkur/karar.tsv', 'igkur-p2/.claude/igkur/p2/karar.tsv', 'igkur-p3/.claude/igkur/p3/karar.tsv']:
    K40.update({s['sira']: s for s in oku(WT / p)})

D, R, KU = 'DEVİR', 'REF', 'KURULU'
# anahtar → (karar, hedef/kanal, gerekce, repo, lisans); listede olmayan satır REF (demo istemi / genel ürün-model-terim)
OZEL = {
    'awesomeselfhosted': (R, '-', 'liste; kendi sunuculu yazılım kapsam dışı', 'awesome-selfhosted/awesome-selfhosted', 'CC0'),
    'selfhostedyazlmreposu': (R, '-', 'awesome-selfhosted ile aynı liste', '-', '-'),
    'promptmotion': (D, 'animasyon-1', 'hazır animasyon istem kütüphanesi; repo belirsiz (crizmo/PromptMotion ★3 zayıf eşleşme)', '-', '-'),
    'eformax': (R, '-', 'CC efor ayarı zaten var; varsayılan Ömer kararı', '-', '-'),
    'awesomedesignmd': (D, 'tasarim-1', '73 marka DESIGN.md; tasarim-katalog ile karşılaştırılsın', 'VoltAgent/awesome-design-md', 'MIT'),
    'awesomedesign': (D, 'tasarim-1', 'awesome-design-md ile aynı', 'VoltAgent/awesome-design-md', 'MIT'),
    'webdesignguidelines': ('DEVİR-IG40', '246', '', '', ''),
    'playwrightmcp': ('DEVİR-IG40', '248', '', '', ''),
    'playwrightcli': ('DEVİR-IG40', '248', '', '', ''),
    'framermotion': ('DEVİR-IG40', '252', '', '', ''),
    'opus46': ('DEVİR-IG40', '83', '', '', ''),
    'hyperframescli': ('DEVİR-IG40', '250', '', '', ''),
    'hyperframescore': ('DEVİR-IG40', '250', '', '', ''),
    'gemini31propreview': ('DEVİR-IG40', '216', '', '', ''),
    'kling': (D, 'animasyon-1', 'görselden video modeli (fal.ai); hesap/ücret ister', '-', '-'),
    'falai': (D, 'animasyon-1', 'Kling çalıştıran servis; hesap/anahtar ister', '-', '-'),
    'klingileyzkrnvideosuretimi': (D, 'animasyon-1', 'Kling ürün videosu istemi (örnek istem)', '-', '-'),
    'threejs': (KU, 'CC', 'threejs skill + webgpu-threejs-tsl plugin kurulu', '-', '-'),
    'manychat': (R, '-', 'IG otomasyon servisi; hesap ister, kapsam dışı', '-', '-'),
    'img2threejs': (D, 'blender-2', 'görselden prosedürel three.js modeli (3D); blender-2 ile karşılaştırılsın', 'img2threejs/img2threejs', 'Apache-2.0'),
    'tsc': (KU, 'CC', 'npx tsc --noEmit; frontend kapıları tip denetimi yapar', '-', '-'),
    'skillui': (D, 'tasarim-1', 'siteden DESIGN.md çıkarır; LİSANS YOK → lisans kapısı (yalnız REF)', 'amaancoderx/skillui', '-'),
    'context7': (KU, 'CC', 'context7-mcp + context7-cli skill kurulu', '-', '-'),
    'omniroute': (D, 'router-1', 'çok sağlayıcılı AI ağ geçidi, limitte modele geçiş', 'diegosouzapw/OmniRoute', 'MIT'),
    'openrouter': (D, 'router-1', 'OmniRoute sağlayıcısı', '-', '-'),
    'claudemem': (KU, 'CC', 'claude-mem plugin kurulu', '-', '-'),
    'headroom': (KU, 'CC', 'headroom plugin + uv aracı kurulu', '-', '-'),
    'rtk': (KU, 'CC', 'rtk kurulu (RTK.md)', '-', '-'),
    'taskobserver': (R, '-', 'repo bulunamadı; düzeltme yakalama feedback belleği + claude-mem ile var', '-', '-'),
    'textobserver': (R, '-', 'Task Observer ile aynı; repo bulunamadı', '-', '-'),
    'sqlitevec': (R, '-', 'claude-mem iç yapısı; ayrı kurulum gerekmez', '-', '-'),
    'slashbrag': (D, 'animasyon-1', 'projeyi 20 sn lansman videosuna çevirir (HyperFrames kurulu)', 'latent-spaces/brag', 'MIT'),
    'latentspacesbrag': (D, 'animasyon-1', '/brag plugin deposu', 'latent-spaces/brag', 'MIT'),
    'bragbrag': (D, 'animasyon-1', '/brag plugin skill\'i', 'latent-spaces/brag', 'MIT'),
    'uiuxpromax': (KU, 'CC', 'ui-ux-pro-max skill kurulu', '-', '-'),
    'uipro': (KU, 'CC', 'ui-ux-pro-max kurucusu; skill zaten kurulu', '-', '-'),
    'awesomeclaudedesign': (D, 'tasarim-1', '68 hazır DESIGN.md', 'VoltAgent/awesome-claude-design', 'MIT'),
    'designmdchrome': (D, 'tasarim-1', 'Chrome eklentisi: siteden DESIGN.md (Ömer kurar)', 'bergside/design-md-chrome', 'MIT'),
    'designmdgeneratorbytypeui': (D, 'tasarim-1', 'token tabanlı DESIGN.md üretici', '-', '-'),
    'designmotionprinciples': (D, 'animasyon-1', 'hareket/easing ilkeleri skill\'i', 'kylezantos/design-motion-principles', 'MIT'),
    'screenshottocode': (D, 'tasarim-1', 'ekran görüntüsünden kod; API anahtarı ister', 'abi/screenshot-to-code', 'MIT'),
    'apianything': (R, '-', 'sitelerin iç API\'sini tersine mühendislik; hizmet şartı riski (camofox emsali); agent-browser + chrome-devtools + scrapling karşılar', 'goodnight000/api-anything', 'MIT'),
    'cstack': (R, '-', '★50, aynı yazarın deposu; kanıt yok', 'goodnight000/cstack', 'MIT'),
    'vite': (KU, 'CC', 'vite skill kurulu', '-', '-'),
    'security': (KU, 'CC', 'security-guidance plugin + semgrep kurulu', '-', '-'),
    'contextmode': (KU, 'CC', 'context-mode plugin kurulu', '-', '-'),
    'manifest': (D, 'router-1', 'oturum maliyet takibi; mnfst/llm-gateway (MIT ★7.5k) olabilir, doğrulanmadı', '-', '-'),
    'skillbus': (R, '-', 'repo bulunamadı; skill zinciri departman-* yönlendirmesiyle var', '-', '-'),
    'agentskills': (KU, 'CC', 'agent-skills plugin (addyosmani) kurulu', '-', '-'),
    'redgreenrefactor': (KU, 'CC', 'superpowers TDD + agent-skills test-driven-development', '-', '-'),
    'ollama': (R, '-', 'yerel model kullanmıyoruz', '-', '-'),
    'skillspector': (KU, 'CC', 'SkillSpector CLI kurulu (~/.local/bin)', '-', '-'),
    'reticle': (R, '-', 'repo bulunamadı; bitti-doğrulama verification-before-completion + frontend görsel QA karşılar', '-', '-'),
    'chisle': (R, '-', 'kısa yazım + YAGNI = ponytail + caveman kurulu; lisans "other"', 'JayPokale/Chisle', 'other'),
    'uiskills': (KU, 'CC', 'ui-skills-root skill kurulu', 'ibelick/ui-skills', 'MIT'),
    'antislop': ('UYARLA', 'CC+claude.ai(kendi)', 'departman-frontend Kapılar: TS lint oxlint + anti-slop kural seti, proje devDependency, sürüm sabit', 'dmmulroy/anti-slop', 'MIT'),
    'oxlint': ('UYARLA', 'CC+claude.ai(kendi)', 'anti-slop satırıyla aynı', 'oxc-project/oxc', 'MIT'),
}
for a in ['usingagentskills', 'interviewme', 'idearefine', 'specdrivendevelopment', 'planningandtaskbreakdown',
          'incrementalimplementation', 'testdrivendevelopment', 'contextengineering', 'sourcedrivendevelopment']:
    OZEL[a] = (KU, 'CC', 'agent-skills plugin (addyosmani) içinde kurulu', 'addyosmani/agent-skills', 'MIT')

satir = []
for s in oku(BU / 'devir40.tsv'):
    satir.append([s['ad'], s['gonderi'], 'DEVİR-IG40', f"sira {s['sira40']}", f"IG-40 {s['karar40']}: {s['gerekce40']}", '-', '-'])
for s in oku(BU / 'kalan.tsv'):
    a = s['anahtar']
    if s['gonderi'].startswith('DY_SoPGKv2A'):
        k = (D, 'ruflo-1', 'Ruflo gönderisi; RUFLO-1 yürütüyor', '-', '-')
    else:
        k = OZEL.get(a) or (R, '-', 'demo istemi' if s['tur'] == 'prompt' else 'genel ürün/model/terim; kurulacak araç değil', '-', '-')
    if k[0] == 'DEVİR-IG40':
        k40 = K40[k[1]]
        k = ('DEVİR-IG40', f'sira {k[1]}', f"IG-40 {k40['karar']}: {k40['gerekce']}", k40['repo'], k40['lisans'])
    satir.append([s['ad'], s['gonderi'], *k])
    s['_k'] = k

with open(BU / 'karar18.tsv', 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, delimiter='\t')
    w.writerow(['ad', 'gonderi', 'karar', 'hedef', 'gerekce', 'repo', 'lisans'])
    w.writerows(satir)
from collections import Counter
print(len(satir), Counter(x[2] for x in satir))

if '--devir' in sys.argv:  # yalnız sona ekler, var olan anahtar tekrar eklenmez
    kol = ['anahtar', 'ad', 'tur', 'link', 'gonderi', 'iddia', 'repo', 'lisans', 'yildiz', 'push', 'arsiv', 'not']
    for s in oku(BU / 'kalan.tsv'):
        k = s.get('_k') or OZEL.get(s['anahtar'])
        if s['gonderi'].startswith('DY_SoPGKv2A'):
            k = (D, 'ruflo-1', 'Ruflo gönderisi', '-', '-')
        if not k or k[0] != D:
            continue
        f = DEVIR / f'{k[1]}.tsv'
        var = f.read_text(encoding='utf-8') if f.exists() else '\t'.join(kol) + '\n'
        if f'\n{s["anahtar"]}\t' in '\n' + var:
            continue
        link = f'https://github.com/{k[3]}' if '/' in k[3] else '-'
        var += '\t'.join([s['anahtar'], s['ad'], s['tur'], link, s['gonderi'], s['iddia'], k[3], k[4], '-', '-', '-', f'IG-18: {k[2]}']) + '\n'
        f.write_bytes(var.encode('utf-8'))
        print('devir +', k[1], s['anahtar'])
