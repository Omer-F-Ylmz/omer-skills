"""DISK-TARA-2: C: tam tarama (os.scandir, 32 iş parçacığı, BelowNormal). Yalnız okur, silmez.
Çıktı: .kos/kopru/rapor/disk-tara-2/dirs.tsv (>=100 MB klasörler, GB<TAB>yol)."""
import os, sys, time, threading
from concurrent.futures import ThreadPoolExecutor

OUT = r"C:\Projeler\omer-skills\.kos\kopru\rapor\disk-tara-2"
os.makedirs(OUT, exist_ok=True)
try:
    import ctypes
    ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x4000)
except Exception:
    pass

sizes = {}
lock = threading.Lock()
skipped = 0
files = 0


def scan(path):
    """Bir klasörün doğrudan dosya toplamı + alt klasör listesi."""
    global skipped, files
    tot, subs, n = 0, [], 0
    try:
        with os.scandir(path) as it:
            for e in it:
                try:
                    st = e.stat(follow_symlinks=False)
                    if st.st_file_attributes & 0x400:  # junction/symlink/bulut yer tutucu: döngü ve çift sayım
                        continue
                    if e.is_dir(follow_symlinks=False):
                        subs.append(e.path)
                    else:
                        tot += st.st_size
                        n += 1
                except OSError:
                    pass
    except OSError:
        with lock:
            skipped += 1
    with lock:
        sizes[path] = tot
        files += n
    return subs


def main():
    t0 = time.time()
    dirs = []
    with ThreadPoolExecutor(32) as ex:
        pending = [ex.submit(scan, "C:\\")]
        while pending:
            nxt = []
            for f in pending:
                for s in f.result():
                    dirs.append(s)
                    nxt.append(ex.submit(scan, s))
            pending = nxt
            with open(os.path.join(OUT, "ilerleme.log"), "w") as pf:
                pf.write(f"{time.time()-t0:.0f}s klasor={len(sizes)} dosya={files} siradaki_seviye={len(pending)}\n")
    # alttan yukarı topla
    total = dict(sizes)
    for p in sorted(sizes, key=lambda x: -x.count("\\")):
        if p != "C:\\":
            parent = os.path.dirname(p)
            if parent in total:
                total[parent] += total[p]
    rows = sorted(((v, p) for p, v in total.items() if v >= 100 * 1024 * 1024), reverse=True)
    with open(os.path.join(OUT, "dirs.tsv"), "w", encoding="utf-8") as f:
        for v, p in rows:
            f.write(f"{v / 2**30:.2f}\t{p}\n")
    with open(os.path.join(OUT, "tara.log"), "w") as f:
        f.write(f"sure={time.time()-t0:.0f}s dosya={files} klasor={len(sizes)} erisilemeyen={skipped} C_kullanilan={total['C:\\']/2**30:.1f}GB\n")


main()
