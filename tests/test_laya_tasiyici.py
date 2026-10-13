import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools" / "olcum"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools" / "jev"))
import jev_yargic  # noqa: E402
import laya_tasiyici  # noqa: E402
from jev.cekirdek import JevHata  # noqa: E402


def _sahte(monkeypatch, rc=0, cevap=None):
    cagri = []

    def run(arg, input=None, **kw):
        g = json.loads(input)
        cagri.append(g)
        c = cevap or [{"kalite": {"score": 3.5, "confidence": 0.8}} for _ in g["states"]]
        return subprocess.CompletedProcess(arg, rc, json.dumps({"cevap": c, "girdi_jeton": 7, "sn": 0.1}).encode(), b"hata")
    monkeypatch.setattr(laya_tasiyici.subprocess, "run", run)
    return cagri


def test_jev_sozlesmesi_ve_onbellek(monkeypatch, tmp_path):
    cagri = _sahte(monkeypatch)
    t = laya_tasiyici.LayaTasiyici(model="multilingual")
    s = [{"yanit": "a"}, {"yanit": "b"}]
    c = jev_yargic.yargila(s, jev_yargic.SORU, t, tmp_path / "ob.json")
    assert [x["kalite"]["score"] for x in c] == [3.5, 3.5]
    assert t.kullanim == [{"cost": 0.0, "input_tokens": 7, "istek": 2, "sn": 0.1}]
    jev_yargic.yargila(s, jev_yargic.SORU, t, tmp_path / "ob.json")  # önbellekten: ikinci çağrı yok
    assert len(cagri) == 1 and cagri[0]["model"] == "multilingual"


def test_hata_jevhata(monkeypatch):
    _sahte(monkeypatch, rc=1)
    with pytest.raises(JevHata):
        laya_tasiyici.LayaTasiyici().yargila([{"yanit": "a"}], jev_yargic.SORU)
