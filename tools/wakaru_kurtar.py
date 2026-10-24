"""REA recover_javascript_sources Windows'ta çalışmıyor (prlimit/linux ister) → wakaru ile eşdeğer kurtarma.
Kullanım: python tools/wakaru_kurtar.py <bundle.js> <çıktı_klasörü> [harita.map]
Çıktı: tek özet satırı `wakaru ok|hata <girdi_bayt> -> <dosya_sayısı> dosya <çıktı_bayt> bayt <sn>s`; çıkış kodu wakaru'nunki."""
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rea_bellek  # NODE_OPTIONS=--max-old-space-size=2048

SURUM = "@wakaru/cli@1.14.0"  # sürüm sabit (@latest sabitsizlik riski)


def kurtar(girdi, cikti, harita=None, zaman_asimi=600):
    girdi, cikti = Path(girdi), Path(cikti)
    cikti.mkdir(parents=True, exist_ok=True)
    argv = ["npx.cmd", "--yes", SURUM, str(girdi), "--unpack", "-o", str(cikti)]
    if harita:
        argv += ["-m", str(harita)]
    t0 = time.time()
    try:
        r = subprocess.run(argv, env=rea_bellek.ortam(), capture_output=True, text=True, timeout=zaman_asimi, creationflags=0x08000000)
        kod, hata = r.returncode, (r.stderr or "")[-300:]
    except subprocess.TimeoutExpired:
        kod, hata = 124, "zaman aşımı"
    dosyalar = [f for f in cikti.rglob("*") if f.is_file()]
    boyut = sum(f.stat().st_size for f in dosyalar)
    print(f"wakaru {'ok' if kod == 0 else 'hata'} {girdi.stat().st_size} -> {len(dosyalar)} dosya {boyut} bayt {time.time() - t0:.1f}s" + ("" if kod == 0 else f" | {hata.strip()}"))
    return kod


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    sys.exit(kurtar(*sys.argv[1:4]))
