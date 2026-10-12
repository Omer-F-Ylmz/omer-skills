"""BLENDER-1-devam-5: claude.ai zip'leri yerel yola bağlı değil, zip_denetle temiz, tarif.py zipten tek başına koşar."""
import json
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "tools"))
sys.path.insert(0, str(KOK / "tools" / "blender"))
sys.path.insert(0, str(KOK / "tools" / "skill-paket"))
import blender_oturum as bo  # noqa: E402
import claude_ai_zip  # noqa: E402
import zip_denetle  # noqa: E402


@pytest.fixture(scope="module")
def zipler(tmp_path_factory):
    return claude_ai_zip.paketle(tmp_path_factory.mktemp("dist"))


def test_zipler_temiz_ve_yerel_yolsuz(zipler):
    assert sorted(z.name for z in zipler) == ["blender-oturum.zip", "blender-uretim.zip"]
    for zp in zipler:
        assert zip_denetle.denetle(zp) == []
        with zipfile.ZipFile(zp) as z:
            for ad in z.namelist():
                veri = z.read(ad)
                assert b"C:/Projeler" not in veri and b"C:\\Projeler" not in veri and b"C:\\Users" not in veri, ad
    with zipfile.ZipFile(zipler[1]) as z:
        assert "blender-uretim/references/tarif.py" in z.namelist()


@pytest.mark.skipif(not Path(bo.BLENDER).is_file(), reason="Blender exe yok")
def test_zipteki_tarif_tek_basina_kosar(zipler, tmp_path):
    zipfile.ZipFile(zipler[1]).extractall(tmp_path)
    spec = tmp_path / "s.json"
    spec.write_text(json.dumps({"nesneler": [{"ad": "Kup", "tur": "kup", "boyut": [0.1, 0.1, 0.1],
                                             "malzeme": "seramik_sirli"}], "isik": "urun", "ozet": ["ad"]}),
                    encoding="utf-8")
    r = subprocess.run([bo.BLENDER, "-b", "--factory-startup", "-P",
                        str(tmp_path / "blender-uretim" / "references" / "tarif.py"), "--", "@" + str(spec)],
                       capture_output=True, encoding="utf-8", errors="replace", timeout=300)
    satir = [s for s in r.stdout.splitlines() if s.startswith("SONUC:")]
    assert satir, r.stdout[-800:] + r.stderr[-800:]
    assert [n["ad"] for n in json.loads(satir[0][6:])["ozet"]] == ["Kup"]
