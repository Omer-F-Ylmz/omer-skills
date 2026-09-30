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
    y.write_bytes(("# Frontend\n\n## Teknikler\n\n" + "".join(f"- {s} · video {V[0]} · 1:00 · kaynak: altyazı\n" for s in GOZLEM + TEKNIK)
                   + f"- Prompt'tan tam site üretimi · video {V[0]} · 4:18 · k00438_0.jpg dosya listesi · kaynak: altyazı\n").encode("utf-8"))
    akil.teknik_duzenle(tmp_path)
    fe = _fe(tmp_path)
    assert all(s not in fe for s in GOZLEM) and "position: fixed" in fe and "alev/gürültü" in fe
    assert "Prompt'tan tam site üretimi" in fe  # tablo satırında kanıt metni ('dosya listesi') gözlem kararı vermez
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


# --- K4 panel uygula: göreli yol cwd'de yoksa repo köküne göre; ikisinde de yoksa açık hata (traceback yok)
def _panel(kok, omer=""):
    p = kok / "docs" / "kurulumlar" / "parti" / "p1" / "panel.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(("| aday | a | b | c | d | e | f | Ömer |\n|---|---|---|---|---|---|---|---|\n"
                   f"| caveman | 1 | 2 | 3 | 4 | 5 | 6 | {omer} |\n").encode("utf-8"))
    return p


def test_k4_panel_yolu_repo_kokune_gore(tmp_path, monkeypatch, capsys):
    kok = tmp_path / "r"
    _panel(kok)
    (tmp_path / "baska").mkdir()
    monkeypatch.chdir(tmp_path / "baska")
    ctx = {"env": {"VIDEO_UYGULA_KOK": str(kok)}, "karar": lambda ns, c: 0}
    assert akil.panel_uygula(SimpleNamespace(panel="docs/kurulumlar/parti/p1/panel.md"), ctx) == 0 and "boş 1" in capsys.readouterr().out
    assert akil.panel_uygula(SimpleNamespace(panel="docs/yok/panel.md"), ctx) == 2 and "dosya yok" in capsys.readouterr().out


# --- K5 panelde Ömer kararı kayda işlenmemişse kapat durur (rc≠0, commit yok)
def test_k5_kayda_islenmemis_kararla_kapat_durur(tmp_path, capsys):
    kok = _repo(tmp_path)
    _panel(kok, "ZATEN VAR")
    d = {"parti": "p1", "videolar": {}, "adaylar": {}}
    assert akil.kapat(tmp_path, d, kok, _ctx()) != 0
    assert "önce: video panel uygula" in capsys.readouterr().out and _git(kok, "log", "--oneline").count("\n") == 1
    (kok / "docs" / "kurulumlar" / "kayit.jsonl").write_bytes(
        (json.dumps({"ad": "caveman", "parti": "p1", "karar": "ZATEN VAR (Ömer, panel)"}, ensure_ascii=False) + "\n").encode("utf-8"))
    assert akil.kapat(tmp_path, d, kok, _ctx()) == 0 and _git(kok, "log", "--oneline").count("\n") == 2


# --- K6 kapat izli departman değişikliğini commit'ten önce listeler ve commit'e alır
def test_k6_departman_degisikligi_kapatta(tmp_path, capsys):
    kok = _repo(tmp_path)
    y = kok / "docs" / "departmanlar" / "frontend.md"
    y.parent.mkdir(parents=True)
    y.write_bytes(b"a\n")
    _git(kok, "add", "-A")
    _git(kok, "commit", "-q", "-m", "fe")
    y.write_bytes(b"a\nb\n")
    assert akil.kapat(tmp_path, {"parti": "p1", "videolar": {}, "adaylar": {}}, kok, _ctx()) == 0
    assert "kapat: eklenecek izli: docs/departmanlar/frontend.md" in capsys.readouterr().out
    assert "docs/departmanlar/frontend.md" in _git(kok, "show", "--name-only", "HEAD")
