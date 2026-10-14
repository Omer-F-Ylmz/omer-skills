"""ÖĞREN-1 d2: kalan token araçlarının en küçük gerçek koşusu → .claude/ogren1/mini/d2.tsv (ad · rc · bayt · süre · kanıt satırı).
Ücretli çağrı yok; model çağrısı yalnız ucuz_alt (OmniRoute :free combo, 1 kez). Anahtar basılmaz.
  python -X utf8 .claude/ogren1/mini_d2.py"""
import json, subprocess, sys, tempfile, time, urllib.request, zipfile
from pathlib import Path

KOK = Path(r"C:\Projeler\omer-skills")
sys.path.insert(0, str(KOK / ".claude/omniroute1"))
from pilot import env_oku  # noqa: E402

MINI = KOK / ".claude/ogren1/mini"
TMP = Path(tempfile.mkdtemp(prefix="ogren1-"))
zipfile.ZipFile(KOK / "dist/yukle-10b/replace/headroom-compress.zip").extractall(TMP)
(TMP / "istem.md").write_text("Bu dosyadaki araç kartını tek cümleyle özetle.", encoding="utf-8")
OMNI = "http://127.0.0.1:20128"
H = f"-H \"authorization: Bearer {env_oku('OMNIROUTE_KEY')}\""
JSONL = KOK / ".kos/kopru/ogren/ozet-token.jsonl"

ISLER = [
    ("graphify_sor", 'python -X utf8 .kos/kopru/graphify_sor.py "env_oku"'),
    ("graphify-query-ayni", 'graphify query "env_oku"'),
    ("harita", "python -c \"import pathlib;print(sum(p.stat().st_size for p in pathlib.Path('.kos/kopru/harita').glob('*.md')),'B harita')\""),
    ("claude-mem-search", 'curl -s -m 10 "http://127.0.0.1:37777/api/search?query=headroom&limit=5"'),
    ("claude-mem-timeline", 'curl -s -m 10 "http://127.0.0.1:37777/api/timeline?anchor=26196&depth_before=2&depth_after=2"'),
    ("claude-usage", "claude-usage today"),
    ("token_olc", "python -X utf8 tools/token_olc.py --help"),
    ("model_sec", "python -X utf8 tools/model_sec.py --help"),
    ("headroom-compress-ham", f"python -c \"print(open(r'{JSONL}',encoding='utf8').read())\""),
    ("headroom-compress", f'python -X utf8 "{TMP}/headroom-compress/scripts/compress.py" "{JSONL}" --oran 0.3'),
    ("rtk-read-ham", "python -c \"print(open('tools/ucuz_alt.py',encoding='utf8').read())\""),
    ("rtk-read", "rtk read tools/ucuz_alt.py"),
    ("rtk-read-aggressive", "rtk read -l aggressive tools/ucuz_alt.py"),
    ("omni-cache", f"curl -s -m 10 {H} {OMNI}/api/cache"),
    ("omni-compression", f"curl -s -m 10 {H} {OMNI}/api/compression/language-packs"),
    ("omni-context-rtk", f"curl -s -m 10 {H} {OMNI}/api/context/rtk/config"),
    ("cli-cost-usage", "omniroute usage --help"),
    ("cli-compression", "omniroute compression --help"),
    ("ucuz_alt", f'python -X utf8 tools/ucuz_alt.py "{TMP}/istem.md" "{TMP}/cikti.md" docs/ogren/token.md'),
]

satir = ["ad\trc\tbayt\tsure_s\tkanit"]
for ad, komut in ISLER:
    t = time.time()
    try:
        p = subprocess.run(komut, shell=True, cwd=KOK, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=180)
        rc, cik = p.returncode, p.stdout + p.stderr
    except subprocess.TimeoutExpired:
        rc, cik = "zaman", ""
    (MINI / f"d2-{ad}.txt").write_text(cik.replace(env_oku("OMNIROUTE_KEY"), "***"), encoding="utf-8")
    kanit = next((s.strip() for s in cik.splitlines() if s.strip()), "")[:140].replace("\t", " ")
    satir.append(f"{ad}\t{rc}\t{len(cik.encode())}\t{time.time() - t:.1f}\t{kanit}")
(MINI / "d2.tsv").write_text("\n".join(satir) + "\n", encoding="utf-8")
print("\n".join(satir))
