"""ROUTER-1 yönlendirici: kural seçimi, sınıflama geri düşüşü, yükseltme/kayıt/SIRA, haftalık özet."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import yonlendir  # noqa: E402


def test_kural_tablosu_en_az_15_tur_ve_gecerli_kademe():
    k = yonlendir.kurallar()
    assert len(k["tur"]) >= 15
    assert all(t["kademe"] in yonlendir.SIRALI and t["dogrulama"] in ("light", "full") for t in k["tur"].values())


def test_sec_boyut_risk_ve_t0_sabit():
    assert yonlendir.sec("kod-yaz")["kademe"] == "T3"
    assert yonlendir.sec("kod-yaz", "buyuk")["kademe"] == "T4"
    assert yonlendir.sec("sayim", "buyuk", ["guvenlik"])["kademe"] == "T0"
    r = yonlendir.sec("regex", risk=["kullaniciya-gider"])
    assert (r["kademe"], r["dogrulama"], r["effort"]) == ("T2", "full", "medium")
    assert yonlendir.sec("mimari", "buyuk", ["guvenlik"])["kademe"] == "T4"
    assert yonlendir.sec("yok-boyle") is None


def test_sinifla_alinti_tutarsa_tur_tutmazsa_t3():
    tanim = "Bu repodaki LICENSE dosyasının lisansını bul."
    iyi = lambda kol, m, g: ('{"etiket": "lisans", "alinti": "LICENSE dosyasının lisansını bul"}', "stop", m, {"total_tokens": 9})
    assert yonlendir.sinifla(tanim, sor=iyi)["kademe"] == "T1"
    uydurma = lambda kol, m, g: ('{"etiket": "lisans", "alinti": "tanımda olmayan bir cümle burada"}', "stop", m, {})
    r = yonlendir.sinifla(tanim, sor=uydurma)
    assert (r["kademe"], r["dogrulama"]) == ("T3", "full")

    def patla(*a):
        raise OSError("ağ yok")
    assert yonlendir.sinifla(tanim, sor=patla)["kademe"] == "T3"


def test_argv_yalin_oturum():
    b = yonlendir.argv(yonlendir.sec("yargi"))
    assert b[:4] == ["--model", "claude-sonnet-5-5", "--effort", "high"] and "--safe-mode" in b


def test_kos_yukseltir_kaydeder_tukenince_sira(tmp_path, monkeypatch):
    monkeypatch.setattr(yonlendir, "KAYIT", tmp_path / "k.jsonl")
    monkeypatch.setattr(yonlendir, "SIRA", tmp_path / "SIRA.md")
    cikti, kd = yonlendir.kos(yonlendir.sec("regex"), lambda kd: (kd["kademe"], {"giris": 5, "cikis": 1}),
                              lambda c, kd: c == "T3", ad="g1")
    assert (cikti, kd["kademe"]) == ("T3", "T3")
    s = [json.loads(x) for x in (tmp_path / "k.jsonl").read_text(encoding="utf-8").splitlines()]
    assert [(x["kademe"], x["sonuc"], x["yukseltme"]) for x in s] == [("T2", "kaldi", 0), ("T3", "gecti", 1)]
    assert not (tmp_path / "SIRA.md").exists()
    cikti, kd = yonlendir.kos(yonlendir.sec("regex"), lambda kd: (None, {}), lambda c, kd: False, ad="g2")
    assert cikti is None and kd["kademe"] == "T4"  # T2 → T3 → T4, iki yükseltme
    assert "YÜKSELTME TÜKENDİ: g2" in (tmp_path / "SIRA.md").read_text(encoding="utf-8")


def test_ozet_yukari_oneri_ve_yaz(tmp_path, monkeypatch):
    kural = tmp_path / "kural.json"
    kural.write_text(yonlendir.KURAL.read_text(encoding="utf-8"), encoding="utf-8")
    monkeypatch.setattr(yonlendir, "KURAL", kural)
    monkeypatch.setattr(yonlendir, "KAYIT", tmp_path / "k.jsonl")
    monkeypatch.setattr(yonlendir, "SIRA", tmp_path / "SIRA.md")
    kd = yonlendir.sec("regex")
    for sonuc in ("kaldi", "kaldi", "gecti"):
        yonlendir.kaydet(kd, sonuc, {}, 0)
    o = yonlendir.ozet(yaz=True)
    assert o["oneri"] == {"regex": "T3"} and yonlendir.kurallar()["tur"]["regex"]["kademe"] == "T3"
