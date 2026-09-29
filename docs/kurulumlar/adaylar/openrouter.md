# OpenRouter
ad: OpenRouter
tur: CLI
video: L9c49WVG_ho
repo: yok
lisans: yok
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: yok
telemetri: İstek üstverisi (zaman damgası, model, token sayıları) kaydedilir. İstem ve yanıt içerikleri varsayılan olarak kaydedilmez, kullanıcı isteğe bağlı açabilir. Upstream sağlayıcıların veri politikaları farklıdır, özellikle ücretsiz modellerde sağlayıcı istemleri eğitimde kullanabilir. Bu ifade arama sonuçlarına dayanıyor, sağlayıcıya göre doğrulanmalı.
yildiz: bilinmiyor
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-29-short)
## Ne
OpenRouter, yüzlerce yapay zeka modeline tek API anahtarı ve OpenAI uyumlu tek uç noktadan erişim sağlayan bir model yönlendirme/aggregator hizmetidir. Bazı modeller ücretsiz (:free) sunulur. Bu bir CLI ya da açık kaynak repo değil, kapalı kaynaklı bir barındırılan hizmettir. Adaydaki "CLI" etiketi yanlış görünüyor.
## Mekanizma
Hesap açılır, API anahtarı üretilir, istekler https://openrouter.ai/api/v1 adresine gönderilir. OpenRouter isteği seçilen modelin upstream sağlayıcısına yönlendirir. Sağlayıcı tercihleri, fallback ve veri politikası filtreleri ayarlanabilir. openrouter/free yönlendiricisi, ücretsiz modeller arasından istek özelliklerine (görsel, araç çağırma, yapılandırılmış çıktı) uygun olanı seçer. Bu bilgiler web aramasından alındı. Video sayfasından yalnızca başlık alınabildi, içerik alınamadı.
## Kanıt
- Ücretsiz model erişimi ve API anahtarı veren sağlayıcı → doğrulandı · OpenRouter ücretsiz modeller koleksiyonu ve openrouter/free yönlendiricisi arama sonuçlarında listeleniyor (openrouter.ai/collections/free-models). Video sayfası içeriği alınamadı, yalnızca başlık okundu: 'Yapay zeka modellerine para ödemeden ücretsiz API anahtarı almanın en kolay yolu'.
- Araç bir CLI'dır → çürütüldü · OpenRouter bir barındırılan API hizmetidir, repo bulunamadı ve aranmadı.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- openrouter.ai üzerinde hesap oluştur
- Keys sayfasından API anahtarı üret (değeri paylaşma, ortam değişkeninde tut)
- Base URL olarak https://openrouter.ai/api/v1 kullan
- Model olarak ':free' ekli bir model ya da openrouter/free seç
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Ödeme yapmadan denemek ve prototip için model erişimi sağlar, tek anahtarla birçok modeli değiştirmeyi kolaylaştırır. Ücretsiz katmanın limiti dar: günde 50 istek, 10 dolarlık kredi alınırsa 1.000, dakikada 20 istek.
## Maliyet/risk
Ücretsiz modellerde istem verisinin sağlayıcıda tutulup eğitimde kullanılması riski var, gizli kod ya da veri gönderilmemeli. Kullanım limiti düşük, ücretsiz model listesi ve kalitesi değişken. Tek bir aracıya bağımlılık oluşur. Kaynak kodu kapalı, lisans bilgisi yok.
## Tasarruf
Token tasarrufu sağlayan bir araç değil. Maliyeti düşüren yönler: ücretsiz modeller, sağlayıcı fiyatının markup'sız yansıtılması ve en ucuz sağlayıcıya yönlendirme.
## Üretilebilir
hedef_tur: yok
tarif: yok
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-29-short/panel.md → Ömer sütunu
## Özellikler
### Tek API anahtarıyla 500'den fazla modele erişim
kaynak: https://openrouter.ai/pricing
### openrouter/free: ücretsiz modeller arasından özelliğe göre otomatik seçim
kaynak: https://openrouter.ai/openrouter/free
### Sağlayıcı veri politikasına göre yönlendirme filtresi
kaynak: https://openrouter.ai/docs/faq
## Destek
- L9c49WVG_ho · 0:00 · Ücretsiz model erişimi ve API anahtarı veren sağlayıcı · kanıt: Sağlayıcı seçeneği olarak sayılıyor.
