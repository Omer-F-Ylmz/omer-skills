"""MOTOR-M6: gözlem süzgeci (panel + frontend.md) · envanter dışı kurulu · dinamik tavan · panel yolu · kapat güvenliği · kapat kapsamı."""
import json
from types import SimpleNamespace

from test_m2a import V
from test_m2b import _rapor
from test_m2g import _fe, _md
from test_m3a import _ctx, _git, _repo

from video import akil
from video import parti as pt


# --- K1 ekran tarifi gözlemdir (panel ve frontend.md aynı süzgeç); teknik yapı taşıyan satır teknik kalır
GOZLEM = ["BLAZING ENERGY sitesi, turuncu 'BLAZING MANGO' ekranı … sağ üstte Contact ve Menu",
          "Salt & Ember restoran sitesi hero bölümü: 'Twelve seats…'",
          "Koyu zeminde 'skill' etiketli küçük bir açılır kutu",
          "Solda site taslağı, sağda 'Animate' paneli; 5 adımlı liste"]
TEKNIK = ["Scroll tabanlı hikaye anlatımı ve ince animasyonlu arka plan",
          "Arka planda alev/gürültü efekti + renk değişimi",
          "başlık ölçeği clamp(48px, 8vw, 138px) ile akışkan",
          "Giriş animasyonlarında 'ease-out', çıkışta 'ease-in' eğrisi",
          "Hero başlığı 'clamp()' ile akışkan ölçek",
          "Sağ üstte sabit menü: position: fixed + backdrop-filter blur"]


def test_k1_gozlem_panel_ve_frontend_ayni_suzgec(tmp_path):
    kare = [{"kare": f"{i}:00", "okunan": s} for i, s in enumerate(GOZLEM + TEKNIK)]
    site = [{"teknik": s, "ne": "ekran", "nasil": "-", "kutuphane": "-", "kanit_zamani": "9:00", "kaynak": "altyazı"} for s in GOZLEM]
    tek, _, _ = akil.site_ogren(tmp_path, [(V[0], _md(site_ui=site, kare=kare))])
    assert {x[0] for x in tek} == set(TEKNIK)  # panelin Site/UI bölümü bu listeden kurulur
    fe = _fe(tmp_path)
    assert "backdrop-filter blur" in fe and "BLAZING MANGO" not in fe and "Twelve seats" not in fe and "Animate" not in fe


def test_k1_teknik_duzenle_geriye_donuk_idempotent(tmp_path):
    y = tmp_path / "docs" / "departmanlar" / "frontend.md"
    y.parent.mkdir(parents=True)
    y.write_bytes(("# Frontend\n\n## Teknikler\n\n" + "".join(f"- {s} · video {V[0]} · 1:00 · kaynak: altyazı\n" for s in GOZLEM + TEKNIK)).encode("utf-8"))
    akil.teknik_duzenle(tmp_path)
    fe = _fe(tmp_path)
    assert all(s not in fe for s in GOZLEM) and "position: fixed" in fe and "alev/gürültü" in fe
    bir = y.read_bytes()
    akil.teknik_duzenle(tmp_path)
    assert y.read_bytes() == bir


# --- K2 kayıtta KUR olan (envanter dışı, ör. npm CLI) aday kurulu sayılır ve karşılaştırma kümesine girer
def test_k2_kayitta_kur_kurulu_karsilastirmada(tmp_path):
    ky = tmp_path / "docs" / "kurulumlar" / "kayit.jsonl"
    ky.parent.mkdir(parents=True)
    ky.write_bytes((json.dumps({"ad": "caveman", "karar": "KUR", "tarih": "2026-09-24"}) + "\n").encode("utf-8"))
    ad, _ = akil.birlestir([(V[0], _rapor(V[0], [("caveman", "CLI", "https://github.com/JuliusBrussee/caveman")]))], tmp_path)
    a = next(iter(ad.values()))
    assert a["kurulu"] == "caveman" and akil._arastirma_disi(a)
    a.update(alt_tur="araç", esdeger_p=1.0)
    assert akil._karsilastir(a)


# --- K3 tavan araştırılacak N + 1 karşılaştırma kadar kendiliğinden genişler; üst sınırlı, defterde satır, çağrı sayılmaz
def _dt(**t):
    return {"parti": "p1", "butce": 0.1, "tavan": {"cagri": 12, "usd": 1.0, "cagri_max": 30, "usd_max": 2.0, **t}}


def test_k3_tavan_genisler_defterde_satir(tmp_path, capsys):
    d = _dt()
    akil._tavan_genislet(tmp_path, d, 6, 1)
    out = capsys.readouterr().out
    assert d["tavan"]["cagri"] == 19 and d["tavan"]["usd"] == 1.7
    assert "tavan genişletildi: +6 araştırma +1 karşılaştırma" in out and "üst sınır" not in out
    satir = (tmp_path / "defter.jsonl").read_text(encoding="utf-8").splitlines()
    assert len(satir) == 1 and "tavan genişletildi" in satir[0] and pt._defter(tmp_path)[0] == 0
    akil._tavan_genislet(tmp_path, d, 6, 1)  # parti başına bir kez
    assert d["tavan"]["cagri"] == 19


def test_k3_ust_sinir(tmp_path, capsys):
    d = _dt(usd=1.5)
    akil._tavan_genislet(tmp_path, d, 40, 1)
    assert d["tavan"]["cagri"] == 30 and d["tavan"]["usd"] == 2.0 and "üst sınır" in capsys.readouterr().out


