"""VIDEO-IZLE-KUR-1: derin izlemede indirilemeyen videolar -> rapor/chrome-video-listesi.md (url + neden). Desktop Chrome'dan izler."""
import re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
K = Path(__file__).resolve().parents[3]
D = K / ".kos/kopru/ogren/video-izle-kur-1"
urls = re.findall(r"https?://\S+", (D / "derin-eksik.txt").read_text(encoding="utf-8"))
CIKTI = [K / "docs/video-tarama/derin", K / "docs/video-tarama/derin-2"]


def kod(u):
    m = re.search(r"/(?:reel|p|tv|shorts)/([\w-]+)", u) or re.search(r"(?:v=|youtu\.be/)([\w-]+)", u)
    return m.group(1) if m else u


neden = {}
for log in ["derin-tur2-goz.log", "derin-tur4.log"]:
    p = D / log
    if not p.exists():
        continue
    for s in p.read_text(encoding="utf-8", errors="replace").splitlines():
        if "\tindirilemedi" in s:
            k, n = s.split("\t")[:2]
            neden[k] = (n.split(":", 1)[1].strip()[:120] if ":" in n else "indirme 0 s (IG oran sınırı / giriş istiyor)")
for k in (K / ".kos/kopru/video-atla.txt").read_text(encoding="utf-8").split():
    neden.setdefault(k, "kalıcı atlama listesinde (video-atla.txt): önceki denemelerde indirilemedi")
satir, eksik = [], 0
for u in dict.fromkeys(urls):
    k = kod(u)
    var = any((c / f"{k}.json").exists() for c in CIKTI)
    if k in neden and not var:
        satir.append(f"- {u} — {neden[k]}")
    elif not var:
        eksik += 1
out = K / ".kos/kopru/rapor/chrome-video-listesi.md"
out.write_text("---\ntype: liste\nstatus: aktif\ntags: [video, chrome]\nrelatedTo: [video-izle-kur-1]\n---\n"
               f"# Chrome ile izlenecek videolar ({len(satir)}) — derin izleme indiremedi\n" + "\n".join(satir) + "\n",
               encoding="utf-8")
print("chrome", len(satir), "hala islenmemis", eksik)
