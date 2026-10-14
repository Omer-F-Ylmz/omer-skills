import io
import json
import urllib.error
from datetime import datetime, timezone

import pytest

from video import kisa, kota

GUNLUK = json.dumps({"error": {"code": 429, "details": [
    {"@type": "type.googleapis.com/google.rpc.QuotaFailure", "violations": [
        {"quotaId": "GenerateRequestsPerDayPerProjectPerModel-FreeTier", "quotaValue": "250"}]},
    {"@type": "type.googleapis.com/google.rpc.RetryInfo", "retryDelay": "13940s"}]}})
DAKIKA = GUNLUK.replace("PerDay", "PerMinute")
PT = kota.pt_tarih  # fixture yamasından önceki özgün işlev


@pytest.fixture(autouse=True)
def dizin(tmp_path, monkeypatch):
    monkeypatch.setattr(kota, "DIZIN", tmp_path)
    monkeypatch.setattr(kota, "pt_tarih", lambda simdi=None: "2026-10-15")
    return tmp_path


def test_pt_tarih():
    u = lambda *a: datetime(*a, tzinfo=timezone.utc)
    assert PT(u(2026, 10, 15, 6, 59)) == "2026-10-14"  # 23:59 PDT
    assert PT(u(2026, 10, 15, 7, 0)) == "2026-10-15"   # 10:00 TR = PT gece yarısı
    assert PT(u(2026, 12, 1, 7, 59)) == "2026-11-30"   # PST: UTC-8
    assert PT(u(2026, 3, 8, 9, 59)) == "2026-03-08"    # 2. pazar öncesi PST


def test_cozumle():
    assert kota.cozumle(GUNLUK) == {"gunluk": True, "kota": "GenerateRequestsPerDayPerProjectPerModel-FreeTier", "limit": 250, "bekle": 13940}
    assert kota.cozumle(DAKIKA)["gunluk"] is False
    assert kota.cozumle(b"<html>")["gunluk"] is False


def test_sayan_ve_defter():
    f = kota.sayan(lambda: ({"a": 1}, {"model": "m1"}))
    f(); f()
    assert kota.oku()["istek"] == {"m1": 2}


def _hata429(govde):
    def iste(*a, **k):
        raise urllib.error.HTTPError("u", 429, "q", {}, io.BytesIO(govde.encode()))
    return iste


def test_yokla():
    assert kota.yokla("k", "m", iste=_hata429(GUNLUK))["gunluk"] is True
    assert kota.yokla("k", "m", iste=lambda *a, **k: {}) == {"gunluk": False}


def test_toplu_gunlukte_durur_ve_kaldigi_yerden_surer(dizin):
    durum, kosan, yoklanan = dizin / "d.json", [], []

    def is_(i):
        kosan.append(i)
        if i == "b":
            raise RuntimeError("gemini: m: HTTP 429 b'{...'")

    def yok(key, m):
        yoklanan.append(m)
        return kota.cozumle(GUNLUK)

    s = kota.toplu(["a", "b", "c"], is_, durum, "k", yokla_=yok)
    assert (s["dur"], s["kaldi"], s["bitti"], kosan, yoklanan) == ("gunluk", "b", ["a"], ["a", "b"], [kisa.MODELLER[0]])
    assert kota.acik_modeller() == kisa.MODELLER[1:]
    kosan.clear()
    s = kota.toplu(["a", "b", "c"], lambda i: kosan.append(i), durum, "k", yokla_=yok)
    assert (s["dur"], s["bitti"], s["hata"], kosan) == ("bitti", ["a", "b", "c"], {}, ["b", "c"])


def test_toplu_hepsi_tukenmisse_istek_yok(dizin):
    for m in kisa.MODELLER:
        kota.tukendi(m, {"gunluk": True})
    s = kota.toplu(["a"], lambda i: pytest.fail("istek atıldı"), dizin / "d.json", "k")
    assert (s["dur"], s["kaldi"]) == ("gunluk", "a")


def test_toplu_dakika_429_ve_diger_hata_elemez(dizin):
    def is_(i):
        raise RuntimeError("gemini: m: HTTP 429" if i == "a" else "gemini: m: HTTP 500")
    s = kota.toplu(["a", "b"], is_, dizin / "d.json", "k", yokla_=lambda key, m: kota.cozumle(DAKIKA))
    assert (s["dur"], s["bitti"], sorted(s["hata"])) == ("bitti", [], ["a", "b"])


def test_gun_bol():
    assert [len(g) for g in kota.gun_bol(list(range(180)), 4, 400)] == [100, 80]
