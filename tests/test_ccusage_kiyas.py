"""KURULUM-V1 d2: tools/ccusage_kiyas.py — ccusage daily --json toplamı ile token_olc çıktısı alan alan kıyas."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import ccusage_kiyas as k  # noqa: E402

CCU = {"inputTokens": 100, "outputTokens": 50, "cacheReadTokens": 1000, "cacheCreationTokens": 40, "totalCost": 10.0}
OLC = {"girdi": 100, "cikti": 45, "cache_okuma": 1000, "cache_5m": 30, "cache_1h": 10, "usd": 11.0}


def test_alan_esleme_ve_fark():
    s = {r[0]: r for r in k.kiyasla(CCU, OLC)}
    assert s["girdi"][1:] == (100, 100, 0.0)
    assert s["cache_yazma"][2] == 40  # 5m + 1h birleşir
    assert s["cikti"][3] == -10.0
    assert s["usd"][3] == 10.0


def test_sifir_bolen_cokmez():
    s = {r[0]: r for r in k.kiyasla({**CCU, "outputTokens": 0}, OLC)}
    assert s["cikti"][3] is None
