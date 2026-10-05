"""A6(c): kurulu aday (kendi aracımız hariç) parti akışında .kos/<video>/<ad>/mekanizma.md "bizdeki kopya" alır; araştırma çağrısı 0,
dosya varsa dokunulmaz (cli.on_ ile aynı fonksiyon)."""
import json

from test_b5 import kos_yap
from test_m2a import V, _ns
from test_m2b import Arastirici, _actx, _parti, _rapor

from video import parti as pt


def _kos(tmp_path, ad, tur="skill"):
    kok = tmp_path / "k"
    p = _parti(kok, "2026-09-29-short", {V[0]: _rapor(V[0], [(ad, tur, None)])})
    (kok / "docs" / "departmanlar" / "envanter.json").write_text(json.dumps([{"ad": "graphify", "tur": "skill"}, {"ad": "stop-slop", "tur": "skill"}]),
                                                                  encoding="utf-8")
    (s := tmp_path / "ev" / ".claude" / "skills" / "stop-slop").mkdir(parents=True)
    (s / "a.js").write_text("const x = 1;\n\nfetch('https://ornek.com/api');\n", encoding="utf-8")
    return kok, p


def _calis(tmp_path, kok, p):
    a = Arastirici()
    ctx = _actx(kok, a)
    ctx["env"]["VIDEO_EV"], ctx["kos"] = str(tmp_path / "ev"), kos_yap()  # gerçek ctx'te kos var (cli.py:1368)
    pt.parti(_ns("akil", p.name), ctx)
    return a


def test_kurulu_aday_bizdeki_kopya_mekanizma(tmp_path):
    kok, p = _kos(tmp_path, "stop-slop")
    _calis(tmp_path, kok, p)
    m = list((kok / ".kos" / V[0]).glob("*/mekanizma.md"))
    assert len(m) == 1 and "bizdeki kopya" in m[0].read_text(encoding="utf-8")
    (a,) = json.loads((p / "durum.json").read_text(encoding="utf-8"))["adaylar"].values()
    assert a["durum"] == "kurulu" and "deneme" not in a  # araştırma çağrısı 0 (test_m2b:138 ölçütü)


def test_kendi_aracimiz_uretilmez(tmp_path):
    kok, p = _kos(tmp_path, "graphify")
    _calis(tmp_path, kok, p)
    assert not list(kok.rglob("mekanizma.md"))


def _eski(kok, yol):
    (m := kok / ".kos" / V[0] / "stop-slop" / "mekanizma.md").parent.mkdir(parents=True)
    m.write_text(f"eski\nkaynak: bizdeki kopya · {yol.as_posix()} @ commit yok\n", encoding="utf-8")
    return m


def test_mekanizma_varsa_dokunulmaz(tmp_path):  # A6(c) eki (5 Eki): aynı kurulu yol → dokunulmaz
    kok, p = _kos(tmp_path, "stop-slop")
    m = _eski(kok, tmp_path / "ev" / ".claude" / "skills" / "stop-slop")
    eski = m.read_text(encoding="utf-8")
    _calis(tmp_path, kok, p)
    assert m.read_text(encoding="utf-8") == eski and len(list((kok / ".kos" / V[0]).glob("*/mekanizma.md"))) == 1


def test_plugin_surumu_degisti_yeniden_yazilir(tmp_path):  # A6(c) eki: sürüm klasörü değişti → yeni yolla yeniden üretilir
    kok, p = _kos(tmp_path, "stop-slop")
    c = tmp_path / "ev" / ".claude" / "plugins" / "cache" / "m" / "stop-slop"
    (c / "1.1.0").mkdir(parents=True)
    (c / "1.1.0" / "a.js").write_text("fetch('https://ornek.com/api');\n", encoding="utf-8")
    for f in (s := tmp_path / "ev" / ".claude" / "skills" / "stop-slop").iterdir():
        f.unlink()
    s.rmdir()
    m = _eski(kok, c / "1.0.0")
    _calis(tmp_path, kok, p)
    t = m.read_text(encoding="utf-8")
    assert not t.startswith("eski") and f"{(c / '1.1.0').as_posix()} @" in t
