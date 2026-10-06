"""MÜKEMMEL-3a K3: dayanaklı kapsam (U = A ∪ B dayanaklı) · kayıp türleri · hüküm."""
import pytest

from video import yonlendir as yon

M = ("=== VIDEO v ===\n# v · başlık · short: false\n## Açıklama bağlantıları\nhttps://github.com/obra/superpowers\n"
     "## Segmentler\n[00:01] ruflo kuruyoruz\n## Ekran metni (OCR)\nclaude-mem panel\n## Kareler\n")


@pytest.fixture(autouse=True)
def _anlamsal_kapali(monkeypatch):
    monkeypatch.setattr(yon, "ANLAMSAL", False)


def _f(*adlar):
    return {"videolar": [{"id": "v", "adaylar": [{"ad": a} for a in adlar]}]}


def test_eslesen_oge_tek_sayilir():
    r = yon.k3([_f("Ruflo")], [_f("Ruflo")], M)
    assert r["u"]["adaylar"] == 1
    assert r["A"]["tum"]["geri"] == r["B"]["tum"]["geri"] == 1.0
    assert sum(r["kayip"].values()) == 0


def test_dayanaksiz_a_ogesi_b_geri_cagirmasini_dusurmez():
    r = yon.k3([_f("Ruflo", "Zzqx Yokmuş")], [_f("Ruflo")], M)
    assert r["B"]["tum"]["geri"] == 1.0
    assert r["A"]["tum"]["dogruluk"] == 0.5 and r["B"]["tum"]["dogruluk"] == 1.0
    assert r["a_dayanaksiz"] == 1


def test_b_nin_a_da_olmayan_dayanakli_ogesi_u_ya_girer():
    r = yon.k3([_f("Ruflo")], [_f("Ruflo", "Superpowers")], M)
    assert r["u"]["adaylar"] == 2
    assert r["B"]["adaylar"]["geri"] == 1.0 and r["A"]["adaylar"]["geri"] == 0.5


def test_b_kayiplari_kaynaga_gore():
    r = yon.k3([_f("Ruflo", "Superpowers", "claude-mem")], [_f()], M)
    assert r["kayip"] == {"konuşma": 1, "kare": 1, "açıklama": 1}
    assert r["B"]["tum"]["geri"] == 0.0


def _r(ag, bg, ad=1.0, bd=1.0, ak=1.0, bk=1.0):
    o = lambda g, d, k: {"tum": {"geri": g, "dogruluk": d}, "kareden_okunanlar": {"geri": k, "dogruluk": 1.0}}  # noqa: E731
    return {"A": o(ag, ad, ak), "B": o(bg, bd, bk)}


def test_hukum_bant_icinde_gecti():
    assert yon.k3_hukum(_r(0.80, 0.76, 0.9, 0.86), (0.7, 0.62), 0.1, short=False) == "geçti"


def test_hukum_bant_disi_kaldi():
    h = yon.k3_hukum(_r(0.80, 0.70), (0.7, 0.5), 0.1, short=False)
    assert h.startswith("kaldı") and "geri" in h and "görev" in h


def test_hukum_short_kareden_okunanlar():
    assert yon.k3_hukum(_r(1, 1, ak=0.9, bk=0.8), (1, 1), 0, short=False) == "geçti"
    assert "kareden_okunanlar" in yon.k3_hukum(_r(1, 1, ak=0.9, bk=0.8), (1, 1), 0, short=True)
