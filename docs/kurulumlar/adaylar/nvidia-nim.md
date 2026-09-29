# Nvidia NIM
ad: Nvidia NIM
tur: CLI
video: L9c49WVG_ho
repo: yok
lisans: bilinmiyor
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: yok
telemetri: Bilinmiyor. Barındırılan servis olduğundan istekler ve istem içerikleri NVIDIA sunucularına gidiyor. Gizlilik koşulları bu araştırmada incelenmedi.
yildiz: bilinmiyor
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-29-short)
## Ne
NVIDIA'nın build.nvidia.com üzerinden sunduğu barındırılan model kataloğu (NIM = NVIDIA Inference Microservices). 100+ modeli (DeepSeek, Llama, Qwen, Mistral, Nemotron) OpenAI uyumlu API ile sunuyor. CLI ya da açık kaynak araç değil, bulut API sağlayıcısı; "CLI" etiketi yanlış sınıflandırma.
## Mekanizma
Ücretsiz NVIDIA Developer Program hesabıyla API anahtarı alınıyor. İstekler OpenAI uyumlu uç noktaya (https://integrate.api.nvidia.com/v1) gidiyor; mevcut OpenAI SDK'ları ve araçları yalnızca base URL ve anahtar değişimiyle çalışıyor. Aynı NIM konteynerleri kendi GPU'nda da çalıştırılabiliyor (geliştirme için ücretsiz, üretimde AI Enterprise lisansı gerekli). Videoda yalnızca ücretsiz model API'si veren sağlayıcı seçeneği olarak sayılıyor; ayrıntı yok, video sayfasından metin alınamadı.
## Kanıt
- Ücretsiz model API'si sunan sağlayıcı → doğrulandı · Web aramasında birden çok kaynak build.nvidia.com'un Developer Program ile kartsız ücretsiz API anahtarı, 100+ model ve OpenAI uyumlu uç nokta sunduğunu belirtiyor. Video sayfasından yalnızca başlık alındı (ücretsiz API anahtarı almanın en kolay yolu), içerik alınamadı.
- Ücretsiz katman limitsiz/sorunsuz kullanılabilir → çürütüldü · Kaynaklar yaklaşık 40 RPM sınırı bildiriyor. NVIDIA forumuna göre limitler modele göre değişiyor ve yayımlanmıyor.
- Nvidia NIM bir CLI aracıdır → çürütüldü · Bulut API kataloğu ve konteyner tabanlı çıkarım mikroservisi. Repo ve CLI bulunamadı.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- build.nvidia.com'da hesap aç (NVIDIA Developer Program'a otomatik katılım, kart gerekmiyor)
- Bir model sayfasından API anahtarı oluştur (değeri gizli tut, ortam değişkeninde sakla)
- İstemcide base URL'yi https://integrate.api.nvidia.com/v1 yap, model adını katalogdan seç
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Prototipleme, yan projeler ve ajan denemeleri için ücretsiz, OpenAI uyumlu ve geniş model seçimi sunuyor. Yedek sağlayıcı olarak da işe yarıyor.
## Maliyet/risk
Ücretsiz katman prototip içindir. Limitler belirsiz ve değişebiliyor, kredi sistemi kaldırılmış olabilir. Prompt verisi üçüncü tarafa gidiyor. Üretim SLA'sı yok. Kendi GPU'da üretim kullanımı için pahalı kurumsal lisans (kaynaklara göre GPU başına yaklaşık 4.500 $/yıl) gerekiyor. Bu rakamlar ikincil kaynaklardan, doğrulanmadı.
## Tasarruf
Token aracısı değil. Tasarruf, ücretsiz katmanla API maliyetini sıfırlamaktan geliyor. Kaynaklara göre limit yaklaşık 40 istek/dk, 200 RPM için başvuru yapılabiliyor. Limitler modele göre değişiyor ve resmî olarak yayımlanmıyor.
## Üretilebilir
hedef_tur: skill
tarif: NIM'i kopyalamak mümkün değil, ama onu kullanan bir skill yazılabilir. Skill; NVIDIA_API_KEY ortam değişkenini okuyup integrate.api.nvidia.com/v1'e OpenAI uyumlu istek atar. Ucuz veya toplu görevleri (özetleme, sınıflandırma) ücretsiz modele yönlendirir. 429 gelirse geri çekilip yeniden dener, 40 RPM üstüne çıkmaz. Anahtar dosyaya yazılmaz.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-29-short/panel.md → Ömer sütunu
## Özellikler
### OpenAI uyumlu uç nokta (integrate.api.nvidia.com/v1)
kaynak: https://freellm.net/providers/nvidia-nim
### Kartsız ücretsiz API anahtarı, 100+ model, yaklaşık 40 RPM
kaynak: https://yangmao.ai/en/providers/nvidia-build/
### Aynı NIM konteynerleri kendi GPU'nda çalıştırılabilir (geliştirmede ücretsiz)
kaynak: https://aihola.com/article/nvidia-nim-free-api-models
## Destek
- L9c49WVG_ho · 0:00 · Ücretsiz model API'si sunan sağlayıcı · kanıt: Sağlayıcı seçeneği olarak sayılıyor.
