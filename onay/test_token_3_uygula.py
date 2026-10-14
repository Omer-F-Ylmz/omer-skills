import token_3_uygula as t


def test_uygula_geri(tmp_path):
    c = tmp_path / ".claude"
    (c / "plugins/marketplaces/omer-skills/tools").mkdir(parents=True)
    (c / "plugins/marketplaces/omer-skills/tools/cagri_sayac.py").write_text("eski", encoding="utf-8")
    (c / "CLAUDE.md").write_bytes(b"- Tests " + t.ESKI.encode() + b", only\r\n")
    assert t.main(["--kuru"], tmp_path) == 0
    assert t.main(["uygula"], tmp_path) == 0
    assert (c / "skills/is-akisi/SKILL.md").exists()
    assert (c / "CLAUDE.md").read_bytes() == b"- Tests " + t.YENI.encode() + b", only\r\n"
    assert (c / "plugins/marketplaces/omer-skills/tools/cagri_sayac.py").read_text(encoding="utf-8") != "eski"
    assert t.main(["--geri"], tmp_path) == 0
    assert t.ESKI.encode() in (c / "CLAUDE.md").read_bytes()
    assert (c / "plugins/marketplaces/omer-skills/tools/cagri_sayac.py").read_text(encoding="utf-8") == "eski"
    assert not (c / "skills/is-akisi").exists()
