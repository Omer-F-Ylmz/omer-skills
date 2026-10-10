# Get 7.4 BILLION Free Tokens/Month from 35 LLMS With One API
## Künye
Get 7.4 BILLION Free Tokens/Month from 35 LLMS With One API · Coding With Abbas · süre: 12:13 · en-orig · https://youtu.be/qzPvSYVyqaw · şema 2
motor: parti 2026-10-10-short-11 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (60)
claude-sonnet-5-5: claude-sonnet-5-5 · 53728 tk · claude-haiku-5-5: claude-haiku-5-5 · 93748 tk
## Özet
Coding With Abbas, açık kaynak FreeLLMAPI aracını gösteriyor: 34 ücretsiz LLM sağlayıcısını tek OpenAI uyumlu yerel uç noktada birleştirir, otomatik yedekleme (fallback) ve hız sınırı yönetimi yapar. Video macOS uygulamasını kurar, Google AI Studio, Groq, Hugging Face ve OpenRouter anahtarlarını ekler, Playground'da dener, analitiği gösterir. Sonra `npx freellmapi setup-claude` ile Claude Code'u yapılandırır, /model slotlarını anlatır, settings.json içeriğini gösterir ve env nesnesini silerek Claude Pro aboneliğine geri döner.
## Bölümler
- 0:00 Ücretsiz LLM API'ye giriş
- 1:08 Yerel kurulum
- 2:28 Google AI Studio yapılandırması
- 5:00 Groq sağlayıcısı ekleme
- 6:03 Hugging Face entegrasyonu
- 7:08 OpenRouter bağlantısı
- 8:28 Kodlama ajanı kurulumu
- 11:04 Gelişmiş yapılandırma ve geri alma
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| FreeLLMAPI | yok | CLI | https://github.com/tashfeenahmed/freellmapi | Ücretsiz LLM sağlayıcılarını tek OpenAI uyumlu yerel uç noktada birleştiren yönlendirici | 0:00 | 34 free LLM providers... unified behind a single local endpoint |
| Claude Code | yok | CLI | yok | Anthropic'in terminal kodlama ajanı; FreeLLMAPI üzerinden yönlendirildi | 9:24 | Terminalde claude çalıştırıldı, Claude Code v2.1.282 açıldı (karede: kanıttan) Terminalde claude çalıştırıldı, Claude Code v2.1.282 açıldı |
| Google AI Studio | yok | MCP | yok | Gemini modelleri için ücretsiz API anahtarı sağlayıcısı | 2:28 | first of all let's use Google AI Studio |
| Groq | yok | MCP | yok | Groq sağlayıcısı; GPT-OSS ve Llama modelleri için anahtar | 5:00 | next provider that I will add is the Grok |
| Hugging Face | yok | MCP | yok | HuggingFace Router sağlayıcısı, erişim tokenı ile | 6:03 | let's add for Hugging Face also |
| OpenRouter | yok | MCP | yok | Ücretsiz modeller için sağlayıcı | 7:08 | For that, I will use OpenRouter |
| Docker | yok | CLI | yok | Alternatif kurulum yolu | 1:08 | you need Docker to set up that on your system |
| npx | yok | CLI | yok | setup-claude komutunu çalıştırmak için kullanıldı | 8:36 | Terminalde npx freellmapi setup-claude --url komutu (karede: kanıttan) Terminalde npx freellmapi setup-claude --url komutu |
| VS Code | yok | CLI | yok | Terminal olarak kullanılan editör | 8:28 | go back to my VS code, and simply I will paste it |
| Gemini 3.1 Flash Lite | yok | prompt | yok | Playground'da 'hi' yanıtını veren model | 4:24 | gemini-3.1-flash-lite -9838ms (karede: kanıttan) gemini-3.1-flash-lite -9838ms |
| Auto fallback | yok | teknik | yok | Limit dolunca sıradaki ücretsiz modele geçen yönlendirme | 3:29 | If one model limit is gone, it will automatically select next |
| Claude Opus 5.5 | yok | ipucu | yok | Geri dönüşte Pro abonelikle kullanılan model | 11:18 | Opus 5.5 · Claude Pro ekranda · kanıt: kare (karede: Opus 5.5 · Claude Pro ekranda) |
| Node.js | yok | teknik | yok | npx'in çalıştığı JavaScript çalışma ortamı; terminalde uyarı çıktısı görünüyor. | 8:44 | ExperimentalWarning: CommonJS module node.js is loading ES Module (karede: Terminalde Node uyarı satırları (ExperimentalWarning) görünüyor) |
| Caveman | yok | plugin | https://github.com/JuliusBrussee/caveman | settings.json'da ek plugin pazaryeri olarak tanımlı; videoda ayrıca kurulmadı. | 10:54 | "repo": "JuliusBrussee/caveman" ayar dosyasında görünüyor (karede: settings.json içinde extraKnownMarketplaces altında caveman kaydı) |
| Impeccable | yok | plugin | https://github.com/pbakaus/impeccable | settings.json'da ek plugin pazaryeri olarak tanımlı; videoda ayrıca kurulmadı. | 10:54 | "repo": "pbakaus/impeccable" ayar dosyasında görünüyor (karede: settings.json içinde extraKnownMarketplaces altında impeccable kaydı) |
| Vercel plugin | yok | plugin | yok | Claude Code'da etkin plugin (vercel@claude-plugins-official); /menüde Vercel komutları görünüyor. | 10:54 | "vercel@claude-plugins-official": true ayar dosyasında görünüyor · kanıt: kare (karede: settings.json içinde vercel@claude-plugins-official: true kaydı) |
| Playground testi | yok | prompt | yok | Playground'da modele kısa bir selam mesajı ('hi') gönderildi. | 4:31 | kaynak: altyazı |
| Claude Code bağlantı testi | yok | prompt | yok | Claude Code'a 'hi' yazıldı; auto modelle yanıt alındı. | 10:30 | kaynak: altyazı |
## Açıklama bağlantıları
- https://youtu.be/IZPGFAS_tRY — Claude Code ile OpenRouter videosu · aday: hayır · Yazarın önceki videosu, referans içerik; izleyicinin kullanacağı araç değil · sınıf: diğer
- https://github.com/tashfeenahmed/freellmapi — FreeLLMAPI GitHub deposu · aday: evet (FreeLLMAPI) · Videoda kurulan ve kullanılan araç · sınıf: diğer
- http://localhost:3001 — Yerel FreeLLMAPI paneli · aday: evet (FreeLLMAPI) · FreeLLMAPI yerel arayüzü · sınıf: diğer
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| npx freellmapi setup-claude --url http://127.0.0.1:31415 | Claude Code'u FreeLLMAPI ağ geçidine yapılandırır (karede: Terminalde npx freellmapi setup-claude --url http://127.0.0.1:31415) | 8:36 | kare |
| curl -fsSL https://freellmapi.co/install.sh / bash | Docker ile tek satırda kurulum (karede: README Quick start bölümünde curl komutu) | 1:20 | kare |
| claude | Claude Code'u başlatır (karede: Terminalde claude komutu ve güven sorusu) | 9:24 | kare |
| /model | Model/slot seçimini açar | 9:30 | altyazı |
| open -e ~/.claude/settings.json | Claude global ayarlarını metin editöründe açar (karede: Terminalde open -e ~/.claude/settings.json ve açılan settings.json) | 10:52 | kare |
| /code-review | Claude Code slash menüsünde görünüyor; videoda çalıştırılmadı. (karede: Slash komut listesinde '/code-review' satırı görünüyor) | 9:30 | kare |
| open -e [yol] (ayar dosyası yolu maskeli) | Claude Code settings.json dosyasını düzenleyicide açar; ENV bloğu silinerek normal abonelik kullanımına dönülür. (karede: Terminalde 'open −e [yol]' komutu yazılı) | 10:52 | kare |
| claude --resume ef769c9f-425a-47b5-b93d-fad6613588b0 | Belirli bir Claude Code oturumunu kimlikle sürdürür (videoda ekranda görünüyor). (karede: Terminalde 'claude —resume' ve oturum kimliği görünüyor) | 11:16 | kare |
| npx freellmapi setup-<ajan> --url http://127.0.0.1:31415 | Aider, Cline, Codex, Continue, OpenCode, Goose, Qwen, Roo gibi ajanlar için otomatik kurulum; bu videoda kullanılmadı. (karede: Agents sayfasında 'npx freellmapi setup-aider/cline/codex/...' satırları görünüyor) | 2:16 | kare |
| BASE_URL=http://127.0.0.1:31415/v1 | Elle yapılandırmada OpenAI uyumlu istemciye verilecek temel uç nokta; ajan ayarlarına yazılır. (karede: Agents sayfasında 'BASE_URL=http://127.0.0.1:31415/v1' yazılı) | 2:16 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| 34 ücretsiz sağlayıcı ve 635 model uç noktası tek yerel uç noktada birleşir | 0:00 | sayısal |
| Ayda yaklaşık 7,4 milyar ücretsiz token | 0:00 | sayısal |
| Google'dan 11 model ile 87 milyon token | 3:29 | sayısal |
| Opus/Sonnet/Haiku slotları uygun ücretsiz modele yönlendirilir; auto önerilir | 9:30 | öneri |
| Env nesnesini silmek Claude'u Pro aboneliğe geri döndürür | 11:04 | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | FreeLLMAPI | FreeLLMAPI | 7.4 billion free tokens |
| açıklama | github.com/tashfeenahmed/freellmapi | FreeLLMAPI | GitHub bağlantısı |
| açıklama | OpenRouter ile Claude Code videosu | aday değil: konu dışı | youtu.be bağlantısı |
| konuşma 2:28 | Google AI Studio | Google AI Studio | API anahtarı alındı |
| konuşma 5:00 | Groq | Groq | anahtar eklendi |
| konuşma 6:03 | Hugging Face | Hugging Face | token oluşturuldu |
| konuşma 7:08 | OpenRouter | OpenRouter | anahtar eklendi |
| konuşma 8:28 | Claude Code | Claude Code | setup-claude ile yapılandırıldı |
| kare 8:36 | npx | npx | npx freellmapi komutu |
| konuşma 1:08 | Docker | Docker | Docker seçeneği anlatıldı |
| kare 8:28 | VS Code | VS Code | terminal olarak kullanıldı |
| kare 4:24 | Gemini 3.1 Flash Lite | Gemini 3.1 Flash Lite | gemini-3.1-flash-lite yanıtı |
| konuşma 3:29 | Auto fallback | Auto fallback | otomatik yedek model seçimi |
| kare 11:18 | Opus 5.5 / Claude Pro | Claude Opus 5.5 | Opus 5.5 · Claude Pro |
| kare 8:14 | Cline, Codex CLI, Aider, Goose vb. ajan listesi | aday değil: konu dışı | Agents sayfasında yalnız listelenmiş, kurulmadı |
| kare 10:54 | caveman, impeccable, vercel eklentileri | aday değil: konu dışı | settings.json'da görünür, anlatılmadı |
| kare 0:00 | Kanal video listesi (Nest.js, Zod, Redux) | aday değil: konu dışı | kanal sayfası |
| kare 1:19 | Apple App Store bağlantısı | aday değil: konu dışı | yalnız README rozeti |
| yorum | Windows .exe ve Docker tartışması | Docker | sahip yorumu Docker önerir |
## Kareden okunanlar
- 0:34: freellmapi.co: The free LLM API. Every model. Live. 820 models, 48 providers, 7.4B
- 8:36: npx freellmapi setup-claude --url http://127.0.0.1:31415 terminalde
- 10:54: settings.json: ANTHROPIC_BASE_URL 127.0.0.1:31415, MODEL auto, slotlar auto
## Belirsizlikler
- Ekrandaki 820 model/48 sağlayıcı ile sözlü ve açıklamadaki 635/34 ve 84/820 rakamları tutarsız.
- Groq sözlü olarak 'Grok' denmiş; ekranda Groq console görünüyor.
- Sözlük eşleşmelerindeki (Three.js, Spline, D3.js vb.) öğeler videoda kullanılmadı; sadece bulanık OCR.
- settings.json'da caveman, impeccable ve vercel eklentileri görünüyor, videoda kullanılmıyor.
- Kanal sayfası kareleri (0:00) Nest.js, Zod vb. videolar konu dışı.
- Yorumlardaki 'Linux/Docker' ve Windows .exe tartışması videoda gösterilmedi.
## Atlanan segment oranı
0/18 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://youtu.be/IZPGFAS_tRY | açıklama | açıklama | hayır |
| https://github.com/tashfeenahmed/freellmapi | açıklama | açıklama | evet |
| http://localhost:3001 | 1:20 | ekran | evet |
| freellmapi.co | 0:34 | ekran | evet |
| https://freellmapi.co/install.sh | 1:20 | ekran | evet |
| https://github.com/tashfeenahmed/freellmapi/releases/latest | 1:32 | ekran | evet |
| aistudio.google.com/u/2/api-keys | 2:52 | ekran | evet |
| console.groq.com/keys | 5:00 | ekran | evet |
| huggingface.co/settings/tokens | 6:08 | ekran | evet |
| openrouter.ai/workspaces/default/keys | 6:54 | ekran | evet |
| https://apps.apple.com/app/id6804648934 | 1:19 | ekran | hayır |
| https://github.com/tashfeenahmed/freellmapi/commit/c659a4c5d15c... (OCR bozuk) | 1:00 | ekran | hayır |
| docker-entrypoint.sh | 1:04 | ekran | hayır |
| https://github.com/tashfeenahmed/freellmapi/commit/e4a47f203dba3b610dc180f628d3e821abbaf564 | 1:05 | ekran | hayır |
| play.google.com/store/apps/details?id=co.freellmapi.app | 1:10 | ekran | hayır |
| https://github.com/tashfeenahmed/freellmapi/blob/main/repo-assets/github-hero.png | 1:12 | ekran | hayır |
| https://github.com/tashfeenahmed/freellmapi/blob/main/repo-assets/desktop.png | 1:28 | ekran | hayır |
| https://ithub.com/tashfeenahmed/freelmapi/blob/main/repo-ssets/desktop.png (OCR bozuk) | 1:30 | ekran | hayır |
| github.com/tashfeenahmed/freelmapi/blob/main/repo-ssets/desktop.png (OCR bozuk) | 1:31 | ekran | hayır |
| github.com/tashfeenahmed/freellmapi/releases/tag/v0.12.0 | 1:34 | ekran | evet |
| https://github.com/tashfeenahmed/frellmapi/releases/download/v0.12.0/FreeLLMAPI-0.12.0-arm64.dmg | 1:46 | ekran | evet |
| studio.google.com | 2:28 | ses | evet |
| aistudio.google.com/u/2/prompts/new_chat | 2:46 | ekran | evet |
| console.groq.com/home | 4:56 | ekran | evet |
| console.grok.com (Groq, söylenen yazım) | 5:00 | ses | evet |
| console.grog.com/home (Groq, OCR yazımı) | 5:07 | ekran | evet |
| huggingface.co (söylenen: Face.co) | 6:03 | ses | evet |
| huggingface.co | 6:06 | ekran | evet |
| huggingface.co/settings/tokens/new?tokenType=fineGrained | 6:14 | ekran | evet |
| claude.ai | 9:26 | ekran | hayır |
| https://console.groq.com/docs/overview | açıklama | açıklama | hayır |
| https://console.groq.com/docs/legal/services-agreement | açıklama | açıklama | hayır |
| https://console.groq.com/docs/quickstart | açıklama | açıklama | hayır |
| https://console.groq.com/docs/models | açıklama | açıklama | hayır |
| https://console.groq.com/docs/api-reference | açıklama | açıklama | hayır |
| https://github.com/groq/groq-api-cookbook | açıklama | açıklama | hayır |
| https://console.groq.com/docs/rate-limits | açıklama | açıklama | hayır |
| https://console.groq.com/docs/integrations | açıklama | açıklama | hayır |
| https://console.groq.com/docs/tool-use/remote-mcp/connectors | açıklama | açıklama | hayır |
| https://huggingface.co/docs/hub/enterprise-sso | açıklama | açıklama | hayır |
| https://console.groq.com/home | açıklama | açıklama | evet |
## İş akışı
- 1. adım — FreeLLMAPI sitesi ve GitHub deposu tanıtıldı — araçlar: FreeLLMAPI, GitHub
- 2. adım — macOS .dmg uygulaması indirilip kuruldu — araçlar: FreeLLMAPI
- 3. adım — Uygulamada Models, Playground, Agents, Analytics sayfaları gezildi — araçlar: FreeLLMAPI
- 4. adım — Google AI Studio'dan API anahtarı alınıp eklendi, 11 model kaydedildi — araçlar: Google AI Studio, FreeLLMAPI
- 5. adım — Sağlık kontrolü yapıldı ve Playground'da auto modelle 'hi' denendi — araçlar: FreeLLMAPI
- 6. adım — Analytics'te istek ve token kullanımı kontrol edildi — araçlar: FreeLLMAPI
- 7. adım — Groq'ta yeni anahtar oluşturulup eklendi — araçlar: Groq, FreeLLMAPI
- 8. adım — Hugging Face'te erişim tokenı oluşturulup eklendi — araçlar: Hugging Face, FreeLLMAPI
- 9. adım — OpenRouter'da anahtar oluşturulup eklendi — araçlar: OpenRouter, FreeLLMAPI
- 10. adım — Tüm sağlayıcıların sağlığı ve toplam token bütçesi kontrol edildi — araçlar: FreeLLMAPI
- 11. adım — Agents sayfasından setup-claude komutu VS Code terminalinde çalıştırıldı — araçlar: npx, VS Code, FreeLLMAPI
- 12. adım — Unified API key yapıştırıldı, Claude Code başlatılıp auto model denendi — araçlar: Claude Code, FreeLLMAPI
- 13. adım — settings.json incelenip env nesnesi silinerek Pro aboneliğe dönüldü — araçlar: Claude Code
## Promptlar
- Playground testi — Playground'da modele kısa bir selam mesajı ('hi') gönderildi.
- Claude Code bağlantı testi — Claude Code'a 'hi' yazıldı; auto modelle yanıt alındı.
ikinci göz KAPALI: --ikinci-goz yok
