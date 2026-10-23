"""İndirilemeyen Instagram kodlarını Chrome (headless, çerezli oturum) ile açar; 'ulaşılamıyor' sayfası = silinmiş. Çerez değeri yazılmaz."""
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

KOK = Path(__file__).resolve().parents[3]
cerez = []
for s in (KOK / ".kos/ig-cookies.txt").read_text(encoding="utf-8").splitlines():
    p = s.replace("#HttpOnly_", "").split("\t")
    if len(p) == 7 and not s.startswith("#"):
        cerez.append({"name": p[5], "value": p[6], "domain": p[0], "path": p[2], "secure": p[3] == "TRUE"})
kodlar = [s.split("\t")[0] for s in (Path(__file__).parent / "ind.tsv").read_text(encoding="utf-8").splitlines() if "instagram" in s.lower()]
if len(sys.argv) > 1:
    kodlar = kodlar[: int(sys.argv[1])]
yok = ("ulaşılamıyor", "isn't available", "isn’t available", "may be broken")
with sync_playwright() as pw:
    b = pw.chromium.launch(channel="chrome", headless=True)
    c = b.new_context(locale="tr-TR")
    c.add_cookies(cerez)
    sayfa = c.new_page()
    for k in kodlar:
        try:
            sayfa.goto(f"https://www.instagram.com/p/{k}/", wait_until="domcontentloaded", timeout=30000)
            sayfa.wait_for_timeout(3500)
            g = sayfa.inner_text("body")[:1500]
            giris = "Log in" in g[:300] or "Giriş yap" in g[:300]
            durum = "SILINMIS" if any(y in g for y in yok) else ("OTURUM-YOK" if giris else "ACIK")
        except Exception as e:
            durum = "HATA " + type(e).__name__
        print(k, len(k), durum, flush=True)
    b.close()
