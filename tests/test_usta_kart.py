import json
import sys
import types
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import usta_kart as UK  # noqa: E402

KAYNAK = "Bu skill dosyalari okur. Komut: rtk read dosya. Tuzak: buyuk dosyayi tam okumak jeton yakar. Ipucu: aralik ver. " * 6


def test_grup_uret_nameerror_vermez(monkeypatch):
    grup = [{"ad": "x-skill", "tur": "skill"}]
    monkeypatch.setattr(UK, "kaynak", lambda k, lim=900: KAYNAK)
    cevap = json.dumps([{
        "ad": "x-skill", "kullanim": ["a", "b", "c"], "tuzak": "t", "token_ipucu": "i", "kombin": [],
        "ornek": "rtk read dosya", "kanit_tuzak": "", "kanit_token": "",
        "kanit_kullanim": ["Bu skill dosyalari okur.", "", ""]}])
    havuz = types.SimpleNamespace(cagir=lambda *a, **k: (cevap, "fake", []))
    monkeypatch.setitem(sys.modules, "ucretsiz_havuz", havuz)
    monkeypatch.setattr(UK, "ikinci_goz", lambda out, g: None)
    out, kol, _ = UK.grup_uret(grup)
    assert out[0]["ad"] == "x-skill" and out[0]["kullanim"]


def test_cli_yardim_ve_yasak(monkeypatch):
    assert "usage" in UK.cli_yardim(sys.executable).lower()
    assert UK.cli_yardim("husky") == "" and UK.cli_yardim("lefthook") == ""


def test_plugin_metin(tmp_path):
    (tmp_path / ".claude-plugin").mkdir()
    (tmp_path / ".claude-plugin/plugin.json").write_text('{"name":"p","description":"yararli"}', encoding="utf-8")
    (tmp_path / "README.md").write_text("# P\nnasil kullanilir", encoding="utf-8")
    t = UK.plugin_metin(tmp_path)
    assert "yararli" in t and "nasil kullanilir" in t


def test_kaynak_cli_zenginlesir(monkeypatch):
    k = {"ad": "x", "tur": "cli", "cagri": "Bash: " + sys.executable + " --help", "yol": "", "ne": "n"}
    monkeypatch.setattr(UK, "cli_yardim", lambda c, sure=20: "usage: x " * 60)
    assert len(UK.kaynak(k)) >= 400
