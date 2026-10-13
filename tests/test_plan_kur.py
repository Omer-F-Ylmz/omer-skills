"""ENVANTER-3: plan_kur.py tek çağrı çıktısı + katalog_ara öğrenim grubu."""
import json
import os
import subprocess
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "tools"))
import katalog_ara as ka  # noqa: E402
import plan_kur as pk  # noqa: E402

ENV = dict(os.environ, PYTHONIOENCODING="utf-8")


def kos(*a):
    return subprocess.run([sys.executable, str(KOK / "tools" / "plan_kur.py"), *a], capture_output=True, text=True,
                          encoding="utf8", env=ENV).stdout


def test_rutin_tek_satir():
    o = kos("README'deki yazım hatasını düzelt.")
    assert "RUTİN" in o and "<aday-listesi>" not in o and len(o) < 600


def test_zor_tum_bolumler_ve_tavan():
    o = kos("Pazarlama sitesi yap: KVKK uyumlu iletişim formu, SEO, güvenlik testi ve yayın")
    for s in ("kapılar:", "inceleme ajanları:", "Konsey", "Kapanış (6)", "<aday-listesi>", "semgrep", "gitleaks"):
        assert s in o, s
    assert len(o) < 20000  # ~≤5k jeton (Desktop notu 1)


def test_cok_is_tek_komut():
    o = kos("ffmpeg ile videonun ilk 10 saniyesini kes.", "Three.js oyununa çok oyunculu mod ve hile önleme ekle")
    assert "# İŞ 1" in o and "# İŞ 2" in o and o.count("RUTİN") == 1


def test_tur_tablosu_araclari_katalogda():
    ad = {json.loads(s)["ad"].lower() for s in (KOK / "docs" / "katalog" / "yetenek.jsonl").read_text(encoding="utf8").splitlines()}
    # plugin ajanları (Agent listesinde) ve kurulmamış ZAP katalogda yok: bilinçli istisna
    istisna = {"zap", "ecc:code-reviewer", "ecc:csharp-reviewer", "differential-review:adversarial-modeler",
               "finish-gate"}  # "UI Finish-Gate Reviewer" çok kelimeli agency ajan adı
    for k, v in pk.TUR.items():
        for parca in " · ".join(v[1:3]).replace(">", "·").split("·"):
            for w in parca.replace(":", " ", 1).split()[1:] if ":" in parca.split()[0] else parca.split():
                w = w.strip("(),").lower()
                if "-" in w.lstrip("-") and w not in istisna and not w.startswith(("ecc:", "differential-review:")):
                    assert w in ad or any(a.endswith(":" + w) for a in ad), (k, w)


def test_ogrenim_ayri_grup(tmp_path, monkeypatch):
    f = tmp_path / "ogrenim.jsonl"
    f.write_text(json.dumps({"ne": "Hero GLB 2 MB altında tutulur", "is": "3D web sitesi", "kaynak": "x.md:3",
                             "alan": "3d,frontend", "araclar": "glb_hat"}, ensure_ascii=False) + "\n", encoding="utf8")
    monkeypatch.setattr(ka, "OGRENIM", f)
    r = ka.ogrenim_ara("3D web sitesi hero GLB boyutu")
    assert len(r) == 1 and r[0]["tur"] == "ogrenim" and r[0]["cagri"] == "x.md:3"
