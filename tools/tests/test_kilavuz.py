import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import kilavuz_aday  # noqa: E402
import kilavuz_ara  # noqa: E402
import kilavuz_derin  # noqa: E402
import kilavuz_ornek  # noqa: E402
import kilavuz_tekil  # noqa: E402


def test_govde_onek_ve_bosluk_atilir():
    assert kilavuz_tekil.govde("---\nname: a\ndescription: b\n---\n# X\n\n y ") == "# X y"


def test_skill_ailesi_skill_md_ile_cakismaz():
    assert [kilavuz_aday.dosya_adi(a) for a in ("skill", "Skill", "ajan")] == ["skill-aile.md", "Skill-aile.md", "ajan.md"]


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


def test_tur_ad_cakismasi_ve_katalog_isareti(tmp_path, monkeypatch):
    (tmp_path / "cikti").mkdir()
    (tmp_path / "tekil.tsv").write_text("ad\ttur\taile\tsha\ttemsilci\tbayt\tyol\na\tskill\tx\t1\ta\t5\t\na\tajan\tx\t2\ta\t5\t\n", encoding="utf8")
    (tmp_path / "cikti" / "p001.jsonl").write_text(
        json.dumps({"ad": "a", "tur": "ajan", **{k: "v" for k in kilavuz_derin.ALAN}}) + "\n"
        + json.dumps({"ad": "a", "tur": "skill", "durum": "katalog"}) + "\n"
        + json.dumps({"ad": "a", **{k: "tursuz" for k in kilavuz_derin.ALAN}}) + "\n", encoding="utf8")
    for m in (kilavuz_derin, kilavuz_ara):
        monkeypatch.setattr(m, "KAT", tmp_path)
    monkeypatch.setattr(kilavuz_derin, "IS", tmp_path)
    kilavuz_derin.birlestir()
    derin = kilavuz_ara.derin_tablo()
    assert derin({"ad": "a", "tur": "ajan"})["nasil"] == "v" and derin({"ad": "a", "tur": "skill"}) is None


def test_tarif_bul_ortak_kelime(tmp_path):
    (tmp_path / "eticaret.md").write_text("# E-ticaret sitesi tarifi\n", encoding="utf8")
    (tmp_path / "oyun.md").write_text("# Oyun tarifi\n", encoding="utf8")
    assert kilavuz_ara.tarif_bul("oyun yap", tmp_path).name == "oyun.md"
    assert kilavuz_ara.tarif_bul("zzz", tmp_path) is None


def test_uygula_duzeltir_ve_dogrulanmadi_isaretler(tmp_path, monkeypatch, capsys):
    (tmp_path / "cikti").mkdir()
    (tmp_path / "ornek").mkdir()
    alan = {a: "x" for a in kilavuz_derin.ALAN}
    (tmp_path / "cikti" / "p001-t.jsonl").write_text(json.dumps({"ad": "a", "tur": "skill", **alan}) + "\n", encoding="utf8")
    (tmp_path / "ornek" / "g.aralik").write_text("1", encoding="utf8")
    karar = tmp_path / "k.jsonl"
    karar.write_text(json.dumps({"ad": "a", "tur": "skill", "yanlis": ["nasil"], "uydurma": ["tuzak"], "duzelt": {"nasil": "dogru"}}), encoding="utf8")
    monkeypatch.setattr(kilavuz_derin, "IS", tmp_path)
    monkeypatch.setattr(kilavuz_ornek, "ORN", tmp_path / "ornek")
    kilavuz_ornek.uygula("g", karar)
    j = json.loads(open(tmp_path / "cikti" / "p001-t.jsonl", encoding="utf8").read())
    assert (j["nasil"], j["tuzak"], j["dogrulandi"]) == ("dogru", "?", False)
    assert f"1:{1 - 2 / len(kilavuz_derin.ALAN):.2f}" in capsys.readouterr().out
    assert json.loads((tmp_path / "ornek" / "dogruluk.json").read_text(encoding="utf8")) == {"1": round(1 - 2 / len(kilavuz_derin.ALAN), 3)}


def test_birlestir_dusuk_ve_orneklemsiz_taslagi_disla(tmp_path, monkeypatch, capsys):
    (tmp_path / "cikti").mkdir()
    (tmp_path / "ornek").mkdir()
    (tmp_path / "tekil.tsv").write_text("ad\ttur\taile\tsha\ttemsilci\tbayt\tyol\n"
                                        + "".join(f"{a}\tskill\tx\t1\t{a}\t5\t\n" for a in "abc"), encoding="utf8")
    for no, ad in ((1, "a"), (2, "b"), (3, "c")):
        (tmp_path / "cikti" / f"p00{no}-t.jsonl").write_text(json.dumps({"ad": ad, "tur": "skill", **{k: "v" for k in kilavuz_derin.ALAN}}) + "\n", encoding="utf8")
    (tmp_path / "ornek" / "dogruluk.json").write_text(json.dumps({"1": 0.9, "2": 0.84}), encoding="utf8")
    monkeypatch.setattr(kilavuz_derin, "KAT", tmp_path)
    monkeypatch.setattr(kilavuz_derin, "IS", tmp_path)
    kilavuz_derin.birlestir()
    assert [json.loads(s)["ad"] for s in open(tmp_path / "derin.jsonl", encoding="utf8")] == ["a"]
    assert "dışlanan parti 2" in capsys.readouterr().out
