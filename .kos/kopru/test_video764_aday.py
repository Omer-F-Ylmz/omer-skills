import importlib.util, json
from pathlib import Path

_s = importlib.util.spec_from_file_location("aday", Path(__file__).with_name("video764_aday.py"))
A = importlib.util.module_from_spec(_s); _s.loader.exec_module(A)


def test_yaz_birlestirir_al_dogrulanmadi(tmp_path, monkeypatch):
    A.K.V2 = tmp_path / "v2.tsv"; A.HAM = tmp_path / "ham.json"; A.TSV = tmp_path / "a.tsv"
    A.K.V2.write_text("id\tlink\tbaşlık\teski karar\tkarar-v2\tgerekçe\tkanıt\tetiket\työntem\n" + "".join(
        f"{i}\tu{i}\tb\t\t{k}\tg\tk\t[karar-v2]\ttoplu\n" for i, k in (("a", "UYARLA"), ("b", "AL"), ("c", "UYARLA"), ("d", "ÖĞREN"))), encoding="utf-8")
    A.HAM.write_text(json.dumps({i: dict(id=i, ad=ad, tur="skill", kaynak="", ne="n", cc_cift="hayir", context="dusuk", token_hafiza="hayir", kategori="k")
                                 for i, ad in (("a", "Postiz"), ("b", "Postiz"), ("c", "Foo Bar"))}), encoding="utf-8")
    A.yaz(ad={"foo-bar-skill"})
    sat = [s.split("\t") for s in A.TSV.read_text(encoding="utf-8").splitlines()]
    assert len(sat) == 3 and sat[1][0] == "Postiz" and sat[1][11] == "2" and sat[1][14] == "evet" and sat[1][13] == "AL"  # a+b tek aday, AL doğrulanmadı
    assert sat[2][4].endswith("foo-bar-skill") and sat[1][4] == "yok"
