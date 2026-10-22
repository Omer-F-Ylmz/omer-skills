import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import ajan_cekirdek as ac  # noqa: E402
import ajan_cekirdek_bagla as b  # noqa: E402

AJAN = "---\nname: x\nmodel: {m}\n---\n\nGövde.\n"


def test_haiku_ve_sonnet_profiline_blok_eklenir_opusa_eklenmez():
    for m in ("haiku", "sonnet"):
        assert ac.onek().strip() in b.bagla(AJAN.format(m=m))
    assert b.bagla(AJAN.format(m="opus")) == AJAN.format(m="opus")


def test_ikinci_calistirma_degistirmez_kaynak_degisince_gunceller():
    bir = b.bagla(AJAN.format(m="haiku"))
    assert b.bagla(bir) == bir
    assert b.bagla(bir.replace(ac.bolum("cekirdek")[:20], "ESKI METIN XXXXXXX")).count(b.ACIL) == 1
    assert "ESKI METIN" not in b.bagla(bir.replace(ac.bolum("cekirdek")[:20], "ESKI METIN XXXXXXX"))


def test_modelsiz_profile_dokunulmaz():
    assert b.bagla("---\nname: x\n---\nGövde\n") == "---\nname: x\n---\nGövde\n"
