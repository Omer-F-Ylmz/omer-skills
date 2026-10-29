"""DERS-TASARIM: ders uygulama noktası karşılaştırması (aynı 10 vaka, aynı `uygula` regex'i). Kollar:
A  mevcut (ders bloğu istemin BAŞINA, ucretsiz_havuz.cagir enjekte eder)
B  ders istemin SONUNA zorunlu kural olarak (yeni-ness: son konum), tek en iyi ders (k=1)
C  iki geçiş: model yanıtlar, sonra eşleşen ders(ler)e göre kendi yanıtını denetleyip düzeltir (uygulama noktası = çıktı denetimi)
Kullanım: python tools/ders_test/tasarim.py [A|B|C ...]  → JSON; ayrıca getir geri çağırma (bekle id'si ≤K içinde mi, model yok)."""
import importlib
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "tools"))
dd = importlib.import_module("ders_dongu")
import ucretsiz_havuz  # noqa: E402

ZINCIR = ["openrouter", "nvidia", "groq"]
DIL ="\nTürkçe ve kısa yanıtla: hangi adımları atarsın?"


def sor(istem):
    for sag in ZINCIR:  # boş yanıt "cevap yok" sayılmaz: sağlayıcı başına 3 deneme, sonra sıradaki
        for _ in range(3):
            m, _, _ = ucretsiz_havuz.cagir("ozet", istem, max_tokens=400, zaman=60, saglayici=sag)
            if m:
                return m
            time.sleep(3)
    return haiku(dd.onek(istem) + istem)


def haiku(istem):  # model merdiveni son halka: Haiku medium (tavan $0,30); aciklama_yaz.claude kalıbı: araçsız, ANTHROPIC_BASE_URL'siz
    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_BASE_URL"}
    with tempfile.TemporaryDirectory(prefix="tasarim-", ignore_cleanup_errors=True) as bos:
        r = subprocess.run(["claude", "-p", "--model", "haiku", "--effort", "medium", "--output-format", "json", "--max-turns", "1",
                            "--tools", "", "--setting-sources", "", "--strict-mcp-config", "--safe-mode",
                            "--disable-slash-commands", "--no-session-persistence"],
                           input=istem, capture_output=True, encoding="utf-8", errors="replace", env=env, cwd=bos, timeout=120)
    try:
        j = json.loads(r.stdout)
    except json.JSONDecodeError:
        return None
    haiku.maliyet += j.get("total_cost_usd", 0)
    return (j.get("result") or "").strip() or None


haiku.maliyet = 0.0


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
    sonuc["haiku_usd"] = round(haiku.maliyet, 3)
    print(json.dumps(sonuc, ensure_ascii=False))
