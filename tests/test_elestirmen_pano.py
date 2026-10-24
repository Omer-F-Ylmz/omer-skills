"""ARAC-KAPI-1B madde 3-4: elestirmen.py (3 ucretsiz elestirmen) + verim_pano eksik-tur sutunu."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import elestirmen  # noqa: E402
import verim_pano  # noqa: E402


def sahte(tur, istem, dosyalar, secenek=(), gorsel=None):
    rol = next(r for r in elestirmen.ROLLER if r in istem)
    return {"ozet": f"{rol} onerisi " + "x" * 400}, "m:free", 1, {}, False


def test_uc_elestirmen_ve_kisa_cikti(tmp_path, capsys):
    f = tmp_path / "ekran.md"
    f.write_text("baslik ve govde", encoding="utf-8")
    cikti = tmp_path / "o.json"
    r = elestirmen.elestir(str(f), sahte)
    assert [x["rol"] for x in r] == ["tasarimci", "kullanici", "performans"]
    assert all(x["oneri"] for x in r)
    assert elestirmen.main([str(f), str(cikti)], sahte) == 0
    ozet = capsys.readouterr().out
    assert len(ozet) <= 600  # Claude jetonu <=200/cagri (~3 karakter/jeton, Turkce)
    assert len(json.loads(cikti.read_text(encoding="utf-8"))) == 3  # tam metin dosyada


def test_ucretsiz_yol_yoksa_rol_yok_isaretli(tmp_path):
    f = tmp_path / "e.md"
    f.write_text("x", encoding="utf-8")
    r = elestirmen.elestir(str(f), lambda *a, **k: (None, None, 2, {}, False))
    assert [x["oneri"] for x in r] == [None, None, None]
    assert elestirmen.main([str(f), str(tmp_path / "o.json")], lambda *a, **k: (None, None, 2, {}, False)) == 5


def test_eksik_tur_maliyeti_ve_en_sik_arac(tmp_path, monkeypatch):
    sira = tmp_path
    (sira / "a.json").write_text(json.dumps({"total_cost_usd": 1.0}), encoding="utf-8")
    (sira / "a-a.json").write_text(json.dumps({"total_cost_usd": 0.5}), encoding="utf-8")
    (sira / "b-a2.json").write_text(json.dumps({"total_cost_usd": 0.25}), encoding="utf-8")
    for ad, e in (("a", ["semgrep", "gitleaks"]), ("b", ["semgrep"])):
        (sira / f"{ad}.denetim.json").write_text(json.dumps({"durum": "arac_eksik", "eksik": e}), encoding="utf-8")
    (sira / "c.denetim.json").write_text(json.dumps({"durum": "ok", "eksik": ["markitdown"]}), encoding="utf-8")
    monkeypatch.setattr(verim_pano, "SIRA", sira)
    dolar, adet, sik = verim_pano.eksik_tur()
    assert (dolar, adet) == (0.75, 2)
    assert sik[0] == ("semgrep", 2) and ("markitdown", 1) not in sik
