"""TOKEN-2 K8: tools/ucuz_alt.py — Claude-dışı combo, bağlam birleştirme, anahtar sızmaz, kesik yanıt ≠ 0."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import ucuz_alt  # noqa: E402


def test_govde_combo_ve_dosyalar(tmp_path):
    d = tmp_path / "a.txt"
    d.write_text("MIT License", encoding="utf-8")
    g = ucuz_alt.govde("lisans?", [d])
    assert g["model"] == "cc-yedek-dis" and "claude" not in g["model"]
    assert g["reasoning_effort"] != "none"  # combo modelleri düşünmesiz 400 döner (TOKEN-2 d3)
    assert "MIT License" in g["messages"][0]["content"] and g["messages"][0]["content"].startswith("lisans?")
    with pytest.raises(ValueError):
        ucuz_alt.govde("x" * (ucuz_alt.TAVAN + 1), [])


@pytest.mark.parametrize("bitis,kod", [("stop", 0), ("length", 2)])
def test_main_yazar_anahtar_basmaz(tmp_path, monkeypatch, capsys, bitis, kod):
    monkeypatch.setenv("OMNIROUTE_KEY", "GIZLI-ANAHTAR")
    yakala = {}
    monkeypatch.setattr(ucuz_alt, "iste", lambda g: yakala.setdefault("g", g) and {
        "model": "gemini-x", "choices": [{"message": {"content": "yanıt"}, "finish_reason": bitis}], "usage": {"prompt_tokens": 5}})
    (tmp_path / "i.md").write_text("soru", encoding="utf-8")
    assert ucuz_alt.main([str(tmp_path / "i.md"), str(tmp_path / "c.md")]) == kod
    assert (tmp_path / "c.md").read_text(encoding="utf-8") == "yanıt"
    assert "GIZLI-ANAHTAR" not in capsys.readouterr().out
