"""VİDEO-GÖZ-1b-1S: son rötuş — yeni bilgi süzgeci · gürültü sözlük/TERIM · yorum kırpma · DML yoksa künye · URL işe yarar/değersiz."""
from video import cli
from video import goz as g


def test_s1_yeni_cift_getiren_satir_tutulur():
    metin = [(10, ["Claude Code"]), (20, ["memory bank"]), (30, ["Claude memory"])]
    assert (30, "Claude memory") in g.ekran_metni(metin, "")


def test_s1_tamamen_tekrar_satir_atilir():
    metin = [(10, ["Claude Code memory"]), (20, ["Code memory"]), (30, ["claude code"])]
    assert g.ekran_metni(metin, "bugün Claude Code ile çalışıyoruz") == [(10, "Claude Code memory")]


def test_s2_kisaltma_cikarilir_sozluk_adi_korunur():
    assert not cli._ocr_gurultu("Principled BSDF")  # d_UE 0:32: anlamsiz_oran BSDF'yi sayıyordu
    assert cli._ocr_gurultu("BSDF") and cli._ocr_gurultu("XQZT VBNM")  # kalan boş → eski kural
    assert cli._ocr_gurultu("GSAP") and not cli._ocr_gurultu("GSAP", ["GSAP"])


def test_s3b_butceyi_asan_sabit_yorum_kirpilir_oncelikli_satirlar_kalir():
    dolgu = [f"this is just a long filler sentence about nothing number {i} ok" for i in range(80)]
    ham = [{"text": "\n".join([*dolgu, "Fix only the exit with cut-and-extend", "see https://x.dev/y"]), "pinned": True, "sahip": True}]
    tk = lambda s: len(s) // 4 + 1  # noqa: E731
    assert 1200 <= tk(" / ".join(ham[0]["text"].splitlines())) < 1500
    out = g.yorum_sec(ham, butce=1000)
    assert len(out) == 1 and out[0].startswith("[sabit] ") and tk(out[0]) <= 1000
    assert "cut-and-extend" in out[0] and "https://x.dev/y" in out[0] and dolgu[0] in out[0] and dolgu[-1] not in out[0]
    assert "number 79" in g.yorum_sec(ham)[0]  # varsayılan bütçe 1500: tam yorum


def test_s3_diger_yorumda_tireli_terim_satiri_tutulur():
    ham = [{"text": "great video\nI use cut-and-extend daily", "pinned": False, "sahip": False}]
    assert g.yorum_sec(ham) == ["I use cut-and-extend daily"]


def test_s5_dml_saglayici_yoksa_cpu_ve_kunye(tmp_path, monkeypatch):
    import sys
    import types
    for f in g.MODEL_DOSYA.values():
        (tmp_path / f).write_text("x")
    monkeypatch.setenv("VIDEO_OCR_MODEL", str(tmp_path))
    al = {}
    ro = types.SimpleNamespace(RapidOCR=lambda params: al.update(params) or (lambda y: None),
                               **{k: types.SimpleNamespace(PPOCRV5=1, PPOCRV4=1, CH=1, LATIN=1, MOBILE=1)
                                  for k in ("LangCls", "LangDet", "LangRec", "ModelType", "OCRVersion")})
    monkeypatch.setitem(sys.modules, "rapidocr", ro)
    monkeypatch.setitem(sys.modules, "onnxruntime", types.SimpleNamespace(get_available_providers=lambda: ["CPUExecutionProvider"]))
    oku = g.rapid_yukle("dml")
    assert oku.cihaz == "cpu (dml yok)" and al["EngineConfig.onnxruntime.use_dml"] is False
