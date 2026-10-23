"""ARKA-KALICI-1 teşhis: bu süreç bir job nesnesinde mi, breakaway izni var mı, CREATE_BREAKAWAY_FROM_JOB gerçekten çalışıyor mu.
python job_teshis.py  → ajan içinden ve köprüden koşup çıktıları karşılaştır."""
import ctypes
import subprocess
import sys
from ctypes import wintypes

k = ctypes.WinDLL("kernel32", use_last_error=True)
k.GetCurrentProcess.restype = wintypes.HANDLE
k.IsProcessInJob.argtypes = [wintypes.HANDLE, wintypes.HANDLE, ctypes.POINTER(wintypes.BOOL)]
k.QueryInformationJobObject.argtypes = [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD, ctypes.c_void_p]
inj = wintypes.BOOL()
k.IsProcessInJob(k.GetCurrentProcess(), None, ctypes.byref(inj))
print("job içinde:", bool(inj.value))


class Sayac(ctypes.Structure):
    _fields_ = [("a", ctypes.c_longlong), ("b", ctypes.c_longlong), ("LimitFlags", wintypes.DWORD), ("pad", ctypes.c_byte * 124)]


b = Sayac()
ok = k.QueryInformationJobObject(None, 9, ctypes.byref(b), ctypes.sizeof(b), None)  # 9 = ExtendedLimitInformation; LimitFlags ofseti 16
if ok:
    bayrak = b.LimitFlags
    print(f"LimitFlags 0x{bayrak:x} · BREAKAWAY_OK {bool(bayrak & 0x800)} · SILENT_BREAKAWAY_OK {bool(bayrak & 0x1000)} · KILL_ON_JOB_CLOSE {bool(bayrak & 0x2000)}")
else:
    print("QueryInformationJobObject hata", ctypes.get_last_error())
try:
    p = subprocess.Popen([sys.executable, "-c", "pass"], creationflags=0x08000000 | 0x01000000)
    p.wait()
    print("CREATE_BREAKAWAY_FROM_JOB: İZİN VAR")
except OSError as e:
    print("CREATE_BREAKAWAY_FROM_JOB: REDDEDİLDİ", e)
