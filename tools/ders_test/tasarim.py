"""DERS-TASARIM: ders uygulama noktası karşılaştırması (aynı 10 vaka, aynı `uygula` regex'i). Kollar:
A  mevcut (ders bloğu istemin BAŞINA, ucretsiz_havuz.cagir enjekte eder)
B  ders istemin SONUNA zorunlu kural olarak (yeni-ness: son konum), tek en iyi ders (k=1)
C  iki geçiş: model yanıtlar, sonra eşleşen ders(ler)e göre kendi yanıtını denetleyip düzeltir (uygulama noktası = çıktı denetimi)
Kullanım: python tools/ders_test/tasarim.py [A|B|C ...]  → JSON; ayrıca getir geri çağırma (bekle id'si ≤K içinde mi, model yok)."""
import importlib
import json
import re
import sys
import time
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "tools"))
dd = importlib.import_module("ders_dongu")
import ucretsiz_havuz  # noqa: E402

DIL = "\nTürkçe ve kısa yanıtla: hangi adımları atarsın?"


def sor(istem):
    for _ in range(4):
        m, _, _ = ucretsiz_havuz.cagir("ozet", istem, max_tokens=400, zaman=60, saglayici="groq")
        if m is not None:
            return m
        time.sleep(10)
    return None


def kol(ad, v):
    gorev = v["gorev"] + DIL
    if ad == "A":
        return sor(gorev)  # onek açık: başa enjeksiyon
    blok, ids = dd.getir(v["tur"], v["gorev"], k=1 if ad == "B" else dd.K, jeton=400)
    if not blok:
        return sor(gorev)
    if ad == "B":
        return sor(gorev + "\n\nZORUNLU KURAL (yanıtın bu kurala uymalı; kuralı yanıtında açıkça uygula):\n" + blok)
    ilk = sor(gorev)
    if not ilk:
        return None
    return sor("Görev: " + v["gorev"] + "\n\nTaslak yanıt:\n" + ilk + "\n\nKurallar:\n" + blok +
               "\n\nTaslağı bu kurallara göre denetle; uymuyorsa düzelt. Türkçe, kısa, yalnız son hâlini yaz.")


if __name__ == "__main__":
    vakalar = json.loads((KOK / "tools/ders_test/vakalar.json").read_text(encoding="utf-8"))
    geri = {v["ad"]: v["bekle"] in dd.getir(v["tur"], v["gorev"])[1] for v in vakalar}
    sonuc = {"geri_cagirma": f"{sum(geri.values())}/{len(vakalar)}", "yok": [a for a, o in geri.items() if not o]}
    asil = dd.onek
    try:
        for ad in sys.argv[1:] or ["A", "B", "C"]:
            dd.onek = asil if ad == "A" else (lambda g, t=None: "")
            ok, kacan, bos = 0, [], 0
            for v in vakalar:
                m = kol(ad, v)
                bos += m is None
                if m and re.search(v["uygula"], m, re.I):
                    ok += 1
                else:
                    kacan.append(v["ad"])
            sonuc[ad] = {"uygulanan": ok, "bos": bos, "kacan": kacan}
    finally:
        dd.onek = asil
    print(json.dumps(sonuc, ensure_ascii=False))
