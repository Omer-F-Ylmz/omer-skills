"""hr2: ML'siz şablon-satır çökertici (Headroom'un yanında; kaldırmaz). stdin → stdout; `hr2.py ac <id>` tam metni geri verir.
Art arda ≥RUN satır aynı şablona uyuyorsa (sayılar maskeli) ilk + son satır kalır, ortası `[×N benzer satır]` olur;
şablondan sapan satırlar (iğne) aynen kalır. JSON dizisi öğe başına bir satıra açılır. Tam metin AC'ye hash ile saklanır.
Çalıştır: python -I -S hr2.py  (yalnız stdlib)."""
import json, os, re, sys
from itertools import groupby
from zlib import crc32

MIN, RUN = 1500, 4  # kr altı tam döner; RUN'dan kısa seri çökmez
AC = os.path.join(os.environ.get("TEMP") or "/tmp", "hr2-ac")


def satirlar(m):
    try:
        j = json.loads(m)
    except ValueError:
        return m.splitlines()
    return [json.dumps(e, ensure_ascii=False) for e in j] if isinstance(j, list) else m.splitlines()


def cokert(ls):
    o = []
    for _, g in groupby(ls, key=lambda l: re.sub(r"\d+", "#", l)):
        g = list(g)
        o += g if len(g) < RUN else [g[0], f"[×{len(g) - 2} benzer satır]", g[-1]]
    return o


def hr2(m):
    if len(m) <= MIN:
        return m
    ls = satirlar(m)
    o = cokert(ls)
    if len(o) == len(ls):
        return m
    i = "%08x" % crc32(m.encode())
    os.makedirs(AC, exist_ok=True)
    with open(os.path.join(AC, i), "w", encoding="utf-8") as f: f.write(m)
    r = "\n".join(o + [f"tam metin ({len(ls)} satır, {len(m)} kr): python -I -S {os.path.abspath(__file__)} ac {i}"])
    return r if len(r) < len(m) else m


def ac(i):
    with open(os.path.join(AC, i), encoding="utf-8") as f: return f.read()


def tepe_mb():  # Windows tepe çalışma kümesi (HR2_RAM=1 ile ölçüm)
    import ctypes
    from ctypes import wintypes
    class C(ctypes.Structure):
        _fields_ = [("cb", wintypes.DWORD), ("pf", wintypes.DWORD)] + [(n, ctypes.c_size_t) for n in ("tepe", "ws", "a", "b", "c", "d", "e", "f")]
    c = C(); c.cb = ctypes.sizeof(c)
    f = ctypes.windll.psapi.GetProcessMemoryInfo
    f.argtypes = [wintypes.HANDLE, ctypes.c_void_p, wintypes.DWORD]
    f(ctypes.c_void_p(-1), ctypes.byref(c), c.cb)  # -1 = geçerli süreç sahte tanıtıcısı
    return round(c.tepe / 1e6)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", newline="\n")
    sys.stdout.write(ac(sys.argv[2]) if sys.argv[1:2] == ["ac"] else hr2(sys.stdin.buffer.read().decode("utf-8")))
    if os.environ.get("HR2_RAM"): print(f"ram_mb={tepe_mb()}", file=sys.stderr)
