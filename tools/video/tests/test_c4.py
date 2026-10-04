"""DERİNLİK-MASTER C4: video başına Kapsam (izleme) satırı · modele giden kare tavanı süreyle büyür · paket jeton bütçesi · tavan ya da
bütçe yüzünden incelenmeyen anlar kapsam.json'da sayılır ve `paket --incelenmedi` / `parti devam --incelenmedi` ile ikinci geçişte işlenir."""
import json
from pathlib import Path

from video import akil, cli
from video import parti as pt
from video.cli import main
from test_c3 import KOD, KOD2, OKUNUR, OcrKos, bolum, paket
from test_o11 import kod, okunur
from test_m9 import _alt, _d
from test_video import VID, ortam  # noqa: F401 (ortam fixture)


def test_butceyi_asan_kare_incelenmedi(ortam, monkeypatch):
    monkeypatch.setattr(cli, "PAKET_BUTCE", 0)
    _, md = paket(ortam, OcrKos({}))
    assert bolum(md, "Kareler") == ["yok"]
    assert bolum(md, "İncelenmedi") == ["[2:30] jeton bütçesi", "[7:30] jeton bütçesi"]


def test_kapsam_json_izleme_ve_ikinci_gecis(ortam, capsys):
    kos = OcrKos({"k00300": KOD, "k00100": KOD2}, sahne_rc=0)  # Ömer onayı (O11 (3)): aynı OCR metni tek kare
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
    # Ömer onayı (O10): tavan KARE_UST sabit, asıl sınır PAKET_BUTCE; süre/3 yalnız taban (canlı b2QkhmQ0sT0: 20 dk → "kare tavanı 7" ×8)
    # Ömer onayı (O11): tavan 20 → bütçe; KARE_UST yalnız güvenlik üst sınırı 60
    assert pt.model_kare(8, 45 * 60) == pt.model_kare(8, 20 * 60) == pt.model_kare(12, 10 * 60) == pt.KARE_UST == 60
    assert pt.model_kare(3, 30) == 3 and pt.model_kare(3, 0) == 3 and pt.model_kare(90, 600) == 90  # short/süresiz değişmez · açık büyük değer korunur
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
    assert a[a.index("--kare") + 1] == "60" and "--incelenmedi" not in a  # Ömer onayı (O11): KARE_UST 60 > kare_sayisi 8
    assert d["videolar"]["e1"]["izleme"] == "sahne 3 · model 2 · incelenmedi 1"
    pt.incelenmedi_isaretle(d, onb)
    s = d["videolar"]["e1"]
    assert s["paket"]["durum"] == "bekliyor" and s["paket"]["incelenmedi"] and s["tarama"]["durum"] == "bekliyor" and s["tarama"]["gecis"] == 2
    cagri.clear()
    s["tarama"]["durum"] = "tamam"  # yalnız paket aşaması sınanır (sahte paket.md taranamaz)
    pt._kos(pd, d, onb, tmp_path / "t", alt, str, None, {})
    assert "--incelenmedi" in next(a for a in cagri if a[0] == "paket") and not any(a[0] == "ozet" for a in cagri)


def test_tavan_20_sinir_butce_24_secilen_15_model(ortam):
    """O10: 24 seçilen · 17 OCR (9 okunur + 8 kod) · 7 metinsiz → 15 kare modele, incelenmedi 0 (eskiden süre/3 tavanı 8'i keserdi)."""
    sahne = b"".join(f"frame:{i} pts:{t}000 pts_time:{t}\nlavfi.scene_score=0.9\n".encode() for i, t in enumerate((100, 200, 400, 500)))
    t = [f"k{15 + 30 * i:05d}" for i in range(20)]
    # Ömer onayı (O11): kare 20 açık (KARE_UST 60 oldu); OCR metinleri kareye özgü (O11 tekrar ayıklama aynı metni tek sayar)
    d, _ = paket(ortam, OcrKos({**{k: okunur(i) for i, k in enumerate(t[:9])}, **{k: kod(i) for i, k in enumerate(t[9:17])}}, sahne_rc=0, sahne=sahne), kare=20)
    kj = json.loads((d / "kapsam.json").read_text(encoding="utf-8"))
    assert "seçilen 24 · OCR 17 · model 15 · incelenmedi 0" in kj["izleme"] and kj["incelenmedi"] == []


def test_girdi_tavani_dusen_kareler_kapsamda_incelenmedi(tmp_path):
    """O10: kare_sigdir (40k girdi) düşürdüğü anlar kapsam.json incelenmedi'ye "girdi tavanı" ile; izleme sayısı güncel; tekrar eklenmez."""
    (tmp_path / "e1").mkdir()
    kj = tmp_path / "e1" / "kapsam.json"
    kj.write_text(json.dumps({"izleme": "seçilen 9 · OCR 0 · model 8 · incelenmedi 1 · OCR gürültü 0", "incelenmedi": [[5, "jeton bütçesi"]]}),
                  encoding="utf-8")
    metin = ""
    while pt.c.token(metin) < pt.GIRDI_TAVAN - 3 * pt.KARE_TK:
        metin += "kelime " * 500
    for _ in range(2):
        pk = {"e1": {"short": False, "metin": metin, "kareler": [f"k{i}.jpg" for i in range(8)], "kare_zaman": [10 * i for i in range(8)]}}
        pt.kare_sigdir(pk, tmp_path)
    n = len(pk["e1"]["kareler"])
    k = json.loads(kj.read_text(encoding="utf-8"))
    assert 0 < n < 8 and k["incelenmedi"] == [[5, "jeton bütçesi"], *[[10 * i, "girdi tavanı"] for i in range(n, 8)]]
    assert f"model {n} · incelenmedi {9 - n} · OCR gürültü 0" in k["izleme"]


def test_panel_kapsam_izleme_alani():
    a = {"tur": "skill", "repo": None, "durum": "x", "kurulu": False, "videolar": {"e1": 1}}
    s, eksik = akil._kapsam("ajan", a, {}, "", "koşmadı", {"videolar": {"e1": {"izleme": "sahne 3 · model 2 · incelenmedi 1"}}})
    assert s.endswith("izleme sahne 3 · model 2 · incelenmedi 1") and "izleme" not in eksik
