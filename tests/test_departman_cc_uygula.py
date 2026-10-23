import importlib.util
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("departman_cc_uygula", KOK / "onay" / "departman_cc_uygula.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def kur(tmp_path):
    k = tmp_path / "kaynak"
    (k / "departman-a").mkdir(parents=True)
    (k / "departman-a" / "SKILL.md").write_text("v1", encoding="utf-8")
    (k / "baska").mkdir()
    (k / "baska" / "SKILL.md").write_text("x", encoding="utf-8")
    return k, tmp_path / "hedef", tmp_path / "yedek"


def test_yalniz_departman_kopyalanir(tmp_path):
    k, h, y = kur(tmp_path)
    assert m.uygula(k, h, y) == ["departman-a"]
    assert (h / "departman-a" / "SKILL.md").read_text(encoding="utf-8") == "v1"
    assert not (h / "baska").exists()


def test_ozdes_olana_dokunmaz_farkliysa_yedekler(tmp_path):
    k, h, y = kur(tmp_path)
    m.uygula(k, h, y)
    assert m.uygula(k, h, y) == []
    (k / "departman-a" / "SKILL.md").write_text("v2", encoding="utf-8")
    assert m.uygula(k, h, y) == ["departman-a"]
    assert (h / "departman-a" / "SKILL.md").read_text(encoding="utf-8") == "v2"
    assert len(list((y / "departman-a").glob("*"))) == 1


def test_geri_yedegi_koyar(tmp_path):
    k, h, y = kur(tmp_path)
    m.uygula(k, h, y)
    (k / "departman-a" / "SKILL.md").write_text("v2", encoding="utf-8")
    m.uygula(k, h, y)
    m.geri(k, h, y)
    assert (h / "departman-a" / "SKILL.md").read_text(encoding="utf-8") == "v1"
