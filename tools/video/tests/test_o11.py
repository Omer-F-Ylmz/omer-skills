"""DERİNLİK-MASTER O11: C4/C3 ikinci düzeltme (canlı b2QkhmQ0sT0 --kare 20 → seçilen 44 · model 20 · incelenmedi 8 "kare tavanı 20")."""

import json
import random
from pathlib import Path

from video import parti as pt
from video.cli import main
from test_c3 import KUTU, OcrKos
from test_video import VID, onbellek, ortam  # noqa: F401 (ortam fixture)
from test_video import jpeg


def test_tek_girdi_hesabi_gercek_kare_jetonu_28_kare_7k_metin_dusmez(tmp_path):
    """(1) kare_sigdir PAKET_BUTCE ile aynı hesap: gerçek kare jetonu (~442) + tam metin; KARE_TK 1600 varsayımı 28 kareyi keserdi."""
    kareler = []
    for i in range(28):
        (y := tmp_path / f"k{i}.jpg").write_bytes(jpeg())
        kareler.append(y.as_posix())
    metin = ""
    while pt.c.token(metin) < 7_000:
        metin += "kelime " * 100
    pk = {"e1": {"short": False, "metin": metin, "kareler": list(kareler), "kare_zaman": list(range(28))}}
    pt.kare_sigdir(pk)
    assert pk["e1"]["kareler"] == kareler and "kare_not" not in pk["e1"]
    assert pt.girdi_tk(metin, kareler) == pt.c.token(metin) + 28 * 442


def test_model_kare_yalniz_butce_20dk_44_secilen_28_model(ortam, monkeypatch):
    """(2) Ömer onayı (O11: tavan 20 → bütçe): KARE_UST güvenlik üst sınırı 60; 20 dk, 44 seçilen (16 OCR okunur + 28 model) → model 28."""
    import test_c2
    ad = lambda i: f"k{10 + 20 * i:05d}"  # noqa: E731 (eşit aralık: 1200 sn / 60)
    for i in range(44, 60):
        monkeypatch.setitem(test_c2.AYNI, ad(i), ad(i - 16))  # 16 aynı ekran (dHash) → seçilmez
    onbellek(ortam, [], duration=1200)
    kos = OcrKos({ad(i): okunur(i) for i in range(16)})
    assert main(["paket", VID, "--kare", str(pt.model_kare(8, 1200)), "--istek-tavan", "0", "--kare-yalniz"], env=ortam, kos=kos, uyku=lambda s: None) == 0
    kj = json.loads((Path(ortam["VIDEO_CACHE"]) / VID / "kapsam.json").read_text(encoding="utf-8"))
    assert "seçilen 44 · OCR 16 · model 28 · incelenmedi 0" in kj["izleme"] and pt.KARE_UST == 60


KELIME = "kurulum ayarlar dosya komut proje sunucu istemci tarayici depolama arama sonuc model ajan beceri eklenti kanca bellek oturum".split()


def satir(i, j):
    """Kareye özgü okunur OCR satırı (kareler arası benzerlik < OCR tekrar eşiği)."""
    return " ".join(random.Random(f"{i}-{j}").sample(KELIME, 6))


def okunur(i):
    return {"tr": [[satir(i, j), *KUTU(j * 40)] for j in range(3)], "en": []}


def kod(i):
    a = random.Random(f"kod{i}").sample(KELIME, 6)
    return {"tr": [[s, *KUTU(j * 30)] for j, s in enumerate([f"def {a[0]}_{a[1]}(ns, ctx):", f"    return {a[2]}(ns) == {a[3]}",
                                                               f"import {a[4]}; {a[5]} = {{}}"])], "en": []}
