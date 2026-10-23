"""Desktop'ta REA'nin config disi kaydi var mi: eklenti (Claude Extensions), extensions-installations, MSIX LocalCache.
Yalniz yol/ad/boyut; icerik yazdirmaz."""
import os
KOKLER = [os.path.expandvars(r"%APPDATA%\Claude"), os.path.expandvars(r"%LOCALAPPDATA%\Claude-Data"),
          os.path.expandvars(r"%LOCALAPPDATA%\Packages\Claude_pzs8sxrjxfjjc\LocalCache")]
for kok in KOKLER:
    for d, alt, fs in os.walk(kok):
        if any(x in d for x in ("Cache", "IndexedDB", "blob_storage", "vm_bundles", "local-agent-mode-sessions", "logs", "Service Worker")):
            alt[:] = []
            continue
        for n in alt + fs:
            nl = n.lower()
            if "rea" in nl.split("-")[0] or nl.startswith("rea") or "extension" in nl:
                print(os.path.join(d, n))
        for f in fs:
            if f.endswith(".json") and ("extension" in f.lower() or "install" in f.lower()):
                p = os.path.join(d, f)
                try:
                    b = open(p, "rb").read()
                    print("  json", p, len(b), "rea-agents" in b.decode("utf-8", "replace"), '"rea"' in b.decode("utf-8", "replace"))
                except Exception:
                    pass
