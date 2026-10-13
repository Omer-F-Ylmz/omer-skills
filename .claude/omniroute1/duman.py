"""OMNIROUTE-2 d3: kesilme kök neden kanıtı — ham yanıttan finish_reason + usage (değer basılmaz).
  python .claude/omniroute1/duman.py <örnek_sayısı> <model|combo>,<max_tokens>[,<reasoning_effort>] ...
Tavan: örnek_sayısı × varyant ≤ 12 çağrı."""
import json, sys, time, urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from pilot import ISTEM, env_oku, ornekler

n, varyant = int(sys.argv[1]), [v.split(",") for v in sys.argv[2:]]
assert n * len(varyant) <= 12
print("ornek\tmodel\tmax\tefor\tdurum\tms\tyanit_model\tfinish\tusage\tuzunluk\tson")
for ad, metin in ornekler()[:n]:
    for v in varyant:
        govde = {"model": v[0], "messages": [{"role": "user", "content": ISTEM + metin}], "max_tokens": int(v[1])}
        if len(v) > 2:
            govde["reasoning_effort"] = v[2]
        q = urllib.request.Request("http://127.0.0.1:20128/v1/chat/completions", method="POST", data=json.dumps(govde).encode(),
                                   headers={"content-type": "application/json", "authorization": f"Bearer {env_oku('OMNIROUTE_KEY')}"})
        t = time.time()
        try:
            j = json.load(urllib.request.urlopen(q, timeout=120))
            c = j["choices"][0]
            y = c["message"].get("content") or ""
            print(ad, v[0], v[1], v[2] if len(v) > 2 else "-", 200, int((time.time() - t) * 1000), j.get("model", "?"),
                  c.get("finish_reason"), json.dumps(j.get("usage"), ensure_ascii=False), len(y), repr(y[-30:]), sep="\t", flush=True)
        except Exception as e:
            print(ad, v[0], v[1], "-", f"{type(e).__name__} {getattr(e, 'code', '')}", int((time.time() - t) * 1000), sep="\t", flush=True)
