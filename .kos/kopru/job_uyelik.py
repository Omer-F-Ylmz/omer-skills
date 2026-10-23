"""YÖNETİCİ-BAĞIMSIZ-1 d1: bir süreç Windows job nesnesinde mi? (Desktop job'u kapanınca içindekiler ölür.)
Görev Zamanlayıcı süreçleri kendi job'unda koşar; ölçüt "Desktop job'u dışında" = bu sürecin job üyeleri arasında verilen pid'ler yok.
  python job_uyelik.py [--cikti dosya] [pid...]   → pid yoksa yönetici (ajan-sira.kilit). Çıkış 0: pid'ler bu sürecin job'unda DEĞİL, 1: en az biri aynı job'da."""
import ctypes, sys
from ctypes import wintypes
from pathlib import Path

K = Path(__file__).resolve().parent
k32 = ctypes.windll.kernel32
k32.OpenProcess.restype = wintypes.HANDLE
k32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
k32.IsProcessInJob.argtypes = [wintypes.HANDLE, wintypes.HANDLE, ctypes.POINTER(wintypes.BOOL)]
k32.CloseHandle.argtypes = [wintypes.HANDLE]


def job_icinde(pid):
    """True/False; süreç açılamazsa None."""
    h = k32.OpenProcess(0x1000, False, int(pid))  # PROCESS_QUERY_LIMITED_INFORMATION
    if not h:
        return None
    try:
        r = wintypes.BOOL()
        return bool(r.value) if k32.IsProcessInJob(h, None, ctypes.byref(r)) else None
    finally:
        k32.CloseHandle(h)


def kendi_job_uyeleri():
    """Bu sürecin job'undaki süreç kimlikleri (job yoksa [])."""
    class LISTE(ctypes.Structure):
        _fields_ = [("n", wintypes.DWORD), ("sayi", wintypes.DWORD), ("pid", ctypes.c_size_t * 4096)]
    b = LISTE()
    if not k32.QueryInformationJobObject(None, 3, ctypes.byref(b), ctypes.sizeof(b), None):  # JobObjectBasicProcessIdList
        return []
    return list(b.pid[:b.sayi])


if __name__ == "__main__":
    import os
    if sys.stdout:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    cikti = None
    if "--cikti" in sys.argv:  # pythonw'de stdout yok: raporu dosyaya yaz
        i = sys.argv.index("--cikti")
        cikti, sys.argv = sys.argv[i + 1], sys.argv[:i] + sys.argv[i + 2:]
        sys.stdout = open(cikti, "w", encoding="utf-8")
    pidler = [int(x) for x in sys.argv[1:]]
    if not pidler:
        try:
            pidler.append(int((K / "ajan-sira.kilit").read_text(encoding="utf-8").split()[0]))
        except (OSError, ValueError, IndexError):
            pass
    uyeler = kendi_job_uyeleri()
    print(f"bu süreç (pid {os.getpid()}) job'da: {job_icinde(os.getpid())} · job üyesi {len(uyeler)}")
    ortak = False
    for p in pidler:
        ayni = p in uyeler
        ortak |= ayni
        print(f"pid {p}: bu sürecin job'unda {'EVET' if ayni else 'hayır'}")
    sys.stdout.flush()
    sys.exit(1 if ortak else 0)  # 1: yönetici ile aynı job'dayız (Desktop job'u)
