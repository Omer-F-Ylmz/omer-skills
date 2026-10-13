"""OMNIROUTE-2 d2: /v1/models sağlayıcı dökümü (değer basılmaz). Yazar: modeller2.json (id listesi).
  python .claude/omniroute1/modeller2.py"""
import collections, json, sys, urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from pilot import env_oku

q = urllib.request.Request("http://127.0.0.1:20128/v1/models", headers={"authorization": f"Bearer {env_oku('OMNIROUTE_KEY')}"})
data = json.load(urllib.request.urlopen(q, timeout=30)).get("data", [])
Path(__file__).with_name("modeller2.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
grup = collections.defaultdict(list)
for m in data:
    grup[m["id"].split("/", 1)[0] if "/" in m["id"] else "-"].append(m["id"])
print(len(data), "model;", {k: len(v) for k, v in grup.items()})
print("alanlar:", sorted({k for m in data for k in m}))
for k, v in grup.items():
    if k in ("auto", "-"):
        continue
    if k in ("openrouter", "or"):
        v = [i for i in v if i.endswith(":free")]
    print(k, len(v), " ".join(i.split("/", 1)[-1] for i in v[:60]))
