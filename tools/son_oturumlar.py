import glob, os, time, json, sys
fs = sorted(glob.glob(os.path.expanduser('~/.claude/projects/*/*.jsonl')), key=os.path.getmtime)[-6:]
for f in fs:
    son = ''
    try:
        with open(f, encoding='utf-8', errors='ignore') as h:
            lines = h.readlines()
        for line in reversed(lines):
            try:
                d = json.loads(line)
            except Exception:
                continue
            m = d.get('message', {})
            c = m.get('content') if isinstance(m, dict) else None
            if isinstance(c, list):
                for x in c:
                    if x.get('type') == 'tool_use':
                        son = 'ARAC ' + x.get('name', '') + ' ' + json.dumps(x.get('input', {}), ensure_ascii=True)[:120]
                        break
                    if x.get('type') == 'text':
                        son = 'METIN ' + x.get('text', '')[:120]
                        break
            if son:
                break
    except Exception as e:
        son = str(e)
    print(time.strftime('%H:%M', time.localtime(os.path.getmtime(f))), os.path.basename(os.path.dirname(f))[-22:], os.path.basename(f)[:8], son.replace('\n', ' '))
