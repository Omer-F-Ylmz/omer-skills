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
    assert sum(v["durum"] == "gecerli" for v in s.values()) == 1  # 6 deneme (google×2, nvidia×2, alibaba×2) bitti; minimax/mistral denenmedi


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
