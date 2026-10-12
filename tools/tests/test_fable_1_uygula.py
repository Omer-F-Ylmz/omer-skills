import importlib.util
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("fable_1_uygula", KOK / "onay" / "fable_1_uygula.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)


def test_kuru_uygula_geri(tmp_path):
    ag = tmp_path / ".claude" / "agents"; ag.mkdir(parents=True)
    (ag / "a.md").write_bytes(b"---\r\nname: a\r\n---\r\ngovde\r\n")
    (ag / "b.md").write_text("---\nname: b\nskills: x\n---\n", encoding="utf-8")
    assert m.main(["--kuru"], ev=tmp_path) == 0
    assert not (tmp_path / ".claude" / "skills").exists()  # kuru yazmaz
    assert m.main(["uygula"], ev=tmp_path) == 0
    assert (ag / "a.md").read_bytes() == b"---\r\nskills: calisma-protokolu\r\nname: a\r\n---\r\ngovde\r\n"
    assert (ag / "b.md").read_text(encoding="utf-8") == "---\nname: b\nskills: x\n---\n"  # skills: varsa dokunulmaz
    assert (tmp_path / ".claude" / "skills" / "calisma-protokolu" / "SKILL.md").exists()
    assert m.main(["--geri"], ev=tmp_path) == 0
    assert (ag / "a.md").read_bytes() == b"---\r\nname: a\r\n---\r\ngovde\r\n"
    assert not (tmp_path / ".claude" / "skills" / "calisma-protokolu").exists()
