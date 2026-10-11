import re
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import ajan_getir_zip as az  # noqa: E402


def _skill(tmp_path, ajanlar):
    sk = tmp_path / "skill"
    sk.mkdir()
    (sk / "SKILL.md").write_text("---\nname: ajan-getir\ndescription: d\n---\n", encoding="utf-8")
    satir = ["ad\tmodel\ttek_satir\tyol"]
    for i, (ad, govde) in enumerate(ajanlar):
        a = tmp_path / f"a{i}.md"
        a.write_bytes(govde.encode("utf-8"))
        satir.append(f"{ad}\tsonnet\tt\t{a.as_posix()}")
    (sk / "katalog.tsv").write_text("\n".join(satir) + "\n", encoding="utf-8")
    return sk


def _bolum(z, yol):
    # claude.ai tarafının yapacağı okuma: dosya#Lbas-bit → yalnız o satırlar
    m = re.fullmatch(r"(references/ajanlar/[a-z0-9._-]+\.md)#L(\d+)-(\d+)", yol)
    assert m, yol
    satirlar = z.read("ajan-getir/" + m.group(1)).decode("utf-8").split("\n")
    return "\n".join(satirlar[int(m.group(2)) - 1:int(m.group(3))])


def test_istemler_gruplu_dosyaya_gomulur_satir_araligi_dogru(tmp_path):
    ajanlar = [("octo:droids:Code Reviewer", "---\nname: Code Reviewer\n---\ngövde 1\n"),
               ("octo:debugger", "﻿---\r\nname: d\r\n---\r\ngövde 2\r\n"),  # BOM + CRLF normalize edilir
               ("Database Optimizer", "---\nname: Database Optimizer\n---\ngövde 3\n")]
    zp = az.paketle(_skill(tmp_path, ajanlar), tmp_path / "out.zip")
    with zipfile.ZipFile(zp) as z:
        adlar = z.namelist()
        assert sorted(adlar) == ["ajan-getir/SKILL.md", "ajan-getir/katalog.tsv",
                                 "ajan-getir/references/ajanlar/kullanici.md", "ajan-getir/references/ajanlar/octo.md"]
        kat = [s.split("\t") for s in z.read("ajan-getir/katalog.tsv").decode().splitlines()[1:]]
        for (ad, govde), (kad, _, _, yol) in zip(ajanlar, kat):
            assert kad == ad
            assert _bolum(z, yol) == govde.lstrip("﻿").replace("\r\n", "\n").rstrip("\n")


def test_buyuk_grup_parcalara_bolunur(tmp_path, monkeypatch):
    monkeypatch.setattr(az, "EN_BUYUK_BAYT", 100)
    ajanlar = [(f"ecc:a{i}", f"---\nname: a{i}\n---\n" + "x" * 60 + f"\nrol {i}\n") for i in range(5)]
    zp = az.paketle(_skill(tmp_path, ajanlar), tmp_path / "out.zip")
    with zipfile.ZipFile(zp) as z:
        assert {"ajan-getir/references/ajanlar/ecc.md", "ajan-getir/references/ajanlar/ecc-2.md"} <= set(z.namelist())
        kat = [s.split("\t") for s in z.read("ajan-getir/katalog.tsv").decode().splitlines()[1:]]
        assert all(_bolum(z, k[3]).endswith(f"rol {i}") for i, k in enumerate(kat))


def test_cok_plugin_200_dosya_sinirini_asmaz(tmp_path):
    # 17:54: claude.ai 286 dosyalı zip'i "maximum 200" ile reddetti; grup sayısı patlarsa harfe göre kovalanır
    ajanlar = [(f"p{i}:ajan", f"---\nname: a{i}\n---\nrol {i}\n") for i in range(250)]
    zp = az.paketle(_skill(tmp_path, ajanlar), tmp_path / "out.zip")
    with zipfile.ZipFile(zp) as z:
        assert len(z.namelist()) <= 200
        kat = [s.split("\t") for s in z.read("ajan-getir/katalog.tsv").decode().splitlines()[1:]]
        assert _bolum(z, kat[137][3]).endswith("rol 137")
