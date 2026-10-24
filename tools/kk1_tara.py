"""KAYNAK-KUTUPHANE-1 parca 1: site basina HTTP tarama (robots/sitemap saygili), kutuphane + GitHub tespiti.
Cikti: docs/kaynak-kutuphane/site/<host>.json (ham) ; ozet yazimi kk1_yaz.py'de."""
import re, json, sys, time, subprocess, urllib.request, urllib.parse, urllib.robotparser, concurrent.futures as cf
SITELER = """github.com mcp.apify.com claude.ai hub.docker.com ollaya.dev github.con inkd.in insforge.dev ko-f1.con last.fn freesound.org learn.code lnkd.in o1laya.dev 9gag.com api.skyfire.xyz crowdin.com eata.typeracer.con example.com lab.pentestit.ru last.fa ncp.apify.com scratch.ait.edu tast.fn api.groq.com astral.sh code.claude.com lamafactory.readthedocs.io tast.fa tryhacke.con xyz.supabase.co api.apify.com austinmarchese.tech bitbucket.org cdn.acttvepteces.con cdn.jsdelivr.net data.typeracer.con en.gravatar.con github.cm hermes-agent.nousresearch.com httrack.com huggingface.co kfinance.kensho.com lamafactory.readthedocs.jo mcp.apify.con nautilustrader.io ollama.com open.spotify.com premium.mcp.pitchbook.com rocm.docs.amd.com skills.sh skool.com t.me t.ne trello.com trendyol.com w.codecadeay.con""".split()
UA = 'Mozilla/5.0 (omer-skills kaynak-kutuphane-1; contact omery3899@gmail.com)'
LIBS = {'three.js': r'THREE\.REVISION|WebGLRenderer|from"three"|"three"', 'gsap': r'gsap|ScrollTrigger', 'lenis': r'lenis',
 'framer-motion/motion': r'framer-motion|motion/react|"motion"', 'react-spring': r'react-spring', 'lottie': r'lottie', 'rive': r'rive\.app|rive-canvas|@rive-app',
 'spline': r'splinetool|@splinetool', 'r3f': r'@react-three|react-three-fiber', 'tailwind': r'tailwind', 'radix': r'@radix-ui|radix-ui', 'shadcn': r'shadcn',
 'next.js': r'/_next/|__NEXT_DATA__', 'astro': r'astro-island|/_astro/', 'nuxt/vue': r'/_nuxt/|data-v-', 'svelte': r'svelte', 'ogl': r'\bogl\b', 'matter-js': r'matter-js|Matter\.Engine',
 'webgl-shader': r'gl_FragColor|fragmentShader|precision (?:high|medium)p', 'codemirror/monaco': r'monaco-editor|codemirror', 'lucide': r'lucide', 'tsl/webgpu': r'WebGPURenderer|three/tsl'}
def get(u, n=1_500_000):
    r = urllib.request.Request(u, headers={'User-Agent': UA, 'Accept-Language': 'en'})
    with urllib.request.urlopen(r, timeout=20) as f:
        return f.read(n).decode('utf8', 'replace'), f.geturl()
def tara(host):
    o = {'host': host, 'durum': 'ok', 'libs': {}, 'github': [], 'npm': [], 'sitemap_url': 0, 'sitemap_ornek': [], 'robots': '', 'alt_sayfa_izinli': None}
    try:
        html, final = get(f'https://{host}/')
    except Exception as e:
        o['durum'] = f'hata: {type(e).__name__} {str(e)[:60]}'; return o
    base = final; o['final'] = final
    rp = urllib.robotparser.RobotFileParser()
    try:
        time.sleep(1); rt, _ = get(urllib.parse.urljoin(base, '/robots.txt'), 100_000); rp.parse(rt.splitlines()); o['robots'] = 'var'
        sm = re.findall(r'(?im)^sitemap:\s*(\S+)', rt)
    except Exception: sm = []; o['robots'] = 'yok'; rp.parse([])
    o['alt_sayfa_izinli'] = rp.can_fetch(UA, base)
    srcs = re.findall(r'<script[^>]+src=["\']([^"\']+)', html)
    corpus = html; js = [urllib.parse.urljoin(base, s) for s in srcs][:6]
    for j in js:
        if not o['alt_sayfa_izinli']: break
        try: time.sleep(1); corpus += get(j, 1_200_000)[0]
        except Exception: pass
    for k, rx in LIBS.items():
        n = len(re.findall(rx, corpus, re.I))
        if n: o['libs'][k] = n
    o['github'] = sorted(set(m.lower() for m in re.findall(r'github\.com/([\w.-]+/[\w.-]+)', corpus) if not m.lower().startswith(('sponsors','topics','features','orgs','marketplace'))))[:6]
    o['npm'] = sorted(set(re.findall(r'npmjs\.com/package/((?:@[\w.-]+/)?[\w.-]+)', corpus)))[:6]
    o['baslik'] = (re.search(r'<title[^>]*>([^<]{0,120})', html) or [0, ''])[1].strip()
    o['aciklama'] = (re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']{0,200})', html, re.I) or [0, ''])[1]
    urls = []
    for s in (sm or [urllib.parse.urljoin(base, '/sitemap.xml')])[:2]:
        try:
            time.sleep(1); x, _ = get(s, 2_000_000)
            sub = re.findall(r'<loc>\s*([^<\s]+\.xml[^<\s]*)', x)
            urls += re.findall(r'<loc>\s*([^<\s]+)', x) if not sub else []
            for s2 in sub[:2]:
                time.sleep(1); x2, _ = get(s2, 2_000_000); urls += re.findall(r'<loc>\s*([^<\s]+)', x2)
        except Exception: pass
    urls = [u for u in dict.fromkeys(urls) if not u.endswith('.xml')]
    o['sitemap_url'] = len(urls); o['sitemap_ornek'] = urls[:8]
    return o
def gh(repo):
    try:
        r = subprocess.run(['gh', 'repo', 'view', repo, '--json', 'licenseInfo,stargazerCount,pushedAt,description,isArchived'], capture_output=True, text=True, encoding='utf8', timeout=30)
        d = json.loads(r.stdout); return {'repo': repo, 'lisans': (d.get('licenseInfo') or {}).get('key') or 'YOK', 'yildiz': d['stargazerCount'], 'son': d['pushedAt'][:10], 'ozet': (d.get('description') or '')[:100]}
    except Exception: return {'repo': repo, 'lisans': '?', 'yildiz': 0, 'son': '', 'ozet': ''}
if __name__ == '__main__':
    out = {}
    with cf.ThreadPoolExecutor(8) as ex:
        for o in ex.map(tara, SITELER): out[o['host']] = o
    repos = sorted({r for o in out.values() for r in o['github']})
    with cf.ThreadPoolExecutor(6) as ex: info = {i['repo']: i for i in ex.map(gh, repos)}
    for o in out.values(): o['repo_bilgi'] = [info[r] for r in o['github']]
    json.dump(out, open('docs/kaynak-kutuphane/tara-parca5.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    print(len(out), 'site;', sum(o['durum'] != 'ok' for o in out.values()), 'hata;', len(repos), 'repo')
