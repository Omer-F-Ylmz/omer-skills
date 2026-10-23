"""OmniRoute ham hakem yanıtlarını kaydeder (ayikla testi için): python omni_ham.py <kurul-girdi.jsonl> <n> <cikti.jsonl>"""
import json
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import kurul  # noqa: E402
import ucretsiz_havuz as uh  # noqa: E402

gir, n, cik = sys.argv[1], int(sys.argv[2]), sys.argv[3]
for x in list(open(gir, encoding="utf-8"))[:n]:
    k = json.loads(x)
    g = {"model": "cc-ucuz-free", "messages": [{"role": "user", "content": kurul.istem(k["state"])}], "max_tokens": 1500, "reasoning_effort": "low"}
    q = urllib.request.Request(uh._url("omniroute"), json.dumps(g).encode(), {"Content-Type": "application/json", "User-Agent": "curl/8",
                               "Authorization": "Bearer " + uh._anahtar("omni")})
    try:
        j = json.load(urllib.request.urlopen(q, timeout=70))
    except Exception as e:  # noqa: BLE001
        j = {"hata": str(e)[:200]}
    open(cik, "a", encoding="utf-8").write(json.dumps({"id": k["id"], "ham": j}, ensure_ascii=False) + "\n")
    print(k["id"], "ok" if "choices" in j else j, flush=True)
