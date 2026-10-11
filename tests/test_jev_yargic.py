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
