"""MOTOR-M3b: altın set ölçüm betiğinin saf parçaları (ağ yok)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import olcum_m3b as o  # noqa: E402

ALTIN = """# Altın set — X (uzun, 1:00) · "b" · k

Özet (kalem): ...

## Kaynaklar
- .kos/altin/X/kaynak.txt

## Araç/servis/ürün (2)
1. RTK (rtk-ai/rtk) · CLI proxy · 00:30 altyazı "trims output" · yüksek
2. Headroom · istek proxy'si · 05:03 altyazı "compresses" · orta

## Açıklama bağlantıları (1)
1. https://github.com/rtk-ai/rtk · 00:30 açıklama · düşük

## Kurulum/komutlar (1)
1. `rtk init -g` · 02:01 kare · yüksek

## Kareden bilgi (1)
1. Headroom Get started ekranı · 05:34 kare [tekil]

## Emin olunmayanlar (1)
1. belki bir şey · 01:00 altyazı · orta
"""

RAPOR = """# X · başlık

## Künye
- süre 1:00

## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| rtk | - | CLI | https://github.com/rtk-ai/rtk/ | çıktıyı kırpar | 00:31 | altyazı |
| Ponytail | - | skill | - | az kod | 10:37 | altyazı |

## Açıklama bağlantıları
- https://www.github.com/rtk-ai/rtk?tab=readme

## Belirsizlikler
- hiçbir şey
"""


def test_altin_oku_kategori_onem_ve_emin_olunmayan_disarida():
    k = o.altin_oku(ALTIN)
    assert [(x["kat"], x["onem"]) for x in k] == [
        ("Araç/servis/ürün", "yüksek"), ("Araç/servis/ürün", "orta"), ("Açıklama bağlantıları", "düşük"),
        ("Kurulum/komutlar", "yüksek"), ("Kareden bilgi", None)]
    assert k[0]["ad"] == "RTK (rtk-ai/rtk)" and k[0]["zaman"] == 30 and k[4]["zaman"] == 334


def test_motor_kalemleri_tablo_ve_madde_kunye_belirsizlik_disarida():
    m = o.motor_kalemleri(RAPOR)
    assert [(x["bolum"], x["ad"]) for x in m] == [
        ("Adaylar", "rtk"), ("Adaylar", "Ponytail"), ("Açıklama bağlantıları", "https://www.github.com/rtk-ai/rtk?tab=readme")]
    assert m[0]["zaman"] == 31


def test_det_esle_ad_repo_url_komut():
    a, m = o.altin_oku(ALTIN), o.motor_kalemleri(RAPOR)
    e = o.det_esle(a, m)
    assert e[0] == 0            # RTK ↔ rtk (ad + repo)
    assert e[2] in (0, 2)       # URL normalize (şema/www/sorgu/son /)
    assert 1 not in e           # Headroom motor çıktısında yok
    assert o.url_norm("HTTPS://www.GitHub.com/a/b/?x=1#y") == "github.com/a/b"
    assert "rtkinitg" in o.anahtarlar("kur: `rtk init -g`", "x")


def test_metrik_ve_olcut():
    a = o.altin_oku(ALTIN)
    m = o.metrik(a, {0, 2})
    assert m["yuksek"] == (1, 2) and m["genel"] == (2, 5)
    assert o.olcut(m, dayanmayan=(0, 10)) == {"yuksek": False, "genel": False, "dayanmayan": True}
    assert o.olcut({"yuksek": (9, 10), "genel": (3, 4)}, dayanmayan=(1, 20)) == {"yuksek": True, "genel": True, "dayanmayan": True}


def test_sebep_siniflama():
    a = o.altin_oku(ALTIN)
    paket = "## Açıklama bağlantıları\n- https://github.com/rtk-ai/rtk\n## Segmentler\n[0:00] a\n[1:00] b\n"
    assert o.sebep(a[3], paket) == "b"           # Kurulum/komutlar formda yok
    assert o.sebep(a[1], paket) == "a"           # 05:03 segmenti pakette yok
    assert o.sebep(a[0], paket) == "c"           # 00:30 pakette var → model atladı
    assert o.sebep(a[4], paket) == "a"           # kare: 05:34 civarı kare yok


def test_jev_tavani_oncelik_sirasi():
    k2, k3, kalan = o.jev_sinirla(list(range(250)), {"sonnet": list(range(40)), "luna": list(range(30))}, 300)
    assert len(k2) == 250 and len(k3["sonnet"]) == 40 and len(k3["luna"]) == 10 and kalan == {"sonnet": 0, "luna": 20}


def test_or_cagir_429_iki_tekrar_sonra_olculemedi_ve_usage():
    istek, uyku = [], []

    def gonder(url, govde, bas):
        istek.append(govde)
        return 429, {}
    y = o.or_cagir("q/free", {}, gonder, uyku.append)("sis", "metin", {"type": "object"})
    assert len(istek) == 3 and len(uyku) == 2 and y["form"] is None and "ölçülemedi" in y["hata"]

    def iyi(url, govde, bas):
        return 200, {"choices": [{"message": {"content": 'ön söz {"videolar": []} son'}}],
                     "usage": {"prompt_tokens": 10, "completion_tokens": 5, "cost": 0.002}}
    y = o.or_cagir("q/free", {}, iyi, uyku.append)("sis", "metin", {"type": "object"})
    assert y["form"] == {"videolar": []} and y["usd"] == 0.002 and y["usage"] == {"input_tokens": 10, "output_tokens": 5}


def test_secim_bicimleri():
    assert o.secim({"choice": "2"}) == "2"
    assert o.secim({"choice": {"0": 0.1, "3": 0.8}}) == "3"
    assert o.secim(None) == "0"


def test_k3_duzelt_url_girdide_ve_kare():
    paket = "## Açıklama bağlantıları\n- https://x.com/nateherk\n"
    assert o.k3_duzelt({"bolum": "Açıklama bağlantıları", "metin": "https://x.com/nateherk/ X"}, "dayanmıyor", paket) == "dayanıyor"
    assert o.k3_duzelt({"bolum": "Site/UI teknikleri", "metin": "başlık (karede: 'Have')"}, "dayanmıyor", paket) == "kare-doğrulanamadı"
    assert o.k3_duzelt({"bolum": "İddialar", "metin": "23 öğe"}, "dayanmıyor", paket) == "dayanmıyor"
    assert o.k3_duzelt({"bolum": "İddialar", "metin": "https://y.com"}, "dayanıyor", paket) == "dayanıyor"
