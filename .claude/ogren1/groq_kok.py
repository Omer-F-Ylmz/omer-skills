"""ÖĞREN-1 d2 madde 6: Groq OmniRoute kırığı kök neden (tek deneme). Anahtar basılmaz; yalnız durum kodu + hata metni başı.
  python -X utf8 .claude/ogren1/groq_kok.py"""
import json, sys, urllib.error, urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(r"C:\Projeler\omer-skills\.claude\omniroute1")))
from pilot import env_oku  # noqa: E402

U = "http://127.0.0.1:20128/v1"
H = {"authorization": f"Bearer {env_oku('OMNIROUTE_KEY')}", "content-type": "application/json", "user-agent": "curl/8.4"}


def iste(yol, govde=None):
    q = urllib.request.Request(U + yol, headers=H, data=json.dumps(govde).encode() if govde else None)
    try:
        with urllib.request.urlopen(q, timeout=60) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")


_, m = iste("/models")
groq = [x["id"] for x in json.loads(m)["data"] if "groq" in x["id"].lower()]
print("katalog groq:", groq)
for model in [*groq[:3], "ucretsiz-groq"]:
    k, y = iste("/chat/completions", {"model": model, "max_tokens": 8, "messages": [{"role": "user", "content": "ok de"}]})
    print(model, k, y[:220].replace("\n", " "))
