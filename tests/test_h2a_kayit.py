"""TOKEN-H2a: feed yoklayıcı — tekilleştirme + boşluk dalı (sahte feed, çevrimdışı)."""
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "tools"))
import h2a_kayit as k  # noqa: E402


def _t(i):
    return {"request_id": f"r{i}", "timestamp": f"t{i}", "model": "m",
            "request_messages": [{"role": "user", "content": f"c{i}"}],
            "compressed_messages": [{"role": "user", "content": f"c{i}"}]}


def _kos(feedler, gorulen):
    cagri, yazilan = [], []
    def cek(limit):
        cagri.append(limit)
        return feedler[limit]
    k.yokla(cek, gorulen, yazilan.append)
    return cagri, yazilan


def test_ortusme_varsa_tekillestirir():
    cagri, yazilan = _kos({10: [_t(1), _t(2)]}, {"r1"})
    assert cagri == [10]
    assert [s["request_id"] for s in yazilan] == ["r2"]
    assert yazilan[0]["request_messages"] == [["user", k.sha8("c2")]]


def test_ortusme_yok_100_ile_kapanir():
    cagri, yazilan = _kos({10: [_t(5)], 100: [_t(1), _t(5)]}, {"r1"})
    assert cagri == [10, 100]
    assert [s.get("request_id") for s in yazilan] == ["r5"]


def test_100_de_ortusmezse_bosluk_yazilir():
    cagri, yazilan = _kos({10: [_t(5)], 100: [_t(4), _t(5)]}, {"r1"})
    assert cagri == [10, 100]
    assert "bosluk" in yazilan[0]
    assert [s.get("request_id") for s in yazilan[1:]] == ["r4", "r5"]


def test_ilk_yoklamada_bosluk_yok():
    cagri, yazilan = _kos({10: [_t(1)]}, set())
    assert cagri == [10]
    assert [s["request_id"] for s in yazilan] == ["r1"]
