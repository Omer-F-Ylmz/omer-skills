"""VİDEO-GÖZ-1b-1R: GÖZ onarımı — R1 OCR önbelleği · R2 metin süzgeci · R3 periyodik taban · R4 sıra/güvenlik/cihaz · R6 kaçan alt nedeni."""
import json
from pathlib import Path

from video import cli
from video import goz as gz


def _goz_sahte(tmp_path, monkeypatch, metin):
    """_goz sahtesi. metin: {t: [satır]} → sahneler bu zamanlar; ffmpeg istenen jpg'leri yazar; rapid okumaları sayılır."""
    d = tmp_path / "vid1"
    d.mkdir(exist_ok=True)
    zaman = sorted(metin)
    monkeypatch.setattr(cli, "_video_indir", lambda ctx, d: d / "goz-video.mp4")
    monkeypatch.setattr(gz, "sahneler", lambda h, f: [(t, 64) for t in zaman])
    monkeypatch.setattr(cli.m, "jpeg_boyut", lambda b: (1280, 720))
    sayac = {"oku": 0}

    def kos(a, timeout=None):
        if a[0] == "ffmpeg" and "rawvideo" not in a:
            for y in ([a[-1] % (i + 1) for i in range(len(zaman))] if "%" in a[-1] else [a[-1]]):
                Path(y).write_bytes(b"x")
        return 0, b"", b""

    def rapid():
        def oku(yol):
            sayac["oku"] += 1
            return [(x, 0.9, i * 30) for i, x in enumerate(metin[int(Path(yol).stem[1:]) / 10])]
        return oku
    return {"kos": kos, "rapid": rapid}, d, sayac


def test_r1_ayni_id_iki_paket_kareleri_durur_ocr_yeniden_kosmaz(tmp_path, monkeypatch):
    metin = {0.0: ["Topview dashboard shows the project settings"], 20.0: ["Cursor editor opens the terminal window"],
             40.0: ["Supabase console creates a new database"]}
    ctx, d, sayac = _goz_sahte(tmp_path, monkeypatch, metin)
    k1 = cli._goz(ctx, d, 60, "", [0.0], 2, o1 := {})
    k2 = cli._goz({"kos": ctx["kos"], "rapid": ctx["rapid"]}, d, 60, "", [40.0], 2, o2 := {})
    assert sayac["oku"] == 3  # 2. koşu OCR'ı önbellekten alır
    assert k1 != k2 and all(y.is_file() for _, y in [*k1, *k2])  # varyant başka varyantın m*.jpg'sini silmez
    assert o2["metin"] == o1["metin"] and o2["ocr_kare"] == 3
    ham = json.loads((d / "goz" / "ocr.json").read_text(encoding="utf-8"))["ham"]
    assert ham[0] == [0.0, [["Topview dashboard shows the project settings", 0.9, 0]]]  # süzülmemiş: metin · skor · y · kare t
