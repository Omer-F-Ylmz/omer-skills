import importlib.util
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("token_8_is2_uygula", KOK / "onay" / "token_8_is2_uygula.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def ajan(d, ad):
    (d / f"{ad}.md").write_text(f"---\nname: {ad}\nmodel: sonnet\ndescription: {ad} işi\n---\ngövde\n", encoding="utf-8")


def test_uygula_tasir_katalog_bulur_geri_tam_doner(tmp_path, monkeypatch):
    ev = tmp_path / ".claude"
    (ev / "agents").mkdir(parents=True)
    (ev / "skills" / "ajan-getir").mkdir(parents=True)
    (ev / "settings.json").write_text("{}", encoding="utf-8")
    for ad in ("cekirdek-a", "uzman-b", "uzman-c"):
        ajan(ev / "agents", ad)
    monkeypatch.setattr(m, "CEKIRDEK", {"cekirdek-a"})
    once = {p.name: p.read_bytes() for p in (ev / "agents").iterdir()}

    assert m.main(["--kuru"], ev) == 0 and len(once) == 3  # kuru dokunmaz
    assert m.main(["uygula"], ev) == 0
    assert [p.stem for p in (ev / "agents").iterdir()] == ["cekirdek-a"]
    assert sorted(p.stem for p in (ev / "agents-katalog").iterdir()) == ["uzman-b", "uzman-c"]
    kat = (ev / "skills" / "ajan-getir" / "katalog.tsv").read_text(encoding="utf-8")
    assert "agents-katalog/uzman-b.md" in kat and "uzman-c" in kat and "cekirdek-a" in kat

    assert m.main(["--geri"], ev) == 0
    assert {p.name: p.read_bytes() for p in (ev / "agents").iterdir()} == once
    assert not (ev / "agents-katalog").exists()
    assert "agents-katalog" not in (ev / "skills" / "ajan-getir" / "katalog.tsv").read_text(encoding="utf-8")
