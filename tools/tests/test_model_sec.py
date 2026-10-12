import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import model_sec as ms  # noqa: E402


def test_model_dusurulmez_effort_siniftan():
    b = ms.bayraklar("mekanik", model="sonnet")
    assert b[:4] == ["--model", "sonnet", "--effort", "low"]
    assert "--safe-mode" in b and b[b.index("--tools") + 1] == ""
    assert ms.bayraklar("yargi")[3] == "high"


def test_geri_dusus_bir_ust_kademe_sonra_opus():
    assert ms.bayraklar("mekanik", kademe=1)[3] == "medium"
    b = ms.bayraklar("yargi", kademe=2)
    assert b[1] == "opus" and b[3] == "xhigh"


def test_ajan_yalniz_istenen_arac_safe_mode_yok():
    b = ms.bayraklar("ajan", arac=["Read", "Bash(git:*)"], mcp_config="{}")
    assert "--safe-mode" not in b
    assert b[b.index("--tools") + 1] == "Read,Bash"
    assert b[b.index("--mcp-config") + 1] == "{}"


def test_bayrak_varsayilan_kapali(monkeypatch):
    monkeypatch.delenv("ROUTER_1", raising=False)
    assert not ms.acik()
