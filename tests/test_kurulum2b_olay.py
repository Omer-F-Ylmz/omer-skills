"""kurulum2b.beyin() beyin-olay.jsonl'e ortak biçimde yazar (t epoch sayısı, ozet/tur/hata anahtarları)."""
import importlib.util
import json
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]


def test_beyin_ortak_bicim(tmp_path, monkeypatch):
    spec = importlib.util.spec_from_file_location("kurulum2b", KOK / "tools/kurulum2b.py")
    k = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(k)
    monkeypatch.setattr(k, "KOK", tmp_path)
    (tmp_path / ".kos/kopru").mkdir(parents=True)
    k.beyin("deneme")
    o = json.loads((tmp_path / ".kos/kopru/beyin-olay.jsonl").read_text(encoding="utf-8"))
    assert isinstance(o["t"], float) and o["ozet"] == "deneme" and o["tur"] == "ilerleme" and o["hata"] is False
