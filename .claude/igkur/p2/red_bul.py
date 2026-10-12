"""IG-40-KUR d2 alt ajan izin reddini transcript'lerden bulur (salt okuma)."""
import json, glob, os, sys, collections

KOK = 'C:/Users/pc/.claude/projects/C--Projeler-omer-skills'
ADAY = sys.argv[1:]


def satirlar(yol):
    with open(yol, encoding='utf-8', errors='ignore') as f:
        for s in f:
            try:
                yield json.loads(s)
            except ValueError:
                pass


def metin(c):
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        return ' '.join(metin(x.get('text') or x.get('content') or '') if isinstance(x, dict) else str(x) for x in c)
    return str(c)


for sid in ADAY:
    ana = f'{KOK}/{sid}.jsonl'
    ilk = next((metin(o['message']['content'])[:160] for o in satirlar(ana)
                if o.get('type') == 'user' and o.get('message')), '')
    print('==', sid, '|', ilk.replace('\n', ' '))
    dosyalar = [ana] + glob.glob(f'{KOK}/{sid}/subagents/*.jsonl')
    say = collections.Counter()
    for d in dosyalar:
        araclar = {}
        for o in satirlar(d):
            m = o.get('message') or {}
            c = m.get('content')
            if not isinstance(c, list):
                continue
            for b in c:
                if not isinstance(b, dict):
                    continue
                if b.get('type') == 'tool_use':
                    araclar[b.get('id')] = (b.get('name'), json.dumps(b.get('input'), ensure_ascii=False)[:160])
                if b.get('type') == 'tool_result' and b.get('is_error'):
                    t = metin(b.get('content'))
                    if any(k in t.lower() for k in ('permission', 'denied', 'izin', 'not allowed', 'reject')):
                        ad, girdi = araclar.get(b.get('tool_use_id'), ('?', ''))
                        anahtar = (os.path.basename(d)[:30], ad, t[:400].replace('\n', ' '))
                        if say[anahtar] == 0:
                            print('  ', o.get('timestamp', '')[:19], *anahtar, '| girdi:', girdi)
                        say[anahtar] += 1
    for k, v in say.items():
        if v > 1:
            print('   x', v, k[0], k[1])
