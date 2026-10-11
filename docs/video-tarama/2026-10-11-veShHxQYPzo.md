# AI Engineer Summit 2023 — DAY 1 Livestream
## Künye
AI Engineer Summit 2023 — DAY 1 Livestream · AI Engineer · süre: 4:50:00 · en-orig · https://youtu.be/veShHxQYPzo · şema 2
motor: parti 2026-10-11-short-2 · claude-sonnet-5-5 · hafif claude -p
kareler: yok
kareler: girdi ≤40000 jeton için 60→0
claude-sonnet-5-5: claude-sonnet-5-5 · 115265 tk · claude-haiku-5-5: claude-haiku-5-5 · 179181 tk
## Özet
AI Engineer Summit 2023 1. gün canlı yayını (4:50:00). Açılış ve duyurular (Network uygulaması açık kaynak), swyx'in '1000x AI Engineer' konuşması, Replit'in herkese AI ve Model Farm duyurusu, Replit Code v1.5 3B'nin eğitimi, AutoGPT'nin 12 milyon dolarlık yatırımı ve Forge/benchmark araçları, OpenAI'dan GPT-4V + DALL-E 3 + Whisper demoları, Lindy ajan toplumu, AI mühendisliği anketi, AI Engineer Foundation ve Agent Protocol, Small AI, PromptHub ipuçları, Storyteller (ModelFusion), yapay zekâ ile oyun üretimi, Sourcegraph Cody kod AI seviyeleri, Wasp Mage tam yığın üretici, LangChain/LangSmith, Pydantic + Instructor ile yapılandırılmış istem, Eugene Yan'ın LLM yapı taşları, Linus Lee'nin gömme uzayı demoları ve Hex/Prefect panelini kapsar.
## Bölümler
- 0:00 Açılış ve lojistik duyurular
- 17:22 Karşılama ve konferans açılışı (Network uygulaması)
- 25:22 swyx: AI mühendisinin rolü
- 35:10 Replit: yazılım geliştirmede AI, Model Farm
- 41:55 Kod için LLM eğitimi (Replit Code v1.5)
- 1:00:33 AutoGPT ve AI ajanları
- 1:13:49 OpenAI: çok kipli modeller
- 1:33:12 Lindy: iş akışlarında ajanlar
- 1:48:52 AI mühendisliği anketi
- 1:57:47 AI Engineer Foundation
- 2:02:57 Small AI
- 2:10:31 PromptHub: istem mühendisliği
- 2:14:30 Storyteller uygulama demosu
- 2:21:46 AI ile oyun üretimi
- 2:35:37 Kod AI seviyeleri (Cody)
- 2:43:28 Mage: tam yığın uygulama üretici
- 2:53:43 Müzik arası
- 2:57:50 LangChain: bağlam ve akıl yürütme
- 3:16:52 Pydantic ile yapılandırılmış istem
- 3:35:00 LLM sistemleri için yapı taşları
- 3:52:30 Gömme uzayı (latent space) manipülasyonu
- 4:11:05 Hex ve Prefect paneli
- 4:19:30 Panel devamı ve kapanış
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Network | yok | plugin | https://github.com/ai-engineer-network | Açılış duyurusunda açık kaynak yapılan etkinlik uygulaması; LLM ile kişi eşleştirme yapıyor. | 23:32 | We are open-sourcing Network both the event app and the matching algorithm |
| Supabase | yok | CLI | yok | Network uygulamasının veritabanı ve PG Vector altyapısı. | 24:32 | superbase for database and PG Vector |
| PG Vector | yok | teknik | yok | Vektör araması için Postgres eklentisi. | 24:32 | go talk to them about PG Vector outside |
| Descope | yok | plugin | yok | Network uygulamasının kimlik doğrulama altyapı ortağı. | 24:32 | infrastructure partners descope for o |
| Replit Ghostwriter | yok | plugin | yok | Replit IDE içinde otomatik tamamlama ve sohbet sunan AI (Ghost Rider). | 37:11 | we built this product called Ghost Rider which does autocomplete chat · kanıt: yok |
| Model Farm | yok | plugin | yok | Replit IDE'de üç satır kodla model çıkarımı sağlayan servis. | 40:19 | model Farm basically gives you access to models right into your IDE |
| replit-code-v1.5-3b | yok | prompt | https://huggingface.co/replit/replit-code-v1_5-3b | Replit'in açık kaynak 3.3B parametreli kod tamamlama modeli. | 43:55 | announcing rapid code V 1.5 3B |
| The Stack | yok | teknik | yok | BigCode'un izinli lisanslı kod veri seti; Replit eğitiminin temeli. | 45:58 | we started from the stack which is an initiative led by big code |
| MosaicML | yok | CLI | https://github.com/mosaicml/llm-foundry | Replit'in H100 GPU'larda modeli eğittiği platform. | 50:01 | we have been on the Mosaic platform for a week |
| FlashAttention | yok | teknik | yok | Eğitim ve çıkarım hızı için dikkat çekirdeği (Triton çekirdeğiyle). | 55:09 | we're using flesh attention with a traton kernel |
| Grouped Query Attention | yok | teknik | yok | Çıkarım performansı için GQA. | 55:09 | we're using the latest gqa · kanıt: yok |
| TensorRT-LLM | yok | teknik | yok | NVIDIA çıkarım hızlandırma çerçevesi. | 56:09 | acceleration framework such as tensor or tlm |
| GGML | yok | teknik | yok | Apple silikonunda yerel çalıştırma için kullanılan kütüphane. | 57:11 | deployed in local say with gml which goes super fast · kanıt: yok |
| StarCoder | yok | teknik | yok | Karşılaştırma yapılan açık kod modeli. | 51:04 | we have star coder Tri which as of yesterday was the state-of-the-art |
| Code Llama | yok | teknik | yok | Replit modelinin yakın olduğu Meta kod modeli. | 52:07 | we're very close to col Lama 7B |
| HumanEval | yok | teknik | yok | Python kod üretimi benchmark'ı. | 50:01 | evaluation pel one on human eval |
| Glaive AI | yok | iş akışı | yok | Sentetik veriyle Replit modelinin instruct sürümü için işbirliği. | 58:12 | collaborations the first one is with glaive AI |
| Perplexity Labs | yok | CLI | yok | Replit modelinin barındırılacağı Labs ortamı. | 59:14 | perplexity AI guys you might have used their Labs |
| Auto-GPT | yok | iş akışı | yok | Açık kaynak otonom ajan deposu; 150.000 yıldız. | 1:04:38 | our open source repo auto gbt hit 150,000 stars on GitHub |
| AutoGPT Forge | yok | iş akışı | yok | Ajan geliştiriciler için standart şablon. | 1:06:42 | we built Forge which is a template for any agent Creator |
| Agent Protocol | yok | teknik | yok | AI Engineer Foundation'ın ajanlar için birleşik REST API şartnamesi. | 2:01:54 | Agent protocol it's a simple API spec |
| GPT-4V | yok | prompt | yok | Görsel girdili GPT-4; görsel açıklama ve karşılaştırma demosu. | 1:19:53 | use gbtv or gbt 4 with image inputs to create a description |
| DALL-E 3 | yok | prompt | yok | Açıklamadan görüntü üreten model. | 1:19:53 | put that into Dolly 3 and generate a synthetic version |
| Whisper | yok | prompt | yok | Video sesinin yazıya çevrilmesi. | 1:28:03 | asking whisper to transcribe the video |
| Lindy | yok | iş akışı | yok | Takvim, e-posta ve toplantı yöneten AI çalışan; ajan toplumu. | 1:38:17 | we build an AI employee ... we've Called It Lindy |
| Small AI | yok | CLI | yok | AI mühendisleri için API ağ geçidi; ince ayarlı küçük modeller. | 2:02:57 | small AI Tim ... API Gateway that actually helps AI Engineers |
| OpenAI fine-tuning | yok | teknik | yok | Üretim trafiğiyle küçük modele ince ayar. | 2:04:58 | screenshot of the fine tuning UI that opena has launched |
| PromptHub | yok | CLI | yok | İstem şablonları, playground ve paylaşım servisi. | 2:13:34 | we have all these available as templates in promptu |
| Multi-Persona Prompting | yok | ipucu | yok | Birden çok persona ile beyin fırtınası yaptıran istem yöntemi. | 2:10:31 | multi Persona prompting calls on various agents |
| According-to yöntemi | yok | ipucu | yok | İstemi belirli kaynağa dayandırarak halüsinasyonu azaltma. | 2:11:31 | adding according to specified Source will increase the chance · kanıt: yok |
| EmotionPrompt | yok | ipucu | yok | İstem sonuna duygusal uyarıcı ekleme. | 2:12:32 | add one of these emotional stimuli to the end |
| ModelFusion | yok | CLI | https://github.com/lgrammel/modelfusion | Storyteller'ın yazıldığı TypeScript AI orkestrasyon kütüphanesi. | 2:14:30 | typescript and model Fusion in AI orchestration library |
| Storyteller | yok | iş akışı | https://github.com/lgrammel/storyteller | Sesli giriş ile çocuk hikâyesi üreten uygulama. | 2:14:30 | Storyteller an app for generating short audio stories |
| GPT-3.5 Turbo Instruct | yok | prompt | yok | Hızlı hikâye taslağı ve başlık üretimi. | 2:16:33 | gpt3 turbo instruct which I found to be very fast |
| Stable Diffusion XL | yok | prompt | yok | Hikâye görseli üretimi (Stability AI). | 2:17:33 | stability AI stable diffusion Xcel where an image is generated · kanıt: yok |
| ElevenLabs | yok | plugin | yok | Konuşma sentezi sağlayıcısı (LMNT ile). | 2:20:35 | speech synthesis element and 11 labs are supported |
| Leonardo | yok | plugin | yok | Özel görüntü modeli eğitilen görsel üretim servisi (oyun sahneleri). | 2:26:55 | I used a tool called Leonardo ... create your own image models |
| Cody | yok | plugin | yok | Sourcegraph'ın tüm kod tabanını bilen AI kodlama asistanı. | 2:35:37 | we're building Cody the only AI coding assistant that knows your entire code base |
| Mage | yok | iş akışı | yok | GPT destekli tam yığın web uygulaması üretici. | 2:43:28 | GPT powered full stack web generator |
| Wasp | yok | CLI | yok | React, Node.js, Prisma'yı tek yapılandırmayla bağlayan çerçeve. | 2:44:29 | glued together with a full stack framework wasp |
| Fly.io | yok | CLI | yok | Wasp CLI ile tek komutla dağıtım hedefi. | 2:45:30 | CLI helper in vosp that makes it super easy to deploy to fly.io |
| LangChain | yok | iş akışı | yok | Bağlam duyarlı akıl yürütme uygulamaları için çerçeve. | 2:57:50 | Lang chain we're trying to help teams close that gap |
| LangSmith | yok | CLI | yok | Zincir ve istem hata ayıklama, değerlendirme, izleme aracı. | 3:09:22 | Lang Smith which is this thing here provides a lot of visibility |
| OpenAI Function Calling | yok | teknik | yok | Json şeması ile yapılandırılmış çıktı alma. | 3:19:52 | we get to Define Json schema of the output that we want |
| Pydantic | yok | teknik | yok | Veri doğrulama ve Json şeması üreten Python kütüphanesi. | 3:20:56 | pantic ... 70 million downloads a month |
| Instructor | yok | CLI | yok | OpenAI çağrılarını Pydantic modellerine bağlayan kütüphane. | 3:21:57 | I built a library called instructor |
| Marvin | yok | CLI | https://github.com/prefecthq/marvin | Prefect'in Pydantic tabanlı açık kaynak LLM kütüphanesi. | 3:22:58 | Marvin is a really great library to try out |
| MMLU | yok | teknik | yok | Çoktan seçmeli bilgi benchmark'ı; tutarsız değerlendirme örneği. | 3:37:04 | MML is a example that's widely used · kanıt: yok |
| SummaC (NLI) | yok | teknik | https://github.com/tingofurro/summac | Cümle düzeyinde doğal dil çıkarımıyla olgusal tutarlılık denetimi. | 3:45:11 | natural language inference task ... apply it at the sentence level · kanıt: yok |
| SelfCheckGPT | yok | teknik | yok | Çoklu örnekleme ile halüsinasyon tespiti. | 3:46:12 | here's an example from sh GPD given an input document we generate a summary multiple times |
| G-Eval | yok | teknik | https://github.com/nlpyang/geval | Güçlü LLM ile özet skorlama. | 3:46:12 | asking a strong LM ... return a summary score |
| OpenAI Moderation API | yok | teknik | yok | Üretimde güvenlik korkuluğu. | 3:44:10 | we can look at open AI moderation API |
| Midjourney | yok | ipucu | yok | Örtük geri bildirim toplama örneği (U/V/yeniden çalıştır). | 3:49:13 | mid Journey you write a prompt it suggests four images |
| GitHub Copilot | yok | plugin | yok | Kabul/ret ile örtük geri bildirim toplama örneği. | 3:49:13 | GitHub co-pilot ... you can either accept the code reject the code |
| Notion AI | yok | plugin | yok | Linus Lee'nin çalıştığı Notion'ın AI özellikleri. | 3:53:32 | it's been almost year since notion launched notion AI |
| T5 gömme/çözücü modeli | yok | teknik | yok | T5'ten ince ayarlı özel otomatik kodlayıcı; Hugging Face'te açık. | 4:07:48 | fine-tuned from T5 checkpoint with as a d using Auto encoder · kanıt: yok |
| CLIP | yok | teknik | yok | Görsel gömme uzayında interpolasyon. | 4:03:39 | using Clip Clips embedding space |
| Karlo | yok | teknik | yok | KakaoBrain'in CLIP gömmesini görüntüye çeviren unCLIP modeli. | 4:08:50 | image model that I was using at the end was caca brains Carlo |
| text-embedding-ada-002 | yok | teknik | yok | OpenAI gömme uzayından metin geri okuma. | 4:02:38 | embed this text using open ai's adaa text Ada 2 · kanıt: yok |
| Hex Magic | yok | plugin | yok | Hex veri bilimi not defterini AI ile güçlendiren özellikler (SQL explode). | 4:18:15 | make using hex feel magical · kanıt: yok |
| Prefect | yok | CLI | yok | İş akışı orkestrasyon aracı. | 4:12:08 | we're a workflow orchestration company |
| LanceDB | yok | CLI | yok | Hex'in RAG için özel kullandığı vektör veritabanı. | 4:23:33 | we ended up working with Lance DB |
| Chroma | yok | CLI | yok | Prefect'in denediği vektör veritabanı. | 4:24:33 | we've done a lot with both chroma and with Lance |
| Rivet | yok | CLI | yok | Ironclad'in deney/iterasyon için açık kaynak kütüphanesi. | 4:26:35 | rivet by Ironclad it's an open source library |
| Replit AI | yok | teknik | yok | Replit AI Chat: hata tespiti ve bağlama duyarlı kod yanıtı | 40:40 | Replit AI Chat paneli hata mesajı ve açıklama gösteriyor (karede: 'Replit AI Chat' paneli, 'Replit AI will detect issues' ve örnek JavaScript sınıfı metni) |
| MultiPL-E | yok | teknik | https://huggingface.co/spaces/bigcode/multilingual-code-evals | Çok dilli kod değerlendirme (eval) harness'i ve liderlik tablosu | 50:46 | Tablo başlıkları JavaScript, PHP, Python, Rust için MultiPL-E olarak görünüyor (karede: 'Based on multilingual-code-evals' ve sütunlar: JavaScript (MultiPL-E), PHP (MultiPL-E), Python, Rust (MultiPL-E)) |
| Apache Spark | yok | teknik | yok | Eğitim veri hattının (filtreleme, temizleme) üzerine kurulduğu dağıtık işleme motoru | 46:58 | this pipeline have been built on spark · kanıt: yok |
| Triton Inference Server | yok | teknik | yok | NVIDIA çıkarım sunucusu; düşük gecikmeli model servisi | 56:09 | usage on the Triton inference server (transkriptte Tron) · kanıt: yok |
| Kubernetes | yok | teknik | yok | Konteyner orkestrasyonu; model dağıtım süresi 18 dakikadan 2 dakikaya indirildi | 56:09 | bad luck to work with kubernetes |
| OpenAI API | yok | teknik | yok | Modellere erişim servisi; GPT, Whisper, DALL·E ve fine-tuning uç noktaları | 1:13:49 | OpenAI çok modlu sunumu ve API erişimi |
| ChatGPT | yok | teknik | https://chat.openai.com | OpenAI sohbet arayüzü; örnek konuşmalar ve günlük kullanım referansı | 1:02:34 | probably using Chachi PE (ChatGPT) to write |
| React | yok | teknik | yok | Storyteller istemci arayüzü ve Mage tarafından üretilen uygulamalarda | 2:15:30 | the client is written using react |
| Fastify | yok | teknik | yok | Storyteller sunucusu (özel uygulama, server-sent events) | 2:15:30 | the server as a custom fastify implementation |
| TypeScript | yok | teknik | yok | Storyteller uygulamasının yazıldığı dil | 2:14:30 | implemented using typescript |
| Zod | yok | teknik | yok | Yapılandırılmış çıktı şeması tanımlama kütüphanesi (ZodStructureDefinition) | 2:18:32 | Kod ekranında ZodStructureDefinition görünüyor · kanıt: kare (karede: Kod parçası: new ZodStructureDefinition({ ... }) ve 'Full audio story: OpenAI gpt-4' etiketi) |
| Prisma | yok | teknik | yok | Üretilen uygulamada veritabanı ORM'i ve veri modeli | 2:44:24 | Ekranda 'Wasp, React, Node.js and Prisma' başlığı (karede: Mage sonuç sayfası: 'Generate your full-stack web app in Wasp, React, Node.js and Prisma') |
| Tailwind CSS | yok | teknik | yok | Üretilen uygulamada CSS yardımcı sınıf çatısı | 2:44:24 | tailwind.config.cjs dosyası görünüyor (karede: Kod ağacında 'tailwind.config.cjs' dosyası) |
| Hugging Face | yok | teknik | https://huggingface.co | Model ve veri seti barındırma platformu; replit modeli burada yayınlandı | 45:58 | huging face umbrella (Hugging Face) |
| Morph | yok | plugin | https://morph.so | Yerel AI kopilotları için VS Code eklentisi; replit modeli ile proje örneği | 58:00 | morph.so ve 'VSCode extension for local copilots' metni (karede: Tweet ekranı: '@morph_labs ... Replit GPT4All ... VSCode extension for local copilots') |
| GPT4All | yok | teknik | yok | Yerel LLM çalıştırma ekosistemi; replit modeli ile kopilot projesi | 58:00 | 'The first GPT4All powered code copilot has launched' (karede: Slayt: 'The first GPT4All powered code copilot has launched') |
| agbenchmark | yok | teknik | yok | Auto-GPT ajanlarını kıyaslayan CI benchmark aracı | 1:05:16 | Ekranda agbenchmark-v0.0.10 sürüm etiketi (karede: GitHub sayfası: 'agbenchmark-v0.0.10 Latest' ve commit listesi) |
| Gmail | yok | teknik | https://mail.google.com | E-posta servisi; Lindy'nin taslak yanıt akışında kullanıldı | 1:40:24 | every morning I open my Gmail and I have all the drafts |
| Google Meet | yok | teknik | https://meet.google.com | Toplantı servisi; Lindy takvim demosunda örnek bağlantı | 1:39:24 | Ekranda meet.google.com bağlantısı · kanıt: kare (karede: E-posta taslağında 'meet.google.com/swz-hpup-rjs' bağlantısı) |
| FAISS | yok | teknik | yok | Vektör arama kütüphanesi (transkriptte 'face' olarak geçiyor) | 4:23:33 | open source tools like face and pine cone · kanıt: yok |
| Pinecone | yok | teknik | yok | Yönetilen vektör veri tabanı | 4:23:33 | open source tools like face and pine cone |
| Smol AI | yok | teknik | https://small.ai | Küçük modelleri üretim verisiyle ince ayarlayan AI geliştirici aracı (sunumdaki proje) | 2:02:57 | small AI ... an API gateway that helps AI engineers |
| GPT-4V ve DALL-E döngüsü | yok | prompt | yok | Fotoğrafı ayrıntılı tarif et; tarifi DALL-E 3'e ver, üretilen görselle orijinali karşılaştırıp farkları yazdır ve farklara göre yeni istem üret. İstem mühendisliği yok, ham çıktı. | 1:20:53 | kaynak: altyazı |
| Video özetleme | yok | prompt | yok | Video karelerini GPT-4V ile betimle, sesi Whisper ile yazıya çevir; hepsini birleştirip blog yazısı üret. | 1:28:03 | kaynak: altyazı |
| RAG'de ilgisiz bağlamı reddetme sınaması | yok | prompt | yok | Yirmi bilim kurgu film listesi verilip Twilight'ı sevip sevmeyeceği soruluyor; uygun değilse 'not applicable' dönmesi isteniyor. | 3:43:09 | kaynak: altyazı |
| Oyun sahnesi üretimi | yok | prompt | yok | Oyun sahnesini Json olarak, ince ayarlı modelle kısa istemle üret; açıklama Leonardo'ya görsel istemi olur. | 2:25:53 | kaynak: altyazı |
| Mage ile yapılacaklar uygulaması | yok | prompt | yok | Uygulama adı ve birkaç cümlelik açıklama ile yaratıcılık düzeyi (sıcaklık) girilir; Mage tam yığın uygulama üretir. | 2:43:28 | kaynak: altyazı |
| Lindy hatası örneği | yok | prompt | yok | Her sabah 9'da ilginç bir kelime ve örnek göndermesi Lindy'ye söylenir; Lindy uydurma kelimeler gönderdi. | 1:41:26 | kaynak: altyazı |
## Açıklama bağlantıları
- https://www.ai.engineer/summit/schedule — Konferans programı sayfası · aday: hayır · Program/referans sayfası; izleyicinin kullanacağı araç ya da servis değil. · sınıf: diğer
## Site/UI teknikleri
- EKSİK: formda site/UI tekniği yok (kısmi kabul)
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| wasp start | İndirilen Mage uygulamasını yerelde çalıştırır (altyazıda 'V start'). | 2:44:29 | altyazı |
| wasp deploy | Uygulamayı tek CLI komutuyla fly.io'ya dağıtır. | 2:45:30 | altyazı |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Replit tüm kullanıcılarına AI'yı varsayılan olarak açıyor. | 39:13 | özellik |
| Replit kod tamamlama P95 gecikmesi 250 ms altında tutuluyor. | 42:55 | sayısal |
| Model 128 H100 GPU ile 1 trilyon token üzerinde eğitildi, HumanEval pass@1 %36. | 50:01 | sayısal |
| Dağıtım süresi 18 dakikadan 2 dakikaya indirildi. | 56:09 | sayısal |
| Auto-GPT 150.000 yıldız, 460+ katkıcı; Redpoint 12 milyon dolar yatırım yaptı. | 1:11:50 | sayısal |
| 2024 çok kipli modeller yılı olacak. | 1:15:49 | öneri |
| Anket: 841 yanıt; yazılım mühendisleri AI mühendislerinden fazla; OpenAI en popüler. | 1:51:57 | sayısal |
| Mage uygulama başına yaklaşık 10-20 cent; yalnız GPT-4 ile 10 kat pahalı olurdu. | 2:48:36 | sayısal |
| Kod AI'da altı seviye var; 5 yılda kodun %99'u AI tarafından yazılacak (Quinn Slack tahmini). | 2:36:37 | sayısal |
| Yanıt ilgili belgenin ortasındaysa doğruluk, hiç belge olmamasından bile kötü. | 3:42:08 | karşılaştırma |
| Önce otomatik değerlendirme (30-100 örnek) kurun, mevcut bilgi erişim tekniklerini yeniden kullanın. | 3:50:14 | öneri |
| EmotionPrompt %8 ile %115 arası iyileşme sağlayabilir; according-to halüsinasyonu %20'ye kadar azaltır. | 2:12:32 | sayısal |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 17:22 | Network uygulaması | Network | Açık kaynak etkinlik uygulaması duyurusu |
| konuşma 18:22 | AutoGPT, Supabase, Fixie, Microsoft, Cloudflare sponsorları | aday değil: sponsor/reklam | Sponsor tanıtımı (Supabase ayrıca Network altyapısı) |
| konuşma 24:32 | Descope | Descope | kimlik doğrulama ortağı |
| konuşma 36:10 | ENIAC, delikli kart, LSP | aday değil: genel kavram | Tarihçe anlatımı |
| konuşma 37:11 | Ghost Rider | Replit Ghostwriter | IDE içi otomatik tamamlama ve sohbet |
| konuşma 40:19 | Model Farm | Model Farm | Üç satırda model çıkarımı |
| konuşma 40:19 | Google Cloud LLM'leri, Llama, Stable Diffusion | Model Farm | Model Farm üzerinde sunulan modeller |
| konuşma 44:56 | Chinchilla makalesi | replit-code-v1.5-3b | Token/parametre oranı gerekçesi |
| konuşma 45:58 | The Stack | The Stack | Eğitim veri seti |
| konuşma 46:58 | Spark | aday değil: başka adayın parçası (replit-code-v1.5-3b) | Veri hattı Spark üzerinde |
| konuşma 48:00 | Scaling data-constrained LMs makalesi | aday değil: başka adayın parçası (replit-code-v1.5-3b) | Veri tekrarı gerekçesi |
| konuşma 50:01 | MosaicML, H100 | MosaicML | Eğitim platformu |
| konuşma 50:01 | FlashAttention, GQA, ALiBi | FlashAttention | Mimari uygulamalar (GQA ayrı aday) |
| konuşma 51:04 | HumanEval, MultiPL-E | HumanEval | Benchmark |
| konuşma 52:07 | StarCoder, Code Llama | StarCoder | Karşılaştırma modelleri (Code Llama ayrı aday) |
| konuşma 56:09 | Triton, TensorRT-LLM, Kubernetes | TensorRT-LLM | Çıkarım ve dağıtım |
| konuşma 57:11 | GGML | GGML | Yerel çalıştırma |
| konuşma 58:12 | Glaive AI, Morph Labs, Perplexity Labs | Glaive AI | Yakın işbirlikleri (Perplexity ayrı aday) |
| kare 58:00 | GPT4All, Rift VSCode eklentisi | aday değil: konu dışı | Replit modeli üstüne topluluk projeleri slaytı; videoda anlatılmadı |
| konuşma 1:06:42 | Forge, Dev tool UI, agbenchmark | AutoGPT Forge | Ajan şablonu ve benchmark |
| konuşma 1:09:46 | OWASP prompt injection | aday değil: genel kavram | Güvenlik riski anlatımı |
| konuşma 1:11:50 | Redpoint Ventures | aday değil: konu dışı | Yatırım haberi |
| konuşma 1:16:50 | GPT-4V, DALL-E 3, Whisper | GPT-4V | Çok kipli ada modeller |
| konuşma 1:19:53 | Streamlit benzeri demo arayüzü | aday değil: konu dışı | Kare yok; ekranda 'Photo to DALL-E with GPT-V' başlığı |
| konuşma 1:38:17 | Lindy | Lindy | AI çalışan |
| konuşma 1:44:31 | Toaster project | aday değil: konu dışı | Çok ajanlı çalışma benzetmesi |
| yorum | Bölüm zaman damgaları listesi | aday değil: konu dışı | Yorumdaki içindekiler |
| yorum | Dini içerikli yorum | aday değil: konu dışı | AI hakkında inanç yorumu |
| konuşma 1:50:55 | Anket | aday değil: konu dışı | AI mühendisliği durumu anketi |
| konuşma 2:00:54 | HashiCorp Terraform / OpenTofu | aday değil: konu dışı | Lisans örneği |
| konuşma 2:01:54 | Agent Protocol | Agent Protocol | Birleşik API |
| konuşma 2:03:57 | Small AI, Candy Co logo | Small AI | API ağ geçidi |
| konuşma 2:04:58 | OpenAI fine-tuning | OpenAI fine-tuning | Fine-tune UI |
| kare 2:04:14 | Vercel AI Accelerator | aday değil: konu dışı | OCR'da geçen başlık; anlatılmadı |
| konuşma 2:10:31 | Multi-persona, according-to, EmotionPrompt | Multi-Persona Prompting | Üç istem yöntemi (diğer ikisi ayrı aday) |
| konuşma 2:13:34 | PromptHub | PromptHub | Şablon sitesi |
| konuşma 2:15:30 | React, Fastify, SSE, TypeScript | Storyteller | Mimari parçalar |
| konuşma 2:15:30 | OpenAI Whisper | Whisper | Transkripsiyon |
| konuşma 2:16:33 | GPT-3.5 Turbo Instruct | GPT-3.5 Turbo Instruct | Hızlı taslak |
| konuşma 2:17:33 | Stable Diffusion XL | Stable Diffusion XL | Görsel üretimi |
| konuşma 2:20:35 | ElevenLabs | ElevenLabs | Ses sentezi |
| konuşma 2:26:55 | Leonardo | Leonardo | Özel görüntü modeli |
| konuşma 2:35:37 | Cody, SAE seviyeleri | Cody | Kod AI seviyeleri anlatımı |
| konuşma 2:43:28 | Mage, Wasp, Prisma, Node.js | Mage | Tam yığın üretici (Wasp ayrı aday) |
| konuşma 2:53:43 | Müzik arası | aday değil: konu dışı | Şarkı sözleri |
| konuşma 2:57:50 | LangChain, LangSmith | LangChain | Bağlam ve akıl yürütme |
| konuşma 3:05:56 | Voyager makalesi, Claude, GPT-4 | aday değil: genel kavram | Yönlendirme örneklerinde anılıyor |
| konuşma 3:16:52 | Pydantic, Instructor, Marvin, function calling | Pydantic | Yapılandırılmış istem |
| konuşma 3:29:04 | RAG örnekleri, sorgu planı, bilgi grafı | Instructor | Instructor uygulamaları |
| konuşma 3:35:00 | MMLU, NLI, SelfCheckGPT, G-Eval | MMLU | Değerlendirme yöntemleri (diğerleri ayrı aday) |
| konuşma 3:44:10 | OpenAI moderation API | OpenAI Moderation API | Güvenlik korkuluğu |
| konuşma 3:49:13 | Copilot, Midjourney | GitHub Copilot | Geri bildirim örnekleri (Midjourney ayrı aday) |
| konuşma 3:53:32 | Notion AI | Notion AI | Notion özellikleri |
| konuşma 4:07:48 | T5, CLIP, Karlo, ada-002 | T5 gömme/çözücü modeli | Gömme demoları (diğerleri ayrı aday) |
| konuşma 4:06:47 | Bret Victor alıntısı, Anthropic araştırması | aday değil: konu dışı | Felsefi/araştırma referansı |
| konuşma 4:12:08 | Prefect, Hex Magic | Prefect | Panel şirketleri (Hex ayrı aday) |
| konuşma 4:23:33 | LanceDB, Chroma, FAISS, Pinecone, Rivet | LanceDB | Vektör DB ve araçlar (Chroma, Rivet ayrı aday; FAISS/Pinecone yalnız anıldı) |
| konuşma 4:48:02 | LlamaIndex, Weights & Biases, Microsoft, GitHub, Cloudflare standları | aday değil: sponsor/reklam | Kapanışta stand duyuruları |
| bağlantılı sayfa | cody.dev dokümanları, askmarvin.ai, eugeneyan.com sayfaları | aday değil: başka adayın parçası (Cody) | Yan sayfalar; Marvin ve Eugene ayrı bölümlerde |
## Kareden okunanlar
- yok
## Belirsizlikler
- Kare görseli gönderilmedi; OCR metni yalnız URL ve genel bağlam için kullanıldı, görsel doğrulama yok.
- Sözlük eşleşmelerindeki Claude Code, context7, Three.js, Hermes Agent, Kling gibi birçok öğe bulanık eşleşme, bu videoda söylenmedi/gösterilmedi; aday yapılmadı.
- 1:01:46'daki influencer e-tablosu URL'leri Auto-GPT demosunun örnek verisi; araç değil.
- Altyazı otomatik; 'rapid/rep' Replit, 'Lang Smith' LangSmith olarak düzeltildi.
- Hugging Face, Anthropic Claude ve GPT-4 anıldı ama ayrıntı verilmedi; Claude 3:04'te yalnız yönlendirme örneği.
- Kurulum komutu olarak 'wasp start' (altyazıda 'V start') ve 'wasp deploy' varsayımı.
- EKSİK: rapor (bölüm eksik: ## Site/UI teknikleri)
## Atlanan segment oranı
0/286 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://www.ai.engineer/summit/schedule | açıklama | açıklama | hayır |
| ai.engineer/network | 23:32 | ses | evet |
| github.com/ai-engineer/network | 24:32 | ses | evet |
| https://www.semianalysis.com/p/google-gemini-eats-the-world-gemini | 42:21 | ekran | hayır |
| https://www.bigcode-project.org/ | 46:02 | ekran | evet |
| https://huggingface.co/spaces/bigcode/multilingual-code-evals | 50:46 | ekran | hayır |
| https://huggingface.co/teknium | 58:00 | ekran | hayır |
| morph.so | 58:00 | ekran | hayır |
| perplexity.ai | 1:00:02 | ekran | evet |
| https://huggingface.co/replit/replit-code-v1_5-3b | 1:00:18 | ekran | evet |
| https://blog.replit.com/llm-training | 1:00:18 | ekran | hayır |
| http://famebit.com/ | 1:01:46 | ekran | hayır |
| http://stylecoalition.com/ | 1:01:46 | ekran | hayır |
| http://nmrkt.com/ | 1:01:46 | ekran | hayır |
| http://www.sociolus.com/ | 1:01:46 | ekran | hayır |
| http://www.alpharank.io/ | 1:01:46 | ekran | hayır |
| http://musefind.com/ | 1:01:46 | ekran | hayır |
| https://vidfall.com/ | 1:01:46 | ekran | hayır |
| http://www.popshorts.com/ | 1:01:46 | ekran | hayır |
| models.com | 1:15:49 | ses | hayır |
| logankilpatrick.medium.com/dont-forget-about-gpt-4-d5ab8c9493fc | 1:30:20 | ekran | hayır |
| lindy.ai | 1:33:52 | ekran | evet |
| meet.google.com/swz-hpup-rjs | 1:39:24 | ekran | hayır |
| slidesmania.com | 1:58:16 | ekran | hayır |
| cody.dev | 2:42:54 | ekran | evet |
| https://usemage.ai/result/5c67d9ec-3b41-4357-90e4-329145ace61a | 2:44:24 | ekran | evet |
| fly.io | 2:45:30 | ses | evet |
| github.com/lgrammel/storyteller | 2:21:36 | ses | evet |
| askmarvin.ai | 3:22:44 | ekran | evet |
| jxnl.github.io/instructor | 3:34:26 | ekran | evet |
| https://eugeneyan.com/writing/llm-patterns/ | 3:35:30 | ekran | hayır |
| patronus.ai/blog/evaluatin | 3:38:54 | ekran | hayır |
| https://arxiv.org/abs/2307.03172 | 3:41:38 | ekran | hayır |
| https://chat.openai.com/share/b59cfd3d-ad6c-4a85-bb64-d41ff365b9a5 | 3:43:06 | ekran | hayır |
| https://arxiv.org/abs/2111.09525 | 3:46:12 | ekran | evet |
| https://arxiv.org/abs/2303.16634 | 3:47:32 | ekran | evet |
| agentprotocol.ai | 2:01:54 | ses | evet |
## İş akışı
- yok
## Promptlar
- GPT-4V ve DALL-E döngüsü — Fotoğrafı ayrıntılı tarif et; tarifi DALL-E 3'e ver, üretilen görselle orijinali karşılaştırıp farkları yazdır ve farklara göre yeni istem üret. İstem mühendisliği yok, ham çıktı.
- Video özetleme — Video karelerini GPT-4V ile betimle, sesi Whisper ile yazıya çevir; hepsini birleştirip blog yazısı üret.
- RAG'de ilgisiz bağlamı reddetme sınaması — Yirmi bilim kurgu film listesi verilip Twilight'ı sevip sevmeyeceği soruluyor; uygun değilse 'not applicable' dönmesi isteniyor.
- Oyun sahnesi üretimi — Oyun sahnesini Json olarak, ince ayarlı modelle kısa istemle üret; açıklama Leonardo'ya görsel istemi olur.
- Mage ile yapılacaklar uygulaması — Uygulama adı ve birkaç cümlelik açıklama ile yaratıcılık düzeyi (sıcaklık) girilir; Mage tam yığın uygulama üretir.
- Lindy hatası örneği — Her sabah 9'da ilginç bir kelime ve örnek göndermesi Lindy'ye söylenir; Lindy uydurma kelimeler gönderdi.
