"""A6(c): kurulu aday (kendi aracımız hariç) parti akışında .kos/<video>/<ad>/mekanizma.md "bizdeki kopya" alır; araştırma çağrısı 0,
dosya varsa dokunulmaz (cli.on_ ile aynı fonksiyon)."""
import json

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
    ctx["env"]["VIDEO_EV"] = str(tmp_path / "ev")
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


def test_mekanizma_varsa_dokunulmaz(tmp_path):
    kok, p = _kos(tmp_path, "stop-slop")
    (m := kok / ".kos" / V[0] / "stop-slop" / "mekanizma.md").parent.mkdir(parents=True)
    m.write_text("eski", encoding="utf-8")
    _calis(tmp_path, kok, p)
    assert m.read_text(encoding="utf-8") == "eski" and len(list((kok / ".kos" / V[0]).glob("*/mekanizma.md"))) == 1
