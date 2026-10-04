"""DERİNLİK-MASTER D2 kablolama + D3: panel "## Denetim" (bahis · bağlanan · aday değil (oran) · KAÇAN? · düşük güven · İz yok);
engelleyen KAÇAN? ya da "İz yok" (D1 sonrası partide İz'siz rapor) `video parti kapat`ı durdurur; kapanışta aday adları bilinen-araclar.txt'ye."""
from test_m11 import _kur

from video import akil as ak
from video import tarama as tr

IZ = ("## Künye\nşema 2\n## İz\n| kaynak | ne | bağlandığı | kanıt |\n|---|---|---|---|\n| konuşma 01:00 | rtk | rtk | geçti |\n"
      "| konuşma 02:00 | AI | aday değil: genel kavram | x |\n")


def _d(tmp_path, tarih="2026-10-05"):
    (tmp_path / "v1.md").write_text(IZ, encoding="utf-8")
    (tmp_path / "v2.md").write_text("## Künye\nşema 1\n", encoding="utf-8")
    (tmp_path / "onb" / "v1").mkdir(parents=True)
    (tmp_path / "onb" / "v1" / "paket.md").write_text("## Segmentler\n[00:01] we install supabase with Cursor and Cursor\n", encoding="utf-8")
    t = lambda v: {"tarama": {"durum": "tamam", "cikti": str(tmp_path / f"{v}.md")}}  # noqa: E731
    return {"parti": "p", "tarih": tarih, "videolar": {"v1": t("v1"), "v2": t("v2")}, "adaylar": {"yeni-arac": {}}}


def test_denetim_sayilari(tmp_path):
    z = ak.denetim(_d(tmp_path), tmp_path, tmp_path / "onb")
    assert (z["bahis"], z["baglanan"], z["aday_degil"]) == (2, 1, 1)
    assert z["kacan"] == [("v1", "paket", "supabase")] and z["dusuk"] == [("v1", "paket", "Cursor")] and z["iz_yok"] == ["v2"]


def test_d1_oncesi_parti_iz_yok_sayilmaz(tmp_path):
    assert ak.denetim(_d(tmp_path, "2026-10-04"), tmp_path, tmp_path / "onb")["iz_yok"] == []


def test_panel_denetim_bolumu(tmp_path):
    pdir, d = _kur(tmp_path)
    p = ak.panel(pdir, d, tmp_path).read_text(encoding="utf-8")
    assert "## Denetim" in p and "KAÇAN? 0" in p


def test_kapat_kacan_ve_iz_yok_durdurur_bilinen_eklenir(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(tr, "denetle", lambda m: [])
    assert ak.kapat(tmp_path / "pd", _d(tmp_path), tmp_path, {"kok": tmp_path / "onb"}) == 1
    out = capsys.readouterr().out
    assert "KAÇAN? 1" in out and "İz yok: v2" in out
    assert "yeni-arac" in (tmp_path / tr.BILINEN).read_text(encoding="utf-8")
