"""VİDEO-13: ASR ad onarımı (VIDEO_ASR_ONAR) · C3 model karesi küçültme (VIDEO_JETON 'K')."""
from PIL import Image

from video import goz as gz, parti as pt

SZ = [("Claude Code", ["claude-code"]), ("Ollama", [])]


def test_asr_onar_bozuk_adi_kanonige_cevirir():
    assert gz.asr_onar("then open cloud code and run it", SZ) == "then open Claude Code and run it"


def test_asr_onar_dogru_ve_ilgisiz_metne_dokunmaz():
    for x in ("open Claude Code now", "the weather is nice", ""):
        assert gz.asr_onar(x, SZ) == x


def test_kare_kucult_uzun_kenari_sinirlar(tmp_path):
    k = tmp_path / "a.jpg"
    Image.new("RGB", (768, 432), "white").save(k)
    y = pt.kare_kucult([k], tmp_path / "k", 512)
    with Image.open(y[0]) as im:
        assert max(im.size) == 512
    assert y[0] != k and k.is_file()  # kaynak kare değişmez (önbellek)
