"""F3-V5: bölümleme — paket zamana göre k parçaya (sınır en yakın bölüm başında), parçalar paralel taranır, formlar mekanik
birleşir (eslesir ile tekil). Testler sahte, canlı çağrı 0."""
import json
import threading

import pytest

from video import hafif
from video import parti as pt
from video import tarama as tr
from video import yonlendir as yon

E1 = "openrouter/openai/gpt-6-luna"
ENV = {"OMNIROUTE_URL": "http://x:1", "OMNIROUTE_KEY": "gizli-anahtar"}
SV = pt.sema(["vid1"])
KARELER = ["C:/c/kare_01.jpg", "C:/c/kare_02.jpg", "C:/c/kare_03.jpg"]
P = "\n".join([
    "=== VIDEO vid1 · süre 9:00 · kare görseli 3 ===",
    "# vid1 · Başlık · Kanal · süre 9:00 · sure_sn 540 · short: false · dil tr · https://youtu.be/vid1",
    "## Chapter", "0:00 Giriş", "2:50 Kurulum", "6:10 Deneme",
    "## Açıklama bağlantıları", "https://x.dev/a",
    "## Segmentler", "damgasız satır", "[0:10] Önce Alfa anlatılıyor.", "[3:00] Sonra Beta kuruluyor.", "[7:00] Sonra Gama deneniyor.",
    "## Ekran metni (OCR)", "[0:20] ALFA EKRAN", "[3:10] BETA EKRAN", "[8:00] GAMA EKRAN",
    "## Kareler", *[f"{k} · {t}" for k, t in zip(KARELER, ("0:30", "3:20", "8:30"))]])


@pytest.fixture(autouse=True)
def _kelime_kurali(monkeypatch):
    monkeypatch.setattr(yon, "ANLAMSAL", False)  # eşleşme yalnız kelime kurallarıyla (belirlenimli)


def _aday(ad):
    return {"ad": ad, "tur": sorted(tr.TUR)[0], "ne": "x", "kanit_zamani": "0:10", "kaynak": "altyazı", "kanit": "x", "repo_url": None}


def _vf(ozet, adlar, bel=(), bolumler=(), linkler=()):
    return {"videolar": [{"id": "vid1", "ozet": ozet, "bolumler": list(bolumler), "adaylar": [_aday(a) for a in adlar],
                          "aciklama_baglantilari": list(linkler), "site_ui": [], "promptlar": [], "iddialar": [],
                          "kareden_okunanlar": [], "belirsizlikler": list(bel)}]}


def test_bolumle_sinirlar_bolum_basinda():
    p3, p4 = yon.bolumle(P, 3), yon.bolumle(P, 4)
    assert [p.splitlines()[0] for p in p3] == [f"Bu çağrı videonun {a}–{b} aralığı; yalnız bu aralıktaki öğeleri yaz."
                                               for a, b in (("0:00", "2:50"), ("2:50", "6:10"), ("6:10", "9:00"))]
    assert len(p4) == 4 and p4[1].startswith("Bu çağrı videonun 2:50–6:10") and p4[3].splitlines()[0].endswith("–9:00 aralığı; yalnız bu aralıktaki öğeleri yaz.")


def test_bolumle_satirlar_dogru_parcada():
    p = yon.bolumle(P, 3)
    for i, (s, o, k) in enumerate([("Alfa", "ALFA", "kare_01"), ("Beta", "BETA", "kare_02"), ("Gama", "GAMA", "kare_03")]):
        for j, x in enumerate(p):
            assert (f"Sonra {s}" in x or f"Önce {s}" in x) == (i == j) and (f"{o} EKRAN" in x) == (i == j) and (k in x) == (i == j)
    for x in p:  # başlık + bölümler + açıklama bağlantıları hepsinde, bölüm başlıkları sırayla
        assert "=== VIDEO vid1" in x and "# vid1 · Başlık" in x and "2:50 Kurulum" in x and "https://x.dev/a" in x
        assert [s for s in x.splitlines() if s.startswith("## ")] == \
            ["## Chapter", "## Açıklama bağlantıları", "## Segmentler", "## Ekran metni (OCR)", "## Kareler"]


def test_bolumle_damgasiz_ilk_parcada():
    p = yon.bolumle(P, 3)
    assert "damgasız satır" in p[0] and not any("damgasız satır" in x for x in p[1:])


def test_bolumle_degerlendir_suzme():
    o = [yon.on_cikarim(x) for x in yon.bolumle(P, 3)]
    assert all("url: https://x.dev/a" in x for x in o)
    assert ["ad: Alfa" in x for x in o] == [True, False, False] and ["ad: Gama" in x for x in o] == [False, False, True]
    assert ["kare: [3:10] BETA EKRAN" in x for x in o] == [False, True, False]


def test_birlestir_tekrar_yok_paraphrase_dahil():
    f = yon.birlestir([_vf("bir", ["Codex GitHub", "Alfa"], ["b1"], [{"zaman": "0:00", "baslik": "G"}], [{"url": "u", "ne": "n", "aday_mi": False, "neden": "n"}]),
                       _vf("iki", ["Codex on GitHub", "Beta"], ["b1", "b2"], [{"zaman": "0:00", "baslik": "G"}], [{"url": "u", "ne": "n", "aday_mi": False, "neden": "n"}]),
                       _vf("üç", ["alfa", "Gama"])])
    v = f["videolar"]
    assert len(v) == 1 and [a["ad"] for a in v[0]["adaylar"]] == ["Codex GitHub", "Alfa", "Beta", "Gama"]
    assert v[0]["ozet"] == "bir iki üç" and v[0]["belirsizlikler"] == ["b1", "b2"]
    assert len(v[0]["bolumler"]) == 1 and len(v[0]["aciklama_baglantilari"]) == 1


def test_birlestir_sema_gecer():
    f = yon.birlestir([_vf("bir", ["A1"]), _vf("iki", ["B1"]), _vf("üç", [])])
    assert pt._denet(f, SV, "form") == []


def _b(c, yanit=None, engel=None):
    def kur(m, env, timeout=600, govde_ek=None):
        def tas(sistem, metin, sema, kareler=(), model=None, **_):
            if engel:
                engel.wait()  # sıralı çağrıda k'ya ulaşılmaz → BrokenBarrierError
            i = next(j for j, s in enumerate(("Alfa", "Beta", "Gama")) if s in metin)
            c.append({"i": i, "sistem": sistem, "metin": metin, "kareler": list(kareler)})
            return (yanit or {}).get(i) or {"form": _vf(f"o{i}", [["Alfa"], ["Beta", "alfa"], ["Gama"]][i]), "usage": {"input_tokens": 10, "output_tokens": 5},
                                             "usd": 0.001, "sure": float(i + 1), "hata": None}
        return tas
    return kur


def _e5(tmp_path, adaylar, c, **k):
    o = tmp_path / "ORN2.json"
    o.write_text('{"id": "ORN2"}', encoding="utf-8")
    return yon.eleme(("S", P, SV, list(KARELER)), adaylar, lambda *a, **kw: {"form": None, "hata": "A yok", "usd": 0}, hafif.MODEL, ENV,
                     lambda ms: [0.8] * len(ms), onbellek=tmp_path / "ab", b_kur=k.pop("b_kur", None) or _b(c),
                     yokla=lambda m, env, gorsel=False: None, ornek21=o, kayit=tmp_path / "k", **k)


def _kayit(tmp_path, ad, i=0):
    return json.loads((tmp_path / "k" / ad.replace("/", "_") / f"{i}.json").read_text(encoding="utf-8"))["yanit"]


def test_v5_v54_k_parca_k_cagri(tmp_path):
    c = []
    _e5(tmp_path, [f"{E1}@V5"], c)
    assert len(c) == 6 and sorted(x["i"] for x in c) == [0, 0, 1, 1, 2, 2]
    for x in c:  # V21 sistemi + parçaya süzülmüş liste · yalnız aralıktaki kareler
        assert x["sistem"].startswith("S\n\n" + yon.EKSIKSIZLIK) and x["sistem"].endswith(yon.ORNEK_BASLIK + '{"id": "ORN2"}')
        assert "url: https://x.dev/a" in x["sistem"] and ("ad: Alfa" in x["sistem"]) == (x["i"] == 0)
        assert x["metin"].startswith("Bu çağrı videonun") and x["kareler"] == [KARELER[x["i"]]]
    c4 = []
    _e5(tmp_path, [f"{E1}@V54"], c4)
    assert len(c4) == 8


def test_v5_paralel(tmp_path):
    c = []
    _e5(tmp_path, [f"{E1}@V5"], c, b_kur=_b(c, engel=threading.Barrier(3, timeout=5)))
    assert len(c) == 6


def test_v5_birlesik_yanit(tmp_path):
    c = []
    _e5(tmp_path, [f"{E1}@V5"], c)
    y = _kayit(tmp_path, f"{E1}@V5")
    v = y["form"]["videolar"][0]
    assert v["ozet"] == "o0 o1 o2" and [a["ad"] for a in v["adaylar"]] == ["Alfa", "Beta", "Gama"] and pt._denet(y["form"], SV, "form") == []
    assert y["usd"] == pytest.approx(0.003) and y["usage"] == {"input_tokens": 30, "output_tokens": 15} and y["sure"] == 3.0 and y["hata"] is None


def test_v5_tavan_parca_basina(tmp_path):
    c = []
    s = _e5(tmp_path, [f"{E1}@V5"], c, tavan_cagri=5)  # 3 + 3 > 5 → ikinci yanıt yok
    assert len(c) == 3 and s["b_usd"] == pytest.approx(0.003)
    c = []
    s = _e5(tmp_path, [f"{E1}@V5"], c, tavan_usd=yon._tahmin(E1, 3) * 2)  # ön tahmin = _tahmin × 3
    assert c == [] and s["satirlar"][0].endswith(" · tavan")


def test_v5_parca_hatasi(tmp_path):
    c = []
    _e5(tmp_path, [f"{E1}@V5"], c, b_kur=_b(c, {1: {"form": None, "usage": {}, "usd": 0.001, "sure": 1.0, "hata": "boom"}}))
    y = _kayit(tmp_path, f"{E1}@V5")
    assert len(c) == 3 and y["hata"] == "parça 2: boom" and y["form"] is None


def test_v5_bilinmeyen_varyant_cagri_0(tmp_path):
    c = []
    s = _e5(tmp_path, [f"{E1}@V55"], c)
    assert c == [] and s["satirlar"] == [f"{E1}@V55 · hata: bilinmeyen varyant: V55 · çağrı 0"]
