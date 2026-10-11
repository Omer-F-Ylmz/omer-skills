"""VİDEO-HIZ-2: süre ≥ ANAHTAR_SN → dhash ve kare çıkarma geçişleri yalnız anahtar kare çözer (aynı ızgara); -ss kareleri ve kısa video eski yol."""
import pytest
from test_hiz3b import _kur

from video import goz as gz

AK = ["-skip_frame", "nokey"]


def _ak(a):
    return any(a[i:i + 2] == AK for i in range(len(a)))


@pytest.mark.parametrize("esik, bayrak, uzun", [(20, "1", True), (3600, "1", False), (20, "0", False)])
def test_uzun_videoda_iki_gecis_anahtar_kare(tmp_path, monkeypatch, esik, bayrak, uzun):
    monkeypatch.setattr(gz, "ANAHTAR_SN", esik)  # _kur süre=30 sn
    if bayrak:
        monkeypatch.setenv("VIDEO_HIZ2", bayrak)
    c = _kur(tmp_path, monkeypatch, (0, b"av1\n"))
    dh, fc, ss = ([a for a, g in c if k(a, g)] for k in (lambda a, g: "rawvideo" in a, lambda a, g: g, lambda a, g: "-ss" in a))
    assert dh and fc and ss
    assert all(_ak(a) == uzun for a in dh + fc)
    assert not any(_ak(a) for a in ss)  # -ss tek kare: tam t karesi gerekir


def test_hw_dususunde_anahtar_kare_korunur(tmp_path, monkeypatch):
    monkeypatch.setattr(gz, "ANAHTAR_SN", 20)
    monkeypatch.setenv("VIDEO_HIZ2", "1")
    c = _kur(tmp_path, monkeypatch, (0, b"av1\n"), hw_hata=True)
    assert all(_ak(a) for a, g in c if "rawvideo" in a or g)


def test_melez_yalniz_dhash_anahtar_kare(tmp_path, monkeypatch):
    """VİDEO-HIZ-3 VIDEO_HIZ2=2: dhash taraması anahtar kare, kare çıkarma tam çözme (seçilen t'nin gerçek karesi)."""
    monkeypatch.setattr(gz, "ANAHTAR_SN", 20)
    monkeypatch.setenv("VIDEO_HIZ2", "2")
    c = _kur(tmp_path, monkeypatch, (0, b"av1\n"))
    dh, fc = [a for a, g in c if "rawvideo" in a], [a for a, g in c if g]
    assert dh and fc and all(map(_ak, dh)) and not any(map(_ak, fc))


def test_bayraksiz_uzun_video_melez(tmp_path, monkeypatch):
    """VİDEO-8: HIZ-7 A/B (HYMDaMcuSGQ) geri çağırma ≥ eski + rapor-denetle GEÇTİ → bayraksız ≥ ANAHTAR_SN melez (=2); VIDEO_HIZ2=0 eski yol."""
    monkeypatch.setattr(gz, "ANAHTAR_SN", 20)
    monkeypatch.delenv("VIDEO_HIZ2", raising=False)
    c = _kur(tmp_path, monkeypatch, (0, b"av1\n"))
    dh, fc = [a for a, g in c if "rawvideo" in a], [a for a, g in c if g]
    assert dh and fc and all(map(_ak, dh)) and not any(map(_ak, fc))


def test_melez_kare_cikarma_paralel_dilim(tmp_path, monkeypatch):
    """VİDEO-HIZ-4: melezde kare çıkarma dilim başına `-ss ızgara -t` süreci; select n dilime göre, numara sahne sırasıyla sürer."""
    from video import cli
    monkeypatch.setattr(gz, "ANAHTAR_SN", 20)
    monkeypatch.setattr(cli, "PARCA", 2)
    monkeypatch.setenv("VIDEO_HIZ2", "2")
    fc = sorted((a, g) for a, g in _kur(tmp_path, monkeypatch, (0, b"av1\n")) if g)
    assert len(fc) == 2 and all("-ss" in a and "-t" in a for a, _ in fc)
    d = {int(a[a.index("-start_number") + 1]): g for a, g in fc}
    assert min(d) == 1 and d[1].count("eq(n,") + 1 == max(d)  # ikinci dilim birincinin kare sayısından sonra numaralanır
    assert all("eq(n,0)" in g for _, g in fc)  # her dilim kendi ızgara başından sayar


def test_kare_sec_izgara_n_tekil():
    """VİDEO-HIZ-5: taban karesi yuvarlanınca sonraki sahneyle aynı ızgara n'ine düşer (2+5=7 → n 4 = 8.0 sn); select tek kare üretir, zip
    sonraki tüm zamanları kaydırırdı (438 sahne → 425 dosya). Tekil n, aynı karede sahne (Hamming) korunur."""
    assert gz.kare_sec([(0.0, 64), (2.0, 20), (8.0, 15)], 10, 0.5, 100) == [(0.0, 64), (2.0, 20), (8.0, 15)]


def test_ara_kare_kaydirma():
    """VİDEO-HIZ-5: anahtar-kare ızgarası (tekrarlı hash) — 0→4 çok farklı → orta n 2; 4→5 bitişik, 5→9 benzer; 9→12 farklı → n 10 (var'da ise atlanır)."""
    hs = [0, 0, 0, 0, 0xFFFF, 0xFFFF0000, 0xFFFF0000, 0xFFFF0000, 0xFFFF0000, 0xFFFF0001, 0xFFFF0001, 0xFFFF0001, 0x0F]
    assert gz.ara_kare(hs, 0.5, [0.0, 20.0]) == [(4.0, 0)]
    assert gz.ara_kare(hs, 0.5, [4.0]) == [(20.0, 0)]


def test_altyazi_hedefli_ek_kare():
    """VİDEO-HIZ-4: araç/repo/URL/komut geçen altyazı satırı → ızgara karesi; ±3 sn'de kare varsa, süre dışıysa ya da sıradan konuşmaysa yok."""
    s = [(10.2, "clone the GitHub repo"), (31.0, "npm install it"), (40.0, "hello everyone"), (61.0, "run this command"), (99.0, "open the link")]
    assert gz.altyazi_zaman(s, 90, 0.5, [0.0, 30.0, 60.0]) == [(10.0, 0)]


def test_es_kare_ardisik_esi_atlar(tmp_path):
    """VİDEO-HIZ-6: zaman sırasıyla son okunan kareyle piksel farkı < ES_ORAN olan kare OCR'sız, kaynağı eşlenir; farklı kare okunur."""
    from PIL import Image, ImageDraw
    y = {}
    for t, metin in ((0.0, "slayt bir"), (2.0, "slayt bir"), (4.0, "slayt iki baska metin"), (6.0, "slayt iki baska metin")):
        im = Image.new("L", (960, 540), 255)
        ImageDraw.Draw(im).text((100, 200), metin, fill=0, font_size=60)
        im.save(y.setdefault(t, tmp_path / f"k{int(t * 10):06d}.jpg"))
    assert gz.es_kare(list(reversed(y.items()))) == {2.0: 0.0, 6.0: 4.0}
