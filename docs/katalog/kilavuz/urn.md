# urn — 20 benzersiz kayıt

**Amaç:** Ürün, pazarlama ve iş ajanları: fiyatlandırma, A/B istatistiği, içerik/mesaj stratejisi, CRM ve martech, ücretli reklam, kriz iletişimi, finans planı, ürün yönetimi.

**İç yapı:** Tümü [ajan], urn-<konu>; gruplar: ölçüm (ab-test, kullanici-davranisi, icerik-performans), metin (baslik, eposta, marka-sesi, mesaj), reklam, satış/CRM, iş/finans.

## En güçlü parçalar
- `urn-ab-test-istatistik` — Örneklem büyüklüğü, MDE, peeking kontrolü ve sample ratio kontrolüyle A/B.
- `urn-kullanici-davranisi` — Huni, kohort, olaylarla kullanıcının neden düştüğünü/dönüştüğünü açıklar.
- `urn-mesaj-mimarisi` — Değer önerisi, sütunlar, kanıt noktaları ve kitle varyantlarıyla mesaj hiyerarşisi.
- `urn-musteri-saglik-skoru` — Kullanım, destek, fatura sinyallerinden SaaS churn için sağlık skoru.
- `urn-finans-plani` — Gelir sürücüleri, maliyet, nakit pisti ve senaryolarla startup planı.
- `urn-kriz-iletisimi` — Holding statement, paydaş sırası, güncelleme ritmi.
- `urn-is-analizi` — İş ihtiyacını süreç haritası, gereksinim ve kabul ölçütüne çevirir.
- `urn-baslik-yazimi` — Çok gösterim az tık durumunda dürüst vaatli başlık.

## Birlikte kullanım
- urn-marka-sesi → urn-mesaj-mimarisi → urn-eposta-metni / urn-sosyal-medya-icerik.
- urn-crm + urn-martech-yigini + urn-musteri-saglik-skoru: satış ve tutundurma verisi.
- urn-google-ads-arama + urn-sosyal-reklam, ai-marketing-hub-claude-ads ile platform operasyonu.

## Tuzaklar
- marketingskills ve ai-marketing-hub-claude-ads ile fiyatlandırma, A/B, reklam konuları çakışır.
- urn-fiyatlandirma ile marketingskills:pricing benzer; seçim ölçütü katalog metninde belirtilmemiş.
- Reklam hesabı/platform erişimi katalog metninde belirtilmemiş.

## Üyeler
- ajan (20): urn-ab-test-istatistik, urn-baslik-yazimi, urn-crm, urn-eposta-metni, urn-finans-plani, urn-fiyatlandirma, urn-google-ads-arama, urn-grafik-tasarim, urn-icerik-performans, urn-icerik-stratejisi, urn-is-analizi, urn-kriz-iletisimi, urn-kullanici-davranisi, urn-marka-sesi, urn-martech-yigini, urn-mesaj-mimarisi, urn-musteri-saglik-skoru, urn-sosyal-medya-icerik, urn-sosyal-reklam, urn-urun-yoneticisi
