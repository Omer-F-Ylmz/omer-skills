"""MÜKEMMEL-1b (O78): sessiz A düşüşü 0 · altyazı orijinal dil · paket kare satırı gerçek sayı."""
import pytest

from video import metin as m
from video import parti as pt
from video import yonlendir as yon
from test_derinlik_kapanis import ROTA10, Sahte, _ctx, _hazir, _ns, _pid
from test_m9 import _alt, _d


# 2: OmniRoute/anahtar yoksa motor başlamaz, çağrı 0, DUR
def test_omni_yok_dur_cagri_0(tmp_path, monkeypatch, capsys):
    kok = _hazir(tmp_path, rota=ROTA10)
    monkeypatch.setattr(pt, "YOKLA", lambda *a, **k: "OmniRoute yok: ConnectionRefusedError", raising=False)
    monkeypatch.setattr(yon, "tara_v10", lambda *a, **k: pytest.fail("DUR'da tara_v10 çağrılmaz"))
    baslat, bekle = [], []
    monkeypatch.setattr(pt, "BASLAT", lambda: baslat.append(1), raising=False)
    monkeypatch.setattr(pt, "BEKLE", bekle.append, raising=False)
    s = Sahte()
    ctx = _ctx(kok, s)
    ctx["env"]["OMNIROUTE_KEY"] = "k"
    assert pt.parti(_ns("devam", _pid(kok)), ctx) == 4
    assert s.cagrilar == [] and "DUR: OmniRoute/anahtar yok (OmniRoute yok: ConnectionRefusedError)" in capsys.readouterr().out
    assert baslat == [1] and sum(bekle) <= 90  # MÜKEMMEL-2c: bir kez başlat, ≤ 90 s yokla, kalkmazsa DUR


# MÜKEMMEL-2c: anahtar yoksa başlatma denenmez, doğrudan DUR
def test_omni_yok_anahtar_yok_baslatma_yok(tmp_path, monkeypatch, capsys):
    kok = _hazir(tmp_path, rota=ROTA10)
    monkeypatch.setattr(pt, "YOKLA", lambda *a, **k: "OmniRoute yok: ConnectionRefusedError", raising=False)
    monkeypatch.setattr(pt, "BASLAT", lambda: pytest.fail("anahtarsız başlatma yok"), raising=False)
    ctx = _ctx(kok, Sahte())
    ctx["env"].pop("OMNIROUTE_KEY", None)
    assert pt.parti(_ns("devam", _pid(kok)), ctx) == 4
    assert "DUR: OmniRoute/anahtar yok" in capsys.readouterr().out


# MÜKEMMEL-2c: kendiliğinden başlatma kalkarsa koşu sürer ve satır yazılır
def test_omni_kendiliginden_baslatildi(tmp_path, monkeypatch, capsys):
    kok = _hazir(tmp_path, rota=ROTA10)
    yanit = iter(["OmniRoute yok: ConnectionRefusedError", "OmniRoute yok: ConnectionRefusedError", None])
    monkeypatch.setattr(pt, "YOKLA", lambda *a, **k: next(yanit), raising=False)
    baslat = []
    monkeypatch.setattr(pt, "BASLAT", lambda: baslat.append(1), raising=False)
    monkeypatch.setattr(pt, "BEKLE", lambda s: None, raising=False)

    def v10(*a, **k):
        raise KeyboardInterrupt
    monkeypatch.setattr(yon, "tara_v10", v10)
    ctx = _ctx(kok, Sahte(kes=1))
    ctx["env"]["OMNIROUTE_KEY"] = "k"
    try:
        pt.parti(_ns("devam", _pid(kok)), ctx)
    except KeyboardInterrupt:
        pass
    out = capsys.readouterr().out
    assert baslat == [1] and "OmniRoute kendiliğinden başlatıldı (" in out and "DUR" not in out
    # MÜKEMMEL-2d: gözetimsiz koşuda kalıcı iz — defterde satır, çağrı tavanına girmez
    iz = [x for x in pt.tr.kayit_oku(kok / ".kos" / _pid(kok) / "defter.jsonl") if x.get("adim") == "omniroute_baslat"]
    assert len(iz) == 1 and "sure_s" in iz[0] and pt._defter(kok / ".kos" / _pid(kok))[0] == 0


# 2: A taşıyıcısı yalnız --a-yolu ile (yoklama ve V10 yok)
def test_a_yolu_bayragi(tmp_path, monkeypatch, capsys):
    kok = _hazir(tmp_path, rota=ROTA10)
    monkeypatch.setattr(pt, "YOKLA", lambda *a, **k: pytest.fail("--a-yolu'nda yoklama yok"), raising=False)
    monkeypatch.setattr(yon, "tara_v10", lambda *a, **k: pytest.fail("--a-yolu'nda tara_v10 çağrılmaz"))
    ns = _ns("devam", _pid(kok))
    ns.a_yolu = True
    s = Sahte(kes=1)
    try:
        pt.parti(ns, _ctx(kok, s))
    except KeyboardInterrupt:
        pass
    assert s.cagrilar and "DUR" not in capsys.readouterr().out


# 3: orijinal dil (meta.language) elle → orijinal oto → eski sıra; language yoksa eski sıra
def test_altyazi_orijinal_dil_once():
    oto = {"de-orig": [1], "en": [1]}
    assert m.dil_sec({"language": "de", "subtitles": {"tr": [1], "en": [1]}, "automatic_captions": oto}) == ("de-orig", "oto")
    assert m.dil_sec({"language": "de-DE", "subtitles": {"tr": [1], "de": [1]}, "automatic_captions": oto}) == ("de", "elle")
    assert m.dil_sec({"subtitles": {"tr": [1], "en": [1]}, "automatic_captions": oto}) == ("tr", "elle")


# 4: paket satırı paket kurulduktan sonra gerçek kare sayısını ve sınırı yazar
def test_paket_satiri_gercek_kare(tmp_path, capsys):
    pd, onb = tmp_path / "pd", tmp_path / "onb"
    pd.mkdir()
    (pd / "defter.jsonl").write_text("", encoding="utf-8")

    def paket(v):
        (onb / v / "paket.md").write_text("# p\n", encoding="utf-8")
        print("paket: x · kareler: a b c · segment 3 · kare 3 · ~100 token metin")
        return 0
    pt._kos(pd, _d("k1"), onb, tmp_path / "t", _alt(onb, sure=1200, paket=paket)[0], str, None, {})
    s = [s for s in capsys.readouterr().out.splitlines() if s.startswith("paket k1:")]
    assert len(s) == 1 and s[0].startswith("paket k1: kare 3 (aday tabanı ") and s[0].endswith("sınır jeton bütçesi)")
