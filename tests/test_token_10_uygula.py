import importlib.util
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("token_10_uygula", KOK / "onay" / "token_10_uygula.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def ajan(d, ad, aciklama):
    (d / f"{ad}.md").write_bytes(f"---\r\nname: {ad}\r\ndescription: {aciklama}\r\n  devam satırı\r\nmodel: sonnet\r\n---\r\ngövde: aynen\r\n".encode("utf8"))


def test_uygula_yalniz_aciklama_degisir_geri_bayt_bayt_doner(tmp_path):
    ev = tmp_path / ".claude"
    (ev / "agents").mkdir(parents=True)
    (ev / "skills" / "ajan-getir").mkdir(parents=True)
    (ev / "settings.json").write_text("{}", encoding="utf-8")
    ajan(ev / "agents", "fe-a", "Uzun eski açıklama")
    ajan(ev / "agents", "Plugin Ajan", "dokunulmaz")
    once = {p.name: p.read_bytes() for p in (ev / "agents").iterdir()}
    es = {"fe-a": "Kısa: yeni açıklama", "yok-b": "x"}

    assert m.main(["--kuru"], ev, es) == 0
    assert {p.name: p.read_bytes() for p in (ev / "agents").iterdir()} == once  # kuru dokunmaz
    assert m.main(["uygula"], ev, es) == 0
    yeni = (ev / "agents" / "fe-a.md").read_bytes().decode("utf8")
    assert 'description: "Kısa: yeni açıklama"\r\nmodel: sonnet\r\n---\r\ngövde: aynen\r\n' in yeni  # ':' tırnaklı, CRLF + gövde korunur
    assert "devam satırı" not in yeni and yeni.startswith("---\r\nname: fe-a\r\n")
    assert (ev / "agents" / "Plugin Ajan.md").read_bytes() == once["Plugin Ajan.md"]
    assert "fe-a" in (ev / "skills" / "ajan-getir" / "katalog.tsv").read_text(encoding="utf-8")

    assert m.main(["--geri"], ev, es) == 0
    assert {p.name: p.read_bytes() for p in (ev / "agents").iterdir()} == once
    assert not (ev / "agents-yedek-token10").exists()
