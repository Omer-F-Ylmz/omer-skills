"""VİDEO-PARTİ-YT1-ONARIM: gece koşucusu tavanda devam --cagri-ek/--usd-ek kullanır; tavanın üst sınırları silinmez."""
from test_m2a import V, Sahte, _ctx, _durum, _kurulum, _ns, _pid

from video import parti as pt


def test_devam_ek_tavan_ust_sinirlarini_korur(tmp_path):
    kok = _kurulum(tmp_path, [V[0]])
    s = Sahte()
    pt.parti(_ns("baslat", kok / "kuyruk.md", usd_tavan_max=3.75), _ctx(kok, s))
    pt.parti(_ns("devam", _pid(kok), cagri_ek=2, usd_ek=0.5), _ctx(kok, s))
    t = _durum(kok)["tavan"]
    assert t["usd_max"] == 3.75 and "cagri_max" in t
