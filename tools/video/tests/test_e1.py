"""DERİNLİK-MASTER E1: denetim.md (≤150 satır) — KAÇAN? · aday değil · ONARIM BEKLİYOR · incelenmedi · risk en yüksek 5 · tohumlu
rastgele 3; her satırda Desktop'un açacağı tam URL (video mm:ss linki · repo)."""
import json

from test_d3 import _d as _d3
from test_m11 import _kur

from video import akil as ak
from video import tarama as tr

YT = "https://www.youtube.com/watch?v="


def _d():
    ad = {f"a{i}": {"ad": f"a{i}", "tur": "skill", "repo": f"o/a{i}", "videolar": {"v1": {"zaman": "1:05"}}} for i in range(10)}
    ad["a0"].update(guvenlik="HIGH/CRITICAL 2", kaynak="u/a0")
    return {"parti": "p1", "videolar": {"v1": {}, "v2": {}}, "adaylar": ad}


def _z(n=1):
    return {"kacan": [("v1", "paket", f"supabase{i or ''}") for i in range(n)], "dusuk": [("v2", "paket", "Cursor")],
            "degil": [("v1", "konuşma 01:00", "Next.js", "aday değil: genel kavram")]}


def _karar():
    k = {f"a{i}": ("SOR", "g", []) for i in range(10)}
    k["a0"], k["a1"] = ("T1", "g", ["lisans"]), ("ONARIM BEKLİYOR", "çözülmedi: x", [])
    return k


def test_bolumler_ve_tam_url(tmp_path):
    (tmp_path / "v2").mkdir()
    (tmp_path / "v2" / "kapsam.json").write_text(json.dumps({"incelenmedi": [[95, "kare tavanı 8"]]}), encoding="utf-8")
    t = ak.denetim_md(_d(), _z(), _karar(), tmp_path)
    b = lambda ad: tr.bolum(t, ad)  # noqa: E731
    assert f"supabase · {YT}v1" in b("KAÇAN?") and "Cursor" not in b("KAÇAN?") and f"{ak.DUSUK_KURAL}: 1" in b("KAÇAN?")  # KAPANIŞ-3
    assert f"Next.js · aday değil: genel kavram · {YT}v1&t=60s" in b("aday değil")
    assert "- a1 · çözülmedi: x · https://github.com/o/a1" in b("ONARIM BEKLİYOR")
    assert f"- v2 · 1 an · {YT}v2&t=95s" in b("İncelenmedi")
    r = b("Risk puanı").strip().splitlines()
    assert len(r) == 5 and r[0].startswith("- a0 · puan 4") and f"{YT}v1&t=65s" in r[0] and "https://github.com/o/a0" in r[0]
    assert r[1].startswith("- a1 · puan 1")
    s = b("Rastgele 3").strip().splitlines()
    assert len(s) == 3 and s == tr.bolum(ak.denetim_md(_d(), _z(), _karar(), tmp_path), "Rastgele 3").strip().splitlines()  # tohumlu
    assert not {x.split(" · ")[0] for x in s} & ({x.split(" · ")[0] for x in r} | {"- a1"})


def test_150_satir_tavani(tmp_path):
    t = ak.denetim_md(_d(), _z(300), _karar(), tmp_path)
    assert len(t.splitlines()) <= 150 and "kesildi" in t.splitlines()[-1]


def test_denetim_aday_degil_satirlari(tmp_path):
    z = ak.denetim(_d3(tmp_path), tmp_path, tmp_path / "onb")
    assert z["degil"] == [("v1", "konuşma 02:00", "AI", "aday değil: genel kavram")]


def test_panel_denetim_md_yazar(tmp_path):
    pdir, d = _kur(tmp_path)
    p = ak.panel(pdir, d, tmp_path)
    assert (p.parent / "denetim.md").read_text(encoding="utf-8").startswith(f"# Denetim — {d['parti']}")
