"""MCP-HAFIF-2: kosucu -p env (DISABLE_AUTOUPDATER + CLAUDE_MEM_INTERNAL) önce/sonra — kol başına 2, tam 4 claude -p (tavan 4).
Girdi jetonu (input+cache_creation+cache_read), süre, kendi süreç ağacımızda görülen git.exe sayısı (temp_git klonu; paralel
oturumların temp_* klasörleri sayıma karışmasın diye klasör değil süreç sayılır). python tools/olcum/env_ab.py <cikti.tsv>"""
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from mcp_hafif_kabul import anlik, torunlar  # noqa: E402

# $0.50 tavanı ilk turda aşılıyordu (tek "tamam" ≈ $0.66 → error_max_budget_usd, usage sıfır): d4 ölçümü geçersizdi
BUTCE = "2.00"


def sonuc(stdout):
    d = json.loads(stdout)
    if d.get("is_error"):
        raise SystemExit(f"claude -p hata: {d.get('subtype')} {d.get('errors') or str(d.get('result'))[:80]}")
    u = d.get("usage", {})
    girdi = u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0) + u.get("cache_read_input_tokens", 0)
    if not girdi:
        raise SystemExit(f"usage boş: {str(d.get('result'))[:80]}")  # plan limiti düz metin döner
    return girdi, u.get("cache_creation_input_tokens", 0)


def kos(ek_env):
    env = {k: v for k, v in os.environ.items()
           if k not in ("ANTHROPIC_BASE_URL", "ANTHROPIC_API_KEY", "DISABLE_AUTOUPDATER", "CLAUDE_MEM_INTERNAL")}
    env.update(ek_env, BROWSER="none")
    git = set()
    with tempfile.TemporaryDirectory(prefix="envab-", ignore_cleanup_errors=True) as bos:
        t = time.time()
        p = subprocess.Popen(["claude", "-p", "Sadece 'tamam' yaz.", "--output-format", "json", "--max-budget-usd", BUTCE],
                             env=env, cwd=bos, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True,
                             encoding="utf-8", creationflags=0x08000000)
        while p.poll() is None and time.time() - t < 300:
            d = anlik()
            git |= {q for q in torunlar(d, p.pid) if d[q][1].lower() == "git.exe"}
            time.sleep(1)
        out = p.communicate(timeout=60)[0]
        sure = time.time() - t
    return (*sonuc(out), round(sure, 1), len(git))


if __name__ == "__main__":
    satir = ["kol\tgirdi_jeton\tcache_yazma\tsure_sn\tgit_surec"]
    for ad, e in (("once", {}), ("sonra", {"DISABLE_AUTOUPDATER": "1", "CLAUDE_MEM_INTERNAL": "1"})) * 2:
        satir.append("\t".join(map(str, (ad, *kos(e)))))
        print(satir[-1], flush=True)
    Path(sys.argv[1]).write_text("\n".join(satir) + "\n", encoding="utf-8")
