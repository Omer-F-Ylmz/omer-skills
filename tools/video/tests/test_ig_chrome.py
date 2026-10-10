"""VİDEO-E: embed + og boş → Desktop Chrome notu yedek meta (ağ yok)."""
import json

import pytest

from video import instagram as ig

NOT = """# ig-ABC — Desktop Chrome okuması
kaynak: https://www.instagram.com/reel/ABC/
hesap: @product.with_zeey (doğrulanmış) · tür: reel

## Açıklama özeti
4 bağlam dosyası: SECURITY.md · CODE_STYLE.md.
Link/repo/araç adı: yok.

## Desktop ön inceleme
- iç not, açıklamaya girmemeli
"""


def test_not_ayristir(tmp_path):
    (tmp_path / "ig-ABC.md").write_text(NOT, encoding="utf-8")
    p = ig.chrome_notu("ABC", tmp_path)
    assert p["hesap"] == "product.with_zeey" and p["tur"] == "kısıtlı" and p["ogeler"] == []
    assert "SECURITY.md" in p["aciklama"] and "iç not" not in p["aciklama"]
    assert ig.chrome_notu("YOK", tmp_path) is None


def test_getir_yedek(tmp_path, monkeypatch):
    kok = tmp_path / "notlar"
    kok.mkdir()
    (kok / "ig-ABC.md").write_text(NOT, encoding="utf-8")
    monkeypatch.setattr(ig, "CHROME_NOT", kok)

    def bos(kod):
        raise ig.IgHata("ig: embed verisi yok")
    monkeypatch.setattr(ig, "sayfa", bos)
    d = tmp_path / "ig-ABC"
    d.mkdir()
    meta = ig.getir(d)
    assert meta["video"] is False and meta["gorseller"] == [] and "Chrome notundan" in meta["goz_not"]
    assert json.loads((d / "meta.json").read_text(encoding="utf-8"))["channel"] == "product.with_zeey"


def test_getir_not_yoksa_hata(tmp_path, monkeypatch):
    monkeypatch.setattr(ig, "CHROME_NOT", tmp_path)

    def bos(kod):
        raise ig.IgHata("ig: embed verisi yok")
    monkeypatch.setattr(ig, "sayfa", bos)
    d = tmp_path / "ig-XYZ"
    d.mkdir()
    with pytest.raises(ig.IgHata):
        ig.getir(d)


def test_engel_yedeklenmez(tmp_path, monkeypatch):
    (tmp_path / "ig-ABC.md").write_text(NOT, encoding="utf-8")
    monkeypatch.setattr(ig, "CHROME_NOT", tmp_path)

    def engel(kod):
        raise ig.IgHata("ig: engellendi")
    monkeypatch.setattr(ig, "sayfa", engel)
    d = tmp_path / "ig-ABC"
    d.mkdir()
    with pytest.raises(ig.IgHata, match="engellendi"):
        ig.getir(d)
