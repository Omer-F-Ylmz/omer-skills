# VİDEO-12: (a) açıkça kuyruklanan satırlar "## Bağlantılı videolar"dan önce; (b) ≥100 dk zaman (356:08) kapanışta h:mm:ss olur
from video import tarama as tr

KY = """| id | dk | başlık | not | durum |
|---|---|---|---|---|
| A1 | 609.2 | uzun a | VİDEO-8 yeniden | bekliyor |
| B2 | 537.1 | uzun b | VİDEO-8 yeniden | bekliyor |
| C3 | 506.6 | uzun c | VİDEO-8 yeniden | bekliyor |

## Bağlantılı videolar
| id | süre | başlık (kısa) | not | durum |
|---|---|---|---|---|
| L1 | 14.6 | bağ 1 | bağlantılı video (A1) | bekliyor |
| L2 | 18.9 | bağ 2 | bağlantılı video (A1) | bekliyor |
"""


def test_bagli_videolar_ana_listeden_sonra():
    assert [h[0] for h in tr.kuyruk_parti(KY)[1]] == ["A1", "B2", "C3"]
    assert [h[0] for h in tr.kuyruk_parti(KY, kapsiz=True)[1]] == ["A1", "B2", "C3", "L1", "L2"]


def test_yalniz_bagli_kalinca_onlar_alinir():
    k = KY.replace("| A1 | 609.2 | uzun a | VİDEO-8 yeniden | bekliyor |", "| A1 | 609.2 | uzun a | VİDEO-8 yeniden | işlendi: x |")
    assert [h[0] for h in tr.kuyruk_parti(k.replace("| bekliyor |\n| C3", "| işlendi: x |\n| C3"))[1]] == ["C3", "L1", "L2"]


def test_uc_haneli_dakika_saate_cevrilir():
    r = "## Site/UI teknikleri\r\n| teknik | ne | zaman | kaynak |\r\n|---|---|---|---|\r\n| Tuval | t | 356:08 | altyazı |\r\n| Panel | p | 1:05:46, 45:10 | kare |\r\n"
    g, n = tr.iz_duzelt(r)
    assert n == 1 and "| 5:56:08 |" in g and "| 1:05:46, 45:10 |" in g and "\r\n" in g
    assert tr.ZAMAN.search("5:56:08") and not tr.ZAMAN.search("356:08")
