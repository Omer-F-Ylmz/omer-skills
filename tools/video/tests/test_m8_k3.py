"""MOTOR-M8 K3: ortadaki videonun istisnası (argparse SystemExit dahil) partiyi durdurmaz; hatalılar özetin sonunda."""
import pytest

from video import parti as pt
from test_m2a import Sahte, _ctx, _durum, _kurulum, _ns
from test_m8_k1 import Alt

V3 = ["aaaaaaaaaa1", "bbbbbbbbbb2", "cccccccccc3"]


@pytest.mark.parametrize("hata", [SystemExit(2), RuntimeError("patladı")])
def test_ortadaki_video_istisna_parti_devam(tmp_path, capsys, hata):
    _kurulum(tmp_path, V3)
    a = Alt(tmp_path, patla=V3[1], hata=hata)
    a.sakla(V3)
    assert pt.parti(_ns("baslat", tmp_path / "kuyruk.md"), {**_ctx(tmp_path, Sahte()), "alt": a}) == 0
    d = _durum(tmp_path)["videolar"]
    assert [d[v]["paket"]["durum"] for v in V3] == ["tamam", "hata", "tamam"] and d[V3[1]]["paket"]["hata"]
    son = capsys.readouterr().out.rsplit("hatalı videolar:", 1)
    assert len(son) == 2 and V3[1] in son[1] and V3[0] not in son[1]
