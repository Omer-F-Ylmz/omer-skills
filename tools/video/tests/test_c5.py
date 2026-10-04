"""DERİNLİK-MASTER C5 hızlı kurgu (Ömer, 5 Eki O15): 5 sn içinde ≥3 sahne kesimi → montaj; kümeden modele en çok OCR metni
(eşitse en yüksek sahne skoru) taşıyan en fazla 2 kare, diğerleri "tekrar (montaj)". Kanıt: b2QkhmQ0sT0 66/67/68/69/70 sn beşi de modele."""

import json
import re
from pathlib import Path

from video.cli import main
from test_c3 import OcrKos
from test_video import VID, onbellek, ortam  # noqa: F401 (ortam fixture)


def kos(ortam, sahneler, metin):
    onbellek(ortam, [], duration=1200)
    d = Path(ortam["VIDEO_CACHE"]) / VID
    (d / "sahne.json").write_text(json.dumps({"durum": "✓", "sahneler": sahneler}), encoding="utf-8")
    assert main(["paket", VID, "--kare", "8", "--istek-tavan", "0", "--kare-yalniz", "--model-tavan", "60"], env=ortam,
                kos=OcrKos(metin), uyku=lambda s: None) == 0
    kj = json.loads((d / "kapsam.json").read_text(encoding="utf-8"))
    return {int(p.name[1:6]) for p in (d / "kareler").glob("k*.jpg")}, kj["izleme"]


def test_montajdan_en_fazla_iki_kare_ocr_metni_sonra_skor(ortam):
    sahne = [[66.0, 0.5], [67.0, 0.6], [68.0, 0.9], [69.0, 0.4], [70.0, 0.3], [300.0, 0.8], [600.0, 0.7]]
    kare, izleme = kos(ortam, sahne, {"k00070": {"tr": [["Settings", 0, 0, 9, 9]], "en": []}})
    assert {66, 67, 68, 69, 70} & kare == {68, 70}  # 70 en çok OCR metni, 68 en yüksek skor
    assert {300, 600} <= kare and re.search(r"tekrar \(montaj\) 3", izleme)


def test_5_sn_icinde_iki_kesim_montaj_degil(ortam):
    kare, izleme = kos(ortam, [[66.0, 0.5], [69.0, 0.6], [75.0, 0.9]], {})
    assert {66, 69, 75} <= kare and "montaj" not in izleme
