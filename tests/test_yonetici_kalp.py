"""YONETICI-OLUM-2: kalp atışı + önceki ölüm kanıtı (iz bırakmadan ölen yönetici)."""
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".kos/kopru"))
import yonetici_kalp

OLU_PID = 2**22 + 7  # Windows'ta olmayan pid


def test_kalp_yaz_alanlari(tmp_path):
    k = tmp_path / "kalp.txt"
    yonetici_kalp.kalp_yaz(k, ram=71, calisan=3, son_olay="BAŞLAT x")
    d = json.loads(k.read_text(encoding="utf-8"))
    assert d["pid"] == os.getpid() and d["ram"] == 71 and d["calisan"] == 3
    assert d["son_olay"] == "BAŞLAT x" and "cikis" not in d and d["boot"] > 0


def test_onceki_olum_iz_yok_temiz_degil(tmp_path):
    k = tmp_path / "kalp.txt"
    k.write_text(json.dumps({"pid": OLU_PID, "saat": "18:04:10", "boot": yonetici_kalp.boot_zamani(), "son_olay": "BAŞLAT y"}), encoding="utf-8")
    m = yonetici_kalp.onceki_olum(k)
    assert "18:04:10" in m and "çıkış izi yok" in m and "BAŞLAT y" in m


def test_onceki_olum_yeniden_baslatma_ayirt_edilir(tmp_path):
    k = tmp_path / "kalp.txt"
    k.write_text(json.dumps({"pid": OLU_PID, "saat": "03:00:00", "boot": 1, "son_olay": ""}), encoding="utf-8")
    assert "yeniden başlatma" in yonetici_kalp.onceki_olum(k)


def test_onceki_olum_temiz_cikis_ve_canli_ve_dosya_yok(tmp_path):
    k = tmp_path / "kalp.txt"
    assert yonetici_kalp.onceki_olum(k) is None
    k.write_text(json.dumps({"pid": OLU_PID, "saat": "1:00:00", "boot": 1, "cikis": "atexit"}), encoding="utf-8")
    assert "atexit" in yonetici_kalp.onceki_olum(k) and "çıkış izi yok" not in yonetici_kalp.onceki_olum(k)
    k.write_text(json.dumps({"pid": os.getpid(), "saat": "1:00:00", "boot": 1}), encoding="utf-8")
    assert yonetici_kalp.onceki_olum(k) is None
