import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from godmode_onsoz import enjekte  # noqa: E402

AJAN = "---\r\nname: x\r\n---\r\ngövde\r\n"


def test_enjekte_guncelle_geri(tmp_path):
    y = tmp_path / "x.md"
    y.write_bytes(AJAN.encode())
    assert enjekte(y, "v1", kuru=True) and y.read_bytes().decode() == AJAN  # kuru yazmaz
    assert enjekte(y, 'v1 {ad} {"json": 1}')
    m = y.read_bytes().decode()
    assert m == '---\r\nname: x\r\n---\r\n<!-- godmode:basla -->\r\nv1 x {"json": 1}\r\n<!-- godmode:bitir -->\r\ngövde\r\n'
    assert not enjekte(y, 'v1 {ad} {"json": 1}')  # idempotent
    assert enjekte(y, "v2") and "v2" in y.read_bytes().decode() and "v1" not in y.read_bytes().decode()
    assert enjekte(y, "ders", isaret="ders-yuvasi")  # iki blok çakışmaz
    assert enjekte(y, "", geri=True) and enjekte(y, "", isaret="ders-yuvasi", geri=True)
    assert y.read_bytes().decode() == AJAN


def test_frontmattersiz_atlanir(tmp_path):
    y = tmp_path / "y.md"
    y.write_text("gövde\n", encoding="utf-8")
    assert not enjekte(y, "v1")
