"""DERİNLİK-1 R4b: devam --yeniden-tara --paket-yeniden paketi R4 ile yeniden kurar (ozet yok); bayraksız eski davranış (test_m2d)."""
from test_m2a import V, Sahte, _ctx, _durum, _kurulum, _ns, _pid

from video import cli
from video import parti as pt


def test_devam_paket_yeniden(tmp_path):
    kok = _kurulum(tmp_path, [V[0]])
    s = Sahte()
    pt.parti(_ns("baslat", kok / "kuyruk.md"), _ctx(kok, s))
    ctx, alt = _ctx(kok, s), []
    ctx["alt"] = lambda argv: alt.append(argv[0]) or 0
    assert pt.parti(_ns("devam", _pid(kok), yeniden_tara=True, paket_yeniden=True), ctx) == 0
    assert alt == ["paket"] and len(s.cagrilar) == 2
    v = _durum(kok)["videolar"][V[0]]
    assert v["paket"]["durum"] == "tamam" and "yeniden" not in v["paket"] and v["tarama"]["durum"] == "tamam"
    assert cli.main(["parti", "devam", "yok", "--yeniden-tara", "--paket-yeniden"], env={"VIDEO_UYGULA_KOK": str(kok)}) == 1  # bayrak tanınır: argparse çıkışı yok, "parti yok"
