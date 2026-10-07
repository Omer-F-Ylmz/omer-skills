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
    sayac = {"oku": 0, "secim": []}

    def kos(a, timeout=None):
        if a[0] == "ffmpeg" and "rawvideo" not in a:
            n, s0 = sum(x.count("eq(n,") for x in a), int(a[a.index("-start_number") + 1]) if "-start_number" in a else 1
            if n:
                sayac["secim"].append(n)
            for y in ([a[-1] % (s0 + i) for i in range(n)] if "%" in a[-1] else [a[-1]]):
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


def test_r3_uzun_secim_ffmpeg_ifadesi_parcali(tmp_path, monkeypatch):
    metin = {float(t): [] for t in range(0, 1200, 10)}  # 120 kare: tek select'te ~117 eq(n,) ffmpeg "Cannot allocate memory" verdi
    ctx, d, sayac = _goz_sahte(tmp_path, monkeypatch, metin)
    cli._goz(ctx, d, 1200, "", [], 2, {})
    assert sum(sayac["secim"]) == 120 and max(sayac["secim"]) <= 50 and sayac["oku"] == 120


def test_r4_kapsam_sira():
    assert gz.kapsam_sira(8) == [0, 4, 2, 6, 1, 3, 5, 7] and sorted(gz.kapsam_sira(13)) == list(range(13)) and gz.kapsam_sira(0) == []


def test_r4_guvenlik_tavani_kayip_videoya_yayilir(tmp_path, monkeypatch):
    metin = {float(t): [f"Screen line number {t} shows the editor content"] for t in range(0, 300, 10)}
    ctx, d, sayac = _goz_sahte(tmp_path, monkeypatch, metin)
    monkeypatch.setattr(gz, "OCR_GUVENLIK", -1)  # ilk 10'luk gruptan sonra keser
    cli._goz(ctx, d, 300, "", [], 2, o := {})
    t = [x for x, _ in o["metin"]]
    assert sayac["oku"] == 10 and t == sorted(t) and min(t) == 0 and max(t) >= 250
    assert len(o["incelenmedi"]) == 20 and {n for _, n in o["incelenmedi"]} == {"OCR güvenlik tavanı"}


def test_r4_ocr_cihaz_motordan():
    def yukle():
        def oku(yol):
            return [("Topview", 0.9, 1)]
        oku.cihaz = "dml"
        return oku
    ctx = {"rapid": yukle}
    cli._ocr(ctx, ["C:/x/k1.jpg"])
    assert ctx["ocr_cihaz"] == "dml"


def test_r6_kacan_alt_nedeni():
    e = "ekranda-var-OCR-kaçırdı"
    altin = {"adaylar": [{"ad": a, "zaman": z, "kaynak": "ekran"} for a, z in
                         [("Kestrelapp", "0:05"), ("Falconkit", "0:05"), ("Gannetdb", "0:05"), ("Heronjs", "0:20"), ("Ibisapi", "1:40")]]}
    ham = [[0.0, [["Kestrelapp opens", 0.9, 0], ["~Falconkit", 0.9, 1], ["Gannetdb", 0.3, 2]]], [22.0, [["unrelated text", 0.9, 0]]]]
    kacan = [(a["ad"], e) for a in altin["adaylar"]] + [("Jaybird", "ASR-bozdu")]
    assert au.kacan_alt(kacan, altin, ham, lambda x: x.startswith("~")) == [
        ("Kestrelapp", f"{e}/bütçe-attı"), ("Falconkit", f"{e}/gürültü-süzgeci"), ("Gannetdb", f"{e}/düşük-güven"),
        ("Heronjs", f"{e}/OCR-okuyamadı"), ("Ibisapi", f"{e}/örnekleme-boşluğu"), ("Jaybird", "ASR-bozdu")]
