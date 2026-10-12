import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location("u", Path(__file__).resolve().parents[1] / "onay" / "mcp_hafif_1_uygula.py")
u = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(u)

ORNEK = (b"# yorum: web_dashboard_interface: app\r\nweb_dashboard: true\r\nweb_dashboard_open_on_launch: false\r\n"
         b"# arayuz\r\nweb_dashboard_interface:\r\ngui_log_window: false\r\n")


def test_kuru_uygula_geri(tmp_path):
    (tmp_path / ".serena").mkdir()
    p = tmp_path / ".serena" / "serena_config.yml"
    p.write_bytes(ORNEK)
    assert u.kuru(tmp_path) == [("web_dashboard_interface", "", "browser")]
    assert p.read_bytes() == ORNEK  # kuru yazmaz
    u.uygula(tmp_path)
    assert p.read_bytes() == ORNEK.replace(b"web_dashboard_interface:\r\n", b"web_dashboard_interface: browser\r\n")
    assert u.uygula(tmp_path) is None  # ikinci kez değişiklik yok, yedek yok
    u.geri(tmp_path)
    assert p.read_bytes() == ORNEK
