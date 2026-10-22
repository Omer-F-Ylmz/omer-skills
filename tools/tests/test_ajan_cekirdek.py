import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kos/kopru"))
import ajan_cekirdek as ac  # noqa: E402
import ajan_sira  # noqa: E402


def test_model_gerek_opus_haric_hepsi():
    assert [ac.model_gerek(m) for m in ("haiku", "sonnet", None, "opus")] == [True, True, True, False]


def test_kuyruk_oneki_opusa_eklenmez_haiku_sonnete_eklenir():
    assert ajan_sira.cekirdek_onek("opus") == ""
    for m in ("haiku", "sonnet"):
        assert ajan_sira.cekirdek_onek(m) == ac.onek()


def test_cekirdek_prompt_onekinde_ilk_siradadir():
    assert ajan_sira.on_ek_kur("sonnet", "ARAC-ONEKGOVDE") == ac.onek() + "ARAC-ONEKGOVDE"
    assert ajan_sira.on_ek_kur("opus", "ARAC-ONEKGOVDE") == "ARAC-ONEKGOVDE"
