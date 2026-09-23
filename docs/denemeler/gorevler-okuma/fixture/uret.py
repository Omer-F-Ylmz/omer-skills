"""20a okuma görev seti fixture üreteci: sentetik, gizli bilgi yok, deterministik. `python uret.py` → 4 dosya (her biri ≥20 KB)."""
import json
import random
from pathlib import Path

D = Path(__file__).parent
r = random.Random(20)
MODUL = ["fiyat", "sepet", "stok", "kargo", "odeme", "kullanici", "rapor", "bildirim"]


def test_ciktisi():
    s = ["============================= test session starts ==============================", "platform win32 -- Python 3.12.4, pytest-8.3.2", "collected 612 items", ""]
    for i in range(612):
        m = MODUL[i % len(MODUL)]
        ad = f"test_{m}_{i:03d}_durum_{r.choice(['bos', 'dolu', 'sinir', 'hatali', 'buyuk'])}"
        sonuc = "FAILED" if i == 437 else "PASSED"
        s.append(f"tests/test_{m}.py::{('test_indirim_sinir_esik' if i == 437 else ad)} {sonuc} [{i * 100 // 612:3d}%]")
    s += ["", "=================================== FAILURES ===================================",
          "___________________________ test_indirim_sinir_esik ____________________________", "",
          "    def test_indirim_sinir_esik():", ">       assert indirimli_fiyat(100, tutar=500) == 90", "E       assert 100 == 90",
          "E        +  where 100 = indirimli_fiyat(100, tutar=500)", "", "tests/test_fiyat.py:88: AssertionError", "",
          "src/fiyat.py:41: in indirimli_fiyat", "    if tutar > ESIK:  # ESIK = 500", "",
          "=========================== short test summary info ============================",
          "FAILED tests/test_fiyat.py::test_indirim_sinir_esik - assert 100 == 90", "================= 1 failed, 611 passed, 3 warnings in 41.27s ================="]
    return "\n".join(s) + "\n"


def siparisler():
    out = []
    for i in range(1000, 1320):
        out.append({"id": f"S-{i}", "musteri": {"ad": f"Musteri {i}", "eposta": f"musteri{i}@ornek.test"},
                    "kalemler": [{"urun": f"U-{r.randint(1, 400)}", "adet": r.randint(1, 5), "fiyat": round(r.uniform(5, 900), 2)} for _ in range(r.randint(1, 3))],
                    "kargo": {"firma": r.choice(["Hizli", "Yavas", "Orta"]), "takip": f"TK{r.randint(10**8, 10**9 - 1)}"},
                    "durum": r.choice(["hazirlaniyor", "kargoda", "teslim", "iade"])})
    hedef = next(x for x in out if x["id"] == "S-1187")
    hedef["musteri"]["eposta"], hedef["kargo"]["takip"], hedef["durum"] = "ayse.kaya@ornek.test", "TK771204993", "iade"
    return json.dumps(out, ensure_ascii=False, indent=1) + "\n"


def diff():
    s = []
    for n in range(60):
        m = MODUL[n % len(MODUL)]
        s += [f"diff --git a/src/{m}_{n}.py b/src/{m}_{n}.py", f"--- a/src/{m}_{n}.py", f"+++ b/src/{m}_{n}.py", f"@@ -{n * 3 + 1},7 +{n * 3 + 1},7 @@"]
        if n == 41:
            s += [" def siparis_iptal(kullanici, siparis):", "-    if kullanici.yetkili and siparis.sahibi == kullanici.id:",
                  "+    if kullanici.yetkili or siparis.sahibi == kullanici.id:", "         siparis.durum = 'iptal'", "         return True", "     return False"]
        else:
            eski, yeni = f"deger_{n}", f"{m}_degeri_{n}"
            s += [f" def hesapla_{n}(x):", f"-    {eski} = x * {n + 1}", f"+    {yeni} = x * {n + 1}", f"-    return {eski}", f"+    return {yeni}",
                  "     # yeniden adlandirma, davranis ayni", ""]
            s += [f" # satir dolgu {k}: {m} modulunde degisiklik yok" for k in range(3)]
    return "\n".join(s) + "\n"


def log():
    s, t = [], 0
    for i in range(420):
        t += r.randint(1, 4)
        z = f"2026-09-20T10:{t // 60 % 60:02d}:{t % 60:02d}"
        if i == 233:
            s += [f"{z} WARN  db.havuz: baglanti havuzu %95 dolu (19/20)", f"{z} ERROR db.havuz: havuz tukendi, 30 sn beklendi istek=7f3a91",
                  f"{z} ERROR siparis.kaydet: SiparisKaydedilemedi: veritabani baglantisi alinamadi istek=7f3a91",
                  f"{z} ERROR http: POST /api/siparis 500 istek=7f3a91 sure=30012ms"]
        elif i == 350:
            s += [f"{z} ERROR bildirim.eposta: SMTP zaman asimi istek=c21d07", f"{z} ERROR http: POST /api/bildirim 502 istek=c21d07"]
        else:
            s.append(f"{z} INFO  http: {r.choice(['GET', 'POST'])} /api/{r.choice(MODUL)} 200 istek={r.randint(0, 16**6 - 1):06x} sure={r.randint(3, 180)}ms")
    return "\n".join(s) + "\n"


for ad, f in (("test-ciktisi.txt", test_ciktisi), ("siparisler.json", siparisler), ("degisiklik.diff", diff), ("uygulama.log", log)):
    (D / ad).write_bytes(f().encode("utf-8"))
