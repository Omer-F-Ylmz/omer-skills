"""MAKARA SLEEP-3: paket redaksiyon/sızıntı kapısı, --bulut kipi (ctypes/Obsidian yok), çek (kid tekil, hedef yeniden eşleme), zincir simülasyonu."""
import json
import shutil
import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import makara_cek as c  # noqa: E402
import makara_gece as g  # noqa: E402
import makara_paket as p  # noqa: E402
from test_makara import _saglam  # noqa: E402

SAHTE_ANAHTAR = "sk-" + "a1B2c3D4e5F6g7H8i9J0k1L2"
AWS = "AKIA" + "Z3MQ7XJ2N5PL6TQW"  # redaksiyonun tanımadığı ama gitleaks'in tanıdığı desen


def _kok(tmp_path, ek=""):
    kok = tmp_path / "kok"
    (kok / "skills/a").mkdir(parents=True)
    (kok / "skills/a/SKILL.md").write_text("# a\nKurallar.\nmail: omery3899@gmail.com yol C:\\Users\\pc\\x " + SAHTE_ANAHTAR + ek, encoding="utf-8")
    kasa = tmp_path / "kasa"
    (kasa / "50-dersler").mkdir(parents=True)
    (kasa / "50-dersler" / f"ders-{time.strftime('%Y-%m-%d')}.md").write_text("- Önce testi çalıştır (×3, ilk x)\n", encoding="utf-8")
    gorev = tmp_path / "tasks.json"
    gorev.write_text(json.dumps({"tasks": [dict(id="t1", split="val", intent="Özetle", reference="En fazla 3 satır.", context_excerpt="HAM " + SAHTE_ANAHTAR)]}), encoding="utf-8")
    return kok, kasa, gorev


def test_paket_redakte_eder_ve_ham_alan_girmez(tmp_path, monkeypatch):
    monkeypatch.setattr(p, "KOK_USTU", {})
    kok, kasa, gorev = _kok(tmp_path)
    ok, m = p.kur(tmp_path / "paket", kok, kasa, gorev, tarayici=lambda d: (True, ""))
    assert ok, m
    tum = "".join(f.read_text(encoding="utf-8") for f in (tmp_path / "paket").rglob("*") if f.is_file() and "tools" not in f.parts)
    for yasak in (SAHTE_ANAHTAR, "omery3899", "gmail.com", "C:\\Users", "HAM"):
        assert yasak not in tum
    assert "context_excerpt" not in tum and (tmp_path / "paket/manifest.json").exists() and (tmp_path / "paket/dersler").exists()


def test_paket_gitleaks_bulgusunda_cikmaz_ve_eski_paket_korunur(tmp_path, monkeypatch):
    monkeypatch.setattr(p, "KOK_USTU", {})
    kok, kasa, gorev = _kok(tmp_path)
    assert p.kur(tmp_path / "paket", kok, kasa, gorev, tarayici=lambda d: (True, ""))[0]
    onceki = (tmp_path / "paket/manifest.json").read_text(encoding="utf-8")
    ok, m = p.kur(tmp_path / "paket", kok, kasa, gorev, tarayici=lambda d: (False, "gitleaks bulgu"))
    assert not ok and "REDDEDİLDİ" in m
    assert (tmp_path / "paket/manifest.json").read_text(encoding="utf-8") == onceki and not (tmp_path / "paket.tmp").exists()
    ok, m = p.kur(tmp_path / "paket", kok, kasa, gorev, tarayici=lambda d: (False, "gitleaks çalışmadı"))  # tarayıcı yoksa temiz sayılmaz
    assert not ok


@pytest.mark.skipif(shutil.which("gitleaks") is None, reason="gitleaks yok")
def test_gercek_gitleaks_redaksiyondan_kacani_yakalar(tmp_path, monkeypatch):
    monkeypatch.setattr(p, "KOK_USTU", {})
    kok, kasa, gorev = _kok(tmp_path)
    assert p.kur(tmp_path / "temiz", kok, kasa, gorev)[0]
    (kok / "skills/a/SKILL.md").write_text("# a\naws_access_key_id = " + AWS + "\n", encoding="utf-8")
    ok, m = p.kur(tmp_path / "kirli", kok, kasa, gorev)
    assert not ok and "gitleaks" in m and not (tmp_path / "kirli").exists()


def test_zincir_paket_bulut_cek(tmp_path, monkeypatch):
    monkeypatch.setattr(p, "KOK_USTU", {})
    monkeypatch.setattr(c, "KOK_USTU", {})
    kok, kasa, gorev = _kok(tmp_path)
    assert p.kur(tmp_path / "paket", kok, kasa, gorev, tarayici=lambda d: (True, ""))[0]

    def yasak(*a, **k):
        raise AssertionError("Claude/Windows yolu çağrıldı")

    class Pen:
        def __getattr__(self, ad):
            return yasak
    for ad, v in dict(BULUT=False, GIRDI=None, M=g.M, KASA=g.KASA, OZET=g.OZET, HAFTA=g.HAFTA, GOREV=g.GOREV, SERITLER=g.SERITLER, TABAN={}, ctypes=Pen()).items():
        monkeypatch.setattr(g, ad, v)
    for ad in ("DIZIN", "DURUM", "ERT", "SONUC", "ENT"):
        monkeypatch.setattr(g.H, ad, getattr(g.H, ad))
    monkeypatch.setattr(g.Say, "bitis", float("inf")); g.Say.n = 0; g.Say.olu = set()
    monkeypatch.setattr(g.H, "cagir", lambda tur, istem, **kw: (_saglam(tur, istem), "fake/x", []))
    monkeypatch.setattr(g.H, "_haiku", yasak)
    monkeypatch.setattr(g.subprocess, "run", yasak)
    out = tmp_path / "out"
    bit = g.bulut(tmp_path / "paket", out, sure=600)
    assert bit == ["skill", "ogren", "router", "kural", "ters"] or set(bit) == {s[0] for s in g.SERITLER}
    kum = sorted((out / "makara/kum").glob("*.json"))
    assert kum and g.Say.claude == 0 and (out / "uyku-ozet.txt").exists() and list((out / "rapor/90-log").glob("uyku-*.md"))
    assert not any(a for a in g.H.ENT if a.prov in ("omniroute", "github"))

    m = tmp_path / "pcm"
    kasa2 = tmp_path / "kasa2"
    assert c.birlestir(out, m, kok)[0] == len(kum)
    yeni, var, atla = c.birlestir(out, m, kok)
    assert (yeni, var) == (0, len(kum))  # aynı kid çift yazılmaz
    r = json.loads(next((m / "kum").glob("*.json")).read_text(encoding="utf-8"))
    assert r["hedef"] == str(kok / "skills/a/SKILL.md") and r["kaynak"] == "bulut" and r["durum"] == "bekliyor"
    assert c.rapor_not(out, kasa2) == 1 and c.rapor_not(out, kasa2) == 1
    assert len(list((kasa2 / "90-log").glob("*-bulut.md"))) == 1


def test_cek_hedef_kok_disina_cikamaz_ve_bozuk_kid_atlanir(tmp_path):
    kok = tmp_path / "kok"; (kok / "skills/a").mkdir(parents=True); (kok / "skills/a/SKILL.md").write_text("x", encoding="utf-8")
    assert c.yerel_hedef("/r/paket/hedefler/skills/a/SKILL.md", kok) == kok / "skills/a/SKILL.md"
    assert c.yerel_hedef("/r/paket/hedefler/../../etc/passwd", kok) is None and c.yerel_hedef("/etc/passwd", kok) is None
    art = tmp_path / "art/makara/kum"; art.mkdir(parents=True)
    (art / "x.json").write_text(json.dumps(dict(id="../kotu", durum="bekliyor", hedef="/r/hedefler/skills/a/SKILL.md", kural="k")), encoding="utf-8")
    assert c.birlestir(tmp_path / "art", tmp_path / "m", kok) == (0, 0, 1)
