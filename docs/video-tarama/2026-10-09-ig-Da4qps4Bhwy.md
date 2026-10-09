# API (Application Programming Interface), uygulamaların birbirleriyle güvenli şek
## Künye
API (Application Programming Interface), uygulamaların birbirleriyle güvenli şek · onurhuseyinkocak.ai · süre: 1:13 · ? · https://www.instagram.com/reel/Da4qps4Bhwy/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-09-short-32 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 18839 tk · claude-haiku-5-5: claude-haiku-5-5 · 49739 tk
## Özet
Video, Claude Code veya Codex kullanan kişilerin API anahtarlarını GitHub'a sızdırmış olabileceğini anlatıyor. GitHub kod aramasında düzenli ifadeyle herkese açık repolardaki sızmış anahtarlar gösteriliyor. Kendi reponu kontrol etmek için TruffleHog reposunun linkini kopyalayıp Claude'a veya Codex'e kurdurup çalıştırtma öneriliyor. Açıklamada ayrıca Gitleaks, ortam değişkenleri ve anahtar yenileme gibi korunma önerileri var.
## Bölümler
- 0:00 Giriş: API anahtarları GitHub'a sızmış olabilir
- 0:17 GitHub kod aramasında sızmış anahtarları gösterme
- 0:51 TruffleHog reposu ve linkin kopyalanması
- 1:05 Yorumlara API yaz çağrısı
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| TruffleHog | yok | CLI | https://github.com/trufflesecurity/trufflehog | Repolarda sızmış API anahtarı ve gizli bilgileri tarayan açık kaynak araç; repo linki Claude'a veya Codex'e verilip kurdurulur. | 0:54 | Ekranda trufflesecurity/trufflehog GitHub reposu, Code düğmesi ve URL kopyalama görünüyor. (karede: kanıttan) Ekranda trufflesecurity/trufflehog GitHub reposu, Code düğmesi ve URL kopyalama görünüyor. |
| Gitleaks | yok | CLI | yok | Repolardaki sızan anahtarları ücretsiz tarayan araç; açıklamada öneriliyor. | açıklama | Açıklamada TruffleHog veya Gitleaks ile ücretsiz tarama önerisi geçiyor. |
| Claude Code | yok | CLI | yok | Yapay zekâ kod aracı; hem anahtar sızdırma riski olarak hem de TruffleHog'u kurup çalıştırma aracı olarak anılıyor. | 0:00 | Cloud Code veya Codex kullanıyorsan sana kötü bir haberin var. |
| Codex | yok | CLI | yok | Yapay zekâ kod aracı; TruffleHog'u kurdurmak için alternatif olarak anılıyor. | 1:00 | Altyazıda Codex'e verme ifadesi görünüyor; konuşmada da anılıyor. (karede: kanıttan) Altyazıda Codex'e verme ifadesi görünüyor; konuşmada da anılıyor. |
| Cursor | yok | CLI | yok | Anahtar sızdırma riski olan AI kod araçları arasında açıklamada anılıyor. | açıklama | Açıklamada Claude Code, Codex, Cursor kullananlar uyarılıyor. |
| GitHub | yok | iş akışı | yok | Kod araması ile herkese açık repolardaki sızmış anahtarlar gösteriliyor. | 0:21 | github.com/search?q=... adresi ve Code search results sekmesi görünüyor. (karede: kanıttan) github.com/search?q=... adresi ve Code search results sekmesi görünüyor. |
| GitHub kod araması regex | yok | teknik | yok | sk- ile başlayan anahtarları bulan düzenli ifade (regex) araması. | 0:36 | Arama URL'sinde sk-[a-zA-Z0-9]{10,50} desenine benzeyen kodlanmış sorgu görünüyor. · kanıt: kare (karede: Arama URL'sinde sk-[a-zA-Z0-9]{10,50} desenine benzeyen kodlanmış sorgu görünüyor.) |
| Kimi | yok | teknik | yok | Sızmış anahtar örneği olarak gösterilen model servisi. | 0:26 | Mesela Kimi için var, Kugan için var. |
| GPT Image 2 | yok | teknik | yok | Sızmış anahtarı bulunan model örneği olarak anılıyor. | 0:00 | Mesela GPT Image 2 için bir tane var. |
| Qwen | yok | teknik | yok | Sızmış anahtar sonuçlarında görünen model. | 0:28 | OCR'da Qwen anahtar satırı ve model-name2 Qwen3.6 görünüyor. (karede: kanıttan) OCR'da Qwen anahtar satırı ve model-name2 Qwen3.6 görünüyor. |
| GLM | yok | teknik | yok | Sızmış yapılandırmada seçili LLM olarak görünen model. | 0:04 | OCR'da selected_llm: GLM satırı var. (karede: kanıttan) OCR'da selected_llm: GLM satırı var. |
| OpenAI API | yok | teknik | yok | OPENAI_API_KEY satırı sızmış sonuçlarda görünüyor. | 0:45 | Karede OPENAI_API_KEY ve OPENAI_BASE_URL satırları görünüyor. (karede: kanıttan) Karede OPENAI_API_KEY ve OPENAI_BASE_URL satırları görünüyor. |
| Environment variable | yok | teknik | yok | Anahtarları kodun dışında tutmak için önerilen yöntem. | açıklama | Açıklamada environment variable ve secret kullan deniyor. |
| Kendi reponda API anahtarı sızıntısını taramak | yok | prompt | yok | TruffleHog GitHub reposunun linkini Claude'a veya Codex'e verip bunu kur ve çalıştır demek; başka bir şey gerekmiyor. | 1:00 | kaynak: altyazı |
## Açıklama bağlantıları
- yok
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| curl https://your-domain.com/v1/models | Örnek bir LLM sağlayıcısının model listesini çekmek için kullanılan yer tutucu bir istek; sızan kod örneğinin parçası. (karede: OCR: sızıntı örneğinde 'curl https://your-domain.com/v1/models' satırı görünüyor (kare tam olarak okunamadı)) | 0:42 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| 8000'den fazla API anahtarı şu anda GitHub'da açıkta. | 0:26 | sayısal |
| Sızan anahtarlar çoğu zaman dakikalar içinde botlar tarafından bulunuyor. | açıklama | sayısal |
| TruffleHog repolardaki sızıntıları ücretsiz tarar. | açıklama | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Claude Code | Claude Code | Cloud Code veya Codex kullanıyorsan |
| konuşma 0:00 | Codex | Codex | Cloud Code veya Codex kullanıyorsan |
| konuşma 0:00 | Cargo Cult Programming | aday değil: genel kavram | Cargo Cult Programming denen şeyi yapıyorsan |
| konuşma 0:00 | GitHub | GitHub | API'ların GitHub'a sızmış olabilir |
| konuşma 0:00 | GPT Image 2 | GPT Image 2 | Mesela GPT Image 2 için bir tane var |
| konuşma 0:00 | Kimi | Kimi | Mesela Kimi için var |
| kare 0:04 | GLM selected_llm | GLM | OCR: selected_llm GLM |
| kare 0:04 | packyapi.com | aday değil: konu dışı | OCR: baseUrl packyapi.com, sızmış örnek içerik |
| kare 0:21 | GitHub kod araması | GitHub kod araması regex | github.com/search?q= adresi |
| kare 0:28 | Qwen | Qwen | OCR: Qwen anahtar satırı |
| kare 0:42 | DeepSeek | aday değil: konu dışı | Sızmış sonuç içeriğinde geçen metin, anlatılmıyor |
| kare 0:42 | LiteLLM | aday değil: konu dışı | Sızmış sonuç içeriğinde LITELLM_API_KEY satırı |
| kare 0:45 | OPENAI_API_KEY | OpenAI API | Karede OPENAI_API_KEY satırı |
| kare 0:45 | siliconflow adresi | aday değil: konu dışı | Sızmış sonuç içeriğinde API adresi |
| kare 0:51 | .claude/skills ve .codex/skills | aday değil: başka adayın parçası (TruffleHog) | TruffleHog repo dosya listesinde klasörler görünüyor |
| kare 0:57 | GitHub Desktop, GitHub CLI, Copilot app menüsü | aday değil: konu dışı | Code menüsünde yalnız seçenek olarak görünüyor |
| konuşma 0:54 | TruffleHog | TruffleHog | Kendi reponda sızıntı kontrolü için Tufflehawk |
| konuşma 1:00 | Claude ve Codex'e kurdurma | Claude Code | bunu Cloud'a ya da Codex'e vereceksin |
| açıklama | Cursor | Cursor | Claude Code, Codex, Cursor veya benzeri AI kod araçları |
| açıklama | Gitleaks | Gitleaks | TruffleHog veya Gitleaks ile repolarını ücretsiz tara |
| açıklama | Environment variable | Environment variable | Environment variable ve secret kullan |
| açıklama | Hashtag'ler | aday değil: konu dışı | #VibeCoding #ClaudeCode #Codex #GitHub #cybersecurity |
| linkli sayfa trufflehog.org | trufflesecurity.com | TruffleHog | Bağlantılı sayfa TruffleHog'un resmi sitesine yönleniyor |
| yorum | Yorumlar | aday değil: konu dışı | Yorumlar girişsiz alınamadı |
## Kareden okunanlar
- 0:17: GitHub ana sayfası: Home, Ask anything, Trending repositories, team-reflect/reflect-open ve 1c7/chinese-independent-developer.
- 0:45: GitHub kod arama sonuçları; OPENAI_API_KEY satırları, siliconflow adresi ve altyazıda 'API key'lerinize dikkat edeceksiniz'.
- 0:57: trufflesecurity/trufflehog reposu, Code menüsü HTTPS URL, GitHub CLI, Download ZIP ve altyazıda 'Şuradan linkini kopyalayacaksın'.
## Belirsizlikler
- Yorumlar girişsiz alınamadığı için içerikleri bilinmiyor.
- Konuşma metni 'Tufflehawk' ve 'Cloud' yazıyor; bunlar TruffleHog ve Claude olarak yorumlandı.
- Kurulum komutu gösterilmedi; araç yalnızca AI'a kurdurularak kullanılıyor.
- 'Cargo Cult Programming' genel kavram olduğu için aday yapılmadı.
- Ekranda görünen anahtar değerleri bilerek yazılmadı.
- Altyazıdaki 'Kugan' yazımı belirsiz, muhtemelen başka bir model adı.
## Atlanan segment oranı
0/2 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://github.com/trufflesecurity/trufflehog | 0:54 | ekran | evet |
| https://trufflehog.org | açıklama | açıklama | evet |
| https://trufflesecurity.com | 0:57 | ekran | evet |
| github.com/search | 0:21 | ekran | evet |
| https://www.packyapi.com | 0:05 | ekran | hayır |
| https://your-domain.com/v1/models | 0:43 | ekran | hayır |
| https://1.api.aithing.net/ | 0:45 | ekran | hayır |
| https://api.siliconflow.cn/v1/chat/completions | 0:45 | ekran | hayır |
| https://ai.xingyungent.cn/v1 | 0:45 | ekran | hayır |
| https://ww.packyapi.com | 0:04 | ekran | hayır |
| https://github.com | 0:17 | ekran | evet |
| https://your-domain.com/v1/models_\ | 0:42 | ekran | hayır |
| https://www.packyani.com (OCR, packyapi olabilir) | 0:47 | ekran | hayır |
| https://github.com/trufflesecurity/trufflehog (OCR: trufflesecurityftrufflehog) | 0:54 | ekran | evet |
| https://github.com/trufflesecurity/trufflehog (OCR bozuk: tzuffl) | 0:57 | ekran | evet |
| https://github.com/trufflesecurity/trufflehog (OCR bozuk: truffl) | 0:58 | ekran | evet |
| https://github.com/trufflesecurity | 1:00 | ekran | hayır |
| https://github.com/trufflesecurity/trufflehog (OCR bozuk: tru) | 1:01 | ekran | evet |
| https://github.com/trufflesecurity/trufflehog (OCR bozuk: trufflesecus) | 1:03 | ekran | evet |
## İş akışı
- 1. adım — Sohbet ve uyarı: API anahtarı sızıntısının riski anlatılır — araçlar: yok
- 2. adım — GitHub ana sayfasına gidilir — araçlar: GitHub
- 3. adım — GitHub kod aramasında sk- kalıbıyla API anahtarı arama sonuçları gösterilir — araçlar: GitHub
- 4. adım — Sızan anahtarların bulunduğu dosyalar ve depolar incelenir (değerler gösterilmez) — araçlar: GitHub
- 5. adım — TruffleHog GitHub reposu açılır — araçlar: GitHub, TruffleHog
- 6. adım — Clone menüsünden HTTPS bağlantısı kopyalanır — araçlar: GitHub
- 7. adım — Bağlantı Claude Code ya da Codex'e verilir — araçlar: Claude Code, Codex
- 8. adım — AI araçtan TruffleHog'u kurup çalıştırması istenir — araçlar: Claude Code, Codex, TruffleHog
- 9. adım — Açıklamada çeşitli koruma adımları sıralanır (istemci tarafına koymama, env variable, commit kontrolü, yenileme) — araçlar: yok
- 10. adım — Açıklamada TruffleHog veya Gitleaks ile ücretsiz tarama önerilir — araçlar: TruffleHog, Gitleaks
- 11. adım — Yorumlara API yazılarak repo bağlantısı istenir — araçlar: Instagram yorumları
## Promptlar
- Kendi reponda API anahtarı sızıntısını taramak — TruffleHog GitHub reposunun linkini Claude'a veya Codex'e verip bunu kur ve çalıştır demek; başka bir şey gerekmiyor.
ikinci göz KAPALI: --ikinci-goz yok
