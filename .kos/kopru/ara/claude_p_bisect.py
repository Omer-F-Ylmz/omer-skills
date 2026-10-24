"""claude -p asilma: enabledPlugins ikiye bolme. Kullanici settings.json'una yazmaz; gecici --settings dosyasi kullanir."""
import json, os, subprocess, sys, tempfile, time

HOME = os.path.expanduser("~")
S = json.load(open(os.path.join(HOME, ".claude", "settings.json"), encoding="utf-8"))
PLUG = [k for k, v in S.get("enabledPlugins", {}).items() if v]
TMO = int(os.environ.get("TMO", "35"))


def kos(extra, label):
    t = time.time()
    try:
        r = subprocess.run(["claude", "-p", "echo ok", *extra], capture_output=True, text=True,
                           timeout=TMO, creationflags=0x08000000, stdin=subprocess.DEVNULL, encoding="utf-8", errors="replace")
        ok = r.returncode == 0 and "ok" in r.stdout.lower()
        res = "OK" if ok else f"rc={r.returncode} {r.stdout[:60]!r}"
    except subprocess.TimeoutExpired:
        res = "ASILDI"
    dt = time.time() - t
    print(f"{label}: {res} {dt:.1f}s", flush=True)
    return res == "OK", dt


def kapali(liste):
    d = {"enabledPlugins": {p: False for p in liste}}
    f = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
    json.dump(d, f)
    f.close()
    return ["--settings", f.name]


if __name__ == "__main__":
    mod = sys.argv[1] if len(sys.argv) > 1 else "ozet"
    if mod == "ozet":
        print(len(PLUG), "etkin eklenti:", PLUG)
        kos(["--setting-sources", "project"], "project-only")
        kos([], "tam")
        kos(kapali(PLUG), "tum-eklenti-kapali")
    elif mod == "bol":
        # kapatilan alt kume argv[2:] adlari (indeks araligi a:b)
        a, b = map(int, sys.argv[2].split(":"))
        kos(kapali(PLUG[a:b]), f"kapali[{a}:{b}]")
    elif mod == "tur":
        import glob
        ip = json.load(open(os.path.join(HOME, ".claude", "plugins", "installed_plugins.json"), encoding="utf-8"))["plugins"]
        dos = sys.argv[2]
        L = [k for k in PLUG if os.path.exists(ip[k][0]["installPath"] + "/" + dos)]
        kos(kapali(L), f"kapali {dos} ({len(L)})")
    elif mod == "hook":
        ip = json.load(open(os.path.join(HOME, ".claude", "plugins", "installed_plugins.json"), encoding="utf-8"))["plugins"]
        L = [k for k in PLUG if os.path.exists(ip[k][0]["installPath"] + "/hooks/hooks.json")]
        a, b = map(int, sys.argv[2].split(":"))
        print(L[a:b] if b - a <= 12 else "")
        kos(kapali(L[a:b]), f"hook-kapali[{a}:{b}]")
    elif mod == "ad":
        ad = sys.argv[2:]
        L = [k for k in PLUG if k.split("@")[0] in ad]
        kos(kapali(L), f"ad-kapali {ad} ({len(L)})")
