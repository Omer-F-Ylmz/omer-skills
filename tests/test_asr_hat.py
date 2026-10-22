import sys
import urllib.error
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import asr_hat as h  # noqa: E402


def hata429(_):
    raise urllib.error.HTTPError("u", 429, "kota", {}, None)


def test_kota_hatasinda_siradaki_kaynak():
    cagri = []
    kaynaklar = [("groq", hata429), ("gemini", lambda w: cagri.append("g") or "iki"), ("yerel", lambda w: "yerel")]
    assert h.donustur("a.wav", kaynaklar) == ("iki", "gemini")
    assert cagri == ["g"]


def test_hepsi_dusunce_yerel_yedek():
    kaynaklar = [("groq", hata429), ("gemini", hata429), ("yerel", lambda w: "yerel")]
    assert h.donustur("a.wav", kaynaklar) == ("yerel", "yerel")
