"""MOTOR-M2f: tamam_eksik raporunda EKSİK bölüm · site öğrenme (teknik kütüphanesi + 23c anatomi) · ZATEN VAR geliştirme karşılaştırması · panel uygula idempotent."""
import json
from types import SimpleNamespace

from test_m2a import V

from video import akil
from video import parti as pt
from video import tarama as tr
from video import uygula as uy


def _pk():
    return {"baslik": "Site dersi", "kanal": "k", "sure": 600, "dil": "en", "id": V[0], "metin": "## Segmentler\n[0:10] a\n"}


def _f(**k):
    f = {"ozet": "Landing page hero: Tailwind CSS, GSAP animasyon, UI site tasarımı", "bolumler": [], "adaylar": [], "promptlar": [],
         "aciklama_baglantilari": [], "site_ui": [], "iddialar": [], "kareden_okunanlar": [], "belirsizlikler": []}
    f.update(k)
    return f


def _d():
    return {"parti": "p1", "model": "m", "butce": 0.1, "tavan": {"usd": 1.0, "cagri": 10}, "videolar": {}, "adaylar": {}}


class Tasiyici:
    def __init__(self, form):
        self.form, self.cagrilar = form, []

    def __call__(self, sistem, metin, sema, **k):
        self.cagrilar.append(metin)
        return {"form": self.form, "usage": {}, "usd": 0.01}


# K1 tamam_eksik: form Site/UI'yi vermedi → rapor bölümü EKSİK başlığıyla yazar; rapor-denetle uyarı sayar, hata değil
def test_k1_eksik_bolum_uyari():
    f, _ = pt.kismi(_f(), [f"{V[0]} rapor: bölüm eksik: ## {tr.SITE_UI}"], V[0])
    md = pt.rapor_md(f, _pk(), [])
    assert tr.frontend_mu(md)
    assert f"## {tr.SITE_UI}\n- EKSİK:" in md
    temiz = "\n".join(s for s in md.splitlines() if "EKSİK:" not in s)  # cli rapor_denetle gibi
    assert not [h for h in tr.denetle(temiz) if tr.SITE_UI in h]
    assert any(tr.SITE_UI in u for u in tr.uyarilar(md))
    assert f"bölüm eksik: ## {tr.SITE_UI}" in tr.denetle(pt.rapor_md(_f(), _pk(), []))  # tam formda hâlâ hata


def _site_md(anatomi=False):
    md = pt.rapor_md(_f(site_ui=[{"teknik": "scroll ile pinlenen hero", "ne": "GSAP ScrollTrigger pin", "kanit_zamani": "1:05", "kaynak": "kare"}],
                        kareden_okunanlar=[{"kare": "kare 2 (2:10)", "okunan": "bento grid 12 kolon"}],
                        promptlar=[{"amac": "hero üret", "metin": "Build a dark landing hero with gradient mesh and a big serif headline for a studio",
                                    "kanit_zamani": "3:00", "kaynak": "kare"}]), _pk(), [])
    return md + ("## Prompt anatomisi\n" + "".join(f"{x}: değer {x}\n" for x in uy.ANATOMI) if anatomi else "")


# K2 site raporu → teknik kütüphanesi + prompt anatomisi (alan varsa 0 çağrı) + panel bölümü
def test_k2_site_ogren_anatomili_cagrisiz(tmp_path):
    t = Tasiyici({x: "x" for x in uy.ANATOMI})
    pdir = tmp_path / "p"
    pdir.mkdir()
    d = _d()
    tek, n, bek = akil.site_ogren(tmp_path, [(V[0], _site_md(anatomi=True))], pdir, d, {"env": {}, "cagir": t})
    assert [x[0] for x in tek] == ["scroll ile pinlenen hero", "bento grid 12 kolon"] and n == 1 and bek == [] and t.cagrilar == []
    fe = (tmp_path / "docs" / "departmanlar" / "frontend.md").read_text(encoding="utf-8")
    assert "scroll ile pinlenen hero" in fe and V[0] in fe
    fp = (tmp_path / "docs" / "departmanlar" / "frontend-promptlar.md").read_text(encoding="utf-8")
    assert V[0] in fp and "3:00" in fp and f"{uy.ANATOMI[0]}: değer" in fp
    assert "a big serif headline for a studio" not in fp  # kalıp ≤15 kelime
    d["site_ui"] = tek
    p = akil.panel(pdir, d, tmp_path).read_text(encoding="utf-8")
    assert f"## {tr.SITE_UI}" in p and "scroll ile pinlenen hero" in p


def test_k2_anatomisiz_site_videosu_tek_cagri(tmp_path):
    t = Tasiyici({x: "y" for x in uy.ANATOMI})
    pdir = tmp_path / "p"
    pdir.mkdir()
    d = _d()
    _, n, bek = akil.site_ogren(tmp_path, [(V[0], _site_md())], pdir, d, {"env": {}, "cagir": t})
    assert len(t.cagrilar) == 1 and n == 1 and bek == []
    akil.site_ogren(tmp_path, [(V[0], _site_md())], pdir, d, {"env": {}, "cagir": t})
    assert len(t.cagrilar) == 1  # anatomi durum'da; yeniden çağrılmaz
    _, _, bek = akil.site_ogren(tmp_path / "b", [(V[0], _site_md())])  # taşıyıcı yok → bekliyor
    assert bek == [V[0]]


def _a(kurulu):
    return {"ad": "x", "adlar": ["x"], "tur": "CLI", "kurulu": kurulu, "repo": None, "arac": True, "durum": "kurulu", "onceki": None,
            "alt_tur": "araç", "esdeger_p": 0.9, "videolar": {V[0]: {"zaman": "1:00", "ne": "n", "kanit": "k", "iddialar": ["hızlı"]}}}


# K3 ZATEN VAR → tek toplu karşılaştırma; kanıtsız öneri yazılmaz; panelde ayrı satır
def test_k3_gelistirme_karsilastirmasi(tmp_path):
    satir = dict(videodaki_kullanim="v", bizdeki_durum="b", fark="f", gelistirme_onerisi="öneri")
    t = Tasiyici({"satirlar": [{"aday": "a1", **satir, "oneri": "UYARLA", "kanit": "1:00 videoda hızlı"},
                               {"aday": "a2", **satir, "oneri": "ÖĞREN", "kanit": ""}]})
    pdir = tmp_path / "p"
    pdir.mkdir()
    d = _d()
    d["adaylar"] = {"a1": _a("rtk"), "a2": _a("jev"), "a3": _a(None)}
    g = akil.gelistir(pdir, d, tmp_path, {"env": {}, "cagir": t})
    assert len(t.cagrilar) == 1 and "ADAY: a3" not in t.cagrilar[0] and "ADAY: a1" in t.cagrilar[0]
    assert [x["aday"] for x in g] == ["a1"]
    akil.gelistir(pdir, d, tmp_path, {"env": {}, "cagir": t})
    assert len(t.cagrilar) == 1
    p = akil.panel(pdir, d, tmp_path).read_text(encoding="utf-8")
    assert "## Geliştirme önerileri" in p and "| a1-gelistirme |" in p and "a2-gelistirme" not in p


# K5 ikinci panel uygula 0 yeni kayıt satırı
def test_k5_panel_uygula_idempotent(tmp_path, capsys):
    pd = tmp_path / "docs" / "kurulumlar" / "parti" / "p1"
    pd.mkdir(parents=True)
    y = pd / "panel.md"
    y.write_text("| aday | tür | video | lisans | güvenlik | önerilen | gerekçe | Ömer |\n|---|---|---|---|---|---|---|---|\n"
                 "| a1 | CLI | 1 | MIT | - | DENE | g | ERTELE |\n| a2 | CLI | 1 | MIT | - | DENE | g | |\n", encoding="utf-8")
    ctx, ns = {"env": {"VIDEO_UYGULA_KOK": str(tmp_path)}}, SimpleNamespace(panel=str(y))
    ky = tmp_path / "docs" / "kurulumlar" / "kayit.jsonl"
    assert akil.panel_uygula(ns, ctx) == 0
    assert akil.panel_uygula(ns, ctx) == 0
    k = [json.loads(s) for s in ky.read_text(encoding="utf-8").splitlines() if s.strip()]
    assert len(k) == 1 and k[0]["parti"] == "p1"
    assert "işlenen 0 · zaten kayıtlı 1 · boş 1 · hatalı 0" in capsys.readouterr().out
