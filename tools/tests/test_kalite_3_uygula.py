import importlib.util
import json
from pathlib import Path

_s = importlib.util.spec_from_file_location("k3u", Path(__file__).resolve().parents[2] / "onay" / "kalite_3_uygula.py")
k3u = importlib.util.module_from_spec(_s)
_s.loader.exec_module(k3u)


def test_uygula_geri_gidis_donus(tmp_path):
    ev, kok = tmp_path / "ev", tmp_path / "kok"
    canli = ev / ".claude" / "skills" / "pdf"
    canli.mkdir(parents=True)
    (canli / "SKILL.md").write_text("---\nname: pdf\ndescription: Eski.\n---\nUZUN GÖVDE\n", encoding="utf-8")
    (ev / ".claude.json").write_text(json.dumps({"mcpServers": {"a": {}}}), encoding="utf-8")
    bol = kok / ".kalite3" / "pilot" / "pdf"
    (bol / "references").mkdir(parents=True)
    (bol / "SKILL.md").write_text("---\nname: pdf\ndescription: Eski.\n---\nÇEKİRDEK\n", encoding="utf-8")
    (bol / "references" / "r.md").write_text("ayrıntı", encoding="utf-8")
    (kok / "docs" / "kutuphane").mkdir(parents=True)
    (kok / "docs" / "kutuphane" / "kalite3-kabul.txt").write_text("pdf\nyok-boyle\n", encoding="utf-8")
    (kok / ".kalite3" / "aciklama-yeni.jsonl").write_text(json.dumps(
        {"ad": "pdf", "yeni": 'Birleştirir "pdf". Use when merging.', "gecerli": True, "denetim": "yok"}) + "\n", encoding="utf-8")
    assert k3u.uygula(ev, kok) is True
    yeni = (canli / "SKILL.md").read_text(encoding="utf-8")
    assert "ÇEKİRDEK" in yeni and 'description: "Birleştirir \\"pdf\\". Use when merging."' in yeni
    assert (canli / "references" / "r.md").exists()
    assert k3u.geri(ev) is True
    assert (canli / "SKILL.md").read_text(encoding="utf-8").endswith("UZUN GÖVDE\n") and not (canli / "references").exists()
