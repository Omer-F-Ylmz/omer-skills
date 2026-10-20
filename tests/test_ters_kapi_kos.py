import json
import sys
from pathlib import Path

import pytest
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools" / "ters"))
import kapi_kos as K  # noqa: E402


def test_rea_yol_which_ile_bulur(monkeypatch):
    monkeypatch.setattr(K.shutil, "which", lambda ad: "C:/x/rea.cmd" if ad == "rea.cmd" else None)
    assert K.rea_yol() == "C:/x/rea.cmd"


def test_rea_yol_bilinen_kurulum_yolu(monkeypatch, tmp_path):
    (tmp_path / "npm").mkdir()
    (tmp_path / "npm" / "rea.cmd").write_text("@echo off")
    monkeypatch.setattr(K.shutil, "which", lambda ad: None)
    monkeypatch.setenv("APPDATA", str(tmp_path))
    assert K.rea_yol() == str(tmp_path / "npm" / "rea.cmd")


def test_rea_yok_kosuyu_durdurur(monkeypatch, tmp_path):
    monkeypatch.setattr(K.shutil, "which", lambda ad: None)
    monkeypatch.setenv("APPDATA", str(tmp_path))
    cagri = []
    monkeypatch.setattr(K.subprocess, "run", lambda *a, **k: cagri.append(a))
    with pytest.raises(K.ReaYok):
        K.rea_kanit({"tur": "js", "yol": "a.js"})
    assert cagri == []  # hata satırıyla koşmak yok: komut hiç çalışmadı


def test_rea_kanit_cozulen_yolla_calisir(monkeypatch):
    monkeypatch.setattr(K, "rea_yol", lambda: "C:/x/rea.cmd")
    komutlar = []

    def sahte(komut, **k):
        komutlar.append(komut)
        return type("C", (), {"stdout": '{"ok":1}'})()
    monkeypatch.setattr(K.subprocess, "run", sahte)
    assert K.rea_kanit({"tur": "dotnet", "derlenmis": "a.dll"}) == '{"ok":1}'
    assert komutlar[0][:2] == ["C:/x/rea.cmd", "inspect-managed-members"]


def test_rea_calisma_hatasi_ve_bos_cikti_hatadir(monkeypatch):
    monkeypatch.setattr(K, "rea_yol", lambda: "C:/x/rea.cmd")
    monkeypatch.setattr(K.subprocess, "run", lambda *a, **k: type("C", (), {"stdout": ""})())
    with pytest.raises(K.ReaYok):
        K.rea_kanit({"tur": "js", "yol": "a.js"})

    def patlat(*a, **k): raise FileNotFoundError("rea")
    monkeypatch.setattr(K.subprocess, "run", patlat)
    with pytest.raises(K.ReaYok):
        K.rea_kanit({"tur": "js", "yol": "a.js"})


def _kare(yol, duz):
    im = Image.new("RGB", (32, 32), (20, 20, 20))
    if not duz:
        for x in range(32):
            for y in range(32): im.putpixel((x, y), ((x * 8) % 256, (y * 8) % 256, 90))
    im.save(yol)


def _dizin(tmp_path, ad, duzlar):
    d = tmp_path / ad; d.mkdir()
    for n, duz in zip((0, 50, 100), duzlar): _kare(d / f"kare-{n}.png", duz)
    return d


def test_duz_referans_kareleri_puandan_cikar(tmp_path):
    orj = _dizin(tmp_path, "orj", (True, False, True))
    yeni = _dizin(tmp_path, "yeni", (False, False, False))
    # tek geçerli kare (50) aynı → 1.0; düz kareler (0, 100) yeniden kuruluma bakmaksızın sayılmaz
    assert K.yeniden_puan(orj, yeni) == 1.0
    assert K.yeniden_puan(orj, _dizin(tmp_path, "bos", (True, True, True))) < 1.0


def test_tum_referans_duzse_puan_yok(tmp_path):
    orj = _dizin(tmp_path, "orj", (True, True, True))
    yeni = _dizin(tmp_path, "yeni", (False, False, False))
    assert K.yeniden_puan(orj, yeni) is None
    assert K.gecerli_kareler(orj) == []


def _hakem_hazirla(monkeypatch, yanit):
    monkeypatch.setattr(K, "YARGIC", tuple(yanit))
    monkeypatch.setattr(K, "DUSEN", {})
    monkeypatch.setattr(K, "SABIT_OY", set())
    monkeypatch.setattr(K, "KULLANILAN", {})
    monkeypatch.setattr(K, "HAIKU_TAVAN", 0)
    monkeypatch.setattr(K, "yargic", lambda aile, ist: json.dumps(yanit[aile]))
    h = {"ad": "t", "maddeler": [{"madde": f"m{i}"} for i in range(5)]}
    return h, {"skill": [{"madde": "a"}], "zemin": [{"madde": "b"}]}


def test_hepsi_ayni_oy_gecersiz_aile_duser(monkeypatch):
    ayri = {"A": [1, 1, 0, 1, 1], "B": [1, 0, 0, 1, 0]}
    h, notlar = _hakem_hazirla(monkeypatch, {
        "mistral": {"A": [1] * 5, "B": [1] * 5},  # ayrıştırmıyor
        "openai": ayri, "google": ayri, "alibaba": ayri})
    import random
    p = K.hakem(h, notlar, random.Random(1))
    assert p is not None
    assert "mistral" not in K.KULLANILAN and set(K.KULLANILAN) == {"openai", "google"}
    assert "mistral" in K.SABIT_OY
    assert sorted(p.values()) == [0.4, 0.8]  # oylar mistral'siz sayıldı


def test_hepsi_sifir_da_gecersiz_ama_1_0_ayrimi_gecerli(monkeypatch):
    assert K.oy_gecerli([[0] * 5, [0] * 5]) is False
    assert K.oy_gecerli([[1] * 5, [1] * 5]) is False
    assert K.oy_gecerli([[1] * 5, [0] * 5]) is True


def test_gecerli_oy_yetmezse_hakem_none(monkeypatch):
    sabit = {"A": [1] * 5, "B": [1] * 5}
    h, notlar = _hakem_hazirla(monkeypatch, {"mistral": sabit, "openai": sabit})
    import random
    assert K.hakem(h, notlar, random.Random(1)) is None


def test_rea_hata_json_kanit_degil(monkeypatch):
    monkeypatch.setattr(K, "rea_yol", lambda: "C:/x/rea.cmd")
    monkeypatch.setattr(K.subprocess, "run", lambda *a, **k: type("C", (), {"stdout": '{"error":"x","code":"unsupported_target"}'})())
    with pytest.raises(K.ReaYok):
        K.rea_kanit({"tur": "js", "yol": "a.js"})
