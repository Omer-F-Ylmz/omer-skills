import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import kilavuz_ara  # noqa: E402
import kilavuz_derin  # noqa: E402
import kilavuz_tekil  # noqa: E402


def test_govde_onek_ve_bosluk_atilir():
    assert kilavuz_tekil.govde("---\nname: a\ndescription: b\n---\n# X\n\n y ") == "# X y"


def test_birlestir_dogrular_kirpar_maskeler(tmp_path, monkeypatch, capsys):
    (tmp_path / "cikti").mkdir()
    (tmp_path / "tekil.tsv").write_text("ad\ttur\taile\tsha\ttemsilci\tbayt\tyol\na\tskill\tx\t1\ta\t5\t\n", encoding="utf8")
    iyi = {"ad": "a", **{k: "v" for k in kilavuz_derin.ALAN}, "nasil": "s " * 100, "tuzak": "anahtar sk-" + "z" * 20}
    (tmp_path / "cikti" / "p001.jsonl").write_text(
        json.dumps(iyi) + "\n" + json.dumps({"ad": "yok", **{k: "v" for k in kilavuz_derin.ALAN}}) + "\nbozuk\n", encoding="utf8")
    monkeypatch.setattr(kilavuz_derin, "KAT", tmp_path)
    monkeypatch.setattr(kilavuz_derin, "IS", tmp_path)
    kilavuz_derin.birlestir()
    d = [json.loads(s) for s in open(tmp_path / "derin.jsonl", encoding="utf8")]
    assert [j["ad"] for j in d] == ["a"] and len(d[0]["nasil"]) <= 160 and "«gizli»" in d[0]["tuzak"]
    assert "json" in capsys.readouterr().out


def test_tarif_bul_ortak_kelime(tmp_path):
    (tmp_path / "eticaret.md").write_text("# E-ticaret sitesi tarifi\n", encoding="utf8")
    (tmp_path / "oyun.md").write_text("# Oyun tarifi\n", encoding="utf8")
    assert kilavuz_ara.tarif_bul("oyun yap", tmp_path).name == "oyun.md"
    assert kilavuz_ara.tarif_bul("zzz", tmp_path) is None
