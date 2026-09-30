"""MOTOR-M8 K1: tire ile başlayan kimlik (-_S3KD0ZIfI) ozet/paket/parti yollarında seçenek sanılmaz."""
import pytest

from video import cli
from video import parti as pt
from test_m2a import Sahte, _ctx, _durum, _kurulum, _ns

TIRELI = ["-_S3KD0ZIfI", "-INveHwbRz4"]


class Alt:
    """Sahte aşama-2 komutu: argv kaydeder; paket çağrısında saklanan paket.md'yi geri yazar; patla videosunda istisna."""

    def __init__(self, kok, patla=None, hata=None):
        self.kok, self.patla, self.hata, self.cagri, self.icerik = kok, patla, hata, [], {}

    def sakla(self, videolar):
        for v in videolar:
            y = self.kok / "c" / v / "paket.md"
            self.icerik[v] = y.read_text(encoding="utf-8")
            y.unlink()

    def __call__(self, argv):
        self.cagri.append(list(argv))
        v = argv[-1]
        if v == self.patla:
            raise self.hata
        if argv[0] == "paket":
            (self.kok / "c" / v / "paket.md").write_text(self.icerik[v], encoding="utf-8")


@pytest.mark.parametrize("vid", TIRELI)
@pytest.mark.parametrize("ayrac", [[], ["--"]])
def test_cli_tireli_kimlik_ozet_paket(monkeypatch, tmp_path, vid, ayrac):
    gor = {}
    monkeypatch.setattr(cli, "ozet", lambda ns, ctx: gor.update(ozet=ns.hedef) or 0)
    monkeypatch.setattr(cli, "paket", lambda ns, ctx: gor.update(paket=(ns.id, ns.kare)) or 0)
    env = {"VIDEO_CACHE": str(tmp_path)}
    assert cli.main(["ozet", *ayrac, vid], env=env) == 0
    assert cli.main(["paket", "--kare", "3", "--istek-tavan", "0", *ayrac, vid], env=env) == 0
    assert gor == {"ozet": [vid], "paket": (vid, 3)}


def test_parti_ic_cagrilar_kimlikten_once_ayirici(tmp_path):
    _kurulum(tmp_path, TIRELI)
    a = Alt(tmp_path)
    a.sakla(TIRELI)
    assert pt.parti(_ns("baslat", tmp_path / "kuyruk.md"), {**_ctx(tmp_path, Sahte()), "alt": a}) == 0
    assert a.cagri and all(x[-2:] == ["--", x[-1]] and x[-1] in TIRELI for x in a.cagri), a.cagri
    assert {v: s["paket"]["durum"] for v, s in _durum(tmp_path)["videolar"].items()} == {v: "tamam" for v in TIRELI}
