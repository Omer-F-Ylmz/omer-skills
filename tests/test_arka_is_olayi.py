"""KARAR-30 m11: arka_ajan.kos biten işi beyin 'is' olayına yazmalı (koçluk döngüsü koc_t buna bağlı)."""
import sys, types
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import arka_ajan


def test_is_olayi_yaz_beyine_iletir(monkeypatch):
    cagri = []
    sahte = types.SimpleNamespace(is_olayi=lambda *a: cagri.append(a))
    monkeypatch.setitem(sys.modules, "beyin_dusun", sahte)
    r = {"total_cost_usd": 0.12, "num_turns": 5, "subtype": "success", "is_error": False}
    arka_ajan.is_olayi_yaz("x-1", {"model": "sonnet"}, r, 0, 120.0)
    assert cagri and cagri[0][0] == "x-1" and cagri[0][2] == 0.12 and cagri[0][4] is True


def test_is_olayi_yaz_hata_yutar(monkeypatch):
    monkeypatch.setitem(sys.modules, "beyin_dusun", types.SimpleNamespace(is_olayi=lambda *a: 1 / 0))
    arka_ajan.is_olayi_yaz("x-2", {}, {}, 1, 1.0)
