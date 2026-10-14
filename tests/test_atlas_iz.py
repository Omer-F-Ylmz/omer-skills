import json, subprocess, sys, time
from pathlib import Path

BETIK = Path(__file__).resolve().parents[1] / ".kos" / "kopru" / "atlas_iz.py"


def test_varsayilan_arac_oturumda_sayilir(tmp_path):
    satir = lambda girdi: json.dumps({"message": {"content": [{"type": "tool_use", "name": "Bash", "input": girdi}]}})
    (tmp_path / "a.jsonl").write_text(satir({"command": "gitleaks detect --source ."}) + "\n", encoding="utf-8")
    (tmp_path / "b.jsonl").write_text(satir({"command": "semgrep-desktop x"}) + "\nbozuk{\n", encoding="utf-8")
    c = subprocess.run([sys.executable, str(BETIK), "guvenlik-test", "--proje", str(tmp_path)],
                       capture_output=True, encoding="utf-8", check=True).stdout
    assert "kullanan oturum 1" in c
    assert "   1  gitleaks" in c
    assert "   0  semgrep" in c  # semgrep-desktop asıl adı saymaz
