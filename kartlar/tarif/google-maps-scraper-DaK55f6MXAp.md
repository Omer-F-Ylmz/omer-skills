# google-maps-scraper (DaK55f6MXAp)

**Amaç:** Yerel işletme verilerini (adres, telefon, e-posta, web sitesi, puan, inceleme sayısı, sosyal medya hesapları) otomatik olarak derleme.
**Araçlar:** Docker, Claude AI, Google Maps API (sıradan tarama yöntemi), Python (scraper.py)

**Adımlar**
1. [0003:00-0004:00] Docker ile araç setini yerel makinada kur ve çalıştır: `docker-compose up -d`.
2. [0003:00-0004:00] Claude AI ile entegre olarak, hedef işletme türünü (örn. 'coffee shops in Austin') belirt ve tarama işlemini başlat.
3. [0002:00-0003:00] Otomatik olarak temizlenmiş verileri (ad, telefon, e-posta, web sitesi, puan, inceleme sayısı, koordinatlar) al ve sosyal medya hesaplarını opsiyonel olarak çek.

**Prompt/kod/ayar:** Claude AI ile entegre çalışan Docker tabanlı komut: `scrape coffee shops in Austin`
**Sonuç:** Temizlenmiş yerel işletme verileri (name, phone, email, website, rating, reviews, lat/lng) + opsiyonel sosyal medya hesapları.
**Bizde (öneri, modelden):** Kurulu araçlarla Google Maps verilerini tarayarak, Claude AI ile entegre bir sistem kurarak benzer bir çözüm oluşturabilirsiniz.
**Daha iyi (öneri):** Google Maps API'yi resmi olarak kullanarak daha hızlı ve güvenilir sonuçlar elde etmek için API anahtarını entegre edebilirsiniz.
