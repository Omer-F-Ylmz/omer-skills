"""DERİNLİK-MASTER E1 eki (Ömer, O33; D1 (a) ile tutarlı): KAÇAN? denetimi yalnız künyesinde şema ≥2 olan raporda; eski şemada
denetim.md'ye "eski şema: İz yok, KAÇAN? denetimi yapılmadı" bilgi satırı (kapat'ı durdurmaz; İz yok kuralı IZ_TARIH ile aynen)."""
from video import akil as ak
from video import tarama as tr

IZ = "## İz\n| kaynak | ne | bağlandığı | kanıt |\n|---|---|---|---|\n| konuşma 01:00 | rtk | rtk | geçti |\n"


def _d(tmp_path, sema):
    (tmp_path / "v1.md").write_text(f"## Künye\nBaşlık · süre: 10:00{sema}\n" + IZ, encoding="utf-8")
    (tmp_path / "onb" / "v1").mkdir(parents=True)
    (tmp_path / "onb" / "v1" / "paket.md").write_text("## Açıklama bağlantıları\n- https://foo.dev/kit\n## Segmentler\n[00:01] rtk\n",
                                                      encoding="utf-8")
    return {"parti": "p", "tarih": "2026-10-03", "videolar": {"v1": {"tarama": {"durum": "tamam", "cikti": str(tmp_path / "v1.md")}}}}


def test_eski_sema_kacan_denetlenmez_bilgi_satiri(tmp_path):
    d = _d(tmp_path, "")
    z = ak.denetim(d, tmp_path, tmp_path / "onb")
    assert z["kacan"] == [] and z["dusuk"] == [] and z["iz_yok"] == []
    assert "eski şema: v1 · İz yok, KAÇAN? denetimi yapılmadı" in tr.bolum(ak.denetim_md(d, z, {}, tmp_path / "onb"), "KAÇAN?")


def test_sema2_kacan_denetlenir(tmp_path):
    d = _d(tmp_path, " · şema 2")
    z = ak.denetim(d, tmp_path, tmp_path / "onb")
    assert z["kacan"] and "eski şema" not in ak.denetim_md(d, z, {}, tmp_path / "onb")
