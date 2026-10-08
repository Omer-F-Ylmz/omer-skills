"""VİDEO-GÖZ-1b-1T: T1 teşhis etiketi kapsam ile aynı eşleşme ve aynı gürültü süzgeciyle (sözlüklü) · T2 S4 kararı."""
import json

from video import altin as au
from video import cli


def _kur(tmp_path, ocr, paket):
    (tmp_path / "goz").mkdir()
    (tmp_path / "goz" / "ocr.json").write_text(json.dumps({"ham": ocr}), encoding="utf-8")
    (tmp_path / "paket.md").write_text(paket, encoding="utf-8")
    (tmp_path / "tarama").mkdir()
    (tmp_path / "tarama" / "sozluk.txt").write_text("GSAP | gsap.com\n", encoding="utf-8")
    return {"VIDEO_TARAMA_DIZIN": str(tmp_path / "tarama")}


def test_t1_sozluk_adi_satiri_butce_atti_der_gurultu_degil(tmp_path, capsys):
    # pipeline (_goz) _ocr_gurultu'yu sözlükle çağırır: GSAP satırı pakete girebilir → teşhis de sözlüklü olmalı
    env = _kur(tmp_path, [[5.0, [["GSAP", 0.95, 0]]]], "# x\n## Segmentler\n[0:01] merhaba\n## Ekran metni (OCR)\n")
    (tmp_path / "a.json").write_text(json.dumps({"adaylar": [{"ad": "GSAP", "zaman": "0:05", "kaynak": "ekran"}]}), encoding="utf-8")
    assert cli.main(["altin", "kapsam", str(tmp_path / "paket.md"), str(tmp_path / "a.json")], env=env) == 0
    assert "GSAP (ekranda-var-OCR-kaçırdı/bütçe-attı)" in capsys.readouterr().out


def test_t1_kapsam_ile_teshis_tutarli():
    # kapsam'ın bulduğu aday kaçanda yok; bütçe-attı denen her aday ham satırda kapsam'ın eşleşmesiyle (gecer + alias) geçer
    altin = {"adaylar": [{"ad": "Manyetik butonlar", "alias": ["magnetic buttons"], "zaman": "4:15", "kaynak": "ekran"},
                         {"ad": "Claude memory", "alias": ["Recalled a memory"], "zaman": "4:54", "kaynak": "ekran"},
                         {"ad": "Framer Motion", "zaman": "0:10", "kaynak": "ekran"}]}
    ham = [[255.0, [["you scroll hard), magnetic buttons, focus styles", 0.98, 0]]], [294.0, [["Recalled a memory, saved 3", 0.92, 0]]]]
    paket = "# x\n## Ekran metni (OCR)\n[0:10] Framer Motion intro\n"
    p = au.kapsam(paket, altin, boyut=lambda y: None)
    k = dict(au.kacan_alt(p["kacan"], altin, ham, lambda x: False))
    assert set(k) == {"Manyetik butonlar", "Claude memory"} and all(v.endswith("/bütçe-attı") for v in k.values())
    for ad in k:
        a = next(x for x in altin["adaylar"] if x["ad"] == ad)
        assert any(au._icerir(x, [ad, *a.get("alias", [])]) for _, r in ham for x, _, _ in r)
        assert not au._icerir(paket, [ad, *a.get("alias", [])])  # paket metninde kapsam ile aynı karar
