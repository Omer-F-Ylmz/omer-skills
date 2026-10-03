"""KANAL-1b B1: KUR değerli sayılır (kaynak KUR)."""
from test_kanal_k1 import _jsonl
from video import kanal


def test_kur_degerli(tmp_path):
    repo = tmp_path / "repo"
    _jsonl(repo / "docs" / "kurulumlar" / "kayit.jsonl", [
        {"ad": "k1", "katman": "T0", "yargi": "KUR", "karar": "ONAY kural k1", "tarih": "2026-09-24", "video": "KKKKKKKKKK1"},
        {"ad": "k2", "yargi": "KUR", "karar": "kural-onay", "tarih": "2026-09-24", "video": "KKKKKKKKKK2"},
        {"ad": "k3", "yargi": "RED", "karar": "RED", "tarih": "2026-09-24", "video": "KKKKKKKKKK3"},
    ])
    deg, _ = kanal.degerli(repo)
    assert deg == {"KKKKKKKKKK1": ["KUR:k1"], "KKKKKKKKKK2": ["KUR:k2"]}
