import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools" / "olcum"))
import jev_yargic  # noqa: E402


class Sahte:
    def yargila(self, states, questions):
        assert set(questions) == {"kalite"} and questions["kalite"]["type"] == "score"
        return [{"kalite": {"score": 2.5, "confidence": 0.7}} for _ in states]


def test_veri_ve_puan(tmp_path):
    d = tmp_path / "2026-10-11-x"
    d.mkdir()
    (d / "G01-1.md").write_text("await _db.Orders.FirstOrDefaultAsync .Result deadlock", encoding="utf-8")
    (d / "notlar.md").write_text("görev değil", encoding="utf-8")
    k = jev_yargic.jev_puanla(jev_yargic.veri([d]), Sahte())
    assert [x["dosya"] for x in k] == ["2026-10-11-x/G01-1.md"]
    assert k[0]["regex"] == 8 and k[0]["jev"] == 5.0 and k[0]["guven"] == 0.7
    assert k[0]["state"]["gorev"] and k[0]["state"]["kabul"]


def test_tsv_doldur_eski_baslik_sutun_eklenir(tmp_path):
    t = tmp_path / "2026-10-11-x.tsv"
    t.write_text("gorev\ttekrar\tkalite\thata\nG01\t1\t8\t\nG02\t1\t10\t\n", encoding="utf-8")
    jev_yargic.tsv_doldur(t, [{"gorev": "G01", "tekrar": "1", "jev": 6.0, "guven": 0.9}, {"gorev": "G02", "tekrar": "1"}])
    L = t.read_text(encoding="utf-8").splitlines()
    assert L == ["gorev\ttekrar\tkalite\thata\tjev\tjev_guven", "G01\t1\t8\t\t6.0\t0.9", "G02\t1\t10\t\t\t"]
    jev_yargic.tsv_doldur(t, [{"gorev": "G02", "tekrar": "1", "jev": 9.0, "guven": 0.8}])  # ikinci kez: sütun yinelenmez
    assert t.read_text(encoding="utf-8").splitlines()[1:] == ["G01\t1\t8\t\t6.0\t0.9", "G02\t1\t10\t\t9.0\t0.8"]
