"""DERİNLİK-MASTER (docs/video-tarama/derinlik-plan.md) maddeleri."""
import json

from test_derinlik2 import PID, _kos, _lisans_satiri, _uyku
from test_m2a import _ns
from test_m2c import Ar, _ctx, _panel

from video import parti as pt


def _gh_a2():
    def gh(args):
        gh.cagrilar.append(args[1])
        if "search/repositories" in args:
            return {"items": []}
        if args[1].endswith("/license"):
            return {"license": {"spdx_id": "Apache-2.0"}}
        if "/commits?" in args[1]:
            return [{"sha": "f00", "commit": {"committer": {"date": "2026-09-30T10:00:00Z"}}}]
        raise RuntimeError("HTTP 404")
    gh.cagrilar = []
    return gh


# A2 (=Y2) --yeniden: önceki aday yeniden araştırılmaz; Kapsam'daki çağrısız eksikler (lisans API, son commit, koşmamış güvenlik) tamamlanır
def test_a2_yeniden_onceki_eksik_kapsam_tamamlanir(tmp_path):
    _kos(tmp_path, [("ajan-k", "plugin", None)], None,
         Ar({"ajan-k": {"repo_url": "https://github.com/o/ajan-k", "lisans": "bilinmiyor", "son_commit": None}}))
    y = next(tmp_path.rglob("durum.json"))
    d = json.loads(y.read_text(encoding="utf-8"))
    d["adaylar"]["ajan-k"]["guvenlik"] = "koşmadı: klon başarısız (ağ)"
    y.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    gh, ar, ns = _gh_a2(), Ar({}), _ns("akil", y.parent.name)
    ns.yeniden = True

    def on(n, c):
        on.n.append(n.aday)
    on.n = []
    c = {**_ctx(tmp_path, ar), "gh": gh, "uyku": _uyku(), "on": on}
    c["env"]["CLAUDE_EVI"] = str(tmp_path / "evi")
    pt.parti(ns, c)
    assert "ajan-k" not in ar.adlar  # model araştırması yok
    assert on.n == ["ajan-k"]  # koşmamış güvenlik taraması yeniden denendi
    assert {"repos/o/ajan-k/license", "repos/o/ajan-k/commits?per_page=1"} <= set(gh.cagrilar)
    ks = next(s for s in _panel(tmp_path, PID)[1].split("## Kapsam", 1)[1].splitlines() if s.startswith("- ajan-k ·"))
    assert "lisans ✓" in ks and "commit ✓ 2026-09-30" in ks
    assert "| Apache-2.0 |" in _lisans_satiri(tmp_path, "ajan-k")
