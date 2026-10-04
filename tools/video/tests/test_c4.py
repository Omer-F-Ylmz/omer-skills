"""DERİNLİK-MASTER C4: video başına Kapsam (izleme) satırı · modele giden kare tavanı süreyle büyür · paket jeton bütçesi · tavan ya da
bütçe yüzünden incelenmeyen anlar kapsam.json'da sayılır ve `paket --incelenmedi` / `parti devam --incelenmedi` ile ikinci geçişte işlenir."""
import json
from pathlib import Path

from video import akil, cli
from video import parti as pt
from video.cli import main
from test_c3 import KOD, OcrKos, bolum, paket
from test_m9 import _alt, _d
from test_video import VID, ortam  # noqa: F401 (ortam fixture)


def test_butceyi_asan_kare_incelenmedi(ortam, monkeypatch):
    monkeypatch.setattr(cli, "PAKET_BUTCE", 0)
    _, md = paket(ortam, OcrKos({}))
    assert bolum(md, "Kareler") == ["yok"]
    assert bolum(md, "İncelenmedi") == ["[2:30] jeton bütçesi", "[7:30] jeton bütçesi"]


def test_kapsam_json_izleme_ve_ikinci_gecis(ortam, capsys):
    kos = OcrKos({"k00300": KOD, "k00100": KOD}, sahne_rc=0)
    d, _ = paket(ortam, kos, kare=1)  # 5:00 modele, 1:40 kare tavanı 1
    kj = json.loads((d / "kapsam.json").read_text(encoding="utf-8"))
    assert kj["incelenmedi"] == [[100, "kare tavanı 1"]]
    assert "seçilen 2 · OCR 2 · model 1 · incelenmedi 1" in kj["izleme"] and "kare-yalnız" in kj["izleme"]
    assert main(["paket", VID, "--kare", "1", "--istek-tavan", "0", "--kare-yalniz", "--incelenmedi"], env=ortam, kos=kos, uyku=lambda s: None) == 0
    md = (d / "paket.md").read_text(encoding="utf-8")
    assert [s.split(" · ")[1] for s in bolum(md, "Kareler")] == ["1:40"] and "## İncelenmedi" not in md
    assert "[1:40] kare tavanı 1" in (d / "paket-1.md").read_text(encoding="utf-8")  # ilk geçiş korunur
    assert json.loads((d / "kapsam.json").read_text(encoding="utf-8"))["incelenmedi"] == []
    capsys.readouterr()
    assert main(["paket", VID, "--kare", "1", "--istek-tavan", "0", "--incelenmedi"], env=ortam, kos=kos, uyku=lambda s: None) == 0
    assert "incelenmedi an yok" in capsys.readouterr().out and (d / "paket.md").read_text(encoding="utf-8") == md


def test_parti_kare_sureyle_buyur_izleme_ikinci_gecis(tmp_path, monkeypatch):
    assert pt.model_kare(8, 45 * 60) == 15 and pt.model_kare(8, 10 * 3600) == pt.KARE_UST
    assert pt.model_kare(3, 60) == 3 and pt.model_kare(30, 600) == 30  # short değişmez · açık büyük değer korunur
    monkeypatch.setattr(pt, "find_spec", lambda n: True)
    pd, onb = tmp_path / "pd", tmp_path / "onb"
    pd.mkdir()

    def pk(v):
        (onb / v / "paket.md").write_text("# p\n", encoding="utf-8")
        (onb / v / "kapsam.json").write_text(json.dumps({"izleme": "sahne 3 · model 2 · incelenmedi 1", "incelenmedi": [[100, "kare tavanı 2"]]}),
                                             encoding="utf-8")
        return 0
    alt, cagri = _alt(onb, sure=3600, paket=pk, whisper=RuntimeError("yok"))
    d = _d("e1")
    pt._kos(pd, d, onb, tmp_path / "t", alt, str, None, {})
    a = next(a for a in cagri if a[0] == "paket")
    assert a[a.index("--kare") + 1] == "20" and "--incelenmedi" not in a  # 60 dk / 3 > kare_sayisi 8
    assert d["videolar"]["e1"]["izleme"] == "sahne 3 · model 2 · incelenmedi 1"
    pt.incelenmedi_isaretle(d, onb)
    s = d["videolar"]["e1"]
    assert s["paket"]["durum"] == "bekliyor" and s["paket"]["incelenmedi"] and s["tarama"]["durum"] == "bekliyor" and s["tarama"]["gecis"] == 2
    cagri.clear()
    s["tarama"]["durum"] = "tamam"  # yalnız paket aşaması sınanır (sahte paket.md taranamaz)
    pt._kos(pd, d, onb, tmp_path / "t", alt, str, None, {})
    assert "--incelenmedi" in next(a for a in cagri if a[0] == "paket") and not any(a[0] == "ozet" for a in cagri)


def test_panel_kapsam_izleme_alani():
    a = {"tur": "skill", "repo": None, "durum": "x", "kurulu": False, "videolar": {"e1": 1}}
    s, eksik = akil._kapsam("ajan", a, {}, "", "koşmadı", {"videolar": {"e1": {"izleme": "sahne 3 · model 2 · incelenmedi 1"}}})
    assert s.endswith("izleme sahne 3 · model 2 · incelenmedi 1") and "izleme" not in eksik
