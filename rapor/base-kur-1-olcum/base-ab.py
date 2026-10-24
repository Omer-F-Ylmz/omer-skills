"""BASE-KUR-1 adim 4: base acik/kapali A/B, 3 is x 2 kol = 6 claude -p kosusu (tavan 6)."""
import json, os, shutil, subprocess, sys, time, pathlib, re

ROOT = pathlib.Path('C:/Projeler/base-olcum')
STUB = ROOT / 'stub'
OUT = pathlib.Path('C:/Projeler/omer-skills/.kos/kopru/ara/base-ab-sonuc.jsonl')
EVENTS = pathlib.Path(os.path.expanduser('~/.base-gbl/.base/hook-events.jsonl'))
CLAUDE = 'C:/Users/pc/.local/bin/claude.exe'
MODEL = 'claude-haiku-5-5'

def fixture(fx):
    if fx.exists():
        shutil.rmtree(fx)
    fx.mkdir(parents=True)
    (fx / 'calc.py').write_text(
        'def normalize(xs):\n    m = max(xs)\n    return [x / m for x in xs]\n\n\n'
        'def avg(xs):\n    return sum(xs) / (len(xs) + 1)\n', newline='\n')
    (fx / 'report.py').write_text(
        'from calc import normalize, avg\n\n\ndef run(data):\n    n = normalize(data)\n    return avg(n)\n', newline='\n')
    (fx / 'cli.py').write_text(
        'import calc\n\n\ndef main():\n    print(calc.normalize([1, 2, 4]))\n', newline='\n')
    (fx / 'test_calc.py').write_text(
        'import unittest\nfrom calc import avg, normalize\n\n\nclass T(unittest.TestCase):\n'
        '    def test_avg(self):\n        self.assertEqual(avg([2, 4]), 3)\n'
        '    def test_norm(self):\n        self.assertEqual(normalize([1, 2]), [0.5, 1.0])\n\n\n'
        'if __name__ == "__main__":\n    unittest.main()\n', newline='\n')
    (fx / 'TODO.md').write_text('- [ ] avg bolen hatasi duzelt\n- [x] normalize yazildi\n- [ ] cli icin test ekle\n', newline='\n')

JOBS = {
    'bul': 'calc.py icindeki normalize fonksiyonu hangi dosya:satirlarda cagriliyor? Yalniz dosya:satir listesi ver, baska aciklama yazma.',
    'duzelt': 'python -m unittest test_calc calistir, kirmizi testi gecirecek en kucuk duzeltmeyi calc.py icinde yap, tekrar calistirip yesil oldugunu goster.',
    'devir': 'Oturum devri: bu klasorde yapilanlari ve kalan isleri en fazla 8 satirlik devir.md dosyasina yaz (TODO.md dikkate al).',
}

def check(job, fx, text):
    if job == 'bul':
        found = set(re.findall(r'(report\.py|cli\.py):(\d+)', text))
        return sorted(found) == [('cli.py', '5'), ('report.py', '5')]
    if job == 'duzelt':
        r = subprocess.run([sys.executable, '-I', '-m', 'unittest', 'test_calc'], cwd=fx, capture_output=True, text=True)
        return r.returncode == 0
    if job == 'devir':
        p = fx / 'devir.md'
        if not p.exists():
            return False
        t = p.read_text(encoding='utf-8', errors='replace').lower()
        return 'avg' in t and 'test' in t and len(t.strip().splitlines()) <= 8

def n_events():
    return sum(1 for _ in open(EVENTS, 'rb')) if EVENTS.exists() else 0

def run(job, arm):
    fx = ROOT / f'{job}-{arm}'
    fixture(fx)
    env = dict(os.environ)
    before = n_events()
    t = time.time()
    r = subprocess.run([CLAUDE, '-p', JOBS[job], '--model', MODEL, '--output-format', 'json',
                        '--permission-mode', 'bypassPermissions', '--setting-sources', 'project', '--settings', f'C:/Projeler/base-olcum/s-{arm}.json', '--max-budget-usd', '0.4'],
                       cwd=fx, env=env, capture_output=True, text=True, timeout=240,stdin=subprocess.DEVNULL, creationflags=0x08000000)
    wall = time.time() - t
    try:
        j = json.loads(r.stdout)
    except Exception:
        j = {'result': r.stdout[-300:] + r.stderr[-300:]}
    u = j.get('usage', {})
    rec = {'is': job, 'kol': arm, 'wall_s': round(wall, 1), 'api_ms': j.get('duration_api_ms'),
           'turns': j.get('num_turns'), 'usd': j.get('total_cost_usd'),
           'in': u.get('input_tokens'), 'cache_w': u.get('cache_creation_input_tokens'),
           'cache_r': u.get('cache_read_input_tokens'), 'out': u.get('output_tokens'),
           'dogru': bool(check(job, fx, j.get('result', '') or '')), 'base_olay': n_events() - before,
           'hata': j.get('is_error')}
    with open(OUT, 'a', encoding='utf-8') as f:
        f.write(json.dumps(rec, ensure_ascii=False) + '\n')
    print(rec, flush=True)

if __name__ == '__main__':
    for job in ['bul', 'duzelt', 'devir']:
        for arm in ['acik', 'kapali']:
            run(job, arm)
