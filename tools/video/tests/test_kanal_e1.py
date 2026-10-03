"""KANAL-2b E1: metadata hatası satır notuna ve .kos günlüğüne yazılır."""
from video import tarama as tr


def test_e1_meta_hatasi_nota_ve_gunluge(tmp_path):
    g = tmp_path / ".kos" / "kanal" / "kuyruk-meta.log"
    sat = [("aaaaaaaaaaa", "?", "?", "kaynak: Ömer", "ERROR: Video unavailable | x"), ("bbbbbbbbbbb", 1.0, "b", "kaynak: Ömer")]
    yeni, _ = tr.kuyruk_ekle("# k\n", sat, raporlu=set(), muaf=set(), baslik="## E", gunluk=g)
    assert "| aaaaaaaaaaa | ? | ? | kaynak: Ömer · meta hatası: ERROR: Video unavailable / x | bekliyor |" in yeni
    assert "| bbbbbbbbbbb | 1.0 | b | kaynak: Ömer | bekliyor |" in yeni
    assert g.read_text(encoding="utf-8").splitlines() == ["aaaaaaaaaaa\tERROR: Video unavailable | x"]
