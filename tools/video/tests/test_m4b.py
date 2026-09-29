"""MOTOR-M4b ölçüm yardımcıları (ağsız): K4 kare aralığı · koşu-2 tavan bölüşümü · kalem durumu · gürültü · kare-luna eki."""
import olcum_m3b as o3
import olcum_m4b as m


def test_k4_zamanlar():
    assert m.k4_zamanlar(0.6) == [2.5 + 5 * i for i in range(7)]  # short: 5 sn
    assert len(m.k4_zamanlar(10)) == 20                          # uzun: max(30, süre/45) = 30 sn
    z = m.k4_zamanlar(27.9)                                       # 1674 sn / 45 = 37,2 sn
    assert len(z) == 45 and abs(z[1] - z[0] - 37.2) < 1e-9


def test_tavan_bol():
    t = m.tavan_bol([(2, .10), (5, .60), (3, .30)])  # Σ 10 / $1,0 → +%20: 12 / $1,2
    assert sum(c for c, _ in t) == 12 and abs(sum(u for _, u in t) - 1.2) < 1e-6
    assert all(c >= 1 for c, _ in t) and t[1][0] == 6 and abs(t[1][1] - .72) < 1e-6


def test_durum_sinifi():
    assert m.durum_sinifi([False, False, None, False]) == "hep kaçtı"  # None = ölçülemedi, sayılmaz
    assert m.durum_sinifi([True, False, True, True]) == "bazen"
    assert m.durum_sinifi([True, True, True, None]) == "hep yakaladı"


def test_gurultu():
    fark, ort, pm = m.gurultu((9, 10), (7, 10))
    assert abs(fark - 20) < 1e-9 and abs(ort - .8) < 1e-9 and abs(pm - .1) < 1e-9


def test_luna_ekle_motor_kalemi():
    md = "# r\n\n## Teknikler\n- eski · 00:10\n"
    yeni = m.luna_ekle(md, [{"zaman": "01:05", "bilgi": "`npx foo` kurulumu", "bolum": "Kurulum/komutlar"},
                            {"zaman": "02:00", "bilgi": "Ayar paneli: tema koyu", "bolum": "Kareden bilgi"},
                            {"zaman": "03:00", "bilgi": "", "bolum": "Teknikler"}])
    k = o3.motor_kalemleri(yeni)
    assert len(k) == 3 and k[0]["metin"].startswith("eski")
    assert k[1]["zaman"] == 65 and "karede" in k[1]["metin"] and k[1]["bolum"].startswith("Kurulum/komutlar")
    assert o3.k3_duzelt(k[2], "dayanmıyor", "") == "kare-doğrulanamadı"
