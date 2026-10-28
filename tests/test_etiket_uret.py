"""SUIT-KIRMIZI-2: katalog kartı 'etiket' alanı (arac_kart) + tools/etiket_uret.py eksik etiketi doldurur."""
import json
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "tools"))
import arac_kart as ak  # noqa: E402
import etiket_uret as eu  # noqa: E402


def _satir():
    return {"ad": "x-arac", "tur": "skill", "ad0": "x-arac", "metin": "deploy helper", "cagri": "Skill x-arac"}


def test_kart_semasinda_etiket_alani_var():
    k = ak.uret(_satir(), {}, None, {"arac": {}}, {}, {})
    assert k["etiket"] == ""


def test_eksik_yalniz_bos_etiketliler():
    ks = [{"ad": "a", "ne": "n", "etiket": ""}, {"ad": "b", "ne": "n", "etiket": "var"}, {"ad": "c", "ne": "n"}]
    assert [k["ad"] for k in eu.eksik(ks)] == ["a", "c"]


def test_doldur_uretici_ile_tamamlar_ve_tavani_korur():
    ks = [{"ad": f"a{i}", "ne": "n", "etiket": ""} for i in range(5)]
    cagri = []

    def uretici(paket):
        cagri.append(len(paket))
        return {k["ad"]: "yayınla, deploy" for k in paket}

    n = eu.doldur(ks, uretici, paket=2, tavan=2)
    assert cagri == [2, 2] and n == 4
    assert sum(1 for k in ks if k["etiket"]) == 4


def test_doldur_uretici_bos_donerse_etiket_bos_kalir():
    ks = [{"ad": "a", "ne": "n", "etiket": ""}]
    assert eu.doldur(ks, lambda p: {}, paket=5, tavan=3) == 0 and ks[0]["etiket"] == ""
