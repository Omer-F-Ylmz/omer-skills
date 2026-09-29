# Groq
ad: Groq
tur: CLI
video: L9c49WVG_ho
repo: yok
lisans: yok
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: yok
telemetri: Bilinmiyor/istemci tarafı yok: kendi CLI'ı olmayan bir bulut API'sidir. İstekler (prompt ve çıktı) Groq sunucularına gönderilir; gizlilik/veri saklama politikası bu incelemede doğrulanmadı.
yildiz: bilinmiyor
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-29-short)
## Ne
Groq, açık ağırlıklı modelleri (Llama, GPT-OSS, Kimi, DeepSeek) kendi LPU çiplerinde çok hızlı çıkarım yapan, OpenAI uyumlu bir bulut LLM API sağlayıcısıdır. Aday bir araç/repo değil, barındırılan bir hizmettir. Videoda yalnızca ücretsiz katman sunan sağlayıcı seçeneklerinden biri olarak geçiyor (ASR'de "Grock"). "CLI" türü uygun değil; gerçek tür: ticari API hizmeti.
## Mekanizma
İstemci, https://api.groq.com/openai/v1 adresine GROQ_API_KEY ile Bearer yetkilendirmeli OpenAI uyumlu istek (chat/responses) gönderir. Model Groq'un LPU donanımında çalışır ve yanıt döner. Bir OpenAI SDK'sında base_url değiştirmek yeterlidir. Ayrıca Batch API, uzak MCP bağlayıcıları (Google Workspace) ve Compound AI sistemleri var.
## Kanıt
- Groq ücretsiz katman sunuyor → doğrulandı · Web araması: kredi kartsız ücretsiz katman, kurumsal düzeyde 30 RPM / 6.000 TPM / 14.400 günlük istek (üçüncü taraf bloglar). Resmi rate-limits sayfası doğrudan okunmadı.
- OpenAI uyumlu API → doğrulandı · console.groq.com/docs/overview: base URL https://api.groq.com/openai/v1 ve OpenAI SDK örneği.
- Bir CLI aracıdır → çürütüldü · Dokümanlarda API/SDK var; aday bir repo/CLI değil, barındırılan hizmet.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- console.groq.com üzerinden hesap açıp API anahtarı oluştur (anahtar değerini paylaşma)
- export GROQ_API_KEY=<anahtar>
- OpenAI SDK'sında base_url='https://api.groq.com/openai/v1' ver ve model olarak örn. openai/gpt-oss-20b kullan
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Ücretsiz veya ucuz ve hızlı çıkarım sağlar. Yardımcı/ucuz model çağrıları, hızlı ön işleme, hafif alt görevler ve kredi kartsız denemeler için kullanılabilir.
## Maliyet/risk
Ücretsiz katman sıkı sınırlı (yaklaşık 30 RPM, 6.000 TPM, 14.400 istek/gün; üçüncü taraf kaynaklara göre, limitler değişebilir). Sınırlar organizasyon düzeyindedir ve aşılınca HTTP 429 döner. Veri üçüncü tarafa gider. Kendi modeli yok, açık modeller sunuyor. Lisans/repo yok, satıcıya bağımlılık var.
## Tasarruf
Token tasarrufu aracı değil. Maliyet düşürücü unsurlar: ücretsiz katman, Batch API'de yarı fiyat, Developer katmanında %25 indirim. Bunlar üçüncü taraf kaynaklara dayanıyor.
## Üretilebilir
hedef_tur: CLI
tarif: Ucuz alt görevler için ince bir 'groq-ask' CLI/skill: GROQ_API_KEY ortam değişkenini okur, https://api.groq.com/openai/v1/chat/completions adresine model (örn. openai/gpt-oss-20b) ve prompt gönderir, çıktıyı stdout'a yazar. 429 durumunda geri çekilip tekrar dener. Anahtar koda gömülmez.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-29-short/panel.md → Ömer sütunu
## Özellikler
### OpenAI uyumlu API (chat/responses), base_url değişimiyle geçiş
kaynak: https://console.groq.com/docs/overview
### Google Workspace (Gmail, Takvim, Drive) uzak MCP bağlayıcıları
kaynak: https://console.groq.com/docs/tool-use/remote-mcp/connectors
### Ücretsiz katman ve rate limitleri
kaynak: https://console.groq.com/docs/rate-limits
### Batch API (yarı fiyat, asenkron)
kaynak: https://www.cloudzero.com/blog/groq-pricing/
## Destek
- L9c49WVG_ho · 0:00 · Ücretsiz katman sunan sağlayıcı (ASR "Grock") · kanıt: Sağlayıcı seçeneği olarak sayılıyor.
