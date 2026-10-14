"""TOKEN-2 K2: 1 adımlık boş görevde ilk istek girdi token'ı — ajan_sira bayrakları, profil yok ↔ 'ajan' profili (2 claude -p)."""
import json, subprocess, sys
from pathlib import Path
KOK = Path(r"C:\Projeler\omer-skills")
sys.path.insert(0, str(KOK / "tools"))
import cc_profil
CLAUDE = r"C:\Users\pc\.local\bin\claude.exe"
TABAN = [CLAUDE, "-p", "--output-format", "json", "--model", "haiku", "--max-turns", "1", "--disable-slash-commands",
         "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}']
kollar = {"once": ["--settings", json.dumps({"promptCacheTtl": "5m"})], "sonra": cc_profil.kur("ajan", env={})[0]}
for ad, ek in kollar.items():
    r = subprocess.run(TABAN + ek, input="Yalnız 'tamam' yaz.", capture_output=True, text=True, encoding="utf-8", cwd=KOK, timeout=600)
    try:
        u = json.loads(r.stdout)["usage"]
    except Exception:
        print(ad, "HATA", r.returncode, r.stdout[:200], r.stderr[:300]); continue
    g = u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0) + u.get("cache_read_input_tokens", 0)
    satir = {"kol": ad, "girdi": g, **{k: u.get(k) for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")}}
    print(json.dumps(satir)); open(KOK / ".claude/token2/k2.jsonl", "a", encoding="utf-8").write(json.dumps(satir) + "\n")
