"""MEM-FIX-4: mem-yedek zincirindeki her modeli ve combo'yu birer kez yoklar (ücretsiz, en çok 5 çağrı)."""
import json, sys, urllib.request, urllib.error, winreg

URL = "http://127.0.0.1:20128/v1/chat/completions"
with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as k:
    KEY = winreg.QueryValueEx(k, "OMNIROUTE_KEY")[0]


def dene(model):
    d = json.dumps({"model": model, "max_tokens": 20, "messages": [{"role": "user", "content": "de ki tamam"}]}).encode()
    r = urllib.request.Request(URL, d, {"Authorization": "Bearer " + KEY, "content-type": "application/json", "User-Agent": "curl/8"})
    try:
        with urllib.request.urlopen(r, timeout=60) as x:
            return x.status, x.read()[:160].decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read()[:160].decode("utf-8", "replace")
    except Exception as e:
        return 0, repr(e)[:160]


for m in sys.argv[1:]:
    print(m, *dene(m))
