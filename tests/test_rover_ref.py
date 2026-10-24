import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import rover_ref as r  # noqa: E402


def test_cogunluk_ve_belirsiz():
    t = {"groq": "bu cloud kod iyi".split(), "gemini": "bu claude kod iyi".split(), "yerel": "bu claude kod iyi".split()}
    metin, bel = r.rover("k", t)
    assert metin == "bu claude kod iyi".split() and bel == []
    t = {"groq": "bu a kod".split(), "gemini": "bu b kod".split(), "yerel": "bu c kod".split()}
    metin, bel = r.rover("k", t)
    assert metin == "bu b kod".split() and len(bel) == 1  # üçlü ayrışma: gemini konur, belirsiz sayılır


def test_klip_kenari_ekleme():
    t = {"groq": "ğ ile kod".split(), "gemini": "değerli ile kod".split(), "yerel": "değerli ile kod".split()}
    assert r.rover("k", t)[0] == "değerli ile kod".split()
