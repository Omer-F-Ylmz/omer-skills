"""A8 (=K2) `video kuyruk yenile`: dk/başlığı "?" satırlar yt-dlp -J ile yeniden doldurulur; başarısızsa nota "meta hatası". Ağsız (sahte kos)."""
import json

from video.cli import main
from test_video import ortam  # noqa: F401 (ortam fixture)

A, B = "AAAAAAAAAAA", "BBBBBBBBBBB"
BAS = "# Kuyruk\r\nNeden? bilinmiyor\r\n\r\n| id | dk | başlık | not | durum |\r\n|---|---|---|---|---|\r\n"
TAMAM = (0, json.dumps({"duration": 125, "title": "Yeni|başlık"}).encode(), b"")
HATA = (1, b"", b"ERROR: [youtube] AAAAAAAAAAA: HTTP Error 429: Too Many Requests\n")


def yenile(tmp_path, ortam, metin, cevap):
    y = tmp_path / "kuyruk.md"
    if not y.exists():
        y.write_bytes(metin.encode("utf-8"))
    istek = []

    def kos(args, timeout=None):
        istek.append(args[-1])
        return cevap

    assert main(["kuyruk", "yenile", "--dosya", str(y)], env=ortam, kos=kos, uyku=lambda s: None) == 0
    return y.read_bytes().decode("utf-8"), istek


def test_a8_rc0_dk_baslik_dolar(tmp_path, ortam):
    out, istek = yenile(tmp_path, ortam, BAS + f"| {A} | ? | ? | n | bekliyor |\r\n", TAMAM)
    assert f"| {A} | 2.1 | Yeni/başlık | n | bekliyor |" in out and istek == [f"https://youtu.be/{A}"]


def test_a8_429_uc_kez_not_ve_soru_kalir(tmp_path, ortam):
    out, istek = yenile(tmp_path, ortam, BAS + f"| {A} | ? | ? | n | bekliyor |\r\n", HATA)
    assert len(istek) == 3  # ilk + 2 yeniden deneme (mevcut 429/403 kuralı)
    satir = next(s for s in out.splitlines() if s.startswith(f"| {A}"))
    assert satir.startswith(f"| {A} | ? | ? | n · meta hatası: ") and "HTTP Error 429" in satir


def test_a8_soru_olmayan_satira_istek_yok(tmp_path, ortam):
    out, istek = yenile(tmp_path, ortam, BAS + f"| {A} | 3.0 | Eski | | bekliyor |\r\n| {B} | 1.5 | ? | | bekliyor |\r\n", TAMAM)
    assert istek == [f"https://youtu.be/{B}"] and f"| {A} | 3.0 | Eski | | bekliyor |\r\n" in out


def test_a8_ikinci_kosuda_not_tekrarlanmaz(tmp_path, ortam):
    metin = BAS + f"| {A} | ? | ? | | bekliyor |\r\n"
    yenile(tmp_path, ortam, metin, HATA)
    out, _ = yenile(tmp_path, ortam, metin, HATA)
    assert out.count("meta hatası:") == 1


def test_a8_crlf_ve_tablo_disi_korunur(tmp_path, ortam):
    out, _ = yenile(tmp_path, ortam, BAS + f"| {A} | ? | ? | n | bekliyor |\r\nson satır\r\n", TAMAM)
    assert out == BAS + f"| {A} | 2.1 | Yeni/başlık | n | bekliyor |\r\nson satır\r\n"
