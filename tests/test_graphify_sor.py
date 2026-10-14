"""GRAPHIFY-ULTRA-1: graphify_sor.py — sentetik graf + git deposunda sıralama ve git grep yedeği (canlı graf gerekmez)."""
import json, subprocess, sys
from pathlib import Path

SOR = Path(__file__).resolve().parents[1] / ".kos/kopru/graphify_sor.py"


def _kur(tmp_path):
    dugum = [{"id": f"f{i}", "label": "fincan.js", "source_file": y, "source_location": "L1"}
             for i, y in enumerate(["docs/r1/_ham/a/b/fincan.js", "docs/r1/_ham/c/fincan.js", "src/sahne/fincan.js", "x/fincan.js"])]
    (tmp_path / "graphify-out").mkdir()
    (tmp_path / "graphify-out/graph.json").write_text(json.dumps({"nodes": dugum, "links": []}), encoding="utf-8")
    (tmp_path / "kayit.py").write_text("import winreg\nv = winreg.QueryValueEx(k, 'a')\n", encoding="utf-8")
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "add", "kayit.py"], cwd=tmp_path, check=True)


def _sor(tmp_path, soru):
    return subprocess.run([sys.executable, str(SOR), soru, "--kok", str(tmp_path)], capture_output=True,
                          text=True, encoding="utf-8").stdout.splitlines()


def test_soruda_gecen_yol_once(tmp_path):
    _kur(tmp_path)
    assert _sor(tmp_path, "src/sahne/fincan.js ne yapar")[0] == "fincan.js · src/sahne/fincan.js:L1"


def test_sig_yol_kopyalardan_once(tmp_path):
    _kur(tmp_path)
    s = _sor(tmp_path, "fincan.js ne yapar")
    assert [x.split(" · ")[1] for x in s] == ["x/fincan.js:L1", "src/sahne/fincan.js:L1", "docs/r1/_ham/c/fincan.js:L1"]


def test_dis_sembol_cagri_yerine_duser(tmp_path):
    _kur(tmp_path)
    assert _sor(tmp_path, "QueryValueEx fonksiyonunu kim çağırıyor") == ["grep: kayit.py:2:v = winreg.QueryValueEx(k, 'a')"]
