"""MCP-HAFIF-2: kosucu -p env (DISABLE_AUTOUPDATER + CLAUDE_MEM_INTERNAL) önce/sonra — tam 2 claude -p (tavan 2, $0.50/çağrı).
Girdi jetonu (input+cache_creation+cache_read), süre, açılışta oluşan temp_git_* sayısı. python tools/olcum/env_ab.py <cikti.tsv>"""
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ONBELLEK = Path.home() / ".claude" / "plugins" / "cache"


def kos(ek_env):
    env = {k: v for k, v in os.environ.items() if k not in ("ANTHROPIC_BASE_URL", "DISABLE_AUTOUPDATER", "CLAUDE_MEM_INTERNAL")}
    env.update(ek_env, BROWSER="none")
    once = {p.name for p in ONBELLEK.glob("temp_*")}
    with tempfile.TemporaryDirectory(prefix="envab-", ignore_cleanup_errors=True) as bos:
        t = time.time()
        r = subprocess.run(["claude", "-p", "Sadece 'tamam' yaz.", "--output-format", "json", "--max-budget-usd", "0.50"],
                           env=env, cwd=bos, capture_output=True, text=True, encoding="utf-8", timeout=300, creationflags=0x08000000)
        sure = time.time() - t
    time.sleep(20)  # arka plan güncelleme klonu açılıştan sonra da sürebilir
    yeni = len({p.name for p in ONBELLEK.glob("temp_*")} - once)
    u = json.loads(r.stdout).get("usage", {})
    girdi = u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0) + u.get("cache_read_input_tokens", 0)
    return girdi, u.get("cache_creation_input_tokens", 0), round(sure, 1), yeni


if __name__ == "__main__":
    satir = ["kol\tgirdi_jeton\tcache_yazma\tsure_sn\tyeni_temp"]
    for ad, e in (("once", {}), ("sonra", {"DISABLE_AUTOUPDATER": "1", "CLAUDE_MEM_INTERNAL": "1"})):
        satir.append("\t".join(map(str, (ad, *kos(e)))))
        print(satir[-1], flush=True)
    Path(sys.argv[1]).write_text("\n".join(satir) + "\n", encoding="utf-8")
