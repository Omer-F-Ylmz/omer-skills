"""KURTAR-FİX-1: arka.py --bagimsiz süreci Görev Zamanlayıcı'dan (Desktop/yönetici job'u dışında) başlatır."""
import subprocess
import sys
import time
from pathlib import Path

ARKA = Path(__file__).resolve().parents[1] / ".kos/kopru/arka.py"


def _ad(pid):
    ps = f"(Get-CimInstance Win32_Process -Filter 'ProcessId={pid}' | Select -First 1 | %{{ '{{0}} {{1}}' -f $_.Name,$_.ParentProcessId }})"
    c = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True, creationflags=0x08000000).stdout.split()
    return (c[0].lower(), int(c[1])) if len(c) == 2 else ("", 0)


def test_bagimsiz_atasi_gorev_zamanlayici(tmp_path):
    betik, iz = tmp_path / "iz.py", tmp_path / "iz.txt"
    betik.write_text(f"import os, time\nopen(r'{iz}', 'w').write(str(os.getpid()))\ntime.sleep(2)\n", encoding="utf-8")
    r = subprocess.run([sys.executable, str(ARKA), "--bagimsiz", str(tmp_path / "g.log"), str(betik)],
                       capture_output=True, text=True, creationflags=0x08000000, timeout=60)
    assert r.returncode == 0, r.stdout + r.stderr
    for _ in range(40):
        if iz.exists() and iz.read_text():
            break
        time.sleep(0.5)
    pid = int(iz.read_text())
    ad, ana = _ad(pid)
    assert ad.startswith("python")
    ana_ad, ata = _ad(ana)  # pythonw (arka --ic) → atası svchost (Zamanlayıcı), bu test süreci değil
    assert ana_ad == "pythonw.exe"
    assert _ad(ata)[0] == "svchost.exe"
