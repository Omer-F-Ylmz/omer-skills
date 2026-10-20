"""KURULUM-V1 d2: onay/kurulum_v1_effortless.py — kuru / --kuru / --geri, CRLF korunur, sonradan değişen ayar geri alınmaz."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "onay"))
import kurulum_v1_effortless as e  # noqa: E402


def kur(tmp_path, monkeypatch, ham):
    h = tmp_path / "settings.json"
    h.write_bytes(ham)
    monkeypatch.setattr(e, "HEDEF", h)
    monkeypatch.setattr(e, "YEDEK", tmp_path / "s.bak")
    return h


def test_kuru_dosyaya_dokunmaz(tmp_path, monkeypatch):
    ham = b'{"model": "opus"}'
    h = kur(tmp_path, monkeypatch, ham)
    assert e.uygula("").startswith("kuru")
    assert h.read_bytes() == ham and not e.YEDEK.exists()


def test_kuru_sonra_geri_bayt_ayni_ve_crlf(tmp_path, monkeypatch):
    ham = b'{\r\n  "model": "opus"\r\n}'
    h = kur(tmp_path, monkeypatch, ham)
    assert e.uygula("--kuru").startswith("uygulandı")
    assert json.loads(h.read_bytes())["modelSettings"][e.MODEL]["effortLevel"] == e.SEVIYE
    assert b"\r\n" in h.read_bytes() and b"\n" not in h.read_bytes().replace(b"\r\n", b"")
    assert e.uygula("--kuru") == "zaten uygulanmış"
    assert e.uygula("--geri") == "geri alındı" and h.read_bytes() == ham


def test_geri_sonradan_degisen_ayari_reddeder(tmp_path, monkeypatch):
    h = kur(tmp_path, monkeypatch, b'{"model": "opus"}')
    e.uygula("--kuru")
    h.write_bytes(h.read_bytes() + b" ")
    assert "reddedildi" in e.uygula("--geri")
