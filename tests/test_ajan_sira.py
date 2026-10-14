"""TOKEN-3 K11: ajan-sira.tsv isteğe bağlı 4. sütun efor=medium|high → --effort; yoksa eski davranış."""
import importlib.util
from pathlib import Path

import pytest

_s = importlib.util.spec_from_file_location("ajan_sira", Path(__file__).resolve().parents[1] / ".kos/kopru/ajan_sira.py")
ajan_sira = importlib.util.module_from_spec(_s)
_s.loader.exec_module(ajan_sira)


def test_dorduncu_sutun_efor(tmp_path, monkeypatch):
    tsv = tmp_path / "k.tsv"
    tsv.write_text("# yorum\na\ti.md\nb\ti.md\t\tefor=medium\nc\ti.md\tx::y\tefor=high\n", encoding="utf-8")
    monkeypatch.setattr(ajan_sira, "KUYRUK", tsv)
    assert ajan_sira.kuyruk() == [("a", "i.md", "", ""), ("b", "i.md", "", "medium"), ("c", "i.md", "x::y", "high")]


def test_gecersiz_efor_reddedilir(tmp_path, monkeypatch):
    tsv = tmp_path / "k.tsv"
    tsv.write_text("a\ti.md\t\tefor=max\n", encoding="utf-8")
    monkeypatch.setattr(ajan_sira, "KUYRUK", tsv)
    with pytest.raises(ValueError):
        ajan_sira.kuyruk()


def test_baslat_argv_env(monkeypatch):
    monkeypatch.setenv("CLAUDE_CODE_EFFORT_LEVEL", "high")
    argv, env = ajan_sira.baslat_argv("medium")
    assert argv[-2:] == ["--effort", "medium"] and "CLAUDE_CODE_EFFORT_LEVEL" not in env
    argv, env = ajan_sira.baslat_argv("")
    assert argv == ajan_sira.ARGV and env is None
