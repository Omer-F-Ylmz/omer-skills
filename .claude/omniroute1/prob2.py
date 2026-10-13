"""OMNIROUTE-2 d2: aday modellere tek kısa istek (tavan: liste boyu, ≤16 çağrı; ~30 token/çağrı). Değer basılmaz.
  python .claude/omniroute1/prob2.py > prob2.tsv"""
import json, re, sys, time, urllib.error, urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from pilot import env_oku

ADAY = ["gemini/gemini-3.1-pro-preview", "gemini/gemini-2.5-pro", "gemini/gemini-3.7-flash", "gemini/gemini-3-flash-preview",
        "gemini/gemini-2.5-flash", "gemini/gemini-3.1-flash-lite", "gemini/gemini-2.5-flash-lite",
        "moonshot/kimi-k3", "moonshot/kimi-k2.7-code", "moonshot/kimi-k2.6",
        "openrouter/nvidia/nemotron-3-ultra-550b-a55b:free", "openrouter/google/gemma-4-31b-it:free",
        "openrouter/thinkingmachines/inkling:free", "openrouter/nvidia/nemotron-3-super-120b-a12b:free"]
assert len(ADAY) <= 16
print("model\tdurum\tms\tyanit_model\tnot")
for m in ADAY:
    q = urllib.request.Request("http://127.0.0.1:20128/v1/chat/completions", method="POST",
                               data=json.dumps({"model": m, "messages": [{"role": "user", "content": "2+2 kaç? Yalnız sayıyı yaz."}], "max_tokens": 200}).encode(),
                               headers={"content-type": "application/json", "authorization": f"Bearer {env_oku('OMNIROUTE_KEY')}"})
    t = time.time()
    try:
        j = json.load(urllib.request.urlopen(q, timeout=90))
        y = (j["choices"][0]["message"].get("content") or "").strip()
        print(f"{m}\t200\t{int((time.time()-t)*1000)}\t{j.get('model','?')}\t{y[:20]!r}", flush=True)
    except urllib.error.HTTPError as e:
        g = e.read().decode("utf-8", "replace")
        g = re.sub(r"[A-Za-z0-9_\-]{28,}", "<MASK>", g).replace("\n", " ")  # olası anahtar parçası maskeli
        print(f"{m}\t{e.code}\t{int((time.time()-t)*1000)}\t-\t{g[:220]}", flush=True)
    except Exception as e:
        print(f"{m}\tERR\t{int((time.time()-t)*1000)}\t-\t{type(e).__name__}", flush=True)
