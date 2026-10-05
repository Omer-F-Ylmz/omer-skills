"""B3 eki (Ömer kararı, 5 Eki): gh arama uçları (search/issues, graphql search) dakikada 30 istek — arama çağrıları arası ≥2.1 sn;
oran sınırında Retry-After / X-RateLimit-Reset kadar (üst sınır ayarda, ≤60) BİR kez bekle, BİR kez yeniden dene; yine olmazsa
erisilemedi. Uyku ve saat sahte; arama olmayan çağrı (releases) beklemez."""
import json

import pytest

from video import getir as gt

SINIR = (1, b"", b"gh: You have exceeded a secondary rate limit (HTTP 403)")


@pytest.fixture
def saat(monkeypatch):
    t, uyku = [1000.0], []
    monkeypatch.setattr(gt, "saat", lambda: t[0])
    monkeypatch.setattr(gt, "uyku", lambda s: (uyku.append(s), t.__setitem__(0, t[0] + s)))
    monkeypatch.setattr(gt, "_son_ara", [float("-inf")])
    return t, uyku


def kos_yap(t, ozel=None):
    def kos(args):
        a = " ".join(args)
        kos.cagri.append((a, t[0]))
        if ozel and (r := ozel(a)):
            return r
        if "releases" in a:
            return 0, b"[]", b""
        if "graphql" in a:
            return 0, json.dumps({"data": {"search": {"nodes": []}}}).encode(), b""
        return 0, json.dumps({"items": [{"title": "T", "html_url": "u", "reactions": {"total_count": 1}}]}).encode(), b""
    kos.cagri = []
    return kos


def test_ayar_sinirlari():
    assert gt.ARAMA["aralik"] >= 2.1 and gt.ARAMA["bekle_ust"] <= 60


def test_ilk_cagri_oran_siniri_bekler_ikinci_deneme_basarili(saat):
    t, uyku = saat
    ilk = [True]

    def ozel(a):
        if "is:open" in a and ilk[0]:
            ilk[0] = False
            return 1, b"HTTP/2.0 403 Forbidden\nRetry-After: 7\n\n{}", SINIR[2]
    hata, kos = [], kos_yap(t, ozel)
    b = gt.yapimci("o/r", kos, hata)
    assert 7 in uyku and hata == [] and "- açık · T · tepki 1" in b
    assert sum("is:open" in a for a, _ in kos.cagri) == 2


def test_iki_kez_sinir_erisilemedi_ust_sinir_kadar_bekler(saat):
    t, uyku = saat
    hata, kos = [], kos_yap(t, lambda a: SINIR if "is:closed" in a else None)
    b = gt.yapimci("o/r", kos, hata)
    assert sum("is:closed" in a for a, _ in kos.cagri) == 2  # bir kez yeniden dene
    assert gt.ARAMA["bekle_ust"] in uyku and "erişilemedi" in b and len(hata) == 1 and "rate limit" in hata[0][1]


def test_ardisik_uc_arama_arasi_en_az_aralik(saat):
    t, _ = saat
    kos = kos_yap(t)
    gt.yapimci("o/r", kos, [])
    z = [z for a, z in kos.cagri if "search/issues" in a or "graphql" in a]
    assert len(z) == 3 and all(b - a >= 2.1 for a, b in zip(z, z[1:]))


def test_releases_beklemez(saat):
    t, uyku = saat
    gt._son_ara[0] = t[0]  # az önce arama yapılmış: arama beklerdi, releases beklemez
    kos = kos_yap(t)
    gt.yapimci("o/r", kos, [])
    assert [z for a, z in kos.cagri if "releases" in a] == [1000.0]
