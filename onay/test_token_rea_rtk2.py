import importlib.util
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import token_rea_rtk2 as t  # noqa: E402


def test_yama_rota_ve_geri(tmp_path):
    kok = tmp_path / "k"
    (kok / "tools").mkdir(parents=True)
    (kok / ".kos/kopru/token-rea").mkdir(parents=True)
    shutil.copy(t.KOK / ".kos/kopru/token-rea/rtk2.py", kok / ".kos/kopru/token-rea/rtk2.py")
    dosya = kok / "tools" / "rtk_onisle.py"
    orijinal = (t.KOK / "tools" / "rtk_onisle.py").read_bytes()
    dosya.write_bytes(orijinal)
    t.main(["uygula"], dosya); t.main(["uygula"], dosya)
    assert dosya.read_bytes().count(t.ISARET.encode()) == 2  # fonksiyon + main, ikinci uygula etkisiz
    s = importlib.util.spec_from_file_location("ro", dosya); m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
    assert m.rtk2_yaz("ls -la tools").startswith("python -I -S ") and m.rtk2_yaz("git diff HEAD~2").endswith("git diff HEAD~2")
    assert m.rtk2_yaz("git status").endswith("git status")
    assert m.rtk2_yaz("git log -3") is None and m.rtk2_yaz("find . -name x") is None and m.rtk2_yaz("ls | head") is None
    t.main(["--geri"], dosya)
    assert dosya.read_bytes() == orijinal
