"""TOKEN-7c-devam-3: ikili yol jeton bayrakları (A şema önek · B haiku dar şema · C kare ayıklama); varsayılan kapalı."""
from PIL import Image

from video import parti as pt


def test_bayrak_kapali_sema_ayni():
    assert pt.JETON == "" and pt.jeton_sema("abc", "", "claude-haiku-5-5") == pt.sema(["abc"], iz=True)


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
    assert len(pt.kare_ayikla(kr)) == 2
