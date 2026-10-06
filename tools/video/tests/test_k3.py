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


def test_dogrulanamadi_ayri_sinif_ii_de_u_disinda_i_de_kare():
    """MÜKEMMEL-3a2: doğrulanamadı öğe (i) U'da kare olarak, (ii) U dışında; sayısı iki varyantta da verilir."""
    f = {"videolar": [{"id": "v", "kareden_okunanlar": [{yon.OLCUM["kareden_okunanlar"][0]: "Qwxz Panosu"}]}]}
    i, ii = yon.k3([f], [_f()], M), yon.k3([f], [_f()], M, dg_u=False)
    assert i["u"]["kareden_okunanlar"] == 1 and ii["u"]["kareden_okunanlar"] == 0
    assert i["kayip"]["kare"] == 1 and ii["kayip"]["kare"] == 0
    assert i["dg"] == ii["dg"] == {"A": 1, "B": 0}


@pytest.mark.parametrize("sonuc, kaynak, u, az, dg", [("görüldü", "kare", 1, 0, 0), ("görülmedi", None, 0, 1, 0),
                                                     ("belirsiz", "doğrulanamadı", 0, 0, 1)])
def test_kare_gorsel_dogrulamasi_siniflar(sonuc, kaynak, u, az, dg):
    """MÜKEMMEL-3b: kare-görsel — görüldü → dayanaklı (kare) · görülmedi → dayanaksız · belirsiz → doğrulanamadı kalır."""
    k = yon.OLCUM["kareden_okunanlar"][0]
    o, gor = {k: "Qwxz Panosu"}, {("kareden_okunanlar", "Qwxz Panosu"): sonuc}
    assert yon.kanit("kareden_okunanlar", o, M, gorsel=gor) == kaynak
    r = yon.k3([{"videolar": [{"id": "v", "kareden_okunanlar": [o]}]}], [_f()], M, dg_u=False, gorsel=gor)
    assert (r["u"]["kareden_okunanlar"], r["a_dayanaksiz"], r["dg"]["A"]) == (u, az, dg)


@pytest.mark.parametrize("x, o", [("kareden_okunanlar", {yon.OLCUM["kareden_okunanlar"][0]: "ruflo panel başlık qqq"}),
                                  ("adaylar", {"ad": "ruflo superpowers claude", "karede_gorulen": "panel"})])
def test_kare_ogesi_daginik_eslesme_dogrulanamadi(x, o):
    """MÜKEMMEL-4b: kelimeler bölümlere dağınık (tüm metinde dayanaklı, tek kaynakta değil) kare öğesi → None değil doğrulanamadı."""
    assert yon.kanit(x, o, M) == "doğrulanamadı"


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


def test_k3_paydalari_doner():
    """MÜKEMMEL-4: n = ölçünün paydası — geri |U| · doğruluk B form başı öğe ort. · kareden_okunanlar |U_kare|."""
    r = yon.k3([_f("Ruflo", "Superpowers")], [_f("Ruflo", "Zzqx Yokmuş", "claude-mem")], M)
    assert r["n"] == {"geri": 3, "dogruluk": 3, "kareden_okunanlar": 0}


def test_ocr_aktar_suzer_ve_kareden_okunanlara_ekler():
    """MÜKEMMEL-4 Mekanizma A: ≥3 harf · tekrarsız (farklı karede aynı metin tek) · video başı ≤ tavan · kaynak "ocr"."""
    p = ("=== VIDEO v ===\n## Segmentler\n[0:01] merhaba\n## Ekran metni (OCR)\n[0:02] Claude Code\n[0:03] 12 ab\n"
         "[0:05] claude code\n[0:06] Ruflo Swarm\n[0:07] Mevcut\n[0:08] Fazla Satır\n## Kareler\n")
    f = {"videolar": [{"id": "v", "kareden_okunanlar": [{"kare": "0:07", "okunan": "Mevcut"}]}]}
    yon.ocr_aktar(f, p, tavan=2)
    assert f["videolar"][0]["kareden_okunanlar"] == [{"kare": "0:07", "okunan": "Mevcut"},
                                                     {"kare": "0:02", "okunan": "Claude Code", "kaynak": "ocr"},
                                                     {"kare": "0:06", "okunan": "Ruflo Swarm", "kaynak": "ocr"}]


@pytest.mark.parametrize("n, h", [({"geri": 3, "dogruluk": 11, "kareden_okunanlar": 3}, "geçti"),
                                  ({"geri": 40, "dogruluk": 40, "kareden_okunanlar": 40}, "kaldı: geri, doğruluk, kareden_okunanlar")])
def test_hukum_bant_max_005_1_bolu_n(n, h):
    """MÜKEMMEL-4: eşitlik bandı = max(0.05, 1/n); geri 1→0.67 (n 3) · doğruluk 1→0.91 (n 11) · kare 1→0.67 (n 3)."""
    assert yon.k3_hukum({**_r(1, 0.67, 1, 0.91, 1, 0.67), "n": n}, (1, 1), 0, short=True) == h
