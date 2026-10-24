import importlib.util
import sys
from pathlib import Path

import pytest

YOL = Path(__file__).resolve().parents[2] / ".kos" / "kopru" / "gorsel_hakem.py"


@pytest.fixture
def hakem(monkeypatch, tmp_path):
    monkeypatch.setattr(sys, "argv", ["gorsel_hakem.py"])  # main() içe aktarmada koşar; PNG yok → çıktı yok
    spec = importlib.util.spec_from_file_location("gorsel_hakem", YOL)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    m.ONBELLEK = tmp_path / "hakem-onbellek.json"  # sahte yanıtlar gerçek önbelleğe yazılıp sonraki koşuda çağrıyı atlatmasın
    m.KOTA = tmp_path / "hakem-kota.json"  # sahte hatalar gerçek kota kaydına sızıp gerçek koşuda aileleri susturmasın
    m.KALIB = tmp_path / "hakem-kalib.json"
    monkeypatch.setattr(m, "kalib", lambda e: {"lo": 0, "hi": 10})  # ölçek ağdan değil sabit: norm = ham puan × 10
    monkeypatch.setattr(m, "yerel_istek", lambda *a: (_ for _ in ()).throw(OSError("test: yerel Ollama yok")))
    return m


def test_kiyas_yaniti_kalite_farki_verir(hakem):
    assert hakem.ayikla('x {"kalite_farki": 7} y', kiyas=True) == {"kalite_farki": 7}


def test_kiyas_alani_eksikse_hata(hakem):
    with pytest.raises(KeyError):
        hakem.ayikla('{"puan": 7}', kiyas=True)


def test_ref_iki_gorsel_gonderir_ve_kiyas_bicimi_kullanir(hakem, monkeypatch):
    gorulen = {}

    def sahte(e, icerik, *_):
        gorulen["icerik"] = icerik
        return '{"kalite_farki": 8}'

    monkeypatch.setattr(hakem, "veri_url", lambda p: f"data:{p}")
    monkeypatch.setattr(hakem.h, "_istek", sahte)
    s = hakem.sor("aday.png", "soru", ref="ref.png")
    assert len(s) == hakem.CIFT and all(v["kalite_farki"] == 8 for v in s.values())
    urller = [c["image_url"]["url"] for c in gorulen["icerik"] if c["type"] == "image_url"]
    assert urller == ["data:ref.png", "data:aday.png"]
    assert "REFERANS" in gorulen["icerik"][0]["text"]


def aileye_gore_yanit(hakem, monkeypatch, yanit, zamanlar=None):  # yanit: aile → metin | istisna; listelenmeyen aile GECERLI
    def sahte(e, icerik, max_tokens, zaman):
        if zamanlar is not None:
            zamanlar.append(zaman)
        aile = next(a for a, adaylar in hakem.ADAY.items() if e in adaylar)
        y = yanit.get(aile, GECERLI)
        if isinstance(y, Exception):
            raise y
        return y

    def haiku_kapali(icerik):
        raise OSError("test: gerçek Haiku çağrısı yok")

    monkeypatch.setattr(hakem, "veri_url", lambda p: f"data:image/jpeg;base64,{p}")
    monkeypatch.setattr(hakem.h, "_istek", sahte)
    monkeypatch.setattr(hakem, "haiku_gorsel", haiku_kapali)


GECERLI = '{"puan": 7, "sivi_mi": true, "plastik_gorunen": false}'


def test_ayrisma_hatasi_kararsiz_sayilir_puan_yazilmaz(hakem, monkeypatch):
    aileye_gore_yanit(hakem, monkeypatch, {"google": "yanıt yok"})
    s = hakem.sor("aday.png", "soru")
    assert s["google"]["durum"] == "kararsiz" and "puan" not in s["google"]
    assert s["alibaba"]["durum"] == s["nvidia"]["durum"] == "gecerli"


def test_tek_aile_hata_verince_yedek_aile_devreye_girer(hakem, monkeypatch):
    aileye_gore_yanit(hakem, monkeypatch, {"google": hakem.h.Hata(503, "geçici")})
    s = hakem.sor("aday.png", "soru")
    assert s["google"]["durum"] == "kararsiz" and "503" in s["google"]["sebep"]
    assert sum(v["durum"] == "gecerli" for v in s.values()) == hakem.CIFT


def test_hic_aile_toplanamazsa_haiku_tek_oy_verir(hakem, monkeypatch):
    aileye_gore_yanit(hakem, monkeypatch, {a: TimeoutError() for a in hakem.ADAY})
    monkeypatch.setattr(hakem, "haiku_gorsel", lambda icerik: GECERLI)
    s = hakem.sor("aday.png", "soru")
    assert s["haiku"]["durum"] == "gecerli" and s["haiku"]["model"].startswith("haiku/")
    assert sum(v["durum"] == "gecerli" for v in s.values()) == 1  # bütün ücretsiz halkalar + yerel düştü, yalnız Haiku oy verdi


def test_sayi_disi_puan_reddedilir(hakem):
    for bozuk in ('{"puan": "7", "sivi_mi": true, "plastik_gorunen": false}',
                  '{"puan": 7.5, "sivi_mi": true, "plastik_gorunen": false}',
                  '{"puan": true, "sivi_mi": true, "plastik_gorunen": false}'):
        with pytest.raises(ValueError):
            hakem.ayikla(bozuk)


def test_buyuk_gorsel_1024e_kucultulur(hakem, tmp_path):
    import base64
    import io

    from PIL import Image

    yol = tmp_path / "buyuk.png"
    Image.new("RGB", (3000, 2000), "white").save(yol)
    veri = hakem.veri_url(yol)
    im = Image.open(io.BytesIO(base64.b64decode(veri.split(",", 1)[1])))
    assert max(im.size) == 1024


def test_istek_basi_zaman_asimi_60_sn(hakem, monkeypatch):
    zamanlar = []
    aileye_gore_yanit(hakem, monkeypatch, {"google": GECERLI, "meta": GECERLI, "nvidia": GECERLI}, zamanlar)
    hakem.sor("aday.png", "soru")
    assert zamanlar and set(zamanlar) == {60}


def test_kota_yenen_model_atlanir_ve_kayda_yazilir(hakem, monkeypatch):
    cagri = []

    def sahte(e, icerik, max_tokens, zaman):
        cagri.append(hakem.h.ad(e))
        if e.prov == "gemini" and e.model == "gemini-3.5-flash-lite":
            raise hakem.h.Hata(429, "Quota exceeded PerDay")
        return GECERLI

    monkeypatch.setattr(hakem, "veri_url", lambda p: f"data:image/jpeg;base64,{p}")
    monkeypatch.setattr(hakem.h, "_istek", sahte)
    s = hakem.sor("a.png", "soru")
    assert s["google"]["model"] == "gemini/gemini-3.6-flash"  # ilk aday 429 → ikinci aday aynı aileyi doldurdu
    kay = hakem.kota_oku()["gemini/gemini-3.5-flash-lite"]
    assert kay["kod"] == 429 and kay["until"] - __import__("time").time() > 3600  # günlük kota ≈ 4 sa
    cagri.clear()
    hakem.ONBELLEK.unlink(missing_ok=True)
    hakem.sor("b.png", "soru")
    assert "gemini/gemini-3.5-flash-lite" not in cagri  # kayıt süresi dolana dek tekrar denenmez


def test_oy_satirinda_aile_model_olcek_norm_var(hakem, monkeypatch):
    aileye_gore_yanit(hakem, monkeypatch, {})
    s = hakem.sor("aday.png", "soru")
    assert s["google"]["model"].startswith("gemini/") and s["google"]["olcek"] == [0, 10] and s["google"]["norm"] == 70


def test_son_care_yerel_haikudan_once_gelir(hakem, monkeypatch):
    aileye_gore_yanit(hakem, monkeypatch, {a: hakem.h.Hata(503, "geçici") for a in hakem.ADAY})
    monkeypatch.setattr(hakem, "yerel_istek", lambda *a: GECERLI)
    s = hakem.sor("aday.png", "soru")
    assert s["yerel"]["durum"] == "gecerli" and "haiku" in s  # tek oy < ASGARI → Haiku da denenir
    assert s["haiku"]["durum"] == "kararsiz"  # test Haiku'yu kapatır


def test_ram_tavani_asilirsa_yerel_model_yuklenmez(hakem, monkeypatch):
    monkeypatch.undo()  # fixture'ın yerel_istek taklidini kaldır; gerçek kapıyı dene
    spec = importlib.util.spec_from_file_location("gorsel_hakem", YOL)
    m = importlib.util.module_from_spec(spec)
    monkeypatch.setattr(sys, "argv", ["gorsel_hakem.py"])
    spec.loader.exec_module(m)
    monkeypatch.setattr(m, "ram_yuzde", lambda: 95)
    with pytest.raises(m.h.Hata) as x:
        m.yerel_istek(m.ADAY["yerel"][0], [], 100, 10)
    assert x.value.kod == 503


def test_tek_oylu_sonuc_onbellege_yazilmaz(hakem, monkeypatch):
    aileye_gore_yanit(hakem, monkeypatch, {a: TimeoutError() for a in hakem.ADAY if a != "alibaba"})
    s = hakem.sor("aday.png", "soru")
    assert gecerli(s) == 1 and not hakem.ONBELLEK.exists()


def gecerli(s):
    return sum(v["durum"] == "gecerli" for v in s.values())
