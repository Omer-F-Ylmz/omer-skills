"""ARKA-BEKCI-1: arka.py kaydı + tools/arka_bekci.py ölü iş / askı yakalama (gerçek alt süreçlerle)."""
import importlib.util
import json
import subprocess
import sys
import time
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
ARKA = KOK / ".kos/kopru/arka.py"


def _bekci(monkeypatch, tmp_path):
    monkeypatch.setenv("ARKA_KOPRU", str(tmp_path))
    monkeypatch.setenv("ARKA_KAYIT", str(tmp_path / "kayit.json"))
    spec = importlib.util.spec_from_file_location("arka_bekci_t", KOK / "tools/arka_bekci.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _baslat(tmp_path, kod, *bayrak):
    betik = tmp_path / "is.py"
    betik.write_text(kod, encoding="utf-8")
    r = subprocess.run([sys.executable, str(ARKA), *bayrak, "--cwd", str(tmp_path), str(tmp_path / "is.log"), str(betik)],
                       capture_output=True, text=True, creationflags=0x08000000, timeout=60)
    assert r.returncode == 0, r.stdout + r.stderr
    k = json.loads((tmp_path / "kayit.json").read_text(encoding="utf-8"))
    return betik, k


def _bekle(m, pid):
    for _ in range(40):
        if m.olusturma(pid) is None:
            return
        time.sleep(0.25)
    raise AssertionError("süreç ölmedi")


def test_olu_is_alarm_ve_tek_yeniden(monkeypatch, tmp_path):
    m = _bekci(monkeypatch, tmp_path)
    _, k = _baslat(tmp_path, "print('yarim')\n", "--yeniden")
    (ad, e), = k.items()
    assert e["yeniden"] and e["durum"] == "calisiyor" and e["pid"]
    _bekle(m, e["pid"])
    olay = m.tara()
    assert (ad, "oldu") in olay and (ad, "yeniden") in olay
    assert "bitiş işareti yazmadan öldü" in (tmp_path / "beyin-alarm.txt").read_text(encoding="utf-8")
    assert json.loads((tmp_path / "beyin-olay.jsonl").read_text(encoding="utf-8").splitlines()[0])["hata"] is True
    k2 = json.loads((tmp_path / "kayit.json").read_text(encoding="utf-8"))
    assert len(k2) == 2 and k2[ad]["durum"] == "oldu" and k2[ad]["yeniden_say"] == 1  # yeniden başlatma yeni kayıt açtı
    yeni = next(a for a in k2 if a != ad)
    assert k2[yeni]["bagimsiz"] and not k2[yeni]["yeniden"]
    for _ in range(60):  # yeni iş de (bitiş işaretsiz) ölünce bir daha yeniden başlatılmaz
        time.sleep(0.5)
        olay2 = m.tara()
        if (yeni, "oldu") in olay2:
            break
    assert (yeni, "oldu") in olay2 and (yeni, "yeniden") not in olay2
    assert len(json.loads((tmp_path / "kayit.json").read_text(encoding="utf-8"))) == 2


def test_biten_is_alarmsiz(monkeypatch, tmp_path):
    m = _bekci(monkeypatch, tmp_path)
    _, k = _baslat(tmp_path, "print('BITTI 3')\n")
    (ad, e), = k.items()
    _bekle(m, e["pid"])
    assert m.tara() == [(ad, "bitti")]
    assert not (tmp_path / "beyin-alarm.txt").exists()


def test_aski_uyarisi_bir_kez(monkeypatch, tmp_path):
    m = _bekci(monkeypatch, tmp_path)
    _, k = _baslat(tmp_path, "import time\ntime.sleep(60)\n")
    (ad, e), = k.items()
    try:
        assert m.tara(simdi=time.time() + 25 * 60) == [(ad, "askida")]
        assert m.tara(simdi=time.time() + 26 * 60) == []
        assert "askıda" in (tmp_path / "beyin-alarm.txt").read_text(encoding="utf-8")
    finally:
        subprocess.run(["taskkill", "/F", "/PID", str(e["pid"])], capture_output=True, creationflags=0x08000000)
