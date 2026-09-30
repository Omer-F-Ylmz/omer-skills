"""MOTOR-M8 K5: short tek segmentte 1 kare değil ≤3 kare, süreye yayılmış."""
import json

from test_m8_k2 import _meta, _paket, _sahte_kare


def test_short_tek_segment_uc_kare(tmp_path, monkeypatch):
    _sahte_kare(monkeypatch)
    d = _meta(tmp_path, "eKnpRVgqXR8", 65)
    (d / "segmentler.jsonl").write_text(json.dumps({"bas": 0, "son": 65, "metin": "bu araç ile landing sayfası kurulur ve yayınlanır"}), encoding="utf-8")
    p = _paket(tmp_path, "eKnpRVgqXR8")
    assert not p["kare_yalniz"] and len(p["kareler"]) == 3
    assert p["kare_zaman"] == sorted(set(p["kare_zaman"])) and p["kare_zaman"][0] < 20 < 45 < p["kare_zaman"][-1]
