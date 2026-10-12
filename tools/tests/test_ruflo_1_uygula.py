import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "onay"))
import ruflo_1_uygula as r  # noqa: E402

AJAN = b"---\nname: a\n---\nGovde\n"


def kur(tmp_path, dersli):
    ev = tmp_path / "ev"
    (ev / ".claude" / "agents").mkdir(parents=True)
    (ev / ".claude" / "agents" / "a.md").write_bytes(AJAN)
    tsv = tmp_path / "ab.tsv"
    tsv.write_text("baslik\n" + "".join(f"t\tk\t{n}\t{k}\t{p}\n" for n in range(12) for k, p in (("derssiz", 0.6), ("dersli", dersli))),
                   encoding="utf-8")
    ders_py = tmp_path / "ders.py"
    ders_py.write_text("", encoding="utf-8")
    return ev, tsv, ders_py, ev / ".claude" / "agents" / "a.md"


def test_kapi_gecmezse_dokunmaz(tmp_path):
    ev, tsv, ders_py, f = kur(tmp_path, 0.5)
    assert r.main(ev, "uygula", tsv, ders_py) == 1 and f.read_bytes() == AJAN


def test_uygula_yedekli_ve_geri(tmp_path):
    ev, tsv, ders_py, f = kur(tmp_path, 0.9)
    assert r.main(ev, "--kuru", tsv, ders_py) == 0 and f.read_bytes() == AJAN
    assert r.main(ev, "uygula", tsv, ders_py) == 0 and b"ders-yuvasi:basla" in f.read_bytes()
    assert list((ev / ".claude" / "yedek").glob("ruflo1-*/a.md"))[0].read_bytes() == AJAN
    assert r.main(ev, "--geri", tsv, ders_py) == 0 and f.read_bytes() == AJAN
