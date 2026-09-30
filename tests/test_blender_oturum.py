"""BLENDER-OTURUM K1: tools/blender_oturum.py — subprocess/netstat taklitli."""
import json
import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import blender_oturum as bo  # noqa: E402

PID = 4242


def dinleme(adres, pid=PID):
    return f"  TCP    {adres}         0.0.0.0:0              LISTENING       {pid}\n"


class Sahte:
    """netstat/tasklist/taskkill ve Blender Popen taklidi."""

    def __init__(self, tmp, netstat="", sonra_netstat="", sonuc=None, canli=True):
        self.komutlar, self.popen = [], []
        self.netstat, self.sonra_netstat = netstat, sonra_netstat
        self.sonuc, self.canli, self.tmp = sonuc, canli, tmp

    def run(self, cmd, **_):
        self.komutlar.append(cmd)
        ad = cmd[0].lower()
        cikti = ""
        if ad == "netstat":
            cikti = self.netstat
        elif ad == "tasklist" and self.canli:
            cikti = f"blender.exe                  {PID} Console    1    700.000 K\n"
        return type("R", (), {"stdout": cikti, "returncode": 0})()

    def Popen(self, cmd, **_):
        self.popen.append(cmd)
        self.netstat = self.sonra_netstat
        if self.sonuc is not None:
            bo.SONUC.write_text(json.dumps(self.sonuc), encoding="utf-8")
        return type("P", (), {"pid": PID})()

    def oldurmeler(self):
        return [c for c in self.komutlar if c[0].lower() == "taskkill"]


@pytest.fixture
def ortam(tmp_path, monkeypatch):
    masa = tmp_path / "Desktop"
    (masa / "TELVE" / "Blender").mkdir(parents=True)
    (masa / "TELVE" / "baska").mkdir(parents=True)
    monkeypatch.setattr(bo, "MASAUSTU", masa)
    monkeypatch.setattr(bo, "DURUM", tmp_path / "durum.json")
    monkeypatch.setattr(bo, "SONUC", tmp_path / "sonuc.json")
    monkeypatch.setattr(bo.time, "sleep", lambda _s: None)
    return masa


def kur(monkeypatch, sahte):
    monkeypatch.setattr(bo.subprocess, "run", sahte.run)
    monkeypatch.setattr(bo.subprocess, "Popen", sahte.Popen)
    return sahte


def test_yol_siniri_disi_2(ortam, tmp_path, monkeypatch):
    s = kur(monkeypatch, Sahte(tmp_path))
    dis = ortam / "TELVE" / "baska" / "x.blend"
    dis.write_bytes(b"")
    assert bo.main(["ac", str(dis)]) == 2
    assert s.popen == []


def test_yeni_siz_olmayan_dosya_2(ortam, tmp_path, monkeypatch):
    s = kur(monkeypatch, Sahte(tmp_path))
    assert bo.main(["ac", str(ortam / "TELVE" / "Blender" / "yok.blend")]) == 2
    assert s.popen == []


def test_yeni_ve_var_olan_dosya_2(ortam, tmp_path, monkeypatch):
    s = kur(monkeypatch, Sahte(tmp_path))
    var = ortam / "TELVE" / "Blender" / "var.blend"
    var.write_bytes(b"x")
    assert bo.main(["ac", str(var), "--yeni"]) == 2
    assert s.popen == []
    assert var.read_bytes() == b"x"


def test_port_dolu_2(ortam, tmp_path, monkeypatch):
    s = kur(monkeypatch, Sahte(tmp_path, netstat=dinleme("127.0.0.1:9876", 999)))
    f = ortam / "TELVE" / "blender" / "a.blend"
    f.write_bytes(b"")
    assert bo.main(["ac", str(f)]) == 2
    assert s.popen == []


def test_host_127_degil_2_ve_pid_ile_kapatir(ortam, tmp_path, monkeypatch):
    s = kur(monkeypatch, Sahte(tmp_path, sonuc={"host": "0.0.0.0", "port": 9876}))
    f = ortam / "TELVE" / "Blender" / "a.blend"
    f.write_bytes(b"")
    assert bo.main(["ac", str(f)]) == 2
    assert s.oldurmeler() == [["taskkill", "/PID", str(PID), "/F"]]


def test_0000_dinleme_surec_kapatilir_1(ortam, tmp_path, monkeypatch):
    s = kur(monkeypatch, Sahte(tmp_path, sonra_netstat=dinleme("0.0.0.0:9876"),
                               sonuc={"host": "127.0.0.1", "port": 9876}))
    f = ortam / "TELVE" / "Blender" / "a.blend"
    f.write_bytes(b"")
    assert bo.main(["ac", str(f)]) == 1
    assert s.oldurmeler() == [["taskkill", "/PID", str(PID), "/F"]]
    assert not bo.DURUM.exists()


def test_kapat_yalniz_durum_pid_ad_ile_oldurme_yok(ortam, tmp_path, monkeypatch):
    s = kur(monkeypatch, Sahte(tmp_path, netstat=dinleme("127.0.0.1:9876")))
    f = ortam / "TELVE" / "Blender" / "a.blend"
    f.write_bytes(b"")
    bo.DURUM.write_text(json.dumps({"pid": PID, "dosya": str(f), "baslangic": 0}), encoding="utf-8")
    assert bo.main(["kapat"]) == 0
    assert s.oldurmeler() == [["taskkill", "/PID", str(PID), "/F"]]
    assert not any("/IM" in c for c in s.komutlar)


def test_calismiyorken_kapat_0(ortam, tmp_path, monkeypatch):
    s = kur(monkeypatch, Sahte(tmp_path, canli=False))
    assert bo.main(["kapat"]) == 0
    assert s.oldurmeler() == []
