import ctypes, shutil, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
K = Path(r"C:\Projeler\omer-skills\.kos\kopru")


class M(ctypes.Structure):
    _fields_ = [("l", ctypes.c_ulong), ("y", ctypes.c_ulong), ("t", ctypes.c_ulonglong), ("a", ctypes.c_ulonglong),
                ("pt", ctypes.c_ulonglong), ("pa", ctypes.c_ulonglong), ("vt", ctypes.c_ulonglong), ("va", ctypes.c_ulonglong), ("e", ctypes.c_ulonglong)]


try:  # YARIM-BEKCI-1: yarım işler çıktının en üstünde
    import yarim_bekci
    print("\n".join(yarim_bekci.ozet_satirlar(K)))
except Exception as e:
    print(f"YARIM: okunamadı ({e!r:.60})")
m = M()
m.l = ctypes.sizeof(M)
ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
print(f"RAM %{m.y} · C: boş {shutil.disk_usage('C:/').free // 2**30} GB")
for ad in ["ajan-sira.log", "ajan-sira-runner.log"]:
    s = (K / ad).read_text(encoding="utf-8", errors="replace").splitlines()
    print(f"-- {ad}")
    for x in [x for x in s if "RAM-BEKÇİ" not in x][-4:]:
        print("  ", x[:160])
for r in ["baslangic-hiz-2-p4.md", "rea-usta-1-p3.md", "rea-agir-1.md"]:
    p = K / "rapor" / r
    print(f"rapor {r}: {'VAR ' + str(p.stat().st_size) + ' B' if p.exists() else 'yok'}")
