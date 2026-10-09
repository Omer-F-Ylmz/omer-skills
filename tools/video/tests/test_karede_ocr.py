"""KAREDE-OCR-1: kaynak=kare satırında karede_gorulen ve kanit boşsa en yakın karenin ham OCR metni (model çağrısı yok)."""
import json

from video import parti as pt


def _kur(tmp_path, ham, kanit=None, zaman="0:12"):
    v = "aaaaaaaaaa1"
    (g := tmp_path / "goz").mkdir(exist_ok=True)
    (g / "ocr.json").write_text(json.dumps({"ham": ham}), encoding="utf-8")
    satir = {"ad": "X", "kanit_zamani": zaman, "kaynak": "kare", "kanit": kanit, "karede_gorulen": None}
    return {"videolar": [{"id": v, "adaylar": [satir]}]}, {v: {"ocr": g / "ocr.json"}}, satir


def test_ocr_en_yakin_kareden_doldurur(tmp_path):
    form, pk, s = _kur(tmp_path, [[2.0, [["uzak", 0.99, 1]]], [11.5, [["Hızlı", 0.99, 1], ["Araç", 0.99, 2]]]])
    pt.ocrdan(form, pk)
    assert s["karede_gorulen"] == "(karede OCR) Hızlı Araç"


def test_ocr_doldurulan_satir_denetimden_gecer(tmp_path, monkeypatch):
    from test_gece_onarim import _kare_form
    v, form, p = _kare_form(tmp_path, monkeypatch, None)
    (tmp_path / "ocr.json").write_text(json.dumps({"ham": [[300.0, [["Hızlı Araç", 0.99, 1]]]]}), encoding="utf-8")
    form["videolar"][0]["adaylar"][0]["kanit_zamani"] = "5:00"
    pt.ocrdan(form, {v: {"ocr": tmp_path / "ocr.json"}})
    assert not [h for h in pt.dogrula(form, {v: p}, [v]).get(v, []) if "karede_gorulen" in h]


def test_ocr_bos_eksik_kalir(tmp_path):
    form, pk, s = _kur(tmp_path, [[11.5, [["silik", 0.01, 1]]]])
    pt.ocrdan(form, pk)
    assert not s["karede_gorulen"]


def test_ocr_kanitli_ya_da_zamansiz_satira_dokunmaz(tmp_path):
    form, pk, s = _kur(tmp_path, [[12.0, [["metin", 0.99, 1]]]], kanit="var")
    pt.ocrdan(form, pk)
    assert not s["karede_gorulen"]
    form, pk, s = _kur(tmp_path, [[12.0, [["metin", 0.99, 1]]]], zaman="açıklama")
    pt.ocrdan(form, pk)
    assert not s["karede_gorulen"]


def test_ocr_gizli_parametre_maskelenir_ve_kisaltilir(tmp_path):
    form, pk, s = _kur(tmp_path, [[12.0, [["https://x.io/?api_key=SIR3T&a=1", 0.99, 1], ["z" * 400, 0.99, 2]]]])
    pt.ocrdan(form, pk)
    assert "SIR3T" not in s["karede_gorulen"] and "api_key=[gizlendi]" in s["karede_gorulen"]
    assert len(s["karede_gorulen"]) <= len("(karede OCR) ") + 200
