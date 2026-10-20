ÖMER'E 1 SATIR: kartsız kalıcı ücretsiz olup henüz açılmamış hesaplar → Mistral (console.mistral.ai) · Cloudflare Workers AI (dash.cloudflare.com) · NVIDIA build (build.nvidia.com) · SambaNova (cloud.sambanova.ai); anahtarı MISTRAL_API_KEY / CLOUDFLARE_API_KEY(+CLOUDFLARE_ACCOUNT_ID) / NVIDIA_API_KEY / SAMBANOVA_API_KEY adıyla kullanıcı ortamına koy (havuza ben eklerim).

Kaynak: okuyucu alt ajanı, resmi belgeler, 20 Eki 2026; "doğrulanamadı" yazanlar kanıtsız. Türkçe sütunu ölçüm değil TAHMİN. Hesabı Ömer açar.

| Sağlayıcı | Ücretsiz sınır | Kart | Türkçe | Kayıt | Env | OpenAI uyumlu uç |
|---|---|---|---|---|---|---|
| Mistral (Free/Experiment) | org düzeyi RPS/dk-jeton/ay; rakam belgede yok (Studio > Limits) | hayır (telefon doğrulanamadı) | iyi (tahmin) | console.mistral.ai/api-keys | MISTRAL_API_KEY | api.mistral.ai/v1 |
| Cloudflare Workers AI | 10.000 Neuron/gün, 00:00 UTC sıfırlanır; metin ~300 RPM | hayır gibi (doğrulanamadı) | orta (tahmin) | dash.cloudflare.com/profile/api-tokens | CLOUDFLARE_API_KEY + CLOUDFLARE_ACCOUNT_ID | api.cloudflare.com/client/v4/accounts/{ID}/ai/v1 |
| NVIDIA build | ~40 RPM (resmi sayfa sayı vermiyor), prototip amaçlı | hayır | orta (tahmin) | build.nvidia.com | NVIDIA_API_KEY | integrate.api.nvidia.com/v1 |
| SambaNova Cloud | model başına 20 RPM · 20 RPD · 200K jeton/gün; preview modeller kalkabilir | hayır | orta/iyi (tahmin) | cloud.sambanova.ai/apis | SAMBANOVA_API_KEY | api.sambanova.ai/v1 |
| Ollama Cloud | "başlangıç" kullanımı, aylık sıfırlanır, aynı anda 1 istek; sayı yok | doğrulanamadı | orta (tahmin) | ollama.com/settings/keys | OLLAMA_API_KEY | ollama.com/v1 |
| Cohere trial | 1.000 çağrı/ay, chat 20 RPM; ticari kullanım YASAK | doğrulanamadı | iyi (tahmin) | dashboard.cohere.com/api-keys | COHERE_API_KEY | api.cohere.ai/compatibility/v1 |

Kalıcı ücretsiz DEĞİL / kapalı (hesap açmaya değmez):
- Cerebras: $5 deneme kredisi 30 gün, kart gerekir (5 RPM · 1M jeton/gün).
- Hugging Face Inference Providers: ücretsiz kullanıcıya aylık kredi yok.
- GitHub Models: 30 Tem 2026'dan beri "fully retired" (docs.github.com). Ölçüm uyumlu: models.github.ai her yola 200 + gövde "OK" döndürüyor → havuzda KAPALI (ENT'te türler boş).

Zaten bağlı ve canlı (20 Eki ölçüm, bkz. envanter.tsv): Groq (gpt-oss-120b/20b, qwen3.8-27b) · OpenRouter :free (hesapta kredi var; model başına günlük tavan ağır) · Gemini (3.1-flash-lite çalışıyor; diğer flash modelleri bugün kota dolu, 2.5 serisi 404) · OmniRoute cc-ucuz-free (OpenRouter'a bağlı, onunla birlikte düşer).
HAVUZ-2 canlı durum (20 Eki 18:00): Cloudflare 200 (havuzda, Türkçe iyi) · Mistral 429 hız sınırı (havuzda, soğumayla yeniden dener) · Ollama anahtar var ama "Free usage limit" 429 (havuzda, 4 sa soğuma) · NVIDIA anahtar var, katalog bayat: llama-3.3 410, mistral-large/nemotron-70b 404, gemma-4/deepseek zaman aşımı (KAPALI) · SambaNova 402 PAYMENT_METHOD_REQUIRED, ücretsiz bakiye yok (KAPALI).
Anahtarsız uç: Pollinations alınmadı — kullanım koşulu sayfası (pollinations.ai/terms) betikle okunamadı (JS), koşul doğrulanmadan eklenmez; ayrıca istemler üçüncü tarafta açık kalabilir, mem-yedek oturum içeriği taşır → eklenmez.
