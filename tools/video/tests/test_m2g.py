"""MOTOR-M2g: geliştirme karşılaştırması bizdeki bilgiyle (boş → çağrı yok, kurulu adaya eylem=kurulum → form_red) · teknik kütüphanesi: gözlem çıkar, kütüphane kontrolü, aynı teknik tek satır."""
from test_m2a import V
from test_m2f import Tasiyici, _a, _d, _f, _pk

from video import akil
from video import parti as pt


def _satir(aday, eylem, oneri):
    return {"aday": aday, "videodaki_kullanim": "v", "bizdeki_durum": "b", "fark": "f", "gelistirme_onerisi": "ölçüm için deneme yap",
            "oneri": oneri, "kanit": "1:00 hızlı", "eylem": eylem}


def _p(tmp_path):
    pdir = tmp_path / "p"
    pdir.mkdir(exist_ok=True)
    return pdir


# K1 bizde bilgisi boş aday çağrıya girmez; panelde "bizde bilgi yok" (hata değil)
def test_k1_bizde_bos_cagriya_girmez(tmp_path):
    pdir, d = _p(tmp_path), _d()
    d["adaylar"] = {"a1": _a("rtk"), "a2": _a("bilinmeyen-arac")}
    t = Tasiyici({"satirlar": [_satir("a1", "ölçüm", "ÖĞREN")]})
    akil.gelistir(pdir, d, tmp_path, {"env": {}, "cagir": t})
    assert len(t.cagrilar) == 1 and "ADAY: a1" in t.cagrilar[0] and "ADAY: a2" not in t.cagrilar[0]
    assert d["bizde_yok"] == ["a2"]
    assert "bizde bilgi yok: a2" in akil.panel(pdir, d, tmp_path).read_text(encoding="utf-8")
    d2, t2 = _d(), Tasiyici({"satirlar": []})
    d2["adaylar"] = {"a2": _a("bilinmeyen-arac")}
    assert akil.gelistir(pdir, d2, tmp_path, {"env": {}, "cagir": t2}) == [] and t2.cagrilar == [] and d2["bizde_yok"] == ["a2"]


# K1 kurulu adaya eylem=kurulum → form_red; "deneme" kelimesi geçen ölçüm önerisi geçer
def test_k1_kuruluya_kurulum_form_red(tmp_path):
    pdir, d = _p(tmp_path), _d()
    d["adaylar"] = {"a1": _a("rtk")}
    t = Tasiyici({"satirlar": [_satir("a1", "kurulum", "UYARLA")]})
    assert akil.gelistir(pdir, d, tmp_path, {"env": {}, "cagir": t}) == [] and len(t.cagrilar) == 3 and "gelistirme" not in d
    d = _d()
    d["adaylar"] = {"a1": _a("rtk")}
    t = Tasiyici({"satirlar": [_satir("a1", "ölçüm", "ÖĞREN")]})
    assert [x["eylem"] for x in akil.gelistir(pdir, d, tmp_path, {"env": {}, "cagir": t})] == ["ölçüm"] and len(t.cagrilar) == 1


def _md(site_ui=(), kare=()):
    return pt.rapor_md(_f(site_ui=list(site_ui), kareden_okunanlar=list(kare)), _pk(), [])


def _fe(kok):
    return (kok / "docs" / "departmanlar" / "frontend.md").read_text(encoding="utf-8")


# K2 ham kare gözlemi kütüphaneye girmez; mekanizmalı kare satırı teknik kalır
def test_k2_gozlem_kutuphaneye_girmez(tmp_path):
    kare = [{"kare": "6:37 sağ alt", "okunan": "sağ altta model etiketi Opus 4.7"},
            {"kare": "1:34 Awwwards sayfası", "okunan": "CLOU, Site of the Day, puan 7.62/10"},
            {"kare": "6:37 terminal", "okunan": "Dev server http://localhost:5174/"},
            {"kare": "2:00 Dosya sekmesi", "okunan": "dosya listesi index.html, script.js"},
            {"kare": "3:10 kod", "okunan": "başlık ölçeği clamp(48px, 8vw, 138px) ile akışkan"}]
    tek, _, _ = akil.site_ogren(tmp_path, [(V[0], _md(kare=kare))])
    fe = _fe(tmp_path)
    assert [x[0] for x in tek] == ["başlık ölçeği clamp(48px, 8vw, 138px) ile akışkan"] and "clamp(48px, 8vw, 138px)" in fe
    for s in ("Opus 4.7", "Site of the Day", "localhost", "index.html"):
        assert s not in fe


# K3 kütüphane adı omer-kutuphaneler + kurulu skill'lerle karşılaştırılır; "kontrol edilmedi" yazılmaz
def test_k3_kutuphane_kontrolu(tmp_path):
    sk = tmp_path / "skills"
    (sk / "omer-kutuphaneler").mkdir(parents=True)
    (sk / "omer-kutuphaneler" / "SKILL.md").write_text(
        "| kütüphane | ne | tip | pinli kurulum | lisans | context7 |\n|---|---|---|---|---|---|\n"
        "| lenis | smooth | landing | npm `npm.cmd i lenis@1.3.26` | MIT | x |\n", encoding="utf-8")
    (sk / "web-sahne-desenleri").mkdir()
    (sk / "web-sahne-desenleri" / "SKILL.md").write_text("WebGL imleç reveal: OGL ile maske\n", encoding="utf-8")
    site = [{"teknik": "Yumuşak kaydırma", "ne": "smooth", "kanit_zamani": "tahmin: Lenis", "kaynak": "omer-kutuphaneler/scroll-craft kontrol edilmedi"},
            {"teknik": "İmleç maskesi", "ne": "mask", "kanit_zamani": "tahmin: OGL", "kaynak": "video"},
            {"teknik": "Parçacık alanı", "ne": "p", "kanit_zamani": "tahmin: zzqlib", "kaynak": "video"}]
    akil.site_ogren(tmp_path, [(V[0], _md(site_ui=site))])
    fe = _fe(tmp_path)
    assert "kontrol edilmedi" not in fe and "tahmin: Lenis" in fe
    assert "bizde: omer-kutuphaneler/lenis@1.3.26" in fe and "bizde: web-sahne-desenleri" in fe
    assert any("zzqlib" in s and "bizde yok" in s for s in fe.splitlines())


# K4 aynı teknik (normalize ad) birden çok videoda → tek satır + tüm kaynaklar
def test_k4_ayni_teknik_tek_satir(tmp_path):
    s1 = [{"teknik": "Scroll ile pinlenen hero", "ne": "pin", "kanit_zamani": "1:05", "kaynak": "video"}]
    s2 = [{"teknik": "scroll ile pinlenen hero", "ne": "pin", "kanit_zamani": "2:10", "kaynak": "video"}]
    akil.site_ogren(tmp_path, [(V[0], _md(site_ui=s1)), (V[1], _md(site_ui=s2))])
    L = [x for x in _fe(tmp_path).splitlines() if "pinlenen" in x]
    assert len(L) == 1 and V[0] in L[0] and V[1] in L[0] and "1:05" in L[0] and "2:10" in L[0]
