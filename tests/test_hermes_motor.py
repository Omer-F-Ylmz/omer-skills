"""HERMES-KUR-1 PARÇA 5c: ajan-sira.tsv motor=hermes → claude -p yerine tools/hermes_motor.py (hermes chat -Q -q, ücretsiz model, $0)."""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / ".kos/kopru"))  # ajan_sira → maliyet_defter
sys.path.insert(0, str(KOK / "tools"))
_s = importlib.util.spec_from_file_location("ajan_sira", KOK / ".kos/kopru/ajan_sira.py")
ajan_sira = importlib.util.module_from_spec(_s)
_s.loader.exec_module(ajan_sira)
import hermes_motor


def test_kuyruk_motor_hermes(tmp_path, monkeypatch):
    tsv = tmp_path / "k.tsv"
    tsv.write_text("a\ti.md\t\tmotor=hermes\nb\ti.md\t\tmotor=ucretsiz\nc\ti.md\n", encoding="utf-8")
    monkeypatch.setattr(ajan_sira, "KUYRUK", tsv)
    assert ajan_sira.kuyruk() == [("a", "i.md", "", "", "hermes", 0, None), ("b", "i.md", "", "", None, 0, None), ("c", "i.md", "", "", None, None, None)]


def test_baslat_argv_hermes_claude_degil():
    argv, env = ajan_sira.baslat_argv("", "hermes")
    assert argv[-1].endswith("hermes_motor.py") and "claude" not in " ".join(argv).lower()
    assert "ANTHROPIC_API_KEY" not in env


def test_sonuc_json_basari_ve_bos():
    j = json.loads(hermes_motor.sonuc_json(0, "HERMES-OK rapor yazıldı"))
    assert (j["subtype"], j["total_cost_usd"], j["num_turns"]) == ("success", 0, 2) and "HERMES-OK" in j["result"]
    assert json.loads(hermes_motor.sonuc_json(0, "  "))["subtype"] != "success"  # boş çıktı başarı değil
    assert json.loads(hermes_motor.sonuc_json(1, "hata"))["subtype"] != "success"


def test_motor_uctan_uca_sahte_hermes(tmp_path):
    """Sahte hermes (python betiği): istem dosyası yolunu alır, içeriğini yankılar → sarmalayıcı tek JSON satırı basar."""
    sahte = tmp_path / "hermes.py"
    sahte.write_text("import sys;q=sys.argv[sys.argv.index('-q')+1];print('YANIT \\u2502 '+q.split()[-1][-12:])", encoding="utf-8")  # │ cp1254 konsolda basılamaz (gerçek koşuda yakalanan hata)
    r = subprocess.run([sys.executable, "-I", str(KOK / "tools/hermes_motor.py"), "--session-id", "x"], input="görev metni".encode(),
                       capture_output=True, env={"HERMES_KOMUT": f"{sys.executable} {sahte}", "SystemRoot": "C:\\Windows"}, timeout=60)
    j = json.loads(r.stdout.decode().strip().splitlines()[-1])
    assert r.returncode == 0 and j["subtype"] == "success" and j["result"].startswith("YANIT")
