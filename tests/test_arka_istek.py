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


def _istek_baslat(tmp_path, kod):
    betik = tmp_path / "uzun.py"
    betik.write_text(kod, encoding="utf-8")
    klasor = tmp_path / "istek"
    klasor.mkdir()
    (klasor / "is1.json").write_text(json.dumps({"komut": [str(betik)], "gunluk": str(tmp_path / "uzun.log")}), encoding="utf-8")
    kayit = []
    arka_istek.isle(klasor, log=lambda *a: kayit.append(a))
    return klasor, kayit, json.loads((klasor / "is1.json").read_text(encoding="utf-8"))


def test_olen_is_bitissiz_yeniden_baslar(tmp_path):
    """Oturum job'ı kapanınca süreç ağacı BITIS yazmadan ölür → yönetici bir sonraki döngüde yeniden başlatır."""
    klasor, kayit, d = _istek_baslat(tmp_path, "import time\nprint('BASLADI', flush=True)\ntime.sleep(25)\n")
    ilk = d["pid"]
    yeni = None
    try:
        subprocess.run(["taskkill", "/T", "/F", "/PID", str(ilk)], capture_output=True)
        time.sleep(1)
        arka_istek.isle(klasor, log=lambda *a: kayit.append(a))
        yeni = json.loads((klasor / "is1.json").read_text(encoding="utf-8"))
        assert yeni["pid"] != ilk and yeni["yeniden"] == 1
        assert any(k[0] == "ARKA-YENIDEN" for k in kayit)
    finally:
        if yeni:
            subprocess.run(["taskkill", "/T", "/F", "/PID", str(yeni["pid"])], capture_output=True)


def test_bitis_yazan_is_yeniden_baslamaz(tmp_path):
    klasor, kayit, d = _istek_baslat(tmp_path, "print('BITIS islenen=0', flush=True)\n")
    time.sleep(2)
    arka_istek.isle(klasor, log=lambda *a: kayit.append(a))
    son = json.loads((klasor / "is1.json").read_text(encoding="utf-8"))
    assert son["pid"] == d["pid"] and "yeniden" not in son
