"""YÖNETİCİ-BAĞIMSIZ-1: job üyeliği testi (d1) + ölen işi kurtarma (d3)."""
import ctypes
import importlib.util
import json
import os
import subprocess
import sys
import time
from ctypes import wintypes
from pathlib import Path

import pytest

KOPRU = Path(__file__).resolve().parents[1] / ".kos/kopru"
sys.path.insert(0, str(KOPRU))
_s = importlib.util.spec_from_file_location("ajan_sira", KOPRU / "ajan_sira.py")
ajan_sira = importlib.util.module_from_spec(_s)
_s.loader.exec_module(ajan_sira)
import job_uyelik

SONUC = json.dumps({"type": "result", "subtype": "success", "session_id": "x"})
SID = "11111111-2222-4333-8444-555555555555"


def test_job_uyelik_atanan_surec_job_icinde():
    k32 = ctypes.windll.kernel32
    k32.CreateJobObjectW.restype = wintypes.HANDLE
    k32.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
    job = k32.CreateJobObjectW(None, None)
    p = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(30)"], creationflags=0x08000000)
    try:
        k32.AssignProcessToJobObject(job, wintypes.HANDLE(int(p._handle)))  # atama reddedilirse süreç zaten başka job'dadır
        assert job_uyelik.job_icinde(p.pid) is True
    finally:
        p.kill()
        k32.CloseHandle(wintypes.HANDLE(job))
    assert job_uyelik.job_icinde(2**22 - 4) is None  # olmayan pid


@pytest.fixture
def cikti(tmp_path, monkeypatch):
    monkeypatch.setattr(ajan_sira, "CIKTI", tmp_path)
    monkeypatch.setattr(ajan_sira, "git_var", lambda ad: False)  # kısa test adları gerçek git log'daki sözcüklerle eşleşmesin
    return tmp_path


def _is(cikti, ad, *, basladi=f"10:00:00 pid 999999 sid {SID}", sonuc=None, yas=0):
    b = cikti / f"{ad}.basladi"
    b.write_text(basladi, encoding="utf-8")
    t = time.time() - yas
    os.utime(b, (t, t))
    if sonuc is not None:
        (cikti / f"{ad}.json").write_text(sonuc, encoding="utf-8")


def _satir(*adlar):
    return [(a, f"{a}.md") for a in adlar]  # kuyruk() satırı: (ad, görev dosyası)


def test_olu_is_kurtarilir_sonuclu_yasli_kuyrukdisi_kurtarilmaz(cikti, capsys):
    _is(cikti, "olu", sonuc="")  # json boş: claude -p sonucu sonda yazar, öldürülünce boş kalır
    _is(cikti, "bitmis", sonuc=SONUC)
    _is(cikti, "eski", sonuc="", yas=3 * 86400)
    _is(cikti, "kuyrukta-degil", sonuc="")
    _is(cikti, "iki-kez", sonuc="")
    (cikti / "iki-kez.kurtar").write_text("2")
    baslayan = {"olu", "bitmis", "eski", "kuyrukta-degil", "iki-kez"}
    devam = ajan_sira.kurtar(_satir("olu", "bitmis", "eski", "iki-kez"), baslayan)
    assert list(devam) == ["olu"]
    assert baslayan == {"bitmis", "eski", "kuyrukta-degil", "iki-kez"}  # yalnız kurtarılan yeniden sıraya girer
    assert (cikti / "olu.kurtar").read_text() == "1"
    assert "KURTAR olu" in capsys.readouterr().out


def test_kurtar_session_id_transkript_varsa_resume_yoksa_bastan(cikti, tmp_path, monkeypatch):
    kok = tmp_path / "ev"
    (kok / ".claude/projects/p").mkdir(parents=True)
    (kok / ".claude/projects/p" / f"{SID}.jsonl").write_text("{}")
    monkeypatch.setattr(Path, "home", lambda: kok)
    _is(cikti, "var", sonuc="")
    _is(cikti, "yok", sonuc="", basladi="10:00:00 pid 999999 sid 99999999-2222-4333-8444-555555555555")
    _is(cikti, "sidsiz", sonuc="", basladi="10:00:00 pid 999999")
    devam = ajan_sira.kurtar(_satir("var", "yok", "sidsiz"), {"var", "yok", "sidsiz"})
    assert devam == {"var": SID, "yok": None, "sidsiz": None}


def test_kurtar_tek_acilista_en_cok_3(cikti):
    adlar = [f"j{i}" for i in range(5)]
    for a in adlar:
        _is(cikti, a, sonuc="")
    assert len(ajan_sira.kurtar(_satir(*adlar), set(adlar))) == 3


def test_canli_claude_is_kurtarilmaz(cikti, monkeypatch):
    _is(cikti, "canli", sonuc="")
    monkeypatch.setattr(ajan_sira, "pid_canli", lambda p: True)
    monkeypatch.setattr(ajan_sira, "claude_sureci", lambda p, b: True)
    assert ajan_sira.kurtar(["canli"], {"canli"}) == {}
