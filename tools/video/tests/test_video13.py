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


def test_k_varsayilan_jeton_0_eski_yol(tmp_path, monkeypatch):  # VİDEO-13-devam-2: K KABUL → VIDEO_JETON verilmezse 512 kenar; "0" eski yol (768)
    from test_m2a import _form
    v = "aaaaaaaaaa1"
    Image.new("RGB", (768, 432), "white").save(k := tmp_path / "a.jpg")
    monkeypatch.setattr(pt.hafif, "GORSEL", True)
    monkeypatch.delenv("VIDEO_JETON", raising=False)
    gor = {}

    def cagir(sistem, metin, sema, **kw):
        with Image.open(kw["kareler"][0]) as im:
            gor[jt] = max(im.size)
        return {"form": {"videolar": [_form(v)]}, "usage": {}, "usd": 0.0, "sure": 0.1, "hata": None, "model": kw["model"]}
    for jt, env in (("yok", {}), ("0", {"VIDEO_JETON": "0"})):
        d = {"butce": .5, "tavan": {"usd": 5.0}, "videolar": {v: {"tarama": {}}}}
        pt._tara_ikili([v], {v: {"kareler": [str(k)], "sure": 300, "metin": "x"}}, {}, lambda s: s, d, tmp_path, env, cagir, ["claude-sonnet-5-5"])
    assert gor == {"yok": 512, "0": 768}


def test_ocr_buyuk_harf_slash_komutu_katlanir():  # VİDEO-13-devam: "/USAGE" ve "/"yu I okuyan "IUSAGE" → /usage; sıradan büyük harf dokunulmaz
    s = gz.ocr_satirlar([("/USAGE - BU CLAUDE CODE", 0.9, 1), ("IUSAGE - BU CLAUDE CODE SOHBETI", 0.9, 2), ("IMPORTANT NOTE", 0.9, 3), ("/compact", 0.9, 4)])
    assert s == ["/usage - BU CLAUDE CODE", "/usage - BU CLAUDE CODE SOHBETI", "IMPORTANT NOTE", "/compact"]


def test_c3a_yazi_karesi_goruntu_yerine_eksik_ocr_metni(tmp_path):  # VİDEO-13-devam-2 C3a 'O': yazı ağırlıklı kare atılır, istemde olmayan OCR satırı eklenir
    import json
    oj = tmp_path / "ocr.json"
    yazi = [[f"satir {i}", .95, i] for i in range(pt.OCR_KARE_SATIR)]
    oj.write_text(json.dumps({"ham": [[1.0, yazi], [2.0, [["logo", .99, 1]]], [3.0, [[f"x{i}", .5, i] for i in range(30)]]]}), encoding="utf-8")
    kr = [str(tmp_path / f"k0000{i}0.jpg") for i in (1, 2, 3)]
    tut, ek = pt.kare_ocr(kr, oj, "satir 0 ve satir 1 zaten istemde")
    assert tut == kr[1:]  # az satırlı (görsel) ve düşük güvenli kare kalır
    assert "k000010.jpg" in ek and "satir 2" in ek and "satir 0 " not in ek and "satir 1 " not in ek
    assert pt.kare_ocr(kr, tmp_path / "yok.json", "") == (kr, "")
