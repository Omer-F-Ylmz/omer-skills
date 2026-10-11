import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import zip_denetle as zd  # noqa: E402


def _zip(yol, dosyalar):
    with zipfile.ZipFile(yol, "w") as z:
        for ad, icerik in dosyalar.items():
            z.writestr(ad, icerik)
    return yol


def test_temiz_zip_gecer(tmp_path):
    z = _zip(tmp_path / "a.zip", {"a/SKILL.md": "---\nname: a\ndescription: Does a. Use when a.\n---\n# a\n"})
    assert zd.denetle(z) == []


def test_claude_ai_ret_nedenleri(tmp_path):
    # 16:40: claude.ai "description cannot contain XML tags" ile reddetti; blender-uretim zip'inde __pycache__ vardı
    z = _zip(tmp_path / "b.zip", {"b/SKILL.md": "---\nname: b\ndescription: says /b <ad|konu>.\n---\n",
                                  "b/references/__pycache__/x.cpython-313.pyc": "x"})
    s = " ".join(zd.denetle(z))
    assert "XML" in s and "__pycache__" in s


def test_belge_ornek_anahtari_yanlis_alarm_degil(tmp_path):
    # 16:50: mukul975 güvenlik paketlerindeki AWS belge örnekleri (AKIAIOSFODNN7EXAMPLE, AKIAXXXX…) gerçek sır değil
    ornek = "AKIA" + "IOSFODNN7EXAMPLE" + " ve AKIA" + "X" * 16 + " ve AKIA" + "EXPOSEDKEY123456"
    z = _zip(tmp_path / "f.zip", {"f/SKILL.md": "---\nname: f\ndescription: Use when f.\n---\n", "f/R.md": ornek})
    assert zd.denetle(z) == []
    gercek = _zip(tmp_path / "g.zip", {"g/SKILL.md": "---\nname: g\ndescription: Use when g.\n---\n",
                                         "g/R.md": "AKIA" + "Q3J7K2LM9PZT4WXY"})
    assert any("gizli" in x for x in zd.denetle(gercek))


def test_eksik_ve_uzun(tmp_path):
    assert any("SKILL.md yok" in x for x in zd.denetle(_zip(tmp_path / "c.zip", {"c/README.md": "x"})))
    uzun = _zip(tmp_path / "d.zip", {"d/SKILL.md": "---\nname: d\ndescription: " + "a" * 1100 + "\n---\n"})
    assert any("1024" in x for x in zd.denetle(uzun))
    adsiz = _zip(tmp_path / "e.zip", {"e/SKILL.md": "---\ndescription: x\n---\n"})
    assert any("name" in x for x in zd.denetle(adsiz))
