import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import wer_loo as w  # noqa: E402


def test_joker_ayrisan_blok_cezasiz():
    og = w.uzlasi("a b c d".split(), "a x c d".split())
    assert og == ["a", None, "c", "d"]
    assert w.hata(og, "a QQ ZZ c d".split()) == 0  # joker çok kelime yutar
    assert w.hata(og, "a b c".split()) == 1  # uzlaşılan 'd' eksik
    assert w.hata(og, "a b e d".split()) == 1  # 'c' yerine 'e'
