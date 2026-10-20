import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import token_rea_hr2 as t  # noqa: E402

HR2 = t.KOK / ".kos/kopru/token-rea/hr2.py"


def test_onay_uygula_geri(tmp_path):
    ev, kok = tmp_path / "ev", tmp_path / "k"
    ev.mkdir(); kok.mkdir()
    (ev / "CLAUDE.md").write_bytes(b"a\r\n"); (kok / "CLAUDE.md").write_bytes(b"b\n")
    t.main(["uygula"], ev, kok); t.main(["uygula"], ev, kok)
    assert (kok / "CLAUDE.md").read_bytes().count(t.SATIR.encode()) == 1
    t.main(["--geri"], ev, kok)
    assert (ev / "CLAUDE.md").read_bytes() == b"a\r\n" and (kok / "CLAUDE.md").read_bytes() == b"b\n"


def test_cokert_igne_kalir_ve_geri_alinir():
    m = "\n".join(f"2026-10-20 10:00:{j % 60:02d} INFO adim {j} tamam" if j != 77 else "ERROR kritik_42 dosya yok" for j in range(300))
    o = subprocess.run([sys.executable, "-I", "-S", str(HR2)], input=m.encode(), capture_output=True).stdout.decode()
    assert "kritik_42" in o and len(o) < len(m) / 5 and "benzer satır" in o
    i = o.rsplit("ac ", 1)[1].strip()
    assert subprocess.run([sys.executable, "-I", "-S", str(HR2), "ac", i], capture_output=True).stdout.decode() == m
    assert subprocess.run([sys.executable, "-I", "-S", str(HR2)], input=b"kisa", capture_output=True).stdout == b"kisa"
