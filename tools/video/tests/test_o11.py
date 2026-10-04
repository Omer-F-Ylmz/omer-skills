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


def ham(bitler):
    """dHash'i bitler olan 9×8 gri ham: satır başına 9 piksel, bit=1 → sonraki piksel küçük."""
    out = []
    for r in range(8):
        p = [128]
        for b in bitler[r * 8:r * 8 + 8]:
            p.append(p[-1] - 1 if b else p[-1] + 1)
        out += p
    return bytes(out)


def cevir(bitler, n):
    return [1 - b if i < n else b for i, b in enumerate(bitler)]


def test_tekrar_ayiklama_metin_benzerligi_ve_ayni_sahne_dhash(ortam):
    """(3) 66/67/70/75 aynı sahne, dHash 3/7/9 → tek kare; 728/730 OCR metni ≥0.9 benzer → tek, uzun olan (730) kalır; 300/302 dHash 8 ama
    arada sahne kesimi (301.5) → ikisi kalır; kod 500/505 dHash 3 ama farklı OCR metni → ikisi kalır (metinliler hash ile birleşmez)."""
    T = [66, 67, 70, 75, 300, 302, 500, 505, 728, 730]
    d = onbellek(ortam, [], duration=1200)
    (d / "segmentler.jsonl").write_text("\n".join(json.dumps({"i": i, "bas": t, "son": t, "metin": "a"}) for i, t in enumerate(T)), encoding="utf-8")
    b = {k: [r.randint(0, 1) for _ in range(64)] for k in ("A", "B", "C", "D", "E") if (r := random.Random(k))}
    bit = {66: b["A"], 67: cevir(b["A"], 3), 70: cevir(b["A"], 7), 75: cevir(b["A"], 9), 300: b["B"], 302: cevir(b["B"], 8), 301: b["C"],
           500: b["D"], 505: cevir(b["D"], 3), 728: b["E"], 730: [1 - x for x in b["E"]]}
    uzun = okunur(728)
    uzun["tr"][2][0] += " proje"
    kos = OcrKos({"k00728": okunur(728), "k00730": uzun, "k00500": kod(500), "k00505": kod(505)}, sahne_rc=0,
                 sahne=b"frame:0    pts:301500  pts_time:301.5\nlavfi.scene_score=0.500000\n")
    kos.ham = lambda yol: ham(bit[int(Path(yol).name[1:6])])
    assert main(["paket", VID, "--kare", "10", "--istek-tavan", "0"], env=ortam, kos=kos, uyku=lambda s: None) == 0
    kj = json.loads((d / "kapsam.json").read_text(encoding="utf-8"))
    assert "seçilen 7 · OCR 3 · model 6 · incelenmedi 0" in kj["izleme"], kj["izleme"]
    md = (d / "paket.md").read_text(encoding="utf-8")
    ocr = md.split("## Ekran metni (OCR)\n")[1].split("\n## ")[0]
    assert uzun["tr"][2][0] in ocr and "[12:10]" in ocr and "[12:08]" not in ocr
    model = {int(Path(y).name[1:6]) for y in (x.split(" · ")[0] for x in md.split("## Kareler\n")[1].splitlines())}
    assert len(model & {66, 67, 70, 75}) == 1 and {300, 301, 302, 500, 505} <= model


def test_atilan_ocr_gurultu_satirlari_ocr_gurultu_txt(ortam):
    """(4) gürültü satırları pakete yazılmaz; <id>/ocr-gurultu.txt'ye "mm:ss · satır"."""
    from test_c3 import GURULTU, paket
    kos = OcrKos({"k00150": {"tr": [*okunur(150)["tr"], [GURULTU[0], *KUTU(200)], [GURULTU[1], *KUTU(240)]], "en": []}})
    d, md = paket(ortam, kos)
    assert GURULTU[0] not in md
    assert (d / "ocr-gurultu.txt").read_text(encoding="utf-8").splitlines() == [f"2:30 · {GURULTU[0]}", f"2:30 · {GURULTU[1]}"]
