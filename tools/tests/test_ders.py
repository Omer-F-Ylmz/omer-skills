import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ogrenme"))
import ders  # noqa: E402


@pytest.fixture
def depo(tmp_path, monkeypatch):
    monkeypatch.setenv("OGRENME_DIZIN", str(tmp_path))
    return tmp_path


def ekle(**k):
    d = dict(ajan="kod", baslik="testler ORNEK_MOD=test ister", kosul="pytest koşarken",
             icerik="ORNEK_MOD=test olmadan conftest KeyError verir; önce env ayarla.", sonuc="basari",
             kaynak="k1", kanit="pytest 3 passed")
    d.update(k)
    return ders.ekle(**d)


def test_ekle_ve_getir(depo):
    r = ekle()
    assert r["durum"] == "yeni"
    blok, ids = ders.getir("kod", "pytest testleri kırmızı, conftest KeyError")
    assert ids == [r["id"]] and "ORNEK_MOD" in blok


def test_ilgisiz_gorev_ders_getirmez(depo):
    ekle()
    blok, ids = ders.getir("kod", "README başlığını Türkçeye çevir")
    assert ids == [] and blok == ""


def test_yinelenen_ders_birlesir(depo):
    a = ekle()
    b = ekle(icerik="conftest ORNEK_MOD=test bekliyor; pytest öncesi ayarla.", kaynak="k2")
    assert b["durum"] == "birlesti" and b["id"] == a["id"]
    assert len(ders.oku()) == 1 and ders.oku()[0]["destek"] == 2


@pytest.mark.parametrize("sir", ["sk-ant-api03-" + "x" * 40, "ghp_" + "a" * 36, "AKIAABCDEFGHIJKLMNOP",
                                 "-----BEGIN PRIVATE KEY-----", "parola: hunter2", "ali@ornek.com", "C:/Users/pc/Desktop"])
def test_sir_iceren_ders_reddedilir(depo, sir):
    with pytest.raises(ValueError):
        ekle(icerik=f"şunu kullan {sir}")
    assert ders.oku() == []


def test_kotu_ders_duser(depo):
    r = ekle()
    for _ in range(3):
        ders.geri_bildir([r["id"]], basari=False)
    assert ders.oku()[0]["durum"] == "dusuk"
    assert ders.getir("kod", "pytest conftest KeyError")[1] == []


def test_basarisizlik_dersi_isaretlenir_ve_butce(depo):
    for i, w in enumerate(["alfa", "beta", "gama", "delta", "epsilon", "zeta"]):
        ekle(baslik=f"{w} pytest conftest", icerik=f"{w} adımı conftest KeyError " + f"{w}x " * 80, kaynak=f"k{i}",
             sonuc="basarisizlik")
    blok, ids = ders.getir("kod", "pytest conftest KeyError")
    assert 1 <= len(ids) <= 2 and len(blok) <= ders.JETON * 4
    assert "kaçın" in blok  # başarısızlıktan gelen ders uyarı olarak sunulur


def test_gorev_metniyle_eslesir(depo):
    # d5: video dersleri istemle ortak terim taşımıyordu → hiç çağrılmadı; ders kaynak görevini de saklar
    g = "transkript.txt'de anılan yazılım araçlarını etiket.json'a JSON olarak yaz."
    r = ekle(ajan="video", baslik="Çıktı şemasını belgeden birebir al", kosul="yapılandırılmış çıktı yazarken",
             icerik="Önce KURALLAR.md oku.", sonuc="basarisizlik", gorev=g)
    assert ders.getir("video", g)[1] == [r["id"]]


def test_en_fazla_iki_ders_kisa_blok(depo):
    for i, w in enumerate(["alfa", "beta", "gama", "delta"]):
        ekle(baslik=f"{w} pytest conftest", icerik=f"{w} KeyError düzelt. Örnek: " + "uzun " * 80, kaynak=f"k{i}")
    blok, ids = ders.getir("kod", "pytest conftest KeyError")
    assert len(ids) <= 2 and len(blok) <= 120 * 4 and "Örnek" not in blok


def test_ek_farkli_yakin_kopya_birlesir(depo):
    a = ekle(baslik="Çıktı şemasını belgelerden birebir al", kosul="çıktı yazarken")
    b = ekle(baslik="Çıktı şemasını belgeden birebir al", kosul="çıktı yazarken", kaynak="k2")
    assert b["id"] == a["id"]


def test_iki_bosa_kullanim_duser(depo):
    r = ekle()
    ders.geri_bildir([r["id"]], basari=False)
    ders.geri_bildir([r["id"]], basari=False)
    assert ders.oku()[0]["durum"] == "dusuk"


def test_ajan_kapsami(depo):
    ekle(ajan="rapor")
    assert ders.getir("kod", "pytest conftest KeyError")[1] == []
    ekle(ajan="*", baslik="genel: pytest conftest", kaynak="g")
    assert len(ders.getir("kod", "pytest conftest KeyError")[1]) == 1


def test_cli_getir_bos_depo(depo, capsys):
    assert ders.main(["getir", "--ajan", "kod", "--gorev", "x"]) == 0
    assert capsys.readouterr().out == ""


def test_cli_ekle_dosyadan(depo, tmp_path):
    aday = tmp_path / "aday.json"
    aday.write_text(json.dumps([{"baslik": "a b c", "kosul": "d", "icerik": "e f"}] * 5), encoding="utf-8")
    assert ders.main(["ekle", "--ajan", "kod", "--sonuc", "basari", "--dosya", str(aday), "--kaynak", "k"]) == 0
    assert len(ders.oku()) == 1  # ≤3 aday alınır, aynılar birleşir


def test_cli_getir_windows_konsolunda_cokmez(depo):
    import os
    import subprocess
    ekle()
    env = {k: v for k, v in os.environ.items() if k not in ("PYTHONIOENCODING", "PYTHONUTF8")}
    r = subprocess.run([sys.executable, str(Path(ders.__file__)), "getir", "--ajan", "kod", "--gorev", "pytest koşarken ORNEK_MOD testler"],
                       capture_output=True, env={**env, "OGRENME_DIZIN": str(depo)}, timeout=30)
    assert r.returncode == 0 and "✓" in r.stdout.decode("utf-8"), r.stderr.decode("utf-8", "replace")[-300:]
