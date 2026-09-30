"""MOTOR-M5b: bütçe kusuru — kalan $ son çağrının altındaysa yeniden istek yok (form_red + not) · bütçe hatası asla "hata" olmaz · --ikinci-goz varsayılanı yok."""
from video import cli
from video import parti as pt

from test_m2a import V, _ctx, _durum, _kurulum, _ns

NOT = "tavan: yeniden istek bütçesi yok"


class Cagir:
    """claude -p gibi: istenen iş --max-budget-usd'yi aşarsa error_max_budget_usd; form her seferinde eksik (red)."""

    def __init__(self, usd, hata=False):
        self.butce, self.usd, self.hata = [], usd, hata

    def __call__(self, sistem, metin, sema, kareler=(), model=None, butce=.5, env=None, **_):
        self.butce.append(butce)
        if self.hata or butce < self.usd:
            return {"form": None, "usage": {}, "usd": butce, "sure": .1, "hata": "error_max_budget_usd: "}
        ids = sema["properties"]["videolar"]["items"]["properties"]["id"]["enum"]
        return {"form": {"videolar": [{"id": v} for v in ids]}, "usage": {"input_tokens": 10, "output_tokens": 5}, "usd": self.usd, "sure": .1, "hata": None}


def test_kalan_butce_son_cagrinin_altinda_yeniden_istek_yok(tmp_path):
    kok = _kurulum(tmp_path, [V[0]])
    c = Cagir(.6)
    pt.parti(_ns("baslat", kok / "kuyruk.md", butce=.8, usd_tavan=1.0, ikinci_goz="yok"), _ctx(kok, c))
    t = _durum(kok)["videolar"][V[0]]["tarama"]
    assert len(c.butce) == 1  # kalan $0,4 < son çağrı $0,6 → ikinci istek yapılmaz
    assert t["durum"] == "form_red" and t["hata"][0] == NOT


def test_butce_hatasi_hata_degil_form_red(tmp_path):
    kok = _kurulum(tmp_path, [V[0]])
    pt.parti(_ns("baslat", kok / "kuyruk.md", ikinci_goz="yok"), _ctx(kok, Cagir(.1, hata=True)))
    t = _durum(kok)["videolar"][V[0]]["tarama"]
    assert t["durum"] == "form_red" and t["hata"][0] == NOT


def test_ikinci_goz_varsayilani_yok(monkeypatch):
    goren = []
    monkeypatch.setattr(pt, "parti", lambda ns, ctx: goren.append(ns.ikinci_goz) or 0)
    cli.main(["parti", "baslat", "kuyruk.md"], env={})
    assert goren == ["yok"]
