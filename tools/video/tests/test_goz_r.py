"""VİDEO-GÖZ-1b-1R: GÖZ onarımı — R1 OCR önbelleği · R2 metin süzgeci · R3 periyodik taban · R4 sıra/güvenlik/cihaz · R6 kaçan alt nedeni."""
import json
from pathlib import Path

from video import altin as au
from video import cli
from video import goz as gz


def _goz_sahte(tmp_path, monkeypatch, metin):
    """_goz sahtesi. metin: {t: [satır]} → sahneler bu zamanlar; ffmpeg select sayısı kadar jpg yazar; rapid okumaları sayılır."""
    d = tmp_path / "vid1"
    d.mkdir(exist_ok=True)
    monkeypatch.setattr(cli, "_video_indir", lambda ctx, d: d / "goz-video.mp4")
    monkeypatch.setattr(gz, "sahneler", lambda h, f: [(t, 64) for t in sorted(metin)])
    monkeypatch.setattr(cli.m, "jpeg_boyut", lambda b: (1280, 720))
    sayac = {"oku": 0}

    def kos(a, timeout=None):
        if a[0] == "ffmpeg" and "rawvideo" not in a:
            n = sum(x.count("eq(n,") for x in a)
            for y in ([a[-1] % (i + 1) for i in range(n)] if "%" in a[-1] else [a[-1]]):
                Path(y).write_bytes(b"x")
        return 0, b"", b""

    def rapid():
        def oku(yol):
            sayac["oku"] += 1
            return [(x, 0.9, i * 30) for i, x in enumerate(metin.get(int(Path(yol).stem[1:]) / 10, []))]
        return oku
    return {"kos": kos, "rapid": rapid}, d, sayac


def test_r1_ayni_id_iki_paket_kareleri_durur_ocr_yeniden_kosmaz(tmp_path, monkeypatch):
    metin = {0.0: ["Topview dashboard shows the project settings"], 10.0: ["Cursor editor opens the terminal window"],
             20.0: ["Supabase console creates a new database"]}
    ctx, d, sayac = _goz_sahte(tmp_path, monkeypatch, metin)
    k1 = cli._goz(ctx, d, 30, "", [0.0], 2, o1 := {})
    k2 = cli._goz({"kos": ctx["kos"], "rapid": ctx["rapid"]}, d, 30, "", [20.0], 2, o2 := {})
    assert sayac["oku"] == 3  # 2. koşu OCR'ı önbellekten alır
    assert k1 != k2 and all(y.is_file() for _, y in [*k1, *k2])  # varyant başka varyantın m*.jpg'sini silmez
    assert o2["metin"] == o1["metin"] and o2["ocr_kare"] == 3
    ham = json.loads((d / "goz" / "ocr.json").read_text(encoding="utf-8"))["ham"]
    assert ham[0] == [0.0, [["Topview dashboard shows the project settings", 0.9, 0]]]  # süzülmemiş: metin · skor · y · kare t


def test_r2_tek_satir_degisen_kare_metne_girer(tmp_path, monkeypatch):
    ortak = [f"Settings panel row {i} describes the workspace option" for i in range(8)]
    metin = {0.0: ortak, 10.0: [*ortak, "Kestrelapp integration enabled for this project"]}  # değişim < 0.15
    ctx, d, _ = _goz_sahte(tmp_path, monkeypatch, metin)
    cli._goz(ctx, d, 20, "", [], 1, o := {})
    assert "Kestrelapp integration enabled for this project" in str(gz.ekran_metni(o["metin"], ""))


def test_r3_tavan_ve_periyodik_taban():
    assert (gz.tavan_ocr(60), gz.tavan_ocr(600), gz.tavan_ocr(1800), gz.tavan_ocr(3600)) == (40, 80, 200, 200)
    assert gz.kare_sec([(0, 64)], 31, 1, 40) == [(0, 64), (10, 0), (20, 0), (30, 0)]  # sahne yok: her 10 sn
    sahne = [(float(i), 30) for i in range(50)]  # 30 dk sabit ekran + ilk 50 sn'de 50 sahne
    k = gz.kare_sec(sahne, 1800, 1, gz.tavan_ocr(1800))
    t = [x for x, _ in k]
    assert len(k) <= 200 and all(s in k for s in sahne) and t == sorted(t)  # tavan içinde, sahneler korunur
    assert max(b - a for a, b in zip(t, t[1:])) <= 15 and t[-1] >= 1780  # aralık 15'e büyür, taban videoya yayılır
