"""ENVANTER-1: kurulu + araştırılmış araçların envanteri -> docs/envanter/envanter.tsv.

Salt okuma. Sır değeri okunmaz/yazılmaz: MCP/ayar dosyalarından yalnız ad (anahtar) alınır.
Kullanım: python tools/envanter/topla.py [--gun 45]
"""
import json, os, re, sys, glob, time, subprocess, datetime as dt
from pathlib import Path

H = Path.home()
CL = H / '.claude'
APP = Path(os.environ.get('APPDATA', H / 'AppData/Roaming')) / 'Claude'
KOK = Path(__file__).resolve().parents[2]
ANA = Path('C:/Projeler/omer-skills')  # canlı repo: Ömer'in commitsiz dosyaları dahil okunur
GUN = int(sys.argv[sys.argv.index('--gun') + 1]) if '--gun' in sys.argv else 45
SUT = ['ad', 'tur', 'nerede', 'surum', 'ozellik', 'is', 'departman', 'son_kullanim', 'eksik_taraf', 'kaynak']


def jload(p):
    try:
        return json.loads(Path(p).read_text(encoding='utf-8'))
    except Exception:
        return {}


def fm(p):
    """SKILL.md / ajan .md ön bölümünden name, description, version."""
    try:
        t = Path(p).read_text(encoding='utf-8', errors='replace')
    except Exception:
        return {}
    if not t.startswith('---'):
        return {}
    s = t.split('\n')
    out, k = {}, None
    for ln in s[1:]:
        if ln.strip() == '---':
            break
        m = re.match(r'^(\s*)([A-Za-z_-]+):\s*(.*)$', ln)
        if m and (not m.group(1) or m.group(2) == 'version'):
            k, v = m.group(2), m.group(3).strip()
            out[k] = '' if v in ('>', '|', '>-', '|-') else v.strip('"\'')
        elif k and ln.startswith((' ', '\t')):
            out[k] = (out.get(k, '') + ' ' + ln.strip()).strip()
    return out


def bol(desc):
    """açıklama -> (özellik, hangi iş)."""
    d = re.sub(r'\s+', ' ', desc or '').strip()
    m = re.search(r'\b(Use (?:this )?(?:when|for|to|after|before)|Kullan[ıi]m:|Ne zaman:)', d)
    if m:
        return d[:m.start()].strip()[:160], d[m.start():].strip()[:160]
    return d[:160], ''


satir = {}


def ekle(ad, tur, **k):
    key = (tur, ad.lower())
    r = satir.setdefault(key, {c: '' for c in SUT} | {'ad': ad, 'tur': tur, '_yer': set()})
    for c, v in k.items():
        if c == 'yer':
            r['_yer'] |= set(v)
        elif v and not r.get(c):
            r[c] = v
    return r


# 1) skill'ler: yerel CC, claude.ai senkron, repo
for p in glob.glob(str(CL / 'skills/*/SKILL.md')):
    f = fm(p); ad = f.get('name') or Path(p).parent.name
    oz, iz = bol(f.get('description'))
    ekle(ad, 'skill', yer={'CC'}, surum=f.get('version', ''), ozellik=oz, **{'is': iz}, kaynak='~/.claude/skills')
syn = glob.glob(str(CL / 'skills/synced/*/*/SKILL.md'))
for p in syn:
    f = fm(p); ad = f.get('name') or Path(p).parent.name
    oz, iz = bol(f.get('description'))
    ekle(ad, 'skill', yer={'claude.ai'}, surum=f.get('version', ''), ozellik=oz, **{'is': iz}, kaynak='claude.ai senkron')
repo_skill = set()
for p in glob.glob(str(ANA / 'skills/*/SKILL.md')):
    f = fm(p); ad = f.get('name') or Path(p).parent.name; repo_skill.add(ad.lower())
    oz, iz = bol(f.get('description'))
    ekle(ad, 'skill', surum=f.get('version', ''), ozellik=oz, **{'is': iz}, kaynak='repo skills/')

# 2) plugin'ler + plugin skill'leri + plugin MCP'leri
ip = jload(CL / 'plugins/installed_plugins.json').get('plugins', {})
acik = jload(CL / 'settings.json').get('enabledPlugins', {})
plugin_mcp = {}
for pid, kur in ip.items():
    k = kur[0] if isinstance(kur, list) else kur
    yol = Path(k.get('installPath', ''))
    pj = jload(yol / '.claude-plugin/plugin.json')
    sk = glob.glob(str(yol / 'skills/*/SKILL.md'))
    cm = glob.glob(str(yol / 'commands/*.md')); ag = glob.glob(str(yol / 'agents/*.md'))
    mcp = list(jload(yol / '.mcp.json').get('mcpServers', jload(yol / '.mcp.json')) or {})
    mcp += list((pj.get('mcpServers') or {}) if isinstance(pj.get('mcpServers'), dict) else [])
    hk = (yol / 'hooks/hooks.json').exists() or bool(pj.get('hooks'))
    durum = 'açık' if acik.get(pid) else 'KAPALI'
    oz = f"{len(sk)} skill · {len(cm)} komut · {len(ag)} ajan · {len(mcp)} MCP{' · hook' if hk else ''} · {durum} — " + re.sub(r'\s+', ' ', pj.get('description', ''))[:100]
    ekle(pid.split('@')[0], 'plugin', yer={'CC'}, surum=k.get('version', ''), ozellik=oz, kaynak=pid,
         son_kullanim=(k.get('lastUpdated') or '')[:10] and 'kur:' + k.get('lastUpdated', '')[:10])
    for p in sk:
        f = fm(p); a = f.get('name') or Path(p).parent.name
        o, i = bol(f.get('description'))
        ekle(a, 'plugin-skill', yer={'CC'}, surum=k.get('version', ''), ozellik=o, **{'is': i}, kaynak=pid + ('' if acik.get(pid) else ' (KAPALI)'))
    for m in mcp:
        plugin_mcp[m] = pid

# 3) MCP: CC (global + bu proje + plugin), Desktop
cj = jload(H / '.claude.json')
for m in cj.get('mcpServers', {}):
    ekle(m, 'mcp', yer={'CC'}, kaynak='~/.claude.json')
for prj, v in cj.get('projects', {}).items():
    if 'omer-skills' in prj.replace('\\', '/') and 'wt' not in prj:
        for m in v.get('mcpServers', {}):
            ekle(m, 'mcp', yer={'CC'}, kaynak='proje .claude.json')
for m in jload(ANA / '.mcp.json').get('mcpServers', {}):
    ekle(m, 'mcp', yer={'CC'}, kaynak='.mcp.json')
for m, pid in plugin_mcp.items():
    ekle(m, 'mcp', yer={'CC'}, kaynak='plugin ' + pid)
dcfg = jload(APP / 'claude_desktop_config.json')
for m in dcfg.get('mcpServers', {}):
    ekle(m, 'mcp', yer={'Desktop'}, kaynak='claude_desktop_config.json')
auth = jload(CL / 'mcp-needs-auth-cache.json')
for m in (auth if isinstance(auth, dict) else {}):
    ekle(m, 'baglayici', yer={'claude.ai'}, kaynak='mcp-needs-auth-cache (yetki bekliyor)')

# 4) CLI: uv tool, npm -g, cc-kopru izinli (Desktop'tan erişim)


def kos(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=120, shell=True).stdout
    except Exception:
        return ''


for ln in kos('uv tool list').splitlines():
    m = re.match(r'^([A-Za-z0-9_.-]+) v(\S+)', ln)
    if m:
        ekle(m.group(1), 'cli', yer={'CC'}, surum=m.group(2), kaynak='uv tool')
try:
    npm = json.loads(kos('npm ls -g --depth=0 --json') or '{}').get('dependencies', {})
except Exception:
    npm = {}
for a, v in npm.items():
    ekle(a, 'cli', yer={'CC'}, surum=v.get('version', ''), kaynak='npm -g')
kj = jload(ANA / 'tools/cc-kopru/kopru.json')
izinli = kj.get('izinli', [])
for a in (izinli if isinstance(izinli, list) else list(izinli)):
    a = a if isinstance(a, str) else str(a.get('ad', a))
    if not a.startswith(('_', '-')):
        ekle(a, 'cli', yer={'CC', 'Desktop'}, kaynak='cc-kopru izinli')

# 5) alt ajanlar (CC)
for p in glob.glob(str(CL / 'agents/*.md')) + glob.glob(str(ANA / '.claude/agents/*.md')):
    f = fm(p); a = f.get('name') or Path(p).stem
    o, i = bol(f.get('description'))
    ekle(a, 'ajan', yer={'CC'}, ozellik=o, **{'is': i}, surum=f.get('model', ''), kaynak='agents/')
ajan_dep = {}  # departman zip'ine gömülü ajan tanımı -> claude.ai'de referans olarak okunur
for p in glob.glob(str(ANA / 'skills/departman-*/ajanlar/*.md')):
    ajan_dep[Path(p).stem.lower()] = Path(p).parents[1].name[len('departman-'):]
repo_ver = {Path(p).parents[1].name.lower(): jload(p).get('version', '') for p in glob.glob(str(ANA / 'plugins/*/.claude-plugin/plugin.json'))}

# 6) araştırılmış (kayit.jsonl) + video envanter (444) eşlemesi
env = json.loads((ANA / 'docs/departmanlar/envanter.json').read_text(encoding='utf-8'))
dep_env = {}
adlar = {k[1] for k in satir}
for x in env:
    kisa = x['ad'].lower().split(':')[-1]  # envanter.json plugin skill'lerini "plugin:skill" yazar
    dep_env.setdefault(kisa, set()).add(x['departman'])
    if kisa not in adlar:
        ekle(x['ad'], x['tur'].lower(), kaynak='envanter.json (kurulu değil?)')
kayit = {}
for ln in (ANA / 'docs/kurulumlar/kayit.jsonl').read_text(encoding='utf-8').splitlines():
    try:
        x = json.loads(ln)
    except Exception:
        continue
    kayit[x.get('ad', '').lower()] = x
adlar = {k[1] for k in satir}
for a, x in kayit.items():
    if a and a not in adlar:
        ekle(x['ad'], 'arastirilan', ozellik=f"yargı {x.get('yargi','')} · {x.get('karar','')}"[:160],
             departman=x.get('departman', ''), son_kullanim=x.get('tarih', ''), kaynak='kurulumlar/kayit.jsonl')

# 7) departman bağı: envanter.json + departman SKILL.md/katalog/docs metninde ad geçişi
dep_tok = {}
for d in glob.glob(str(ANA / 'skills/departman-*')):
    dn = Path(d).name[len('departman-'):]
    metin = ''
    for p in [Path(d) / 'SKILL.md', Path(d) / 'katalog.md', ANA / f'docs/departmanlar/{dn}.md']:
        if p.exists():
            metin += p.read_text(encoding='utf-8', errors='replace').lower()
    dep_tok[dn] = set(re.findall(r'[a-z0-9][a-z0-9_.@-]*[a-z0-9]', metin))

# 8) kullanım: transkriptler (son GUN gün) Skill/MCP/Agent çağrıları, Desktop MCP günlükleri
son = {}
sinir = time.time() - GUN * 86400
mb = 0
RX = [(re.compile(rb'"skill":\s*"([^"]{2,80})"'), 's'), (re.compile(rb'mcp__([A-Za-z0-9-]+(?:_[A-Za-z0-9-]+)*?)__'), 'm'),
      (re.compile(rb'"subagent_type":\s*"([^"]{2,80})"'), 'a')]
for p in glob.glob(str(CL / 'projects/*/*.jsonl')):
    st = os.stat(p)
    if st.st_mtime < sinir:
        continue
    mb += st.st_size
    gun = dt.date.fromtimestamp(st.st_mtime).isoformat()
    b = Path(p).read_bytes()
    for rx, t in RX:
        for a in set(rx.findall(b)):
            a = a.decode('utf-8', 'replace').lower()
            if t == 'm' and a.startswith('plugin_'):
                a = a.split('_', 2)[-1]
            for n in {a, a.split(':')[-1]}:
                if son.get(n, '') < gun:
                    son[n] = gun
for p in glob.glob(str(APP / 'logs/mcp-server-*.log')):
    n = Path(p).stem[len('mcp-server-'):].lower()
    gun = dt.date.fromtimestamp(os.stat(p).st_mtime).isoformat()
    son['desktop:' + n] = max(son.get('desktop:' + n, ''), gun)
bashk = {}  # Bash günlüğü: komut başı kelimesi -> son gün (CLI kullanımı)
for ln in (CL / 'bash-commands.log').read_text(encoding='utf-8', errors='replace').splitlines():
    m = re.match(r'^\[(\d{4}-\d\d-\d\d)T', ln)
    if not m:
        continue
    for seg in re.split(r'[;|&()]+|\$\(', ln[m.end():]):
        w = seg.split()
        while w and (w[0] in ('rtk', 'proxy', 'time', 'timeout', 'env', 'sudo', 'exec') or '=' in w[0] or w[0].isdigit()):
            w = w[1:]
        if w:
            k = Path(w[0].strip('"\'')).stem.lower()
            bashk[k] = max(bashk.get(k, ''), m.group(1))


def cli_adlari(a):
    b = a.lower().split('/')[-1]
    return {b, re.sub(r'-(cli|ai|mcp)$', '', b), b.rstrip('y') if b.endswith('yy') else b, b.replace('-cli', '')}


hist = {}
for ln in (CL / 'history.jsonl').read_text(encoding='utf-8', errors='replace').splitlines():
    try:
        x = json.loads(ln)
    except Exception:
        continue
    g = dt.date.fromtimestamp(x.get('timestamp', 0) / 1000).isoformat() if x.get('timestamp') else ''
    for a in re.findall(r'(?:^|\s)/([a-z0-9][a-z0-9:_-]+)', x.get('display', '')):
        a = a.split(':')[-1]
        hist[a] = max(hist.get(a, ''), g)

# 9) birleştir + yaz
for (tur, a), r in satir.items():
    y = r.pop('_yer')
    if tur in ('skill',):
        cc = 'CC' in y or 'claude.ai' in y  # senkron skill CC'de anthropic-skills: olarak da görünür
        ai = 'claude.ai' in y
        r['nerede'] = 'ikisi' if ai else ('CC' if cc else 'yok')
        r['eksik_taraf'] = '' if ai else ('claude.ai' if cc else 'ikisi (yalnız repo)' if a in repo_skill else 'kurulu değil')
    elif tur in ('plugin', 'plugin-skill', 'ajan'):
        r['nerede'] = 'CC'
        r['eksik_taraf'] = 'claude.ai' + (' (senkron kopya var)' if tur == 'plugin-skill' and ('skill', a) in satir and satir[('skill', a)].get('nerede') == 'ikisi' else '')
    elif tur in ('mcp', 'cli'):
        d, c = 'Desktop' in y, 'CC' in y
        r['nerede'] = 'ikisi' if d and c else ('Desktop' if d else 'CC' if c else 'yok')
        r['eksik_taraf'] = '' if d and c else ('CC' if d else 'Desktop/claude.ai' if c else 'kurulu değil')
    elif tur == 'baglayici':
        r['nerede'] = 'claude.ai'; r['eksik_taraf'] = 'CC (görünmüyor)'
    else:
        r['nerede'] = r['nerede'] or ('yok' if tur == 'arastirilan' else '')
    deps = set(dep_env.get(a, set()) | dep_env.get(a.split(':')[-1], set()))
    for dn, tok in dep_tok.items():
        if a in tok or a.split(':')[-1] in tok:
            deps.add(dn)
    if a.startswith('departman-'):
        r['departman'] = a[len('departman-'):]
    elif tur == 'ajan' and a in ajan_dep:
        r['departman'] = ajan_dep[a]
        r['eksik_taraf'] = f'claude.ai (yalnız departman-{ajan_dep[a]}/ajanlar referansı)'
    if not r['departman']:
        r['departman'] = ','.join(sorted(deps))
    if tur in ('plugin', 'plugin-skill') and r['kaynak'].split(' ')[0].endswith('@omer-skills'):
        rv = repo_ver.get(a, '')
        if rv and rv != r['surum']:
            r['eksik_taraf'] += f' · CC eski: repo {rv}'
    if not r['son_kullanim'] or r['son_kullanim'].startswith('kur:'):
        u = max([son.get(a, ''), hist.get(a, ''), son.get('desktop:' + a, '')]
                + ([bashk.get(n, '') for n in cli_adlari(a)] if tur == 'cli' else []))
        r['son_kullanim'] = ('kullanım:' + u) if u else r['son_kullanim']
    kx = kayit.get(a)
    if kx and not r['son_kullanim']:
        r['son_kullanim'] = 'kayıt:' + kx.get('tarih', '')

# plugin'in kullanımı/departmanı = skill'leri ve MCP'lerinin en yenisi/birleşimi
for (tur, a), r in satir.items():
    if tur in ('plugin-skill', 'mcp'):
        pid = r['kaynak'].replace('plugin ', '').split(' ')[0]
        p = satir.get(('plugin', pid.split('@')[0].lower()))
        if p and pid.startswith(p['kaynak']):
            pu = p['son_kullanim'] if p['son_kullanim'].startswith('kullanım:') else ''
            if r['son_kullanim'].startswith('kullanım:') and r['son_kullanim'] > pu:
                p['son_kullanim'] = r['son_kullanim']
            p['departman'] = ','.join(sorted(set(filter(None, (p['departman'] + ',' + r['departman']).split(',')))))

cikti = KOK / 'docs/envanter/envanter.tsv'
cikti.parent.mkdir(parents=True, exist_ok=True)
temiz = lambda v: re.sub(r'[\t\r\n]+', ' ', str(v))
srt = sorted(satir.values(), key=lambda r: (r['tur'], r['ad'].lower()))
with open(cikti, 'w', encoding='utf-8', newline='') as fo:
    fo.write('\t'.join(SUT) + '\n')
    for r in srt:
        fo.write('\t'.join(temiz(r[c]) for c in SUT) + '\n')
import collections as C
print('satir', len(srt), 'transkript_mb', mb // 2**20, 'synced', len(syn))
print('tur', dict(C.Counter(r['tur'] for r in srt)))
print('nerede', dict(C.Counter((r['tur'], r['nerede']) for r in srt)))
print('depsiz', dict(C.Counter(r['tur'] for r in srt if not r['departman'])))
print('kullanimsiz', dict(C.Counter(r['tur'] for r in srt if not r['son_kullanim'].startswith('kullanım:'))))
