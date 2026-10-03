"""KANAL-2b C1: kuyruk notunda "takip: hayır" olan videonun kanalı otomatik takibe eklenmez; listedeki kanalın değeri değişmez."""
import json

from test_kanal_a3 import A, N, _kur
from video import kanal

KUYRUK = f"| {N} | 12 | x | takip: hayır | bekliyor |\n| {A} | 12 | x | takip: hayır | bekliyor |\n"


def test_takip_hayir_eklemez(tmp_path):
    repo, ctx = _kur(tmp_path)
    assert kanal.takip_ekle(repo, [A, N], ctx, KUYRUK) == []
    j = json.loads((repo / "docs" / "video-tarama" / "kanallar.json").read_text(encoding="utf-8"))
    assert "UCn" not in j
    assert j["UCa"]["karar"] == "bir-kez"  # listedeki değer korunur
