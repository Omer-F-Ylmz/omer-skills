import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "onay"))
import ruflo_1_uygula as r  # noqa: E402

AJAN = b"---\nname: a\n---\nGovde\n"


def kur(tmp_path, dersli, jeton=900, aile="kod"):
    ev = tmp_path / "ev"
    (ev / ".claude" / "agents").mkdir(parents=True)
    for ad in ("dn-a", "vid-a", "a"):
        (ev / ".claude" / "agents" / f"{ad}.md").write_bytes(AJAN)
    tsv = tmp_path / "ab.tsv"
    tsv.write_text("baslik\n" + "".join(f"t\t{aile}\t{n}\t{k}\t{p}\t0\t3\t{j}\t0\t0\t0\n" for n in range(5)
                                        for k, p, j in (("derssiz", 0.6, 1000), ("dersli", dersli, jeton))), encoding="utf-8")
    ders_py = tmp_path / "ders.py"
    ders_py.write_text("", encoding="utf-8")
    return ev, tsv, ders_py, ev / ".claude" / "agents"


def test_kapi_gecmezse_dokunmaz(tmp_path):
    ev, tsv, ders_py, d = kur(tmp_path, 0.5)
    assert r.main(ev, "uygula", tsv, ders_py) == 1 and (d / "dn-a.md").read_bytes() == AJAN


def test_kalite_iyi_jeton_fazlaysa_gecmez(tmp_path):
    ev, tsv, ders_py, d = kur(tmp_path, 0.9, jeton=1100)
    assert r.main(ev, "uygula", tsv, ders_py) == 1 and (d / "dn-a.md").read_bytes() == AJAN


def test_uygula_yalniz_gecen_aile_yedekli_ve_geri(tmp_path):
    ev, tsv, ders_py, d = kur(tmp_path, 0.9)
    assert r.main(ev, "--kuru", tsv, ders_py) == 0 and (d / "dn-a.md").read_bytes() == AJAN
    assert r.main(ev, "uygula", tsv, ders_py) == 0 and b"ders-yuvasi:basla" in (d / "dn-a.md").read_bytes()
    assert (d / "vid-a.md").read_bytes() == AJAN and (d / "a.md").read_bytes() == AJAN  # video ailesi geçmedi, ailesiz dokunulmaz
    assert [f.name for f in (ev / ".claude" / "yedek").glob("ruflo1-*/*.md")] == ["dn-a.md"]
    assert r.main(ev, "--geri", tsv, ders_py) == 0 and (d / "dn-a.md").read_bytes() == AJAN


def test_aile_eksik_cift_gecmez(tmp_path):
    ev, tsv, ders_py, d = kur(tmp_path, 0.9, aile="video")
    k = r.kabul(tsv)
    assert k["video"][0] and not k["kod"][0] and "0/4" in k["kod"][1]
