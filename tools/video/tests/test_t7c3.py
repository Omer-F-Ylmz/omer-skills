"""TOKEN-7c-devam-3: ikili yol jeton bayrakları (A şema önek · B haiku dar şema · C kare ayıklama); varsayılan kapalı."""
from PIL import Image

from video import parti as pt


def test_bayrak_kapali_sema_ayni():
    assert pt.JETON == "K" and pt.jeton_sema("abc", "K", "claude-haiku-5-5") == pt.sema(["abc"], iz=True)  # VİDEO-9: C kapalı · VİDEO-13-devam-2: K şemaya dokunmaz


def test_a_enum_yok_b_yalniz_haiku():
    vid = lambda s: s["properties"]["videolar"]["items"]
    a = vid(pt.jeton_sema("abc", "A", "claude-sonnet-5-5"))
    assert a["properties"]["id"] == {"type": "string"} and pt.jeton_sema("x", "A", "s") == pt.jeton_sema("y", "A", "s")
    h, s = vid(pt.jeton_sema("abc", "B", "claude-haiku-5-5")), vid(pt.jeton_sema("abc", "B", "claude-sonnet-5-5"))
    assert not set(pt.B_DISI) & (set(h["properties"]) | set(h["required"])) and set(pt.B_DISI) <= set(s["required"])


def test_c_yinelenen_kare_atilir_tavan(tmp_path, monkeypatch):
    def kare(ad, renk):
        im = Image.new("L", (90, 80))
        im.paste(255, (0, 0, renk, 80))  # dikey kenar konumu dHash'i belirler
        im.save(p := tmp_path / ad)
        return str(p)
    kr = [kare("1.jpg", 10), kare("2.jpg", 10), kare("3.jpg", 50), kare("4.jpg", 10)]
    assert pt.kare_ayikla(kr) == [kr[0], kr[2]]  # 2 ve 4, 1'in yinesi (dönüp gelen ekran dahil)
    monkeypatch.setattr(pt, "JETON_KARE", 2)
    kr = [kare(f"k{i}.jpg", 10 * i + 5) for i in range(8)]
    assert len(pt.kare_ayikla(kr)) == 2 and len(pt.kare_ayikla(kr, piksel=True)) == 2


def test_c2_piksel_farki_yazi_degisimini_tutar(tmp_path):
    """VİDEO-9: dHash aynı / yazı farklı kare C'de atılıyordu; C2 (goz.es_kare yöntemi) tutar, dönüp gelen eş ekranı atar."""
    from video import metin as m

    def kare(ad, yazi=False, ters=False):
        im = Image.linear_gradient("L").rotate(270 if ters else 90).resize((480, 270))
        if yazi:
            im.paste(0, (120, 100, 150, 115))  # 30×15 yazı bloğu: 9×8 dHash'i değiştirmez, piksel oranı 0.0035 > ES_ORAN
        im.save(p := tmp_path / ad)
        return str(p)
    a, b, c, d = kare("1.png"), kare("2.png", yazi=True), kare("3.png"), kare("4.png", ters=True)
    dh = lambda y: m.dhash(Image.open(y).convert("L").resize((9, 8)).tobytes())
    assert dh(a) == dh(b) and pt.kare_ayikla([a, b]) == [a]  # C'nin kaybı
    assert pt.kare_ayikla([a, b, c, d], piksel=True) == [a, b, d]  # 3, 1'in eşi (dönüp gelen ekran)
