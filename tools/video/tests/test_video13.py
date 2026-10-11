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


def test_ocr_buyuk_harf_slash_komutu_katlanir():  # VİDEO-13-devam: "/USAGE" ve "/"yu I okuyan "IUSAGE" → /usage; sıradan büyük harf dokunulmaz
    s = gz.ocr_satirlar([("/USAGE - BU CLAUDE CODE", 0.9, 1), ("IUSAGE - BU CLAUDE CODE SOHBETI", 0.9, 2), ("IMPORTANT NOTE", 0.9, 3), ("/compact", 0.9, 4)])
    assert s == ["/usage - BU CLAUDE CODE", "/usage - BU CLAUDE CODE SOHBETI", "IMPORTANT NOTE", "/compact"]
