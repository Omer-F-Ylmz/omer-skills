"""ENVANTER-1: envanter.tsv -> docs/envanter/bosluk.md (boşluk raporu). Salt okuma."""
import csv, re, collections as C
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
R = list(csv.DictReader(open(KOK / 'docs/envanter/envanter.tsv', encoding='utf-8'), delimiter='\t'))
KURULU = ('skill', 'plugin', 'plugin-skill', 'mcp', 'cli', 'ajan')
kul = lambda r: r['son_kullanim'].startswith('kullanım:')
liste = lambda xs, n=400: ', '.join(sorted(xs))[:n * 10] or '—'
o = ['# ENVANTER-1 boşluk raporu', '',
     f'Kaynak: `docs/envanter/envanter.tsv` ({len(R)} satır), üreten `tools/envanter/topla.py` + bu betik. '
     'Kullanım = son 45 günün CC transkriptlerinde Skill/subagent/mcp__ çağrısı, history.jsonl slash komutu, Desktop MCP günlüğü. '
     'claude.ai sohbetlerindeki skill kullanımı CC\'den görünmez → claude.ai tarafında "kullanılmadı" kesin değil.', '']

o += ['## 1. Sayım (tür × nerede)', '']
for t in KURULU + ('baglayici', 'arastirilan'):
    c = C.Counter(r['nerede'] for r in R if r['tur'] == t)
    o.append(f'- {t}: ' + ' · '.join(f'{k or "?"} {v}' for k, v in sorted(c.items())))

o += ['', '## 2. Departmana bağlanmamış kurulu araçlar', '']
for t in KURULU:
    xs = [r for r in R if r['tur'] == t and not r['departman']]
    o.append(f'- **{t}** {len(xs)}/{sum(1 for r in R if r["tur"] == t)}')
    if t in ('plugin', 'mcp', 'cli'):
        o.append('  - ' + liste(r['ad'] for r in xs))
    elif t in ('ajan', 'skill', 'plugin-skill'):
        on = C.Counter((r['ad'].split('-')[0] if t == 'ajan' else r['kaynak'].split('@')[0].split(' ')[0]) for r in xs)
        o.append('  - öbek (önek/kaynak): ' + ', '.join(f'{k} {v}' for k, v in on.most_common(25)))

o += ['', '## 3. Son 45 günde hiç kullanılmamış kurulu araçlar', '']
for t in KURULU:
    xs = [r for r in R if r['tur'] == t and not kul(r)]
    o.append(f'- **{t}** {len(xs)}/{sum(1 for r in R if r["tur"] == t)} kullanılmadı')
    if t in ('plugin', 'mcp', 'cli'):
        o.append('  - ' + liste(r['ad'] for r in xs))
o.append('- Kullanılan plugin/MCP/CLI: ' + liste(f"{r['ad']}({r['son_kullanim'][9:]})" for r in R if r['tur'] in ('plugin', 'mcp', 'cli') and kul(r)))
kap = [r['ad'] for r in R if r['tur'] == 'plugin' and 'KAPALI' in r['ozellik']]
o.append(f'- Kurulu ama KAPALI plugin ({len(kap)}): ' + liste(kap))

o += ['', '## 4. İki tarafta eşit olmayanlar', '']
for t, ad in (('mcp', 'MCP'), ('cli', 'CLI')):
    for n in ('CC', 'Desktop'):
        xs = [r['ad'] for r in R if r['tur'] == t and r['nerede'] == n]
        o.append(f'- {ad} yalnız {n} ({len(xs)}): ' + liste(xs))
sk = [r for r in R if r['tur'] == 'skill' and r['nerede'] == 'CC']
o.append(f'- skill yalnız CC ({len(sk)}; claude.ai\'ye zip gerekir) öbek: ' + ', '.join(f'{k} {v}' for k, v in C.Counter(r['kaynak'] for r in sk).most_common()))
ps = [r for r in R if r['tur'] == 'plugin-skill' and 'senkron kopya var' not in r['eksik_taraf']]
o.append(f'- plugin skill\'i claude.ai\'de kopyası olmayan: {len(ps)}/{sum(1 for r in R if r["tur"] == "plugin-skill")} '
         '(plugin skill\'leri claude.ai\'ye yalnız zip ile gider)')
ps_kul = [r['ad'] for r in ps if kul(r)]
o.append(f'  - bunlardan CC\'de son 45 günde KULLANILANLAR (claude.ai\'ye taşınmaya ilk aday, {len(ps_kul)}): ' + liste(ps_kul))
o.append(f'- ajan: {sum(1 for r in R if r["tur"] == "ajan")} CC alt ajanı; claude.ai\'de alt ajan yok, '
         f'{sum(1 for r in R if r["tur"] == "ajan" and "ajanlar referansı" in r["eksik_taraf"])} tanesi departman-*/ajanlar ile talimat olarak okunur.')
eski = [f"{r['ad']} {r['surum']} ({r['eksik_taraf'].split('repo ')[-1]})" for r in R if 'CC eski' in r['eksik_taraf'] and r['tur'] == 'plugin']
o.append('- Kendi plugin\'leri CC\'de eski sürüm (onay betiği koşmadı): ' + liste(eski))
yok = [f"{r['ad']}({r['kaynak']})" for r in R if r['tur'] in KURULU and r['nerede'] in ('yok', '')]
o.append(f'- Envanter.json\'da var, kurulu bulunamadı ({len(yok)}): ' + liste(yok))
o.append(f'- claude.ai bağlayıcıları: CC araç listesinde claude.ai bağlayıcısı görünmüyor; yalnız mcp-needs-auth-cache adları: '
         + liste(r['ad'] for r in R if r['tur'] == 'baglayici') + '. Tam liste claude.ai Ayarlar > Bağlayıcılar\'dan Ömer\'in bakmasını gerektirir.')

o += ['', '## 5. Departman Dizin\'inde olmayan alt ajanlar (önek öbekleri)', '']
ONEK = {'fe': 'frontend', 'qa': 'test-qa', 'sec': 'guvenlik', 'db': 'veri-db', 'dn': 'backend-dotnet', 'be': 'backend-dotnet',
        'git': 'surec-git-yayin', 'pln': 'surec-plan', 'inc': 'surec-inceleme', 'dok': 'belge', 'ara': 'arastirma-ogrenme',
        'ajn': 'surec-ajan-arac', 'vrm': 'verimlilik'}
dep_yok = C.Counter(r['ad'].split('-')[0] for r in R if r['tur'] == 'ajan' and not r['departman'] and re.match(r'^[a-z]{2,4}-', r['ad']))
o.append('- Departmanı olan önek (Dizin\'e eklenebilir): ' + ', '.join(f'{k}- {v} → {ONEK[k]}' for k, v in dep_yok.most_common() if k in ONEK))
o.append('- Departmanı OLMAYAN önek (müdür yok): ' + ', '.join(f'{k}- {v}' for k, v in dep_yok.most_common() if k not in ONEK)
         + ' — `is-arac.md` §Departmansız işler bunlara giriş sırası verir.')

(KOK / 'docs/envanter/bosluk.md').write_text('\n'.join(o) + '\n', encoding='utf-8', newline='\n')
print('\n'.join(o)[:6000])
