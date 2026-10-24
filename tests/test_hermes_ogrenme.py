"""HERMES-KUR-1 P6: Hermes'in ürettiği skill → gitleaks kapısı; bundled olanlar aday sayılmaz."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import hermes_ogrenme


def test_aday_kapisi(tmp_path, monkeypatch):
    gercek = hermes_ogrenme.subprocess.run
    monkeypatch.setattr(hermes_ogrenme.subprocess, "run", lambda a, **k: None if "beyin_kayit.py" in " ".join(a) else gercek(a, **k))  # gerçek beyin-olay.jsonl kirlenmesin
    home, hedef = tmp_path / "h", tmp_path / "aday"
    s = home / "skills"
    (s / "apple/apple-notes").mkdir(parents=True)
    (s / "apple/apple-notes/SKILL.md").write_text("bundled", encoding="utf-8")
    (s / ".bundled_manifest").write_text("apple-notes:abc\n", encoding="utf-8")
    (s / "benim-temiz").mkdir()
    (s / "benim-temiz/SKILL.md").write_text("---\nname: benim-temiz\n---\nmerhaba", encoding="utf-8")
    (s / "benim-sizinti").mkdir()
    (s / "benim-sizinti/SKILL.md").write_text("token = ghp_" + "aB3dE5gH7jK9mN1pQ3sT5vW7yZ9bD1fH3jL5", encoding="utf-8")
    sonuc = hermes_ogrenme.main(home, hedef)
    assert sonuc == {"aday": ["benim-temiz"], "kirmizi": ["benim-sizinti"]}
    assert (hedef / "benim-temiz/SKILL.md").exists() and not (hedef / "benim-sizinti").exists()
