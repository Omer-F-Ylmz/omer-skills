"""KAREDE-OCR-2: `video parti rapor-yenile` — kapanmış partinin tamam_eksik raporu, sonradan bulunan OCR ile çağrısız yeniden üretilir."""
import json

from video import cli, parti as pt


def _kur(tmp_path, monkeypatch, durum="kapandi"):
    from test_gece_onarim import _kare_form
    v, form, p = _kare_form(tmp_path, monkeypatch, "")
    form["videolar"][0]["adaylar"][0]["kanit_zamani"] = "5:00"
    p["ocr"] = tmp_path / "goz" / "ocr.json"
    (pdir := tmp_path / ".kos" / "P1").joinpath("form").mkdir(parents=True)
    (pdir / "form" / f"{v}.json").write_text(json.dumps(form["videolar"][0], ensure_ascii=False), encoding="utf-8")
    tdir = tmp_path / "tarama"
    _dn = pt._denet  # kanit-boş şema hatası bu testin konusu değil; karede_gorulen kuralı kalır
    monkeypatch.setattr(pt, "_denet", lambda x, s, yol: [h for h in _dn(x, s, yol) if ".kanit:" not in h])
    d = {"parti": "P1", "tarih": "2026-10-09", "model": "m", "durum": durum, "kayit": (tmp_path / "kayit.jsonl").as_posix(),
         "videolar": {v: {"paket": {"durum": "tamam"}, "tarama": {"durum": "bekliyor"}}}}
    assert pt._kismi_kabul(pdir, d, v, p, tdir)  # OCR yok → tamam_eksik raporu (gerçek yol)
    assert d["videolar"][v]["tarama"]["durum"] == "tamam_eksik"
    pt._yaz(pdir / "durum.json", d)
    (tmp_path / v).mkdir(); (tmp_path / v / "paket.md").write_text("x", encoding="utf-8")
    monkeypatch.setattr(pt, "paket_oku", lambda yol: p)
    return v, p, pdir, d


def _ocr(p, ham=None):
    p["ocr"].parent.mkdir(exist_ok=True)
    p["ocr"].write_text(json.dumps({"ham": ham or [[300.0, [["Hızlı Araç", 0.99, 1]]]]}), encoding="utf-8")


def test_komut_tanimli(tmp_path):
    assert cli.main(["parti", "rapor-yenile", "yok", "--kuru"], env={"VIDEO_UYGULA_KOK": str(tmp_path)}) == 1  # argparse çıkışı yok → "parti yok"


def test_ocr_varsa_rapor_ezilir_tamama_doner_kayit_cift_satir_yok(tmp_path, monkeypatch):
    v, p, pdir, d = _kur(tmp_path, monkeypatch)
    kayit = tmp_path / "kayit.jsonl"
    onceki = kayit.read_bytes()
    r = tmp_path / "tarama" / f"2026-10-09-{v}.md"
    _ocr(p)
    s = pt.rapor_yenile(tmp_path, tmp_path, ["P1"], kuru=False)
    assert s["tamam"] == 1 and "(karede OCR) Hızlı Araç" in r.read_text(encoding="utf-8")
    assert json.loads((pdir / "durum.json").read_text(encoding="utf-8"))["videolar"][v]["tarama"]["durum"] == "tamam"
    assert kayit.read_bytes() == onceki and len(list((tmp_path / "tarama").glob("*.md"))) == 1


def test_ocr_yoksa_rapor_bayt_ayni(tmp_path, monkeypatch):
    v, p, pdir, d = _kur(tmp_path, monkeypatch)
    r = tmp_path / "tarama" / f"2026-10-09-{v}.md"
    once, durum = r.read_bytes(), (pdir / "durum.json").read_bytes()
    assert pt.rapor_yenile(tmp_path, tmp_path, ["P1"], kuru=False)["tamam"] == 0
    _ocr(p, [[300.0, [["silik", 0.01, 1]]]])
    assert pt.rapor_yenile(tmp_path, tmp_path, ["P1"], kuru=False)["tamam"] == 0
    assert r.read_bytes() == once and (pdir / "durum.json").read_bytes() == durum


def test_kuru_yazmaz_sayar(tmp_path, monkeypatch):
    v, p, pdir, d = _kur(tmp_path, monkeypatch)
    r = tmp_path / "tarama" / f"2026-10-09-{v}.md"
    once = r.read_bytes()
    _ocr(p)
    s = pt.rapor_yenile(tmp_path, tmp_path, ["P1"], kuru=True); assert s["tamam"] == 1, dict(s)
    assert r.read_bytes() == once


def test_calisan_parti_dokunulmaz_ikinci_goz_kuyrugu_korunur(tmp_path, monkeypatch):
    v, p, pdir, d = _kur(tmp_path, monkeypatch, durum="calisiyor")
    _ocr(p)
    r = tmp_path / "tarama" / f"2026-10-09-{v}.md"
    once = r.read_bytes()
    assert pt.rapor_yenile(tmp_path, tmp_path, ["P1"], kuru=False)["acik"] == 1 and r.read_bytes() == once
    d["durum"] = "kapandi"
    r.write_bytes(once + "ikinci göz: luna · eklenen 1\n".encode("utf-8"))
    pt._yaz(pdir / "durum.json", d)
    pt.rapor_yenile(tmp_path, tmp_path, ["P1"], kuru=False)
    assert r.read_text(encoding="utf-8").endswith("ikinci göz: luna · eklenen 1\n") and "(karede OCR)" in r.read_text(encoding="utf-8")
