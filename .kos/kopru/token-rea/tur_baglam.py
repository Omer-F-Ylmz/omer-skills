"""Tur × bağlam ölçümü (yalnız ölçüm; /autocompact DEĞİŞMEZ). Son 14 gün ana oturum transkriptlerinden:
istek başı bağlam (girdi+cache okuma+cache yazma) dağılımı ve 'bağlam >E olunca sabit tabana (S) sıfırlansaydı' karşı-olgusal cache-okuma tasarrufu.
Kalite etkisi bu betikte ÖLÇÜLMEZ (devir kaybı); öneri için ayrı A/B gerekir. Claude çağrısı yok.
  python tur_baglam.py [gün=14] [S=30000]"""
import json, sys, time
from pathlib import Path

GUN, S = int(sys.argv[1]) if len(sys.argv) > 1 else 14, int(sys.argv[2]) if len(sys.argv) > 2 else 30000
KOK = Path.home() / ".claude" / "projects"
sinir = time.time() - GUN * 86400
oturumlar = []
for f in KOK.glob("*/*.jsonl"):  # alt ajan dosyaları ayrı dizinde (*/*/subagents), burada yok
    if f.stat().st_mtime < sinir:
        continue
    gor, ctx = set(), []
    for ln in f.open(encoding="utf-8", errors="replace"):
        try:
            d = json.loads(ln)
        except ValueError:
            continue
        m = d.get("message") or {}
        u = m.get("usage")
        if d.get("type") != "assistant" or d.get("isSidechain") or not u or m.get("id") in gor:
            continue
        gor.add(m.get("id"))
        ctx.append((u.get("input_tokens", 0) + u.get("cache_read_input_tokens", 0) + u.get("cache_creation_input_tokens", 0), u.get("cache_read_input_tokens", 0)))
    if len(ctx) >= 5:  # tek istekli claude -p ölçüm oturumları dışarıda
        oturumlar.append(ctx)

tum = [c for o in oturumlar for c in o]
cr = sum(c[1] for c in tum)
print(f"oturum={len(oturumlar)} istek={len(tum)} cache_okuma_toplam={cr/1e6:.1f}M medyan_oturum_istek={sorted(len(o) for o in oturumlar)[len(oturumlar)//2]}")
for E in (80000, 120000, 160000):
    kazanc, sifir = 0, 0
    for o in oturumlar:
        ek = 0  # sıfırlama sonrası düşen bağlam (gerçek bağlam − yeni baz)
        on = 0
        for ctx_t, cr_t in o:
            if ctx_t < 0.6 * on: ek = 0  # otomatik sıkıştırma olmuş: eski sıfırlama geçersiz
            on = ctx_t
            g = ctx_t - ek
            if g > E:
                ek, sifir, g = ctx_t - S, sifir + 1, S
            kazanc += min(cr_t, ek) if ek else 0
    print(f"E={E//1000}k S={S//1000}k: sıfırlama={sifir} cache_okuma_tasarrufu~{kazanc/1e6:.1f}M (%{100*kazanc/max(1,cr):.1f} cache okuma; devir yeniden yazma maliyeti hariç)")
iri = sum(1 for c in tum if c[0] > 120000)
print(f"istek>120k payı: %{100*iri/len(tum):.1f}; bunların cache okuma payı: %{100*sum(c[1] for c in tum if c[0]>120000)/max(1,cr):.1f}")
