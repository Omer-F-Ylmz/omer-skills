import importlib.util
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("token_12_uygula", KOK / "onay" / "token_12_uygula.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def test_uygula_kendi_yedegine_yazar_geri_bayt_bayt_doner(tmp_path):
    ev = tmp_path / ".claude"
    (ev / "agents").mkdir(parents=True)
    (ev / "agents-yedek-token10").mkdir()  # TOKEN-10 yedeği varken TOKEN-12 ayrı dizine yedekler
    (ev / "settings.json").write_text("{}", encoding="utf-8")
    p = ev / "agents" / "engineering-x.md"
    p.write_bytes("---\r\nname: X Engineer\r\ndescription: Uzun eski açıklama\r\ncolor: blue\r\n---\r\ngövde\r\n".encode("utf8"))
    once = p.read_bytes()
    es = {"engineering-x": "Kısa yeni açıklama"}

    assert m.main(["uygula"], ev, es) == 0
    assert p.read_bytes() == once.replace("Uzun eski açıklama".encode("utf8"), "Kısa yeni açıklama".encode("utf8"))
    assert (ev / "agents-yedek-token12" / "engineering-x.md").read_bytes() == once
    assert m.main(["--geri"], ev, es) == 0
    assert p.read_bytes() == once and not (ev / "agents-yedek-token12").exists()
    assert (ev / "agents-yedek-token10").is_dir()


def test_esleme_dosyasi_87_ajan_120_kr_alti():
    es = m.t10.esleme(m.ESLEME)
    assert len(es) == 87 and all(0 < len(v) <= 120 and "\n" not in v for v in es.values())
    assert len(on := m.t10.esleme(m.ONARIM)) == 2 and not on.keys() & es.keys() and all(len(v) <= 120 for v in on.values())
