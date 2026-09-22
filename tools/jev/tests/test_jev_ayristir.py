import json
from pathlib import Path

from jev import ayristir as a

F = Path(__file__).parent / "fixtures"


def test_dotnet_konsol_hata_sayisi():
    h = a.log_hatalari((F / "dotnet-konsol.txt").read_text(encoding="utf-8"))
    adlar = [x["ad"] for x in h]
    # 3 test (2 VSTest + 1 MTP) + 1 benzersiz derleme hatası (MSBuild özette tekrarlar); uyarı ve özet satırı sayılmaz.
    assert len(h) == 4
    assert "App.Tests.SiparisTests.Toplam_dogru" in adlar and "App.Tests.IadeTests.Iade_reddi" in adlar
    assert any("CS0103" in x for x in adlar)
    toplam = next(x for x in h if x["ad"].endswith("Toplam_dogru"))
    assert "Expected: 10" in toplam["metin"]


def test_trx_hata_sayisi():
    h = a.log_hatalari((F / "sonuc.trx").read_text(encoding="utf-8"))
    assert [x["ad"] for x in h] == ["App.Tests.SiparisTests.Toplam_dogru", "App.Tests.KargoTests.Zaman_asimi"]
    assert "Assert.Equal" in h[0]["metin"]


def test_pytest_hata_sayisi():
    h = a.log_hatalari((F / "pytest.txt").read_text(encoding="utf-8"))
    assert [x["ad"] for x in h] == ["tests/test_a.py::test_x", "tests/test_b.py::test_y", "tests/test_a.py::test_db"]
    assert "ModuleNotFoundError" in h[1]["metin"]


def test_ilgili_py_fonksiyon_sinirinda_boler():
    satirlar = ["x = 1"] * 150
    satirlar[0], satirlar[49], satirlar[99] = "def a():", "def b():", "class C:"
    assert a.parcala_dosya("m.py", "\n".join(satirlar)) == [(1, 49), (50, 99), (100, 150)]


def test_ilgili_cs_ve_ts_siniri():
    cs = ["// x"] * 120
    cs[59] = "    public async Task<int> Hesapla(int a)"
    assert a.parcala_dosya("A.cs", "\n".join(cs))[0] == (1, 59)
    ts = ["let x = 1;"] * 120
    ts[69] = "export function hesapla() {"
    assert a.parcala_dosya("a.ts", "\n".join(ts))[0] == (1, 69)


def test_ilgili_sinirsiz_dosya_satirla_boler():
    assert a.parcala_dosya("n.txt", "\n".join(["z"] * 200)) == [(1, 80), (81, 160), (161, 200)]


def test_kanit_madde_ayirma():
    d = a.iddialar((F / "rapor.md").read_text(encoding="utf-8"))
    assert [n for n, _ in d] == [3, 4, 6, 7, 9]
    assert d[0][1] == "Commit abc1234 pushlandı."
    assert d[2][1] == "gitleaks 0 sızıntı."


GIZLI = "hunter2-" + "gizli-deger"


def gitleaks_kaydi():
    return [
        {
            "RuleID": "generic-api-key",
            "Description": "Detected a Generic API Key",
            "File": "src/ayar.py",
            "StartLine": 7,
            "Secret": GIZLI,
            "Match": f"sifre = {GIZLI}",
            "Line": f"    sifre = {GIZLI}  # eski",
            "Commit": "abc",
            "Email": "dev@ornek.com",
        }
    ]


def test_gitleaks_secret_match_line_statee_girmez():
    b = a.bulgular(gitleaks_kaydi())
    assert len(b) == 1 and b[0]["kural"] == "generic-api-key" and b[0]["dosya"] == "src/ayar.py" and b[0]["satir"] == 7
    assert GIZLI not in b[0]["state"] and "sifre" not in b[0]["state"]
    assert "dev@ornek.com" not in b[0]["state"]


def test_semgrep_eslesen_satir_statee_girmez():
    veri = {"results": [{"check_id": "py.hardcoded", "path": "a.py", "start": {"line": 3},
                         "extra": {"message": "Sabit parola", "severity": "ERROR", "lines": f"p = '{GIZLI}'",
                                   "metavars": {"$X": {"abstract_content": GIZLI}}}}]}
    b = a.bulgular(veri)
    assert b[0]["kural"] == "py.hardcoded" and b[0]["satir"] == 3
    assert GIZLI not in b[0]["state"] and "Sabit parola" in b[0]["state"]


def test_sarif_ve_axe():
    sarif = {"runs": [{"results": [{"ruleId": "CA2100", "message": {"text": "SQL enjeksiyon"},
                                    "locations": [{"physicalLocation": {"artifactLocation": {"uri": "Db.cs"}, "region": {"startLine": 12}}}]}]}]}
    assert a.bulgular(sarif)[0] | {"state": ""} == {"kural": "CA2100", "dosya": "Db.cs", "satir": 12, "state": ""}
    axe = {"url": "http://localhost/", "violations": [{"id": "color-contrast", "impact": "serious", "help": "Kontrast", "nodes": [{}, {}]}]}
    b = a.bulgular(axe)
    assert b[0]["kural"] == "color-contrast" and "serious" in b[0]["state"]
