"""uret_malzeme: sağlayıcı sırası, tavan, çok bacaklı video (ağ çağrısı yok, sahte sağlayıcı)."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import uret_malzeme as um


class Sahte(um.Saglayici):
    def __init__(self, ad, ucretsiz, fiyat, turler=("gorsel", "video", "3d"), hazir=True):
        self.ad, self.ucretsiz, self.fiyat, self.turler, self._hazir = ad, ucretsiz, fiyat, turler, hazir
        self.cagri = []

    def tahmin(self, tur, adet=1):
        return 0.0 if self.ucretsiz else self.fiyat * adet

    def hazir(self):
        return self._hazir

    def uret(self, tur, prompt, girdi, cikti):
        self.cagri.append((tur, prompt, girdi))
        cikti.write_bytes(b"x")
        return cikti


def test_ucretsiz_once_ucretli_sonra():
    p, f, ucuz = Sahte("p", False, 0.5), Sahte("f", True, 0), Sahte("u", False, 0.02)
    assert [s.ad for s in um.sirala("gorsel", [p, ucuz, f])] == ["f", "u", "p"]


def test_hazir_olmayan_ve_turu_desteklemeyen_elenir():
    a = Sahte("a", True, 0, hazir=False)
    b = Sahte("b", True, 0, turler=("gorsel",))
    c = Sahte("c", False, 0.1)
    assert [s.ad for s in um.sirala("3d", [a, b, c])] == ["c"]


def test_tavan_asilirsa_secilmez():
    s = Sahte("p", False, 0.5)
    with pytest.raises(ValueError, match="tavan"):
        um.sec("3d", [s], tavan=0.30)
    assert um.sec("3d", [s], tavan=0.60) is s


def test_ucretsiz_tavansiz_secilir():
    assert um.sec("gorsel", [Sahte("f", True, 0)], tavan=None).ad == "f"


def test_ucretli_tavansiz_reddedilir():
    with pytest.raises(ValueError, match="tavan"):
        um.sec("gorsel", [Sahte("p", False, 0.1)], tavan=None)


def test_video_bacak_son_kareden_baslar(tmp_path):
    s = Sahte("v", True, 0)
    ilk = tmp_path / "ilk.png"
    ilk.write_bytes(b"i")
    kareler = []

    def son_kare(video, hedef):
        kareler.append(video.name)
        hedef.write_bytes(b"k")
        return hedef

    cikt = um.video_bacaklari(s, ["bir", "iki", "uc"], ilk, tmp_path, son_kare)
    assert [c[2].name for c in s.cagri] == ["ilk.png", "bacak1-son.png", "bacak2-son.png"]
    assert kareler == ["bacak1.mp4", "bacak2.mp4"]  # son bacağın son karesi gerekmez
    assert len(cikt) == 3


def test_kuru_maliyet_yazar_ve_uretmez(tmp_path, capsys):
    rc = um.main(["3d", "--girdi", str(tmp_path / "x.png"), "--cikti", str(tmp_path), "--kuru"])
    assert rc == 0
    assert "tahmin" in capsys.readouterr().out
