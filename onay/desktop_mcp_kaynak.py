"""Desktop'un MCP sunucu listesini nerede tuttugunu bulur: profil klasorlerinde 'brave-search' ve 'code-mode'
gecen dosyalarin YOLU + boyut + mtime (icerik yazdirmaz)."""
import os, sys, time
sys.stdout = open(r"C:\Projeler\omer-skills\.kos\kopru\desktop_mcp_kaynak.txt", "w", encoding="utf-8")

KOKLER = [os.path.expandvars(r"%LOCALAPPDATA%\Claude-Data"), os.path.expandvars(r"%APPDATA%\Claude")]
for kok in KOKLER:
    for d, alt, dosyalar in os.walk(kok):
        if any(x in d for x in ("Cache", "GPUCache", "Code Cache", "blob_storage", "vm_bundles", "Crashpad")):
            continue
        for f in dosyalar:
            p = os.path.join(d, f)
            try:
                if os.path.getsize(p) > 5_000_000:
                    continue
                b = open(p, "rb").read()
            except Exception:
                continue
            bs, cm = b"brave-search" in b, b"code-mode" in b
            if bs or cm:
                print(f"{'B' if bs else '-'}{'C' if cm else '-'} {len(b):>9} {time.strftime('%H:%M', time.localtime(os.path.getmtime(p)))} {p}")
