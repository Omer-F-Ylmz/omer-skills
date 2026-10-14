import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parents[1] / "tools"))
import cc_profil  # noqa: E402
import token_4_uygula as t4  # noqa: E402


def test_uygula_geri_ve_cc_profil_tools(tmp_path):
    profil = tmp_path / "cc-arka.json"
    shutil.copy2(t4.KOK / "profiller" / "cc-arka.json", profil)
    once = profil.read_bytes()
    assert t4.main(["uygula"], profil) == 0
    assert json.loads(profil.read_bytes())["ajan"]["araclar"] == t4.ARACLAR
    args, _ = cc_profil.kur("ajan", env={}, profiller=profil, gecici=tmp_path / "g")
    assert args[args.index("--tools") + 1] == ",".join(t4.ARACLAR)
    assert t4.main(["uygula"], profil) == 1  # ikinci kez eklemez
    assert t4.main(["--geri"], profil) == 0
    assert profil.read_bytes() == once
