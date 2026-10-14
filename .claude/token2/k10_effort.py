"""TOKEN-2 d4 K9b: --effort medium gerçek mekanik adımda (test koşma + kısa rapor), 1 claude -p, MCP'siz, doğrudan vekil (global ayara dokunmaz).
Kalite kapısı: cevap satırı betiğin kendi hesapladığı doğru değerle aynı mı. Taban (high) d3 k9_dusunme ölçümü + bu kayıttaki istek başı çıktı."""
import json, re, subprocess, sys, time
from pathlib import Path

import psutil

KOK = Path(r"C:\Projeler\omer-skills"); D = KOK / ".claude" / "token2"
TEST = "tests/test_varlik_getir.py tests/test_ucuz_alt.py"
ISTEM = (f"Run `python -m pytest -q {TEST}` with Bash, then run `python skills/blender-uretim/varlik_getir.py ara copper --kaynak ambientcg --n 3`. "
         "Reply with exactly one line: `passed=<N> sonuc=<number of items in the JSON list>`.")
dogru_p = re.search(r"(\d+) passed", subprocess.run(f"python -m pytest -q {TEST}", shell=True, cwd=KOK, capture_output=True, text=True).stdout).group(1)
while psutil.virtual_memory().percent >= 85:
    time.sleep(60)
t0 = time.time()
r = subprocess.run(["claude", "-p", "--model", "opus", "--effort", "medium", "--output-format", "json", "--max-turns", "6",
                    "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}', "--disable-slash-commands",
                    "--permission-mode", "acceptEdits", "--allowedTools", "Bash"],
                   input=ISTEM, capture_output=True, text=True, encoding="utf-8", cwd=KOK, timeout=900, shell=True,
                   creationflags=subprocess.CREATE_NO_WINDOW)
j = json.loads(r.stdout); u = j["usage"]
cevap = str(j.get("result", "")).strip()
out = {"kol": "effort_medium", "cevap": cevap[:80], "kalite": cevap.startswith(f"passed={dogru_p} sonuc=3"), "tur": j.get("num_turns"),
       "cikti": u["output_tokens"], "dusunme": u.get("output_tokens_details", {}).get("thinking_tokens"), "sure_sn": round(time.time() - t0)}
print(json.dumps(out, ensure_ascii=False))
with open(D / "k10_effort.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(out, ensure_ascii=False) + "\n")
print("BITTI")
