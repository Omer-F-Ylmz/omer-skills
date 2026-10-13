"""OMNIROUTE-1 envanter sondası: uç kodları + kısa gövde; anahtar değeri hiçbir çıktıya yazılmaz."""
import json, os, re, sys, urllib.request, urllib.error, winreg

B = "http://127.0.0.1:20128"


def anahtar():
    v = os.environ.get("OMNIROUTE_KEY")
    if v:
        return v
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as k:
        return winreg.QueryValueEx(k, "OMNIROUTE_KEY")[0]


K = anahtar()


def maske(s):
    return re.sub(r"(sk|or|gsk|AIza)[-_A-Za-z0-9]{6,}", "***", s.replace(K, "***"))


def iste(yol, govde=None, basliklar=None):
    h = {"content-type": "application/json", **(basliklar or {})}
    r = urllib.request.Request(B + yol, data=json.dumps(govde).encode() if govde is not None else None, headers=h)
    try:
        with urllib.request.urlopen(r, timeout=60) as y:
            return y.status, y.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")
    except Exception as e:
        return 0, repr(e)


if __name__ == "__main__":
    kip = sys.argv[1] if len(sys.argv) > 1 else "uclar"
    bearer = {"authorization": "Bearer " + K}
    if kip == "uclar":
        for y in ("/api/combos", "/api/providers", "/api/settings", "/v1/models"):
            for ad, h in (("bearer", bearer), ("xkey", {"x-api-key": K})):
                k, g = iste(y, basliklar=h)
                print(y, ad, k, maske(g[:160]).replace("\n", " "))
        for ad, h in (("yok", {}), ("bearer", bearer), ("xkey", {"x-api-key": K})):
            k, g = iste("/v1/messages", {}, h)
            print("/v1/messages", ad, k, maske(g[:160]).replace("\n", " "))
    elif kip == "get":
        k, g = iste(sys.argv[2], basliklar=bearer)
        print(k, maske(g[: int(sys.argv[3]) if len(sys.argv) > 3 else 1500]))
