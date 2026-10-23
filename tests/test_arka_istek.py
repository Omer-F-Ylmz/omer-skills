"""ARKA-KALICI-1: istek dosyası → yönetici arka.py ile başlatır, pid yazar, ikinci kez başlatmaz; isteyen süreç bitse de iş yaşar."""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

KOPRU = Path(__file__).resolve().parents[1] / ".kos/kopru"
sys.path.insert(0, str(KOPRU))
import arka_istek  # noqa: E402


def _canli(pid):
    r = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH"], capture_output=True, text=True)
    return str(pid) in r.stdout


def test_istek_baslar_pid_yazar_tekrar_baslatmaz(tmp_path):
    betik = tmp_path / "uzun.py"
    betik.write_text("import time\nprint('BASLADI', flush=True)\ntime.sleep(25)\nprint('BITIS')\n", encoding="utf-8")
    gunluk = tmp_path / "uzun.log"
    klasor = tmp_path / "istek"
    klasor.mkdir()
    # isteyen "ajan": isteği yazar ve hemen çıkar
    subprocess.run([sys.executable, "-c",
                    f"import json;json.dump({{'komut':[r'{betik}'],'gunluk':r'{gunluk}'}},open(r'{klasor / 'is1.json'}','w'))"], check=True)
    kayit = []
    arka_istek.isle(klasor, log=lambda *a: kayit.append(a))
    d = json.loads((klasor / "is1.json").read_text(encoding="utf-8"))
    pid = d["pid"]
    try:
        time.sleep(1.5)
        assert _canli(pid)
        assert "BASLADI" in gunluk.read_text(encoding="utf-8")
        arka_istek.isle(klasor, log=lambda *a: kayit.append(a))  # ikinci döngü: yeni süreç yok
        assert json.loads((klasor / "is1.json").read_text(encoding="utf-8"))["pid"] == pid
        assert len(kayit) == 1
    finally:
        subprocess.run(["taskkill", "/T", "/F", "/PID", str(pid)], capture_output=True)


def test_gecersiz_istek_hata_yazar_baslatmaz(tmp_path):
    (tmp_path / "kotu.json").write_text(json.dumps({"komut": []}), encoding="utf-8")
    arka_istek.isle(tmp_path, log=lambda *a: None)
    d = json.loads((tmp_path / "kotu.json").read_text(encoding="utf-8"))
    assert "hata" in d and "pid" not in d
