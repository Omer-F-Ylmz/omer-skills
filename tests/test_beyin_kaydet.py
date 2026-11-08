import sys
from pathlib import Path

import pytest

KOK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KOK / "tools"))
import beyin  # noqa: E402
import beyin_kayit as bk  # noqa: E402


@pytest.fixture
def kasa(tmp_path, monkeypatch):
    monkeypatch.setattr(bk, "PROJELER", tmp_path)
    return tmp_path


def test_kaydet_blok_yazar(kasa, capsys):
    beyin.main(["kaydet", "demo", "ilk ders\nikinci satır", "--etiket", "basari"])
    s = (kasa / "demo.md").read_text(encoding="utf-8")
    assert s.startswith("# demo\n") and "· basari" in s and "- ilk ders\n- ikinci satır" in s
    assert "yazıldı" in capsys.readouterr().out


def test_ayni_metin_iki_kez_yazilmaz(kasa, capsys):
    beyin.main(["kaydet", "demo", "ders A"])
    beyin.main(["kaydet", "demo", "ders A"])
    assert (kasa / "demo.md").read_text(encoding="utf-8").count("ders A") == 1
    assert "zaten yazıldı" in capsys.readouterr().out


def test_bos_metin_yazmaz(kasa):
    beyin.main(["kaydet", "demo", "  "])
    assert not (kasa / "demo.md").exists()


def test_zorunlu_arac_kaydet_ogrenme_kaniti():
    import importlib.util
    spec = importlib.util.spec_from_file_location("za", KOK / ".kos/kopru/zorunlu_arac.py")
    za = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(za)
    assert any("beyin.py kaydet" in x for x in za.OGRENME_SONDA)
